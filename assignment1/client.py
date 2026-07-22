#!/usr/bin/env python3
"""
Assignment 1 - Reliable UDP Client (Stop-and-Wait)

Sends 10 sequenced UDP messages and waits for ACK|SEQ for each message.
Retransmits when timeout expires.

Produces/updates result_table.csv with one row per loss condition.
"""

import argparse
import csv
import os
import socket
import time

ROLL_NO = "CS-BTC24-08"
NAME = "Sonkalpa Borah"

SERVER_IP = "10.0.0.1"
SERVER_PORT = 5000
TOTAL_MESSAGES = 10

TIMEOUT_BY_LAST_DIGIT = {
    0: 0.5,
    1: 0.5,
    2: 0.7,
    3: 0.7,
    4: 1.0,
    5: 1.0,
    6: 1.2,
    7: 1.2,
    8: 1.5,
    9: 1.5,
}

CSV_COLUMNS = [
    "roll_no",
    "name",
    "loss_percent",
    "timeout",
    "total_messages",
    "total_packets_sent",
    "total_retransmissions",
    "transfer_time_seconds",
    "status",
]


def derive_timeout_from_roll(roll_no: str) -> float:
    digits = [c for c in roll_no if c.isdigit()]
    if not digits:
        return 1.0
    return TIMEOUT_BY_LAST_DIGIT[int(digits[-1])]


def parse_ack(raw: bytes):
    try:
        text = raw.decode(errors="replace").strip()
        part1, part2 = text.split("|", 1)
        if part1 != "ACK":
            return None
        return int(part2)
    except Exception:
        return None


def upsert_result_row(csv_path: str, row: dict):
    rows = []
    if os.path.exists(csv_path):
        with open(csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for existing in reader:
                if all(col in existing for col in CSV_COLUMNS):
                    rows.append(existing)

    replaced = False
    for i, existing in enumerate(rows):
        if existing.get("loss_percent") == str(row["loss_percent"]):
            rows[i] = {k: str(v) for k, v in row.items()}
            replaced = True
            break

    if not replaced:
        rows.append({k: str(v) for k, v in row.items()})

    rows.sort(key=lambda r: float(r["loss_percent"]))

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for item in rows:
            writer.writerow(item)


def main():
    parser = argparse.ArgumentParser(description="Reliable UDP client")
    parser.add_argument("--server-ip", default=SERVER_IP)
    parser.add_argument("--port", type=int, default=SERVER_PORT)
    parser.add_argument("--loss-percent", type=int, required=True)
    parser.add_argument("--timeout", type=float, default=derive_timeout_from_roll(ROLL_NO))
    parser.add_argument("--messages", type=int, default=TOTAL_MESSAGES)
    parser.add_argument("--csv", default="result_table.csv")
    args = parser.parse_args()

    total_packets_sent = 0
    total_retransmissions = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(args.timeout)
        started = time.perf_counter()

        for seq in range(1, args.messages + 1):
            payload = f"{seq}|Message {seq} from h2".encode()

            while True:
                sock.sendto(payload, (args.server_ip, args.port))
                total_packets_sent += 1

                try:
                    data, _ = sock.recvfrom(4096)
                except socket.timeout:
                    total_retransmissions += 1
                    continue

                ack_seq = parse_ack(data)
                if ack_seq == seq:
                    break

                total_retransmissions += 1

        transfer_time = time.perf_counter() - started

    print(f"TOTAL_MESSAGES={args.messages}")
    print(f"LOSS_PERCENT={args.loss_percent}")
    print(f"TIMEOUT={args.timeout}")
    print(f"TOTAL_PACKETS_SENT={total_packets_sent}")
    print(f"TOTAL_RETRANSMISSIONS={total_retransmissions}")
    print(f"TRANSFER_TIME_SECONDS={transfer_time:.6f}")
    print("STATUS=SUCCESS")

    row = {
        "roll_no": ROLL_NO,
        "name": NAME,
        "loss_percent": args.loss_percent,
        "timeout": args.timeout,
        "total_messages": args.messages,
        "total_packets_sent": total_packets_sent,
        "total_retransmissions": total_retransmissions,
        "transfer_time_seconds": round(transfer_time, 6),
        "status": "SUCCESS",
    }
    upsert_result_row(args.csv, row)


if __name__ == "__main__":
    main()
