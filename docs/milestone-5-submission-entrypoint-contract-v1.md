# ARC AGI3 Milestone #5 - Submission Entrypoint Contract v1

## Status

Milestone #5 Task 4 defines the submission entrypoint contract for the ARC-AGI-3 project.

This is not a real Kaggle submission. It does not authenticate with Kaggle, does not upload files, does not call external APIs, and does not create any legal certification claim.

## Baseline

- baseline dry-run package commit: 8dfb106 Add ARC AGI3 Kaggle submission dry-run package
- entrypoint name: arc_agi3_submission_entrypoint
- entrypoint mode: CONTRACT_ONLY_LOCAL_DRY_RUN
- entrypoint runtime: PYTHON_LOCAL_ONLY
- expected output file: submission.json
- expected smoke mode: LOCAL_CONTRACT_SMOKE_ONLY
- Kaggle submission sent: false

## Required inputs

1. repo_root
2. source_package
3. test_suite
4. dry_run_package
5. public_repo_index

## Expected outputs

1. submission_candidate_path: submission.json
2. entrypoint_report_json: submission-entrypoint-contract-v1.json
3. entrypoint_report_markdown: submission-entrypoint-contract-v1.md
4. entrypoint_contract_manifest: submission-entrypoint-contract-manifest-v1.txt

## Blocked actions

- kaggle_api_authentication
- kaggle_api_submission
- network_upload
- external_api_call
- secret_or_token_read
- private_core_export
- legal_certification_claim

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
