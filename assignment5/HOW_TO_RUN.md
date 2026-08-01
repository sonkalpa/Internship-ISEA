# Assignment 5 - HOW TO RUN

## Quick WSL Method

From `assignment5/`:

```bash
bash run_wsl_assignment5.sh
```

This generates:

- `chat_history.csv`
- `performance_results.csv`
- `graphs/clients_vs_delay.png`
- `graphs/clients_vs_throughput.png`
- `graphs/message_type_distribution.png`
- `screenshots/client_connection.png`
- `screenshots/broadcast_message.png`
- `screenshots/private_message.png`
- `screenshots/client_disconnect.png`
- `screenshots/tcp_connection_termination.png`
- `report.md`
- `report.pdf`

## Manual Mininet Method

```bash
sudo mn --topo single,5
```

Run server on `h1` and clients on `h2..h5` using `server.py` and `client.py`.
Use display filter `tcp.port == 5000` in Wireshark for verification screenshots.

## Validation

```bash
python3 check_submission.py
```
