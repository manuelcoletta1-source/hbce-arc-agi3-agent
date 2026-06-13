# ARC-AGI-3 Dataset Sample Registry v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #3  
Task: #1  
Mode: PUBLIC_DATASET_SAMPLE_REGISTRY_V1  
Boundary: deterministic public sample registry only.

## Purpose

Dataset Sample Registry v1 creates a deterministic public-safe registry for ARC-style sample tasks.

The registry provides stable sample identifiers, input and expected-output grids, shape metadata, sample signatures, registry signature, JSON artifact, Markdown artifact, and validation state.

It is the first building block of Milestone #3, where the public ARC-AGI-3 branch moves from a single-task deterministic baseline into a multi-task benchmark pipeline.

## Pipeline position

Dataset Sample Registry v1 opens the Milestone #3 chain:

dataset_sample_registry → batch_benchmark_runner → multi_task_outcome_aggregator → strategy_selection_index → failure_taxonomy → report_index_generator → local_submission_candidate_builder → public_readiness_audit → milestone_3_dry_run_release_package → milestone_3_closure

## Capabilities

Dataset Sample Registry v1 provides:

- deterministic sample records
- stable sample IDs
- input grid validation
- expected output validation
- ARC color integer validation
- registry signature
- sample signatures
- JSON artifact generation
- Markdown artifact generation
- validation contract
- public-safe metadata

## Safety boundary

Dataset Sample Registry v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory
- send a Kaggle submission

## Acceptance criteria

Dataset Sample Registry v1 is PASS only if:

- all tests pass
- default samples are generated
- custom samples are accepted
- invalid grids are rejected
- missing names are rejected
- registry generation is deterministic
- Markdown artifact is generated
- JSON artifact is generated
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_DATASET_SAMPLE_REGISTRY_V1_READY=true  
ARC_AGI3_DATASET_SAMPLE_REGISTRY_STATUS=DATASET_SAMPLE_REGISTRY_READY  
ARC_AGI3_DATASET_SAMPLE_REGISTRY_PIPELINE_STATUS=DATASET_SAMPLE_REGISTRY_PIPELINE_READY  
ARC_AGI3_DATASET_SAMPLE_REGISTRY_VALIDATION=DATASET_SAMPLE_REGISTRY_VALID  
ARC_AGI3_DATASET_SAMPLE_REGISTRY_ARTIFACTS_READY=true  
ARC_AGI3_DATASET_SAMPLE_REGISTRY_SAMPLE_COUNT=3  
ARC_AGI3_MILESTONE_3_TASK_1_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
