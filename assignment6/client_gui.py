#!/usr/bin/env python3
"""Assignment 6 GUI-based TCP chat client using tkinter."""

from __future__ import annotations

import socket
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext


class ChatGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Assignment 6 Chat Client")
        self.root.geometry("820x560")

        self.sock: socket.socket | None = None
        self.receiver_thread: threading.Thread | None = None
        self.connected = False
        self.username = ""

        self._build_login_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_login_window(self) -> None:
        self.login_frame = tk.Frame(self.root, padx=16, pady=16)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0, sticky="w", pady=4)
        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=4)

        tk.Label(self.login_frame, text="Password (optional)").grid(row=1, column=0, sticky="w", pady=4)
        self.password_entry = tk.Entry(self.login_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=4)

        tk.Label(self.login_frame, text="Server Host").grid(row=2, column=0, sticky="w", pady=4)
        self.host_entry = tk.Entry(self.login_frame, width=30)
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.grid(row=2, column=1, pady=4)

        tk.Label(self.login_frame, text="Server Port").grid(row=3, column=0, sticky="w", pady=4)
        self.port_entry = tk.Entry(self.login_frame, width=30)
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=3, column=1, pady=4)

        self.connect_btn = tk.Button(self.login_frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.login_status = tk.Label(self.login_frame, text="Disconnected", fg="red")
        self.login_status.grid(row=5, column=0, columnspan=2)

    def _build_chat_window(self) -> None:
        self.chat_frame = tk.Frame(self.root, padx=10, pady=10)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(self.chat_frame)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = tk.Frame(self.chat_frame, width=220)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_area = scrolledtext.ScrolledText(left, wrap=tk.WORD, state=tk.DISABLED)
        self.message_area.pack(fill=tk.BOTH, expand=True)

        entry_row = tk.Frame(left)
        entry_row.pack(fill=tk.X, pady=8)

        self.message_entry = tk.Entry(entry_row)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", lambda _e: self.send_broadcast())

        self.send_btn = tk.Button(entry_row, text="Send", command=self.send_broadcast)
        self.send_btn.pack(side=tk.LEFT, padx=4)

        private_row = tk.Frame(left)
        private_row.pack(fill=tk.X)

        tk.Label(private_row, text="Private to:").pack(side=tk.LEFT)
        self.private_to_entry = tk.Entry(private_row, width=16)
        self.private_to_entry.pack(side=tk.LEFT, padx=6)
        self.private_btn = tk.Button(private_row, text="Send Private", command=self.send_private)
        self.private_btn.pack(side=tk.LEFT)

        self.disconnect_btn = tk.Button(left, text="Disconnect", command=self.disconnect)
        self.disconnect_btn.pack(anchor="w", pady=8)

        tk.Label(right, text="Online Users").pack(anchor="w")
        self.user_list = tk.Listbox(right, height=20)
        self.user_list.pack(fill=tk.Y, expand=True)
        self.user_list.bind("<<ListboxSelect>>", self._copy_selected_user)

        self.status_label = tk.Label(right, text="Connected", fg="green")
        self.status_label.pack(anchor="w", pady=8)

    def append_message(self, text: str) -> None:
        self.message_area.configure(state=tk.NORMAL)
        self.message_area.insert(tk.END, text + "\n")
        self.message_area.see(tk.END)
        self.message_area.configure(state=tk.DISABLED)

    def connect(self) -> None:
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Validation Error", "Username cannot be empty")
            return

        host = self.host_entry.get().strip() or "127.0.0.1"
        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Validation Error", "Port must be a number")
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.sendall((username + "\n").encode("utf-8"))
        except OSError as exc:
            messagebox.showerror("Connection Error", f"Could not connect: {exc}")
            return

        self.sock = sock
        self.username = username
        self.connected = True

        self.login_frame.destroy()
        self._build_chat_window()
        self.append_message(f"Connected as {username} to {host}:{port}")

        self.receiver_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.receiver_thread.start()

    def _send(self, line: str) -> None:
        if not self.sock:
            return
        try:
            self.sock.sendall((line + "\n").encode("utf-8"))
        except OSError:
            self.disconnect()

    def send_broadcast(self) -> None:
        text = self.message_entry.get().strip()
        if not text:
            return
        self._send(text)
        self.message_entry.delete(0, tk.END)

    def send_private(self) -> None:
        text = self.message_entry.get().strip()
        target = self.private_to_entry.get().strip()
        if not text:
            return
        if not target:
            messagebox.showerror("Validation Error", "Enter target username for private message")
            return

        self._send(f"/msg {target} {text}")
        self.message_entry.delete(0, tk.END)

    def _copy_selected_user(self, _event=None) -> None:
        selection = self.user_list.curselection()
        if not selection:
            return
        username = self.user_list.get(selection[0])
        self.private_to_entry.delete(0, tk.END)
        self.private_to_entry.insert(0, username)

    def _update_online_users(self, users_csv: str) -> None:
        users = [u for u in users_csv.split(",") if u]
        self.user_list.delete(0, tk.END)
        for user in users:
            self.user_list.insert(tk.END, user)

    def receive_loop(self) -> None:
        assert self.sock is not None
        rfile = self.sock.makefile("r", encoding="utf-8", newline="\n")
        try:
            for raw in rfile:
                msg = raw.rstrip("\n")
                self.root.after(0, self._handle_incoming, msg)
                if not self.connected:
                    break
        except OSError:
            pass
        finally:
            self.root.after(0, self.disconnect)

    def _handle_incoming(self, msg: str) -> None:
        if msg.startswith("ONLINE_USERS:"):
            self._update_online_users(msg.split(":", 1)[1])
            return
        self.append_message(msg)

    def disconnect(self) -> None:
        if not self.connected:
            return
        self.connected = False
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.sock.close()
            except OSError:
                pass
        self.sock = None

        if hasattr(self, "status_label"):
            self.status_label.configure(text="Disconnected", fg="red")
            self.append_message("Disconnected from server")

    def on_close(self) -> None:
        self.disconnect()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    ChatGUI().run()


if __name__ == "__main__":
    main()
