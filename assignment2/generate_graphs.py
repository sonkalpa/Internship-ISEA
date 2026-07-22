#!/usr/bin/env python3
"""
Generates the three required graphs from result_table.csv and
message_response_log.csv, and saves them into graphs/.

Run this AFTER client.py has produced both CSV files.
"""

import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = "graphs"
os.makedirs(OUT_DIR, exist_ok=True)


def load_result_table(path="result_table.csv"):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def load_message_log(path="message_response_log.csv"):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def graph_mode_vs_response_time(result_rows):
    """Average response time per mode (averaged across all message sizes)."""
    modes = ["persistent", "new_connection"]
    avgs = []
    for mode in modes:
        vals = [float(r["average_response_time_seconds"]) for r in result_rows if r["mode"] == mode]
        avgs.append(sum(vals) / len(vals))

    plt.figure(figsize=(6, 4.5))
    bars = plt.bar(modes, avgs, color=["#4C72B0", "#DD8452"])
    plt.xlabel("Mode")
    plt.ylabel("Average Response Time (s)")
    plt.title("Mode vs Average Response Time")
    for b, v in zip(bars, avgs):
        plt.text(b.get_x() + b.get_width() / 2, v, f"{v:.4f}", ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mode_vs_response_time.png"), dpi=150)
    plt.close()


def graph_message_size_vs_throughput(result_rows):
    sizes = sorted(set(int(r["message_size_bytes"]) for r in result_rows))
    plt.figure(figsize=(6.5, 4.5))
    for mode, color in [("persistent", "#4C72B0"), ("new_connection", "#DD8452")]:
        throughputs = []
        for size in sizes:
            for r in result_rows:
                if r["mode"] == mode and int(r["message_size_bytes"]) == size:
                    throughputs.append(float(r["throughput_bytes_per_second"]))
        plt.plot(sizes, throughputs, marker="o", label=mode, color=color)
    plt.xlabel("Message Size (bytes)")
    plt.ylabel("Throughput (bytes/second)")
    plt.title("Message Size vs Throughput")
    plt.xticks(sizes)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "message_size_vs_throughput.png"), dpi=150)
    plt.close()


def graph_message_response_time_512(message_rows):
    """Response time per message number, for 512-byte messages, both modes."""
    plt.figure(figsize=(6.5, 4.5))
    for mode, color in [("persistent", "#4C72B0"), ("new_connection", "#DD8452")]:
        pts = [(int(r["message_number"]), float(r["response_time_seconds"]))
               for r in message_rows if r["mode"] == mode and int(r["message_size_bytes"]) == 512]
        pts.sort(key=lambda x: x[0])
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        plt.plot(xs, ys, marker="o", label=mode, color=color)
    plt.xlabel("Message Number")
    plt.ylabel("Response Time (s)")
    plt.title("Response Time per Message (512 bytes)")
    plt.xticks(range(1, 11))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "message_response_time.png"), dpi=150)
    plt.close()


def main():
    result_rows = load_result_table()
    message_rows = load_message_log()

    graph_mode_vs_response_time(result_rows)
    graph_message_size_vs_throughput(result_rows)
    graph_message_response_time_512(message_rows)

    print(f"[graphs] Saved 3 graphs to {OUT_DIR}/")


if __name__ == "__main__":
    main()
