import json
from pathlib import Path

import pytest

from hbce_arc_agi3.dataset_sample_registry import (
    build_dataset_sample_record,
    generate_and_validate_dataset_sample_registry,
    generate_dataset_sample_registry,
    render_dataset_sample_registry_markdown,
    validate_dataset_sample_registry,
    write_dataset_sample_registry_artifacts,
)


def test_dataset_sample_record_builds_valid_record():
    record = build_dataset_sample_record(
        {
            "name": "sample-record",
            "input_grid": [[0, 1], [0, 0]],
            "expected_output": [[0, 1], [0, 0]],
            "tags": ["smoke", "identity"],
        }
    )

    assert record.status == "DATASET_SAMPLE_RECORD_READY"
    assert record.sample_id.startswith("SAMPLE-")
    assert record.input_shape == [2, 2]
    assert record.expected_shape == [2, 2]
    assert record.metadata["public_safe"] is True


def test_dataset_sample_registry_generates_default_samples():
    registry = generate_dataset_sample_registry()
    validation = validate_dataset_sample_registry(registry)

    assert registry.status == "DATASET_SAMPLE_REGISTRY_READY"
    assert registry.registry_status == "DATASET_SAMPLE_REGISTRY_VALID"
    assert registry.sample_count == 3
    assert len(registry.sample_ids) == 3
    assert validation["status"] == "DATASET_SAMPLE_REGISTRY_VALID"


def test_dataset_sample_registry_pipeline_wrapper():
    result = generate_and_validate_dataset_sample_registry()

    assert result["status"] == "DATASET_SAMPLE_REGISTRY_PIPELINE_READY"
    assert result["dataset_sample_registry"]["status"] == "DATASET_SAMPLE_REGISTRY_READY"
    assert result["validation"]["status"] == "DATASET_SAMPLE_REGISTRY_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_dataset_sample_registry_is_deterministic():
    first = generate_dataset_sample_registry()
    second = generate_dataset_sample_registry()

    assert first.to_dict() == second.to_dict()
    assert first.signature == second.signature
    assert first.registry_id == second.registry_id


def test_dataset_sample_registry_accepts_custom_samples():
    registry = generate_dataset_sample_registry(
        [
            {
                "name": "custom-a",
                "split": "unit-test",
                "input_grid": [[1]],
                "expected_output": [[1]],
                "tags": ["custom"],
            }
        ]
    )

    assert registry.sample_count == 1
    assert registry.samples[0]["name"] == "custom-a"
    assert registry.samples[0]["split"] == "unit-test"


def test_dataset_sample_registry_rejects_invalid_grid():
    with pytest.raises(ValueError, match="rectangular"):
        build_dataset_sample_record(
            {
                "name": "bad-grid",
                "input_grid": [[1], [1, 2]],
                "expected_output": [[1]],
            }
        )


def test_dataset_sample_registry_rejects_missing_name():
    with pytest.raises(ValueError, match="name"):
        build_dataset_sample_record(
            {
                "input_grid": [[1]],
                "expected_output": [[1]],
            }
        )


def test_dataset_sample_registry_markdown_contains_boundary():
    registry = generate_dataset_sample_registry()
    markdown = render_dataset_sample_registry_markdown(registry)

    assert "# ARC-AGI-3 Dataset Sample Registry v1" in markdown
    assert "public_safe=true" in markdown
    assert "external_api_dependency=false" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert registry.signature in markdown


def test_dataset_sample_registry_writes_artifacts(tmp_path: Path):
    registry = generate_dataset_sample_registry()
    artifacts = write_dataset_sample_registry_artifacts(registry, output_dir=tmp_path / "registry")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["sample_count"] == 3
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Dataset Sample Registry v1")


def test_dataset_sample_registry_validation_rejects_broken_contract():
    validation = validate_dataset_sample_registry(
        {
            "status": "BROKEN",
            "metadata": {},
            "samples": [],
        }
    )

    assert validation["status"] == "DATASET_SAMPLE_REGISTRY_INVALID"
    assert validation["valid"] is False
