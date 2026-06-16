from pathlib import Path

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_review_decision_closure import (
    NEXT_STAGE,
    SOURCE_TASK,
    TASK_NAME,
    TASK_VERDICT,
    build_review_decision_closure_record,
    validate_review_decision_closure_record,
    write_artifacts,
)


def test_review_decision_closure_record_is_valid():
    record = build_review_decision_closure_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["source_task"] == SOURCE_TASK
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["review_decision_closure_ready"] is True
    assert record["review_decision_closure_valid"] is True
    assert record["review_decision_closure_passed"] is True
    assert record["review_decision_closure"] == "CLOSED_REAL_EXECUTION_STILL_BLOCKED"
    assert record["milestone_subchain_closed"] is True
    assert record["milestone_subchain_locked"] is True
    assert record["closed_task_count"] == 6
    assert record["source_decision_valid"] is True
    assert record["source_decision_passed"] is True
    assert record["source_decision_real_execution_blocked"] is True
    assert record["controlled_runtime_wiring_execution_allowed"] is False
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["gate_count"] >= 30
    assert record["issue_count"] == 0
    assert validate_review_decision_closure_record(record) == []


def test_review_decision_closure_fails_closed_when_runtime_wiring_is_marked_real():
    record = build_review_decision_closure_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_performed"] = True

    issues = validate_review_decision_closure_record(record)

    assert "runtime_wiring_performed_NOT_FALSE" in issues


def test_review_decision_closure_fails_closed_when_closure_input_fails():
    record = build_review_decision_closure_record(baseline_commit="TEST-COMMIT")
    record["closure_inputs"][0]["status"] = False

    issues = validate_review_decision_closure_record(record)

    assert "CLOSURE_INPUT_FAILED" in issues


def test_review_decision_closure_fails_closed_when_chain_count_changes():
    record = build_review_decision_closure_record(baseline_commit="TEST-COMMIT")
    record["closed_task_count"] = 5

    issues = validate_review_decision_closure_record(record)

    assert "CLOSED_TASK_COUNT_MISMATCH" in issues


def test_review_decision_closure_artifacts_are_written(tmp_path: Path):
    record = build_review_decision_closure_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-review-decision-closure-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-review-decision-closure-index-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-review-decision-closure-manifest-v1.txt" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-review-decision-closure-v1.md" in written_files
