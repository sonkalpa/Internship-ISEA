# How to run this on Mininet (do this yourself — I can't run Mininet here)

This sandbox has no root/network-namespace access, so I could not start Mininet
or capture real Wireshark traffic. Everything below was written and
**functionally tested over a local TCP loopback connection** (I ran server.py
and client.py against each other and confirmed correct logs, CSVs, and
graphs — see the sample files included). You just need to run the same two
scripts inside your Mininet VM to get the real, graded numbers and captures.

## 1. Edit client.py
Open `client.py` and set:
```python
ROLL_NO = "your roll number"
NAME = "your name"
```

## 2. Start Mininet with the required link shaping
```bash
sudo mn --link tc,bw=5,delay=50ms
```
Inside the Mininet CLI, verify the topology (screenshot each command):
```
mininet> nodes
mininet> net
mininet> pingall
```

## 3. Start the server on h1
Open a terminal on h1 (or use `xterm h1` from the Mininet CLI):
```bash
h1 python3 server.py --host 10.0.0.1 --port 5000
```
(or from an xterm on h1: `python3 server.py --host 10.0.0.1 --port 5000`)
Screenshot the server terminal after it starts → `server_output.png`.

## 4. Start Wireshark capture on h1 (or on s1's interface)
Before running the client, start a capture with filter:
```
tcp.port == 5000
```
Keep it running through the whole client run so you capture both modes.

## 5. Run the client on h2
```bash
h2 python3 client.py --server-ip 10.0.0.1
```
This automatically runs all 6 combinations (2 modes × 3 sizes), 10 messages
each, and writes:
- `message_response_log.csv`
- `result_table.csv`

Screenshot the client terminal output → `client_output.png`.

## 6. Stop the Wireshark capture and pull out the 4 required screenshots
From the capture, save:
- `persistent_handshake.png` — the SYN/SYN-ACK/ACK at the start of the persistent run
- `persistent_data_packets.png` — the repeated request/ACK exchanges on that one connection
- `persistent_connection_close.png` — the single FIN/ACK teardown
- `new_connection_multiple_handshakes.png` — repeated SYN/SYN-ACK/ACK (and FIN/ACK) pairs, one per message

Tip: sort by tcp.stream in Wireshark — persistent mode will show as a single
stream number across the 10 messages; new_connection mode will show 10
different stream numbers.

## 7. Generate the graphs
Still inside Mininet (or in your normal shell — this step doesn't touch the
network), from the same folder as the CSVs:
```bash
pip install matplotlib   # if not already installed
python3 generate_graphs.py
```
This creates `graphs/mode_vs_response_time.png`,
`graphs/message_size_vs_throughput.png`, and
`graphs/message_response_time.png`.

## 8. Fill in report.docx
Open `report.docx` — the topology explanation, TCP handshake explanation,
persistent-vs-new-connection explanation, and answers to the conceptual
questions are already written. Replace every `[bracketed red placeholder]`
with your real result table, your 3 graphs, your 9 screenshots, your name,
and roll number, then export/save as `report.pdf`.

## 9. Assemble the submission folder
```
ROLLNO_NAME_TCP_ASSIGNMENT/
├── server.py
├── client.py
├── server_log.txt
├── result_table.csv
├── message_response_log.csv
├── graphs/
│   ├── mode_vs_response_time.png
│   ├── message_size_vs_throughput.png
│   └── message_response_time.png
├── screenshots/
│   ├── nodes.png, net.png, pingall.png
│   ├── server_output.png, client_output.png
│   ├── persistent_handshake.png
│   ├── persistent_data_packets.png
│   ├── persistent_connection_close.png
│   └── new_connection_multiple_handshakes.png
└── report.pdf
```
Then zip it as `ROLLNO_NAME_TCP_ASSIGNMENT.zip`.

## What's already done for you vs. what you must do
| Done for you | You must do |
|---|---|
| server.py, client.py (tested end-to-end) | Run them inside actual Mininet with tc bw=5,delay=50ms |
| generate_graphs.py (tested, produces correct plot types) | Re-run it on your real CSVs |
| report.docx with topology/TCP/mode explanations and question answers pre-written | Take the actual Wireshark screenshots and Mininet CLI screenshots; fill in your real result numbers, your name/roll no |
| Sample result_table.csv / message_response_log.csv (from a loopback test, NOT real network data) | Replace these with your real Mininet-generated CSVs |
