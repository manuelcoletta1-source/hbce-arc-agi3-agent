# ARC-AGI-3 Environment Harness v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #2  
Mode: PUBLIC_ENVIRONMENT_HARNESS_V1  
Boundary: deterministic local execution wrapper only.

## Purpose

Environment Harness v1 executes a loaded local task through the current public ARC-AGI-3 baseline pipeline.

It does not solve ARC-AGI-3 by declaration. It creates a deterministic execution wrapper so that every task attempt can produce a comparable public run object.

## Pipeline position

Environment Harness v1 connects:

task_loader → task_adapter → observer → world_model → planner → verification_scoring → trace_schema

## Capabilities

Environment Harness v1 provides:

- task-file execution through the public pipeline
- loaded-task execution entrypoint
- deterministic run id
- full observation/world/plan/verification/score/trace output
- trace validation
- run validation contract
- public-safe metadata

## Safety boundary

Environment Harness v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory

## Acceptance criteria

Environment Harness v1 is PASS only if:

- all tests pass
- task files run through the full public pipeline
- run ids are deterministic
- trace schema validation passes
- invalid loaded input fails safely
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_ENVIRONMENT_HARNESS_V1_READY=true  
ARC_AGI3_ENVIRONMENT_HARNESS_STATUS=ENVIRONMENT_HARNESS_READY  
ARC_AGI3_ENVIRONMENT_HARNESS_PIPELINE_STATUS=ENVIRONMENT_HARNESS_PIPELINE_READY  
ARC_AGI3_ENVIRONMENT_HARNESS_VALIDATION=ENVIRONMENT_HARNESS_VALID  
ARC_AGI3_ENVIRONMENT_HARNESS_TRACE_VALIDATION=TRACE_SCHEMA_VALID  
ARC_AGI3_ENVIRONMENT_HARNESS_EXECUTES_DATASET_CODE=false  
ARC_AGI3_MILESTONE_2_TASK_2_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
