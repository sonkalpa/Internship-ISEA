#!/usr/bin/env python3
"""Validate Assignment 3 required submission artifacts."""

from pathlib import Path
import csv
import re
import sys


def check_exists_non_empty(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing: {path.name}")
        return
    if path.is_file() and path.stat().st_size == 0:
        errors.append(f"Empty file: {path.name}")


def main() -> int:
    base = Path(__file__).resolve().parent
    errors: list[str] = []

    required_files = [
        base / "raw_capture.c",
        base / "program_output.txt",
        base / "capture.pcapng",
        base / "packet_comparison_template.csv",
        base / "report.pdf",
    ]

    required_screenshots = [
        base / "screenshots" / "traffic_generation.png",
        base / "screenshots" / "program_output.png",
        base / "screenshots" / "wireshark_packets.png",
        base / "screenshots" / "comparison_packets.png",
    ]

    for path in required_files + required_screenshots:
        check_exists_non_empty(path, errors)

    output_path = base / "program_output.txt"
    if output_path.exists():
        text = output_path.read_text(encoding="utf-8", errors="replace")
        packet_count = len(re.findall(r"^PACKET_NO=", text, flags=re.MULTILINE))
        if packet_count < 20:
            errors.append(f"program_output.txt has only {packet_count} packets (< 20)")
        if "ASSIGNED_PROTOCOL=TCP" not in text:
            errors.append("program_output.txt missing ASSIGNED_PROTOCOL=TCP")

    csv_path = base / "packet_comparison_template.csv"
    if csv_path.exists():
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        data_rows = [r for r in rows[1:] if any(cell.strip() for cell in r)]
        if len(data_rows) < 5:
            errors.append("packet_comparison_template.csv has fewer than 5 filled rows")

    if errors:
        print("Submission check: FAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Submission check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
