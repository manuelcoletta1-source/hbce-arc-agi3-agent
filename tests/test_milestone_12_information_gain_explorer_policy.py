from pathlib import Path

from hbce_arc_agi3.milestone_12_information_gain_explorer_policy import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_information_gain_explorer_record,
    rank_exploratory_actions,
    score_action_information_gain,
    select_exploratory_action,
    validate_information_gain_explorer_record,
    write_artifacts,
)


def _sample_case():
    return {
        "case_id": "sample_navigation",
        "family": "navigation_goal",
        "action_space": ["UP", "DOWN", "LEFT", "RIGHT", "WAIT"],
        "optimal_actions": ["RIGHT", "RIGHT", "DOWN"],
        "minimum_action_count": 3,
    }


def test_information_gain_explorer_record_is_valid():
    record = build_information_gain_explorer_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["milestone_12_status"] == "OPENED_CANONICALLY"
    assert record["information_gain_explorer_ready"] is True
    assert record["information_gain_explorer_valid"] is True
    assert record["information_gain_explorer_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["benchmark_case_count"] == 6
    assert record["measurement_target_count"] == 10
    assert record["explorer_policy"]["case_count"] == 6
    assert record["explorer_policy"]["selected_action_count"] == 6
    assert record["explorer_policy"]["wait_action_selected_count"] == 0
    assert record["explorer_policy"]["invalid_action_selected_count"] == 0
    assert record["explorer_policy"]["first_optimal_action_selected_count"] == 6
    assert record["explorer_policy"]["mean_expected_information_gain"] > 0.0
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_information_gain_explorer_record(record) == []


def test_score_action_information_gain_prefers_first_optimal_action():
    case = _sample_case()

    right_score = score_action_information_gain(case, "RIGHT")
    wait_score = score_action_information_gain(case, "WAIT")

    assert right_score["expected_information_gain"] > wait_score["expected_information_gain"]
    assert right_score["first_optimal"] is True
    assert wait_score["wait_action"] is True


def test_rank_exploratory_actions_puts_best_action_first():
    ranked = rank_exploratory_actions(_sample_case())

    assert ranked[0]["action"] == "RIGHT"
    assert ranked[0]["expected_information_gain"] > ranked[-1]["expected_information_gain"]


def test_select_exploratory_action_returns_valid_non_wait_action():
    selected = select_exploratory_action(_sample_case())

    assert selected["selected_action"] == "RIGHT"
    assert selected["selected_wait_action"] is False
    assert selected["selected_expected_information_gain"] > 0.0


def test_information_gain_explorer_fails_if_external_api_dependency_is_enabled():
    record = build_information_gain_explorer_record(baseline_commit="TEST-COMMIT")
    record["external_api_dependency"] = True

    issues = validate_information_gain_explorer_record(record)

    assert "external_api_dependency_NOT_FALSE" in issues


def test_information_gain_explorer_fails_if_wait_is_selected():
    record = build_information_gain_explorer_record(baseline_commit="TEST-COMMIT")
    record["explorer_policy"]["wait_action_selected_count"] = 1

    issues = validate_information_gain_explorer_record(record)

    assert "WAIT_ACTION_SELECTED" in issues


def test_information_gain_explorer_artifacts_are_written(tmp_path: Path):
    record = build_information_gain_explorer_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-information-gain-explorer-policy-v1.json" in written_files
    assert "milestone-12-information-gain-explorer-policy-index-v1.json" in written_files
    assert "milestone-12-information-gain-explorer-policy-manifest-v1.txt" in written_files
    assert "milestone-12-information-gain-explorer-policy-v1.md" in written_files
