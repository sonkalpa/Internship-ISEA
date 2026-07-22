# PRD - ISEA Internship Assignments

## 1) Product Overview

This repository documents and delivers three internship assignments under the
Summer Internship on Cyber Security and Secure App Development.

Assignments in scope:

1. Assignment 1 - Reliable UDP in Mininet
2. Assignment 2 - TCP Wireshark Performance Analysis in Mininet
3. Assignment 3 - Raw Socket Packet Analysis

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
| M4 - Assignment 1 and 3 validation evidence | In Progress | A1 includes one-command WSL runner; Mininet/Wireshark final evidence pending |
| M5 - Final internship packaging and review | Not Started | Depends on M4 completion |

## 11) Change Log

- 2026-07-22: Initial PRD created for assignments 1-3 planning and milestone tracking.
- 2026-07-22: Updated PRD after adding `assignment1/` and `assignment3/` foundations.
- 2026-07-22: Updated PRD after Assignment 1 local validation output generation.
- 2026-07-22: Added Assignment 3 run-support artifacts for packet comparison workflow.
- 2026-07-22: Standardized Assignment 1 and 3 deliverable structure to match Assignment 2 organization style.
- 2026-07-22: Updated PRD with Assignment 1 WSL fallback execution strategy.
- 2026-07-22: Added Assignment 1 WSL automation script for terminal-only execution.
