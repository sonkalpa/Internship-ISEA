#!/usr/bin/env python3
"""WSL-friendly Assignment 4 runner using Mininet LinuxBridge when available."""

import csv
import json
import os
import shlex
import shutil
import subprocess
import time
from pathlib import Path

from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.nodelib import LinuxBridge


def _ovs_available() -> bool:
    try:
        result = subprocess.run(
            ["ovs-vsctl", "show"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=2,
        )
        return result.returncode == 0
    except Exception:
        return False


def _linuxbridge_available() -> bool:
    return shutil.which("brctl") is not None


def _is_wsl() -> bool:
    try:
        release = os.uname().release.lower()
    except Exception:
        return False
    return "microsoft" in release or "wsl" in release


def choose_switch():
    forced = os.environ.get("A4_SWITCH", "").strip().lower()

    if forced == "ovs" and _ovs_available():
        return OVSBridge, "OVSBridge (forced)"
    if forced == "linuxbridge" and _linuxbridge_available():
        return LinuxBridge, "LinuxBridge (forced)"
    if forced == "loopback":
        return None, "Loopback fallback (forced)"

    if _is_wsl() and _linuxbridge_available():
        return LinuxBridge, "LinuxBridge (WSL default)"
    if _ovs_available():
        return OVSBridge, "OVSBridge"
    if _linuxbridge_available():
        return LinuxBridge, "LinuxBridge (fallback)"
    return None, "Loopback fallback (no switch backend)"


def write_system_details(path: Path) -> None:
    commands = [
        ["uname", "-a"],
        ["python3", "--version"],
        ["ip", "addr"],
    ]

    with path.open("w", encoding="utf-8") as f:
        for cmd in commands:
            f.write(f"# {' '.join(cmd)}\n")
            completed = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            f.write(completed.stdout)
            f.write("\n")


def run_mininet_flow(script_dir: Path) -> None:
    logs_dir = script_dir / "logs"
    tmp_dir = script_dir / "tmp_perf"
    logs_dir.mkdir(exist_ok=True)
    tmp_dir.mkdir(exist_ok=True)

    chat_log = script_dir / "chat_log.txt"
    event_log = script_dir / "server_events.log"
    perf_csv = script_dir / "performance_results.csv"
    capture_file = script_dir / "capture.pcapng"
    details_file = script_dir / "system_details.txt"
    run_info_file = script_dir / "run_info.txt"

    chat_log.write_text("", encoding="utf-8")
    event_log.write_text("", encoding="utf-8")

    for path in tmp_dir.glob("*.json"):
        path.unlink(missing_ok=True)

    write_system_details(details_file)

    switch_cls, switch_label = choose_switch()

    if switch_cls is None:
        raise RuntimeError(
            "No usable Mininet switch backend found. Set A4_SWITCH if needed."
        )

    setLogLevel("warning")

    net = Mininet(controller=None, switch=switch_cls, build=False)
    h1 = net.addHost("h1", ip="10.0.0.1/8")
    h2 = net.addHost("h2", ip="10.0.0.2/8")
    h3 = net.addHost("h3", ip="10.0.0.3/8")
    h4 = net.addHost("h4", ip="10.0.0.4/8")
    s1 = net.addSwitch("s1")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    rows = []

    net.start()
    ping_loss = net.pingAll()

    with run_info_file.open("w", encoding="utf-8") as f:
        f.write(f"SWITCH_BACKEND={switch_label}\n")
        f.write("TOPOLOGY=h1--s1--{h2,h3,h4}\n")
        f.write(f"PINGALL_LOSS_PERCENT={ping_loss}\n")

    hosts = [h2, h3, h4]
    usernames = ["ClientA", "ClientB", "ClientC"]

    try:
        for clients in (1, 2, 3):
            h1.cmd('pkill -f "python3 server.py" >/dev/null 2>&1 || true')

            server_log = logs_dir / f"server_{clients}.out.txt"
            server_cmd = (
                f"cd {shlex.quote(str(script_dir))} && "
                f"python3 server.py --host 10.0.0.1 --port 5000 "
                f"--chat-log {shlex.quote(str(chat_log))} "
                f"--event-log {shlex.quote(str(event_log))}"
            )
            server_proc = h1.popen(server_cmd, shell=True, stdout=server_log.open("w"), stderr=subprocess.STDOUT)

            time.sleep(1.0)

            cap_proc = None
            if clients == 3 and shutil.which("dumpcap") is not None:
                capture_file.unlink(missing_ok=True)
                cap_proc = subprocess.Popen(
                    [
                        "dumpcap",
                        "-i",
                        "any",
                        "-f",
                        "tcp port 5000",
                        "-a",
                        "duration:25",
                        "-w",
                        str(capture_file),
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                time.sleep(1.0)

            client_procs = []
            summary_files = []
            start_ts = time.time()

            for i in range(clients):
                summary = tmp_dir / f"summary_{clients}_{i+1}.json"
                summary_files.append(summary)
                client_log = logs_dir / f"client_{clients}_{i+1}.out.txt"

                client_cmd = (
                    f"cd {shlex.quote(str(script_dir))} && "
                    f"python3 client.py --host 10.0.0.1 --port 5000 "
                    f"--username {shlex.quote(usernames[i])} "
                    f"--auto-count 20 --auto-delay 0.03 "
                    f"--summary-file {shlex.quote(str(summary))}"
                )
                proc = hosts[i].popen(
                    client_cmd,
                    shell=True,
                    stdout=client_log.open("w"),
                    stderr=subprocess.STDOUT,
                )
                client_procs.append(proc)

            for proc in client_procs:
                proc.wait(timeout=120)

            duration = max(time.time() - start_ts, 0.001)

            if cap_proc is not None:
                try:
                    cap_proc.wait(timeout=40)
                except subprocess.TimeoutExpired:
                    cap_proc.terminate()
                    cap_proc.wait(timeout=5)

            h1.cmd('pkill -f "python3 server.py" >/dev/null 2>&1 || true')
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.terminate()

            avg_samples = []
            for summary in summary_files:
                data = json.loads(summary.read_text(encoding="utf-8"))
                avg_samples.append(float(data.get("avg_delivery_time_ms", 0.0)))

            total_messages = clients * 20
            avg_delivery = sum(avg_samples) / len(avg_samples) if avg_samples else 0.0
            throughput = total_messages / duration

            rows.append(
                {
                    "clients": clients,
                    "total_messages": total_messages,
                    "avg_delivery_time_ms": round(avg_delivery, 3),
                    "throughput_msgs_per_sec": round(throughput, 3),
                }
            )

            time.sleep(1.0)
    finally:
        net.stop()

    with perf_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "clients",
                "total_messages",
                "avg_delivery_time_ms",
                "throughput_msgs_per_sec",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row["clients"],
                    row["total_messages"],
                    row["avg_delivery_time_ms"],
                    row["throughput_msgs_per_sec"],
                ]
            )


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    run_mininet_flow(script_dir)
    print("Generated Assignment 4 artifacts:")
    print("- chat_log.txt")
    print("- server_events.log")
    print("- performance_results.csv")
    print("- system_details.txt")
    print("- run_info.txt")
    print("- capture.pcapng (if dumpcap available)")


if __name__ == "__main__":
    main()
