import json
from pathlib import Path

import pytest

from hbce_arc_agi3.planner_strategy import (
    build_strategy_from_grid_payload,
    select_planner_strategy,
    validate_planner_strategy,
)
from hbce_arc_agi3.rule_hypothesis import generate_rule_hypotheses
from hbce_arc_agi3.task_loader import load_task_file


def test_planner_strategy_selects_highest_confidence_hypothesis():
    payload = {
        "id": "strategy-demo",
        "grid": [
            [1, 0, 1],
            [2, 0, 2],
        ],
    }

    hypotheses = generate_rule_hypotheses(payload)
    strategy = select_planner_strategy(hypotheses)
    validation = validate_planner_strategy(strategy)

    assert strategy.status == "PLANNER_STRATEGY_READY"
    assert validation["status"] == "PLANNER_STRATEGY_VALID"
    assert strategy.task_id == "strategy-demo"
    assert strategy.selected_rule_type == "horizontal_symmetry_candidate"
    assert strategy.selected_action == "evaluate_horizontal_mirror"
    assert strategy.confidence == 0.65
    assert strategy.ranked_hypotheses[0]["selected"] is True


def test_planner_strategy_is_deterministic():
    payload = {
        "id": "stable-strategy",
        "grid": [
            [0, 4, 4],
            [0, 0, 4],
            [5, 0, 0],
        ],
    }

    first = build_strategy_from_grid_payload(payload)
    second = build_strategy_from_grid_payload(payload)

    assert first == second
    assert first["planner_strategy"]["metadata"]["strategy_signature"] == second["planner_strategy"]["metadata"]["strategy_signature"]


def test_planner_strategy_pipeline_from_grid_payload():
    payload = {
        "id": "pipeline-strategy",
        "grid": [
            [1, 0, 2, 2],
            [1, 0, 0, 2],
            [0, 3, 3, 0],
        ],
    }

    result = build_strategy_from_grid_payload(payload)

    assert result["status"] == "PLANNER_STRATEGY_PIPELINE_READY"
    assert result["object_model"]["status"] == "OBJECT_MODEL_READY"
    assert result["rule_hypotheses"]["status"] == "RULE_HYPOTHESIS_READY"
    assert result["planner_strategy"]["status"] == "PLANNER_STRATEGY_READY"
    assert result["validation"]["status"] == "PLANNER_STRATEGY_VALID"


def test_planner_strategy_accepts_loaded_task_payload(tmp_path: Path):
    task_path = tmp_path / "strategy-task.json"
    task_path.write_text(
        json.dumps({"id": "loaded-strategy", "grid": [[1, 0], [1, 2]], "goal": "solve"}),
        encoding="utf-8",
    )

    loaded = load_task_file(task_path, base_dir=tmp_path)
    result = build_strategy_from_grid_payload(loaded.to_dict())

    assert result["status"] == "PLANNER_STRATEGY_PIPELINE_READY"
    assert result["planner_strategy"]["status"] == "PLANNER_STRATEGY_READY"
    assert result["planner_strategy"]["metadata"]["uses_rule_hypothesis"] is True
    assert result["planner_strategy"]["metadata"]["uses_object_model"] is True


def test_planner_strategy_rejects_invalid_hypothesis_payload():
    with pytest.raises(ValueError, match="valid RULE_HYPOTHESIS_READY"):
        select_planner_strategy({"status": "BROKEN", "hypotheses": []})


def test_planner_strategy_validation_rejects_broken_contract():
    validation = validate_planner_strategy(
        {
            "status": "BROKEN",
            "strategy_id": "",
            "metadata": {},
        }
    )

    assert validation["status"] == "PLANNER_STRATEGY_INVALID"
    assert validation["valid"] is False
