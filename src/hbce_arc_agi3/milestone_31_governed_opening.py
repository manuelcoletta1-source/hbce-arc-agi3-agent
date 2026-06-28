from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed_final_closure import (
    CLOSURE_STATUS as SOURCE_CLOSURE_STATUS,
    FINAL_TASK_NUMBER as SOURCE_FINAL_TASK_NUMBER,
    MILESTONE_ID as SOURCE_MILESTONE_ID,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    PROCESS_STATUS as SOURCE_PROCESS_STATUS,
    READY_FOR_NEXT_MILESTONE as SOURCE_READY_FOR_NEXT_MILESTONE,
    TASK_BUDGET_MAX as SOURCE_TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    TECHNICAL_STATUS as SOURCE_TECHNICAL_STATUS,
    run_identity_boundary_fail_closed_final_closure,
    task_6_signature,
    validate_final_closure_report,
)


MILESTONE_ID = "MILESTONE_31"
TASK_ID = "MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
OPENING_REVISION = "MILESTONE_31_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

CURRENT_TASK_NUMBER = 1
TASK_BUDGET_MAX = 8

NEXT_STAGE = "MILESTONE_31_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

OPENING_STATUS = "OPEN"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8"

IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_1 = False
OBJECTIVE_SELECTION_REQUIRED_NEXT = True
SCOPE_LOCK_REQUIRED_NEXT = True

GENERATED_ARTIFACT_COUNT = 5

PROPOSED_OPERATOR_SEED_ID = "JOKER_C2_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE"
PROPOSED_OPERATOR_SEED_STATUS = "CANDIDATE_ONLY_NOT_LOCKED"
PROPOSED_OPERATOR_SEED_OBJECTIVE = (
    "Define a verified operator authorization session gate for JOKER-C2 that can activate "
    "private authorized scope only after verified Manuel identity, valid authorization, sufficient context, "
    "available verification and preserved fail-closed guardrails."
)

SOURCE_CLOSURE_REPORT_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-final-closure-v1/task-6-final-closure-report.json")
SOURCE_CLOSURE_CASES_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-final-closure-v1/task-6-closure-cases.json")
SOURCE_CLOSURE_MANIFEST_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-final-closure-v1/task-6-manifest.json")
SOURCE_CLOSURE_INDEX_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-final-closure-v1/task-6-index.txt")
SOURCE_CLOSURE_MARKDOWN_PATH = Path("examples/milestone-30/identity-boundary-fail-closed-final-closure-v1/task-6-final-closure-report.md")


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
            "milestone_id": MILESTONE_ID,
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "opening_revision": OPENING_REVISION,
            "source_task_6_signature": task_6_signature(),
            "proposed_operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
            "proposed_operator_seed_status": PROPOSED_OPERATOR_SEED_STATUS,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "next_stage": NEXT_STAGE,
        }
    )


def build_source_closure_snapshot() -> dict[str, Any]:
    runtime = run_identity_boundary_fail_closed_final_closure()
    persisted = _load_json(SOURCE_CLOSURE_REPORT_PATH)

    runtime_valid = validate_final_closure_report(runtime)
    persisted_valid = validate_final_closure_report(persisted)

    return {
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_closure_id": runtime.get("closure_id"),
        "persisted_closure_id": persisted.get("closure_id"),
        "runtime_closure_signature": runtime.get("closure_signature"),
        "persisted_closure_signature": persisted.get("closure_signature"),
        "runtime_task_6_signature": runtime.get("task_6_signature"),
        "persisted_task_6_signature": persisted.get("task_6_signature"),
        "source_closure_status": persisted.get("closure_status"),
        "source_technical_status": persisted.get("technical_status"),
        "source_process_status": persisted.get("process_status"),
        "source_milestone_closed": persisted.get("milestone_closed"),
        "source_ready_for_next_milestone": persisted.get("ready_for_next_milestone"),
        "source_private_core_access_allowed_without_verified_manuel": persisted.get("source_private_core_access_allowed_without_verified_manuel"),
        "source_unverified_manuel_assumption_allowed": persisted.get("source_unverified_manuel_assumption_allowed"),
        "source_external_command_authority_allowed": persisted.get("source_external_command_authority_allowed"),
        "source_task_budget_max": persisted.get("task_budget_max"),
        "source_final_task_number": persisted.get("final_task_number"),
        "source_task_7_unused": persisted.get("task_7_unused"),
        "source_task_8_unused": persisted.get("task_8_unused"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_closure": (
            runtime.get("closure_id") == persisted.get("closure_id")
            and runtime.get("closure_signature") == persisted.get("closure_signature")
            and runtime.get("task_6_signature") == persisted.get("task_6_signature") == task_6_signature()
        ),
    }


def validate_source_closure_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_milestone_id") != SOURCE_MILESTONE_ID:
        return False
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("source_closure_status") != SOURCE_CLOSURE_STATUS:
        return False
    if snapshot.get("source_technical_status") != SOURCE_TECHNICAL_STATUS:
        return False
    if snapshot.get("source_process_status") != SOURCE_PROCESS_STATUS:
        return False
    if snapshot.get("source_milestone_closed") is not True:
        return False
    if snapshot.get("source_ready_for_next_milestone") is not SOURCE_READY_FOR_NEXT_MILESTONE:
        return False
    if snapshot.get("source_private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if snapshot.get("source_unverified_manuel_assumption_allowed") is not False:
        return False
    if snapshot.get("source_external_command_authority_allowed") is not False:
        return False
    if snapshot.get("source_task_budget_max") != SOURCE_TASK_BUDGET_MAX:
        return False
    if snapshot.get("source_final_task_number") != SOURCE_FINAL_TASK_NUMBER:
        return False
    if snapshot.get("source_task_7_unused") is not True:
        return False
    if snapshot.get("source_task_8_unused") is not True:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_closure"))


def build_governed_opening_report() -> dict[str, Any]:
    source_snapshot = build_source_closure_snapshot()
    source_dependency_valid = validate_source_closure_snapshot(source_snapshot)

    core = {
        "milestone_id": MILESTONE_ID,
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "opening_revision": OPENING_REVISION,
        "source_task_6_signature": task_6_signature(),
        "task_1_signature": task_1_signature(),
        "source_dependency_valid": source_dependency_valid,
        "source_closure_snapshot": source_snapshot,
        "opening_status": OPENING_STATUS,
        "technical_status": TECHNICAL_STATUS,
        "process_status": PROCESS_STATUS,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
        "objective_selection_required_next": OBJECTIVE_SELECTION_REQUIRED_NEXT,
        "scope_lock_required_next": SCOPE_LOCK_REQUIRED_NEXT,
        "proposed_operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
        "proposed_operator_seed_status": PROPOSED_OPERATOR_SEED_STATUS,
        "proposed_operator_seed_objective": PROPOSED_OPERATOR_SEED_OBJECTIVE,
        "guardrails_carried_forward": {
            "private_core_access_allowed_without_verified_manuel": False,
            "unverified_manuel_assumption_allowed": False,
            "external_command_authority_allowed": False,
            "fail_closed_default": True,
            "candidate_seed_not_locked": True,
            "implementation_not_started": True,
        },
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    opening_id = "MILESTONE-31-GOVERNED-OPENING-" + _stable_digest(core)
    opening_signature = _stable_digest(
        {
            "opening_id": opening_id,
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "source_task_6_signature": task_6_signature(),
            "task_1_signature": task_1_signature(),
            "opening_revision": OPENING_REVISION,
            "proposed_operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        **core,
        "opening_id": opening_id,
        "opening_signature": opening_signature,
    }


def validate_governed_opening_report(report: Mapping[str, Any]) -> bool:
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("opening_revision") != OPENING_REVISION:
        return False
    if report.get("source_task_6_signature") != task_6_signature():
        return False
    if report.get("task_1_signature") != task_1_signature():
        return False
    if report.get("source_dependency_valid") is not True:
        return False
    if not validate_source_closure_snapshot(report.get("source_closure_snapshot", {})):
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
    if report.get("implementation_started") is not False:
        return False
    if report.get("implementation_allowed_at_task_1") is not False:
        return False
    if report.get("objective_selection_required_next") is not True:
        return False
    if report.get("scope_lock_required_next") is not True:
        return False
    if report.get("proposed_operator_seed_id") != PROPOSED_OPERATOR_SEED_ID:
        return False
    if report.get("proposed_operator_seed_status") != PROPOSED_OPERATOR_SEED_STATUS:
        return False
    guardrails = report.get("guardrails_carried_forward", {})
    if guardrails.get("private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if guardrails.get("unverified_manuel_assumption_allowed") is not False:
        return False
    if guardrails.get("external_command_authority_allowed") is not False:
        return False
    if guardrails.get("fail_closed_default") is not True:
        return False
    if guardrails.get("candidate_seed_not_locked") is not True:
        return False
    if guardrails.get("implementation_not_started") is not True:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("opening_id") and report.get("opening_signature"))


def render_opening_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 31 Task 1 Governed Opening With Task Budget",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"OPENING_ID={report.get('opening_id')}",
        f"OPENING_SIGNATURE={report.get('opening_signature')}",
        f"OPENING_STATUS={report.get('opening_status')}",
        f"TECHNICAL_STATUS={report.get('technical_status')}",
        f"PROCESS_STATUS={report.get('process_status')}",
        f"TASK_BUDGET_MAX={report.get('task_budget_max')}",
        f"CURRENT_TASK_NUMBER={report.get('current_task_number')}",
        f"PROPOSED_OPERATOR_SEED_ID={report.get('proposed_operator_seed_id')}",
        f"PROPOSED_OPERATOR_SEED_STATUS={report.get('proposed_operator_seed_status')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Candidate seed",
        "",
        str(report.get("proposed_operator_seed_objective")),
        "",
    ]
    return "\n".join(lines)


def write_task_1_artifacts(base_dir: str | Path = "examples/milestone-31/governed-opening-with-task-budget-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_governed_opening_report()

    seed_candidate = {
        "milestone_id": MILESTONE_ID,
        "task_id": TASK_ID,
        "proposed_operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
        "proposed_operator_seed_status": PROPOSED_OPERATOR_SEED_STATUS,
        "proposed_operator_seed_objective": PROPOSED_OPERATOR_SEED_OBJECTIVE,
        "candidate_only": True,
        "selected": False,
        "scope_locked": False,
        "implementation_started": False,
        "requires_task_2_objective_selection": True,
        "requires_task_2_scope_lock": True,
    }

    manifest = {
        "milestone_id": MILESTONE_ID,
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "opening_revision": OPENING_REVISION,
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
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-1-governed-opening.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-governed-opening.md").write_text(
        render_opening_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-1-proposed-operator-seed.json").write_text(
        json.dumps(seed_candidate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-1-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"OPENING_REVISION={OPENING_REVISION}",
                f"SOURCE_TASK_6_SIGNATURE={task_6_signature()}",
                f"TASK_1_SIGNATURE={task_1_signature()}",
                f"OPENING_ID={report['opening_id']}",
                f"OPENING_SIGNATURE={report['opening_signature']}",
                f"OPENING_STATUS={report['opening_status']}",
                f"TECHNICAL_STATUS={report['technical_status']}",
                f"PROCESS_STATUS={report['process_status']}",
                f"SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
                f"SOURCE_MILESTONE_CLOSED={str(report['source_closure_snapshot']['source_milestone_closed']).lower()}",
                f"SOURCE_READY_FOR_NEXT_MILESTONE={str(report['source_closure_snapshot']['source_ready_for_next_milestone']).lower()}",
                f"PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(report['guardrails_carried_forward']['private_core_access_allowed_without_verified_manuel']).lower()}",
                f"UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['guardrails_carried_forward']['unverified_manuel_assumption_allowed']).lower()}",
                f"EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['guardrails_carried_forward']['external_command_authority_allowed']).lower()}",
                f"FAIL_CLOSED_DEFAULT={str(report['guardrails_carried_forward']['fail_closed_default']).lower()}",
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

    return {"report": report, "manifest": manifest, "seed_candidate": seed_candidate, "output_dir": str(output_dir)}


def task_1_status_lines() -> tuple[str, ...]:
    report = build_governed_opening_report()
    return (
        "MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
        f"MILESTONE_31_TASK_1_MILESTONE_ID={MILESTONE_ID}",
        f"MILESTONE_31_TASK_1_TASK_ID={TASK_ID}",
        f"MILESTONE_31_TASK_1_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_31_TASK_1_OPENING_REVISION={OPENING_REVISION}",
        f"MILESTONE_31_TASK_1_SOURCE_TASK_6_SIGNATURE={task_6_signature()}",
        f"MILESTONE_31_TASK_1_TASK_1_SIGNATURE={task_1_signature()}",
        f"MILESTONE_31_TASK_1_OPENING_ID={report['opening_id']}",
        f"MILESTONE_31_TASK_1_OPENING_SIGNATURE={report['opening_signature']}",
        f"MILESTONE_31_TASK_1_OPENING_STATUS={report['opening_status']}",
        f"MILESTONE_31_TASK_1_TECHNICAL_STATUS={report['technical_status']}",
        f"MILESTONE_31_TASK_1_PROCESS_STATUS={report['process_status']}",
        f"MILESTONE_31_TASK_1_SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
        f"MILESTONE_31_TASK_1_SOURCE_MILESTONE_CLOSED={str(report['source_closure_snapshot']['source_milestone_closed']).lower()}",
        f"MILESTONE_31_TASK_1_SOURCE_READY_FOR_NEXT_MILESTONE={str(report['source_closure_snapshot']['source_ready_for_next_milestone']).lower()}",
        f"MILESTONE_31_TASK_1_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL={str(report['guardrails_carried_forward']['private_core_access_allowed_without_verified_manuel']).lower()}",
        f"MILESTONE_31_TASK_1_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report['guardrails_carried_forward']['unverified_manuel_assumption_allowed']).lower()}",
        f"MILESTONE_31_TASK_1_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report['guardrails_carried_forward']['external_command_authority_allowed']).lower()}",
        f"MILESTONE_31_TASK_1_FAIL_CLOSED_DEFAULT={str(report['guardrails_carried_forward']['fail_closed_default']).lower()}",
        f"MILESTONE_31_TASK_1_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_31_TASK_1_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_31_TASK_1_IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
        f"MILESTONE_31_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1={str(IMPLEMENTATION_ALLOWED_AT_TASK_1).lower()}",
        f"MILESTONE_31_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT={str(OBJECTIVE_SELECTION_REQUIRED_NEXT).lower()}",
        f"MILESTONE_31_TASK_1_SCOPE_LOCK_REQUIRED_NEXT={str(SCOPE_LOCK_REQUIRED_NEXT).lower()}",
        f"MILESTONE_31_TASK_1_PROPOSED_OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}",
        f"MILESTONE_31_TASK_1_PROPOSED_OPERATOR_SEED_STATUS={PROPOSED_OPERATOR_SEED_STATUS}",
        f"MILESTONE_31_TASK_1_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_31_TASK_1_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_1_artifacts()
    for line in task_1_status_lines():
        print(line)
