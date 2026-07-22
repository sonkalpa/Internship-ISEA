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
for loss in 0 5 10; do
  echo "  - profile loss=${loss}%"

  sudo mn --topo single,2 --controller none <<EOF >/dev/null
h1 bash -lc "cd $SCRIPT_DIR && python3 server.py --host 10.0.0.1 --port 5000 --expected 10 --reply-delay-ms 30 > logs/server_loss${loss}.out.txt 2>&1 &"
py import time; time.sleep(1)
h2 bash -lc "cd $SCRIPT_DIR && python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent ${loss} --timeout 1.5 --emulate-loss --seed 2408 > logs/client_loss${loss}.txt 2>&1"
py import time; time.sleep(1)
h1 pkill -f "python3 server.py" || true
exit
EOF

  sudo mn -c >/dev/null 2>&1 || true
done

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
