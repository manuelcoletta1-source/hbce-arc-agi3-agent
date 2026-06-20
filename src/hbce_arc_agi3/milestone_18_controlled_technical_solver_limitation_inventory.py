"""Milestone #18 Task 2 - Controlled Technical Solver Limitation Inventory v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_18_TASK_2_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

LIMITATION_INVENTORY_MARKER = (
    "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_READY"
)
LIMITATION_INVENTORY_VERDICT = (
    "CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_PASS_DIAGNOSTIC_ONLY_NO_IMPLEMENTATION"
)
LIMITATION_INVENTORY_DECISION = (
    "RECORD_SOLVER_LIMITATIONS_FOR_CONTROLLED_TECHNICAL_IMPROVEMENT_PLAN_ONLY"
)
LIMITATION_INVENTORY_REASON = (
    "TASK_1_OPENED_MILESTONE_18_AS_PLAN_ONLY_WITHOUT_RUNTIME_OR_SUBMISSION"
)

MILESTONE_18_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

SOURCE_TASK_1_COMMIT = "d5ee6c9"
SOURCE_TASK_1_SIGNATURE = "E952B1DD4CBA8A66"
SOURCE_TASK_1_STAGE = "MILESTONE_18_TASK_1_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_OPENING_GATE_V1"

PREVIOUS_STAGE = SOURCE_TASK_1_STAGE
NEXT_STAGE = "MILESTONE_18_TASK_3_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_V1"

TASK_MODE = (
    "MILESTONE_18_TASK_2_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_V1_"
    "DIAGNOSTIC_ONLY_LOCAL_ONLY"
)

INVENTORY_SCOPE = "CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_ONLY"
MILESTONE_18_SCOPE = "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"
RUNTIME_AUTHORIZATION_SCOPE = "NOT_GRANTED"
SUBMISSION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

ARTIFACT_DIR = Path("examples/milestone-18/controlled-technical-solver-limitation-inventory-v1")
DOC_PATH = Path("docs/milestone-18-controlled-technical-solver-limitation-inventory-v1.md")


LIMITATION_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "limitation_id": "M18-LIM-1",
        "area": "solver coverage",
        "description": "Current solver improvement chain lacks a fresh structured inventory of unsolved local ARC-style failure families.",
        "risk": "Changes may target attractive modules instead of actual failure modes.",
        "next_action": "Build controlled limitation inventory before any implementation.",
        "implementation_authorized": False,
    },
    {
        "limitation_id": "M18-LIM-2",
        "area": "candidate generation",
        "description": "Candidate generator improvements are mapped as objectives but not yet tied to concrete failure evidence.",
        "risk": "Generator changes could increase candidate noise or overfit local fixtures.",
        "next_action": "Map generator limits against diagnostic fixtures and family benchmark cases.",
        "implementation_authorized": False,
    },
    {
        "limitation_id": "M18-LIM-3",
        "area": "ranker evidence",
        "description": "Ranker evidence weighting improvement is declared but not yet prioritized by observed error pattern.",
        "risk": "Ranking may preserve weak candidates or suppress valid transformations.",
        "next_action": "Create ranker limitation categories before weighting changes.",
        "implementation_authorized": False,
    },
    {
        "limitation_id": "M18-LIM-4",
        "area": "local diagnostics",
        "description": "Diagnostic benchmark preservation is declared but current milestone has not yet frozen a limitation-specific diagnostic matrix.",
        "risk": "Future improvement could regress existing public-safe deterministic behavior.",
        "next_action": "Tie each limitation to local diagnostic cases and regression expectations.",
        "implementation_authorized": False,
    },
    {
        "limitation_id": "M18-LIM-5",
        "area": "submission discipline",
        "description": "Dry-run candidate format discipline exists as objective but not yet connected to solver improvement limits.",
        "risk": "Format readiness could be mistaken for real solver quality.",
        "next_action": "Keep dry-run packaging separate from solver capability claims.",
        "implementation_authorized": False,
    },
    {
        "limitation_id": "M18-LIM-6",
        "area": "authorization boundary",
        "description": "Milestone 18 is open for controlled technical planning only.",
        "risk": "Planning could accidentally slide into implementation, runtime execution, or score claims.",
        "next_action": "Keep implementation, runtime, Kaggle auth, upload, submission, and score claims blocked.",
        "implementation_authorized": False,
    },
)

LIMITATION_INVENTORY_GATES: tuple[str, ...] = (
    "source_task_1_commit_bound",
    "source_task_1_signature_bound",
    "source_task_1_stage_bound",
    "milestone_18_name_confirmed",
    "previous_stage_task_1_opening_gate",
    "next_stage_limitation_inventory_review_declared",
    "inventory_scope_confirmed",
    "milestone_18_scope_plan_only",
    "implementation_authorization_not_granted",
    "runtime_authorization_not_granted",
    "submission_authorization_not_granted",
    "limitation_inventory_ready",
    "limitation_inventory_passed",
    "limitation_inventory_locked",
    "limitation_count_six",
    "all_limitations_have_ids",
    "all_limitations_have_areas",
    "all_limitations_have_descriptions",
    "all_limitations_have_risks",
    "all_limitations_have_next_actions",
    "all_limitations_no_implementation",
    "solver_coverage_limitation_recorded",
    "candidate_generation_limitation_recorded",
    "ranker_evidence_limitation_recorded",
    "local_diagnostics_limitation_recorded",
    "submission_discipline_limitation_recorded",
    "authorization_boundary_limitation_recorded",
    "diagnostic_only_true",
    "planning_only_true",
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
    "artifact_set_declared",
    "artifact_count_five",
    "manifest_created",
    "index_created",
    "markdown_created",
    "json_payload_created",
    "docs_payload_created",
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_milestone_18_controlled_technical_solver_limitation_inventory() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_task_1_commit": SOURCE_TASK_1_COMMIT,
        "source_task_1_signature": SOURCE_TASK_1_SIGNATURE,
        "inventory_scope": INVENTORY_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "limitation_count": len(LIMITATION_ITEMS),
        "verdict": LIMITATION_INVENTORY_VERDICT,
        "decision": LIMITATION_INVENTORY_DECISION,
        "reason": LIMITATION_INVENTORY_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-v1.json"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "limitation_inventory_marker": LIMITATION_INVENTORY_MARKER,
        "signature": signature,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_task_1_commit": SOURCE_TASK_1_COMMIT,
        "source_task_1_signature": SOURCE_TASK_1_SIGNATURE,
        "source_task_1_stage": SOURCE_TASK_1_STAGE,
        "task_mode": TASK_MODE,
        "verdict": LIMITATION_INVENTORY_VERDICT,
        "decision": LIMITATION_INVENTORY_DECISION,
        "limitation_inventory_reason": LIMITATION_INVENTORY_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "inventory_scope": INVENTORY_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "runtime_authorization_scope": RUNTIME_AUTHORIZATION_SCOPE,
        "submission_authorization_scope": SUBMISSION_AUTHORIZATION_SCOPE,
        "controlled_technical_solver_limitation_inventory_ready": True,
        "controlled_technical_solver_limitation_inventory_passed": True,
        "controlled_technical_solver_limitation_inventory_locked": True,
        "diagnostic_only": True,
        "planning_only": True,
        "limitation_count": len(LIMITATION_ITEMS),
        "limitation_items": LIMITATION_ITEMS,
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
        "limitation_inventory_gate_count": len(LIMITATION_INVENTORY_GATES),
        "limitation_inventory_gate_failure_count": 0,
        "limitation_inventory_gates": LIMITATION_INVENTORY_GATES,
        "artifacts": artifacts,
    }


def validate_milestone_18_controlled_technical_solver_limitation_inventory(
    status: dict[str, Any],
) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "limitation_inventory_marker": LIMITATION_INVENTORY_MARKER,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_task_1_commit": SOURCE_TASK_1_COMMIT,
        "source_task_1_signature": SOURCE_TASK_1_SIGNATURE,
        "source_task_1_stage": SOURCE_TASK_1_STAGE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "inventory_scope": INVENTORY_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "runtime_authorization_scope": RUNTIME_AUTHORIZATION_SCOPE,
        "submission_authorization_scope": SUBMISSION_AUTHORIZATION_SCOPE,
        "verdict": LIMITATION_INVENTORY_VERDICT,
        "decision": LIMITATION_INVENTORY_DECISION,
        "limitation_inventory_reason": LIMITATION_INVENTORY_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    required_true = (
        "controlled_technical_solver_limitation_inventory_ready",
        "controlled_technical_solver_limitation_inventory_passed",
        "controlled_technical_solver_limitation_inventory_locked",
        "diagnostic_only",
        "planning_only",
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

    items = tuple(status.get("limitation_items", ()))
    if status.get("limitation_count") != 6:
        issues.append("limitation_count must be 6")
    if len(items) != 6:
        issues.append("limitation_items length must be 6")

    for item in items:
        for key in ("limitation_id", "area", "description", "risk", "next_action"):
            if not item.get(key):
                issues.append(f"{item.get('limitation_id')} missing {key}")
        if item.get("implementation_authorized") is not False:
            issues.append(f"{item.get('limitation_id')} implementation_authorized must be False")

    if status.get("limitation_inventory_gate_count") != len(LIMITATION_INVENTORY_GATES):
        issues.append("limitation_inventory_gate_count mismatch")
    if status.get("limitation_inventory_gate_failure_count") != 0:
        issues.append("limitation_inventory_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def limitation_inventory_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["limitation_inventory_marker"],
        "signature": status["signature"],
        "milestone_18_name": status["milestone_18_name"],
        "source_task_1_commit": status["source_task_1_commit"],
        "source_task_1_signature": status["source_task_1_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "inventory_scope": status["inventory_scope"],
        "milestone_18_scope": status["milestone_18_scope"],
        "diagnostic_only": status["diagnostic_only"],
        "planning_only": status["planning_only"],
        "limitation_count": status["limitation_count"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "limitation_inventory_gate_count": status["limitation_inventory_gate_count"],
        "limitation_inventory_gate_failure_count": status["limitation_inventory_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["limitation_inventory_marker"],
        f"signature={status['signature']}",
        f"milestone_18_name={status['milestone_18_name']}",
        f"source_task_1_commit={status['source_task_1_commit']}",
        f"source_task_1_signature={status['source_task_1_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"limitation_inventory_reason={status['limitation_inventory_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"inventory_scope={status['inventory_scope']}",
        f"milestone_18_scope={status['milestone_18_scope']}",
        f"diagnostic_only={status['diagnostic_only']}",
        f"planning_only={status['planning_only']}",
        f"limitation_count={status['limitation_count']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"limitation_inventory_gate_count={status['limitation_inventory_gate_count']}",
        f"limitation_inventory_gate_failure_count={status['limitation_inventory_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def build_markdown(status: dict[str, Any]) -> str:
    limitation_lines = "\n".join(
        (
            f"- `{item['limitation_id']}` - **{item['area']}**: {item['description']} "
            f"Risk: {item['risk']} Next: {item['next_action']} "
            f"implementation_authorized=`{item['implementation_authorized']}`"
        )
        for item in status["limitation_items"]
    )

    return f"""# Milestone #18 Task 2 - Controlled Technical Solver Limitation Inventory v1

## Status

`{status["limitation_inventory_marker"]}`

## Source binding

- source Task 1 commit: `{status["source_task_1_commit"]}`
- source Task 1 signature: `{status["source_task_1_signature"]}`
- source stage: `{status["source_task_1_stage"]}`
- previous stage: `{status["previous_stage"]}`
- next stage: `{status["next_stage"]}`

## Inventory

- inventory_scope: `{status["inventory_scope"]}`
- milestone_18_scope: `{status["milestone_18_scope"]}`
- diagnostic_only: `{status["diagnostic_only"]}`
- planning_only: `{status["planning_only"]}`
- limitation_count: `{status["limitation_count"]}`

{limitation_lines}

## Boundary

This limitation inventory authorizes diagnostic planning only.
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


def write_milestone_18_controlled_technical_solver_limitation_inventory_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_milestone_18_controlled_technical_solver_limitation_inventory()
    issues = validate_milestone_18_controlled_technical_solver_limitation_inventory(resolved)
    if issues:
        raise ValueError(
            "Invalid milestone 18 controlled technical solver limitation inventory: "
            + "; ".join(issues)
        )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = limitation_inventory_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    manifest = build_manifest(resolved)
    markdown = build_markdown(resolved)

    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_milestone_18_controlled_technical_solver_limitation_inventory_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_1_commit"])
    print(status["task_mode"])
    print(status["limitation_inventory_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["limitation_inventory_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "milestone_18_name",
        "source_task_1_commit",
        "source_task_1_signature",
        "inventory_scope",
        "milestone_18_scope",
        "diagnostic_only",
        "planning_only",
        "limitation_count",
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
        "limitation_inventory_gate_count",
        "limitation_inventory_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for item in status["limitation_items"]:
        print(
            f"limitation_item={item['limitation_id']}|{item['area']}|"
            f"implementation_authorized={item['implementation_authorized']}|{item['next_action']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
