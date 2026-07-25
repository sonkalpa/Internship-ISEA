# Assignment 1 Report - Reliable UDP Communication in Mininet

## 1. Student Details

- Name: Sonkalpa Borah
- Roll No: CS-BTC24-08
- Timeout used (roll last digit 8): 1.5 seconds

## 2. Objective

The objective of this assignment is to implement reliable message transfer over
UDP using stop-and-wait logic. Reliability is added by attaching sequence
numbers, waiting for ACK packets, applying timeout, and retransmitting packets
when ACK is not received.

## 3. Topology and Setup

- Topology: `h1 -- s1 -- h2`
- `h1` runs the UDP server and `h2` runs the UDP client.
- Client message format: `SEQ|MESSAGE`
- Server ACK format: `ACK|SEQ`

In this run environment (WSL), packet-loss behavior was executed using the
provided application-level fallback mode (`--emulate-loss`) because kernel
`tc/netem` was unavailable.

## 4. Program Design

### Client

- Sends one message at a time.
- Waits for matching ACK for current sequence number.
- If timeout occurs or ACK is lost/invalid, retransmits the same sequence.
- Tracks total sent packets, retransmissions, and total transfer time.

### Server

- Receives `SEQ|MESSAGE` packets.
- Sends `ACK|SEQ` for every received packet.
- Maintains set of seen sequence numbers.
- Counts unique packets and duplicates.

## 5. Results

From `result_table.csv`:

| loss_percent | timeout | total_messages | total_packets_sent | total_retransmissions | transfer_time_seconds | status |
|---|---:|---:|---:|---:|---:|---|
| 0 | 1.5 | 10 | 10 | 0 | 0.304568 | SUCCESS |
| 5 | 1.5 | 10 | 10 | 0 | 0.305424 | SUCCESS |
| 10 | 1.5 | 10 | 11 | 1 | 0.335629 | SUCCESS |

Observation: as loss increases to 10%, one retransmission appears and transfer
time increases.

## 6. Server-Side Duplicate Observation

From `logs/server_loss10.out.txt`, the server detected one duplicate packet
(`seq=4`) and still completed with:

- `TOTAL_UNIQUE_MESSAGES_RECEIVED=10`
- `TOTAL_DUPLICATES_DETECTED=1`
- `STATUS=SUCCESS`

## 7. Required Answers

1. Why is ACK needed?
   - ACK confirms successful delivery of a specific sequence number, so the
     sender knows when it can move to the next packet.

2. Why is timeout needed?
   - Timeout allows the sender to recover when data or ACK is lost by
     triggering retransmission after waiting for a bounded period.

3. Why can duplicate messages occur?
   - If ACK is lost, the sender retransmits the same packet. The receiver may
     already have processed it, so the same sequence number arrives again.

4. What happens when packet loss increases?
   - Retransmissions increase, transfer time increases, and protocol overhead
     increases, reducing effective performance.

5. How is this method similar to TCP?
   - It uses reliability concepts similar to TCP: sequence tracking,
     acknowledgment, timeout, and retransmission.

6. How is it different from TCP?
   - This implementation is minimal stop-and-wait logic without TCP features
     like sliding window, congestion control, flow control, and byte-stream
     management.

## 8. Screenshots

Add these screenshots in `screenshots/` and include them in the final PDF:

- `nodes.png`
- `net.png`
- `pingall.png`
- `server_output.png`
- `client_output.png`

## 9. Conclusion

The reliable UDP implementation correctly delivered all 10 messages across
tested loss profiles, detected duplicates at higher loss, and showed expected
increase in retransmission/time with loss.
