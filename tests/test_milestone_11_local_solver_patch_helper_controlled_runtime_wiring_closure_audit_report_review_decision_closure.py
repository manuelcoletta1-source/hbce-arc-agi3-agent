from pathlib import Path

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_closure_audit_report_review_decision_closure import (
    NEXT_STAGE,
    SOURCE_TASK,
    TASK_NAME,
    TASK_VERDICT,
    build_closure_audit_report_review_decision_closure_record,
    validate_closure_audit_report_review_decision_closure_record,
    write_artifacts,
)


def test_closure_audit_report_review_decision_closure_record_is_valid():
    record = build_closure_audit_report_review_decision_closure_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["source_task"] == SOURCE_TASK
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["closure_audit_report_review_decision_closure_ready"] is True
    assert record["closure_audit_report_review_decision_closure_valid"] is True
    assert record["closure_audit_report_review_decision_closure_passed"] is True
    assert record["closure_audit_report_review_decision_closure"] == "DECISION_CLOSURE_PASS_REAL_EXECUTION_STILL_BLOCKED"
    assert record["closure_complete"] is True
    assert record["milestone_11_final_closure_ready"] is True
    assert record["milestone_12_candidate_exists"] is True
    assert record["milestone_12_candidate_status"] == "NOT_OPENED_CANONICALLY"
    assert record["milestone_12_opening_allowed"] is False
    assert record["real_execution_authorized"] is False
    assert record["closed_task_count"] == 11
    assert record["source_decision_valid"] is True
    assert record["source_decision_passed"] is True
    assert record["source_closure_progression_authorized"] is True
    assert record["source_real_execution_blocked"] is True
    assert record["closure_summary"]["closure"] == "DECISION_CLOSURE_PASS_REAL_EXECUTION_STILL_BLOCKED"
    assert record["closure_summary"]["milestone_11_final_closure_ready"] is True
    assert record["closure_summary"]["milestone_12_candidate_status"] == "NOT_OPENED_CANONICALLY"
    assert record["closure_summary"]["milestone_12_opening_allowed"] is False
    assert record["closure_summary"]["real_runtime_wiring"] == "BLOCKED"
    assert record["controlled_runtime_wiring_execution_allowed"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["gate_count"] >= 40
    assert record["issue_count"] == 0
    assert validate_closure_audit_report_review_decision_closure_record(record) == []


def test_closure_audit_report_review_decision_closure_fails_closed_when_milestone_12_is_opened():
    record = build_closure_audit_report_review_decision_closure_record(baseline_commit="TEST-COMMIT")
    record["milestone_12_opening_allowed"] = True

    issues = validate_closure_audit_report_review_decision_closure_record(record)

    assert "milestone_12_opening_allowed_NOT_FALSE" in issues


def test_closure_audit_report_review_decision_closure_fails_closed_when_real_execution_is_authorized():
    record = build_closure_audit_report_review_decision_closure_record(baseline_commit="TEST-COMMIT")
    record["real_execution_authorized"] = True

    issues = validate_closure_audit_report_review_decision_closure_record(record)

    assert "real_execution_authorized_NOT_FALSE" in issues


def test_closure_audit_report_review_decision_closure_fails_closed_when_runtime_wiring_is_performed():
    record = build_closure_audit_report_review_decision_closure_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_performed"] = True

    issues = validate_closure_audit_report_review_decision_closure_record(record)

    assert "runtime_wiring_performed_NOT_FALSE" in issues


def test_closure_audit_report_review_decision_closure_artifacts_are_written(tmp_path: Path):
    record = build_closure_audit_report_review_decision_closure_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-closure-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-closure-index-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-closure-manifest-v1.txt" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-closure-v1.md" in written_files
