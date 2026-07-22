# Assignment 1 - HOW TO RUN

This guide includes a WSL-friendly flow that works from Ubuntu terminal on
Windows, even when `tc/netem` is unavailable.

## Quickest Working Method on WSL

Run this one command from `assignment1/`:

```bash
bash run_wsl_assignment1.sh
```

It will:

- run loss profiles `0`, `5`, `10` sequentially
- generate `result_table.csv`
- generate logs under `logs/`

## Manual WSL Method (No `xterm`, no `tc/netem`)

Use this if you want full control and visible output in one terminal.

### 1) Start Mininet

```bash
sudo mn
```

### 2) Verify topology

```bash
nodes
net
pingall
```

### 3) Start server on `h1` in background

```bash
h1 bash -lc "cd /mnt/e/ASSIGNMENT/Internship-ISEA/assignment1 && python3 server.py --host 10.0.0.1 --port 5000 --expected 10 --reply-delay-ms 30 > logs/server_loss0.out.txt 2>&1 &"
```

### 4) Run client on `h2` for loss 0

```bash
h2 bash -lc "cd /mnt/e/ASSIGNMENT/Internship-ISEA/assignment1 && python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent 0 --timeout 1.5 --emulate-loss --seed 2408 > logs/client_loss0.txt 2>&1"
```

### 5) Restart server and run loss 5

```bash
h1 pkill -f "python3 server.py" || true
h1 bash -lc "cd /mnt/e/ASSIGNMENT/Internship-ISEA/assignment1 && python3 server.py --host 10.0.0.1 --port 5000 --expected 10 --reply-delay-ms 30 > logs/server_loss5.out.txt 2>&1 &"
h2 bash -lc "cd /mnt/e/ASSIGNMENT/Internship-ISEA/assignment1 && python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent 5 --timeout 1.5 --emulate-loss --seed 2408 > logs/client_loss5.txt 2>&1"
```

### 6) Restart server and run loss 10

```bash
h1 pkill -f "python3 server.py" || true
h1 bash -lc "cd /mnt/e/ASSIGNMENT/Internship-ISEA/assignment1 && python3 server.py --host 10.0.0.1 --port 5000 --expected 10 --reply-delay-ms 30 > logs/server_loss10.out.txt 2>&1 &"
h2 bash -lc "cd /mnt/e/ASSIGNMENT/Internship-ISEA/assignment1 && python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent 10 --timeout 1.5 --emulate-loss --seed 2408 > logs/client_loss10.txt 2>&1"
```

### 7) Exit Mininet

```bash
exit
```

## Native Mininet `tc/netem` Method (If available)

Use this only if your system supports `sch_netem`:

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=0
```

Repeat for loss `5` and `10`.

## Required screenshots

Save these under `screenshots/`:

- `nodes.png`
- `net.png`
- `pingall.png`
- `server_output.png`
- `client_output.png`

## CSV validation

`result_table.csv` header must be exactly:

`roll_no,name,loss_percent,timeout,total_messages,total_packets_sent,total_retransmissions,transfer_time_seconds,status`

It must contain 3 rows for loss `0`, `5`, and `10`.

## Final report

Use `report_template.md` and create:

- `report.pdf` (required)
- optional editable source: `report.docx`
