import json
from pathlib import Path

from hbce_arc_agi3.object_model import build_object_model
from hbce_arc_agi3.rule_hypothesis import (
    generate_rule_hypotheses,
    validate_rule_hypothesis_set,
)
from hbce_arc_agi3.task_loader import load_task_file


def test_rule_hypothesis_generates_candidate_rules_from_grid():
    payload = {
        "id": "rules-demo",
        "grid": [
            [1, 0, 2, 2],
            [1, 0, 0, 2],
            [0, 3, 3, 0],
        ],
    }

    hypotheses = generate_rule_hypotheses(payload)
    validation = validate_rule_hypothesis_set(hypotheses)

    rule_types = [hypothesis.rule_type for hypothesis in hypotheses.hypotheses]

    assert hypotheses.status == "RULE_HYPOTHESIS_READY"
    assert validation["status"] == "RULE_HYPOTHESIS_VALID"
    assert hypotheses.task_id == "rules-demo"
    assert "preserve_structure" in rule_types
    assert "object_count_invariant" in rule_types
    assert "dominant_value_focus" in rule_types
    assert "horizontal_symmetry_candidate" in rule_types
    assert "vertical_symmetry_candidate" in rule_types
    assert "largest_object_anchor" in rule_types


def test_rule_hypothesis_is_deterministic():
    payload = {
        "id": "stable-rules",
        "grid": [
            [0, 4, 4],
            [0, 0, 4],
            [5, 0, 0],
        ],
    }

    first = generate_rule_hypotheses(payload)
    second = generate_rule_hypotheses(payload)

    assert first.to_dict() == second.to_dict()
    assert first.metadata["signature"] == second.metadata["signature"]


def test_rule_hypothesis_accepts_object_model_payload():
    model = build_object_model(
        {
            "id": "object-model-rules",
            "grid": [
                [1, 1, 0],
                [0, 2, 2],
            ],
        }
    )

    hypotheses = generate_rule_hypotheses(model)

    assert hypotheses.status == "RULE_HYPOTHESIS_READY"
    assert hypotheses.object_model_signature == model.signature
    assert hypotheses.metadata["executes_dataset_code"] is False


def test_rule_hypothesis_accepts_loaded_task_payload(tmp_path: Path):
    task_path = tmp_path / "rules-task.json"
    task_path.write_text(
        json.dumps({"id": "loaded-rules", "grid": [[1, 0], [1, 2]], "goal": "solve"}),
        encoding="utf-8",
    )

    loaded = load_task_file(task_path, base_dir=tmp_path)
    hypotheses = generate_rule_hypotheses(loaded.to_dict())

    assert hypotheses.status == "RULE_HYPOTHESIS_READY"
    assert hypotheses.task_id == "loaded-rules"
    assert hypotheses.hypothesis_count >= 4


def test_rule_hypothesis_detects_symmetry_confidence():
    payload = {
        "id": "symmetric-rules",
        "grid": [
            [1, 0, 1],
            [2, 0, 2],
        ],
    }

    hypotheses = generate_rule_hypotheses(payload)
    horizontal = [
        hypothesis
        for hypothesis in hypotheses.hypotheses
        if hypothesis.rule_type == "horizontal_symmetry_candidate"
    ][0]

    assert horizontal.evidence["horizontal_symmetric"] is True
    assert horizontal.confidence == 0.65


def test_rule_hypothesis_validation_rejects_broken_contract():
    validation = validate_rule_hypothesis_set(
        {
            "status": "BROKEN",
            "hypothesis_count": 1,
            "hypotheses": [],
            "metadata": {},
        }
    )

    assert validation["status"] == "RULE_HYPOTHESIS_INVALID"
    assert validation["valid"] is False
