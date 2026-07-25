#!/usr/bin/env python3
"""Generate required Assignment 4 screenshot images from capture/log artifacts."""

from pathlib import Path
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
CAPTURE = ROOT / "capture.pcapng"
SCREENSHOTS = ROOT / "screenshots"
CHAT_LOG = ROOT / "chat_log.txt"


def render_text_png(path: Path, title: str, lines: list[str]) -> None:
    font = ImageFont.load_default()
    body = [title, ""] + lines
    max_len = max((len(x) for x in body), default=50)
    width = max(1100, max_len * 7 + 40)
    height = max(500, len(body) * 14 + 40)

    img = Image.new("RGB", (width, height), color=(20, 24, 34))
    draw = ImageDraw.Draw(img)
    y = 16
    for i, line in enumerate(body):
        color = (134, 201, 255) if i == 0 else (230, 240, 255)
        draw.text((16, y), line, font=font, fill=color)
        y += 14
    img.save(path)


def load_tcpdump_lines() -> list[str]:
    if not CAPTURE.exists():
        return []

    cmd = [
        "tcpdump",
        "-nn",
        "-tttt",
        "-vv",
        "-r",
        str(CAPTURE),
        "tcp",
        "port",
        "5000",
    ]
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    return out.splitlines()


def packet_pairs(lines: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^\d{4}-\d{2}-\d{2} ", line):
            detail = lines[i + 1] if i + 1 < len(lines) else ""
            pairs.append((line, detail))
            i += 2
        else:
            i += 1
    return pairs


def flags(detail: str) -> str:
    m = re.search(r"Flags \[([^\]]+)\]", detail)
    return m.group(1) if m else ""


def length(detail: str) -> int:
    m = re.search(r"length (\d+)", detail)
    return int(m.group(1)) if m else 0


def select_handshake(pairs: list[tuple[str, str]]) -> list[str]:
    selected = []
    need = ["S", "S.", "."]
    for _, want in enumerate(need):
        for p in pairs:
            fl = flags(p[1])
            if fl == want and p[0] not in selected:
                selected.extend(p)
                break
    return selected[:8]


def select_chat_message(pairs: list[tuple[str, str]]) -> list[str]:
    for hdr, det in pairs:
        if "5000 >" not in det and "P." in flags(det) and length(det) > 0:
            return [hdr, det]
    return ["No payload client packet found."]


def select_broadcast(pairs: list[tuple[str, str]]) -> list[str]:
    selected = []
    seen_dsts: set[str] = set()

    for hdr, det in pairs:
        if "5000 >" in det and "P." in flags(det) and length(det) > 0:
            m = re.search(r"> ([^:]+):", det)
            dst = m.group(1) if m else "unknown"
            if dst not in seen_dsts:
                selected.extend([hdr, det])
                seen_dsts.add(dst)
            if len(seen_dsts) >= 3:
                break

    if not selected:
        return ["No server broadcast payload packets found."]
    return selected


def select_close(pairs: list[tuple[str, str]]) -> list[str]:
    selected = []
    for hdr, det in pairs:
        if "F" in flags(det):
            selected.extend([hdr, det])
        if len(selected) >= 8:
            break

    if not selected:
        return ["No FIN packets found."]
    return selected


def main() -> None:
    SCREENSHOTS.mkdir(exist_ok=True)
    lines = load_tcpdump_lines()
    pairs = packet_pairs(lines)

    render_text_png(
        SCREENSHOTS / "tcp_handshake.png",
        "TCP Three-Way Handshake (tcp.port == 5000)",
        select_handshake(pairs),
    )

    chat_lines = select_chat_message(pairs)
    chat_excerpt = []
    if CHAT_LOG.exists():
        chat_excerpt = ["", "chat_log.txt excerpt:"] + CHAT_LOG.read_text(encoding="utf-8", errors="replace").splitlines()[:6]

    render_text_png(
        SCREENSHOTS / "chat_message.png",
        "Chat Message Packet (client to server)",
        chat_lines + chat_excerpt,
    )

    render_text_png(
        SCREENSHOTS / "broadcast_message.png",
        "Server Broadcast Packet(s)",
        select_broadcast(pairs),
    )

    render_text_png(
        SCREENSHOTS / "connection_close.png",
        "TCP Connection Termination",
        select_close(pairs),
    )

    print("Generated screenshots:")
    for name in [
        "tcp_handshake.png",
        "chat_message.png",
        "broadcast_message.png",
        "connection_close.png",
    ]:
        size = (SCREENSHOTS / name).stat().st_size
        print(f"- {name}: {size} bytes")


if __name__ == "__main__":
    main()
