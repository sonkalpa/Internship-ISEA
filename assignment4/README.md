# Assignment 4 - Multi-Client Chat Server using TCP

This folder contains the Assignment 4 implementation for a concurrent TCP chat
server, multi-client messaging, Mininet execution artifacts, and performance
analysis.

## Student Details

- Name: Sonkalpa Borah
- Roll No: CS-BTC24-08

## Assignment Objectives

- Build a threaded TCP chat server on port `5000`.
- Register client usernames and broadcast messages.
- Log connect/disconnect events and chat messages.
- Measure performance for 1, 2, and 3 clients.
- Generate required performance graphs.

## Files

```text
assignment4/
  server.py
  client.py
  run_performance.py
  run_wsl_assignment4.py
  run_wsl_assignment4.sh
  generate_graphs.py
  generate_screenshots.py
  generate_report_pdf.py
  check_submission.py
  README.md
  HOW_TO_RUN.md
  report_template.md
  chat_log.txt
  server_events.log
  performance_results.csv
  capture.pcapng
  report.md
  report.pdf
  system_details.txt
  run_info.txt
  logs/
  graphs/
    clients_vs_delay.png
    clients_vs_throughput.png
  screenshots/
    tcp_handshake.png
    chat_message.png
    broadcast_message.png
    connection_close.png
```

## Quick Local Run (WSL/Linux)

Terminal 1:

```bash
python3 server.py
```

Terminal 2:

```bash
python3 client.py --username ClientA
```

Terminal 3:

```bash
python3 client.py --username ClientB
```

## Performance Run

```bash
python3 run_performance.py
python3 generate_graphs.py
```

This generates `performance_results.csv` and PNG files in `graphs/`.

## One-Command WSL Run

```bash
bash run_wsl_assignment4.sh
```

This executes Mininet flow, collects logs/capture, and generates graphs plus
required screenshot artifacts.

## Mininet Mapping (Assignment Requirement)

- `h1`: `python3 server.py`
- `h2`: `python3 client.py --username ClientA`
- `h3`: `python3 client.py --username ClientB`
- `h4`: `python3 client.py --username ClientC`

## Status

- Mininet run completed on WSL with LinuxBridge backend.
- Performance CSV generated for 1/2/3 clients.
- Graphs, packet evidence screenshots, and report generated.

## Submission Check

```bash
python3 check_submission.py
```
