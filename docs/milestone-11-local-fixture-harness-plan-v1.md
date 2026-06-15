# ARC AGI3 Milestone #11 Task 4 - Local Fixture Harness Plan v1

Milestone #11 Task 4 creates a local diagnostic fixture harness plan after the public game failure taxonomy.

The previous task classified the current condition as `NO_LOCAL_PUBLIC_FIXTURES` and `MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE`. This task defines how to create local diagnostic fixtures and a deterministic harness without claiming public or private Kaggle score.

## Baseline

- baseline commit: b609069 Add ARC AGI3 public game failure taxonomy
- task mode: MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_LOCAL_ONLY
- task scope: LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_PLAN_NO_SCORE_NO_SUBMISSION
- task verdict: LOCAL_FIXTURE_HARNESS_PLAN_READY_FOR_DIAGNOSTIC_FIXTURE_GENERATION
- next stage: MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1
- primary classification: MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE
- solver failure detected: false
- solver not measured: true
- harness plan created: true
- diagnostic only: true
- fixture generation performed: false
- official score claim allowed: false
- synthetic fixture score claim allowed: false
- real public score claimed: false
- private score claimed: false
- real benchmark score: none
- real submission candidate created: false
- submission json created: false
- upload package created: false
- real submission decision: NOT_AUTHORIZED
- real submission allowed: false
- Kaggle authentication allowed: false
- Kaggle submission sent: false
- fail closed required: true
- fail closed active: true

## Harness components

1. local fixture loader
2. episode runner
3. observation trace recorder
4. world model probe
5. goal inference probe
6. planner probe
7. transition verifier probe
8. score boundary guard

## Fixture classes

1. object persistence fixture
2. color rule fixture
3. movement transition fixture
4. goal inference fixture
5. planner loop fixture
6. verifier mismatch fixture

## Boundary

Local diagnostic fixture results are not Kaggle scores. They are solver diagnostics only.

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

ARC_AGI3_MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY=true  
ARC_AGI3_MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1_VALID=true  
ARC_AGI3_MILESTONE_11_TASK_4_READY=true  
ARC_AGI3_MILESTONE_11_TASK_4_MODE=MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_LOCAL_ONLY  
ARC_AGI3_MILESTONE_11_TASK_4_VERDICT=LOCAL_FIXTURE_HARNESS_PLAN_READY_FOR_DIAGNOSTIC_FIXTURE_GENERATION  
ARC_AGI3_MILESTONE_11_TASK_4_BASELINE_COMMIT=b609069  
ARC_AGI3_MILESTONE_11_TASK_4_NEXT_STAGE=MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1  
ARC_AGI3_MILESTONE_11_PRIMARY_CLASSIFICATION=MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE  
ARC_AGI3_MILESTONE_11_SOLVER_FAILURE_DETECTED=false  
ARC_AGI3_MILESTONE_11_SOLVER_NOT_MEASURED=true  
ARC_AGI3_MILESTONE_11_DIAGNOSTIC_ONLY=true  
ARC_AGI3_MILESTONE_11_FIXTURE_GENERATION_PERFORMED=false  
ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false  
ARC_AGI3_MILESTONE_11_SYNTHETIC_FIXTURE_SCORE_CLAIM_ALLOWED=false  
ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false  
ARC_AGI3_MILESTONE_11_PRIVATE_SCORE_CLAIMED=false  
ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_CANDIDATE_CREATED=false  
ARC_AGI3_MILESTONE_11_SUBMISSION_JSON_CREATED=false  
ARC_AGI3_MILESTONE_11_UPLOAD_PACKAGE_CREATED=false  
ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED  
ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false  
ARC_AGI3_MILESTONE_11_KAGGLE_AUTHENTICATION_ALLOWED=false  
ARC_AGI3_MILESTONE_11_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_MILESTONE_11_FAIL_CLOSED_REQUIRED=true  
ARC_AGI3_MILESTONE_11_FAIL_CLOSED_ACTIVE=true  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
