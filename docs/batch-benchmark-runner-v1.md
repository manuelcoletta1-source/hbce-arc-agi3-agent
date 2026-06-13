# ARC-AGI-3 Batch Benchmark Runner v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #3  
Task: #2  
Mode: PUBLIC_BATCH_BENCHMARK_RUNNER_V1  
Boundary: deterministic public batch runner only.

## Purpose

Batch Benchmark Runner v1 runs the public Dataset Sample Registry v1 records through a deterministic baseline runner.

It creates per-task benchmark records, deterministic predictions, exact-match status, mismatch counts, cell accuracy, batch-level aggregate metrics, JSON artifact, Markdown artifact, and validation state.

This module is the second building block of Milestone #3 and prepares the repository for multi-task outcome aggregation.

## Pipeline position

Batch Benchmark Runner v1 extends the Milestone #3 chain:

dataset_sample_registry → batch_benchmark_runner → multi_task_outcome_aggregator → strategy_selection_index → failure_taxonomy → report_index_generator → local_submission_candidate_builder → public_readiness_audit → milestone_3_dry_run_release_package → milestone_3_closure

## Input

Batch Benchmark Runner v1 consumes:

- Dataset Sample Registry v1
- registry ID
- registry samples
- sample input grids
- sample expected outputs
- sample metadata

## Output

Batch Benchmark Runner v1 produces:

- batch run ID
- per-task benchmark records
- deterministic predictions
- exact match count
- mismatch count
- verified count
- average cell accuracy
- task signatures
- batch signature
- JSON artifact
- Markdown artifact

## Public strategy

The initial public runner uses:

`identity_baseline_v1`

This strategy predicts the input grid as the output grid. It is intentionally simple, deterministic, public, and safe. Later Milestone #3 modules may rank or select richer public strategies without exposing private HBCE/JOKER-C2 logic.

## Safety boundary

Batch Benchmark Runner v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory
- send a Kaggle submission

## Acceptance criteria

Batch Benchmark Runner v1 is PASS only if:

- all tests pass
- Dataset Sample Registry v1 is consumed
- batch records are generated
- deterministic predictions are generated
- matched and mismatched counts are calculated
- average cell accuracy is calculated
- registry payload validation is enforced
- unsupported private strategies are rejected
- Markdown artifact is generated
- JSON artifact is generated
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_BATCH_BENCHMARK_RUNNER_V1_READY=true  
ARC_AGI3_BATCH_BENCHMARK_STATUS=BATCH_BENCHMARK_RUN_READY  
ARC_AGI3_BATCH_BENCHMARK_PIPELINE_STATUS=BATCH_BENCHMARK_PIPELINE_READY  
ARC_AGI3_BATCH_BENCHMARK_VALIDATION=BATCH_BENCHMARK_RUN_VALID  
ARC_AGI3_BATCH_BENCHMARK_USES_DATASET_SAMPLE_REGISTRY=true  
ARC_AGI3_BATCH_BENCHMARK_TASK_COUNT=3  
ARC_AGI3_BATCH_BENCHMARK_MATCHED_COUNT=2  
ARC_AGI3_BATCH_BENCHMARK_MISMATCHED_COUNT=1  
ARC_AGI3_BATCH_BENCHMARK_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_3_TASK_2_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
