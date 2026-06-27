from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_28_query_result_export import (
    ALLOWED_OUTPUT_FORMATS,
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    EXPORT_REVISION,
    FORBIDDEN_OPERATIONS,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID as TASK_3_SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_export_payload,
    task_3_signature,
    validate_export_payload,
)


TASK_ID = "MILESTONE_28_TASK_4_QUERY_RESULT_EXPORT_VALIDATION_V1"
VALIDATION_REVISION = "MILESTONE_28_QUERY_RESULT_EXPORT_VALIDATION_V1"

MILESTONE_ID = "MILESTONE_28"
CURRENT_TASK_NUMBER = 4
NEXT_STAGE = "MILESTONE_28_TASK_5_QUERY_RESULT_EXPORT_REGRESSION_INTEGRATION_V1"

VALIDATION_STATUS = "VALID"
VALIDATION_CASE_COUNT = 6
REQUIRED_PASS_COUNT = 6
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

EXPORT_JSON_PATH = Path("examples/milestone-28/query-result-export-implementation-v1/task-3-query-result-export.json")
EXPORT_MD_PATH = Path("examples/milestone-28/query-result-export-implementation-v1/task-3-query-result-export.md")
EXPORT_INDEX_JSON_PATH = Path("examples/milestone-28/query-result-export-implementation-v1/task-3-export-index.json")
EXPORT_MANIFEST_PATH = Path("examples/milestone-28/query-result-export-implementation-v1/task-3-manifest.json")
EXPORT_INDEX_TXT_PATH = Path("examples/milestone-28/query-result-export-implementation-v1/task-3-index.txt")


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
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
            "export_revision": EXPORT_REVISION,
            "validation_revision": VALIDATION_REVISION,
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


def _validate_persisted_export_payload() -> dict[str, Any]:
    payload = _load_json(EXPORT_JSON_PATH)
    passed = (
        validate_export_payload(payload)
        and payload.get("export_status") == "READY"
        and payload.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and payload.get("scope_lock_id") == SCOPE_LOCK_ID
        and payload.get("exported_record_count") == 1
        and payload.get("current_task_number") == 3
        and payload.get("next_stage") == SOURCE_NEXT_STAGE
    )
    observed = {
        "export_status": payload.get("export_status"),
        "export_id": payload.get("export_id"),
        "export_signature": payload.get("export_signature"),
        "exported_record_count": payload.get("exported_record_count"),
        "next_stage": payload.get("next_stage"),
    }
    return _case(
        "PERSISTED_EXPORT_PAYLOAD_VALID",
        passed,
        {
            "export_status": "READY",
            "exported_record_count": 1,
            "next_stage": "MILESTONE_28_TASK_4_QUERY_RESULT_EXPORT_VALIDATION_V1",
        },
        observed,
        "PERSISTED_EXPORT_PAYLOAD_INVALID",
    )


def _validate_runtime_export_stability() -> dict[str, Any]:
    persisted = _load_json(EXPORT_JSON_PATH)
    runtime = build_export_payload()
    passed = (
        validate_export_payload(runtime)
        and persisted.get("export_id") == runtime.get("export_id")
        and persisted.get("export_signature") == runtime.get("export_signature")
        and persisted.get("task_3_signature") == runtime.get("task_3_signature") == task_3_signature()
        and persisted.get("exported_record_count") == runtime.get("exported_record_count") == 1
        and persisted.get("exported_records") == runtime.get("exported_records")
    )
    observed = {
        "persisted_export_id": persisted.get("export_id"),
        "runtime_export_id": runtime.get("export_id"),
        "persisted_export_signature": persisted.get("export_signature"),
        "runtime_export_signature": runtime.get("export_signature"),
        "runtime_record_count": runtime.get("exported_record_count"),
    }
    return _case(
        "RUNTIME_EXPORT_STABILITY_VALID",
        passed,
        {
            "stable_export_id": True,
            "stable_export_signature": True,
            "exported_record_count": 1,
        },
        observed,
        "RUNTIME_EXPORT_STABILITY_INVALID",
    )


def _validate_manifest_consistency() -> dict[str, Any]:
    payload = _load_json(EXPORT_JSON_PATH)
    manifest = _load_json(EXPORT_MANIFEST_PATH)
    passed = (
        manifest.get("task_id") == SOURCE_TASK_ID
        and manifest.get("source_task_id") == TASK_3_SOURCE_TASK_ID
        and manifest.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and manifest.get("scope_lock_id") == SCOPE_LOCK_ID
        and manifest.get("export_revision") == EXPORT_REVISION
        and manifest.get("export_id") == payload.get("export_id")
        and manifest.get("export_signature") == payload.get("export_signature")
        and manifest.get("export_status") == "READY"
        and manifest.get("exported_record_count") == payload.get("exported_record_count")
        and manifest.get("generated_artifact_count") == SOURCE_GENERATED_ARTIFACT_COUNT
        and manifest.get("next_stage") == SOURCE_NEXT_STAGE
    )
    observed = {
        "manifest_export_id": manifest.get("export_id"),
        "payload_export_id": payload.get("export_id"),
        "manifest_export_signature": manifest.get("export_signature"),
        "payload_export_signature": payload.get("export_signature"),
        "manifest_generated_artifact_count": manifest.get("generated_artifact_count"),
    }
    return _case(
        "EXPORT_MANIFEST_CONSISTENCY_VALID",
        passed,
        {
            "manifest_matches_payload": True,
            "generated_artifact_count": SOURCE_GENERATED_ARTIFACT_COUNT,
        },
        observed,
        "EXPORT_MANIFEST_CONSISTENCY_INVALID",
    )


def _validate_export_index_consistency() -> dict[str, Any]:
    payload = _load_json(EXPORT_JSON_PATH)
    export_index = _load_json(EXPORT_INDEX_JSON_PATH)
    passed = (
        export_index.get("task_id") == SOURCE_TASK_ID
        and export_index.get("export_id") == payload.get("export_id")
        and export_index.get("export_signature") == payload.get("export_signature")
        and export_index.get("exported_record_count") == payload.get("exported_record_count")
        and export_index.get("exported_records") == payload.get("exported_records")
    )
    observed = {
        "index_export_id": export_index.get("export_id"),
        "payload_export_id": payload.get("export_id"),
        "index_record_count": export_index.get("exported_record_count"),
        "payload_record_count": payload.get("exported_record_count"),
    }
    return _case(
        "EXPORT_INDEX_CONSISTENCY_VALID",
        passed,
        {"index_matches_payload": True},
        observed,
        "EXPORT_INDEX_CONSISTENCY_INVALID",
    )


def _validate_markdown_and_text_index_consistency() -> dict[str, Any]:
    payload = _load_json(EXPORT_JSON_PATH)
    markdown = EXPORT_MD_PATH.read_text(encoding="utf-8")
    index_text = EXPORT_INDEX_TXT_PATH.read_text(encoding="utf-8")
    passed = (
        payload.get("export_id") in markdown
        and payload.get("export_signature") in markdown
        and "MILESTONE_26" in markdown
        and "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_READY=true" in index_text
        and f"EXPORT_ID={payload.get('export_id')}" in index_text
        and f"EXPORT_SIGNATURE={payload.get('export_signature')}" in index_text
        and "EXPORT_STATUS=READY" in index_text
        and "EXPORTED_RECORD_COUNT=1" in index_text
        and "LOCAL_ONLY=true" in index_text
        and "NETWORK_ACCESS_ALLOWED=false" in index_text
        and f"NEXT_STAGE={SOURCE_NEXT_STAGE}" in index_text
    )
    observed = {
        "markdown_contains_export_id": payload.get("export_id") in markdown,
        "markdown_contains_milestone_26": "MILESTONE_26" in markdown,
        "index_contains_ready_marker": "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_READY=true" in index_text,
        "index_contains_export_status": "EXPORT_STATUS=READY" in index_text,
    }
    return _case(
        "MARKDOWN_AND_TEXT_INDEX_CONSISTENCY_VALID",
        passed,
        {"markdown_and_index_match_payload": True},
        observed,
        "MARKDOWN_AND_TEXT_INDEX_CONSISTENCY_INVALID",
    )


def _validate_scope_authority_guards() -> dict[str, Any]:
    payload = _load_json(EXPORT_JSON_PATH)
    passed = (
        payload.get("local_only") is True
        and payload.get("network_access_allowed") is False
        and payload.get("shell_execution_allowed") is False
        and payload.get("repository_mutation_allowed") is False
        and payload.get("remote_registry_lookup_allowed") is False
        and payload.get("deep_recursive_dependency_traversal_allowed") is False
        and payload.get("external_model_call_allowed") is False
        and tuple(payload.get("forbidden_operations", ())) == FORBIDDEN_OPERATIONS
        and tuple(payload.get("export_formats", ())) == ALLOWED_OUTPUT_FORMATS
    )
    observed = {
        "local_only": payload.get("local_only"),
        "network_access_allowed": payload.get("network_access_allowed"),
        "shell_execution_allowed": payload.get("shell_execution_allowed"),
        "remote_registry_lookup_allowed": payload.get("remote_registry_lookup_allowed"),
        "deep_recursive_dependency_traversal_allowed": payload.get("deep_recursive_dependency_traversal_allowed"),
        "external_model_call_allowed": payload.get("external_model_call_allowed"),
        "forbidden_operation_count": len(payload.get("forbidden_operations", ())),
        "allowed_output_format_count": len(payload.get("export_formats", ())),
    }
    return _case(
        "SCOPE_AUTHORITY_GUARDS_VALID",
        passed,
        {
            "local_only": True,
            "network_access_allowed": False,
            "forbidden_operation_count": len(FORBIDDEN_OPERATIONS),
            "allowed_output_format_count": len(ALLOWED_OUTPUT_FORMATS),
        },
        observed,
        "SCOPE_AUTHORITY_GUARDS_INVALID",
    )


def run_query_result_export_validation() -> dict[str, Any]:
    case_results = [
        _validate_persisted_export_payload(),
        _validate_runtime_export_stability(),
        _validate_manifest_consistency(),
        _validate_export_index_consistency(),
        _validate_markdown_and_text_index_consistency(),
        _validate_scope_authority_guards(),
    ]

    pass_count = sum(1 for case in case_results if case["passed"])
    fail_count = len(case_results) - pass_count
    validation_passed = (
        len(case_results) == VALIDATION_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    payload = _load_json(EXPORT_JSON_PATH)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "export_revision": EXPORT_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "source_export_id": payload.get("export_id"),
        "source_export_signature": payload.get("export_signature"),
        "source_export_status": payload.get("export_status"),
        "source_exported_record_count": payload.get("exported_record_count"),
        "validation_status": VALIDATION_STATUS if validation_passed else "INVALID",
        "validation_case_count": len(case_results),
        "required_pass_count": REQUIRED_PASS_COUNT,
        "required_fail_count": REQUIRED_FAIL_COUNT,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "validation_passed": validation_passed,
        "case_results": case_results,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "next_stage": NEXT_STAGE,
    }

    report["validation_id"] = "MILESTONE-28-QUERY-EXPORT-VALIDATION-" + _stable_digest(report)
    report["validation_signature"] = _stable_digest(
        {
            "validation_id": report["validation_id"],
            "source_export_id": report["source_export_id"],
            "source_export_signature": report["source_export_signature"],
            "case_results": case_results,
            "validation_revision": VALIDATION_REVISION,
        }
    )
    return report


def validate_validation_report(report: Mapping[str, Any]) -> bool:
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
    if report.get("export_revision") != EXPORT_REVISION:
        return False
    if report.get("validation_revision") != VALIDATION_REVISION:
        return False
    if report.get("validation_status") != VALIDATION_STATUS:
        return False
    if report.get("validation_case_count") != VALIDATION_CASE_COUNT:
        return False
    if report.get("pass_count") != REQUIRED_PASS_COUNT:
        return False
    if report.get("fail_count") != REQUIRED_FAIL_COUNT:
        return False
    if report.get("source_export_status") != "READY":
        return False
    if report.get("source_exported_record_count") != 1:
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    if not all(case.get("passed") is True for case in report.get("case_results", [])):
        return False
    return bool(report.get("validation_passed"))


def render_validation_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 28 Task 4 Query Result Export Validation",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"VALIDATION_STATUS={report.get('validation_status')}",
        f"VALIDATION_ID={report.get('validation_id')}",
        f"VALIDATION_SIGNATURE={report.get('validation_signature')}",
        f"SOURCE_EXPORT_ID={report.get('source_export_id')}",
        f"SOURCE_EXPORT_SIGNATURE={report.get('source_export_signature')}",
        f"SOURCE_EXPORT_STATUS={report.get('source_export_status')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Validation cases",
    ]
    for case in report.get("case_results", []):
        lines.append(f"- {case['case_id']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_4_artifacts(base_dir: str | Path = "examples/milestone-28/query-result-export-validation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_query_result_export_validation()
    cases = {
        "task_id": TASK_ID,
        "validation_id": report["validation_id"],
        "validation_status": report["validation_status"],
        "validation_case_count": report["validation_case_count"],
        "case_results": report["case_results"],
    }
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "validation_revision": VALIDATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "validation_id": report["validation_id"],
        "validation_signature": report["validation_signature"],
        "validation_status": report["validation_status"],
        "validation_passed": report["validation_passed"],
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
        json.dumps(cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_28_TASK_4_QUERY_RESULT_EXPORT_VALIDATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"EXPORT_REVISION={EXPORT_REVISION}",
                f"VALIDATION_REVISION={VALIDATION_REVISION}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"TASK_4_SIGNATURE={task_4_signature()}",
                f"SOURCE_EXPORT_ID={report['source_export_id']}",
                f"SOURCE_EXPORT_SIGNATURE={report['source_export_signature']}",
                f"SOURCE_EXPORT_STATUS={report['source_export_status']}",
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
    report = run_query_result_export_validation()
    return (
        "MILESTONE_28_TASK_4_QUERY_RESULT_EXPORT_VALIDATION_READY=true",
        f"MILESTONE_28_TASK_4_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_28_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_28_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_28_TASK_4_EXPORT_REVISION={EXPORT_REVISION}",
        f"MILESTONE_28_TASK_4_VALIDATION_REVISION={VALIDATION_REVISION}",
        f"MILESTONE_28_TASK_4_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_28_TASK_4_TASK_4_SIGNATURE={task_4_signature()}",
        f"MILESTONE_28_TASK_4_SOURCE_EXPORT_ID={report['source_export_id']}",
        f"MILESTONE_28_TASK_4_SOURCE_EXPORT_SIGNATURE={report['source_export_signature']}",
        f"MILESTONE_28_TASK_4_SOURCE_EXPORT_STATUS={report['source_export_status']}",
        f"MILESTONE_28_TASK_4_VALIDATION_ID={report['validation_id']}",
        f"MILESTONE_28_TASK_4_VALIDATION_SIGNATURE={report['validation_signature']}",
        f"MILESTONE_28_TASK_4_VALIDATION_STATUS={report['validation_status']}",
        f"MILESTONE_28_TASK_4_VALIDATION_CASE_COUNT={report['validation_case_count']}",
        f"MILESTONE_28_TASK_4_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_28_TASK_4_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_28_TASK_4_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_28_TASK_4_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_28_TASK_4_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_28_TASK_4_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    artifacts = write_task_4_artifacts()
    for line in task_4_status_lines():
        print(line)
