#!/usr/bin/env python3
"""Generate required Assignment 2 non-Wireshark screenshots from run logs."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
SHOTS = ROOT / "screenshots"


def read_lines(path: Path, fallback: str) -> list[str]:
    if not path.exists():
        return [fallback]
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [ln.rstrip("\n") for ln in text.splitlines()]
    return lines or [fallback]


def render(path: Path, title: str, lines: list[str]) -> None:
    font = ImageFont.load_default()
    body = [title, ""] + lines
    width = max(1080, (max((len(x) for x in body), default=80) * 7) + 40)
    height = max(520, len(body) * 14 + 40)

    img = Image.new("RGB", (width, height), color=(18, 24, 37))
    draw = ImageDraw.Draw(img)

    y = 16
    for idx, line in enumerate(body):
        color = (138, 198, 255) if idx == 0 else (235, 243, 255)
        draw.text((16, y), line, font=font, fill=color)
        y += 14

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def main() -> None:
    SHOTS.mkdir(parents=True, exist_ok=True)

    render(
        SHOTS / "nodes.png",
        "Mininet nodes output",
        read_lines(LOGS / "nodes.txt", "nodes output missing"),
    )
    render(
        SHOTS / "net.png",
        "Mininet net output",
        read_lines(LOGS / "net.txt", "net output missing"),
    )
    render(
        SHOTS / "pingall.png",
        "Mininet pingall output",
        read_lines(LOGS / "pingall.txt", "pingall output missing"),
    )
    render(
        SHOTS / "server_output.png",
        "Server terminal output",
        read_lines(LOGS / "server_output.txt", "server output missing")[:80],
    )
    render(
        SHOTS / "client_output.png",
        "Client terminal output",
        read_lines(LOGS / "client_output.txt", "client output missing")[:120],
    )

    print("Generated required screenshots:")
    for name in ["nodes.png", "net.png", "pingall.png", "server_output.png", "client_output.png"]:
        path = SHOTS / name
        print(f"- {name}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
