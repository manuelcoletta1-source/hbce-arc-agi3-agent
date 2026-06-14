from pathlib import Path

from hbce_arc_agi3.milestone_6_operator_approval_declaration import (
    BASELINE_COMMIT,
    DECLARATION_GATES,
    DECLARATION_ISSUES,
    DECLARATION_MODE,
    DECLARATION_SCOPE,
    DECLARATION_STATUS,
    DECLARATION_VERDICT,
    PIPELINE_STATUS,
    REQUIRED_OPERATOR_DECLARATIONS,
    VALIDATION_STATUS,
    build_milestone_6_operator_approval_declaration,
    render_operator_approval_declaration_manifest,
    render_operator_approval_declaration_markdown,
    run_milestone_6_operator_approval_declaration_pipeline,
    validate_milestone_6_operator_approval_declaration,
    write_operator_approval_declaration_artifacts,
)


def test_operator_approval_declaration_ready():
    declaration = build_milestone_6_operator_approval_declaration()

    assert declaration["status"] == DECLARATION_STATUS
    assert declaration["baseline_commit"] == BASELINE_COMMIT
    assert declaration["declaration_mode"] == DECLARATION_MODE
    assert declaration["declaration_scope"] == DECLARATION_SCOPE
    assert declaration["declaration_verdict"] == DECLARATION_VERDICT
    assert declaration["required_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert declaration["declared_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert declaration["provided_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert declaration["accepted_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert declaration["declaration_gate_count"] == len(DECLARATION_GATES)
    assert declaration["passed_gate_count"] == len(DECLARATION_GATES)
    assert declaration["declaration_issue_count"] == 0
    assert declaration["warning_count"] == 0
    assert declaration["operator_approval_declaration_ready"] is True


def test_operator_approval_declaration_grants_approval_but_not_submission():
    declaration = build_milestone_6_operator_approval_declaration()

    assert declaration["operator_approval_required"] is True
    assert declaration["operator_approval_declared"] is True
    assert declaration["operator_approval_received"] is True
    assert declaration["operator_approval_granted"] is True
    assert declaration["real_submission_allowed"] is False
    assert declaration["ready_for_real_kaggle_submission"] is False
    assert declaration["real_submission_created"] is False
    assert declaration["kaggle_submission_sent"] is False
    assert declaration["upload_performed"] is False
    assert declaration["precheck_gate_required"] is True


def test_operator_declarations_are_declared_and_accepted():
    declaration = build_milestone_6_operator_approval_declaration()
    declarations = declaration["declaration_record"]["declared_operator_declarations"]

    assert [item["name"] for item in declarations] == list(REQUIRED_OPERATOR_DECLARATIONS)
    assert all(item["required"] is True for item in declarations)
    assert all(item["declared"] is True for item in declarations)
    assert all(item["provided"] is True for item in declarations)
    assert all(item["accepted"] is True for item in declarations)
    assert all(item["status"] == "DECLARED_AND_ACCEPTED_FOR_DECISION_CHAIN" for item in declarations)


def test_operator_approval_declaration_gates_pass():
    declaration = build_milestone_6_operator_approval_declaration()

    assert [gate["name"] for gate in declaration["declaration_gates"]] == list(DECLARATION_GATES)
    assert all(gate["passed"] is True for gate in declaration["declaration_gates"])
    assert all(gate["severity"] == "PASS" for gate in declaration["declaration_gates"])


def test_operator_approval_declaration_issues_inactive():
    declaration = build_milestone_6_operator_approval_declaration()

    assert [issue["name"] for issue in declaration["declaration_issues"]] == list(DECLARATION_ISSUES)
    assert all(issue["active"] is False for issue in declaration["declaration_issues"])
    assert all(issue["severity"] == "BLOCKING" for issue in declaration["declaration_issues"])


def test_operator_approval_declaration_record_is_conservative():
    declaration = build_milestone_6_operator_approval_declaration()
    record = declaration["declaration_record"]

    assert record["operator_approval_declaration_ready"] is True
    assert record["operator_approval_required"] is True
    assert record["operator_approval_declared"] is True
    assert record["operator_approval_received"] is True
    assert record["operator_approval_granted"] is True
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
    assert record["precheck_gate_required"] is True


def test_operator_approval_declaration_boundary_is_intact():
    declaration = build_milestone_6_operator_approval_declaration()
    boundary = declaration["boundary"]

    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_operator_approval_declaration_index_is_safe():
    declaration = build_milestone_6_operator_approval_declaration()
    index = declaration["declaration_index"]

    assert index["declaration_mode"] == DECLARATION_MODE
    assert index["declaration_scope"] == DECLARATION_SCOPE
    assert index["declaration_verdict"] == DECLARATION_VERDICT
    assert index["required_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert index["declared_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert index["accepted_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert index["operator_approval_declared"] is True
    assert index["operator_approval_received"] is True
    assert index["operator_approval_granted"] is True
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["real_submission_created"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["precheck_gate_required"] is True
    assert index["external_api_dependency"] is False
    assert index["private_core_exposure"] is False
    assert index["legal_certification"] is False


def test_operator_approval_declaration_validation_passes():
    declaration = build_milestone_6_operator_approval_declaration()
    validation = validate_milestone_6_operator_approval_declaration(declaration)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_operator_approval_declaration_pipeline_ready():
    payload = run_milestone_6_operator_approval_declaration_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["declaration_status"] == DECLARATION_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["declaration_mode"] == DECLARATION_MODE
    assert payload["declaration_verdict"] == DECLARATION_VERDICT
    assert payload["required_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert payload["declared_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert payload["provided_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert payload["accepted_declaration_count"] == len(REQUIRED_OPERATOR_DECLARATIONS)
    assert payload["declaration_gate_count"] == len(DECLARATION_GATES)
    assert payload["passed_gate_count"] == len(DECLARATION_GATES)
    assert payload["declaration_issue_count"] == 0
    assert payload["operator_approval_declaration_ready"] is True
    assert payload["operator_approval_granted"] is True
    assert payload["real_submission_allowed"] is False
    assert payload["kaggle_submission_sent"] is False


def test_operator_approval_declaration_markdown_contains_markers():
    declaration = build_milestone_6_operator_approval_declaration()
    markdown = render_operator_approval_declaration_markdown(declaration)

    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_DECLARATION_MODE=OPERATOR_APPROVAL_DECLARATION_ONLY_NO_SUBMISSION" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_DECLARED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_RECEIVED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_GRANTED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_REQUIRED_DECLARATION_COUNT=8" in markdown
    assert "ARC_AGI3_MILESTONE_6_DECLARED_DECLARATION_COUNT=8" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_PRECHECK_GATE_REQUIRED=true" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_operator_approval_declaration_manifest_contains_boundary():
    declaration = build_milestone_6_operator_approval_declaration()
    manifest = render_operator_approval_declaration_manifest(declaration)

    assert "ARC AGI3 MILESTONE 6 OPERATOR APPROVAL DECLARATION MANIFEST v1" in manifest
    assert "declaration_mode=OPERATOR_APPROVAL_DECLARATION_ONLY_NO_SUBMISSION" in manifest
    assert "declaration_verdict=OPERATOR_APPROVAL_DECLARED_REAL_SUBMISSION_STILL_BLOCKED" in manifest
    assert "required_declaration_count=8" in manifest
    assert "declared_declaration_count=8" in manifest
    assert "accepted_declaration_count=8" in manifest
    assert "operator_approval_declared=True" in manifest
    assert "operator_approval_received=True" in manifest
    assert "operator_approval_granted=True" in manifest
    assert "real_submission_allowed=False" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest
    assert "precheck_gate_required=True" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_operator_approval_declaration_writes_artifacts(tmp_path: Path):
    declaration = build_milestone_6_operator_approval_declaration()
    paths = write_operator_approval_declaration_artifacts(declaration, output_dir=str(tmp_path))

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])
    index_path = Path(paths["index_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()
    assert "MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 MILESTONE 6 OPERATOR APPROVAL DECLARATION MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
    assert "OPERATOR_APPROVAL_DECLARED_REAL_SUBMISSION_STILL_BLOCKED" in index_path.read_text(encoding="utf-8")
