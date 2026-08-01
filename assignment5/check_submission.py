#!/usr/bin/env python3
"""Validate Assignment 5 required files and formats."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


def main() -> int:
    base = Path(__file__).resolve().parent
    errors: list[str] = []

    required = [
        base / "server.py",
        base / "client.py",
        base / "chat_history.csv",
        base / "performance_results.csv",
        base / "report.pdf",
        base / "graphs" / "clients_vs_delay.png",
        base / "graphs" / "clients_vs_throughput.png",
        base / "graphs" / "message_type_distribution.png",
        base / "screenshots" / "client_connection.png",
        base / "screenshots" / "broadcast_message.png",
        base / "screenshots" / "private_message.png",
        base / "screenshots" / "client_disconnect.png",
        base / "screenshots" / "tcp_connection_termination.png",
    ]

    for p in required:
        if not p.exists():
            errors.append(f"Missing: {p.relative_to(base)}")
        elif p.is_file() and p.stat().st_size == 0:
            errors.append(f"Empty file: {p.relative_to(base)}")

    perf = base / "performance_results.csv"
    if perf.exists():
        with perf.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))

        expected = [
            "clients",
            "broadcast_messages",
            "private_messages",
            "avg_delay_ms",
            "throughput_msgs_per_sec",
        ]
        if not rows or rows[0] != expected:
            errors.append("performance_results.csv header mismatch")
        data_rows = [r for r in rows[1:] if any(c.strip() for c in r)]
        if len(data_rows) != 3:
            errors.append(f"performance_results.csv requires 3 rows (2/3/4 clients), found {len(data_rows)}")

    history = base / "chat_history.csv"
    if history.exists():
        with history.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))

        expected = ["timestamp", "sender", "receiver", "message_type", "message"]
        if not rows or rows[0] != expected:
            errors.append("chat_history.csv header mismatch")
        data_rows = [r for r in rows[1:] if any(c.strip() for c in r)]
        if len(data_rows) == 0:
            errors.append("chat_history.csv has no message rows")

    if errors:
        print("Submission check: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Submission check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
