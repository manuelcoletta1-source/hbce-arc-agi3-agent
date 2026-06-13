import json
from pathlib import Path

import pytest

from hbce_arc_agi3.observer import observe_agent_state
from hbce_arc_agi3.task_loader import (
    list_task_json_files,
    load_and_validate_task_file,
    load_task_directory,
    load_task_file,
    validate_loaded_task,
)
from hbce_arc_agi3.world_model import build_world_model_from_observation


def test_task_loader_loads_json_and_normalizes_task(tmp_path: Path):
    task_path = tmp_path / "task.json"
    task_path.write_text(
        json.dumps({"id": "loader-demo", "grid": [[1, 0], [2, 2]], "goal": "solve"}),
        encoding="utf-8",
    )

    loaded = load_task_file(task_path, base_dir=tmp_path)
    validation = validate_loaded_task(loaded)

    assert loaded.status == "TASK_LOADER_READY"
    assert loaded.task_id == "loader-demo"
    assert loaded.normalized["task_id"] == "loader-demo"
    assert loaded.normalized["grid"] == [[1, 0], [2, 2]]
    assert loaded.metadata["executes_dataset_code"] is False
    assert validation["status"] == "TASK_LOADER_VALID"


def test_task_loader_rejects_non_json_files(tmp_path: Path):
    task_path = tmp_path / "task.txt"
    task_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="must be .json"):
        load_task_file(task_path, base_dir=tmp_path)


def test_task_loader_rejects_base_dir_escape(tmp_path: Path):
    outside = tmp_path.parent / "outside-task-loader-test.json"
    outside.write_text('{"id":"outside","grid":[[1]],"goal":"solve"}', encoding="utf-8")

    try:
        with pytest.raises(ValueError, match="escapes base_dir"):
            load_task_file(outside, base_dir=tmp_path)
    finally:
        outside.unlink(missing_ok=True)


def test_task_loader_directory_is_deterministic(tmp_path: Path):
    b = tmp_path / "b.json"
    a = tmp_path / "a.json"
    noise = tmp_path / "ignore.txt"

    b.write_text('{"id":"b","grid":[[2]],"goal":"solve"}', encoding="utf-8")
    a.write_text('{"id":"a","grid":[[1]],"goal":"solve"}', encoding="utf-8")
    noise.write_text("ignored", encoding="utf-8")

    files = list_task_json_files(tmp_path)
    loaded = load_task_directory(tmp_path)

    assert [Path(path).name for path in files] == ["a.json", "b.json"]
    assert [task.task_id for task in loaded] == ["a", "b"]


def test_task_loader_output_feeds_observer_world_model(tmp_path: Path):
    task_path = tmp_path / "pipeline.json"
    task_path.write_text(
        json.dumps({"id": "pipeline-demo", "grid": [[1, 0], [0, 1]], "goal": "solve"}),
        encoding="utf-8",
    )

    result = load_and_validate_task_file(task_path, base_dir=tmp_path)
    loaded_state = result["loaded_task"]["normalized"]

    observation = observe_agent_state(loaded_state)
    world = build_world_model_from_observation(observation.to_dict())

    assert result["status"] == "TASK_LOADER_PIPELINE_READY"
    assert result["validation"]["status"] == "TASK_LOADER_VALID"
    assert observation.status == "OBSERVER_READY"
    assert world.status == "WORLD_MODEL_READY"
    assert world.density == 0.5
