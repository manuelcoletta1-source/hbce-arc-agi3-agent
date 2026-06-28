from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_30_objective_scope_lock import (
    validate_objective_scope_lock_report,
)
from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed import (
    DECISION_ALLOW_PRIVATE,
    DECISION_BLOCK,
    DECISION_REFUSE,
    DECISION_RESTRICT,
    IMPLEMENTATION_REVISION,
    PRIVATE_MODE_ID,
    PUBLIC_MODE_ID,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    evaluate_identity_boundary,
    task_3_signature,
    validate_identity_boundary_decision,
    validate_identity_boundary_implementation_report,
)
from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed_validation import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    REQUIRED_FAIL_COUNT as SOURCE_REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT as SOURCE_REQUIRED_PASS_COUNT,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    VALIDATION_STATUS,
    run_identity_boundary_fail_closed_validation,
    task_4_signature,
    validate_identity_boundary_validation_report,
)


TASK_ID = "MILESTONE_30_TASK_5_IDENTITY_BOUNDARY_FAIL_CLOSED_REGRESSION_INTEGRATION_V1"
REGRESSION_INTEGRATION_REVISION = "MILESTONE_30_IDENTITY_BOUNDARY_FAIL_CLOSED_REGRESSION_INTEGRATION_V1"

CURRENT_TASK_NUMBER = 5
NEXT_STAGE = "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_V1"

INTEGRATION_STATUS = "VALID"
INTEGRATION_CASE_COUNT = 9
REQUIRED_PASS_COUNT = 9
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

SOURCE_VALIDATION_REPORT_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-validation-v1/task-4-validation-report.json")
SOURCE_VALIDATION_CASES_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-validation-v1/task-4-validation-cases.json")
SOURCE_VALIDATION_MANIFEST_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-validation-v1/task-4-manifest.json")
SOURCE_VALIDATION_INDEX_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-validation-v1/task-4-index.txt")
SOURCE_VALIDATION_MARKDOWN_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-validation-v1/task-4-validation-report.md")

SOURCE_IMPLEMENTATION_REPORT_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-identity-boundary-implementation.json")
SOURCE_IMPLEMENTATION_CASES_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-runtime-cases.json")
SOURCE_IMPLEMENTATION_MATRIX_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-decision-matrix.json")
SOURCE_SCOPE_LOCK_PATH = Path("examples/milestone-30/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.json")


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_5_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "implementation_revision": IMPLEMENTATION_REVISION,
            "validation_revision": VALIDATION_REVISION,
            "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
            "task_4_signature": task_4_signature(),
            "integration_case_count": INTEGRATION_CASE_COUNT,
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


def build_validation_snapshot() -> dict[str, Any]:
    runtime = run_identity_boundary_fail_closed_validation()
    persisted = _load_json(SOURCE_VALIDATION_REPORT_PATH)

    runtime_valid = validate_identity_boundary_validation_report(runtime)
    persisted_valid = validate_identity_boundary_validation_report(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_validation_id": runtime.get("validation_id"),
        "persisted_validation_id": persisted.get("validation_id"),
        "runtime_validation_signature": runtime.get("validation_signature"),
        "persisted_validation_signature": persisted.get("validation_signature"),
        "runtime_task_4_signature": runtime.get("task_4_signature"),
        "persisted_task_4_signature": persisted.get("task_4_signature"),
        "selected_objective_id": persisted.get("selected_objective_id"),
        "scope_lock_id": persisted.get("scope_lock_id"),
        "source_implementation_id": persisted.get("source_implementation_id"),
        "source_implementation_signature": persisted.get("source_implementation_signature"),
        "source_implementation_status": persisted.get("source_implementation_status"),
        "source_implementation_complete": persisted.get("source_implementation_complete"),
        "source_runtime_cases_valid": persisted.get("source_runtime_cases_valid"),
        "source_runtime_case_count": persisted.get("source_runtime_case_count"),
        "source_private_core_access_allowed_without_verified_manuel": persisted.get("source_private_core_access_allowed_without_verified_manuel"),
        "source_unverified_manuel_assumption_allowed": persisted.get("source_unverified_manuel_assumption_allowed"),
        "source_external_command_authority_allowed": persisted.get("source_external_command_authority_allowed"),
        "validation_status": persisted.get("validation_status"),
        "validation_case_count": persisted.get("validation_case_count"),
        "pass_count": persisted.get("pass_count"),
        "fail_count": persisted.get("fail_count"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_validation": (
            runtime.get("validation_id") == persisted.get("validation_id")
            and runtime.get("validation_signature") == persisted.get("validation_signature")
            and runtime.get("task_4_signature") == persisted.get("task_4_signature") == task_4_signature()
        ),
    }


def validate_validation_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("source_implementation_status") != "READY":
        return False
    if snapshot.get("source_implementation_complete") is not True:
        return False
    if snapshot.get("source_runtime_cases_valid") is not True:
        return False
    if snapshot.get("source_runtime_case_count") != 8:
        return False
    if snapshot.get("source_private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if snapshot.get("source_unverified_manuel_assumption_allowed") is not False:
        return False
    if snapshot.get("source_external_command_authority_allowed") is not False:
        return False
    if snapshot.get("validation_status") != VALIDATION_STATUS:
        return False
    if snapshot.get("validation_case_count") != VALIDATION_CASE_COUNT:
        return False
    if snapshot.get("pass_count") != SOURCE_REQUIRED_PASS_COUNT:
        return False
    if snapshot.get("fail_count") != SOURCE_REQUIRED_FAIL_COUNT:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_validation"))


def _validate_validation_report_case() -> dict[str, Any]:
    report = _load_json(SOURCE_VALIDATION_REPORT_PATH)
    passed = (
        validate_identity_boundary_validation_report(report)
        and report.get("validation_status") == "VALID"
        and report.get("validation_passed") is True
        and report.get("pass_count") == 9
        and report.get("fail_count") == 0
        and report.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_4_VALIDATION_REPORT_VALID",
        passed,
        {"validation_status": "VALID", "validation_passed": True, "pass_count": 9, "fail_count": 0},
        {
            "validation_status": report.get("validation_status"),
            "validation_passed": report.get("validation_passed"),
            "pass_count": report.get("pass_count"),
            "fail_count": report.get("fail_count"),
            "next_stage": report.get("next_stage"),
        },
        "TASK_4_VALIDATION_REPORT_INVALID",
    )


def _validate_runtime_stability_case() -> dict[str, Any]:
    snapshot = build_validation_snapshot()
    passed = validate_validation_snapshot(snapshot)
    return _case(
        "TASK_4_VALIDATION_RUNTIME_STABILITY_VALID",
        passed,
        {"stable_validation": True},
        snapshot,
        "TASK_4_VALIDATION_RUNTIME_STABILITY_INVALID",
    )


def _validate_artifact_set_case() -> dict[str, Any]:
    paths = (
        SOURCE_VALIDATION_REPORT_PATH,
        SOURCE_VALIDATION_CASES_PATH,
        SOURCE_VALIDATION_MANIFEST_PATH,
        SOURCE_VALIDATION_INDEX_PATH,
        SOURCE_VALIDATION_MARKDOWN_PATH,
    )
    missing = [str(path) for path in paths if not path.exists()]
    readable = []
    for path in paths:
        if path.exists():
            readable.append(path.read_text(encoding="utf-8") != "")
    passed = not missing and all(readable)
    return _case(
        "TASK_4_VALIDATION_ARTIFACT_SET_PRESENT",
        passed,
        {"artifact_count": 5, "missing": []},
        {"artifact_count": len(paths), "missing": missing, "readable_count": sum(1 for item in readable if item)},
        "TASK_4_VALIDATION_ARTIFACT_SET_INCOMPLETE",
    )


def _validate_manifest_case() -> dict[str, Any]:
    report = _load_json(SOURCE_VALIDATION_REPORT_PATH)
    manifest = _load_json(SOURCE_VALIDATION_MANIFEST_PATH)
    passed = (
        manifest.get("task_id") == SOURCE_TASK_ID
        and manifest.get("source_task_id") == report.get("source_task_id")
        and manifest.get("selected_objective_id") == report.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and manifest.get("scope_lock_id") == report.get("scope_lock_id") == SCOPE_LOCK_ID
        and manifest.get("source_implementation_id") == report.get("source_implementation_id")
        and manifest.get("source_implementation_signature") == report.get("source_implementation_signature")
        and manifest.get("validation_id") == report.get("validation_id")
        and manifest.get("validation_signature") == report.get("validation_signature")
        and manifest.get("validation_status") == report.get("validation_status") == "VALID"
        and manifest.get("validation_passed") is True
        and manifest.get("pass_count") == report.get("pass_count") == 9
        and manifest.get("fail_count") == report.get("fail_count") == 0
        and manifest.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_4_VALIDATION_MANIFEST_CONSISTENCY_VALID",
        passed,
        {"manifest_matches_validation_report": True},
        {
            "manifest_validation_id": manifest.get("validation_id"),
            "report_validation_id": report.get("validation_id"),
            "manifest_status": manifest.get("validation_status"),
            "manifest_next_stage": manifest.get("next_stage"),
        },
        "TASK_4_VALIDATION_MANIFEST_CONSISTENCY_INVALID",
    )


def _validate_validation_case_set_case() -> dict[str, Any]:
    report = _load_json(SOURCE_VALIDATION_REPORT_PATH)
    cases = _load_json(SOURCE_VALIDATION_CASES_PATH)
    observed_case_ids = {case.get("case_id") for case in cases.get("validation_cases", [])}
    expected_case_ids = {
        "TASK_3_IMPLEMENTATION_REPORT_VALID",
        "TASK_3_IMPLEMENTATION_RUNTIME_STABILITY_VALID",
        "TASK_3_IMPLEMENTATION_ARTIFACT_SET_PRESENT",
        "TASK_3_IMPLEMENTATION_MANIFEST_CONSISTENCY_VALID",
        "TASK_3_RUNTIME_CASE_SET_VALID",
        "TASK_3_DECISION_MATRIX_VALID",
        "TASK_3_IMPLEMENTATION_INDEX_MARKERS_VALID",
        "TASK_3_DIRECT_FAIL_CLOSED_PROBES_VALID",
        "TASK_3_SOURCE_SCOPE_CHAIN_VALID",
    }

    passed = (
        cases.get("task_id") == SOURCE_TASK_ID
        and cases.get("validation_id") == report.get("validation_id")
        and cases.get("validation_status") == "VALID"
        and cases.get("validation_case_count") == VALIDATION_CASE_COUNT
        and observed_case_ids == expected_case_ids
        and all(case.get("passed") is True for case in cases.get("validation_cases", []))
        and all(case.get("failure_reason") == "NONE" for case in cases.get("validation_cases", []))
    )
    return _case(
        "TASK_4_VALIDATION_CASE_SET_VALID",
        passed,
        {"case_ids": sorted(expected_case_ids), "validation_case_count": 9},
        {"case_ids": sorted(observed_case_ids), "validation_case_count": cases.get("validation_case_count")},
        "TASK_4_VALIDATION_CASE_SET_INVALID",
    )


def _validate_direct_regression_probes_case() -> dict[str, Any]:
    probes = {
        "unverified_private_core": evaluate_identity_boundary({"request_id": "REGRESSION-UNVERIFIED-PRIVATE", "private_core_requested": True}),
        "external_command": evaluate_identity_boundary({"request_id": "REGRESSION-EXTERNAL-COMMAND", "external_command_requested": True}),
        "missing_authorization": evaluate_identity_boundary(
            {
                "request_id": "REGRESSION-MISSING-AUTH",
                "verified_identity_is_manuel": True,
                "authorization_valid": False,
                "context_sufficient": True,
                "verification_available": True,
            }
        ),
        "unverified_public_srsc": evaluate_identity_boundary(
            {
                "request_id": "REGRESSION-PUBLIC-SRSC",
                "verified_identity_is_manuel": False,
                "public_topic": "SRSC_SIMULAZIONE_DEL_REALE_SPECIFICO_DELLA_COSCIENZA",
                "context_sufficient": True,
            }
        ),
        "verified_private": evaluate_identity_boundary(
            {
                "request_id": "REGRESSION-VERIFIED-PRIVATE",
                "verified_identity_is_manuel": True,
                "authorization_valid": True,
                "context_sufficient": True,
                "verification_available": True,
                "private_core_requested": True,
            }
        ),
    }

    passed = (
        all(validate_identity_boundary_decision(probe) for probe in probes.values())
        and probes["unverified_private_core"]["decision"] == DECISION_BLOCK
        and probes["unverified_private_core"]["private_core_access_granted"] is False
        and probes["external_command"]["decision"] == DECISION_BLOCK
        and probes["external_command"]["external_command_authority_granted"] is False
        and probes["missing_authorization"]["decision"] == DECISION_REFUSE
        and probes["unverified_public_srsc"]["decision"] == DECISION_RESTRICT
        and probes["unverified_public_srsc"]["runtime_mode"] == PUBLIC_MODE_ID
        and probes["verified_private"]["decision"] == DECISION_ALLOW_PRIVATE
        and probes["verified_private"]["runtime_mode"] == PRIVATE_MODE_ID
        and probes["verified_private"]["private_core_access_granted"] is True
    )
    return _case(
        "IDENTITY_BOUNDARY_DIRECT_REGRESSION_PROBES_VALID",
        passed,
        {"direct_regression_probes_valid": True},
        {name: {"decision": probe["decision"], "record": probe["decision_record_id"]} for name, probe in probes.items()},
        "IDENTITY_BOUNDARY_DIRECT_REGRESSION_PROBES_INVALID",
    )


def _validate_source_implementation_case() -> dict[str, Any]:
    report = _load_json(SOURCE_IMPLEMENTATION_REPORT_PATH)
    cases = _load_json(SOURCE_IMPLEMENTATION_CASES_PATH)
    matrix = _load_json(SOURCE_IMPLEMENTATION_MATRIX_PATH)

    passed = (
        validate_identity_boundary_implementation_report(report)
        and cases.get("implementation_id") == report.get("implementation_id")
        and cases.get("runtime_case_count") == 8
        and cases.get("pass_count") == 8
        and cases.get("fail_count") == 0
        and matrix.get("scope_lock_id") == SCOPE_LOCK_ID
        and matrix.get("hard_denials", {}).get("private_core_access_allowed_without_verified_manuel") is False
        and matrix.get("hard_denials", {}).get("unverified_manuel_assumption_allowed") is False
        and matrix.get("hard_denials", {}).get("external_command_authority_allowed") is False
    )
    return _case(
        "TASK_3_SOURCE_IMPLEMENTATION_REMAINS_VALID",
        passed,
        {"source_implementation_valid": True},
        {
            "implementation_id": report.get("implementation_id"),
            "runtime_case_count": cases.get("runtime_case_count"),
            "matrix_scope_lock_id": matrix.get("scope_lock_id"),
            "hard_denials": matrix.get("hard_denials", {}),
        },
        "TASK_3_SOURCE_IMPLEMENTATION_INVALID",
    )


def _validate_scope_lock_guardrails_case() -> dict[str, Any]:
    scope = _load_json(SOURCE_SCOPE_LOCK_PATH)
    passed = (
        validate_objective_scope_lock_report(scope)
        and scope.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and scope.get("scope_lock_id") == SCOPE_LOCK_ID
        and scope.get("scope_locked") is True
        and scope.get("scope_rules_valid") is True
        and scope.get("implementation_allowed_next") is True
        and scope.get("private_core_exposure_allowed") is False
        and scope.get("unverified_manuel_assumption_allowed") is False
        and scope.get("external_command_authority_allowed") is False
    )
    return _case(
        "TASK_2_SCOPE_LOCK_GUARDRAILS_REMAIN_VALID",
        passed,
        {"scope_lock_guardrails_valid": True},
        {
            "scope_lock_id": scope.get("scope_lock_id"),
            "scope_rules_valid": scope.get("scope_rules_valid"),
            "private_core_exposure_allowed": scope.get("private_core_exposure_allowed"),
            "unverified_manuel_assumption_allowed": scope.get("unverified_manuel_assumption_allowed"),
            "external_command_authority_allowed": scope.get("external_command_authority_allowed"),
        },
        "TASK_2_SCOPE_LOCK_GUARDRAILS_INVALID",
    )


def _validate_transition_and_budget_case() -> dict[str, Any]:
    report = _load_json(SOURCE_VALIDATION_REPORT_PATH)
    passed = (
        report.get("task_budget_max") == TASK_BUDGET_MAX == 8
        and report.get("current_task_number") == SOURCE_CURRENT_TASK_NUMBER == 4
        and CURRENT_TASK_NUMBER == 5
        and report.get("next_stage") == TASK_ID
        and NEXT_STAGE == "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_V1"
        and SOURCE_GENERATED_ARTIFACT_COUNT == 5
        and GENERATED_ARTIFACT_COUNT == 5
    )
    return _case(
        "TASK_5_TRANSITION_AND_BUDGET_VALID",
        passed,
        {"task_budget_max": 8, "source_current_task_number": 4, "current_task_number": 5},
        {
            "task_budget_max": report.get("task_budget_max"),
            "source_current_task_number": report.get("current_task_number"),
            "current_task_number": CURRENT_TASK_NUMBER,
            "source_next_stage": report.get("next_stage"),
            "next_stage": NEXT_STAGE,
        },
        "TASK_5_TRANSITION_AND_BUDGET_INVALID",
    )


def run_identity_boundary_fail_closed_regression_integration() -> dict[str, Any]:
    integration_cases = [
        _validate_validation_report_case(),
        _validate_runtime_stability_case(),
        _validate_artifact_set_case(),
        _validate_manifest_case(),
        _validate_validation_case_set_case(),
        _validate_direct_regression_probes_case(),
        _validate_source_implementation_case(),
        _validate_scope_lock_guardrails_case(),
        _validate_transition_and_budget_case(),
    ]

    pass_count = sum(1 for case in integration_cases if case["passed"])
    fail_count = len(integration_cases) - pass_count
    integration_passed = (
        len(integration_cases) == INTEGRATION_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    validation_report = _load_json(SOURCE_VALIDATION_REPORT_PATH)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "task_5_signature": task_5_signature(),
        "source_implementation_id": validation_report.get("source_implementation_id"),
        "source_implementation_signature": validation_report.get("source_implementation_signature"),
        "source_validation_id": validation_report.get("validation_id"),
        "source_validation_signature": validation_report.get("validation_signature"),
        "source_validation_status": validation_report.get("validation_status"),
        "source_validation_passed": validation_report.get("validation_passed"),
        "source_private_core_access_allowed_without_verified_manuel": validation_report.get("source_private_core_access_allowed_without_verified_manuel"),
        "source_unverified_manuel_assumption_allowed": validation_report.get("source_unverified_manuel_assumption_allowed"),
        "source_external_command_authority_allowed": validation_report.get("source_external_command_authority_allowed"),
        "integration_status": INTEGRATION_STATUS if integration_passed else "INVALID",
        "integration_case_count": len(integration_cases),
        "required_pass_count": REQUIRED_PASS_COUNT,
        "required_fail_count": REQUIRED_FAIL_COUNT,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "integration_passed": integration_passed,
        "integration_cases": integration_cases,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    report["integration_id"] = "MILESTONE-30-IDENTITY-BOUNDARY-INTEGRATION-" + _stable_digest(report)
    report["integration_signature"] = _stable_digest(
        {
            "integration_id": report["integration_id"],
            "source_implementation_id": report["source_implementation_id"],
            "source_implementation_signature": report["source_implementation_signature"],
            "source_validation_id": report["source_validation_id"],
            "source_validation_signature": report["source_validation_signature"],
            "task_4_signature": report["task_4_signature"],
            "task_5_signature": report["task_5_signature"],
            "integration_cases": integration_cases,
            "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
            "next_stage": NEXT_STAGE,
        }
    )
    return report


def validate_identity_boundary_regression_integration_report(report: Mapping[str, Any]) -> bool:
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
    if report.get("regression_integration_revision") != REGRESSION_INTEGRATION_REVISION:
        return False
    if report.get("task_4_signature") != task_4_signature():
        return False
    if report.get("task_5_signature") != task_5_signature():
        return False
    if report.get("source_validation_status") != "VALID":
        return False
    if report.get("source_validation_passed") is not True:
        return False
    if report.get("source_private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if report.get("source_unverified_manuel_assumption_allowed") is not False:
        return False
    if report.get("source_external_command_authority_allowed") is not False:
        return False
    if report.get("integration_status") != INTEGRATION_STATUS:
        return False
    if report.get("integration_case_count") != INTEGRATION_CASE_COUNT:
        return False
    if report.get("pass_count") != REQUIRED_PASS_COUNT:
        return False
    if report.get("fail_count") != REQUIRED_FAIL_COUNT:
        return False
    if report.get("integration_passed") is not True:
        return False
    if not all(case.get("passed") is True for case in report.get("integration_cases", [])):
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("integration_id") and report.get("integration_signature"))


def render_regression_integration_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 30 Task 5 Identity Boundary Fail-Closed Regression Integration",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"INTEGRATION_ID={report.get('integration_id')}",
        f"INTEGRATION_SIGNATURE={report.get('integration_signature')}",
        f"SOURCE_VALIDATION_ID={report.get('source_validation_id')}",
        f"SOURCE_VALIDATION_SIGNATURE={report.get('source_validation_signature')}",
        f"INTEGRATION_STATUS={report.get('integration_status')}",
        f"INTEGRATION_CASE_COUNT={report.get('integration_case_count')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Regression integration cases",
    ]
    for case in report.get("integration_cases", []):
        lines.append(f"- {case['case_id']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_5_artifacts(base_dir: str | Path = "examples/milestone-30/identity-boundary-fail-closed-regression-integration-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_identity_boundary_fail_closed_regression_integration()

    integration_cases = {
        "task_id": TASK_ID,
        "integration_id": report["integration_id"],
        "integration_status": report["integration_status"],
        "integration_case_count": report["integration_case_count"],
        "integration_cases": report["integration_cases"],
    }

    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_4_signature": task_4_signature(),
        "task_5_signature": task_5_signature(),
        "source_implementation_id": report["source_implementation_id"],
        "source_implementation_signature": report["source_implementation_signature"],
        "source_validation_id": report["source_validation_id"],
        "source_validation_signature": report["source_validation_signature"],
        "integration_id": report["integration_id"],
        "integration_signature": report["integration_signature"],
        "integration_status": report["integration_status"],
        "integration_passed": report["integration_passed"],
        "integration_case_count": report["integration_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-5-regression-integration-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-5-regression-integration-report.md").write_text(
        render_regression_integration_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-5-regression-integration-cases.json").write_text(
        json.dumps(integration_cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-5-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-5-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_30_TASK_5_IDENTITY_BOUNDARY_FAIL_CLOSED_REGRESSION_INTEGRATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
                f"VALIDATION_REVISION={VALIDATION_REVISION}",
                f"REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}",
                f"TASK_4_SIGNATURE={task_4_signature()}",
                f"TASK_5_SIGNATURE={task_5_signature()}",
                f"SOURCE_IMPLEMENTATION_ID={report['source_implementation_id']}",
                f"SOURCE_IMPLEMENTATION_SIGNATURE={report['source_implementation_signature']}",
                f"SOURCE_VALIDATION_ID={report['source_validation_id']}",
                f"SOURCE_VALIDATION_SIGNATURE={report['source_validation_signature']}",
                f"SOURCE_VALIDATION_STATUS={report['source_validation_status']}",
                f"SOURCE_VALIDATION_PASSED={str(report['source_validation_passed']).lower()}",
                f"SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(report['source_private_core_access_allowed_without_verified_manuel']).lower()}",
                f"SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['source_unverified_manuel_assumption_allowed']).lower()}",
                f"SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['source_external_command_authority_allowed']).lower()}",
                f"INTEGRATION_ID={report['integration_id']}",
                f"INTEGRATION_SIGNATURE={report['integration_signature']}",
                f"INTEGRATION_STATUS={report['integration_status']}",
                f"INTEGRATION_CASE_COUNT={report['integration_case_count']}",
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


def task_5_status_lines() -> tuple[str, ...]:
    report = run_identity_boundary_fail_closed_regression_integration()
    return (
        "MILESTONE_30_TASK_5_IDENTITY_BOUNDARY_FAIL_CLOSED_REGRESSION_INTEGRATION_READY=true",
        f"MILESTONE_30_TASK_5_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_30_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_30_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_30_TASK_5_IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
        f"MILESTONE_30_TASK_5_VALIDATION_REVISION={VALIDATION_REVISION}",
        f"MILESTONE_30_TASK_5_REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}",
        f"MILESTONE_30_TASK_5_TASK_4_SIGNATURE={task_4_signature()}",
        f"MILESTONE_30_TASK_5_TASK_5_SIGNATURE={task_5_signature()}",
        f"MILESTONE_30_TASK_5_SOURCE_IMPLEMENTATION_ID={report['source_implementation_id']}",
        f"MILESTONE_30_TASK_5_SOURCE_IMPLEMENTATION_SIGNATURE={report['source_implementation_signature']}",
        f"MILESTONE_30_TASK_5_SOURCE_VALIDATION_ID={report['source_validation_id']}",
        f"MILESTONE_30_TASK_5_SOURCE_VALIDATION_SIGNATURE={report['source_validation_signature']}",
        f"MILESTONE_30_TASK_5_SOURCE_VALIDATION_STATUS={report['source_validation_status']}",
        f"MILESTONE_30_TASK_5_SOURCE_VALIDATION_PASSED={str(report['source_validation_passed']).lower()}",
        f"MILESTONE_30_TASK_5_SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(report['source_private_core_access_allowed_without_verified_manuel']).lower()}",
        f"MILESTONE_30_TASK_5_SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['source_unverified_manuel_assumption_allowed']).lower()}",
        f"MILESTONE_30_TASK_5_SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['source_external_command_authority_allowed']).lower()}",
        f"MILESTONE_30_TASK_5_INTEGRATION_ID={report['integration_id']}",
        f"MILESTONE_30_TASK_5_INTEGRATION_SIGNATURE={report['integration_signature']}",
        f"MILESTONE_30_TASK_5_INTEGRATION_STATUS={report['integration_status']}",
        f"MILESTONE_30_TASK_5_INTEGRATION_CASE_COUNT={report['integration_case_count']}",
        f"MILESTONE_30_TASK_5_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_30_TASK_5_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_30_TASK_5_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_30_TASK_5_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_30_TASK_5_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_30_TASK_5_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_5_artifacts()
    for line in task_5_status_lines():
        print(line)
