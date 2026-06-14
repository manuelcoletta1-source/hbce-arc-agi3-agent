from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_submission_candidate_rebuild_gate import (
    EXPECTED_REBUILD_GATE_CASE_COUNT,
    EXPECTED_REBUILD_GATE_CHECK_COUNT,
    EXPECTED_REBUILD_GATE_FAILURE_COUNT,
    EXPECTED_REBUILD_GATE_PASS_COUNT,
    EXPECTED_SELECTED_CANDIDATE_ID,
    GATE_MODE,
    GATE_SCOPE,
    GATE_STATUS,
    GATE_VERDICT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_10_submission_candidate_rebuild_gate,
    build_rebuild_gate_checks,
    build_rebuild_gate_decision,
    build_rebuild_gate_source_summary,
    build_rebuild_gate_state,
    evaluate_all_rebuild_gate_cases,
    evaluate_rebuild_gate_case,
    render_rebuild_gate_manifest,
    render_rebuild_gate_markdown,
    run_milestone_10_submission_candidate_rebuild_gate_pipeline,
    validate_milestone_10_submission_candidate_rebuild_gate,
    write_rebuild_gate_artifacts,
)


def test_rebuild_gate_source_summary_reads_candidate_refresh():
    summary = build_rebuild_gate_source_summary()
    assert summary["candidate_refresh_present"] is True
    assert summary["candidate_status"] == "MILESTONE_10_CANDIDATE_REFRESH_V1_READY"
    assert summary["candidate_refresh_id"].startswith("MILESTONE-10-CANDIDATE-REFRESH-")
    assert summary["candidate_ready"] is True
    assert summary["candidate_locked"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_7_SUBMISSION_CANDIDATE_REBUILD_GATE_V1"
    assert summary["candidate_count"] == 4
    assert summary["ranked_candidate_count"] == 4
    assert summary["selected_candidate_count"] == 1
    assert summary["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert summary["candidate_package_id"].startswith("MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-")
    assert summary["candidate_artifact_created"] is True
    assert summary["real_submission_candidate_created"] is False
    assert summary["submission_json_created"] is False
    assert summary["upload_package_created"] is False
    assert summary["rebuild_gate_required_next"] is True
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True


def test_rebuild_gate_decision_allows_only_local_rebuild():
    decision = build_rebuild_gate_decision()
    assert decision["decision"] == "ALLOW_LOCAL_SUBMISSION_CANDIDATE_REBUILD_ONLY"
    assert decision["local_candidate_rebuild_allowed"] is True
    assert decision["real_submission_allowed"] is False
    assert decision["manual_upload_allowed"] is False
    assert decision["kaggle_authentication_allowed"] is False
    assert decision["kaggle_submission_allowed"] is False
    assert decision["submission_json_creation_allowed_now"] is False
    assert decision["upload_package_creation_allowed_now"] is False
    assert decision["operator_approval_required_for_real_submission"] is True
    assert decision["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert decision["next_allowed_stage"] == NEXT_ALLOWED_STAGE


def test_rebuild_gate_state_is_conservative():
    state = build_rebuild_gate_state()
    assert state["rebuild_gate_required"] is True
    assert state["rebuild_gate_created"] is True
    assert state["rebuild_gate_ready"] is True
    assert state["rebuild_gate_locked"] is True
    assert state["rebuild_gate_passed"] is True
    assert state["gate_mode"] == GATE_MODE
    assert state["gate_scope"] == GATE_SCOPE
    assert state["gate_verdict"] == GATE_VERDICT
    assert state["local_candidate_rebuild_allowed"] is True
    assert state["submission_candidate_rebuild_required_next"] is True
    assert state["real_submission_candidate_created"] is False
    assert state["submission_json_created"] is False
    assert state["upload_package_created"] is False
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_active"] is True


def test_rebuild_gate_checks_all_pass():
    checks = build_rebuild_gate_checks()
    assert all(checks.values())


def test_each_rebuild_gate_case_passes():
    case_ids = [
        "m10_rebuild_gate_candidate_source_ready_v1",
        "m10_rebuild_gate_selected_candidate_valid_v1",
        "m10_rebuild_gate_candidate_package_ready_v1",
        "m10_rebuild_gate_local_rebuild_allowed_v1",
        "m10_rebuild_gate_real_submission_candidate_blocked_v1",
        "m10_rebuild_gate_submission_json_blocked_v1",
        "m10_rebuild_gate_upload_package_blocked_v1",
        "m10_rebuild_gate_fail_closed_preserved_v1",
        "m10_rebuild_gate_boundary_controls_preserved_v1",
        "m10_rebuild_gate_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_rebuild_gate_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_rebuild_gate_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_rebuild_gate_case("missing_rebuild_gate_case")


def test_all_rebuild_gate_cases_pass():
    results = evaluate_all_rebuild_gate_cases()
    assert len(results) == EXPECTED_REBUILD_GATE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_rebuild_gate_record_ready():
    gate = build_milestone_10_submission_candidate_rebuild_gate()
    assert gate["status"] == GATE_STATUS
    assert gate["gate_mode"] == GATE_MODE
    assert gate["gate_scope"] == GATE_SCOPE
    assert gate["gate_verdict"] == GATE_VERDICT
    assert gate["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert gate["rebuild_gate_ready"] is True
    assert gate["rebuild_gate_locked"] is True
    assert gate["rebuild_gate_created"] is True
    assert gate["rebuild_gate_passed"] is True
    assert gate["local_candidate_rebuild_allowed"] is True
    assert gate["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert gate["rebuild_gate_check_count"] == EXPECTED_REBUILD_GATE_CHECK_COUNT
    assert gate["rebuild_gate_case_count"] == EXPECTED_REBUILD_GATE_CASE_COUNT
    assert gate["rebuild_gate_pass_count"] == EXPECTED_REBUILD_GATE_PASS_COUNT
    assert gate["rebuild_gate_failure_count"] == EXPECTED_REBUILD_GATE_FAILURE_COUNT
    assert gate["passed_gate_count"] == gate["rebuild_gate_gate_count"]
    assert gate["rebuild_gate_issue_count"] == 0


def test_candidate_refresh_source_is_hashed():
    source = build_milestone_10_submission_candidate_rebuild_gate()["candidate_refresh_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_CANDIDATE_REFRESH_V1_READY"
    assert source["candidate_refresh_id"].startswith("MILESTONE-10-CANDIDATE-REFRESH-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_rebuild_gate_keeps_submission_blocked():
    gate = build_milestone_10_submission_candidate_rebuild_gate()
    assert gate["local_candidate_rebuild_allowed"] is True
    assert gate["submission_candidate_rebuild_required_next"] is True
    assert gate["real_submission_candidate_created"] is False
    assert gate["submission_json_created"] is False
    assert gate["upload_package_created"] is False
    assert gate["real_submission_decision"] == "NOT_AUTHORIZED"
    assert gate["real_submission_allowed"] is False
    assert gate["manual_upload_allowed"] is False
    assert gate["kaggle_authentication_allowed"] is False
    assert gate["kaggle_submission_sent"] is False
    assert gate["fail_closed_required"] is True
    assert gate["fail_closed_active"] is True


def test_rebuild_gate_validation_and_pipeline_pass():
    gate = build_milestone_10_submission_candidate_rebuild_gate()
    validation = validate_milestone_10_submission_candidate_rebuild_gate(gate)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_submission_candidate_rebuild_gate_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["gate_status"] == GATE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["rebuild_gate_ready"] is True
    assert payload["rebuild_gate_pass_count"] == 10
    assert payload["rebuild_gate_failure_count"] == 0


def test_rebuild_gate_markdown_and_manifest_contain_markers():
    gate = build_milestone_10_submission_candidate_rebuild_gate()
    markdown = render_rebuild_gate_markdown(gate)
    manifest = render_rebuild_gate_manifest(gate)
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REBUILD_GATE_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REBUILD_GATE_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_LOCAL_CANDIDATE_REBUILD_ALLOWED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "REBUILD_GATE_DECISION" in manifest
    assert "REBUILD_GATE_VALIDATION_RESULTS" in manifest
    assert "m10_rebuild_gate_local_rebuild_allowed_v1" in manifest


def test_rebuild_gate_writes_artifacts(tmp_path: Path):
    gate = build_milestone_10_submission_candidate_rebuild_gate()
    paths = write_rebuild_gate_artifacts(gate, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_REBUILD_GATE_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "REBUILD_GATE_PASS_LOCAL_CANDIDATE_REBUILD_ALLOWED_REAL_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_rebuild_gate_metadata_safe():
    metadata = build_milestone_10_submission_candidate_rebuild_gate()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_rebuild_gate_index_is_conservative():
    index = build_milestone_10_submission_candidate_rebuild_gate()["rebuild_gate_index"]
    assert index["rebuild_gate_ready"] is True
    assert index["rebuild_gate_created"] is True
    assert index["rebuild_gate_passed"] is True
    assert index["local_candidate_rebuild_allowed"] is True
    assert index["submission_candidate_rebuild_required_next"] is True
    assert index["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert index["real_submission_candidate_created"] is False
    assert index["submission_json_created"] is False
    assert index["upload_package_created"] is False
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_8_SUBMISSION_CANDIDATE_REBUILD_V1"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
