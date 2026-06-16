from pathlib import Path

from hbce_arc_agi3.milestone_12_verified_planner_policy import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_plan_for_case,
    build_verified_planner_policy_record,
    validate_verified_planner_policy_record,
    write_artifacts,
)


def _sample_case_model():
    return {
        "case_id": "sample_case",
        "family": "navigation_goal",
        "action_space": ["UP", "DOWN", "LEFT", "RIGHT", "WAIT"],
        "optimal_actions": ["RIGHT", "DOWN"],
        "minimum_action_count": 2,
    }


def _sample_verification():
    return {
        "case_id": "sample_case",
        "verified": True,
        "optimal_rollout_verified": True,
        "invalid_guard_verified": True,
        "explorer_probe_verified": True,
        "transition_history_verified": True,
    }


def test_verified_planner_policy_record_is_valid():
    record = build_verified_planner_policy_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["verified_planner_policy_ready"] is True
    assert record["verified_planner_policy_valid"] is True
    assert record["verified_planner_policy_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["case_count"] == 6
    assert record["verified_case_count"] == 6
    assert record["plan_count"] == 6
    assert record["verified_plan_count"] == 6
    assert record["action_count"] > 0
    assert record["planner_issue_count"] == 0
    assert record["measurement_target_count"] == 10
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_verified_planner_policy_record(record) == []


def test_build_plan_for_case_returns_executable_verified_plan():
    plan = build_plan_for_case(_sample_case_model(), _sample_verification())

    assert plan["executable"] is True
    assert plan["actions"] == ["RIGHT", "DOWN"]
    assert plan["action_count"] == 2
    assert plan["minimal_plan"] is True
    assert plan["issue_count"] == 0


def test_build_plan_for_case_fails_when_action_is_invalid():
    case_model = _sample_case_model()
    case_model["optimal_actions"] = ["RIGHT", "JUMP"]

    plan = build_plan_for_case(case_model, _sample_verification())

    assert plan["executable"] is False
    assert plan["actions_valid"] is False
    assert plan["issue_count"] > 0


def test_verified_planner_policy_fails_if_submission_is_sent():
    record = build_verified_planner_policy_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_verified_planner_policy_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_verified_planner_policy_fails_if_policy_missing():
    record = build_verified_planner_policy_record(baseline_commit="TEST-COMMIT")
    record["planner_policy"] = None

    issues = validate_verified_planner_policy_record(record)

    assert "PLANNER_POLICY_MISSING" in issues


def test_verified_planner_policy_fails_if_plan_count_mutated():
    record = build_verified_planner_policy_record(baseline_commit="TEST-COMMIT")
    record["plan_count"] = 5

    issues = validate_verified_planner_policy_record(record)

    assert "PLAN_COUNT_MISMATCH" in issues


def test_verified_planner_policy_artifacts_are_written(tmp_path: Path):
    record = build_verified_planner_policy_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-verified-planner-policy-v1.json" in written_files
    assert "milestone-12-verified-planner-policy-index-v1.json" in written_files
    assert "milestone-12-verified-planner-policy-manifest-v1.txt" in written_files
    assert "milestone-12-verified-planner-policy-v1.md" in written_files
