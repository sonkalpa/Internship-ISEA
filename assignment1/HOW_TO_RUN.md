# Assignment 1 - HOW TO RUN

This guide is written for Mininet evaluation and final evidence collection.

## 1) Open Mininet with required loss profile

Run these 3 cases separately:

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=0
```

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=5
```

```bash
sudo mn --link tc,bw=5,delay=30ms,loss=10
```

## 2) Verify topology in each run

```bash
nodes
net
pingall
```

Take screenshots for:

- `screenshots/nodes.png`
- `screenshots/net.png`
- `screenshots/pingall.png`

## 3) Run server and client

In Mininet terminal:

```bash
h1 python3 server.py --host 10.0.0.1 --port 5000 --expected 10
```

In another Mininet terminal:

```bash
h2 python3 client.py --server-ip 10.0.0.1 --port 5000 --loss-percent <LOSS> --timeout 1.5
```

Use `<LOSS>` as `0`, `5`, `10` for the corresponding Mininet run.

Take screenshots for:

- `screenshots/server_output.png`
- `screenshots/client_output.png`

## 4) Validate CSV output

`result_table.csv` must contain exactly these columns:

`roll_no,name,loss_percent,timeout,total_messages,total_packets_sent,total_retransmissions,transfer_time_seconds,status`

It should contain exactly 3 rows for loss `0`, `5`, and `10`.

## 5) Final report

Use `report_template.md` as outline and prepare final report as PDF.

Recommended final file names:

- `report.pdf` (submission)
- optional editable source: `report.docx`

## 6) Folder checklist before submission

- `client.py`
- `server.py`
- `result_table.csv`
- `screenshots/` (required PNG files)
- `report.pdf`
