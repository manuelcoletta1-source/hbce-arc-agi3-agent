"""Milestone #18 Task 1 - Controlled Technical Solver Improvement Opening Gate v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_18_TASK_1_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_OPENING_GATE_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

OPENING_GATE_MARKER = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_OPENING_GATE_READY"
OPENING_GATE_VERDICT = (
    "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_OPENING_GATE_PASS_PLAN_ONLY_NO_IMPLEMENTATION"
)
OPENING_GATE_DECISION = (
    "OPEN_MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
)
OPENING_GATE_REASON = (
    "OPERATOR_DIRECTION_RECEIVED_AFTER_MILESTONE_17_TERMINAL_STOP_RECORD"
)

SOURCE_MILESTONE_17_TERMINAL_STOP_COMMIT = "bd94b8a"
SOURCE_MILESTONE_17_TERMINAL_STOP_SIGNATURE = "B0355A824F6C64C7"
SOURCE_MILESTONE_17_TERMINAL_STAGE = (
    "MILESTONE_17_TASK_67_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_TERMINAL_STOP_RECORD_V1"
)

MILESTONE_18_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"
PREVIOUS_STAGE = "OPERATOR_DIRECTION_REQUIRED_BEFORE_MILESTONE_18"
NEXT_STAGE = "MILESTONE_18_TASK_2_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_V1"

TASK_MODE = (
    "MILESTONE_18_TASK_1_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_OPENING_GATE_V1_"
    "PLAN_ONLY_LOCAL_ONLY"
)

OPENING_SCOPE = "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_OPENING_GATE_ONLY"
MILESTONE_18_SCOPE = "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"
RUNTIME_AUTHORIZATION_SCOPE = "NOT_GRANTED"
SUBMISSION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

ARTIFACT_DIR = Path("examples/milestone-18/controlled-technical-solver-improvement-opening-gate-v1")
DOC_PATH = Path("docs/milestone-18-controlled-technical-solver-improvement-opening-gate-v1.md")


OPENING_GATE_GATES: tuple[str, ...] = (
    "source_milestone_17_terminal_stop_commit_bound",
    "source_milestone_17_terminal_stop_signature_bound",
    "source_milestone_17_terminal_stage_bound",
    "operator_direction_received",
    "milestone_17_stopped_confirmed",
    "milestone_18_opening_allowed",
    "milestone_18_opened",
    "milestone_18_scope_plan_only",
    "opening_scope_confirmed",
    "previous_stage_operator_direction_required",
    "next_stage_limitation_inventory_declared",
    "implementation_authorization_not_granted",
    "runtime_authorization_not_granted",
    "submission_authorization_not_granted",
    "implementation_not_authorized",
    "implementation_blocked",
    "implementation_not_performed",
    "runtime_solver_patch_not_allowed",
    "runtime_solver_not_modified",
    "candidate_generator_patch_not_allowed",
    "candidate_generator_not_modified",
    "ranker_patch_not_allowed",
    "ranker_not_modified",
    "runtime_wiring_not_allowed",
    "runtime_wiring_not_performed",
    "runtime_activation_not_authorized",
    "runtime_activation_not_performed",
    "runtime_execution_not_allowed",
    "runtime_execution_not_performed",
    "real_evaluation_not_allowed",
    "real_submission_not_allowed",
    "manual_upload_not_allowed",
    "upload_not_performed",
    "kaggle_authentication_not_allowed",
    "kaggle_authentication_not_performed",
    "kaggle_submission_not_sent",
    "competitive_score_claim_not_allowed",
    "official_score_claim_not_allowed",
    "private_core_not_exposed",
    "legal_certification_false",
    "fail_closed_required",
    "fail_closed_active",
    "local_only_true",
    "deterministic_true",
    "public_safe_true",
    "external_api_dependency_false",
    "internet_during_eval_false",
    "opening_gate_ready",
    "opening_gate_passed",
    "opening_gate_locked",
    "artifact_set_declared",
    "artifact_count_five",
    "manifest_created",
    "index_created",
    "markdown_created",
    "json_payload_created",
    "docs_payload_created",
    "technical_solver_improvement_objective_declared",
    "limitation_inventory_next",
    "diagnostic_scope_not_runtime",
    "planning_scope_not_implementation",
    "no_private_hbce_core_exposure",
    "no_kaggle_score_claim",
)


OBJECTIVES: tuple[dict[str, str], ...] = (
    {
        "objective_id": "M18-OBJ-1",
        "name": "solver limitation inventory",
        "status": "NEXT_TASK",
        "implementation_authorized": "false",
    },
    {
        "objective_id": "M18-OBJ-2",
        "name": "candidate generator improvement map",
        "status": "PLANNED_NOT_AUTHORIZED",
        "implementation_authorized": "false",
    },
    {
        "objective_id": "M18-OBJ-3",
        "name": "ranker evidence weighting improvement map",
        "status": "PLANNED_NOT_AUTHORIZED",
        "implementation_authorized": "false",
    },
    {
        "objective_id": "M18-OBJ-4",
        "name": "local diagnostic benchmark preservation",
        "status": "PLANNED_NOT_AUTHORIZED",
        "implementation_authorized": "false",
    },
    {
        "objective_id": "M18-OBJ-5",
        "name": "dry-run candidate format discipline",
        "status": "PLANNED_NOT_AUTHORIZED",
        "implementation_authorized": "false",
    },
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_milestone_18_controlled_technical_solver_improvement_opening_gate() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_milestone_17_terminal_stop_commit": SOURCE_MILESTONE_17_TERMINAL_STOP_COMMIT,
        "source_milestone_17_terminal_stop_signature": SOURCE_MILESTONE_17_TERMINAL_STOP_SIGNATURE,
        "source_milestone_17_terminal_stage": SOURCE_MILESTONE_17_TERMINAL_STAGE,
        "opening_scope": OPENING_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "verdict": OPENING_GATE_VERDICT,
        "decision": OPENING_GATE_DECISION,
        "reason": OPENING_GATE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_received": True,
        "milestone_18_opened": True,
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-improvement-opening-gate-v1.json"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-improvement-opening-gate-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-improvement-opening-gate-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-improvement-opening-gate-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "opening_gate_marker": OPENING_GATE_MARKER,
        "signature": signature,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_milestone_17_terminal_stop_commit": SOURCE_MILESTONE_17_TERMINAL_STOP_COMMIT,
        "source_milestone_17_terminal_stop_signature": SOURCE_MILESTONE_17_TERMINAL_STOP_SIGNATURE,
        "source_milestone_17_terminal_stage": SOURCE_MILESTONE_17_TERMINAL_STAGE,
        "task_mode": TASK_MODE,
        "verdict": OPENING_GATE_VERDICT,
        "decision": OPENING_GATE_DECISION,
        "opening_gate_reason": OPENING_GATE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_received": True,
        "operator_direction_value": MILESTONE_18_NAME,
        "milestone_17_stopped": True,
        "milestone_18_opening_allowed": True,
        "milestone_18_opened": True,
        "opening_scope": OPENING_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "runtime_authorization_scope": RUNTIME_AUTHORIZATION_SCOPE,
        "submission_authorization_scope": SUBMISSION_AUTHORIZATION_SCOPE,
        "controlled_technical_solver_improvement_opening_gate_ready": True,
        "controlled_technical_solver_improvement_opening_gate_passed": True,
        "controlled_technical_solver_improvement_opening_gate_locked": True,
        "technical_solver_improvement_objectives": OBJECTIVES,
        "objective_count": len(OBJECTIVES),
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "runtime_solver_patch_allowed": False,
        "runtime_solver_modified": False,
        "candidate_generator_patch_allowed": False,
        "candidate_generator_modified": False,
        "ranker_patch_allowed": False,
        "ranker_modified": False,
        "runtime_wiring_allowed": False,
        "runtime_wiring_performed": False,
        "runtime_activation_authorized": False,
        "runtime_activation_performed": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "opening_gate_count": len(OPENING_GATE_GATES),
        "opening_gate_failure_count": 0,
        "opening_gates": OPENING_GATE_GATES,
        "artifacts": artifacts,
    }


def validate_milestone_18_controlled_technical_solver_improvement_opening_gate(
    status: dict[str, Any],
) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "opening_gate_marker": OPENING_GATE_MARKER,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_milestone_17_terminal_stop_commit": SOURCE_MILESTONE_17_TERMINAL_STOP_COMMIT,
        "source_milestone_17_terminal_stop_signature": SOURCE_MILESTONE_17_TERMINAL_STOP_SIGNATURE,
        "source_milestone_17_terminal_stage": SOURCE_MILESTONE_17_TERMINAL_STAGE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "opening_scope": OPENING_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "runtime_authorization_scope": RUNTIME_AUTHORIZATION_SCOPE,
        "submission_authorization_scope": SUBMISSION_AUTHORIZATION_SCOPE,
        "verdict": OPENING_GATE_VERDICT,
        "decision": OPENING_GATE_DECISION,
        "opening_gate_reason": OPENING_GATE_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    required_true = (
        "operator_direction_received",
        "milestone_17_stopped",
        "milestone_18_opening_allowed",
        "milestone_18_opened",
        "controlled_technical_solver_improvement_opening_gate_ready",
        "controlled_technical_solver_improvement_opening_gate_passed",
        "controlled_technical_solver_improvement_opening_gate_locked",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
        "local_only",
        "deterministic",
        "public_safe",
    )
    required_false = (
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
        "candidate_generator_patch_allowed",
        "candidate_generator_modified",
        "ranker_patch_allowed",
        "ranker_modified",
        "runtime_wiring_allowed",
        "runtime_wiring_performed",
        "runtime_activation_authorized",
        "runtime_activation_performed",
        "runtime_execution_allowed",
        "runtime_execution_performed",
        "real_evaluation_allowed",
        "real_submission_allowed",
        "manual_upload_allowed",
        "upload_performed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_submission_sent",
        "competitive_score_claim_allowed",
        "official_score_claim_allowed",
        "private_core_exposure",
        "legal_certification",
        "external_api_dependency",
        "internet_during_eval",
    )

    for key in required_true:
        if status.get(key) is not True:
            issues.append(f"{key} must be True")
    for key in required_false:
        if status.get(key) is not False:
            issues.append(f"{key} must be False")

    objectives = tuple(status.get("technical_solver_improvement_objectives", ()))
    if status.get("objective_count") != 5:
        issues.append("objective_count must be 5")
    if len(objectives) != 5:
        issues.append("technical_solver_improvement_objectives length must be 5")
    for objective in objectives:
        if objective.get("implementation_authorized") != "false":
            issues.append(f"{objective.get('objective_id')} implementation_authorized must be false")

    if status.get("opening_gate_count") != len(OPENING_GATE_GATES):
        issues.append("opening_gate_count mismatch")
    if status.get("opening_gate_failure_count") != 0:
        issues.append("opening_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def opening_gate_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["opening_gate_marker"],
        "signature": status["signature"],
        "milestone_18_name": status["milestone_18_name"],
        "source_milestone_17_terminal_stop_commit": status["source_milestone_17_terminal_stop_commit"],
        "source_milestone_17_terminal_stop_signature": status["source_milestone_17_terminal_stop_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "opening_scope": status["opening_scope"],
        "milestone_18_scope": status["milestone_18_scope"],
        "operator_direction_received": status["operator_direction_received"],
        "milestone_17_stopped": status["milestone_17_stopped"],
        "milestone_18_opened": status["milestone_18_opened"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "opening_gate_count": status["opening_gate_count"],
        "opening_gate_failure_count": status["opening_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["opening_gate_marker"],
        f"signature={status['signature']}",
        f"milestone_18_name={status['milestone_18_name']}",
        f"source_milestone_17_terminal_stop_commit={status['source_milestone_17_terminal_stop_commit']}",
        f"source_milestone_17_terminal_stop_signature={status['source_milestone_17_terminal_stop_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"opening_gate_reason={status['opening_gate_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"operator_direction_received={status['operator_direction_received']}",
        f"milestone_17_stopped={status['milestone_17_stopped']}",
        f"milestone_18_opened={status['milestone_18_opened']}",
        f"opening_scope={status['opening_scope']}",
        f"milestone_18_scope={status['milestone_18_scope']}",
        f"objective_count={status['objective_count']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"opening_gate_count={status['opening_gate_count']}",
        f"opening_gate_failure_count={status['opening_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def build_markdown(status: dict[str, Any]) -> str:
    objective_lines = "\n".join(
        f"- `{obj['objective_id']}` - {obj['name']} · `{obj['status']}` · implementation_authorized=`{obj['implementation_authorized']}`"
        for obj in status["technical_solver_improvement_objectives"]
    )

    return f"""# Milestone #18 Task 1 - Controlled Technical Solver Improvement Opening Gate v1

## Status

`{status["opening_gate_marker"]}`

## Source binding

- source Milestone #17 terminal stop commit: `{status["source_milestone_17_terminal_stop_commit"]}`
- source Milestone #17 terminal stop signature: `{status["source_milestone_17_terminal_stop_signature"]}`
- source stage: `{status["source_milestone_17_terminal_stage"]}`
- previous stage: `{status["previous_stage"]}`
- next stage: `{status["next_stage"]}`

## Opening decision

- milestone_18_name: `{status["milestone_18_name"]}`
- operator_direction_received: `{status["operator_direction_received"]}`
- milestone_17_stopped: `{status["milestone_17_stopped"]}`
- milestone_18_opened: `{status["milestone_18_opened"]}`
- opening_scope: `{status["opening_scope"]}`
- milestone_18_scope: `{status["milestone_18_scope"]}`

## Objectives

{objective_lines}

## Boundary

This opening gate authorizes planning only.
It does not authorize implementation.
It does not authorize runtime execution.
It does not authorize real evaluation.
It does not authorize Kaggle authentication, upload, or submission.
It does not authorize competitive or official score claims.
It does not expose private HBCE/JOKER-C2 core material.

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`
"""


def write_milestone_18_controlled_technical_solver_improvement_opening_gate_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_milestone_18_controlled_technical_solver_improvement_opening_gate()
    issues = validate_milestone_18_controlled_technical_solver_improvement_opening_gate(resolved)
    if issues:
        raise ValueError(
            "Invalid milestone 18 controlled technical solver improvement opening gate: "
            + "; ".join(issues)
        )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = opening_gate_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    manifest = build_manifest(resolved)
    markdown = build_markdown(resolved)

    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-improvement-opening-gate-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-improvement-opening-gate-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-improvement-opening-gate-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-improvement-opening-gate-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_milestone_18_controlled_technical_solver_improvement_opening_gate_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_milestone_17_terminal_stop_commit"])
    print(status["task_mode"])
    print(status["opening_gate_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["opening_gate_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "milestone_18_name",
        "source_milestone_17_terminal_stop_commit",
        "source_milestone_17_terminal_stop_signature",
        "operator_direction_received",
        "operator_direction_value",
        "milestone_17_stopped",
        "milestone_18_opening_allowed",
        "milestone_18_opened",
        "opening_scope",
        "milestone_18_scope",
        "objective_count",
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_blocked",
        "implementation_performed",
        "runtime_execution_allowed",
        "runtime_execution_performed",
        "real_evaluation_allowed",
        "real_submission_allowed",
        "manual_upload_allowed",
        "upload_performed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_submission_sent",
        "competitive_score_claim_allowed",
        "official_score_claim_allowed",
        "private_core_exposure",
        "legal_certification",
        "fail_closed_required",
        "fail_closed_active",
        "local_only",
        "deterministic",
        "public_safe",
        "external_api_dependency",
        "internet_during_eval",
        "opening_gate_count",
        "opening_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for objective in status["technical_solver_improvement_objectives"]:
        print(
            f"technical_solver_improvement_objective={objective['objective_id']}|{objective['name']}|"
            f"{objective['status']}|implementation_authorized={objective['implementation_authorized']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
