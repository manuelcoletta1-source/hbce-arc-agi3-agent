from pathlib import Path

from hbce_arc_agi3.milestone_12_world_model_verifier import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_verification_report,
    build_world_model_verifier_record,
    validate_world_model_verifier_record,
    verify_transition_history,
    write_artifacts,
)


def test_world_model_verifier_record_is_valid():
    record = build_world_model_verifier_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["world_model_verifier_ready"] is True
    assert record["world_model_verifier_valid"] is True
    assert record["world_model_verifier_passed"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["case_count"] == 6
    assert record["verified_case_count"] == 6
    assert record["rollout_count"] == 18
    assert record["verified_rollout_count"] == 18
    assert record["verification_issue_count"] == 0
    assert record["verification_report"]["optimal_rollout_verified_count"] == 6
    assert record["verification_report"]["invalid_guard_verified_count"] == 6
    assert record["verification_report"]["explorer_probe_verified_count"] == 6
    assert record["verification_report"]["transition_history_verified_count"] == 6
    assert record["verification_report"]["boundary_guard_verified_count"] == 10
    assert record["public_overfit_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_world_model_verifier_record(record) == []


def test_verify_transition_history_accepts_valid_history():
    rollout = {
        "states": [
            {"history": []},
            {
                "history": [
                    {
                        "valid": True,
                        "progress_made": True,
                    }
                ]
            },
        ]
    }

    report = verify_transition_history(rollout)

    assert report["verified"] is True
    assert report["issue"] == "NONE"
    assert report["state_count"] == 2
    assert report["transition_count"] == 1


def test_verify_transition_history_rejects_missing_states():
    report = verify_transition_history({})

    assert report["verified"] is False
    assert report["issue"] == "STATES_MISSING"


def test_build_verification_report_fails_closed_on_missing_source():
    report = build_verification_report(None)

    assert report["case_count"] == 0
    assert report["verification_issue_count"] == 1
    assert report["measurement_target_count"] == 10


def test_world_model_verifier_fails_if_submission_is_sent():
    record = build_world_model_verifier_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_world_model_verifier_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_world_model_verifier_fails_if_report_missing():
    record = build_world_model_verifier_record(baseline_commit="TEST-COMMIT")
    record["verification_report"] = None

    issues = validate_world_model_verifier_record(record)

    assert "VERIFICATION_REPORT_MISSING" in issues


def test_world_model_verifier_artifacts_are_written(tmp_path: Path):
    record = build_world_model_verifier_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-world-model-verifier-v1.json" in written_files
    assert "milestone-12-world-model-verifier-index-v1.json" in written_files
    assert "milestone-12-world-model-verifier-manifest-v1.txt" in written_files
    assert "milestone-12-world-model-verifier-v1.md" in written_files
