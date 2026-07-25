#!/usr/bin/env python3
"""Check Assignment 1 submission completeness."""

from pathlib import Path
import csv
import sys


ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "client.py",
    "server.py",
    "result_table.csv",
    "HOW_TO_RUN.md",
]

REQUIRED_SCREENSHOTS = [
    "nodes.png",
    "net.png",
    "pingall.png",
    "server_output.png",
    "client_output.png",
]

CSV_COLUMNS = [
    "roll_no",
    "name",
    "loss_percent",
    "timeout",
    "total_messages",
    "total_packets_sent",
    "total_retransmissions",
    "transfer_time_seconds",
    "status",
]


def check_files():
    missing = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            missing.append(rel)

    screenshots_dir = ROOT / "screenshots"
    for name in REQUIRED_SCREENSHOTS:
        if not (screenshots_dir / name).exists():
            missing.append(f"screenshots/{name}")

    if not (ROOT / "report.pdf").exists():
        missing.append("report.pdf")

    return missing


def check_csv():
    csv_path = ROOT / "result_table.csv"
    if not csv_path.exists():
        return ["result_table.csv missing"], []

    issues = []
    rows = []
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != CSV_COLUMNS:
            issues.append("result_table.csv columns do not match required header")
        rows = list(reader)

    if len(rows) != 3:
        issues.append(f"result_table.csv must have 3 data rows, found {len(rows)}")

    losses = sorted(row.get("loss_percent", "") for row in rows)
    if losses != ["0", "10", "5"]:
        issues.append(f"loss_percent values should be 0,5,10; found {','.join(losses)}")

    return issues, rows


def main():
    missing = check_files()
    csv_issues, _ = check_csv()

    if not missing and not csv_issues:
        print("Submission check: PASS")
        print("All required files, screenshots, report.pdf, and CSV structure are present.")
        return 0

    print("Submission check: FAIL")
    if missing:
        print("Missing items:")
        for item in missing:
            print(f"- {item}")

    if csv_issues:
        print("CSV issues:")
        for issue in csv_issues:
            print(f"- {issue}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
