from __future__ import annotations

from dataclasses import asdict, dataclass
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


MILESTONE_ID = "MILESTONE_27"
TASK_ID = "MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_V1"
SOURCE_TASK_ID = TASK_3_ID
VALIDATION_REVISION = "MILESTONE_27_QUERY_INTERFACE_VALIDATION_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 4
NEXT_STAGE = "MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_V1"

VALIDATION_CASE_COUNT = 6
REQUIRED_READY_CASE_COUNT = 4
REQUIRED_BLOCKED_CASE_COUNT = 2

_VALIDATION_SIGNATURE_SEED = {
    "task_id": TASK_ID,
    "source_task_id": SOURCE_TASK_ID,
    "selected_objective_id": SELECTED_OBJECTIVE_ID,
    "scope_lock_id": SCOPE_LOCK_ID,
    "query_interface_revision": QUERY_INTERFACE_REVISION,
    "validation_revision": VALIDATION_REVISION,
    "case_count": VALIDATION_CASE_COUNT,
}


@dataclass(frozen=True)
class QueryValidationCase:
    case_id: str
    query: Mapping[str, Any]
    expected_query_status: str
    expected_matched_count: int | None = None
    expected_blocked: bool | None = None
    expected_milestone_id: str | None = None
    expected_evidence_present: bool | None = None


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def task_4_signature() -> str:
    return _stable_digest(_VALIDATION_SIGNATURE_SEED)


def build_validation_cases() -> tuple[QueryValidationCase, ...]:
    return (
        QueryValidationCase(
            case_id="READY_MILESTONE_26_EXACT",
            query={"milestone_id": "MILESTONE_26", "local_only": True},
            expected_query_status="READY",
            expected_matched_count=1,
            expected_blocked=False,
            expected_milestone_id="MILESTONE_26",
            expected_evidence_present=True,
        ),
        QueryValidationCase(
            case_id="READY_CLOSED_PASS_FILTER",
            query={
                "archive_status": "CLOSED",
                "technical_status": "PASS",
                "final_task_number_lte": 8,
                "local_only": True,
            },
            expected_query_status="READY",
            expected_matched_count=2,
            expected_blocked=False,
            expected_evidence_present=True,
        ),
        QueryValidationCase(
            case_id="READY_SUPPRESS_EVIDENCE",
            query={"milestone_id": "MILESTONE_26", "include_evidence": False, "local_only": True},
            expected_query_status="READY",
            expected_matched_count=1,
            expected_blocked=False,
            expected_milestone_id="MILESTONE_26",
            expected_evidence_present=False,
        ),
        QueryValidationCase(
            case_id="READY_LIMIT_ONE",
            query={"archive_status": "CLOSED", "technical_status": "PASS", "limit": 1, "local_only": True},
            expected_query_status="READY",
            expected_matched_count=1,
            expected_blocked=False,
            expected_evidence_present=True,
        ),
        QueryValidationCase(
            case_id="BLOCK_NON_LOCAL",
            query={"milestone_id": "MILESTONE_26", "local_only": False},
            expected_query_status="BLOCKED_BY_SCOPE_LOCK",
            expected_matched_count=0,
            expected_blocked=True,
        ),
        QueryValidationCase(
            case_id="BLOCK_FORBIDDEN_NETWORK_AND_DEEP_SCAN",
            query={
                "milestone_id": "MILESTONE_26",
                "local_only": True,
                "forbidden_operations": ("network_access", "deep_recursive_dependency_traversal"),
            },
            expected_query_status="BLOCKED_BY_SCOPE_LOCK",
            expected_matched_count=0,
            expected_blocked=True,
        ),
    )


def _case_failure_reason(case: QueryValidationCase, result: Mapping[str, Any]) -> str | None:
    if not validate_query_result(result):
        return "RESULT_CONTRACT_INVALID"

    if result.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return "SELECTED_OBJECTIVE_MISMATCH"

    if result.get("scope_lock_id") != SCOPE_LOCK_ID:
        return "SCOPE_LOCK_MISMATCH"

    if result.get("query_interface_revision") != QUERY_INTERFACE_REVISION:
        return "QUERY_INTERFACE_REVISION_MISMATCH"

    if result.get("query_status") != case.expected_query_status:
        return "QUERY_STATUS_MISMATCH"

    if case.expected_blocked is not None and result.get("blocked") is not case.expected_blocked:
        return "BLOCKED_FLAG_MISMATCH"

    if case.expected_matched_count is not None and result.get("matched_count") != case.expected_matched_count:
        return "MATCHED_COUNT_MISMATCH"

    if result.get("local_only") is not True:
        return "LOCAL_ONLY_NOT_ENFORCED"

    if result.get("network_access_allowed") is not False:
        return "NETWORK_ACCESS_NOT_BLOCKED"

    if result.get("shell_execution_allowed") is not False:
        return "SHELL_EXECUTION_NOT_BLOCKED"

    if result.get("deep_recursive_dependency_traversal_allowed") is not False:
        return "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_NOT_BLOCKED"

    records = result.get("records", [])

    if case.expected_milestone_id is not None:
        if not records:
            return "EXPECTED_RECORD_MISSING"
        if records[0].get("milestone_id") != case.expected_milestone_id:
            return "EXPECTED_MILESTONE_ID_MISMATCH"

    if case.expected_evidence_present is not None and records:
        evidence = records[0].get("evidence_bundle", [])
        if case.expected_evidence_present and not evidence:
            return "EXPECTED_EVIDENCE_MISSING"
        if not case.expected_evidence_present and evidence:
            return "EVIDENCE_SUPPRESSION_FAILED"

    return None


def validate_case(case: QueryValidationCase) -> dict[str, Any]:
    result = query_closed_milestone_archive_index(case.query)
    failure_reason = _case_failure_reason(case, result)

    return {
        "case_id": case.case_id,
        "query": dict(case.query),
        "expected_query_status": case.expected_query_status,
        "actual_query_status": result.get("query_status"),
        "expected_matched_count": case.expected_matched_count,
        "actual_matched_count": result.get("matched_count"),
        "expected_blocked": case.expected_blocked,
        "actual_blocked": result.get("blocked"),
        "passed": failure_reason is None,
        "failure_reason": failure_reason or "NONE",
        "query_id": result.get("query_id"),
        "result_signature": result.get("result_signature"),
        "forbidden_operations_detected": list(result.get("forbidden_operations_detected", [])),
    }


def run_query_interface_validation() -> dict[str, Any]:
    cases = build_validation_cases()
    case_results = [validate_case(case) for case in cases]

    pass_count = sum(1 for item in case_results if item["passed"])
    fail_count = len(case_results) - pass_count
    ready_case_count = sum(1 for item in case_results if item["actual_query_status"] == "READY")
    blocked_case_count = sum(1 for item in case_results if item["actual_query_status"] == "BLOCKED_BY_SCOPE_LOCK")

    validation_passed = (
        fail_count == 0
        and pass_count == VALIDATION_CASE_COUNT
        and ready_case_count == REQUIRED_READY_CASE_COUNT
        and blocked_case_count == REQUIRED_BLOCKED_CASE_COUNT
    )

    payload = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "query_interface_revision": QUERY_INTERFACE_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "local_only": LOCAL_ONLY,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "scope_lock_enforced": True,
        "validation_case_count": len(case_results),
        "required_ready_case_count": REQUIRED_READY_CASE_COUNT,
        "required_blocked_case_count": REQUIRED_BLOCKED_CASE_COUNT,
        "ready_case_count": ready_case_count,
        "blocked_case_count": blocked_case_count,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "validation_passed": validation_passed,
        "validation_status": "VALID" if validation_passed else "INVALID",
        "case_results": case_results,
    }

    payload["validation_id"] = "MILESTONE-27-QUERY-VALIDATION-" + _stable_digest(payload)
    payload["validation_signature"] = _stable_digest(
        {
            "validation_id": payload["validation_id"],
            "case_results": case_results,
            "validation_revision": VALIDATION_REVISION,
        }
    )
    payload["next_stage"] = NEXT_STAGE
    return payload


def validate_validation_report(report: Mapping[str, Any]) -> bool:
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
    if report.get("local_only") is not True:
        return False
    if report.get("network_access_allowed") is not False:
        return False
    if report.get("deep_recursive_dependency_traversal_allowed") is not False:
        return False
    if report.get("scope_lock_enforced") is not True:
        return False
    if report.get("validation_case_count") != VALIDATION_CASE_COUNT:
        return False
    if report.get("pass_count") != VALIDATION_CASE_COUNT:
        return False
    if report.get("fail_count") != 0:
        return False
    if report.get("ready_case_count") != REQUIRED_READY_CASE_COUNT:
        return False
    if report.get("blocked_case_count") != REQUIRED_BLOCKED_CASE_COUNT:
        return False
    if report.get("validation_status") != "VALID":
        return False
    return bool(report.get("validation_passed"))


def render_validation_report_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 27 Task 4 Query Interface Validation Report",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"VALIDATION_STATUS={report.get('validation_status')}",
        f"VALIDATION_ID={report.get('validation_id')}",
        f"SCOPE_LOCK_ID={report.get('scope_lock_id')}",
        f"QUERY_INTERFACE_REVISION={report.get('query_interface_revision')}",
        f"VALIDATION_REVISION={report.get('validation_revision')}",
        f"TASK_4_SIGNATURE={report.get('task_4_signature')}",
        f"VALIDATION_SIGNATURE={report.get('validation_signature')}",
        f"VALIDATION_CASE_COUNT={report.get('validation_case_count')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"READY_CASE_COUNT={report.get('ready_case_count')}",
        f"BLOCKED_CASE_COUNT={report.get('blocked_case_count')}",
        "",
        "## Cases",
    ]

    for case in report.get("case_results", []):
        lines.extend(
            [
                f"- {case['case_id']}",
                f"  - passed: {str(case['passed']).lower()}",
                f"  - expected_query_status: {case['expected_query_status']}",
                f"  - actual_query_status: {case['actual_query_status']}",
                f"  - failure_reason: {case['failure_reason']}",
                f"  - query_id: {case['query_id']}",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def write_task_4_artifacts(base_dir: str | Path = "examples/milestone-27/query-interface-validation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_query_interface_validation()
    case_matrix = {
        "task_id": TASK_ID,
        "validation_id": report["validation_id"],
        "case_count": report["validation_case_count"],
        "case_results": report["case_results"],
    }
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "query_interface_revision": QUERY_INTERFACE_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "validation_id": report["validation_id"],
        "validation_signature": report["validation_signature"],
        "validation_status": report["validation_status"],
        "validation_passed": report["validation_passed"],
        "generated_artifact_count": 5,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-4-validation-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-validation-report.md").write_text(
        render_validation_report_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-4-validation-cases.json").write_text(
        json.dumps(case_matrix, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"QUERY_INTERFACE_REVISION={QUERY_INTERFACE_REVISION}",
                f"VALIDATION_REVISION={VALIDATION_REVISION}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"TASK_4_SIGNATURE={task_4_signature()}",
                f"VALIDATION_ID={report['validation_id']}",
                f"VALIDATION_SIGNATURE={report['validation_signature']}",
                f"VALIDATION_STATUS={report['validation_status']}",
                f"VALIDATION_CASE_COUNT={report['validation_case_count']}",
                f"PASS_COUNT={report['pass_count']}",
                f"FAIL_COUNT={report['fail_count']}",
                f"READY_CASE_COUNT={report['ready_case_count']}",
                f"BLOCKED_CASE_COUNT={report['blocked_case_count']}",
                "LOCAL_ONLY=true",
                "NETWORK_ACCESS_ALLOWED=false",
                "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_4_status_lines() -> tuple[str, ...]:
    report = run_query_interface_validation()
    return (
        "MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_READY=true",
        f"MILESTONE_27_TASK_4_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_27_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_27_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_27_TASK_4_QUERY_INTERFACE_REVISION={QUERY_INTERFACE_REVISION}",
        f"MILESTONE_27_TASK_4_VALIDATION_REVISION={VALIDATION_REVISION}",
        f"MILESTONE_27_TASK_4_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_27_TASK_4_TASK_4_SIGNATURE={task_4_signature()}",
        f"MILESTONE_27_TASK_4_VALIDATION_ID={report['validation_id']}",
        f"MILESTONE_27_TASK_4_VALIDATION_SIGNATURE={report['validation_signature']}",
        f"MILESTONE_27_TASK_4_VALIDATION_STATUS={report['validation_status']}",
        f"MILESTONE_27_TASK_4_VALIDATION_CASE_COUNT={report['validation_case_count']}",
        f"MILESTONE_27_TASK_4_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_27_TASK_4_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_27_TASK_4_READY_CASE_COUNT={report['ready_case_count']}",
        f"MILESTONE_27_TASK_4_BLOCKED_CASE_COUNT={report['blocked_case_count']}",
        "MILESTONE_27_TASK_4_LOCAL_ONLY=true",
        "MILESTONE_27_TASK_4_NETWORK_ACCESS_ALLOWED=false",
        "MILESTONE_27_TASK_4_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
        "MILESTONE_27_TASK_4_GENERATED_ARTIFACT_COUNT=5",
        f"MILESTONE_27_TASK_4_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_27_TASK_4_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_27_TASK_4_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    artifacts = write_task_4_artifacts()
    for line in task_4_status_lines():
        print(line)
