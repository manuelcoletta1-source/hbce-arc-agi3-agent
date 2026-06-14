# ARC AGI3 Milestone #5 - Submission Entrypoint Contract v1

## Status

- status: MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_READY
- contract_id: MILESTONE-5-ENTRYPOINT-CONTRACT-DDF92647579C
- signature: DDF92647579C4F56
- baseline_commit: 8dfb106 Add ARC AGI3 Kaggle submission dry-run package
- dry_run_package_id: MILESTONE-5-DRY-RUN-PACKAGE-09867B871A64
- dry_run_package_signature: 09867B871A647F41
- entrypoint_name: arc_agi3_submission_entrypoint
- entrypoint_mode: CONTRACT_ONLY_LOCAL_DRY_RUN
- entrypoint_runtime: PYTHON_LOCAL_ONLY
- expected_output_file: submission.json
- expected_smoke_mode: LOCAL_CONTRACT_SMOKE_ONLY
- ready_for_local_submission_smoke_test: True
- kaggle_submission_sent: False

## Required inputs

- repo_root: required=True - Path to local repository root.
- source_package: required=True - src/hbce_arc_agi3 local source tree.
- test_suite: required=True - tests local validation suite.
- dry_run_package: required=True - Milestone #5 Task 3 dry-run package JSON.
- public_repo_index: required=True - Milestone #5 Task 2 public repo release index JSON.

## Expected outputs

- submission_candidate_path: `submission.json` produced_by_contract_task=False
- entrypoint_report_json: `submission-entrypoint-contract-v1.json` produced_by_contract_task=True
- entrypoint_report_markdown: `submission-entrypoint-contract-v1.md` produced_by_contract_task=True
- entrypoint_contract_manifest: `submission-entrypoint-contract-manifest-v1.txt` produced_by_contract_task=True

## Allowed actions

- read_local_public_artifacts
- validate_local_contract
- render_contract_report
- render_contract_manifest
- run_local_tests
- produce_dry_run_metadata

## Blocked actions

- kaggle_api_authentication
- kaggle_api_submission
- network_upload
- external_api_call
- secret_or_token_read
- private_core_export
- legal_certification_claim

## Next actions

- create_public_safety_and_boundary_checklist_v1
- create_kaggle_submission_preflight_report_v1
- create_local_submission_smoke_test_v1
- create_submission_candidate_format_report_v1
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

ARC_AGI3_MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_V1_READY=true
ARC_AGI3_MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_VALID=true
ARC_AGI3_MILESTONE_5_ENTRYPOINT_MODE=CONTRACT_ONLY_LOCAL_DRY_RUN
ARC_AGI3_MILESTONE_5_EXPECTED_OUTPUT_FILE=submission.json
ARC_AGI3_MILESTONE_5_READY_FOR_LOCAL_SUBMISSION_SMOKE_TEST=true
ARC_AGI3_MILESTONE_5_KAGGLE_API_SUBMISSION_BLOCKED=true
ARC_AGI3_MILESTONE_5_NETWORK_UPLOAD_BLOCKED=true
ARC_AGI3_MILESTONE_5_EXTERNAL_API_CALL_BLOCKED=true
ARC_AGI3_MILESTONE_5_BASELINE_DRY_RUN_PACKAGE_COMMIT=8dfb106
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
ARC_AGI3_LEGAL_CERTIFICATION=false
