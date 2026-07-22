# Assignment 3 Linux Run Steps

Use these steps on a Linux machine (or Mininet host) with root access.

## 1) Build

```bash
gcc raw_capture.c -o raw_capture
```

## 2) Start packet capture program

Capture 20 packets and save console output:

```bash
sudo ./raw_capture 20 | tee program_output.txt
```

## 3) Generate TCP traffic in another terminal

Use one or more commands while step 2 is running:

```bash
nc -v 127.0.0.1 5000
```

```bash
curl http://example.com
```

```bash
ssh 127.0.0.1
```

## 4) Wireshark capture

- Interface: choose the interface used by the generated TCP traffic.
- Display filter: `tcp` or `ip.proto == 6`
- Save capture as `capture.pcapng`

## 5) Fill comparison table

Use `packet_comparison_template.csv` and fill 5 matched packets.

## 6) Collect screenshots

Put files into `screenshots/`:

- `traffic_generation.png`
- `program_output.png`
- `wireshark_packets.png`
- `comparison_packets.png`
