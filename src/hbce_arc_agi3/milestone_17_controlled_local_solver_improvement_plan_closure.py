"""Milestone #17 Task 13 - Controlled Local Solver Improvement Plan Closure v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_13_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_CLOSURE_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

CLOSURE_STATUS_MARKER = "MILESTONE_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_CLOSURE_READY"
CLOSURE_VERDICT = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_CLOSURE_PASS_PLAN_AND_REVIEW_CLOSED"
CLOSURE_DECISION = "CLOSE_LOCAL_SOLVER_IMPROVEMENT_PLAN_AND_REVIEW_CYCLE_NO_IMPLEMENTATION_AUTHORIZED"
CLOSURE_REASON = "TASK_12_CONFIRMED_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_REVIEW_WITHOUT_IMPLEMENTATION_AUTHORIZATION"

PREVIOUS_STAGE = "MILESTONE_17_TASK_12_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_REVIEW_V1"
NEXT_STAGE = "MILESTONE_17_TASK_14_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_V1"

SOURCE_TASK_12_FINAL_BASELINE_COMMIT = "ee29733"
SOURCE_TASK_12_FINAL_SIGNATURE = "B83CF1D86F83BDE8"

PLANNING_SCOPE = "LOCAL_SOLVER_IMPROVEMENT_ONLY"
PLAN_SCOPE = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
PLAN_REVIEW_SCOPE = "REVIEW_ONLY_CONFIRM_PLAN"
CLOSURE_SCOPE = "CLOSE_PLAN_AND_REVIEW_CYCLE_ONLY"
PLAN_AUTHORIZATION_SCOPE = "PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

TASK_MODE = "MILESTONE_17_TASK_13_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_CLOSURE_V1_CLOSURE_ONLY_LOCAL_ONLY"

ARTIFACT_DIR = Path("examples/milestone-17/controlled-local-solver-improvement-plan-closure-v1")
DOC_PATH = Path("docs/milestone-17-controlled-local-solver-improvement-plan-closure-v1.md")


CLOSED_PLAN_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "plan_item_id": "M17-LSIP-1",
        "workstream_id": "M17-LSIG-WS-1",
        "name": "Baseline solver limitation inventory",
        "closure_result": "CLOSED_PLAN_CONFIRMED_NO_IMPLEMENTATION",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-2",
        "workstream_id": "M17-LSIG-WS-2",
        "name": "Local diagnostic fixture matrix",
        "closure_result": "CLOSED_PLAN_CONFIRMED_NO_IMPLEMENTATION",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-3",
        "workstream_id": "M17-LSIG-WS-3",
        "name": "Candidate generator improvement map",
        "closure_result": "CLOSED_PLAN_CONFIRMED_NO_IMPLEMENTATION",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-4",
        "workstream_id": "M17-LSIG-WS-4",
        "name": "Ranker evidence weighting plan",
        "closure_result": "CLOSED_PLAN_CONFIRMED_NO_IMPLEMENTATION",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-5",
        "workstream_id": "M17-LSIG-WS-5",
        "name": "Regression and no-score-claim measurement plan",
        "closure_result": "CLOSED_PLAN_CONFIRMED_NO_SCORE_CLAIM",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "plan_item_id": "M17-LSIP-6",
        "workstream_id": "M17-LSIG-WS-6",
        "name": "Future implementation authorization gate design",
        "closure_result": "CLOSED_PLAN_CONFIRMED_NO_AUTHORIZATION_GRANTED",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
)


CLOSURE_GATES: tuple[str, ...] = tuple(
    [
        "source_task_12_commit_bound",
        "source_task_12_signature_bound",
        "previous_stage_bound",
        "next_stage_declared",
        "planning_scope_confirmed",
        "plan_scope_confirmed",
        "plan_review_scope_confirmed",
        "closure_scope_confirmed",
        "plan_authorization_scope_plan_only",
        "implementation_authorization_scope_not_granted",
        "plan_closed",
        "review_closed",
        "closure_ready",
        "closure_passed",
        "closure_locked",
        "closed_plan_item_count_six",
        "closed_plan_item_ids_unique",
        "all_closed_items_no_implementation",
        "all_closed_items_no_runtime",
        "all_closed_items_no_submission",
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
    ]
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_controlled_local_solver_improvement_plan_closure() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_12_final_baseline_commit": SOURCE_TASK_12_FINAL_BASELINE_COMMIT,
        "source_task_12_final_signature": SOURCE_TASK_12_FINAL_SIGNATURE,
        "closure_scope": CLOSURE_SCOPE,
        "closed_plan_item_count": len(CLOSED_PLAN_ITEMS),
        "verdict": CLOSURE_VERDICT,
        "decision": CLOSURE_DECISION,
        "reason": CLOSURE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-closure-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-closure-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-closure-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-closure-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "closure_status_marker": CLOSURE_STATUS_MARKER,
        "signature": signature,
        "source_task_12_final_baseline_commit": SOURCE_TASK_12_FINAL_BASELINE_COMMIT,
        "source_task_12_final_signature": SOURCE_TASK_12_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": CLOSURE_VERDICT,
        "decision": CLOSURE_DECISION,
        "closure_reason": CLOSURE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "planning_scope": PLANNING_SCOPE,
        "plan_scope": PLAN_SCOPE,
        "plan_review_scope": PLAN_REVIEW_SCOPE,
        "closure_scope": CLOSURE_SCOPE,
        "plan_authorized": True,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "controlled_local_solver_improvement_plan_closed": True,
        "controlled_local_solver_improvement_plan_review_closed": True,
        "controlled_local_solver_improvement_plan_closure_ready": True,
        "controlled_local_solver_improvement_plan_closure_passed": True,
        "controlled_local_solver_improvement_plan_closure_locked": True,
        "plan_item_count": len(CLOSED_PLAN_ITEMS),
        "closed_plan_item_count": len(CLOSED_PLAN_ITEMS),
        "closed_plan_items": CLOSED_PLAN_ITEMS,
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
        "closure_gate_count": len(CLOSURE_GATES),
        "closure_gate_failure_count": 0,
        "closure_gates": CLOSURE_GATES,
        "artifacts": artifacts,
    }


def validate_controlled_local_solver_improvement_plan_closure(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "closure_status_marker": CLOSURE_STATUS_MARKER,
        "source_task_12_final_baseline_commit": SOURCE_TASK_12_FINAL_BASELINE_COMMIT,
        "source_task_12_final_signature": SOURCE_TASK_12_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "planning_scope": PLANNING_SCOPE,
        "plan_scope": PLAN_SCOPE,
        "plan_review_scope": PLAN_REVIEW_SCOPE,
        "closure_scope": CLOSURE_SCOPE,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "verdict": CLOSURE_VERDICT,
        "decision": CLOSURE_DECISION,
        "closure_reason": CLOSURE_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    items = tuple(status.get("closed_plan_items", ()))
    item_ids = [item.get("plan_item_id") for item in items]

    if status.get("plan_item_count") != 6:
        issues.append("plan_item_count must be 6")
    if status.get("closed_plan_item_count") != 6:
        issues.append("closed_plan_item_count must be 6")
    if len(items) != 6:
        issues.append("closed_plan_items length must be 6")
    if len(item_ids) != len(set(item_ids)):
        issues.append("closed plan item IDs must be unique")

    for item in items:
        if not str(item.get("closure_result", "")).startswith("CLOSED_PLAN_CONFIRMED"):
            issues.append(f"{item.get('plan_item_id')} closure_result must confirm closure")
        if item.get("implementation_allowed") is not False:
            issues.append(f"{item.get('plan_item_id')} implementation_allowed must be False")
        if item.get("runtime_allowed") is not False:
            issues.append(f"{item.get('plan_item_id')} runtime_allowed must be False")
        if item.get("submission_allowed") is not False:
            issues.append(f"{item.get('plan_item_id')} submission_allowed must be False")

    required_true = (
        "plan_authorized",
        "controlled_local_solver_improvement_plan_closed",
        "controlled_local_solver_improvement_plan_review_closed",
        "controlled_local_solver_improvement_plan_closure_ready",
        "controlled_local_solver_improvement_plan_closure_passed",
        "controlled_local_solver_improvement_plan_closure_locked",
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

    if status.get("closure_gate_count") != len(CLOSURE_GATES):
        issues.append("closure_gate_count mismatch")
    if status.get("closure_gate_failure_count") != 0:
        issues.append("closure_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def closure_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["closure_status_marker"],
        "signature": status["signature"],
        "source_task_12_final_baseline_commit": status["source_task_12_final_baseline_commit"],
        "source_task_12_final_signature": status["source_task_12_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "closure_scope": status["closure_scope"],
        "closed_plan_item_count": status["closed_plan_item_count"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "competitive_score_claim_allowed": status["competitive_score_claim_allowed"],
        "official_score_claim_allowed": status["official_score_claim_allowed"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "closure_gate_count": status["closure_gate_count"],
        "closure_gate_failure_count": status["closure_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    item_lines = "\n".join(
        f"- `{item['plan_item_id']}` / `{item['workstream_id']}` — {item['name']} · `{item['closure_result']}`"
        for item in status["closed_plan_items"]
    )

    return f"""# Milestone #17 Task 13 - Controlled Local Solver Improvement Plan Closure v1

## Status

`{status["closure_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 12 final baseline commit: `{status["source_task_12_final_baseline_commit"]}`
- source Task 12 final signature: `{status["source_task_12_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Closure

- planning_scope: `{status["planning_scope"]}`
- plan_scope: `{status["plan_scope"]}`
- plan_review_scope: `{status["plan_review_scope"]}`
- closure_scope: `{status["closure_scope"]}`
- closed_plan_item_count: `{status["closed_plan_item_count"]}`

{item_lines}

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Boundary

- implementation_authorized: `{status["implementation_authorized"]}`
- implementation_blocked: `{status["implementation_blocked"]}`
- runtime_execution_allowed: `{status["runtime_execution_allowed"]}`
- real_evaluation_allowed: `{status["real_evaluation_allowed"]}`
- real_submission_allowed: `{status["real_submission_allowed"]}`
- kaggle_submission_sent: `{status["kaggle_submission_sent"]}`
- competitive_score_claim_allowed: `{status["competitive_score_claim_allowed"]}`
- official_score_claim_allowed: `{status["official_score_claim_allowed"]}`
- private_core_exposure: `{status["private_core_exposure"]}`
- legal_certification: `{status["legal_certification"]}`
- fail_closed_active: `{status["fail_closed_active"]}`

## Validation

- closure_gate_count: `{status["closure_gate_count"]}`
- closure_gate_failure_count: `{status["closure_gate_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["closure_status_marker"],
        f"signature={status['signature']}",
        f"source_task_12_final_baseline_commit={status['source_task_12_final_baseline_commit']}",
        f"source_task_12_final_signature={status['source_task_12_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"closure_reason={status['closure_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"closure_scope={status['closure_scope']}",
        f"closed_plan_item_count={status['closed_plan_item_count']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"official_score_claim_allowed={status['official_score_claim_allowed']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"closure_gate_count={status['closure_gate_count']}",
        f"closure_gate_failure_count={status['closure_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_controlled_local_solver_improvement_plan_closure_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_local_solver_improvement_plan_closure()
    issues = validate_controlled_local_solver_improvement_plan_closure(resolved)
    if issues:
        raise ValueError("Invalid controlled local solver improvement plan closure: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = closure_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-closure-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-closure-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-closure-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-plan-closure-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_local_solver_improvement_plan_closure_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_12_final_baseline_commit"])
    print(status["task_mode"])
    print(status["closure_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["closure_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_12_final_baseline_commit",
        "source_task_12_final_signature",
        "planning_scope",
        "plan_scope",
        "plan_review_scope",
        "closure_scope",
        "plan_authorized",
        "plan_authorization_scope",
        "implementation_authorization_scope",
        "controlled_local_solver_improvement_plan_closed",
        "controlled_local_solver_improvement_plan_review_closed",
        "controlled_local_solver_improvement_plan_closure_ready",
        "controlled_local_solver_improvement_plan_closure_passed",
        "controlled_local_solver_improvement_plan_closure_locked",
        "plan_item_count",
        "closed_plan_item_count",
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
        "closure_gate_count",
        "closure_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for item in status["closed_plan_items"]:
        print(
            f"closed_plan_item={item['plan_item_id']}|{item['workstream_id']}|"
            f"{item['closure_result']}|{item['name']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
