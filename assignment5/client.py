#!/usr/bin/env python3
"""Assignment 5 client with broadcast, private messaging, and /list support."""

from __future__ import annotations

import argparse
import json
import socket
import threading
import time
from pathlib import Path


def run_client(
    host: str,
    port: int,
    username: str,
    auto_count: int,
    auto_delay: float,
    private_every: int,
    targets: list[str],
    summary_file: Path | None,
) -> None:
    send_times: dict[str, float] = {}
    delivery_samples_ms: list[float] = []
    lock = threading.Lock()
    done = threading.Event()

    broadcast_sent = 0
    private_sent = 0
    sent_messages = 0

    start_ts = time.time()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall((username + "\n").encode("utf-8"))

        rfile = sock.makefile("r", encoding="utf-8", newline="\n")

        def receiver() -> None:
            for raw in rfile:
                msg = raw.rstrip("\n")
                print(msg)

                with lock:
                    for token, sent_ts in list(send_times.items()):
                        if token in msg:
                            delivery_samples_ms.append((time.time() - sent_ts) * 1000.0)
                            send_times.pop(token, None)

                if done.is_set():
                    break

        rx = threading.Thread(target=receiver, daemon=True)
        rx.start()

        if auto_count > 0:
            for i in range(1, auto_count + 1):
                if targets and private_every > 0 and i % private_every == 0:
                    token = f"pm-{i:03d}"
                    target = targets[(i // private_every - 1) % len(targets)]
                    outbound = f"/msg {target} {token}"
                    private_sent += 1
                else:
                    token = f"bc-{i:03d}"
                    outbound = token
                    broadcast_sent += 1

                with lock:
                    send_times[token] = time.time()

                sock.sendall((outbound + "\n").encode("utf-8"))
                sent_messages += 1

                if i % 20 == 0:
                    sock.sendall(b"/list\n")

                if auto_delay > 0:
                    time.sleep(auto_delay)

            time.sleep(1.5)
        else:
            print("Type message and Enter. Use /quit to exit.")
            while True:
                try:
                    outbound = input().strip()
                except EOFError:
                    outbound = "/quit"

                if not outbound:
                    continue
                if outbound == "/quit":
                    break

                token = f"manual-{int(time.time() * 1000)}"
                if outbound.startswith("/msg "):
                    private_sent += 1
                else:
                    broadcast_sent += 1

                with lock:
                    send_times[token] = time.time()

                sock.sendall((outbound + "\n").encode("utf-8"))
                sent_messages += 1

        done.set()
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

    duration_sec = max(time.time() - start_ts, 0.001)
    avg_delay_ms = sum(delivery_samples_ms) / len(delivery_samples_ms) if delivery_samples_ms else 0.0

    summary = {
        "username": username,
        "sent_messages": sent_messages,
        "broadcast_sent": broadcast_sent,
        "private_sent": private_sent,
        "received_matches": len(delivery_samples_ms),
        "avg_delay_ms": round(avg_delay_ms, 3),
        "duration_sec": round(duration_sec, 3),
    }

    print(json.dumps(summary, indent=2))
    if summary_file is not None:
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Assignment 5 chat client")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--username", default="Client")
    parser.add_argument("--auto-count", type=int, default=0)
    parser.add_argument("--auto-delay", type=float, default=0.02)
    parser.add_argument("--private-every", type=int, default=5)
    parser.add_argument("--targets", default="")
    parser.add_argument("--summary-file", default="")
    args = parser.parse_args()

    targets = [t.strip() for t in args.targets.split(",") if t.strip()]
    summary_file = Path(args.summary_file) if args.summary_file else None

    run_client(
        host=args.host,
        port=args.port,
        username=args.username,
        auto_count=args.auto_count,
        auto_delay=args.auto_delay,
        private_every=args.private_every,
        targets=targets,
        summary_file=summary_file,
    )


if __name__ == "__main__":
    main()
