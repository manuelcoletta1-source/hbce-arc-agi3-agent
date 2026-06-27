from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_27_query_interface import (
    DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
    LOCAL_ONLY,
    NETWORK_ACCESS_ALLOWED,
    QUERY_INTERFACE_REVISION,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SHELL_EXECUTION_ALLOWED,
    TASK_ID as TASK_3_ID,
    query_closed_milestone_archive_index,
    task_3_signature,
    validate_query_result,
)
from hbce_arc_agi3.milestone_27_query_interface_validation import (
    TASK_ID as TASK_4_ID,
    VALIDATION_REVISION,
    run_query_interface_validation,
    task_4_signature,
    validate_validation_report,
)


MILESTONE_ID = "MILESTONE_27"
TASK_ID = "MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_V1"
SOURCE_TASK_ID = TASK_4_ID
REGRESSION_REVISION = "MILESTONE_27_QUERY_INTERFACE_REGRESSION_INTEGRATION_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 5
NEXT_STAGE = "MILESTONE_27_TASK_6_QUERY_INTERFACE_FINAL_CLOSURE_V1"

REGRESSION_CASE_COUNT = 6
REQUIRED_PASS_COUNT = 6
REQUIRED_FAIL_COUNT = 0

TASK_3_ARTIFACT_DIR = Path("examples/milestone-27/query-interface-implementation-v1")
TASK_4_ARTIFACT_DIR = Path("examples/milestone-27/query-interface-validation-v1")

TASK_3_PRIMARY_RESULT_PATH = TASK_3_ARTIFACT_DIR / "task-3-query-interface-result.json"
TASK_3_BLOCKED_RESULT_PATH = TASK_3_ARTIFACT_DIR / "task-3-query-interface-blocked-result.json"
TASK_4_VALIDATION_REPORT_PATH = TASK_4_ARTIFACT_DIR / "task-4-validation-report.json"
TASK_4_VALIDATION_CASES_PATH = TASK_4_ARTIFACT_DIR / "task-4-validation-cases.json"
TASK_4_MANIFEST_PATH = TASK_4_ARTIFACT_DIR / "task-4-manifest.json"

_REGRESSION_SIGNATURE_SEED = {
    "task_id": TASK_ID,
    "source_task_id": SOURCE_TASK_ID,
    "selected_objective_id": SELECTED_OBJECTIVE_ID,
    "scope_lock_id": SCOPE_LOCK_ID,
    "query_interface_revision": QUERY_INTERFACE_REVISION,
    "validation_revision": VALIDATION_REVISION,
    "regression_revision": REGRESSION_REVISION,
    "case_count": REGRESSION_CASE_COUNT,
}


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def task_5_signature() -> str:
    return _stable_digest(_REGRESSION_SIGNATURE_SEED)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _case(case_id: str, passed: bool, expected: Any, observed: Any, failure_reason: str = "NONE") -> dict[str, Any]:
    return {
        "case_id": case_id,
        "passed": passed,
        "failure_reason": "NONE" if passed else failure_reason,
        "expected": expected,
        "observed": observed,
    }


def _validate_task_4_report_artifact() -> dict[str, Any]:
    report = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    passed = validate_validation_report(report)
    observed = {
        "validation_status": report.get("validation_status"),
        "pass_count": report.get("pass_count"),
        "fail_count": report.get("fail_count"),
        "validation_id": report.get("validation_id"),
    }
    expected = {
        "validation_status": "VALID",
        "pass_count": 6,
        "fail_count": 0,
    }
    return _case("TASK_4_VALIDATION_REPORT_ARTIFACT_VALID", passed, expected, observed, "TASK_4_REPORT_INVALID")


def _validate_task_3_primary_query_stability() -> dict[str, Any]:
    persisted = _load_json(TASK_3_PRIMARY_RESULT_PATH)
    runtime = query_closed_milestone_archive_index({"milestone_id": "MILESTONE_26", "local_only": True})

    passed = (
        validate_query_result(persisted)
        and validate_query_result(runtime)
        and persisted.get("query_id") == runtime.get("query_id")
        and persisted.get("result_signature") == runtime.get("result_signature")
        and persisted.get("task_3_signature") == runtime.get("task_3_signature")
        and runtime.get("matched_count") == 1
        and runtime.get("records", [{}])[0].get("milestone_id") == "MILESTONE_26"
    )

    expected = {
        "query_status": "READY",
        "matched_count": 1,
        "stable_query_id": persisted.get("query_id"),
    }
    observed = {
        "query_status": runtime.get("query_status"),
        "matched_count": runtime.get("matched_count"),
        "runtime_query_id": runtime.get("query_id"),
        "persisted_query_id": persisted.get("query_id"),
    }
    return _case("TASK_3_PRIMARY_QUERY_RUNTIME_STABLE", passed, expected, observed, "TASK_3_PRIMARY_QUERY_DRIFT")


def _validate_task_3_blocked_query_stability() -> dict[str, Any]:
    persisted = _load_json(TASK_3_BLOCKED_RESULT_PATH)
    runtime = query_closed_milestone_archive_index({"milestone_id": "MILESTONE_26", "local_only": False})

    passed = (
        validate_query_result(persisted)
        and validate_query_result(runtime)
        and persisted.get("query_id") == runtime.get("query_id")
        and persisted.get("result_signature") == runtime.get("result_signature")
        and runtime.get("query_status") == "BLOCKED_BY_SCOPE_LOCK"
        and runtime.get("blocked") is True
        and runtime.get("matched_count") == 0
    )

    expected = {
        "query_status": "BLOCKED_BY_SCOPE_LOCK",
        "matched_count": 0,
        "stable_query_id": persisted.get("query_id"),
    }
    observed = {
        "query_status": runtime.get("query_status"),
        "matched_count": runtime.get("matched_count"),
        "runtime_query_id": runtime.get("query_id"),
        "persisted_query_id": persisted.get("query_id"),
    }
    return _case("TASK_3_BLOCKED_QUERY_RUNTIME_STABLE", passed, expected, observed, "TASK_3_BLOCKED_QUERY_DRIFT")


def _validate_runtime_validation_report_stability() -> dict[str, Any]:
    persisted = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    runtime = run_query_interface_validation()

    comparable_fields = (
        "validation_status",
        "validation_case_count",
        "pass_count",
        "fail_count",
        "ready_case_count",
        "blocked_case_count",
        "validation_id",
        "validation_signature",
    )

    passed = (
        validate_validation_report(persisted)
        and validate_validation_report(runtime)
        and all(persisted.get(field) == runtime.get(field) for field in comparable_fields)
    )

    expected = {field: persisted.get(field) for field in comparable_fields}
    observed = {field: runtime.get(field) for field in comparable_fields}
    return _case("TASK_4_RUNTIME_VALIDATION_REPORT_STABLE", passed, expected, observed, "TASK_4_VALIDATION_RUNTIME_DRIFT")


def _validate_case_matrix_integrated() -> dict[str, Any]:
    cases = _load_json(TASK_4_VALIDATION_CASES_PATH)
    case_results = cases.get("case_results", [])

    passed = (
        cases.get("case_count") == REGRESSION_CASE_COUNT
        and len(case_results) == REGRESSION_CASE_COUNT
        and all(item.get("passed") is True for item in case_results)
        and {item.get("actual_query_status") for item in case_results} == {"READY", "BLOCKED_BY_SCOPE_LOCK"}
    )

    expected = {
        "case_count": 6,
        "all_passed": True,
        "statuses": ["BLOCKED_BY_SCOPE_LOCK", "READY"],
    }
    observed = {
        "case_count": cases.get("case_count"),
        "all_passed": all(item.get("passed") is True for item in case_results),
        "statuses": sorted({str(item.get("actual_query_status")) for item in case_results}),
    }
    return _case("TASK_4_CASE_MATRIX_INTEGRATED", passed, expected, observed, "TASK_4_CASE_MATRIX_INVALID")


def _validate_scope_lock_regression_guard() -> dict[str, Any]:
    result = query_closed_milestone_archive_index(
        {
            "milestone_id": "MILESTONE_26",
            "local_only": True,
            "forbidden_operations": ("network_access", "shell_execution", "deep_recursive_dependency_traversal"),
        }
    )

    forbidden = set(result.get("forbidden_operations_detected", []))
    passed = (
        validate_query_result(result)
        and result.get("query_status") == "BLOCKED_BY_SCOPE_LOCK"
        and result.get("blocked") is True
        and result.get("records") == []
        and {"NETWORK_ACCESS", "SHELL_EXECUTION", "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL"}.issubset(forbidden)
        and result.get("network_access_allowed") is False
        and result.get("shell_execution_allowed") is False
        and result.get("deep_recursive_dependency_traversal_allowed") is False
    )

    expected = {
        "query_status": "BLOCKED_BY_SCOPE_LOCK",
        "blocked": True,
        "required_forbidden": ["NETWORK_ACCESS", "SHELL_EXECUTION", "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL"],
    }
    observed = {
        "query_status": result.get("query_status"),
        "blocked": result.get("blocked"),
        "forbidden_operations_detected": sorted(forbidden),
    }
    return _case("SCOPE_LOCK_REGRESSION_GUARD_BLOCKS_FORBIDDEN_OPERATIONS", passed, expected, observed, "SCOPE_LOCK_GUARD_REGRESSION")


def run_query_interface_regression_integration() -> dict[str, Any]:
    case_results = [
        _validate_task_4_report_artifact(),
        _validate_task_3_primary_query_stability(),
        _validate_task_3_blocked_query_stability(),
        _validate_runtime_validation_report_stability(),
        _validate_case_matrix_integrated(),
        _validate_scope_lock_regression_guard(),
    ]

    pass_count = sum(1 for item in case_results if item["passed"])
    fail_count = len(case_results) - pass_count

    integration_passed = (
        len(case_results) == REGRESSION_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "query_interface_revision": QUERY_INTERFACE_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "regression_revision": REGRESSION_REVISION,
        "task_3_id": TASK_3_ID,
        "task_4_id": TASK_4_ID,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "task_5_signature": task_5_signature(),
        "local_only": LOCAL_ONLY,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "scope_lock_enforced": True,
        "regression_case_count": len(case_results),
        "required_pass_count": REQUIRED_PASS_COUNT,
        "required_fail_count": REQUIRED_FAIL_COUNT,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "integration_passed": integration_passed,
        "integration_status": "INTEGRATED" if integration_passed else "INVALID",
        "case_results": case_results,
    }

    report["integration_id"] = "MILESTONE-27-QUERY-REGRESSION-" + _stable_digest(report)
    report["integration_signature"] = _stable_digest(
        {
            "integration_id": report["integration_id"],
            "case_results": case_results,
            "regression_revision": REGRESSION_REVISION,
        }
    )
    report["next_stage"] = NEXT_STAGE
    return report


def validate_regression_integration_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("query_interface_revision") != QUERY_INTERFACE_REVISION:
        return False
    if report.get("validation_revision") != VALIDATION_REVISION:
        return False
    if report.get("regression_revision") != REGRESSION_REVISION:
        return False
    if report.get("local_only") is not True:
        return False
    if report.get("network_access_allowed") is not False:
        return False
    if report.get("shell_execution_allowed") is not False:
        return False
    if report.get("deep_recursive_dependency_traversal_allowed") is not False:
        return False
    if report.get("scope_lock_enforced") is not True:
        return False
    if report.get("regression_case_count") != REGRESSION_CASE_COUNT:
        return False
    if report.get("pass_count") != REQUIRED_PASS_COUNT:
        return False
    if report.get("fail_count") != REQUIRED_FAIL_COUNT:
        return False
    if report.get("integration_status") != "INTEGRATED":
        return False
    if not all(item.get("passed") is True for item in report.get("case_results", [])):
        return False
    return bool(report.get("integration_passed"))


def render_regression_integration_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 27 Task 5 Query Interface Regression Integration Report",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"INTEGRATION_STATUS={report.get('integration_status')}",
        f"INTEGRATION_ID={report.get('integration_id')}",
        f"SCOPE_LOCK_ID={report.get('scope_lock_id')}",
        f"QUERY_INTERFACE_REVISION={report.get('query_interface_revision')}",
        f"VALIDATION_REVISION={report.get('validation_revision')}",
        f"REGRESSION_REVISION={report.get('regression_revision')}",
        f"TASK_5_SIGNATURE={report.get('task_5_signature')}",
        f"INTEGRATION_SIGNATURE={report.get('integration_signature')}",
        f"REGRESSION_CASE_COUNT={report.get('regression_case_count')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        "",
        "## Regression cases",
    ]

    for case in report.get("case_results", []):
        lines.extend(
            [
                f"- {case['case_id']}",
                f"  - passed: {str(case['passed']).lower()}",
                f"  - failure_reason: {case['failure_reason']}",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def write_task_5_artifacts(base_dir: str | Path = "examples/milestone-27/query-interface-regression-integration-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_query_interface_regression_integration()
    case_matrix = {
        "task_id": TASK_ID,
        "integration_id": report["integration_id"],
        "case_count": report["regression_case_count"],
        "case_results": report["case_results"],
    }
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "query_interface_revision": QUERY_INTERFACE_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "regression_revision": REGRESSION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "task_5_signature": task_5_signature(),
        "integration_id": report["integration_id"],
        "integration_signature": report["integration_signature"],
        "integration_status": report["integration_status"],
        "integration_passed": report["integration_passed"],
        "generated_artifact_count": 5,
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
    (output_dir / "task-5-regression-cases.json").write_text(
        json.dumps(case_matrix, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-5-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-5-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"QUERY_INTERFACE_REVISION={QUERY_INTERFACE_REVISION}",
                f"VALIDATION_REVISION={VALIDATION_REVISION}",
                f"REGRESSION_REVISION={REGRESSION_REVISION}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"TASK_4_SIGNATURE={task_4_signature()}",
                f"TASK_5_SIGNATURE={task_5_signature()}",
                f"INTEGRATION_ID={report['integration_id']}",
                f"INTEGRATION_SIGNATURE={report['integration_signature']}",
                f"INTEGRATION_STATUS={report['integration_status']}",
                f"REGRESSION_CASE_COUNT={report['regression_case_count']}",
                f"PASS_COUNT={report['pass_count']}",
                f"FAIL_COUNT={report['fail_count']}",
                "LOCAL_ONLY=true",
                "NETWORK_ACCESS_ALLOWED=false",
                "SHELL_EXECUTION_ALLOWED=false",
                "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_5_status_lines() -> tuple[str, ...]:
    report = run_query_interface_regression_integration()
    return (
        "MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_READY=true",
        f"MILESTONE_27_TASK_5_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_27_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_27_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_27_TASK_5_QUERY_INTERFACE_REVISION={QUERY_INTERFACE_REVISION}",
        f"MILESTONE_27_TASK_5_VALIDATION_REVISION={VALIDATION_REVISION}",
        f"MILESTONE_27_TASK_5_REGRESSION_REVISION={REGRESSION_REVISION}",
        f"MILESTONE_27_TASK_5_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_27_TASK_5_TASK_4_SIGNATURE={task_4_signature()}",
        f"MILESTONE_27_TASK_5_TASK_5_SIGNATURE={task_5_signature()}",
        f"MILESTONE_27_TASK_5_INTEGRATION_ID={report['integration_id']}",
        f"MILESTONE_27_TASK_5_INTEGRATION_SIGNATURE={report['integration_signature']}",
        f"MILESTONE_27_TASK_5_INTEGRATION_STATUS={report['integration_status']}",
        f"MILESTONE_27_TASK_5_REGRESSION_CASE_COUNT={report['regression_case_count']}",
        f"MILESTONE_27_TASK_5_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_27_TASK_5_FAIL_COUNT={report['fail_count']}",
        "MILESTONE_27_TASK_5_LOCAL_ONLY=true",
        "MILESTONE_27_TASK_5_NETWORK_ACCESS_ALLOWED=false",
        "MILESTONE_27_TASK_5_SHELL_EXECUTION_ALLOWED=false",
        "MILESTONE_27_TASK_5_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
        "MILESTONE_27_TASK_5_GENERATED_ARTIFACT_COUNT=5",
        f"MILESTONE_27_TASK_5_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_27_TASK_5_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_27_TASK_5_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    artifacts = write_task_5_artifacts()
    for line in task_5_status_lines():
        print(line)
