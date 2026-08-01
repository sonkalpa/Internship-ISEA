#!/usr/bin/env python3
"""Generate Assignment 5 required graphs from performance_results.csv."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "performance_results.csv"
GRAPH_DIR = ROOT / "graphs"


def read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows()
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    clients = [int(r["clients"]) for r in rows]
    delays = [float(r["avg_delay_ms"]) for r in rows]
    throughputs = [float(r["throughput_msgs_per_sec"]) for r in rows]
    broadcasts = [int(r["broadcast_messages"]) for r in rows]
    privates = [int(r["private_messages"]) for r in rows]

    plt.figure(figsize=(7, 4.5))
    plt.plot(clients, delays, marker="o", linewidth=2)
    plt.title("Clients vs Average Delivery Time")
    plt.xlabel("Number of Clients")
    plt.ylabel("Average Delivery Time (ms)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(clients)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "clients_vs_delay.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.plot(clients, throughputs, marker="o", linewidth=2)
    plt.title("Clients vs Throughput")
    plt.xlabel("Number of Clients")
    plt.ylabel("Throughput (messages/second)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(clients)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "clients_vs_throughput.png", dpi=150)
    plt.close()

    width = 0.35
    x = list(range(len(clients)))
    plt.figure(figsize=(7.5, 4.8))
    plt.bar([i - width / 2 for i in x], broadcasts, width=width, label="Broadcast")
    plt.bar([i + width / 2 for i in x], privates, width=width, label="Private")
    plt.xticks(x, [str(c) for c in clients])
    plt.title("Broadcast Messages vs Private Messages")
    plt.xlabel("Number of Clients")
    plt.ylabel("Message Count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "message_type_distribution.png", dpi=150)
    plt.close()

    print("Generated graphs:")
    print("- graphs/clients_vs_delay.png")
    print("- graphs/clients_vs_throughput.png")
    print("- graphs/message_type_distribution.png")


if __name__ == "__main__":
    main()
