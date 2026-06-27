from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_27_query_interface_final_closure import (
    FINAL_TASK_NUMBER as SOURCE_FINAL_TASK_NUMBER,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    PROCESS_STATUS as SOURCE_PROCESS_STATUS,
    TASK_BUDGET_MAX as SOURCE_TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    TECHNICAL_STATUS as SOURCE_TECHNICAL_STATUS,
    run_query_interface_final_closure,
    task_6_signature,
    validate_final_closure_report,
)


MILESTONE_ID = "MILESTONE_28"
TASK_ID = "MILESTONE_28_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
SOURCE_MILESTONE_ID = "MILESTONE_27"
SOURCE_FINAL_CLOSURE_TASK_ID = SOURCE_TASK_ID
OPENING_REVISION = "MILESTONE_28_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
TASK_7_USED = False
TASK_8_USED = False

OPENING_STATUS = "OPEN"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8"
IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_1 = False
OBJECTIVE_SELECTION_REQUIRED_NEXT = True
SCOPE_LOCK_REQUIRED_NEXT = True
READY_FOR_OBJECTIVE_SELECTION = True
READY_FOR_SCOPE_LOCK = True

DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
FAST_SOURCE_CLOSURE_SNAPSHOT = True
SOURCE_CLOSURE_REQUIRED = True
SOURCE_CLOSURE_VALID_REQUIRED = True

NEXT_STAGE = "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

_OPENING_SIGNATURE_SEED = {
    "task_id": TASK_ID,
    "source_milestone_id": SOURCE_MILESTONE_ID,
    "source_final_closure_task_id": SOURCE_FINAL_CLOSURE_TASK_ID,
    "opening_revision": OPENING_REVISION,
    "task_budget_max": TASK_BUDGET_MAX,
    "current_task_number": CURRENT_TASK_NUMBER,
    "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
    "next_stage": NEXT_STAGE,
}


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def task_1_signature() -> str:
    return _stable_digest(_OPENING_SIGNATURE_SEED)


def build_source_closure_snapshot() -> dict[str, Any]:
    source = run_query_interface_final_closure()
    source_valid = validate_final_closure_report(source)

    return {
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_task_id": source.get("task_id"),
        "source_closure_id": source.get("closure_id"),
        "source_closure_signature": source.get("closure_signature"),
        "source_task_6_signature": task_6_signature(),
        "source_final_status": source.get("process_status"),
        "source_closure_status": source.get("closure_status"),
        "source_technical_status": source.get("technical_status"),
        "source_process_status": source.get("process_status"),
        "source_task_budget_max": source.get("task_budget_max"),
        "source_final_task_number": source.get("final_task_number"),
        "source_task_7_used": source.get("task_7_used"),
        "source_task_8_used": source.get("task_8_used"),
        "source_milestone_closed": source.get("milestone_closed"),
        "source_ready_for_next_milestone": source.get("ready_for_next_milestone"),
        "source_next_stage": source.get("next_stage"),
        "source_valid": source_valid,
    }


def validate_source_closure_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_milestone_id") != SOURCE_MILESTONE_ID:
        return False
    if snapshot.get("source_task_id") != SOURCE_FINAL_CLOSURE_TASK_ID:
        return False
    if snapshot.get("source_final_status") != SOURCE_PROCESS_STATUS:
        return False
    if snapshot.get("source_closure_status") != "CLOSED":
        return False
    if snapshot.get("source_technical_status") != SOURCE_TECHNICAL_STATUS:
        return False
    if snapshot.get("source_process_status") != SOURCE_PROCESS_STATUS:
        return False
    if snapshot.get("source_task_budget_max") != SOURCE_TASK_BUDGET_MAX:
        return False
    if snapshot.get("source_final_task_number") != SOURCE_FINAL_TASK_NUMBER:
        return False
    if snapshot.get("source_task_7_used") is not False:
        return False
    if snapshot.get("source_task_8_used") is not False:
        return False
    if snapshot.get("source_milestone_closed") is not True:
        return False
    if snapshot.get("source_ready_for_next_milestone") is not True:
        return False
    if snapshot.get("source_next_stage") != "MILESTONE_28_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1":
        return False
    return bool(snapshot.get("source_valid"))


def run_governed_opening() -> dict[str, Any]:
    source_snapshot = build_source_closure_snapshot()
    source_valid = validate_source_closure_snapshot(source_snapshot)

    opening_ready = (
        source_valid
        and TASK_BUDGET_MAX == 8
        and CURRENT_TASK_NUMBER == 1
        and IMPLEMENTATION_STARTED is False
        and IMPLEMENTATION_ALLOWED_AT_TASK_1 is False
        and OBJECTIVE_SELECTION_REQUIRED_NEXT is True
        and SCOPE_LOCK_REQUIRED_NEXT is True
        and READY_FOR_OBJECTIVE_SELECTION is True
        and READY_FOR_SCOPE_LOCK is True
    )

    report = {
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_final_closure_task_id": SOURCE_FINAL_CLOSURE_TASK_ID,
        "opening_revision": OPENING_REVISION,
        "task_1_signature": task_1_signature(),
        "source_task_6_signature": task_6_signature(),
        "opening_status": OPENING_STATUS if opening_ready else "INVALID",
        "technical_status": TECHNICAL_STATUS if opening_ready else "INVALID",
        "process_status": PROCESS_STATUS if opening_ready else "INVALID",
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "task_7_used": TASK_7_USED,
        "task_8_used": TASK_8_USED,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
        "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
        "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
        "ready_for_objective_selection": READY_FOR_OBJECTIVE_SELECTION,
        "ready_for_scope_lock": READY_FOR_SCOPE_LOCK,
        "fast_source_closure_snapshot": FAST_SOURCE_CLOSURE_SNAPSHOT,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "source_closure_required": SOURCE_CLOSURE_REQUIRED,
        "source_closure_valid_required": SOURCE_CLOSURE_VALID_REQUIRED,
        "source_closure_snapshot": source_snapshot,
        "source_closure_valid": source_valid,
        "opening_ready": opening_ready,
        "next_stage": NEXT_STAGE,
    }

    report["opening_id"] = "MILESTONE-28-GOVERNED-OPENING-" + _stable_digest(report)
    report["opening_signature"] = _stable_digest(
        {
            "opening_id": report["opening_id"],
            "source_closure_snapshot": source_snapshot,
            "opening_revision": OPENING_REVISION,
            "task_budget_max": TASK_BUDGET_MAX,
            "next_stage": NEXT_STAGE,
        }
    )
    return report


def validate_governed_opening_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("source_milestone_id") != SOURCE_MILESTONE_ID:
        return False
    if report.get("source_final_closure_task_id") != SOURCE_FINAL_CLOSURE_TASK_ID:
        return False
    if report.get("opening_revision") != OPENING_REVISION:
        return False
    if report.get("opening_status") != OPENING_STATUS:
        return False
    if report.get("technical_status") != TECHNICAL_STATUS:
        return False
    if report.get("process_status") != PROCESS_STATUS:
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("task_7_used") is not False:
        return False
    if report.get("task_8_used") is not False:
        return False
    if report.get("implementation_started") is not False:
        return False
    if report.get("implementation_allowed_at_task_1") is not False:
        return False
    if report.get("objective_selection_required_next") is not True:
        return False
    if report.get("scope_lock_required_next") is not True:
        return False
    if report.get("ready_for_objective_selection") is not True:
        return False
    if report.get("ready_for_scope_lock") is not True:
        return False
    if report.get("deep_recursive_dependency_traversal_allowed") is not False:
        return False
    if report.get("source_closure_valid") is not True:
        return False
    if not validate_source_closure_snapshot(report.get("source_closure_snapshot", {})):
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("opening_ready"))


def render_governed_opening_markdown(report: Mapping[str, Any]) -> str:
    source = report.get("source_closure_snapshot", {})
    lines = [
        "# Milestone 28 Task 1 Governed Opening With Task Budget",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"MILESTONE_ID={report.get('milestone_id')}",
        f"OPENING_STATUS={report.get('opening_status')}",
        f"OPENING_ID={report.get('opening_id')}",
        f"OPENING_SIGNATURE={report.get('opening_signature')}",
        f"TASK_1_SIGNATURE={report.get('task_1_signature')}",
        f"SOURCE_MILESTONE_ID={report.get('source_milestone_id')}",
        f"SOURCE_CLOSURE_ID={source.get('source_closure_id')}",
        f"SOURCE_CLOSURE_SIGNATURE={source.get('source_closure_signature')}",
        f"SOURCE_FINAL_STATUS={source.get('source_final_status')}",
        f"SOURCE_TECHNICAL_STATUS={source.get('source_technical_status')}",
        f"SOURCE_FINAL_TASK_NUMBER={source.get('source_final_task_number')}",
        f"TASK_BUDGET_MAX={report.get('task_budget_max')}",
        f"CURRENT_TASK_NUMBER={report.get('current_task_number')}",
        f"IMPLEMENTATION_STARTED={str(report.get('implementation_started')).lower()}",
        f"IMPLEMENTATION_ALLOWED_AT_TASK_1={str(report.get('implementation_allowed_at_task_1')).lower()}",
        f"OBJECTIVE_SELECTION_REQUIRED_NEXT={str(report.get('objective_selection_required_next')).lower()}",
        f"SCOPE_LOCK_REQUIRED_NEXT={str(report.get('scope_lock_required_next')).lower()}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
    ]
    return "\n".join(lines)


def write_task_1_artifacts(base_dir: str | Path = "examples/milestone-28/governed-opening-with-task-budget-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_governed_opening()
    manifest = {
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_final_closure_task_id": SOURCE_FINAL_CLOSURE_TASK_ID,
        "opening_revision": OPENING_REVISION,
        "task_1_signature": task_1_signature(),
        "source_task_6_signature": task_6_signature(),
        "opening_id": report["opening_id"],
        "opening_signature": report["opening_signature"],
        "opening_status": report["opening_status"],
        "opening_ready": report["opening_ready"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
        "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
        "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
        "generated_artifact_count": 4,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-1-governed-opening.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-governed-opening.md").write_text(
        render_governed_opening_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-1-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_28_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
                f"TASK_ID={TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}",
                f"SOURCE_FINAL_CLOSURE_TASK_ID={SOURCE_FINAL_CLOSURE_TASK_ID}",
                f"OPENING_REVISION={OPENING_REVISION}",
                f"TASK_1_SIGNATURE={task_1_signature()}",
                f"SOURCE_TASK_6_SIGNATURE={task_6_signature()}",
                f"OPENING_ID={report['opening_id']}",
                f"OPENING_SIGNATURE={report['opening_signature']}",
                f"OPENING_STATUS={report['opening_status']}",
                f"TECHNICAL_STATUS={report['technical_status']}",
                f"PROCESS_STATUS={report['process_status']}",
                "SOURCE_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
                "SOURCE_TECHNICAL_STATUS=PASS",
                "SOURCE_FINAL_TASK_NUMBER=6",
                "SOURCE_TASK_7_USED=false",
                "SOURCE_TASK_8_USED=false",
                "SOURCE_MILESTONE_CLOSED=true",
                "SOURCE_READY_FOR_NEXT_MILESTONE=true",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                "IMPLEMENTATION_STARTED=false",
                "IMPLEMENTATION_ALLOWED_AT_TASK_1=false",
                "OBJECTIVE_SELECTION_REQUIRED_NEXT=true",
                "SCOPE_LOCK_REQUIRED_NEXT=true",
                "FAST_SOURCE_CLOSURE_SNAPSHOT=true",
                "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_1_status_lines() -> tuple[str, ...]:
    report = run_governed_opening()
    source = report["source_closure_snapshot"]
    return (
        "MILESTONE_28_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
        f"MILESTONE_28_TASK_1_MILESTONE_ID={MILESTONE_ID}",
        f"MILESTONE_28_TASK_1_SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}",
        f"MILESTONE_28_TASK_1_SOURCE_FINAL_CLOSURE_TASK_ID={SOURCE_FINAL_CLOSURE_TASK_ID}",
        f"MILESTONE_28_TASK_1_OPENING_REVISION={OPENING_REVISION}",
        f"MILESTONE_28_TASK_1_TASK_1_SIGNATURE={task_1_signature()}",
        f"MILESTONE_28_TASK_1_SOURCE_TASK_6_SIGNATURE={task_6_signature()}",
        f"MILESTONE_28_TASK_1_OPENING_ID={report['opening_id']}",
        f"MILESTONE_28_TASK_1_OPENING_SIGNATURE={report['opening_signature']}",
        f"MILESTONE_28_TASK_1_OPENING_STATUS={report['opening_status']}",
        f"MILESTONE_28_TASK_1_TECHNICAL_STATUS={report['technical_status']}",
        f"MILESTONE_28_TASK_1_PROCESS_STATUS={report['process_status']}",
        f"MILESTONE_28_TASK_1_SOURCE_FINAL_STATUS={source['source_final_status']}",
        f"MILESTONE_28_TASK_1_SOURCE_TECHNICAL_STATUS={source['source_technical_status']}",
        f"MILESTONE_28_TASK_1_SOURCE_FINAL_TASK_NUMBER={source['source_final_task_number']}",
        f"MILESTONE_28_TASK_1_SOURCE_TASK_7_USED={str(source['source_task_7_used']).lower()}",
        f"MILESTONE_28_TASK_1_SOURCE_TASK_8_USED={str(source['source_task_8_used']).lower()}",
        f"MILESTONE_28_TASK_1_SOURCE_MILESTONE_CLOSED={str(source['source_milestone_closed']).lower()}",
        f"MILESTONE_28_TASK_1_SOURCE_READY_FOR_NEXT_MILESTONE={str(source['source_ready_for_next_milestone']).lower()}",
        f"MILESTONE_28_TASK_1_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_28_TASK_1_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        "MILESTONE_28_TASK_1_IMPLEMENTATION_STARTED=false",
        "MILESTONE_28_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1=false",
        "MILESTONE_28_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true",
        "MILESTONE_28_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true",
        "MILESTONE_28_TASK_1_FAST_SOURCE_CLOSURE_SNAPSHOT=true",
        "MILESTONE_28_TASK_1_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
        "MILESTONE_28_TASK_1_GENERATED_ARTIFACT_COUNT=4",
        f"MILESTONE_28_TASK_1_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    artifacts = write_task_1_artifacts()
    for line in task_1_status_lines():
        print(line)
