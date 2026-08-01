# Assignment 6 - HOW TO RUN

## Quick WSL Method

From `assignment6/`:

```bash
bash run_wsl_assignment6.sh
```

This generates backend evidence artifacts, GUI/wireshark screenshots, and
`report.pdf`.

## Manual GUI Run

Start server:

```bash
python3 server.py --host 0.0.0.0 --port 5000
```

Run GUI clients:

```bash
python3 client_gui.py
```

Use Mininet topology (`single,5`) for formal execution and take screenshots of
login, connection, main window, broadcast/private messaging, join/leave, and
wireshark verification (`tcp.port == 5000`).

## Validation

```bash
python3 check_submission.py
```
