from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_15_TASK_10_FINAL_CLOSURE_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_FINAL_CLOSURE_ONLY_LOCAL_ONLY"
CLOSURE_STATUS = "MILESTONE_15_FINAL_CLOSURE_READY"
CLOSURE_VERDICT = "MILESTONE_15_CLOSED_IMPLEMENTATION_BLOCK_ACTIVE_NO_RUNTIME_ACTIVATION"
CLOSURE_DECISION = "CLOSE_MILESTONE_15_WITH_IMPLEMENTATION_BLOCK_CONFIRMED"
BLOCK_REASON = "TASK_9_IMPLEMENTATION_BLOCK_CLOSURE_REVIEW_CONFIRMED_BLOCK_ACTIVE"

PREVIOUS_STAGE = "MILESTONE_15_TASK_9_IMPLEMENTATION_BLOCK_CLOSURE_REVIEW_V1"
NEXT_STAGE = "MILESTONE_16_PENDING_OPERATOR_DIRECTION"

SOURCE_TASK_9_FINAL_BASELINE_COMMIT = "ff4aa9f"
SOURCE_TASK_9_FINAL_SIGNATURE = "3409B78DFD78F374"
SOURCE_TASK_8_FINAL_BASELINE_COMMIT = "115a6a9"
SOURCE_TASK_8_FINAL_SIGNATURE = "C08A4A04B5EBA5C9"
SOURCE_TASK_7_FINAL_BASELINE_COMMIT = "73a7fbd"
SOURCE_TASK_7_FINAL_SIGNATURE = "B2CDE3D0D82C2DD6"
SOURCE_TASK_6_FINAL_BASELINE_COMMIT = "c70df02"
SOURCE_TASK_6_FINAL_SIGNATURE = "D93E57F44AAF8A8E"
SOURCE_TASK_5_FINAL_BASELINE_COMMIT = "cd005ad"
SOURCE_TASK_5_FINAL_SIGNATURE = "1065B790C4AE1364"
SOURCE_TASK_4_FINAL_BASELINE_COMMIT = "2e7e02c"
SOURCE_TASK_4_FINAL_SIGNATURE = "3DA3C07D68125962"
SOURCE_TASK_3_FINAL_BASELINE_COMMIT = "756df18"
SOURCE_TASK_3_FINAL_SIGNATURE = "3FF1874D0CEBB5C2"
SOURCE_TASK_2_FINAL_BASELINE_COMMIT = "7cd11c0"
SOURCE_TASK_2_FINAL_SIGNATURE = "92DD45142240063F"
SOURCE_TASK_1_FINAL_BASELINE_COMMIT = "ed48f9c"
SOURCE_TASK_1_FINAL_SIGNATURE = "22CAADB16533FB69"
SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT = "f7ee729"
SOURCE_MILESTONE_14_FINAL_SIGNATURE = "05F1CDD559B63B8C"

OUTPUT_DIR = Path("examples/milestone-15/final-closure-v1")
DOC_PATH = Path("docs/milestone-15-final-closure-v1.md")


CHECKS = (
    "TASK_1_OPERATOR_DECISION_GATE_CONFIRMED",
    "TASK_2_OPERATOR_DECISION_RECORD_CONFIRMED",
    "TASK_3_AUTHORIZATION_BOUNDARY_CONFIRMED",
    "TASK_4_RUNTIME_ACTIVATION_BOUNDARY_CONFIRMED",
    "TASK_5_RUNTIME_ACTIVATION_REVIEW_CONFIRMED",
    "TASK_6_IMPLEMENTATION_BLOCK_REVIEW_CONFIRMED",
    "TASK_7_IMPLEMENTATION_AUTHORIZATION_DECISION_CONFIRMED",
    "TASK_8_IMPLEMENTATION_AUTHORIZATION_RECORD_CONFIRMED",
    "TASK_9_IMPLEMENTATION_BLOCK_CLOSURE_REVIEW_CONFIRMED",
    "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
    "NO_OPERATOR_DECISION_RECEIVED",
    "NO_EXPLICIT_OPERATOR_AUTHORIZATION_RECEIVED",
    "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED",
    "NO_IMPLEMENTATION_AUTHORIZED",
    "NO_IMPLEMENTATION_PERFORMED",
    "NO_RUNTIME_SOLVER_PATCH_ALLOWED",
    "NO_RANKER_RUNTIME_PATCH_ALLOWED",
    "NO_CANDIDATE_GENERATOR_PATCH_ALLOWED",
    "NO_RUNTIME_WIRING_PERFORMED",
    "NO_RUNTIME_ACTIVATION_PERFORMED",
    "NO_RUNTIME_EXECUTION_PERFORMED",
    "NO_REAL_EVALUATION_PERFORMED",
    "NO_REAL_SUBMISSION_ALLOWED",
    "NO_KAGGLE_AUTHENTICATION_ALLOWED",
    "NO_KAGGLE_UPLOAD_ALLOWED",
    "NO_KAGGLE_SUBMISSION_SENT",
    "NO_PRIVATE_CORE_EXPOSURE",
    "NO_LEGAL_CERTIFICATION",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
    "MILESTONE_15_CLOSURE_LOCKED",
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


def build_milestone_15_task_10_final_closure(
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
        "source_task_9_final_baseline_commit": SOURCE_TASK_9_FINAL_BASELINE_COMMIT,
        "source_task_9_final_signature": SOURCE_TASK_9_FINAL_SIGNATURE,
        "source_task_8_final_baseline_commit": SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        "source_task_8_final_signature": SOURCE_TASK_8_FINAL_SIGNATURE,
        "source_task_7_final_baseline_commit": SOURCE_TASK_7_FINAL_BASELINE_COMMIT,
        "source_task_7_final_signature": SOURCE_TASK_7_FINAL_SIGNATURE,
        "source_task_6_final_baseline_commit": SOURCE_TASK_6_FINAL_BASELINE_COMMIT,
        "source_task_6_final_signature": SOURCE_TASK_6_FINAL_SIGNATURE,
        "source_task_5_final_baseline_commit": SOURCE_TASK_5_FINAL_BASELINE_COMMIT,
        "source_task_5_final_signature": SOURCE_TASK_5_FINAL_SIGNATURE,
        "source_task_4_final_baseline_commit": SOURCE_TASK_4_FINAL_BASELINE_COMMIT,
        "source_task_4_final_signature": SOURCE_TASK_4_FINAL_SIGNATURE,
        "source_task_3_final_baseline_commit": SOURCE_TASK_3_FINAL_BASELINE_COMMIT,
        "source_task_3_final_signature": SOURCE_TASK_3_FINAL_SIGNATURE,
        "source_task_2_final_baseline_commit": SOURCE_TASK_2_FINAL_BASELINE_COMMIT,
        "source_task_2_final_signature": SOURCE_TASK_2_FINAL_SIGNATURE,
        "source_task_1_final_baseline_commit": SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
        "source_task_1_final_signature": SOURCE_TASK_1_FINAL_SIGNATURE,
        "source_milestone_14_final_baseline_commit": SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT,
        "source_milestone_14_final_signature": SOURCE_MILESTONE_14_FINAL_SIGNATURE,
        "milestone_15_final_closure_created": True,
        "milestone_15_closed": True,
        "task_9_closure_review_confirmed": True,
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
        "milestone_15_final_closure_checks": CHECKS,
        "milestone_15_final_closure_check_count": len(CHECKS),
        "milestone_15_final_closure_failure_count": 0,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def validate_milestone_15_task_10_final_closure(
    closure: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = (
        "milestone_15_final_closure_created",
        "milestone_15_closed",
        "task_9_closure_review_confirmed",
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
    )

    for key in expected_true:
        if closure.get(key) is not True:
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
        if closure.get(key) is not False:
            issues.append(f"{key}:expected_false")

    expected_pairs = {
        "closure_verdict": CLOSURE_VERDICT,
        "closure_decision": CLOSURE_DECISION,
        "block_reason": BLOCK_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "source_task_9_final_baseline_commit": SOURCE_TASK_9_FINAL_BASELINE_COMMIT,
        "source_task_9_final_signature": SOURCE_TASK_9_FINAL_SIGNATURE,
        "implementation_authorization_record_value": "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED",
    }

    for key, expected in expected_pairs.items():
        if closure.get(key) != expected:
            issues.append(f"{key}:mismatch")

    if closure.get("milestone_15_final_closure_check_count") != len(CHECKS):
        issues.append("milestone_15_final_closure_check_count_mismatch")

    if closure.get("milestone_15_final_closure_failure_count") != 0:
        issues.append("milestone_15_final_closure_failure_count_nonzero")

    return {
        "status": TASK_VALID if not issues else f"{TASK_NAME}_INVALID",
        "valid": not issues,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "issues": issues,
        "warnings": warnings,
    }


def write_milestone_15_task_10_final_closure_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-15-final-closure-v1.json"
    output_index = output_dir / "milestone-15-final-closure-index-v1.json"
    output_manifest = output_dir / "milestone-15-final-closure-manifest-v1.txt"
    output_md = output_dir / "milestone-15-final-closure-v1.md"

    closure = build_milestone_15_task_10_final_closure()
    validation = validate_milestone_15_task_10_final_closure(closure)

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
        "milestone_15_closed": closure["milestone_15_closed"],
        "implementation_authorized": closure["implementation_authorized"],
        "implementation_performed": closure["implementation_performed"],
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
        f"source_task_9_final_baseline_commit={closure['source_task_9_final_baseline_commit']}",
        f"source_task_9_final_signature={closure['source_task_9_final_signature']}",
        f"milestone_15_closed={closure['milestone_15_closed']}",
        f"operator_decision_received={closure['operator_decision_received']}",
        f"explicit_operator_authorization_received={closure['explicit_operator_authorization_received']}",
        f"implementation_authorization_granted={closure['implementation_authorization_granted']}",
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
        f"milestone_15_final_closure_check_count={closure['milestone_15_final_closure_check_count']}",
        f"milestone_15_final_closure_failure_count={closure['milestone_15_final_closure_failure_count']}",
        "",
    ]

    md_lines = [
        "# Milestone 15 - Task 10 - Final Closure v1",
        "",
        f"Status: `{closure['status']}`",
        f"Validation: `{validation['status']}`",
        f"Signature: `{closure['signature']}`",
        f"Baseline commit: `{closure['baseline_commit']}`",
        "",
        "## Purpose",
        "",
        "This task closes Milestone 15 after the implementation authorization chain remained blocked.",
        "",
        "The closure confirms that no explicit operator authorization was received, no implementation was performed, and no runtime path was opened.",
        "",
        "## Closure",
        "",
        f"- Closure verdict: `{closure['closure_verdict']}`",
        f"- Closure decision: `{closure['closure_decision']}`",
        f"- Block reason: `{closure['block_reason']}`",
        f"- Milestone 15 closed: `{closure['milestone_15_closed']}`",
        "",
        "## Boundary",
        "",
        f"- operator_decision_received: `{closure['operator_decision_received']}`",
        f"- explicit_operator_authorization_received: `{closure['explicit_operator_authorization_received']}`",
        f"- implementation_authorization_granted: `{closure['implementation_authorization_granted']}`",
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
    "build_milestone_15_task_10_final_closure",
    "validate_milestone_15_task_10_final_closure",
    "write_milestone_15_task_10_final_closure_artifacts",
]
