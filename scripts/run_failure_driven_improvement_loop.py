from hbce_arc_agi3.failure_driven_improvement_loop import (
    run_failure_driven_improvement_pipeline,
    write_failure_driven_improvement_artifacts,
)


def main() -> None:
    payload = run_failure_driven_improvement_pipeline()
    artifacts = write_failure_driven_improvement_artifacts(payload)

    print(payload["status"])
    print(payload["report_status"])
    print(payload["validation_status"])
    print(payload["improvement_loop_id"])
    print(payload["source_benchmark_id"])
    print(payload["analyzed_task_count"])
    print(payload["matching_task_count"])
    print(payload["failing_task_count"])
    print(payload["improvement_item_count"])
    print(payload["highest_priority"])
    print(payload["next_solver_target"])
    print(payload["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
