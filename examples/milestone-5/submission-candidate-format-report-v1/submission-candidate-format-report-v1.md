# ARC AGI3 Milestone #5 - Submission Candidate Format Report v1

## Status

- status: MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY
- report_id: MILESTONE-5-CANDIDATE-FORMAT-05303A620DD2
- signature: 05303A620DD2F362
- baseline_commit: 47d47d2 Add ARC AGI3 local submission smoke test
- local_smoke_id: MILESTONE-5-LOCAL-SMOKE-0F0FDCE696D4
- local_smoke_signature: 0F0FDCE696D480F9
- candidate_kind: LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY
- submission_filename: submission.json
- submission_mode: LOCAL_SMOKE_ONLY_NO_UPLOAD
- candidate_task_count: 3
- valid_task_count: 3
- format_gate_count: 14
- passed_gate_count: 14
- format_issue_count: 0
- warning_count: 0
- ready_for_submission_candidate_dry_run: True
- ready_for_milestone_5_closure: True
- ready_for_real_kaggle_submission: False
- kaggle_submission_sent: False

## Task format statuses

- SMOKE-TASK-IDENTITY-2X2: valid=True attempt_1_grid_valid=True attempt_2_grid_valid=True
- SMOKE-TASK-COLOR-REMAP-2X2: valid=True attempt_1_grid_valid=True attempt_2_grid_valid=True
- SMOKE-TASK-OBJECT-FILL-3X3: valid=True attempt_1_grid_valid=True attempt_2_grid_valid=True

## Format gates

- local_smoke_test_present: passed=True severity=PASS
- local_candidate_present: passed=True severity=PASS
- local_smoke_test_ready: passed=True severity=PASS
- local_candidate_kind_valid: passed=True severity=PASS
- submission_filename_valid: passed=True severity=PASS
- submission_mode_valid: passed=True severity=PASS
- candidate_tasks_present: passed=True severity=PASS
- candidate_task_count_matches_smoke_test: passed=True severity=PASS
- all_task_ids_valid: passed=True severity=PASS
- all_attempt_keys_present: passed=True severity=PASS
- all_attempt_grids_valid: passed=True severity=PASS
- candidate_json_serializable: passed=True severity=PASS
- candidate_boundary_intact: passed=True severity=PASS
- kaggle_submission_not_sent: passed=True severity=PASS

## Format issues

- missing_local_smoke_test: active=False severity=BLOCKING
- missing_local_candidate: active=False severity=BLOCKING
- local_smoke_test_not_ready: active=False severity=BLOCKING
- candidate_kind_invalid: active=False severity=BLOCKING
- submission_filename_invalid: active=False severity=BLOCKING
- submission_mode_invalid: active=False severity=BLOCKING
- candidate_tasks_missing: active=False severity=BLOCKING
- candidate_task_count_mismatch: active=False severity=BLOCKING
- task_id_invalid: active=False severity=BLOCKING
- attempt_key_missing: active=False severity=BLOCKING
- attempt_grid_invalid: active=False severity=BLOCKING
- candidate_json_not_serializable: active=False severity=BLOCKING
- boundary_violation: active=False severity=BLOCKING
- kaggle_submission_already_sent: active=False severity=BLOCKING

## Candidate preview

- candidate_kind: LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY
- submission_filename: submission.json
- submission_mode: LOCAL_SMOKE_ONLY_NO_UPLOAD
- task_count: 3
- kaggle_submission_sent: False

## Next actions

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
