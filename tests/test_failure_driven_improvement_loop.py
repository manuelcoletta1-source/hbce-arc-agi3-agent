from hbce_arc_agi3.failure_driven_improvement_loop import (
    classify_failure,
    load_expanded_batch_benchmark_payload,
    run_failure_driven_improvement_loop,
    run_failure_driven_improvement_pipeline,
    validate_failure_driven_improvement_report,
)


def test_load_expanded_batch_benchmark_payload():
    payload = load_expanded_batch_benchmark_payload()

    assert payload["status"] == "EXPANDED_BATCH_BENCHMARK_PIPELINE_READY"
    assert payload["benchmark_status"] == "EXPANDED_BATCH_BENCHMARK_READY"
    assert payload["validation_status"] == "EXPANDED_BATCH_BENCHMARK_VALID"


def test_classify_color_only_overranked_by_combined_candidate():
    task_result = {
        "task_family": "color_transform",
        "best_candidate_type": "COLOR_SHAPE_COMBINED",
        "expected_best_available": True,
        "best_candidate_matches_expected": False,
    }

    classification = classify_failure(task_result)

    assert classification["failure_type"] == "COLOR_ONLY_TASK_OVERRANKED_BY_COMBINED_CANDIDATE"
    assert classification["target_module"] == "candidate_ranker.py"
    assert classification["priority"] == "HIGH"


def test_run_failure_driven_improvement_loop_ready():
    report = run_failure_driven_improvement_loop()

    assert report.status == "FAILURE_DRIVEN_IMPROVEMENT_LOOP_READY"
    assert report.analyzed_task_count >= 3
    assert report.failing_task_count >= 1
    assert report.improvement_item_count >= 1
    assert report.highest_priority == "HIGH"
    assert report.next_solver_target == "candidate_ranker.py"
    assert report.metadata["uses_expanded_batch_benchmark_v2"] is True
    assert report.metadata["failure_driven_solver_improvement"] is True
    assert report.metadata["external_api_dependency"] is False
    assert report.metadata["kaggle_submission_sent"] is False


def test_validate_failure_driven_improvement_report_valid():
    report = run_failure_driven_improvement_loop()
    validation = validate_failure_driven_improvement_report(report)

    assert validation["status"] == "FAILURE_DRIVEN_IMPROVEMENT_LOOP_VALID"
    assert validation["valid"] is True
    assert validation["errors"] == []


def test_failure_driven_improvement_pipeline_ready():
    payload = run_failure_driven_improvement_pipeline()

    assert payload["status"] == "FAILURE_DRIVEN_IMPROVEMENT_PIPELINE_READY"
    assert payload["report_status"] == "FAILURE_DRIVEN_IMPROVEMENT_LOOP_READY"
    assert payload["validation_status"] == "FAILURE_DRIVEN_IMPROVEMENT_LOOP_VALID"
    assert payload["improvement_item_count"] >= 1
    assert payload["highest_priority"] == "HIGH"
    assert payload["next_solver_target"] == "candidate_ranker.py"
    assert payload["metadata"]["public_safe"] is True
    assert payload["metadata"]["local_only"] is True
    assert payload["metadata"]["dry_run_only"] is True
    assert payload["metadata"]["legal_certification"] is False
