from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_candidate_generator_runtime_upgrade import (
    EXPECTED_BOUNDARY_CONTROL_COUNT,
    EXPECTED_FAMILY_COUNT,
    EXPECTED_GENERATOR_OPERATION_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_RUNTIME_CASE_COUNT,
    EXPECTED_RUNTIME_FAILURE_COUNT,
    EXPECTED_RUNTIME_PASS_COUNT,
    EXPECTED_RUNTIME_PROFILE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    RUNTIME_GATES,
    RUNTIME_ISSUES,
    RUNTIME_MODE,
    RUNTIME_SCOPE,
    RUNTIME_STATUS,
    RUNTIME_VERDICT,
    VALIDATION_STATUS,
    build_color_mapping_runtime_candidates,
    build_milestone_8_candidate_generator_runtime_upgrade,
    build_object_model_runtime_candidates,
    build_shape_symmetry_runtime_candidates,
    evaluate_all_runtime_upgrade_cases,
    evaluate_runtime_upgrade_case,
    generate_runtime_upgraded_candidates,
    render_candidate_generator_runtime_upgrade_manifest,
    render_candidate_generator_runtime_upgrade_markdown,
    run_milestone_8_candidate_generator_runtime_upgrade_pipeline,
    validate_milestone_8_candidate_generator_runtime_upgrade,
    write_candidate_generator_runtime_upgrade_artifacts,
)
from hbce_arc_agi3.milestone_8_competitive_solver_kernel import normalize_grid


def test_color_mapping_runtime_candidates_use_training_pair():
    training_input = normalize_grid([[0, 1, 2], [0, 1, 2]])
    training_output = normalize_grid([[0, 3, 4], [0, 3, 4]])
    target_input = normalize_grid([[0, 1, 2], [2, 1, 0]])
    expected = normalize_grid([[0, 3, 4], [4, 3, 0]])
    candidates = build_color_mapping_runtime_candidates(
        target_input,
        training_input=training_input,
        training_output=training_output,
    )
    assert any(candidate["grid"] == expected for candidate in candidates)
    assert all(candidate["family"] == "color_mapping" for candidate in candidates)


def test_color_mapping_runtime_candidates_preserve_background():
    grid = normalize_grid([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
    candidates = build_color_mapping_runtime_candidates(grid)
    assert any(candidate["grid"] == normalize_grid([[0, 2, 0], [0, 2, 0], [0, 0, 0]]) for candidate in candidates)


def test_object_model_runtime_candidates_include_right_and_down():
    grid = normalize_grid([[0, 0, 0, 0], [0, 5, 5, 0], [0, 0, 0, 0]])
    candidates = build_object_model_runtime_candidates(grid)
    grids = {candidate["grid"] for candidate in candidates}
    assert normalize_grid([[0, 0, 0, 0], [0, 0, 5, 5], [0, 0, 0, 0]]) in grids
    assert normalize_grid([[0, 0, 0, 0], [0, 0, 0, 0], [0, 5, 5, 0]]) in grids


def test_shape_symmetry_runtime_candidates_include_reflections():
    grid = normalize_grid([[1, 0], [2, 0], [3, 0]])
    candidates = build_shape_symmetry_runtime_candidates(grid)
    grids = {candidate["grid"] for candidate in candidates}
    assert normalize_grid([[3, 0], [2, 0], [1, 0]]) in grids
    assert normalize_grid([[0, 1], [0, 2], [0, 3]]) in grids


def test_generate_runtime_upgraded_candidates_ranked_and_deduplicated():
    candidates = generate_runtime_upgraded_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
    signatures = [candidate["signature"] for candidate in candidates]
    scores = [candidate["evidence_score"] for candidate in candidates]
    assert len(candidates) >= 4
    assert len(signatures) == len(set(signatures))
    assert scores == sorted(scores, reverse=True)
    assert [candidate["runtime_rank"] for candidate in candidates] == list(range(1, len(candidates) + 1))


def test_generate_runtime_upgraded_candidates_covers_core_families():
    candidates = generate_runtime_upgraded_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
    families = {candidate["family"] for candidate in candidates}
    assert {"color_mapping", "object_model", "shape_symmetry"}.issubset(families)
    assert all(candidate["runtime_candidate_ready"] is True for candidate in candidates)


def test_each_runtime_upgrade_case_passes():
    case_ids = [
        "runtime_upgrade_color_training_pair_candidate_v2",
        "runtime_upgrade_color_background_guard_candidate_v2",
        "runtime_upgrade_object_translate_right_candidate_v2",
        "runtime_upgrade_object_translate_down_candidate_v2",
        "runtime_upgrade_shape_reflect_horizontal_candidate_v2",
        "runtime_upgrade_shape_reflect_vertical_candidate_v2",
        "runtime_upgrade_cross_family_merge_deduplicate_v2",
        "runtime_upgrade_cross_family_rank_candidates_v2",
    ]
    for case_id in case_ids:
        result = evaluate_runtime_upgrade_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_runtime_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_runtime_upgrade_case("missing_runtime_case")


def test_all_runtime_upgrade_cases_pass_and_cover_families():
    results = evaluate_all_runtime_upgrade_cases()
    assert len(results) == EXPECTED_RUNTIME_CASE_COUNT
    assert all(result["passed"] is True for result in results)
    assert {result["family"] for result in results} == {
        "color_mapping",
        "object_model",
        "shape_symmetry",
        "cross_family_composition",
    }


def test_runtime_record_ready():
    runtime = build_milestone_8_candidate_generator_runtime_upgrade()
    assert runtime["status"] == RUNTIME_STATUS
    assert runtime["runtime_mode"] == RUNTIME_MODE
    assert runtime["runtime_scope"] == RUNTIME_SCOPE
    assert runtime["runtime_verdict"] == RUNTIME_VERDICT
    assert runtime["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert runtime["family_count"] == EXPECTED_FAMILY_COUNT
    assert runtime["runtime_profile_count"] == EXPECTED_RUNTIME_PROFILE_COUNT
    assert runtime["generator_operation_count"] == EXPECTED_GENERATOR_OPERATION_COUNT
    assert runtime["runtime_case_count"] == EXPECTED_RUNTIME_CASE_COUNT
    assert runtime["runtime_pass_count"] == EXPECTED_RUNTIME_PASS_COUNT
    assert runtime["runtime_failure_count"] == EXPECTED_RUNTIME_FAILURE_COUNT
    assert runtime["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert runtime["boundary_control_count"] == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert runtime["passed_gate_count"] == len(RUNTIME_GATES)
    assert runtime["runtime_issue_count"] == 0
    assert runtime["runtime_ready"] is True


def test_benchmark_source_is_present_and_hashed():
    source = build_milestone_8_candidate_generator_runtime_upgrade()["benchmark_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_READY"
    assert source["benchmark_id"].startswith("MILESTONE-8-FAMILY-BENCHMARK-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_runtime_keeps_submission_blocked():
    runtime = build_milestone_8_candidate_generator_runtime_upgrade()
    assert runtime["real_submission_created"] is False
    assert runtime["real_submission_allowed"] is False
    assert runtime["ready_for_real_kaggle_submission"] is False
    assert runtime["kaggle_submission_sent"] is False
    assert runtime["upload_performed"] is False
    assert runtime["kaggle_authentication_performed"] is False
    assert runtime["score_claim_absent"] is True
    assert runtime["public_leaderboard_claim_absent"] is True


def test_runtime_gates_and_issues_are_clean():
    runtime = build_milestone_8_candidate_generator_runtime_upgrade()
    assert [item["name"] for item in runtime["runtime_gates"]] == list(RUNTIME_GATES)
    assert [item["name"] for item in runtime["runtime_issues"]] == list(RUNTIME_ISSUES)
    assert all(item["passed"] is True for item in runtime["runtime_gates"])
    assert all(item["active"] is False for item in runtime["runtime_issues"])


def test_runtime_validation_and_pipeline_pass():
    runtime = build_milestone_8_candidate_generator_runtime_upgrade()
    validation = validate_milestone_8_candidate_generator_runtime_upgrade(runtime)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_8_candidate_generator_runtime_upgrade_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["runtime_status"] == RUNTIME_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["runtime_ready"] is True
    assert payload["runtime_pass_count"] == 8
    assert payload["runtime_failure_count"] == 0


def test_runtime_markdown_and_manifest_contain_markers():
    runtime = build_milestone_8_candidate_generator_runtime_upgrade()
    markdown = render_candidate_generator_runtime_upgrade_markdown(runtime)
    manifest = render_candidate_generator_runtime_upgrade_manifest(runtime)
    assert "ARC_AGI3_MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_RUNTIME_PASS_COUNT=8" in markdown
    assert "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_5_RANKER_RUNTIME_UPGRADE_V2" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "RUNTIME_RESULTS" in manifest
    assert "SAMPLE_CANDIDATES" in manifest
    assert "runtime_upgrade_color_training_pair_candidate_v2" in manifest
    assert "runtime_upgrade_cross_family_rank_candidates_v2" in manifest


def test_runtime_writes_artifacts(tmp_path: Path):
    runtime = build_milestone_8_candidate_generator_runtime_upgrade()
    paths = write_candidate_generator_runtime_upgrade_artifacts(runtime, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY_FOR_RANKER_RUNTIME_UPGRADE" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_runtime_metadata_safe():
    metadata = build_milestone_8_candidate_generator_runtime_upgrade()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
