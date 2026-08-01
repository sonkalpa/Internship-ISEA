#!/usr/bin/env python3
"""Generate Assignment 5 required screenshot artifacts from logs/capture."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
SHOTS = ROOT / "screenshots"
CAPTURE = ROOT / "capture.pcapng"


def render_text_png(path: Path, title: str, lines: list[str]) -> None:
    font = ImageFont.load_default()
    body = [title, ""] + lines
    width = max(1120, max((len(x) for x in body), default=90) * 7 + 40)
    height = max(520, len(body) * 14 + 40)

    img = Image.new("RGB", (width, height), color=(18, 24, 38))
    draw = ImageDraw.Draw(img)

    y = 16
    for idx, line in enumerate(body):
        color = (137, 198, 255) if idx == 0 else (235, 244, 255)
        draw.text((16, y), line, font=font, fill=color)
        y += 14

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def tcpdump_pairs() -> list[tuple[str, str]]:
    if not CAPTURE.exists() or CAPTURE.stat().st_size == 0:
        return []

    out = subprocess.check_output(
        ["tcpdump", "-nn", "-tttt", "-vv", "-r", str(CAPTURE)],
        text=True,
        stderr=subprocess.STDOUT,
    )
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


def first_match(pairs: list[tuple[str, str]], pred) -> list[str]:
    for h, d in pairs:
        if pred(h, d):
            return [h, d]
    return ["No matching packets found in capture."]


def main() -> None:
    SHOTS.mkdir(parents=True, exist_ok=True)

    server_lines = read_lines(LOGS / "server_output.txt")
    client_lines = []
    for p in sorted(LOGS.glob("client_*_Client*.txt")):
        client_lines.extend(read_lines(p))

    render_text_png(
        SHOTS / "client_connection.png",
        "Client Connection Events",
        [ln for ln in server_lines if "SYSTEM:JOIN" in ln or "WELCOME" in ln][:40]
        or ["No join lines found; see server output log."],
    )

    render_text_png(
        SHOTS / "broadcast_message.png",
        "Broadcast Message Evidence",
        [ln for ln in client_lines if "[Client" in ln and "bc-" in ln][:60]
        or ["No broadcast lines found in client logs."],
    )

    render_text_png(
        SHOTS / "private_message.png",
        "Private Message Evidence",
        [ln for ln in client_lines if "[PM" in ln][:60]
        or ["No private message lines found in client logs."],
    )

    render_text_png(
        SHOTS / "client_disconnect.png",
        "Client Disconnect Events",
        [ln for ln in server_lines if "SYSTEM:LEAVE" in ln][:40]
        or ["No leave lines found; see server output log."],
    )

    pairs = tcpdump_pairs()
    fin_lines = first_match(pairs, lambda _h, d: "Flags [F" in d)
    render_text_png(
        SHOTS / "tcp_connection_termination.png",
        "TCP Connection Termination",
        fin_lines,
    )

    print("Generated screenshots:")
    for name in [
        "client_connection.png",
        "broadcast_message.png",
        "private_message.png",
        "client_disconnect.png",
        "tcp_connection_termination.png",
    ]:
        p = SHOTS / name
        print(f"- {name}: {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
