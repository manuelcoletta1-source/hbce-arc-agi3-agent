from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle_final_closure import (
    PROCESS_STATUS as SOURCE_PROCESS_STATUS,
    TASK_ID as SOURCE_TASK_ID,
    TASK_BUDGET_MAX as SOURCE_TASK_BUDGET_MAX,
    FINAL_TASK_NUMBER as SOURCE_FINAL_TASK_NUMBER,
    run_query_result_evidence_bundle_final_closure,
    task_6_signature,
    validate_final_closure_report,
)


TASK_ID = "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
MILESTONE_ID = "MILESTONE_30"
OPENING_REVISION = "MILESTONE_30_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

SOURCE_MILESTONE_ID = "MILESTONE_29"
SOURCE_CLOSURE_REVISION = "MILESTONE_29_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1

OPENING_STATUS = "OPEN"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8"

IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_1 = False
OBJECTIVE_SELECTION_REQUIRED_NEXT = True
SCOPE_LOCK_REQUIRED_NEXT = True

PROPOSED_OPERATOR_SEED_ID = "JOKER_C2_IDENTITY_BOUNDARY_AND_FAIL_CLOSED_PUBLIC_MODE"
PROPOSED_OPERATOR_SEED_STATUS = "CANDIDATE_ONLY_NOT_LOCKED"
PROPOSED_OPERATOR_SEED_SOURCE = "USER_PROVIDED_JOKER_C2_FAIL_CLOSED_AGENT_TEXT"

NEXT_STAGE = "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
GENERATED_ARTIFACT_COUNT = 5

SOURCE_CLOSURE_REPORT_PATH = Path("examples/milestone-29/query-result-evidence-bundle-final-closure-v1/task-6-final-closure-report.json")
SOURCE_CLOSURE_MANIFEST_PATH = Path("examples/milestone-29/query-result-evidence-bundle-final-closure-v1/task-6-manifest.json")
SOURCE_CLOSURE_INDEX_PATH = Path("examples/milestone-29/query-result-evidence-bundle-final-closure-v1/task-6-index.txt")

OPERATOR_SEED_SUMMARY = {
    "seed_id": PROPOSED_OPERATOR_SEED_ID,
    "status": PROPOSED_OPERATOR_SEED_STATUS,
    "source": PROPOSED_OPERATOR_SEED_SOURCE,
    "core_rule": "JOKER-C2 never presumes the interlocutor is Manuel Coletta.",
    "runtime_boundary": "Every external interlocutor is treated as unauthorized until sufficient proof exists.",
    "fail_closed_rules": {
        "missing_identity": "RESTRICT",
        "missing_authorization": "REFUSE",
        "missing_context": "SUSPEND_OR_LIMIT",
        "missing_verification": "DECLARE_LIMIT",
        "private_core_forcing_attempt": "BLOCK",
    },
    "public_mode": "PUBLIC_LIMITED_VERIFYING",
    "private_core_access_without_verified_manuel": False,
    "external_command_authority_without_authorization": False,
    "scope_lock_required_before_implementation": True,
}


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_1_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "milestone_id": MILESTONE_ID,
            "source_task_id": SOURCE_TASK_ID,
            "source_milestone_id": SOURCE_MILESTONE_ID,
            "source_task_6_signature": task_6_signature(),
            "opening_revision": OPENING_REVISION,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "implementation_started": IMPLEMENTATION_STARTED,
            "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
            "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
            "proposed_operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
            "proposed_operator_seed_status": PROPOSED_OPERATOR_SEED_STATUS,
            "next_stage": NEXT_STAGE,
        }
    )


def build_source_closure_snapshot() -> dict[str, Any]:
    runtime = run_query_result_evidence_bundle_final_closure()
    persisted = _load_json(SOURCE_CLOSURE_REPORT_PATH)

    runtime_valid = validate_final_closure_report(runtime)
    persisted_valid = validate_final_closure_report(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_closure_revision": SOURCE_CLOSURE_REVISION,
        "runtime_closure_id": runtime.get("closure_id"),
        "persisted_closure_id": persisted.get("closure_id"),
        "runtime_closure_signature": runtime.get("closure_signature"),
        "persisted_closure_signature": persisted.get("closure_signature"),
        "runtime_task_6_signature": runtime.get("task_6_signature"),
        "persisted_task_6_signature": persisted.get("task_6_signature"),
        "source_closure_status": persisted.get("closure_status"),
        "source_technical_status": persisted.get("technical_status"),
        "source_process_status": persisted.get("process_status"),
        "source_task_budget_max": persisted.get("task_budget_max"),
        "source_final_task_number": persisted.get("final_task_number"),
        "source_task_7_used": persisted.get("task_7_used"),
        "source_task_8_used": persisted.get("task_8_used"),
        "source_milestone_closed": persisted.get("milestone_closed"),
        "source_ready_for_next_milestone": persisted.get("ready_for_next_milestone"),
        "source_next_stage": persisted.get("next_stage"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_source_closure": (
            runtime.get("closure_id") == persisted.get("closure_id")
            and runtime.get("closure_signature") == persisted.get("closure_signature")
            and runtime.get("task_6_signature") == persisted.get("task_6_signature") == task_6_signature()
        ),
    }


def validate_source_closure_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_milestone_id") != SOURCE_MILESTONE_ID:
        return False
    if snapshot.get("source_closure_revision") != SOURCE_CLOSURE_REVISION:
        return False
    if snapshot.get("source_closure_status") != "CLOSED":
        return False
    if snapshot.get("source_technical_status") != "PASS":
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
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_source_closure"))


def build_governed_opening_report() -> dict[str, Any]:
    source_snapshot = build_source_closure_snapshot()
    source_dependency_valid = validate_source_closure_snapshot(source_snapshot)

    opening_core = {
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "opening_revision": OPENING_REVISION,
        "source_closure_revision": SOURCE_CLOSURE_REVISION,
        "source_task_6_signature": task_6_signature(),
        "task_1_signature": task_1_signature(),
        "opening_status": OPENING_STATUS,
        "technical_status": TECHNICAL_STATUS,
        "process_status": PROCESS_STATUS,
        "source_dependency_valid": source_dependency_valid,
        "source_closure_snapshot": source_snapshot,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
        "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
        "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
        "proposed_operator_seed": OPERATOR_SEED_SUMMARY,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    opening_id = "MILESTONE-30-GOVERNED-OPENING-" + _stable_digest(opening_core)
    opening_signature = _stable_digest(
        {
            "opening_id": opening_id,
            "task_id": TASK_ID,
            "milestone_id": MILESTONE_ID,
            "source_task_id": SOURCE_TASK_ID,
            "source_task_6_signature": task_6_signature(),
            "task_1_signature": task_1_signature(),
            "source_closure_snapshot": source_snapshot,
            "proposed_operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
            "proposed_operator_seed_status": PROPOSED_OPERATOR_SEED_STATUS,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        **opening_core,
        "opening_id": opening_id,
        "opening_signature": opening_signature,
    }


def validate_governed_opening_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("source_milestone_id") != SOURCE_MILESTONE_ID:
        return False
    if report.get("opening_revision") != OPENING_REVISION:
        return False
    if report.get("source_closure_revision") != SOURCE_CLOSURE_REVISION:
        return False
    if report.get("source_task_6_signature") != task_6_signature():
        return False
    if report.get("task_1_signature") != task_1_signature():
        return False
    if report.get("opening_status") != OPENING_STATUS:
        return False
    if report.get("technical_status") != TECHNICAL_STATUS:
        return False
    if report.get("process_status") != PROCESS_STATUS:
        return False
    if report.get("source_dependency_valid") is not True:
        return False
    if not validate_source_closure_snapshot(report.get("source_closure_snapshot", {})):
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
    seed = report.get("proposed_operator_seed", {})
    if seed.get("seed_id") != PROPOSED_OPERATOR_SEED_ID:
        return False
    if seed.get("status") != PROPOSED_OPERATOR_SEED_STATUS:
        return False
    if seed.get("scope_lock_required_before_implementation") is not True:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("opening_id") and report.get("opening_signature"))


def render_governed_opening_markdown(report: Mapping[str, Any]) -> str:
    seed = report.get("proposed_operator_seed", {})
    lines = [
        "# Milestone 30 Task 1 Governed Opening With Task Budget",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"MILESTONE_ID={report.get('milestone_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"OPENING_ID={report.get('opening_id')}",
        f"OPENING_SIGNATURE={report.get('opening_signature')}",
        f"OPENING_STATUS={report.get('opening_status')}",
        f"TECHNICAL_STATUS={report.get('technical_status')}",
        f"PROCESS_STATUS={report.get('process_status')}",
        f"SOURCE_DEPENDENCY_VALID={str(report.get('source_dependency_valid')).lower()}",
        f"TASK_BUDGET_MAX={report.get('task_budget_max')}",
        f"CURRENT_TASK_NUMBER={report.get('current_task_number')}",
        f"IMPLEMENTATION_STARTED={str(report.get('implementation_started')).lower()}",
        f"IMPLEMENTATION_ALLOWED_AT_TASK_1={str(report.get('implementation_allowed_at_task_1')).lower()}",
        f"OBJECTIVE_SELECTION_REQUIRED_NEXT={str(report.get('objective_selection_required_next')).lower()}",
        f"SCOPE_LOCK_REQUIRED_NEXT={str(report.get('scope_lock_required_next')).lower()}",
        f"PROPOSED_OPERATOR_SEED_ID={seed.get('seed_id')}",
        f"PROPOSED_OPERATOR_SEED_STATUS={seed.get('status')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Operator seed",
        "",
        "The operator-provided fail-closed JOKER-C2 identity boundary text is registered only as candidate input for the next scope lock.",
        "It is not implemented in Task 1.",
        "",
    ]
    return "\n".join(lines)


def write_task_1_artifacts(base_dir: str | Path = "examples/milestone-30/governed-opening-with-task-budget-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_governed_opening_report()

    manifest = {
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "opening_revision": OPENING_REVISION,
        "source_closure_revision": SOURCE_CLOSURE_REVISION,
        "source_task_6_signature": task_6_signature(),
        "task_1_signature": task_1_signature(),
        "opening_id": report["opening_id"],
        "opening_signature": report["opening_signature"],
        "opening_status": report["opening_status"],
        "technical_status": report["technical_status"],
        "process_status": report["process_status"],
        "source_dependency_valid": report["source_dependency_valid"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
        "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
        "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
        "proposed_operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
        "proposed_operator_seed_status": PROPOSED_OPERATOR_SEED_STATUS,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    operator_seed = {
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "proposed_operator_seed": OPERATOR_SEED_SUMMARY,
        "implementation_status": "NOT_IMPLEMENTED_IN_TASK_1",
        "scope_lock_required_next": True,
    }

    (output_dir / "task-1-governed-opening.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-governed-opening.md").write_text(
        render_governed_opening_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-1-operator-seed.json").write_text(
        json.dumps(operator_seed, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
                f"TASK_ID={TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}",
                f"OPENING_REVISION={OPENING_REVISION}",
                f"SOURCE_CLOSURE_REVISION={SOURCE_CLOSURE_REVISION}",
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
                f"PROPOSED_OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}",
                f"PROPOSED_OPERATOR_SEED_STATUS={PROPOSED_OPERATOR_SEED_STATUS}",
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
        "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
        f"MILESTONE_30_TASK_1_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_30_TASK_1_SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}",
        f"MILESTONE_30_TASK_1_OPENING_REVISION={OPENING_REVISION}",
        f"MILESTONE_30_TASK_1_SOURCE_CLOSURE_REVISION={SOURCE_CLOSURE_REVISION}",
        f"MILESTONE_30_TASK_1_SOURCE_TASK_6_SIGNATURE={task_6_signature()}",
        f"MILESTONE_30_TASK_1_TASK_1_SIGNATURE={task_1_signature()}",
        f"MILESTONE_30_TASK_1_OPENING_ID={report['opening_id']}",
        f"MILESTONE_30_TASK_1_OPENING_SIGNATURE={report['opening_signature']}",
        f"MILESTONE_30_TASK_1_OPENING_STATUS={report['opening_status']}",
        f"MILESTONE_30_TASK_1_TECHNICAL_STATUS={report['technical_status']}",
        f"MILESTONE_30_TASK_1_PROCESS_STATUS={report['process_status']}",
        f"MILESTONE_30_TASK_1_SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
        f"MILESTONE_30_TASK_1_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_30_TASK_1_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_30_TASK_1_IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
        f"MILESTONE_30_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1={str(IMPLEMENTATION_ALLOWED_AT_TASK_1).lower()}",
        f"MILESTONE_30_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT={str(OBJECTIVE_SELECTION_REQUIRED_NEXT).lower()}",
        f"MILESTONE_30_TASK_1_SCOPE_LOCK_REQUIRED_NEXT={str(SCOPE_LOCK_REQUIRED_NEXT).lower()}",
        f"MILESTONE_30_TASK_1_PROPOSED_OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}",
        f"MILESTONE_30_TASK_1_PROPOSED_OPERATOR_SEED_STATUS={PROPOSED_OPERATOR_SEED_STATUS}",
        f"MILESTONE_30_TASK_1_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_30_TASK_1_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_1_artifacts()
    for line in task_1_status_lines():
        print(line)
