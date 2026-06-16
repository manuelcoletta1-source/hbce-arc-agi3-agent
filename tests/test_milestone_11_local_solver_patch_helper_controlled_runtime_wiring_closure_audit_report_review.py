from pathlib import Path

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_closure_audit_report_review import (
    NEXT_STAGE,
    SOURCE_TASK,
    TASK_NAME,
    TASK_VERDICT,
    build_closure_audit_report_review_record,
    validate_closure_audit_report_review_record,
    write_artifacts,
)


def test_closure_audit_report_review_record_is_valid():
    record = build_closure_audit_report_review_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["source_task"] == SOURCE_TASK
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["closure_audit_report_review_ready"] is True
    assert record["closure_audit_report_review_valid"] is True
    assert record["closure_audit_report_review_passed"] is True
    assert record["closure_audit_report_review"] == "REVIEW_PASS_READY_FOR_DECISION_REAL_EXECUTION_BLOCKED"
    assert record["reviewed_task_count"] == 9
    assert record["source_report_valid"] is True
    assert record["source_report_passed"] is True
    assert record["source_report_real_execution_blocked"] is True
    assert record["source_report_summary_ok"] is True
    assert record["review_summary"]["real_runtime_wiring"] == "BLOCKED"
    assert record["review_summary"]["runtime_solver_patch"] == "BLOCKED"
    assert record["review_summary"]["decision_required_next"] is True
    assert record["controlled_runtime_wiring_execution_allowed"] is False
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["gate_count"] >= 35
    assert record["issue_count"] == 0
    assert validate_closure_audit_report_review_record(record) == []


def test_closure_audit_report_review_fails_closed_when_runtime_wiring_is_marked_real():
    record = build_closure_audit_report_review_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_performed"] = True

    issues = validate_closure_audit_report_review_record(record)

    assert "runtime_wiring_performed_NOT_FALSE" in issues


def test_closure_audit_report_review_fails_closed_when_review_check_fails():
    record = build_closure_audit_report_review_record(baseline_commit="TEST-COMMIT")
    record["review_checks"][0]["status"] = False

    issues = validate_closure_audit_report_review_record(record)

    assert "REVIEW_CHECK_FAILED" in issues


def test_closure_audit_report_review_fails_closed_when_reviewed_task_count_changes():
    record = build_closure_audit_report_review_record(baseline_commit="TEST-COMMIT")
    record["reviewed_task_count"] = 8

    issues = validate_closure_audit_report_review_record(record)

    assert "REVIEWED_TASK_COUNT_MISMATCH" in issues


def test_closure_audit_report_review_artifacts_are_written(tmp_path: Path):
    record = build_closure_audit_report_review_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-index-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-manifest-v1.txt" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-v1.md" in written_files
