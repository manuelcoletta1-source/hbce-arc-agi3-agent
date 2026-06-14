from pathlib import Path

from hbce_arc_agi3.milestone_6_real_submission_decision_layer import (
    BASELINE_COMMIT,
    DECISION_GATES,
    DECISION_ISSUES,
    DECISION_MODE,
    DECISION_SCOPE,
    DECISION_STATUS,
    DECISION_VERDICT,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_6_real_submission_decision_layer,
    render_real_submission_decision_layer_markdown,
    render_real_submission_decision_manifest,
    run_milestone_6_real_submission_decision_layer_pipeline,
    validate_milestone_6_real_submission_decision_layer,
    write_real_submission_decision_layer_artifacts,
)


def test_real_submission_decision_layer_ready():
    decision = build_milestone_6_real_submission_decision_layer()

    assert decision["status"] == DECISION_STATUS
    assert decision["baseline_commit"] == BASELINE_COMMIT
    assert decision["decision_mode"] == DECISION_MODE
    assert decision["decision_scope"] == DECISION_SCOPE
    assert decision["decision_verdict"] == DECISION_VERDICT
    assert decision["artifact_count"] == 3
    assert decision["ready_artifact_count"] == 3
    assert decision["decision_gate_count"] == len(DECISION_GATES)
    assert decision["passed_gate_count"] == len(DECISION_GATES)
    assert decision["decision_issue_count"] == 0
    assert decision["warning_count"] == 0
    assert decision["decision_layer_ready"] is True


def test_real_submission_decision_layer_blocks_submission():
    decision = build_milestone_6_real_submission_decision_layer()

    assert decision["operator_approval_required"] is True
    assert decision["operator_approval_received"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["ready_for_real_kaggle_submission"] is False
    assert decision["real_submission_created"] is False
    assert decision["kaggle_submission_sent"] is False
    assert decision["upload_performed"] is False


def test_decision_artifacts_are_ready():
    decision = build_milestone_6_real_submission_decision_layer()

    assert all(item["present"] is True for item in decision["artifact_statuses"])
    assert all(item["ready"] is True for item in decision["artifact_statuses"])
    assert all(item["sha256_16"] != "MISSING_HASH" for item in decision["artifact_statuses"])


def test_decision_gates_pass():
    decision = build_milestone_6_real_submission_decision_layer()

    assert [gate["name"] for gate in decision["decision_gates"]] == list(DECISION_GATES)
    assert all(gate["passed"] is True for gate in decision["decision_gates"])
    assert all(gate["severity"] == "PASS" for gate in decision["decision_gates"])


def test_decision_issues_inactive():
    decision = build_milestone_6_real_submission_decision_layer()

    assert [issue["name"] for issue in decision["decision_issues"]] == list(DECISION_ISSUES)
    assert all(issue["active"] is False for issue in decision["decision_issues"])
    assert all(issue["severity"] == "BLOCKING" for issue in decision["decision_issues"])


def test_decision_record_is_conservative():
    decision = build_milestone_6_real_submission_decision_layer()
    record = decision["decision_record"]

    assert record["operator_approval_required"] is True
    assert record["operator_approval_received"] is False
    assert record["operator_identity_verified_for_submission"] is False
    assert record["real_submission_allowed"] is False
    assert record["real_submission_created"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["upload_performed"] is False
    assert record["external_api_dependency"] is False
    assert record["secrets_required"] is False
    assert record["legal_certification"] is False
    assert record["private_core_exposure"] is False


def test_decision_boundary_is_intact():
    decision = build_milestone_6_real_submission_decision_layer()
    boundary = decision["boundary"]

    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_decision_index_is_safe():
    decision = build_milestone_6_real_submission_decision_layer()
    index = decision["decision_index"]

    assert index["decision_mode"] == DECISION_MODE
    assert index["decision_scope"] == DECISION_SCOPE
    assert index["decision_verdict"] == DECISION_VERDICT
    assert index["operator_approval_required"] is True
    assert index["operator_approval_received"] is False
    assert index["real_submission_allowed"] is False
    assert index["real_submission_created"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["external_api_dependency"] is False
    assert index["private_core_exposure"] is False
    assert index["legal_certification"] is False


def test_decision_validation_passes():
    decision = build_milestone_6_real_submission_decision_layer()
    validation = validate_milestone_6_real_submission_decision_layer(decision)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_decision_pipeline_ready():
    payload = run_milestone_6_real_submission_decision_layer_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["decision_status"] == DECISION_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["decision_mode"] == DECISION_MODE
    assert payload["decision_verdict"] == DECISION_VERDICT
    assert payload["artifact_count"] == 3
    assert payload["ready_artifact_count"] == 3
    assert payload["decision_gate_count"] == len(DECISION_GATES)
    assert payload["passed_gate_count"] == len(DECISION_GATES)
    assert payload["decision_issue_count"] == 0
    assert payload["decision_layer_ready"] is True
    assert payload["real_submission_allowed"] is False
    assert payload["kaggle_submission_sent"] is False


def test_decision_markdown_contains_markers():
    decision = build_milestone_6_real_submission_decision_layer()
    markdown = render_real_submission_decision_layer_markdown(decision)

    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_DECISION_MODE=DECISION_LAYER_ONLY_NO_SUBMISSION" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_RECEIVED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_decision_manifest_contains_boundary():
    decision = build_milestone_6_real_submission_decision_layer()
    manifest = render_real_submission_decision_manifest(decision)

    assert "ARC AGI3 MILESTONE 6 REAL SUBMISSION DECISION LAYER MANIFEST v1" in manifest
    assert "decision_mode=DECISION_LAYER_ONLY_NO_SUBMISSION" in manifest
    assert "decision_verdict=REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL" in manifest
    assert "operator_approval_required=True" in manifest
    assert "operator_approval_received=False" in manifest
    assert "real_submission_allowed=False" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_decision_writes_artifacts(tmp_path: Path):
    decision = build_milestone_6_real_submission_decision_layer()
    paths = write_real_submission_decision_layer_artifacts(decision, output_dir=str(tmp_path))

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])
    index_path = Path(paths["index_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()
    assert "MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 MILESTONE 6 REAL SUBMISSION DECISION LAYER MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
    assert "REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL" in index_path.read_text(encoding="utf-8")
