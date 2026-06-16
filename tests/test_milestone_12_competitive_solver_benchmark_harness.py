from pathlib import Path

from hbce_arc_agi3.milestone_12_competitive_solver_benchmark_harness import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    SYNTHETIC_BENCHMARK_CASES,
    TASK_NAME,
    TASK_VERDICT,
    build_benchmark_harness_record,
    evaluate_candidate_policy,
    evaluate_case,
    run_reference_benchmark,
    validate_benchmark_harness_record,
    write_artifacts,
)


def test_benchmark_harness_record_is_valid():
    record = build_benchmark_harness_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["milestone_12_status"] == "OPENED_CANONICALLY"
    assert record["benchmark_harness_ready"] is True
    assert record["benchmark_harness_valid"] is True
    assert record["benchmark_harness_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["benchmark_case_count"] == 6
    assert record["reference_candidate_count"] == 3
    assert record["measurement_target_count"] == 10
    assert record["benchmark"]["best_candidate_id"] == "reference_optimal_policy"
    assert record["benchmark"]["best_completion_rate"] == 1.0
    assert record["benchmark"]["best_mean_action_efficiency"] == 1.0
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_benchmark_harness_record(record) == []


def test_evaluate_case_accepts_probe_then_optimal_subsequence():
    case = SYNTHETIC_BENCHMARK_CASES[0]
    result = evaluate_case(case, ["WAIT"] + list(case["optimal_actions"]))

    assert result["completed"] is True
    assert result["candidate_action_count"] == case["minimum_action_count"] + 1
    assert result["action_efficiency"] < 1.0
    assert result["excess_action_count"] == 1


def test_reference_benchmark_ranks_optimal_policy_first():
    benchmark = run_reference_benchmark()

    assert benchmark["best_candidate_id"] == "reference_optimal_policy"
    assert benchmark["ranked_candidate_ids"][0] == "reference_optimal_policy"
    assert benchmark["best_completion_rate"] == 1.0
    assert benchmark["best_mean_action_efficiency"] == 1.0


def test_noop_policy_fails_all_cases():
    candidate_plans = {case["case_id"]: [] for case in SYNTHETIC_BENCHMARK_CASES}
    result = evaluate_candidate_policy("noop", candidate_plans)

    assert result["completion_rate"] == 0.0
    assert result["completed_case_count"] == 0
    assert result["failed_case_count"] == len(SYNTHETIC_BENCHMARK_CASES)


def test_benchmark_harness_fails_if_submission_is_allowed():
    record = build_benchmark_harness_record(baseline_commit="TEST-COMMIT")
    record["real_submission_allowed"] = True

    issues = validate_benchmark_harness_record(record)

    assert "real_submission_allowed_NOT_FALSE" in issues


def test_benchmark_harness_artifacts_are_written(tmp_path: Path):
    record = build_benchmark_harness_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-competitive-solver-benchmark-harness-v1.json" in written_files
    assert "milestone-12-competitive-solver-benchmark-harness-index-v1.json" in written_files
    assert "milestone-12-competitive-solver-benchmark-harness-manifest-v1.txt" in written_files
    assert "milestone-12-competitive-solver-benchmark-harness-v1.md" in written_files
