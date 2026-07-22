# Assignment 3 - HOW TO RUN

Run this assignment on Linux (or Mininet host namespace) with root access.

## 1) Compile

```bash
gcc raw_capture.c -o raw_capture
```

## 2) Capture system details (for report)

```bash
uname -a > system_details.txt
gcc --version >> system_details.txt
ip addr >> system_details.txt
```

## 3) Start raw capture

```bash
sudo ./raw_capture 20 | tee program_output.txt
```

Keep this running while generating traffic in another terminal.

## 4) Generate TCP traffic (roll last digit 8 => protocol TCP)

Use one or more commands:

```bash
nc -v 127.0.0.1 5000
```

```bash
curl http://example.com
```

```bash
ssh 127.0.0.1
```

Take screenshot: `screenshots/traffic_generation.png`.

## 5) Wireshark capture and verification

1. Open Wireshark on interface carrying this traffic.
2. Filter with `tcp` or `ip.proto == 6`.
3. Save capture as `capture.pcapng` in this folder.
4. Pick any 5 packets and fill `packet_comparison_template.csv`.

Take screenshots:

- `screenshots/program_output.png`
- `screenshots/wireshark_packets.png`
- `screenshots/comparison_packets.png`

## 6) Final report

Use `report_template.md` outline and prepare final report as PDF:

- `report.pdf` (submission)
- optional editable source: `report.docx`

## 7) Folder checklist before submission

- `raw_capture.c`
- `program_output.txt`
- `capture.pcapng`
- `packet_comparison_template.csv` (filled)
- `system_details.txt`
- `screenshots/` (required PNG files)
- `report.pdf`
