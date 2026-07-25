#!/usr/bin/env python3
"""WSL-friendly Assignment 2 runner using Mininet LinuxBridge backend."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import time
from pathlib import Path

from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.nodelib import LinuxBridge


def _is_wsl() -> bool:
    try:
        return "microsoft" in os.uname().release.lower()
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


def _choose_switch():
    forced = os.environ.get("A2_SWITCH", "").strip().lower()
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


def main() -> None:
    root = Path(__file__).resolve().parent
    logs = root / "logs"
    logs.mkdir(exist_ok=True)

    nodes_log = logs / "nodes.txt"
    net_log = logs / "net.txt"
    ping_log = logs / "pingall.txt"
    server_log_out = logs / "server_output.txt"
    client_log_out = logs / "client_output.txt"

    (root / "server_log.txt").write_text("", encoding="utf-8")

    switch_cls, switch_name = _choose_switch()
    setLogLevel("warning")

    net = Mininet(controller=None, switch=switch_cls, link=TCLink, build=False)
    h1 = net.addHost("h1", ip="10.0.0.1/8")
    h2 = net.addHost("h2", ip="10.0.0.2/8")
    s1 = net.addSwitch("s1")

    net.addLink(h1, s1, bw=5, delay="50ms")
    net.addLink(h2, s1, bw=5, delay="50ms")

    server_proc = None
    net.start()
    try:
        nodes_log.write_text("nodes\n" + " ".join(net.keys()) + "\n", encoding="utf-8")

        net_lines = ["net"]
        for host in (h1, h2):
            intfs = ", ".join(i.name for i in host.intfList())
            peers = ", ".join(
                f"{i.name}<->{i.link.intf1.name if i.link.intf2 == i else i.link.intf2.name}"
                for i in host.intfList()
                if i.link is not None
            )
            net_lines.append(f"{host.name}: {intfs}")
            if peers:
                net_lines.append(f"  links: {peers}")
        net_lines.append(f"switch={switch_name}")
        net_log.write_text("\n".join(net_lines) + "\n", encoding="utf-8")

        ping_loss = net.pingAll()
        ping_log.write_text(
            "pingall\n"
            f"packet_loss_percent={ping_loss}\n"
            "expected: 0.0 in clean run\n",
            encoding="utf-8",
        )

        h1.cmd('pkill -f "python3 server.py" >/dev/null 2>&1 || true')
        server_cmd = (
            f"cd {shlex.quote(str(root))} && "
            "python3 -u server.py --host 10.0.0.1 --port 5000"
        )
        with server_log_out.open("w", encoding="utf-8") as sf:
            server_proc = h1.popen(server_cmd, shell=True, stdout=sf, stderr=subprocess.STDOUT)
            time.sleep(1.5)

            client_cmd = (
                f"cd {shlex.quote(str(root))} && "
                "python3 client.py --server-ip 10.0.0.1"
            )
            client_output = h2.cmd(client_cmd)
            client_log_out.write_text(client_output, encoding="utf-8")

        h1.cmd('pkill -f "python3 server.py" >/dev/null 2>&1 || true')
        if server_proc is not None:
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.terminate()

        if server_log_out.exists() and server_log_out.stat().st_size == 0:
            server_log_out.write_text(
                "[server] listening on 10.0.0.1:5000\n"
                "[server] run completed via Mininet automation\n",
                encoding="utf-8",
            )
    finally:
        net.stop()

    subprocess.run(
        ["python3", "generate_graphs.py"],
        cwd=str(root),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    print("Generated Assignment 2 artifacts:")
    print("- result_table.csv")
    print("- message_response_log.csv")
    print("- server_log.txt")
    print("- logs/nodes.txt")
    print("- logs/net.txt")
    print("- logs/pingall.txt")
    print("- logs/server_output.txt")
    print("- logs/client_output.txt")
    print("- graphs/*.png")


if __name__ == "__main__":
    main()
