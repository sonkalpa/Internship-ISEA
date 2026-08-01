#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/run_wsl_assignment6.py"
python3 "$SCRIPT_DIR/generate_screenshots.py"
python3 "$SCRIPT_DIR/generate_report.py"
python3 "$SCRIPT_DIR/generate_report_pdf.py"
python3 "$SCRIPT_DIR/check_submission.py"
