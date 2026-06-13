import json
from pathlib import Path

import pytest

from hbce_arc_agi3.object_model import (
    build_object_model,
    build_object_model_from_grid,
    extract_grid,
    validate_object_model,
)
from hbce_arc_agi3.task_loader import load_task_file


def test_object_model_extracts_connected_components():
    grid = [
        [1, 0, 2, 2],
        [1, 0, 0, 2],
        [0, 3, 3, 0],
    ]

    model = build_object_model_from_grid(grid)
    validation = validate_object_model(model)

    assert model.status == "OBJECT_MODEL_READY"
    assert model.object_count == 3
    assert model.occupied_cell_count == 7
    assert model.grid_cell_count == 12
    assert model.object_density == 0.583333
    assert validation["status"] == "OBJECT_MODEL_VALID"

    first = model.objects[0]
    assert first.value == 1
    assert first.cell_count == 2
    assert first.bbox == {"min_row": 0, "min_col": 0, "max_row": 1, "max_col": 0}
    assert first.width == 1
    assert first.height == 2


def test_object_model_is_deterministic():
    grid = [
        [0, 4, 4],
        [0, 0, 4],
        [5, 0, 0],
    ]

    first = build_object_model_from_grid(grid)
    second = build_object_model_from_grid(grid)

    assert first.signature == second.signature
    assert first.to_dict() == second.to_dict()


def test_object_model_supports_loaded_task_payload(tmp_path: Path):
    task_path = tmp_path / "object-task.json"
    task_path.write_text(
        json.dumps({"id": "object-loaded", "grid": [[1, 1, 0], [0, 2, 2]], "goal": "solve"}),
        encoding="utf-8",
    )

    loaded = load_task_file(task_path, base_dir=tmp_path)
    model = build_object_model(loaded.to_dict())

    assert model.status == "OBJECT_MODEL_READY"
    assert model.object_count == 2
    assert model.metadata["executes_dataset_code"] is False
    assert model.metadata["external_api_dependency"] is False


def test_object_model_extract_grid_from_nested_payload():
    payload = {
        "run": {
            "loaded_task": {
                "normalized": {
                    "grid": [[7, 0], [7, 7]],
                }
            }
        }
    }

    assert extract_grid(payload) == [[7, 0], [7, 7]]


def test_object_model_rejects_invalid_grid_shape():
    with pytest.raises(ValueError, match="equal width"):
        build_object_model_from_grid([[1], [1, 2]])


def test_object_model_rejects_missing_grid():
    with pytest.raises(ValueError, match="No grid found"):
        build_object_model({"id": "missing-grid"})
