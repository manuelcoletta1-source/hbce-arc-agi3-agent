from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_family_benchmark_cases import (
    BENCHMARK_GATES,
    BENCHMARK_ISSUES,
    BENCHMARK_MODE,
    BENCHMARK_SCOPE,
    BENCHMARK_STATUS,
    BENCHMARK_VERDICT,
    EXPECTED_BENCHMARK_CASE_COUNT,
    EXPECTED_BENCHMARK_FAILURE_COUNT,
    EXPECTED_BENCHMARK_PASS_COUNT,
    EXPECTED_BOUNDARY_CONTROL_COUNT,
    EXPECTED_EVIDENCE_FIELD_COUNT,
    EXPECTED_FAMILY_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_8_family_benchmark_cases,
    evaluate_all_family_benchmark_cases,
    evaluate_family_benchmark_case,
    render_family_benchmark_cases_manifest,
    render_family_benchmark_cases_markdown,
    run_milestone_8_family_benchmark_cases_pipeline,
    validate_milestone_8_family_benchmark_cases,
    write_family_benchmark_cases_artifacts,
)


def test_each_known_family_benchmark_case_passes():
    case_ids = [
        "family_benchmark_color_palette_transfer_v2",
        "family_benchmark_color_background_guard_v2",
        "family_benchmark_object_component_detection_v2",
        "family_benchmark_object_translate_right_v2",
        "family_benchmark_object_translate_down_v2",
        "family_benchmark_shape_reflect_horizontal_v2",
        "family_benchmark_shape_reflect_vertical_v2",
        "family_benchmark_cross_family_candidate_ranking_v2",
    ]
    for case_id in case_ids:
        result = evaluate_family_benchmark_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_family_benchmark_case("missing_case")


def test_all_family_benchmark_cases_pass_and_cover_families():
    results = evaluate_all_family_benchmark_cases()
    assert len(results) == EXPECTED_BENCHMARK_CASE_COUNT
    assert all(result["passed"] is True for result in results)
    assert {result["family"] for result in results} == {
        "color_mapping",
        "object_model",
        "shape_symmetry",
        "cross_family_composition",
    }


def test_benchmark_record_ready():
    benchmark = build_milestone_8_family_benchmark_cases()
    assert benchmark["status"] == BENCHMARK_STATUS
    assert benchmark["benchmark_mode"] == BENCHMARK_MODE
    assert benchmark["benchmark_scope"] == BENCHMARK_SCOPE
    assert benchmark["benchmark_verdict"] == BENCHMARK_VERDICT
    assert benchmark["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert benchmark["family_count"] == EXPECTED_FAMILY_COUNT
    assert benchmark["benchmark_case_count"] == EXPECTED_BENCHMARK_CASE_COUNT
    assert benchmark["benchmark_pass_count"] == EXPECTED_BENCHMARK_PASS_COUNT
    assert benchmark["benchmark_failure_count"] == EXPECTED_BENCHMARK_FAILURE_COUNT
    assert benchmark["evidence_field_count"] == EXPECTED_EVIDENCE_FIELD_COUNT
    assert benchmark["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert benchmark["boundary_control_count"] == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert benchmark["passed_gate_count"] == len(BENCHMARK_GATES)
    assert benchmark["benchmark_issue_count"] == 0
    assert benchmark["benchmark_ready"] is True


def test_kernel_source_is_present_and_hashed():
    source = build_milestone_8_family_benchmark_cases()["kernel_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_READY"
    assert source["kernel_id"].startswith("MILESTONE-8-SOLVER-KERNEL-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_benchmark_keeps_submission_blocked():
    benchmark = build_milestone_8_family_benchmark_cases()
    assert benchmark["real_submission_created"] is False
    assert benchmark["real_submission_allowed"] is False
    assert benchmark["ready_for_real_kaggle_submission"] is False
    assert benchmark["kaggle_submission_sent"] is False
    assert benchmark["upload_performed"] is False
    assert benchmark["kaggle_authentication_performed"] is False
    assert benchmark["score_claim_absent"] is True
    assert benchmark["public_leaderboard_claim_absent"] is True


def test_benchmark_gates_and_issues_are_clean():
    benchmark = build_milestone_8_family_benchmark_cases()
    assert [item["name"] for item in benchmark["benchmark_gates"]] == list(BENCHMARK_GATES)
    assert [item["name"] for item in benchmark["benchmark_issues"]] == list(BENCHMARK_ISSUES)
    assert all(item["passed"] is True for item in benchmark["benchmark_gates"])
    assert all(item["active"] is False for item in benchmark["benchmark_issues"])


def test_benchmark_validation_passes():
    benchmark = build_milestone_8_family_benchmark_cases()
    validation = validate_milestone_8_family_benchmark_cases(benchmark)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_benchmark_pipeline_ready():
    payload = run_milestone_8_family_benchmark_cases_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["benchmark_status"] == BENCHMARK_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["benchmark_mode"] == BENCHMARK_MODE
    assert payload["benchmark_verdict"] == BENCHMARK_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["family_count"] == EXPECTED_FAMILY_COUNT
    assert payload["benchmark_case_count"] == EXPECTED_BENCHMARK_CASE_COUNT
    assert payload["benchmark_pass_count"] == EXPECTED_BENCHMARK_PASS_COUNT
    assert payload["benchmark_failure_count"] == EXPECTED_BENCHMARK_FAILURE_COUNT
    assert payload["benchmark_issue_count"] == 0
    assert payload["benchmark_ready"] is True
    assert payload["kaggle_submission_sent"] is False


def test_benchmark_markdown_contains_markers():
    markdown = render_family_benchmark_cases_markdown(build_milestone_8_family_benchmark_cases())
    assert "ARC_AGI3_MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_BENCHMARK_MODE=FAMILY_BENCHMARK_CASES_V2_LOCAL_ONLY" in markdown
    assert "ARC_AGI3_MILESTONE_8_BENCHMARK_PASS_COUNT=8" in markdown
    assert "ARC_AGI3_MILESTONE_8_BENCHMARK_FAILURE_COUNT=0" in markdown
    assert "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_4_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_benchmark_manifest_contains_results():
    manifest = render_family_benchmark_cases_manifest(build_milestone_8_family_benchmark_cases())
    assert "ARC AGI3 MILESTONE 8 FAMILY BENCHMARK CASES MANIFEST v2" in manifest
    assert "benchmark_mode=FAMILY_BENCHMARK_CASES_V2_LOCAL_ONLY" in manifest
    assert "BENCHMARK_RESULTS" in manifest
    assert "family_benchmark_color_palette_transfer_v2" in manifest
    assert "family_benchmark_cross_family_candidate_ranking_v2" in manifest
    assert "benchmark_pass_count=8" in manifest
    assert "benchmark_failure_count=0" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_benchmark_writes_artifacts(tmp_path: Path):
    benchmark = build_milestone_8_family_benchmark_cases()
    paths = write_family_benchmark_cases_artifacts(benchmark, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "FAMILY_BENCHMARK_CASES_V2_READY_FOR_CANDIDATE_GENERATOR_RUNTIME_UPGRADE" in Path(paths["index_path"]).read_text(encoding="utf-8")


def test_benchmark_metadata_safe():
    metadata = build_milestone_8_family_benchmark_cases()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_family_results_have_required_evidence_fields():
    benchmark = build_milestone_8_family_benchmark_cases()
    for result in benchmark["benchmark_results"]:
        assert set(result) == {
            "case_id",
            "family",
            "operation",
            "priority",
            "passed",
            "evidence_score",
            "expected_status",
            "actual_status",
        }


def test_benchmark_index_is_conservative():
    index = build_milestone_8_family_benchmark_cases()["benchmark_index"]
    assert index["benchmark_ready"] is True
    assert index["benchmark_locked"] is True
    assert index["benchmark_pass_count"] == 8
    assert index["benchmark_failure_count"] == 0
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False


def test_boundary_controls_are_complete():
    benchmark = build_milestone_8_family_benchmark_cases()
    assert benchmark["boundary_control_count"] == 9
    assert set(benchmark["boundary_controls"]) == {
        "public_safe",
        "deterministic",
        "local_only",
        "dry_run_only",
        "external_api_dependency_false",
        "contains_api_keys_false",
        "kaggle_submission_sent_false",
        "private_core_exposure_false",
        "legal_certification_false",
    }
