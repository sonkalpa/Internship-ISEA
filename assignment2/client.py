#!/usr/bin/env python3
"""
Assignment 2 - TCP Client

Supports two modes:
  persistent      -> open one TCP connection, send all messages over it, then close.
  new_connection  -> open a brand-new TCP connection for every single message.

For each message size in MESSAGE_SIZES, sends NUM_MESSAGES messages in both
modes, measuring per-message response time (time between sending the request
and receiving the ACK) and overall throughput.

Produces:
  message_response_log.csv  (60 rows: 2 modes x 3 sizes x 10 messages)
  result_table.csv          (6 rows: 2 modes x 3 sizes)

Edit ROLL_NO and NAME below before running.
"""

import socket
import time
import csv
import argparse

# ---- EDIT THESE BEFORE SUBMISSION -----------------------------------------
ROLL_NO = "CS-BTC24-08"
NAME = "Sonkalpa Borah"
# -----------------------------------------------------------------------------

SERVER_IP = "10.0.0.1"
SERVER_PORT = 5000
MESSAGE_SIZES = [128, 512, 1024]
NUM_MESSAGES = 10
BANDWIDTH_MBPS = 5
DELAY_MS = 50


def build_message(msg_id, size):
    # size = total size of the MESSAGE_DATA field, filled with 'A'
    data = "A" * size
    return f"{msg_id}|{size}|{data}\n".encode()


def recv_line(sock, buf):
    while b"\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            return None, buf
        buf += chunk
    line, _, rest = buf.partition(b"\n")
    return line, rest


def run_persistent(size, results_log):
    """Open ONE connection, send NUM_MESSAGES messages over it, then close."""
    response_times = []
    total_bytes = 0
    start_total = time.perf_counter()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        buf = b""
        for i in range(1, NUM_MESSAGES + 1):
            msg = build_message(i, size)
            t0 = time.perf_counter()
            s.sendall(msg)
            line, buf = recv_line(s, buf)
            t1 = time.perf_counter()
            rt = t1 - t0
            response_times.append(rt)
            total_bytes += len(msg)
            results_log.append(("persistent", size, i, rt))
        # connection closes automatically on exit from `with` block

    total_time = time.perf_counter() - start_total
    return response_times, total_bytes, total_time


def run_new_connection(size, results_log):
    """Open a NEW connection for every message, close it after the ACK."""
    response_times = []
    total_bytes = 0
    start_total = time.perf_counter()

    for i in range(1, NUM_MESSAGES + 1):
        msg = build_message(i, size)
        t0 = time.perf_counter()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            buf = b""
            s.sendall(msg)
            line, buf = recv_line(s, buf)
        t1 = time.perf_counter()
        rt = t1 - t0
        response_times.append(rt)
        total_bytes += len(msg)
        results_log.append(("new_connection", size, i, rt))

    total_time = time.perf_counter() - start_total
    return response_times, total_bytes, total_time


def main():
    global SERVER_IP
    parser = argparse.ArgumentParser(description="Assignment 2 TCP client")
    parser.add_argument("--server-ip", default=SERVER_IP)
    args = parser.parse_args()
    SERVER_IP = args.server_ip

    detailed_log = []   # (mode, size, msg_number, response_time)
    summary_rows = []    # for result_table.csv

    for mode, run_fn in [("persistent", run_persistent), ("new_connection", run_new_connection)]:
        for size in MESSAGE_SIZES:
            response_times, total_bytes, total_time = run_fn(size, detailed_log)
            avg_rt = sum(response_times) / len(response_times)
            throughput = total_bytes / total_time if total_time > 0 else 0
            summary_rows.append({
                "roll_no": ROLL_NO,
                "name": NAME,
                "mode": mode,
                "bandwidth_mbps": BANDWIDTH_MBPS,
                "delay_ms": DELAY_MS,
                "message_size_bytes": size,
                "total_messages": NUM_MESSAGES,
                "average_response_time_seconds": round(avg_rt, 6),
                "throughput_bytes_per_second": round(throughput, 2),
                "status": "success",
            })
            print(f"[client] mode={mode} size={size}B avg_rt={avg_rt:.4f}s "
                  f"throughput={throughput:.2f} B/s")

    # write message_response_log.csv (60 rows)
    with open("message_response_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["roll_no", "name", "mode", "message_size_bytes",
                          "message_number", "response_time_seconds"])
        for mode, size, msg_number, rt in detailed_log:
            writer.writerow([ROLL_NO, NAME, mode, size, msg_number, round(rt, 6)])

    # write result_table.csv (6 rows)
    with open("result_table.csv", "w", newline="") as f:
        fieldnames = ["roll_no", "name", "mode", "bandwidth_mbps", "delay_ms",
                      "message_size_bytes", "total_messages",
                      "average_response_time_seconds", "throughput_bytes_per_second",
                      "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print("[client] Done. Wrote message_response_log.csv and result_table.csv")


if __name__ == "__main__":
    main()
