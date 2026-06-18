from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_16_TASK_6_OPERATOR_DIRECTION_WAIT_STATE_REVIEW_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_REVIEW_ONLY_LOCAL_ONLY"
REVIEW_STATUS = "MILESTONE_16_OPERATOR_DIRECTION_WAIT_STATE_REVIEW_READY"
REVIEW_VERDICT = "OPERATOR_DIRECTION_WAIT_STATE_REVIEW_PASS_WAIT_STATE_STILL_ACTIVE"
REVIEW_DECISION = "CONFIRM_WAIT_STATE_ACTIVE_NO_IMPLEMENTATION"
BLOCK_REASON = "TASK_5_WAIT_STATE_CONFIRMED_ACTIVE"

PREVIOUS_STAGE = "MILESTONE_16_TASK_5_OPERATOR_DIRECTION_WAIT_STATE_V1"
NEXT_STAGE = "MILESTONE_16_TASK_7_OPERATOR_DIRECTION_WAIT_STATE_CLOSURE_V1"

SOURCE_TASK_5_FINAL_BASELINE_COMMIT = "03acb5a"
SOURCE_TASK_5_FINAL_SIGNATURE = "EC9F02EC0CF5AC8F"
SOURCE_TASK_4_FINAL_BASELINE_COMMIT = "36887a0"
SOURCE_TASK_4_FINAL_SIGNATURE = "7A0DD6F0A4F3F4C8"

OUTPUT_DIR = Path("examples/milestone-16/operator-direction-wait-state-review-v1")
DOC_PATH = Path("docs/milestone-16-operator-direction-wait-state-review-v1.md")


CHECKS = (
    "TASK_5_WAIT_STATE_CONFIRMED",
    "WAIT_STATE_REVIEW_CREATED",
    "WAIT_STATE_REVIEW_READY",
    "WAIT_STATE_REVIEW_PASSED",
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


def build_milestone_16_task_6_operator_direction_wait_state_review(
    *,
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    baseline = baseline_commit or _git_head()

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "review_verdict": REVIEW_VERDICT,
        "review_decision": REVIEW_DECISION,
        "block_reason": BLOCK_REASON,
        "checks": CHECKS,
    }

    return {
        "task_name": TASK_NAME,
        "status": TASK_READY,
        "mode": MODE,
        "review_status": REVIEW_STATUS,
        "review_verdict": REVIEW_VERDICT,
        "review_decision": REVIEW_DECISION,
        "block_reason": BLOCK_REASON,
        "signature": _signature(seed),
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "source_task_5_final_baseline_commit": SOURCE_TASK_5_FINAL_BASELINE_COMMIT,
        "source_task_5_final_signature": SOURCE_TASK_5_FINAL_SIGNATURE,
        "source_task_4_final_baseline_commit": SOURCE_TASK_4_FINAL_BASELINE_COMMIT,
        "source_task_4_final_signature": SOURCE_TASK_4_FINAL_SIGNATURE,
        "milestone_16_opened": True,
        "task_5_wait_state_confirmed": True,
        "operator_direction_wait_state_review_created": True,
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
        "review_only": True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "milestone_16_operator_direction_wait_state_review_checks": CHECKS,
        "milestone_16_operator_direction_wait_state_review_check_count": len(CHECKS),
        "milestone_16_operator_direction_wait_state_review_failure_count": 0,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def validate_milestone_16_task_6_operator_direction_wait_state_review(
    review: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = (
        "milestone_16_opened",
        "task_5_wait_state_confirmed",
        "operator_direction_wait_state_review_created",
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
        "review_only",
        "public_safe",
        "deterministic",
        "local_only",
    )

    for key in expected_true:
        if review.get(key) is not True:
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
        if review.get(key) is not False:
            issues.append(f"{key}:expected_false")

    expected_pairs = {
        "review_verdict": REVIEW_VERDICT,
        "review_decision": REVIEW_DECISION,
        "block_reason": BLOCK_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "source_task_5_final_baseline_commit": SOURCE_TASK_5_FINAL_BASELINE_COMMIT,
        "source_task_5_final_signature": SOURCE_TASK_5_FINAL_SIGNATURE,
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "selected_direction_option_id": "NONE",
        "wait_state_reason": "NO_EXPLICIT_OPERATOR_DIRECTION_RECEIVED",
    }

    for key, expected in expected_pairs.items():
        if review.get(key) != expected:
            issues.append(f"{key}:mismatch")

    if review.get("direction_option_count") != 5:
        issues.append("direction_option_count_mismatch")

    if review.get("selected_direction_option_count") != 0:
        issues.append("selected_direction_option_count_nonzero")

    if review.get("milestone_16_operator_direction_wait_state_review_check_count") != len(CHECKS):
        issues.append("milestone_16_operator_direction_wait_state_review_check_count_mismatch")

    if review.get("milestone_16_operator_direction_wait_state_review_failure_count") != 0:
        issues.append("milestone_16_operator_direction_wait_state_review_failure_count_nonzero")

    return {
        "status": TASK_VALID if not issues else f"{TASK_NAME}_INVALID",
        "valid": not issues,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "issues": issues,
        "warnings": warnings,
    }


def write_milestone_16_task_6_operator_direction_wait_state_review_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-16-operator-direction-wait-state-review-v1.json"
    output_index = output_dir / "milestone-16-operator-direction-wait-state-review-index-v1.json"
    output_manifest = output_dir / "milestone-16-operator-direction-wait-state-review-manifest-v1.txt"
    output_md = output_dir / "milestone-16-operator-direction-wait-state-review-v1.md"

    review = build_milestone_16_task_6_operator_direction_wait_state_review()
    validation = validate_milestone_16_task_6_operator_direction_wait_state_review(review)

    payload = {
        "review": review,
        "validation": validation,
    }

    index = {
        "task_name": review["task_name"],
        "status": review["status"],
        "validation_status": validation["status"],
        "valid": validation["valid"],
        "signature": review["signature"],
        "baseline_commit": review["baseline_commit"],
        "previous_stage": review["previous_stage"],
        "next_stage": review["next_stage"],
        "review_verdict": review["review_verdict"],
        "review_decision": review["review_decision"],
        "wait_state_active": review["wait_state_active"],
        "wait_state_closed": review["wait_state_closed"],
        "selected_direction_option_id": review["selected_direction_option_id"],
        "operator_direction_received": review["operator_direction_received"],
        "implementation_authorized": review["implementation_authorized"],
        "runtime_activation_performed": review["runtime_activation_performed"],
        "real_submission_allowed": review["real_submission_allowed"],
        "artifact_paths": {
            "json": str(output_json),
            "index": str(output_index),
            "manifest": str(output_manifest),
            "markdown": str(output_md),
            "doc": str(doc_path),
        },
    }

    manifest_lines = [
        f"task_name={review['task_name']}",
        f"status={review['status']}",
        f"validation_status={validation['status']}",
        f"valid={validation['valid']}",
        f"signature={review['signature']}",
        f"baseline_commit={review['baseline_commit']}",
        f"mode={review['mode']}",
        f"review_status={review['review_status']}",
        f"review_verdict={review['review_verdict']}",
        f"review_decision={review['review_decision']}",
        f"block_reason={review['block_reason']}",
        f"previous_stage={review['previous_stage']}",
        f"next_stage={review['next_stage']}",
        f"source_task_5_final_baseline_commit={review['source_task_5_final_baseline_commit']}",
        f"source_task_5_final_signature={review['source_task_5_final_signature']}",
        f"wait_state_review_ready={review['wait_state_review_ready']}",
        f"wait_state_review_passed={review['wait_state_review_passed']}",
        f"wait_state_active={review['wait_state_active']}",
        f"wait_state_closed={review['wait_state_closed']}",
        f"decision_gate_blocked={review['decision_gate_blocked']}",
        f"direction_option_count={review['direction_option_count']}",
        f"direction_option_selected={review['direction_option_selected']}",
        f"selected_direction_option_id={review['selected_direction_option_id']}",
        f"operator_direction_required={review['operator_direction_required']}",
        f"operator_direction_received={review['operator_direction_received']}",
        f"operator_direction_value={review['operator_direction_value']}",
        f"implementation_authorized={review['implementation_authorized']}",
        f"implementation_blocked={review['implementation_blocked']}",
        f"implementation_performed={review['implementation_performed']}",
        f"runtime_solver_modified={review['runtime_solver_modified']}",
        f"runtime_wiring_performed={review['runtime_wiring_performed']}",
        f"runtime_activation_performed={review['runtime_activation_performed']}",
        f"runtime_execution_performed={review['runtime_execution_performed']}",
        f"real_submission_allowed={review['real_submission_allowed']}",
        f"kaggle_submission_sent={review['kaggle_submission_sent']}",
        f"private_core_exposure={review['private_core_exposure']}",
        f"legal_certification={review['legal_certification']}",
        f"milestone_16_operator_direction_wait_state_review_check_count={review['milestone_16_operator_direction_wait_state_review_check_count']}",
        f"milestone_16_operator_direction_wait_state_review_failure_count={review['milestone_16_operator_direction_wait_state_review_failure_count']}",
        "",
    ]

    md_lines = [
        "# Milestone 16 - Task 6 - Operator Direction Wait State Review v1",
        "",
        f"Status: `{review['status']}`",
        f"Validation: `{validation['status']}`",
        f"Signature: `{review['signature']}`",
        f"Baseline commit: `{review['baseline_commit']}`",
        "",
        "## Purpose",
        "",
        "This task reviews the active wait state created by Task 5.",
        "",
        "The wait state remains active. No explicit operator direction has been received. No direction option is selected. No implementation, runtime activation, runtime execution, Kaggle upload, or real submission is authorized.",
        "",
        "## Review",
        "",
        f"- Review verdict: `{review['review_verdict']}`",
        f"- Review decision: `{review['review_decision']}`",
        f"- Wait state review ready: `{review['wait_state_review_ready']}`",
        f"- Wait state review passed: `{review['wait_state_review_passed']}`",
        f"- Wait state active: `{review['wait_state_active']}`",
        f"- Wait state closed: `{review['wait_state_closed']}`",
        f"- Selected option: `{review['selected_direction_option_id']}`",
        f"- Block reason: `{review['block_reason']}`",
        "",
        "## Boundary",
        "",
        f"- operator_direction_required: `{review['operator_direction_required']}`",
        f"- operator_direction_received: `{review['operator_direction_received']}`",
        f"- implementation_authorized: `{review['implementation_authorized']}`",
        f"- implementation_blocked: `{review['implementation_blocked']}`",
        f"- implementation_performed: `{review['implementation_performed']}`",
        f"- runtime_solver_modified: `{review['runtime_solver_modified']}`",
        f"- runtime_wiring_performed: `{review['runtime_wiring_performed']}`",
        f"- runtime_activation_performed: `{review['runtime_activation_performed']}`",
        f"- runtime_execution_performed: `{review['runtime_execution_performed']}`",
        f"- real_submission_allowed: `{review['real_submission_allowed']}`",
        f"- kaggle_submission_sent: `{review['kaggle_submission_sent']}`",
        f"- private_core_exposure: `{review['private_core_exposure']}`",
        f"- legal_certification: `{review['legal_certification']}`",
        "",
    ]

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text("\n".join(manifest_lines), encoding="utf-8")
    output_md.write_text("\n".join(md_lines), encoding="utf-8")
    doc_path.write_text("\n".join(md_lines), encoding="utf-8")

    return review, validation, {
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
    "REVIEW_STATUS",
    "REVIEW_VERDICT",
    "REVIEW_DECISION",
    "BLOCK_REASON",
    "PREVIOUS_STAGE",
    "NEXT_STAGE",
    "build_milestone_16_task_6_operator_direction_wait_state_review",
    "validate_milestone_16_task_6_operator_direction_wait_state_review",
    "write_milestone_16_task_6_operator_direction_wait_state_review_artifacts",
]
