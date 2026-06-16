from pathlib import Path

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_closure_audit_report import (
    NEXT_STAGE,
    SOURCE_TASK,
    TASK_NAME,
    TASK_VERDICT,
    build_closure_audit_report_record,
    validate_closure_audit_report_record,
    write_artifacts,
)


def test_closure_audit_report_record_is_valid():
    record = build_closure_audit_report_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["source_task"] == SOURCE_TASK
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["closure_audit_report_ready"] is True
    assert record["closure_audit_report_valid"] is True
    assert record["closure_audit_report_passed"] is True
    assert record["closure_audit_report"] == "REPORT_READY_REAL_EXECUTION_STILL_BLOCKED"
    assert record["reported_task_count"] == 8
    assert record["source_audit_valid"] is True
    assert record["source_audit_passed"] is True
    assert record["source_audit_real_execution_blocked"] is True
    assert record["report_summary"]["real_runtime_wiring"] == "BLOCKED"
    assert record["report_summary"]["runtime_solver_patch"] == "BLOCKED"
    assert record["controlled_runtime_wiring_execution_allowed"] is False
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["gate_count"] >= 35
    assert record["issue_count"] == 0
    assert validate_closure_audit_report_record(record) == []


def test_closure_audit_report_fails_closed_when_runtime_wiring_is_marked_real():
    record = build_closure_audit_report_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_performed"] = True

    issues = validate_closure_audit_report_record(record)

    assert "runtime_wiring_performed_NOT_FALSE" in issues


def test_closure_audit_report_fails_closed_when_report_finding_fails():
    record = build_closure_audit_report_record(baseline_commit="TEST-COMMIT")
    record["report_findings"][0]["status"] = False

    issues = validate_closure_audit_report_record(record)

    assert "REPORT_FINDING_FAILED" in issues


def test_closure_audit_report_fails_closed_when_reported_task_count_changes():
    record = build_closure_audit_report_record(baseline_commit="TEST-COMMIT")
    record["reported_task_count"] = 7

    issues = validate_closure_audit_report_record(record)

    assert "REPORTED_TASK_COUNT_MISMATCH" in issues


def test_closure_audit_report_artifacts_are_written(tmp_path: Path):
    record = build_closure_audit_report_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-index-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-manifest-v1.txt" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-v1.md" in written_files
