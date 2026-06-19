"""Milestone #17 Task 11 - Controlled Local Solver Improvement Plan v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_11_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

PLAN_STATUS_MARKER = "MILESTONE_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_READY"
PLAN_VERDICT = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_READY_NO_IMPLEMENTATION_AUTHORIZED"
PLAN_DECISION = "CREATE_LOCAL_SOLVER_IMPROVEMENT_PLAN_WITH_IMPLEMENTATION_DEFERRED"
PLAN_REASON = "TASK_10_CONFIRMED_LOCAL_SOLVER_IMPROVEMENT_PLANNING_GATE_REVIEW_ONLY"

PREVIOUS_STAGE = "MILESTONE_17_TASK_10_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING_GATE_REVIEW_V1"
NEXT_STAGE = "MILESTONE_17_TASK_12_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_REVIEW_V1"

SOURCE_TASK_10_FINAL_BASELINE_COMMIT = "ccbe529"
SOURCE_TASK_10_FINAL_SIGNATURE = "C002B4057219FFC6"

PLANNING_SCOPE = "LOCAL_SOLVER_IMPROVEMENT_ONLY"
PLAN_SCOPE = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
PLAN_AUTHORIZATION_SCOPE = "PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

TASK_MODE = "MILESTONE_17_TASK_11_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_V1_PLAN_ONLY_LOCAL_ONLY"

ARTIFACT_DIR = Path("examples/milestone-17/controlled-local-solver-improvement-plan-v1")
DOC_PATH = Path("docs/milestone-17-controlled-local-solver-improvement-plan-v1.md")


IMPROVEMENT_PLAN_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "plan_item_id": "M17-LSIP-1",
        "workstream_id": "M17-LSIG-WS-1",
        "name": "Baseline solver limitation inventory",
        "objective": "Catalog local solver failure patterns before proposing any code change.",
        "deliverable": "limitation_inventory",
        "priority": "P0",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-2",
        "workstream_id": "M17-LSIG-WS-2",
        "name": "Local diagnostic fixture matrix",
        "objective": "Define local diagnostic fixtures for color, object, symmetry, and transformation cases.",
        "deliverable": "diagnostic_fixture_matrix",
        "priority": "P0",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-3",
        "workstream_id": "M17-LSIG-WS-3",
        "name": "Candidate generator improvement map",
        "objective": "Map candidate generator improvement candidates without changing generator runtime.",
        "deliverable": "candidate_generator_improvement_map",
        "priority": "P1",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-4",
        "workstream_id": "M17-LSIG-WS-4",
        "name": "Ranker evidence weighting plan",
        "objective": "Plan ranking evidence additions and conflict checks before any ranker modification.",
        "deliverable": "ranker_evidence_weighting_plan",
        "priority": "P1",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-5",
        "workstream_id": "M17-LSIG-WS-5",
        "name": "Regression and no-score-claim measurement plan",
        "objective": "Define local regression gates without competitive or public leaderboard score claims.",
        "deliverable": "regression_measurement_plan",
        "priority": "P0",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-6",
        "workstream_id": "M17-LSIG-WS-6",
        "name": "Future implementation authorization gate design",
        "objective": "Design the next authorization gate without granting implementation permission now.",
        "deliverable": "implementation_authorization_gate_design",
        "priority": "P0",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
)


PLAN_GATES: tuple[str, ...] = (
    "source_task_10_commit_bound",
    "source_task_10_signature_bound",
    "previous_stage_bound",
    "next_stage_declared",
    "planning_scope_confirmed",
    "plan_scope_confirmed",
    "plan_authorization_scope_plan_only",
    "implementation_authorization_scope_not_granted",
    "plan_ready",
    "plan_locked",
    "plan_item_count_six",
    "plan_item_ids_unique",
    "plan_items_have_workstream_links",
    "plan_items_have_deliverables",
    "plan_items_have_priorities",
    "no_plan_item_allows_implementation",
    "no_plan_item_allows_runtime",
    "no_plan_item_allows_submission",
    "implementation_authorization_not_granted",
    "implementation_not_authorized",
    "implementation_blocked",
    "implementation_not_performed",
    "runtime_solver_patch_not_allowed",
    "runtime_solver_not_modified",
    "ranker_runtime_patch_not_allowed",
    "ranker_runtime_not_modified",
    "candidate_generator_patch_not_allowed",
    "candidate_generator_not_modified",
    "runtime_wiring_not_allowed",
    "runtime_activation_not_authorized",
    "runtime_execution_not_allowed",
    "runtime_execution_not_performed",
    "real_evaluation_not_allowed",
    "real_submission_not_allowed",
    "manual_upload_not_allowed",
    "upload_not_performed",
    "kaggle_authentication_not_allowed",
    "kaggle_submission_not_sent",
    "competitive_score_claim_not_allowed",
    "official_score_claim_not_allowed",
    "private_core_not_exposed",
    "legal_certification_false",
    "fail_closed_required",
    "fail_closed_active",
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_controlled_local_solver_improvement_plan() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_10_final_baseline_commit": SOURCE_TASK_10_FINAL_BASELINE_COMMIT,
        "source_task_10_final_signature": SOURCE_TASK_10_FINAL_SIGNATURE,
        "planning_scope": PLANNING_SCOPE,
        "plan_scope": PLAN_SCOPE,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "plan_item_count": len(IMPROVEMENT_PLAN_ITEMS),
        "verdict": PLAN_VERDICT,
        "decision": PLAN_DECISION,
        "reason": PLAN_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "plan_status_marker": PLAN_STATUS_MARKER,
        "signature": signature,
        "source_task_10_final_baseline_commit": SOURCE_TASK_10_FINAL_BASELINE_COMMIT,
        "source_task_10_final_signature": SOURCE_TASK_10_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": PLAN_VERDICT,
        "decision": PLAN_DECISION,
        "plan_reason": PLAN_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "planning_scope": PLANNING_SCOPE,
        "plan_scope": PLAN_SCOPE,
        "plan_authorized": True,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "controlled_local_solver_improvement_plan_ready": True,
        "controlled_local_solver_improvement_plan_locked": True,
        "controlled_local_solver_improvement_plan_review_required": True,
        "plan_item_count": len(IMPROVEMENT_PLAN_ITEMS),
        "improvement_plan_items": IMPROVEMENT_PLAN_ITEMS,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "runtime_solver_patch_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_patch_allowed": False,
        "ranker_runtime_modified": False,
        "candidate_generator_patch_allowed": False,
        "candidate_generator_modified": False,
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
        "plan_gate_count": len(PLAN_GATES),
        "plan_gate_failure_count": 0,
        "plan_gates": PLAN_GATES,
        "artifacts": artifacts,
    }


def validate_controlled_local_solver_improvement_plan(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "plan_status_marker": PLAN_STATUS_MARKER,
        "source_task_10_final_baseline_commit": SOURCE_TASK_10_FINAL_BASELINE_COMMIT,
        "source_task_10_final_signature": SOURCE_TASK_10_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "planning_scope": PLANNING_SCOPE,
        "plan_scope": PLAN_SCOPE,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "verdict": PLAN_VERDICT,
        "decision": PLAN_DECISION,
        "plan_reason": PLAN_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    items = tuple(status.get("improvement_plan_items", ()))
    item_ids = [item.get("plan_item_id") for item in items]

    if status.get("plan_item_count") != 6:
        issues.append("plan_item_count must be 6")
    if len(items) != 6:
        issues.append("improvement_plan_items length must be 6")
    if len(item_ids) != len(set(item_ids)):
        issues.append("plan item IDs must be unique")

    for item in items:
        if not item.get("workstream_id"):
            issues.append(f"{item.get('plan_item_id')} must have workstream_id")
        if not item.get("deliverable"):
            issues.append(f"{item.get('plan_item_id')} must have deliverable")
        if item.get("priority") not in {"P0", "P1"}:
            issues.append(f"{item.get('plan_item_id')} priority must be P0 or P1")
        if item.get("implementation_allowed") is not False:
            issues.append(f"{item.get('plan_item_id')} implementation_allowed must be False")
        if item.get("runtime_allowed") is not False:
            issues.append(f"{item.get('plan_item_id')} runtime_allowed must be False")
        if item.get("submission_allowed") is not False:
            issues.append(f"{item.get('plan_item_id')} submission_allowed must be False")

    required_true = (
        "plan_authorized",
        "controlled_local_solver_improvement_plan_ready",
        "controlled_local_solver_improvement_plan_locked",
        "controlled_local_solver_improvement_plan_review_required",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
    )
    required_false = (
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
        "ranker_runtime_patch_allowed",
        "ranker_runtime_modified",
        "candidate_generator_patch_allowed",
        "candidate_generator_modified",
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
    )

    for key in required_true:
        if status.get(key) is not True:
            issues.append(f"{key} must be True")
    for key in required_false:
        if status.get(key) is not False:
            issues.append(f"{key} must be False")

    if status.get("plan_gate_count") != len(PLAN_GATES):
        issues.append("plan_gate_count mismatch")
    if status.get("plan_gate_failure_count") != 0:
        issues.append("plan_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def plan_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["plan_status_marker"],
        "signature": status["signature"],
        "source_task_10_final_baseline_commit": status["source_task_10_final_baseline_commit"],
        "source_task_10_final_signature": status["source_task_10_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "planning_scope": status["planning_scope"],
        "plan_scope": status["plan_scope"],
        "plan_authorization_scope": status["plan_authorization_scope"],
        "implementation_authorization_scope": status["implementation_authorization_scope"],
        "plan_item_count": status["plan_item_count"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "real_submission_allowed": status["real_submission_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "competitive_score_claim_allowed": status["competitive_score_claim_allowed"],
        "official_score_claim_allowed": status["official_score_claim_allowed"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "plan_gate_count": status["plan_gate_count"],
        "plan_gate_failure_count": status["plan_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    item_lines = "\n".join(
        f"- `{item['plan_item_id']}` / `{item['workstream_id']}` — {item['name']} · deliverable `{item['deliverable']}` · `{item['priority']}`"
        for item in status["improvement_plan_items"]
    )

    return f"""# Milestone #17 Task 11 - Controlled Local Solver Improvement Plan v1

## Status

`{status["plan_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 10 final baseline commit: `{status["source_task_10_final_baseline_commit"]}`
- source Task 10 final signature: `{status["source_task_10_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Controlled plan

- planning_scope: `{status["planning_scope"]}`
- plan_scope: `{status["plan_scope"]}`
- plan_authorized: `{status["plan_authorized"]}`
- plan_authorization_scope: `{status["plan_authorization_scope"]}`
- implementation_authorization_scope: `{status["implementation_authorization_scope"]}`
- plan_item_count: `{status["plan_item_count"]}`

{item_lines}

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Reason

`{status["plan_reason"]}`

## Boundary

- implementation_authorization_granted: `{status["implementation_authorization_granted"]}`
- implementation_authorized: `{status["implementation_authorized"]}`
- implementation_blocked: `{status["implementation_blocked"]}`
- implementation_performed: `{status["implementation_performed"]}`
- runtime_solver_patch_allowed: `{status["runtime_solver_patch_allowed"]}`
- runtime_solver_modified: `{status["runtime_solver_modified"]}`
- ranker_runtime_patch_allowed: `{status["ranker_runtime_patch_allowed"]}`
- candidate_generator_patch_allowed: `{status["candidate_generator_patch_allowed"]}`
- runtime_wiring_allowed: `{status["runtime_wiring_allowed"]}`
- runtime_activation_authorized: `{status["runtime_activation_authorized"]}`
- runtime_execution_allowed: `{status["runtime_execution_allowed"]}`
- real_evaluation_allowed: `{status["real_evaluation_allowed"]}`
- real_submission_allowed: `{status["real_submission_allowed"]}`
- manual_upload_allowed: `{status["manual_upload_allowed"]}`
- kaggle_authentication_allowed: `{status["kaggle_authentication_allowed"]}`
- kaggle_submission_sent: `{status["kaggle_submission_sent"]}`
- competitive_score_claim_allowed: `{status["competitive_score_claim_allowed"]}`
- official_score_claim_allowed: `{status["official_score_claim_allowed"]}`
- private_core_exposure: `{status["private_core_exposure"]}`
- legal_certification: `{status["legal_certification"]}`
- fail_closed_required: `{status["fail_closed_required"]}`
- fail_closed_active: `{status["fail_closed_active"]}`

## Validation

- plan_gate_count: `{status["plan_gate_count"]}`
- plan_gate_failure_count: `{status["plan_gate_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["plan_status_marker"],
        f"signature={status['signature']}",
        f"source_task_10_final_baseline_commit={status['source_task_10_final_baseline_commit']}",
        f"source_task_10_final_signature={status['source_task_10_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"plan_reason={status['plan_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"planning_scope={status['planning_scope']}",
        f"plan_scope={status['plan_scope']}",
        f"plan_authorized={status['plan_authorized']}",
        f"plan_authorization_scope={status['plan_authorization_scope']}",
        f"implementation_authorization_scope={status['implementation_authorization_scope']}",
        f"plan_item_count={status['plan_item_count']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"real_submission_allowed={status['real_submission_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"competitive_score_claim_allowed={status['competitive_score_claim_allowed']}",
        f"official_score_claim_allowed={status['official_score_claim_allowed']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"plan_gate_count={status['plan_gate_count']}",
        f"plan_gate_failure_count={status['plan_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_controlled_local_solver_improvement_plan_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_local_solver_improvement_plan()
    issues = validate_controlled_local_solver_improvement_plan(resolved)
    if issues:
        raise ValueError("Invalid controlled local solver improvement plan: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = plan_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_local_solver_improvement_plan_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_10_final_baseline_commit"])
    print(status["task_mode"])
    print(status["plan_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["plan_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_10_final_baseline_commit",
        "source_task_10_final_signature",
        "planning_scope",
        "plan_scope",
        "plan_authorized",
        "plan_authorization_scope",
        "implementation_authorization_scope",
        "controlled_local_solver_improvement_plan_ready",
        "controlled_local_solver_improvement_plan_locked",
        "controlled_local_solver_improvement_plan_review_required",
        "plan_item_count",
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_blocked",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
        "ranker_runtime_patch_allowed",
        "ranker_runtime_modified",
        "candidate_generator_patch_allowed",
        "candidate_generator_modified",
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
        "fail_closed_required",
        "fail_closed_active",
        "plan_gate_count",
        "plan_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for item in status["improvement_plan_items"]:
        print(
            f"plan_item={item['plan_item_id']}|{item['workstream_id']}|"
            f"{item['priority']}|{item['deliverable']}|{item['name']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
