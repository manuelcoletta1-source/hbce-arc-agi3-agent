from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_competitive_solver_kernel import (
    EXPECTED_BOUNDARY_CONTROL_COUNT,
    EXPECTED_KERNEL_FAMILY_COUNT,
    EXPECTED_KERNEL_OPERATION_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SAMPLE_CASE_COUNT,
    KERNEL_GATES,
    KERNEL_ISSUES,
    KERNEL_MODE,
    KERNEL_SCOPE,
    KERNEL_STATUS,
    KERNEL_VERDICT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    apply_color_mapping,
    background_color,
    build_milestone_8_competitive_solver_kernel,
    candidate_signature,
    connected_components,
    generate_kernel_candidates,
    infer_color_mapping,
    merge_candidate_sets,
    normalize_grid,
    rank_kernel_candidates,
    reflect_grid_horizontal,
    reflect_grid_vertical,
    render_competitive_solver_kernel_manifest,
    render_competitive_solver_kernel_markdown,
    run_milestone_8_competitive_solver_kernel_pipeline,
    translate_component,
    validate_milestone_8_competitive_solver_kernel,
    write_competitive_solver_kernel_artifacts,
)


def test_normalize_grid_rejects_bad_grid():
    assert normalize_grid([[1, 2], [3, 4]]) == ((1, 2), (3, 4))
    with pytest.raises(ValueError):
        normalize_grid([])
    with pytest.raises(ValueError):
        normalize_grid([[1], [1, 2]])


def test_background_color_is_frequency_based_with_tiebreak():
    assert background_color([[0, 1, 1], [0, 2, 2]]) == 0
    assert background_color([[9, 8], [8, 9]]) == 8


def test_color_mapping_infers_and_applies_palette_transfer():
    source = [[0, 1, 1], [0, 2, 2]]
    target = [[0, 3, 3], [0, 4, 4]]
    mapping = infer_color_mapping(source, target)
    assert mapping == {0: 0, 1: 3, 2: 4}
    assert apply_color_mapping(source, mapping) == normalize_grid(target)


def test_color_mapping_conflict_resolution_is_deterministic():
    source = [[1, 1, 1], [2, 2, 2]]
    target = [[7, 7, 8], [4, 5, 4]]
    assert infer_color_mapping(source, target) == {1: 7, 2: 4}


def test_apply_color_mapping_preserves_background():
    grid = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
    assert apply_color_mapping(grid, {0: 9, 1: 2}, preserve_background=True)[0][0] == 0
    assert apply_color_mapping(grid, {0: 9, 1: 2}, preserve_background=True)[1][1] == 2
    assert apply_color_mapping(grid, {0: 9, 1: 2}, preserve_background=False)[0][0] == 9


def test_connected_components_detects_objects():
    components = connected_components([[0, 2, 2], [0, 0, 0], [3, 0, 3]], background=0)
    assert len(components) == 3
    assert components[0]["size"] == 2
    assert components[0]["color"] == 2


def test_translate_component_moves_in_bounds_and_blocks_out_of_bounds():
    grid = normalize_grid([[0, 0, 0], [0, 5, 5], [0, 0, 0]])
    cells = connected_components(grid, background=0)[0]["cells"]
    assert translate_component(grid, cells, dr=1, dc=0) == normalize_grid([[0, 0, 0], [0, 0, 0], [0, 5, 5]])
    assert translate_component(grid, cells, dr=0, dc=2) == grid


def test_reflection_operations_preserve_dimensions():
    grid = [[1, 0], [2, 0], [3, 0]]
    assert reflect_grid_horizontal(grid) == normalize_grid([[3, 0], [2, 0], [1, 0]])
    assert reflect_grid_vertical(grid) == normalize_grid([[0, 1], [0, 2], [0, 3]])


def test_candidate_signature_is_deterministic():
    grid = [[1, 2], [3, 4]]
    assert candidate_signature(grid) == candidate_signature(grid)
    assert candidate_signature(grid) != candidate_signature([[1, 2], [4, 3]])


def test_merge_candidate_sets_deduplicates_by_grid_and_keeps_best_score():
    grid = normalize_grid([[1]])
    merged = merge_candidate_sets(
        [{"candidate_id": "low", "family": "x", "operation": "a", "grid": grid, "evidence_score": 1.0}],
        [{"candidate_id": "high", "family": "x", "operation": "b", "grid": grid, "evidence_score": 5.0}],
    )
    assert len(merged) == 1
    assert merged[0]["candidate_id"] == "high"


def test_rank_kernel_candidates_orders_by_score_then_signature():
    candidates = rank_kernel_candidates(
        [
            {"candidate_id": "a", "family": "x", "operation": "a", "grid": [[1]], "evidence_score": 1.0},
            {"candidate_id": "b", "family": "x", "operation": "b", "grid": [[2]], "evidence_score": 9.0},
        ]
    )
    assert candidates[0]["candidate_id"] == "b"
    assert "rank_signal" in candidates[0]


def test_generate_kernel_candidates_returns_ranked_candidates():
    candidates = generate_kernel_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
    assert len(candidates) >= 4
    assert candidates[0]["evidence_score"] >= candidates[-1]["evidence_score"]
    assert all("signature" in item for item in candidates)


def test_kernel_record_ready():
    kernel = build_milestone_8_competitive_solver_kernel()
    assert kernel["status"] == KERNEL_STATUS
    assert kernel["kernel_mode"] == KERNEL_MODE
    assert kernel["kernel_scope"] == KERNEL_SCOPE
    assert kernel["kernel_verdict"] == KERNEL_VERDICT
    assert kernel["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert kernel["kernel_family_count"] == EXPECTED_KERNEL_FAMILY_COUNT
    assert kernel["kernel_operation_count"] == EXPECTED_KERNEL_OPERATION_COUNT
    assert kernel["sample_case_count"] == EXPECTED_SAMPLE_CASE_COUNT
    assert kernel["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert kernel["boundary_control_count"] == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert kernel["passed_gate_count"] == len(KERNEL_GATES)
    assert kernel["kernel_issue_count"] == 0
    assert kernel["kernel_ready"] is True


def test_kernel_keeps_submission_blocked():
    kernel = build_milestone_8_competitive_solver_kernel()
    assert kernel["solver_kernel_v2_created"] is True
    assert kernel["runtime_solver_iteration_performed"] is True
    assert kernel["real_submission_created"] is False
    assert kernel["real_submission_allowed"] is False
    assert kernel["ready_for_real_kaggle_submission"] is False
    assert kernel["kaggle_submission_sent"] is False
    assert kernel["upload_performed"] is False
    assert kernel["kaggle_authentication_performed"] is False


def test_kernel_gates_and_issues_are_clean():
    kernel = build_milestone_8_competitive_solver_kernel()
    assert [item["name"] for item in kernel["kernel_gates"]] == list(KERNEL_GATES)
    assert [item["name"] for item in kernel["kernel_issues"]] == list(KERNEL_ISSUES)
    assert all(item["passed"] is True for item in kernel["kernel_gates"])
    assert all(item["active"] is False for item in kernel["kernel_issues"])


def test_kernel_validation_pipeline_and_artifacts(tmp_path: Path):
    kernel = build_milestone_8_competitive_solver_kernel()
    validation = validate_milestone_8_competitive_solver_kernel(kernel)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_8_competitive_solver_kernel_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["kernel_status"] == KERNEL_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS

    markdown = render_competitive_solver_kernel_markdown(kernel)
    manifest = render_competitive_solver_kernel_manifest(kernel)
    assert "ARC_AGI3_MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_SOLVER_KERNEL_V2_CREATED=true" in markdown
    assert "KERNEL_OPERATIONS" in manifest
    assert "infer_color_mapping" in manifest

    paths = write_competitive_solver_kernel_artifacts(kernel, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
