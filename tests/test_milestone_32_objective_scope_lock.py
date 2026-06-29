import json
from pathlib import Path

from hbce_arc_agi3.milestone_32_objective_scope_lock import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_CASE_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_OPENING_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_2_signature,
    run_milestone_32_objective_scope_lock,
    validate_milestone_32_objective_scope_lock_report,
    write_task_2_artifacts,
)


def test_milestone_32_objective_scope_lock_report_is_valid():
    report = run_milestone_32_objective_scope_lock()

    assert validate_milestone_32_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_opening_task_id"] == SOURCE_OPENING_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_2_signature"] == task_2_signature()
    assert report["source_opening_status"] == "READY"
    assert report["source_opening_passed"] is True
    assert report["scope_lock_status"] == "LOCKED"
    assert report["scope_lock_case_count"] == SCOPE_LOCK_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["scope_lock_passed"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_32_boundary_flags_are_locked():
    report = run_milestone_32_objective_scope_lock()

    assert report["opc_technical_proof_receipt_only"] is True
    assert report["legal_certification"] is False
    assert report["ipr_card_internal_operational_identity_certificate"] is True
    assert report["ipr_card_official_public_identity_document"] is False
    assert report["explicit_legal_boundary_required"] is True


def test_milestone_32_proof_links_are_locked():
    report = run_milestone_32_objective_scope_lock()

    assert report["ai_output_linked_to_verified_operational_subject"] is True
    assert report["ai_output_linked_to_governed_session"] is True
    assert report["ai_output_linked_to_event_trace"] is True
    assert report["ai_output_linked_to_technical_proof_receipt"] is True
    assert report["ai_output_linked_to_audit_record"] is True
    assert report["ai_output_linked_to_model_usage_record"] is True


def test_milestone_32_objective_scope_lock_cases_are_all_passed():
    report = run_milestone_32_objective_scope_lock()

    assert len(report["scope_lock_cases"]) == SCOPE_LOCK_CASE_COUNT
    assert all(case["passed"] is True for case in report["scope_lock_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["scope_lock_cases"])


def test_milestone_32_objective_scope_lock_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_2_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_opening_task_id"] == SOURCE_OPENING_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_2_signature"] == task_2_signature()
    assert artifacts["manifest"]["scope_lock_status"] == "LOCKED"
    assert artifacts["manifest"]["scope_lock_passed"] is True
    assert artifacts["manifest"]["scope_lock_case_count"] == SCOPE_LOCK_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["task_budget_max"] == TASK_BUDGET_MAX
    assert artifacts["manifest"]["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-2-objective-scope-lock-report.json"
    index_path = Path(tmp_path) / "task-2-index.txt"

    assert report_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_milestone_32_objective_scope_lock_report(report)
    assert "MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index_path.read_text(encoding="utf-8")


def test_milestone_32_objective_scope_lock_rejects_mutated_report():
    report = run_milestone_32_objective_scope_lock()
    report["legal_certification"] = True

    assert not validate_milestone_32_objective_scope_lock_report(report)
