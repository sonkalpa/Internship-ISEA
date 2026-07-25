#!/usr/bin/env python3
"""Generate Assignment 4 graphs from performance_results.csv."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "performance_results.csv"
GRAPH_DIR = ROOT / "graphs"


def read_rows() -> tuple[list[int], list[float], list[float]]:
    clients = []
    avg_delay = []
    throughput = []

    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clients.append(int(row["clients"]))
            avg_delay.append(float(row["avg_delivery_time_ms"]))
            throughput.append(float(row["throughput_msgs_per_sec"]))

    return clients, avg_delay, throughput


def main() -> None:
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    clients, avg_delay, throughput = read_rows()

    plt.figure(figsize=(7, 4.5))
    plt.plot(clients, avg_delay, marker="o", linewidth=2)
    plt.title("Clients vs Average Delivery Time")
    plt.xlabel("Number of Clients")
    plt.ylabel("Average Delivery Time (ms)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(clients)
    plt.tight_layout()
    delay_path = GRAPH_DIR / "clients_vs_delay.png"
    plt.savefig(delay_path, dpi=150)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.plot(clients, throughput, marker="o", linewidth=2)
    plt.title("Clients vs Throughput")
    plt.xlabel("Number of Clients")
    plt.ylabel("Throughput (messages/second)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(clients)
    plt.tight_layout()
    throughput_path = GRAPH_DIR / "clients_vs_throughput.png"
    plt.savefig(throughput_path, dpi=150)
    plt.close()

    print(f"Generated {delay_path}")
    print(f"Generated {throughput_path}")


if __name__ == "__main__":
    main()
