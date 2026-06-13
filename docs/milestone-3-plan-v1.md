# ARC-AGI-3 Milestone #3 Plan v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Branch: main  
Previous milestone: Milestone #2  
Previous milestone status: MILESTONE_2_CLOSED_PASS  
Previous closure commit: `47fd32e Close ARC AGI3 milestone 2`  
Mode: PUBLIC_RND_NEXT_PHASE  
Boundary: public deterministic R&D only.

## Purpose

Milestone #3 opens the next public ARC-AGI-3 development phase after the successful closure of Milestone #2.

Milestone #2 created the deterministic baseline chain:

task_loader → environment_harness → object_model → rule_hypothesis → planner_strategy → outcome_verification → score_calibration → benchmark_report → kaggle_dry_run_package → milestone_closure

Milestone #3 moves from a single-task deterministic baseline toward a multi-task benchmark execution layer.

The goal is not to send a Kaggle submission yet. The goal is to build a stronger public preparation layer that can run multiple tasks, aggregate outcomes, generate indexed reports, and prepare a local submission candidate without exposing private HBCE/JOKER-C2 runtime logic.

## Milestone #3 objective

Milestone #3 objective:

Build a deterministic multi-task public benchmark pipeline for ARC-AGI-3 preparation.

Core direction:

- multi-task benchmark input registry
- batch runner
- prediction/result aggregation
- strategy selection index
- failure taxonomy
- report index
- local submission candidate builder
- readiness audit
- milestone closure

## Planned task chain

### Task 1 — Dataset Sample Registry v1

Create a public-safe registry structure for sample ARC-style tasks.

Expected output:

- sample task index
- deterministic task identifiers
- public-safe metadata
- no dataset code execution
- no credentials
- validation tests

### Task 2 — Batch Benchmark Runner v1

Create a deterministic batch runner that processes multiple sample tasks through the public pipeline.

Expected output:

- batch run object
- per-task execution records
- aggregate result object
- public-safe metadata
- validation tests

### Task 3 — Multi-Task Outcome Aggregator v1

Aggregate outcome verification and score calibration across multiple tasks.

Expected output:

- total tasks
- matched tasks
- partial tasks
- failed tasks
- unverified tasks
- average calibrated score
- aggregate quality band
- validation tests

### Task 4 — Strategy Selection Index v1

Create an index for selecting or ranking public strategy candidates.

Expected output:

- strategy candidates
- deterministic ranking
- score-linked selection
- no model calls
- no private strategy exposure
- validation tests

### Task 5 — Failure Taxonomy v1

Create a deterministic taxonomy for classifying ARC-style failures.

Expected output:

- shape mismatch
- partial cell mismatch
- object mismatch
- transformation mismatch
- unverified expected output
- validation tests

### Task 6 — Report Index Generator v1

Generate an indexed report across multiple benchmark reports.

Expected output:

- report index Markdown
- report index JSON
- per-task report links
- aggregate summary
- validation tests

### Task 7 — Local Submission Candidate Builder v1

Build a local-only submission candidate artifact.

Expected output:

- candidate manifest
- candidate predictions placeholder/structure
- deterministic package signature
- no Kaggle live submission
- validation tests

### Task 8 — Public Readiness Audit v1

Audit whether the public ARC-AGI-3 repo is ready for a controlled external review stage.

Expected output:

- readiness status
- public boundary checks
- missing-item diagnostics
- no credentials
- no private core exposure
- validation tests

### Task 9 — Milestone #3 Dry-Run Release Package v1

Create a local release/dry-run package for Milestone #3.

Expected output:

- manifest
- report index
- readiness audit
- hashes
- package signature
- validation tests

### Task 10 — Milestone #3 Report / Closure v1

Close Milestone #3 with a deterministic closure artifact.

Expected output:

- task chain
- commit chain
- tests passed
- dry-run release package
- public boundary
- readiness for next phase
- validation tests

## Public boundary

Milestone #3 must preserve:

- public_safe=true
- deterministic=true
- external_api_dependency=false
- executes_dataset_code=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false
- legalCertification=false

## Non-goals

Milestone #3 does not:

- submit to Kaggle
- claim leaderboard score
- call external AI APIs
- execute private dataset code
- expose HBCE private runtime code
- expose IPR memory
- expose private MATRIX/JOKER-C2 core
- claim legal or public authority certification

## Current public baseline

Milestone #2 closure baseline:

- closure commit: `47fd32e`
- closure status: `MILESTONE_2_CLOSED_PASS`
- tests passed: `107 passed`
- dry-run package: `KAGGLE-DRYRUN-41C18DE4A1D2`
- closure signature: `EDFD1234147D5021`
- Kaggle submission sent: `false`

## Acceptance criteria

Milestone #3 is open when:

- this plan exists in the public repo
- operational markers are present
- tests still pass from the previous baseline
- the plan is committed and pushed to main

## Operational markers

ARC_AGI3_MILESTONE_3_PLAN_V1_READY=true  
ARC_AGI3_MILESTONE_3_STATUS=OPEN_READY  
ARC_AGI3_MILESTONE_3_PREVIOUS_MILESTONE=MILESTONE_2_CLOSED_PASS  
ARC_AGI3_MILESTONE_3_PREVIOUS_CLOSURE_COMMIT=47fd32e  
ARC_AGI3_MILESTONE_3_TASKS_PLANNED=10  
ARC_AGI3_MILESTONE_3_PUBLIC_RND_NEXT_PHASE=true  
ARC_AGI3_MILESTONE_3_MULTI_TASK_PIPELINE_TARGET=true  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
