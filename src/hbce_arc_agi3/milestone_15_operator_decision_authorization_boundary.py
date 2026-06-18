from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TASK_NAME = "MILESTONE_15_TASK_3_OPERATOR_DECISION_AUTHORIZATION_BOUNDARY_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_AUTHORIZATION_BOUNDARY_ONLY_LOCAL_ONLY"
BOUNDARY_STATUS = "OPERATOR_DECISION_AUTHORIZATION_BOUNDARY_READY"
BOUNDARY_VERDICT = "PENDING_OPERATOR_DECISION_DOES_NOT_AUTHORIZE_IMPLEMENTATION"
BOUNDARY_DECISION = "KEEP_IMPLEMENTATION_AND_RUNTIME_BLOCKED"
BLOCK_REASON = "OPERATOR_DECISION_PENDING_NO_AUTHORIZATION_GRANTED"

PREVIOUS_STAGE = "MILESTONE_15_TASK_2_OPERATOR_DECISION_RECORD_V1"
SOURCE_TASK_1_STAGE = "MILESTONE_15_TASK_1_EXPLICIT_OPERATOR_DECISION_GATE_V1"
SOURCE_MILESTONE_14_FINAL_CLOSURE = "MILESTONE_14_CLOSED_WITHOUT_RUNTIME_ACTIVATION"
NEXT_STAGE = "MILESTONE_15_TASK_4_RUNTIME_ACTIVATION_AUTHORIZATION_BOUNDARY_V1"

SOURCE_TASK_2_FINAL_BASELINE_COMMIT = "7cd11c0"
SOURCE_TASK_2_FINAL_SIGNATURE = "92DD45142240063F"
SOURCE_TASK_1_FINAL_BASELINE_COMMIT = "ed48f9c"
SOURCE_TASK_1_FINAL_SIGNATURE = "22CAADB16533FB69"
SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT = "f7ee729"
SOURCE_MILESTONE_14_FINAL_SIGNATURE = "05F1CDD559B63B8C"

OUTPUT_DIR = Path("examples/milestone-15/operator-decision-authorization-boundary-v1")
DOC_PATH = Path("docs/milestone-15-operator-decision-authorization-boundary-v1.md")


AuthorizationBoundaryCheck = Literal[
    "TASK_2_OPERATOR_DECISION_RECORD_CONFIRMED",
    "TASK_1_DECISION_GATE_CONFIRMED",
    "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
    "OPERATOR_DECISION_REQUIRED",
    "OPERATOR_DECISION_PENDING",
    "PENDING_DECISION_NOT_AUTHORIZATION",
    "NO_IMPLICIT_AUTHORIZATION",
    "IMPLEMENTATION_REMAINS_BLOCKED",
    "RUNTIME_ACTIVATION_REMAINS_BLOCKED",
    "REAL_SUBMISSION_REMAINS_BLOCKED",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
]


@dataclass(frozen=True)
class Milestone15Task3AuthorizationBoundary:
    task_name: str
    status: str
    mode: str
    boundary_status: str
    boundary_verdict: str
    boundary_decision: str
    block_reason: str
    signature: str
    baseline_commit: str

    previous_stage: str
    source_task_1_stage: str
    source_milestone_14_final_closure: str
    next_stage: str

    source_task_2_final_baseline_commit: str
    source_task_2_final_signature: str
    source_task_1_final_baseline_commit: str
    source_task_1_final_signature: str
    source_milestone_14_final_baseline_commit: str
    source_milestone_14_final_signature: str

    authorization_boundary_created: bool
    operator_decision_required: bool
    operator_decision_received: bool
    operator_decision_value: str
    operator_decision_recorded: bool
    pending_decision_is_authorization: bool
    operator_decision_authorizes_implementation: bool
    explicit_authorization_required: bool
    explicit_authorization_received: bool
    no_implicit_authorization: bool

    implementation_authorized: bool
    implementation_blocked: bool
    runtime_activation_authorized: bool
    runtime_activation_performed: bool
    runtime_execution_performed: bool
    runtime_solver_modified: bool
    ranker_runtime_modified: bool
    candidate_generator_modified: bool
    implementation_performed: bool

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

    authorization_boundary_checks: tuple[AuthorizationBoundaryCheck, ...]
    authorization_boundary_check_count: int
    authorization_boundary_failure_count: int
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


def build_milestone_15_task_3_authorization_boundary(
    *,
    baseline_commit: str | None = None,
) -> Milestone15Task3AuthorizationBoundary:
    baseline = baseline_commit or _git_head()

    checks: tuple[AuthorizationBoundaryCheck, ...] = (
        "TASK_2_OPERATOR_DECISION_RECORD_CONFIRMED",
        "TASK_1_DECISION_GATE_CONFIRMED",
        "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
        "OPERATOR_DECISION_REQUIRED",
        "OPERATOR_DECISION_PENDING",
        "PENDING_DECISION_NOT_AUTHORIZATION",
        "NO_IMPLICIT_AUTHORIZATION",
        "IMPLEMENTATION_REMAINS_BLOCKED",
        "RUNTIME_ACTIVATION_REMAINS_BLOCKED",
        "REAL_SUBMISSION_REMAINS_BLOCKED",
        "FAIL_CLOSED_ACTIVE",
        "PUBLIC_SAFE_BOUNDARY_PRESERVED",
    )

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "boundary_verdict": BOUNDARY_VERDICT,
        "boundary_decision": BOUNDARY_DECISION,
        "block_reason": BLOCK_REASON,
        "checks": checks,
    }

    return Milestone15Task3AuthorizationBoundary(
        task_name=TASK_NAME,
        status=TASK_READY,
        mode=MODE,
        boundary_status=BOUNDARY_STATUS,
        boundary_verdict=BOUNDARY_VERDICT,
        boundary_decision=BOUNDARY_DECISION,
        block_reason=BLOCK_REASON,
        signature=_signature(seed),
        baseline_commit=baseline,
        previous_stage=PREVIOUS_STAGE,
        source_task_1_stage=SOURCE_TASK_1_STAGE,
        source_milestone_14_final_closure=SOURCE_MILESTONE_14_FINAL_CLOSURE,
        next_stage=NEXT_STAGE,
        source_task_2_final_baseline_commit=SOURCE_TASK_2_FINAL_BASELINE_COMMIT,
        source_task_2_final_signature=SOURCE_TASK_2_FINAL_SIGNATURE,
        source_task_1_final_baseline_commit=SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
        source_task_1_final_signature=SOURCE_TASK_1_FINAL_SIGNATURE,
        source_milestone_14_final_baseline_commit=SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT,
        source_milestone_14_final_signature=SOURCE_MILESTONE_14_FINAL_SIGNATURE,
        authorization_boundary_created=True,
        operator_decision_required=True,
        operator_decision_received=False,
        operator_decision_value="PENDING_EXPLICIT_OPERATOR_DECISION",
        operator_decision_recorded=False,
        pending_decision_is_authorization=False,
        operator_decision_authorizes_implementation=False,
        explicit_authorization_required=True,
        explicit_authorization_received=False,
        no_implicit_authorization=True,
        implementation_authorized=False,
        implementation_blocked=True,
        runtime_activation_authorized=False,
        runtime_activation_performed=False,
        runtime_execution_performed=False,
        runtime_solver_modified=False,
        ranker_runtime_modified=False,
        candidate_generator_modified=False,
        implementation_performed=False,
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
        authorization_boundary_checks=checks,
        authorization_boundary_check_count=len(checks),
        authorization_boundary_failure_count=0,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_15_task_3_authorization_boundary(
    boundary: Milestone15Task3AuthorizationBoundary,
) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = {
        "authorization_boundary_created": boundary.authorization_boundary_created,
        "operator_decision_required": boundary.operator_decision_required,
        "explicit_authorization_required": boundary.explicit_authorization_required,
        "no_implicit_authorization": boundary.no_implicit_authorization,
        "implementation_blocked": boundary.implementation_blocked,
        "public_overfit_guard_required": boundary.public_overfit_guard_required,
        "fail_closed_required": boundary.fail_closed_required,
        "fail_closed_active": boundary.fail_closed_active,
        "public_safe": boundary.public_safe,
        "deterministic": boundary.deterministic,
        "local_only": boundary.local_only,
    }

    for key, value in expected_true.items():
        if value is not True:
            issues.append(f"{key}:expected_true")

    expected_false = {
        "operator_decision_received": boundary.operator_decision_received,
        "operator_decision_recorded": boundary.operator_decision_recorded,
        "pending_decision_is_authorization": boundary.pending_decision_is_authorization,
        "operator_decision_authorizes_implementation": boundary.operator_decision_authorizes_implementation,
        "explicit_authorization_received": boundary.explicit_authorization_received,
        "implementation_authorized": boundary.implementation_authorized,
        "runtime_activation_authorized": boundary.runtime_activation_authorized,
        "runtime_activation_performed": boundary.runtime_activation_performed,
        "runtime_execution_performed": boundary.runtime_execution_performed,
        "runtime_solver_modified": boundary.runtime_solver_modified,
        "ranker_runtime_modified": boundary.ranker_runtime_modified,
        "candidate_generator_modified": boundary.candidate_generator_modified,
        "implementation_performed": boundary.implementation_performed,
        "real_evaluation_performed": boundary.real_evaluation_performed,
        "real_submission_allowed": boundary.real_submission_allowed,
        "ready_for_real_kaggle_submission": boundary.ready_for_real_kaggle_submission,
        "manual_upload_allowed": boundary.manual_upload_allowed,
        "kaggle_authentication_allowed": boundary.kaggle_authentication_allowed,
        "kaggle_authentication_performed": boundary.kaggle_authentication_performed,
        "kaggle_upload_allowed": boundary.kaggle_upload_allowed,
        "kaggle_upload_performed": boundary.kaggle_upload_performed,
        "kaggle_submission_sent": boundary.kaggle_submission_sent,
        "external_api_dependency": boundary.external_api_dependency,
        "internet_during_eval": boundary.internet_during_eval,
        "private_core_exposure": boundary.private_core_exposure,
        "legal_certification": boundary.legal_certification,
        "official_score_claim_allowed": boundary.official_score_claim_allowed,
        "competitive_score_claim_allowed": boundary.competitive_score_claim_allowed,
        "public_overfit_allowed": boundary.public_overfit_allowed,
    }

    for key, value in expected_false.items():
        if value is not False:
            issues.append(f"{key}:expected_false")

    if boundary.boundary_verdict != BOUNDARY_VERDICT:
        issues.append("boundary_verdict_mismatch")

    if boundary.boundary_decision != BOUNDARY_DECISION:
        issues.append("boundary_decision_mismatch")

    if boundary.block_reason != BLOCK_REASON:
        issues.append("block_reason_mismatch")

    if boundary.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage_mismatch")

    if boundary.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    if boundary.operator_decision_value != "PENDING_EXPLICIT_OPERATOR_DECISION":
        issues.append("operator_decision_value_mismatch")

    if boundary.authorization_boundary_check_count != len(boundary.authorization_boundary_checks):
        issues.append("authorization_boundary_check_count_mismatch")

    if boundary.authorization_boundary_failure_count != 0:
        issues.append("authorization_boundary_failure_count_nonzero")

    status = TASK_VALID if not issues else f"{TASK_NAME}_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_15_task_3_authorization_boundary_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[Milestone15Task3AuthorizationBoundary, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-15-operator-decision-authorization-boundary-v1.json"
    output_index = output_dir / "milestone-15-operator-decision-authorization-boundary-index-v1.json"
    output_manifest = output_dir / "milestone-15-operator-decision-authorization-boundary-manifest-v1.txt"
    output_md = output_dir / "milestone-15-operator-decision-authorization-boundary-v1.md"

    boundary = build_milestone_15_task_3_authorization_boundary()
    validation = validate_milestone_15_task_3_authorization_boundary(boundary)

    payload = {
        "record": asdict(boundary),
        "validation": asdict(validation),
    }

    index = {
        "task_name": boundary.task_name,
        "status": boundary.status,
        "validation_status": validation.status,
        "valid": validation.valid,
        "signature": boundary.signature,
        "baseline_commit": boundary.baseline_commit,
        "previous_stage": boundary.previous_stage,
        "next_stage": boundary.next_stage,
        "boundary_verdict": boundary.boundary_verdict,
        "boundary_decision": boundary.boundary_decision,
        "operator_decision_value": boundary.operator_decision_value,
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
            f"task_name={boundary.task_name}",
            f"status={boundary.status}",
            f"validation_status={validation.status}",
            f"valid={validation.valid}",
            f"signature={boundary.signature}",
            f"baseline_commit={boundary.baseline_commit}",
            f"mode={boundary.mode}",
            f"boundary_status={boundary.boundary_status}",
            f"boundary_verdict={boundary.boundary_verdict}",
            f"boundary_decision={boundary.boundary_decision}",
            f"block_reason={boundary.block_reason}",
            f"previous_stage={boundary.previous_stage}",
            f"next_stage={boundary.next_stage}",
            f"source_task_2_final_baseline_commit={boundary.source_task_2_final_baseline_commit}",
            f"source_task_2_final_signature={boundary.source_task_2_final_signature}",
            f"operator_decision_required={boundary.operator_decision_required}",
            f"operator_decision_received={boundary.operator_decision_received}",
            f"operator_decision_value={boundary.operator_decision_value}",
            f"pending_decision_is_authorization={boundary.pending_decision_is_authorization}",
            f"operator_decision_authorizes_implementation={boundary.operator_decision_authorizes_implementation}",
            f"explicit_authorization_required={boundary.explicit_authorization_required}",
            f"explicit_authorization_received={boundary.explicit_authorization_received}",
            f"implementation_authorized={boundary.implementation_authorized}",
            f"implementation_blocked={boundary.implementation_blocked}",
            f"runtime_activation_authorized={boundary.runtime_activation_authorized}",
            f"runtime_activation_performed={boundary.runtime_activation_performed}",
            f"implementation_performed={boundary.implementation_performed}",
            f"real_submission_allowed={boundary.real_submission_allowed}",
            f"legal_certification={boundary.legal_certification}",
            f"authorization_boundary_check_count={boundary.authorization_boundary_check_count}",
            f"authorization_boundary_failure_count={boundary.authorization_boundary_failure_count}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 15 - Task 3 - Operator Decision Authorization Boundary v1",
            "",
            f"Status: `{boundary.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{boundary.signature}`",
            f"Baseline commit: `{boundary.baseline_commit}`",
            "",
            "## Purpose",
            "",
            "This task formalizes that a pending operator decision does not authorize implementation.",
            "",
            "No implicit authorization is created by the absence of a decision.",
            "",
            "## Boundary decision",
            "",
            f"- Boundary verdict: `{boundary.boundary_verdict}`",
            f"- Boundary decision: `{boundary.boundary_decision}`",
            f"- Block reason: `{boundary.block_reason}`",
            f"- Operator decision value: `{boundary.operator_decision_value}`",
            "",
            "## Boundary",
            "",
            f"- pending_decision_is_authorization: `{boundary.pending_decision_is_authorization}`",
            f"- operator_decision_authorizes_implementation: `{boundary.operator_decision_authorizes_implementation}`",
            f"- explicit_authorization_required: `{boundary.explicit_authorization_required}`",
            f"- explicit_authorization_received: `{boundary.explicit_authorization_received}`",
            f"- implementation_authorized: `{boundary.implementation_authorized}`",
            f"- implementation_blocked: `{boundary.implementation_blocked}`",
            f"- runtime_activation_authorized: `{boundary.runtime_activation_authorized}`",
            f"- runtime_activation_performed: `{boundary.runtime_activation_performed}`",
            f"- implementation_performed: `{boundary.implementation_performed}`",
            f"- real_submission_allowed: `{boundary.real_submission_allowed}`",
            f"- legal_certification: `{boundary.legal_certification}`",
            "",
        ]
    )

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text(manifest, encoding="utf-8")
    output_md.write_text(md, encoding="utf-8")
    doc_path.write_text(md, encoding="utf-8")

    return boundary, validation, {
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
    "BOUNDARY_STATUS",
    "BOUNDARY_VERDICT",
    "BOUNDARY_DECISION",
    "BLOCK_REASON",
    "PREVIOUS_STAGE",
    "NEXT_STAGE",
    "Milestone15Task3AuthorizationBoundary",
    "ValidationResult",
    "build_milestone_15_task_3_authorization_boundary",
    "validate_milestone_15_task_3_authorization_boundary",
    "write_milestone_15_task_3_authorization_boundary_artifacts",
]
