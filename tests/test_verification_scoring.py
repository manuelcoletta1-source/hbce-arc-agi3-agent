from hbce_arc_agi3.observer import observe_agent_state
from hbce_arc_agi3.planner import build_plan
from hbce_arc_agi3.scoring import (
    score_verified_plan,
    verify_and_score_plan,
    verify_plan_output,
)
from hbce_arc_agi3.task_adapter import normalize_task
from hbce_arc_agi3.trace_schema import build_agent_trace, validate_trace_dict
from hbce_arc_agi3.world_model import build_world_model_from_observation


def _plan_chain(grid):
    task = normalize_task({"id": "verification-demo", "grid": grid, "goal": "solve"})
    observation = observe_agent_state(task.to_agent_state())
    world_model = build_world_model_from_observation(observation.to_dict())
    plan = build_plan(world_model.to_dict(), goal=task.goal_hint)
    return task, observation, world_model, plan


def test_verify_plan_output_contract():
    _task, _observation, world_model, plan = _plan_chain([[1, 0], [2, 2]])

    verification = verify_plan_output(plan, world_model.to_dict())

    assert verification.status == "VERIFICATION_READY"
    assert verification.verified is True
    assert verification.reason == "planner_output_verified_against_world_model"
    assert verification.checks["plan_status_ready"] is True
    assert verification.checks["selected_action_in_candidates"] is True
    assert verification.metadata["public_safe"] is True


def test_score_verified_plan_contract():
    _task, _observation, world_model, plan = _plan_chain([[1, 0], [2, 2]])

    verification = verify_plan_output(plan, world_model.to_dict())
    score = score_verified_plan(verification, plan)

    assert score.status == "SCORING_READY"
    assert 0.0 <= score.score <= 1.0
    assert score.grade in {"A", "B", "C", "D"}
    assert score.components["verification_ratio"] == 1.0
    assert score.metadata["deterministic"] is True


def test_verify_and_score_trace_chain_is_valid():
    task, observation, world_model, plan = _plan_chain([[1]])

    result = verify_and_score_plan(plan, world_model.to_dict())

    trace = build_agent_trace(
        task_id=task.task_id,
        observation=observation.to_dict(),
        model=world_model.to_dict(),
        goal=task.goal_hint,
        plan=plan,
        action=plan["selected_action"],
        verification=result["verification"],
        score=result["score"],
    )

    validation = validate_trace_dict(trace.to_dict())

    assert result["status"] == "VERIFICATION_SCORING_READY"
    assert result["verification"]["verified"] is True
    assert result["score"]["status"] == "SCORING_READY"
    assert validation["status"] == "TRACE_SCHEMA_VALID"


def test_invalid_plan_gets_failed_verification_and_penalty_score():
    result = verify_and_score_plan({"status": "BROKEN_PLAN"}, {"status": "WORLD_MODEL_READY", "dimensions": {"cell_count": 1}})

    assert result["status"] == "VERIFICATION_SCORING_READY"
    assert result["verification"]["verified"] is False
    assert result["verification"]["status"] == "VERIFICATION_FAILED"
    assert result["score"]["score"] < 0.5
