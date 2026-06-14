from hbce_arc_agi3.candidate_generator import generate_candidates
from hbce_arc_agi3.candidate_ranker import rank_candidates, validate_candidate_ranking_report
from hbce_arc_agi3.expanded_batch_benchmark import (
    build_expanded_batch_benchmark_tasks,
    run_expanded_batch_benchmark,
)
from hbce_arc_agi3.failure_driven_improvement_loop import (
    run_failure_driven_improvement_loop,
    run_failure_driven_improvement_pipeline,
    validate_failure_driven_improvement_report,
)


def _color_only_task():
    return next(
        task
        for task in build_expanded_batch_benchmark_tasks()
        if task.task_id == "EXPANDED-BATCH-V2-COLOR-ONLY"
    )


def test_color_only_task_prefers_color_remap_candidate():
    task = _color_only_task()

    generation = generate_candidates(
        task.train_pairs,
        task.test_input,
        task_id=task.task_id,
        background_color=0,
    )

    ranking = rank_candidates(generation)
    data = ranking.to_dict()

    assert data["best_candidate"]["candidate_type"] == "COLOR_REMAP"
    assert data["best_candidate"]["candidate_grid"] == task.expected_best_grid
    assert data["ranking_policy"]["task_family_policy"] == "TASK_FAMILY_AWARE_v1"
    assert data["ranking_policy"]["inferred_task_family"] == "color_transform"

    validation = validate_candidate_ranking_report(ranking)

    assert validation["status"] == "CANDIDATE_RANKING_VALID"
    assert validation["valid"] is True


def test_expanded_batch_benchmark_match_rate_closes_after_ranker_policy_fix():
    report = run_expanded_batch_benchmark()

    assert report.status == "EXPANDED_BATCH_BENCHMARK_READY"
    assert report.expected_available_count == 3
    assert report.expected_match_count == 3
    assert report.best_candidate_match_rate == 1.0
    assert report.failure_reasons == ()


def test_failure_loop_has_no_active_failures_after_ranker_policy_fix():
    report = run_failure_driven_improvement_loop()
    validation = validate_failure_driven_improvement_report(report)

    assert report.status == "FAILURE_DRIVEN_IMPROVEMENT_LOOP_READY"
    assert report.failing_task_count == 0
    assert report.improvement_item_count == 0
    assert report.highest_priority == "NONE"
    assert report.next_solver_target == "none"
    assert validation["status"] == "FAILURE_DRIVEN_IMPROVEMENT_LOOP_VALID"
    assert validation["valid"] is True


def test_failure_loop_pipeline_ready_after_ranker_policy_fix():
    payload = run_failure_driven_improvement_pipeline()

    assert payload["status"] == "FAILURE_DRIVEN_IMPROVEMENT_PIPELINE_READY"
    assert payload["failing_task_count"] == 0
    assert payload["improvement_item_count"] == 0
    assert payload["highest_priority"] == "NONE"
    assert payload["next_solver_target"] == "none"
