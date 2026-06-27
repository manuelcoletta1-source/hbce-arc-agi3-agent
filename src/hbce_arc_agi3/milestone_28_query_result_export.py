from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_28_objective_scope_lock import (
    ALLOWED_INPUT_ARTIFACTS,
    ALLOWED_OUTPUT_FORMATS,
    FORBIDDEN_OPERATIONS,
    LOCAL_ONLY,
    MILESTONE_ID,
    NETWORK_ACCESS_ALLOWED,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    run_objective_scope_lock,
    task_2_signature,
    validate_objective_scope_lock_report,
)


TASK_ID = "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_V1"
EXPORT_REVISION = "MILESTONE_28_QUERY_RESULT_EXPORT_IMPLEMENTATION_V1"

CURRENT_TASK_NUMBER = 3
NEXT_STAGE = "MILESTONE_28_TASK_4_QUERY_RESULT_EXPORT_VALIDATION_V1"

IMPLEMENTATION_STARTED = True
IMPLEMENTATION_COMPLETE = True
IMPLEMENTATION_LOCAL_ONLY = True

NETWORK_ACCESS_ALLOWED = False
SHELL_EXECUTION_ALLOWED = False
REPOSITORY_MUTATION_ALLOWED = False
REMOTE_REGISTRY_LOOKUP_ALLOWED = False
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
EXTERNAL_MODEL_CALL_ALLOWED = False

GENERATED_ARTIFACT_COUNT = 5

PRIMARY_QUERY_RESULT_PATH = Path("examples/milestone-27/query-interface-implementation-v1/task-3-query-interface-result.json")
BLOCKED_QUERY_RESULT_PATH = Path("examples/milestone-27/query-interface-implementation-v1/task-3-query-interface-blocked-result.json")
TASK_4_VALIDATION_REPORT_PATH = Path("examples/milestone-27/query-interface-validation-v1/task-4-validation-report.json")
TASK_5_REGRESSION_REPORT_PATH = Path("examples/milestone-27/query-interface-regression-integration-v1/task-5-regression-integration-report.json")
TASK_6_FINAL_CLOSURE_REPORT_PATH = Path("examples/milestone-27/query-interface-final-closure-v1/task-6-final-closure-report.json")
TASK_2_SCOPE_LOCK_REPORT_PATH = Path("examples/milestone-28/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.json")


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
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
            "export_revision": EXPORT_REVISION,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "next_stage": NEXT_STAGE,
        }
    )


def build_scope_lock_snapshot() -> dict[str, Any]:
    runtime = run_objective_scope_lock()
    persisted = _load_json(TASK_2_SCOPE_LOCK_REPORT_PATH)
    runtime_valid = validate_objective_scope_lock_report(runtime)
    persisted_valid = validate_objective_scope_lock_report(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_scope_lock_artifact_id": runtime.get("scope_lock_artifact_id"),
        "persisted_scope_lock_artifact_id": persisted.get("scope_lock_artifact_id"),
        "runtime_scope_lock_signature": runtime.get("scope_lock_signature"),
        "persisted_scope_lock_signature": persisted.get("scope_lock_signature"),
        "selected_objective_id": runtime.get("selected_objective_id"),
        "scope_lock_id": runtime.get("scope_lock_id"),
        "task_2_signature": task_2_signature(),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_scope_lock": runtime.get("scope_lock_artifact_id") == persisted.get("scope_lock_artifact_id")
        and runtime.get("scope_lock_signature") == persisted.get("scope_lock_signature"),
    }


def validate_scope_lock_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_scope_lock"))


def build_export_payload() -> dict[str, Any]:
    primary = _load_json(PRIMARY_QUERY_RESULT_PATH)
    blocked = _load_json(BLOCKED_QUERY_RESULT_PATH)
    validation = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    regression = _load_json(TASK_5_REGRESSION_REPORT_PATH)
    closure = _load_json(TASK_6_FINAL_CLOSURE_REPORT_PATH)
    scope_snapshot = build_scope_lock_snapshot()

    records = primary.get("records", [])
    exported_records = [
        {
            "milestone_id": record.get("milestone_id"),
            "archive_status": record.get("archive_status"),
            "technical_status": record.get("technical_status"),
            "process_status": record.get("process_status"),
            "final_task_number": record.get("final_task_number"),
            "closure_commit": record.get("closure_commit"),
            "closure_signature": record.get("closure_signature"),
        }
        for record in records
    ]

    payload = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "export_revision": EXPORT_REVISION,
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "scope_lock_snapshot": scope_snapshot,
        "scope_lock_valid": validate_scope_lock_snapshot(scope_snapshot),
        "local_only": LOCAL_ONLY,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_complete": IMPLEMENTATION_COMPLETE,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "repository_mutation_allowed": REPOSITORY_MUTATION_ALLOWED,
        "remote_registry_lookup_allowed": REMOTE_REGISTRY_LOOKUP_ALLOWED,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "external_model_call_allowed": EXTERNAL_MODEL_CALL_ALLOWED,
        "allowed_input_artifacts": list(ALLOWED_INPUT_ARTIFACTS),
        "allowed_output_formats": list(ALLOWED_OUTPUT_FORMATS),
        "forbidden_operations": list(FORBIDDEN_OPERATIONS),
        "source_primary_query_id": primary.get("query_id"),
        "source_primary_result_signature": primary.get("result_signature"),
        "source_blocked_query_id": blocked.get("query_id"),
        "source_blocked_result_signature": blocked.get("result_signature"),
        "source_validation_id": validation.get("validation_id"),
        "source_validation_signature": validation.get("validation_signature"),
        "source_integration_id": regression.get("integration_id"),
        "source_integration_signature": regression.get("integration_signature"),
        "source_closure_id": closure.get("closure_id"),
        "source_closure_signature": closure.get("closure_signature"),
        "exported_record_count": len(exported_records),
        "exported_records": exported_records,
        "export_formats": list(ALLOWED_OUTPUT_FORMATS),
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "next_stage": NEXT_STAGE,
    }

    payload["export_id"] = "MILESTONE-28-QUERY-EXPORT-" + _stable_digest(payload)
    payload["export_signature"] = _stable_digest(
        {
            "export_id": payload["export_id"],
            "exported_records": exported_records,
            "source_primary_result_signature": payload["source_primary_result_signature"],
            "source_blocked_result_signature": payload["source_blocked_result_signature"],
            "export_revision": EXPORT_REVISION,
        }
    )
    payload["export_status"] = "READY" if validate_export_payload(payload) else "INVALID"
    return payload


def validate_export_payload(payload: Mapping[str, Any]) -> bool:
    if payload.get("task_id") != TASK_ID:
        return False
    if payload.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if payload.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if payload.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if payload.get("export_revision") != EXPORT_REVISION:
        return False
    if payload.get("scope_lock_valid") is not True:
        return False
    if payload.get("local_only") is not True:
        return False
    if payload.get("implementation_started") is not True:
        return False
    if payload.get("implementation_complete") is not True:
        return False
    if payload.get("network_access_allowed") is not False:
        return False
    if payload.get("shell_execution_allowed") is not False:
        return False
    if payload.get("remote_registry_lookup_allowed") is not False:
        return False
    if payload.get("deep_recursive_dependency_traversal_allowed") is not False:
        return False
    if payload.get("external_model_call_allowed") is not False:
        return False
    if payload.get("exported_record_count") < 1:
        return False
    if tuple(payload.get("export_formats", ())) != ALLOWED_OUTPUT_FORMATS:
        return False
    if tuple(payload.get("forbidden_operations", ())) != FORBIDDEN_OPERATIONS:
        return False
    if payload.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if payload.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if payload.get("next_stage") != NEXT_STAGE:
        return False
    return True


def render_export_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 28 Task 3 Query Result Export",
        "",
        f"TASK_ID={payload.get('task_id')}",
        f"SOURCE_TASK_ID={payload.get('source_task_id')}",
        f"EXPORT_STATUS={payload.get('export_status')}",
        f"EXPORT_ID={payload.get('export_id')}",
        f"EXPORT_SIGNATURE={payload.get('export_signature')}",
        f"SELECTED_OBJECTIVE_ID={payload.get('selected_objective_id')}",
        f"SCOPE_LOCK_ID={payload.get('scope_lock_id')}",
        f"EXPORT_REVISION={payload.get('export_revision')}",
        f"TASK_3_SIGNATURE={payload.get('task_3_signature')}",
        f"EXPORTED_RECORD_COUNT={payload.get('exported_record_count')}",
        f"LOCAL_ONLY={str(payload.get('local_only')).lower()}",
        f"NETWORK_ACCESS_ALLOWED={str(payload.get('network_access_allowed')).lower()}",
        f"DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED={str(payload.get('deep_recursive_dependency_traversal_allowed')).lower()}",
        f"NEXT_STAGE={payload.get('next_stage')}",
        "",
        "## Exported records",
    ]

    for record in payload.get("exported_records", []):
        lines.append(
            f"- {record.get('milestone_id')} / {record.get('archive_status')} / "
            f"{record.get('technical_status')} / final_task={record.get('final_task_number')}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_3_artifacts(base_dir: str | Path = "examples/milestone-28/query-result-export-implementation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = build_export_payload()
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "export_revision": EXPORT_REVISION,
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "export_id": payload["export_id"],
        "export_signature": payload["export_signature"],
        "export_status": payload["export_status"],
        "exported_record_count": payload["exported_record_count"],
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    export_index = {
        "task_id": TASK_ID,
        "export_id": payload["export_id"],
        "export_signature": payload["export_signature"],
        "exported_record_count": payload["exported_record_count"],
        "exported_records": payload["exported_records"],
    }

    (output_dir / "task-3-query-result-export.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-query-result-export.md").write_text(
        render_export_markdown(payload),
        encoding="utf-8",
    )
    (output_dir / "task-3-export-index.json").write_text(
        json.dumps(export_index, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"EXPORT_REVISION={EXPORT_REVISION}",
                f"TASK_2_SIGNATURE={task_2_signature()}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"EXPORT_ID={payload['export_id']}",
                f"EXPORT_SIGNATURE={payload['export_signature']}",
                f"EXPORT_STATUS={payload['export_status']}",
                f"EXPORTED_RECORD_COUNT={payload['exported_record_count']}",
                "IMPLEMENTATION_STARTED=true",
                "IMPLEMENTATION_COMPLETE=true",
                "LOCAL_ONLY=true",
                "NETWORK_ACCESS_ALLOWED=false",
                "SHELL_EXECUTION_ALLOWED=false",
                "REPOSITORY_MUTATION_ALLOWED=false",
                "REMOTE_REGISTRY_LOOKUP_ALLOWED=false",
                "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
                "EXTERNAL_MODEL_CALL_ALLOWED=false",
                f"ALLOWED_OUTPUT_FORMAT_COUNT={len(ALLOWED_OUTPUT_FORMATS)}",
                f"FORBIDDEN_OPERATION_COUNT={len(FORBIDDEN_OPERATIONS)}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"payload": payload, "manifest": manifest, "output_dir": str(output_dir)}


def task_3_status_lines() -> tuple[str, ...]:
    payload = build_export_payload()
    return (
        "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_READY=true",
        f"MILESTONE_28_TASK_3_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_28_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_28_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_28_TASK_3_EXPORT_REVISION={EXPORT_REVISION}",
        f"MILESTONE_28_TASK_3_TASK_2_SIGNATURE={task_2_signature()}",
        f"MILESTONE_28_TASK_3_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_28_TASK_3_EXPORT_ID={payload['export_id']}",
        f"MILESTONE_28_TASK_3_EXPORT_SIGNATURE={payload['export_signature']}",
        f"MILESTONE_28_TASK_3_EXPORT_STATUS={payload['export_status']}",
        f"MILESTONE_28_TASK_3_EXPORTED_RECORD_COUNT={payload['exported_record_count']}",
        "MILESTONE_28_TASK_3_IMPLEMENTATION_STARTED=true",
        "MILESTONE_28_TASK_3_IMPLEMENTATION_COMPLETE=true",
        "MILESTONE_28_TASK_3_LOCAL_ONLY=true",
        "MILESTONE_28_TASK_3_NETWORK_ACCESS_ALLOWED=false",
        "MILESTONE_28_TASK_3_SHELL_EXECUTION_ALLOWED=false",
        "MILESTONE_28_TASK_3_REPOSITORY_MUTATION_ALLOWED=false",
        "MILESTONE_28_TASK_3_REMOTE_REGISTRY_LOOKUP_ALLOWED=false",
        "MILESTONE_28_TASK_3_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
        "MILESTONE_28_TASK_3_EXTERNAL_MODEL_CALL_ALLOWED=false",
        f"MILESTONE_28_TASK_3_ALLOWED_OUTPUT_FORMAT_COUNT={len(ALLOWED_OUTPUT_FORMATS)}",
        f"MILESTONE_28_TASK_3_FORBIDDEN_OPERATION_COUNT={len(FORBIDDEN_OPERATIONS)}",
        f"MILESTONE_28_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_28_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_28_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_28_TASK_3_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    artifacts = write_task_3_artifacts()
    for line in task_3_status_lines():
        print(line)
