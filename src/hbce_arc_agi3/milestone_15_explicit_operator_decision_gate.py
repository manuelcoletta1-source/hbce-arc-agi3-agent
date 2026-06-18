from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TASK_NAME = "MILESTONE_15_TASK_1_EXPLICIT_OPERATOR_DECISION_GATE_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_DECISION_GATE_ONLY_LOCAL_ONLY"
GATE_STATUS = "EXPLICIT_OPERATOR_DECISION_GATE_READY"
GATE_VERDICT = "OPERATOR_DECISION_REQUIRED_NO_IMPLEMENTATION_AUTHORIZED"
GATE_DECISION = "WAIT_FOR_EXPLICIT_OPERATOR_DECISION"
BLOCK_REASON = "MILESTONE_14_CLOSED_WITHOUT_RUNTIME_ACTIVATION_OPERATOR_DECISION_REQUIRED"

PREVIOUS_STAGE = "MILESTONE_14_TASK_11_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_FINAL_CLOSURE_V1"
SOURCE_MILESTONE_14_FINAL_CLOSURE = "MILESTONE_14_CLOSED_WITHOUT_RUNTIME_ACTIVATION"
NEXT_STAGE = "MILESTONE_15_TASK_2_OPERATOR_DECISION_RECORD_V1"

SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT = "f7ee729"
SOURCE_MILESTONE_14_FINAL_SIGNATURE = "05F1CDD559B63B8C"
SOURCE_TASK_8_FINAL_BASELINE_COMMIT = "f5a263c"
SOURCE_QIV_FINAL_BASELINE_COMMIT = "9589d48"
SOURCE_QIV_FINAL_SIGNATURE = "F9F238F1EEAAF02B"
SOURCE_TASK_9_FINAL_BASELINE_COMMIT = "9a092a5"
SOURCE_TASK_9_FINAL_SIGNATURE = "D6D132659FF2406B"
SOURCE_TASK_10_FINAL_BASELINE_COMMIT = "151a919"
SOURCE_TASK_10_FINAL_SIGNATURE = "18D905E701373134"

OUTPUT_DIR = Path("examples/milestone-15/explicit-operator-decision-gate-v1")
OUTPUT_JSON = OUTPUT_DIR / "milestone-15-explicit-operator-decision-gate-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-15-explicit-operator-decision-gate-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-15-explicit-operator-decision-gate-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-15-explicit-operator-decision-gate-v1.md"
DOC_PATH = Path("docs/milestone-15-explicit-operator-decision-gate-v1.md")


DecisionGateCheck = Literal[
    "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
    "OPERATOR_DECISION_REQUIRED",
    "OPERATOR_DECISION_NOT_RECEIVED",
    "NO_IMPLICIT_AUTHORIZATION",
    "IMPLEMENTATION_REMAINS_BLOCKED",
    "RUNTIME_REMAINS_INACTIVE",
    "REAL_SUBMISSION_REMAINS_BLOCKED",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
]


@dataclass(frozen=True)
class Milestone15Task1DecisionGate:
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
    source_milestone_14_final_closure: str
    next_stage: str

    source_milestone_14_final_baseline_commit: str
    source_milestone_14_final_signature: str
    source_task_8_final_baseline_commit: str
    source_qiv_final_baseline_commit: str
    source_qiv_final_signature: str
    source_task_9_final_baseline_commit: str
    source_task_9_final_signature: str
    source_task_10_final_baseline_commit: str
    source_task_10_final_signature: str

    milestone_15_opened: bool
    explicit_operator_decision_gate_created: bool
    operator_decision_required: bool
    operator_decision_received: bool
    operator_decision_value: str
    operator_decision_recorded: bool
    no_implicit_authorization: bool

    milestone_14_closed: bool
    milestone_14_closed_without_runtime_activation: bool
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

    decision_gate_checks: tuple[DecisionGateCheck, ...]
    decision_gate_check_count: int
    decision_gate_failure_count: int
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


def build_milestone_15_task_1_decision_gate(
    *,
    baseline_commit: str | None = None,
) -> Milestone15Task1DecisionGate:
    baseline = baseline_commit or _git_head()

    checks: tuple[DecisionGateCheck, ...] = (
        "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
        "OPERATOR_DECISION_REQUIRED",
        "OPERATOR_DECISION_NOT_RECEIVED",
        "NO_IMPLICIT_AUTHORIZATION",
        "IMPLEMENTATION_REMAINS_BLOCKED",
        "RUNTIME_REMAINS_INACTIVE",
        "REAL_SUBMISSION_REMAINS_BLOCKED",
        "FAIL_CLOSED_ACTIVE",
        "PUBLIC_SAFE_BOUNDARY_PRESERVED",
    )

    seed = {
        "task_name": TASK_NAME,
        "baseline_commit": baseline,
        "previous_stage": PREVIOUS_STAGE,
        "source_milestone_14_final_closure": SOURCE_MILESTONE_14_FINAL_CLOSURE,
        "next_stage": NEXT_STAGE,
        "gate_verdict": GATE_VERDICT,
        "gate_decision": GATE_DECISION,
        "block_reason": BLOCK_REASON,
        "checks": checks,
    }

    return Milestone15Task1DecisionGate(
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
        source_milestone_14_final_closure=SOURCE_MILESTONE_14_FINAL_CLOSURE,
        next_stage=NEXT_STAGE,
        source_milestone_14_final_baseline_commit=SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT,
        source_milestone_14_final_signature=SOURCE_MILESTONE_14_FINAL_SIGNATURE,
        source_task_8_final_baseline_commit=SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        source_qiv_final_baseline_commit=SOURCE_QIV_FINAL_BASELINE_COMMIT,
        source_qiv_final_signature=SOURCE_QIV_FINAL_SIGNATURE,
        source_task_9_final_baseline_commit=SOURCE_TASK_9_FINAL_BASELINE_COMMIT,
        source_task_9_final_signature=SOURCE_TASK_9_FINAL_SIGNATURE,
        source_task_10_final_baseline_commit=SOURCE_TASK_10_FINAL_BASELINE_COMMIT,
        source_task_10_final_signature=SOURCE_TASK_10_FINAL_SIGNATURE,
        milestone_15_opened=True,
        explicit_operator_decision_gate_created=True,
        operator_decision_required=True,
        operator_decision_received=False,
        operator_decision_value="PENDING_EXPLICIT_OPERATOR_DECISION",
        operator_decision_recorded=False,
        no_implicit_authorization=True,
        milestone_14_closed=True,
        milestone_14_closed_without_runtime_activation=True,
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
        decision_gate_checks=checks,
        decision_gate_check_count=len(checks),
        decision_gate_failure_count=0,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_15_task_1_decision_gate(
    gate: Milestone15Task1DecisionGate,
) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = {
        "milestone_15_opened": gate.milestone_15_opened,
        "explicit_operator_decision_gate_created": gate.explicit_operator_decision_gate_created,
        "operator_decision_required": gate.operator_decision_required,
        "no_implicit_authorization": gate.no_implicit_authorization,
        "milestone_14_closed": gate.milestone_14_closed,
        "milestone_14_closed_without_runtime_activation": gate.milestone_14_closed_without_runtime_activation,
        "implementation_blocked": gate.implementation_blocked,
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
        "operator_decision_recorded": gate.operator_decision_recorded,
        "implementation_authorized": gate.implementation_authorized,
        "runtime_activation_authorized": gate.runtime_activation_authorized,
        "runtime_activation_performed": gate.runtime_activation_performed,
        "runtime_execution_performed": gate.runtime_execution_performed,
        "runtime_solver_modified": gate.runtime_solver_modified,
        "ranker_runtime_modified": gate.ranker_runtime_modified,
        "candidate_generator_modified": gate.candidate_generator_modified,
        "implementation_performed": gate.implementation_performed,
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

    if gate.source_milestone_14_final_closure != SOURCE_MILESTONE_14_FINAL_CLOSURE:
        issues.append("source_milestone_14_final_closure_mismatch")

    if gate.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    if gate.operator_decision_value != "PENDING_EXPLICIT_OPERATOR_DECISION":
        issues.append("operator_decision_value_mismatch")

    if gate.decision_gate_check_count != len(gate.decision_gate_checks):
        issues.append("decision_gate_check_count_mismatch")

    if gate.decision_gate_failure_count != 0:
        issues.append("decision_gate_failure_count_nonzero")

    status = TASK_VALID if not issues else f"{TASK_NAME}_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_15_task_1_decision_gate_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[Milestone15Task1DecisionGate, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-15-explicit-operator-decision-gate-v1.json"
    output_index = output_dir / "milestone-15-explicit-operator-decision-gate-index-v1.json"
    output_manifest = output_dir / "milestone-15-explicit-operator-decision-gate-manifest-v1.txt"
    output_md = output_dir / "milestone-15-explicit-operator-decision-gate-v1.md"

    gate = build_milestone_15_task_1_decision_gate()
    validation = validate_milestone_15_task_1_decision_gate(gate)

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
        "source_milestone_14_final_closure": gate.source_milestone_14_final_closure,
        "next_stage": gate.next_stage,
        "gate_verdict": gate.gate_verdict,
        "gate_decision": gate.gate_decision,
        "operator_decision_value": gate.operator_decision_value,
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
            f"source_milestone_14_final_closure={gate.source_milestone_14_final_closure}",
            f"next_stage={gate.next_stage}",
            f"source_milestone_14_final_baseline_commit={gate.source_milestone_14_final_baseline_commit}",
            f"source_milestone_14_final_signature={gate.source_milestone_14_final_signature}",
            f"milestone_15_opened={gate.milestone_15_opened}",
            f"explicit_operator_decision_gate_created={gate.explicit_operator_decision_gate_created}",
            f"operator_decision_required={gate.operator_decision_required}",
            f"operator_decision_received={gate.operator_decision_received}",
            f"operator_decision_value={gate.operator_decision_value}",
            f"operator_decision_recorded={gate.operator_decision_recorded}",
            f"no_implicit_authorization={gate.no_implicit_authorization}",
            f"implementation_authorized={gate.implementation_authorized}",
            f"implementation_blocked={gate.implementation_blocked}",
            f"runtime_activation_authorized={gate.runtime_activation_authorized}",
            f"runtime_activation_performed={gate.runtime_activation_performed}",
            f"implementation_performed={gate.implementation_performed}",
            f"real_submission_allowed={gate.real_submission_allowed}",
            f"legal_certification={gate.legal_certification}",
            f"decision_gate_check_count={gate.decision_gate_check_count}",
            f"decision_gate_failure_count={gate.decision_gate_failure_count}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 15 - Task 1 - Explicit Operator Decision Gate v1",
            "",
            f"Status: `{gate.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{gate.signature}`",
            f"Baseline commit: `{gate.baseline_commit}`",
            "",
            "## Purpose",
            "",
            "This task opens Milestone 15 as an explicit operator decision gate after Milestone 14 final closure.",
            "",
            "Milestone 15 does not authorize implementation by default.",
            "",
            "## Gate decision",
            "",
            f"- Gate verdict: `{gate.gate_verdict}`",
            f"- Gate decision: `{gate.gate_decision}`",
            f"- Block reason: `{gate.block_reason}`",
            f"- Operator decision value: `{gate.operator_decision_value}`",
            "",
            "## Boundary",
            "",
            f"- milestone_15_opened: `{gate.milestone_15_opened}`",
            f"- operator_decision_required: `{gate.operator_decision_required}`",
            f"- operator_decision_received: `{gate.operator_decision_received}`",
            f"- no_implicit_authorization: `{gate.no_implicit_authorization}`",
            f"- implementation_authorized: `{gate.implementation_authorized}`",
            f"- implementation_blocked: `{gate.implementation_blocked}`",
            f"- runtime_activation_authorized: `{gate.runtime_activation_authorized}`",
            f"- runtime_activation_performed: `{gate.runtime_activation_performed}`",
            f"- implementation_performed: `{gate.implementation_performed}`",
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
    "SOURCE_MILESTONE_14_FINAL_CLOSURE",
    "NEXT_STAGE",
    "Milestone15Task1DecisionGate",
    "ValidationResult",
    "build_milestone_15_task_1_decision_gate",
    "validate_milestone_15_task_1_decision_gate",
    "write_milestone_15_task_1_decision_gate_artifacts",
]
