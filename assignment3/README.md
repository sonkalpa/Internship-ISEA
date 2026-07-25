# Assignment 3 - Raw Socket Packet Analysis

This folder contains the Assignment 3 implementation for raw packet capture and
protocol analysis.

## Student Details

- Name: Sonkalpa Borah
- Roll No: CS-BTC24-08
- Last digit: `8`
- Assigned protocol: `TCP` (as per assignment mapping 7-9 -> TCP)

## Objective

Capture packets using Linux raw sockets, extract IP and TCP header fields,
generate traffic, compare with Wireshark, and document analysis.

## Files

```text
assignment3/
  raw_capture.c
  generate_tcp_traffic.py
  README.md
  HOW_TO_RUN.md
  run_wsl_assignment3.sh
  check_submission.py
  report_template.md
  generate_report_pdf.py
  packet_comparison_template.csv
  screenshots/                (required PNGs)
  program_output.txt          (captured)
  system_details.txt          (captured)
  traffic_generation_output.txt
  capture.pcapng
  report.md
  report.pdf
```

## Implemented Program Behavior

`raw_capture.c`:

- opens a raw socket for the assigned protocol
- captures at least 20 packets (default)
- prints required fields per packet:
  - `SRC_IP`, `DST_IP`, `PROTOCOL`, `PROTOCOL_NO`, `TTL`, `PACKET_SIZE`
- prints TCP-specific fields:
  - `TCP_SRC_PORT`, `TCP_DST_PORT`, `TCP_FLAGS`
- includes one extra IP header field for enhancement:
  - `IP_IDENTIFICATION`

## Compile and Run (Linux)

```bash
gcc raw_capture.c -o raw_capture
sudo ./raw_capture
```

To capture a custom number of packets:

```bash
sudo ./raw_capture 30
```

## Example Traffic Generation (TCP)

Preferred local generator (deterministic):

```bash
python3 generate_tcp_traffic.py --count 40 --port 5000 --delay 0.03
```

Alternative commands while raw socket program is running:

```bash
nc -v 127.0.0.1 5000
```

```bash
curl http://example.com
```

```bash
ssh 127.0.0.1
```

## Wireshark Verification

- capture on the same interface used for traffic
- filter examples:
  - `tcp`
  - `ip.proto == 6`
- save capture file as `capture.pcapng`
- this repository run used `dumpcap` for capture because `tshark` was not
  available in the WSL image

## Required Screenshots

- `traffic_generation.png`
- `program_output.png`
- `wireshark_packets.png`
- `comparison_packets.png`

For replacing generated screenshots with original captures from your own run,
follow `ORIGINAL_SCREENSHOT_STEPS.md`.

## Completed Artifacts

- captured 20 TCP packets in `program_output.txt`
- generated TCP traffic evidence in `traffic_generation_output.txt`
- captured network trace in `capture.pcapng`
- filled 5-row comparison in `packet_comparison_template.csv`
- completed report in `report.md` and `report.pdf`
- generated required screenshot files in `screenshots/`

## Fast WSL Command

```bash
bash run_wsl_assignment3.sh
```

## Submission Check

Run this local checker before final zip submission:

```bash
python3 check_submission.py
```
