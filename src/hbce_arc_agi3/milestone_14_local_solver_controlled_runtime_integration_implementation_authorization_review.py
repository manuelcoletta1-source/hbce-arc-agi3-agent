from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_REVIEW_ONLY_LOCAL_ONLY"
REVIEW_STATUS = "IMPLEMENTATION_AUTHORIZATION_REVIEW_READY"
REVIEW_VERDICT = "IMPLEMENTATION_AUTHORIZATION_DENIED_PENDING_EXPLICIT_OPERATOR_APPROVAL"
AUTHORIZATION_STATUS = "NOT_AUTHORIZED"
BLOCK_REASON = "OPERATOR_APPROVAL_GATE_CLOSED_AND_QIV_DOES_NOT_AUTHORIZE_IMPLEMENTATION"

PREVIOUS_STAGE = "MILESTONE_14_TASK_8_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1"
QIV_STAGE = "QIV_V2_4_RUNTIME_CONSTRAINT_LINK_V1"
NEXT_STAGE = "MILESTONE_14_TASK_10_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_CLOSURE_REVIEW_V1"

SOURCE_GATE_FINAL_BASELINE_COMMIT = "f5a263c"
SOURCE_QIV_FINAL_BASELINE_COMMIT = "9589d48"
SOURCE_QIV_FINAL_SIGNATURE = "F9F238F1EEAAF02B"

OUTPUT_DIR = Path("examples/milestone-14/local-solver-controlled-runtime-integration-implementation-authorization-review-v1")
OUTPUT_JSON = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-v1.md"
DOC_PATH = Path("docs/milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-v1.md")


ReviewGate = Literal[
    "OPERATOR_APPROVAL_GATE_CLOSED",
    "EXPLICIT_OPERATOR_APPROVAL_NOT_RECEIVED",
    "QIV_DOES_NOT_AUTHORIZE_IMPLEMENTATION",
    "RUNTIME_ACTIVATION_FORBIDDEN",
    "REAL_SUBMISSION_FORBIDDEN",
    "PUBLIC_SAFE_BOUNDARY_REQUIRED",
    "FAIL_CLOSED_ACTIVE",
]


@dataclass(frozen=True)
class Milestone14Task9AuthorizationReview:
    task_name: str
    status: str
    mode: str
    review_status: str
    review_verdict: str
    authorization_status: str
    block_reason: str
    signature: str
    baseline_commit: str
    previous_stage: str
    qiv_stage: str
    next_stage: str
    source_gate_final_baseline_commit: str
    source_qiv_final_baseline_commit: str
    source_qiv_final_signature: str
    authorization_review_performed: bool
    authorization_review_passed: bool
    implementation_authorized: bool
    implementation_blocked: bool
    operator_approval_required: bool
    operator_approval_received: bool
    operator_approval_gate_closed: bool
    qiv_constraint_link_present: bool
    qiv_authorizes_implementation: bool
    qiv_overrides_operator_gate: bool
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
    review_gates: tuple[ReviewGate, ...]
    review_gate_count: int
    review_gate_failure_count: int
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


def build_milestone_14_task_9_authorization_review(
    *,
    baseline_commit: str | None = None,
) -> Milestone14Task9AuthorizationReview:
    baseline = baseline_commit or _git_head()
    gates: tuple[ReviewGate, ...] = (
        "OPERATOR_APPROVAL_GATE_CLOSED",
        "EXPLICIT_OPERATOR_APPROVAL_NOT_RECEIVED",
        "QIV_DOES_NOT_AUTHORIZE_IMPLEMENTATION",
        "RUNTIME_ACTIVATION_FORBIDDEN",
        "REAL_SUBMISSION_FORBIDDEN",
        "PUBLIC_SAFE_BOUNDARY_REQUIRED",
        "FAIL_CLOSED_ACTIVE",
    )

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "qiv_stage": QIV_STAGE,
        "next_stage": NEXT_STAGE,
        "authorization_status": AUTHORIZATION_STATUS,
        "block_reason": BLOCK_REASON,
        "gates": gates,
    }

    return Milestone14Task9AuthorizationReview(
        task_name=TASK_NAME,
        status=TASK_READY,
        mode=MODE,
        review_status=REVIEW_STATUS,
        review_verdict=REVIEW_VERDICT,
        authorization_status=AUTHORIZATION_STATUS,
        block_reason=BLOCK_REASON,
        signature=_signature(seed),
        baseline_commit=baseline,
        previous_stage=PREVIOUS_STAGE,
        qiv_stage=QIV_STAGE,
        next_stage=NEXT_STAGE,
        source_gate_final_baseline_commit=SOURCE_GATE_FINAL_BASELINE_COMMIT,
        source_qiv_final_baseline_commit=SOURCE_QIV_FINAL_BASELINE_COMMIT,
        source_qiv_final_signature=SOURCE_QIV_FINAL_SIGNATURE,
        authorization_review_performed=True,
        authorization_review_passed=True,
        implementation_authorized=False,
        implementation_blocked=True,
        operator_approval_required=True,
        operator_approval_received=False,
        operator_approval_gate_closed=True,
        qiv_constraint_link_present=True,
        qiv_authorizes_implementation=False,
        qiv_overrides_operator_gate=False,
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
        review_gates=gates,
        review_gate_count=len(gates),
        review_gate_failure_count=0,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_14_task_9_authorization_review(
    review: Milestone14Task9AuthorizationReview,
) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = {
        "authorization_review_performed": review.authorization_review_performed,
        "authorization_review_passed": review.authorization_review_passed,
        "implementation_blocked": review.implementation_blocked,
        "operator_approval_required": review.operator_approval_required,
        "operator_approval_gate_closed": review.operator_approval_gate_closed,
        "qiv_constraint_link_present": review.qiv_constraint_link_present,
        "public_overfit_guard_required": review.public_overfit_guard_required,
        "fail_closed_required": review.fail_closed_required,
        "fail_closed_active": review.fail_closed_active,
        "public_safe": review.public_safe,
        "deterministic": review.deterministic,
        "local_only": review.local_only,
    }

    for key, value in expected_true.items():
        if value is not True:
            issues.append(f"{key}:expected_true")

    expected_false = {
        "implementation_authorized": review.implementation_authorized,
        "operator_approval_received": review.operator_approval_received,
        "qiv_authorizes_implementation": review.qiv_authorizes_implementation,
        "qiv_overrides_operator_gate": review.qiv_overrides_operator_gate,
        "runtime_activation_performed": review.runtime_activation_performed,
        "runtime_execution_performed": review.runtime_execution_performed,
        "runtime_solver_modified": review.runtime_solver_modified,
        "ranker_runtime_modified": review.ranker_runtime_modified,
        "candidate_generator_modified": review.candidate_generator_modified,
        "implementation_performed": review.implementation_performed,
        "real_evaluation_performed": review.real_evaluation_performed,
        "real_submission_allowed": review.real_submission_allowed,
        "ready_for_real_kaggle_submission": review.ready_for_real_kaggle_submission,
        "manual_upload_allowed": review.manual_upload_allowed,
        "kaggle_authentication_allowed": review.kaggle_authentication_allowed,
        "kaggle_authentication_performed": review.kaggle_authentication_performed,
        "kaggle_upload_allowed": review.kaggle_upload_allowed,
        "kaggle_upload_performed": review.kaggle_upload_performed,
        "kaggle_submission_sent": review.kaggle_submission_sent,
        "external_api_dependency": review.external_api_dependency,
        "internet_during_eval": review.internet_during_eval,
        "private_core_exposure": review.private_core_exposure,
        "legal_certification": review.legal_certification,
        "official_score_claim_allowed": review.official_score_claim_allowed,
        "competitive_score_claim_allowed": review.competitive_score_claim_allowed,
        "public_overfit_allowed": review.public_overfit_allowed,
    }

    for key, value in expected_false.items():
        if value is not False:
            issues.append(f"{key}:expected_false")

    if review.authorization_status != AUTHORIZATION_STATUS:
        issues.append("authorization_status_mismatch")

    if review.review_verdict != REVIEW_VERDICT:
        issues.append("review_verdict_mismatch")

    if review.block_reason != BLOCK_REASON:
        issues.append("block_reason_mismatch")

    if review.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage_mismatch")

    if review.qiv_stage != QIV_STAGE:
        issues.append("qiv_stage_mismatch")

    if review.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    if review.review_gate_count != len(review.review_gates):
        issues.append("review_gate_count_mismatch")

    if review.review_gate_failure_count != 0:
        issues.append("review_gate_failure_count_nonzero")

    status = TASK_VALID if not issues else f"{TASK_NAME}_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_14_task_9_authorization_review_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[Milestone14Task9AuthorizationReview, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-v1.json"
    output_index = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-index-v1.json"
    output_manifest = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-manifest-v1.txt"
    output_md = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-v1.md"

    review = build_milestone_14_task_9_authorization_review()
    validation = validate_milestone_14_task_9_authorization_review(review)

    payload = {
        "record": asdict(review),
        "validation": asdict(validation),
    }

    index = {
        "task_name": review.task_name,
        "status": review.status,
        "validation_status": validation.status,
        "valid": validation.valid,
        "signature": review.signature,
        "baseline_commit": review.baseline_commit,
        "previous_stage": review.previous_stage,
        "qiv_stage": review.qiv_stage,
        "next_stage": review.next_stage,
        "authorization_status": review.authorization_status,
        "review_verdict": review.review_verdict,
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
            f"task_name={review.task_name}",
            f"status={review.status}",
            f"validation_status={validation.status}",
            f"valid={validation.valid}",
            f"signature={review.signature}",
            f"baseline_commit={review.baseline_commit}",
            f"mode={review.mode}",
            f"review_status={review.review_status}",
            f"review_verdict={review.review_verdict}",
            f"authorization_status={review.authorization_status}",
            f"block_reason={review.block_reason}",
            f"previous_stage={review.previous_stage}",
            f"qiv_stage={review.qiv_stage}",
            f"next_stage={review.next_stage}",
            f"source_gate_final_baseline_commit={review.source_gate_final_baseline_commit}",
            f"source_qiv_final_baseline_commit={review.source_qiv_final_baseline_commit}",
            f"source_qiv_final_signature={review.source_qiv_final_signature}",
            f"authorization_review_performed={review.authorization_review_performed}",
            f"authorization_review_passed={review.authorization_review_passed}",
            f"implementation_authorized={review.implementation_authorized}",
            f"implementation_blocked={review.implementation_blocked}",
            f"operator_approval_required={review.operator_approval_required}",
            f"operator_approval_received={review.operator_approval_received}",
            f"operator_approval_gate_closed={review.operator_approval_gate_closed}",
            f"qiv_constraint_link_present={review.qiv_constraint_link_present}",
            f"qiv_authorizes_implementation={review.qiv_authorizes_implementation}",
            f"qiv_overrides_operator_gate={review.qiv_overrides_operator_gate}",
            f"runtime_activation_performed={review.runtime_activation_performed}",
            f"implementation_performed={review.implementation_performed}",
            f"real_submission_allowed={review.real_submission_allowed}",
            f"legal_certification={review.legal_certification}",
            f"review_gate_count={review.review_gate_count}",
            f"review_gate_failure_count={review.review_gate_failure_count}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 14 - Task 9 - Implementation Authorization Review v1",
            "",
            f"Status: `{review.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{review.signature}`",
            f"Baseline commit: `{review.baseline_commit}`",
            "",
            "## Purpose",
            "",
            "This task reviews whether implementation can be authorized after the operator approval gate and the QIV v2.4 runtime constraint link.",
            "",
            "The result is intentionally negative: implementation is not authorized.",
            "",
            "## Decision",
            "",
            f"- Review verdict: `{review.review_verdict}`",
            f"- Authorization status: `{review.authorization_status}`",
            f"- Block reason: `{review.block_reason}`",
            "",
            "## Chain",
            "",
            f"- Previous stage: `{review.previous_stage}`",
            f"- QIV stage: `{review.qiv_stage}`",
            f"- Next stage: `{review.next_stage}`",
            "",
            "## Boundary",
            "",
            f"- implementation_authorized: `{review.implementation_authorized}`",
            f"- implementation_blocked: `{review.implementation_blocked}`",
            f"- operator_approval_received: `{review.operator_approval_received}`",
            f"- qiv_authorizes_implementation: `{review.qiv_authorizes_implementation}`",
            f"- qiv_overrides_operator_gate: `{review.qiv_overrides_operator_gate}`",
            f"- runtime_activation_performed: `{review.runtime_activation_performed}`",
            f"- runtime_execution_performed: `{review.runtime_execution_performed}`",
            f"- implementation_performed: `{review.implementation_performed}`",
            f"- real_submission_allowed: `{review.real_submission_allowed}`",
            f"- legal_certification: `{review.legal_certification}`",
            "",
        ]
    )

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text(manifest, encoding="utf-8")
    output_md.write_text(md, encoding="utf-8")
    doc_path.write_text(md, encoding="utf-8")

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
    "AUTHORIZATION_STATUS",
    "BLOCK_REASON",
    "PREVIOUS_STAGE",
    "QIV_STAGE",
    "NEXT_STAGE",
    "Milestone14Task9AuthorizationReview",
    "ValidationResult",
    "build_milestone_14_task_9_authorization_review",
    "validate_milestone_14_task_9_authorization_review",
    "write_milestone_14_task_9_authorization_review_artifacts",
]
