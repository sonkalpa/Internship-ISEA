# Assignment 2 - HOW TO RUN

## Quick WSL Method

From `assignment2/` run:

```bash
python3 run_wsl_assignment2.py
python3 generate_required_screenshots.py
python3 generate_report_pdf.py
python3 check_submission.py
```

This generates/refreshes:

- `server_log.txt`
- `result_table.csv`
- `message_response_log.csv`
- `graphs/mode_vs_response_time.png`
- `graphs/message_size_vs_throughput.png`
- `graphs/message_response_time.png`
- `screenshots/nodes.png`
- `screenshots/net.png`
- `screenshots/pingall.png`
- `screenshots/server_output.png`
- `screenshots/client_output.png`
- `report.pdf`

## Manual Mininet Method

### 1) Start Mininet with required link profile

```bash
sudo mn --link tc,bw=5,delay=50ms
```

### 2) Capture topology screenshots

In Mininet CLI:

- `nodes`
- `net`
- `pingall`

Save as:

- `screenshots/nodes.png`
- `screenshots/net.png`
- `screenshots/pingall.png`

### 3) Start server on h1

```bash
h1 python3 server.py --host 10.0.0.1 --port 5000
```

Save screenshot as `screenshots/server_output.png`.

### 4) Start client on h2

```bash
h2 python3 client.py --server-ip 10.0.0.1
```

Save screenshot as `screenshots/client_output.png`.

### 5) Wireshark screenshots

Filter:

- `tcp.port == 5000`

Required files:

- `screenshots/persistent_handshake.png`
- `screenshots/persistent_data_packets.png`
- `screenshots/persistent_connection_close.png`
- `screenshots/new_connection_multiple_handshakes.png`

### 6) Generate graphs and report PDF

```bash
python3 generate_graphs.py
python3 generate_report_pdf.py
```

### 7) Validate submission files

```bash
python3 check_submission.py
```
