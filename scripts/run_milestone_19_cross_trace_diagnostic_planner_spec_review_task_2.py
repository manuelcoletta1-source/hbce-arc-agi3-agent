from __future__ import annotations

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_spec_review_task_2 import (
    TASK_NAME,
    build_cross_trace_diagnostic_planner_spec_review,
    write_artifacts,
)


def main() -> None:
    data = build_cross_trace_diagnostic_planner_spec_review()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_commit"])
    print(data["previous_signature"])
    print(data["source_planning_intake_signature"])
    print(data["review_scope"])
    print(data["verdict"])
    print(data["next_stage"])

    for key in (
        "milestone_19_name",
        "previous_task",
        "previous_commit",
        "previous_signature",
        "source_planning_intake_task",
        "source_planning_intake_id",
        "source_planning_intake_signature",
        "spec_review_ready",
        "spec_review_passed",
        "planning_intake_confirmed",
        "implementation_gate_required",
        "implementation_gate_created",
        "implementation_authorized",
        "runtime_activation_performed",
        "runtime_solver_modified",
        "real_evaluation_performed",
        "kaggle_submission_sent",
        "operator_approval_required",
        "operator_approval_received",
        "review_item_count",
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

    for item in data["review_items"]:
        print(
            "spec_review_item="
            f"{item['review_id']}|"
            f"{item['review_area']}|"
            f"{item['review_status']}|"
            f"implementation_authorized={item.get('implementation_authorized', False)}|"
            f"blocking_issue={item['blocking_issue']}"
        )

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
