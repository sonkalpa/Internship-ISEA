#!/usr/bin/env python3
"""Run Assignment 6 backend simulation and capture artifacts in WSL."""

from __future__ import annotations

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
    if _is_wsl() and _linuxbridge_available():
        return LinuxBridge, "LinuxBridge (WSL default)"
    if _ovs_available():
        return OVSBridge, "OVSBridge"
    if _linuxbridge_available():
        return LinuxBridge, "LinuxBridge"
    raise RuntimeError("No usable Mininet switch backend found")


def write_system_details(path: Path) -> None:
    cmds = [["uname", "-a"], ["python3", "--version"], ["ip", "addr"]]
    with path.open("w", encoding="utf-8") as f:
        for cmd in cmds:
            f.write(f"# {' '.join(cmd)}\n")
            out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
            f.write(out.stdout)
            f.write("\n")


def run() -> None:
    root = Path(__file__).resolve().parent
    logs = root / "logs"
    logs.mkdir(exist_ok=True)

    capture = root / "capture.pcapng"
    history = root / "chat_history.csv"
    events = root / "server_events.log"
    details = root / "system_details.txt"
    run_info = root / "run_info.txt"

    write_system_details(details)
    for p in [capture, history, events]:
        p.unlink(missing_ok=True)

    setLogLevel("warning")
    switch_cls, switch_name = choose_switch()

    net = Mininet(controller=None, switch=switch_cls, build=False)
    h1 = net.addHost("h1", ip="10.0.0.1/8")
    h2 = net.addHost("h2", ip="10.0.0.2/8")
    h3 = net.addHost("h3", ip="10.0.0.3/8")
    h4 = net.addHost("h4", ip="10.0.0.4/8")
    h5 = net.addHost("h5", ip="10.0.0.5/8")
    s1 = net.addSwitch("s1")
    for h in (h1, h2, h3, h4, h5):
        net.addLink(h, s1)

    net.start()
    ping_loss = net.pingAll()
    run_info.write_text(
        f"SWITCH_BACKEND={switch_name}\n"
        "TOPOLOGY=h1--s1--{h2,h3,h4,h5}\n"
        f"PINGALL_LOSS_PERCENT={ping_loss}\n",
        encoding="utf-8",
    )

    server_log = logs / "server_output.txt"
    cmd_server = (
        f"cd {shlex.quote(str(root))} && "
        f"python3 -u server.py --host 10.0.0.1 --port 5000 "
        f"--history-file {shlex.quote(str(history))} --event-file {shlex.quote(str(events))}"
    )

    with server_log.open("w", encoding="utf-8") as sf:
        server_proc = h1.popen(cmd_server, shell=True, stdout=sf, stderr=subprocess.STDOUT)
        time.sleep(1.5)

        cap_proc = None
        if shutil.which("dumpcap") is not None:
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

        # Reuse assignment5 auto client for backend traffic verification.
        a5_client = root.parent / "assignment5" / "client.py"
        hosts = [h2, h3, h4, h5]
        users = ["GuiA", "GuiB", "GuiC", "GuiD"]
        procs = []
        for host, user in zip(hosts, users):
            targets = ",".join([u for u in users if u != user])
            log_path = logs / f"client_{user}.txt"
            cmd = (
                f"python3 {shlex.quote(str(a5_client))} --host 10.0.0.1 --port 5000 "
                f"--username {shlex.quote(user)} --auto-count 30 --auto-delay 0.02 "
                f"--private-every 4 --targets {shlex.quote(targets)}"
            )
            with log_path.open("w", encoding="utf-8") as lf:
                p = host.popen(cmd, shell=True, stdout=lf, stderr=subprocess.STDOUT)
            procs.append(p)

        for p in procs:
            p.wait(timeout=180)

        if cap_proc is not None:
            try:
                cap_proc.wait(timeout=40)
            except subprocess.TimeoutExpired:
                cap_proc.terminate()

        h1.cmd('pkill -f "python3 server.py" >/dev/null 2>&1 || true')
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.terminate()

    net.stop()

    print("Generated Assignment 6 backend artifacts:")
    print("- capture.pcapng")
    print("- chat_history.csv")
    print("- server_events.log")
    print("- logs/*.txt")


if __name__ == "__main__":
    run()
