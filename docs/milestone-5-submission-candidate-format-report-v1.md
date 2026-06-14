# ARC AGI3 Milestone #5 - Submission Candidate Format Report v1

## Status

Milestone #5 Task 8 validates the local smoke-only submission candidate format.

This report is not a Kaggle submission. It does not create a real `submission.json`, does not authenticate with Kaggle, does not upload files, does not call external APIs, does not read secrets or tokens, and does not create any legal certification claim.

## Baseline

- baseline local smoke test commit: 47d47d2 Add ARC AGI3 local submission smoke test
- candidate kind: LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY
- expected submission filename: submission.json
- submission mode: LOCAL_SMOKE_ONLY_NO_UPLOAD
- candidate task count: 3
- valid task count: 3
- format gate count: 14
- format issue count: 0
- warning count: 0
- ready for submission candidate dry-run: true
- ready for Milestone #5 closure: true
- ready for real Kaggle submission: false
- Kaggle submission sent: false

## Format requirements

Each candidate task must contain:

- task_id
- attempt_1
- attempt_2

Each attempt must be a rectangular integer grid with values from 0 to 9.

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

ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_V1_READY=true  
ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_VALID=true  
ARC_AGI3_MILESTONE_5_SUBMISSION_FILENAME=submission.json  
ARC_AGI3_MILESTONE_5_CANDIDATE_KIND=LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY  
ARC_AGI3_MILESTONE_5_SUBMISSION_MODE=LOCAL_SMOKE_ONLY_NO_UPLOAD  
ARC_AGI3_MILESTONE_5_CANDIDATE_TASK_COUNT=3  
ARC_AGI3_MILESTONE_5_VALID_TASK_COUNT=3  
ARC_AGI3_MILESTONE_5_FORMAT_GATE_COUNT=14  
ARC_AGI3_MILESTONE_5_FORMAT_ISSUE_COUNT=0  
ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_CANDIDATE_DRY_RUN=true  
ARC_AGI3_MILESTONE_5_READY_FOR_MILESTONE_5_CLOSURE=true  
ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false  
ARC_AGI3_MILESTONE_5_BASELINE_LOCAL_SMOKE_TEST_COMMIT=47d47d2  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
