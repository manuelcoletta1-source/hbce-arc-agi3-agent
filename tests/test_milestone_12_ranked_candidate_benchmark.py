from pathlib import Path

from hbce_arc_agi3.milestone_12_ranked_candidate_benchmark import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_benchmark_case,
    build_ranked_candidate_benchmark_record,
    validate_ranked_candidate_benchmark_record,
    write_artifacts,
)


def _sample_selected_candidate():
    return {
        "ranked_candidate_id": "RANKED-C1",
        "case_id": "case_a",
        "family": "navigation_goal",
        "source_candidate_id": "C1",
        "candidate_kind": "VERIFIED_EPISODE_REPLAY",
        "actions": ["RIGHT", "DOWN"],
        "rank_within_case": 1,
        "global_rank": 1,
        "rank_score": 1052,
        "ranker_ready": True,
        "candidate_verified": True,
        "selected_for_case": True,
    }


def test_ranked_candidate_benchmark_record_is_valid():
    record = build_ranked_candidate_benchmark_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["ranked_candidate_benchmark_ready"] is True
    assert record["ranked_candidate_benchmark_valid"] is True
    assert record["ranked_candidate_benchmark_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["case_count"] == 6
    assert record["selected_candidate_count"] == 6
    assert record["benchmark_case_count"] == 6
    assert record["benchmark_pass_count"] == 6
    assert record["benchmark_warning_count"] == 0
    assert record["benchmark_failure_count"] == 0
    assert record["top_replay_candidate_count"] == 6
    assert record["measurement_target_count"] == 10
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_ranked_candidate_benchmark_record(record) == []


def test_build_benchmark_case_passes_for_verified_selected_candidate():
    case = build_benchmark_case(_sample_selected_candidate())

    assert case["benchmark_passed"] is True
    assert case["warning_count"] == 0
    assert case["failure_count"] == 0
    assert case["candidate_kind"] == "VERIFIED_EPISODE_REPLAY"


def test_build_benchmark_case_warns_for_non_replay_candidate():
    candidate = _sample_selected_candidate()
    candidate["candidate_kind"] = "PREFIX_SAFE_REPLAY"

    case = build_benchmark_case(candidate)

    assert case["benchmark_passed"] is True
    assert case["warning_count"] == 1
    assert case["failure_count"] == 0


def test_ranked_candidate_benchmark_fails_if_submission_is_sent():
    record = build_ranked_candidate_benchmark_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_ranked_candidate_benchmark_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_ranked_candidate_benchmark_fails_if_benchmark_missing():
    record = build_ranked_candidate_benchmark_record(baseline_commit="TEST-COMMIT")
    record["benchmark"] = None

    issues = validate_ranked_candidate_benchmark_record(record)

    assert "BENCHMARK_MISSING" in issues


def test_ranked_candidate_benchmark_fails_if_pass_count_mutated():
    record = build_ranked_candidate_benchmark_record(baseline_commit="TEST-COMMIT")
    record["benchmark_pass_count"] = 5

    issues = validate_ranked_candidate_benchmark_record(record)

    assert "BENCHMARK_PASS_COUNT_MISMATCH" in issues


def test_ranked_candidate_benchmark_artifacts_are_written(tmp_path: Path):
    record = build_ranked_candidate_benchmark_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-ranked-candidate-benchmark-v1.json" in written_files
    assert "milestone-12-ranked-candidate-benchmark-index-v1.json" in written_files
    assert "milestone-12-ranked-candidate-benchmark-manifest-v1.txt" in written_files
    assert "milestone-12-ranked-candidate-benchmark-v1.md" in written_files
