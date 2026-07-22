# Assignment 1 Report Template

## 1. Student Details

- Name:
- Roll No:
- Timeout used (from roll rule):

## 2. Objective

Describe stop-and-wait reliable UDP goal in 3-5 lines.

## 3. Mininet Topology and Setup

- Topology: `h1 -- s1 -- h2`
- Commands used for setup.
- Insert screenshots: `nodes.png`, `net.png`, `pingall.png`

## 4. Program Design

- Packet format used: `SEQ|MESSAGE`
- ACK format used: `ACK|SEQ`
- Timeout and retransmission logic.
- Duplicate detection logic at server.

## 5. Experimental Results

- Insert/describe `result_table.csv`.
- Mention behavior for loss 0, 5, 10.

## 6. Screenshots

- `server_output.png`
- `client_output.png`

## 7. Answers

1. Why is ACK needed?
2. Why is timeout needed?
3. Why can duplicate messages occur?
4. What happens when packet loss increases?
5. How is this method similar to TCP?
6. How is it different from TCP?

## 8. Conclusion

Short summary of correctness and observations.
