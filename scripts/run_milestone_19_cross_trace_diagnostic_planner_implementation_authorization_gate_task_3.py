from __future__ import annotations

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_authorization_gate_task_3 import (
    TASK_NAME,
    build_cross_trace_diagnostic_planner_implementation_authorization_gate,
    write_artifacts,
)


def main() -> None:
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_commit"])
    print(data["previous_signature"])
    print(data["source_spec_review_signature"])
    print(data["gate_scope"])
    print(data["verdict"])
    print(data["next_stage"])

    for key in (
        "milestone_19_name",
        "previous_task",
        "previous_commit",
        "previous_signature",
        "source_spec_review_task",
        "source_spec_review_id",
        "source_spec_review_signature",
        "implementation_authorization_gate_ready",
        "implementation_authorization_gate_created",
        "implementation_authorization_gate_review_required",
        "implementation_authorization_gate_passed",
        "implementation_authorized",
        "implementation_authorization_received",
        "implementation_decision_selected",
        "selected_operator_decision_value",
        "operator_approval_required",
        "operator_approval_received",
        "operator_decision_required_for_implementation",
        "operator_decision_received",
        "runtime_activation_authorized",
        "runtime_activation_performed",
        "runtime_solver_modified",
        "candidate_generator_modified",
        "ranker_modified",
        "verifier_modified",
        "real_evaluation_authorized",
        "real_evaluation_performed",
        "real_submission_authorized",
        "submission_artifact_created",
        "kaggle_submission_sent",
        "internet_during_eval",
        "external_api_dependency",
        "hidden_label_accessed",
        "private_core_exposure",
        "legal_certification",
        "planning_only_until_operator_decision",
        "gate_item_count",
        "acceptance_gate_count",
        "acceptance_gate_failure_count",
    ):
        print(f"{key}={data[key]}")

    print(f"allowed_operator_decision_values={list(data['allowed_operator_decision_values'])}")
    print(f"pipeline_model={list(data['pipeline_model'])}")
    print(f"feature_families={list(data['feature_families'])}")
    print(f"required_output_fields={list(data['required_output_fields'])}")

    for item in data["gate_items"]:
        print(
            "implementation_authorization_gate_item="
            f"{item['gate_item_id']}|"
            f"{item['gate_area']}|"
            f"{item['gate_status']}|"
            f"implementation_authorized={item.get('implementation_authorized', False)}|"
            f"blocking_issue={item['blocking_issue']}"
        )

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
