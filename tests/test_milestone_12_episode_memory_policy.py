from pathlib import Path

from hbce_arc_agi3.milestone_12_episode_memory_policy import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_episode_memory_entry,
    build_episode_memory_policy_record,
    validate_episode_memory_policy_record,
    write_artifacts,
)


def _sample_plan():
    return {
        "case_id": "sample_case",
        "family": "navigation_goal",
        "plan_id": "PLAN-SAMPLE_CASE",
        "actions": ["RIGHT", "DOWN"],
        "action_count": 2,
        "verified_source_case": True,
        "actions_valid": True,
        "minimal_plan": True,
        "executable": True,
        "issue_count": 0,
    }


def test_episode_memory_policy_record_is_valid():
    record = build_episode_memory_policy_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["episode_memory_policy_ready"] is True
    assert record["episode_memory_policy_valid"] is True
    assert record["episode_memory_policy_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["case_count"] == 6
    assert record["episode_count"] == 6
    assert record["verified_episode_count"] == 6
    assert record["memory_record_count"] == 6
    assert record["trace_step_count"] > 0
    assert record["reuse_candidate_count"] == 6
    assert record["episode_issue_count"] == 0
    assert record["measurement_target_count"] == 10
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_episode_memory_policy_record(record) == []


def test_build_episode_memory_entry_is_reusable():
    entry = build_episode_memory_entry(_sample_plan())

    assert entry["verified_episode"] is True
    assert entry["reusable_in_candidate_policy"] is True
    assert entry["action_count"] == 2
    assert entry["trace_step_count"] == 2
    assert entry["trace_steps"][0]["prefix"] == ["RIGHT"]
    assert entry["trace_steps"][1]["terminal_after_step"] is True
    assert entry["issue_count"] == 0


def test_build_episode_memory_entry_fails_when_source_plan_not_executable():
    plan = _sample_plan()
    plan["executable"] = False

    entry = build_episode_memory_entry(plan)

    assert entry["verified_episode"] is False
    assert entry["reusable_in_candidate_policy"] is False
    assert entry["issue_count"] > 0


def test_episode_memory_policy_fails_if_submission_is_sent():
    record = build_episode_memory_policy_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_episode_memory_policy_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_episode_memory_policy_fails_if_policy_missing():
    record = build_episode_memory_policy_record(baseline_commit="TEST-COMMIT")
    record["episode_memory_policy"] = None

    issues = validate_episode_memory_policy_record(record)

    assert "EPISODE_MEMORY_POLICY_MISSING" in issues


def test_episode_memory_policy_fails_if_episode_count_mutated():
    record = build_episode_memory_policy_record(baseline_commit="TEST-COMMIT")
    record["episode_count"] = 5

    issues = validate_episode_memory_policy_record(record)

    assert "EPISODE_COUNT_MISMATCH" in issues


def test_episode_memory_policy_artifacts_are_written(tmp_path: Path):
    record = build_episode_memory_policy_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-episode-memory-policy-v1.json" in written_files
    assert "milestone-12-episode-memory-policy-index-v1.json" in written_files
    assert "milestone-12-episode-memory-policy-manifest-v1.txt" in written_files
    assert "milestone-12-episode-memory-policy-v1.md" in written_files
