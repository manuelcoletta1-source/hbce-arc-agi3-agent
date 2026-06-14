from pathlib import Path

from hbce_arc_agi3.milestone_5_submission_entrypoint_contract import (
    ALLOWED_ACTIONS,
    BLOCKED_ACTIONS,
    CONTRACT_STATUS,
    ENTRYPOINT_MODE,
    ENTRYPOINT_NAME,
    ENTRYPOINT_RUNTIME,
    EXPECTED_OUTPUT_FILE,
    EXPECTED_OUTPUTS,
    PIPELINE_STATUS,
    REQUIRED_INPUTS,
    VALIDATION_STATUS,
    build_entrypoint_inputs,
    build_entrypoint_outputs,
    build_submission_entrypoint_contract,
    render_submission_entrypoint_contract_manifest,
    render_submission_entrypoint_contract_markdown,
    run_submission_entrypoint_contract_pipeline,
    validate_submission_entrypoint_contract,
    write_submission_entrypoint_contract_artifacts,
)


def test_submission_entrypoint_contract_ready():
    contract = build_submission_entrypoint_contract()

    assert contract.status == CONTRACT_STATUS
    assert contract.baseline_commit.startswith("8dfb106")
    assert contract.entrypoint_name == ENTRYPOINT_NAME
    assert contract.entrypoint_mode == ENTRYPOINT_MODE
    assert contract.entrypoint_runtime == ENTRYPOINT_RUNTIME
    assert contract.expected_output_file == EXPECTED_OUTPUT_FILE
    assert len(contract.required_inputs) == len(REQUIRED_INPUTS)
    assert len(contract.expected_outputs) == len(EXPECTED_OUTPUTS)
    assert len(contract.blocked_actions) == len(BLOCKED_ACTIONS)
    assert len(contract.allowed_actions) == len(ALLOWED_ACTIONS)
    assert contract.ready_for_local_submission_smoke_test is True
    assert contract.kaggle_submission_sent is False


def test_submission_entrypoint_contract_blocks_submission_actions():
    contract = build_submission_entrypoint_contract()

    assert "kaggle_api_submission" in contract.blocked_actions
    assert "kaggle_api_authentication" in contract.blocked_actions
    assert "network_upload" in contract.blocked_actions
    assert "external_api_call" in contract.blocked_actions
    assert "secret_or_token_read" in contract.blocked_actions
    assert "private_core_export" in contract.blocked_actions
    assert "legal_certification_claim" in contract.blocked_actions


def test_submission_entrypoint_contract_validation_passes():
    contract = build_submission_entrypoint_contract()
    validation = validate_submission_entrypoint_contract(contract)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_submission_entrypoint_contract_pipeline_ready():
    payload = run_submission_entrypoint_contract_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["contract_status"] == CONTRACT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["entrypoint_mode"] == ENTRYPOINT_MODE
    assert payload["expected_output_file"] == EXPECTED_OUTPUT_FILE
    assert payload["ready_for_local_submission_smoke_test"] is True
    assert payload["kaggle_submission_sent"] is False


def test_submission_entrypoint_contract_markdown_contains_markers():
    contract = build_submission_entrypoint_contract()
    markdown = render_submission_entrypoint_contract_markdown(contract)

    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_ENTRYPOINT_MODE=CONTRACT_ONLY_LOCAL_DRY_RUN" in markdown
    assert "ARC_AGI3_MILESTONE_5_EXPECTED_OUTPUT_FILE=submission.json" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_LOCAL_SUBMISSION_SMOKE_TEST=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_KAGGLE_API_SUBMISSION_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_NETWORK_UPLOAD_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_EXTERNAL_API_CALL_BLOCKED=true" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_submission_entrypoint_contract_manifest_contains_boundary():
    contract = build_submission_entrypoint_contract()
    manifest = render_submission_entrypoint_contract_manifest(contract)

    assert "ARC AGI3 SUBMISSION ENTRYPOINT CONTRACT MANIFEST v1" in manifest
    assert "entrypoint_mode=CONTRACT_ONLY_LOCAL_DRY_RUN" in manifest
    assert "expected_output_file=submission.json" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "kaggle_api_submission" in manifest
    assert "network_upload" in manifest
    assert "external_api_call" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_submission_entrypoint_contract_writes_artifacts(tmp_path: Path):
    contract = build_submission_entrypoint_contract()
    paths = write_submission_entrypoint_contract_artifacts(
        contract,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 SUBMISSION ENTRYPOINT CONTRACT MANIFEST v1" in manifest_path.read_text(encoding="utf-8")


def test_submission_entrypoint_contract_inputs_outputs_are_stable():
    inputs = build_entrypoint_inputs()
    outputs = build_entrypoint_outputs()

    assert [item.name for item in inputs] == [
        "repo_root",
        "source_package",
        "test_suite",
        "dry_run_package",
        "public_repo_index",
    ]
    assert [item.path for item in outputs] == [
        "submission.json",
        "submission-entrypoint-contract-v1.json",
        "submission-entrypoint-contract-v1.md",
        "submission-entrypoint-contract-manifest-v1.txt",
    ]
