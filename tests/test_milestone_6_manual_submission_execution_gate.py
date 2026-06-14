from pathlib import Path

from hbce_arc_agi3.milestone_6_manual_submission_execution_gate import (
    BASELINE_COMMIT,
    GATE_MODE,
    GATE_SCOPE,
    GATE_STATUS,
    GATE_VERDICT,
    GATES,
    ISSUES,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_6_manual_submission_execution_gate,
    render_manual_submission_execution_gate_manifest,
    render_manual_submission_execution_gate_markdown,
    run_milestone_6_manual_submission_execution_gate_pipeline,
    validate_milestone_6_manual_submission_execution_gate,
    write_manual_submission_execution_gate_artifacts,
)


def test_manual_submission_execution_gate_ready():
    gate = build_milestone_6_manual_submission_execution_gate()
    assert gate["status"] == GATE_STATUS
    assert gate["baseline_commit"] == BASELINE_COMMIT
    assert gate["gate_mode"] == GATE_MODE
    assert gate["gate_scope"] == GATE_SCOPE
    assert gate["gate_verdict"] == GATE_VERDICT
    assert gate["gate_count"] == len(GATES)
    assert gate["passed_gate_count"] == len(GATES)
    assert gate["issue_count"] == 0
    assert gate["manual_execution_gate_ready"] is True


def test_manual_submission_execution_gate_does_not_execute():
    gate = build_milestone_6_manual_submission_execution_gate()
    assert gate["manual_execution_gate_required"] is True
    assert gate["manual_execution_performed"] is False
    assert gate["real_submission_allowed"] is False
    assert gate["ready_for_real_kaggle_submission"] is False
    assert gate["real_submission_created"] is False
    assert gate["kaggle_submission_sent"] is False
    assert gate["upload_performed"] is False
    assert gate["kaggle_authentication_performed"] is False


def test_manual_submission_execution_record_is_conservative():
    record = build_milestone_6_manual_submission_execution_gate()["manual_execution_record"]
    assert record["manual_execution_gate_ready"] is True
    assert record["manual_execution_gate_required"] is True
    assert record["manual_execution_performed"] is False
    assert record["precheck_passed"] is True
    assert record["operator_approval_granted"] is True
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["secrets_required"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_manual_submission_execution_gates_pass():
    gate = build_milestone_6_manual_submission_execution_gate()
    assert [item["name"] for item in gate["manual_execution_gates"]] == list(GATES)
    assert all(item["passed"] is True for item in gate["manual_execution_gates"])
    assert all(item["severity"] == "PASS" for item in gate["manual_execution_gates"])


def test_manual_submission_execution_issues_inactive():
    gate = build_milestone_6_manual_submission_execution_gate()
    assert [item["name"] for item in gate["manual_execution_issues"]] == list(ISSUES)
    assert all(item["active"] is False for item in gate["manual_execution_issues"])


def test_manual_submission_execution_boundary_intact():
    boundary = build_milestone_6_manual_submission_execution_gate()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_manual_submission_execution_validation_passes():
    gate = build_milestone_6_manual_submission_execution_gate()
    validation = validate_milestone_6_manual_submission_execution_gate(gate)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_manual_submission_execution_pipeline_ready():
    payload = run_milestone_6_manual_submission_execution_gate_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["gate_status"] == GATE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["gate_mode"] == GATE_MODE
    assert payload["gate_verdict"] == GATE_VERDICT
    assert payload["gate_count"] == len(GATES)
    assert payload["passed_gate_count"] == len(GATES)
    assert payload["issue_count"] == 0
    assert payload["manual_execution_gate_ready"] is True
    assert payload["manual_execution_performed"] is False
    assert payload["kaggle_submission_sent"] is False


def test_manual_submission_execution_markdown_contains_markers():
    markdown = render_manual_submission_execution_gate_markdown(build_milestone_6_manual_submission_execution_gate())
    assert "ARC_AGI3_MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_GATE_MODE=MANUAL_SUBMISSION_EXECUTION_GATE_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_6_MANUAL_EXECUTION_PERFORMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_manual_submission_execution_manifest_contains_boundary():
    manifest = render_manual_submission_execution_gate_manifest(build_milestone_6_manual_submission_execution_gate())
    assert "ARC AGI3 MILESTONE 6 MANUAL SUBMISSION EXECUTION GATE MANIFEST v1" in manifest
    assert "gate_mode=MANUAL_SUBMISSION_EXECUTION_GATE_ONLY_NO_UPLOAD" in manifest
    assert "manual_execution_gate_ready=True" in manifest
    assert "manual_execution_performed=False" in manifest
    assert "real_submission_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest
    assert "kaggle_authentication_performed=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_manual_submission_execution_writes_artifacts(tmp_path: Path):
    gate = build_milestone_6_manual_submission_execution_gate()
    paths = write_manual_submission_execution_gate_artifacts(gate, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "MANUAL_EXECUTION_GATE_READY_REAL_SUBMISSION_NOT_PERFORMED" in Path(paths["index_path"]).read_text(encoding="utf-8")
