# PRD - ISEA Internship Assignments

## 1) Product Overview

This repository documents and delivers internship assignments under the
Summer Internship on Cyber Security and Secure App Development.

Assignments in scope:

1. Assignment 1 - Reliable UDP in Mininet
2. Assignment 2 - TCP Wireshark Performance Analysis in Mininet
3. Assignment 3 - Raw Socket Packet Analysis
4. Assignment 4 - Multi-Client Chat Server over TCP
5. Assignment 5 - Advanced Multi-Client Chat Server over TCP
6. Assignment 6 - GUI-Based Multi-Client Chat Application over TCP

## 2) Objectives

- Build correct networking implementations required by each assignment.
- Collect measurable outputs (logs, tables, graphs, captures, screenshots).
- Provide reproducible run instructions and submission-ready documentation.
- Maintain continuous progress tracking across milestones.

## 3) Users and Reviewers

- Primary user: student maintainer of this repository.
- Reviewers: internship mentors/faculty evaluating technical correctness,
  reproducibility, and analysis quality.

## 4) Scope

### In Scope

- Code and scripts for assignment implementation.
- Mininet-based experiments and packet-level analysis.
- Report artifacts and evidence.
- Documentation updates in `README.md`, `prd.md`, and `plan.md` after each
  milestone update.

### Out of Scope

- Production deployment of services.
- Unrelated coursework or external projects.

## 5) Assignment Deliverables

### Assignment 1 - Reliable UDP

- Client/server implementation with reliability behavior over UDP.
- Logs proving delivery/acknowledgment behavior.
- Experiment notes for Mininet setup and execution.
- Assignment-specific README in `assignment1/`.

### Assignment 2 - TCP Performance

- Persistent vs new-connection comparison implementation.
- Response time and throughput measurements.
- Packet-capture evidence and generated graphs.
- Assignment-specific documentation in `assignment2/`.

### Assignment 3 - Raw Socket Packet Analysis

- Raw socket implementation and packet parsing/inspection outputs.
- Protocol-level observations with evidence.
- Assignment-specific README in `assignment3/`.

### Assignment 4 - Multi-Client Chat Server

- Concurrent TCP chat server implementation.
- Multi-client messaging validation evidence.
- Assignment-specific README in `assignment4/`.

### Assignment 5 - Advanced Chat Server

- Enhanced client state management and routing features.
- Private messaging, online user list, and persistent history evidence.
- Performance CSV, graphs, Wireshark verification screenshots, and report.

### Assignment 6 - GUI-Based Chat Application

- GUI client implementation over reused server/networking logic.
- GUI behavior evidence and wireshark verification screenshots.
- Assignment-specific documentation and final report.

## 6) Functional Requirements

- Each assignment folder must include runnable scripts and clear run steps.
- Output files must be structured and versioned in the same assignment folder.
- README files must explain objective, setup, run steps, and outputs.
- Milestone status must be reflected in `plan.md` and summarized in root
  `README.md`.

## 7) Non-Functional Requirements

- Reproducibility: steps should run on the documented environment.
- Traceability: outputs map directly to assignment objectives.
- Clarity: documentation readable by an evaluator without extra context.

## 8) Acceptance Criteria

- A1, A2, A3 each contain code + evidence + assignment README.
- A4 contains code + evidence + assignment README when that milestone is done.
- A5 and A6 each contain code + evidence + assignment README when done.
- Root `README.md` reflects latest overall progress.
- `plan.md` milestone table is current.
- `prd.md` is updated whenever scope or requirements materially change.

## 9) Risks and Dependencies

- Environment tooling (Mininet/Wireshark/raw socket permissions).
- Time needed to run repeated experiments and generate clean evidence.
- Requirement interpretation if assignment statements are incomplete.

## 10) Milestone Status (Current)

| Milestone | Status | Notes |
|---|---|---|
| M1 - Assignment 1 setup and implementation | Completed | `assignment1/` created with UDP client/server and README |
| M2 - Assignment 2 implementation and analysis | Completed | Existing deliverables in `assignment2/` |
| M3 - Assignment 3 setup and implementation | Completed | `assignment3/` created with raw socket code and README |
| M4 - Assignment 1 and 3 validation evidence | Completed | A1 and A3 evidence/report artifacts completed and verified |
| M5 - Final packaging for A1-A3 | Completed | root docs and milestone trackers refreshed |
| M6 - Assignment 4 execution | Completed | Mininet run completed with logs, capture evidence, screenshots, graphs, and report artifacts |
| M7 - Final packaging for A1-A4 | Completed | assignment-wise audit finished and zip-ready deliverables generated |
| M8 - Assignment 5 execution | Completed | advanced chat feature set, performance evidence, screenshots, and report artifacts generated |
| M9 - Assignment 6 execution | Completed | GUI client, verification evidence, screenshots, and report artifacts generated |
| M10 - Final packaging for A1-A6 | Completed | zip-ready deliverables generated in assignment folders and `submissions/` |

## 11) Change Log

- 2026-07-22: Initial PRD created for assignments 1-3 planning and milestone tracking.
- 2026-07-22: Updated PRD after adding `assignment1/` and `assignment3/` foundations.
- 2026-07-22: Updated PRD after Assignment 1 local validation output generation.
- 2026-07-22: Added Assignment 3 run-support artifacts for packet comparison workflow.
- 2026-07-22: Standardized Assignment 1 and 3 deliverable structure to match Assignment 2 organization style.
- 2026-07-22: Updated PRD with Assignment 1 WSL fallback execution strategy.
- 2026-07-22: Added Assignment 1 WSL automation script for terminal-only execution.
- 2026-07-22: Added Assignment 3 WSL automation and deterministic TCP traffic generation workflow.
- 2026-07-22: Improved Assignment 1 WSL automation with Python Mininet runner to prevent CLI blocking.
- 2026-07-22: Improved Assignment 1 WSL runner with automatic LinuxBridge fallback when OVS cannot start.
- 2026-07-22: Improved Assignment 1 WSL runner with automatic loopback fallback when switch backends are unavailable.
- 2026-07-22: Updated Assignment 1 runner to default to loopback mode on WSL for stability.
- 2026-07-25: Updated PRD after successful Assignment 1 WSL run output generation.
- 2026-07-25: Added Assignment 1 report draft and automated submission completeness checker.
- 2026-07-25: Updated PRD after Assignment 1 screenshot collection and final report generation.
- 2026-07-25: Updated PRD after Assignment 3 capture evidence, packet comparison, screenshots, and report completion.
- 2026-07-25: Expanded assignment scope to include Assignment 4 planning milestone.
- 2026-07-25: Started Assignment 4 implementation with server/client scaffold, performance runner, and graph generator.
- 2026-07-25: Added Assignment 4 WSL Mininet automation, packet-capture evidence generation, and submission checker.
- 2026-07-25: Generated Assignment 4 performance CSV, graphs, required screenshot set, and final report PDF.
- 2026-07-25: Added Assignment 2 WSL Mininet automation and completeness checker to close missing screenshot/report artifacts.
- 2026-07-25: Completed Assignment 2 requirement gaps and finalized `report.pdf`.
- 2026-07-25: Performed full A1-A4 requirement audit against assignment PDFs.
- 2026-07-25: Generated final zip submission packages for Assignments 1-4 under `submissions/`.
- 2026-08-01: Added Assignment 5 implementation, automation workflow, required evidence artifacts, checker, and report pipeline.
- 2026-08-01: Added Assignment 6 GUI client implementation, verification workflow, required screenshot set, checker, and report pipeline.
- 2026-08-01: Updated repository packaging to include A5 and A6 submission zip files.
