from pathlib import Path

from hbce_arc_agi3.milestone_6_operator_approval_contract import (
    BASELINE_COMMIT,
    CONTRACT_GATES,
    CONTRACT_ISSUES,
    CONTRACT_MODE,
    CONTRACT_SCOPE,
    CONTRACT_STATUS,
    CONTRACT_VERDICT,
    PIPELINE_STATUS,
    REQUIRED_OPERATOR_DECLARATIONS,
    VALIDATION_STATUS,
    build_milestone_6_operator_approval_contract,
    render_operator_approval_contract_manifest,
    render_operator_approval_contract_markdown,
    run_milestone_6_operator_approval_contract_pipeline,
    validate_milestone_6_operator_approval_contract,
    write_operator_approval_contract_artifacts,
)


def test_operator_approval_contract_ready():
    contract = build_milestone_6_operator_approval_contract()

    assert contract["status"] == CONTRACT_STATUS
    assert contract["baseline_commit"] == BASELINE_COMMIT
    assert contract["contract_mode"] == CONTRACT_MODE
    assert contract["contract_scope"] == CONTRACT_SCOPE
    assert contract["contract_verdict"] == CONTRACT_VERDICT
    assert contract["required_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert contract["provided_declaration_count"] == 0
    assert contract["accepted_declaration_count"] == 0
    assert contract["contract_gate_count"] == len(CONTRACT_GATES)
    assert contract["passed_gate_count"] == len(CONTRACT_GATES)
    assert contract["contract_issue_count"] == 0
    assert contract["warning_count"] == 0
    assert contract["operator_approval_contract_ready"] is True


def test_operator_approval_contract_does_not_grant_approval():
    contract = build_milestone_6_operator_approval_contract()

    assert contract["operator_approval_required"] is True
    assert contract["operator_approval_granted"] is False
    assert contract["operator_approval_received"] is False
    assert contract["real_submission_allowed"] is False
    assert contract["ready_for_real_kaggle_submission"] is False
    assert contract["real_submission_created"] is False
    assert contract["kaggle_submission_sent"] is False
    assert contract["upload_performed"] is False


def test_operator_declarations_are_pending():
    contract = build_milestone_6_operator_approval_contract()
    declarations = contract["contract_record"]["required_declarations"]

    assert [item["name"] for item in declarations] == list(REQUIRED_OPERATOR_DECLARATIONS)
    assert all(item["required"] is True for item in declarations)
    assert all(item["provided"] is False for item in declarations)
    assert all(item["accepted"] is False for item in declarations)
    assert all(item["status"] == "PENDING_EXPLICIT_OPERATOR_APPROVAL" for item in declarations)


def test_operator_approval_contract_gates_pass():
    contract = build_milestone_6_operator_approval_contract()

    assert [gate["name"] for gate in contract["contract_gates"]] == list(CONTRACT_GATES)
    assert all(gate["passed"] is True for gate in contract["contract_gates"])
    assert all(gate["severity"] == "PASS" for gate in contract["contract_gates"])


def test_operator_approval_contract_issues_inactive():
    contract = build_milestone_6_operator_approval_contract()

    assert [issue["name"] for issue in contract["contract_issues"]] == list(CONTRACT_ISSUES)
    assert all(issue["active"] is False for issue in contract["contract_issues"])
    assert all(issue["severity"] == "BLOCKING" for issue in contract["contract_issues"])


def test_operator_approval_contract_record_is_conservative():
    contract = build_milestone_6_operator_approval_contract()
    record = contract["contract_record"]

    assert record["operator_approval_contract_ready"] is True
    assert record["operator_approval_required"] is True
    assert record["operator_approval_granted"] is False
    assert record["operator_approval_received"] is False
    assert record["operator_identity_verified_for_submission"] is False
    assert record["real_submission_allowed"] is False
    assert record["ready_for_real_kaggle_submission"] is False
    assert record["real_submission_created"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["upload_performed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["secrets_required"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_operator_approval_contract_boundary_is_intact():
    contract = build_milestone_6_operator_approval_contract()
    boundary = contract["boundary"]

    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_operator_approval_contract_index_is_safe():
    contract = build_milestone_6_operator_approval_contract()
    index = contract["contract_index"]

    assert index["contract_mode"] == CONTRACT_MODE
    assert index["contract_scope"] == CONTRACT_SCOPE
    assert index["contract_verdict"] == CONTRACT_VERDICT
    assert index["required_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert index["operator_approval_required"] is True
    assert index["operator_approval_granted"] is False
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["real_submission_created"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["external_api_dependency"] is False
    assert index["private_core_exposure"] is False
    assert index["legal_certification"] is False


def test_operator_approval_contract_validation_passes():
    contract = build_milestone_6_operator_approval_contract()
    validation = validate_milestone_6_operator_approval_contract(contract)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_operator_approval_contract_pipeline_ready():
    payload = run_milestone_6_operator_approval_contract_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["contract_status"] == CONTRACT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["contract_mode"] == CONTRACT_MODE
    assert payload["contract_verdict"] == CONTRACT_VERDICT
    assert payload["required_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert payload["provided_declaration_count"] == 0
    assert payload["accepted_declaration_count"] == 0
    assert payload["contract_gate_count"] == len(CONTRACT_GATES)
    assert payload["passed_gate_count"] == len(CONTRACT_GATES)
    assert payload["contract_issue_count"] == 0
    assert payload["operator_approval_contract_ready"] is True
    assert payload["operator_approval_granted"] is False
    assert payload["real_submission_allowed"] is False
    assert payload["kaggle_submission_sent"] is False


def test_operator_approval_contract_markdown_contains_markers():
    contract = build_milestone_6_operator_approval_contract()
    markdown = render_operator_approval_contract_markdown(contract)

    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_CONTRACT_MODE=OPERATOR_APPROVAL_CONTRACT_ONLY_NO_APPROVAL" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_GRANTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_RECEIVED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_REQUIRED_DECLARATION_COUNT=8" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_operator_approval_contract_manifest_contains_boundary():
    contract = build_milestone_6_operator_approval_contract()
    manifest = render_operator_approval_contract_manifest(contract)

    assert "ARC AGI3 MILESTONE 6 OPERATOR APPROVAL CONTRACT MANIFEST v1" in manifest
    assert "contract_mode=OPERATOR_APPROVAL_CONTRACT_ONLY_NO_APPROVAL" in manifest
    assert "contract_verdict=OPERATOR_APPROVAL_REQUIRED_BUT_NOT_GRANTED" in manifest
    assert "required_declaration_count=8" in manifest
    assert "provided_declaration_count=0" in manifest
    assert "accepted_declaration_count=0" in manifest
    assert "operator_approval_required=True" in manifest
    assert "operator_approval_granted=False" in manifest
    assert "operator_approval_received=False" in manifest
    assert "real_submission_allowed=False" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_operator_approval_contract_writes_artifacts(tmp_path: Path):
    contract = build_milestone_6_operator_approval_contract()
    paths = write_operator_approval_contract_artifacts(contract, output_dir=str(tmp_path))

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])
    index_path = Path(paths["index_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()
    assert "MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 MILESTONE 6 OPERATOR APPROVAL CONTRACT MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
    assert "OPERATOR_APPROVAL_REQUIRED_BUT_NOT_GRANTED" in index_path.read_text(encoding="utf-8")
