from pathlib import Path
import json

from hbce_arc_agi3.milestone_31_verified_operator_session_gate import (
    DECISION_ALLOW_SESSION,
    DECISION_BLOCK,
    DECISION_DECLARE_LIMIT,
    DECISION_REFUSE,
    DECISION_RESTRICT,
    DECISION_SUSPEND_OR_LIMIT,
    GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_REVISION,
    NEXT_STAGE,
    PRIVATE_MODE_ID,
    PUBLIC_MODE_ID,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SESSION_CASE_COUNT,
    SESSION_GATE_MODE_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_source_scope_snapshot,
    build_verified_operator_session_gate_implementation_report,
    evaluate_verified_operator_session_gate,
    run_verified_operator_session_gate_runtime_cases,
    task_3_signature,
    validate_runtime_cases,
    validate_source_scope_snapshot,
    validate_verified_operator_session_gate_decision,
    validate_verified_operator_session_gate_implementation_report,
    write_task_3_artifacts,
)


def test_milestone_31_verified_operator_session_gate_source_scope_snapshot_is_valid():
    snapshot = build_source_scope_snapshot()

    assert validate_source_scope_snapshot(snapshot)
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["scope_locked"] is True
    assert snapshot["scope_rules_valid"] is True
    assert snapshot["implementation_allowed_next"] is True
    assert snapshot["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert snapshot["policy_fail_closed_default"] is True
    assert snapshot["policy_private_core_without_verified_manuel_allowed"] is False
    assert snapshot["policy_unverified_manuel_assumption_allowed"] is False
    assert snapshot["policy_external_command_authority_allowed"] is False
    assert snapshot["forbidden_operations_all_false"] is True
    assert snapshot["stable_scope_lock"] is True


def test_milestone_31_verified_operator_session_gate_decision_paths_are_fail_closed():
    public = evaluate_verified_operator_session_gate({"request_id": "PUBLIC"})
    allowed = evaluate_verified_operator_session_gate(
        {
            "request_id": "ALLOW",
            "verified_identity_is_manuel": True,
            "authorization_valid": True,
            "context_sufficient": True,
            "verification_available": True,
            "requested_private_scope": True,
            "operator_intent": "activate session",
            "session_trace_id": "SESSION-TRACE-ALLOW",
            "private_core_requested": True,
        }
    )
    missing_identity = evaluate_verified_operator_session_gate(
        {
            "request_id": "NO-ID",
            "requested_private_scope": True,
            "authorization_valid": True,
            "context_sufficient": True,
            "verification_available": True,
            "operator_intent": "activate session",
            "session_trace_id": "SESSION-TRACE-NO-ID",
        }
    )
    missing_auth = evaluate_verified_operator_session_gate(
        {
            "request_id": "NO-AUTH",
            "verified_identity_is_manuel": True,
            "requested_private_scope": True,
            "authorization_valid": False,
            "context_sufficient": True,
            "verification_available": True,
            "operator_intent": "activate session",
            "session_trace_id": "SESSION-TRACE-NO-AUTH",
        }
    )
    missing_context = evaluate_verified_operator_session_gate(
        {
            "request_id": "NO-CONTEXT",
            "verified_identity_is_manuel": True,
            "requested_private_scope": True,
            "authorization_valid": True,
            "context_sufficient": False,
            "verification_available": True,
            "operator_intent": "activate session",
            "session_trace_id": "SESSION-TRACE-NO-CONTEXT",
        }
    )
    missing_verification = evaluate_verified_operator_session_gate(
        {
            "request_id": "NO-VERIFY",
            "verified_identity_is_manuel": True,
            "requested_private_scope": True,
            "authorization_valid": True,
            "context_sufficient": True,
            "verification_available": False,
            "operator_intent": "activate session",
            "session_trace_id": "SESSION-TRACE-NO-VERIFY",
        }
    )
    external = evaluate_verified_operator_session_gate(
        {
            "request_id": "EXTERNAL",
            "verified_identity_is_manuel": True,
            "authorization_valid": True,
            "context_sufficient": True,
            "verification_available": True,
            "requested_private_scope": True,
            "operator_intent": "activate session",
            "session_trace_id": "SESSION-TRACE-EXTERNAL",
            "external_command_requested": True,
        }
    )

    assert validate_verified_operator_session_gate_decision(public)
    assert validate_verified_operator_session_gate_decision(allowed)
    assert validate_verified_operator_session_gate_decision(missing_identity)
    assert validate_verified_operator_session_gate_decision(missing_auth)
    assert validate_verified_operator_session_gate_decision(missing_context)
    assert validate_verified_operator_session_gate_decision(missing_verification)
    assert validate_verified_operator_session_gate_decision(external)

    assert public["decision"] == DECISION_RESTRICT
    assert public["runtime_mode"] == PUBLIC_MODE_ID
    assert allowed["decision"] == DECISION_ALLOW_SESSION
    assert allowed["runtime_mode"] == PRIVATE_MODE_ID
    assert allowed["private_authorized_scope_activated"] is True
    assert allowed["private_core_access_granted"] is True
    assert missing_identity["decision"] == DECISION_BLOCK
    assert missing_auth["decision"] == DECISION_REFUSE
    assert missing_context["decision"] == DECISION_SUSPEND_OR_LIMIT
    assert missing_verification["decision"] == DECISION_DECLARE_LIMIT
    assert external["decision"] == DECISION_BLOCK
    assert external["external_command_authority_granted"] is False


def test_milestone_31_verified_operator_session_gate_runtime_cases_are_valid():
    cases = run_verified_operator_session_gate_runtime_cases()
    case_ids = {case["case_id"] for case in cases}
    decisions = {case["case_id"]: case["observed"]["decision"] for case in cases}

    assert len(cases) == SESSION_CASE_COUNT
    assert validate_runtime_cases(cases)
    assert case_ids == {
        "PUBLIC_UNVERIFIED_LIMITED_RESTRICTED",
        "VERIFIED_MANUEL_AUTHORIZED_SESSION_ALLOWED",
        "MISSING_IDENTITY_PRIVATE_SCOPE_BLOCKED",
        "MISSING_AUTHORIZATION_REFUSED",
        "MISSING_CONTEXT_SUSPENDED_OR_LIMITED",
        "MISSING_VERIFICATION_DECLARED_LIMIT",
        "PRIVATE_CORE_FORCING_WITHOUT_VERIFIED_MANUEL_BLOCKED",
        "EXTERNAL_COMMAND_ATTEMPT_BLOCKED",
        "MISSING_SESSION_TRACE_SUSPENDED_OR_LIMITED",
    }
    assert decisions["VERIFIED_MANUEL_AUTHORIZED_SESSION_ALLOWED"] == DECISION_ALLOW_SESSION
    assert decisions["MISSING_IDENTITY_PRIVATE_SCOPE_BLOCKED"] == DECISION_BLOCK
    assert decisions["MISSING_AUTHORIZATION_REFUSED"] == DECISION_REFUSE
    assert decisions["MISSING_CONTEXT_SUSPENDED_OR_LIMITED"] == DECISION_SUSPEND_OR_LIMIT
    assert decisions["MISSING_VERIFICATION_DECLARED_LIMIT"] == DECISION_DECLARE_LIMIT
    assert decisions["EXTERNAL_COMMAND_ATTEMPT_BLOCKED"] == DECISION_BLOCK


def test_milestone_31_verified_operator_session_gate_implementation_report_is_valid():
    report = build_verified_operator_session_gate_implementation_report()

    assert validate_verified_operator_session_gate_implementation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["implementation_revision"] == IMPLEMENTATION_REVISION
    assert report["task_3_signature"] == task_3_signature()
    assert report["implementation_status"] == "READY"
    assert report["implementation_started"] is True
    assert report["implementation_complete"] is True
    assert report["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert report["session_case_count"] == SESSION_CASE_COUNT
    assert report["pass_count"] == 9
    assert report["fail_count"] == 0
    assert report["runtime_cases_valid"] is True
    assert report["private_core_access_without_verified_manuel_allowed"] is False
    assert report["unverified_manuel_assumption_allowed"] is False
    assert report["external_command_authority_allowed"] is False
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_31_verified_operator_session_gate_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_3_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_3_signature"] == task_3_signature()
    assert artifacts["manifest"]["implementation_status"] == "READY"
    assert artifacts["manifest"]["implementation_started"] is True
    assert artifacts["manifest"]["implementation_complete"] is True
    assert artifacts["manifest"]["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert artifacts["manifest"]["session_case_count"] == SESSION_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == 9
    assert artifacts["manifest"]["fail_count"] == 0
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-3-session-gate-implementation.json"
    markdown_path = Path(tmp_path) / "task-3-session-gate-implementation.md"
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
    assert validate_verified_operator_session_gate_implementation_report(report)
    assert "MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_READY=true" in index_path.read_text(encoding="utf-8")
