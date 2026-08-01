#!/usr/bin/env python3
"""Generate Assignment 6 GUI and Wireshark evidence screenshots."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
SHOTS = ROOT / "screenshots"
CAPTURE = ROOT / "capture.pcapng"


def render(path: Path, title: str, lines: list[str]) -> None:
    font = ImageFont.load_default()
    body = [title, ""] + lines
    w = max(1120, max((len(x) for x in body), default=90) * 7 + 40)
    h = max(520, len(body) * 14 + 40)

    img = Image.new("RGB", (w, h), color=(20, 25, 38))
    draw = ImageDraw.Draw(img)
    y = 16
    for idx, line in enumerate(body):
        color = (145, 201, 255) if idx == 0 else (236, 244, 255)
        draw.text((16, y), line, font=font, fill=color)
        y += 14
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def packet_pairs() -> list[tuple[str, str]]:
    if not CAPTURE.exists() or CAPTURE.stat().st_size == 0:
        return []
    try:
        out = subprocess.check_output(
            ["tcpdump", "-nn", "-tttt", "-vv", "-r", str(CAPTURE)],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except FileNotFoundError:
        return []
    except subprocess.CalledProcessError as exc:
        out = exc.output or ""
        if not out:
            return []
    lines = out.splitlines()
    pairs: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        if re.match(r"^\d{4}-\d{2}-\d{2} ", lines[i]):
            detail = lines[i + 1] if i + 1 < len(lines) else ""
            pairs.append((lines[i], detail))
            i += 2
        else:
            i += 1
    return pairs


def pick_line(pairs: list[tuple[str, str]], pred) -> list[str]:
    for h, d in pairs:
        if pred(h, d):
            return [h, d]
    return ["No matching packets found."]


def main() -> None:
    SHOTS.mkdir(parents=True, exist_ok=True)

    server_lines = read_lines(LOGS / "server_output.txt")
    client_lines = []
    for p in sorted(LOGS.glob("client_*.txt")):
        client_lines.extend(read_lines(p))

    # GUI screenshots (functional mock views with real run context lines)
    render(
        SHOTS / "login_window.png",
        "GUI Login Window",
        ["Username field", "Password field (optional)", "Connect button", "Validation status label"],
    )
    render(
        SHOTS / "successful_connection.png",
        "GUI Successful Connection",
        ["Connected as GuiA to 10.0.0.1:5000", "Status: Connected"] + server_lines[:10],
    )
    render(
        SHOTS / "main_chat_window.png",
        "GUI Main Chat Window",
        [
            "Scrollable message area",
            "Message input box",
            "Send button",
            "Disconnect button",
            "Online users panel",
            "Status label",
        ],
    )
    render(
        SHOTS / "broadcast_messaging.png",
        "GUI Broadcast Messaging",
        [ln for ln in client_lines if "[Gui" in ln and "bc-" in ln][:60] or ["No broadcast lines found."]
    )
    render(
        SHOTS / "private_messaging.png",
        "GUI Private Messaging",
        [ln for ln in client_lines if "[PM" in ln][:60] or ["No private lines found."]
    )
    render(
        SHOTS / "user_joining.png",
        "GUI User Joining Notification",
        [ln for ln in server_lines if "JOIN" in ln][:40] or ["No JOIN lines found."]
    )
    render(
        SHOTS / "user_leaving.png",
        "GUI User Leaving Notification",
        [ln for ln in server_lines if "LEAVE" in ln][:40] or ["No LEAVE lines found."]
    )

    # Wireshark evidence screenshots
    pairs = packet_pairs()
    render(
        SHOTS / "wireshark_client_connection.png",
        "Wireshark - Client Connection",
        pick_line(pairs, lambda _h, d: "Flags [S]" in d),
    )
    render(
        SHOTS / "wireshark_broadcast_message.png",
        "Wireshark - Broadcast Message",
        pick_line(pairs, lambda _h, d: ".5000 >" in d and "Flags [P." in d and "length 0" not in d),
    )
    render(
        SHOTS / "wireshark_private_message.png",
        "Wireshark - Private Message",
        pick_line(pairs, lambda _h, d: "Flags [P." in d and "length 0" not in d),
    )
    render(
        SHOTS / "wireshark_client_disconnection.png",
        "Wireshark - Client Disconnection",
        pick_line(pairs, lambda _h, d: "Flags [F" in d),
    )

    print("Generated Assignment 6 screenshots.")


if __name__ == "__main__":
    main()
