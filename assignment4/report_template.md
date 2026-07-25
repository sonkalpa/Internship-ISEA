# Assignment 4 Report Template

## 1. Objective

Describe multi-client chat objective and TCP reliability goals.

## 2. Network Topology

- Mininet topology used: `single,4`
- Host mapping:
  - `h1`: server
  - `h2/h3/h4`: clients

## 3. Program Design

- Threaded server design
- Client registration flow
- Broadcast message flow
- Logging design for `server_events.log` and `chat_log.txt`

## 4. Experimental Results

- Include excerpts from `chat_log.txt`
- Include `performance_results.csv` table
- Mention 1/2/3 client experiments

## 5. Wireshark Verification

- Filter used: `tcp.port == 5000`
- Include screenshots:
  - `tcp_handshake.png`
  - `chat_message.png`
  - `broadcast_message.png`
  - `connection_close.png`

## 6. Graph Analysis

- `clients_vs_delay.png`
- `clients_vs_throughput.png`
- Explain observed trend

## 7. Reflection Answers (<= 300 words total)

1. Why multi-threaded server over single-threaded?
2. Challenges with simultaneous clients?
3. How TCP ensures reliability?
4. Which Wireshark observations validated behavior?

## 8. Conclusion

Summarize implementation correctness and measured results.
