from pathlib import Path

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_execution_contract import (
    NEXT_STAGE,
    SOURCE_TASK,
    TASK_NAME,
    TASK_VERDICT,
    build_execution_contract_record,
    validate_execution_contract_record,
    write_artifacts,
)


def test_execution_contract_record_is_valid():
    record = build_execution_contract_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["source_task"] == SOURCE_TASK
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["execution_contract_ready"] is True
    assert record["controlled_runtime_wiring_dry_run_allowed"] is True
    assert record["controlled_runtime_wiring_execution_allowed"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["contract_gate_count"] >= 25
    assert record["contract_issue_count"] == 0
    assert validate_execution_contract_record(record) == []


def test_execution_contract_fails_closed_when_required_boundary_is_broken():
    record = build_execution_contract_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_performed"] = True

    issues = validate_execution_contract_record(record)

    assert "runtime_wiring_performed_NOT_FALSE" in issues


def test_execution_contract_artifacts_are_written(tmp_path: Path):
    record = build_execution_contract_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-index-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-manifest-v1.txt" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-v1.md" in written_files
