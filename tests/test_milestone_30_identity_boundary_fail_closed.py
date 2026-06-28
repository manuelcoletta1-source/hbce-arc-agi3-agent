from pathlib import Path
import json

from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed import (
    DECISION_BLOCK,
    DECISION_DECLARE_LIMIT,
    DECISION_REFUSE,
    DECISION_RESTRICT,
    DECISION_SUSPEND_OR_LIMIT,
    DECISION_ALLOW_PRIVATE,
    GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_REVISION,
    NEXT_STAGE,
    PRIVATE_MODE_ID,
    PUBLIC_MODE_ID,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    RUNTIME_CASE_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_identity_boundary_implementation_report,
    build_source_scope_snapshot,
    evaluate_identity_boundary,
    run_identity_boundary_runtime_cases,
    task_3_signature,
    validate_identity_boundary_decision,
    validate_identity_boundary_implementation_report,
    validate_source_scope_snapshot,
    write_task_3_artifacts,
)


def test_milestone_30_identity_boundary_source_scope_snapshot_is_valid():
    snapshot = build_source_scope_snapshot()

    assert validate_source_scope_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["scope_locked"] is True
    assert snapshot["scope_rules_valid"] is True
    assert snapshot["implementation_allowed_next"] is True
    assert snapshot["public_mode_id"] == PUBLIC_MODE_ID
    assert snapshot["private_mode_id"] == PRIVATE_MODE_ID
    assert snapshot["private_core_exposure_allowed"] is False
    assert snapshot["unverified_manuel_assumption_allowed"] is False
    assert snapshot["external_command_authority_allowed"] is False
    assert snapshot["stable_scope_lock"] is True


def test_milestone_30_identity_boundary_runtime_decisions_are_fail_closed():
    cases = run_identity_boundary_runtime_cases()

    assert len(cases) == RUNTIME_CASE_COUNT
    assert all(case["passed"] is True for case in cases)
    assert all(case["failure_reason"] == "NONE" for case in cases)
    observed = {case["case_id"]: case["observed"] for case in cases}

    assert observed["UNVERIFIED_EXTERNAL_PUBLIC_TOPIC_RESTRICTED"]["decision"] == DECISION_RESTRICT
    assert observed["VERIFIED_MANUEL_PRIVATE_SCOPE_ALLOWED"]["decision"] == DECISION_ALLOW_PRIVATE
    assert observed["VERIFIED_MANUEL_PRIVATE_SCOPE_ALLOWED"]["runtime_mode"] == PRIVATE_MODE_ID
    assert observed["VERIFIED_MANUEL_PRIVATE_SCOPE_ALLOWED"]["private_core_access_granted"] is True
    assert observed["MISSING_AUTHORIZATION_REFUSED"]["decision"] == DECISION_REFUSE
    assert observed["MISSING_CONTEXT_SUSPENDED_OR_LIMITED"]["decision"] == DECISION_SUSPEND_OR_LIMIT
    assert observed["MISSING_VERIFICATION_DECLARED_LIMIT"]["decision"] == DECISION_DECLARE_LIMIT
    assert observed["PRIVATE_CORE_FORCING_BLOCKED"]["decision"] == DECISION_BLOCK
    assert observed["PRIVATE_CORE_FORCING_BLOCKED"]["private_core_access_granted"] is False
    assert observed["EXTERNAL_COMMAND_ATTEMPT_BLOCKED"]["decision"] == DECISION_BLOCK
    assert observed["EXTERNAL_COMMAND_ATTEMPT_BLOCKED"]["external_command_authority_granted"] is False


def test_milestone_30_identity_boundary_direct_evaluation_never_assumes_manuel():
    decision = evaluate_identity_boundary(
        {
            "verified_identity_is_manuel": False,
            "authorization_valid": True,
            "context_sufficient": True,
            "verification_available": True,
            "private_core_requested": True,
            "external_command_requested": False,
            "public_topic": "HBCE",
            "request_id": "DIRECT-UNVERIFIED-PRIVATE",
        }
    )

    assert validate_identity_boundary_decision(decision)
    assert decision["decision"] == DECISION_BLOCK
    assert decision["runtime_mode"] == PUBLIC_MODE_ID
    assert decision["private_core_access_granted"] is False
    assert decision["external_command_authority_granted"] is False
    assert decision["verified_identity_is_manuel"] is False


def test_milestone_30_identity_boundary_implementation_report_is_valid():
    report = build_identity_boundary_implementation_report()

    assert validate_identity_boundary_implementation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["implementation_revision"] == IMPLEMENTATION_REVISION
    assert report["task_3_signature"] == task_3_signature()
    assert report["source_dependency_valid"] is True
    assert report["scope_rules_valid"] is True
    assert report["implementation_status"] == "READY"
    assert report["implementation_started"] is True
    assert report["implementation_complete"] is True
    assert report["runtime_case_count"] == RUNTIME_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["runtime_cases_valid"] is True
    assert report["public_mode_id"] == PUBLIC_MODE_ID
    assert report["private_mode_id"] == PRIVATE_MODE_ID
    assert report["private_core_access_allowed_without_verified_manuel"] is False
    assert report["unverified_manuel_assumption_allowed"] is False
    assert report["external_command_authority_allowed"] is False
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_30_identity_boundary_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_3_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["implementation_status"] == "READY"
    assert artifacts["manifest"]["implementation_started"] is True
    assert artifacts["manifest"]["implementation_complete"] is True
    assert artifacts["manifest"]["runtime_cases_valid"] is True
    assert artifacts["manifest"]["runtime_case_count"] == RUNTIME_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-3-identity-boundary-implementation.json"
    markdown_path = Path(tmp_path) / "task-3-identity-boundary-implementation.md"
    cases_path = Path(tmp_path) / "task-3-runtime-cases.json"
    matrix_path = Path(tmp_path) / "task-3-decision-matrix.json"
    manifest_path = Path(tmp_path) / "task-3-manifest.json"
    index_path = Path(tmp_path) / "task-3-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert cases_path.exists()
    assert matrix_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_identity_boundary_implementation_report(report)
    assert "MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_READY=true" in index_path.read_text(encoding="utf-8")
