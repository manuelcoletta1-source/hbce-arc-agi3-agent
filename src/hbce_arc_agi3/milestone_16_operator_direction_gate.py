from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_16_TASK_1_OPERATOR_DIRECTION_GATE_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_DIRECTION_GATE_ONLY_LOCAL_ONLY"
GATE_STATUS = "MILESTONE_16_OPERATOR_DIRECTION_GATE_READY"
GATE_VERDICT = "MILESTONE_16_OPENED_PENDING_EXPLICIT_OPERATOR_DIRECTION"
GATE_DECISION = "WAIT_FOR_OPERATOR_DIRECTION_NO_IMPLEMENTATION_ALLOWED"
BLOCK_REASON = "MILESTONE_15_CLOSED_IMPLEMENTATION_BLOCK_ACTIVE_NO_RUNTIME_ACTIVATION"

PREVIOUS_STAGE = "MILESTONE_15_TASK_10_FINAL_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_16_TASK_2_OPERATOR_DIRECTION_RECORD_V1"

SOURCE_MILESTONE_15_FINAL_BASELINE_COMMIT = "5f80a18"
SOURCE_MILESTONE_15_FINAL_SIGNATURE = "7D901B580AA49543"
SOURCE_TASK_10_FINAL_BASELINE_COMMIT = "5f80a18"
SOURCE_TASK_10_FINAL_SIGNATURE = "7D901B580AA49543"
SOURCE_TASK_9_FINAL_BASELINE_COMMIT = "ff4aa9f"
SOURCE_TASK_9_FINAL_SIGNATURE = "3409B78DFD78F374"

OUTPUT_DIR = Path("examples/milestone-16/operator-direction-gate-v1")
DOC_PATH = Path("docs/milestone-16-operator-direction-gate-v1.md")


CHECKS = (
    "MILESTONE_15_FINAL_CLOSURE_CONFIRMED",
    "MILESTONE_16_OPENING_AS_DIRECTION_GATE_ONLY",
    "OPERATOR_DIRECTION_REQUIRED",
    "OPERATOR_DIRECTION_NOT_RECEIVED",
    "OPERATOR_AUTHORIZATION_NOT_RECEIVED",
    "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED",
    "NO_IMPLEMENTATION_AUTHORIZED",
    "NO_IMPLEMENTATION_PERFORMED",
    "NO_IMPLEMENTATION_PATCH_CREATED",
    "NO_IMPLEMENTATION_PATCH_APPLIED",
    "NO_RUNTIME_SOLVER_PATCH_ALLOWED",
    "NO_RANKER_RUNTIME_PATCH_ALLOWED",
    "NO_CANDIDATE_GENERATOR_PATCH_ALLOWED",
    "NO_RUNTIME_WIRING_ALLOWED",
    "NO_RUNTIME_WIRING_PERFORMED",
    "NO_RUNTIME_ACTIVATION_AUTHORIZED",
    "NO_RUNTIME_ACTIVATION_PERFORMED",
    "NO_RUNTIME_EXECUTION_ALLOWED",
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


def build_milestone_16_task_1_operator_direction_gate(
    *,
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    baseline = baseline_commit or _git_head()

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "gate_verdict": GATE_VERDICT,
        "gate_decision": GATE_DECISION,
        "block_reason": BLOCK_REASON,
        "checks": CHECKS,
    }

    return {
        "task_name": TASK_NAME,
        "status": TASK_READY,
        "mode": MODE,
        "gate_status": GATE_STATUS,
        "gate_verdict": GATE_VERDICT,
        "gate_decision": GATE_DECISION,
        "block_reason": BLOCK_REASON,
        "signature": _signature(seed),
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "source_milestone_15_final_baseline_commit": SOURCE_MILESTONE_15_FINAL_BASELINE_COMMIT,
        "source_milestone_15_final_signature": SOURCE_MILESTONE_15_FINAL_SIGNATURE,
        "source_task_10_final_baseline_commit": SOURCE_TASK_10_FINAL_BASELINE_COMMIT,
        "source_task_10_final_signature": SOURCE_TASK_10_FINAL_SIGNATURE,
        "source_task_9_final_baseline_commit": SOURCE_TASK_9_FINAL_BASELINE_COMMIT,
        "source_task_9_final_signature": SOURCE_TASK_9_FINAL_SIGNATURE,
        "milestone_16_opened": True,
        "milestone_16_opened_as_direction_gate_only": True,
        "milestone_16_direction_status": "PENDING_OPERATOR_DIRECTION",
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
        "milestone_16_operator_direction_gate_checks": CHECKS,
        "milestone_16_operator_direction_gate_check_count": len(CHECKS),
        "milestone_16_operator_direction_gate_failure_count": 0,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def validate_milestone_16_task_1_operator_direction_gate(
    gate: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = (
        "milestone_16_opened",
        "milestone_16_opened_as_direction_gate_only",
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
        if gate.get(key) is not True:
            issues.append(f"{key}:expected_true")

    expected_false = (
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
        if gate.get(key) is not False:
            issues.append(f"{key}:expected_false")

    expected_pairs = {
        "gate_verdict": GATE_VERDICT,
        "gate_decision": GATE_DECISION,
        "block_reason": BLOCK_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "source_milestone_15_final_baseline_commit": SOURCE_MILESTONE_15_FINAL_BASELINE_COMMIT,
        "source_milestone_15_final_signature": SOURCE_MILESTONE_15_FINAL_SIGNATURE,
        "milestone_16_direction_status": "PENDING_OPERATOR_DIRECTION",
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
    }

    for key, expected in expected_pairs.items():
        if gate.get(key) != expected:
            issues.append(f"{key}:mismatch")

    if gate.get("milestone_16_operator_direction_gate_check_count") != len(CHECKS):
        issues.append("milestone_16_operator_direction_gate_check_count_mismatch")

    if gate.get("milestone_16_operator_direction_gate_failure_count") != 0:
        issues.append("milestone_16_operator_direction_gate_failure_count_nonzero")

    return {
        "status": TASK_VALID if not issues else f"{TASK_NAME}_INVALID",
        "valid": not issues,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "issues": issues,
        "warnings": warnings,
    }


def write_milestone_16_task_1_operator_direction_gate_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-16-operator-direction-gate-v1.json"
    output_index = output_dir / "milestone-16-operator-direction-gate-index-v1.json"
    output_manifest = output_dir / "milestone-16-operator-direction-gate-manifest-v1.txt"
    output_md = output_dir / "milestone-16-operator-direction-gate-v1.md"

    gate = build_milestone_16_task_1_operator_direction_gate()
    validation = validate_milestone_16_task_1_operator_direction_gate(gate)

    payload = {
        "gate": gate,
        "validation": validation,
    }

    index = {
        "task_name": gate["task_name"],
        "status": gate["status"],
        "validation_status": validation["status"],
        "valid": validation["valid"],
        "signature": gate["signature"],
        "baseline_commit": gate["baseline_commit"],
        "previous_stage": gate["previous_stage"],
        "next_stage": gate["next_stage"],
        "gate_verdict": gate["gate_verdict"],
        "gate_decision": gate["gate_decision"],
        "milestone_16_direction_status": gate["milestone_16_direction_status"],
        "operator_direction_received": gate["operator_direction_received"],
        "implementation_authorized": gate["implementation_authorized"],
        "runtime_activation_performed": gate["runtime_activation_performed"],
        "real_submission_allowed": gate["real_submission_allowed"],
        "artifact_paths": {
            "json": str(output_json),
            "index": str(output_index),
            "manifest": str(output_manifest),
            "markdown": str(output_md),
            "doc": str(doc_path),
        },
    }

    manifest_lines = [
        f"task_name={gate['task_name']}",
        f"status={gate['status']}",
        f"validation_status={validation['status']}",
        f"valid={validation['valid']}",
        f"signature={gate['signature']}",
        f"baseline_commit={gate['baseline_commit']}",
        f"mode={gate['mode']}",
        f"gate_status={gate['gate_status']}",
        f"gate_verdict={gate['gate_verdict']}",
        f"gate_decision={gate['gate_decision']}",
        f"block_reason={gate['block_reason']}",
        f"previous_stage={gate['previous_stage']}",
        f"next_stage={gate['next_stage']}",
        f"source_milestone_15_final_baseline_commit={gate['source_milestone_15_final_baseline_commit']}",
        f"source_milestone_15_final_signature={gate['source_milestone_15_final_signature']}",
        f"milestone_16_opened={gate['milestone_16_opened']}",
        f"milestone_16_direction_status={gate['milestone_16_direction_status']}",
        f"operator_direction_required={gate['operator_direction_required']}",
        f"operator_direction_received={gate['operator_direction_received']}",
        f"operator_direction_value={gate['operator_direction_value']}",
        f"implementation_authorized={gate['implementation_authorized']}",
        f"implementation_blocked={gate['implementation_blocked']}",
        f"implementation_performed={gate['implementation_performed']}",
        f"runtime_solver_modified={gate['runtime_solver_modified']}",
        f"runtime_wiring_performed={gate['runtime_wiring_performed']}",
        f"runtime_activation_performed={gate['runtime_activation_performed']}",
        f"runtime_execution_performed={gate['runtime_execution_performed']}",
        f"real_submission_allowed={gate['real_submission_allowed']}",
        f"kaggle_submission_sent={gate['kaggle_submission_sent']}",
        f"private_core_exposure={gate['private_core_exposure']}",
        f"legal_certification={gate['legal_certification']}",
        f"milestone_16_operator_direction_gate_check_count={gate['milestone_16_operator_direction_gate_check_count']}",
        f"milestone_16_operator_direction_gate_failure_count={gate['milestone_16_operator_direction_gate_failure_count']}",
        "",
    ]

    md_lines = [
        "# Milestone 16 - Task 1 - Operator Direction Gate v1",
        "",
        f"Status: `{gate['status']}`",
        f"Validation: `{validation['status']}`",
        f"Signature: `{gate['signature']}`",
        f"Baseline commit: `{gate['baseline_commit']}`",
        "",
        "## Purpose",
        "",
        "This task opens Milestone 16 as a direction gate only.",
        "",
        "No implementation, runtime activation, runtime execution, Kaggle upload, or real submission is authorized.",
        "",
        "## Gate",
        "",
        f"- Gate verdict: `{gate['gate_verdict']}`",
        f"- Gate decision: `{gate['gate_decision']}`",
        f"- Direction status: `{gate['milestone_16_direction_status']}`",
        f"- Block reason: `{gate['block_reason']}`",
        "",
        "## Boundary",
        "",
        f"- operator_direction_required: `{gate['operator_direction_required']}`",
        f"- operator_direction_received: `{gate['operator_direction_received']}`",
        f"- implementation_authorized: `{gate['implementation_authorized']}`",
        f"- implementation_blocked: `{gate['implementation_blocked']}`",
        f"- implementation_performed: `{gate['implementation_performed']}`",
        f"- runtime_solver_modified: `{gate['runtime_solver_modified']}`",
        f"- runtime_wiring_performed: `{gate['runtime_wiring_performed']}`",
        f"- runtime_activation_performed: `{gate['runtime_activation_performed']}`",
        f"- runtime_execution_performed: `{gate['runtime_execution_performed']}`",
        f"- real_submission_allowed: `{gate['real_submission_allowed']}`",
        f"- kaggle_submission_sent: `{gate['kaggle_submission_sent']}`",
        f"- private_core_exposure: `{gate['private_core_exposure']}`",
        f"- legal_certification: `{gate['legal_certification']}`",
        "",
    ]

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text("\n".join(manifest_lines), encoding="utf-8")
    output_md.write_text("\n".join(md_lines), encoding="utf-8")
    doc_path.write_text("\n".join(md_lines), encoding="utf-8")

    return gate, validation, {
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
    "GATE_STATUS",
    "GATE_VERDICT",
    "GATE_DECISION",
    "BLOCK_REASON",
    "PREVIOUS_STAGE",
    "NEXT_STAGE",
    "build_milestone_16_task_1_operator_direction_gate",
    "validate_milestone_16_task_1_operator_direction_gate",
    "write_milestone_16_task_1_operator_direction_gate_artifacts",
]
