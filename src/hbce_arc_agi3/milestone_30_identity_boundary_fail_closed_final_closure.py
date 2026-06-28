from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_30_governed_opening import (
    TASK_ID as TASK_1_ID,
    task_1_signature,
    validate_governed_opening_report,
)
from hbce_arc_agi3.milestone_30_objective_scope_lock import (
    TASK_ID as TASK_2_ID,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    task_2_signature,
    validate_objective_scope_lock_report,
)
from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed import (
    TASK_ID as TASK_3_ID,
    IMPLEMENTATION_REVISION,
    task_3_signature,
    validate_identity_boundary_implementation_report,
)
from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed_validation import (
    TASK_ID as TASK_4_ID,
    VALIDATION_REVISION,
    task_4_signature,
    validate_identity_boundary_validation_report,
)
from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed_regression_integration import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    INTEGRATION_CASE_COUNT as SOURCE_INTEGRATION_CASE_COUNT,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    REGRESSION_INTEGRATION_REVISION,
    REQUIRED_FAIL_COUNT as SOURCE_REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT as SOURCE_REQUIRED_PASS_COUNT,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    run_identity_boundary_fail_closed_regression_integration,
    task_5_signature,
    validate_identity_boundary_regression_integration_report,
)


TASK_ID = "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_V1"
FINAL_CLOSURE_REVISION = "MILESTONE_30_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_V1"
MILESTONE_ID = "MILESTONE_30"

FINAL_TASK_NUMBER = 6
CURRENT_TASK_NUMBER = 6

NEXT_STAGE = "MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

CLOSURE_STATUS = "CLOSED"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"

MILESTONE_CLOSED = True
READY_FOR_NEXT_MILESTONE = True
IMPLEMENTATION_COMPLETE = True
VALIDATION_COMPLETE = True
REGRESSION_INTEGRATION_COMPLETE = True

TASK_7_UNUSED = True
TASK_8_UNUSED = True

CLOSURE_CASE_COUNT = 10
REQUIRED_PASS_COUNT = 10
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

SOURCE_INTEGRATION_REPORT_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-regression-integration-v1/task-5-regression-integration-report.json")
SOURCE_INTEGRATION_CASES_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-regression-integration-v1/task-5-regression-integration-cases.json")
SOURCE_INTEGRATION_MANIFEST_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-regression-integration-v1/task-5-manifest.json")
SOURCE_INTEGRATION_INDEX_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-regression-integration-v1/task-5-index.txt")
SOURCE_INTEGRATION_MARKDOWN_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-regression-integration-v1/task-5-regression-integration-report.md")

TASK_1_REPORT_PATH = Path("examples/milestone-30/governed-opening-with-task-budget-v1/task-1-governed-opening.json")
TASK_2_REPORT_PATH = Path("examples/milestone-30/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.json")
TASK_3_REPORT_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1/task-3-identity-boundary-implementation.json")
TASK_4_REPORT_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-validation-v1/task-4-validation-report.json")
TASK_5_REPORT_PATH = SOURCE_INTEGRATION_REPORT_PATH


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_6_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "milestone_id": MILESTONE_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "implementation_revision": IMPLEMENTATION_REVISION,
            "validation_revision": VALIDATION_REVISION,
            "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
            "final_closure_revision": FINAL_CLOSURE_REVISION,
            "task_1_signature": task_1_signature(),
            "task_2_signature": task_2_signature(),
            "task_3_signature": task_3_signature(),
            "task_4_signature": task_4_signature(),
            "task_5_signature": task_5_signature(),
            "task_budget_max": TASK_BUDGET_MAX,
            "final_task_number": FINAL_TASK_NUMBER,
            "process_status": PROCESS_STATUS,
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


def build_integration_snapshot() -> dict[str, Any]:
    runtime = run_identity_boundary_fail_closed_regression_integration()
    persisted = _load_json(SOURCE_INTEGRATION_REPORT_PATH)

    runtime_valid = validate_identity_boundary_regression_integration_report(runtime)
    persisted_valid = validate_identity_boundary_regression_integration_report(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_integration_id": runtime.get("integration_id"),
        "persisted_integration_id": persisted.get("integration_id"),
        "runtime_integration_signature": runtime.get("integration_signature"),
        "persisted_integration_signature": persisted.get("integration_signature"),
        "runtime_task_5_signature": runtime.get("task_5_signature"),
        "persisted_task_5_signature": persisted.get("task_5_signature"),
        "selected_objective_id": persisted.get("selected_objective_id"),
        "scope_lock_id": persisted.get("scope_lock_id"),
        "source_validation_status": persisted.get("source_validation_status"),
        "source_validation_passed": persisted.get("source_validation_passed"),
        "source_private_core_access_allowed_without_verified_manuel": persisted.get("source_private_core_access_allowed_without_verified_manuel"),
        "source_unverified_manuel_assumption_allowed": persisted.get("source_unverified_manuel_assumption_allowed"),
        "source_external_command_authority_allowed": persisted.get("source_external_command_authority_allowed"),
        "integration_status": persisted.get("integration_status"),
        "integration_case_count": persisted.get("integration_case_count"),
        "pass_count": persisted.get("pass_count"),
        "fail_count": persisted.get("fail_count"),
        "integration_passed": persisted.get("integration_passed"),
        "task_budget_max": persisted.get("task_budget_max"),
        "current_task_number": persisted.get("current_task_number"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_integration": (
            runtime.get("integration_id") == persisted.get("integration_id")
            and runtime.get("integration_signature") == persisted.get("integration_signature")
            and runtime.get("task_5_signature") == persisted.get("task_5_signature") == task_5_signature()
        ),
    }


def validate_integration_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("source_validation_status") != "VALID":
        return False
    if snapshot.get("source_validation_passed") is not True:
        return False
    if snapshot.get("source_private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if snapshot.get("source_unverified_manuel_assumption_allowed") is not False:
        return False
    if snapshot.get("source_external_command_authority_allowed") is not False:
        return False
    if snapshot.get("integration_status") != "VALID":
        return False
    if snapshot.get("integration_case_count") != SOURCE_INTEGRATION_CASE_COUNT:
        return False
    if snapshot.get("pass_count") != SOURCE_REQUIRED_PASS_COUNT:
        return False
    if snapshot.get("fail_count") != SOURCE_REQUIRED_FAIL_COUNT:
        return False
    if snapshot.get("integration_passed") is not True:
        return False
    if snapshot.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if snapshot.get("current_task_number") != SOURCE_CURRENT_TASK_NUMBER:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_integration"))


def _validate_task_chain_reports_case() -> dict[str, Any]:
    task_1 = _load_json(TASK_1_REPORT_PATH)
    task_2 = _load_json(TASK_2_REPORT_PATH)
    task_3 = _load_json(TASK_3_REPORT_PATH)
    task_4 = _load_json(TASK_4_REPORT_PATH)
    task_5 = _load_json(TASK_5_REPORT_PATH)

    passed = (
        validate_governed_opening_report(task_1)
        and validate_objective_scope_lock_report(task_2)
        and validate_identity_boundary_implementation_report(task_3)
        and validate_identity_boundary_validation_report(task_4)
        and validate_identity_boundary_regression_integration_report(task_5)
        and task_1.get("next_stage") == TASK_2_ID
        and task_2.get("next_stage") == TASK_3_ID
        and task_3.get("next_stage") == TASK_4_ID
        and task_4.get("next_stage") == SOURCE_TASK_ID
        and task_5.get("next_stage") == TASK_ID
        and task_1.get("task_1_signature") == task_1_signature()
        and task_2.get("task_2_signature") == task_2_signature()
        and task_3.get("task_3_signature") == task_3_signature()
        and task_4.get("task_4_signature") == task_4_signature()
        and task_5.get("task_5_signature") == task_5_signature()
    )
    return _case(
        "MILESTONE_30_TASK_CHAIN_REPORTS_VALID",
        passed,
        {"task_chain_valid": True, "task_count": 5},
        {
            "task_1_next": task_1.get("next_stage"),
            "task_2_next": task_2.get("next_stage"),
            "task_3_next": task_3.get("next_stage"),
            "task_4_next": task_4.get("next_stage"),
            "task_5_next": task_5.get("next_stage"),
        },
        "MILESTONE_30_TASK_CHAIN_REPORTS_INVALID",
    )


def _validate_integration_report_case() -> dict[str, Any]:
    report = _load_json(SOURCE_INTEGRATION_REPORT_PATH)
    passed = (
        validate_identity_boundary_regression_integration_report(report)
        and report.get("integration_status") == "VALID"
        and report.get("integration_passed") is True
        and report.get("pass_count") == 9
        and report.get("fail_count") == 0
        and report.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_5_REGRESSION_INTEGRATION_REPORT_VALID",
        passed,
        {"integration_status": "VALID", "integration_passed": True, "pass_count": 9, "fail_count": 0},
        {
            "integration_status": report.get("integration_status"),
            "integration_passed": report.get("integration_passed"),
            "pass_count": report.get("pass_count"),
            "fail_count": report.get("fail_count"),
            "next_stage": report.get("next_stage"),
        },
        "TASK_5_REGRESSION_INTEGRATION_REPORT_INVALID",
    )


def _validate_runtime_stability_case() -> dict[str, Any]:
    snapshot = build_integration_snapshot()
    passed = validate_integration_snapshot(snapshot)
    return _case(
        "TASK_5_REGRESSION_INTEGRATION_RUNTIME_STABILITY_VALID",
        passed,
        {"stable_integration": True},
        snapshot,
        "TASK_5_REGRESSION_INTEGRATION_RUNTIME_STABILITY_INVALID",
    )


def _validate_artifact_set_case() -> dict[str, Any]:
    paths = (
        SOURCE_INTEGRATION_REPORT_PATH,
        SOURCE_INTEGRATION_CASES_PATH,
        SOURCE_INTEGRATION_MANIFEST_PATH,
        SOURCE_INTEGRATION_INDEX_PATH,
        SOURCE_INTEGRATION_MARKDOWN_PATH,
    )
    missing = [str(path) for path in paths if not path.exists()]
    readable = []
    for path in paths:
        if path.exists():
            readable.append(path.read_text(encoding="utf-8") != "")
    passed = not missing and all(readable)
    return _case(
        "TASK_5_REGRESSION_INTEGRATION_ARTIFACT_SET_PRESENT",
        passed,
        {"artifact_count": 5, "missing": []},
        {"artifact_count": len(paths), "missing": missing, "readable_count": sum(1 for item in readable if item)},
        "TASK_5_REGRESSION_INTEGRATION_ARTIFACT_SET_INCOMPLETE",
    )


def _validate_manifest_case() -> dict[str, Any]:
    report = _load_json(SOURCE_INTEGRATION_REPORT_PATH)
    manifest = _load_json(SOURCE_INTEGRATION_MANIFEST_PATH)
    passed = (
        manifest.get("task_id") == SOURCE_TASK_ID
        and manifest.get("source_task_id") == report.get("source_task_id")
        and manifest.get("selected_objective_id") == report.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and manifest.get("scope_lock_id") == report.get("scope_lock_id") == SCOPE_LOCK_ID
        and manifest.get("integration_id") == report.get("integration_id")
        and manifest.get("integration_signature") == report.get("integration_signature")
        and manifest.get("source_validation_id") == report.get("source_validation_id")
        and manifest.get("source_validation_signature") == report.get("source_validation_signature")
        and manifest.get("integration_status") == report.get("integration_status") == "VALID"
        and manifest.get("integration_passed") is True
        and manifest.get("pass_count") == report.get("pass_count") == 9
        and manifest.get("fail_count") == report.get("fail_count") == 0
        and manifest.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_5_REGRESSION_INTEGRATION_MANIFEST_CONSISTENCY_VALID",
        passed,
        {"manifest_matches_integration_report": True},
        {
            "manifest_integration_id": manifest.get("integration_id"),
            "report_integration_id": report.get("integration_id"),
            "manifest_status": manifest.get("integration_status"),
            "manifest_next_stage": manifest.get("next_stage"),
        },
        "TASK_5_REGRESSION_INTEGRATION_MANIFEST_CONSISTENCY_INVALID",
    )


def _validate_integration_case_set_case() -> dict[str, Any]:
    report = _load_json(SOURCE_INTEGRATION_REPORT_PATH)
    cases = _load_json(SOURCE_INTEGRATION_CASES_PATH)
    expected_case_ids = {
        "TASK_4_VALIDATION_REPORT_VALID",
        "TASK_4_VALIDATION_RUNTIME_STABILITY_VALID",
        "TASK_4_VALIDATION_ARTIFACT_SET_PRESENT",
        "TASK_4_VALIDATION_MANIFEST_CONSISTENCY_VALID",
        "TASK_4_VALIDATION_CASE_SET_VALID",
        "IDENTITY_BOUNDARY_DIRECT_REGRESSION_PROBES_VALID",
        "TASK_3_SOURCE_IMPLEMENTATION_REMAINS_VALID",
        "TASK_2_SCOPE_LOCK_GUARDRAILS_REMAIN_VALID",
        "TASK_5_TRANSITION_AND_BUDGET_VALID",
    }
    observed_case_ids = {case.get("case_id") for case in cases.get("integration_cases", [])}
    passed = (
        cases.get("task_id") == SOURCE_TASK_ID
        and cases.get("integration_id") == report.get("integration_id")
        and cases.get("integration_status") == "VALID"
        and cases.get("integration_case_count") == SOURCE_INTEGRATION_CASE_COUNT
        and observed_case_ids == expected_case_ids
        and all(case.get("passed") is True for case in cases.get("integration_cases", []))
        and all(case.get("failure_reason") == "NONE" for case in cases.get("integration_cases", []))
    )
    return _case(
        "TASK_5_REGRESSION_INTEGRATION_CASE_SET_VALID",
        passed,
        {"case_ids": sorted(expected_case_ids), "integration_case_count": 9},
        {"case_ids": sorted(observed_case_ids), "integration_case_count": cases.get("integration_case_count")},
        "TASK_5_REGRESSION_INTEGRATION_CASE_SET_INVALID",
    )


def _validate_guardrail_final_state_case() -> dict[str, Any]:
    integration = _load_json(SOURCE_INTEGRATION_REPORT_PATH)
    implementation = _load_json(TASK_3_REPORT_PATH)
    validation = _load_json(TASK_4_REPORT_PATH)
    scope = _load_json(TASK_2_REPORT_PATH)

    passed = (
        integration.get("source_private_core_access_allowed_without_verified_manuel") is False
        and integration.get("source_unverified_manuel_assumption_allowed") is False
        and integration.get("source_external_command_authority_allowed") is False
        and validation.get("source_private_core_access_allowed_without_verified_manuel") is False
        and validation.get("source_unverified_manuel_assumption_allowed") is False
        and validation.get("source_external_command_authority_allowed") is False
        and implementation.get("private_core_access_allowed_without_verified_manuel") is False
        and implementation.get("unverified_manuel_assumption_allowed") is False
        and implementation.get("external_command_authority_allowed") is False
        and scope.get("private_core_exposure_allowed") is False
        and scope.get("unverified_manuel_assumption_allowed") is False
        and scope.get("external_command_authority_allowed") is False
    )
    return _case(
        "MILESTONE_30_FAIL_CLOSED_GUARDRAIL_FINAL_STATE_VALID",
        passed,
        {
            "private_core_access_without_verified_manuel": False,
            "unverified_manuel_assumption": False,
            "external_command_authority": False,
        },
        {
            "integration_guardrails": {
                "private_core": integration.get("source_private_core_access_allowed_without_verified_manuel"),
                "unverified_manuel": integration.get("source_unverified_manuel_assumption_allowed"),
                "external_command": integration.get("source_external_command_authority_allowed"),
            },
            "scope_guardrails": {
                "private_core": scope.get("private_core_exposure_allowed"),
                "unverified_manuel": scope.get("unverified_manuel_assumption_allowed"),
                "external_command": scope.get("external_command_authority_allowed"),
            },
        },
        "MILESTONE_30_FAIL_CLOSED_GUARDRAIL_FINAL_STATE_INVALID",
    )


def _validate_task_budget_case() -> dict[str, Any]:
    task_1 = _load_json(TASK_1_REPORT_PATH)
    task_5 = _load_json(TASK_5_REPORT_PATH)
    passed = (
        task_1.get("task_budget_max") == TASK_BUDGET_MAX == 8
        and task_5.get("task_budget_max") == TASK_BUDGET_MAX
        and task_5.get("current_task_number") == SOURCE_CURRENT_TASK_NUMBER == 5
        and FINAL_TASK_NUMBER == 6
        and TASK_7_UNUSED is True
        and TASK_8_UNUSED is True
        and PROCESS_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    )
    return _case(
        "MILESTONE_30_TASK_BUDGET_FINAL_STATE_VALID",
        passed,
        {"task_budget_max": 8, "final_task_number": 6, "task_7_unused": True, "task_8_unused": True},
        {
            "task_1_budget": task_1.get("task_budget_max"),
            "task_5_budget": task_5.get("task_budget_max"),
            "task_5_number": task_5.get("current_task_number"),
            "final_task_number": FINAL_TASK_NUMBER,
            "process_status": PROCESS_STATUS,
        },
        "MILESTONE_30_TASK_BUDGET_FINAL_STATE_INVALID",
    )


def _validate_final_transition_case() -> dict[str, Any]:
    task_5 = _load_json(TASK_5_REPORT_PATH)
    passed = (
        task_5.get("next_stage") == TASK_ID
        and NEXT_STAGE == "MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
        and MILESTONE_CLOSED is True
        and READY_FOR_NEXT_MILESTONE is True
    )
    return _case(
        "MILESTONE_30_FINAL_TRANSITION_VALID",
        passed,
        {"milestone_closed": True, "ready_for_next_milestone": True, "next_stage": NEXT_STAGE},
        {"task_5_next_stage": task_5.get("next_stage"), "closure_next_stage": NEXT_STAGE},
        "MILESTONE_30_FINAL_TRANSITION_INVALID",
    )


def _validate_status_closure_case() -> dict[str, Any]:
    passed = (
        CLOSURE_STATUS == "CLOSED"
        and TECHNICAL_STATUS == "PASS"
        and MILESTONE_CLOSED is True
        and IMPLEMENTATION_COMPLETE is True
        and VALIDATION_COMPLETE is True
        and REGRESSION_INTEGRATION_COMPLETE is True
    )
    return _case(
        "MILESTONE_30_STATUS_CLOSURE_VALID",
        passed,
        {"closure_status": "CLOSED", "technical_status": "PASS"},
        {"closure_status": CLOSURE_STATUS, "technical_status": TECHNICAL_STATUS, "process_status": PROCESS_STATUS},
        "MILESTONE_30_STATUS_CLOSURE_INVALID",
    )


def _validate_signature_chain_case() -> dict[str, Any]:
    task_1 = _load_json(TASK_1_REPORT_PATH)
    task_2 = _load_json(TASK_2_REPORT_PATH)
    task_3 = _load_json(TASK_3_REPORT_PATH)
    task_4 = _load_json(TASK_4_REPORT_PATH)
    task_5 = _load_json(TASK_5_REPORT_PATH)
    passed = (
        task_1.get("task_1_signature") == task_1_signature()
        and task_2.get("task_2_signature") == task_2_signature()
        and task_3.get("task_3_signature") == task_3_signature()
        and task_4.get("task_4_signature") == task_4_signature()
        and task_5.get("task_5_signature") == task_5_signature()
        and task_6_signature() != task_5_signature()
    )
    return _case(
        "MILESTONE_30_SIGNATURE_CHAIN_VALID",
        passed,
        {"signature_chain_valid": True},
        {
            "task_1_signature": task_1.get("task_1_signature"),
            "task_2_signature": task_2.get("task_2_signature"),
            "task_3_signature": task_3.get("task_3_signature"),
            "task_4_signature": task_4.get("task_4_signature"),
            "task_5_signature": task_5.get("task_5_signature"),
            "task_6_signature": task_6_signature(),
        },
        "MILESTONE_30_SIGNATURE_CHAIN_INVALID",
    )


def _validate_generated_artifact_count_case() -> dict[str, Any]:
    passed = (
        SOURCE_GENERATED_ARTIFACT_COUNT == 5
        and GENERATED_ARTIFACT_COUNT == 5
        and TASK_1_REPORT_PATH.exists()
        and TASK_2_REPORT_PATH.exists()
        and TASK_3_REPORT_PATH.exists()
        and TASK_4_REPORT_PATH.exists()
        and TASK_5_REPORT_PATH.exists()
    )
    return _case(
        "MILESTONE_30_GENERATED_ARTIFACT_COUNT_VALID",
        passed,
        {"source_generated_artifact_count": 5, "closure_generated_artifact_count": 5},
        {"source_generated_artifact_count": SOURCE_GENERATED_ARTIFACT_COUNT, "closure_generated_artifact_count": GENERATED_ARTIFACT_COUNT},
        "MILESTONE_30_GENERATED_ARTIFACT_COUNT_INVALID",
    )


def run_identity_boundary_fail_closed_final_closure() -> dict[str, Any]:
    closure_cases = [
        _validate_task_chain_reports_case(),
        _validate_integration_report_case(),
        _validate_runtime_stability_case(),
        _validate_artifact_set_case(),
        _validate_manifest_case(),
        _validate_integration_case_set_case(),
        _validate_guardrail_final_state_case(),
        _validate_task_budget_case(),
        _validate_final_transition_case(),
        _validate_status_closure_case(),
        _validate_signature_chain_case(),
        _validate_generated_artifact_count_case(),
    ]

    pass_count = sum(1 for case in closure_cases if case["passed"])
    fail_count = len(closure_cases) - pass_count
    closure_passed = pass_count == len(closure_cases) and fail_count == 0

    integration = _load_json(SOURCE_INTEGRATION_REPORT_PATH)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "final_closure_revision": FINAL_CLOSURE_REVISION,
        "task_1_signature": task_1_signature(),
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "task_5_signature": task_5_signature(),
        "task_6_signature": task_6_signature(),
        "source_integration_id": integration.get("integration_id"),
        "source_integration_signature": integration.get("integration_signature"),
        "source_integration_status": integration.get("integration_status"),
        "source_integration_passed": integration.get("integration_passed"),
        "source_private_core_access_allowed_without_verified_manuel": integration.get("source_private_core_access_allowed_without_verified_manuel"),
        "source_unverified_manuel_assumption_allowed": integration.get("source_unverified_manuel_assumption_allowed"),
        "source_external_command_authority_allowed": integration.get("source_external_command_authority_allowed"),
        "closure_status": CLOSURE_STATUS,
        "technical_status": TECHNICAL_STATUS,
        "process_status": PROCESS_STATUS,
        "milestone_closed": MILESTONE_CLOSED,
        "ready_for_next_milestone": READY_FOR_NEXT_MILESTONE,
        "implementation_complete": IMPLEMENTATION_COMPLETE,
        "validation_complete": VALIDATION_COMPLETE,
        "regression_integration_complete": REGRESSION_INTEGRATION_COMPLETE,
        "closure_case_count": len(closure_cases),
        "required_pass_count": len(closure_cases),
        "required_fail_count": 0,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "closure_passed": closure_passed,
        "closure_cases": closure_cases,
        "task_budget_max": TASK_BUDGET_MAX,
        "final_task_number": FINAL_TASK_NUMBER,
        "task_7_unused": TASK_7_UNUSED,
        "task_8_unused": TASK_8_UNUSED,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    report["closure_id"] = "MILESTONE-30-IDENTITY-BOUNDARY-FINAL-CLOSURE-" + _stable_digest(report)
    report["closure_signature"] = _stable_digest(
        {
            "closure_id": report["closure_id"],
            "source_integration_id": report["source_integration_id"],
            "source_integration_signature": report["source_integration_signature"],
            "task_5_signature": report["task_5_signature"],
            "task_6_signature": report["task_6_signature"],
            "closure_cases": closure_cases,
            "process_status": PROCESS_STATUS,
            "next_stage": NEXT_STAGE,
        }
    )
    return report


def validate_final_closure_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("final_closure_revision") != FINAL_CLOSURE_REVISION:
        return False
    if report.get("task_1_signature") != task_1_signature():
        return False
    if report.get("task_2_signature") != task_2_signature():
        return False
    if report.get("task_3_signature") != task_3_signature():
        return False
    if report.get("task_4_signature") != task_4_signature():
        return False
    if report.get("task_5_signature") != task_5_signature():
        return False
    if report.get("task_6_signature") != task_6_signature():
        return False
    if report.get("source_integration_status") != "VALID":
        return False
    if report.get("source_integration_passed") is not True:
        return False
    if report.get("source_private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if report.get("source_unverified_manuel_assumption_allowed") is not False:
        return False
    if report.get("source_external_command_authority_allowed") is not False:
        return False
    if report.get("closure_status") != CLOSURE_STATUS:
        return False
    if report.get("technical_status") != TECHNICAL_STATUS:
        return False
    if report.get("process_status") != PROCESS_STATUS:
        return False
    if report.get("milestone_closed") is not True:
        return False
    if report.get("ready_for_next_milestone") is not True:
        return False
    if report.get("implementation_complete") is not True:
        return False
    if report.get("validation_complete") is not True:
        return False
    if report.get("regression_integration_complete") is not True:
        return False
    if report.get("pass_count") != report.get("required_pass_count"):
        return False
    if report.get("fail_count") != 0:
        return False
    if report.get("closure_passed") is not True:
        return False
    if not all(case.get("passed") is True for case in report.get("closure_cases", [])):
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("final_task_number") != FINAL_TASK_NUMBER:
        return False
    if report.get("task_7_unused") is not True:
        return False
    if report.get("task_8_unused") is not True:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("closure_id") and report.get("closure_signature"))


def render_final_closure_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 30 Task 6 Identity Boundary Fail-Closed Final Closure",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"MILESTONE_ID={report.get('milestone_id')}",
        f"CLOSURE_ID={report.get('closure_id')}",
        f"CLOSURE_SIGNATURE={report.get('closure_signature')}",
        f"SOURCE_INTEGRATION_ID={report.get('source_integration_id')}",
        f"SOURCE_INTEGRATION_SIGNATURE={report.get('source_integration_signature')}",
        f"CLOSURE_STATUS={report.get('closure_status')}",
        f"TECHNICAL_STATUS={report.get('technical_status')}",
        f"PROCESS_STATUS={report.get('process_status')}",
        f"MILESTONE_CLOSED={str(report.get('milestone_closed')).lower()}",
        f"READY_FOR_NEXT_MILESTONE={str(report.get('ready_for_next_milestone')).lower()}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Closure cases",
    ]
    for case in report.get("closure_cases", []):
        lines.append(f"- {case['case_id']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_6_artifacts(base_dir: str | Path = "examples/milestone-30/identity-boundary-fail-closed-final-closure-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_identity_boundary_fail_closed_final_closure()

    closure_cases = {
        "task_id": TASK_ID,
        "closure_id": report["closure_id"],
        "closure_status": report["closure_status"],
        "closure_case_count": report["closure_case_count"],
        "closure_cases": report["closure_cases"],
    }

    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "final_closure_revision": FINAL_CLOSURE_REVISION,
        "task_1_signature": task_1_signature(),
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "task_5_signature": task_5_signature(),
        "task_6_signature": task_6_signature(),
        "source_integration_id": report["source_integration_id"],
        "source_integration_signature": report["source_integration_signature"],
        "closure_id": report["closure_id"],
        "closure_signature": report["closure_signature"],
        "closure_status": report["closure_status"],
        "technical_status": report["technical_status"],
        "process_status": report["process_status"],
        "milestone_closed": report["milestone_closed"],
        "ready_for_next_milestone": report["ready_for_next_milestone"],
        "closure_passed": report["closure_passed"],
        "closure_case_count": report["closure_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "task_budget_max": TASK_BUDGET_MAX,
        "final_task_number": FINAL_TASK_NUMBER,
        "task_7_unused": TASK_7_UNUSED,
        "task_8_unused": TASK_8_UNUSED,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-6-final-closure-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-6-final-closure-report.md").write_text(
        render_final_closure_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-6-closure-cases.json").write_text(
        json.dumps(closure_cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-6-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-6-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}",
                f"TASK_1_SIGNATURE={task_1_signature()}",
                f"TASK_2_SIGNATURE={task_2_signature()}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"TASK_4_SIGNATURE={task_4_signature()}",
                f"TASK_5_SIGNATURE={task_5_signature()}",
                f"TASK_6_SIGNATURE={task_6_signature()}",
                f"SOURCE_INTEGRATION_ID={report['source_integration_id']}",
                f"SOURCE_INTEGRATION_SIGNATURE={report['source_integration_signature']}",
                f"SOURCE_INTEGRATION_STATUS={report['source_integration_status']}",
                f"SOURCE_INTEGRATION_PASSED={str(report['source_integration_passed']).lower()}",
                f"SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(report['source_private_core_access_allowed_without_verified_manuel']).lower()}",
                f"SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['source_unverified_manuel_assumption_allowed']).lower()}",
                f"SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['source_external_command_authority_allowed']).lower()}",
                f"CLOSURE_ID={report['closure_id']}",
                f"CLOSURE_SIGNATURE={report['closure_signature']}",
                f"CLOSURE_STATUS={report['closure_status']}",
                f"TECHNICAL_STATUS={report['technical_status']}",
                f"PROCESS_STATUS={report['process_status']}",
                f"MILESTONE_CLOSED={str(report['milestone_closed']).lower()}",
                f"READY_FOR_NEXT_MILESTONE={str(report['ready_for_next_milestone']).lower()}",
                f"IMPLEMENTATION_COMPLETE={str(report['implementation_complete']).lower()}",
                f"VALIDATION_COMPLETE={str(report['validation_complete']).lower()}",
                f"REGRESSION_INTEGRATION_COMPLETE={str(report['regression_integration_complete']).lower()}",
                f"CLOSURE_CASE_COUNT={report['closure_case_count']}",
                f"PASS_COUNT={report['pass_count']}",
                f"FAIL_COUNT={report['fail_count']}",
                f"CLOSURE_PASSED={str(report['closure_passed']).lower()}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"FINAL_TASK_NUMBER={FINAL_TASK_NUMBER}",
                f"TASK_7_UNUSED={str(TASK_7_UNUSED).lower()}",
                f"TASK_8_UNUSED={str(TASK_8_UNUSED).lower()}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_6_status_lines() -> tuple[str, ...]:
    report = run_identity_boundary_fail_closed_final_closure()
    return (
        "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_READY=true",
        f"MILESTONE_30_TASK_6_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_30_TASK_6_MILESTONE_ID={MILESTONE_ID}",
        f"MILESTONE_30_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_30_TASK_6_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_30_TASK_6_FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}",
        f"MILESTONE_30_TASK_6_TASK_1_SIGNATURE={task_1_signature()}",
        f"MILESTONE_30_TASK_6_TASK_2_SIGNATURE={task_2_signature()}",
        f"MILESTONE_30_TASK_6_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_30_TASK_6_TASK_4_SIGNATURE={task_4_signature()}",
        f"MILESTONE_30_TASK_6_TASK_5_SIGNATURE={task_5_signature()}",
        f"MILESTONE_30_TASK_6_TASK_6_SIGNATURE={task_6_signature()}",
        f"MILESTONE_30_TASK_6_SOURCE_INTEGRATION_ID={report['source_integration_id']}",
        f"MILESTONE_30_TASK_6_SOURCE_INTEGRATION_SIGNATURE={report['source_integration_signature']}",
        f"MILESTONE_30_TASK_6_SOURCE_INTEGRATION_STATUS={report['source_integration_status']}",
        f"MILESTONE_30_TASK_6_SOURCE_INTEGRATION_PASSED={str(report['source_integration_passed']).lower()}",
        f"MILESTONE_30_TASK_6_SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(report['source_private_core_access_allowed_without_verified_manuel']).lower()}",
        f"MILESTONE_30_TASK_6_SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['source_unverified_manuel_assumption_allowed']).lower()}",
        f"MILESTONE_30_TASK_6_SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['source_external_command_authority_allowed']).lower()}",
        f"MILESTONE_30_TASK_6_CLOSURE_ID={report['closure_id']}",
        f"MILESTONE_30_TASK_6_CLOSURE_SIGNATURE={report['closure_signature']}",
        f"MILESTONE_30_TASK_6_CLOSURE_STATUS={report['closure_status']}",
        f"MILESTONE_30_TASK_6_TECHNICAL_STATUS={report['technical_status']}",
        f"MILESTONE_30_TASK_6_PROCESS_STATUS={report['process_status']}",
        f"MILESTONE_30_TASK_6_MILESTONE_CLOSED={str(report['milestone_closed']).lower()}",
        f"MILESTONE_30_TASK_6_READY_FOR_NEXT_MILESTONE={str(report['ready_for_next_milestone']).lower()}",
        f"MILESTONE_30_TASK_6_IMPLEMENTATION_COMPLETE={str(report['implementation_complete']).lower()}",
        f"MILESTONE_30_TASK_6_VALIDATION_COMPLETE={str(report['validation_complete']).lower()}",
        f"MILESTONE_30_TASK_6_REGRESSION_INTEGRATION_COMPLETE={str(report['regression_integration_complete']).lower()}",
        f"MILESTONE_30_TASK_6_CLOSURE_CASE_COUNT={report['closure_case_count']}",
        f"MILESTONE_30_TASK_6_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_30_TASK_6_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_30_TASK_6_CLOSURE_PASSED={str(report['closure_passed']).lower()}",
        f"MILESTONE_30_TASK_6_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_30_TASK_6_FINAL_TASK_NUMBER={FINAL_TASK_NUMBER}",
        f"MILESTONE_30_TASK_6_TASK_7_UNUSED={str(TASK_7_UNUSED).lower()}",
        f"MILESTONE_30_TASK_6_TASK_8_UNUSED={str(TASK_8_UNUSED).lower()}",
        f"MILESTONE_30_TASK_6_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_30_TASK_6_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_6_artifacts()
    for line in task_6_status_lines():
        print(line)
