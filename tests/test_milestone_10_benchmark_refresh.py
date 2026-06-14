from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_benchmark_refresh import (
    EXPECTED_BENCHMARK_CASE_COUNT,
    EXPECTED_BENCHMARK_CHECK_COUNT,
    EXPECTED_BENCHMARK_FAILURE_COUNT,
    EXPECTED_BENCHMARK_FAMILY_COUNT,
    EXPECTED_BENCHMARK_PASS_COUNT,
    EXPECTED_BENCHMARK_TASK_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    REFRESH_MODE,
    REFRESH_SCOPE,
    REFRESH_STATUS,
    REFRESH_VERDICT,
    VALIDATION_STATUS,
    build_benchmark_refresh_checks,
    build_benchmark_refresh_metrics,
    build_benchmark_refresh_source_summary,
    build_benchmark_refresh_state,
    build_local_benchmark_task_catalog,
    build_milestone_10_benchmark_refresh,
    evaluate_all_benchmark_refresh_cases,
    evaluate_all_local_benchmark_tasks,
    evaluate_benchmark_refresh_case,
    evaluate_local_benchmark_task,
    render_benchmark_refresh_manifest,
    render_benchmark_refresh_markdown,
    run_milestone_10_benchmark_refresh_pipeline,
    validate_milestone_10_benchmark_refresh,
    write_benchmark_refresh_artifacts,
)


def test_refresh_source_summary_reads_patch_implementation():
    summary = build_benchmark_refresh_source_summary()
    assert summary["implementation_present"] is True
    assert summary["implementation_status"] == "MILESTONE_10_SOLVER_PATCH_IMPLEMENTATION_V1_READY"
    assert summary["implementation_id"].startswith("MILESTONE-10-SOLVER-PATCH-IMPLEMENTATION-")
    assert summary["implementation_ready"] is True
    assert summary["implementation_locked"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_5_BENCHMARK_REFRESH_V1"
    assert summary["implementation_function_count"] == 6
    assert summary["patch_target_count"] == 6
    assert summary["runtime_helper_functions_created"] is True
    assert summary["submission_candidate_created"] is False
    assert summary["benchmark_required_next"] is True
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")


def test_local_benchmark_task_catalog_is_safe_and_complete():
    catalog = build_local_benchmark_task_catalog()
    assert len(catalog) == EXPECTED_BENCHMARK_TASK_COUNT
    assert len({task["family"] for task in catalog}) == EXPECTED_BENCHMARK_FAMILY_COUNT
    assert all(task["local_only"] is True for task in catalog)
    assert all(task["deterministic"] is True for task in catalog)
    assert all(task["uses_patch_helper"] is True for task in catalog)
    assert all(task["requires_external_api"] is False for task in catalog)
    assert all(task["requires_kaggle_upload"] is False for task in catalog)
    assert all(task["creates_submission_candidate"] is False for task in catalog)


def test_each_local_benchmark_task_passes():
    for task in build_local_benchmark_task_catalog():
        result = evaluate_local_benchmark_task(task["task_id"])
        assert result["passed"] is True
        assert result["score"] >= task["expected_min_score"]


def test_unknown_local_benchmark_task_fails_closed():
    with pytest.raises(ValueError):
        evaluate_local_benchmark_task("missing_benchmark_task")


def test_all_local_benchmark_tasks_and_metrics_pass():
    results = evaluate_all_local_benchmark_tasks()
    metrics = build_benchmark_refresh_metrics()
    assert len(results) == EXPECTED_BENCHMARK_TASK_COUNT
    assert all(result["passed"] is True for result in results)
    assert metrics["benchmark_task_count"] == EXPECTED_BENCHMARK_TASK_COUNT
    assert metrics["benchmark_family_count"] == EXPECTED_BENCHMARK_FAMILY_COUNT
    assert metrics["benchmark_task_pass_count"] == EXPECTED_BENCHMARK_TASK_COUNT
    assert metrics["benchmark_task_failure_count"] == 0
    assert metrics["average_score"] >= 95
    assert metrics["minimum_score"] >= 90


def test_refresh_state_keeps_candidate_refresh_as_next_only():
    state = build_benchmark_refresh_state()
    assert state["benchmark_refresh_required"] is True
    assert state["benchmark_refresh_created"] is True
    assert state["benchmark_refresh_ready"] is True
    assert state["benchmark_refresh_locked"] is True
    assert state["refresh_mode"] == REFRESH_MODE
    assert state["refresh_scope"] == REFRESH_SCOPE
    assert state["refresh_verdict"] == REFRESH_VERDICT
    assert state["candidate_refresh_required_next"] is True
    assert state["submission_candidate_created"] is False
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_active"] is True


def test_benchmark_refresh_checks_all_pass():
    checks = build_benchmark_refresh_checks()
    assert all(checks.values())


def test_each_benchmark_refresh_case_passes():
    case_ids = [
        "m10_benchmark_refresh_implementation_source_ready_v1",
        "m10_benchmark_refresh_task_catalog_ready_v1",
        "m10_benchmark_refresh_color_remap_pass_v1",
        "m10_benchmark_refresh_object_boundary_pass_v1",
        "m10_benchmark_refresh_symmetry_pass_v1",
        "m10_benchmark_refresh_composition_pass_v1",
        "m10_benchmark_refresh_ranker_pass_v1",
        "m10_benchmark_refresh_trace_pass_v1",
        "m10_benchmark_refresh_fail_closed_preserved_v1",
        "m10_benchmark_refresh_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_benchmark_refresh_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_benchmark_refresh_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_benchmark_refresh_case("missing_benchmark_refresh_case")


def test_all_benchmark_refresh_cases_pass():
    results = evaluate_all_benchmark_refresh_cases()
    assert len(results) == EXPECTED_BENCHMARK_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_benchmark_refresh_record_ready():
    refresh = build_milestone_10_benchmark_refresh()
    assert refresh["status"] == REFRESH_STATUS
    assert refresh["refresh_mode"] == REFRESH_MODE
    assert refresh["refresh_scope"] == REFRESH_SCOPE
    assert refresh["refresh_verdict"] == REFRESH_VERDICT
    assert refresh["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert refresh["refresh_ready"] is True
    assert refresh["refresh_locked"] is True
    assert refresh["benchmark_refresh_created"] is True
    assert refresh["benchmark_refresh_ready"] is True
    assert refresh["benchmark_refresh_locked"] is True
    assert refresh["benchmark_task_count"] == EXPECTED_BENCHMARK_TASK_COUNT
    assert refresh["benchmark_family_count"] == EXPECTED_BENCHMARK_FAMILY_COUNT
    assert refresh["benchmark_check_count"] == EXPECTED_BENCHMARK_CHECK_COUNT
    assert refresh["benchmark_case_count"] == EXPECTED_BENCHMARK_CASE_COUNT
    assert refresh["benchmark_pass_count"] == EXPECTED_BENCHMARK_PASS_COUNT
    assert refresh["benchmark_failure_count"] == EXPECTED_BENCHMARK_FAILURE_COUNT
    assert refresh["passed_gate_count"] == refresh["benchmark_gate_count"]
    assert refresh["benchmark_issue_count"] == 0


def test_patch_implementation_source_is_hashed():
    source = build_milestone_10_benchmark_refresh()["implementation_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_SOLVER_PATCH_IMPLEMENTATION_V1_READY"
    assert source["implementation_id"].startswith("MILESTONE-10-SOLVER-PATCH-IMPLEMENTATION-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_benchmark_refresh_keeps_submission_candidate_blocked():
    refresh = build_milestone_10_benchmark_refresh()
    assert refresh["candidate_refresh_required_next"] is True
    assert refresh["submission_candidate_created"] is False
    assert refresh["real_submission_decision"] == "NOT_AUTHORIZED"
    assert refresh["real_submission_allowed"] is False
    assert refresh["manual_upload_allowed"] is False
    assert refresh["kaggle_authentication_allowed"] is False
    assert refresh["kaggle_submission_sent"] is False
    assert refresh["fail_closed_required"] is True
    assert refresh["fail_closed_active"] is True


def test_benchmark_refresh_validation_and_pipeline_pass():
    refresh = build_milestone_10_benchmark_refresh()
    validation = validate_milestone_10_benchmark_refresh(refresh)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_benchmark_refresh_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["refresh_status"] == REFRESH_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["refresh_ready"] is True
    assert payload["benchmark_pass_count"] == 10
    assert payload["benchmark_failure_count"] == 0


def test_benchmark_refresh_markdown_and_manifest_contain_markers():
    refresh = build_milestone_10_benchmark_refresh()
    markdown = render_benchmark_refresh_markdown(refresh)
    manifest = render_benchmark_refresh_manifest(refresh)
    assert "ARC_AGI3_MILESTONE_10_BENCHMARK_REFRESH_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_BENCHMARK_REFRESH_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_BENCHMARK_TASK_COUNT=6" in markdown
    assert "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_REQUIRED_NEXT=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "BENCHMARK_TASK_RESULTS" in manifest
    assert "BENCHMARK_VALIDATION_RESULTS" in manifest
    assert "m10_benchmark_refresh_task_catalog_ready_v1" in manifest


def test_benchmark_refresh_writes_artifacts(tmp_path: Path):
    refresh = build_milestone_10_benchmark_refresh()
    paths = write_benchmark_refresh_artifacts(refresh, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_10_BENCHMARK_REFRESH_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_BENCHMARK_REFRESH_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "BENCHMARK_REFRESH_READY_FOR_CONTROLLED_CANDIDATE_REFRESH" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_benchmark_refresh_metadata_safe():
    metadata = build_milestone_10_benchmark_refresh()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_benchmark_refresh_index_is_conservative():
    index = build_milestone_10_benchmark_refresh()["benchmark_index"]
    assert index["refresh_ready"] is True
    assert index["benchmark_refresh_created"] is True
    assert index["benchmark_refresh_ready"] is True
    assert index["benchmark_task_count"] == EXPECTED_BENCHMARK_TASK_COUNT
    assert index["benchmark_family_count"] == EXPECTED_BENCHMARK_FAMILY_COUNT
    assert index["benchmark_task_pass_count"] == EXPECTED_BENCHMARK_TASK_COUNT
    assert index["benchmark_task_failure_count"] == 0
    assert index["average_score"] >= 95
    assert index["candidate_refresh_required_next"] is True
    assert index["submission_candidate_created"] is False
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_6_CANDIDATE_REFRESH_V1"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
