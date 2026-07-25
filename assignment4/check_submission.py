#!/usr/bin/env python3
"""Validate Assignment 4 submission readiness."""

from pathlib import Path
import csv
import sys


def main() -> int:
    base = Path(__file__).resolve().parent
    errors: list[str] = []

    required = [
        base / "server.py",
        base / "client.py",
        base / "chat_log.txt",
        base / "server_events.log",
        base / "performance_results.csv",
        base / "report.pdf",
        base / "graphs" / "clients_vs_delay.png",
        base / "graphs" / "clients_vs_throughput.png",
        base / "screenshots" / "tcp_handshake.png",
        base / "screenshots" / "chat_message.png",
        base / "screenshots" / "broadcast_message.png",
        base / "screenshots" / "connection_close.png",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Missing: {path.name}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"Empty file: {path.name}")

    perf = base / "performance_results.csv"
    if perf.exists():
        with perf.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        expected_header = [
            "clients",
            "total_messages",
            "avg_delivery_time_ms",
            "throughput_msgs_per_sec",
        ]

        if not rows or rows[0] != expected_header:
            errors.append("performance_results.csv header is invalid")
        data_rows = [r for r in rows[1:] if any(cell.strip() for cell in r)]
        if len(data_rows) < 3:
            errors.append("performance_results.csv must include rows for 1, 2, and 3 clients")

    if errors:
        print("Submission check: FAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Submission check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
