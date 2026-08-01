#!/usr/bin/env python3
"""WSL-friendly Assignment 5 runner with Mininet automation."""

from __future__ import annotations

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


def _is_wsl() -> bool:
    try:
        return "microsoft" in os.uname().release.lower() or "wsl" in os.uname().release.lower()
    except Exception:
        return False


def _ovs_available() -> bool:
    try:
        res = subprocess.run(
            ["ovs-vsctl", "show"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=2,
        )
        return res.returncode == 0
    except Exception:
        return False


def _linuxbridge_available() -> bool:
    return shutil.which("brctl") is not None


def choose_switch():
    forced = os.environ.get("A5_SWITCH", "").strip().lower()

    if forced == "ovs" and _ovs_available():
        return OVSBridge, "OVSBridge (forced)"
    if forced == "linuxbridge" and _linuxbridge_available():
        return LinuxBridge, "LinuxBridge (forced)"
    if _is_wsl() and _linuxbridge_available():
        return LinuxBridge, "LinuxBridge (WSL default)"
    if _ovs_available():
        return OVSBridge, "OVSBridge"
    if _linuxbridge_available():
        return LinuxBridge, "LinuxBridge"
    raise RuntimeError("No usable Mininet switch backend found")


def write_system_details(path: Path) -> None:
    commands = [["uname", "-a"], ["python3", "--version"], ["ip", "addr"]]
    with path.open("w", encoding="utf-8") as f:
        for cmd in commands:
            f.write(f"# {' '.join(cmd)}\n")
            out = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            f.write(out.stdout)
            f.write("\n")


def run() -> None:
    root = Path(__file__).resolve().parent
    logs = root / "logs"
    tmp = root / "tmp_perf"
    logs.mkdir(exist_ok=True)
    tmp.mkdir(exist_ok=True)

    history = root / "chat_history.csv"
    perf = root / "performance_results.csv"
    events = root / "server_events.log"
    stats = root / "server_stats.txt"
    state = root / "client_state.csv"
    run_info = root / "run_info.txt"
    details = root / "system_details.txt"
    capture = root / "capture.pcapng"

    write_system_details(details)

    for p in [history, perf, events, stats, state, capture]:
        p.unlink(missing_ok=True)
    for p in tmp.glob("*.json"):
        p.unlink(missing_ok=True)

    setLogLevel("warning")
    switch_cls, switch_label = choose_switch()

    net = Mininet(controller=None, switch=switch_cls, build=False)
    h1 = net.addHost("h1", ip="10.0.0.1/8")
    h2 = net.addHost("h2", ip="10.0.0.2/8")
    h3 = net.addHost("h3", ip="10.0.0.3/8")
    h4 = net.addHost("h4", ip="10.0.0.4/8")
    h5 = net.addHost("h5", ip="10.0.0.5/8")
    s1 = net.addSwitch("s1")
    for h in (h1, h2, h3, h4, h5):
        net.addLink(h, s1)

    rows: list[dict[str, float | int]] = []

    net.start()
    ping_loss = net.pingAll()
    run_info.write_text(
        f"SWITCH_BACKEND={switch_label}\n"
        "TOPOLOGY=h1--s1--{h2,h3,h4,h5}\n"
        f"PINGALL_LOSS_PERCENT={ping_loss}\n",
        encoding="utf-8",
    )

    server_log_file = logs / "server_output.txt"
    server_cmd = (
        f"cd {shlex.quote(str(root))} && "
        f"python3 -u server.py --host 10.0.0.1 --port 5000 "
        f"--history-file {shlex.quote(str(history))} "
        f"--event-file {shlex.quote(str(events))} "
        f"--stats-file {shlex.quote(str(stats))} "
        f"--state-file {shlex.quote(str(state))}"
    )

    with server_log_file.open("w", encoding="utf-8") as sf:
        server_proc = h1.popen(server_cmd, shell=True, stdout=sf, stderr=subprocess.STDOUT)
        time.sleep(1.5)

        hosts = [h2, h3, h4, h5]
        usernames = ["ClientA", "ClientB", "ClientC", "ClientD"]

        for client_count in (2, 3, 4):
            active_hosts = hosts[:client_count]
            active_users = usernames[:client_count]

            cap_proc = None
            if client_count == 4 and shutil.which("dumpcap") is not None:
                cap_proc = subprocess.Popen(
                    [
                        "dumpcap",
                        "-i",
                        "any",
                        "-f",
                        "tcp port 5000",
                        "-a",
                        "duration:30",
                        "-w",
                        str(capture),
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                time.sleep(1.0)

            start_ts = time.time()
            procs = []
            summary_paths = []

            for host, uname in zip(active_hosts, active_users):
                targets = [u for u in active_users if u != uname]
                targets_arg = ",".join(targets)
                summary_path = tmp / f"summary_{client_count}_{uname}.json"
                summary_paths.append(summary_path)
                log_path = logs / f"client_{client_count}_{uname}.txt"

                cmd = (
                    f"cd {shlex.quote(str(root))} && "
                    f"python3 client.py --host 10.0.0.1 --port 5000 "
                    f"--username {shlex.quote(uname)} --auto-count 50 --auto-delay 0.02 "
                    f"--private-every 5 --targets {shlex.quote(targets_arg)} "
                    f"--summary-file {shlex.quote(str(summary_path))}"
                )

                with log_path.open("w", encoding="utf-8") as lf:
                    p = host.popen(cmd, shell=True, stdout=lf, stderr=subprocess.STDOUT)
                procs.append(p)

            for p in procs:
                p.wait(timeout=180)

            duration = max(time.time() - start_ts, 0.001)

            if cap_proc is not None:
                try:
                    cap_proc.wait(timeout=40)
                except subprocess.TimeoutExpired:
                    cap_proc.terminate()

            data = [json.loads(sp.read_text(encoding="utf-8")) for sp in summary_paths]
            total_messages = sum(int(d["sent_messages"]) for d in data)
            total_broadcast = sum(int(d["broadcast_sent"]) for d in data)
            total_private = sum(int(d["private_sent"]) for d in data)

            total_matches = sum(int(d["received_matches"]) for d in data)
            if total_matches > 0:
                weighted_delay = sum(float(d["avg_delay_ms"]) * int(d["received_matches"]) for d in data)
                avg_delay_ms = weighted_delay / total_matches
            else:
                avg_delay_ms = 0.0

            throughput = total_messages / duration

            rows.append(
                {
                    "clients": client_count,
                    "broadcast_messages": total_broadcast,
                    "private_messages": total_private,
                    "avg_delay_ms": round(avg_delay_ms, 3),
                    "throughput_msgs_per_sec": round(throughput, 3),
                }
            )

            time.sleep(1.0)

        h1.cmd('pkill -f "python3 server.py" >/dev/null 2>&1 || true')
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.terminate()

    net.stop()

    with perf.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "clients",
                "broadcast_messages",
                "private_messages",
                "avg_delay_ms",
                "throughput_msgs_per_sec",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print("Generated Assignment 5 artifacts:")
    print("- chat_history.csv")
    print("- performance_results.csv")
    print("- server_events.log")
    print("- server_stats.txt")
    print("- client_state.csv")
    print("- capture.pcapng")


if __name__ == "__main__":
    run()
