from __future__ import annotations

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_proposal import (
    TASK_NAME,
    build_candidate_generator_implementation_proposal,
    write_artifacts,
)


def main() -> None:
    data = build_candidate_generator_implementation_proposal()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_commit"])
    print(data["previous_signature"])
    print(data["source_decision_gate_review_signature"])
    print(data["proposal_scope"])
    print(data["verdict"])
    print(data["next_stage"])
    print(f"milestone_18_name={data['milestone_18_name']}")
    print(f"previous_task={data['previous_task']}")
    print(f"previous_commit={data['previous_commit']}")
    print(f"previous_signature={data['previous_signature']}")
    print(f"source_decision_gate_review_task={data['source_decision_gate_review_task']}")
    print(f"source_decision_gate_review_id={data['source_decision_gate_review_id']}")
    print(f"source_decision_gate_review_signature={data['source_decision_gate_review_signature']}")
    print(f"implementation_proposal_ready={data['implementation_proposal_ready']}")
    print(f"implementation_proposal_created={data['implementation_proposal_created']}")
    print(f"implementation_proposal_review_required={data['implementation_proposal_review_required']}")
    print(f"implementation_code_authorized={data['implementation_code_authorized']}")
    print(f"implementation_allowed_now={data['implementation_allowed_now']}")
    print(f"implementation_authorization_scope={data['implementation_authorization_scope']}")
    print(f"operator_authorization_required={data['operator_authorization_required']}")
    print(f"operator_authorization_received={data['operator_authorization_received']}")
    print(f"proposal_item_count={data['proposal_item_count']}")
    print(f"blocking_issue_count={data['blocking_issue_count']}")
    print(f"acceptance_gate_count={data['acceptance_gate_count']}")
    print(f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}")

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for item in data["proposal_items"]:
        print(
            "proposal_item="
            f"{item['proposal_id']}|"
            f"{item['source_review_item']}|"
            f"{item['source_improvement_item']}|"
            f"{item['source_limitation_id']}|"
            f"{item['proposal_area']}|"
            f"{item['proposal_kind']}|"
            f"{item['implementation_scope']}|"
            f"proposal_review_required={item['proposal_review_required']}|"
            f"implementation_code_authorized={item['implementation_code_authorized']}|"
            f"runtime_execution_authorized={item['runtime_execution_authorized']}|"
            f"real_submission_authorized={item['real_submission_authorized']}"
        )

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
