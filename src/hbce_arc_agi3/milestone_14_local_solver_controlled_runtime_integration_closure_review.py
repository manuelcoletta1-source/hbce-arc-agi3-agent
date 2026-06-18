from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_CLOSURE_REVIEW_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_CLOSURE_REVIEW_ONLY_LOCAL_ONLY"
CLOSURE_STATUS = "CONTROLLED_RUNTIME_INTEGRATION_CLOSURE_REVIEW_READY"
CLOSURE_VERDICT = "CONTROLLED_RUNTIME_INTEGRATION_REVIEW_CLOSED_IMPLEMENTATION_STILL_BLOCKED"
CLOSURE_DECISION = "CLOSE_REVIEW_CHAIN_WITHOUT_IMPLEMENTATION"
BLOCK_REASON = "OPERATOR_APPROVAL_NOT_RECEIVED_AND_AUTHORIZATION_REVIEW_DENIED_IMPLEMENTATION"

PREVIOUS_STAGE = "MILESTONE_14_TASK_9_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
SOURCE_OPERATOR_GATE_STAGE = "MILESTONE_14_TASK_8_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1"
SOURCE_QIV_STAGE = "QIV_V2_4_RUNTIME_CONSTRAINT_LINK_V1"
NEXT_STAGE = "MILESTONE_14_TASK_11_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_FINAL_CLOSURE_V1"

SOURCE_OPERATOR_GATE_FINAL_BASELINE_COMMIT = "f5a263c"
SOURCE_QIV_FINAL_BASELINE_COMMIT = "9589d48"
SOURCE_QIV_FINAL_SIGNATURE = "F9F238F1EEAAF02B"
SOURCE_AUTHORIZATION_REVIEW_FINAL_BASELINE_COMMIT = "9a092a5"
SOURCE_AUTHORIZATION_REVIEW_FINAL_SIGNATURE = "D6D132659FF2406B"

OUTPUT_DIR = Path("examples/milestone-14/local-solver-controlled-runtime-integration-closure-review-v1")
OUTPUT_JSON = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-closure-review-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-closure-review-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-closure-review-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-closure-review-v1.md"
DOC_PATH = Path("docs/milestone-14-local-solver-controlled-runtime-integration-closure-review-v1.md")


ClosureGate = Literal[
    "TASK_8_OPERATOR_GATE_CLOSED",
    "QIV_CONSTRAINT_LINK_VALID_NON_AUTHORIZING",
    "TASK_9_AUTHORIZATION_REVIEW_DENIED",
    "IMPLEMENTATION_NOT_PERFORMED",
    "RUNTIME_NOT_ACTIVATED",
    "REAL_SUBMISSION_NOT_ALLOWED",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
]


@dataclass(frozen=True)
class Milestone14Task10ClosureReview:
    task_name: str
    status: str
    mode: str
    closure_status: str
    closure_verdict: str
    closure_decision: str
    block_reason: str
    signature: str
    baseline_commit: str
    previous_stage: str
    source_operator_gate_stage: str
    source_qiv_stage: str
    next_stage: str
    source_operator_gate_final_baseline_commit: str
    source_qiv_final_baseline_commit: str
    source_qiv_final_signature: str
    source_authorization_review_final_baseline_commit: str
    source_authorization_review_final_signature: str
    closure_review_performed: bool
    closure_review_passed: bool
    review_chain_closed: bool
    ready_for_final_closure: bool
    implementation_authorized: bool
    implementation_blocked: bool
    operator_approval_required: bool
    operator_approval_received: bool
    operator_gate_closed: bool
    qiv_constraint_link_valid: bool
    qiv_authorizes_implementation: bool
    qiv_overrides_operator_gate: bool
    authorization_review_denied: bool
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
    closure_gates: tuple[ClosureGate, ...]
    closure_gate_count: int
    closure_gate_failure_count: int
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


def build_milestone_14_task_10_closure_review(
    *,
    baseline_commit: str | None = None,
) -> Milestone14Task10ClosureReview:
    baseline = baseline_commit or _git_head()
    gates: tuple[ClosureGate, ...] = (
        "TASK_8_OPERATOR_GATE_CLOSED",
        "QIV_CONSTRAINT_LINK_VALID_NON_AUTHORIZING",
        "TASK_9_AUTHORIZATION_REVIEW_DENIED",
        "IMPLEMENTATION_NOT_PERFORMED",
        "RUNTIME_NOT_ACTIVATED",
        "REAL_SUBMISSION_NOT_ALLOWED",
        "FAIL_CLOSED_ACTIVE",
        "PUBLIC_SAFE_BOUNDARY_PRESERVED",
    )

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "source_operator_gate_stage": SOURCE_OPERATOR_GATE_STAGE,
        "source_qiv_stage": SOURCE_QIV_STAGE,
        "next_stage": NEXT_STAGE,
        "closure_verdict": CLOSURE_VERDICT,
        "closure_decision": CLOSURE_DECISION,
        "block_reason": BLOCK_REASON,
        "gates": gates,
    }

    return Milestone14Task10ClosureReview(
        task_name=TASK_NAME,
        status=TASK_READY,
        mode=MODE,
        closure_status=CLOSURE_STATUS,
        closure_verdict=CLOSURE_VERDICT,
        closure_decision=CLOSURE_DECISION,
        block_reason=BLOCK_REASON,
        signature=_signature(seed),
        baseline_commit=baseline,
        previous_stage=PREVIOUS_STAGE,
        source_operator_gate_stage=SOURCE_OPERATOR_GATE_STAGE,
        source_qiv_stage=SOURCE_QIV_STAGE,
        next_stage=NEXT_STAGE,
        source_operator_gate_final_baseline_commit=SOURCE_OPERATOR_GATE_FINAL_BASELINE_COMMIT,
        source_qiv_final_baseline_commit=SOURCE_QIV_FINAL_BASELINE_COMMIT,
        source_qiv_final_signature=SOURCE_QIV_FINAL_SIGNATURE,
        source_authorization_review_final_baseline_commit=SOURCE_AUTHORIZATION_REVIEW_FINAL_BASELINE_COMMIT,
        source_authorization_review_final_signature=SOURCE_AUTHORIZATION_REVIEW_FINAL_SIGNATURE,
        closure_review_performed=True,
        closure_review_passed=True,
        review_chain_closed=True,
        ready_for_final_closure=True,
        implementation_authorized=False,
        implementation_blocked=True,
        operator_approval_required=True,
        operator_approval_received=False,
        operator_gate_closed=True,
        qiv_constraint_link_valid=True,
        qiv_authorizes_implementation=False,
        qiv_overrides_operator_gate=False,
        authorization_review_denied=True,
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
        closure_gates=gates,
        closure_gate_count=len(gates),
        closure_gate_failure_count=0,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_14_task_10_closure_review(
    review: Milestone14Task10ClosureReview,
) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = {
        "closure_review_performed": review.closure_review_performed,
        "closure_review_passed": review.closure_review_passed,
        "review_chain_closed": review.review_chain_closed,
        "ready_for_final_closure": review.ready_for_final_closure,
        "implementation_blocked": review.implementation_blocked,
        "operator_approval_required": review.operator_approval_required,
        "operator_gate_closed": review.operator_gate_closed,
        "qiv_constraint_link_valid": review.qiv_constraint_link_valid,
        "authorization_review_denied": review.authorization_review_denied,
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

    if review.closure_verdict != CLOSURE_VERDICT:
        issues.append("closure_verdict_mismatch")

    if review.closure_decision != CLOSURE_DECISION:
        issues.append("closure_decision_mismatch")

    if review.block_reason != BLOCK_REASON:
        issues.append("block_reason_mismatch")

    if review.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage_mismatch")

    if review.source_operator_gate_stage != SOURCE_OPERATOR_GATE_STAGE:
        issues.append("source_operator_gate_stage_mismatch")

    if review.source_qiv_stage != SOURCE_QIV_STAGE:
        issues.append("source_qiv_stage_mismatch")

    if review.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    if review.closure_gate_count != len(review.closure_gates):
        issues.append("closure_gate_count_mismatch")

    if review.closure_gate_failure_count != 0:
        issues.append("closure_gate_failure_count_nonzero")

    status = TASK_VALID if not issues else f"{TASK_NAME}_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_14_task_10_closure_review_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[Milestone14Task10ClosureReview, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-14-local-solver-controlled-runtime-integration-closure-review-v1.json"
    output_index = output_dir / "milestone-14-local-solver-controlled-runtime-integration-closure-review-index-v1.json"
    output_manifest = output_dir / "milestone-14-local-solver-controlled-runtime-integration-closure-review-manifest-v1.txt"
    output_md = output_dir / "milestone-14-local-solver-controlled-runtime-integration-closure-review-v1.md"

    review = build_milestone_14_task_10_closure_review()
    validation = validate_milestone_14_task_10_closure_review(review)

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
        "source_operator_gate_stage": review.source_operator_gate_stage,
        "source_qiv_stage": review.source_qiv_stage,
        "next_stage": review.next_stage,
        "closure_verdict": review.closure_verdict,
        "closure_decision": review.closure_decision,
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
            f"closure_status={review.closure_status}",
            f"closure_verdict={review.closure_verdict}",
            f"closure_decision={review.closure_decision}",
            f"block_reason={review.block_reason}",
            f"previous_stage={review.previous_stage}",
            f"source_operator_gate_stage={review.source_operator_gate_stage}",
            f"source_qiv_stage={review.source_qiv_stage}",
            f"next_stage={review.next_stage}",
            f"source_operator_gate_final_baseline_commit={review.source_operator_gate_final_baseline_commit}",
            f"source_qiv_final_baseline_commit={review.source_qiv_final_baseline_commit}",
            f"source_qiv_final_signature={review.source_qiv_final_signature}",
            f"source_authorization_review_final_baseline_commit={review.source_authorization_review_final_baseline_commit}",
            f"source_authorization_review_final_signature={review.source_authorization_review_final_signature}",
            f"closure_review_performed={review.closure_review_performed}",
            f"closure_review_passed={review.closure_review_passed}",
            f"review_chain_closed={review.review_chain_closed}",
            f"ready_for_final_closure={review.ready_for_final_closure}",
            f"implementation_authorized={review.implementation_authorized}",
            f"implementation_blocked={review.implementation_blocked}",
            f"operator_approval_received={review.operator_approval_received}",
            f"qiv_authorizes_implementation={review.qiv_authorizes_implementation}",
            f"runtime_activation_performed={review.runtime_activation_performed}",
            f"implementation_performed={review.implementation_performed}",
            f"real_submission_allowed={review.real_submission_allowed}",
            f"legal_certification={review.legal_certification}",
            f"closure_gate_count={review.closure_gate_count}",
            f"closure_gate_failure_count={review.closure_gate_failure_count}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 14 - Task 10 - Controlled Runtime Integration Closure Review v1",
            "",
            f"Status: `{review.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{review.signature}`",
            f"Baseline commit: `{review.baseline_commit}`",
            "",
            "## Purpose",
            "",
            "This task closes the review chain after Task 8, the QIV v2.4 runtime constraint link, and Task 9.",
            "",
            "The closure confirms that controlled runtime integration remains blocked because operator approval was not received and implementation authorization was denied.",
            "",
            "## Decision",
            "",
            f"- Closure verdict: `{review.closure_verdict}`",
            f"- Closure decision: `{review.closure_decision}`",
            f"- Block reason: `{review.block_reason}`",
            "",
            "## Chain",
            "",
            f"- Previous stage: `{review.previous_stage}`",
            f"- Operator gate stage: `{review.source_operator_gate_stage}`",
            f"- QIV stage: `{review.source_qiv_stage}`",
            f"- Next stage: `{review.next_stage}`",
            "",
            "## Boundary",
            "",
            f"- review_chain_closed: `{review.review_chain_closed}`",
            f"- ready_for_final_closure: `{review.ready_for_final_closure}`",
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
    "CLOSURE_STATUS",
    "CLOSURE_VERDICT",
    "CLOSURE_DECISION",
    "BLOCK_REASON",
    "PREVIOUS_STAGE",
    "SOURCE_OPERATOR_GATE_STAGE",
    "SOURCE_QIV_STAGE",
    "NEXT_STAGE",
    "Milestone14Task10ClosureReview",
    "ValidationResult",
    "build_milestone_14_task_10_closure_review",
    "validate_milestone_14_task_10_closure_review",
    "write_milestone_14_task_10_closure_review_artifacts",
]
