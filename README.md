# Internship-ISEA

Repository for internship assignments and supporting artifacts.

## Contents

- `assignment2/` - TCP connection performance analysis (persistent vs new connection)

## Assignment 2 at a Glance

`assignment2/` contains:

- Python TCP client and server
- Generated CSV logs and summary tables
- Graphs for required analysis
- Packet-capture screenshots
- Assignment report draft (`report.docx`)

See `assignment2/README.md` for complete details and commands.

## Run Assignment 2

From the `assignment2/` directory:

```bash
python3 server.py --host 127.0.0.1 --port 5000
python3 client.py --server-ip 127.0.0.1
python3 generate_graphs.py
```

## Update Policy

This repository README and each assignment README are updated whenever assignment files are changed so the documentation stays in sync with the latest commit.
