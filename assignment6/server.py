#!/usr/bin/env python3
"""Assignment 6 server.

Reuses Assignment 5 server behavior with minimal changes.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import socket
import threading
from pathlib import Path


class ChatServer:
    def __init__(self, host: str, port: int, history_file: Path, event_file: Path) -> None:
        self.host = host
        self.port = port
        self.history_file = history_file
        self.event_file = event_file
        self.clients: dict[str, socket.socket] = {}
        self.lock = threading.Lock()

        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.event_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.history_file.exists():
            with self.history_file.open("w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerow(["timestamp", "sender", "receiver", "message_type", "message"])

    @staticmethod
    def now() -> str:
        return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_event(self, line: str) -> None:
        with self.event_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def append_history(self, sender: str, receiver: str, message_type: str, message: str) -> None:
        with self.history_file.open("a", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow([self.now(), sender, receiver, message_type, message])

    @staticmethod
    def send_line(conn: socket.socket, msg: str) -> None:
        conn.sendall((msg + "\n").encode("utf-8", errors="replace"))

    def broadcast_system(self, msg: str, exclude: str = "") -> None:
        for uname, conn in list(self.clients.items()):
            if uname == exclude:
                continue
            try:
                self.send_line(conn, msg)
            except OSError:
                continue

    def send_online_list(self) -> None:
        payload = "ONLINE_USERS:" + ",".join(sorted(self.clients.keys()))
        for conn in list(self.clients.values()):
            try:
                self.send_line(conn, payload)
            except OSError:
                continue

    def send_last_five(self, username: str, conn: socket.socket) -> None:
        sent = []
        with self.history_file.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if row.get("sender") == username:
                    sent.append(row)
        for row in sent[-5:]:
            self.send_line(
                conn,
                f"HISTORY|{row['timestamp']}|{row['sender']}|{row['receiver']}|{row['message_type']}|{row['message']}",
            )

    def handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        ip, port = addr
        username = ""
        try:
            rfile = conn.makefile("r", encoding="utf-8", newline="\n")
            first = rfile.readline()
            if not first:
                conn.close()
                return
            username = first.strip()
            if not username:
                self.send_line(conn, "ERROR: empty username")
                conn.close()
                return

            with self.lock:
                if username in self.clients:
                    self.send_line(conn, "ERROR: username already online")
                    conn.close()
                    return
                self.clients[username] = conn

            self.log_event(f"{self.now()},JOIN,{username},{ip}:{port}")
            self.send_line(conn, f"SYSTEM:WELCOME:{username}")
            self.send_last_five(username, conn)

            with self.lock:
                self.broadcast_system(f"SYSTEM:JOIN:{username}", exclude=username)
                self.send_online_list()

            for raw in rfile:
                msg = raw.strip()
                if not msg:
                    continue

                with self.lock:
                    if msg == "/list":
                        self.send_line(conn, "ONLINE_USERS:" + ",".join(sorted(self.clients.keys())))
                        self.append_history(username, username, "list", "/list")
                        continue

                    if msg.startswith("/msg "):
                        parts = msg.split(" ", 2)
                        if len(parts) < 3:
                            self.send_line(conn, "ERROR: usage /msg <username> <message>")
                            continue
                        target = parts[1].strip()
                        body = parts[2].strip()
                        tconn = self.clients.get(target)
                        if tconn is None:
                            self.send_line(conn, f"ERROR: user '{target}' does not exist")
                            self.append_history(username, target, "private_error", body)
                            continue

                        self.send_line(tconn, f"[PM][{username}] {body}")
                        self.send_line(conn, f"[PM to {target}] {body}")
                        self.append_history(username, target, "private", body)
                        continue

                    for c in list(self.clients.values()):
                        self.send_line(c, f"[{username}] {msg}")
                    self.append_history(username, "ALL", "broadcast", msg)
        except Exception:
            pass
        finally:
            with self.lock:
                self.clients.pop(username, None)
                if username:
                    self.broadcast_system(f"SYSTEM:LEAVE:{username}", exclude=username)
                    self.send_online_list()
            if username:
                self.log_event(f"{self.now()},LEAVE,{username},{ip}:{port}")
            try:
                conn.close()
            except OSError:
                pass

    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((self.host, self.port))
            srv.listen(50)
            print(f"[server] listening on {self.host}:{self.port}")
            while True:
                conn, addr = srv.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()


def main() -> None:
    parser = argparse.ArgumentParser(description="Assignment 6 chat server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--history-file", default="chat_history.csv")
    parser.add_argument("--event-file", default="server_events.log")
    args = parser.parse_args()

    ChatServer(
        host=args.host,
        port=args.port,
        history_file=Path(args.history_file),
        event_file=Path(args.event_file),
    ).start()


if __name__ == "__main__":
    main()
