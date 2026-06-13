import json
from pathlib import Path

import pytest

from hbce_arc_agi3.environment_harness import (
    run_and_validate_task_file,
    run_loaded_task,
    run_task_file,
    validate_environment_run,
)
from hbce_arc_agi3.task_loader import load_task_file


def test_environment_harness_runs_task_file_pipeline(tmp_path: Path):
    task_path = tmp_path / "task.json"
    task_path.write_text(
        json.dumps({"id": "env-demo", "grid": [[1, 0], [2, 2]], "goal": "solve"}),
        encoding="utf-8",
    )

    run = run_task_file(task_path, base_dir=tmp_path)
    validation = validate_environment_run(run)

    assert run.status == "ENVIRONMENT_HARNESS_READY"
    assert run.task_id == "env-demo"
    assert run.observation["status"] == "OBSERVER_READY"
    assert run.world_model["status"] == "WORLD_MODEL_READY"
    assert run.plan["status"] == "PLANNER_READY"
    assert run.verification_scoring["status"] == "VERIFICATION_SCORING_READY"
    assert run.trace_validation["status"] == "TRACE_SCHEMA_VALID"
    assert validation["status"] == "ENVIRONMENT_HARNESS_VALID"


def test_environment_harness_run_id_is_deterministic(tmp_path: Path):
    task_path = tmp_path / "stable.json"
    task_path.write_text(
        json.dumps({"id": "stable-run", "grid": [[1, 0], [0, 1]], "goal": "solve"}),
        encoding="utf-8",
    )

    first = run_task_file(task_path, base_dir=tmp_path)
    second = run_task_file(task_path, base_dir=tmp_path)

    assert first.run_id == second.run_id
    assert first.to_dict() == second.to_dict()


def test_environment_harness_loaded_task_entrypoint(tmp_path: Path):
    task_path = tmp_path / "loaded.json"
    task_path.write_text(
        json.dumps({"id": "loaded-entrypoint", "grid": [[3]], "goal": "solve"}),
        encoding="utf-8",
    )

    loaded = load_task_file(task_path, base_dir=tmp_path)
    run = run_loaded_task(loaded)

    assert run.status == "ENVIRONMENT_HARNESS_READY"
    assert run.task_id == "loaded-entrypoint"
    assert run.metadata["executes_dataset_code"] is False
    assert run.metadata["external_api_dependency"] is False


def test_environment_harness_wrapper_contract(tmp_path: Path):
    task_path = tmp_path / "wrapper.json"
    task_path.write_text(
        json.dumps({"id": "wrapper-demo", "grid": [[1]], "goal": "solve"}),
        encoding="utf-8",
    )

    result = run_and_validate_task_file(task_path, base_dir=tmp_path)

    assert result["status"] == "ENVIRONMENT_HARNESS_PIPELINE_READY"
    assert result["run"]["status"] == "ENVIRONMENT_HARNESS_READY"
    assert result["validation"]["status"] == "ENVIRONMENT_HARNESS_VALID"
    assert result["metadata"]["public_safe"] is True


def test_environment_harness_rejects_invalid_loaded_input():
    with pytest.raises(ValueError, match="TASK_LOADER_READY"):
        run_loaded_task({"status": "BROKEN_TASK"})
