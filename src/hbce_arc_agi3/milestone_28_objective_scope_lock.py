from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_28_governed_opening import (
    MILESTONE_ID,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    OPENING_REVISION,
    PROCESS_STATUS as SOURCE_PROCESS_STATUS,
    TASK_BUDGET_MAX as OPENING_TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    run_governed_opening,
    task_1_signature,
    validate_governed_opening_report,
)


TASK_ID = "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
OBJECTIVE_SELECTION_REVISION = "MILESTONE_28_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

TASK_BUDGET_MAX = OPENING_TASK_BUDGET_MAX
CURRENT_TASK_NUMBER = 2
NEXT_STAGE = "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_V1"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_RESULT_EXPORT_LOCAL_ONLY"
SELECTED_OBJECTIVE_LABEL = "Closed milestone archive index query result export local-only"
SCOPE_LOCK_ID = "MILESTONE_28_SCOPE_CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_RESULT_EXPORT_LOCAL_ONLY"

OBJECTIVE_SELECTION_READY = True
SCOPE_LOCKED = True
IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_NEXT = True
IMPLEMENTATION_ALLOWED_AT_TASK_2 = False

LOCAL_ONLY = True
NETWORK_ACCESS_ALLOWED = False
SHELL_EXECUTION_ALLOWED = False
REPOSITORY_MUTATION_ALLOWED = False
REMOTE_REGISTRY_LOOKUP_ALLOWED = False
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
EXTERNAL_MODEL_CALL_ALLOWED = False

ALLOWED_INPUT_ARTIFACTS = (
    "examples/milestone-27/query-interface-implementation-v1/task-3-query-interface-result.json",
    "examples/milestone-27/query-interface-implementation-v1/task-3-query-interface-blocked-result.json",
    "examples/milestone-27/query-interface-validation-v1/task-4-validation-report.json",
    "examples/milestone-27/query-interface-regression-integration-v1/task-5-regression-integration-report.json",
    "examples/milestone-27/query-interface-final-closure-v1/task-6-final-closure-report.json",
    "examples/milestone-28/governed-opening-with-task-budget-v1/task-1-governed-opening.json",
)

FORBIDDEN_OPERATIONS = (
    "NETWORK_ACCESS",
    "SHELL_EXECUTION",
    "REPOSITORY_MUTATION_DURING_RUNTIME_QUERY",
    "REMOTE_REGISTRY_LOOKUP",
    "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL",
    "EXTERNAL_MODEL_CALL",
    "UNBOUNDED_FILE_SYSTEM_SCAN",
    "TASK_BUDGET_EXTENSION",
)

ALLOWED_OUTPUT_FORMATS = (
    "JSON_EXPORT",
    "MARKDOWN_EXPORT",
    "TEXT_INDEX",
    "MANIFEST",
)


@dataclass(frozen=True)
class ObjectiveCandidate:
    objective_id: str
    label: str
    selected: bool
    local_only: bool
    implementation_allowed_next: bool
    reason: str


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def task_2_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "objective_selection_revision": OBJECTIVE_SELECTION_REVISION,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "next_stage": NEXT_STAGE,
        }
    )


def build_source_opening_snapshot() -> dict[str, Any]:
    source = run_governed_opening()
    source_valid = validate_governed_opening_report(source)

    return {
        "source_task_id": source.get("task_id"),
        "source_milestone_id": source.get("milestone_id"),
        "source_opening_id": source.get("opening_id"),
        "source_opening_signature": source.get("opening_signature"),
        "source_task_1_signature": task_1_signature(),
        "source_opening_revision": source.get("opening_revision"),
        "source_opening_status": source.get("opening_status"),
        "source_technical_status": source.get("technical_status"),
        "source_process_status": source.get("process_status"),
        "source_task_budget_max": source.get("task_budget_max"),
        "source_current_task_number": source.get("current_task_number"),
        "source_implementation_started": source.get("implementation_started"),
        "source_implementation_allowed_at_task_1": source.get("implementation_allowed_at_task_1"),
        "source_objective_selection_required_next": source.get("objective_selection_required_next"),
        "source_scope_lock_required_next": source.get("scope_lock_required_next"),
        "source_next_stage": source.get("next_stage"),
        "source_valid": source_valid,
    }


def validate_source_opening_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_milestone_id") != MILESTONE_ID:
        return False
    if snapshot.get("source_opening_revision") != OPENING_REVISION:
        return False
    if snapshot.get("source_opening_status") != "OPEN":
        return False
    if snapshot.get("source_technical_status") != "PASS":
        return False
    if snapshot.get("source_process_status") != SOURCE_PROCESS_STATUS:
        return False
    if snapshot.get("source_task_budget_max") != TASK_BUDGET_MAX:
        return False
    if snapshot.get("source_current_task_number") != 1:
        return False
    if snapshot.get("source_implementation_started") is not False:
        return False
    if snapshot.get("source_implementation_allowed_at_task_1") is not False:
        return False
    if snapshot.get("source_objective_selection_required_next") is not True:
        return False
    if snapshot.get("source_scope_lock_required_next") is not True:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    return bool(snapshot.get("source_valid"))


def build_objective_candidates() -> tuple[ObjectiveCandidate, ...]:
    return (
        ObjectiveCandidate(
            objective_id=SELECTED_OBJECTIVE_ID,
            label=SELECTED_OBJECTIVE_LABEL,
            selected=True,
            local_only=True,
            implementation_allowed_next=True,
            reason="Selected because it extends the Milestone 27 query interface into deterministic local export artifacts without widening runtime authority.",
        ),
        ObjectiveCandidate(
            objective_id="REMOTE_ARCHIVE_QUERY_RESULT_EXPORT_REJECTED",
            label="Remote archive query result export",
            selected=False,
            local_only=False,
            implementation_allowed_next=False,
            reason="Rejected because remote lookup is outside the governed local-only scope.",
        ),
        ObjectiveCandidate(
            objective_id="DEEP_ARCHIVE_DEPENDENCY_EXPORT_REJECTED",
            label="Deep archive dependency export",
            selected=False,
            local_only=False,
            implementation_allowed_next=False,
            reason="Rejected because deep recursive dependency traversal is explicitly forbidden.",
        ),
    )


def selected_objective() -> dict[str, Any]:
    selected = [candidate for candidate in build_objective_candidates() if candidate.selected]
    if len(selected) != 1:
        raise ValueError("Milestone 28 Task 2 requires exactly one selected objective.")
    return asdict(selected[0])


def run_objective_scope_lock() -> dict[str, Any]:
    source_snapshot = build_source_opening_snapshot()
    source_valid = validate_source_opening_snapshot(source_snapshot)
    objective = selected_objective()
    candidates = [asdict(candidate) for candidate in build_objective_candidates()]

    scope_ready = (
        source_valid
        and objective["objective_id"] == SELECTED_OBJECTIVE_ID
        and objective["local_only"] is True
        and objective["implementation_allowed_next"] is True
        and OBJECTIVE_SELECTION_READY is True
        and SCOPE_LOCKED is True
        and IMPLEMENTATION_STARTED is False
        and IMPLEMENTATION_ALLOWED_NEXT is True
        and IMPLEMENTATION_ALLOWED_AT_TASK_2 is False
        and LOCAL_ONLY is True
        and NETWORK_ACCESS_ALLOWED is False
        and SHELL_EXECUTION_ALLOWED is False
        and REMOTE_REGISTRY_LOOKUP_ALLOWED is False
        and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED is False
        and EXTERNAL_MODEL_CALL_ALLOWED is False
    )

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "objective_selection_revision": OBJECTIVE_SELECTION_REVISION,
        "task_1_signature": task_1_signature(),
        "task_2_signature": task_2_signature(),
        "source_opening_snapshot": source_snapshot,
        "source_opening_valid": source_valid,
        "candidate_count": len(candidates),
        "objective_candidates": candidates,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "selected_objective_label": SELECTED_OBJECTIVE_LABEL,
        "selected_objective": objective,
        "scope_lock_id": SCOPE_LOCK_ID,
        "objective_selection_ready": OBJECTIVE_SELECTION_READY,
        "scope_locked": SCOPE_LOCKED,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_next": IMPLEMENTATION_ALLOWED_NEXT,
        "implementation_allowed_at_task_2": IMPLEMENTATION_ALLOWED_AT_TASK_2,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "local_only": LOCAL_ONLY,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "repository_mutation_allowed": REPOSITORY_MUTATION_ALLOWED,
        "remote_registry_lookup_allowed": REMOTE_REGISTRY_LOOKUP_ALLOWED,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "external_model_call_allowed": EXTERNAL_MODEL_CALL_ALLOWED,
        "allowed_input_artifacts": list(ALLOWED_INPUT_ARTIFACTS),
        "allowed_output_formats": list(ALLOWED_OUTPUT_FORMATS),
        "forbidden_operations": list(FORBIDDEN_OPERATIONS),
        "scope_ready": scope_ready,
        "next_stage": NEXT_STAGE,
    }

    report["scope_lock_signature"] = _stable_digest(
        {
            "task_id": TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "source_opening_id": source_snapshot.get("source_opening_id"),
            "forbidden_operations": FORBIDDEN_OPERATIONS,
            "next_stage": NEXT_STAGE,
        }
    )
    report["scope_lock_artifact_id"] = "MILESTONE-28-SCOPE-LOCK-" + _stable_digest(report)
    return report


def validate_objective_scope_lock_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("objective_selection_revision") != OBJECTIVE_SELECTION_REVISION:
        return False
    if report.get("source_opening_valid") is not True:
        return False
    if not validate_source_opening_snapshot(report.get("source_opening_snapshot", {})):
        return False
    if report.get("candidate_count") != 3:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("objective_selection_ready") is not True:
        return False
    if report.get("scope_locked") is not True:
        return False
    if report.get("implementation_started") is not False:
        return False
    if report.get("implementation_allowed_next") is not True:
        return False
    if report.get("implementation_allowed_at_task_2") is not False:
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("local_only") is not True:
        return False
    if report.get("network_access_allowed") is not False:
        return False
    if report.get("shell_execution_allowed") is not False:
        return False
    if report.get("remote_registry_lookup_allowed") is not False:
        return False
    if report.get("deep_recursive_dependency_traversal_allowed") is not False:
        return False
    if report.get("external_model_call_allowed") is not False:
        return False
    if tuple(report.get("forbidden_operations", ())) != FORBIDDEN_OPERATIONS:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("scope_ready"))


def render_scope_lock_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 28 Task 2 Objective Selection and Scope Lock",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"MILESTONE_ID={report.get('milestone_id')}",
        f"OBJECTIVE_SELECTION_REVISION={report.get('objective_selection_revision')}",
        f"SELECTED_OBJECTIVE_ID={report.get('selected_objective_id')}",
        f"SCOPE_LOCK_ID={report.get('scope_lock_id')}",
        f"SCOPE_LOCK_ARTIFACT_ID={report.get('scope_lock_artifact_id')}",
        f"SCOPE_LOCK_SIGNATURE={report.get('scope_lock_signature')}",
        f"TASK_2_SIGNATURE={report.get('task_2_signature')}",
        f"OBJECTIVE_SELECTION_READY={str(report.get('objective_selection_ready')).lower()}",
        f"SCOPE_LOCKED={str(report.get('scope_locked')).lower()}",
        f"IMPLEMENTATION_STARTED={str(report.get('implementation_started')).lower()}",
        f"IMPLEMENTATION_ALLOWED_NEXT={str(report.get('implementation_allowed_next')).lower()}",
        f"IMPLEMENTATION_ALLOWED_AT_TASK_2={str(report.get('implementation_allowed_at_task_2')).lower()}",
        f"LOCAL_ONLY={str(report.get('local_only')).lower()}",
        f"NETWORK_ACCESS_ALLOWED={str(report.get('network_access_allowed')).lower()}",
        f"DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED={str(report.get('deep_recursive_dependency_traversal_allowed')).lower()}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Candidates",
    ]
    for candidate in report.get("objective_candidates", []):
        lines.append(f"- {candidate['objective_id']} selected={str(candidate['selected']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_2_artifacts(base_dir: str | Path = "examples/milestone-28/objective-selection-and-scope-lock-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_objective_scope_lock()
    candidates = {
        "task_id": TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "candidate_count": report["candidate_count"],
        "objective_candidates": report["objective_candidates"],
    }
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "objective_selection_revision": OBJECTIVE_SELECTION_REVISION,
        "task_1_signature": task_1_signature(),
        "task_2_signature": task_2_signature(),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_artifact_id": report["scope_lock_artifact_id"],
        "scope_lock_signature": report["scope_lock_signature"],
        "scope_ready": report["scope_ready"],
        "implementation_allowed_next": IMPLEMENTATION_ALLOWED_NEXT,
        "implementation_started": IMPLEMENTATION_STARTED,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": 5,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-2-objective-scope-lock.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-2-objective-scope-lock.md").write_text(
        render_scope_lock_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-2-objective-candidates.json").write_text(
        json.dumps(candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-2-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-2-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"OBJECTIVE_SELECTION_REVISION={OBJECTIVE_SELECTION_REVISION}",
                f"TASK_1_SIGNATURE={task_1_signature()}",
                f"TASK_2_SIGNATURE={task_2_signature()}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SELECTED_OBJECTIVE_LABEL={SELECTED_OBJECTIVE_LABEL}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"SCOPE_LOCK_ARTIFACT_ID={report['scope_lock_artifact_id']}",
                f"SCOPE_LOCK_SIGNATURE={report['scope_lock_signature']}",
                "OBJECTIVE_SELECTION_READY=true",
                "SCOPE_LOCKED=true",
                "IMPLEMENTATION_STARTED=false",
                "IMPLEMENTATION_ALLOWED_NEXT=true",
                "IMPLEMENTATION_ALLOWED_AT_TASK_2=false",
                "LOCAL_ONLY=true",
                "NETWORK_ACCESS_ALLOWED=false",
                "SHELL_EXECUTION_ALLOWED=false",
                "REPOSITORY_MUTATION_ALLOWED=false",
                "REMOTE_REGISTRY_LOOKUP_ALLOWED=false",
                "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
                "EXTERNAL_MODEL_CALL_ALLOWED=false",
                f"ALLOWED_INPUT_ARTIFACT_COUNT={len(ALLOWED_INPUT_ARTIFACTS)}",
                f"FORBIDDEN_OPERATION_COUNT={len(FORBIDDEN_OPERATIONS)}",
                f"ALLOWED_OUTPUT_FORMAT_COUNT={len(ALLOWED_OUTPUT_FORMATS)}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_2_status_lines() -> tuple[str, ...]:
    report = run_objective_scope_lock()
    return (
        "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true",
        f"MILESTONE_28_TASK_2_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_28_TASK_2_MILESTONE_ID={MILESTONE_ID}",
        f"MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_REVISION={OBJECTIVE_SELECTION_REVISION}",
        f"MILESTONE_28_TASK_2_TASK_1_SIGNATURE={task_1_signature()}",
        f"MILESTONE_28_TASK_2_TASK_2_SIGNATURE={task_2_signature()}",
        f"MILESTONE_28_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_28_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_28_TASK_2_SCOPE_LOCK_ARTIFACT_ID={report['scope_lock_artifact_id']}",
        f"MILESTONE_28_TASK_2_SCOPE_LOCK_SIGNATURE={report['scope_lock_signature']}",
        "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_READY=true",
        "MILESTONE_28_TASK_2_SCOPE_LOCKED=true",
        "MILESTONE_28_TASK_2_IMPLEMENTATION_STARTED=false",
        "MILESTONE_28_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true",
        "MILESTONE_28_TASK_2_IMPLEMENTATION_ALLOWED_AT_TASK_2=false",
        "MILESTONE_28_TASK_2_LOCAL_ONLY=true",
        "MILESTONE_28_TASK_2_NETWORK_ACCESS_ALLOWED=false",
        "MILESTONE_28_TASK_2_SHELL_EXECUTION_ALLOWED=false",
        "MILESTONE_28_TASK_2_REMOTE_REGISTRY_LOOKUP_ALLOWED=false",
        "MILESTONE_28_TASK_2_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
        "MILESTONE_28_TASK_2_EXTERNAL_MODEL_CALL_ALLOWED=false",
        f"MILESTONE_28_TASK_2_ALLOWED_INPUT_ARTIFACT_COUNT={len(ALLOWED_INPUT_ARTIFACTS)}",
        f"MILESTONE_28_TASK_2_FORBIDDEN_OPERATION_COUNT={len(FORBIDDEN_OPERATIONS)}",
        f"MILESTONE_28_TASK_2_ALLOWED_OUTPUT_FORMAT_COUNT={len(ALLOWED_OUTPUT_FORMATS)}",
        "MILESTONE_28_TASK_2_GENERATED_ARTIFACT_COUNT=5",
        f"MILESTONE_28_TASK_2_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_28_TASK_2_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_28_TASK_2_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    artifacts = write_task_2_artifacts()
    for line in task_2_status_lines():
        print(line)
