from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_candidate_refresh import (
    CANDIDATE_MODE,
    CANDIDATE_SCOPE,
    CANDIDATE_STATUS,
    CANDIDATE_VERDICT,
    EXPECTED_CANDIDATE_CASE_COUNT,
    EXPECTED_CANDIDATE_CHECK_COUNT,
    EXPECTED_CANDIDATE_COUNT,
    EXPECTED_CANDIDATE_FAILURE_COUNT,
    EXPECTED_CANDIDATE_PASS_COUNT,
    EXPECTED_RANKED_CANDIDATE_COUNT,
    EXPECTED_SELECTED_CANDIDATE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_candidate_refresh_catalog,
    build_candidate_refresh_checks,
    build_candidate_refresh_package,
    build_candidate_refresh_source_summary,
    build_candidate_refresh_state,
    build_milestone_10_candidate_refresh,
    evaluate_all_candidate_refresh_cases,
    evaluate_candidate_refresh_case,
    rank_candidate_refresh_catalog,
    render_candidate_refresh_manifest,
    render_candidate_refresh_markdown,
    run_milestone_10_candidate_refresh_pipeline,
    validate_milestone_10_candidate_refresh,
    write_candidate_refresh_artifacts,
)


def test_candidate_refresh_source_summary_reads_benchmark():
    summary = build_candidate_refresh_source_summary()
    assert summary["benchmark_present"] is True
    assert summary["benchmark_status"] == "MILESTONE_10_BENCHMARK_REFRESH_V1_READY"
    assert summary["refresh_id"].startswith("MILESTONE-10-BENCHMARK-REFRESH-")
    assert summary["refresh_ready"] is True
    assert summary["refresh_locked"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_6_CANDIDATE_REFRESH_V1"
    assert summary["benchmark_task_count"] == 6
    assert summary["benchmark_family_count"] == 6
    assert summary["average_score"] >= 95
    assert summary["candidate_refresh_required_next"] is True
    assert summary["submission_candidate_created"] is False
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True
    assert Path(summary["candidate_source_path"]).exists()


def test_candidate_catalog_is_safe_complete_and_rankable():
    catalog = build_candidate_refresh_catalog()
    assert len(catalog) == EXPECTED_CANDIDATE_COUNT
    assert len({item["family"] for item in catalog}) == EXPECTED_CANDIDATE_COUNT
    assert all(item["local_only"] is True for item in catalog)
    assert all(item["deterministic"] is True for item in catalog)
    assert all(item["requires_external_api"] is False for item in catalog)
    assert all(item["requires_kaggle_upload"] is False for item in catalog)
    assert all(item["creates_real_submission"] is False for item in catalog)
    assert all(item["creates_submission_json"] is False for item in catalog)
    assert all(item["trace_ready"] is True for item in catalog)
    assert all(item["stable_order"] is True for item in catalog)


def test_candidate_ranking_selects_balanced_patch_stack():
    ranking = rank_candidate_refresh_catalog()
    assert ranking["ranking_ready"] is True
    assert ranking["candidate_count"] == EXPECTED_CANDIDATE_COUNT
    assert ranking["ranked_candidate_count"] == EXPECTED_RANKED_CANDIDATE_COUNT
    assert ranking["selected_candidate_count"] == EXPECTED_SELECTED_CANDIDATE_COUNT
    assert ranking["selected_candidate_id"] == "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
    assert ranking["ranked_candidate_ids"][0] == "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"


def test_candidate_package_is_created_but_not_submission():
    package = build_candidate_refresh_package()
    assert package["package_id"].startswith("MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-")
    assert package["candidate_package_created"] is True
    assert package["candidate_package_ready"] is True
    assert package["candidate_artifact_created"] is True
    assert package["real_submission_candidate_created"] is False
    assert package["submission_json_created"] is False
    assert package["upload_package_created"] is False
    assert package["ready_for_rebuild_gate"] is True


def test_candidate_state_keeps_real_submission_blocked():
    state = build_candidate_refresh_state()
    assert state["candidate_refresh_required"] is True
    assert state["candidate_refresh_created"] is True
    assert state["candidate_refresh_ready"] is True
    assert state["candidate_refresh_locked"] is True
    assert state["candidate_mode"] == CANDIDATE_MODE
    assert state["candidate_scope"] == CANDIDATE_SCOPE
    assert state["candidate_verdict"] == CANDIDATE_VERDICT
    assert state["candidate_artifact_created"] is True
    assert state["real_submission_candidate_created"] is False
    assert state["submission_json_created"] is False
    assert state["upload_package_created"] is False
    assert state["rebuild_gate_required_next"] is True
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_active"] is True


def test_candidate_refresh_checks_all_pass():
    checks = build_candidate_refresh_checks()
    assert all(checks.values())


def test_each_candidate_refresh_case_passes():
    case_ids = [
        "m10_candidate_refresh_benchmark_source_ready_v1",
        "m10_candidate_refresh_catalog_ready_v1",
        "m10_candidate_refresh_ranking_ready_v1",
        "m10_candidate_refresh_selected_candidate_ready_v1",
        "m10_candidate_refresh_package_ready_v1",
        "m10_candidate_refresh_trace_ready_v1",
        "m10_candidate_refresh_no_submission_json_v1",
        "m10_candidate_refresh_real_submission_blocked_v1",
        "m10_candidate_refresh_fail_closed_preserved_v1",
        "m10_candidate_refresh_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_candidate_refresh_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_candidate_refresh_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_candidate_refresh_case("missing_candidate_refresh_case")


def test_all_candidate_refresh_cases_pass():
    results = evaluate_all_candidate_refresh_cases()
    assert len(results) == EXPECTED_CANDIDATE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_candidate_refresh_record_ready():
    candidate = build_milestone_10_candidate_refresh()
    assert candidate["status"] == CANDIDATE_STATUS
    assert candidate["candidate_mode"] == CANDIDATE_MODE
    assert candidate["candidate_scope"] == CANDIDATE_SCOPE
    assert candidate["candidate_verdict"] == CANDIDATE_VERDICT
    assert candidate["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert candidate["candidate_ready"] is True
    assert candidate["candidate_locked"] is True
    assert candidate["candidate_refresh_created"] is True
    assert candidate["candidate_refresh_ready"] is True
    assert candidate["candidate_refresh_locked"] is True
    assert candidate["candidate_count"] == EXPECTED_CANDIDATE_COUNT
    assert candidate["ranked_candidate_count"] == EXPECTED_RANKED_CANDIDATE_COUNT
    assert candidate["selected_candidate_count"] == EXPECTED_SELECTED_CANDIDATE_COUNT
    assert candidate["selected_candidate_id"] == "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
    assert candidate["candidate_check_count"] == EXPECTED_CANDIDATE_CHECK_COUNT
    assert candidate["candidate_case_count"] == EXPECTED_CANDIDATE_CASE_COUNT
    assert candidate["candidate_pass_count"] == EXPECTED_CANDIDATE_PASS_COUNT
    assert candidate["candidate_failure_count"] == EXPECTED_CANDIDATE_FAILURE_COUNT
    assert candidate["passed_gate_count"] == candidate["candidate_gate_count"]
    assert candidate["candidate_issue_count"] == 0


def test_benchmark_source_is_hashed():
    source = build_milestone_10_candidate_refresh()["benchmark_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_BENCHMARK_REFRESH_V1_READY"
    assert source["refresh_id"].startswith("MILESTONE-10-BENCHMARK-REFRESH-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_candidate_refresh_keeps_submission_blocked():
    candidate = build_milestone_10_candidate_refresh()
    assert candidate["candidate_artifact_created"] is True
    assert candidate["real_submission_candidate_created"] is False
    assert candidate["submission_json_created"] is False
    assert candidate["upload_package_created"] is False
    assert candidate["rebuild_gate_required_next"] is True
    assert candidate["real_submission_decision"] == "NOT_AUTHORIZED"
    assert candidate["real_submission_allowed"] is False
    assert candidate["manual_upload_allowed"] is False
    assert candidate["kaggle_authentication_allowed"] is False
    assert candidate["kaggle_submission_sent"] is False
    assert candidate["fail_closed_required"] is True
    assert candidate["fail_closed_active"] is True


def test_candidate_refresh_validation_and_pipeline_pass():
    candidate = build_milestone_10_candidate_refresh()
    validation = validate_milestone_10_candidate_refresh(candidate)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_candidate_refresh_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["candidate_status"] == CANDIDATE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["candidate_ready"] is True
    assert payload["candidate_pass_count"] == 10
    assert payload["candidate_failure_count"] == 0


def test_candidate_refresh_markdown_and_manifest_contain_markers():
    candidate = build_milestone_10_candidate_refresh()
    markdown = render_candidate_refresh_markdown(candidate)
    manifest = render_candidate_refresh_manifest(candidate)
    assert "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_CANDIDATE_COUNT=4" in markdown
    assert "ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_ID=M10-CANDIDATE-BALANCED-PATCH-STACK-v1" in markdown
    assert "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "CANDIDATE_RANKING" in manifest
    assert "CANDIDATE_VALIDATION_RESULTS" in manifest
    assert "m10_candidate_refresh_catalog_ready_v1" in manifest


def test_candidate_refresh_writes_artifacts(tmp_path: Path):
    candidate = build_milestone_10_candidate_refresh()
    paths = write_candidate_refresh_artifacts(candidate, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_10_CANDIDATE_REFRESH_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "CANDIDATE_REFRESH_READY_FOR_SUBMISSION_CANDIDATE_REBUILD_GATE" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_candidate_refresh_metadata_safe():
    metadata = build_milestone_10_candidate_refresh()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_candidate_refresh_index_is_conservative():
    index = build_milestone_10_candidate_refresh()["candidate_index"]
    assert index["candidate_ready"] is True
    assert index["candidate_refresh_created"] is True
    assert index["candidate_refresh_ready"] is True
    assert index["candidate_count"] == EXPECTED_CANDIDATE_COUNT
    assert index["ranked_candidate_count"] == EXPECTED_RANKED_CANDIDATE_COUNT
    assert index["selected_candidate_count"] == EXPECTED_SELECTED_CANDIDATE_COUNT
    assert index["selected_candidate_id"] == "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
    assert index["candidate_artifact_created"] is True
    assert index["real_submission_candidate_created"] is False
    assert index["submission_json_created"] is False
    assert index["upload_package_created"] is False
    assert index["rebuild_gate_required_next"] is True
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_7_SUBMISSION_CANDIDATE_REBUILD_GATE_V1"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True


def test_candidate_ranking_is_stable_across_runs():
    first = build_milestone_10_candidate_refresh()
    second = build_milestone_10_candidate_refresh()
    assert first["selected_candidate_id"] == second["selected_candidate_id"]
    assert first["candidate_ranking"]["ranked_candidate_ids"] == second["candidate_ranking"]["ranked_candidate_ids"]
    assert first["candidate_package"]["signature"] == second["candidate_package"]["signature"]
