from __future__ import annotations

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_proposal_review import (
    TASK_NAME,
    build_candidate_generator_implementation_proposal_review,
    write_artifacts,
)


def main() -> None:
    data = build_candidate_generator_implementation_proposal_review()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_commit"])
    print(data["previous_signature"])
    print(data["source_proposal_signature"])
    print(data["review_scope"])
    print(data["verdict"])
    print(data["next_stage"])
    print(f"milestone_18_name={data['milestone_18_name']}")
    print(f"previous_task={data['previous_task']}")
    print(f"previous_commit={data['previous_commit']}")
    print(f"previous_signature={data['previous_signature']}")
    print(f"source_proposal_task={data['source_proposal_task']}")
    print(f"source_proposal_id={data['source_proposal_id']}")
    print(f"source_proposal_signature={data['source_proposal_signature']}")
    print(f"implementation_proposal_review_ready={data['implementation_proposal_review_ready']}")
    print(f"implementation_proposal_review_passed={data['implementation_proposal_review_passed']}")
    print(f"implementation_proposal_confirmed={data['implementation_proposal_confirmed']}")
    print(f"authorization_review_gate_required={data['authorization_review_gate_required']}")
    print(f"authorization_review_gate_allowed_next={data['authorization_review_gate_allowed_next']}")
    print(f"implementation_code_authorized={data['implementation_code_authorized']}")
    print(f"implementation_allowed_now={data['implementation_allowed_now']}")
    print(f"implementation_authorization_scope={data['implementation_authorization_scope']}")
    print(f"operator_authorization_required={data['operator_authorization_required']}")
    print(f"operator_authorization_received={data['operator_authorization_received']}")
    print(f"review_item_count={data['review_item_count']}")
    print(f"confirmed_review_item_count={data['confirmed_review_item_count']}")
    print(f"blocking_issue_count={data['blocking_issue_count']}")
    print(f"acceptance_gate_count={data['acceptance_gate_count']}")
    print(f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}")

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for item in data["review_items"]:
        print(
            "proposal_review_item="
            f"{item['review_id']}|"
            f"{item['source_proposal_id']}|"
            f"{item['source_improvement_item']}|"
            f"{item['source_limitation_id']}|"
            f"{item['review_area']}|"
            f"{item['review_decision']}|"
            f"{item['review_effect']}|"
            f"proposal_accepted_for_next_gate={item['proposal_accepted_for_next_gate']}|"
            f"authorization_review_gate_required={item['authorization_review_gate_required']}|"
            f"implementation_code_authorized={item['implementation_code_authorized']}|"
            f"runtime_execution_authorized={item['runtime_execution_authorized']}|"
            f"real_submission_authorized={item['real_submission_authorized']}"
        )

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
