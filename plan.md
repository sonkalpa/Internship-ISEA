# Execution Plan and Milestones

## Plan Goal

Complete Assignments 1 through 4 with the same quality standard, and keep
progress fully traceable in repository docs.

## Milestone Board

| Milestone | Status | Target Output |
|---|---|---|
| M1 - Assignment 1 foundation | Completed | `assignment1/` folder with code and README added |
| M2 - Assignment 1 validation and evidence | Completed | WSL run, screenshots, `report.pdf`, and submission checker validation completed |
| M3 - Assignment 3 foundation | Completed | `assignment3/` folder with `raw_capture.c` and README added |
| M4 - Assignment 3 validation and evidence | Completed | WSL run completed with `program_output.txt`, `capture.pcapng`, screenshots, and `report.pdf` |
| M5 - Final consolidation (A1-A3) | Completed | root docs refreshed and evidence checkers passing |
| M6 - Assignment 4 execution | In Progress | Mininet run, performance CSV, graphs, screenshots, and report generated; final reviewer pass pending |

## Work Breakdown

### Milestone M1 - Assignment 1 foundation

- Create `assignment1/` structure.
- Add initial implementation files.
- Add `assignment1/README.md` with objective and run steps.

### Milestone M2 - Assignment 1 validation and evidence

- Execute tests in target environment.
- Generate logs and capture evidence.
- Add summary tables/graphs if required.
- Update `README.md`, `prd.md`, and `plan.md`.

### Milestone M3 - Assignment 3 foundation

- Create `assignment3/` structure.
- Add raw socket analysis scripts.
- Add `assignment3/README.md` with usage and expected outputs.

### Milestone M4 - Assignment 3 validation and evidence

- Run packet analysis scenarios.
- Save outputs/screenshots and protocol observations.
- Update `README.md`, `prd.md`, and `plan.md`.

### Milestone M5 - Final consolidation (A1-A3)

- Cross-check all assignment folders for completeness.
- Ensure each folder has reproducible run instructions.
- Finalize root documentation and progress table.

### Milestone M6 - Assignment 4 execution

- Read Assignment 4 statement and extract deliverables.
- Implement threaded chat server and client workflow.
- Run Mininet experiment and collect logs/capture evidence.
- Generate performance CSV, graphs, and final report artifacts.

## Tracking Rules

- After every milestone update, refresh all three files:
  - `README.md`
  - `prd.md`
  - `plan.md`
- Keep milestone states as: `Pending`, `In Progress`, `Completed`, or `Blocked`.
- Record notable updates under an inline update log.

## Update Log

- 2026-07-22: Plan initialized; Assignment 2 considered complete; Assignment 1 and 3 queued.
- 2026-07-22: Completed foundation setup for `assignment1/` and `assignment3/`; started Assignment 1 validation phase.
- 2026-07-22: Ran local validation for Assignment 1 and generated baseline `result_table.csv` + logs.
- 2026-07-22: Added Assignment 3 Linux execution checklist and packet comparison template.
- 2026-07-22: Standardized Assignment 1 and 3 structure with HOW_TO_RUN guides, report templates, and screenshot checklists.
- 2026-07-22: Added WSL-compatible Assignment 1 execution path using emulated loss and reply delay flags.
- 2026-07-22: Added `run_wsl_assignment1.sh` for one-command WSL execution without `tc/netem`.
- 2026-07-22: Added `run_wsl_assignment3.sh` and `generate_tcp_traffic.py` for one-command Assignment 3 execution.
- 2026-07-22: Added `run_wsl_assignment1.py` and wired shell runner to avoid Mininet CLI hang in WSL.
- 2026-07-22: Added automatic LinuxBridge fallback in Assignment 1 WSL runner for OVS service failures.
- 2026-07-22: Added loopback fallback in Assignment 1 WSL runner when OVS and LinuxBridge are both unavailable.
- 2026-07-22: Defaulted WSL execution to loopback mode to prevent OVS startup hangs.
- 2026-07-25: Completed Assignment 1 WSL execution and generated updated logs/result table.
- 2026-07-25: Added Assignment 1 `report.md` draft and `check_submission.py` validator.
- 2026-07-25: Completed Assignment 1 screenshots and report PDF; submission check now passes.
- 2026-07-25: Completed Assignment 3 run artifacts (`program_output.txt`, `capture.pcapng`, traffic output, and system details).
- 2026-07-25: Completed Assignment 3 packet comparison, report (`report.md` + `report.pdf`), and screenshot evidence set.
- 2026-07-25: Updated plan milestones to mark Assignment 3 complete and queued Assignment 4 kickoff.
- 2026-07-25: Initialized `assignment4/` scaffold with threaded chat server/client and run guides.
- 2026-07-25: Generated Assignment 4 baseline `performance_results.csv` and graph files in `assignment4/graphs/`.
- 2026-07-25: Added WSL Mininet runner for Assignment 4 and generated `run_info.txt`, `system_details.txt`, and `capture.pcapng`.
- 2026-07-25: Generated Assignment 4 required screenshot set and finalized `report.md` + `report.pdf`.
