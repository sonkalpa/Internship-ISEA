# Assignment 4 - HOW TO RUN

## Quick WSL Method

From `assignment4/`:

```bash
bash run_wsl_assignment4.sh
```

Generated artifacts:

- `chat_log.txt`
- `server_events.log`
- `performance_results.csv`
- `capture.pcapng`
- `graphs/clients_vs_delay.png`
- `graphs/clients_vs_throughput.png`
- `screenshots/tcp_handshake.png`
- `screenshots/chat_message.png`
- `screenshots/broadcast_message.png`
- `screenshots/connection_close.png`

## 1) Mininet Topology

```bash
sudo mn --topo single,4
```

Inside Mininet CLI, verify:

```text
nodes
net
pingall
```

## 2) Start Server and Clients (Mininet)

In Mininet CLI:

```text
h1 python3 server.py
h2 python3 client.py --host 10.0.0.1 --username ClientA
h3 python3 client.py --host 10.0.0.1 --username ClientB
h4 python3 client.py --host 10.0.0.1 --username ClientC
```

## 3) Message Logging Requirements

- Server event log format (`server_events.log`):
  - `timestamp,EVENT,username,client_ip`
- Chat log format (`chat_log.txt`):
  - `timestamp,username,message`

## 4) Performance Measurement

Local automated run (outside Mininet):

```bash
python3 run_performance.py
```

This generates `performance_results.csv` with required columns:

- `clients`
- `total_messages`
- `avg_delivery_time_ms`
- `throughput_msgs_per_sec`

## 5) Graph Generation

```bash
python3 generate_graphs.py
```

Generated files:

- `graphs/clients_vs_delay.png`
- `graphs/clients_vs_throughput.png`

## 6) Wireshark Evidence

- Capture on Mininet interface with filter:
  - `tcp.port == 5000`
- Required screenshots:
  - `screenshots/tcp_handshake.png`
  - `screenshots/chat_message.png`
  - `screenshots/broadcast_message.png`
  - `screenshots/connection_close.png`

## 7) Final Report

Use `report_template.md` and export `report.pdf`.

Automated helper:

```bash
python3 generate_report_pdf.py
```

## 8) Submission Validation

```bash
python3 check_submission.py
```
