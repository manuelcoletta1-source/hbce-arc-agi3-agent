# ARC-AGI-3 Milestone #2 Plan

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Mode: PUBLIC_RND_BASELINE_MILESTONE_2_PLAN  
Previous milestone: Milestone #1 CLOSED_PASS  
Previous final commit: f7ee3c8  
Boundary: offline, deterministic, public-safe ARC-AGI-3 benchmark development.

## 1. Milestone #2 objective

Milestone #2 moves the project from a public deterministic skeleton baseline toward stronger ARC-AGI-3 task behavior.

Milestone #1 proved that the repository can support:

- task adapter
- observer
- world model
- planner
- verification and scoring
- trace schema
- submission package skeleton
- milestone reporting

Milestone #2 must now improve the agent’s actual task-processing capability without exposing private HBCE/JOKER-C2 runtime logic and without using external APIs.

## 2. Canonical Milestone #2 chain

The target chain is:

dataset_inspection → task_loader → task_adapter → environment_harness → observer → object_model → rule_hypothesis → planner_strategy → verification_scoring → trace_schema → dry_run_submission_package

## 3. Technical goals

Milestone #2 focuses on practical benchmark behavior.

The main goals are:

- create a safe task loader for local ARC-AGI-3 sample structures
- create an environment harness that can run deterministic task attempts
- expand object-level grid interpretation
- introduce rule hypothesis generation
- expand planner strategies beyond baseline symbolic actions
- calibrate verification and scoring against task outcomes
- generate richer public benchmark reports
- prepare Kaggle-ready dry-run packaging without sending a live submission

## 4. Planned tasks

| Task | Scope | Expected output | Status |
| --- | --- | --- | --- |
| 1 | Task loader v1 | safe local task loading contract | PLANNED |
| 2 | Environment harness v1 | deterministic execution wrapper | PLANNED |
| 3 | Object model v1 | connected components / object-level grid model | PLANNED |
| 4 | Rule hypothesis v1 | candidate transformation rules | PLANNED |
| 5 | Planner strategy expansion v1 | strategy selection from hypotheses | PLANNED |
| 6 | Outcome verification v1 | compare predicted output / expected-like structures when available | PLANNED |
| 7 | Score calibration v1 | scoring components linked to outcomes | PLANNED |
| 8 | Benchmark report generator v1 | public report from run traces | PLANNED |
| 9 | Kaggle dry-run package v1 | local dry-run package, no live submission | PLANNED |
| 10 | Milestone #2 report | closure report and parent registry update | PLANNED |

## 5. Safety and exposure boundary

Milestone #2 must not include:

- API keys
- Kaggle tokens
- private HBCE/JOKER-C2 runtime code
- private IPR memory
- proprietary corpus full text
- live Kaggle submission
- legal certification claims
- operational weaponization material

Mandatory boundary markers:

- ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
- ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
- ARC_AGI3_KAGGLE_SUBMISSION_SENT=false
- legalCertification=false

## 6. Acceptance criteria

Milestone #2 can close only when:

- all tests pass
- task loader is deterministic
- environment harness produces repeatable execution output
- object model produces stable object-level structures
- rule hypotheses are traceable
- planner strategy selection is deterministic
- verification/scoring can evaluate outcomes
- benchmark report generator works locally
- dry-run package validates
- no private runtime/code/keys are exposed

## 7. Starting point

Milestone #2 starts from:

- public repo final Milestone #1 commit: f7ee3c8
- parent registry commit: 5e70147
- Milestone #1 test status: 28 passed

## 8. Next immediate task

The next immediate task is:

Task 1 — Task loader v1

Purpose:

Create a safe local loader that can inspect and normalize task-like JSON structures from controlled local files without executing arbitrary dataset code.

## Operational markers

ARC_AGI3_MILESTONE_2_PLAN_READY=true  
ARC_AGI3_MILESTONE_2_STATUS=OPEN_PLANNED  
ARC_AGI3_MILESTONE_2_START_COMMIT=f7ee3c8  
ARC_AGI3_MILESTONE_2_PARENT_REGISTRY_COMMIT=5e70147  
ARC_AGI3_MILESTONE_2_NEXT_TASK=TASK_LOADER_V1  
ARC_AGI3_PUBLIC_BASELINE_MILESTONE_1_CLOSED=true  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
