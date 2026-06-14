# ARC AGI3 Milestone #5 - Submission Candidate Dry-Run Package v1

## Status

- status: MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY
- package_id: MILESTONE-5-DRY-RUN-CANDIDATE-7B89C4D5AA87
- signature: 7B89C4D5AA872D5B
- baseline_commit: d2f2750 Add ARC AGI3 submission candidate format report
- format_report_id: MILESTONE-5-CANDIDATE-FORMAT-05303A620DD2
- format_report_signature: 05303A620DD2F362
- local_smoke_id: MILESTONE-5-LOCAL-SMOKE-0F0FDCE696D4
- local_smoke_signature: 0F0FDCE696D480F9
- package_mode: LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD
- candidate_kind: LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY
- submission_filename: submission.json
- submission_mode: LOCAL_SMOKE_ONLY_NO_UPLOAD
- package_artifact_count: 5
- ready_artifact_count: 5
- package_gate_count: 16
- passed_gate_count: 16
- package_issue_count: 0
- warning_count: 0
- candidate_task_count: 3
- dry_run_package_ready: True
- ready_for_milestone_5_closure: True
- ready_for_real_kaggle_submission: False
- kaggle_submission_sent: False

## Artifact statuses

- submission_candidate_format_report: present=True ready=True sha256_16=2AE350CF32308D83
- local_submission_candidate_smoke_only: present=True ready=True sha256_16=6EF4BA5C672A5CEC
- local_submission_smoke_test: present=True ready=True sha256_16=6186E30D0D9DAF08
- kaggle_submission_preflight_report: present=True ready=True sha256_16=799DCFAD290C78E6
- public_safety_boundary_checklist: present=True ready=True sha256_16=E10096494F15DC71

## Package gates

- format_report_present: passed=True severity=PASS
- format_report_ready: passed=True severity=PASS
- local_candidate_present: passed=True severity=PASS
- local_candidate_valid: passed=True severity=PASS
- local_smoke_test_ready: passed=True severity=PASS
- preflight_report_ready: passed=True severity=PASS
- public_safety_checklist_ready: passed=True severity=PASS
- all_package_artifacts_present: passed=True severity=PASS
- all_package_artifacts_ready: passed=True severity=PASS
- candidate_task_count_matches_format_report: passed=True severity=PASS
- format_report_allows_dry_run: passed=True severity=PASS
- boundary_intact: passed=True severity=PASS
- candidate_json_serializable: passed=True severity=PASS
- package_mode_local_only: passed=True severity=PASS
- package_no_archive_no_upload: passed=True severity=PASS
- kaggle_submission_not_sent: passed=True severity=PASS

## Package issues

- format_report_missing: active=False severity=BLOCKING
- format_report_not_ready: active=False severity=BLOCKING
- local_candidate_missing: active=False severity=BLOCKING
- local_candidate_invalid: active=False severity=BLOCKING
- local_smoke_test_not_ready: active=False severity=BLOCKING
- preflight_report_not_ready: active=False severity=BLOCKING
- public_safety_checklist_not_ready: active=False severity=BLOCKING
- package_artifact_missing: active=False severity=BLOCKING
- package_artifact_not_ready: active=False severity=BLOCKING
- candidate_task_count_mismatch: active=False severity=BLOCKING
- format_report_dry_run_not_allowed: active=False severity=BLOCKING
- boundary_violation: active=False severity=BLOCKING
- candidate_json_not_serializable: active=False severity=BLOCKING
- package_mode_invalid: active=False severity=BLOCKING
- archive_or_upload_mode_detected: active=False severity=BLOCKING
- kaggle_submission_already_sent: active=False severity=BLOCKING

## Dry-run index

- package_mode: LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD
- artifact_count: 5
- ready_artifact_count: 5
- contains_archive: False
- contains_upload_step: False
- contains_real_kaggle_submission: False

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

ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_V1_READY=true
ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_VALID=true
ARC_AGI3_MILESTONE_5_DRY_RUN_PACKAGE_MODE=LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD
ARC_AGI3_MILESTONE_5_PACKAGE_ARTIFACT_COUNT=5
ARC_AGI3_MILESTONE_5_READY_ARTIFACT_COUNT=5
ARC_AGI3_MILESTONE_5_PACKAGE_GATE_COUNT=16
ARC_AGI3_MILESTONE_5_PACKAGE_ISSUE_COUNT=0
ARC_AGI3_MILESTONE_5_CANDIDATE_TASK_COUNT=3
ARC_AGI3_MILESTONE_5_DRY_RUN_PACKAGE_READY=true
ARC_AGI3_MILESTONE_5_READY_FOR_MILESTONE_5_CLOSURE=true
ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false
ARC_AGI3_MILESTONE_5_BASELINE_CANDIDATE_FORMAT_REPORT_COMMIT=d2f2750
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
ARC_AGI3_LEGAL_CERTIFICATION=false
