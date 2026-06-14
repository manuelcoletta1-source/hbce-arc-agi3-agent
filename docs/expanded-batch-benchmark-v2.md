# ARC AGI3 Milestone #4 Task 7 - Expanded Batch Benchmark v2

## Status

Expanded Batch Benchmark v2 connects the modern Milestone #4 solver pipeline to a deterministic multi-task benchmark.

Pipeline:

Candidate Generator v1
Candidate Ranker v1
Expanded Batch Benchmark v2

This is not a Kaggle submission. It is a local, public-safe, dry-run benchmark layer for measuring whether the candidate generator/ranker chain behaves consistently across more than one task.

## Operational purpose

Task 7 exists because a single smoke test is not enough. A solver that works once may be a solver, or it may be a lucky accident wearing a fake mustache. This benchmark introduces batch-level metrics before any submission logic is touched.

The module measures:

- tasks processed;
- candidate generation success rate;
- ranking success rate;
- best candidate match rate;
- average best score;
- best and worst task score;
- task-level failure reasons.

## Files

src/hbce_arc_agi3/expanded_batch_benchmark.py
scripts/run_expanded_batch_benchmark.py
tests/test_expanded_batch_benchmark.py
examples/milestone-4/expanded-batch-benchmark-v2/

## Boundary

public_safe=true
deterministic=true
local_only=true
dry_run_only=true
external_api_dependency=false
contains_api_keys=false
kaggle_submission_sent=false
private_core_exposure=false
legal_certification=false

## Markers

ARC_AGI3_MILESTONE_4_TASK_7_EXPANDED_BATCH_BENCHMARK_V2_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_STATUS=EXPANDED_BATCH_BENCHMARK_READY  
ARC_AGI3_MILESTONE_4_TASK_7_PIPELINE_STATUS=EXPANDED_BATCH_BENCHMARK_PIPELINE_READY  
ARC_AGI3_MILESTONE_4_TASK_7_VALIDATION=EXPANDED_BATCH_BENCHMARK_VALID  
ARC_AGI3_MILESTONE_4_TASK_7_TASKS_PROCESSED_MINIMUM_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_CANDIDATE_GENERATION_SUCCESS_RATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_RANKING_SUCCESS_RATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_BEST_CANDIDATE_MATCH_RATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_AVERAGE_BEST_SCORE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_USES_CANDIDATE_GENERATOR_V1=true  
ARC_AGI3_MILESTONE_4_TASK_7_USES_CANDIDATE_RANKER_V1=true  
ARC_AGI3_MILESTONE_4_TASK_7_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
