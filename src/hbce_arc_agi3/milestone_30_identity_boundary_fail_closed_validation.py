from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed import (
    DECISION_ALLOW_PRIVATE,
    DECISION_BLOCK,
    DECISION_DECLARE_LIMIT,
    DECISION_REFUSE,
    DECISION_RESTRICT,
    DECISION_SUSPEND_OR_LIMIT,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_REVISION,
    IMPLEMENTATION_STATUS,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    PRIVATE_MODE_ID,
    PUBLIC_MODE_ID,
    REQUIRED_FAIL_COUNT as SOURCE_REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT as SOURCE_REQUIRED_PASS_COUNT,
    RUNTIME_CASE_COUNT as SOURCE_RUNTIME_CASE_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID as SOURCE_IMPLEMENTATION_SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_identity_boundary_implementation_report,
    evaluate_identity_boundary,
    run_identity_boundary_runtime_cases,
    task_3_signature,
    validate_identity_boundary_decision,
    validate_identity_boundary_implementation_report,
)


TASK_ID = "MILESTONE_30_TASK_4_IDENTITY_BOUNDARY_FAIL_CLOSED_VALIDATION_V1"
VALIDATION_REVISION = "MILESTONE_30_IDENTITY_BOUNDARY_FAIL_CLOSED_VALIDATION_V1"

CURRENT_TASK_NUMBER = 4
NEXT_STAGE = "MILESTONE_30_TASK_5_IDENTITY_BOUNDARY_FAIL_CLOSED_REGRESSION_INTEGRATION_V1"

VALIDATION_STATUS = "VALID"
VALIDATION_CASE_COUNT = 9
REQUIRED_PASS_COUNT = 9
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

SOURCE_IMPLEMENTATION_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-identity-boundary-implementation.json")
SOURCE_RUNTIME_CASES_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-runtime-cases.json")
SOURCE_DECISION_MATRIX_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-decision-matrix.json")
SOURCE_MANIFEST_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-manifest.json")
SOURCE_INDEX_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-index.txt")
SOURCE_MARKDOWN_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-identity-boundary-implementation.md")


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_4_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "implementation_revision": IMPLEMENTATION_REVISION,
            "validation_revision": VALIDATION_REVISION,
            "task_3_signature": task_3_signature(),
            "validation_case_count": VALIDATION_CASE_COUNT,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "next_stage": NEXT_STAGE,
        }
    )


def _case(case_id: str, passed: bool, expected: Any, observed: Any, failure_reason: str = "NONE") -> dict[str, Any]:
    return {
        "case_id": case_id,
        "passed": passed,
        "failure_reason": "NONE" if passed else failure_reason,
        "expected": expected,
        "observed": observed,
    }


def build_implementation_snapshot() -> dict[str, Any]:
    runtime = build_identity_boundary_implementation_report()
    persisted = _load_json(SOURCE_IMPLEMENTATION_PATH)

    runtime_valid = validate_identity_boundary_implementation_report(runtime)
    persisted_valid = validate_identity_boundary_implementation_report(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_implementation_id": runtime.get("implementation_id"),
        "persisted_implementation_id": persisted.get("implementation_id"),
        "runtime_implementation_signature": runtime.get("implementation_signature"),
        "persisted_implementation_signature": persisted.get("implementation_signature"),
        "runtime_task_3_signature": runtime.get("task_3_signature"),
        "persisted_task_3_signature": persisted.get("task_3_signature"),
        "selected_objective_id": persisted.get("selected_objective_id"),
        "scope_lock_id": persisted.get("scope_lock_id"),
        "implementation_revision": persisted.get("implementation_revision"),
        "implementation_status": persisted.get("implementation_status"),
        "implementation_started": persisted.get("implementation_started"),
        "implementation_complete": persisted.get("implementation_complete"),
        "source_dependency_valid": persisted.get("source_dependency_valid"),
        "scope_rules_valid": persisted.get("scope_rules_valid"),
        "runtime_case_count": persisted.get("runtime_case_count"),
        "pass_count": persisted.get("pass_count"),
        "fail_count": persisted.get("fail_count"),
        "runtime_cases_valid": persisted.get("runtime_cases_valid"),
        "public_mode_id": persisted.get("public_mode_id"),
        "private_mode_id": persisted.get("private_mode_id"),
        "private_core_access_allowed_without_verified_manuel": persisted.get("private_core_access_allowed_without_verified_manuel"),
        "unverified_manuel_assumption_allowed": persisted.get("unverified_manuel_assumption_allowed"),
        "external_command_authority_allowed": persisted.get("external_command_authority_allowed"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_implementation": (
            runtime.get("implementation_id") == persisted.get("implementation_id")
            and runtime.get("implementation_signature") == persisted.get("implementation_signature")
            and runtime.get("task_3_signature") == persisted.get("task_3_signature") == task_3_signature()
        ),
    }


def validate_implementation_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("implementation_revision") != IMPLEMENTATION_REVISION:
        return False
    if snapshot.get("implementation_status") != IMPLEMENTATION_STATUS:
        return False
    if snapshot.get("implementation_started") is not True:
        return False
    if snapshot.get("implementation_complete") is not True:
        return False
    if snapshot.get("source_dependency_valid") is not True:
        return False
    if snapshot.get("scope_rules_valid") is not True:
        return False
    if snapshot.get("runtime_case_count") != SOURCE_RUNTIME_CASE_COUNT:
        return False
    if snapshot.get("pass_count") != SOURCE_REQUIRED_PASS_COUNT:
        return False
    if snapshot.get("fail_count") != SOURCE_REQUIRED_FAIL_COUNT:
        return False
    if snapshot.get("runtime_cases_valid") is not True:
        return False
    if snapshot.get("public_mode_id") != PUBLIC_MODE_ID:
        return False
    if snapshot.get("private_mode_id") != PRIVATE_MODE_ID:
        return False
    if snapshot.get("private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if snapshot.get("unverified_manuel_assumption_allowed") is not False:
        return False
    if snapshot.get("external_command_authority_allowed") is not False:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_implementation"))


def _validate_implementation_report_case() -> dict[str, Any]:
    report = _load_json(SOURCE_IMPLEMENTATION_PATH)
    passed = (
        validate_identity_boundary_implementation_report(report)
        and report.get("implementation_status") == "READY"
        and report.get("implementation_complete") is True
        and report.get("runtime_cases_valid") is True
        and report.get("pass_count") == 8
        and report.get("fail_count") == 0
        and report.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_3_IMPLEMENTATION_REPORT_VALID",
        passed,
        {"implementation_status": "READY", "runtime_cases_valid": True, "pass_count": 8, "fail_count": 0},
        {
            "implementation_status": report.get("implementation_status"),
            "implementation_complete": report.get("implementation_complete"),
            "runtime_cases_valid": report.get("runtime_cases_valid"),
            "pass_count": report.get("pass_count"),
            "fail_count": report.get("fail_count"),
            "next_stage": report.get("next_stage"),
        },
        "TASK_3_IMPLEMENTATION_REPORT_INVALID",
    )


def _validate_runtime_stability_case() -> dict[str, Any]:
    snapshot = build_implementation_snapshot()
    passed = validate_implementation_snapshot(snapshot)
    return _case(
        "TASK_3_IMPLEMENTATION_RUNTIME_STABILITY_VALID",
        passed,
        {"stable_implementation": True},
        snapshot,
        "TASK_3_IMPLEMENTATION_RUNTIME_STABILITY_INVALID",
    )


def _validate_artifact_set_case() -> dict[str, Any]:
    paths = (
        SOURCE_IMPLEMENTATION_PATH,
        SOURCE_RUNTIME_CASES_PATH,
        SOURCE_DECISION_MATRIX_PATH,
        SOURCE_MANIFEST_PATH,
        SOURCE_INDEX_PATH,
        SOURCE_MARKDOWN_PATH,
    )
    missing = [str(path) for path in paths if not path.exists()]
    readable = []
    for path in paths:
        if path.exists():
            readable.append(path.read_text(encoding="utf-8") != "")
    passed = not missing and all(readable)
    return _case(
        "TASK_3_IMPLEMENTATION_ARTIFACT_SET_PRESENT",
        passed,
        {"artifact_count": 6, "missing": []},
        {"artifact_count": len(paths), "missing": missing, "readable_count": sum(1 for item in readable if item)},
        "TASK_3_IMPLEMENTATION_ARTIFACT_SET_INCOMPLETE",
    )


def _validate_manifest_case() -> dict[str, Any]:
    report = _load_json(SOURCE_IMPLEMENTATION_PATH)
    manifest = _load_json(SOURCE_MANIFEST_PATH)
    passed = (
        manifest.get("task_id") == SOURCE_TASK_ID
        and manifest.get("source_task_id") == report.get("source_task_id")
        and manifest.get("selected_objective_id") == report.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and manifest.get("scope_lock_id") == report.get("scope_lock_id") == SCOPE_LOCK_ID
        and manifest.get("implementation_id") == report.get("implementation_id")
        and manifest.get("implementation_signature") == report.get("implementation_signature")
        and manifest.get("task_3_signature") == report.get("task_3_signature") == task_3_signature()
        and manifest.get("implementation_status") == "READY"
        and manifest.get("implementation_started") is True
        and manifest.get("implementation_complete") is True
        and manifest.get("runtime_cases_valid") is True
        and manifest.get("pass_count") == report.get("pass_count") == 8
        and manifest.get("fail_count") == report.get("fail_count") == 0
        and manifest.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_3_IMPLEMENTATION_MANIFEST_CONSISTENCY_VALID",
        passed,
        {"manifest_matches_implementation_report": True},
        {
            "manifest_implementation_id": manifest.get("implementation_id"),
            "report_implementation_id": report.get("implementation_id"),
            "manifest_status": manifest.get("implementation_status"),
            "manifest_next_stage": manifest.get("next_stage"),
        },
        "TASK_3_IMPLEMENTATION_MANIFEST_CONSISTENCY_INVALID",
    )


def _validate_runtime_cases_case() -> dict[str, Any]:
    report = _load_json(SOURCE_IMPLEMENTATION_PATH)
    cases = _load_json(SOURCE_RUNTIME_CASES_PATH)
    expected_case_ids = {
        "UNVERIFIED_EXTERNAL_PUBLIC_TOPIC_RESTRICTED",
        "VERIFIED_MANUEL_PRIVATE_SCOPE_ALLOWED",
        "MISSING_AUTHORIZATION_REFUSED",
        "MISSING_CONTEXT_SUSPENDED_OR_LIMITED",
        "MISSING_VERIFICATION_DECLARED_LIMIT",
        "PRIVATE_CORE_FORCING_BLOCKED",
        "EXTERNAL_COMMAND_ATTEMPT_BLOCKED",
        "UNSUPPORTED_PUBLIC_TOPIC_RESTRICTED_WITHOUT_RESPONSE",
    }
    observed_case_ids = {case.get("case_id") for case in cases.get("runtime_cases", [])}
    decisions = {case.get("case_id"): case.get("observed", {}).get("decision") for case in cases.get("runtime_cases", [])}

    passed = (
        cases.get("task_id") == SOURCE_TASK_ID
        and cases.get("implementation_id") == report.get("implementation_id")
        and cases.get("runtime_case_count") == SOURCE_RUNTIME_CASE_COUNT
        and cases.get("pass_count") == 8
        and cases.get("fail_count") == 0
        and observed_case_ids == expected_case_ids
        and decisions.get("PRIVATE_CORE_FORCING_BLOCKED") == DECISION_BLOCK
        and decisions.get("EXTERNAL_COMMAND_ATTEMPT_BLOCKED") == DECISION_BLOCK
        and decisions.get("MISSING_AUTHORIZATION_REFUSED") == DECISION_REFUSE
        and decisions.get("MISSING_CONTEXT_SUSPENDED_OR_LIMITED") == DECISION_SUSPEND_OR_LIMIT
        and decisions.get("MISSING_VERIFICATION_DECLARED_LIMIT") == DECISION_DECLARE_LIMIT
        and decisions.get("VERIFIED_MANUEL_PRIVATE_SCOPE_ALLOWED") == DECISION_ALLOW_PRIVATE
        and all(case.get("passed") is True for case in cases.get("runtime_cases", []))
        and all(validate_identity_boundary_decision(case.get("observed", {})) for case in cases.get("runtime_cases", []))
    )
    return _case(
        "TASK_3_RUNTIME_CASE_SET_VALID",
        passed,
        {"case_ids": sorted(expected_case_ids), "pass_count": 8, "fail_count": 0},
        {"case_ids": sorted(observed_case_ids), "decisions": decisions},
        "TASK_3_RUNTIME_CASE_SET_INVALID",
    )


def _validate_decision_matrix_case() -> dict[str, Any]:
    matrix = _load_json(SOURCE_DECISION_MATRIX_PATH)
    decisions = matrix.get("decisions", {})
    hard_denials = matrix.get("hard_denials", {})

    passed = (
        matrix.get("task_id") == SOURCE_TASK_ID
        and matrix.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and matrix.get("scope_lock_id") == SCOPE_LOCK_ID
        and matrix.get("public_mode_id") == PUBLIC_MODE_ID
        and matrix.get("private_mode_id") == PRIVATE_MODE_ID
        and decisions.get("missing_identity") == DECISION_RESTRICT
        and decisions.get("missing_authorization") == DECISION_REFUSE
        and decisions.get("missing_context") == DECISION_SUSPEND_OR_LIMIT
        and decisions.get("missing_verification") == DECISION_DECLARE_LIMIT
        and decisions.get("private_core_forcing_attempt") == DECISION_BLOCK
        and decisions.get("external_command_attempt") == DECISION_BLOCK
        and decisions.get("verified_manuel_authorized_scope") == DECISION_ALLOW_PRIVATE
        and hard_denials.get("private_core_access_allowed_without_verified_manuel") is False
        and hard_denials.get("unverified_manuel_assumption_allowed") is False
        and hard_denials.get("external_command_authority_allowed") is False
    )
    return _case(
        "TASK_3_DECISION_MATRIX_VALID",
        passed,
        {"decision_matrix_valid": True},
        {"decisions": decisions, "hard_denials": hard_denials},
        "TASK_3_DECISION_MATRIX_INVALID",
    )


def _validate_index_case() -> dict[str, Any]:
    report = _load_json(SOURCE_IMPLEMENTATION_PATH)
    index = SOURCE_INDEX_PATH.read_text(encoding="utf-8")
    required_markers = (
        "MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_READY=true",
        f"IMPLEMENTATION_ID={report.get('implementation_id')}",
        f"IMPLEMENTATION_SIGNATURE={report.get('implementation_signature')}",
        "IMPLEMENTATION_STATUS=READY",
        "IMPLEMENTATION_STARTED=true",
        "IMPLEMENTATION_COMPLETE=true",
        "RUNTIME_CASE_COUNT=8",
        "PASS_COUNT=8",
        "FAIL_COUNT=0",
        "RUNTIME_CASES_VALID=true",
        f"PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
        f"PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
        "PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false",
        "UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false",
        "EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false",
        f"NEXT_STAGE={SOURCE_NEXT_STAGE}",
    )
    missing = [marker for marker in required_markers if marker not in index]
    passed = not missing
    return _case(
        "TASK_3_IMPLEMENTATION_INDEX_MARKERS_VALID",
        passed,
        {"missing_markers": []},
        {"missing_markers": missing, "required_marker_count": len(required_markers)},
        "TASK_3_IMPLEMENTATION_INDEX_MARKERS_INVALID",
    )


def _validate_direct_fail_closed_probe_case() -> dict[str, Any]:
    probes = [
        evaluate_identity_boundary({"request_id": "PROBE-UNVERIFIED-PRIVATE", "private_core_requested": True}),
        evaluate_identity_boundary({"request_id": "PROBE-EXTERNAL-COMMAND", "external_command_requested": True}),
        evaluate_identity_boundary(
            {
                "request_id": "PROBE-MISSING-AUTH",
                "verified_identity_is_manuel": True,
                "authorization_valid": False,
                "context_sufficient": True,
                "verification_available": True,
            }
        ),
        evaluate_identity_boundary(
            {
                "request_id": "PROBE-VERIFIED-PRIVATE",
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": True,
                "private_core_requested": True,
            }
        ),
    ]
    passed = (
        all(validate_identity_boundary_decision(probe) for probe in probes)
        and probes[0]["decision"] == DECISION_BLOCK
        and probes[0]["private_core_access_granted"] is False
        and probes[1]["decision"] == DECISION_BLOCK
        and probes[1]["external_command_authority_granted"] is False
        and probes[2]["decision"] == DECISION_REFUSE
        and probes[3]["decision"] == DECISION_ALLOW_PRIVATE
        and probes[3]["runtime_mode"] == PRIVATE_MODE_ID
        and probes[3]["private_core_access_granted"] is True
    )
    return _case(
        "TASK_3_DIRECT_FAIL_CLOSED_PROBES_VALID",
        passed,
        {"direct_fail_closed_probes_valid": True},
        {"probe_decisions": [probe["decision"] for probe in probes], "probe_ids": [probe["decision_record_id"] for probe in probes]},
        "TASK_3_DIRECT_FAIL_CLOSED_PROBES_INVALID",
    )


def _validate_source_chain_case() -> dict[str, Any]:
    report = _load_json(SOURCE_IMPLEMENTATION_PATH)
    snapshot = build_implementation_snapshot()
    passed = (
        validate_implementation_snapshot(snapshot)
        and report.get("source_dependency_valid") is True
        and report.get("scope_rules_valid") is True
        and report.get("source_scope_snapshot", {}).get("scope_locked") is True
        and report.get("source_scope_snapshot", {}).get("implementation_allowed_next") is True
        and report.get("source_scope_snapshot", {}).get("source_next_stage") == SOURCE_TASK_ID
    )
    return _case(
        "TASK_3_SOURCE_SCOPE_CHAIN_VALID",
        passed,
        {"source_chain_valid": True},
        {
            "source_dependency_valid": report.get("source_dependency_valid"),
            "scope_rules_valid": report.get("scope_rules_valid"),
            "source_scope_snapshot": report.get("source_scope_snapshot", {}),
        },
        "TASK_3_SOURCE_SCOPE_CHAIN_INVALID",
    )


def run_identity_boundary_fail_closed_validation() -> dict[str, Any]:
    validation_cases = [
        _validate_implementation_report_case(),
        _validate_runtime_stability_case(),
        _validate_artifact_set_case(),
        _validate_manifest_case(),
        _validate_runtime_cases_case(),
        _validate_decision_matrix_case(),
        _validate_index_case(),
        _validate_direct_fail_closed_probe_case(),
        _validate_source_chain_case(),
    ]

    pass_count = sum(1 for case in validation_cases if case["passed"])
    fail_count = len(validation_cases) - pass_count
    validation_passed = (
        len(validation_cases) == VALIDATION_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    implementation_report = _load_json(SOURCE_IMPLEMENTATION_PATH)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_implementation_source_task_id": SOURCE_IMPLEMENTATION_SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "source_implementation_id": implementation_report.get("implementation_id"),
        "source_implementation_signature": implementation_report.get("implementation_signature"),
        "source_implementation_status": implementation_report.get("implementation_status"),
        "source_implementation_complete": implementation_report.get("implementation_complete"),
        "source_runtime_cases_valid": implementation_report.get("runtime_cases_valid"),
        "source_runtime_case_count": implementation_report.get("runtime_case_count"),
        "source_pass_count": implementation_report.get("pass_count"),
        "source_fail_count": implementation_report.get("fail_count"),
        "source_public_mode_id": implementation_report.get("public_mode_id"),
        "source_private_mode_id": implementation_report.get("private_mode_id"),
        "source_private_core_access_allowed_without_verified_manuel": implementation_report.get("private_core_access_allowed_without_verified_manuel"),
        "source_unverified_manuel_assumption_allowed": implementation_report.get("unverified_manuel_assumption_allowed"),
        "source_external_command_authority_allowed": implementation_report.get("external_command_authority_allowed"),
        "validation_status": VALIDATION_STATUS if validation_passed else "INVALID",
        "validation_case_count": len(validation_cases),
        "required_pass_count": REQUIRED_PASS_COUNT,
        "required_fail_count": REQUIRED_FAIL_COUNT,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "validation_passed": validation_passed,
        "validation_cases": validation_cases,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    report["validation_id"] = "MILESTONE-30-IDENTITY-BOUNDARY-VALIDATION-" + _stable_digest(report)
    report["validation_signature"] = _stable_digest(
        {
            "validation_id": report["validation_id"],
            "source_implementation_id": report["source_implementation_id"],
            "source_implementation_signature": report["source_implementation_signature"],
            "task_3_signature": report["task_3_signature"],
            "task_4_signature": report["task_4_signature"],
            "validation_cases": validation_cases,
            "validation_revision": VALIDATION_REVISION,
            "next_stage": NEXT_STAGE,
        }
    )
    return report


def validate_identity_boundary_validation_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("implementation_revision") != IMPLEMENTATION_REVISION:
        return False
    if report.get("validation_revision") != VALIDATION_REVISION:
        return False
    if report.get("task_3_signature") != task_3_signature():
        return False
    if report.get("task_4_signature") != task_4_signature():
        return False
    if report.get("source_implementation_status") != "READY":
        return False
    if report.get("source_implementation_complete") is not True:
        return False
    if report.get("source_runtime_cases_valid") is not True:
        return False
    if report.get("source_runtime_case_count") != SOURCE_RUNTIME_CASE_COUNT:
        return False
    if report.get("source_pass_count") != SOURCE_REQUIRED_PASS_COUNT:
        return False
    if report.get("source_fail_count") != SOURCE_REQUIRED_FAIL_COUNT:
        return False
    if report.get("source_public_mode_id") != PUBLIC_MODE_ID:
        return False
    if report.get("source_private_mode_id") != PRIVATE_MODE_ID:
        return False
    if report.get("source_private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if report.get("source_unverified_manuel_assumption_allowed") is not False:
        return False
    if report.get("source_external_command_authority_allowed") is not False:
        return False
    if report.get("validation_status") != VALIDATION_STATUS:
        return False
    if report.get("validation_case_count") != VALIDATION_CASE_COUNT:
        return False
    if report.get("pass_count") != REQUIRED_PASS_COUNT:
        return False
    if report.get("fail_count") != REQUIRED_FAIL_COUNT:
        return False
    if report.get("validation_passed") is not True:
        return False
    if not all(case.get("passed") is True for case in report.get("validation_cases", [])):
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("validation_id") and report.get("validation_signature"))


def render_validation_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 30 Task 4 Identity Boundary Fail-Closed Validation",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"VALIDATION_ID={report.get('validation_id')}",
        f"VALIDATION_SIGNATURE={report.get('validation_signature')}",
        f"SOURCE_IMPLEMENTATION_ID={report.get('source_implementation_id')}",
        f"SOURCE_IMPLEMENTATION_SIGNATURE={report.get('source_implementation_signature')}",
        f"VALIDATION_STATUS={report.get('validation_status')}",
        f"VALIDATION_CASE_COUNT={report.get('validation_case_count')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Validation cases",
    ]
    for case in report.get("validation_cases", []):
        lines.append(f"- {case['case_id']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_4_artifacts(base_dir: str | Path = "examples/milestone-30/identity-boundary-fail-closed-validation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_identity_boundary_fail_closed_validation()

    validation_cases = {
        "task_id": TASK_ID,
        "validation_id": report["validation_id"],
        "validation_status": report["validation_status"],
        "validation_case_count": report["validation_case_count"],
        "validation_cases": report["validation_cases"],
    }

    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "source_implementation_id": report["source_implementation_id"],
        "source_implementation_signature": report["source_implementation_signature"],
        "validation_id": report["validation_id"],
        "validation_signature": report["validation_signature"],
        "validation_status": report["validation_status"],
        "validation_passed": report["validation_passed"],
        "validation_case_count": report["validation_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-4-validation-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-validation-report.md").write_text(
        render_validation_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-4-validation-cases.json").write_text(
        json.dumps(validation_cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_30_TASK_4_IDENTITY_BOUNDARY_FAIL_CLOSED_VALIDATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
                f"VALIDATION_REVISION={VALIDATION_REVISION}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"TASK_4_SIGNATURE={task_4_signature()}",
                f"SOURCE_IMPLEMENTATION_ID={report['source_implementation_id']}",
                f"SOURCE_IMPLEMENTATION_SIGNATURE={report['source_implementation_signature']}",
                f"SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}",
                f"SOURCE_IMPLEMENTATION_COMPLETE={str(report['source_implementation_complete']).lower()}",
                f"SOURCE_RUNTIME_CASES_VALID={str(report['source_runtime_cases_valid']).lower()}",
                f"SOURCE_RUNTIME_CASE_COUNT={report['source_runtime_case_count']}",
                f"SOURCE_PASS_COUNT={report['source_pass_count']}",
                f"SOURCE_FAIL_COUNT={report['source_fail_count']}",
                f"SOURCE_PUBLIC_MODE_ID={report['source_public_mode_id']}",
                f"SOURCE_PRIVATE_MODE_ID={report['source_private_mode_id']}",
                f"SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(report['source_private_core_access_allowed_without_verified_manuel']).lower()}",
                f"SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['source_unverified_manuel_assumption_allowed']).lower()}",
                f"SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['source_external_command_authority_allowed']).lower()}",
                f"VALIDATION_ID={report['validation_id']}",
                f"VALIDATION_SIGNATURE={report['validation_signature']}",
                f"VALIDATION_STATUS={report['validation_status']}",
                f"VALIDATION_CASE_COUNT={report['validation_case_count']}",
                f"PASS_COUNT={report['pass_count']}",
                f"FAIL_COUNT={report['fail_count']}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_4_status_lines() -> tuple[str, ...]:
    report = run_identity_boundary_fail_closed_validation()
    return (
        "MILESTONE_30_TASK_4_IDENTITY_BOUNDARY_FAIL_CLOSED_VALIDATION_READY=true",
        f"MILESTONE_30_TASK_4_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_30_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_30_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_30_TASK_4_IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
        f"MILESTONE_30_TASK_4_VALIDATION_REVISION={VALIDATION_REVISION}",
        f"MILESTONE_30_TASK_4_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_30_TASK_4_TASK_4_SIGNATURE={task_4_signature()}",
        f"MILESTONE_30_TASK_4_SOURCE_IMPLEMENTATION_ID={report['source_implementation_id']}",
        f"MILESTONE_30_TASK_4_SOURCE_IMPLEMENTATION_SIGNATURE={report['source_implementation_signature']}",
        f"MILESTONE_30_TASK_4_SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}",
        f"MILESTONE_30_TASK_4_SOURCE_IMPLEMENTATION_COMPLETE={str(report['source_implementation_complete']).lower()}",
        f"MILESTONE_30_TASK_4_SOURCE_RUNTIME_CASES_VALID={str(report['source_runtime_cases_valid']).lower()}",
        f"MILESTONE_30_TASK_4_SOURCE_RUNTIME_CASE_COUNT={report['source_runtime_case_count']}",
        f"MILESTONE_30_TASK_4_SOURCE_PASS_COUNT={report['source_pass_count']}",
        f"MILESTONE_30_TASK_4_SOURCE_FAIL_COUNT={report['source_fail_count']}",
        f"MILESTONE_30_TASK_4_SOURCE_PUBLIC_MODE_ID={report['source_public_mode_id']}",
        f"MILESTONE_30_TASK_4_SOURCE_PRIVATE_MODE_ID={report['source_private_mode_id']}",
        f"MILESTONE_30_TASK_4_SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(report['source_private_core_access_allowed_without_verified_manuel']).lower()}",
        f"MILESTONE_30_TASK_4_SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['source_unverified_manuel_assumption_allowed']).lower()}",
        f"MILESTONE_30_TASK_4_SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['source_external_command_authority_allowed']).lower()}",
        f"MILESTONE_30_TASK_4_VALIDATION_ID={report['validation_id']}",
        f"MILESTONE_30_TASK_4_VALIDATION_SIGNATURE={report['validation_signature']}",
        f"MILESTONE_30_TASK_4_VALIDATION_STATUS={report['validation_status']}",
        f"MILESTONE_30_TASK_4_VALIDATION_CASE_COUNT={report['validation_case_count']}",
        f"MILESTONE_30_TASK_4_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_30_TASK_4_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_30_TASK_4_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_30_TASK_4_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_30_TASK_4_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_30_TASK_4_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_4_artifacts()
    for line in task_4_status_lines():
        print(line)
