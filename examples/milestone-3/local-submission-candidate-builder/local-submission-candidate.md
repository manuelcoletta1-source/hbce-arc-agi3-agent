# ARC-AGI-3 Local Submission Candidate Builder v1

Status: LOCAL_SUBMISSION_CANDIDATE_BUILDER_READY
Candidate status: LOCAL_SUBMISSION_CANDIDATE_VALID
Candidate ID: LOCAL-SUBMISSION-CANDIDATE-E226DE7C08C2
Report index ID: REPORT-INDEX-380079FFB6E9
Batch ID: BATCH-BENCHMARK-5748D8399B3A
Registry ID: DATASET-SAMPLE-REGISTRY-21F03BA2C85E
Aggregate ID: MULTI-TASK-OUTCOME-9A52836EEB09
Strategy index ID: STRATEGY-SELECTION-INDEX-6DA2C585190E
Failure taxonomy report ID: FAILURE-TAXONOMY-REPORT-FC3663E93EA3
Selected strategy: identity_baseline_v1
Submission mode: LOCAL_DRY_RUN_ONLY
Task count: 3
Eligible task count: 2
Blocked task count: 1
Remediation required count: 1
Ready for public readiness audit: true
Ready for Kaggle submission: false
Kaggle submission sent: false

## Candidate tasks

### BATCH-TASK-CCBB59ECD386

- Sample ID: SAMPLE-1DE9E816D958
- Sample name: preserve-non-background
- Outcome status: OUTCOME_MATCH
- Failure class: NO_FAILURE_EXACT_MATCH
- Severity: NONE
- Eligible for submission: true
- Local output status: LOCAL_TASK_OUTPUT_ACCEPTED_BASELINE
- Local prediction ref: LOCAL-PREDICTION-BA520FB41CF1
- Remediation required: false
- Signature: F8E849E5513FB343

### BATCH-TASK-CCC2336D8AF5

- Sample ID: SAMPLE-84E8BE15DED7
- Sample name: identity-single-object
- Outcome status: OUTCOME_MATCH
- Failure class: NO_FAILURE_EXACT_MATCH
- Severity: NONE
- Eligible for submission: true
- Local output status: LOCAL_TASK_OUTPUT_ACCEPTED_BASELINE
- Local prediction ref: LOCAL-PREDICTION-4FC9200BBB3B
- Remediation required: false
- Signature: D92FCC346DE365C3

### BATCH-TASK-CF3376CA69F0

- Sample ID: SAMPLE-B4DD92F8949D
- Sample name: partial-transform-reference
- Outcome status: OUTCOME_PARTIAL
- Failure class: PARTIAL_TRANSFORM_REFERENCE_MISMATCH
- Severity: LOW
- Eligible for submission: false
- Local output status: LOCAL_TASK_OUTPUT_PARTIAL_REPAIR_REQUIRED
- Local prediction ref: LOCAL-PREDICTION-B45927BC5B86
- Remediation required: true
- Signature: 6839E17774CF56A2

## Boundary

- local_only=true
- dry_run_only=true
- public_safe=true
- deterministic=true
- external_api_dependency=false
- executes_dataset_code=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false

Candidate signature: E226DE7C08C2B5EE
