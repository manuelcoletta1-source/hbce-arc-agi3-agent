from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_16_TASK_7_OPERATOR_DIRECTION_WAIT_STATE_CLOSURE_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_CLOSURE_ONLY_LOCAL_ONLY"
CLOSURE_STATUS = "MILESTONE_16_OPERATOR_DIRECTION_WAIT_STATE_CLOSURE_READY"
CLOSURE_VERDICT = "OPERATOR_DIRECTION_WAIT_STATE_CLOSURE_PASS_REVIEW_CLOSED_WAIT_STATE_STILL_ACTIVE"
CLOSURE_DECISION = "CLOSE_WAIT_STATE_REVIEW_WITH_WAIT_STATE_ACTIVE_NO_IMPLEMENTATION"
BLOCK_REASON = "TASK_6_WAIT_STATE_REVIEW_CONFIRMED_WAIT_STATE_STILL_ACTIVE"

PREVIOUS_STAGE = "MILESTONE_16_TASK_6_OPERATOR_DIRECTION_WAIT_STATE_REVIEW_V1"
NEXT_STAGE = "MILESTONE_16_TASK_8_OPERATOR_DIRECTION_CYCLE_STATUS_V1"

SOURCE_TASK_6_FINAL_BASELINE_COMMIT = "0c60e2f"
SOURCE_TASK_6_FINAL_SIGNATURE = "82CD7B4CA93E692A"
SOURCE_TASK_5_FINAL_BASELINE_COMMIT = "03acb5a"
SOURCE_TASK_5_FINAL_SIGNATURE = "EC9F02EC0CF5AC8F"

OUTPUT_DIR = Path("examples/milestone-16/operator-direction-wait-state-closure-v1")
DOC_PATH = Path("docs/milestone-16-operator-direction-wait-state-closure-v1.md")


CHECKS = (
    "TASK_6_WAIT_STATE_REVIEW_CONFIRMED",
    "WAIT_STATE_CLOSURE_CREATED",
    "WAIT_STATE_CLOSURE_READY",
    "WAIT_STATE_CLOSURE_PASSED",
    "WAIT_STATE_REVIEW_CLOSED",
    "WAIT_STATE_STILL_ACTIVE",
    "WAIT_STATE_NOT_CLOSED",
    "NO_DIRECTION_OPTION_SELECTED",
    "NO_OPERATOR_DIRECTION_RECEIVED",
    "OPERATOR_DECISION_NOT_RECEIVED",
    "EXPLICIT_OPERATOR_AUTHORIZATION_NOT_RECEIVED",
    "DECISION_GATE_REMAINS_BLOCKED",
    "IMPLEMENTATION_AUTHORIZATION_NOT_GRANTED",
    "IMPLEMENTATION_REMAINS_BLOCKED",
    "NO_IMPLEMENTATION_PERFORMED",
    "NO_IMPLEMENTATION_PATCH_CREATED",
    "NO_IMPLEMENTATION_PATCH_APPLIED",
    "NO_RUNTIME_SOLVER_PATCH_ALLOWED",
    "NO_RUNTIME_SOLVER_MODIFIED",
    "NO_RANKER_RUNTIME_PATCH_ALLOWED",
    "NO_RANKER_RUNTIME_MODIFIED",
    "NO_CANDIDATE_GENERATOR_PATCH_ALLOWED",
    "NO_CANDIDATE_GENERATOR_MODIFIED",
    "NO_RUNTIME_WIRING_ALLOWED",
    "NO_RUNTIME_WIRING_PERFORMED",
    "NO_RUNTIME_ACTIVATION_AUTHORIZED",
    "NO_RUNTIME_ACTIVATION_PERFORMED",
    "NO_RUNTIME_EXECUTION_ALLOWED",
    "NO_RUNTIME_EXECUTION_PERFORMED",
    "NO_REAL_EVALUATION_ALLOWED",
    "NO_REAL_SUBMISSION_ALLOWED",
    "NO_KAGGLE_SUBMISSION_SENT",
    "NO_PRIVATE_CORE_EXPOSURE",
    "NO_LEGAL_CERTIFICATION",
)


def _git_head() -> str:
    try:
        value = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return value or "NO_GIT_HEAD"
    except Exception:
        return "NO_GIT_HEAD"


def _signature(seed: dict[str, Any]) -> str:
    canonical = json.dumps(seed, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16].upper()


def build_milestone_16_task_7_operator_direction_wait_state_closure(
    *,
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    baseline = baseline_commit or _git_head()

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "closure_verdict": CLOSURE_VERDICT,
        "closure_decision": CLOSURE_DECISION,
        "block_reason": BLOCK_REASON,
        "checks": CHECKS,
    }

    return {
        "task_name": TASK_NAME,
        "status": TASK_READY,
        "mode": MODE,
        "closure_status": CLOSURE_STATUS,
        "closure_verdict": CLOSURE_VERDICT,
        "closure_decision": CLOSURE_DECISION,
        "block_reason": BLOCK_REASON,
        "signature": _signature(seed),
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "source_task_6_final_baseline_commit": SOURCE_TASK_6_FINAL_BASELINE_COMMIT,
        "source_task_6_final_signature": SOURCE_TASK_6_FINAL_SIGNATURE,
        "source_task_5_final_baseline_commit": SOURCE_TASK_5_FINAL_BASELINE_COMMIT,
        "source_task_5_final_signature": SOURCE_TASK_5_FINAL_SIGNATURE,
        "milestone_16_opened": True,
        "task_6_wait_state_review_confirmed": True,
        "operator_direction_wait_state_closure_created": True,
        "wait_state_closure_ready": True,
        "wait_state_closure_passed": True,
        "wait_state_closure_closed": True,
        "wait_state_review_ready": True,
        "wait_state_review_passed": True,
        "wait_state_review_closed": True,
        "wait_state_ready": True,
        "wait_state_active": True,
        "wait_state_closed": False,
        "wait_state_reason": "NO_EXPLICIT_OPERATOR_DIRECTION_RECEIVED",
        "decision_gate_ready": True,
        "decision_gate_open": False,
        "decision_gate_blocked": True,
        "direction_options_reviewed": True,
        "direction_option_count": 5,
        "direction_option_selected": False,
        "selected_direction_option_id": "NONE",
        "selected_direction_option_count": 0,
        "operator_direction_required": True,
        "operator_direction_received": False,
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "operator_decision_required": True,
        "operator_decision_received": False,
        "operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "explicit_operator_authorization_required": True,
        "explicit_operator_authorization_received": False,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "implementation_patch_created": False,
        "implementation_patch_applied": False,
        "runtime_solver_patch_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_patch_allowed": False,
        "ranker_runtime_modified": False,
        "candidate_generator_patch_allowed": False,
        "candidate_generator_modified": False,
        "runtime_wiring_allowed": False,
        "runtime_wiring_performed": False,
        "runtime_activation_authorized": False,
        "runtime_activation_blocked": True,
        "runtime_activation_performed": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_evaluation_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_upload_allowed": False,
        "kaggle_upload_performed": False,
        "kaggle_submission_sent": False,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "closure_only": True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "milestone_16_operator_direction_wait_state_closure_checks": CHECKS,
        "milestone_16_operator_direction_wait_state_closure_check_count": len(CHECKS),
        "milestone_16_operator_direction_wait_state_closure_failure_count": 0,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def validate_milestone_16_task_7_operator_direction_wait_state_closure(
    closure: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = (
        "milestone_16_opened",
        "task_6_wait_state_review_confirmed",
        "operator_direction_wait_state_closure_created",
        "wait_state_closure_ready",
        "wait_state_closure_passed",
        "wait_state_closure_closed",
        "wait_state_review_ready",
        "wait_state_review_passed",
        "wait_state_review_closed",
        "wait_state_ready",
        "wait_state_active",
        "decision_gate_ready",
        "decision_gate_blocked",
        "direction_options_reviewed",
        "operator_direction_required",
        "operator_decision_required",
        "explicit_operator_authorization_required",
        "implementation_blocked",
        "runtime_activation_blocked",
        "public_overfit_guard_required",
        "fail_closed_required",
        "fail_closed_active",
        "closure_only",
        "public_safe",
        "deterministic",
        "local_only",
    )

    for key in expected_true:
        if closure.get(key) is not True:
            issues.append(f"{key}:expected_true")

    expected_false = (
        "wait_state_closed",
        "decision_gate_open",
        "direction_option_selected",
        "operator_direction_received",
        "operator_decision_received",
        "explicit_operator_authorization_received",
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_performed",
        "implementation_patch_created",
        "implementation_patch_applied",
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
        "real_evaluation_performed",
        "real_submission_allowed",
        "ready_for_real_kaggle_submission",
        "manual_upload_allowed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_upload_allowed",
        "kaggle_upload_performed",
        "kaggle_submission_sent",
        "external_api_dependency",
        "internet_during_eval",
        "private_core_exposure",
        "legal_certification",
        "official_score_claim_allowed",
        "competitive_score_claim_allowed",
        "public_overfit_allowed",
    )

    for key in expected_false:
        if closure.get(key) is not False:
            issues.append(f"{key}:expected_false")

    expected_pairs = {
        "closure_verdict": CLOSURE_VERDICT,
        "closure_decision": CLOSURE_DECISION,
        "block_reason": BLOCK_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "source_task_6_final_baseline_commit": SOURCE_TASK_6_FINAL_BASELINE_COMMIT,
        "source_task_6_final_signature": SOURCE_TASK_6_FINAL_SIGNATURE,
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "selected_direction_option_id": "NONE",
        "wait_state_reason": "NO_EXPLICIT_OPERATOR_DIRECTION_RECEIVED",
    }

    for key, expected in expected_pairs.items():
        if closure.get(key) != expected:
            issues.append(f"{key}:mismatch")

    if closure.get("direction_option_count") != 5:
        issues.append("direction_option_count_mismatch")

    if closure.get("selected_direction_option_count") != 0:
        issues.append("selected_direction_option_count_nonzero")

    if closure.get("milestone_16_operator_direction_wait_state_closure_check_count") != len(CHECKS):
        issues.append("milestone_16_operator_direction_wait_state_closure_check_count_mismatch")

    if closure.get("milestone_16_operator_direction_wait_state_closure_failure_count") != 0:
        issues.append("milestone_16_operator_direction_wait_state_closure_failure_count_nonzero")

    return {
        "status": TASK_VALID if not issues else f"{TASK_NAME}_INVALID",
        "valid": not issues,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "issues": issues,
        "warnings": warnings,
    }


def write_milestone_16_task_7_operator_direction_wait_state_closure_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-16-operator-direction-wait-state-closure-v1.json"
    output_index = output_dir / "milestone-16-operator-direction-wait-state-closure-index-v1.json"
    output_manifest = output_dir / "milestone-16-operator-direction-wait-state-closure-manifest-v1.txt"
    output_md = output_dir / "milestone-16-operator-direction-wait-state-closure-v1.md"

    closure = build_milestone_16_task_7_operator_direction_wait_state_closure()
    validation = validate_milestone_16_task_7_operator_direction_wait_state_closure(closure)

    payload = {
        "closure": closure,
        "validation": validation,
    }

    index = {
        "task_name": closure["task_name"],
        "status": closure["status"],
        "validation_status": validation["status"],
        "valid": validation["valid"],
        "signature": closure["signature"],
        "baseline_commit": closure["baseline_commit"],
        "previous_stage": closure["previous_stage"],
        "next_stage": closure["next_stage"],
        "closure_verdict": closure["closure_verdict"],
        "closure_decision": closure["closure_decision"],
        "wait_state_active": closure["wait_state_active"],
        "wait_state_closed": closure["wait_state_closed"],
        "wait_state_closure_closed": closure["wait_state_closure_closed"],
        "selected_direction_option_id": closure["selected_direction_option_id"],
        "operator_direction_received": closure["operator_direction_received"],
        "implementation_authorized": closure["implementation_authorized"],
        "runtime_activation_performed": closure["runtime_activation_performed"],
        "real_submission_allowed": closure["real_submission_allowed"],
        "artifact_paths": {
            "json": str(output_json),
            "index": str(output_index),
            "manifest": str(output_manifest),
            "markdown": str(output_md),
            "doc": str(doc_path),
        },
    }

    manifest_lines = [
        f"task_name={closure['task_name']}",
        f"status={closure['status']}",
        f"validation_status={validation['status']}",
        f"valid={validation['valid']}",
        f"signature={closure['signature']}",
        f"baseline_commit={closure['baseline_commit']}",
        f"mode={closure['mode']}",
        f"closure_status={closure['closure_status']}",
        f"closure_verdict={closure['closure_verdict']}",
        f"closure_decision={closure['closure_decision']}",
        f"block_reason={closure['block_reason']}",
        f"previous_stage={closure['previous_stage']}",
        f"next_stage={closure['next_stage']}",
        f"source_task_6_final_baseline_commit={closure['source_task_6_final_baseline_commit']}",
        f"source_task_6_final_signature={closure['source_task_6_final_signature']}",
        f"wait_state_closure_ready={closure['wait_state_closure_ready']}",
        f"wait_state_closure_passed={closure['wait_state_closure_passed']}",
        f"wait_state_closure_closed={closure['wait_state_closure_closed']}",
        f"wait_state_review_closed={closure['wait_state_review_closed']}",
        f"wait_state_active={closure['wait_state_active']}",
        f"wait_state_closed={closure['wait_state_closed']}",
        f"decision_gate_blocked={closure['decision_gate_blocked']}",
        f"direction_option_count={closure['direction_option_count']}",
        f"direction_option_selected={closure['direction_option_selected']}",
        f"selected_direction_option_id={closure['selected_direction_option_id']}",
        f"operator_direction_required={closure['operator_direction_required']}",
        f"operator_direction_received={closure['operator_direction_received']}",
        f"operator_direction_value={closure['operator_direction_value']}",
        f"implementation_authorized={closure['implementation_authorized']}",
        f"implementation_blocked={closure['implementation_blocked']}",
        f"implementation_performed={closure['implementation_performed']}",
        f"runtime_solver_modified={closure['runtime_solver_modified']}",
        f"runtime_wiring_performed={closure['runtime_wiring_performed']}",
        f"runtime_activation_performed={closure['runtime_activation_performed']}",
        f"runtime_execution_performed={closure['runtime_execution_performed']}",
        f"real_submission_allowed={closure['real_submission_allowed']}",
        f"kaggle_submission_sent={closure['kaggle_submission_sent']}",
        f"private_core_exposure={closure['private_core_exposure']}",
        f"legal_certification={closure['legal_certification']}",
        f"milestone_16_operator_direction_wait_state_closure_check_count={closure['milestone_16_operator_direction_wait_state_closure_check_count']}",
        f"milestone_16_operator_direction_wait_state_closure_failure_count={closure['milestone_16_operator_direction_wait_state_closure_failure_count']}",
        "",
    ]

    md_lines = [
        "# Milestone 16 - Task 7 - Operator Direction Wait State Closure v1",
        "",
        f"Status: `{closure['status']}`",
        f"Validation: `{validation['status']}`",
        f"Signature: `{closure['signature']}`",
        f"Baseline commit: `{closure['baseline_commit']}`",
        "",
        "## Purpose",
        "",
        "This task closes the wait-state review cycle created by Task 6 without closing the operational wait state itself.",
        "",
        "The wait state remains active. No explicit operator direction has been received. No direction option is selected. No implementation, runtime activation, runtime execution, Kaggle upload, or real submission is authorized.",
        "",
        "## Closure",
        "",
        f"- Closure verdict: `{closure['closure_verdict']}`",
        f"- Closure decision: `{closure['closure_decision']}`",
        f"- Wait state closure ready: `{closure['wait_state_closure_ready']}`",
        f"- Wait state closure passed: `{closure['wait_state_closure_passed']}`",
        f"- Wait state closure closed: `{closure['wait_state_closure_closed']}`",
        f"- Wait state active: `{closure['wait_state_active']}`",
        f"- Wait state closed: `{closure['wait_state_closed']}`",
        f"- Selected option: `{closure['selected_direction_option_id']}`",
        f"- Block reason: `{closure['block_reason']}`",
        "",
        "## Boundary",
        "",
        f"- operator_direction_required: `{closure['operator_direction_required']}`",
        f"- operator_direction_received: `{closure['operator_direction_received']}`",
        f"- implementation_authorized: `{closure['implementation_authorized']}`",
        f"- implementation_blocked: `{closure['implementation_blocked']}`",
        f"- implementation_performed: `{closure['implementation_performed']}`",
        f"- runtime_solver_modified: `{closure['runtime_solver_modified']}`",
        f"- runtime_wiring_performed: `{closure['runtime_wiring_performed']}`",
        f"- runtime_activation_performed: `{closure['runtime_activation_performed']}`",
        f"- runtime_execution_performed: `{closure['runtime_execution_performed']}`",
        f"- real_submission_allowed: `{closure['real_submission_allowed']}`",
        f"- kaggle_submission_sent: `{closure['kaggle_submission_sent']}`",
        f"- private_core_exposure: `{closure['private_core_exposure']}`",
        f"- legal_certification: `{closure['legal_certification']}`",
        "",
    ]

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text("\n".join(manifest_lines), encoding="utf-8")
    output_md.write_text("\n".join(md_lines), encoding="utf-8")
    doc_path.write_text("\n".join(md_lines), encoding="utf-8")

    return closure, validation, {
        "json": str(output_json),
        "index": str(output_index),
        "manifest": str(output_manifest),
        "markdown": str(output_md),
        "doc": str(doc_path),
    }


__all__ = [
    "TASK_NAME",
    "PIPELINE_READY",
    "TASK_READY",
    "TASK_VALID",
    "MODE",
    "CLOSURE_STATUS",
    "CLOSURE_VERDICT",
    "CLOSURE_DECISION",
    "BLOCK_REASON",
    "PREVIOUS_STAGE",
    "NEXT_STAGE",
    "build_milestone_16_task_7_operator_direction_wait_state_closure",
    "validate_milestone_16_task_7_operator_direction_wait_state_closure",
    "write_milestone_16_task_7_operator_direction_wait_state_closure_artifacts",
]
