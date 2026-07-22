#!/usr/bin/env python3
"""
Generate local TCP traffic for Assignment 3 packet capture.

Starts a local TCP server and performs repeated client connections to create
observable TCP handshakes and data packets.
"""

import argparse
import socket
import threading
import time


def run_server(host: str, port: int, expected_connections: int):
    accepted = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(50)

        while accepted < expected_connections:
            conn, _ = s.accept()
            with conn:
                _ = conn.recv(4096)
                conn.sendall(b"OK")
            accepted += 1


def run_clients(host: str, port: int, count: int, delay: float):
    for i in range(1, count + 1):
        payload = f"packet-{i}".encode()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((host, port))
            c.sendall(payload)
            _ = c.recv(1024)
        if delay > 0:
            time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(description="Generate local TCP traffic")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--count", type=int, default=40)
    parser.add_argument("--delay", type=float, default=0.03)
    parser.add_argument("--startup-delay", type=float, default=1.0)
    args = parser.parse_args()

    server_thread = threading.Thread(
        target=run_server,
        args=(args.host, args.port, args.count),
        daemon=True,
    )
    server_thread.start()

    time.sleep(args.startup_delay)
    run_clients(args.host, args.port, args.count, args.delay)

    server_thread.join(timeout=3)
    print(f"Generated {args.count} TCP connections to {args.host}:{args.port}")


if __name__ == "__main__":
    main()
