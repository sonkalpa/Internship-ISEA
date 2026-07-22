# Assignment 1 - Reliable UDP Communication in Mininet

This folder contains the Assignment 1 implementation using stop-and-wait
reliability over UDP.

## Student Details

- Name: Sonkalpa Borah
- Roll No: CS-BTC24-08
- Timeout Rule (last digit 8): `1.5` seconds

## Objective

Build a UDP client-server program in Mininet with:

- sequence numbers
- ACKs
- timeout and retransmission
- duplicate detection at the server

## Files

```text
assignment1/
  client.py
  server.py
  HOW_TO_RUN.md
  run_wsl_assignment1.sh
  report_template.md
  result_table.csv            (generated)
  logs/                       (generated local run logs)
  screenshots/                (add required PNGs)
  report.pdf                  (to be added)
```

## Packet Formats

- Data packet: `SEQ|MESSAGE`
- ACK packet: `ACK|SEQ`

## Mininet Setup

Run one condition at a time:

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=0
```

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=5
```

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=10
```

After starting Mininet, verify:

```bash
nodes
net
pingall
```

## Run Steps

1. In Mininet terminal for `h1`:

```bash
h1 python3 server.py --host 10.0.0.1 --port 5000 --expected 10
```

2. In Mininet terminal for `h2` (match current loss setting):

```bash
h2 python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent 0 --timeout 1.5
```

3. Repeat step 2 for `--loss-percent 5` and `--loss-percent 10` in their
   corresponding Mininet runs.

If `tc/netem` is unavailable (for example on WSL2), use the fallback mode in
`HOW_TO_RUN.md` with:

- server flag: `--reply-delay-ms 30`
- client flag: `--emulate-loss`

Fastest WSL command:

```bash
bash run_wsl_assignment1.sh
```

## Required Console Output

Client prints:

- `TOTAL_MESSAGES=10`
- `LOSS_PERCENT=...`
- `TIMEOUT=...`
- `TOTAL_PACKETS_SENT=...`
- `TOTAL_RETRANSMISSIONS=...`
- `TRANSFER_TIME_SECONDS=...`
- `STATUS=SUCCESS`

Server prints:

- `TOTAL_UNIQUE_MESSAGES_RECEIVED=10`
- `TOTAL_DUPLICATES_DETECTED=...`
- `STATUS=SUCCESS`

## CSV Requirement

`result_table.csv` columns are exactly:

`roll_no,name,loss_percent,timeout,total_messages,total_packets_sent,total_retransmissions,transfer_time_seconds,status`

It must have 3 data rows for loss `0`, `5`, `10`.

## Screenshots to Collect

- `nodes.png`
- `net.png`
- `pingall.png`
- `server_output.png`
- `client_output.png`

## Status

- Code foundation: completed
- Local functional validation (loss 0/5/10 rows): completed
- Local validation logs are stored under `logs/` (loopback run)
- Mininet packet-loss validation + screenshots/report: pending

## Detailed Run Guide

Use `HOW_TO_RUN.md` for step-by-step execution and submission checklist.
