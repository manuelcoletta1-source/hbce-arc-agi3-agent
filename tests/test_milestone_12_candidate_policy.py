from pathlib import Path

from hbce_arc_agi3.milestone_12_candidate_policy import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_candidate_policy_record,
    build_candidates_for_episode,
    validate_candidate_policy_record,
    write_artifacts,
)


def _sample_episode():
    return {
        "episode_id": "EPISODE-SAMPLE_CASE",
        "case_id": "sample_case",
        "family": "navigation_goal",
        "actions": ["RIGHT", "DOWN"],
        "action_count": 2,
        "verified_episode": True,
        "reusable_in_candidate_policy": True,
        "issue_count": 0,
    }


def test_candidate_policy_record_is_valid():
    record = build_candidate_policy_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["candidate_policy_ready"] is True
    assert record["candidate_policy_valid"] is True
    assert record["candidate_policy_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["case_count"] == 6
    assert record["episode_count"] == 6
    assert record["candidate_count"] == 18
    assert record["verified_candidate_count"] == 18
    assert record["replay_candidate_count"] == 6
    assert record["prefix_candidate_count"] == 6
    assert record["heuristic_candidate_count"] == 6
    assert record["ranker_ready_candidate_count"] == 18
    assert record["candidate_issue_count"] == 0
    assert record["measurement_target_count"] == 10
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_candidate_policy_record(record) == []


def test_build_candidates_for_episode_emits_three_ranker_ready_candidates():
    candidates = build_candidates_for_episode(_sample_episode())

    assert len(candidates) == 3
    assert {candidate["candidate_kind"] for candidate in candidates} == {
        "VERIFIED_EPISODE_REPLAY",
        "PREFIX_SAFE_REPLAY",
        "FAMILY_HEURISTIC_REPLAY",
    }
    assert all(candidate["ranker_ready"] is True for candidate in candidates)
    assert all(candidate["issue_count"] == 0 for candidate in candidates)


def test_prefix_candidate_uses_first_action_only():
    candidates = build_candidates_for_episode(_sample_episode())
    prefix_candidate = [
        candidate for candidate in candidates if candidate["candidate_kind"] == "PREFIX_SAFE_REPLAY"
    ][0]

    assert prefix_candidate["actions"] == ["RIGHT"]
    assert prefix_candidate["candidate_length"] == 1


def test_candidate_policy_fails_if_submission_is_sent():
    record = build_candidate_policy_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_candidate_policy_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_candidate_policy_fails_if_policy_missing():
    record = build_candidate_policy_record(baseline_commit="TEST-COMMIT")
    record["candidate_policy"] = None

    issues = validate_candidate_policy_record(record)

    assert "CANDIDATE_POLICY_MISSING" in issues


def test_candidate_policy_fails_if_candidate_count_mutated():
    record = build_candidate_policy_record(baseline_commit="TEST-COMMIT")
    record["candidate_count"] = 17

    issues = validate_candidate_policy_record(record)

    assert "CANDIDATE_COUNT_MISMATCH" in issues


def test_candidate_policy_artifacts_are_written(tmp_path: Path):
    record = build_candidate_policy_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-candidate-policy-v1.json" in written_files
    assert "milestone-12-candidate-policy-index-v1.json" in written_files
    assert "milestone-12-candidate-policy-manifest-v1.txt" in written_files
    assert "milestone-12-candidate-policy-v1.md" in written_files
