from hbce_arc_agi3.strategy_selection_index import (
    generate_and_validate_strategy_selection_index,
    write_strategy_selection_index_artifacts,
)


def main() -> None:
    result = generate_and_validate_strategy_selection_index()
    index = result["strategy_selection_index"]
    validation = result["validation"]
    artifacts = write_strategy_selection_index_artifacts(index)

    print(result["status"])
    print(index["status"])
    print(validation["status"])
    print(index["index_status"])
    print(index["index_id"])
    print(index["aggregate_id"])
    print(index["batch_id"])
    print(index["registry_id"])
    print(index["candidate_count"])
    print(index["selected_strategy_id"])
    print(index["selected_strategy_name"])
    print(index["selected_score"])
    print(index["selected_quality_band"])
    print(index["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(index["metadata"])


if __name__ == "__main__":
    main()
