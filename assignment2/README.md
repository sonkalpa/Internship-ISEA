# Assignment 2 - TCP Connection Performance Analysis

This folder contains the complete deliverables for **Assignment 2** (`ASSIGNMENT/assignment2`).

## Student Details

- **Name:** Sonkalpa Borah
- **Roll No:** CS-BTC24-08

## Assignment Scope

The objective is to compare TCP communication behavior and performance between:

- **Persistent connection mode** (single connection reused for multiple messages)
- **New connection mode** (fresh connection for each message)

Measurements include:

- Average response time
- Throughput
- Packet-level behavior from capture analysis

## Folder Structure (`ASSIGNMENT/assignment2`)

```text
assignment2/
  client.py
  server.py
  generate_graphs.py
  result_table.csv
  message_response_log.csv
  server_log.txt
  report.docx
  graphs/
    mode_vs_response_time.png
    message_size_vs_throughput.png
    message_response_time.png
  screenshots/
    persistent_handshake.png
    persistent_data_packets.png
    persistent_connection_close.png
    new_connection_multiple_handshakes.png
```

## How To Run (Assignment 2)

From `ASSIGNMENT/assignment2` (or this folder if copied standalone):

1. Start server:

```bash
python3 server.py --host 127.0.0.1 --port 5000
```

2. Run client in another terminal:

```bash
python3 client.py --server-ip 127.0.0.1
```

3. Generate plots:

```bash
python3 generate_graphs.py
```

## Generated Outputs

- `result_table.csv`: 6 summary rows (2 modes x 3 message sizes)
- `message_response_log.csv`: per-message timing log
- `graphs/*.png`: required analysis plots
- `screenshots/*.png`: packet-capture evidence
- `report.docx`: final written report for Assignment 2

## Environment Note

Execution was completed in WSL with local loopback capture where Mininet/OVS kernel features were limited in the host environment. The analysis and output files in `ASSIGNMENT/assignment2` are complete and submission-ready.
