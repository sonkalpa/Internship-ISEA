# Assignment 3 - Original Screenshot Steps

Use this to replace generated screenshots with original screenshots from your
own terminal/Wireshark session.

## 1) Re-run experiment in Ubuntu (WSL)

From `assignment3/`:

```bash
bash run_wsl_assignment3.sh
```

If `tshark` is unavailable, capture separately:

```bash
sudo dumpcap -i lo -a duration:20 -w capture.pcapng
```

## 2) Take terminal screenshots (original)

- Start traffic generation and capture terminal: save as
  `screenshots/traffic_generation.png`.
- Start raw capture and capture terminal: save as
  `screenshots/program_output.png`.

## 3) Take Wireshark screenshot (original)

Open this file in Wireshark:

- `E:\ASSIGNMENT\Internship-ISEA\assignment3\capture.pcapng`

Apply display filter:

- `tcp` (or `ip.proto == 6`)

Useful frame references from current capture for quick selection:

- Frame `1`: SYN
- Frame `2`: SYN-ACK
- Frame `3`: ACK
- Frame `4`: client payload (`PSH,ACK`)
- Frame `6`: server payload (`PSH,ACK`)

Take packet-list + packet-detail screenshot and save as:

- `screenshots/wireshark_packets.png`

## 4) Take comparison screenshot (original)

Open `packet_comparison_template.csv`, ensure 5 matched rows are visible, and
take screenshot:

- `screenshots/comparison_packets.png`

## 5) Keep same filenames

Replace the files in `assignment3/screenshots/` using the exact required names
so submission validators continue to pass.
