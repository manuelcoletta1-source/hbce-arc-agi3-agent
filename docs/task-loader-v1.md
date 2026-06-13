# ARC-AGI-3 Task Loader v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #2  
Mode: PUBLIC_TASK_LOADER_V1  
Boundary: safe local JSON loading only.

## Purpose

Task Loader v1 opens Milestone #2 by adding safe local loading for task-like JSON files.

It reads controlled local JSON files, validates the file boundary, parses JSON data, and normalizes the result through the public task adapter.

It does not execute dataset code.

## Pipeline position

Task Loader v1 extends the public pipeline:

task_loader → task_adapter → observer → world_model → planner → verification_scoring → trace_schema

## Capabilities

Task Loader v1 provides:

- single local JSON task loading
- deterministic directory listing
- deterministic directory loading
- base directory boundary enforcement
- JSON-root validation
- file-size guard
- normalized task adapter output
- loaded-task validation contract

## Safety boundary

Task Loader v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory

## Acceptance criteria

Task Loader v1 is PASS only if:

- all tests pass
- local JSON task files load deterministically
- non-JSON files are rejected
- base_dir escape is rejected
- loaded output validates
- loaded output feeds observer and world model
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_TASK_LOADER_V1_READY=true  
ARC_AGI3_TASK_LOADER_STATUS=TASK_LOADER_READY  
ARC_AGI3_TASK_LOADER_PIPELINE_STATUS=TASK_LOADER_PIPELINE_READY  
ARC_AGI3_TASK_LOADER_VALIDATION=TASK_LOADER_VALID  
ARC_AGI3_TASK_LOADER_EXECUTES_DATASET_CODE=false  
ARC_AGI3_TASK_LOADER_LOCAL_JSON_ONLY=true  
ARC_AGI3_MILESTONE_2_TASK_1_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
