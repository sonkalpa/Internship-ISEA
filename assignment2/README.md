# Assignment 2 - TCP Connection Performance Analysis

This assignment compares TCP communication behavior between:

- `persistent` mode (single connection reused for multiple messages)
- `new_connection` mode (one connection per message)

## Student Details

- Name: Sonkalpa Borah
- Roll No: CS-BTC24-08

## Objective

Measure and compare the following for both modes:

- average response time
- throughput
- packet-level connection behavior

## Files in This Folder

```text
assignment2/
  client.py
  server.py
  generate_graphs.py
  HOW_TO_RUN.md
  result_table.csv
  message_response_log.csv
  server_log.txt
  report.docx
  graphs/
  screenshots/
```

## Quick Local Run

Use this for functional verification on one machine.

1. Start server:

```bash
python3 server.py --host 127.0.0.1 --port 5000
```

2. Run client in a second terminal:

```bash
python3 client.py --server-ip 127.0.0.1
```

3. Generate graphs:

```bash
python3 generate_graphs.py
```

## Mininet Run (for graded network results)

Use the full Mininet and Wireshark workflow in `HOW_TO_RUN.md`.

## Outputs

- `result_table.csv` - summary metrics for each mode and message size
- `message_response_log.csv` - per-message response times
- `graphs/*.png` - generated analysis plots
- `screenshots/*.png` - packet-capture evidence
- `report.docx` - report template/content for final submission

## Notes

- Default test message sizes: 128, 512, and 1024 bytes
- Messages per size per mode: 10
- You can edit `ROLL_NO` and `NAME` in `client.py` before final submission

## Documentation Maintenance

This README is updated whenever assignment contents are changed so documentation matches the latest commit.
