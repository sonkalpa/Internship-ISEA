#!/usr/bin/env python3
"""TCP chat client for Assignment 4 (interactive and auto modes)."""

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
    summary_file: Path | None,
) -> None:
    send_times: dict[str, float] = {}
    delivery_samples_ms: list[float] = []
    lock = threading.Lock()
    done = threading.Event()

    start_ts = time.time()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall((username + "\n").encode("utf-8"))

        rfile = sock.makefile("r", encoding="utf-8", newline="\n")

        def receiver() -> None:
            own_prefix = f"[{username}] "
            for raw in rfile:
                message = raw.rstrip("\n")
                print(message)

                if message.startswith(own_prefix):
                    payload = message[len(own_prefix) :]
                    with lock:
                        if payload in send_times:
                            sent_ts = send_times.pop(payload)
                            delivery_samples_ms.append((time.time() - sent_ts) * 1000.0)

                if done.is_set():
                    break

        rx_thread = threading.Thread(target=receiver, daemon=True)
        rx_thread.start()

        sent_messages = 0
        if auto_count > 0:
            for i in range(1, auto_count + 1):
                payload = f"auto-{i:02d}"
                with lock:
                    send_times[payload] = time.time()
                sock.sendall((payload + "\n").encode("utf-8"))
                sent_messages += 1
                if auto_delay > 0:
                    time.sleep(auto_delay)

            time.sleep(1.0)
        else:
            print("Type message and press Enter. Use /quit to exit.")
            while True:
                try:
                    payload = input()
                except EOFError:
                    payload = "/quit"

                if payload.strip() == "/quit":
                    break

                with lock:
                    send_times[payload] = time.time()
                sock.sendall((payload + "\n").encode("utf-8"))
                sent_messages += 1

        done.set()
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

    duration_sec = max(time.time() - start_ts, 0.001)
    avg_delivery_ms = (
        sum(delivery_samples_ms) / len(delivery_samples_ms)
        if delivery_samples_ms
        else 0.0
    )

    summary = {
        "username": username,
        "sent_messages": sent_messages,
        "received_own_broadcasts": len(delivery_samples_ms),
        "avg_delivery_time_ms": round(avg_delivery_ms, 3),
        "duration_sec": round(duration_sec, 3),
    }

    print(json.dumps(summary, indent=2))

    if summary_file is not None:
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP chat client")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--username", default="user")
    parser.add_argument("--auto-count", type=int, default=0)
    parser.add_argument("--auto-delay", type=float, default=0.03)
    parser.add_argument("--summary-file", default="")
    args = parser.parse_args()

    summary_file = Path(args.summary_file) if args.summary_file else None
    run_client(
        host=args.host,
        port=args.port,
        username=args.username,
        auto_count=args.auto_count,
        auto_delay=args.auto_delay,
        summary_file=summary_file,
    )


if __name__ == "__main__":
    main()
