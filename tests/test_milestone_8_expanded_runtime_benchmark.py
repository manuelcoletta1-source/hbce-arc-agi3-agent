from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_expanded_runtime_benchmark import (
    BENCHMARK_GATES,
    BENCHMARK_ISSUES,
    BENCHMARK_MODE,
    BENCHMARK_SCOPE,
    BENCHMARK_STATUS,
    BENCHMARK_VERDICT,
    EXPECTED_BOUNDARY_CONTROL_COUNT,
    EXPECTED_EXPANDED_CASE_COUNT,
    EXPECTED_EXPANDED_FAILURE_COUNT,
    EXPECTED_EXPANDED_PASS_COUNT,
    EXPECTED_FAMILY_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_8_expanded_runtime_benchmark,
    evaluate_all_expanded_runtime_cases,
    evaluate_expanded_runtime_case,
    render_expanded_runtime_benchmark_manifest,
    render_expanded_runtime_benchmark_markdown,
    run_milestone_8_expanded_runtime_benchmark_pipeline,
    validate_milestone_8_expanded_runtime_benchmark,
    write_expanded_runtime_benchmark_artifacts,
)


def test_each_expanded_runtime_case_passes():
    case_ids = [
        "expanded_runtime_color_hint_top_family_v2",
        "expanded_runtime_color_training_pair_top_operation_v2",
        "expanded_runtime_color_background_guard_v2",
        "expanded_runtime_object_hint_top_family_v2",
        "expanded_runtime_object_right_candidate_exists_v2",
        "expanded_runtime_object_down_candidate_exists_v2",
        "expanded_runtime_shape_hint_top_family_v2",
        "expanded_runtime_shape_reflection_candidates_exist_v2",
        "expanded_runtime_cross_family_score_order_v2",
        "expanded_runtime_cross_family_deduplication_v2",
        "expanded_runtime_deterministic_repeatability_v2",
        "expanded_runtime_boundary_guard_v2",
    ]
    for case_id in case_ids:
        result = evaluate_expanded_runtime_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_expanded_runtime_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_expanded_runtime_case("missing_expanded_case")


def test_all_expanded_runtime_cases_pass_and_cover_families():
    results = evaluate_all_expanded_runtime_cases()
    assert len(results) == EXPECTED_EXPANDED_CASE_COUNT
    assert all(result["passed"] is True for result in results)
    assert {result["family"] for result in results} == {
        "color_mapping",
        "object_model",
        "shape_symmetry",
        "cross_family_composition",
    }


def test_expanded_benchmark_record_ready():
    benchmark = build_milestone_8_expanded_runtime_benchmark()
    assert benchmark["status"] == BENCHMARK_STATUS
    assert benchmark["benchmark_mode"] == BENCHMARK_MODE
    assert benchmark["benchmark_scope"] == BENCHMARK_SCOPE
    assert benchmark["benchmark_verdict"] == BENCHMARK_VERDICT
    assert benchmark["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert benchmark["family_count"] == EXPECTED_FAMILY_COUNT
    assert benchmark["expanded_case_count"] == EXPECTED_EXPANDED_CASE_COUNT
    assert benchmark["expanded_pass_count"] == EXPECTED_EXPANDED_PASS_COUNT
    assert benchmark["expanded_failure_count"] == EXPECTED_EXPANDED_FAILURE_COUNT
    assert benchmark["sample_ranked_candidate_count"] == EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT
    assert benchmark["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert benchmark["boundary_control_count"] == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert benchmark["passed_gate_count"] == len(BENCHMARK_GATES)
    assert benchmark["benchmark_issue_count"] == 0
    assert benchmark["benchmark_ready"] is True


def test_ranker_source_is_present_and_hashed():
    source = build_milestone_8_expanded_runtime_benchmark()["ranker_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY"
    assert source["ranker_id"].startswith("MILESTONE-8-RANKER-RUNTIME-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_expanded_benchmark_keeps_submission_blocked():
    benchmark = build_milestone_8_expanded_runtime_benchmark()
    assert benchmark["real_submission_created"] is False
    assert benchmark["real_submission_allowed"] is False
    assert benchmark["ready_for_real_kaggle_submission"] is False
    assert benchmark["kaggle_submission_sent"] is False
    assert benchmark["upload_performed"] is False
    assert benchmark["kaggle_authentication_performed"] is False
    assert benchmark["score_claim_absent"] is True
    assert benchmark["public_leaderboard_claim_absent"] is True


def test_expanded_benchmark_gates_and_issues_are_clean():
    benchmark = build_milestone_8_expanded_runtime_benchmark()
    assert [item["name"] for item in benchmark["benchmark_gates"]] == list(BENCHMARK_GATES)
    assert [item["name"] for item in benchmark["benchmark_issues"]] == list(BENCHMARK_ISSUES)
    assert all(item["passed"] is True for item in benchmark["benchmark_gates"])
    assert all(item["active"] is False for item in benchmark["benchmark_issues"])


def test_expanded_benchmark_validation_and_pipeline_pass():
    benchmark = build_milestone_8_expanded_runtime_benchmark()
    validation = validate_milestone_8_expanded_runtime_benchmark(benchmark)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_8_expanded_runtime_benchmark_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["benchmark_status"] == BENCHMARK_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["benchmark_ready"] is True
    assert payload["expanded_pass_count"] == 12
    assert payload["expanded_failure_count"] == 0


def test_expanded_benchmark_markdown_and_manifest_contain_markers():
    benchmark = build_milestone_8_expanded_runtime_benchmark()
    markdown = render_expanded_runtime_benchmark_markdown(benchmark)
    manifest = render_expanded_runtime_benchmark_manifest(benchmark)
    assert "ARC_AGI3_MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_EXPANDED_PASS_COUNT=12" in markdown
    assert "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_7_SUBMISSION_CANDIDATE_REFRESH_V2" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "EXPANDED_RESULTS" in manifest
    assert "SAMPLE_RANKED_CANDIDATES" in manifest
    assert "expanded_runtime_color_training_pair_top_operation_v2" in manifest
    assert "expanded_runtime_boundary_guard_v2" in manifest


def test_expanded_benchmark_writes_artifacts(tmp_path: Path):
    benchmark = build_milestone_8_expanded_runtime_benchmark()
    paths = write_expanded_runtime_benchmark_artifacts(benchmark, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "EXPANDED_RUNTIME_BENCHMARK_V2_READY_FOR_SUBMISSION_CANDIDATE_REFRESH" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_expanded_benchmark_metadata_safe():
    metadata = build_milestone_8_expanded_runtime_benchmark()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_expanded_results_have_required_fields():
    benchmark = build_milestone_8_expanded_runtime_benchmark()
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
    assert all(set(result) == required for result in benchmark["expanded_results"])


def test_sample_ranked_candidates_are_ranked_and_deduplicated():
    benchmark = build_milestone_8_expanded_runtime_benchmark()
    ranked = benchmark["sample_ranked_candidates"]
    signatures = [candidate["signature"] for candidate in ranked]
    scores = [candidate["ranker_score"] for candidate in ranked]
    assert [candidate["ranker_rank"] for candidate in ranked] == list(range(1, len(ranked) + 1))
    assert scores == sorted(scores, reverse=True)
    assert len(signatures) == len(set(signatures))


def test_expanded_index_is_conservative():
    index = build_milestone_8_expanded_runtime_benchmark()["benchmark_index"]
    assert index["benchmark_ready"] is True
    assert index["benchmark_locked"] is True
    assert index["expanded_pass_count"] == 12
    assert index["expanded_failure_count"] == 0
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
