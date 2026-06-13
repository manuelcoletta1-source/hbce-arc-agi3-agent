import json
from pathlib import Path

import pytest

from hbce_arc_agi3.color_transform_detector import (
    apply_stable_color_mapping,
    build_color_transform_detector_smoke_pairs,
    detect_color_transform_pair,
    detect_color_transforms,
    render_color_transform_detector_markdown,
    run_color_transform_detector_pipeline,
    validate_color_transform_detection_report,
    write_color_transform_detector_artifacts,
)


def test_detect_color_transform_pair_identity():
    report = detect_color_transform_pair([[0, 1], [2, 2]], [[0, 1], [2, 2]])

    assert report.status == "COLOR_TRANSFORM_PAIR_READY"
    assert report.transform_type == "COLOR_IDENTITY_OR_PRESERVED"
    assert report.changed_source_colors == tuple()
    assert report.confidence == 1.0


def test_detect_color_transform_pair_recolor():
    report = detect_color_transform_pair([[0, 1], [2, 2]], [[0, 3], [2, 2]])

    assert report.transform_type == "COLOR_REMAP"
    assert report.changed_source_colors == (1,)
    assert report.dominant_mappings[1].source_color == 1
    assert report.dominant_mappings[1].target_color == 3


def test_detect_color_transform_pair_palette_expansion():
    report = detect_color_transform_pair([[0, 1], [1, 1]], [[0, 1], [1, 2]])

    assert report.transform_type == "AMBIGUOUS_COLOR_MAPPING"
    assert 2 in report.added_colors
    assert 1 in report.ambiguous_source_colors


def test_detect_color_transform_pair_palette_reduction():
    report = detect_color_transform_pair([[0, 1], [2, 2]], [[0, 1], [1, 1]])

    assert report.transform_type == "PALETTE_REDUCTION"
    assert report.removed_colors == (2,)
    assert report.changed_source_colors == (2,)


def test_detect_color_transform_pair_shape_changed():
    report = detect_color_transform_pair([[1, 1]], [[1], [1]])

    assert report.shape_preserving is False
    assert report.transform_type == "SHAPE_CHANGED_PALETTE_ONLY"
    assert report.dominant_mappings == tuple()


def test_detect_color_transform_pair_ambiguous_mapping():
    report = detect_color_transform_pair([[1, 1], [1, 1]], [[2, 2], [3, 3]])

    assert report.transform_type == "AMBIGUOUS_COLOR_MAPPING"
    assert report.ambiguous_source_colors == (1,)


def test_detect_color_transform_pair_background_mapping():
    report = detect_color_transform_pair([[0, 1], [0, 1]], [[0, 2], [0, 2]], input_background_color=0)

    assert report.background_mapping is not None
    assert report.background_mapping.source_color == 0
    assert report.background_mapping.target_color == 0


def test_detect_color_transforms_smoke_report():
    report = detect_color_transforms(build_color_transform_detector_smoke_pairs())

    assert report.status == "COLOR_TRANSFORM_DETECTION_READY"
    assert report.pair_count == 2
    assert report.transform_type == "AGGREGATE_STABLE_COLOR_REMAP"
    assert report.has_ambiguous_mapping is False
    assert report.confidence == 1.0


def test_detect_color_transforms_stable_mappings():
    report = detect_color_transforms(build_color_transform_detector_smoke_pairs())
    mapping_dict = {mapping.source_color: mapping.target_color for mapping in report.stable_mappings}

    assert mapping_dict[0] == 0
    assert mapping_dict[1] == 3
    assert mapping_dict[2] == 2


def test_detect_color_transforms_unstable_source_colors():
    report = detect_color_transforms(
        [
            {"input": [[1]], "output": [[2]]},
            {"input": [[1]], "output": [[3]]},
        ]
    )

    assert report.has_ambiguous_mapping is True
    assert report.unstable_source_colors == (1,)
    assert report.transform_type == "AGGREGATE_AMBIGUOUS_COLOR_MAPPING"


def test_apply_stable_color_mapping():
    report = detect_color_transforms(build_color_transform_detector_smoke_pairs())

    transformed = apply_stable_color_mapping([[1, 2, 0]], report.stable_mappings)

    assert transformed == [[3, 2, 0]]


def test_apply_stable_color_mapping_mapping_dicts():
    transformed = apply_stable_color_mapping(
        [[1, 2, 0]],
        [
            {"source_color": 1, "target_color": 4},
            {"source_color": 2, "target_color": 5},
        ],
    )

    assert transformed == [[4, 5, 0]]


def test_detect_color_transforms_rejects_empty_pairs():
    with pytest.raises(ValueError, match="at least one"):
        detect_color_transforms([])


def test_color_transform_detection_validation_passes():
    report = detect_color_transforms(build_color_transform_detector_smoke_pairs())
    validation = validate_color_transform_detection_report(report)

    assert validation["status"] == "COLOR_TRANSFORM_DETECTION_VALID"
    assert validation["valid"] is True
    assert validation["pair_count"] == 2


def test_color_transform_detection_validation_rejects_broken_payload():
    validation = validate_color_transform_detection_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "pair_reports": [],
        }
    )

    assert validation["status"] == "COLOR_TRANSFORM_DETECTION_INVALID"
    assert validation["valid"] is False


def test_color_transform_detector_pipeline_is_valid():
    payload = run_color_transform_detector_pipeline()

    assert payload["status"] == "COLOR_TRANSFORM_DETECTOR_PIPELINE_READY"
    assert payload["detector_status"] == "COLOR_TRANSFORM_DETECTION_READY"
    assert payload["validation_status"] == "COLOR_TRANSFORM_DETECTION_VALID"
    assert payload["stable_mapping_count"] == 3
    assert payload["metadata"]["candidate_generator_signal"] is True


def test_color_transform_detector_pipeline_is_deterministic():
    first = run_color_transform_detector_pipeline()
    second = run_color_transform_detector_pipeline()

    assert first == second
    assert first["signature"] == second["signature"]


def test_color_transform_detector_markdown_contains_boundary():
    payload = run_color_transform_detector_pipeline()
    markdown = render_color_transform_detector_markdown(payload)

    assert "# ARC-AGI-3 Milestone #4 Task 3" in markdown
    assert "candidate_generator_signal=true" in markdown
    assert "candidate_ranker_signal=true" in markdown
    assert "kaggle_submission_sent=false" in markdown


def test_color_transform_detector_writes_artifacts(tmp_path: Path):
    payload = run_color_transform_detector_pipeline()
    artifacts = write_color_transform_detector_artifacts(payload, output_dir=str(tmp_path / "colors"))

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["validation_status"] == "COLOR_TRANSFORM_DETECTION_VALID"
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Milestone #4 Task 3")
