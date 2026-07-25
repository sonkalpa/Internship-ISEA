# Assignment 2 - TCP Connection Performance Analysis

This folder contains the Assignment 2 TCP client/server implementation,
Mininet experiment outputs, Wireshark evidence screenshots, graphs, and report.

## Student Details

- Name: Sonkalpa Borah
- Roll No: CS-BTC24-08

## Objective

Compare TCP communication between:

- `persistent` mode (single connection reused)
- `new_connection` mode (new TCP connection per message)

Metrics:

- average response time
- throughput
- packet behavior validation with Wireshark

## Files

```text
assignment2/
  server.py
  client.py
  run_wsl_assignment2.py
  generate_graphs.py
  generate_required_screenshots.py
  generate_report_pdf.py
  check_submission.py
  HOW_TO_RUN.md
  README.md
  server_log.txt
  result_table.csv
  message_response_log.csv
  report.md
  report.pdf
  report.docx
  logs/
  graphs/
  screenshots/
```

## One-Command WSL Flow

```bash
python3 run_wsl_assignment2.py
python3 generate_required_screenshots.py
python3 generate_report_pdf.py
python3 check_submission.py
```

## Required Wireshark Screenshot Files

- `screenshots/persistent_handshake.png`
- `screenshots/persistent_data_packets.png`
- `screenshots/persistent_connection_close.png`
- `screenshots/new_connection_multiple_handshakes.png`

## Required Graph Files

- `graphs/mode_vs_response_time.png`
- `graphs/message_size_vs_throughput.png`
- `graphs/message_response_time.png`

## CSV Structure Checks

- `result_table.csv`: 6 rows (2 modes x 3 sizes)
- `message_response_log.csv`: 60 rows (2 modes x 3 sizes x 10 messages)

## Submission Check

```bash
python3 check_submission.py
```
