# Assignment 3 - HOW TO RUN

This guide includes a WSL-friendly command flow.

## Quickest Working Method (WSL/Linux)

From `assignment3/` run:

```bash
bash run_wsl_assignment3.sh
```

Optional arguments:

```bash
bash run_wsl_assignment3.sh <packet_count> <traffic_connections>
```

Example:

```bash
bash run_wsl_assignment3.sh 25 60
```

This command will generate:

- `program_output.txt`
- `system_details.txt`
- `traffic_generation_output.txt`
- `capture.pcapng` (if `tshark` is available)

## Manual Method (step-by-step)

### 1) Compile

```bash
gcc raw_capture.c -o raw_capture
```

### 2) Capture system details

```bash
uname -a > system_details.txt
gcc --version >> system_details.txt
ip addr >> system_details.txt
```

### 3) Start traffic generator in one terminal

```bash
python3 generate_tcp_traffic.py --count 40 --port 5000 --delay 0.03
```

### 4) Start raw capture in another terminal

```bash
sudo ./raw_capture 20 | tee program_output.txt
```

### 5) Wireshark/tshark capture

- GUI Wireshark filter: `tcp` or `ip.proto == 6`
- Save file as `capture.pcapng`

If you prefer terminal capture:

```bash
sudo tshark -i any -f "tcp" -a duration:20 -w capture.pcapng
```

### 6) Fill comparison template

Fill 5 rows in `packet_comparison_template.csv` from Wireshark + program output.

### 7) Take required screenshots

- `screenshots/traffic_generation.png`
- `screenshots/program_output.png`
- `screenshots/wireshark_packets.png`
- `screenshots/comparison_packets.png`

### 8) Final report

Use `report_template.md` and export:

- `report.pdf`
- optional: `report.docx`
