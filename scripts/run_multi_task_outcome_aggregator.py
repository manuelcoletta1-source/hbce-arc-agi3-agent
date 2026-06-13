from hbce_arc_agi3.multi_task_outcome_aggregator import (
    generate_and_validate_multi_task_outcome_aggregate,
    write_multi_task_outcome_artifacts,
)


def main() -> None:
    result = generate_and_validate_multi_task_outcome_aggregate()
    aggregate = result["multi_task_outcome_aggregate"]
    validation = result["validation"]
    artifacts = write_multi_task_outcome_artifacts(aggregate)

    print(result["status"])
    print(aggregate["status"])
    print(validation["status"])
    print(aggregate["aggregate_status"])
    print(aggregate["aggregate_id"])
    print(aggregate["batch_id"])
    print(aggregate["registry_id"])
    print(aggregate["task_count"])
    print(aggregate["matched_count"])
    print(aggregate["partial_count"])
    print(aggregate["failed_count"])
    print(aggregate["unverified_count"])
    print(aggregate["average_cell_accuracy"])
    print(aggregate["average_calibrated_score"])
    print(aggregate["exact_match_rate"])
    print(aggregate["aggregate_quality_band"])
    print(aggregate["aggregate_verdict"])
    print(aggregate["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(aggregate["metadata"])


if __name__ == "__main__":
    main()
