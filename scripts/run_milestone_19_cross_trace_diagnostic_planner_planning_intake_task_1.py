from __future__ import annotations

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    TASK_NAME,
    build_cross_trace_diagnostic_planner_planning_intake,
    write_artifacts,
)


def main() -> None:
    data = build_cross_trace_diagnostic_planner_planning_intake()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_milestone_closure_commit"])
    print(data["previous_milestone_closure_signature"])
    print(data["implementation_status"])
    print(data["verdict"])
    print(data["next_stage"])

    for key in (
        "milestone_19_name",
        "previous_milestone",
        "previous_milestone_closure_commit",
        "previous_milestone_closure_signature",
        "planning_artifact_ready",
        "planning_artifact_source",
        "planning_scope",
        "implementation_status",
        "closure_status",
        "acceptance_gate_count",
        "acceptance_gate_failure_count",
    ):
        print(f"{key}={data[key]}")

    print(f"pipeline_model={list(data['pipeline_model'])}")
    print(f"feature_families={list(data['feature_families'])}")
    print(f"required_output_fields={list(data['required_output_fields'])}")

    for test in data["test_plan"]:
        print(
            "test_plan_item="
            f"{test['test_id']}|{test['objective']}|{test['pass_condition']}"
        )

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
