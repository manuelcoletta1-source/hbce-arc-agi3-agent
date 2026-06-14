# ARC AGI3 Milestone #10 - Candidate Refresh v1

Milestone #10 Task 6 creates a controlled local candidate refresh after benchmark refresh.

The refresh creates a local candidate artifact and deterministic ranking package. It does not create a real submission candidate, does not create submission.json, does not upload, does not authenticate with Kaggle, and does not perform real submission. The next stage is a submission candidate rebuild gate.

## Baseline

- baseline commit: ed3aa9d Add ARC AGI3 benchmark refresh
- candidate mode: MILESTONE_10_CANDIDATE_REFRESH_V1_LOCAL_ONLY
- candidate scope: LOCAL_CANDIDATE_REFRESH_NO_REAL_SUBMISSION
- candidate verdict: CANDIDATE_REFRESH_READY_FOR_SUBMISSION_CANDIDATE_REBUILD_GATE
- next allowed stage: MILESTONE_10_TASK_7_SUBMISSION_CANDIDATE_REBUILD_GATE_V1
- candidate count: 4
- ranked candidate count: 4
- selected candidate count: 1
- selected candidate id: M10-CANDIDATE-BALANCED-PATCH-STACK-v1
- candidate check count: 26
- candidate case count: 10
- candidate pass count: 10
- candidate failure count: 0
- candidate refresh created: true
- candidate refresh ready: true
- candidate artifact created: true
- real submission candidate created: false
- submission json created: false
- upload package created: false
- rebuild gate required next: true
- real submission decision: NOT_AUTHORIZED
- real submission allowed: false
- manual upload allowed: false
- Kaggle authentication allowed: false
- Kaggle submission sent: false
- fail closed required: true
- fail closed active: true

## Candidate refresh outputs

1. Local candidate catalog
2. Deterministic candidate ranking
3. Selected candidate record
4. Candidate refresh package
5. Rebuild gate handoff markers

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

ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_V1_READY=true  
ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_V1_VALID=true  
ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_READY=true  
ARC_AGI3_MILESTONE_10_CANDIDATE_MODE=MILESTONE_10_CANDIDATE_REFRESH_V1_LOCAL_ONLY  
ARC_AGI3_MILESTONE_10_CANDIDATE_VERDICT=CANDIDATE_REFRESH_READY_FOR_SUBMISSION_CANDIDATE_REBUILD_GATE  
ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=ed3aa9d  
ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_7_SUBMISSION_CANDIDATE_REBUILD_GATE_V1  
ARC_AGI3_MILESTONE_10_CANDIDATE_COUNT=4  
ARC_AGI3_MILESTONE_10_RANKED_CANDIDATE_COUNT=4  
ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_COUNT=1  
ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_ID=M10-CANDIDATE-BALANCED-PATCH-STACK-v1  
ARC_AGI3_MILESTONE_10_CANDIDATE_CHECK_COUNT=26  
ARC_AGI3_MILESTONE_10_CANDIDATE_CASE_COUNT=10  
ARC_AGI3_MILESTONE_10_CANDIDATE_PASS_COUNT=10  
ARC_AGI3_MILESTONE_10_CANDIDATE_FAILURE_COUNT=0  
ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_CREATED=true  
ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_READY=true  
ARC_AGI3_MILESTONE_10_CANDIDATE_ARTIFACT_CREATED=true  
ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false  
ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false  
ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false  
ARC_AGI3_MILESTONE_10_REBUILD_GATE_REQUIRED_NEXT=true  
ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED  
ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_ALLOWED=false  
ARC_AGI3_MILESTONE_10_MANUAL_UPLOAD_ALLOWED=false  
ARC_AGI3_MILESTONE_10_KAGGLE_AUTHENTICATION_ALLOWED=false  
ARC_AGI3_MILESTONE_10_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_MILESTONE_10_FAIL_CLOSED_REQUIRED=true  
ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
