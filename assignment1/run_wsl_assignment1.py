#!/usr/bin/env python3
"""
WSL-friendly Assignment 1 runner.

Builds a simple Mininet topology using OVS bridge mode (no external controller),
then executes loss profiles 0/5/10 with application-level loss emulation.
"""

import os
import shutil
import subprocess
import shlex
import time

from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.nodelib import LinuxBridge


def _ovs_available() -> bool:
    try:
        cmd = ["ovs-vsctl", "show"]
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def _linuxbridge_available() -> bool:
    return shutil.which("brctl") is not None


def _choose_switch_class():
    forced = os.environ.get("A1_SWITCH", "").strip().lower()

    if forced == "ovs":
        if _ovs_available():
            return OVSBridge, "OVSBridge (forced)"
        return None, "Loopback fallback (forced ovs unavailable)"

    if forced == "linuxbridge":
        if _linuxbridge_available():
            return LinuxBridge, "LinuxBridge (forced)"
        return None, "Loopback fallback (forced linuxbridge unavailable)"

    if _ovs_available():
        return OVSBridge, "OVSBridge"

    if _linuxbridge_available():
        return LinuxBridge, "LinuxBridge (fallback - OVS unavailable)"

    return None, "Loopback fallback (OVS and LinuxBridge unavailable)"


def _run_local_profiles(script_dir: str, log_dir: str):
    print("[runner] starting local loopback fallback mode (no Mininet switch backend)")

    for loss in (0, 5, 10):
        print(f"[runner] running profile loss={loss}% (loopback)")

        server_log = os.path.join(log_dir, f"server_loss{loss}.out.txt")
        client_log = os.path.join(log_dir, f"client_loss{loss}.txt")

        server_cmd = [
            "python3",
            "server.py",
            "--host",
            "127.0.0.1",
            "--port",
            "5000",
            "--expected",
            "10",
            "--reply-delay-ms",
            "30",
        ]
        with open(server_log, "w", encoding="utf-8", newline="\n") as sf:
            server_proc = subprocess.Popen(  # noqa: S603
                server_cmd,
                cwd=script_dir,
                stdout=sf,
                stderr=sf,
                text=True,
            )

        time.sleep(1.0)

        client_cmd = [
            "python3",
            "client.py",
            "--server-ip",
            "127.0.0.1",
            "--port",
            "5000",
            "--loss-percent",
            str(loss),
            "--timeout",
            "1.5",
            "--emulate-loss",
            "--seed",
            "2408",
        ]

        completed = subprocess.run(  # noqa: S603
            client_cmd,
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )

        with open(client_log, "w", encoding="utf-8", newline="\n") as cf:
            cf.write(completed.stdout)

        try:
            server_proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            server_proc.terminate()
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.kill()

    print("[runner] profiles complete")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "logs")

    os.makedirs(log_dir, exist_ok=True)

    setLogLevel("warning")

    switch_cls, switch_label = _choose_switch_class()

    if switch_cls is None:
        print(f"[runner] switch backend unavailable: {switch_label}")
        _run_local_profiles(script_dir, log_dir)
        return

    net = Mininet(controller=None, switch=switch_cls, build=False)
    h1 = net.addHost("h1", ip="10.0.0.1/8")
    h2 = net.addHost("h2", ip="10.0.0.2/8")
    s1 = net.addSwitch("s1")
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    print(f"[runner] starting Mininet topology (h1 -- s1 -- h2) with {switch_label}")
    net.start()

    try:
        ping_loss = net.pingAll()
        print(f"[runner] pingAll packet loss: {ping_loss}%")

        for loss in (0, 5, 10):
            print(f"[runner] running profile loss={loss}%")

            server_log = os.path.join(log_dir, f"server_loss{loss}.out.txt")
            client_log = os.path.join(log_dir, f"client_loss{loss}.txt")

            h1.cmd('pkill -f "python3 server.py" >/dev/null 2>&1 || true')

            server_cmd = (
                f"cd {shlex.quote(script_dir)} && "
                f"python3 server.py --host 10.0.0.1 --port 5000 --expected 10 "
                f"--reply-delay-ms 30 > {shlex.quote(server_log)} 2>&1 &"
            )
            h1.cmd(server_cmd)
            time.sleep(1.0)

            client_cmd = (
                f"cd {shlex.quote(script_dir)} && "
                f"python3 client.py --server-ip 10.0.0.1 --port 5000 "
                f"--loss-percent {loss} --timeout 1.5 --emulate-loss --seed 2408"
            )
            output = h2.cmd(client_cmd)
            with open(client_log, "w", encoding="utf-8", newline="\n") as f:
                f.write(output)

            h1.cmd('pkill -f "python3 server.py" >/dev/null 2>&1 || true')
            time.sleep(0.3)

        print("[runner] profiles complete")
    finally:
        print("[runner] stopping Mininet")
        net.stop()


if __name__ == "__main__":
    main()
