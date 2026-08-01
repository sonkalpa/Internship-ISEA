#!/usr/bin/env python3
"""Assignment 5 advanced multi-client TCP chat server."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import socket
import threading
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ClientState:
    username: str
    ip: str
    port: int
    login_time: str
    status: str
    conn: socket.socket


class AdvancedChatServer:
    def __init__(
        self,
        host: str,
        port: int,
        history_file: Path,
        event_file: Path,
        stats_file: Path,
        state_file: Path,
    ) -> None:
        self.host = host
        self.port = port
        self.history_file = history_file
        self.event_file = event_file
        self.stats_file = stats_file
        self.state_file = state_file

        self.clients: dict[str, ClientState] = {}
        self.lock = threading.Lock()

        self.messages_processed = 0
        self.broadcast_messages = 0
        self.private_messages = 0

        self._init_files()

    @staticmethod
    def _timestamp() -> str:
        return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _init_files(self) -> None:
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.event_file.parent.mkdir(parents=True, exist_ok=True)
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.history_file.exists():
            with self.history_file.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "sender", "receiver", "message_type", "message"])

        if not self.event_file.exists():
            self.event_file.write_text("", encoding="utf-8")

        with self.state_file.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "username", "ip", "port", "login_time", "status"])

        self._write_stats()

    def _log_event(self, line: str) -> None:
        with self.event_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def _append_history(self, sender: str, receiver: str, message_type: str, message: str) -> None:
        with self.history_file.open("a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self._timestamp(), sender, receiver, message_type, message])

    def _append_state(self, state: ClientState) -> None:
        with self.state_file.open("a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                self._timestamp(),
                state.username,
                state.ip,
                state.port,
                state.login_time,
                state.status,
            ])

    def _write_stats(self) -> None:
        with self.stats_file.open("w", encoding="utf-8") as f:
            f.write(f"connected_users={len(self.clients)}\n")
            f.write(f"messages_processed={self.messages_processed}\n")
            f.write(f"broadcast_messages={self.broadcast_messages}\n")
            f.write(f"private_messages={self.private_messages}\n")

    @staticmethod
    def _send_line(conn: socket.socket, text: str) -> None:
        conn.sendall((text + "\n").encode("utf-8", errors="replace"))

    def _send_online_list_to_all(self) -> None:
        users = sorted(self.clients.keys())
        payload = "ONLINE_USERS:" + ",".join(users)
        for state in list(self.clients.values()):
            try:
                self._send_line(state.conn, payload)
            except OSError:
                continue

    def _broadcast_system(self, message: str, exclude_user: str = "") -> None:
        for username, state in list(self.clients.items()):
            if username == exclude_user:
                continue
            try:
                self._send_line(state.conn, message)
            except OSError:
                continue

    def _send_last_five_sent(self, username: str, conn: socket.socket) -> None:
        rows = []
        with self.history_file.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("sender") == username:
                    rows.append(row)

        for row in rows[-5:]:
            line = (
                f"HISTORY|{row['timestamp']}|{row['sender']}|{row['receiver']}|"
                f"{row['message_type']}|{row['message']}"
            )
            self._send_line(conn, line)

    def _handle_command(self, sender: str, conn: socket.socket, message: str) -> None:
        if message == "/list":
            users = sorted(self.clients.keys())
            self._send_line(conn, "ONLINE_USERS:" + ",".join(users))
            self.messages_processed += 1
            self._append_history(sender, sender, "list", "/list")
            return

        if message.startswith("/msg "):
            parts = message.split(" ", 2)
            if len(parts) < 3:
                self._send_line(conn, "ERROR: usage /msg <username> <message>")
                return

            target = parts[1].strip()
            pm_text = parts[2].strip()
            if not target or not pm_text:
                self._send_line(conn, "ERROR: usage /msg <username> <message>")
                return

            target_state = self.clients.get(target)
            if target_state is None:
                self._send_line(conn, f"ERROR: user '{target}' does not exist")
                self._append_history(sender, target, "private_error", pm_text)
                return

            self._send_line(target_state.conn, f"[PM][{sender}] {pm_text}")
            self._send_line(conn, f"[PM to {target}] {pm_text}")
            self.messages_processed += 1
            self.private_messages += 1
            self._append_history(sender, target, "private", pm_text)
            return

        # broadcast message
        for state in list(self.clients.values()):
            self._send_line(state.conn, f"[{sender}] {message}")

        self.messages_processed += 1
        self.broadcast_messages += 1
        self._append_history(sender, "ALL", "broadcast", message)

    def handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        client_ip, client_port = addr
        username = ""

        try:
            reader = conn.makefile("r", encoding="utf-8", newline="\n")
            first = reader.readline()
            if not first:
                conn.close()
                return

            username = first.strip()
            if not username:
                self._send_line(conn, "ERROR: empty username")
                conn.close()
                return

            with self.lock:
                if username in self.clients:
                    self._send_line(conn, "ERROR: username already online")
                    conn.close()
                    return

                state = ClientState(
                    username=username,
                    ip=client_ip,
                    port=client_port,
                    login_time=self._timestamp(),
                    status="online",
                    conn=conn,
                )
                self.clients[username] = state
                self._append_state(state)
                self._write_stats()

            self._log_event(f"{self._timestamp()},JOIN,{username},{client_ip}:{client_port}")
            self._send_line(conn, f"SYSTEM:WELCOME:{username}")
            self._send_last_five_sent(username, conn)

            with self.lock:
                self._broadcast_system(f"SYSTEM:JOIN:{username}", exclude_user=username)
                self._send_online_list_to_all()

            for raw in reader:
                msg = raw.strip()
                if not msg:
                    continue

                with self.lock:
                    self._handle_command(username, conn, msg)
                    self._write_stats()

        except Exception:
            pass
        finally:
            with self.lock:
                state = self.clients.pop(username, None)
                if state is not None:
                    state.status = "offline"
                    self._append_state(state)
                    self._broadcast_system(f"SYSTEM:LEAVE:{username}", exclude_user=username)
                    self._send_online_list_to_all()
                    self._write_stats()

            if username:
                self._log_event(f"{self._timestamp()},LEAVE,{username},{client_ip}:{client_port}")

            try:
                conn.close()
            except OSError:
                pass

    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen(50)
            print(f"[server] listening on {self.host}:{self.port}")

            while True:
                conn, addr = server.accept()
                th = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                th.start()


def main() -> None:
    parser = argparse.ArgumentParser(description="Assignment 5 advanced chat server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--history-file", default="chat_history.csv")
    parser.add_argument("--event-file", default="server_events.log")
    parser.add_argument("--stats-file", default="server_stats.txt")
    parser.add_argument("--state-file", default="client_state.csv")
    args = parser.parse_args()

    server = AdvancedChatServer(
        host=args.host,
        port=args.port,
        history_file=Path(args.history_file),
        event_file=Path(args.event_file),
        stats_file=Path(args.stats_file),
        state_file=Path(args.state_file),
    )
    server.start()


if __name__ == "__main__":
    main()
