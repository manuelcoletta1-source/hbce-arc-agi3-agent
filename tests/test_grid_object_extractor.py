import json
from pathlib import Path

import pytest

from hbce_arc_agi3.grid_object_extractor import (
    build_grid_object_extractor_smoke_grid,
    color_inventory,
    extract_grid_objects,
    infer_background_color,
    render_grid_object_extractor_markdown,
    run_grid_object_extractor_pipeline,
    validate_grid_object_extraction_report,
    write_grid_object_extractor_artifacts,
)


def test_color_inventory_counts_colors():
    assert color_inventory([[0, 1], [1, 2]]) == {0: 1, 1: 2, 2: 1}


def test_infer_background_prefers_zero_when_present():
    assert infer_background_color([[2, 2], [0, 1]]) == 0


def test_infer_background_uses_most_frequent_without_zero():
    assert infer_background_color([[2, 2], [1, 3]]) == 2


def test_extract_grid_objects_excludes_background_by_default():
    report = extract_grid_objects(build_grid_object_extractor_smoke_grid(), background_color=0)

    assert report.status == "GRID_OBJECT_EXTRACTION_READY"
    assert report.background_color == 0
    assert report.object_count == 3
    assert [obj.color for obj in report.objects] == [1, 2, 3]


def test_extract_grid_objects_computes_density():
    report = extract_grid_objects(build_grid_object_extractor_smoke_grid(), background_color=0)

    assert report.object_density == 0.583333


def test_extract_grid_objects_bounding_box_and_area():
    report = extract_grid_objects(build_grid_object_extractor_smoke_grid(), background_color=0)
    first = report.objects[0]

    assert first.color == 1
    assert first.area == 3
    assert first.bounding_box == {
        "min_row": 0,
        "min_col": 1,
        "max_row": 1,
        "max_col": 2,
        "height": 2,
        "width": 2,
    }


def test_extract_grid_objects_centroid_and_border_touch():
    report = extract_grid_objects(build_grid_object_extractor_smoke_grid(), background_color=0)
    first = report.objects[0]

    assert first.centroid == {"row": 0.333333, "col": 1.333333}
    assert first.touches_border is True


def test_extract_grid_objects_mask_is_relative_to_bbox():
    report = extract_grid_objects(build_grid_object_extractor_smoke_grid(), background_color=0)
    first = report.objects[0]

    assert first.mask == ((1, 1), (1, 0))


def test_extract_grid_objects_include_background():
    report = extract_grid_objects(build_grid_object_extractor_smoke_grid(), background_color=0, include_background=True)

    assert report.include_background is True
    assert report.object_count > 3
    assert any(obj.color == 0 for obj in report.objects)


def test_extract_grid_objects_connectivity_8_merges_diagonal_cells():
    grid = [[1, 0], [0, 1]]

    report_4 = extract_grid_objects(grid, background_color=0, connectivity=4)
    report_8 = extract_grid_objects(grid, background_color=0, connectivity=8)

    assert report_4.object_count == 2
    assert report_8.object_count == 1


def test_extract_grid_objects_rejects_invalid_connectivity():
    with pytest.raises(ValueError, match="connectivity"):
        extract_grid_objects([[1]], connectivity=6)


def test_extract_grid_objects_rejects_invalid_background_color():
    with pytest.raises(ValueError, match="background_color"):
        extract_grid_objects([[1]], background_color=99)


def test_grid_object_extraction_validation_passes():
    report = extract_grid_objects(build_grid_object_extractor_smoke_grid(), background_color=0)
    validation = validate_grid_object_extraction_report(report)

    assert validation["status"] == "GRID_OBJECT_EXTRACTION_VALID"
    assert validation["valid"] is True
    assert validation["object_count"] == 3


def test_grid_object_extraction_validation_rejects_broken_payload():
    validation = validate_grid_object_extraction_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "objects": [],
        }
    )

    assert validation["status"] == "GRID_OBJECT_EXTRACTION_INVALID"
    assert validation["valid"] is False


def test_grid_object_extractor_pipeline_is_valid():
    payload = run_grid_object_extractor_pipeline()

    assert payload["status"] == "GRID_OBJECT_EXTRACTOR_PIPELINE_READY"
    assert payload["extractor_status"] == "GRID_OBJECT_EXTRACTION_READY"
    assert payload["validation_status"] == "GRID_OBJECT_EXTRACTION_VALID"
    assert payload["object_count"] == 3
    assert payload["metadata"]["agentic_state_feature"] is True


def test_grid_object_extractor_pipeline_is_deterministic():
    first = run_grid_object_extractor_pipeline()
    second = run_grid_object_extractor_pipeline()

    assert first == second
    assert first["signature"] == second["signature"]


def test_grid_object_extractor_markdown_contains_boundary():
    payload = run_grid_object_extractor_pipeline()
    markdown = render_grid_object_extractor_markdown(payload)

    assert "# ARC-AGI-3 Milestone #4 Task 2" in markdown
    assert "agentic_state_feature=true" in markdown
    assert "kaggle_submission_sent=false" in markdown


def test_grid_object_extractor_writes_artifacts(tmp_path: Path):
    payload = run_grid_object_extractor_pipeline()
    artifacts = write_grid_object_extractor_artifacts(payload, output_dir=str(tmp_path / "objects"))

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["validation_status"] == "GRID_OBJECT_EXTRACTION_VALID"
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Milestone #4 Task 2")
