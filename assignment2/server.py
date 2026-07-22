#!/usr/bin/env python3
"""
Assignment 2 - TCP Server
Listens on port 5000, accepts connections from the client (persistent or
new_connection mode), receives messages of the form:

    MSG_ID|MESSAGE_SIZE|MESSAGE_DATA

and replies with:

    ACK|MSG_ID|RECEIVED_SIZE

Every request is logged to server_log.txt as:
    timestamp, client_ip, mode, msg_id, received_size, ack_sent

The wire format does not carry an explicit "mode" field (per the assignment's
fixed message format), so the server infers the mode per-connection:
if more than one message arrives on the same TCP connection before it is
closed, that connection is logged as "persistent"; if only one message is
exchanged before the connection closes, it is logged as "new_connection".
"""

import socket
import threading
import datetime
import argparse

HOST = "0.0.0.0"      # bind on all interfaces (server itself is 10.0.0.1 in Mininet)
PORT = 5000
LOG_FILE = "server_log.txt"
log_lock = threading.Lock()


def log_line(text):
    with log_lock:
        with open(LOG_FILE, "a") as f:
            f.write(text + "\n")


def recv_line(conn, buf):
    """Read from conn until a full '\n'-terminated line is available.
    Returns (line_without_newline, remaining_buffer) or (None, buf) on EOF."""
    while b"\n" not in buf:
        data = conn.recv(4096)
        if not data:
            return None, buf
        buf += data
    line, _, rest = buf.partition(b"\n")
    return line, rest


def handle_client(conn, addr):
    client_ip = addr[0]
    buf = b""
    msg_count = 0
    received_msgs = []  # store (msg_id, size, ack_sent) to log after we know the mode

    while True:
        line, buf = recv_line(conn, buf)
        if line is None:
            break
        try:
            msg_id, msg_size, msg_data = line.decode(errors="replace").split("|", 2)
            received_size = len(msg_data)
        except ValueError:
            # malformed message, ignore
            continue

        ack = f"ACK|{msg_id}|{received_size}\n"
        conn.sendall(ack.encode())
        msg_count += 1
        received_msgs.append((msg_id, received_size))

    # Now that the connection is closed, decide the mode for logging purposes.
    mode = "persistent" if msg_count > 1 else "new_connection"
    timestamp_close = datetime.datetime.now().isoformat()
    for msg_id, received_size in received_msgs:
        log_line(f"{timestamp_close},{client_ip},{mode},{msg_id},{received_size},True")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Assignment 2 TCP server")
    parser.add_argument("--host", default=HOST, help="Host/IP to bind to (default 0.0.0.0)")
    parser.add_argument("--port", type=int, default=PORT, help="Port to listen on (default 5000)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((args.host, args.port))
        s.listen(50)
        print(f"[server] listening on {args.host}:{args.port}")

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()


if __name__ == "__main__":
    main()
