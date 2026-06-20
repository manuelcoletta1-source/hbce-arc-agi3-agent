from __future__ import annotations

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_authorization_gate import (
    TASK_NAME,
    build_candidate_generator_implementation_authorization_gate,
    write_artifacts,
)


def main() -> None:
    data = build_candidate_generator_implementation_authorization_gate()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_commit"])
    print(data["previous_signature"])
    print(data["source_review_signature"])
    print(data["gate_scope"])
    print(data["verdict"])
    print(data["next_stage"])
    print(f"milestone_18_name={data['milestone_18_name']}")
    print(f"previous_task={data['previous_task']}")
    print(f"previous_commit={data['previous_commit']}")
    print(f"previous_signature={data['previous_signature']}")
    print(f"source_review_task={data['source_review_task']}")
    print(f"source_review_id={data['source_review_id']}")
    print(f"source_review_signature={data['source_review_signature']}")
    print(f"authorization_gate_ready={data['authorization_gate_ready']}")
    print(f"authorization_gate_created={data['authorization_gate_created']}")
    print(f"authorization_gate_locked={data['authorization_gate_locked']}")
    print(f"authorization_gate_open={data['authorization_gate_open']}")
    print(f"authorization_gate_review_required={data['authorization_gate_review_required']}")
    print(f"authorization_gate_passed={data['authorization_gate_passed']}")
    print(f"implementation_allowed_now={data['implementation_allowed_now']}")
    print(f"operator_authorization_required={data['operator_authorization_required']}")
    print(f"operator_authorization_received={data['operator_authorization_received']}")
    print(f"gate_condition_count={data['gate_condition_count']}")
    print(f"blocking_issue_count={data['blocking_issue_count']}")
    print(f"acceptance_gate_count={data['acceptance_gate_count']}")
    print(f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}")

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for condition in data["gate_conditions"]:
        print(
            "gate_condition="
            f"{condition['condition_id']}|"
            f"{condition['source_review_item']}|"
            f"{condition['source_improvement_item']}|"
            f"{condition['source_limitation_id']}|"
            f"{condition['gate_area']}|"
            f"{condition['gate_decision']}|"
            f"{condition['authorization_effect']}|"
            f"implementation_authorized={condition['implementation_authorized']}|"
            f"runtime_execution_authorized={condition['runtime_execution_authorized']}"
        )

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
