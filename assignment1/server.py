#!/usr/bin/env python3
"""
Assignment 1 - Reliable UDP Server

Receives packets in format:
  SEQ|MESSAGE

Sends ACK in format:
  ACK|SEQ

Tracks unique messages and duplicates.
"""

import argparse
import socket

HOST = "0.0.0.0"
PORT = 5000


def parse_message(raw: bytes):
    try:
        text = raw.decode(errors="replace").strip()
        seq_text, message = text.split("|", 1)
        return int(seq_text), message
    except Exception:
        return None, None


def main():
    parser = argparse.ArgumentParser(description="Reliable UDP server")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--expected", type=int, default=10, help="Expected unique messages")
    args = parser.parse_args()

    seen = set()
    duplicates = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((args.host, args.port))
        print(f"[server] listening on {args.host}:{args.port}")

        while len(seen) < args.expected:
            data, addr = sock.recvfrom(4096)
            seq, message = parse_message(data)
            if seq is None:
                continue

            is_duplicate = seq in seen
            if is_duplicate:
                duplicates += 1
            else:
                seen.add(seq)

            ack = f"ACK|{seq}".encode()
            sock.sendto(ack, addr)

            print(
                f"[server] src={addr[0]} seq={seq} duplicate={is_duplicate} "
                f"payload_len={len(message)}"
            )

    print(f"TOTAL_UNIQUE_MESSAGES_RECEIVED={len(seen)}")
    print(f"TOTAL_DUPLICATES_DETECTED={duplicates}")
    print("STATUS=SUCCESS")


if __name__ == "__main__":
    main()
