#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKETS="${1:-20}"
TRAFFIC_COUNT="${2:-40}"

echo "[1/6] Preparing files and dependencies..."
cd "$SCRIPT_DIR"
python3 -m py_compile generate_tcp_traffic.py

echo "[2/6] Capturing system details..."
{
  echo "# uname -a"
  uname -a
  echo
  echo "# gcc --version"
  gcc --version
  echo
  echo "# ip addr"
  ip addr
} > system_details.txt

echo "[3/6] Building raw capture program..."
gcc raw_capture.c -o raw_capture

TSHARK_PID=""
if command -v tshark >/dev/null 2>&1; then
  echo "[4/6] Starting tshark capture to capture.pcapng..."
  sudo tshark -i any -f "tcp" -a duration:20 -w capture.pcapng >/dev/null 2>&1 &
  TSHARK_PID="$!"
else
  echo "[4/6] tshark not found. Skipping automatic pcap capture."
  echo "       You can still capture manually in Wireshark GUI."
fi

echo "[5/6] Generating TCP traffic and collecting raw packet output..."
python3 generate_tcp_traffic.py --count "$TRAFFIC_COUNT" --port 5000 --delay 0.03 --startup-delay 1 \
  > traffic_generation_output.txt 2>&1 &
TRAFFIC_PID="$!"

sudo ./raw_capture "$PACKETS" | tee program_output.txt
wait "$TRAFFIC_PID" || true

if [[ -n "$TSHARK_PID" ]]; then
  wait "$TSHARK_PID" || true
fi

echo "[6/6] Done. Generated artifacts:"
echo "  - program_output.txt"
echo "  - system_details.txt"
echo "  - traffic_generation_output.txt"
if [[ -f capture.pcapng ]]; then
  echo "  - capture.pcapng"
fi

echo
echo "Next: fill packet_comparison_template.csv using Wireshark + program output,"
echo "then take required screenshots in screenshots/."
