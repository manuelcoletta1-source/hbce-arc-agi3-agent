# ARC AGI3 Milestone #4 Task 9 - Candidate Ranker Task-Family Policy Fix v1

## Status

Task 9 fixes the failure isolated by the Failure-Driven Solver Improvement Loop v1.

The failed case was:

EXPANDED-BATCH-V2-COLOR-ONLY

Before the fix, the ranker selected COLOR_SHAPE_COMBINED even though the task family was color_transform and the expected candidate type was COLOR_REMAP.

## Fix

candidate_ranker.py now includes a task-family-aware ranking policy.

For color_transform tasks:

- COLOR_REMAP receives a positive task-family policy adjustment.
- COLOR_SHAPE_COMBINED receives a negative task-family policy adjustment.
- SHAPE_TRANSFORM receives a smaller negative adjustment.

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

ARC_AGI3_MILESTONE_4_TASK_9_CANDIDATE_RANKER_TASK_FAMILY_POLICY_FIX_READY=true  
ARC_AGI3_MILESTONE_4_TASK_9_COLOR_ONLY_REMAP_SELECTED=true  
ARC_AGI3_MILESTONE_4_TASK_9_EXPANDED_BATCH_MATCH_RATE_FIXED=true  
ARC_AGI3_MILESTONE_4_TASK_9_FAILURE_LOOP_CLOSED=true  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
