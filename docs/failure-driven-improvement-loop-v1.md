# ARC AGI3 Milestone #4 Task 8 - Failure-Driven Solver Improvement Loop v1

## Status

Failure-Driven Solver Improvement Loop v1 uses the Expanded Batch Benchmark v2 output to identify solver failures and convert them into concrete improvement targets.

## Operational purpose

The purpose of Task 8 is to stop treating benchmark output as decoration. The loop reads task-level benchmark results, isolates mismatches, classifies the failure, selects the target module, and emits the recommended next solver action.

The first observed failure comes from the color-only benchmark task:

EXPANDED-BATCH-V2-COLOR-ONLY

The task family is color_transform, but the ranker selects COLOR_SHAPE_COMBINED as best candidate. The improvement target is therefore candidate_ranker.py, with a task-family-aware ranking rule.

## Files

src/hbce_arc_agi3/failure_driven_improvement_loop.py
scripts/run_failure_driven_improvement_loop.py
tests/test_failure_driven_improvement_loop.py
examples/milestone-4/failure-driven-improvement-loop-v1/

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

ARC_AGI3_MILESTONE_4_TASK_8_FAILURE_DRIVEN_IMPROVEMENT_LOOP_V1_READY=true  
ARC_AGI3_MILESTONE_4_TASK_8_STATUS=FAILURE_DRIVEN_IMPROVEMENT_LOOP_READY  
ARC_AGI3_MILESTONE_4_TASK_8_VALIDATION=FAILURE_DRIVEN_IMPROVEMENT_LOOP_VALID  
ARC_AGI3_MILESTONE_4_TASK_8_USES_EXPANDED_BATCH_BENCHMARK_V2=true  
ARC_AGI3_MILESTONE_4_TASK_8_FAILURE_CLASSIFICATION_READY=true  
ARC_AGI3_MILESTONE_4_TASK_8_NEXT_SOLVER_TARGET_READY=true  
ARC_AGI3_MILESTONE_4_TASK_8_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
