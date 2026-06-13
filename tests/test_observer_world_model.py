from hbce_arc_agi3.observer import observe_agent_state, observe_task
from hbce_arc_agi3.task_adapter import normalize_task
from hbce_arc_agi3.trace_schema import build_agent_trace, validate_trace_dict
from hbce_arc_agi3.world_model import (
    build_symbolic_world_model,
    build_world_model_from_observation,
)


def test_observer_extracts_grid_features_from_agent_state():
    task = normalize_task(
        {
            "id": "observer-demo",
            "grid": [[1, 0], [2, 2]],
            "objects": [{"id": "obj-1", "kind": "symbol"}],
            "goal": "solve",
        }
    )

    observation = observe_agent_state(task.to_agent_state())

    assert observation.status == "OBSERVER_READY"
    assert observation.task_id == "observer-demo"
    assert observation.width == 2
    assert observation.height == 2
    assert observation.cell_count == 4
    assert observation.symbols == {"0": 1, "1": 1, "2": 2}
    assert len(observation.non_empty_cells) == 3
    assert observation.metadata["public_safe"] is True


def test_world_model_derives_symbolic_properties():
    task = normalize_task({"id": "world-demo", "input": [[0, 3], [0, 0]], "objective": "solve"})
    observation = observe_agent_state(task.to_agent_state())
    model = build_world_model_from_observation(observation.to_dict())

    assert model.status == "WORLD_MODEL_READY"
    assert model.task_id == "world-demo"
    assert model.dimensions == {"width": 2, "height": 2, "cell_count": 4}
    assert model.symbol_inventory == {"0": 3, "3": 1}
    assert model.non_empty_cell_count == 1
    assert model.density == 0.25
    assert "GRID_DIMENSIONS_KNOWN" in model.inferred_properties
    assert "SYMBOL_INVENTORY_READY" in model.inferred_properties


def test_observer_world_model_trace_chain_is_public_safe():
    task = normalize_task({"id": "chain-demo", "grid": [[1]], "goal": "solve"})
    observation = observe_task(task.to_agent_state())
    world_model = build_symbolic_world_model(observation)

    trace = build_agent_trace(
        task_id=task.task_id,
        observation=observation,
        model=world_model,
        goal=task.goal_hint,
        plan={"candidate_actions": ["noop"]},
        action={"type": "noop"},
        verification={"verified": True},
        score={"score": 1.0},
    )

    result = validate_trace_dict(trace.to_dict())

    assert result["status"] == "TRACE_SCHEMA_VALID"
    assert trace.metadata["public_safe"] is True
    assert world_model["metadata"]["public_safe"] is True
    assert observation["metadata"]["public_safe"] is True
