from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_31_objective_scope_lock import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_ALLOWED_NEXT as SOURCE_IMPLEMENTATION_ALLOWED_NEXT,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    PRIVATE_MODE_ID,
    PUBLIC_MODE_ID,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_REVISION,
    SELECTED_OBJECTIVE_ID,
    SELECTED_OBJECTIVE_STATUS,
    SESSION_GATE_MODE_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_objective_scope_lock_report,
    task_2_signature,
    validate_objective_scope_lock_report,
    validate_scope_rules,
)


TASK_ID = "MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_V1"
IMPLEMENTATION_REVISION = "MILESTONE_31_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_V1"

CURRENT_TASK_NUMBER = 3
NEXT_STAGE = "MILESTONE_31_TASK_4_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_VALIDATION_V1"

IMPLEMENTATION_STATUS = "READY"
IMPLEMENTATION_STARTED = True
IMPLEMENTATION_COMPLETE = True

SESSION_CASE_COUNT = 9
REQUIRED_PASS_COUNT = 9
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

DECISION_ALLOW_SESSION = "ALLOW_AUTHORIZED_PRIVATE_SESSION"
DECISION_BLOCK = "BLOCK"
DECISION_REFUSE = "REFUSE"
DECISION_RESTRICT = "RESTRICT_PUBLIC_LIMITED"
DECISION_SUSPEND_OR_LIMIT = "SUSPEND_OR_LIMIT"
DECISION_DECLARE_LIMIT = "DECLARE_LIMIT"

GATE_STATUS_ACTIVE = "SESSION_GATE_ACTIVE"
GATE_STATUS_FAIL_CLOSED = "SESSION_GATE_FAIL_CLOSED"
GATE_STATUS_PUBLIC_LIMITED = "SESSION_GATE_PUBLIC_LIMITED"

SOURCE_SCOPE_LOCK_PATH = Path("examples/milestone-31/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.json")
SOURCE_POLICY_MATRIX_PATH = Path("examples/milestone-31/objective-selection-and-scope-lock-v1/task-2-policy-matrix.json")
SOURCE_MANIFEST_PATH = Path("examples/milestone-31/objective-selection-and-scope-lock-v1/task-2-manifest.json")
SOURCE_INDEX_PATH = Path("examples/milestone-31/objective-selection-and-scope-lock-v1/task-2-index.txt")


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_3_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "scope_lock_revision": SCOPE_LOCK_REVISION,
            "implementation_revision": IMPLEMENTATION_REVISION,
            "task_2_signature": task_2_signature(),
            "session_gate_mode_id": SESSION_GATE_MODE_ID,
            "session_case_count": SESSION_CASE_COUNT,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "next_stage": NEXT_STAGE,
        }
    )


def _decision_record_id(payload: Mapping[str, Any]) -> str:
    return "M31-SESSION-GATE-DECISION-" + _stable_digest(payload)


def build_source_scope_snapshot() -> dict[str, Any]:
    runtime = build_objective_scope_lock_report()
    persisted = _load_json(SOURCE_SCOPE_LOCK_PATH)
    policy = _load_json(SOURCE_POLICY_MATRIX_PATH)

    runtime_valid = validate_objective_scope_lock_report(runtime)
    persisted_valid = validate_objective_scope_lock_report(persisted)
    policy_guardrails = policy.get("guardrails", {})
    forbidden_operations = policy.get("forbidden_operations", {})

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_scope_lock_artifact_id": runtime.get("scope_lock_artifact_id"),
        "persisted_scope_lock_artifact_id": persisted.get("scope_lock_artifact_id"),
        "runtime_scope_lock_signature": runtime.get("scope_lock_signature"),
        "persisted_scope_lock_signature": persisted.get("scope_lock_signature"),
        "runtime_task_2_signature": runtime.get("task_2_signature"),
        "persisted_task_2_signature": persisted.get("task_2_signature"),
        "selected_objective_id": persisted.get("selected_objective_id"),
        "selected_objective_status": persisted.get("selected_objective_status"),
        "scope_lock_id": persisted.get("scope_lock_id"),
        "scope_locked": persisted.get("scope_locked"),
        "scope_rules_valid": persisted.get("scope_rules_valid"),
        "implementation_allowed_next": persisted.get("implementation_allowed_next"),
        "session_gate_mode_id": persisted.get("runtime_modes", {}).get("session_gate_mode_id"),
        "policy_fail_closed_default": policy_guardrails.get("fail_closed_default"),
        "policy_private_core_without_verified_manuel_allowed": policy_guardrails.get("private_core_access_without_verified_manuel_allowed"),
        "policy_unverified_manuel_assumption_allowed": policy_guardrails.get("unverified_manuel_assumption_allowed"),
        "policy_external_command_authority_allowed": policy_guardrails.get("external_command_authority_allowed"),
        "forbidden_operations_all_false": all(value is False for value in forbidden_operations.values()),
        "task_budget_max": persisted.get("task_budget_max"),
        "source_current_task_number": persisted.get("current_task_number"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_scope_lock": (
            runtime.get("scope_lock_artifact_id") == persisted.get("scope_lock_artifact_id")
            and runtime.get("scope_lock_signature") == persisted.get("scope_lock_signature")
            and runtime.get("task_2_signature") == persisted.get("task_2_signature") == task_2_signature()
        ),
    }


def validate_source_scope_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("selected_objective_status") != SELECTED_OBJECTIVE_STATUS:
        return False
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("scope_locked") is not True:
        return False
    if snapshot.get("scope_rules_valid") is not True:
        return False
    if snapshot.get("implementation_allowed_next") is not SOURCE_IMPLEMENTATION_ALLOWED_NEXT:
        return False
    if snapshot.get("session_gate_mode_id") != SESSION_GATE_MODE_ID:
        return False
    if snapshot.get("policy_fail_closed_default") is not True:
        return False
    if snapshot.get("policy_private_core_without_verified_manuel_allowed") is not False:
        return False
    if snapshot.get("policy_unverified_manuel_assumption_allowed") is not False:
        return False
    if snapshot.get("policy_external_command_authority_allowed") is not False:
        return False
    if snapshot.get("forbidden_operations_all_false") is not True:
        return False
    if snapshot.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if snapshot.get("source_current_task_number") != SOURCE_CURRENT_TASK_NUMBER:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_scope_lock"))


def evaluate_verified_operator_session_gate(request: Mapping[str, Any]) -> dict[str, Any]:
    request_id = str(request.get("request_id", "REQUEST-UNSPECIFIED"))
    verified_identity_is_manuel = bool(request.get("verified_identity_is_manuel", False))
    authorization_valid = bool(request.get("authorization_valid", False))
    context_sufficient = bool(request.get("context_sufficient", False))
    verification_available = bool(request.get("verification_available", False))
    requested_private_scope = bool(request.get("requested_private_scope", False))
    private_core_requested = bool(request.get("private_core_requested", False))
    external_command_requested = bool(request.get("external_command_requested", False))
    operator_intent = str(request.get("operator_intent", "")).strip()
    session_trace_id = str(request.get("session_trace_id", "")).strip()
    public_topic = str(request.get("public_topic", "PUBLIC_FRAMEWORK_EXPLANATION")).strip()

    decision = DECISION_RESTRICT
    reason = "PUBLIC_LIMITED_VERIFYING_DEFAULT"
    runtime_mode = PUBLIC_MODE_ID
    session_gate_status = GATE_STATUS_PUBLIC_LIMITED
    private_authorized_scope_activated = False
    private_core_access_granted = False
    external_command_authority_granted = False
    unverified_manuel_assumption = False

    if external_command_requested:
        decision = DECISION_BLOCK
        reason = "EXTERNAL_COMMAND_AUTHORITY_FORBIDDEN"
        session_gate_status = GATE_STATUS_FAIL_CLOSED
    elif private_core_requested and not verified_identity_is_manuel:
        decision = DECISION_BLOCK
        reason = "PRIVATE_CORE_REQUEST_WITHOUT_VERIFIED_MANUEL"
        session_gate_status = GATE_STATUS_FAIL_CLOSED
    elif requested_private_scope and not verified_identity_is_manuel:
        decision = DECISION_BLOCK
        reason = "PRIVATE_SCOPE_REQUEST_WITHOUT_VERIFIED_MANUEL"
        session_gate_status = GATE_STATUS_FAIL_CLOSED
    elif verified_identity_is_manuel and requested_private_scope and not authorization_valid:
        decision = DECISION_REFUSE
        reason = "MISSING_OR_INVALID_AUTHORIZATION"
        session_gate_status = GATE_STATUS_FAIL_CLOSED
    elif verified_identity_is_manuel and requested_private_scope and authorization_valid and not context_sufficient:
        decision = DECISION_SUSPEND_OR_LIMIT
        reason = "INSUFFICIENT_CONTEXT"
        session_gate_status = GATE_STATUS_FAIL_CLOSED
    elif verified_identity_is_manuel and requested_private_scope and authorization_valid and context_sufficient and not verification_available:
        decision = DECISION_DECLARE_LIMIT
        reason = "VERIFICATION_UNAVAILABLE"
        session_gate_status = GATE_STATUS_FAIL_CLOSED
    elif verified_identity_is_manuel and requested_private_scope and authorization_valid and context_sufficient and verification_available and not operator_intent:
        decision = DECISION_SUSPEND_OR_LIMIT
        reason = "MISSING_OPERATOR_INTENT"
        session_gate_status = GATE_STATUS_FAIL_CLOSED
    elif verified_identity_is_manuel and requested_private_scope and authorization_valid and context_sufficient and verification_available and not session_trace_id:
        decision = DECISION_SUSPEND_OR_LIMIT
        reason = "MISSING_SESSION_TRACE_ID"
        session_gate_status = GATE_STATUS_FAIL_CLOSED
    elif verified_identity_is_manuel and requested_private_scope and authorization_valid and context_sufficient and verification_available and operator_intent and session_trace_id:
        decision = DECISION_ALLOW_SESSION
        reason = "VERIFIED_OPERATOR_AUTHORIZED_SESSION_GRANTED"
        runtime_mode = PRIVATE_MODE_ID
        session_gate_status = GATE_STATUS_ACTIVE
        private_authorized_scope_activated = True
        private_core_access_granted = bool(private_core_requested)
    else:
        decision = DECISION_RESTRICT
        reason = "PUBLIC_LIMITED_VERIFYING_DEFAULT"
        session_gate_status = GATE_STATUS_PUBLIC_LIMITED

    payload = {
        "request_id": request_id,
        "decision": decision,
        "reason": reason,
        "runtime_mode": runtime_mode,
        "session_gate_mode_id": SESSION_GATE_MODE_ID,
        "session_gate_status": session_gate_status,
        "verified_identity_is_manuel": verified_identity_is_manuel,
        "authorization_valid": authorization_valid,
        "context_sufficient": context_sufficient,
        "verification_available": verification_available,
        "requested_private_scope": requested_private_scope,
        "operator_intent_present": bool(operator_intent),
        "session_trace_id_present": bool(session_trace_id),
        "public_topic": public_topic,
        "private_authorized_scope_activated": private_authorized_scope_activated,
        "private_core_access_granted": private_core_access_granted,
        "external_command_authority_granted": external_command_authority_granted,
        "unverified_manuel_assumption": unverified_manuel_assumption,
        "fail_closed_default": decision != DECISION_ALLOW_SESSION,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
    }
    return {
        **payload,
        "decision_record_id": _decision_record_id(payload),
    }


def validate_verified_operator_session_gate_decision(decision: Mapping[str, Any]) -> bool:
    required = {
        "decision_record_id",
        "request_id",
        "decision",
        "reason",
        "runtime_mode",
        "session_gate_mode_id",
        "session_gate_status",
        "verified_identity_is_manuel",
        "authorization_valid",
        "context_sufficient",
        "verification_available",
        "requested_private_scope",
        "operator_intent_present",
        "session_trace_id_present",
        "private_authorized_scope_activated",
        "private_core_access_granted",
        "external_command_authority_granted",
        "unverified_manuel_assumption",
        "fail_closed_default",
        "scope_lock_id",
        "implementation_revision",
    }
    if not required.issubset(decision.keys()):
        return False
    if decision.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if decision.get("implementation_revision") != IMPLEMENTATION_REVISION:
        return False
    if decision.get("session_gate_mode_id") != SESSION_GATE_MODE_ID:
        return False
    if decision.get("external_command_authority_granted") is not False:
        return False
    if decision.get("unverified_manuel_assumption") is not False:
        return False
    if decision.get("private_core_access_granted") and decision.get("verified_identity_is_manuel") is not True:
        return False
    if decision.get("private_authorized_scope_activated"):
        return (
            decision.get("decision") == DECISION_ALLOW_SESSION
            and decision.get("runtime_mode") == PRIVATE_MODE_ID
            and decision.get("session_gate_status") == GATE_STATUS_ACTIVE
            and decision.get("verified_identity_is_manuel") is True
            and decision.get("authorization_valid") is True
            and decision.get("context_sufficient") is True
            and decision.get("verification_available") is True
            and decision.get("requested_private_scope") is True
            and decision.get("operator_intent_present") is True
            and decision.get("session_trace_id_present") is True
            and decision.get("fail_closed_default") is False
        )
    return (
        decision.get("decision") in {
            DECISION_BLOCK,
            DECISION_REFUSE,
            DECISION_RESTRICT,
            DECISION_SUSPEND_OR_LIMIT,
            DECISION_DECLARE_LIMIT,
        }
        and decision.get("runtime_mode") == PUBLIC_MODE_ID
        and decision.get("private_authorized_scope_activated") is False
        and decision.get("fail_closed_default") is True
    )


def _runtime_case(case_id: str, request: Mapping[str, Any], expected_decision: str, expected_runtime_mode: str, expected_gate_status: str) -> dict[str, Any]:
    observed = evaluate_verified_operator_session_gate({"request_id": case_id, **dict(request)})
    passed = (
        validate_verified_operator_session_gate_decision(observed)
        and observed["decision"] == expected_decision
        and observed["runtime_mode"] == expected_runtime_mode
        and observed["session_gate_status"] == expected_gate_status
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "failure_reason": "NONE" if passed else "SESSION_GATE_DECISION_MISMATCH",
        "expected": {
            "decision": expected_decision,
            "runtime_mode": expected_runtime_mode,
            "session_gate_status": expected_gate_status,
        },
        "observed": observed,
    }


def run_verified_operator_session_gate_runtime_cases() -> list[dict[str, Any]]:
    return [
        _runtime_case(
            "PUBLIC_UNVERIFIED_LIMITED_RESTRICTED",
            {"public_topic": "PUBLIC_FRAMEWORK_EXPLANATION"},
            DECISION_RESTRICT,
            PUBLIC_MODE_ID,
            GATE_STATUS_PUBLIC_LIMITED,
        ),
        _runtime_case(
            "VERIFIED_MANUEL_AUTHORIZED_SESSION_ALLOWED",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": True,
                "requested_private_scope": True,
                "operator_intent": "activate authorized operator session",
                "session_trace_id": "SESSION-TRACE-31-3-AUTHORIZED",
                "private_core_requested": True,
            },
            DECISION_ALLOW_SESSION,
            PRIVATE_MODE_ID,
            GATE_STATUS_ACTIVE,
        ),
        _runtime_case(
            "MISSING_IDENTITY_PRIVATE_SCOPE_BLOCKED",
            {
                "verified_identity_is_manuel": False,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": True,
                "requested_private_scope": True,
                "operator_intent": "attempt private scope",
                "session_trace_id": "SESSION-TRACE-31-3-MISSING-ID",
            },
            DECISION_BLOCK,
            PUBLIC_MODE_ID,
            GATE_STATUS_FAIL_CLOSED,
        ),
        _runtime_case(
            "MISSING_AUTHORIZATION_REFUSED",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": False,
                "context_sufficient": True,
                "verification_available": True,
                "requested_private_scope": True,
                "operator_intent": "attempt private scope",
                "session_trace_id": "SESSION-TRACE-31-3-MISSING-AUTH",
            },
            DECISION_REFUSE,
            PUBLIC_MODE_ID,
            GATE_STATUS_FAIL_CLOSED,
        ),
        _runtime_case(
            "MISSING_CONTEXT_SUSPENDED_OR_LIMITED",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": False,
                "verification_available": True,
                "requested_private_scope": True,
                "operator_intent": "attempt private scope",
                "session_trace_id": "SESSION-TRACE-31-3-MISSING-CONTEXT",
            },
            DECISION_SUSPEND_OR_LIMIT,
            PUBLIC_MODE_ID,
            GATE_STATUS_FAIL_CLOSED,
        ),
        _runtime_case(
            "MISSING_VERIFICATION_DECLARED_LIMIT",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": False,
                "requested_private_scope": True,
                "operator_intent": "attempt private scope",
                "session_trace_id": "SESSION-TRACE-31-3-MISSING-VERIFICATION",
            },
            DECISION_DECLARE_LIMIT,
            PUBLIC_MODE_ID,
            GATE_STATUS_FAIL_CLOSED,
        ),
        _runtime_case(
            "PRIVATE_CORE_FORCING_WITHOUT_VERIFIED_MANUEL_BLOCKED",
            {
                "verified_identity_is_manuel": False,
                "private_core_requested": True,
                "requested_private_scope": True,
                "operator_intent": "force private core",
                "session_trace_id": "SESSION-TRACE-31-3-CORE-FORCE",
            },
            DECISION_BLOCK,
            PUBLIC_MODE_ID,
            GATE_STATUS_FAIL_CLOSED,
        ),
        _runtime_case(
            "EXTERNAL_COMMAND_ATTEMPT_BLOCKED",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": True,
                "requested_private_scope": True,
                "operator_intent": "attempt external command",
                "session_trace_id": "SESSION-TRACE-31-3-EXTERNAL-COMMAND",
                "external_command_requested": True,
            },
            DECISION_BLOCK,
            PUBLIC_MODE_ID,
            GATE_STATUS_FAIL_CLOSED,
        ),
        _runtime_case(
            "MISSING_SESSION_TRACE_SUSPENDED_OR_LIMITED",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": True,
                "requested_private_scope": True,
                "operator_intent": "attempt private scope",
                "session_trace_id": "",
            },
            DECISION_SUSPEND_OR_LIMIT,
            PUBLIC_MODE_ID,
            GATE_STATUS_FAIL_CLOSED,
        ),
    ]


def validate_runtime_cases(cases: Sequence[Mapping[str, Any]]) -> bool:
    if len(cases) != SESSION_CASE_COUNT:
        return False
    if not all(case.get("passed") is True for case in cases):
        return False
    return all(validate_verified_operator_session_gate_decision(case.get("observed", {})) for case in cases)


def build_session_gate_decision_matrix() -> dict[str, Any]:
    return {
        "task_id": TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "session_gate_mode_id": SESSION_GATE_MODE_ID,
        "runtime_modes": {
            "public_mode_id": PUBLIC_MODE_ID,
            "private_mode_id": PRIVATE_MODE_ID,
        },
        "decisions": {
            "verified_authorized_contextual_verified_traceable_private_scope": DECISION_ALLOW_SESSION,
            "public_unverified_default": DECISION_RESTRICT,
            "missing_identity_private_scope": DECISION_BLOCK,
            "missing_authorization": DECISION_REFUSE,
            "missing_context": DECISION_SUSPEND_OR_LIMIT,
            "missing_verification": DECISION_DECLARE_LIMIT,
            "missing_operator_intent": DECISION_SUSPEND_OR_LIMIT,
            "missing_session_trace_id": DECISION_SUSPEND_OR_LIMIT,
            "private_core_forcing_without_verified_manuel": DECISION_BLOCK,
            "external_command_attempt": DECISION_BLOCK,
        },
        "hard_denials": {
            "private_core_access_without_verified_manuel_allowed": False,
            "unverified_manuel_assumption_allowed": False,
            "external_command_authority_allowed": False,
            "session_authorization_without_valid_authorization_allowed": False,
            "session_authorization_without_context_allowed": False,
            "session_authorization_without_verification_allowed": False,
        },
    }


def build_verified_operator_session_gate_implementation_report() -> dict[str, Any]:
    source_snapshot = build_source_scope_snapshot()
    source_dependency_valid = validate_source_scope_snapshot(source_snapshot)
    source_report = _load_json(SOURCE_SCOPE_LOCK_PATH)
    scope_rules_valid = validate_scope_rules(source_report.get("scope_rules", {}))

    runtime_cases = run_verified_operator_session_gate_runtime_cases()
    pass_count = sum(1 for case in runtime_cases if case["passed"])
    fail_count = len(runtime_cases) - pass_count
    runtime_cases_valid = validate_runtime_cases(runtime_cases)

    core = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "selected_objective_status": SELECTED_OBJECTIVE_STATUS,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "source_dependency_valid": source_dependency_valid,
        "scope_rules_valid": scope_rules_valid,
        "source_scope_snapshot": source_snapshot,
        "implementation_status": IMPLEMENTATION_STATUS,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_complete": IMPLEMENTATION_COMPLETE,
        "session_gate_mode_id": SESSION_GATE_MODE_ID,
        "public_mode_id": PUBLIC_MODE_ID,
        "private_mode_id": PRIVATE_MODE_ID,
        "decision_matrix": build_session_gate_decision_matrix(),
        "session_case_count": len(runtime_cases),
        "required_pass_count": REQUIRED_PASS_COUNT,
        "required_fail_count": REQUIRED_FAIL_COUNT,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "runtime_cases_valid": runtime_cases_valid,
        "runtime_cases": runtime_cases,
        "private_core_access_without_verified_manuel_allowed": False,
        "unverified_manuel_assumption_allowed": False,
        "external_command_authority_allowed": False,
        "session_authorization_without_valid_authorization_allowed": False,
        "session_authorization_without_context_allowed": False,
        "session_authorization_without_verification_allowed": False,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    implementation_id = "MILESTONE-31-VERIFIED-OPERATOR-SESSION-GATE-" + _stable_digest(core)
    implementation_signature = _stable_digest(
        {
            "implementation_id": implementation_id,
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "task_2_signature": task_2_signature(),
            "task_3_signature": task_3_signature(),
            "implementation_revision": IMPLEMENTATION_REVISION,
            "runtime_cases": runtime_cases,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        **core,
        "implementation_id": implementation_id,
        "implementation_signature": implementation_signature,
    }


def validate_verified_operator_session_gate_implementation_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("selected_objective_status") != SELECTED_OBJECTIVE_STATUS:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("scope_lock_revision") != SCOPE_LOCK_REVISION:
        return False
    if report.get("implementation_revision") != IMPLEMENTATION_REVISION:
        return False
    if report.get("task_2_signature") != task_2_signature():
        return False
    if report.get("task_3_signature") != task_3_signature():
        return False
    if report.get("source_dependency_valid") is not True:
        return False
    if not validate_source_scope_snapshot(report.get("source_scope_snapshot", {})):
        return False
    if report.get("scope_rules_valid") is not True:
        return False
    if report.get("implementation_status") != IMPLEMENTATION_STATUS:
        return False
    if report.get("implementation_started") is not True:
        return False
    if report.get("implementation_complete") is not True:
        return False
    if report.get("session_gate_mode_id") != SESSION_GATE_MODE_ID:
        return False
    if report.get("public_mode_id") != PUBLIC_MODE_ID:
        return False
    if report.get("private_mode_id") != PRIVATE_MODE_ID:
        return False
    if report.get("session_case_count") != SESSION_CASE_COUNT:
        return False
    if report.get("pass_count") != REQUIRED_PASS_COUNT:
        return False
    if report.get("fail_count") != REQUIRED_FAIL_COUNT:
        return False
    if report.get("runtime_cases_valid") is not True:
        return False
    if not validate_runtime_cases(report.get("runtime_cases", [])):
        return False
    false_fields = [
        "private_core_access_without_verified_manuel_allowed",
        "unverified_manuel_assumption_allowed",
        "external_command_authority_allowed",
        "session_authorization_without_valid_authorization_allowed",
        "session_authorization_without_context_allowed",
        "session_authorization_without_verification_allowed",
    ]
    if any(report.get(field) is not False for field in false_fields):
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("implementation_id") and report.get("implementation_signature"))


def render_implementation_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 31 Task 3 Verified Operator Authorization Session Gate Implementation",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"IMPLEMENTATION_ID={report.get('implementation_id')}",
        f"IMPLEMENTATION_SIGNATURE={report.get('implementation_signature')}",
        f"IMPLEMENTATION_STATUS={report.get('implementation_status')}",
        f"SESSION_GATE_MODE_ID={report.get('session_gate_mode_id')}",
        f"SESSION_CASE_COUNT={report.get('session_case_count')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"RUNTIME_CASES_VALID={str(report.get('runtime_cases_valid')).lower()}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Runtime cases",
    ]
    for case in report.get("runtime_cases", []):
        observed = case.get("observed", {})
        lines.append(f"- {case['case_id']} decision={observed.get('decision')} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_3_artifacts(base_dir: str | Path = "examples/milestone-31/verified-operator-authorization-session-gate-implementation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_verified_operator_session_gate_implementation_report()

    runtime_cases = {
        "task_id": TASK_ID,
        "implementation_id": report["implementation_id"],
        "session_gate_mode_id": SESSION_GATE_MODE_ID,
        "session_case_count": report["session_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "runtime_cases": report["runtime_cases"],
    }

    decision_matrix = build_session_gate_decision_matrix()

    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "implementation_id": report["implementation_id"],
        "implementation_signature": report["implementation_signature"],
        "implementation_status": report["implementation_status"],
        "implementation_started": report["implementation_started"],
        "implementation_complete": report["implementation_complete"],
        "session_gate_mode_id": SESSION_GATE_MODE_ID,
        "session_case_count": report["session_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "runtime_cases_valid": report["runtime_cases_valid"],
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-3-session-gate-implementation.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-session-gate-implementation.md").write_text(
        render_implementation_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-3-runtime-cases.json").write_text(
        json.dumps(runtime_cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-decision-matrix.json").write_text(
        json.dumps(decision_matrix, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SELECTED_OBJECTIVE_STATUS={SELECTED_OBJECTIVE_STATUS}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}",
                f"IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
                f"TASK_2_SIGNATURE={task_2_signature()}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
                f"SCOPE_RULES_VALID={str(report['scope_rules_valid']).lower()}",
                f"IMPLEMENTATION_ID={report['implementation_id']}",
                f"IMPLEMENTATION_SIGNATURE={report['implementation_signature']}",
                f"IMPLEMENTATION_STATUS={report['implementation_status']}",
                f"IMPLEMENTATION_STARTED={str(report['implementation_started']).lower()}",
                f"IMPLEMENTATION_COMPLETE={str(report['implementation_complete']).lower()}",
                f"SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}",
                f"PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
                f"PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
                f"SESSION_CASE_COUNT={report['session_case_count']}",
                f"PASS_COUNT={report['pass_count']}",
                f"FAIL_COUNT={report['fail_count']}",
                f"RUNTIME_CASES_VALID={str(report['runtime_cases_valid']).lower()}",
                f"PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED={str(report['private_core_access_without_verified_manuel_allowed']).lower()}",
                f"UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['unverified_manuel_assumption_allowed']).lower()}",
                f"EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['external_command_authority_allowed']).lower()}",
                f"SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED={str(report['session_authorization_without_valid_authorization_allowed']).lower()}",
                f"SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED={str(report['session_authorization_without_context_allowed']).lower()}",
                f"SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED={str(report['session_authorization_without_verification_allowed']).lower()}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "runtime_cases": runtime_cases, "decision_matrix": decision_matrix, "output_dir": str(output_dir)}


def task_3_status_lines() -> tuple[str, ...]:
    report = build_verified_operator_session_gate_implementation_report()
    return (
        "MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_READY=true",
        f"MILESTONE_31_TASK_3_TASK_ID={TASK_ID}",
        f"MILESTONE_31_TASK_3_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_31_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_31_TASK_3_SELECTED_OBJECTIVE_STATUS={SELECTED_OBJECTIVE_STATUS}",
        f"MILESTONE_31_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_31_TASK_3_SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}",
        f"MILESTONE_31_TASK_3_IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
        f"MILESTONE_31_TASK_3_TASK_2_SIGNATURE={task_2_signature()}",
        f"MILESTONE_31_TASK_3_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_31_TASK_3_SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
        f"MILESTONE_31_TASK_3_SCOPE_RULES_VALID={str(report['scope_rules_valid']).lower()}",
        f"MILESTONE_31_TASK_3_IMPLEMENTATION_ID={report['implementation_id']}",
        f"MILESTONE_31_TASK_3_IMPLEMENTATION_SIGNATURE={report['implementation_signature']}",
        f"MILESTONE_31_TASK_3_IMPLEMENTATION_STATUS={report['implementation_status']}",
        f"MILESTONE_31_TASK_3_IMPLEMENTATION_STARTED={str(report['implementation_started']).lower()}",
        f"MILESTONE_31_TASK_3_IMPLEMENTATION_COMPLETE={str(report['implementation_complete']).lower()}",
        f"MILESTONE_31_TASK_3_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}",
        f"MILESTONE_31_TASK_3_PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
        f"MILESTONE_31_TASK_3_PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
        f"MILESTONE_31_TASK_3_SESSION_CASE_COUNT={report['session_case_count']}",
        f"MILESTONE_31_TASK_3_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_31_TASK_3_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_31_TASK_3_RUNTIME_CASES_VALID={str(report['runtime_cases_valid']).lower()}",
        f"MILESTONE_31_TASK_3_PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED={str(report['private_core_access_without_verified_manuel_allowed']).lower()}",
        f"MILESTONE_31_TASK_3_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['unverified_manuel_assumption_allowed']).lower()}",
        f"MILESTONE_31_TASK_3_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['external_command_authority_allowed']).lower()}",
        f"MILESTONE_31_TASK_3_SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED={str(report['session_authorization_without_valid_authorization_allowed']).lower()}",
        f"MILESTONE_31_TASK_3_SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED={str(report['session_authorization_without_context_allowed']).lower()}",
        f"MILESTONE_31_TASK_3_SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED={str(report['session_authorization_without_verification_allowed']).lower()}",
        f"MILESTONE_31_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_31_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_31_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_31_TASK_3_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_3_artifacts()
    for line in task_3_status_lines():
        print(line)
