from pathlib import Path

from hbce_arc_agi3.milestone_12_executable_world_model import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_executable_world_model_record,
    execute_rollout,
    execute_transition,
    initial_world_state,
    validate_executable_world_model_record,
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


def test_executable_world_model_record_is_valid():
    record = build_executable_world_model_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["executable_world_model_ready"] is True
    assert record["executable_world_model_valid"] is True
    assert record["executable_world_model_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["case_count"] == 6
    assert record["rollout_count"] == 18
    assert record["transition_count"] > 0
    assert record["measurement_target_count"] == 10
    assert record["world_model"]["invalid_transition_count"] == 6
    assert record["world_model"]["explorer_action_valid_count"] == 6
    assert record["world_model"]["model_consistent_case_count"] == 6
    assert record["world_model"]["model_consistency_check_count"] == 30
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_executable_world_model_record(record) == []


def test_execute_transition_advances_on_expected_action():
    case = _sample_case()
    state = initial_world_state(case)

    next_state = execute_transition(case, state, "RIGHT")

    assert next_state["progress_index"] == 1
    assert next_state["step_count"] == 1
    assert next_state["completed"] is False
    assert next_state["failed"] is False
    assert next_state["history"][0]["progress_made"] is True


def test_execute_transition_fails_closed_on_invalid_action():
    case = _sample_case()
    state = initial_world_state(case)

    next_state = execute_transition(case, state, "__INVALID_ACTION__")

    assert next_state["failed"] is True
    assert next_state["invalid_action_count"] == 1
    assert next_state["history"][0]["valid"] is False


def test_execute_rollout_completes_optimal_sequence():
    case = _sample_case()

    rollout = execute_rollout(case, ["RIGHT", "RIGHT", "DOWN"], "TEST_OPTIMAL")

    assert rollout["completed"] is True
    assert rollout["failed"] is False
    assert rollout["executed_action_count"] == 3
    assert rollout["action_efficiency"] == 1.0


def test_executable_world_model_fails_if_kaggle_submission_is_sent():
    record = build_executable_world_model_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_executable_world_model_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_executable_world_model_fails_if_world_model_missing():
    record = build_executable_world_model_record(baseline_commit="TEST-COMMIT")
    record["world_model"] = None

    issues = validate_executable_world_model_record(record)

    assert "WORLD_MODEL_MISSING" in issues


def test_executable_world_model_artifacts_are_written(tmp_path: Path):
    record = build_executable_world_model_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-executable-world-model-v1.json" in written_files
    assert "milestone-12-executable-world-model-index-v1.json" in written_files
    assert "milestone-12-executable-world-model-manifest-v1.txt" in written_files
    assert "milestone-12-executable-world-model-v1.md" in written_files
