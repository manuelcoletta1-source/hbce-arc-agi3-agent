from __future__ import annotations

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_improvement_map_review import (
    TASK_NAME,
    build_candidate_generator_improvement_map_review,
    write_artifacts,
)


def main() -> None:
    data = build_candidate_generator_improvement_map_review()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_commit"])
    print(data["previous_signature"])
    print(data["source_map_signature"])
    print(data["review_scope"])
    print(data["verdict"])
    print(data["next_stage"])
    print(f"milestone_18_name={data['milestone_18_name']}")
    print(f"previous_task={data['previous_task']}")
    print(f"previous_commit={data['previous_commit']}")
    print(f"previous_signature={data['previous_signature']}")
    print(f"source_map_task={data['source_map_task']}")
    print(f"source_map_id={data['source_map_id']}")
    print(f"source_map_signature={data['source_map_signature']}")
    print(f"review_item_count={data['review_item_count']}")
    print(f"confirmed_item_count={data['confirmed_item_count']}")
    print(f"blocking_issue_count={data['blocking_issue_count']}")
    print(f"acceptance_gate_count={data['acceptance_gate_count']}")
    print(f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}")

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for item in data["review_items"]:
        print(
            "review_item="
            f"{item['review_id']}|"
            f"{item['source_item_id']}|"
            f"{item['source_limitation_id']}|"
            f"{item['improvement_area']}|"
            f"{item['review_decision']}|"
            f"blocking_issue={item['blocking_issue']}|"
            f"implementation_authorized={item['implementation_authorized']}|"
            f"runtime_execution_authorized={item['runtime_execution_authorized']}"
        )

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
