from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_16_TASK_3_DIRECTION_OPTIONS_REVIEW_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_OPTIONS_REVIEW_ONLY_LOCAL_ONLY"
REVIEW_STATUS = "MILESTONE_16_DIRECTION_OPTIONS_REVIEW_READY"
REVIEW_VERDICT = "DIRECTION_OPTIONS_REVIEW_READY_NO_OPTION_SELECTED"
REVIEW_DECISION = "REVIEW_OPTIONS_NO_OPERATOR_DIRECTION_SELECTED"
BLOCK_REASON = "TASK_2_OPERATOR_DIRECTION_RECORD_CONFIRMED_PENDING_DIRECTION"

PREVIOUS_STAGE = "MILESTONE_16_TASK_2_OPERATOR_DIRECTION_RECORD_V1"
NEXT_STAGE = "MILESTONE_16_TASK_4_OPERATOR_DIRECTION_DECISION_GATE_V1"

SOURCE_TASK_2_FINAL_BASELINE_COMMIT = "723759c"
SOURCE_TASK_2_FINAL_SIGNATURE = "462BEB4F98EF951A"
SOURCE_TASK_1_FINAL_BASELINE_COMMIT = "6393a02"
SOURCE_TASK_1_FINAL_SIGNATURE = "CC061B8120F619BA"
SOURCE_MILESTONE_15_FINAL_BASELINE_COMMIT = "5f80a18"
SOURCE_MILESTONE_15_FINAL_SIGNATURE = "7D901B580AA49543"

OUTPUT_DIR = Path("examples/milestone-16/direction-options-review-v1")
DOC_PATH = Path("docs/milestone-16-direction-options-review-v1.md")


DIRECTION_OPTIONS: tuple[dict[str, Any], ...] = (
    {
        "option_id": "OPTION_A_WAIT_FOR_OPERATOR_DIRECTION",
        "label": "Wait for explicit operator direction",
        "review_status": "AVAILABLE_FOR_OPERATOR_SELECTION",
        "selected": False,
        "implementation_authorized_if_selected": False,
        "runtime_activation_authorized_if_selected": False,
        "real_submission_authorized_if_selected": False,
        "description": "Maintain the current implementation block until an explicit operator direction is received.",
    },
    {
        "option_id": "OPTION_B_CLOSE_DIRECTION_CYCLE_NO_ACTION",
        "label": "Close direction cycle with no action",
        "review_status": "AVAILABLE_FOR_OPERATOR_SELECTION",
        "selected": False,
        "implementation_authorized_if_selected": False,
        "runtime_activation_authorized_if_selected": False,
        "real_submission_authorized_if_selected": False,
        "description": "Close the current decision cycle without authorizing runtime or implementation changes.",
    },
    {
        "option_id": "OPTION_C_AUTHORIZE_DIAGNOSTIC_PLANNING_ONLY",
        "label": "Authorize diagnostic planning only",
        "review_status": "AVAILABLE_FOR_OPERATOR_SELECTION",
        "selected": False,
        "implementation_authorized_if_selected": False,
        "runtime_activation_authorized_if_selected": False,
        "real_submission_authorized_if_selected": False,
        "description": "Allow a planning-only diagnostic stage without modifying solver, ranker, candidate generator, runtime wiring, or submission path.",
    },
    {
        "option_id": "OPTION_D_AUTHORIZE_CONTROLLED_IMPLEMENTATION_REVIEW",
        "label": "Authorize controlled implementation review",
        "review_status": "AVAILABLE_FOR_OPERATOR_SELECTION",
        "selected": False,
        "implementation_authorized_if_selected": False,
        "runtime_activation_authorized_if_selected": False,
        "real_submission_authorized_if_selected": False,
        "description": "Review the possibility of a controlled implementation path, without granting implementation authorization in this task.",
    },
    {
        "option_id": "OPTION_E_REQUEST_ADDITIONAL_OPERATOR_INPUT",
        "label": "Request additional operator input",
        "review_status": "AVAILABLE_FOR_OPERATOR_SELECTION",
        "selected": False,
        "implementation_authorized_if_selected": False,
        "runtime_activation_authorized_if_selected": False,
        "real_submission_authorized_if_selected": False,
        "description": "Keep the system fail-closed and require more explicit operator direction before any downstream decision.",
    },
)


CHECKS = (
    "TASK_2_OPERATOR_DIRECTION_RECORD_CONFIRMED",
    "DIRECTION_OPTIONS_REVIEW_CREATED",
    "DIRECTION_OPTIONS_CATALOG_CREATED",
    "DIRECTION_OPTIONS_COUNT_VALID",
    "NO_DIRECTION_OPTION_SELECTED",
    "NO_OPERATOR_DIRECTION_RECEIVED",
    "OPERATOR_DECISION_NOT_RECEIVED",
    "EXPLICIT_OPERATOR_AUTHORIZATION_NOT_RECEIVED",
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
    "NO_KAGGLE_UPLOAD_ALLOWED",
    "NO_KAGGLE_SUBMISSION_SENT",
    "NO_PRIVATE_CORE_EXPOSURE",
    "NO_LEGAL_CERTIFICATION",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
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


def build_milestone_16_task_3_direction_options_review(
    *,
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    baseline = baseline_commit or _git_head()
    selected_options = [
        option for option in DIRECTION_OPTIONS if option.get("selected") is True
    ]

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "review_verdict": REVIEW_VERDICT,
        "review_decision": REVIEW_DECISION,
        "block_reason": BLOCK_REASON,
        "direction_options": DIRECTION_OPTIONS,
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
        "source_task_2_final_baseline_commit": SOURCE_TASK_2_FINAL_BASELINE_COMMIT,
        "source_task_2_final_signature": SOURCE_TASK_2_FINAL_SIGNATURE,
        "source_task_1_final_baseline_commit": SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
        "source_task_1_final_signature": SOURCE_TASK_1_FINAL_SIGNATURE,
        "source_milestone_15_final_baseline_commit": SOURCE_MILESTONE_15_FINAL_BASELINE_COMMIT,
        "source_milestone_15_final_signature": SOURCE_MILESTONE_15_FINAL_SIGNATURE,
        "milestone_16_opened": True,
        "task_2_operator_direction_record_confirmed": True,
        "direction_options_review_created": True,
        "direction_options_catalog_created": True,
        "direction_option_count": len(DIRECTION_OPTIONS),
        "direction_options": list(DIRECTION_OPTIONS),
        "direction_option_selected": False,
        "selected_direction_option_id": "NONE",
        "selected_direction_option_count": len(selected_options),
        "operator_direction_required": True,
        "operator_direction_received": False,
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "operator_decision_required": True,
        "operator_decision_received": False,
        "operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "explicit_operator_authorization_required": True,
        "explicit_operator_authorization_received": False,
        "explicit_operator_authorization_value": "NO_EXPLICIT_OPERATOR_AUTHORIZATION_RECEIVED",
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
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "milestone_16_direction_options_review_checks": CHECKS,
        "milestone_16_direction_options_review_check_count": len(CHECKS),
        "milestone_16_direction_options_review_failure_count": 0,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def validate_milestone_16_task_3_direction_options_review(
    review: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = (
        "milestone_16_opened",
        "task_2_operator_direction_record_confirmed",
        "direction_options_review_created",
        "direction_options_catalog_created",
        "operator_direction_required",
        "operator_decision_required",
        "explicit_operator_authorization_required",
        "implementation_blocked",
        "runtime_activation_blocked",
        "public_overfit_guard_required",
        "fail_closed_required",
        "fail_closed_active",
        "public_safe",
        "deterministic",
        "local_only",
    )

    for key in expected_true:
        if review.get(key) is not True:
            issues.append(f"{key}:expected_true")

    expected_false = (
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
        "source_task_2_final_baseline_commit": SOURCE_TASK_2_FINAL_BASELINE_COMMIT,
        "source_task_2_final_signature": SOURCE_TASK_2_FINAL_SIGNATURE,
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "selected_direction_option_id": "NONE",
    }

    for key, expected in expected_pairs.items():
        if review.get(key) != expected:
            issues.append(f"{key}:mismatch")

    if review.get("direction_option_count") != len(DIRECTION_OPTIONS):
        issues.append("direction_option_count_mismatch")

    if review.get("selected_direction_option_count") != 0:
        issues.append("selected_direction_option_count_nonzero")

    for option in review.get("direction_options", []):
        if option.get("selected") is not False:
            issues.append(f"{option.get('option_id', 'UNKNOWN')}:option_selected")
        if option.get("implementation_authorized_if_selected") is not False:
            issues.append(f"{option.get('option_id', 'UNKNOWN')}:implementation_authorized_in_review")
        if option.get("runtime_activation_authorized_if_selected") is not False:
            issues.append(f"{option.get('option_id', 'UNKNOWN')}:runtime_activation_authorized_in_review")
        if option.get("real_submission_authorized_if_selected") is not False:
            issues.append(f"{option.get('option_id', 'UNKNOWN')}:real_submission_authorized_in_review")

    if review.get("milestone_16_direction_options_review_check_count") != len(CHECKS):
        issues.append("milestone_16_direction_options_review_check_count_mismatch")

    if review.get("milestone_16_direction_options_review_failure_count") != 0:
        issues.append("milestone_16_direction_options_review_failure_count_nonzero")

    return {
        "status": TASK_VALID if not issues else f"{TASK_NAME}_INVALID",
        "valid": not issues,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "issues": issues,
        "warnings": warnings,
    }


def write_milestone_16_task_3_direction_options_review_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-16-direction-options-review-v1.json"
    output_index = output_dir / "milestone-16-direction-options-review-index-v1.json"
    output_manifest = output_dir / "milestone-16-direction-options-review-manifest-v1.txt"
    output_md = output_dir / "milestone-16-direction-options-review-v1.md"

    review = build_milestone_16_task_3_direction_options_review()
    validation = validate_milestone_16_task_3_direction_options_review(review)

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
        "direction_option_count": review["direction_option_count"],
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
        f"source_task_2_final_baseline_commit={review['source_task_2_final_baseline_commit']}",
        f"source_task_2_final_signature={review['source_task_2_final_signature']}",
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
        f"milestone_16_direction_options_review_check_count={review['milestone_16_direction_options_review_check_count']}",
        f"milestone_16_direction_options_review_failure_count={review['milestone_16_direction_options_review_failure_count']}",
        "",
    ]

    md_lines = [
        "# Milestone 16 - Task 3 - Direction Options Review v1",
        "",
        f"Status: `{review['status']}`",
        f"Validation: `{validation['status']}`",
        f"Signature: `{review['signature']}`",
        f"Baseline commit: `{review['baseline_commit']}`",
        "",
        "## Purpose",
        "",
        "This task reviews possible operator direction options after the operator direction record.",
        "",
        "No direction option is selected. No implementation, runtime activation, runtime execution, Kaggle upload, or real submission is authorized.",
        "",
        "## Review",
        "",
        f"- Review verdict: `{review['review_verdict']}`",
        f"- Review decision: `{review['review_decision']}`",
        f"- Direction option count: `{review['direction_option_count']}`",
        f"- Selected option: `{review['selected_direction_option_id']}`",
        f"- Block reason: `{review['block_reason']}`",
        "",
        "## Options",
        "",
    ]

    for option in review["direction_options"]:
        md_lines.extend(
            [
                f"### {option['option_id']}",
                "",
                f"- Label: `{option['label']}`",
                f"- Review status: `{option['review_status']}`",
                f"- Selected: `{option['selected']}`",
                f"- Implementation authorized if selected: `{option['implementation_authorized_if_selected']}`",
                f"- Runtime activation authorized if selected: `{option['runtime_activation_authorized_if_selected']}`",
                f"- Real submission authorized if selected: `{option['real_submission_authorized_if_selected']}`",
                f"- Description: {option['description']}",
                "",
            ]
        )

    md_lines.extend(
        [
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
    )

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
    "DIRECTION_OPTIONS",
    "build_milestone_16_task_3_direction_options_review",
    "validate_milestone_16_task_3_direction_options_review",
    "write_milestone_16_task_3_direction_options_review_artifacts",
]
