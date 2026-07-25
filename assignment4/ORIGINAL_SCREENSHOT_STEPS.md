# Assignment 4 - Original Screenshot Steps

Use this checklist to capture original Wireshark screenshots from your own run
and replace current generated images.

## 1) Re-run Assignment 4 in WSL/Ubuntu

From `assignment4/`:

```bash
bash run_wsl_assignment4.sh
```

This regenerates:

- `capture.pcapng`
- `chat_log.txt`
- `performance_results.csv`

## 2) Open capture in Wireshark

Open:

- `E:\ASSIGNMENT\Internship-ISEA\assignment4\capture.pcapng`

Display filter:

- `tcp.port == 5000`

## 3) Capture required original screenshots

Save with exact names:

- `screenshots/tcp_handshake.png`
- `screenshots/chat_message.png`
- `screenshots/broadcast_message.png`
- `screenshots/connection_close.png`

Helpful frame references from current capture:

- Handshake: frames `1-2-5` (SYN, SYN, SYN-ACK) and ACK around frames `9-10`
- Chat message packet (client -> server payload): frame `13`
- Broadcast payloads (server -> clients): frames `43`, `47`, `51`
- Connection close (`FIN,ACK`): frames `325`, `326`, `327`

## 4) Recommended screenshot content

For each screenshot, include:

- packet list pane
- selected packet details pane (TCP flags/ports visible)
- display filter bar (`tcp.port == 5000`)

## 5) Replace files in place

Overwrite files in `assignment4/screenshots/` using the same filenames to keep
the folder submission-ready.
