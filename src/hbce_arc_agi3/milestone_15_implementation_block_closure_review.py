from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_15_TASK_9_IMPLEMENTATION_BLOCK_CLOSURE_REVIEW_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_CLOSURE_REVIEW_ONLY_LOCAL_ONLY"
REVIEW_STATUS = "IMPLEMENTATION_BLOCK_CLOSURE_REVIEW_READY"
REVIEW_VERDICT = "IMPLEMENTATION_BLOCK_CLOSURE_REVIEW_PASS_BLOCK_STILL_ACTIVE"
REVIEW_DECISION = "CLOSE_IMPLEMENTATION_BLOCK_REVIEW_WITH_BLOCK_ACTIVE"
BLOCK_REASON = "TASK_8_AUTHORIZATION_RECORD_CONFIRMED_NO_IMPLEMENTATION_AUTHORIZATION_GRANTED"

PREVIOUS_STAGE = "MILESTONE_15_TASK_8_IMPLEMENTATION_AUTHORIZATION_RECORD_V1"
NEXT_STAGE = "MILESTONE_15_TASK_10_MILESTONE_15_FINAL_CLOSURE_V1"

SOURCE_TASK_8_FINAL_BASELINE_COMMIT = "115a6a9"
SOURCE_TASK_8_FINAL_SIGNATURE = "C08A4A04B5EBA5C9"
SOURCE_TASK_7_FINAL_BASELINE_COMMIT = "73a7fbd"
SOURCE_TASK_7_FINAL_SIGNATURE = "B2CDE3D0D82C2DD6"
SOURCE_TASK_6_FINAL_BASELINE_COMMIT = "c70df02"
SOURCE_TASK_6_FINAL_SIGNATURE = "D93E57F44AAF8A8E"

OUTPUT_DIR = Path("examples/milestone-15/implementation-block-closure-review-v1")
DOC_PATH = Path("docs/milestone-15-implementation-block-closure-review-v1.md")


CHECKS = (
    "TASK_8_AUTHORIZATION_RECORD_CONFIRMED",
    "TASK_7_DECISION_GATE_CONFIRMED",
    "TASK_6_IMPLEMENTATION_BLOCK_CONFIRMED",
    "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED",
    "NO_IMPLEMENTATION_AUTHORIZED",
    "NO_IMPLEMENTATION_PERFORMED",
    "NO_IMPLEMENTATION_PATCH_CREATED",
    "NO_IMPLEMENTATION_PATCH_APPLIED",
    "NO_RUNTIME_SOLVER_PATCH_ALLOWED",
    "NO_RANKER_RUNTIME_PATCH_ALLOWED",
    "NO_CANDIDATE_GENERATOR_PATCH_ALLOWED",
    "NO_RUNTIME_WIRING_ALLOWED",
    "NO_RUNTIME_ACTIVATION_AUTHORIZED",
    "NO_RUNTIME_EXECUTION_ALLOWED",
    "NO_REAL_EVALUATION_PERFORMED",
    "NO_REAL_SUBMISSION_ALLOWED",
    "NO_KAGGLE_UPLOAD_ALLOWED",
    "NO_PRIVATE_CORE_EXPOSURE",
    "NO_LEGAL_CERTIFICATION",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
    "READY_FOR_FINAL_CLOSURE_REVIEW",
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


def build_milestone_15_task_9_implementation_block_closure_review(
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
        "source_task_8_final_baseline_commit": SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        "source_task_8_final_signature": SOURCE_TASK_8_FINAL_SIGNATURE,
        "source_task_7_final_baseline_commit": SOURCE_TASK_7_FINAL_BASELINE_COMMIT,
        "source_task_7_final_signature": SOURCE_TASK_7_FINAL_SIGNATURE,
        "source_task_6_final_baseline_commit": SOURCE_TASK_6_FINAL_BASELINE_COMMIT,
        "source_task_6_final_signature": SOURCE_TASK_6_FINAL_SIGNATURE,
        "implementation_block_closure_review_created": True,
        "task_8_authorization_record_confirmed": True,
        "task_7_decision_gate_confirmed": True,
        "task_6_implementation_block_confirmed": True,
        "operator_decision_required": True,
        "operator_decision_received": False,
        "operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "explicit_operator_authorization_required": True,
        "explicit_operator_authorization_received": False,
        "explicit_operator_authorization_value": "NO_EXPLICIT_OPERATOR_AUTHORIZATION_RECEIVED",
        "implementation_authorization_recorded": True,
        "implementation_authorization_record_value": "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED",
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
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "ready_for_milestone_15_final_closure": True,
        "implementation_block_closure_review_checks": CHECKS,
        "implementation_block_closure_review_check_count": len(CHECKS),
        "implementation_block_closure_review_failure_count": 0,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def validate_milestone_15_task_9_implementation_block_closure_review(
    review: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = (
        "implementation_block_closure_review_created",
        "task_8_authorization_record_confirmed",
        "task_7_decision_gate_confirmed",
        "task_6_implementation_block_confirmed",
        "operator_decision_required",
        "explicit_operator_authorization_required",
        "implementation_authorization_recorded",
        "implementation_blocked",
        "runtime_activation_blocked",
        "public_overfit_guard_required",
        "fail_closed_required",
        "fail_closed_active",
        "public_safe",
        "deterministic",
        "local_only",
        "ready_for_milestone_15_final_closure",
    )

    for key in expected_true:
        if review.get(key) is not True:
            issues.append(f"{key}:expected_true")

    expected_false = (
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
        "source_task_8_final_baseline_commit": SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        "source_task_8_final_signature": SOURCE_TASK_8_FINAL_SIGNATURE,
        "implementation_authorization_record_value": "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED",
    }

    for key, expected in expected_pairs.items():
        if review.get(key) != expected:
            issues.append(f"{key}:mismatch")

    if review.get("implementation_block_closure_review_check_count") != len(CHECKS):
        issues.append("implementation_block_closure_review_check_count_mismatch")

    if review.get("implementation_block_closure_review_failure_count") != 0:
        issues.append("implementation_block_closure_review_failure_count_nonzero")

    return {
        "status": TASK_VALID if not issues else f"{TASK_NAME}_INVALID",
        "valid": not issues,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "issues": issues,
        "warnings": warnings,
    }


def write_milestone_15_task_9_implementation_block_closure_review_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-15-implementation-block-closure-review-v1.json"
    output_index = output_dir / "milestone-15-implementation-block-closure-review-index-v1.json"
    output_manifest = output_dir / "milestone-15-implementation-block-closure-review-manifest-v1.txt"
    output_md = output_dir / "milestone-15-implementation-block-closure-review-v1.md"

    review = build_milestone_15_task_9_implementation_block_closure_review()
    validation = validate_milestone_15_task_9_implementation_block_closure_review(review)

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
        "implementation_authorization_granted": review["implementation_authorization_granted"],
        "implementation_authorized": review["implementation_authorized"],
        "implementation_performed": review["implementation_performed"],
        "ready_for_milestone_15_final_closure": review["ready_for_milestone_15_final_closure"],
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
        f"source_task_8_final_baseline_commit={review['source_task_8_final_baseline_commit']}",
        f"source_task_8_final_signature={review['source_task_8_final_signature']}",
        f"task_8_authorization_record_confirmed={review['task_8_authorization_record_confirmed']}",
        f"implementation_authorization_granted={review['implementation_authorization_granted']}",
        f"implementation_authorized={review['implementation_authorized']}",
        f"implementation_blocked={review['implementation_blocked']}",
        f"implementation_performed={review['implementation_performed']}",
        f"runtime_solver_patch_allowed={review['runtime_solver_patch_allowed']}",
        f"runtime_solver_modified={review['runtime_solver_modified']}",
        f"runtime_wiring_allowed={review['runtime_wiring_allowed']}",
        f"runtime_wiring_performed={review['runtime_wiring_performed']}",
        f"runtime_activation_authorized={review['runtime_activation_authorized']}",
        f"runtime_activation_performed={review['runtime_activation_performed']}",
        f"runtime_execution_allowed={review['runtime_execution_allowed']}",
        f"runtime_execution_performed={review['runtime_execution_performed']}",
        f"real_submission_allowed={review['real_submission_allowed']}",
        f"legal_certification={review['legal_certification']}",
        f"ready_for_milestone_15_final_closure={review['ready_for_milestone_15_final_closure']}",
        f"implementation_block_closure_review_check_count={review['implementation_block_closure_review_check_count']}",
        f"implementation_block_closure_review_failure_count={review['implementation_block_closure_review_failure_count']}",
        "",
    ]

    md_lines = [
        "# Milestone 15 - Task 9 - Implementation Block Closure Review v1",
        "",
        f"Status: `{review['status']}`",
        f"Validation: `{validation['status']}`",
        f"Signature: `{review['signature']}`",
        f"Baseline commit: `{review['baseline_commit']}`",
        "",
        "## Purpose",
        "",
        "This task closes the implementation block review chain after Task 8.",
        "",
        "The review confirms that no implementation authorization has been granted and no runtime path has been opened.",
        "",
        "## Review",
        "",
        f"- Review verdict: `{review['review_verdict']}`",
        f"- Review decision: `{review['review_decision']}`",
        f"- Block reason: `{review['block_reason']}`",
        "",
        "## Boundary",
        "",
        f"- task_8_authorization_record_confirmed: `{review['task_8_authorization_record_confirmed']}`",
        f"- implementation_authorization_granted: `{review['implementation_authorization_granted']}`",
        f"- implementation_authorized: `{review['implementation_authorized']}`",
        f"- implementation_blocked: `{review['implementation_blocked']}`",
        f"- implementation_performed: `{review['implementation_performed']}`",
        f"- runtime_solver_patch_allowed: `{review['runtime_solver_patch_allowed']}`",
        f"- runtime_solver_modified: `{review['runtime_solver_modified']}`",
        f"- runtime_wiring_allowed: `{review['runtime_wiring_allowed']}`",
        f"- runtime_wiring_performed: `{review['runtime_wiring_performed']}`",
        f"- runtime_activation_authorized: `{review['runtime_activation_authorized']}`",
        f"- runtime_activation_performed: `{review['runtime_activation_performed']}`",
        f"- runtime_execution_allowed: `{review['runtime_execution_allowed']}`",
        f"- runtime_execution_performed: `{review['runtime_execution_performed']}`",
        f"- real_submission_allowed: `{review['real_submission_allowed']}`",
        f"- legal_certification: `{review['legal_certification']}`",
        f"- ready_for_milestone_15_final_closure: `{review['ready_for_milestone_15_final_closure']}`",
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
    "build_milestone_15_task_9_implementation_block_closure_review",
    "validate_milestone_15_task_9_implementation_block_closure_review",
    "write_milestone_15_task_9_implementation_block_closure_review_artifacts",
]
