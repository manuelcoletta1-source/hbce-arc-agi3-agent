from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle import (
    validate_query_result_evidence_bundle,
)
from hbce_arc_agi3.milestone_29_query_result_evidence_bundle_validation import (
    validate_validation_report,
)
from hbce_arc_agi3.milestone_29_query_result_evidence_bundle_regression_integration import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    EVIDENCE_BUNDLE_REVISION,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    INTEGRATION_CASE_COUNT,
    INTEGRATION_STATUS,
    MILESTONE_ID,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    REGRESSION_INTEGRATION_REVISION,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_INTEGRATION_TASK_ID,
    VALIDATION_REVISION,
    run_query_result_evidence_bundle_regression_integration,
    task_5_signature,
    validate_regression_integration_report,
)


TASK_ID = "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_V1"
FINAL_CLOSURE_REVISION = "MILESTONE_29_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_V1"

CURRENT_TASK_NUMBER = 6
FINAL_TASK_NUMBER = 6
TASK_7_USED = False
TASK_8_USED = False

CLOSURE_STATUS = "CLOSED"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"

CLOSURE_CASE_COUNT = 8
REQUIRED_PASS_COUNT = 8
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

MILESTONE_CLOSED = True
READY_FOR_NEXT_MILESTONE = True
NEXT_STAGE = "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

TASK_5_INTEGRATION_REPORT_PATH = Path("examples/milestone-29/query-result-evidence-bundle-regression-integration-v1/task-5-regression-integration-report.json")
TASK_5_INTEGRATION_CASES_PATH = Path("examples/milestone-29/query-result-evidence-bundle-regression-integration-v1/task-5-regression-integration-cases.json")
TASK_5_MANIFEST_PATH = Path("examples/milestone-29/query-result-evidence-bundle-regression-integration-v1/task-5-manifest.json")
TASK_5_INDEX_PATH = Path("examples/milestone-29/query-result-evidence-bundle-regression-integration-v1/task-5-index.txt")
TASK_5_MARKDOWN_PATH = Path("examples/milestone-29/query-result-evidence-bundle-regression-integration-v1/task-5-regression-integration-report.md")

TASK_4_VALIDATION_REPORT_PATH = Path("examples/milestone-29/query-result-evidence-bundle-validation-v1/task-4-validation-report.json")
TASK_3_BUNDLE_PATH = Path("examples/milestone-29/query-result-evidence-bundle-implementation-v1/task-3-evidence-bundle.json")
TASK_2_SCOPE_LOCK_PATH = Path("examples/milestone-29/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.json")
TASK_1_OPENING_PATH = Path("examples/milestone-29/governed-opening-with-task-budget-v1/task-1-governed-opening.json")


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
            "source_integration_task_id": SOURCE_INTEGRATION_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
            "validation_revision": VALIDATION_REVISION,
            "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
            "final_closure_revision": FINAL_CLOSURE_REVISION,
            "task_5_signature": task_5_signature(),
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "final_task_number": FINAL_TASK_NUMBER,
            "task_7_used": TASK_7_USED,
            "task_8_used": TASK_8_USED,
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
    runtime = run_query_result_evidence_bundle_regression_integration()
    persisted = _load_json(TASK_5_INTEGRATION_REPORT_PATH)
    runtime_valid = validate_regression_integration_report(runtime)
    persisted_valid = validate_regression_integration_report(persisted)

    return {
        "source_integration_task_id": SOURCE_INTEGRATION_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_integration_id": runtime.get("integration_id"),
        "persisted_integration_id": persisted.get("integration_id"),
        "runtime_integration_signature": runtime.get("integration_signature"),
        "persisted_integration_signature": persisted.get("integration_signature"),
        "runtime_task_5_signature": runtime.get("task_5_signature"),
        "persisted_task_5_signature": persisted.get("task_5_signature"),
        "selected_objective_id": persisted.get("selected_objective_id"),
        "scope_lock_id": persisted.get("scope_lock_id"),
        "source_evidence_bundle_id": persisted.get("source_evidence_bundle_id"),
        "source_evidence_bundle_signature": persisted.get("source_evidence_bundle_signature"),
        "source_validation_id": persisted.get("source_validation_id"),
        "source_validation_signature": persisted.get("source_validation_signature"),
        "source_validation_status": persisted.get("source_validation_status"),
        "source_implementation_status": persisted.get("source_implementation_status"),
        "source_scope_lock_valid": persisted.get("source_scope_lock_valid"),
        "source_chain_valid": persisted.get("source_chain_valid"),
        "source_evidence_valid": persisted.get("source_evidence_valid"),
        "integration_status": persisted.get("integration_status"),
        "integration_case_count": persisted.get("integration_case_count"),
        "pass_count": persisted.get("pass_count"),
        "fail_count": persisted.get("fail_count"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_integration": (
            runtime.get("integration_id") == persisted.get("integration_id")
            and runtime.get("integration_signature") == persisted.get("integration_signature")
            and runtime.get("task_5_signature") == persisted.get("task_5_signature") == task_5_signature()
        ),
    }


def validate_integration_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_integration_task_id") != SOURCE_INTEGRATION_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("source_validation_status") != "VALID":
        return False
    if snapshot.get("source_implementation_status") != "READY":
        return False
    if snapshot.get("source_scope_lock_valid") is not True:
        return False
    if snapshot.get("source_chain_valid") is not True:
        return False
    if snapshot.get("source_evidence_valid") is not True:
        return False
    if snapshot.get("integration_status") != INTEGRATION_STATUS:
        return False
    if snapshot.get("integration_case_count") != INTEGRATION_CASE_COUNT:
        return False
    if snapshot.get("pass_count") != 9:
        return False
    if snapshot.get("fail_count") != 0:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_integration"))


def _validate_integration_report_case() -> dict[str, Any]:
    report = _load_json(TASK_5_INTEGRATION_REPORT_PATH)
    passed = (
        validate_regression_integration_report(report)
        and report.get("integration_status") == "VALID"
        and report.get("pass_count") == 9
        and report.get("fail_count") == 0
        and report.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_5_REGRESSION_INTEGRATION_REPORT_VALID",
        passed,
        {"integration_status": "VALID", "pass_count": 9, "fail_count": 0},
        {
            "integration_status": report.get("integration_status"),
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
        TASK_5_INTEGRATION_REPORT_PATH,
        TASK_5_INTEGRATION_CASES_PATH,
        TASK_5_MANIFEST_PATH,
        TASK_5_INDEX_PATH,
        TASK_5_MARKDOWN_PATH,
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
    report = _load_json(TASK_5_INTEGRATION_REPORT_PATH)
    manifest = _load_json(TASK_5_MANIFEST_PATH)
    passed = (
        manifest.get("task_id") == SOURCE_INTEGRATION_TASK_ID
        and manifest.get("source_task_id") == report.get("source_task_id")
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


def _validate_index_case() -> dict[str, Any]:
    report = _load_json(TASK_5_INTEGRATION_REPORT_PATH)
    index = TASK_5_INDEX_PATH.read_text(encoding="utf-8")
    required_markers = (
        "MILESTONE_29_TASK_5_QUERY_RESULT_EVIDENCE_BUNDLE_REGRESSION_INTEGRATION_READY=true",
        f"SOURCE_EVIDENCE_BUNDLE_ID={report.get('source_evidence_bundle_id')}",
        f"SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report.get('source_evidence_bundle_signature')}",
        f"SOURCE_VALIDATION_ID={report.get('source_validation_id')}",
        f"SOURCE_VALIDATION_SIGNATURE={report.get('source_validation_signature')}",
        "SOURCE_VALIDATION_STATUS=VALID",
        "SOURCE_IMPLEMENTATION_STATUS=READY",
        "SOURCE_SCOPE_LOCK_VALID=true",
        "SOURCE_CHAIN_VALID=true",
        "SOURCE_EVIDENCE_VALID=true",
        f"INTEGRATION_ID={report.get('integration_id')}",
        f"INTEGRATION_SIGNATURE={report.get('integration_signature')}",
        "INTEGRATION_STATUS=VALID",
        "INTEGRATION_CASE_COUNT=9",
        "PASS_COUNT=9",
        "FAIL_COUNT=0",
        f"NEXT_STAGE={SOURCE_NEXT_STAGE}",
    )
    missing = [marker for marker in required_markers if marker not in index]
    passed = not missing
    return _case(
        "TASK_5_REGRESSION_INTEGRATION_INDEX_MARKERS_VALID",
        passed,
        {"missing_markers": []},
        {"missing_markers": missing, "required_marker_count": len(required_markers)},
        "TASK_5_REGRESSION_INTEGRATION_INDEX_MARKERS_INVALID",
    )


def _validate_lineage_case() -> dict[str, Any]:
    task_1 = _load_json(TASK_1_OPENING_PATH)
    task_2 = _load_json(TASK_2_SCOPE_LOCK_PATH)
    task_3 = _load_json(TASK_3_BUNDLE_PATH)
    task_4 = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    task_5 = _load_json(TASK_5_INTEGRATION_REPORT_PATH)

    passed = (
        task_1.get("opening_status") == "OPEN"
        and task_1.get("technical_status") == "PASS"
        and task_2.get("objective_selection_ready") is True
        and task_2.get("scope_locked") is True
        and validate_query_result_evidence_bundle(task_3)
        and validate_validation_report(task_4)
        and validate_regression_integration_report(task_5)
        and task_3.get("evidence_bundle_id") == task_4.get("source_evidence_bundle_id") == task_5.get("source_evidence_bundle_id")
        and task_4.get("validation_id") == task_5.get("source_validation_id")
    )
    return _case(
        "MILESTONE_29_LINEAGE_FROM_OPENING_TO_INTEGRATION_VALID",
        passed,
        {"lineage_valid": True},
        {
            "task_1_opening_status": task_1.get("opening_status"),
            "task_2_scope_locked": task_2.get("scope_locked"),
            "task_3_bundle_id": task_3.get("evidence_bundle_id"),
            "task_4_source_bundle_id": task_4.get("source_evidence_bundle_id"),
            "task_5_source_bundle_id": task_5.get("source_evidence_bundle_id"),
            "task_4_validation_id": task_4.get("validation_id"),
            "task_5_source_validation_id": task_5.get("source_validation_id"),
        },
        "MILESTONE_29_LINEAGE_INVALID",
    )


def _validate_budget_closure_case() -> dict[str, Any]:
    report = _load_json(TASK_5_INTEGRATION_REPORT_PATH)
    passed = (
        report.get("task_budget_max") == TASK_BUDGET_MAX == 8
        and report.get("current_task_number") == SOURCE_CURRENT_TASK_NUMBER == 5
        and CURRENT_TASK_NUMBER == FINAL_TASK_NUMBER == 6
        and TASK_7_USED is False
        and TASK_8_USED is False
        and MILESTONE_CLOSED is True
        and READY_FOR_NEXT_MILESTONE is True
        and report.get("next_stage") == TASK_ID
        and NEXT_STAGE == "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    )
    return _case(
        "MILESTONE_29_TASK_BUDGET_AND_FINAL_CLOSURE_VALID",
        passed,
        {
            "task_budget_max": 8,
            "source_current_task_number": 5,
            "final_task_number": 6,
            "task_7_used": False,
            "task_8_used": False,
            "milestone_closed": True,
        },
        {
            "task_budget_max": report.get("task_budget_max"),
            "source_current_task_number": report.get("current_task_number"),
            "current_task_number": CURRENT_TASK_NUMBER,
            "final_task_number": FINAL_TASK_NUMBER,
            "task_7_used": TASK_7_USED,
            "task_8_used": TASK_8_USED,
            "milestone_closed": MILESTONE_CLOSED,
            "source_next_stage": report.get("next_stage"),
            "next_stage": NEXT_STAGE,
        },
        "MILESTONE_29_TASK_BUDGET_AND_FINAL_CLOSURE_INVALID",
    )


def _validate_source_status_case() -> dict[str, Any]:
    report = _load_json(TASK_5_INTEGRATION_REPORT_PATH)
    passed = (
        report.get("source_validation_status") == "VALID"
        and report.get("source_implementation_status") == "READY"
        and report.get("source_scope_lock_valid") is True
        and report.get("source_chain_valid") is True
        and report.get("source_evidence_valid") is True
        and report.get("integration_status") == "VALID"
    )
    return _case(
        "MILESTONE_29_SOURCE_STATUSES_REMAIN_VALID",
        passed,
        {
            "source_validation_status": "VALID",
            "source_implementation_status": "READY",
            "source_scope_lock_valid": True,
            "source_chain_valid": True,
            "source_evidence_valid": True,
            "integration_status": "VALID",
        },
        {
            "source_validation_status": report.get("source_validation_status"),
            "source_implementation_status": report.get("source_implementation_status"),
            "source_scope_lock_valid": report.get("source_scope_lock_valid"),
            "source_chain_valid": report.get("source_chain_valid"),
            "source_evidence_valid": report.get("source_evidence_valid"),
            "integration_status": report.get("integration_status"),
        },
        "MILESTONE_29_SOURCE_STATUSES_INVALID",
    )


def run_query_result_evidence_bundle_final_closure() -> dict[str, Any]:
    case_results = [
        _validate_integration_report_case(),
        _validate_runtime_stability_case(),
        _validate_artifact_set_case(),
        _validate_manifest_case(),
        _validate_index_case(),
        _validate_lineage_case(),
        _validate_budget_closure_case(),
        _validate_source_status_case(),
    ]

    pass_count = sum(1 for case in case_results if case["passed"])
    fail_count = len(case_results) - pass_count
    closure_passed = (
        len(case_results) == CLOSURE_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    integration_report = _load_json(TASK_5_INTEGRATION_REPORT_PATH)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_INTEGRATION_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "final_closure_revision": FINAL_CLOSURE_REVISION,
        "task_5_signature": task_5_signature(),
        "task_6_signature": task_6_signature(),
        "source_evidence_bundle_id": integration_report.get("source_evidence_bundle_id"),
        "source_evidence_bundle_signature": integration_report.get("source_evidence_bundle_signature"),
        "source_validation_id": integration_report.get("source_validation_id"),
        "source_validation_signature": integration_report.get("source_validation_signature"),
        "source_integration_id": integration_report.get("integration_id"),
        "source_integration_signature": integration_report.get("integration_signature"),
        "source_integration_status": integration_report.get("integration_status"),
        "source_validation_status": integration_report.get("source_validation_status"),
        "source_implementation_status": integration_report.get("source_implementation_status"),
        "source_scope_lock_valid": integration_report.get("source_scope_lock_valid"),
        "source_chain_valid": integration_report.get("source_chain_valid"),
        "source_evidence_valid": integration_report.get("source_evidence_valid"),
        "closure_status": CLOSURE_STATUS if closure_passed else "INVALID",
        "technical_status": TECHNICAL_STATUS if closure_passed else "FAIL",
        "process_status": PROCESS_STATUS if closure_passed else "INVALID",
        "closure_case_count": len(case_results),
        "required_pass_count": REQUIRED_PASS_COUNT,
        "required_fail_count": REQUIRED_FAIL_COUNT,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "closure_passed": closure_passed,
        "case_results": case_results,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "final_task_number": FINAL_TASK_NUMBER,
        "task_7_used": TASK_7_USED,
        "task_8_used": TASK_8_USED,
        "milestone_closed": MILESTONE_CLOSED if closure_passed else False,
        "ready_for_next_milestone": READY_FOR_NEXT_MILESTONE if closure_passed else False,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    report["closure_id"] = "MILESTONE-29-QUERY-RESULT-EVIDENCE-BUNDLE-FINAL-CLOSURE-" + _stable_digest(report)
    report["closure_signature"] = _stable_digest(
        {
            "closure_id": report["closure_id"],
            "source_evidence_bundle_id": report["source_evidence_bundle_id"],
            "source_evidence_bundle_signature": report["source_evidence_bundle_signature"],
            "source_validation_id": report["source_validation_id"],
            "source_validation_signature": report["source_validation_signature"],
            "source_integration_id": report["source_integration_id"],
            "source_integration_signature": report["source_integration_signature"],
            "task_5_signature": report["task_5_signature"],
            "task_6_signature": report["task_6_signature"],
            "case_results": case_results,
            "final_closure_revision": FINAL_CLOSURE_REVISION,
            "process_status": report["process_status"],
            "next_stage": NEXT_STAGE,
        }
    )
    return report


def validate_final_closure_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_INTEGRATION_TASK_ID:
        return False
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("evidence_bundle_revision") != EVIDENCE_BUNDLE_REVISION:
        return False
    if report.get("validation_revision") != VALIDATION_REVISION:
        return False
    if report.get("regression_integration_revision") != REGRESSION_INTEGRATION_REVISION:
        return False
    if report.get("final_closure_revision") != FINAL_CLOSURE_REVISION:
        return False
    if report.get("task_5_signature") != task_5_signature():
        return False
    if report.get("task_6_signature") != task_6_signature():
        return False
    if report.get("source_integration_status") != "VALID":
        return False
    if report.get("source_validation_status") != "VALID":
        return False
    if report.get("source_implementation_status") != "READY":
        return False
    if report.get("source_scope_lock_valid") is not True:
        return False
    if report.get("source_chain_valid") is not True:
        return False
    if report.get("source_evidence_valid") is not True:
        return False
    if report.get("closure_status") != CLOSURE_STATUS:
        return False
    if report.get("technical_status") != TECHNICAL_STATUS:
        return False
    if report.get("process_status") != PROCESS_STATUS:
        return False
    if report.get("closure_case_count") != CLOSURE_CASE_COUNT:
        return False
    if report.get("pass_count") != REQUIRED_PASS_COUNT:
        return False
    if report.get("fail_count") != REQUIRED_FAIL_COUNT:
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("final_task_number") != FINAL_TASK_NUMBER:
        return False
    if report.get("task_7_used") is not False:
        return False
    if report.get("task_8_used") is not False:
        return False
    if report.get("milestone_closed") is not True:
        return False
    if report.get("ready_for_next_milestone") is not True:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    if not all(case.get("passed") is True for case in report.get("case_results", [])):
        return False
    return bool(report.get("closure_passed") and report.get("closure_id") and report.get("closure_signature"))


def render_final_closure_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 29 Task 6 Query Result Evidence Bundle Final Closure",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"CLOSURE_ID={report.get('closure_id')}",
        f"CLOSURE_SIGNATURE={report.get('closure_signature')}",
        f"SOURCE_EVIDENCE_BUNDLE_ID={report.get('source_evidence_bundle_id')}",
        f"SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report.get('source_evidence_bundle_signature')}",
        f"SOURCE_VALIDATION_ID={report.get('source_validation_id')}",
        f"SOURCE_VALIDATION_SIGNATURE={report.get('source_validation_signature')}",
        f"SOURCE_INTEGRATION_ID={report.get('source_integration_id')}",
        f"SOURCE_INTEGRATION_SIGNATURE={report.get('source_integration_signature')}",
        f"CLOSURE_STATUS={report.get('closure_status')}",
        f"TECHNICAL_STATUS={report.get('technical_status')}",
        f"PROCESS_STATUS={report.get('process_status')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"TASK_7_USED={str(report.get('task_7_used')).lower()}",
        f"TASK_8_USED={str(report.get('task_8_used')).lower()}",
        f"MILESTONE_CLOSED={str(report.get('milestone_closed')).lower()}",
        f"READY_FOR_NEXT_MILESTONE={str(report.get('ready_for_next_milestone')).lower()}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Final closure cases",
    ]
    for case in report.get("case_results", []):
        lines.append(f"- {case['case_id']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_6_artifacts(base_dir: str | Path = "examples/milestone-29/query-result-evidence-bundle-final-closure-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_query_result_evidence_bundle_final_closure()
    cases = {
        "task_id": TASK_ID,
        "closure_id": report["closure_id"],
        "closure_status": report["closure_status"],
        "closure_case_count": report["closure_case_count"],
        "case_results": report["case_results"],
    }
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_INTEGRATION_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "final_closure_revision": FINAL_CLOSURE_REVISION,
        "task_5_signature": task_5_signature(),
        "task_6_signature": task_6_signature(),
        "source_evidence_bundle_id": report["source_evidence_bundle_id"],
        "source_evidence_bundle_signature": report["source_evidence_bundle_signature"],
        "source_validation_id": report["source_validation_id"],
        "source_validation_signature": report["source_validation_signature"],
        "source_integration_id": report["source_integration_id"],
        "source_integration_signature": report["source_integration_signature"],
        "closure_id": report["closure_id"],
        "closure_signature": report["closure_signature"],
        "closure_status": report["closure_status"],
        "technical_status": report["technical_status"],
        "process_status": report["process_status"],
        "closure_passed": report["closure_passed"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "final_task_number": FINAL_TASK_NUMBER,
        "task_7_used": TASK_7_USED,
        "task_8_used": TASK_8_USED,
        "milestone_closed": report["milestone_closed"],
        "ready_for_next_milestone": report["ready_for_next_milestone"],
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
    (output_dir / "task-6-final-closure-cases.json").write_text(
        json.dumps(cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-6-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-6-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_INTEGRATION_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"EVIDENCE_BUNDLE_REVISION={EVIDENCE_BUNDLE_REVISION}",
                f"VALIDATION_REVISION={VALIDATION_REVISION}",
                f"REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}",
                f"FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}",
                f"TASK_5_SIGNATURE={task_5_signature()}",
                f"TASK_6_SIGNATURE={task_6_signature()}",
                f"SOURCE_EVIDENCE_BUNDLE_ID={report['source_evidence_bundle_id']}",
                f"SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report['source_evidence_bundle_signature']}",
                f"SOURCE_VALIDATION_ID={report['source_validation_id']}",
                f"SOURCE_VALIDATION_SIGNATURE={report['source_validation_signature']}",
                f"SOURCE_INTEGRATION_ID={report['source_integration_id']}",
                f"SOURCE_INTEGRATION_SIGNATURE={report['source_integration_signature']}",
                f"SOURCE_INTEGRATION_STATUS={report['source_integration_status']}",
                f"SOURCE_VALIDATION_STATUS={report['source_validation_status']}",
                f"SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}",
                f"SOURCE_SCOPE_LOCK_VALID={str(report['source_scope_lock_valid']).lower()}",
                f"SOURCE_CHAIN_VALID={str(report['source_chain_valid']).lower()}",
                f"SOURCE_EVIDENCE_VALID={str(report['source_evidence_valid']).lower()}",
                f"CLOSURE_ID={report['closure_id']}",
                f"CLOSURE_SIGNATURE={report['closure_signature']}",
                f"CLOSURE_STATUS={report['closure_status']}",
                f"TECHNICAL_STATUS={report['technical_status']}",
                f"PROCESS_STATUS={report['process_status']}",
                f"CLOSURE_CASE_COUNT={report['closure_case_count']}",
                f"PASS_COUNT={report['pass_count']}",
                f"FAIL_COUNT={report['fail_count']}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"FINAL_TASK_NUMBER={FINAL_TASK_NUMBER}",
                f"TASK_7_USED={str(TASK_7_USED).lower()}",
                f"TASK_8_USED={str(TASK_8_USED).lower()}",
                f"MILESTONE_CLOSED={str(report['milestone_closed']).lower()}",
                f"READY_FOR_NEXT_MILESTONE={str(report['ready_for_next_milestone']).lower()}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_6_status_lines() -> tuple[str, ...]:
    report = run_query_result_evidence_bundle_final_closure()
    return (
        "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_READY=true",
        f"MILESTONE_29_TASK_6_SOURCE_TASK_ID={SOURCE_INTEGRATION_TASK_ID}",
        f"MILESTONE_29_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_29_TASK_6_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_29_TASK_6_FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}",
        f"MILESTONE_29_TASK_6_TASK_5_SIGNATURE={task_5_signature()}",
        f"MILESTONE_29_TASK_6_TASK_6_SIGNATURE={task_6_signature()}",
        f"MILESTONE_29_TASK_6_SOURCE_EVIDENCE_BUNDLE_ID={report['source_evidence_bundle_id']}",
        f"MILESTONE_29_TASK_6_SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report['source_evidence_bundle_signature']}",
        f"MILESTONE_29_TASK_6_SOURCE_VALIDATION_ID={report['source_validation_id']}",
        f"MILESTONE_29_TASK_6_SOURCE_VALIDATION_SIGNATURE={report['source_validation_signature']}",
        f"MILESTONE_29_TASK_6_SOURCE_INTEGRATION_ID={report['source_integration_id']}",
        f"MILESTONE_29_TASK_6_SOURCE_INTEGRATION_SIGNATURE={report['source_integration_signature']}",
        f"MILESTONE_29_TASK_6_SOURCE_INTEGRATION_STATUS={report['source_integration_status']}",
        f"MILESTONE_29_TASK_6_SOURCE_VALIDATION_STATUS={report['source_validation_status']}",
        f"MILESTONE_29_TASK_6_SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}",
        f"MILESTONE_29_TASK_6_SOURCE_SCOPE_LOCK_VALID={str(report['source_scope_lock_valid']).lower()}",
        f"MILESTONE_29_TASK_6_SOURCE_CHAIN_VALID={str(report['source_chain_valid']).lower()}",
        f"MILESTONE_29_TASK_6_SOURCE_EVIDENCE_VALID={str(report['source_evidence_valid']).lower()}",
        f"MILESTONE_29_TASK_6_CLOSURE_ID={report['closure_id']}",
        f"MILESTONE_29_TASK_6_CLOSURE_SIGNATURE={report['closure_signature']}",
        f"MILESTONE_29_TASK_6_CLOSURE_STATUS={report['closure_status']}",
        f"MILESTONE_29_TASK_6_TECHNICAL_STATUS={report['technical_status']}",
        f"MILESTONE_29_TASK_6_PROCESS_STATUS={report['process_status']}",
        f"MILESTONE_29_TASK_6_CLOSURE_CASE_COUNT={report['closure_case_count']}",
        f"MILESTONE_29_TASK_6_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_29_TASK_6_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_29_TASK_6_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_29_TASK_6_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_29_TASK_6_FINAL_TASK_NUMBER={FINAL_TASK_NUMBER}",
        f"MILESTONE_29_TASK_6_TASK_7_USED={str(TASK_7_USED).lower()}",
        f"MILESTONE_29_TASK_6_TASK_8_USED={str(TASK_8_USED).lower()}",
        f"MILESTONE_29_TASK_6_MILESTONE_CLOSED={str(report['milestone_closed']).lower()}",
        f"MILESTONE_29_TASK_6_READY_FOR_NEXT_MILESTONE={str(report['ready_for_next_milestone']).lower()}",
        f"MILESTONE_29_TASK_6_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_29_TASK_6_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_6_artifacts()
    for line in task_6_status_lines():
        print(line)
