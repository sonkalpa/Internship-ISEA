#!/usr/bin/env python3
"""Multi-client TCP chat server for Assignment 4."""

import argparse
import datetime as dt
import socket
import threading
from pathlib import Path


def now_time() -> str:
    return dt.datetime.now().strftime("%H:%M:%S")


class ChatServer:
    def __init__(self, host: str, port: int, chat_log: Path, event_log: Path):
        self.host = host
        self.port = port
        self.chat_log = chat_log
        self.event_log = event_log
        self.clients: dict[socket.socket, tuple[str, str]] = {}
        self.lock = threading.Lock()

    def write_event(self, event: str, username: str, client_ip: str) -> None:
        line = f"{now_time()},{event},{username},{client_ip}\n"
        with self.event_log.open("a", encoding="utf-8") as f:
            f.write(line)

    def write_chat(self, username: str, message: str) -> None:
        line = f"{now_time()},{username},{message}\n"
        with self.chat_log.open("a", encoding="utf-8") as f:
            f.write(line)

    def broadcast(self, message: str) -> None:
        payload = (message + "\n").encode("utf-8", errors="replace")
        dead_clients: list[socket.socket] = []

        with self.lock:
            for conn in list(self.clients.keys()):
                try:
                    conn.sendall(payload)
                except OSError:
                    dead_clients.append(conn)

            for conn in dead_clients:
                username, client_ip = self.clients.pop(conn, ("UNKNOWN", "0.0.0.0"))
                self.write_event("DISCONNECTED", username, client_ip)
                try:
                    conn.close()
                except OSError:
                    pass

    def handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        client_ip = addr[0]
        username = "UNKNOWN"

        try:
            rfile = conn.makefile("r", encoding="utf-8", newline="\n")
            first_line = rfile.readline()
            if not first_line:
                conn.close()
                return

            username = first_line.strip() or f"USER_{addr[1]}"

            with self.lock:
                self.clients[conn] = (username, client_ip)

            self.write_event("CONNECTED", username, client_ip)

            for line in rfile:
                message = line.strip()
                if not message:
                    continue

                self.write_chat(username, message)
                self.broadcast(f"[{username}] {message}")

        except Exception:
            pass
        finally:
            with self.lock:
                self.clients.pop(conn, None)
            self.write_event("DISCONNECTED", username, client_ip)
            try:
                conn.close()
            except OSError:
                pass

    def start(self) -> None:
        self.chat_log.parent.mkdir(parents=True, exist_ok=True)
        self.event_log.parent.mkdir(parents=True, exist_ok=True)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen(30)
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = server.accept()
                th = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                th.start()


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-client TCP chat server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--chat-log", default="chat_log.txt")
    parser.add_argument("--event-log", default="server_events.log")
    args = parser.parse_args()

    server = ChatServer(
        host=args.host,
        port=args.port,
        chat_log=Path(args.chat_log),
        event_log=Path(args.event_log),
    )
    server.start()


if __name__ == "__main__":
    main()
