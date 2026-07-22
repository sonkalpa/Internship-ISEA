# Assignment 3 Report Template

## 1. Objective

Describe raw socket packet analysis goal and assigned protocol.

## 2. Student and System Configuration

- Name:
- Roll No:
- Assigned protocol:
- Include output summary from `system_details.txt`.

## 3. Compile and Run Commands

- `gcc raw_capture.c -o raw_capture`
- `sudo ./raw_capture 20`

## 4. Program Design

- Raw socket initialization.
- IP header parsing.
- TCP field extraction (port + flags).
- Additional IP field shown (`IP_IDENTIFICATION`).

## 5. Traffic Generation

- Commands used.
- Interface used.
- Screenshot: `traffic_generation.png`.

## 6. Experimental Results

- Include excerpts from `program_output.txt`.
- Mention at least 20 packets captured.

## 7. Wireshark Verification

- Include `capture.pcapng` reference.
- Fill and include 5-packet comparison table from
  `packet_comparison_template.csv`.
- Screenshots: `wireshark_packets.png`, `comparison_packets.png`.

## 8. Header Analysis

For 3 packets, answer:

1. Why is TTL not zero?
2. Why do packet sizes differ?
3. What does protocol field provide?
4. What if protocol field is modified?
5. What do TCP fields reveal?

## 9. Program Enhancement

- Explain selected extra field (`IP_IDENTIFICATION`).
- Show values from at least 5 packets.
- Mention if values changed or remained stable.

## 10. Reflection Answers (<= 300 words total)

1. Why root privileges are required for raw sockets.
2. Difference between raw sockets and TCP/UDP sockets.
3. One advantage and one limitation.
4. One networking/cybersecurity use case.

## 11. Conclusion

Short summary of what was verified using raw output and Wireshark.
