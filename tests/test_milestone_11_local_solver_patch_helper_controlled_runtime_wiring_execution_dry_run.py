from pathlib import Path

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_execution_dry_run import (
    NEXT_STAGE,
    SOURCE_TASK,
    TASK_NAME,
    TASK_VERDICT,
    build_execution_dry_run_record,
    validate_execution_dry_run_record,
    write_artifacts,
)


def test_execution_dry_run_record_is_valid():
    record = build_execution_dry_run_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["source_task"] == SOURCE_TASK
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["execution_dry_run_ready"] is True
    assert record["execution_dry_run_valid"] is True
    assert record["controlled_runtime_wiring_dry_run_completed"] is True
    assert record["controlled_runtime_wiring_execution_allowed"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["gate_count"] >= 25
    assert record["issue_count"] == 0
    assert validate_execution_dry_run_record(record) == []


def test_execution_dry_run_fails_closed_when_execution_is_marked_real():
    record = build_execution_dry_run_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_performed"] = True

    issues = validate_execution_dry_run_record(record)

    assert "runtime_wiring_performed_NOT_FALSE" in issues


def test_execution_dry_run_steps_never_execute_real_operations():
    record = build_execution_dry_run_record(baseline_commit="TEST-COMMIT")

    assert record["dry_run_step_count"] == len(record["dry_run_steps"])
    assert all(step["simulated"] is True for step in record["dry_run_steps"])
    assert all(step["executed"] is False for step in record["dry_run_steps"])


def test_execution_dry_run_artifacts_are_written(tmp_path: Path):
    record = build_execution_dry_run_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-index-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-manifest-v1.txt" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-v1.md" in written_files
