# ARC AGI3 Milestone #5 - Local Submission Smoke Test v1

## Status

- status: MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY
- smoke_id: MILESTONE-5-LOCAL-SMOKE-0F0FDCE696D4
- signature: 0F0FDCE696D480F9
- baseline_commit: 3c56cd7 Add ARC AGI3 Kaggle submission preflight report
- preflight_report_id: MILESTONE-5-PREFLIGHT-REPORT-2BE57C675A9B
- preflight_report_signature: 2BE57C675A9BE695
- smoke_mode: LOCAL_SMOKE_ONLY_NO_UPLOAD
- candidate_kind: LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY
- expected_submission_filename: submission.json
- smoke_case_count: 3
- smoke_case_passed_count: 3
- candidate_task_count: 3
- ready_for_submission_candidate_format_report: True
- ready_for_real_kaggle_submission: False
- kaggle_submission_sent: False

## Smoke cases

- SMOKE-TASK-IDENTITY-2X2: strategy=identity_grid_passthrough passed=True
- SMOKE-TASK-COLOR-REMAP-2X2: strategy=foreground_to_constant_color passed=True
- SMOKE-TASK-OBJECT-FILL-3X3: strategy=single_object_fill passed=True

## Local submission candidate

- candidate_kind: LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY
- submission_filename: submission.json
- submission_mode: LOCAL_SMOKE_ONLY_NO_UPLOAD
- task_count: 3
- kaggle_submission_sent: False

## Next actions

- create_submission_candidate_format_report_v1
- create_submission_candidate_dry_run_v1
- close_milestone_5_submission_preparation_v1

## Boundary

- public_safe=true
- deterministic=true
- local_only=true
- dry_run_only=true
- external_api_dependency=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false
- legal_certification=false

## Markers

ARC_AGI3_MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_V1_READY=true
ARC_AGI3_MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_VALID=true
ARC_AGI3_MILESTONE_5_LOCAL_SMOKE_ONLY_NO_UPLOAD=true
ARC_AGI3_MILESTONE_5_EXPECTED_SUBMISSION_FILENAME=submission.json
ARC_AGI3_MILESTONE_5_SMOKE_CASE_COUNT=3
ARC_AGI3_MILESTONE_5_SMOKE_CASE_PASSED_COUNT=3
ARC_AGI3_MILESTONE_5_CANDIDATE_TASK_COUNT=3
ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_CANDIDATE_FORMAT_REPORT=true
ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false
ARC_AGI3_MILESTONE_5_BASELINE_PREFLIGHT_REPORT_COMMIT=3c56cd7
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
ARC_AGI3_LEGAL_CERTIFICATION=false
