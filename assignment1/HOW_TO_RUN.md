# Assignment 1 - HOW TO RUN

This file provides two execution modes:

- Mode A: native Mininet `tc/netem` (preferred where available)
- Mode B: WSL-safe fallback using application-level loss emulation

Use Mode B when `sch_netem` is unavailable and `--link tc,...` fails.

## Mode A (Preferred): Mininet `tc/netem`

Run each profile in a fresh Mininet session:

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=0
```

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=5
```

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=10
```

Inside Mininet:

```bash
nodes
net
pingall
```

Run server/client:

```bash
h1 python3 server.py --host 10.0.0.1 --port 5000 --expected 10
```

```bash
h2 python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent <LOSS> --timeout 1.5
```

Replace `<LOSS>` with `0`, `5`, and `10` in each profile run.

## Mode B (WSL Fallback): No `tc/netem` required

### Step 1: Start default Mininet

```bash
sudo mn
```

### Step 2: Verify topology

```bash
nodes
net
pingall
```

### Step 3: Open host terminals

```bash
xterm h1 h2
```

### Step 4: In `h1` terminal, run server with artificial 30ms ACK delay

```bash
cd /mnt/e/ASSIGNMENT/Internship-ISEA/assignment1
python3 server.py --host 10.0.0.1 --port 5000 --expected 10 --reply-delay-ms 30
```

### Step 5: In `h2` terminal, run client profile for LOSS=0

```bash
cd /mnt/e/ASSIGNMENT/Internship-ISEA/assignment1
python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent 0 --timeout 1.5 --emulate-loss --seed 2408
```

### Step 6: Run LOSS=5 profile (same Mininet session is fine)

```bash
python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent 5 --timeout 1.5 --emulate-loss --seed 2408
```

### Step 7: Run LOSS=10 profile

```bash
python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent 10 --timeout 1.5 --emulate-loss --seed 2408
```

### Step 8: Stop Mininet

In Mininet CLI:

```bash
exit
```

## Required screenshots

Save these under `screenshots/`:

- `nodes.png`
- `net.png`
- `pingall.png`
- `server_output.png`
- `client_output.png`

## CSV validation

`result_table.csv` must keep this exact header:

`roll_no,name,loss_percent,timeout,total_messages,total_packets_sent,total_retransmissions,transfer_time_seconds,status`

It must contain 3 rows for loss `0`, `5`, and `10`.

## Final report

Use `report_template.md` and create:

- `report.pdf` (required)
- optional editable source: `report.docx`
