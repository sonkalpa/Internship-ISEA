#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v mn >/dev/null 2>&1; then
  echo "Error: Mininet is not installed in WSL/Linux."
  exit 1
fi

echo "[1/5] Cleaning previous Mininet state..."
mn -c >/dev/null 2>&1 || true

echo "[2/5] Running Assignment 4 Mininet experiment..."
python3 "$SCRIPT_DIR/run_wsl_assignment4.py"

echo "[3/5] Generating performance graphs..."
python3 "$SCRIPT_DIR/generate_graphs.py"

echo "[4/5] Generating screenshot evidence from capture..."
python3 "$SCRIPT_DIR/generate_screenshots.py"

echo "[5/5] Done. Key files:"
echo "  - $SCRIPT_DIR/chat_log.txt"
echo "  - $SCRIPT_DIR/server_events.log"
echo "  - $SCRIPT_DIR/performance_results.csv"
echo "  - $SCRIPT_DIR/graphs/clients_vs_delay.png"
echo "  - $SCRIPT_DIR/graphs/clients_vs_throughput.png"
echo "  - $SCRIPT_DIR/screenshots/tcp_handshake.png"
echo "  - $SCRIPT_DIR/screenshots/chat_message.png"
echo "  - $SCRIPT_DIR/screenshots/broadcast_message.png"
echo "  - $SCRIPT_DIR/screenshots/connection_close.png"
