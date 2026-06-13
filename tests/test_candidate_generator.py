import json
from pathlib import Path

import pytest

from hbce_arc_agi3.candidate_generator import (
    apply_shape_transform_to_foreground,
    build_candidate_generator_smoke_expected_best_grid,
    build_candidate_generator_smoke_test_input,
    build_candidate_generator_smoke_train_pairs,
    generate_candidates,
    most_common_foreground_color,
    reflect_grid_horizontal,
    reflect_grid_vertical,
    render_candidate_generator_markdown,
    rotate_grid_90,
    rotate_grid_180,
    rotate_grid_270,
    run_candidate_generator_pipeline,
    transform_mask_by_type,
    validate_candidate_generation_report,
    write_candidate_generator_artifacts,
)


def test_grid_rotations_are_deterministic():
    grid = [[1, 2], [3, 4]]

    assert rotate_grid_90(grid) == [[3, 1], [4, 2]]
    assert rotate_grid_180(grid) == [[4, 3], [2, 1]]
    assert rotate_grid_270(grid) == [[2, 4], [1, 3]]


def test_grid_reflections_are_deterministic():
    grid = [[1, 2], [3, 4]]

    assert reflect_grid_horizontal(grid) == [[3, 4], [1, 2]]
    assert reflect_grid_vertical(grid) == [[2, 1], [4, 3]]


def test_transform_mask_by_type_rotates():
    assert transform_mask_by_type([[1, 0], [1, 1]], "ROTATE_90") == ((1, 1), (1, 0))


def test_transform_mask_by_type_reflects():
    assert transform_mask_by_type([[1, 0], [1, 1]], "REFLECT_VERTICAL") == ((0, 1), (1, 1))


def test_most_common_foreground_color():
    assert most_common_foreground_color([[0, 3, 3], [0, 2, 3]], background_color=0) == 3


def test_apply_shape_transform_to_foreground_rotate_90():
    grid = [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]

    transformed = apply_shape_transform_to_foreground(grid, "ROTATE_90", background_color=0, fill_color=9)

    assert transformed == [
        [0, 9, 9],
        [0, 9, 0],
        [0, 0, 0],
    ]


def test_apply_shape_transform_to_foreground_identity():
    grid = [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]

    transformed = apply_shape_transform_to_foreground(grid, "SHAPE_IDENTITY", background_color=0, fill_color=1)

    assert transformed == grid


def test_generate_candidates_report_ready():
    report = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )

    assert report.status == "CANDIDATE_GENERATION_READY"
    assert report.train_pair_count == 2
    assert report.candidate_count == 4
    assert report.best_candidate.candidate_type == "COLOR_SHAPE_COMBINED"


def test_generate_candidates_best_matches_expected_smoke():
    report = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )

    assert report.best_candidate.candidate_grid == tuple(tuple(row) for row in build_candidate_generator_smoke_expected_best_grid())


def test_generate_candidates_uses_previous_modules():
    report = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )

    assert report.object_extraction["status"] == "GRID_OBJECT_EXTRACTION_READY"
    assert report.color_detection["status"] == "COLOR_TRANSFORM_DETECTION_READY"
    assert report.shape_detection["status"] == "SHAPE_SYMMETRY_DETECTION_READY"


def test_generate_candidates_rejects_empty_train_pairs():
    with pytest.raises(ValueError, match="at least one"):
        generate_candidates([], build_candidate_generator_smoke_test_input())


def test_candidate_generation_validation_passes():
    report = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )
    validation = validate_candidate_generation_report(report)

    assert validation["status"] == "CANDIDATE_GENERATION_VALID"
    assert validation["valid"] is True
    assert validation["candidate_count"] == 4
    assert validation["best_candidate_type"] == "COLOR_SHAPE_COMBINED"


def test_candidate_generation_validation_rejects_broken_payload():
    validation = validate_candidate_generation_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "candidates": [],
            "best_candidate": {},
        }
    )

    assert validation["status"] == "CANDIDATE_GENERATION_INVALID"
    assert validation["valid"] is False


def test_candidate_generator_pipeline_is_valid():
    payload = run_candidate_generator_pipeline()

    assert payload["status"] == "CANDIDATE_GENERATOR_PIPELINE_READY"
    assert payload["generator_status"] == "CANDIDATE_GENERATION_READY"
    assert payload["validation_status"] == "CANDIDATE_GENERATION_VALID"
    assert payload["candidate_count"] == 4
    assert payload["best_candidate_type"] == "COLOR_SHAPE_COMBINED"
    assert payload["best_candidate_matches_expected_smoke"] is True
    assert payload["metadata"]["uses_grid_object_extractor_v1"] is True
    assert payload["metadata"]["uses_color_transform_detector_v1"] is True
    assert payload["metadata"]["uses_shape_symmetry_detector_v1"] is True


def test_candidate_generator_pipeline_is_deterministic():
    first = run_candidate_generator_pipeline()
    second = run_candidate_generator_pipeline()

    assert first == second
    assert first["signature"] == second["signature"]


def test_candidate_generator_markdown_contains_boundary():
    payload = run_candidate_generator_pipeline()
    markdown = render_candidate_generator_markdown(payload)

    assert "# ARC-AGI-3 Milestone #4 Task 5" in markdown
    assert "candidate_generator_output=true" in markdown
    assert "candidate_ranker_input=true" in markdown
    assert "kaggle_submission_sent=false" in markdown


def test_candidate_generator_writes_artifacts(tmp_path: Path):
    payload = run_candidate_generator_pipeline()
    artifacts = write_candidate_generator_artifacts(payload, output_dir=str(tmp_path / "candidate"))

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["validation_status"] == "CANDIDATE_GENERATION_VALID"
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Milestone #4 Task 5")
