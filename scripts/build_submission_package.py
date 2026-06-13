from hbce_arc_agi3.observer import observe_agent_state
from hbce_arc_agi3.planner import build_plan
from hbce_arc_agi3.scoring import verify_and_score_plan
from hbce_arc_agi3.submission_package import build_public_submission_package_from_pipeline
from hbce_arc_agi3.task_adapter import normalize_task
from hbce_arc_agi3.trace_schema import build_agent_trace
from hbce_arc_agi3.world_model import build_world_model_from_observation


def main() -> None:
    task = normalize_task(
        {
            "id": "submission-package-smoke",
            "grid": [[1, 0], [2, 2]],
            "goal": "solve",
        }
    )

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

    result = build_public_submission_package_from_pipeline(
        task_id=task.task_id,
        trace=trace.to_dict(),
        verification_scoring=verification_scoring,
    )

    print(result["status"])
    print(result["package"]["status"])
    print(result["validation"]["status"])
    print(result["package"]["package_id"])
    print(result["package"]["metadata"])


if __name__ == "__main__":
    main()
