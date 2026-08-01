#!/usr/bin/env python3
"""Validate Assignment 6 required files."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    base = Path(__file__).resolve().parent
    errors: list[str] = []

    required = [
        base / "server.py",
        base / "client_gui.py",
        base / "report.pdf",
        base / "screenshots" / "login_window.png",
        base / "screenshots" / "successful_connection.png",
        base / "screenshots" / "main_chat_window.png",
        base / "screenshots" / "broadcast_messaging.png",
        base / "screenshots" / "private_messaging.png",
        base / "screenshots" / "user_joining.png",
        base / "screenshots" / "user_leaving.png",
        base / "screenshots" / "wireshark_client_connection.png",
        base / "screenshots" / "wireshark_broadcast_message.png",
        base / "screenshots" / "wireshark_private_message.png",
        base / "screenshots" / "wireshark_client_disconnection.png",
    ]

    for p in required:
        if not p.exists():
            errors.append(f"Missing: {p.relative_to(base)}")
        elif p.is_file() and p.stat().st_size == 0:
            errors.append(f"Empty file: {p.relative_to(base)}")

    if errors:
        print("Submission check: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Submission check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
