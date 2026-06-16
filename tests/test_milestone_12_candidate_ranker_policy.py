from pathlib import Path

from hbce_arc_agi3.milestone_12_candidate_ranker_policy import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_candidate_ranker_policy_record,
    rank_candidates,
    score_candidate,
    validate_candidate_ranker_policy_record,
    write_artifacts,
)


def _sample_candidates():
    return [
        {
            "candidate_id": "C1",
            "candidate_signature": "SIG1",
            "case_id": "case_a",
            "family": "navigation_goal",
            "candidate_kind": "PREFIX_SAFE_REPLAY",
            "candidate_policy": "DETERMINISTIC_EPISODE_MEMORY_REUSE",
            "actions": ["RIGHT"],
            "candidate_length": 1,
            "source_episode_id": "E1",
            "candidate_verified": True,
            "ranker_ready": True,
            "issue_count": 0,
        },
        {
            "candidate_id": "C2",
            "candidate_signature": "SIG2",
            "case_id": "case_a",
            "family": "navigation_goal",
            "candidate_kind": "VERIFIED_EPISODE_REPLAY",
            "candidate_policy": "DETERMINISTIC_EPISODE_MEMORY_REUSE",
            "actions": ["RIGHT", "DOWN"],
            "candidate_length": 2,
            "source_episode_id": "E1",
            "candidate_verified": True,
            "ranker_ready": True,
            "issue_count": 0,
        },
        {
            "candidate_id": "C3",
            "candidate_signature": "SIG3",
            "case_id": "case_a",
            "family": "navigation_goal",
            "candidate_kind": "FAMILY_HEURISTIC_REPLAY",
            "candidate_policy": "DETERMINISTIC_EPISODE_MEMORY_REUSE",
            "actions": ["RIGHT", "DOWN"],
            "candidate_length": 2,
            "source_episode_id": "E1",
            "candidate_verified": True,
            "ranker_ready": True,
            "issue_count": 0,
        },
    ]


def test_candidate_ranker_policy_record_is_valid():
    record = build_candidate_ranker_policy_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["candidate_ranker_policy_ready"] is True
    assert record["candidate_ranker_policy_valid"] is True
    assert record["candidate_ranker_policy_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["case_count"] == 6
    assert record["candidate_count"] == 18
    assert record["ranked_candidate_count"] == 18
    assert record["selected_candidate_count"] == 6
    assert record["top_replay_candidate_count"] == 6
    assert record["ranker_ready_candidate_count"] == 18
    assert record["ranker_issue_count"] == 0
    assert record["measurement_target_count"] == 10
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_candidate_ranker_policy_record(record) == []


def test_score_candidate_prefers_verified_episode_replay():
    candidates = _sample_candidates()
    scores = {candidate["candidate_kind"]: score_candidate(candidate)["score"] for candidate in candidates}

    assert scores["VERIFIED_EPISODE_REPLAY"] > scores["PREFIX_SAFE_REPLAY"]
    assert scores["PREFIX_SAFE_REPLAY"] > scores["FAMILY_HEURISTIC_REPLAY"]


def test_rank_candidates_selects_replay_as_top_for_case():
    ranked = rank_candidates(_sample_candidates())
    selected = [candidate for candidate in ranked if candidate["selected_for_case"] is True]

    assert len(selected) == 1
    assert selected[0]["candidate_kind"] == "VERIFIED_EPISODE_REPLAY"
    assert selected[0]["rank_within_case"] == 1


def test_candidate_ranker_policy_fails_if_submission_is_sent():
    record = build_candidate_ranker_policy_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_candidate_ranker_policy_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_candidate_ranker_policy_fails_if_policy_missing():
    record = build_candidate_ranker_policy_record(baseline_commit="TEST-COMMIT")
    record["ranker_policy"] = None

    issues = validate_candidate_ranker_policy_record(record)

    assert "RANKER_POLICY_MISSING" in issues


def test_candidate_ranker_policy_fails_if_selected_count_mutated():
    record = build_candidate_ranker_policy_record(baseline_commit="TEST-COMMIT")
    record["selected_candidate_count"] = 5

    issues = validate_candidate_ranker_policy_record(record)

    assert "SELECTED_CANDIDATE_COUNT_MISMATCH" in issues


def test_candidate_ranker_policy_artifacts_are_written(tmp_path: Path):
    record = build_candidate_ranker_policy_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-candidate-ranker-policy-v1.json" in written_files
    assert "milestone-12-candidate-ranker-policy-index-v1.json" in written_files
    assert "milestone-12-candidate-ranker-policy-manifest-v1.txt" in written_files
    assert "milestone-12-candidate-ranker-policy-v1.md" in written_files
