# Assignment 2 Report - TCP Connection Performance Analysis using Mininet and Wireshark

## 1. Student Details

- Name: Sonkalpa Borah
- Roll No: CS-BTC24-08

## 2. Objective

This assignment compares TCP communication performance between two modes:
`persistent` (single connection reused) and `new_connection` (new TCP
connection per message). The comparison is based on response time, throughput,
and packet behavior observed in Wireshark.

## 3. Mininet Topology and Setup

- Topology: `h1 -- s1 -- h2`
- Server host: `h1` (`10.0.0.1`)
- Client host: `h2` (`10.0.0.2`)
- Link profile: `bw=5 Mbps`, `delay=50 ms`

Screenshots included:

- `screenshots/nodes.png`
- `screenshots/net.png`
- `screenshots/pingall.png`
- `screenshots/server_output.png`
- `screenshots/client_output.png`

## 4. Program Design

### Message format

- Request: `MSG_ID|MESSAGE_SIZE|MESSAGE_DATA`
- Response: `ACK|MSG_ID|RECEIVED_SIZE`

### Modes

- `persistent`: one connection for all 10 messages per message size
- `new_connection`: one connection for every message

### Logging and outputs

- `server_log.txt`: per-message receive + ACK log
- `message_response_log.csv`: per-message response times (60 rows)
- `result_table.csv`: summary metrics (6 rows)

## 5. Experimental Results

Result table (`result_table.csv`) contains 6 rows (2 modes x 3 sizes):

| mode | message_size_bytes | average_response_time_seconds | throughput_bytes_per_second |
|---|---:|---:|---:|
| persistent | 128 | 0.000114 | 1020271.77 |
| persistent | 512 | 0.000184 | 2627838.18 |
| persistent | 1024 | 0.000095 | 9715702.05 |
| new_connection | 128 | 0.000407 | 328750.70 |
| new_connection | 512 | 0.000442 | 1162581.58 |
| new_connection | 1024 | 0.000362 | 2818630.76 |

Observed trend:

- Persistent mode has slightly lower response time than new-connection mode.
- Throughput increases as message size increases.
- New-connection mode incurs additional connection setup/teardown overhead.

## 6. Graphs

Generated graph files:

- `graphs/mode_vs_response_time.png`
- `graphs/message_size_vs_throughput.png`
- `graphs/message_response_time.png`

Graph interpretation:

- `mode_vs_response_time`: persistent mode performs better on average.
- `message_size_vs_throughput`: larger payload size yields higher throughput.
- `message_response_time`: response-time variation is higher for
  new-connection due repeated handshakes.

## 7. Wireshark Verification

Display filter used: `tcp.port == 5000`

Screenshots included:

- `screenshots/persistent_handshake.png`
- `screenshots/persistent_data_packets.png`
- `screenshots/persistent_connection_close.png`
- `screenshots/new_connection_multiple_handshakes.png`

Packet-level observations:

- Persistent mode shows one initial three-way handshake and one final close.
- New-connection mode shows repeated SYN/SYN-ACK/ACK and FIN sequences.

## 8. Answers to Required Questions

1. Why does TCP use a three-way handshake?
   - It establishes synchronized sequence numbers and confirms both sides are
     ready to communicate reliably.

2. Which mode had lower response time?
   - Persistent mode showed lower average response time.

3. Why does new-connection mode have more overhead?
   - Every message requires handshake and teardown packets, adding delay and
     control traffic.

4. Which mode is better for CampusChat and why?
   - Persistent mode, because chat is interactive and benefits from avoiding
     repeated connect overhead.

5. Which mode is suitable for NetAttend and why?
   - New-connection mode can be suitable for short periodic updates where each
     request is independent and server state can stay simple.

6. How does message size affect throughput?
   - Throughput increases with message size because protocol overhead is
     amortized over larger payloads.

7. How did Wireshark help verify TCP behavior?
   - It visually confirmed handshake patterns, data exchanges, and connection
     close behavior for each mode.

## 9. Conclusion

The TCP implementation meets assignment requirements for both modes, produces
the required CSV files and graphs, and Wireshark evidence confirms the expected
protocol behavior differences between persistent and new-connection designs.
