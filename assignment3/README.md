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
  README.md
  HOW_TO_RUN.md
  report_template.md
  packet_comparison_template.csv
  screenshots/                (add required PNGs)
  program_output.txt          (replace template with actual output)
  system_details.txt          (replace template with Linux command output)
  capture.pcapng              (to be generated)
  report.pdf                  (to be added)
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

Use any one or more while the raw socket program is running:

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

## Required Screenshots

- `traffic_generation.png`
- `program_output.png`
- `wireshark_packets.png`
- `comparison_packets.png`

## Remaining Work

- run live experiment and save `program_output.txt`
- collect Wireshark packet comparison table for 5 packets
- complete report sections (header analysis, reflection answers)
- follow detailed Linux checklist in `HOW_TO_RUN.md`
