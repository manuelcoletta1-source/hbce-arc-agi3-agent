import json
from pathlib import Path

import pytest

from hbce_arc_agi3.shape_symmetry_detector import (
    build_shape_symmetry_detector_smoke_pairs,
    classify_shape_transform,
    detect_shape_transform_pair,
    detect_shape_symmetry_transforms,
    foreground_bbox,
    foreground_cells,
    foreground_mask,
    mask_signature,
    normalize_mask,
    reflect_mask_horizontal,
    reflect_mask_vertical,
    render_shape_symmetry_detector_markdown,
    rotate_mask_90,
    rotate_mask_180,
    rotate_mask_270,
    run_shape_symmetry_detector_pipeline,
    shape_symmetry_profile,
    validate_shape_symmetry_detection_report,
    write_shape_symmetry_detector_artifacts,
)


def test_normalize_mask_accepts_binary_mask():
    assert normalize_mask([[1, 0], [1, 1]]) == ((1, 0), (1, 1))


def test_normalize_mask_rejects_non_binary_value():
    with pytest.raises(ValueError, match="0 or 1"):
        normalize_mask([[2]])


def test_rotate_mask_90():
    assert rotate_mask_90([[1, 0], [1, 1]]) == ((1, 1), (1, 0))


def test_rotate_mask_180():
    assert rotate_mask_180([[1, 0], [1, 1]]) == ((1, 1), (0, 1))


def test_rotate_mask_270():
    assert rotate_mask_270([[1, 0], [1, 1]]) == ((0, 1), (1, 1))


def test_reflect_masks():
    mask = [[1, 0], [1, 1]]

    assert reflect_mask_horizontal(mask) == ((1, 1), (1, 0))
    assert reflect_mask_vertical(mask) == ((0, 1), (1, 1))


def test_shape_symmetry_profile_detects_symmetry():
    profile = shape_symmetry_profile([[1, 0, 1], [0, 1, 0], [1, 0, 1]])

    assert profile["horizontal_reflection_symmetric"] is True
    assert profile["vertical_reflection_symmetric"] is True
    assert profile["rotational_180_symmetric"] is True


def test_foreground_cells_and_bbox():
    cells = foreground_cells([[0, 1, 1], [0, 1, 0]], background_color=0)

    assert cells == ((0, 1), (0, 2), (1, 1))
    assert foreground_bbox(cells) == {
        "min_row": 0,
        "min_col": 1,
        "max_row": 1,
        "max_col": 2,
        "height": 2,
        "width": 2,
    }


def test_foreground_mask_trims_to_bbox():
    assert foreground_mask([[0, 1, 1], [0, 1, 0]], background_color=0) == ((1, 1), (1, 0))


def test_mask_signature_is_deterministic():
    assert mask_signature([[1, 0], [1, 1]]) == mask_signature([[1, 0], [1, 1]])


def test_classify_shape_transform_identity():
    assert classify_shape_transform([[1, 0], [1, 1]], [[1, 0], [1, 1]]) == "SHAPE_IDENTITY"


def test_classify_shape_transform_rotate_90():
    assert classify_shape_transform([[1, 0], [1, 1]], [[1, 1], [1, 0]]) == "ROTATE_90"


def test_classify_shape_transform_rotate_180():
    assert classify_shape_transform([[1, 0], [1, 1]], [[1, 1], [0, 1]]) == "ROTATE_180"


def test_classify_shape_transform_rotate_270():
    assert classify_shape_transform([[1, 0], [1, 1]], [[0, 1], [1, 1]]) == "ROTATE_270"


def test_classify_shape_transform_reflect_horizontal():
    assert classify_shape_transform([[1, 1], [1, 0]], [[1, 0], [1, 1]]) == "REFLECT_HORIZONTAL"


def test_classify_shape_transform_reflect_vertical():
    assert classify_shape_transform([[1, 1], [1, 0]], [[1, 1], [0, 1]]) == "REFLECT_VERTICAL"


def test_detect_shape_transform_pair_rotation():
    report = detect_shape_transform_pair(
        [[0, 1, 0], [0, 1, 1], [0, 0, 0]],
        [[0, 2, 2], [0, 2, 0], [0, 0, 0]],
    )

    assert report.status == "SHAPE_SYMMETRY_PAIR_READY"
    assert report.transform_type == "ROTATE_90"
    assert report.confidence == 1.0


def test_detect_shape_transform_pair_translation():
    report = detect_shape_transform_pair(
        [[1, 1, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 1, 1], [0, 1, 0]],
    )

    assert report.transform_type == "TRANSLATION"
    assert report.translation_vector == {"row_delta": 1, "col_delta": 1}


def test_detect_shape_transform_pair_shape_changed():
    report = detect_shape_transform_pair(
        [[1, 0], [0, 0]],
        [[1, 1], [0, 0]],
    )

    assert report.transform_type == "SHAPE_CHANGED"
    assert report.confidence == 0.0


def test_detect_shape_symmetry_transforms_smoke_report():
    report = detect_shape_symmetry_transforms(build_shape_symmetry_detector_smoke_pairs())

    assert report.status == "SHAPE_SYMMETRY_DETECTION_READY"
    assert report.pair_count == 2
    assert report.dominant_transform_type == "ROTATE_90"
    assert report.stable_transform_type == "ROTATE_90"
    assert report.has_rotation_signal is True
    assert report.confidence == 1.0


def test_detect_shape_symmetry_transforms_rejects_empty_pairs():
    with pytest.raises(ValueError, match="at least one"):
        detect_shape_symmetry_transforms([])


def test_shape_symmetry_detection_validation_passes():
    report = detect_shape_symmetry_transforms(build_shape_symmetry_detector_smoke_pairs())
    validation = validate_shape_symmetry_detection_report(report)

    assert validation["status"] == "SHAPE_SYMMETRY_DETECTION_VALID"
    assert validation["valid"] is True
    assert validation["pair_count"] == 2


def test_shape_symmetry_detection_validation_rejects_broken_payload():
    validation = validate_shape_symmetry_detection_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "pair_reports": [],
        }
    )

    assert validation["status"] == "SHAPE_SYMMETRY_DETECTION_INVALID"
    assert validation["valid"] is False


def test_shape_symmetry_detector_pipeline_is_valid():
    payload = run_shape_symmetry_detector_pipeline()

    assert payload["status"] == "SHAPE_SYMMETRY_DETECTOR_PIPELINE_READY"
    assert payload["detector_status"] == "SHAPE_SYMMETRY_DETECTION_READY"
    assert payload["validation_status"] == "SHAPE_SYMMETRY_DETECTION_VALID"
    assert payload["dominant_transform_type"] == "ROTATE_90"
    assert payload["metadata"]["candidate_generator_signal"] is True


def test_shape_symmetry_detector_pipeline_is_deterministic():
    first = run_shape_symmetry_detector_pipeline()
    second = run_shape_symmetry_detector_pipeline()

    assert first == second
    assert first["signature"] == second["signature"]


def test_shape_symmetry_detector_markdown_contains_boundary():
    payload = run_shape_symmetry_detector_pipeline()
    markdown = render_shape_symmetry_detector_markdown(payload)

    assert "# ARC-AGI-3 Milestone #4 Task 4" in markdown
    assert "candidate_generator_signal=true" in markdown
    assert "candidate_ranker_signal=true" in markdown
    assert "kaggle_submission_sent=false" in markdown


def test_shape_symmetry_detector_writes_artifacts(tmp_path: Path):
    payload = run_shape_symmetry_detector_pipeline()
    artifacts = write_shape_symmetry_detector_artifacts(payload, output_dir=str(tmp_path / "shape"))

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["validation_status"] == "SHAPE_SYMMETRY_DETECTION_VALID"
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Milestone #4 Task 4")
