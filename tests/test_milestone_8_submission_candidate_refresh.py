from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_submission_candidate_refresh import (
    EXPECTED_BOUNDARY_CONTROL_COUNT,
    EXPECTED_REFRESH_CASE_COUNT,
    EXPECTED_REFRESH_FAILURE_COUNT,
    EXPECTED_REFRESH_PASS_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SUBMISSION_CANDIDATE_COUNT,
    EXPECTED_TASK_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    REFRESH_GATES,
    REFRESH_ISSUES,
    REFRESH_MODE,
    REFRESH_SCOPE,
    REFRESH_STATUS,
    REFRESH_VERDICT,
    VALIDATION_STATUS,
    build_local_submission_candidate_payload,
    build_milestone_8_submission_candidate_refresh,
    build_submission_candidate_for_task,
    evaluate_all_refresh_cases,
    evaluate_refresh_case,
    render_submission_candidate_refresh_manifest,
    render_submission_candidate_refresh_markdown,
    run_milestone_8_submission_candidate_refresh_pipeline,
    validate_milestone_8_submission_candidate_refresh,
    write_submission_candidate_refresh_artifacts,
)


def test_local_submission_candidate_payload_ready():
    payload = build_local_submission_candidate_payload()
    assert payload["candidate_format"] == "ARC_AGI3_LOCAL_SUBMISSION_CANDIDATE_V2"
    assert payload["task_count"] == EXPECTED_TASK_COUNT
    assert payload["submission_candidate_count"] == EXPECTED_SUBMISSION_CANDIDATE_COUNT
    assert payload["solution_count"] == EXPECTED_SUBMISSION_CANDIDATE_COUNT
    assert payload["candidate_outputs_ranked"] is True
    assert payload["candidate_outputs_deduplicated"] is True
    assert payload["local_only"] is True
    assert payload["dry_run_only"] is True
    assert payload["kaggle_submission_sent"] is False


def test_local_submission_candidate_covers_profile_families():
    payload = build_local_submission_candidate_payload()
    assert set(payload["profile_families"]) == {
        "color_mapping",
        "object_model",
        "shape_symmetry",
        "cross_family_composition",
    }


def test_submission_candidate_entries_have_selected_outputs():
    payload = build_local_submission_candidate_payload()
    for candidate in payload["candidates"]:
        assert candidate["candidate_ready"] is True
        assert candidate["solution_count"] == 1
        assert candidate["ranker_rank"] == 1
        assert isinstance(candidate["ranker_score"], float)
        assert candidate["selected_grid"]
        assert candidate["signature"]


def test_submission_candidate_payload_is_deterministic():
    assert build_local_submission_candidate_payload() == build_local_submission_candidate_payload()


def test_each_refresh_case_passes():
    case_ids = [
        "refresh_expanded_benchmark_source_ready_v2",
        "refresh_candidate_count_valid_v2",
        "refresh_profile_family_coverage_valid_v2",
        "refresh_selected_candidate_grids_valid_v2",
        "refresh_ranker_score_order_available_v2",
        "refresh_deterministic_repeatability_v2",
        "refresh_manifest_index_ready_v2",
        "refresh_submission_boundary_guard_v2",
    ]
    for case_id in case_ids:
        result = evaluate_refresh_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_refresh_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_refresh_case("missing_refresh_case")


def test_all_refresh_cases_pass():
    results = evaluate_all_refresh_cases()
    assert len(results) == EXPECTED_REFRESH_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_refresh_record_ready():
    refresh = build_milestone_8_submission_candidate_refresh()
    assert refresh["status"] == REFRESH_STATUS
    assert refresh["refresh_mode"] == REFRESH_MODE
    assert refresh["refresh_scope"] == REFRESH_SCOPE
    assert refresh["refresh_verdict"] == REFRESH_VERDICT
    assert refresh["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert refresh["task_count"] == EXPECTED_TASK_COUNT
    assert refresh["submission_candidate_count"] == EXPECTED_SUBMISSION_CANDIDATE_COUNT
    assert refresh["refresh_case_count"] == EXPECTED_REFRESH_CASE_COUNT
    assert refresh["refresh_pass_count"] == EXPECTED_REFRESH_PASS_COUNT
    assert refresh["refresh_failure_count"] == EXPECTED_REFRESH_FAILURE_COUNT
    assert refresh["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert refresh["boundary_control_count"] == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert refresh["passed_gate_count"] == len(REFRESH_GATES)
    assert refresh["refresh_issue_count"] == 0
    assert refresh["refresh_ready"] is True


def test_expanded_benchmark_source_is_present_and_hashed():
    source = build_milestone_8_submission_candidate_refresh()["expanded_benchmark_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_READY"
    assert source["benchmark_id"].startswith("MILESTONE-8-EXPANDED-RUNTIME-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_refresh_keeps_submission_blocked():
    refresh = build_milestone_8_submission_candidate_refresh()
    assert refresh["real_submission_created"] is False
    assert refresh["real_submission_allowed"] is False
    assert refresh["ready_for_real_kaggle_submission"] is False
    assert refresh["kaggle_submission_sent"] is False
    assert refresh["upload_performed"] is False
    assert refresh["kaggle_authentication_performed"] is False
    assert refresh["score_claim_absent"] is True
    assert refresh["public_leaderboard_claim_absent"] is True


def test_refresh_gates_and_issues_are_clean():
    refresh = build_milestone_8_submission_candidate_refresh()
    assert [item["name"] for item in refresh["refresh_gates"]] == list(REFRESH_GATES)
    assert [item["name"] for item in refresh["refresh_issues"]] == list(REFRESH_ISSUES)
    assert all(item["passed"] is True for item in refresh["refresh_gates"])
    assert all(item["active"] is False for item in refresh["refresh_issues"])


def test_refresh_validation_and_pipeline_pass():
    refresh = build_milestone_8_submission_candidate_refresh()
    validation = validate_milestone_8_submission_candidate_refresh(refresh)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_8_submission_candidate_refresh_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["refresh_status"] == REFRESH_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["refresh_ready"] is True
    assert payload["submission_candidate_count"] == 4
    assert payload["refresh_pass_count"] == 8
    assert payload["refresh_failure_count"] == 0


def test_refresh_markdown_and_manifest_contain_markers():
    refresh = build_milestone_8_submission_candidate_refresh()
    markdown = render_submission_candidate_refresh_markdown(refresh)
    manifest = render_submission_candidate_refresh_manifest(refresh)
    assert "ARC_AGI3_MILESTONE_8_SUBMISSION_CANDIDATE_REFRESH_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_SUBMISSION_CANDIDATE_REFRESH_V2_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_SUBMISSION_CANDIDATE_COUNT=4" in markdown
    assert "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_8_FINAL_COMPETITIVE_READINESS_REFRESH_V2" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "REFRESH_RESULTS" in manifest
    assert "LOCAL_SUBMISSION_CANDIDATES" in manifest
    assert "submission_refresh_color_mapping_probe_v2" in manifest
    assert "refresh_submission_boundary_guard_v2" in manifest


def test_refresh_writes_artifacts(tmp_path: Path):
    refresh = build_milestone_8_submission_candidate_refresh()
    paths = write_submission_candidate_refresh_artifacts(refresh, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["candidate_path"]).exists()
    assert "MILESTONE_8_SUBMISSION_CANDIDATE_REFRESH_V2_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_8_SUBMISSION_CANDIDATE_REFRESH_V2_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "SUBMISSION_CANDIDATE_REFRESH_V2_READY_FOR_FINAL_COMPETITIVE_READINESS_REFRESH" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_LOCAL_SUBMISSION_CANDIDATE_V2" in Path(paths["candidate_path"]).read_text(
        encoding="utf-8"
    )


def test_refresh_metadata_safe():
    metadata = build_milestone_8_submission_candidate_refresh()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_refresh_results_have_required_fields():
    refresh = build_milestone_8_submission_candidate_refresh()
    required = {
        "case_id",
        "family",
        "operation",
        "priority",
        "passed",
        "evidence_score",
        "expected_status",
        "actual_status",
    }
    assert all(set(result) == required for result in refresh["refresh_results"])


def test_refresh_index_is_conservative():
    index = build_milestone_8_submission_candidate_refresh()["refresh_index"]
    assert index["refresh_ready"] is True
    assert index["refresh_locked"] is True
    assert index["submission_candidate_count"] == 4
    assert index["refresh_pass_count"] == 8
    assert index["refresh_failure_count"] == 0
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
