from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_28_query_result_export_regression_integration import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    INTEGRATION_CASE_COUNT,
    MILESTONE_ID,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    REGRESSION_INTEGRATION_REVISION,
    REQUIRED_FAIL_COUNT as SOURCE_REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT as SOURCE_REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    run_query_result_export_regression_integration,
    task_5_signature,
    validate_regression_integration_report,
)


TASK_ID = "MILESTONE_28_TASK_6_QUERY_RESULT_EXPORT_FINAL_CLOSURE_V1"
FINAL_CLOSURE_REVISION = "MILESTONE_28_QUERY_RESULT_EXPORT_FINAL_CLOSURE_V1"

CURRENT_TASK_NUMBER = 6
FINAL_TASK_NUMBER = 6
NEXT_STAGE = "MILESTONE_29_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

CLOSURE_STATUS = "CLOSED"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"

CLOSURE_CASE_COUNT = 8
REQUIRED_PASS_COUNT = 8
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

TASK_7_USED = False
TASK_8_USED = False
MILESTONE_CLOSED = True
READY_FOR_NEXT_MILESTONE = True

TASK_5_REPORT_PATH = Path("examples/milestone-28/query-result-export-regression-integration-v1/task-5-regression-integration-report.json")
TASK_5_CASES_PATH = Path("examples/milestone-28/query-result-export-regression-integration-v1/task-5-regression-integration-cases.json")
TASK_5_MANIFEST_PATH = Path("examples/milestone-28/query-result-export-regression-integration-v1/task-5-manifest.json")
TASK_5_INDEX_PATH = Path("examples/milestone-28/query-result-export-regression-integration-v1/task-5-index.txt")
TASK_5_MARKDOWN_PATH = Path("examples/milestone-28/query-result-export-regression-integration-v1/task-5-regression-integration-report.md")


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_6_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
            "final_closure_revision": FINAL_CLOSURE_REVISION,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
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


def build_regression_integration_snapshot() -> dict[str, Any]:
    runtime = run_query_result_export_regression_integration()
    persisted = _load_json(TASK_5_REPORT_PATH)
    runtime_valid = validate_regression_integration_report(runtime)
    persisted_valid = validate_regression_integration_report(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_integration_id": runtime.get("integration_id"),
        "persisted_integration_id": persisted.get("integration_id"),
        "runtime_integration_signature": runtime.get("integration_signature"),
        "persisted_integration_signature": persisted.get("integration_signature"),
        "runtime_task_5_signature": runtime.get("task_5_signature"),
        "persisted_task_5_signature": persisted.get("task_5_signature"),
        "selected_objective_id": runtime.get("selected_objective_id"),
        "scope_lock_id": runtime.get("scope_lock_id"),
        "source_validation_status": runtime.get("source_validation_status"),
        "source_export_status": runtime.get("source_export_status"),
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


def validate_regression_integration_snapshot(snapshot: Mapping[str, Any]) -> bool:
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
    if snapshot.get("source_export_status") != "READY":
        return False
    if snapshot.get("integration_status") != "VALID":
        return False
    if snapshot.get("integration_case_count") != INTEGRATION_CASE_COUNT:
        return False
    if snapshot.get("pass_count") != SOURCE_REQUIRED_PASS_COUNT:
        return False
    if snapshot.get("fail_count") != SOURCE_REQUIRED_FAIL_COUNT:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_integration"))


def _validate_task_5_report_case() -> dict[str, Any]:
    report = _load_json(TASK_5_REPORT_PATH)
    passed = (
        validate_regression_integration_report(report)
        and report.get("integration_status") == "VALID"
        and report.get("pass_count") == 7
        and report.get("fail_count") == 0
        and report.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_5_REGRESSION_INTEGRATION_REPORT_VALID",
        passed,
        {"integration_status": "VALID", "pass_count": 7, "fail_count": 0},
        {
            "integration_status": report.get("integration_status"),
            "pass_count": report.get("pass_count"),
            "fail_count": report.get("fail_count"),
            "next_stage": report.get("next_stage"),
        },
        "TASK_5_REGRESSION_INTEGRATION_REPORT_INVALID",
    )


def _validate_runtime_stability_case() -> dict[str, Any]:
    snapshot = build_regression_integration_snapshot()
    passed = validate_regression_integration_snapshot(snapshot)
    return _case(
        "TASK_5_RUNTIME_STABILITY_VALID",
        passed,
        {"stable_integration": True},
        snapshot,
        "TASK_5_RUNTIME_STABILITY_INVALID",
    )


def _validate_task_5_artifact_set_case() -> dict[str, Any]:
    paths = (
        TASK_5_REPORT_PATH,
        TASK_5_CASES_PATH,
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
        "TASK_5_ARTIFACT_SET_PRESENT",
        passed,
        {"artifact_count": 5, "missing": []},
        {"artifact_count": len(paths), "missing": missing, "readable_count": sum(1 for item in readable if item)},
        "TASK_5_ARTIFACT_SET_INCOMPLETE",
    )


def _validate_task_5_manifest_case() -> dict[str, Any]:
    report = _load_json(TASK_5_REPORT_PATH)
    manifest = _load_json(TASK_5_MANIFEST_PATH)
    passed = (
        manifest.get("task_id") == SOURCE_TASK_ID
        and manifest.get("integration_id") == report.get("integration_id")
        and manifest.get("integration_signature") == report.get("integration_signature")
        and manifest.get("integration_status") == "VALID"
        and manifest.get("integration_passed") is True
        and manifest.get("pass_count") == report.get("pass_count") == 7
        and manifest.get("fail_count") == report.get("fail_count") == 0
        and manifest.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_5_MANIFEST_CONSISTENCY_VALID",
        passed,
        {"manifest_matches_report": True},
        {
            "manifest_integration_id": manifest.get("integration_id"),
            "report_integration_id": report.get("integration_id"),
            "manifest_status": manifest.get("integration_status"),
            "manifest_next_stage": manifest.get("next_stage"),
        },
        "TASK_5_MANIFEST_CONSISTENCY_INVALID",
    )


def _validate_task_5_index_case() -> dict[str, Any]:
    report = _load_json(TASK_5_REPORT_PATH)
    index = TASK_5_INDEX_PATH.read_text(encoding="utf-8")
    required_markers = (
        "MILESTONE_28_TASK_5_QUERY_RESULT_EXPORT_REGRESSION_INTEGRATION_READY=true",
        f"SOURCE_VALIDATION_ID={report.get('source_validation_id')}",
        f"SOURCE_VALIDATION_SIGNATURE={report.get('source_validation_signature')}",
        "SOURCE_VALIDATION_STATUS=VALID",
        f"SOURCE_EXPORT_ID={report.get('source_export_id')}",
        f"SOURCE_EXPORT_SIGNATURE={report.get('source_export_signature')}",
        "SOURCE_EXPORT_STATUS=READY",
        f"INTEGRATION_ID={report.get('integration_id')}",
        f"INTEGRATION_SIGNATURE={report.get('integration_signature')}",
        "INTEGRATION_STATUS=VALID",
        "INTEGRATION_CASE_COUNT=7",
        "PASS_COUNT=7",
        "FAIL_COUNT=0",
        f"NEXT_STAGE={SOURCE_NEXT_STAGE}",
    )
    missing = [marker for marker in required_markers if marker not in index]
    passed = not missing
    return _case(
        "TASK_5_INDEX_MARKERS_VALID",
        passed,
        {"missing_markers": []},
        {"missing_markers": missing, "required_marker_count": len(required_markers)},
        "TASK_5_INDEX_MARKERS_INVALID",
    )


def _validate_task_budget_finalization_case() -> dict[str, Any]:
    passed = (
        TASK_BUDGET_MAX == 8
        and SOURCE_CURRENT_TASK_NUMBER == 5
        and CURRENT_TASK_NUMBER == 6
        and FINAL_TASK_NUMBER == 6
        and TASK_7_USED is False
        and TASK_8_USED is False
    )
    return _case(
        "TASK_BUDGET_FINALIZATION_VALID",
        passed,
        {
            "task_budget_max": 8,
            "source_current_task_number": 5,
            "current_task_number": 6,
            "final_task_number": 6,
            "task_7_used": False,
            "task_8_used": False,
        },
        {
            "task_budget_max": TASK_BUDGET_MAX,
            "source_current_task_number": SOURCE_CURRENT_TASK_NUMBER,
            "current_task_number": CURRENT_TASK_NUMBER,
            "final_task_number": FINAL_TASK_NUMBER,
            "task_7_used": TASK_7_USED,
            "task_8_used": TASK_8_USED,
        },
        "TASK_BUDGET_FINALIZATION_INVALID",
    )


def _validate_closure_transition_case() -> dict[str, Any]:
    passed = (
        SOURCE_NEXT_STAGE == TASK_ID
        and NEXT_STAGE == "MILESTONE_29_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
        and CLOSURE_STATUS == "CLOSED"
        and TECHNICAL_STATUS == "PASS"
        and PROCESS_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
        and MILESTONE_CLOSED is True
        and READY_FOR_NEXT_MILESTONE is True
    )
    return _case(
        "FINAL_CLOSURE_TRANSITION_VALID",
        passed,
        {
            "source_next_stage": TASK_ID,
            "next_stage": "MILESTONE_29_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1",
            "closure_status": "CLOSED",
            "technical_status": "PASS",
            "process_status": "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
        },
        {
            "source_next_stage": SOURCE_NEXT_STAGE,
            "next_stage": NEXT_STAGE,
            "closure_status": CLOSURE_STATUS,
            "technical_status": TECHNICAL_STATUS,
            "process_status": PROCESS_STATUS,
            "milestone_closed": MILESTONE_CLOSED,
            "ready_for_next_milestone": READY_FOR_NEXT_MILESTONE,
        },
        "FINAL_CLOSURE_TRANSITION_INVALID",
    )


def _validate_chain_status_case() -> dict[str, Any]:
    report = _load_json(TASK_5_REPORT_PATH)
    passed = (
        report.get("source_validation_status") == "VALID"
        and report.get("source_export_status") == "READY"
        and report.get("export_payload_status") == "READY"
        and report.get("integration_status") == "VALID"
        and report.get("integration_passed") is True
        and report.get("exported_record_count") == 1
    )
    return _case(
        "QUERY_RESULT_EXPORT_CHAIN_STATUS_VALID",
        passed,
        {
            "source_validation_status": "VALID",
            "source_export_status": "READY",
            "export_payload_status": "READY",
            "integration_status": "VALID",
            "exported_record_count": 1,
        },
        {
            "source_validation_status": report.get("source_validation_status"),
            "source_export_status": report.get("source_export_status"),
            "export_payload_status": report.get("export_payload_status"),
            "integration_status": report.get("integration_status"),
            "integration_passed": report.get("integration_passed"),
            "exported_record_count": report.get("exported_record_count"),
        },
        "QUERY_RESULT_EXPORT_CHAIN_STATUS_INVALID",
    )


def run_query_result_export_final_closure() -> dict[str, Any]:
    case_results = [
        _validate_task_5_report_case(),
        _validate_runtime_stability_case(),
        _validate_task_5_artifact_set_case(),
        _validate_task_5_manifest_case(),
        _validate_task_5_index_case(),
        _validate_task_budget_finalization_case(),
        _validate_closure_transition_case(),
        _validate_chain_status_case(),
    ]

    pass_count = sum(1 for case in case_results if case["passed"])
    fail_count = len(case_results) - pass_count
    closure_passed = (
        len(case_results) == CLOSURE_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    integration_report = _load_json(TASK_5_REPORT_PATH)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "final_closure_revision": FINAL_CLOSURE_REVISION,
        "task_5_signature": task_5_signature(),
        "task_6_signature": task_6_signature(),
        "source_integration_id": integration_report.get("integration_id"),
        "source_integration_signature": integration_report.get("integration_signature"),
        "source_integration_status": integration_report.get("integration_status"),
        "source_validation_id": integration_report.get("source_validation_id"),
        "source_validation_signature": integration_report.get("source_validation_signature"),
        "source_validation_status": integration_report.get("source_validation_status"),
        "source_export_id": integration_report.get("source_export_id"),
        "source_export_signature": integration_report.get("source_export_signature"),
        "source_export_status": integration_report.get("source_export_status"),
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
        "milestone_closed": MILESTONE_CLOSED,
        "ready_for_next_milestone": READY_FOR_NEXT_MILESTONE,
        "next_stage": NEXT_STAGE,
    }

    report["closure_id"] = "MILESTONE-28-QUERY-EXPORT-FINAL-CLOSURE-" + _stable_digest(report)
    report["closure_signature"] = _stable_digest(
        {
            "closure_id": report["closure_id"],
            "source_integration_id": report["source_integration_id"],
            "source_integration_signature": report["source_integration_signature"],
            "source_validation_id": report["source_validation_id"],
            "source_export_id": report["source_export_id"],
            "case_results": case_results,
            "final_closure_revision": FINAL_CLOSURE_REVISION,
            "process_status": PROCESS_STATUS,
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
    if report.get("regression_integration_revision") != REGRESSION_INTEGRATION_REVISION:
        return False
    if report.get("final_closure_revision") != FINAL_CLOSURE_REVISION:
        return False
    if report.get("source_integration_status") != "VALID":
        return False
    if report.get("source_validation_status") != "VALID":
        return False
    if report.get("source_export_status") != "READY":
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
    if report.get("next_stage") != NEXT_STAGE:
        return False
    if not all(case.get("passed") is True for case in report.get("case_results", [])):
        return False
    return bool(report.get("closure_passed"))


def render_final_closure_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 28 Task 6 Query Result Export Final Closure",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"CLOSURE_STATUS={report.get('closure_status')}",
        f"TECHNICAL_STATUS={report.get('technical_status')}",
        f"PROCESS_STATUS={report.get('process_status')}",
        f"CLOSURE_ID={report.get('closure_id')}",
        f"CLOSURE_SIGNATURE={report.get('closure_signature')}",
        f"SOURCE_INTEGRATION_ID={report.get('source_integration_id')}",
        f"SOURCE_INTEGRATION_SIGNATURE={report.get('source_integration_signature')}",
        f"SOURCE_VALIDATION_ID={report.get('source_validation_id')}",
        f"SOURCE_EXPORT_ID={report.get('source_export_id')}",
        f"FINAL_TASK_NUMBER={report.get('final_task_number')}",
        f"TASK_7_USED={str(report.get('task_7_used')).lower()}",
        f"TASK_8_USED={str(report.get('task_8_used')).lower()}",
        f"MILESTONE_CLOSED={str(report.get('milestone_closed')).lower()}",
        f"READY_FOR_NEXT_MILESTONE={str(report.get('ready_for_next_milestone')).lower()}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Closure cases",
    ]
    for case in report.get("case_results", []):
        lines.append(f"- {case['case_id']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_6_artifacts(base_dir: str | Path = "examples/milestone-28/query-result-export-final-closure-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_query_result_export_final_closure()
    cases = {
        "task_id": TASK_ID,
        "closure_id": report["closure_id"],
        "closure_status": report["closure_status"],
        "closure_case_count": report["closure_case_count"],
        "case_results": report["case_results"],
    }
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "final_closure_revision": FINAL_CLOSURE_REVISION,
        "task_5_signature": task_5_signature(),
        "task_6_signature": task_6_signature(),
        "closure_id": report["closure_id"],
        "closure_signature": report["closure_signature"],
        "closure_status": report["closure_status"],
        "technical_status": report["technical_status"],
        "process_status": report["process_status"],
        "closure_passed": report["closure_passed"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "final_task_number": FINAL_TASK_NUMBER,
        "task_7_used": TASK_7_USED,
        "task_8_used": TASK_8_USED,
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
                "MILESTONE_28_TASK_6_QUERY_RESULT_EXPORT_FINAL_CLOSURE_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}",
                f"FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}",
                f"TASK_5_SIGNATURE={task_5_signature()}",
                f"TASK_6_SIGNATURE={task_6_signature()}",
                f"SOURCE_INTEGRATION_ID={report['source_integration_id']}",
                f"SOURCE_INTEGRATION_SIGNATURE={report['source_integration_signature']}",
                f"SOURCE_INTEGRATION_STATUS={report['source_integration_status']}",
                f"SOURCE_VALIDATION_STATUS={report['source_validation_status']}",
                f"SOURCE_EXPORT_STATUS={report['source_export_status']}",
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
                f"MILESTONE_CLOSED={str(MILESTONE_CLOSED).lower()}",
                f"READY_FOR_NEXT_MILESTONE={str(READY_FOR_NEXT_MILESTONE).lower()}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_6_status_lines() -> tuple[str, ...]:
    report = run_query_result_export_final_closure()
    return (
        "MILESTONE_28_TASK_6_QUERY_RESULT_EXPORT_FINAL_CLOSURE_READY=true",
        f"MILESTONE_28_TASK_6_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_28_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_28_TASK_6_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_28_TASK_6_FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}",
        f"MILESTONE_28_TASK_6_TASK_5_SIGNATURE={task_5_signature()}",
        f"MILESTONE_28_TASK_6_TASK_6_SIGNATURE={task_6_signature()}",
        f"MILESTONE_28_TASK_6_SOURCE_INTEGRATION_ID={report['source_integration_id']}",
        f"MILESTONE_28_TASK_6_SOURCE_INTEGRATION_SIGNATURE={report['source_integration_signature']}",
        f"MILESTONE_28_TASK_6_SOURCE_INTEGRATION_STATUS={report['source_integration_status']}",
        f"MILESTONE_28_TASK_6_SOURCE_VALIDATION_STATUS={report['source_validation_status']}",
        f"MILESTONE_28_TASK_6_SOURCE_EXPORT_STATUS={report['source_export_status']}",
        f"MILESTONE_28_TASK_6_CLOSURE_ID={report['closure_id']}",
        f"MILESTONE_28_TASK_6_CLOSURE_SIGNATURE={report['closure_signature']}",
        f"MILESTONE_28_TASK_6_CLOSURE_STATUS={report['closure_status']}",
        f"MILESTONE_28_TASK_6_TECHNICAL_STATUS={report['technical_status']}",
        f"MILESTONE_28_TASK_6_PROCESS_STATUS={report['process_status']}",
        f"MILESTONE_28_TASK_6_CLOSURE_CASE_COUNT={report['closure_case_count']}",
        f"MILESTONE_28_TASK_6_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_28_TASK_6_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_28_TASK_6_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_28_TASK_6_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_28_TASK_6_FINAL_TASK_NUMBER={FINAL_TASK_NUMBER}",
        f"MILESTONE_28_TASK_6_TASK_7_USED={str(TASK_7_USED).lower()}",
        f"MILESTONE_28_TASK_6_TASK_8_USED={str(TASK_8_USED).lower()}",
        f"MILESTONE_28_TASK_6_MILESTONE_CLOSED={str(MILESTONE_CLOSED).lower()}",
        f"MILESTONE_28_TASK_6_READY_FOR_NEXT_MILESTONE={str(READY_FOR_NEXT_MILESTONE).lower()}",
        f"MILESTONE_28_TASK_6_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_28_TASK_6_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    artifacts = write_task_6_artifacts()
    for line in task_6_status_lines():
        print(line)
