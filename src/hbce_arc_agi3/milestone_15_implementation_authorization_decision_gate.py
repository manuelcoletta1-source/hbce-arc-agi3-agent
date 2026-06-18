from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TASK_NAME = "MILESTONE_15_TASK_7_IMPLEMENTATION_AUTHORIZATION_DECISION_GATE_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_DECISION_GATE_ONLY_LOCAL_ONLY"
GATE_STATUS = "IMPLEMENTATION_AUTHORIZATION_DECISION_GATE_READY"
GATE_VERDICT = "IMPLEMENTATION_AUTHORIZATION_NOT_GRANTED_IMPLEMENTATION_REMAINS_BLOCKED"
GATE_DECISION = "DO_NOT_IMPLEMENT_PENDING_EXPLICIT_OPERATOR_AUTHORIZATION"
BLOCK_REASON = "TASK_6_IMPLEMENTATION_BLOCK_CONFIRMED_NO_AUTHORIZATION_RECEIVED"

PREVIOUS_STAGE = "MILESTONE_15_TASK_6_IMPLEMENTATION_BLOCK_REVIEW_GATE_V1"
NEXT_STAGE = "MILESTONE_15_TASK_8_IMPLEMENTATION_AUTHORIZATION_RECORD_V1"

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

OUTPUT_DIR = Path("examples/milestone-15/implementation-authorization-decision-gate-v1")
DOC_PATH = Path("docs/milestone-15-implementation-authorization-decision-gate-v1.md")


ImplementationAuthorizationDecisionCheck = Literal[
    "TASK_6_IMPLEMENTATION_BLOCK_REVIEW_CONFIRMED",
    "TASK_5_RUNTIME_ACTIVATION_REVIEW_CONFIRMED",
    "TASK_4_RUNTIME_ACTIVATION_BOUNDARY_CONFIRMED",
    "TASK_3_AUTHORIZATION_BOUNDARY_CONFIRMED",
    "TASK_2_OPERATOR_DECISION_RECORD_CONFIRMED",
    "TASK_1_OPERATOR_DECISION_GATE_CONFIRMED",
    "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
    "OPERATOR_DECISION_REQUIRED",
    "OPERATOR_DECISION_STILL_PENDING",
    "EXPLICIT_OPERATOR_AUTHORIZATION_REQUIRED",
    "EXPLICIT_OPERATOR_AUTHORIZATION_NOT_RECEIVED",
    "IMPLEMENTATION_AUTHORIZATION_DECISION_REQUIRED",
    "IMPLEMENTATION_AUTHORIZATION_DECISION_NOT_RECEIVED",
    "IMPLEMENTATION_AUTHORIZATION_NOT_GRANTED",
    "IMPLEMENTATION_REMAINS_BLOCKED",
    "NO_RUNTIME_SOLVER_PATCH_ALLOWED",
    "NO_RUNTIME_WIRING_ALLOWED",
    "NO_RUNTIME_EXECUTION_ALLOWED",
    "NO_REAL_SUBMISSION_ALLOWED",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
]


@dataclass(frozen=True)
class Milestone15Task7ImplementationAuthorizationDecisionGate:
    task_name: str
    status: str
    mode: str
    gate_status: str
    gate_verdict: str
    gate_decision: str
    block_reason: str
    signature: str
    baseline_commit: str

    previous_stage: str
    next_stage: str

    source_task_6_final_baseline_commit: str
    source_task_6_final_signature: str
    source_task_5_final_baseline_commit: str
    source_task_5_final_signature: str
    source_task_4_final_baseline_commit: str
    source_task_4_final_signature: str
    source_task_3_final_baseline_commit: str
    source_task_3_final_signature: str
    source_task_2_final_baseline_commit: str
    source_task_2_final_signature: str
    source_task_1_final_baseline_commit: str
    source_task_1_final_signature: str
    source_milestone_14_final_baseline_commit: str
    source_milestone_14_final_signature: str

    implementation_authorization_decision_gate_created: bool
    task_6_implementation_block_confirmed: bool
    task_5_runtime_activation_review_confirmed: bool
    task_4_runtime_activation_boundary_confirmed: bool

    operator_decision_required: bool
    operator_decision_received: bool
    operator_decision_value: str

    explicit_operator_authorization_required: bool
    explicit_operator_authorization_received: bool
    explicit_operator_authorization_value: str

    implementation_authorization_decision_required: bool
    implementation_authorization_decision_received: bool
    implementation_authorization_decision_value: str
    implementation_authorization_granted: bool
    implementation_authorized: bool
    implementation_blocked: bool
    implementation_performed: bool
    implementation_patch_created: bool
    implementation_patch_applied: bool

    runtime_solver_patch_allowed: bool
    runtime_solver_modified: bool
    ranker_runtime_patch_allowed: bool
    ranker_runtime_modified: bool
    candidate_generator_patch_allowed: bool
    candidate_generator_modified: bool
    runtime_wiring_allowed: bool
    runtime_wiring_performed: bool

    runtime_activation_authorized: bool
    runtime_activation_blocked: bool
    runtime_activation_performed: bool
    runtime_execution_allowed: bool
    runtime_execution_performed: bool

    real_evaluation_performed: bool
    real_submission_allowed: bool
    ready_for_real_kaggle_submission: bool
    manual_upload_allowed: bool
    kaggle_authentication_allowed: bool
    kaggle_authentication_performed: bool
    kaggle_upload_allowed: bool
    kaggle_upload_performed: bool
    kaggle_submission_sent: bool

    external_api_dependency: bool
    internet_during_eval: bool
    private_core_exposure: bool
    legal_certification: bool
    official_score_claim_allowed: bool
    competitive_score_claim_allowed: bool
    public_overfit_allowed: bool
    public_overfit_guard_required: bool
    fail_closed_required: bool
    fail_closed_active: bool
    public_safe: bool
    deterministic: bool
    local_only: bool

    implementation_authorization_decision_checks: tuple[ImplementationAuthorizationDecisionCheck, ...]
    implementation_authorization_decision_check_count: int
    implementation_authorization_decision_failure_count: int
    created_at_utc: str


@dataclass(frozen=True)
class ValidationResult:
    status: str
    valid: bool
    issue_count: int
    warning_count: int
    issues: list[str]
    warnings: list[str]


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


def _signature(seed: dict[str, object]) -> str:
    canonical = json.dumps(seed, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16].upper()


def build_milestone_15_task_7_implementation_authorization_decision_gate(
    *,
    baseline_commit: str | None = None,
) -> Milestone15Task7ImplementationAuthorizationDecisionGate:
    baseline = baseline_commit or _git_head()

    checks: tuple[ImplementationAuthorizationDecisionCheck, ...] = (
        "TASK_6_IMPLEMENTATION_BLOCK_REVIEW_CONFIRMED",
        "TASK_5_RUNTIME_ACTIVATION_REVIEW_CONFIRMED",
        "TASK_4_RUNTIME_ACTIVATION_BOUNDARY_CONFIRMED",
        "TASK_3_AUTHORIZATION_BOUNDARY_CONFIRMED",
        "TASK_2_OPERATOR_DECISION_RECORD_CONFIRMED",
        "TASK_1_OPERATOR_DECISION_GATE_CONFIRMED",
        "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
        "OPERATOR_DECISION_REQUIRED",
        "OPERATOR_DECISION_STILL_PENDING",
        "EXPLICIT_OPERATOR_AUTHORIZATION_REQUIRED",
        "EXPLICIT_OPERATOR_AUTHORIZATION_NOT_RECEIVED",
        "IMPLEMENTATION_AUTHORIZATION_DECISION_REQUIRED",
        "IMPLEMENTATION_AUTHORIZATION_DECISION_NOT_RECEIVED",
        "IMPLEMENTATION_AUTHORIZATION_NOT_GRANTED",
        "IMPLEMENTATION_REMAINS_BLOCKED",
        "NO_RUNTIME_SOLVER_PATCH_ALLOWED",
        "NO_RUNTIME_WIRING_ALLOWED",
        "NO_RUNTIME_EXECUTION_ALLOWED",
        "NO_REAL_SUBMISSION_ALLOWED",
        "FAIL_CLOSED_ACTIVE",
        "PUBLIC_SAFE_BOUNDARY_PRESERVED",
    )

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "gate_verdict": GATE_VERDICT,
        "gate_decision": GATE_DECISION,
        "block_reason": BLOCK_REASON,
        "checks": checks,
    }

    return Milestone15Task7ImplementationAuthorizationDecisionGate(
        task_name=TASK_NAME,
        status=TASK_READY,
        mode=MODE,
        gate_status=GATE_STATUS,
        gate_verdict=GATE_VERDICT,
        gate_decision=GATE_DECISION,
        block_reason=BLOCK_REASON,
        signature=_signature(seed),
        baseline_commit=baseline,
        previous_stage=PREVIOUS_STAGE,
        next_stage=NEXT_STAGE,
        source_task_6_final_baseline_commit=SOURCE_TASK_6_FINAL_BASELINE_COMMIT,
        source_task_6_final_signature=SOURCE_TASK_6_FINAL_SIGNATURE,
        source_task_5_final_baseline_commit=SOURCE_TASK_5_FINAL_BASELINE_COMMIT,
        source_task_5_final_signature=SOURCE_TASK_5_FINAL_SIGNATURE,
        source_task_4_final_baseline_commit=SOURCE_TASK_4_FINAL_BASELINE_COMMIT,
        source_task_4_final_signature=SOURCE_TASK_4_FINAL_SIGNATURE,
        source_task_3_final_baseline_commit=SOURCE_TASK_3_FINAL_BASELINE_COMMIT,
        source_task_3_final_signature=SOURCE_TASK_3_FINAL_SIGNATURE,
        source_task_2_final_baseline_commit=SOURCE_TASK_2_FINAL_BASELINE_COMMIT,
        source_task_2_final_signature=SOURCE_TASK_2_FINAL_SIGNATURE,
        source_task_1_final_baseline_commit=SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
        source_task_1_final_signature=SOURCE_TASK_1_FINAL_SIGNATURE,
        source_milestone_14_final_baseline_commit=SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT,
        source_milestone_14_final_signature=SOURCE_MILESTONE_14_FINAL_SIGNATURE,
        implementation_authorization_decision_gate_created=True,
        task_6_implementation_block_confirmed=True,
        task_5_runtime_activation_review_confirmed=True,
        task_4_runtime_activation_boundary_confirmed=True,
        operator_decision_required=True,
        operator_decision_received=False,
        operator_decision_value="PENDING_EXPLICIT_OPERATOR_DECISION",
        explicit_operator_authorization_required=True,
        explicit_operator_authorization_received=False,
        explicit_operator_authorization_value="NO_EXPLICIT_OPERATOR_AUTHORIZATION_RECEIVED",
        implementation_authorization_decision_required=True,
        implementation_authorization_decision_received=False,
        implementation_authorization_decision_value="PENDING_EXPLICIT_OPERATOR_AUTHORIZATION",
        implementation_authorization_granted=False,
        implementation_authorized=False,
        implementation_blocked=True,
        implementation_performed=False,
        implementation_patch_created=False,
        implementation_patch_applied=False,
        runtime_solver_patch_allowed=False,
        runtime_solver_modified=False,
        ranker_runtime_patch_allowed=False,
        ranker_runtime_modified=False,
        candidate_generator_patch_allowed=False,
        candidate_generator_modified=False,
        runtime_wiring_allowed=False,
        runtime_wiring_performed=False,
        runtime_activation_authorized=False,
        runtime_activation_blocked=True,
        runtime_activation_performed=False,
        runtime_execution_allowed=False,
        runtime_execution_performed=False,
        real_evaluation_performed=False,
        real_submission_allowed=False,
        ready_for_real_kaggle_submission=False,
        manual_upload_allowed=False,
        kaggle_authentication_allowed=False,
        kaggle_authentication_performed=False,
        kaggle_upload_allowed=False,
        kaggle_upload_performed=False,
        kaggle_submission_sent=False,
        external_api_dependency=False,
        internet_during_eval=False,
        private_core_exposure=False,
        legal_certification=False,
        official_score_claim_allowed=False,
        competitive_score_claim_allowed=False,
        public_overfit_allowed=False,
        public_overfit_guard_required=True,
        fail_closed_required=True,
        fail_closed_active=True,
        public_safe=True,
        deterministic=True,
        local_only=True,
        implementation_authorization_decision_checks=checks,
        implementation_authorization_decision_check_count=len(checks),
        implementation_authorization_decision_failure_count=0,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_15_task_7_implementation_authorization_decision_gate(
    gate: Milestone15Task7ImplementationAuthorizationDecisionGate,
) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = {
        "implementation_authorization_decision_gate_created": gate.implementation_authorization_decision_gate_created,
        "task_6_implementation_block_confirmed": gate.task_6_implementation_block_confirmed,
        "task_5_runtime_activation_review_confirmed": gate.task_5_runtime_activation_review_confirmed,
        "task_4_runtime_activation_boundary_confirmed": gate.task_4_runtime_activation_boundary_confirmed,
        "operator_decision_required": gate.operator_decision_required,
        "explicit_operator_authorization_required": gate.explicit_operator_authorization_required,
        "implementation_authorization_decision_required": gate.implementation_authorization_decision_required,
        "implementation_blocked": gate.implementation_blocked,
        "runtime_activation_blocked": gate.runtime_activation_blocked,
        "public_overfit_guard_required": gate.public_overfit_guard_required,
        "fail_closed_required": gate.fail_closed_required,
        "fail_closed_active": gate.fail_closed_active,
        "public_safe": gate.public_safe,
        "deterministic": gate.deterministic,
        "local_only": gate.local_only,
    }

    for key, value in expected_true.items():
        if value is not True:
            issues.append(f"{key}:expected_true")

    expected_false = {
        "operator_decision_received": gate.operator_decision_received,
        "explicit_operator_authorization_received": gate.explicit_operator_authorization_received,
        "implementation_authorization_decision_received": gate.implementation_authorization_decision_received,
        "implementation_authorization_granted": gate.implementation_authorization_granted,
        "implementation_authorized": gate.implementation_authorized,
        "implementation_performed": gate.implementation_performed,
        "implementation_patch_created": gate.implementation_patch_created,
        "implementation_patch_applied": gate.implementation_patch_applied,
        "runtime_solver_patch_allowed": gate.runtime_solver_patch_allowed,
        "runtime_solver_modified": gate.runtime_solver_modified,
        "ranker_runtime_patch_allowed": gate.ranker_runtime_patch_allowed,
        "ranker_runtime_modified": gate.ranker_runtime_modified,
        "candidate_generator_patch_allowed": gate.candidate_generator_patch_allowed,
        "candidate_generator_modified": gate.candidate_generator_modified,
        "runtime_wiring_allowed": gate.runtime_wiring_allowed,
        "runtime_wiring_performed": gate.runtime_wiring_performed,
        "runtime_activation_authorized": gate.runtime_activation_authorized,
        "runtime_activation_performed": gate.runtime_activation_performed,
        "runtime_execution_allowed": gate.runtime_execution_allowed,
        "runtime_execution_performed": gate.runtime_execution_performed,
        "real_evaluation_performed": gate.real_evaluation_performed,
        "real_submission_allowed": gate.real_submission_allowed,
        "ready_for_real_kaggle_submission": gate.ready_for_real_kaggle_submission,
        "manual_upload_allowed": gate.manual_upload_allowed,
        "kaggle_authentication_allowed": gate.kaggle_authentication_allowed,
        "kaggle_authentication_performed": gate.kaggle_authentication_performed,
        "kaggle_upload_allowed": gate.kaggle_upload_allowed,
        "kaggle_upload_performed": gate.kaggle_upload_performed,
        "kaggle_submission_sent": gate.kaggle_submission_sent,
        "external_api_dependency": gate.external_api_dependency,
        "internet_during_eval": gate.internet_during_eval,
        "private_core_exposure": gate.private_core_exposure,
        "legal_certification": gate.legal_certification,
        "official_score_claim_allowed": gate.official_score_claim_allowed,
        "competitive_score_claim_allowed": gate.competitive_score_claim_allowed,
        "public_overfit_allowed": gate.public_overfit_allowed,
    }

    for key, value in expected_false.items():
        if value is not False:
            issues.append(f"{key}:expected_false")

    if gate.gate_verdict != GATE_VERDICT:
        issues.append("gate_verdict_mismatch")

    if gate.gate_decision != GATE_DECISION:
        issues.append("gate_decision_mismatch")

    if gate.block_reason != BLOCK_REASON:
        issues.append("block_reason_mismatch")

    if gate.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage_mismatch")

    if gate.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    if gate.operator_decision_value != "PENDING_EXPLICIT_OPERATOR_DECISION":
        issues.append("operator_decision_value_mismatch")

    if gate.explicit_operator_authorization_value != "NO_EXPLICIT_OPERATOR_AUTHORIZATION_RECEIVED":
        issues.append("explicit_operator_authorization_value_mismatch")

    if gate.implementation_authorization_decision_value != "PENDING_EXPLICIT_OPERATOR_AUTHORIZATION":
        issues.append("implementation_authorization_decision_value_mismatch")

    if gate.implementation_authorization_decision_check_count != len(gate.implementation_authorization_decision_checks):
        issues.append("implementation_authorization_decision_check_count_mismatch")

    if gate.implementation_authorization_decision_failure_count != 0:
        issues.append("implementation_authorization_decision_failure_count_nonzero")

    status = TASK_VALID if not issues else f"{TASK_NAME}_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_15_task_7_implementation_authorization_decision_gate_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[Milestone15Task7ImplementationAuthorizationDecisionGate, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-15-implementation-authorization-decision-gate-v1.json"
    output_index = output_dir / "milestone-15-implementation-authorization-decision-gate-index-v1.json"
    output_manifest = output_dir / "milestone-15-implementation-authorization-decision-gate-manifest-v1.txt"
    output_md = output_dir / "milestone-15-implementation-authorization-decision-gate-v1.md"

    gate = build_milestone_15_task_7_implementation_authorization_decision_gate()
    validation = validate_milestone_15_task_7_implementation_authorization_decision_gate(gate)

    payload = {
        "record": asdict(gate),
        "validation": asdict(validation),
    }

    index = {
        "task_name": gate.task_name,
        "status": gate.status,
        "validation_status": validation.status,
        "valid": validation.valid,
        "signature": gate.signature,
        "baseline_commit": gate.baseline_commit,
        "previous_stage": gate.previous_stage,
        "next_stage": gate.next_stage,
        "gate_verdict": gate.gate_verdict,
        "gate_decision": gate.gate_decision,
        "implementation_authorization_granted": gate.implementation_authorization_granted,
        "implementation_authorized": gate.implementation_authorized,
        "implementation_performed": gate.implementation_performed,
        "runtime_solver_modified": gate.runtime_solver_modified,
        "runtime_wiring_performed": gate.runtime_wiring_performed,
        "artifact_paths": {
            "json": str(output_json),
            "index": str(output_index),
            "manifest": str(output_manifest),
            "markdown": str(output_md),
            "doc": str(doc_path),
        },
    }

    manifest = "\n".join(
        [
            f"task_name={gate.task_name}",
            f"status={gate.status}",
            f"validation_status={validation.status}",
            f"valid={validation.valid}",
            f"signature={gate.signature}",
            f"baseline_commit={gate.baseline_commit}",
            f"mode={gate.mode}",
            f"gate_status={gate.gate_status}",
            f"gate_verdict={gate.gate_verdict}",
            f"gate_decision={gate.gate_decision}",
            f"block_reason={gate.block_reason}",
            f"previous_stage={gate.previous_stage}",
            f"next_stage={gate.next_stage}",
            f"source_task_6_final_baseline_commit={gate.source_task_6_final_baseline_commit}",
            f"source_task_6_final_signature={gate.source_task_6_final_signature}",
            f"operator_decision_required={gate.operator_decision_required}",
            f"operator_decision_received={gate.operator_decision_received}",
            f"operator_decision_value={gate.operator_decision_value}",
            f"explicit_operator_authorization_required={gate.explicit_operator_authorization_required}",
            f"explicit_operator_authorization_received={gate.explicit_operator_authorization_received}",
            f"implementation_authorization_decision_required={gate.implementation_authorization_decision_required}",
            f"implementation_authorization_decision_received={gate.implementation_authorization_decision_received}",
            f"implementation_authorization_decision_value={gate.implementation_authorization_decision_value}",
            f"implementation_authorization_granted={gate.implementation_authorization_granted}",
            f"implementation_authorized={gate.implementation_authorized}",
            f"implementation_blocked={gate.implementation_blocked}",
            f"implementation_performed={gate.implementation_performed}",
            f"implementation_patch_created={gate.implementation_patch_created}",
            f"implementation_patch_applied={gate.implementation_patch_applied}",
            f"runtime_solver_patch_allowed={gate.runtime_solver_patch_allowed}",
            f"runtime_solver_modified={gate.runtime_solver_modified}",
            f"runtime_wiring_allowed={gate.runtime_wiring_allowed}",
            f"runtime_wiring_performed={gate.runtime_wiring_performed}",
            f"runtime_activation_authorized={gate.runtime_activation_authorized}",
            f"runtime_activation_performed={gate.runtime_activation_performed}",
            f"runtime_execution_allowed={gate.runtime_execution_allowed}",
            f"runtime_execution_performed={gate.runtime_execution_performed}",
            f"real_submission_allowed={gate.real_submission_allowed}",
            f"legal_certification={gate.legal_certification}",
            f"implementation_authorization_decision_check_count={gate.implementation_authorization_decision_check_count}",
            f"implementation_authorization_decision_failure_count={gate.implementation_authorization_decision_failure_count}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 15 - Task 7 - Implementation Authorization Decision Gate v1",
            "",
            f"Status: `{gate.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{gate.signature}`",
            f"Baseline commit: `{gate.baseline_commit}`",
            "",
            "## Purpose",
            "",
            "This task formalizes the implementation authorization decision gate after Task 6.",
            "",
            "No explicit operator authorization has been received; therefore implementation remains blocked.",
            "",
            "## Decision",
            "",
            f"- Gate verdict: `{gate.gate_verdict}`",
            f"- Gate decision: `{gate.gate_decision}`",
            f"- Block reason: `{gate.block_reason}`",
            f"- Operator decision value: `{gate.operator_decision_value}`",
            f"- Implementation authorization decision value: `{gate.implementation_authorization_decision_value}`",
            "",
            "## Boundary",
            "",
            f"- task_6_implementation_block_confirmed: `{gate.task_6_implementation_block_confirmed}`",
            f"- explicit_operator_authorization_received: `{gate.explicit_operator_authorization_received}`",
            f"- implementation_authorization_granted: `{gate.implementation_authorization_granted}`",
            f"- implementation_authorized: `{gate.implementation_authorized}`",
            f"- implementation_blocked: `{gate.implementation_blocked}`",
            f"- implementation_performed: `{gate.implementation_performed}`",
            f"- implementation_patch_created: `{gate.implementation_patch_created}`",
            f"- implementation_patch_applied: `{gate.implementation_patch_applied}`",
            f"- runtime_solver_patch_allowed: `{gate.runtime_solver_patch_allowed}`",
            f"- runtime_solver_modified: `{gate.runtime_solver_modified}`",
            f"- runtime_wiring_allowed: `{gate.runtime_wiring_allowed}`",
            f"- runtime_wiring_performed: `{gate.runtime_wiring_performed}`",
            f"- runtime_activation_performed: `{gate.runtime_activation_performed}`",
            f"- runtime_execution_performed: `{gate.runtime_execution_performed}`",
            f"- real_submission_allowed: `{gate.real_submission_allowed}`",
            f"- legal_certification: `{gate.legal_certification}`",
            "",
        ]
    )

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text(manifest, encoding="utf-8")
    output_md.write_text(md, encoding="utf-8")
    doc_path.write_text(md, encoding="utf-8")

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
    "Milestone15Task7ImplementationAuthorizationDecisionGate",
    "ValidationResult",
    "build_milestone_15_task_7_implementation_authorization_decision_gate",
    "validate_milestone_15_task_7_implementation_authorization_decision_gate",
    "write_milestone_15_task_7_implementation_authorization_decision_gate_artifacts",
]
