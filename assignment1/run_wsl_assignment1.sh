#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
CSV_FILE="$SCRIPT_DIR/result_table.csv"

if ! command -v mn >/dev/null 2>&1; then
  echo "Error: Mininet is not installed."
  echo "Install with: sudo apt install -y mininet openvswitch-switch xterm"
  exit 1
fi

echo "[1/5] Requesting sudo access..."
sudo -v

echo "[2/5] Cleaning previous Mininet state..."
sudo mn -c >/dev/null 2>&1 || true

mkdir -p "$LOG_DIR"
rm -f "$CSV_FILE"

echo "[3/5] Running Assignment 1 profiles (loss=0,5,10) in WSL-safe mode..."
sudo -E python3 "$SCRIPT_DIR/run_wsl_assignment1.py"

echo "[4/5] Generated files:"
echo "  - $CSV_FILE"
echo "  - $LOG_DIR/client_loss0.txt"
echo "  - $LOG_DIR/client_loss5.txt"
echo "  - $LOG_DIR/client_loss10.txt"
echo "  - $LOG_DIR/server_loss0.out.txt"
echo "  - $LOG_DIR/server_loss5.out.txt"
echo "  - $LOG_DIR/server_loss10.out.txt"

echo "[5/5] result_table.csv preview:"
cat "$CSV_FILE"

echo
echo "Done. Capture required screenshots manually from a normal interactive run if needed."
