from hbce_arc_agi3.report_index_generator import (
    generate_and_validate_report_index,
    write_report_index_artifacts,
)


def main() -> None:
    result = generate_and_validate_report_index()
    index = result["report_index"]
    validation = result["validation"]
    artifacts = write_report_index_artifacts(index)

    print(result["status"])
    print(index["status"])
    print(validation["status"])
    print(index["index_status"])
    print(index["report_index_id"])
    print(index["indexed_report_count"])
    print(index["indexed_artifact_count"])
    print(index["ready_report_count"])
    print(index["source_chain_ids"]["dataset_sample_registry_id"])
    print(index["source_chain_ids"]["batch_id"])
    print(index["source_chain_ids"]["multi_task_outcome_aggregate_id"])
    print(index["source_chain_ids"]["strategy_selection_index_id"])
    print(index["source_chain_ids"]["failure_taxonomy_report_id"])
    print(index["source_chain_ids"]["selected_strategy_id"])
    print(index["source_chain_ids"]["primary_failure_class"])
    print(index["source_chain_ids"]["severity_band"])
    print(index["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(index["metadata"])


if __name__ == "__main__":
    main()
