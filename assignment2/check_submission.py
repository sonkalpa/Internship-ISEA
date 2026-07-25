#!/usr/bin/env python3
"""Validate Assignment 2 required submission artifacts."""

from pathlib import Path
import csv
import sys


def main() -> int:
    base = Path(__file__).resolve().parent
    errors: list[str] = []

    required = [
        base / "server.py",
        base / "client.py",
        base / "server_log.txt",
        base / "result_table.csv",
        base / "message_response_log.csv",
        base / "graphs" / "mode_vs_response_time.png",
        base / "graphs" / "message_size_vs_throughput.png",
        base / "graphs" / "message_response_time.png",
        base / "screenshots" / "nodes.png",
        base / "screenshots" / "net.png",
        base / "screenshots" / "pingall.png",
        base / "screenshots" / "server_output.png",
        base / "screenshots" / "client_output.png",
        base / "screenshots" / "persistent_handshake.png",
        base / "screenshots" / "persistent_data_packets.png",
        base / "screenshots" / "persistent_connection_close.png",
        base / "screenshots" / "new_connection_multiple_handshakes.png",
        base / "report.pdf",
    ]

    for path in required:
        if not path.exists():
            errors.append(f"Missing: {path.relative_to(base)}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"Empty file: {path.relative_to(base)}")

    result_csv = base / "result_table.csv"
    if result_csv.exists():
        with result_csv.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))

        expected_header = [
            "roll_no",
            "name",
            "mode",
            "bandwidth_mbps",
            "delay_ms",
            "message_size_bytes",
            "total_messages",
            "average_response_time_seconds",
            "throughput_bytes_per_second",
            "status",
        ]

        if not rows or rows[0] != expected_header:
            errors.append("result_table.csv header mismatch")
        data_rows = [r for r in rows[1:] if any(c.strip() for c in r)]
        if len(data_rows) != 6:
            errors.append(f"result_table.csv requires 6 data rows, found {len(data_rows)}")

    msg_csv = base / "message_response_log.csv"
    if msg_csv.exists():
        with msg_csv.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))

        expected_header = [
            "roll_no",
            "name",
            "mode",
            "message_size_bytes",
            "message_number",
            "response_time_seconds",
        ]

        if not rows or rows[0] != expected_header:
            errors.append("message_response_log.csv header mismatch")
        data_rows = [r for r in rows[1:] if any(c.strip() for c in r)]
        if len(data_rows) != 60:
            errors.append(f"message_response_log.csv requires 60 rows, found {len(data_rows)}")

    if errors:
        print("Submission check: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Submission check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
