from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_final_competitive_readiness_refresh import (
    EXPECTED_AUDIT_CASE_COUNT,
    EXPECTED_AUDIT_FAILURE_COUNT,
    EXPECTED_AUDIT_PASS_COUNT,
    EXPECTED_BOUNDARY_CONTROL_COUNT,
    EXPECTED_CLOSED_TASK_COUNT,
    EXPECTED_READINESS_CHECK_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SOURCE_COMMIT_COUNT,
    EXPECTED_SUBMISSION_CANDIDATE_COUNT,
    FINAL_MODE,
    FINAL_SCOPE,
    FINAL_STATUS,
    FINAL_VERDICT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_8_final_competitive_readiness_refresh,
    build_readiness_checks,
    evaluate_all_final_refresh_cases,
    evaluate_final_refresh_case,
    render_final_competitive_readiness_refresh_manifest,
    render_final_competitive_readiness_refresh_markdown,
    run_milestone_8_final_competitive_readiness_refresh_pipeline,
    validate_milestone_8_final_competitive_readiness_refresh,
    write_final_competitive_readiness_refresh_artifacts,
)


def test_readiness_checks_all_pass():
    checks = build_readiness_checks()
    assert len(checks) == EXPECTED_READINESS_CHECK_COUNT
    assert all(checks.values())


def test_each_final_refresh_case_passes():
    case_ids = [
        "final_refresh_source_artifact_ready_v2",
        "final_refresh_local_candidate_payload_ready_v2",
        "final_refresh_task_chain_complete_v2",
        "final_refresh_candidate_count_valid_v2",
        "final_refresh_candidate_hash_available_v2",
        "final_refresh_artifact_index_ready_v2",
        "final_refresh_readiness_checks_pass_v2",
        "final_refresh_boundary_controls_pass_v2",
        "final_refresh_submission_still_blocked_v2",
        "final_refresh_next_stage_valid_v2",
    ]
    for case_id in case_ids:
        result = evaluate_final_refresh_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_final_refresh_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_final_refresh_case("missing_final_refresh_case")


def test_all_final_refresh_cases_pass():
    results = evaluate_all_final_refresh_cases()
    assert len(results) == EXPECTED_AUDIT_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_final_record_ready():
    final = build_milestone_8_final_competitive_readiness_refresh()
    assert final["status"] == FINAL_STATUS
    assert final["final_mode"] == FINAL_MODE
    assert final["final_scope"] == FINAL_SCOPE
    assert final["final_verdict"] == FINAL_VERDICT
    assert final["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert final["closed_task_count"] == EXPECTED_CLOSED_TASK_COUNT
    assert final["source_commit_count"] == EXPECTED_SOURCE_COMMIT_COUNT
    assert final["readiness_check_count"] == EXPECTED_READINESS_CHECK_COUNT
    assert final["audit_case_count"] == EXPECTED_AUDIT_CASE_COUNT
    assert final["audit_pass_count"] == EXPECTED_AUDIT_PASS_COUNT
    assert final["audit_failure_count"] == EXPECTED_AUDIT_FAILURE_COUNT
    assert final["submission_candidate_count"] == EXPECTED_SUBMISSION_CANDIDATE_COUNT
    assert final["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert final["boundary_control_count"] == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert final["passed_gate_count"] == final["final_gate_count"]
    assert final["final_issue_count"] == 0
    assert final["final_ready"] is True


def test_source_commits_chain_is_complete():
    final = build_milestone_8_final_competitive_readiness_refresh()
    commits = [item["commit"] for item in final["source_commits"]]
    assert commits == ["69af006", "4a93654", "1df6919", "3ea3687", "537b277", "c68ab45", "0e7e086"]


def test_refresh_and_candidate_sources_are_present_and_hashed():
    final = build_milestone_8_final_competitive_readiness_refresh()
    assert final["refresh_source"]["present"] is True
    assert final["refresh_source"]["status"] == "MILESTONE_8_SUBMISSION_CANDIDATE_REFRESH_V2_READY"
    assert final["refresh_source"]["sha256"] != "MISSING_HASH"
    assert final["local_candidate_source"]["present"] is True
    assert final["local_candidate_source"]["candidate_format"] == "ARC_AGI3_LOCAL_SUBMISSION_CANDIDATE_V2"
    assert final["local_candidate_source"]["sha256"] != "MISSING_HASH"


def test_final_keeps_submission_blocked():
    final = build_milestone_8_final_competitive_readiness_refresh()
    assert final["real_submission_created"] is False
    assert final["real_submission_allowed"] is False
    assert final["ready_for_real_kaggle_submission"] is False
    assert final["kaggle_submission_sent"] is False
    assert final["upload_performed"] is False
    assert final["kaggle_authentication_performed"] is False
    assert final["score_claim_absent"] is True
    assert final["public_leaderboard_claim_absent"] is True


def test_final_gates_and_issues_are_clean():
    final = build_milestone_8_final_competitive_readiness_refresh()
    assert all(item["passed"] is True for item in final["final_gates"])
    assert all(item["active"] is False for item in final["final_issues"])
    assert final["final_gate_count"] == final["passed_gate_count"]


def test_final_validation_and_pipeline_pass():
    final = build_milestone_8_final_competitive_readiness_refresh()
    validation = validate_milestone_8_final_competitive_readiness_refresh(final)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_8_final_competitive_readiness_refresh_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["final_status"] == FINAL_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["final_ready"] is True
    assert payload["audit_pass_count"] == 10
    assert payload["audit_failure_count"] == 0


def test_final_markdown_and_manifest_contain_markers():
    final = build_milestone_8_final_competitive_readiness_refresh()
    markdown = render_final_competitive_readiness_refresh_markdown(final)
    manifest = render_final_competitive_readiness_refresh_manifest(final)
    assert "ARC_AGI3_MILESTONE_8_FINAL_COMPETITIVE_READINESS_REFRESH_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_FINAL_COMPETITIVE_READINESS_REFRESH_V2_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_AUDIT_PASS_COUNT=10" in markdown
    assert "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "SOURCE_COMMITS" in manifest
    assert "AUDIT_RESULTS" in manifest
    assert "final_refresh_submission_still_blocked_v2" in manifest


def test_final_writes_artifacts(tmp_path: Path):
    final = build_milestone_8_final_competitive_readiness_refresh()
    paths = write_final_competitive_readiness_refresh_artifacts(final, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_8_FINAL_COMPETITIVE_READINESS_REFRESH_V2_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_8_FINAL_COMPETITIVE_READINESS_REFRESH_V2_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "FINAL_COMPETITIVE_READINESS_REFRESH_V2_COMPLETE_REAL_SUBMISSION_STILL_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_final_metadata_safe():
    metadata = build_milestone_8_final_competitive_readiness_refresh()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_final_index_is_conservative():
    index = build_milestone_8_final_competitive_readiness_refresh()["final_index"]
    assert index["final_ready"] is True
    assert index["final_locked"] is True
    assert index["audit_pass_count"] == 10
    assert index["audit_failure_count"] == 0
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
