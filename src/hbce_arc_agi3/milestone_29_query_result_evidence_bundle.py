from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_28_query_result_export import (
    TASK_ID as EXPORT_TASK_ID,
    validate_export_payload,
)
from hbce_arc_agi3.milestone_28_query_result_export_validation import (
    EXPORT_JSON_PATH,
)
from hbce_arc_agi3.milestone_29_objective_scope_lock import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    FORBIDDEN_OPERATIONS,
    LOCAL_ONLY,
    NETWORK_ACCESS_ALLOWED,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    REMOTE_REGISTRY_LOOKUP_ALLOWED,
    REPOSITORY_MUTATION_ALLOWED,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_REVISION,
    SELECTED_OBJECTIVE_ID,
    SHELL_EXECUTION_ALLOWED,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_objective_scope_lock_report,
    task_2_signature,
    validate_objective_scope_lock_report,
)


TASK_ID = "MILESTONE_29_TASK_3_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
EVIDENCE_BUNDLE_REVISION = "MILESTONE_29_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"

MILESTONE_ID = "MILESTONE_29"
CURRENT_TASK_NUMBER = 3
NEXT_STAGE = "MILESTONE_29_TASK_4_QUERY_RESULT_EVIDENCE_BUNDLE_VALIDATION_V1"

IMPLEMENTATION_STARTED = True
IMPLEMENTATION_COMPLETE = True
IMPLEMENTATION_STATUS = "READY"

DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
EXTERNAL_MODEL_CALL_ALLOWED = False

EVIDENCE_ITEM_COUNT = 6
GENERATED_ARTIFACT_COUNT = 5

TASK_2_SCOPE_LOCK_PATH = Path("examples/milestone-29/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.json")
TASK_2_MANIFEST_PATH = Path("examples/milestone-29/objective-selection-and-scope-lock-v1/task-2-manifest.json")
TASK_2_INDEX_PATH = Path("examples/milestone-29/objective-selection-and-scope-lock-v1/task-2-index.txt")

M28_FINAL_CLOSURE_REPORT_PATH = Path("examples/milestone-28/query-result-export-final-closure-v1/task-6-final-closure-report.json")
M28_REGRESSION_INTEGRATION_REPORT_PATH = Path("examples/milestone-28/query-result-export-regression-integration-v1/task-5-regression-integration-report.json")
M28_VALIDATION_REPORT_PATH = Path("examples/milestone-28/query-result-export-validation-v1/task-4-validation-report.json")
M28_EXPORT_PAYLOAD_PATH = Path(EXPORT_JSON_PATH)


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_3_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
            "task_2_signature": task_2_signature(),
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "implementation_started": IMPLEMENTATION_STARTED,
            "implementation_complete": IMPLEMENTATION_COMPLETE,
            "next_stage": NEXT_STAGE,
        }
    )


def evidence_source_paths() -> tuple[Path, ...]:
    return (
        TASK_2_SCOPE_LOCK_PATH,
        TASK_2_MANIFEST_PATH,
        M28_FINAL_CLOSURE_REPORT_PATH,
        M28_REGRESSION_INTEGRATION_REPORT_PATH,
        M28_VALIDATION_REPORT_PATH,
        M28_EXPORT_PAYLOAD_PATH,
    )


def build_scope_lock_snapshot() -> dict[str, Any]:
    runtime = build_objective_scope_lock_report()
    persisted = _load_json(TASK_2_SCOPE_LOCK_PATH)
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
        "objective_selection_ready": persisted.get("objective_selection_ready"),
        "scope_locked": persisted.get("scope_locked"),
        "implementation_allowed_next": persisted.get("implementation_allowed_next"),
        "local_only": persisted.get("scope_guard", {}).get("local_only"),
        "network_access_allowed": persisted.get("scope_guard", {}).get("network_access_allowed"),
        "shell_execution_allowed": persisted.get("scope_guard", {}).get("shell_execution_allowed"),
        "repository_mutation_allowed": persisted.get("scope_guard", {}).get("repository_mutation_allowed"),
        "remote_registry_lookup_allowed": persisted.get("scope_guard", {}).get("remote_registry_lookup_allowed"),
        "deep_recursive_dependency_traversal_allowed": persisted.get("scope_guard", {}).get("deep_recursive_dependency_traversal_allowed"),
        "external_model_call_allowed": persisted.get("scope_guard", {}).get("external_model_call_allowed"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_scope_lock": (
            runtime.get("scope_lock_artifact_id") == persisted.get("scope_lock_artifact_id")
            and runtime.get("scope_lock_signature") == persisted.get("scope_lock_signature")
            and runtime.get("task_2_signature") == persisted.get("task_2_signature") == task_2_signature()
        ),
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
    if snapshot.get("objective_selection_ready") is not True:
        return False
    if snapshot.get("scope_locked") is not True:
        return False
    if snapshot.get("implementation_allowed_next") is not True:
        return False
    if snapshot.get("local_only") is not True:
        return False
    for key in (
        "network_access_allowed",
        "shell_execution_allowed",
        "repository_mutation_allowed",
        "remote_registry_lookup_allowed",
        "deep_recursive_dependency_traversal_allowed",
        "external_model_call_allowed",
    ):
        if snapshot.get(key) is not False:
            return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_scope_lock"))


def build_evidence_items() -> tuple[dict[str, Any], ...]:
    items = []
    for path in evidence_source_paths():
        if not path.exists():
            raise FileNotFoundError(f"Missing evidence source: {path}")
        text = path.read_text(encoding="utf-8")
        items.append(
            {
                "path": str(path),
                "sha256": _sha256_file(path),
                "byte_count": len(path.read_bytes()),
                "text_char_count": len(text),
                "local_only": True,
            }
        )
    return tuple(items)


def validate_evidence_items(items: Sequence[Mapping[str, Any]]) -> bool:
    if len(items) != EVIDENCE_ITEM_COUNT:
        return False
    seen_paths = set()
    for item in items:
        path = Path(str(item.get("path")))
        if path in seen_paths:
            return False
        seen_paths.add(path)
        if path not in evidence_source_paths():
            return False
        if not path.exists():
            return False
        if item.get("sha256") != _sha256_file(path):
            return False
        if item.get("byte_count") != len(path.read_bytes()):
            return False
        if item.get("text_char_count") != len(path.read_text(encoding="utf-8")):
            return False
        if item.get("local_only") is not True:
            return False
    return True


def build_query_result_evidence_bundle() -> dict[str, Any]:
    scope_snapshot = build_scope_lock_snapshot()
    scope_valid = validate_scope_lock_snapshot(scope_snapshot)
    evidence_items = build_evidence_items()

    export_payload = _load_json(M28_EXPORT_PAYLOAD_PATH)
    export_valid = validate_export_payload(export_payload)

    final_closure = _load_json(M28_FINAL_CLOSURE_REPORT_PATH)
    regression = _load_json(M28_REGRESSION_INTEGRATION_REPORT_PATH)
    validation = _load_json(M28_VALIDATION_REPORT_PATH)

    source_chain = {
        "export_task_id": EXPORT_TASK_ID,
        "export_status": export_payload.get("export_status"),
        "exported_record_count": export_payload.get("exported_record_count"),
        "validation_status": validation.get("validation_status"),
        "validation_pass_count": validation.get("pass_count"),
        "validation_fail_count": validation.get("fail_count"),
        "integration_status": regression.get("integration_status"),
        "integration_pass_count": regression.get("pass_count"),
        "integration_fail_count": regression.get("fail_count"),
        "closure_status": final_closure.get("closure_status"),
        "technical_status": final_closure.get("technical_status"),
        "process_status": final_closure.get("process_status"),
        "source_export_id": validation.get("source_export_id"),
        "source_export_signature": validation.get("source_export_signature"),
        "source_validation_id": regression.get("source_validation_id"),
        "source_validation_signature": regression.get("source_validation_signature"),
        "source_integration_id": final_closure.get("source_integration_id"),
        "source_integration_signature": final_closure.get("source_integration_signature"),
        "source_closure_id": final_closure.get("closure_id"),
        "source_closure_signature": final_closure.get("closure_signature"),
    }

    source_chain_valid = (
        export_valid
        and source_chain["export_status"] == "READY"
        and source_chain["exported_record_count"] == 1
        and source_chain["validation_status"] == "VALID"
        and source_chain["validation_pass_count"] == 6
        and source_chain["validation_fail_count"] == 0
        and source_chain["integration_status"] == "VALID"
        and source_chain["integration_pass_count"] == 7
        and source_chain["integration_fail_count"] == 0
        and source_chain["closure_status"] == "CLOSED"
        and source_chain["technical_status"] == "PASS"
        and source_chain["process_status"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    )

    evidence_valid = validate_evidence_items(evidence_items)

    bundle_core = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "scope_snapshot": scope_snapshot,
        "source_chain": source_chain,
        "evidence_items": list(evidence_items),
    }

    evidence_bundle_id = "MILESTONE-29-QUERY-RESULT-EVIDENCE-BUNDLE-" + _stable_digest(bundle_core)
    evidence_bundle_signature = _stable_digest(
        {
            "evidence_bundle_id": evidence_bundle_id,
            "task_2_signature": task_2_signature(),
            "task_3_signature": task_3_signature(),
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "source_chain": source_chain,
            "evidence_items": list(evidence_items),
        }
    )

    return {
        **bundle_core,
        "evidence_bundle_id": evidence_bundle_id,
        "evidence_bundle_signature": evidence_bundle_signature,
        "implementation_status": IMPLEMENTATION_STATUS if scope_valid and source_chain_valid and evidence_valid else "INVALID",
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_complete": IMPLEMENTATION_COMPLETE if scope_valid and source_chain_valid and evidence_valid else False,
        "scope_lock_valid": scope_valid,
        "source_chain_valid": source_chain_valid,
        "evidence_valid": evidence_valid,
        "evidence_item_count": len(evidence_items),
        "local_only": LOCAL_ONLY,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "repository_mutation_allowed": REPOSITORY_MUTATION_ALLOWED,
        "remote_registry_lookup_allowed": REMOTE_REGISTRY_LOOKUP_ALLOWED,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "external_model_call_allowed": EXTERNAL_MODEL_CALL_ALLOWED,
        "forbidden_operation_count": len(FORBIDDEN_OPERATIONS),
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }


def validate_query_result_evidence_bundle(bundle: Mapping[str, Any]) -> bool:
    if bundle.get("task_id") != TASK_ID:
        return False
    if bundle.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if bundle.get("milestone_id") != MILESTONE_ID:
        return False
    if bundle.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if bundle.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if bundle.get("scope_lock_revision") != SCOPE_LOCK_REVISION:
        return False
    if bundle.get("evidence_bundle_revision") != EVIDENCE_BUNDLE_REVISION:
        return False
    if bundle.get("task_2_signature") != task_2_signature():
        return False
    if bundle.get("task_3_signature") != task_3_signature():
        return False
    if not validate_scope_lock_snapshot(bundle.get("scope_snapshot", {})):
        return False
    if bundle.get("implementation_status") != IMPLEMENTATION_STATUS:
        return False
    if bundle.get("implementation_started") is not True:
        return False
    if bundle.get("implementation_complete") is not True:
        return False
    if bundle.get("scope_lock_valid") is not True:
        return False
    if bundle.get("source_chain_valid") is not True:
        return False
    if bundle.get("evidence_valid") is not True:
        return False
    if bundle.get("evidence_item_count") != EVIDENCE_ITEM_COUNT:
        return False
    if not validate_evidence_items(bundle.get("evidence_items", [])):
        return False
    if bundle.get("local_only") is not True:
        return False
    for key in (
        "network_access_allowed",
        "shell_execution_allowed",
        "repository_mutation_allowed",
        "remote_registry_lookup_allowed",
        "deep_recursive_dependency_traversal_allowed",
        "external_model_call_allowed",
    ):
        if bundle.get(key) is not False:
            return False
    if bundle.get("forbidden_operation_count") != len(FORBIDDEN_OPERATIONS):
        return False
    if bundle.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if bundle.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if bundle.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if bundle.get("next_stage") != NEXT_STAGE:
        return False
    return bool(bundle.get("evidence_bundle_id") and bundle.get("evidence_bundle_signature"))


def render_evidence_bundle_markdown(bundle: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 29 Task 3 Query Result Evidence Bundle",
        "",
        f"TASK_ID={bundle.get('task_id')}",
        f"SOURCE_TASK_ID={bundle.get('source_task_id')}",
        f"SELECTED_OBJECTIVE_ID={bundle.get('selected_objective_id')}",
        f"SCOPE_LOCK_ID={bundle.get('scope_lock_id')}",
        f"EVIDENCE_BUNDLE_ID={bundle.get('evidence_bundle_id')}",
        f"EVIDENCE_BUNDLE_SIGNATURE={bundle.get('evidence_bundle_signature')}",
        f"IMPLEMENTATION_STATUS={bundle.get('implementation_status')}",
        f"IMPLEMENTATION_STARTED={str(bundle.get('implementation_started')).lower()}",
        f"IMPLEMENTATION_COMPLETE={str(bundle.get('implementation_complete')).lower()}",
        f"SCOPE_LOCK_VALID={str(bundle.get('scope_lock_valid')).lower()}",
        f"SOURCE_CHAIN_VALID={str(bundle.get('source_chain_valid')).lower()}",
        f"EVIDENCE_VALID={str(bundle.get('evidence_valid')).lower()}",
        f"EVIDENCE_ITEM_COUNT={bundle.get('evidence_item_count')}",
        f"LOCAL_ONLY={str(bundle.get('local_only')).lower()}",
        f"NEXT_STAGE={bundle.get('next_stage')}",
        "",
        "## Evidence items",
    ]
    for item in bundle.get("evidence_items", []):
        lines.append(f"- {item['path']} sha256={item['sha256']}")
    lines.append("")
    return "\n".join(lines)


def write_task_3_artifacts(base_dir: str | Path = "examples/milestone-29/query-result-evidence-bundle-implementation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle = build_query_result_evidence_bundle()

    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
        "task_2_signature": task_2_signature(),
        "task_3_signature": task_3_signature(),
        "evidence_bundle_id": bundle["evidence_bundle_id"],
        "evidence_bundle_signature": bundle["evidence_bundle_signature"],
        "implementation_status": bundle["implementation_status"],
        "implementation_started": bundle["implementation_started"],
        "implementation_complete": bundle["implementation_complete"],
        "scope_lock_valid": bundle["scope_lock_valid"],
        "source_chain_valid": bundle["source_chain_valid"],
        "evidence_valid": bundle["evidence_valid"],
        "evidence_item_count": bundle["evidence_item_count"],
        "local_only": bundle["local_only"],
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    evidence_index = {
        "task_id": TASK_ID,
        "evidence_bundle_id": bundle["evidence_bundle_id"],
        "evidence_bundle_signature": bundle["evidence_bundle_signature"],
        "evidence_item_count": bundle["evidence_item_count"],
        "evidence_items": bundle["evidence_items"],
    }

    (output_dir / "task-3-evidence-bundle.json").write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-evidence-bundle.md").write_text(
        render_evidence_bundle_markdown(bundle),
        encoding="utf-8",
    )
    (output_dir / "task-3-evidence-index.json").write_text(
        json.dumps(evidence_index, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_29_TASK_3_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"EVIDENCE_BUNDLE_REVISION={EVIDENCE_BUNDLE_REVISION}",
                f"TASK_2_SIGNATURE={task_2_signature()}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"EVIDENCE_BUNDLE_ID={bundle['evidence_bundle_id']}",
                f"EVIDENCE_BUNDLE_SIGNATURE={bundle['evidence_bundle_signature']}",
                f"IMPLEMENTATION_STATUS={bundle['implementation_status']}",
                f"IMPLEMENTATION_STARTED={str(bundle['implementation_started']).lower()}",
                f"IMPLEMENTATION_COMPLETE={str(bundle['implementation_complete']).lower()}",
                f"SCOPE_LOCK_VALID={str(bundle['scope_lock_valid']).lower()}",
                f"SOURCE_CHAIN_VALID={str(bundle['source_chain_valid']).lower()}",
                f"EVIDENCE_VALID={str(bundle['evidence_valid']).lower()}",
                f"EVIDENCE_ITEM_COUNT={bundle['evidence_item_count']}",
                f"LOCAL_ONLY={str(LOCAL_ONLY).lower()}",
                f"NETWORK_ACCESS_ALLOWED={str(NETWORK_ACCESS_ALLOWED).lower()}",
                f"SHELL_EXECUTION_ALLOWED={str(SHELL_EXECUTION_ALLOWED).lower()}",
                f"REPOSITORY_MUTATION_ALLOWED={str(REPOSITORY_MUTATION_ALLOWED).lower()}",
                f"REMOTE_REGISTRY_LOOKUP_ALLOWED={str(REMOTE_REGISTRY_LOOKUP_ALLOWED).lower()}",
                f"DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED={str(DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED).lower()}",
                f"EXTERNAL_MODEL_CALL_ALLOWED={str(EXTERNAL_MODEL_CALL_ALLOWED).lower()}",
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

    return {"bundle": bundle, "manifest": manifest, "output_dir": str(output_dir)}


def task_3_status_lines() -> tuple[str, ...]:
    bundle = build_query_result_evidence_bundle()
    return (
        "MILESTONE_29_TASK_3_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_READY=true",
        f"MILESTONE_29_TASK_3_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_29_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_29_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_29_TASK_3_EVIDENCE_BUNDLE_REVISION={EVIDENCE_BUNDLE_REVISION}",
        f"MILESTONE_29_TASK_3_TASK_2_SIGNATURE={task_2_signature()}",
        f"MILESTONE_29_TASK_3_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_29_TASK_3_EVIDENCE_BUNDLE_ID={bundle['evidence_bundle_id']}",
        f"MILESTONE_29_TASK_3_EVIDENCE_BUNDLE_SIGNATURE={bundle['evidence_bundle_signature']}",
        f"MILESTONE_29_TASK_3_IMPLEMENTATION_STATUS={bundle['implementation_status']}",
        f"MILESTONE_29_TASK_3_IMPLEMENTATION_STARTED={str(bundle['implementation_started']).lower()}",
        f"MILESTONE_29_TASK_3_IMPLEMENTATION_COMPLETE={str(bundle['implementation_complete']).lower()}",
        f"MILESTONE_29_TASK_3_SCOPE_LOCK_VALID={str(bundle['scope_lock_valid']).lower()}",
        f"MILESTONE_29_TASK_3_SOURCE_CHAIN_VALID={str(bundle['source_chain_valid']).lower()}",
        f"MILESTONE_29_TASK_3_EVIDENCE_VALID={str(bundle['evidence_valid']).lower()}",
        f"MILESTONE_29_TASK_3_EVIDENCE_ITEM_COUNT={bundle['evidence_item_count']}",
        f"MILESTONE_29_TASK_3_LOCAL_ONLY={str(LOCAL_ONLY).lower()}",
        f"MILESTONE_29_TASK_3_NETWORK_ACCESS_ALLOWED={str(NETWORK_ACCESS_ALLOWED).lower()}",
        f"MILESTONE_29_TASK_3_SHELL_EXECUTION_ALLOWED={str(SHELL_EXECUTION_ALLOWED).lower()}",
        f"MILESTONE_29_TASK_3_REPOSITORY_MUTATION_ALLOWED={str(REPOSITORY_MUTATION_ALLOWED).lower()}",
        f"MILESTONE_29_TASK_3_REMOTE_REGISTRY_LOOKUP_ALLOWED={str(REMOTE_REGISTRY_LOOKUP_ALLOWED).lower()}",
        f"MILESTONE_29_TASK_3_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED={str(DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED).lower()}",
        f"MILESTONE_29_TASK_3_EXTERNAL_MODEL_CALL_ALLOWED={str(EXTERNAL_MODEL_CALL_ALLOWED).lower()}",
        f"MILESTONE_29_TASK_3_FORBIDDEN_OPERATION_COUNT={len(FORBIDDEN_OPERATIONS)}",
        f"MILESTONE_29_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_29_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_29_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_29_TASK_3_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_3_artifacts()
    for line in task_3_status_lines():
        print(line)
