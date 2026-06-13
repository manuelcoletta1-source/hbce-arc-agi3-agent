from hbce_arc_agi3.observer import observe_agent_state
from hbce_arc_agi3.planner import build_plan
from hbce_arc_agi3.scoring import verify_and_score_plan
from hbce_arc_agi3.submission_package import (
    build_public_submission_package_from_pipeline,
    build_submission_package,
    validate_submission_package,
)
from hbce_arc_agi3.task_adapter import normalize_task
from hbce_arc_agi3.trace_schema import build_agent_trace, validate_trace_dict
from hbce_arc_agi3.world_model import build_world_model_from_observation


def _pipeline():
    task = normalize_task({"id": "submission-demo", "grid": [[1, 0], [2, 2]], "goal": "solve"})
    observation = observe_agent_state(task.to_agent_state())
    world = build_world_model_from_observation(observation.to_dict())
    plan = build_plan(world.to_dict(), goal=task.goal_hint)
    verification_scoring = verify_and_score_plan(plan, world.to_dict())

    trace = build_agent_trace(
        task_id=task.task_id,
        observation=observation.to_dict(),
        model=world.to_dict(),
        goal=task.goal_hint,
        plan=plan,
        action=plan["selected_action"],
        verification=verification_scoring["verification"],
        score=verification_scoring["score"],
    )

    return task, trace, verification_scoring


def test_submission_package_contract_is_ready():
    task, trace, verification_scoring = _pipeline()

    package = build_submission_package(
        task_id=task.task_id,
        trace=trace.to_dict(),
        verification=verification_scoring["verification"],
        score=verification_scoring["score"],
    )

    data = package.to_dict()

    assert data["status"] == "SUBMISSION_PACKAGE_READY"
    assert data["package_id"].startswith("ARC-SUBMISSION-")
    assert data["metadata"]["public_safe"] is True
    assert data["metadata"]["external_api_dependency"] is False
    assert data["metadata"]["kaggle_submission_sent"] is False
    assert data["metadata"]["contains_api_keys"] is False


def test_submission_package_validation_passes():
    task, trace, verification_scoring = _pipeline()

    package = build_submission_package(
        task_id=task.task_id,
        trace=trace.to_dict(),
        verification=verification_scoring["verification"],
        score=verification_scoring["score"],
    )
    validation = validate_submission_package(package)

    assert validation["status"] == "SUBMISSION_PACKAGE_VALID"
    assert validation["valid"] is True
    assert validation["checks"]["required_agent_source_artifact"] is True
    assert validation["checks"]["contains_no_private_runtime"] is True


def test_public_submission_package_pipeline_is_trace_compatible():
    task, trace, verification_scoring = _pipeline()

    result = build_public_submission_package_from_pipeline(
        task_id=task.task_id,
        trace=trace.to_dict(),
        verification_scoring=verification_scoring,
    )

    trace_validation = validate_trace_dict(trace.to_dict())

    assert result["status"] == "PUBLIC_SUBMISSION_PACKAGE_SKELETON_READY"
    assert result["package"]["status"] == "SUBMISSION_PACKAGE_READY"
    assert result["validation"]["status"] == "SUBMISSION_PACKAGE_VALID"
    assert trace_validation["status"] == "TRACE_SCHEMA_VALID"


def test_invalid_submission_package_fails_safely():
    validation = validate_submission_package(
        {
            "status": "BROKEN",
            "metadata": {
                "public_safe": False,
                "external_api_dependency": True,
                "kaggle_submission_sent": True,
            },
        }
    )

    assert validation["status"] == "SUBMISSION_PACKAGE_INVALID"
    assert validation["valid"] is False
