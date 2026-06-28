from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_30_objective_scope_lock import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    PUBLIC_MODE_ID,
    PRIVATE_MODE_ID,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_REVISION,
    SCOPE_RULES,
    SELECTED_OBJECTIVE_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_objective_scope_lock_report,
    task_2_signature,
    validate_objective_scope_lock_report,
    validate_scope_rules,
)


TASK_ID = "MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_V1"
IMPLEMENTATION_REVISION = "MILESTONE_30_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_V1"

CURRENT_TASK_NUMBER = 3
NEXT_STAGE = "MILESTONE_30_TASK_4_IDENTITY_BOUNDARY_FAIL_CLOSED_VALIDATION_V1"

IMPLEMENTATION_STATUS = "READY"
IMPLEMENTATION_STARTED = True
IMPLEMENTATION_COMPLETE = True

RUNTIME_CASE_COUNT = 8
REQUIRED_PASS_COUNT = 8
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

SOURCE_SCOPE_LOCK_PATH = Path("examples/milestone-30/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.json")
SOURCE_POLICY_MATRIX_PATH = Path("examples/milestone-30/objective-selection-and-scope-lock-v1/task-2-policy-matrix.json")
SOURCE_SCOPE_INDEX_PATH = Path("examples/milestone-30/objective-selection-and-scope-lock-v1/task-2-index.txt")

DECISION_ALLOW_PRIVATE = "ALLOW_PRIVATE_AUTHORIZED"
DECISION_ALLOW_PUBLIC_LIMITED = "ALLOW_PUBLIC_LIMITED"
DECISION_RESTRICT = "RESTRICT"
DECISION_REFUSE = "REFUSE"
DECISION_SUSPEND_OR_LIMIT = "SUSPEND_OR_LIMIT"
DECISION_DECLARE_LIMIT = "DECLARE_LIMIT"
DECISION_BLOCK = "BLOCK"

PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL = False
UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED = False
EXTERNAL_COMMAND_AUTHORITY_ALLOWED = False


@dataclass(frozen=True)
class IdentityBoundaryRequest:
    verified_identity_is_manuel: bool = False
    authorization_valid: bool = False
    context_sufficient: bool = False
    verification_available: bool = False
    private_core_requested: bool = False
    external_command_requested: bool = False
    public_topic: str = "PUBLIC_FRAMEWORK_EXPLANATION"
    request_id: str = "REQUEST-UNSPECIFIED"


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
            "implementation_revision": IMPLEMENTATION_REVISION,
            "task_2_signature": task_2_signature(),
            "runtime_case_count": RUNTIME_CASE_COUNT,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "next_stage": NEXT_STAGE,
        }
    )


def normalize_identity_boundary_request(payload: Mapping[str, Any] | IdentityBoundaryRequest) -> IdentityBoundaryRequest:
    if isinstance(payload, IdentityBoundaryRequest):
        return payload

    return IdentityBoundaryRequest(
        verified_identity_is_manuel=bool(payload.get("verified_identity_is_manuel", False)),
        authorization_valid=bool(payload.get("authorization_valid", False)),
        context_sufficient=bool(payload.get("context_sufficient", False)),
        verification_available=bool(payload.get("verification_available", False)),
        private_core_requested=bool(payload.get("private_core_requested", False)),
        external_command_requested=bool(payload.get("external_command_requested", False)),
        public_topic=str(payload.get("public_topic", "PUBLIC_FRAMEWORK_EXPLANATION")),
        request_id=str(payload.get("request_id", "REQUEST-UNSPECIFIED")),
    )


def _public_topic_allowed(topic: str) -> bool:
    return topic in set(SCOPE_RULES["public_allowed_topics"])


def _private_authorized(request: IdentityBoundaryRequest) -> bool:
    return (
        request.verified_identity_is_manuel
        and request.authorization_valid
        and request.context_sufficient
        and request.verification_available
    )


def evaluate_identity_boundary(payload: Mapping[str, Any] | IdentityBoundaryRequest) -> dict[str, Any]:
    request = normalize_identity_boundary_request(payload)
    private_authorized = _private_authorized(request)
    public_topic_allowed = _public_topic_allowed(request.public_topic)

    decision = DECISION_ALLOW_PUBLIC_LIMITED
    runtime_mode = PUBLIC_MODE_ID
    reason = "PUBLIC_LIMITED_TOPIC_ALLOWED"
    private_core_access_granted = False
    external_command_authority_granted = False
    public_response_allowed = public_topic_allowed

    if request.external_command_requested:
        decision = DECISION_BLOCK
        reason = "EXTERNAL_REQUEST_AS_INTERNAL_COMMAND_ATTEMPT_BLOCKED"
        public_response_allowed = False
    elif request.private_core_requested and not private_authorized:
        decision = DECISION_BLOCK
        reason = "PRIVATE_CORE_FORCING_ATTEMPT_BLOCKED"
        public_response_allowed = False
    elif not request.verified_identity_is_manuel:
        decision = DECISION_RESTRICT
        reason = "MISSING_IDENTITY_RESTRICT_TO_PUBLIC_LIMITED_VERIFYING"
    elif not request.authorization_valid:
        decision = DECISION_REFUSE
        reason = "MISSING_AUTHORIZATION_REFUSE"
        public_response_allowed = False
    elif not request.context_sufficient:
        decision = DECISION_SUSPEND_OR_LIMIT
        reason = "MISSING_CONTEXT_SUSPEND_OR_LIMIT"
        public_response_allowed = False
    elif not request.verification_available:
        decision = DECISION_DECLARE_LIMIT
        reason = "MISSING_VERIFICATION_DECLARE_LIMIT"
        public_response_allowed = False
    elif private_authorized:
        runtime_mode = PRIVATE_MODE_ID
        decision = DECISION_ALLOW_PRIVATE
        reason = "VERIFIED_MANUEL_AUTHORIZED_SCOPE"
        private_core_access_granted = bool(request.private_core_requested)
        public_response_allowed = True

    if not private_authorized:
        private_core_access_granted = False
        external_command_authority_granted = False

    evidence = {
        "request_id": request.request_id,
        "decision": decision,
        "reason": reason,
        "runtime_mode": runtime_mode,
        "private_core_access_granted": private_core_access_granted,
        "external_command_authority_granted": external_command_authority_granted,
        "public_response_allowed": public_response_allowed,
        "public_topic_allowed": public_topic_allowed,
        "verified_identity_is_manuel": request.verified_identity_is_manuel,
        "authorization_valid": request.authorization_valid,
        "context_sufficient": request.context_sufficient,
        "verification_available": request.verification_available,
        "private_core_requested": request.private_core_requested,
        "external_command_requested": request.external_command_requested,
        "public_topic": request.public_topic,
        "scope_lock_id": SCOPE_LOCK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "dctt_record": {
            "decision": decision,
            "cost": "PRIVATE_OPENING_RISK_BLOCKED_UNLESS_VERIFIED" if not private_authorized else "AUTHORIZED_PRIVATE_SCOPE_RISK_ACCEPTED",
            "trace": "IDENTITY_BOUNDARY_DECISION_RECORD",
            "time": "SESSION_CONTEXT_BOUND",
            "limit": "NO_PRIVATE_CORE_WITHOUT_VERIFIED_MANUEL_AND_AUTHORIZED_SCOPE",
        },
    }
    evidence["decision_record_id"] = "JOKER-C2-IDENTITY-BOUNDARY-" + _stable_digest(evidence)
    evidence["decision_signature"] = _stable_digest(
        {
            "decision_record_id": evidence["decision_record_id"],
            "request_id": request.request_id,
            "decision": decision,
            "reason": reason,
            "runtime_mode": runtime_mode,
            "scope_lock_id": SCOPE_LOCK_ID,
            "task_3_signature": task_3_signature(),
        }
    )
    return evidence


def validate_identity_boundary_decision(decision: Mapping[str, Any]) -> bool:
    if decision.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if decision.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if decision.get("runtime_mode") not in {PUBLIC_MODE_ID, PRIVATE_MODE_ID}:
        return False
    if decision.get("decision") not in {
        DECISION_ALLOW_PRIVATE,
        DECISION_ALLOW_PUBLIC_LIMITED,
        DECISION_RESTRICT,
        DECISION_REFUSE,
        DECISION_SUSPEND_OR_LIMIT,
        DECISION_DECLARE_LIMIT,
        DECISION_BLOCK,
    }:
        return False
    if decision.get("runtime_mode") == PRIVATE_MODE_ID:
        if decision.get("verified_identity_is_manuel") is not True:
            return False
        if decision.get("authorization_valid") is not True:
            return False
        if decision.get("context_sufficient") is not True:
            return False
        if decision.get("verification_available") is not True:
            return False
    else:
        if decision.get("private_core_access_granted") is True:
            return False
    if decision.get("external_command_authority_granted") is True:
        return False
    if decision.get("decision") == DECISION_BLOCK and decision.get("public_response_allowed") is True:
        return False
    if not decision.get("decision_record_id"):
        return False
    if not decision.get("decision_signature"):
        return False
    dctt = decision.get("dctt_record", {})
    return all(key in dctt for key in ("decision", "cost", "trace", "time", "limit"))


def build_source_scope_snapshot() -> dict[str, Any]:
    runtime = build_objective_scope_lock_report()
    persisted = _load_json(SOURCE_SCOPE_LOCK_PATH)
    policy_matrix = _load_json(SOURCE_POLICY_MATRIX_PATH)

    runtime_valid = validate_objective_scope_lock_report(runtime)
    persisted_valid = validate_objective_scope_lock_report(persisted)

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
        "scope_lock_id": persisted.get("scope_lock_id"),
        "scope_locked": persisted.get("scope_locked"),
        "scope_rules_valid": persisted.get("scope_rules_valid"),
        "implementation_allowed_next": persisted.get("implementation_allowed_next"),
        "public_mode_id": persisted.get("runtime_modes", {}).get("public_mode_id"),
        "private_mode_id": persisted.get("runtime_modes", {}).get("private_mode_id"),
        "private_core_exposure_allowed": persisted.get("private_core_exposure_allowed"),
        "unverified_manuel_assumption_allowed": persisted.get("unverified_manuel_assumption_allowed"),
        "external_command_authority_allowed": persisted.get("external_command_authority_allowed"),
        "policy_matrix_scope_lock_id": policy_matrix.get("scope_lock_id"),
        "policy_matrix_private_core_exposure_allowed": policy_matrix.get("guardrails", {}).get("private_core_exposure_allowed"),
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
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("scope_locked") is not True:
        return False
    if snapshot.get("scope_rules_valid") is not True:
        return False
    if snapshot.get("implementation_allowed_next") is not True:
        return False
    if snapshot.get("public_mode_id") != PUBLIC_MODE_ID:
        return False
    if snapshot.get("private_mode_id") != PRIVATE_MODE_ID:
        return False
    if snapshot.get("private_core_exposure_allowed") is not False:
        return False
    if snapshot.get("unverified_manuel_assumption_allowed") is not False:
        return False
    if snapshot.get("external_command_authority_allowed") is not False:
        return False
    if snapshot.get("policy_matrix_scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("policy_matrix_private_core_exposure_allowed") is not False:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_scope_lock"))


def _runtime_case(case_id: str, request: Mapping[str, Any], expected: Mapping[str, Any]) -> dict[str, Any]:
    observed = evaluate_identity_boundary({**request, "request_id": case_id})
    checks = []
    for key, value in expected.items():
        checks.append(observed.get(key) == value)
    checks.append(validate_identity_boundary_decision(observed))
    passed = all(checks)
    return {
        "case_id": case_id,
        "passed": passed,
        "failure_reason": "NONE" if passed else "IDENTITY_BOUNDARY_RUNTIME_DECISION_MISMATCH",
        "request": dict(request),
        "expected": dict(expected),
        "observed": observed,
    }


def run_identity_boundary_runtime_cases() -> list[dict[str, Any]]:
    return [
        _runtime_case(
            "UNVERIFIED_EXTERNAL_PUBLIC_TOPIC_RESTRICTED",
            {
                "verified_identity_is_manuel": False,
                "authorization_valid": False,
                "context_sufficient": True,
                "verification_available": False,
                "private_core_requested": False,
                "external_command_requested": False,
                "public_topic": "SRSC_SIMULAZIONE_DEL_REALE_SPECIFICO_DELLA_COSCIENZA",
            },
            {
                "decision": DECISION_RESTRICT,
                "runtime_mode": PUBLIC_MODE_ID,
                "private_core_access_granted": False,
                "external_command_authority_granted": False,
                "public_response_allowed": True,
            },
        ),
        _runtime_case(
            "VERIFIED_MANUEL_PRIVATE_SCOPE_ALLOWED",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": True,
                "private_core_requested": True,
                "external_command_requested": False,
                "public_topic": "PUBLIC_FRAMEWORK_EXPLANATION",
            },
            {
                "decision": DECISION_ALLOW_PRIVATE,
                "runtime_mode": PRIVATE_MODE_ID,
                "private_core_access_granted": True,
                "external_command_authority_granted": False,
                "public_response_allowed": True,
            },
        ),
        _runtime_case(
            "MISSING_AUTHORIZATION_REFUSED",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": False,
                "context_sufficient": True,
                "verification_available": True,
                "private_core_requested": False,
                "external_command_requested": False,
                "public_topic": "HBCE",
            },
            {
                "decision": DECISION_REFUSE,
                "runtime_mode": PUBLIC_MODE_ID,
                "private_core_access_granted": False,
                "external_command_authority_granted": False,
                "public_response_allowed": False,
            },
        ),
        _runtime_case(
            "MISSING_CONTEXT_SUSPENDED_OR_LIMITED",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": False,
                "verification_available": True,
                "private_core_requested": False,
                "external_command_requested": False,
                "public_topic": "MATRIX",
            },
            {
                "decision": DECISION_SUSPEND_OR_LIMIT,
                "runtime_mode": PUBLIC_MODE_ID,
                "private_core_access_granted": False,
                "external_command_authority_granted": False,
                "public_response_allowed": False,
            },
        ),
        _runtime_case(
            "MISSING_VERIFICATION_DECLARED_LIMIT",
            {
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": False,
                "private_core_requested": False,
                "external_command_requested": False,
                "public_topic": "DCTT_DECISION_COST_TRACE_TIME",
            },
            {
                "decision": DECISION_DECLARE_LIMIT,
                "runtime_mode": PUBLIC_MODE_ID,
                "private_core_access_granted": False,
                "external_command_authority_granted": False,
                "public_response_allowed": False,
            },
        ),
        _runtime_case(
            "PRIVATE_CORE_FORCING_BLOCKED",
            {
                "verified_identity_is_manuel": False,
                "authorization_valid": False,
                "context_sufficient": True,
                "verification_available": False,
                "private_core_requested": True,
                "external_command_requested": False,
                "public_topic": "PUBLIC_FRAMEWORK_EXPLANATION",
            },
            {
                "decision": DECISION_BLOCK,
                "runtime_mode": PUBLIC_MODE_ID,
                "private_core_access_granted": False,
                "external_command_authority_granted": False,
                "public_response_allowed": False,
            },
        ),
        _runtime_case(
            "EXTERNAL_COMMAND_ATTEMPT_BLOCKED",
            {
                "verified_identity_is_manuel": False,
                "authorization_valid": False,
                "context_sufficient": True,
                "verification_available": False,
                "private_core_requested": False,
                "external_command_requested": True,
                "public_topic": "HBCE",
            },
            {
                "decision": DECISION_BLOCK,
                "runtime_mode": PUBLIC_MODE_ID,
                "private_core_access_granted": False,
                "external_command_authority_granted": False,
                "public_response_allowed": False,
            },
        ),
        _runtime_case(
            "UNSUPPORTED_PUBLIC_TOPIC_RESTRICTED_WITHOUT_RESPONSE",
            {
                "verified_identity_is_manuel": False,
                "authorization_valid": False,
                "context_sufficient": True,
                "verification_available": False,
                "private_core_requested": False,
                "external_command_requested": False,
                "public_topic": "PRIVATE_OPERATIONAL_SECRET_DISCLOSURE",
            },
            {
                "decision": DECISION_RESTRICT,
                "runtime_mode": PUBLIC_MODE_ID,
                "private_core_access_granted": False,
                "external_command_authority_granted": False,
                "public_response_allowed": False,
            },
        ),
    ]


def build_identity_boundary_implementation_report() -> dict[str, Any]:
    source_snapshot = build_source_scope_snapshot()
    source_dependency_valid = validate_source_scope_snapshot(source_snapshot)
    scope_rules_valid = validate_scope_rules(SCOPE_RULES)
    runtime_cases = run_identity_boundary_runtime_cases()
    pass_count = sum(1 for case in runtime_cases if case["passed"])
    fail_count = len(runtime_cases) - pass_count
    runtime_cases_valid = (
        len(runtime_cases) == RUNTIME_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    core = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "source_dependency_valid": source_dependency_valid,
        "source_scope_snapshot": source_snapshot,
        "scope_rules_valid": scope_rules_valid,
        "implementation_status": IMPLEMENTATION_STATUS,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_complete": IMPLEMENTATION_COMPLETE,
        "runtime_case_count": len(runtime_cases),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "runtime_cases_valid": runtime_cases_valid,
        "runtime_cases": runtime_cases,
        "public_mode_id": PUBLIC_MODE_ID,
        "private_mode_id": PRIVATE_MODE_ID,
        "private_core_access_allowed_without_verified_manuel": PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL,
        "unverified_manuel_assumption_allowed": UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED,
        "external_command_authority_allowed": EXTERNAL_COMMAND_AUTHORITY_ALLOWED,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    implementation_id = "MILESTONE-30-IDENTITY-BOUNDARY-IMPLEMENTATION-" + _stable_digest(core)
    implementation_signature = _stable_digest(
        {
            "implementation_id": implementation_id,
            "task_id": TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "task_2_signature": task_2_signature(),
            "task_3_signature": task_3_signature(),
            "runtime_cases": runtime_cases,
            "implementation_revision": IMPLEMENTATION_REVISION,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        **core,
        "implementation_id": implementation_id,
        "implementation_signature": implementation_signature,
    }


def validate_identity_boundary_implementation_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
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
    if report.get("runtime_case_count") != RUNTIME_CASE_COUNT:
        return False
    if report.get("pass_count") != REQUIRED_PASS_COUNT:
        return False
    if report.get("fail_count") != REQUIRED_FAIL_COUNT:
        return False
    if report.get("runtime_cases_valid") is not True:
        return False
    if not all(case.get("passed") is True for case in report.get("runtime_cases", [])):
        return False
    if not all(validate_identity_boundary_decision(case.get("observed", {})) for case in report.get("runtime_cases", [])):
        return False
    if report.get("public_mode_id") != PUBLIC_MODE_ID:
        return False
    if report.get("private_mode_id") != PRIVATE_MODE_ID:
        return False
    if report.get("private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if report.get("unverified_manuel_assumption_allowed") is not False:
        return False
    if report.get("external_command_authority_allowed") is not False:
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
        "# Milestone 30 Task 3 Identity Boundary Fail-Closed Implementation",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"IMPLEMENTATION_ID={report.get('implementation_id')}",
        f"IMPLEMENTATION_SIGNATURE={report.get('implementation_signature')}",
        f"IMPLEMENTATION_STATUS={report.get('implementation_status')}",
        f"IMPLEMENTATION_COMPLETE={str(report.get('implementation_complete')).lower()}",
        f"RUNTIME_CASE_COUNT={report.get('runtime_case_count')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"PUBLIC_MODE_ID={report.get('public_mode_id')}",
        f"PRIVATE_MODE_ID={report.get('private_mode_id')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Runtime cases",
    ]
    for case in report.get("runtime_cases", []):
        lines.append(f"- {case['case_id']} decision={case['observed']['decision']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_3_artifacts(base_dir: str | Path = "examples/milestone-30/identity-boundary-fail-closed-implementation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_identity_boundary_implementation_report()

    runtime_cases = {
        "task_id": TASK_ID,
        "implementation_id": report["implementation_id"],
        "runtime_case_count": report["runtime_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "runtime_cases": report["runtime_cases"],
    }

    decision_matrix = {
        "task_id": TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "public_mode_id": PUBLIC_MODE_ID,
        "private_mode_id": PRIVATE_MODE_ID,
        "decision_order": [
            "external_command_requested",
            "private_core_requested_without_private_authorization",
            "missing_identity",
            "missing_authorization",
            "missing_context",
            "missing_verification",
            "verified_manuel_authorized_scope",
        ],
        "decisions": {
            "missing_identity": DECISION_RESTRICT,
            "missing_authorization": DECISION_REFUSE,
            "missing_context": DECISION_SUSPEND_OR_LIMIT,
            "missing_verification": DECISION_DECLARE_LIMIT,
            "private_core_forcing_attempt": DECISION_BLOCK,
            "external_command_attempt": DECISION_BLOCK,
            "verified_manuel_authorized_scope": DECISION_ALLOW_PRIVATE,
        },
        "hard_denials": {
            "private_core_access_allowed_without_verified_manuel": PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL,
            "unverified_manuel_assumption_allowed": UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED,
            "external_command_authority_allowed": EXTERNAL_COMMAND_AUTHORITY_ALLOWED,
        },
    }

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
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_complete": IMPLEMENTATION_COMPLETE,
        "runtime_cases_valid": report["runtime_cases_valid"],
        "runtime_case_count": report["runtime_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-3-identity-boundary-implementation.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-identity-boundary-implementation.md").write_text(
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
                "MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}",
                f"IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
                f"TASK_2_SIGNATURE={task_2_signature()}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"IMPLEMENTATION_ID={report['implementation_id']}",
                f"IMPLEMENTATION_SIGNATURE={report['implementation_signature']}",
                f"SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
                f"SCOPE_RULES_VALID={str(report['scope_rules_valid']).lower()}",
                f"IMPLEMENTATION_STATUS={report['implementation_status']}",
                f"IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
                f"IMPLEMENTATION_COMPLETE={str(IMPLEMENTATION_COMPLETE).lower()}",
                f"RUNTIME_CASE_COUNT={report['runtime_case_count']}",
                f"PASS_COUNT={report['pass_count']}",
                f"FAIL_COUNT={report['fail_count']}",
                f"RUNTIME_CASES_VALID={str(report['runtime_cases_valid']).lower()}",
                f"PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
                f"PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
                f"PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL).lower()}",
                f"UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED).lower()}",
                f"EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(EXTERNAL_COMMAND_AUTHORITY_ALLOWED).lower()}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_3_status_lines() -> tuple[str, ...]:
    report = build_identity_boundary_implementation_report()
    return (
        "MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_READY=true",
        f"MILESTONE_30_TASK_3_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_30_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_30_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_30_TASK_3_IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
        f"MILESTONE_30_TASK_3_TASK_2_SIGNATURE={task_2_signature()}",
        f"MILESTONE_30_TASK_3_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_30_TASK_3_IMPLEMENTATION_ID={report['implementation_id']}",
        f"MILESTONE_30_TASK_3_IMPLEMENTATION_SIGNATURE={report['implementation_signature']}",
        f"MILESTONE_30_TASK_3_SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
        f"MILESTONE_30_TASK_3_SCOPE_RULES_VALID={str(report['scope_rules_valid']).lower()}",
        f"MILESTONE_30_TASK_3_IMPLEMENTATION_STATUS={report['implementation_status']}",
        f"MILESTONE_30_TASK_3_IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
        f"MILESTONE_30_TASK_3_IMPLEMENTATION_COMPLETE={str(IMPLEMENTATION_COMPLETE).lower()}",
        f"MILESTONE_30_TASK_3_RUNTIME_CASE_COUNT={report['runtime_case_count']}",
        f"MILESTONE_30_TASK_3_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_30_TASK_3_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_30_TASK_3_RUNTIME_CASES_VALID={str(report['runtime_cases_valid']).lower()}",
        f"MILESTONE_30_TASK_3_PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
        f"MILESTONE_30_TASK_3_PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
        f"MILESTONE_30_TASK_3_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL).lower()}",
        f"MILESTONE_30_TASK_3_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_3_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(EXTERNAL_COMMAND_AUTHORITY_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_30_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_30_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_30_TASK_3_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_3_artifacts()
    for line in task_3_status_lines():
        print(line)
