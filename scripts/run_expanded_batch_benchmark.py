from hbce_arc_agi3.expanded_batch_benchmark import (
    run_expanded_batch_benchmark_pipeline,
    write_expanded_batch_benchmark_artifacts,
)


def main() -> None:
    payload = run_expanded_batch_benchmark_pipeline()
    artifacts = write_expanded_batch_benchmark_artifacts(payload)

    print(payload["status"])
    print(payload["benchmark_status"])
    print(payload["validation_status"])
    print(payload["benchmark_id"])
    print(payload["task_count"])
    print(payload["tasks_processed"])
    print(payload["candidate_generation_success_rate"])
    print(payload["ranking_success_rate"])
    print(payload["best_candidate_match_rate"])
    print(payload["average_best_score"])
    print(payload["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
