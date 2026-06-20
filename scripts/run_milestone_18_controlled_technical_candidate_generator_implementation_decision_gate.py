from __future__ import annotations

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_decision_gate import (
    TASK_NAME,
    build_candidate_generator_implementation_decision_gate,
    write_artifacts,
)


def main() -> None:
    data = build_candidate_generator_implementation_decision_gate()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_commit"])
    print(data["previous_signature"])
    print(data["source_gate_review_signature"])
    print(data["decision_scope"])
    print(data["verdict"])
    print(data["next_stage"])
    print(f"milestone_18_name={data['milestone_18_name']}")
    print(f"previous_task={data['previous_task']}")
    print(f"previous_commit={data['previous_commit']}")
    print(f"previous_signature={data['previous_signature']}")
    print(f"source_gate_review_task={data['source_gate_review_task']}")
    print(f"source_gate_review_id={data['source_gate_review_id']}")
    print(f"source_gate_review_signature={data['source_gate_review_signature']}")
    print(f"decision_gate_ready={data['decision_gate_ready']}")
    print(f"decision_gate_created={data['decision_gate_created']}")
    print(f"decision_gate_locked={data['decision_gate_locked']}")
    print(f"decision_gate_review_required={data['decision_gate_review_required']}")
    print(f"decision_gate_passed={data['decision_gate_passed']}")
    print(f"decision_gate_value={data['decision_gate_value']}")
    print(f"implementation_proposal_review_allowed_next={data['implementation_proposal_review_allowed_next']}")
    print(f"implementation_code_authorized={data['implementation_code_authorized']}")
    print(f"implementation_allowed_now={data['implementation_allowed_now']}")
    print(f"implementation_authorization_scope={data['implementation_authorization_scope']}")
    print(f"operator_authorization_required={data['operator_authorization_required']}")
    print(f"operator_authorization_received={data['operator_authorization_received']}")
    print(f"decision_item_count={data['decision_item_count']}")
    print(f"blocking_issue_count={data['blocking_issue_count']}")
    print(f"acceptance_gate_count={data['acceptance_gate_count']}")
    print(f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}")

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for item in data["decision_items"]:
        print(
            "decision_item="
            f"{item['decision_id']}|"
            f"{item['source_gate_review_item']}|"
            f"{item['source_improvement_item']}|"
            f"{item['source_limitation_id']}|"
            f"{item['decision_area']}|"
            f"{item['decision_value']}|"
            f"{item['decision_effect']}|"
            f"implementation_code_authorized={item['implementation_code_authorized']}|"
            f"runtime_execution_authorized={item['runtime_execution_authorized']}|"
            f"real_submission_authorized={item['real_submission_authorized']}"
        )

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
