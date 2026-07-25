#!/usr/bin/env python3
"""
WSL-friendly Assignment 1 runner.

Builds a simple Mininet topology using OVS bridge mode (no external controller),
then executes loss profiles 0/5/10 with application-level loss emulation.
"""

import os
import shlex
import time

from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSBridge


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "logs")

    os.makedirs(log_dir, exist_ok=True)

    setLogLevel("warning")

    net = Mininet(controller=None, switch=OVSBridge, build=False)
    h1 = net.addHost("h1", ip="10.0.0.1/8")
    h2 = net.addHost("h2", ip="10.0.0.2/8")
    s1 = net.addSwitch("s1")
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    print("[runner] starting Mininet topology (h1 -- s1 -- h2)")
    net.build()
    s1.start([])

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
