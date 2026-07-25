#!/usr/bin/env python3
"""Run Assignment 4 performance experiments for 1, 2, and 3 clients."""

import csv
import json
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "server.py"
CLIENT = ROOT / "client.py"
RESULTS = ROOT / "performance_results.csv"
TMP = ROOT / "tmp_perf"


def run_experiment(client_count: int, messages_per_client: int) -> dict[str, float]:
    server_proc = subprocess.Popen(
        [sys.executable, str(SERVER), "--host", "127.0.0.1", "--port", "5000"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        time.sleep(1.0)

        procs = []
        summary_files = []
        start_ts = time.time()

        for i in range(1, client_count + 1):
            summary = TMP / f"summary_{client_count}_{i}.json"
            summary_files.append(summary)

            proc = subprocess.Popen(
                [
                    sys.executable,
                    str(CLIENT),
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "5000",
                    "--username",
                    f"Client{i}",
                    "--auto-count",
                    str(messages_per_client),
                    "--auto-delay",
                    "0.02",
                    "--summary-file",
                    str(summary),
                ],
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            procs.append(proc)

        for proc in procs:
            proc.wait(timeout=120)

        duration_sec = max(time.time() - start_ts, 0.001)

        avg_samples = []
        delivered = 0
        for path in summary_files:
            data = json.loads(path.read_text(encoding="utf-8"))
            avg_samples.append(float(data.get("avg_delivery_time_ms", 0.0)))
            delivered += int(data.get("received_own_broadcasts", 0))

        avg_delivery_ms = sum(avg_samples) / len(avg_samples) if avg_samples else 0.0
        total_messages = client_count * messages_per_client
        throughput = total_messages / duration_sec

        return {
            "clients": client_count,
            "total_messages": total_messages,
            "avg_delivery_time_ms": round(avg_delivery_ms, 3),
            "throughput_msgs_per_sec": round(throughput, 3),
            "delivered_own_echoes": delivered,
        }
    finally:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    rows = []

    for clients in (1, 2, 3):
        result = run_experiment(client_count=clients, messages_per_client=20)
        rows.append(result)
        print(result)

    with RESULTS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "clients",
                "total_messages",
                "avg_delivery_time_ms",
                "throughput_msgs_per_sec",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row["clients"],
                    row["total_messages"],
                    row["avg_delivery_time_ms"],
                    row["throughput_msgs_per_sec"],
                ]
            )

    print(f"Generated {RESULTS}")


if __name__ == "__main__":
    main()
