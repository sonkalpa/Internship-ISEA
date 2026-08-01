#!/usr/bin/env python3
"""Generate a simple PDF report from report.md without external dependencies."""

from pathlib import Path
from textwrap import wrap


PAGE_WIDTH = 612
PAGE_HEIGHT = 792
LEFT_MARGIN = 50
TOP_Y = 760
LINE_HEIGHT = 14
MAX_CHARS = 92
LINES_PER_PAGE = 48


def normalize_lines(markdown_text: str):
    raw_lines = markdown_text.splitlines()
    lines = []
    for line in raw_lines:
        text = line.rstrip()

        if text.startswith("#"):
            text = text.lstrip("#").strip()
            if text:
                lines.append(text.upper())
                lines.append("")
            continue

        if text.startswith("- "):
            text = "* " + text[2:]

        if text.startswith("|") and text.endswith("|"):
            text = text.strip("|")
            text = " | ".join(part.strip() for part in text.split("|"))

        if not text:
            lines.append("")
            continue

        wrapped = wrap(text, width=MAX_CHARS) or [""]
        lines.extend(wrapped)

    return lines


def pdf_escape(text: str):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_content_stream(page_lines):
    ops = ["BT", f"/F1 11 Tf", f"{LEFT_MARGIN} {TOP_Y} Td"]
    first = True

    for line in page_lines:
        escaped = pdf_escape(line)
        if first:
            ops.append(f"({escaped}) Tj")
            first = False
        else:
            ops.append(f"0 -{LINE_HEIGHT} Td")
            ops.append(f"({escaped}) Tj")

    ops.append("ET")
    return "\n".join(ops).encode("ascii", errors="replace")


def generate_pdf(lines, output_path: Path):
    pages = [lines[i : i + LINES_PER_PAGE] for i in range(0, len(lines), LINES_PER_PAGE)]

    objects = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")

    page_count = len(pages)
    first_page_obj = 3
    first_content_obj = first_page_obj + page_count
    font_obj = first_content_obj + page_count

    kids = " ".join(f"{first_page_obj + i} 0 R" for i in range(page_count))
    objects.append(f"<< /Type /Pages /Count {page_count} /Kids [{kids}] >>".encode("ascii"))

    for i in range(page_count):
        content_ref = first_content_obj + i
        page_obj = (
            "<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_obj} 0 R >> >> "
            f"/Contents {content_ref} 0 R >>"
        )
        objects.append(page_obj.encode("ascii"))

    for page_lines in pages:
        stream = build_content_stream(page_lines)
        header = f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
        objects.append(header + stream + b"\nendstream")

    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n")

    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode("ascii"))

    trailer = (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    )
    pdf.extend(trailer.encode("ascii"))

    output_path.write_bytes(pdf)


def main() -> None:
    root = Path(__file__).resolve().parent
    source = root / "report.md"
    target = root / "report.pdf"

    text = source.read_text(encoding="utf-8")
    lines = normalize_lines(text)
    generate_pdf(lines, target)
    print(f"Generated {target}")


if __name__ == "__main__":
    main()
