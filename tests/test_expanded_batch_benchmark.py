from hbce_arc_agi3.expanded_batch_benchmark import (
    build_expanded_batch_benchmark_tasks,
    run_expanded_batch_benchmark,
    run_expanded_batch_benchmark_pipeline,
    validate_expanded_batch_benchmark_report,
)


def test_build_expanded_batch_benchmark_tasks_minimum_three():
    tasks = build_expanded_batch_benchmark_tasks()

    assert len(tasks) >= 3
    assert all(task.task_id.startswith("EXPANDED-BATCH-V2-") for task in tasks)
    assert all(task.train_pairs for task in tasks)
    assert all(task.test_input for task in tasks)


def test_run_expanded_batch_benchmark_ready():
    report = run_expanded_batch_benchmark()

    assert report.status == "EXPANDED_BATCH_BENCHMARK_READY"
    assert report.task_count >= 3
    assert report.tasks_processed == report.task_count
    assert report.generation_success_count == report.task_count
    assert report.ranking_success_count == report.task_count
    assert report.candidate_generation_success_rate == 1.0
    assert report.ranking_success_rate == 1.0
    assert report.average_best_score > 0.0
    assert report.metadata["uses_candidate_generator_v1"] is True
    assert report.metadata["uses_candidate_ranker_v1"] is True
    assert report.metadata["external_api_dependency"] is False
    assert report.metadata["kaggle_submission_sent"] is False
    assert report.metadata["private_core_exposure"] is False


def test_validate_expanded_batch_benchmark_report_valid():
    report = run_expanded_batch_benchmark()
    validation = validate_expanded_batch_benchmark_report(report)

    assert validation["status"] == "EXPANDED_BATCH_BENCHMARK_VALID"
    assert validation["valid"] is True
    assert validation["errors"] == []


def test_expanded_batch_benchmark_pipeline_ready():
    payload = run_expanded_batch_benchmark_pipeline()

    assert payload["status"] == "EXPANDED_BATCH_BENCHMARK_PIPELINE_READY"
    assert payload["benchmark_status"] == "EXPANDED_BATCH_BENCHMARK_READY"
    assert payload["validation_status"] == "EXPANDED_BATCH_BENCHMARK_VALID"
    assert payload["task_count"] >= 3
    assert payload["tasks_processed"] == payload["task_count"]
    assert payload["candidate_generation_success_rate"] == 1.0
    assert payload["ranking_success_rate"] == 1.0
    assert payload["average_best_score"] > 0.0
    assert payload["metadata"]["public_safe"] is True
    assert payload["metadata"]["local_only"] is True
    assert payload["metadata"]["dry_run_only"] is True
    assert payload["metadata"]["legal_certification"] is False
