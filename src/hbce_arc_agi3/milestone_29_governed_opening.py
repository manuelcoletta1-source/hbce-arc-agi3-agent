from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_28_query_result_export_final_closure import (
    CLOSURE_STATUS as SOURCE_CLOSURE_STATUS,
    FINAL_TASK_NUMBER as SOURCE_FINAL_TASK_NUMBER,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    PROCESS_STATUS as SOURCE_PROCESS_STATUS,
    TASK_BUDGET_MAX as SOURCE_TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    TECHNICAL_STATUS as SOURCE_TECHNICAL_STATUS,
    TASK_7_USED as SOURCE_TASK_7_USED,
    TASK_8_USED as SOURCE_TASK_8_USED,
    run_query_result_export_final_closure,
    task_6_signature,
    validate_final_closure_report,
)


TASK_ID = "MILESTONE_29_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
MILESTONE_ID = "MILESTONE_29"
SOURCE_MILESTONE_ID = "MILESTONE_28"
OPENING_REVISION = "MILESTONE_29_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

OPENING_STATUS = "OPEN"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
GENERATED_ARTIFACT_COUNT = 5

IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_1 = False
OBJECTIVE_SELECTION_REQUIRED_NEXT = True
SCOPE_LOCK_REQUIRED_NEXT = True
NEXT_STAGE = "MILESTONE_29_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def task_1_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "milestone_id": MILESTONE_ID,
            "source_task_id": SOURCE_TASK_ID,
            "source_task_6_signature": task_6_signature(),
            "opening_revision": OPENING_REVISION,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "implementation_started": IMPLEMENTATION_STARTED,
            "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
            "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
            "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
            "next_stage": NEXT_STAGE,
        }
    )


def build_source_closure_snapshot() -> dict[str, Any]:
    source = run_query_result_export_final_closure()
    source_valid = validate_final_closure_report(source)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_task_6_signature": task_6_signature(),
        "source_closure_id": source.get("closure_id"),
        "source_closure_signature": source.get("closure_signature"),
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
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_milestone_id") != SOURCE_MILESTONE_ID:
        return False
    if snapshot.get("source_task_6_signature") != task_6_signature():
        return False
    if snapshot.get("source_closure_status") != SOURCE_CLOSURE_STATUS:
        return False
    if snapshot.get("source_technical_status") != SOURCE_TECHNICAL_STATUS:
        return False
    if snapshot.get("source_process_status") != SOURCE_PROCESS_STATUS:
        return False
    if snapshot.get("source_task_budget_max") != SOURCE_TASK_BUDGET_MAX:
        return False
    if snapshot.get("source_final_task_number") != SOURCE_FINAL_TASK_NUMBER:
        return False
    if snapshot.get("source_task_7_used") is not SOURCE_TASK_7_USED:
        return False
    if snapshot.get("source_task_8_used") is not SOURCE_TASK_8_USED:
        return False
    if snapshot.get("source_milestone_closed") is not True:
        return False
    if snapshot.get("source_ready_for_next_milestone") is not True:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    return bool(snapshot.get("source_valid"))


def build_governed_opening_report() -> dict[str, Any]:
    source_snapshot = build_source_closure_snapshot()
    source_valid = validate_source_closure_snapshot(source_snapshot)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "opening_revision": OPENING_REVISION,
        "source_task_6_signature": task_6_signature(),
        "task_1_signature": task_1_signature(),
        "source_closure_snapshot": source_snapshot,
        "opening_status": OPENING_STATUS if source_valid else "BLOCKED",
        "technical_status": TECHNICAL_STATUS if source_valid else "FAIL",
        "process_status": PROCESS_STATUS if source_valid else "BLOCKED",
        "source_dependency_valid": source_valid,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
        "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
        "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    report["opening_id"] = "MILESTONE-29-GOVERNED-OPENING-" + _stable_digest(report)
    report["opening_signature"] = _stable_digest(
        {
            "opening_id": report["opening_id"],
            "source_task_6_signature": report["source_task_6_signature"],
            "source_closure_id": source_snapshot.get("source_closure_id"),
            "task_1_signature": report["task_1_signature"],
            "opening_revision": OPENING_REVISION,
            "task_budget_max": TASK_BUDGET_MAX,
            "next_stage": NEXT_STAGE,
        }
    )
    return report


def validate_governed_opening_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("source_milestone_id") != SOURCE_MILESTONE_ID:
        return False
    if report.get("opening_revision") != OPENING_REVISION:
        return False
    if report.get("source_task_6_signature") != task_6_signature():
        return False
    if report.get("task_1_signature") != task_1_signature():
        return False
    if not validate_source_closure_snapshot(report.get("source_closure_snapshot", {})):
        return False
    if report.get("opening_status") != OPENING_STATUS:
        return False
    if report.get("technical_status") != TECHNICAL_STATUS:
        return False
    if report.get("process_status") != PROCESS_STATUS:
        return False
    if report.get("source_dependency_valid") is not True:
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("implementation_started") is not False:
        return False
    if report.get("implementation_allowed_at_task_1") is not False:
        return False
    if report.get("objective_selection_required_next") is not True:
        return False
    if report.get("scope_lock_required_next") is not True:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("opening_id") and report.get("opening_signature"))


def render_governed_opening_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 29 Task 1 Governed Opening With Task Budget",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"MILESTONE_ID={report.get('milestone_id')}",
        f"OPENING_STATUS={report.get('opening_status')}",
        f"TECHNICAL_STATUS={report.get('technical_status')}",
        f"PROCESS_STATUS={report.get('process_status')}",
        f"OPENING_ID={report.get('opening_id')}",
        f"OPENING_SIGNATURE={report.get('opening_signature')}",
        f"SOURCE_TASK_6_SIGNATURE={report.get('source_task_6_signature')}",
        f"TASK_1_SIGNATURE={report.get('task_1_signature')}",
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


def write_task_1_artifacts(base_dir: str | Path = "examples/milestone-29/governed-opening-with-task-budget-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_governed_opening_report()
    snapshot = report["source_closure_snapshot"]

    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "opening_revision": OPENING_REVISION,
        "source_task_6_signature": task_6_signature(),
        "task_1_signature": task_1_signature(),
        "opening_id": report["opening_id"],
        "opening_signature": report["opening_signature"],
        "opening_status": report["opening_status"],
        "technical_status": report["technical_status"],
        "process_status": report["process_status"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
        "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
        "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
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
    (output_dir / "task-1-source-closure-snapshot.json").write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_29_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}",
                f"OPENING_REVISION={OPENING_REVISION}",
                f"SOURCE_TASK_6_SIGNATURE={task_6_signature()}",
                f"TASK_1_SIGNATURE={task_1_signature()}",
                f"OPENING_ID={report['opening_id']}",
                f"OPENING_SIGNATURE={report['opening_signature']}",
                f"OPENING_STATUS={report['opening_status']}",
                f"TECHNICAL_STATUS={report['technical_status']}",
                f"PROCESS_STATUS={report['process_status']}",
                f"SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
                f"IMPLEMENTATION_ALLOWED_AT_TASK_1={str(IMPLEMENTATION_ALLOWED_AT_TASK_1).lower()}",
                f"OBJECTIVE_SELECTION_REQUIRED_NEXT={str(OBJECTIVE_SELECTION_REQUIRED_NEXT).lower()}",
                f"SCOPE_LOCK_REQUIRED_NEXT={str(SCOPE_LOCK_REQUIRED_NEXT).lower()}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_1_status_lines() -> tuple[str, ...]:
    report = build_governed_opening_report()
    return (
        "MILESTONE_29_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
        f"MILESTONE_29_TASK_1_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_29_TASK_1_SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}",
        f"MILESTONE_29_TASK_1_MILESTONE_ID={MILESTONE_ID}",
        f"MILESTONE_29_TASK_1_OPENING_REVISION={OPENING_REVISION}",
        f"MILESTONE_29_TASK_1_SOURCE_TASK_6_SIGNATURE={task_6_signature()}",
        f"MILESTONE_29_TASK_1_TASK_1_SIGNATURE={task_1_signature()}",
        f"MILESTONE_29_TASK_1_OPENING_ID={report['opening_id']}",
        f"MILESTONE_29_TASK_1_OPENING_SIGNATURE={report['opening_signature']}",
        f"MILESTONE_29_TASK_1_OPENING_STATUS={report['opening_status']}",
        f"MILESTONE_29_TASK_1_TECHNICAL_STATUS={report['technical_status']}",
        f"MILESTONE_29_TASK_1_PROCESS_STATUS={report['process_status']}",
        f"MILESTONE_29_TASK_1_SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
        f"MILESTONE_29_TASK_1_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_29_TASK_1_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_29_TASK_1_IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
        f"MILESTONE_29_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1={str(IMPLEMENTATION_ALLOWED_AT_TASK_1).lower()}",
        f"MILESTONE_29_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT={str(OBJECTIVE_SELECTION_REQUIRED_NEXT).lower()}",
        f"MILESTONE_29_TASK_1_SCOPE_LOCK_REQUIRED_NEXT={str(SCOPE_LOCK_REQUIRED_NEXT).lower()}",
        f"MILESTONE_29_TASK_1_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_29_TASK_1_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_1_artifacts()
    for line in task_1_status_lines():
        print(line)
