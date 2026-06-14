from pathlib import Path

from hbce_arc_agi3.milestone_6_real_submission_precheck_gate import (
    BASELINE_COMMIT,
    PIPELINE_STATUS,
    PRECHECK_GATES,
    PRECHECK_ISSUES,
    PRECHECK_MODE,
    PRECHECK_SCOPE,
    PRECHECK_STATUS,
    PRECHECK_VERDICT,
    VALIDATION_STATUS,
    build_milestone_6_real_submission_precheck_gate,
    render_real_submission_precheck_gate_manifest,
    render_real_submission_precheck_gate_markdown,
    run_milestone_6_real_submission_precheck_gate_pipeline,
    validate_milestone_6_real_submission_precheck_gate,
    write_real_submission_precheck_gate_artifacts,
)


def test_real_submission_precheck_gate_ready():
    precheck = build_milestone_6_real_submission_precheck_gate()
    assert precheck["status"] == PRECHECK_STATUS
    assert precheck["baseline_commit"] == BASELINE_COMMIT
    assert precheck["precheck_mode"] == PRECHECK_MODE
    assert precheck["precheck_scope"] == PRECHECK_SCOPE
    assert precheck["precheck_verdict"] == PRECHECK_VERDICT
    assert precheck["artifact_count"] == 3
    assert precheck["ready_artifact_count"] == 3
    assert precheck["precheck_gate_count"] == len(PRECHECK_GATES)
    assert precheck["passed_gate_count"] == len(PRECHECK_GATES)
    assert precheck["precheck_issue_count"] == 0
    assert precheck["precheck_gate_ready"] is True
    assert precheck["precheck_passed"] is True


def test_real_submission_precheck_gate_blocks_submission():
    precheck = build_milestone_6_real_submission_precheck_gate()
    assert precheck["operator_approval_granted"] is True
    assert precheck["manual_execution_gate_required"] is True
    assert precheck["real_submission_allowed"] is False
    assert precheck["ready_for_real_kaggle_submission"] is False
    assert precheck["real_submission_created"] is False
    assert precheck["kaggle_submission_sent"] is False
    assert precheck["upload_performed"] is False
    assert precheck["kaggle_authentication_performed"] is False


def test_precheck_artifacts_are_ready():
    precheck = build_milestone_6_real_submission_precheck_gate()
    assert all(item["present"] is True for item in precheck["artifact_statuses"])
    assert all(item["ready"] is True for item in precheck["artifact_statuses"])
    assert all(item["sha256_16"] != "MISSING_HASH" for item in precheck["artifact_statuses"])


def test_precheck_record_is_conservative():
    record = build_milestone_6_real_submission_precheck_gate()["precheck_record"]
    assert record["precheck_gate_ready"] is True
    assert record["precheck_passed"] is True
    assert record["operator_approval_granted"] is True
    assert record["manual_execution_gate_required"] is True
    assert record["real_submission_allowed"] is False
    assert record["ready_for_real_kaggle_submission"] is False
    assert record["real_submission_created"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["upload_performed"] is False
    assert record["kaggle_authentication_performed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_precheck_gates_pass():
    precheck = build_milestone_6_real_submission_precheck_gate()
    assert [gate["name"] for gate in precheck["precheck_gates"]] == list(PRECHECK_GATES)
    assert all(gate["passed"] is True for gate in precheck["precheck_gates"])
    assert all(gate["severity"] == "PASS" for gate in precheck["precheck_gates"])


def test_precheck_issues_inactive():
    precheck = build_milestone_6_real_submission_precheck_gate()
    assert [issue["name"] for issue in precheck["precheck_issues"]] == list(PRECHECK_ISSUES)
    assert all(issue["active"] is False for issue in precheck["precheck_issues"])


def test_precheck_boundary_is_intact():
    boundary = build_milestone_6_real_submission_precheck_gate()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_precheck_validation_passes():
    precheck = build_milestone_6_real_submission_precheck_gate()
    validation = validate_milestone_6_real_submission_precheck_gate(precheck)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_precheck_pipeline_ready():
    payload = run_milestone_6_real_submission_precheck_gate_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["precheck_status"] == PRECHECK_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["precheck_mode"] == PRECHECK_MODE
    assert payload["precheck_verdict"] == PRECHECK_VERDICT
    assert payload["artifact_count"] == 3
    assert payload["ready_artifact_count"] == 3
    assert payload["precheck_gate_count"] == len(PRECHECK_GATES)
    assert payload["passed_gate_count"] == len(PRECHECK_GATES)
    assert payload["precheck_issue_count"] == 0
    assert payload["precheck_gate_ready"] is True
    assert payload["precheck_passed"] is True
    assert payload["real_submission_allowed"] is False
    assert payload["kaggle_submission_sent"] is False


def test_precheck_markdown_contains_markers():
    markdown = render_real_submission_precheck_gate_markdown(build_milestone_6_real_submission_precheck_gate())
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_PRECHECK_MODE=REAL_SUBMISSION_PRECHECK_GATE_ONLY_NO_SUBMISSION" in markdown
    assert "ARC_AGI3_MILESTONE_6_PRECHECK_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_GRANTED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_MANUAL_EXECUTION_GATE_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_KAGGLE_AUTHENTICATION_PERFORMED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_precheck_manifest_contains_boundary():
    manifest = render_real_submission_precheck_gate_manifest(build_milestone_6_real_submission_precheck_gate())
    assert "ARC AGI3 MILESTONE 6 REAL SUBMISSION PRECHECK GATE MANIFEST v1" in manifest
    assert "precheck_mode=REAL_SUBMISSION_PRECHECK_GATE_ONLY_NO_SUBMISSION" in manifest
    assert "precheck_verdict=PRECHECK_PASS_REAL_SUBMISSION_STILL_BLOCKED_BY_MANUAL_EXECUTION_GATE" in manifest
    assert "precheck_gate_ready=True" in manifest
    assert "precheck_passed=True" in manifest
    assert "operator_approval_granted=True" in manifest
    assert "manual_execution_gate_required=True" in manifest
    assert "real_submission_allowed=False" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest
    assert "kaggle_authentication_performed=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_precheck_writes_artifacts(tmp_path: Path):
    precheck = build_milestone_6_real_submission_precheck_gate()
    paths = write_real_submission_precheck_gate_artifacts(precheck, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "PRECHECK_PASS_REAL_SUBMISSION_STILL_BLOCKED_BY_MANUAL_EXECUTION_GATE" in Path(paths["index_path"]).read_text(encoding="utf-8")
