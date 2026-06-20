from __future__ import annotations

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_improvement_map import (
    TASK_NAME,
    build_candidate_generator_improvement_map,
    write_artifacts,
)


def main() -> None:
    data = build_candidate_generator_improvement_map()
    paths = write_artifacts()

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(data["status"])
    print(data["validation"])
    print(data["signature"])
    print(data["previous_commit"])
    print(data["map_scope"])
    print(data["verdict"])
    print(data["next_stage"])
    print(f"milestone_18_name={data['milestone_18_name']}")
    print(f"previous_task={data['previous_task']}")
    print(f"previous_commit={data['previous_commit']}")
    print(f"previous_signature={data['previous_signature']}")
    print(f"item_count={data['item_count']}")
    print(f"improvement_area_count={data['improvement_area_count']}")
    print(f"blocking_issue_count={data['blocking_issue_count']}")
    print(f"acceptance_gate_count={data['acceptance_gate_count']}")
    print(f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}")

    for key, value in data["boundary_controls"].items():
        print(f"{key}={value}")

    for item in data["improvement_items"]:
        print(
            "improvement_item="
            f"{item['item_id']}|"
            f"{item['source_limitation_id']}|"
            f"{item['improvement_area']}|"
            f"{item['implementation_status']}|"
            f"review_required={item['review_required_before_implementation']}|"
            f"implementation_authorized={item['implementation_authorized']}"
        )

    for artifact_type, path in paths.items():
        print(f"{artifact_type}={path}")


if __name__ == "__main__":
    main()
