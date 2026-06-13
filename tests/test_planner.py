from hbce_arc_agi3.observer import observe_agent_state
from hbce_arc_agi3.planner import build_plan, plan_from_world_model
from hbce_arc_agi3.task_adapter import normalize_task
from hbce_arc_agi3.trace_schema import build_agent_trace, validate_trace_dict
from hbce_arc_agi3.world_model import build_world_model_from_observation


def _world_from_grid(grid):
    task = normalize_task({"id": "planner-demo", "grid": grid, "goal": "solve"})
    observation = observe_agent_state(task.to_agent_state())
    return task, observation, build_world_model_from_observation(observation.to_dict())


def test_planner_generates_candidate_actions_from_world_model():
    task, _observation, world_model = _world_from_grid([[1, 0], [2, 2]])
    plan = plan_from_world_model(world_model.to_dict(), goal=task.goal_hint)

    assert plan.status == "PLANNER_READY"
    assert plan.task_id == "planner-demo"
    assert plan.goal == "solve"
    assert len(plan.candidate_actions) >= 2
    assert plan.selected_action.action_type == "preserve_non_empty_structure"
    assert plan.metadata["public_safe"] is True
    assert plan.metadata["deterministic"] is True


def test_planner_empty_grid_uses_safe_noop():
    task, _observation, world_model = _world_from_grid([])
    plan = plan_from_world_model(world_model.to_dict(), goal=task.goal_hint)

    assert plan.status == "PLANNER_READY"
    assert plan.selected_action.action_type == "noop"
    assert plan.selected_action.payload["reason"] == "empty_or_unknown_grid"


def test_planner_trace_chain_is_valid():
    task, observation, world_model = _world_from_grid([[1]])
    plan = build_plan(world_model.to_dict(), goal=task.goal_hint)

    trace = build_agent_trace(
        task_id=task.task_id,
        observation=observation.to_dict(),
        model=world_model.to_dict(),
        goal=task.goal_hint,
        plan=plan,
        action=plan["selected_action"],
        verification={"verified": True, "reason": "planner_baseline_output_valid"},
        score={"score": 1.0, "reason": "baseline_trace_chain_valid"},
    )

    result = validate_trace_dict(trace.to_dict())

    assert result["status"] == "TRACE_SCHEMA_VALID"
    assert plan["status"] == "PLANNER_READY"
    assert plan["metadata"]["source"] == "planner_baseline_v1"
