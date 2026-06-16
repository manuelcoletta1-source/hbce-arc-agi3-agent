from pathlib import Path

from hbce_arc_agi3.milestone_12_public_overfit_guard import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_guard_case,
    build_public_overfit_guard_record,
    validate_public_overfit_guard_record,
    write_artifacts,
)


def _sample_benchmark_case():
    return {
        "benchmark_case_id": "BENCHMARK-CASE-1",
        "case_id": "case_a",
        "family": "navigation_goal",
        "source_ranked_candidate_id": "RANKED-C1",
        "source_candidate_id": "C1",
        "candidate_kind": "VERIFIED_EPISODE_REPLAY",
        "rank_score": 1052,
        "actions": ["RIGHT", "DOWN"],
        "action_count": 2,
        "benchmark_passed": True,
        "warning_count": 0,
        "failure_count": 0,
        "score_claim": None,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
    }


def test_public_overfit_guard_record_is_valid():
    record = build_public_overfit_guard_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["public_overfit_guard_ready"] is True
    assert record["public_overfit_guard_valid"] is True
    assert record["public_overfit_guard_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["source_benchmark_case_count"] == 6
    assert record["guard_case_count"] == 6
    assert record["guard_pass_count"] == 6
    assert record["guard_failure_count"] == 0
    assert record["public_overfit_violation_count"] == 0
    assert record["forbidden_field_hit_count"] == 0
    assert record["forbidden_text_hit_count"] == 0
    assert record["score_claim_violation_count"] == 0
    assert record["submission_violation_count"] == 0
    assert record["boundary_violation_count"] == 0
    assert record["measurement_target_count"] == 10
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_public_overfit_guard_record(record) == []


def test_build_guard_case_passes_for_action_only_case():
    guard_case = build_guard_case(_sample_benchmark_case())

    assert guard_case["guard_passed"] is True
    assert guard_case["failure_count"] == 0
    assert guard_case["field_hits"] == []
    assert guard_case["text_hits"] == []


def test_build_guard_case_blocks_for_expected_output_field():
    case = _sample_benchmark_case()
    case["expected_output"] = [[1, 2], [3, 4]]

    guard_case = build_guard_case(case)

    assert guard_case["guard_passed"] is False
    assert guard_case["public_overfit_violation"] is True
    assert "expected_output" in guard_case["field_hits"]


def test_build_guard_case_blocks_for_score_claim():
    case = _sample_benchmark_case()
    case["score_claim"] = 0.42

    guard_case = build_guard_case(case)

    assert guard_case["guard_passed"] is False
    assert guard_case["score_claim_violation"] is True


def test_public_overfit_guard_fails_if_submission_sent():
    record = build_public_overfit_guard_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_public_overfit_guard_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_public_overfit_guard_fails_if_violation_count_mutated():
    record = build_public_overfit_guard_record(baseline_commit="TEST-COMMIT")
    record["public_overfit_violation_count"] = 1

    issues = validate_public_overfit_guard_record(record)

    assert "PUBLIC_OVERFIT_VIOLATION_COUNT_MISMATCH" in issues


def test_public_overfit_guard_artifacts_are_written(tmp_path: Path):
    record = build_public_overfit_guard_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-public-overfit-guard-v1.json" in written_files
    assert "milestone-12-public-overfit-guard-index-v1.json" in written_files
    assert "milestone-12-public-overfit-guard-manifest-v1.txt" in written_files
    assert "milestone-12-public-overfit-guard-v1.md" in written_files
