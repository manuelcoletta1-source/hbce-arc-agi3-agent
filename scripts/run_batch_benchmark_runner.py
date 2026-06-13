from hbce_arc_agi3.batch_benchmark_runner import (
    generate_and_validate_batch_benchmark_run,
    write_batch_benchmark_artifacts,
)


def main() -> None:
    result = generate_and_validate_batch_benchmark_run()
    batch_run = result["batch_benchmark_run"]
    validation = result["validation"]
    artifacts = write_batch_benchmark_artifacts(batch_run)

    print(result["status"])
    print(batch_run["status"])
    print(validation["status"])
    print(batch_run["batch_status"])
    print(batch_run["batch_id"])
    print(batch_run["registry_id"])
    print(batch_run["task_count"])
    print(batch_run["matched_count"])
    print(batch_run["mismatched_count"])
    print(batch_run["average_cell_accuracy"])
    print(batch_run["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(batch_run["metadata"])


if __name__ == "__main__":
    main()
