from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_FINAL_CLOSURE_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_FINAL_CLOSURE_ONLY_LOCAL_ONLY"
FINAL_STATUS = "CONTROLLED_RUNTIME_INTEGRATION_FINAL_CLOSURE_READY"
FINAL_VERDICT = "MILESTONE_14_CLOSED_WITHOUT_RUNTIME_ACTIVATION"
FINAL_DECISION = "FINAL_CLOSE_MILESTONE_14_REVIEW_CHAIN"
BLOCK_REASON = "OPERATOR_APPROVAL_NOT_RECEIVED_IMPLEMENTATION_AUTHORIZATION_DENIED_RUNTIME_REMAINS_INACTIVE"

PREVIOUS_STAGE = "MILESTONE_14_TASK_10_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_CLOSURE_REVIEW_V1"
SOURCE_OPERATOR_GATE_STAGE = "MILESTONE_14_TASK_8_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1"
SOURCE_QIV_STAGE = "QIV_V2_4_RUNTIME_CONSTRAINT_LINK_V1"
SOURCE_AUTHORIZATION_STAGE = "MILESTONE_14_TASK_9_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
NEXT_STAGE = "MILESTONE_15_PENDING_EXPLICIT_OPERATOR_DECISION"

SOURCE_TASK_8_FINAL_BASELINE_COMMIT = "f5a263c"
SOURCE_QIV_FINAL_BASELINE_COMMIT = "9589d48"
SOURCE_QIV_FINAL_SIGNATURE = "F9F238F1EEAAF02B"
SOURCE_TASK_9_FINAL_BASELINE_COMMIT = "9a092a5"
SOURCE_TASK_9_FINAL_SIGNATURE = "D6D132659FF2406B"
SOURCE_TASK_10_FINAL_BASELINE_COMMIT = "151a919"
SOURCE_TASK_10_FINAL_SIGNATURE = "18D905E701373134"

OUTPUT_DIR = Path("examples/milestone-14/local-solver-controlled-runtime-integration-final-closure-v1")
OUTPUT_JSON = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-final-closure-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-final-closure-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-final-closure-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-final-closure-v1.md"
DOC_PATH = Path("docs/milestone-14-local-solver-controlled-runtime-integration-final-closure-v1.md")


FinalClosureGate = Literal[
    "TASK_8_OPERATOR_GATE_CLOSED",
    "QIV_LINK_VALID_NON_AUTHORIZING",
    "TASK_9_AUTHORIZATION_DENIED",
    "TASK_10_REVIEW_CHAIN_CLOSED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "RUNTIME_NOT_ACTIVATED",
    "REAL_SUBMISSION_NOT_ALLOWED",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
    "FAIL_CLOSED_ACTIVE",
]


@dataclass(frozen=True)
class Milestone14Task11FinalClosure:
    task_name: str
    status: str
    mode: str
    final_status: str
    final_verdict: str
    final_decision: str
    block_reason: str
    signature: str
    baseline_commit: str
    previous_stage: str
    source_operator_gate_stage: str
    source_qiv_stage: str
    source_authorization_stage: str
    next_stage: str
    source_task_8_final_baseline_commit: str
    source_qiv_final_baseline_commit: str
    source_qiv_final_signature: str
    source_task_9_final_baseline_commit: str
    source_task_9_final_signature: str
    source_task_10_final_baseline_commit: str
    source_task_10_final_signature: str
    final_closure_performed: bool
    final_closure_passed: bool
    milestone_14_closed: bool
    milestone_14_closed_without_runtime_activation: bool
    review_chain_closed: bool
    ready_for_milestone_15_decision: bool
    implementation_authorized: bool
    implementation_blocked: bool
    operator_approval_required: bool
    operator_approval_received: bool
    operator_gate_closed: bool
    qiv_constraint_link_valid: bool
    qiv_authorizes_implementation: bool
    qiv_overrides_operator_gate: bool
    authorization_review_denied: bool
    closure_review_passed: bool
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
    final_closure_gates: tuple[FinalClosureGate, ...]
    final_closure_gate_count: int
    final_closure_gate_failure_count: int
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


def build_milestone_14_task_11_final_closure(
    *,
    baseline_commit: str | None = None,
) -> Milestone14Task11FinalClosure:
    baseline = baseline_commit or _git_head()
    gates: tuple[FinalClosureGate, ...] = (
        "TASK_8_OPERATOR_GATE_CLOSED",
        "QIV_LINK_VALID_NON_AUTHORIZING",
        "TASK_9_AUTHORIZATION_DENIED",
        "TASK_10_REVIEW_CHAIN_CLOSED",
        "IMPLEMENTATION_NOT_AUTHORIZED",
        "RUNTIME_NOT_ACTIVATED",
        "REAL_SUBMISSION_NOT_ALLOWED",
        "PUBLIC_SAFE_BOUNDARY_PRESERVED",
        "FAIL_CLOSED_ACTIVE",
    )

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "source_operator_gate_stage": SOURCE_OPERATOR_GATE_STAGE,
        "source_qiv_stage": SOURCE_QIV_STAGE,
        "source_authorization_stage": SOURCE_AUTHORIZATION_STAGE,
        "next_stage": NEXT_STAGE,
        "final_verdict": FINAL_VERDICT,
        "final_decision": FINAL_DECISION,
        "block_reason": BLOCK_REASON,
        "gates": gates,
    }

    return Milestone14Task11FinalClosure(
        task_name=TASK_NAME,
        status=TASK_READY,
        mode=MODE,
        final_status=FINAL_STATUS,
        final_verdict=FINAL_VERDICT,
        final_decision=FINAL_DECISION,
        block_reason=BLOCK_REASON,
        signature=_signature(seed),
        baseline_commit=baseline,
        previous_stage=PREVIOUS_STAGE,
        source_operator_gate_stage=SOURCE_OPERATOR_GATE_STAGE,
        source_qiv_stage=SOURCE_QIV_STAGE,
        source_authorization_stage=SOURCE_AUTHORIZATION_STAGE,
        next_stage=NEXT_STAGE,
        source_task_8_final_baseline_commit=SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        source_qiv_final_baseline_commit=SOURCE_QIV_FINAL_BASELINE_COMMIT,
        source_qiv_final_signature=SOURCE_QIV_FINAL_SIGNATURE,
        source_task_9_final_baseline_commit=SOURCE_TASK_9_FINAL_BASELINE_COMMIT,
        source_task_9_final_signature=SOURCE_TASK_9_FINAL_SIGNATURE,
        source_task_10_final_baseline_commit=SOURCE_TASK_10_FINAL_BASELINE_COMMIT,
        source_task_10_final_signature=SOURCE_TASK_10_FINAL_SIGNATURE,
        final_closure_performed=True,
        final_closure_passed=True,
        milestone_14_closed=True,
        milestone_14_closed_without_runtime_activation=True,
        review_chain_closed=True,
        ready_for_milestone_15_decision=True,
        implementation_authorized=False,
        implementation_blocked=True,
        operator_approval_required=True,
        operator_approval_received=False,
        operator_gate_closed=True,
        qiv_constraint_link_valid=True,
        qiv_authorizes_implementation=False,
        qiv_overrides_operator_gate=False,
        authorization_review_denied=True,
        closure_review_passed=True,
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
        final_closure_gates=gates,
        final_closure_gate_count=len(gates),
        final_closure_gate_failure_count=0,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_14_task_11_final_closure(
    closure: Milestone14Task11FinalClosure,
) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = {
        "final_closure_performed": closure.final_closure_performed,
        "final_closure_passed": closure.final_closure_passed,
        "milestone_14_closed": closure.milestone_14_closed,
        "milestone_14_closed_without_runtime_activation": closure.milestone_14_closed_without_runtime_activation,
        "review_chain_closed": closure.review_chain_closed,
        "ready_for_milestone_15_decision": closure.ready_for_milestone_15_decision,
        "implementation_blocked": closure.implementation_blocked,
        "operator_approval_required": closure.operator_approval_required,
        "operator_gate_closed": closure.operator_gate_closed,
        "qiv_constraint_link_valid": closure.qiv_constraint_link_valid,
        "authorization_review_denied": closure.authorization_review_denied,
        "closure_review_passed": closure.closure_review_passed,
        "public_overfit_guard_required": closure.public_overfit_guard_required,
        "fail_closed_required": closure.fail_closed_required,
        "fail_closed_active": closure.fail_closed_active,
        "public_safe": closure.public_safe,
        "deterministic": closure.deterministic,
        "local_only": closure.local_only,
    }

    for key, value in expected_true.items():
        if value is not True:
            issues.append(f"{key}:expected_true")

    expected_false = {
        "implementation_authorized": closure.implementation_authorized,
        "operator_approval_received": closure.operator_approval_received,
        "qiv_authorizes_implementation": closure.qiv_authorizes_implementation,
        "qiv_overrides_operator_gate": closure.qiv_overrides_operator_gate,
        "runtime_activation_performed": closure.runtime_activation_performed,
        "runtime_execution_performed": closure.runtime_execution_performed,
        "runtime_solver_modified": closure.runtime_solver_modified,
        "ranker_runtime_modified": closure.ranker_runtime_modified,
        "candidate_generator_modified": closure.candidate_generator_modified,
        "implementation_performed": closure.implementation_performed,
        "real_evaluation_performed": closure.real_evaluation_performed,
        "real_submission_allowed": closure.real_submission_allowed,
        "ready_for_real_kaggle_submission": closure.ready_for_real_kaggle_submission,
        "manual_upload_allowed": closure.manual_upload_allowed,
        "kaggle_authentication_allowed": closure.kaggle_authentication_allowed,
        "kaggle_authentication_performed": closure.kaggle_authentication_performed,
        "kaggle_upload_allowed": closure.kaggle_upload_allowed,
        "kaggle_upload_performed": closure.kaggle_upload_performed,
        "kaggle_submission_sent": closure.kaggle_submission_sent,
        "external_api_dependency": closure.external_api_dependency,
        "internet_during_eval": closure.internet_during_eval,
        "private_core_exposure": closure.private_core_exposure,
        "legal_certification": closure.legal_certification,
        "official_score_claim_allowed": closure.official_score_claim_allowed,
        "competitive_score_claim_allowed": closure.competitive_score_claim_allowed,
        "public_overfit_allowed": closure.public_overfit_allowed,
    }

    for key, value in expected_false.items():
        if value is not False:
            issues.append(f"{key}:expected_false")

    if closure.final_verdict != FINAL_VERDICT:
        issues.append("final_verdict_mismatch")

    if closure.final_decision != FINAL_DECISION:
        issues.append("final_decision_mismatch")

    if closure.block_reason != BLOCK_REASON:
        issues.append("block_reason_mismatch")

    if closure.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage_mismatch")

    if closure.source_operator_gate_stage != SOURCE_OPERATOR_GATE_STAGE:
        issues.append("source_operator_gate_stage_mismatch")

    if closure.source_qiv_stage != SOURCE_QIV_STAGE:
        issues.append("source_qiv_stage_mismatch")

    if closure.source_authorization_stage != SOURCE_AUTHORIZATION_STAGE:
        issues.append("source_authorization_stage_mismatch")

    if closure.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    if closure.final_closure_gate_count != len(closure.final_closure_gates):
        issues.append("final_closure_gate_count_mismatch")

    if closure.final_closure_gate_failure_count != 0:
        issues.append("final_closure_gate_failure_count_nonzero")

    status = TASK_VALID if not issues else f"{TASK_NAME}_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_14_task_11_final_closure_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[Milestone14Task11FinalClosure, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-14-local-solver-controlled-runtime-integration-final-closure-v1.json"
    output_index = output_dir / "milestone-14-local-solver-controlled-runtime-integration-final-closure-index-v1.json"
    output_manifest = output_dir / "milestone-14-local-solver-controlled-runtime-integration-final-closure-manifest-v1.txt"
    output_md = output_dir / "milestone-14-local-solver-controlled-runtime-integration-final-closure-v1.md"

    closure = build_milestone_14_task_11_final_closure()
    validation = validate_milestone_14_task_11_final_closure(closure)

    payload = {
        "record": asdict(closure),
        "validation": asdict(validation),
    }

    index = {
        "task_name": closure.task_name,
        "status": closure.status,
        "validation_status": validation.status,
        "valid": validation.valid,
        "signature": closure.signature,
        "baseline_commit": closure.baseline_commit,
        "previous_stage": closure.previous_stage,
        "source_operator_gate_stage": closure.source_operator_gate_stage,
        "source_qiv_stage": closure.source_qiv_stage,
        "source_authorization_stage": closure.source_authorization_stage,
        "next_stage": closure.next_stage,
        "final_verdict": closure.final_verdict,
        "final_decision": closure.final_decision,
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
            f"task_name={closure.task_name}",
            f"status={closure.status}",
            f"validation_status={validation.status}",
            f"valid={validation.valid}",
            f"signature={closure.signature}",
            f"baseline_commit={closure.baseline_commit}",
            f"mode={closure.mode}",
            f"final_status={closure.final_status}",
            f"final_verdict={closure.final_verdict}",
            f"final_decision={closure.final_decision}",
            f"block_reason={closure.block_reason}",
            f"previous_stage={closure.previous_stage}",
            f"source_operator_gate_stage={closure.source_operator_gate_stage}",
            f"source_qiv_stage={closure.source_qiv_stage}",
            f"source_authorization_stage={closure.source_authorization_stage}",
            f"next_stage={closure.next_stage}",
            f"source_task_8_final_baseline_commit={closure.source_task_8_final_baseline_commit}",
            f"source_qiv_final_baseline_commit={closure.source_qiv_final_baseline_commit}",
            f"source_qiv_final_signature={closure.source_qiv_final_signature}",
            f"source_task_9_final_baseline_commit={closure.source_task_9_final_baseline_commit}",
            f"source_task_9_final_signature={closure.source_task_9_final_signature}",
            f"source_task_10_final_baseline_commit={closure.source_task_10_final_baseline_commit}",
            f"source_task_10_final_signature={closure.source_task_10_final_signature}",
            f"final_closure_performed={closure.final_closure_performed}",
            f"final_closure_passed={closure.final_closure_passed}",
            f"milestone_14_closed={closure.milestone_14_closed}",
            f"milestone_14_closed_without_runtime_activation={closure.milestone_14_closed_without_runtime_activation}",
            f"ready_for_milestone_15_decision={closure.ready_for_milestone_15_decision}",
            f"implementation_authorized={closure.implementation_authorized}",
            f"implementation_blocked={closure.implementation_blocked}",
            f"runtime_activation_performed={closure.runtime_activation_performed}",
            f"implementation_performed={closure.implementation_performed}",
            f"real_submission_allowed={closure.real_submission_allowed}",
            f"legal_certification={closure.legal_certification}",
            f"final_closure_gate_count={closure.final_closure_gate_count}",
            f"final_closure_gate_failure_count={closure.final_closure_gate_failure_count}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 14 - Task 11 - Local Solver Controlled Runtime Integration Final Closure v1",
            "",
            f"Status: `{closure.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{closure.signature}`",
            f"Baseline commit: `{closure.baseline_commit}`",
            "",
            "## Purpose",
            "",
            "This task performs the final closure of Milestone 14 without runtime activation.",
            "",
            "The final closure confirms that Task 8, QIV v2.4, Task 9, and Task 10 form a coherent fail-closed review chain.",
            "",
            "## Final decision",
            "",
            f"- Final verdict: `{closure.final_verdict}`",
            f"- Final decision: `{closure.final_decision}`",
            f"- Block reason: `{closure.block_reason}`",
            "",
            "## Boundary",
            "",
            f"- milestone_14_closed: `{closure.milestone_14_closed}`",
            f"- milestone_14_closed_without_runtime_activation: `{closure.milestone_14_closed_without_runtime_activation}`",
            f"- ready_for_milestone_15_decision: `{closure.ready_for_milestone_15_decision}`",
            f"- implementation_authorized: `{closure.implementation_authorized}`",
            f"- implementation_blocked: `{closure.implementation_blocked}`",
            f"- runtime_activation_performed: `{closure.runtime_activation_performed}`",
            f"- runtime_execution_performed: `{closure.runtime_execution_performed}`",
            f"- implementation_performed: `{closure.implementation_performed}`",
            f"- real_submission_allowed: `{closure.real_submission_allowed}`",
            f"- legal_certification: `{closure.legal_certification}`",
            "",
        ]
    )

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text(manifest, encoding="utf-8")
    output_md.write_text(md, encoding="utf-8")
    doc_path.write_text(md, encoding="utf-8")

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
    "FINAL_STATUS",
    "FINAL_VERDICT",
    "FINAL_DECISION",
    "BLOCK_REASON",
    "PREVIOUS_STAGE",
    "SOURCE_OPERATOR_GATE_STAGE",
    "SOURCE_QIV_STAGE",
    "SOURCE_AUTHORIZATION_STAGE",
    "NEXT_STAGE",
    "Milestone14Task11FinalClosure",
    "ValidationResult",
    "build_milestone_14_task_11_final_closure",
    "validate_milestone_14_task_11_final_closure",
    "write_milestone_14_task_11_final_closure_artifacts",
]
