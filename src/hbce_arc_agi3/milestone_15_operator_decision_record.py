from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TASK_NAME = "MILESTONE_15_TASK_2_OPERATOR_DECISION_RECORD_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_DECISION_RECORD_ONLY_LOCAL_ONLY"
RECORD_STATUS = "OPERATOR_DECISION_RECORD_READY"
RECORD_VERDICT = "OPERATOR_DECISION_NOT_RECEIVED_IMPLEMENTATION_STILL_BLOCKED"
RECORD_DECISION = "RECORD_PENDING_OPERATOR_DECISION_ONLY"
BLOCK_REASON = "NO_EXPLICIT_OPERATOR_DECISION_RECORDED"

PREVIOUS_STAGE = "MILESTONE_15_TASK_1_EXPLICIT_OPERATOR_DECISION_GATE_V1"
SOURCE_MILESTONE_14_FINAL_CLOSURE = "MILESTONE_14_CLOSED_WITHOUT_RUNTIME_ACTIVATION"
NEXT_STAGE = "MILESTONE_15_TASK_3_OPERATOR_DECISION_AUTHORIZATION_BOUNDARY_V1"

SOURCE_TASK_1_FINAL_BASELINE_COMMIT = "ed48f9c"
SOURCE_TASK_1_FINAL_SIGNATURE = "22CAADB16533FB69"
SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT = "f7ee729"
SOURCE_MILESTONE_14_FINAL_SIGNATURE = "05F1CDD559B63B8C"

OUTPUT_DIR = Path("examples/milestone-15/operator-decision-record-v1")
OUTPUT_JSON = OUTPUT_DIR / "milestone-15-operator-decision-record-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-15-operator-decision-record-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-15-operator-decision-record-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-15-operator-decision-record-v1.md"
DOC_PATH = Path("docs/milestone-15-operator-decision-record-v1.md")


DecisionRecordCheck = Literal[
    "TASK_1_DECISION_GATE_CONFIRMED",
    "OPERATOR_DECISION_REQUIRED",
    "OPERATOR_DECISION_NOT_RECEIVED",
    "OPERATOR_DECISION_VALUE_PENDING",
    "NO_AUTHORIZATION_RECORDED",
    "IMPLEMENTATION_REMAINS_BLOCKED",
    "RUNTIME_REMAINS_INACTIVE",
    "REAL_SUBMISSION_REMAINS_BLOCKED",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
]


@dataclass(frozen=True)
class Milestone15Task2OperatorDecisionRecord:
    task_name: str
    status: str
    mode: str
    record_status: str
    record_verdict: str
    record_decision: str
    block_reason: str
    signature: str
    baseline_commit: str

    previous_stage: str
    source_milestone_14_final_closure: str
    next_stage: str

    source_task_1_final_baseline_commit: str
    source_task_1_final_signature: str
    source_milestone_14_final_baseline_commit: str
    source_milestone_14_final_signature: str

    operator_decision_record_created: bool
    operator_decision_required: bool
    operator_decision_received: bool
    operator_decision_value: str
    operator_decision_recorded: bool
    operator_decision_authorizes_implementation: bool
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

    decision_record_checks: tuple[DecisionRecordCheck, ...]
    decision_record_check_count: int
    decision_record_failure_count: int
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


def build_milestone_15_task_2_operator_decision_record(
    *,
    baseline_commit: str | None = None,
) -> Milestone15Task2OperatorDecisionRecord:
    baseline = baseline_commit or _git_head()

    checks: tuple[DecisionRecordCheck, ...] = (
        "TASK_1_DECISION_GATE_CONFIRMED",
        "OPERATOR_DECISION_REQUIRED",
        "OPERATOR_DECISION_NOT_RECEIVED",
        "OPERATOR_DECISION_VALUE_PENDING",
        "NO_AUTHORIZATION_RECORDED",
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
        "next_stage": NEXT_STAGE,
        "record_verdict": RECORD_VERDICT,
        "record_decision": RECORD_DECISION,
        "block_reason": BLOCK_REASON,
        "checks": checks,
    }

    return Milestone15Task2OperatorDecisionRecord(
        task_name=TASK_NAME,
        status=TASK_READY,
        mode=MODE,
        record_status=RECORD_STATUS,
        record_verdict=RECORD_VERDICT,
        record_decision=RECORD_DECISION,
        block_reason=BLOCK_REASON,
        signature=_signature(seed),
        baseline_commit=baseline,
        previous_stage=PREVIOUS_STAGE,
        source_milestone_14_final_closure=SOURCE_MILESTONE_14_FINAL_CLOSURE,
        next_stage=NEXT_STAGE,
        source_task_1_final_baseline_commit=SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
        source_task_1_final_signature=SOURCE_TASK_1_FINAL_SIGNATURE,
        source_milestone_14_final_baseline_commit=SOURCE_MILESTONE_14_FINAL_BASELINE_COMMIT,
        source_milestone_14_final_signature=SOURCE_MILESTONE_14_FINAL_SIGNATURE,
        operator_decision_record_created=True,
        operator_decision_required=True,
        operator_decision_received=False,
        operator_decision_value="PENDING_EXPLICIT_OPERATOR_DECISION",
        operator_decision_recorded=False,
        operator_decision_authorizes_implementation=False,
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
        decision_record_checks=checks,
        decision_record_check_count=len(checks),
        decision_record_failure_count=0,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_15_task_2_operator_decision_record(
    record: Milestone15Task2OperatorDecisionRecord,
) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = {
        "operator_decision_record_created": record.operator_decision_record_created,
        "operator_decision_required": record.operator_decision_required,
        "no_implicit_authorization": record.no_implicit_authorization,
        "implementation_blocked": record.implementation_blocked,
        "public_overfit_guard_required": record.public_overfit_guard_required,
        "fail_closed_required": record.fail_closed_required,
        "fail_closed_active": record.fail_closed_active,
        "public_safe": record.public_safe,
        "deterministic": record.deterministic,
        "local_only": record.local_only,
    }

    for key, value in expected_true.items():
        if value is not True:
            issues.append(f"{key}:expected_true")

    expected_false = {
        "operator_decision_received": record.operator_decision_received,
        "operator_decision_recorded": record.operator_decision_recorded,
        "operator_decision_authorizes_implementation": record.operator_decision_authorizes_implementation,
        "implementation_authorized": record.implementation_authorized,
        "runtime_activation_authorized": record.runtime_activation_authorized,
        "runtime_activation_performed": record.runtime_activation_performed,
        "runtime_execution_performed": record.runtime_execution_performed,
        "runtime_solver_modified": record.runtime_solver_modified,
        "ranker_runtime_modified": record.ranker_runtime_modified,
        "candidate_generator_modified": record.candidate_generator_modified,
        "implementation_performed": record.implementation_performed,
        "real_evaluation_performed": record.real_evaluation_performed,
        "real_submission_allowed": record.real_submission_allowed,
        "ready_for_real_kaggle_submission": record.ready_for_real_kaggle_submission,
        "manual_upload_allowed": record.manual_upload_allowed,
        "kaggle_authentication_allowed": record.kaggle_authentication_allowed,
        "kaggle_authentication_performed": record.kaggle_authentication_performed,
        "kaggle_upload_allowed": record.kaggle_upload_allowed,
        "kaggle_upload_performed": record.kaggle_upload_performed,
        "kaggle_submission_sent": record.kaggle_submission_sent,
        "external_api_dependency": record.external_api_dependency,
        "internet_during_eval": record.internet_during_eval,
        "private_core_exposure": record.private_core_exposure,
        "legal_certification": record.legal_certification,
        "official_score_claim_allowed": record.official_score_claim_allowed,
        "competitive_score_claim_allowed": record.competitive_score_claim_allowed,
        "public_overfit_allowed": record.public_overfit_allowed,
    }

    for key, value in expected_false.items():
        if value is not False:
            issues.append(f"{key}:expected_false")

    if record.record_verdict != RECORD_VERDICT:
        issues.append("record_verdict_mismatch")

    if record.record_decision != RECORD_DECISION:
        issues.append("record_decision_mismatch")

    if record.block_reason != BLOCK_REASON:
        issues.append("block_reason_mismatch")

    if record.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage_mismatch")

    if record.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    if record.operator_decision_value != "PENDING_EXPLICIT_OPERATOR_DECISION":
        issues.append("operator_decision_value_mismatch")

    if record.decision_record_check_count != len(record.decision_record_checks):
        issues.append("decision_record_check_count_mismatch")

    if record.decision_record_failure_count != 0:
        issues.append("decision_record_failure_count_nonzero")

    status = TASK_VALID if not issues else f"{TASK_NAME}_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_15_task_2_operator_decision_record_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[Milestone15Task2OperatorDecisionRecord, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-15-operator-decision-record-v1.json"
    output_index = output_dir / "milestone-15-operator-decision-record-index-v1.json"
    output_manifest = output_dir / "milestone-15-operator-decision-record-manifest-v1.txt"
    output_md = output_dir / "milestone-15-operator-decision-record-v1.md"

    record = build_milestone_15_task_2_operator_decision_record()
    validation = validate_milestone_15_task_2_operator_decision_record(record)

    payload = {
        "record": asdict(record),
        "validation": asdict(validation),
    }

    index = {
        "task_name": record.task_name,
        "status": record.status,
        "validation_status": validation.status,
        "valid": validation.valid,
        "signature": record.signature,
        "baseline_commit": record.baseline_commit,
        "previous_stage": record.previous_stage,
        "next_stage": record.next_stage,
        "record_verdict": record.record_verdict,
        "record_decision": record.record_decision,
        "operator_decision_value": record.operator_decision_value,
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
            f"task_name={record.task_name}",
            f"status={record.status}",
            f"validation_status={validation.status}",
            f"valid={validation.valid}",
            f"signature={record.signature}",
            f"baseline_commit={record.baseline_commit}",
            f"mode={record.mode}",
            f"record_status={record.record_status}",
            f"record_verdict={record.record_verdict}",
            f"record_decision={record.record_decision}",
            f"block_reason={record.block_reason}",
            f"previous_stage={record.previous_stage}",
            f"next_stage={record.next_stage}",
            f"source_task_1_final_baseline_commit={record.source_task_1_final_baseline_commit}",
            f"source_task_1_final_signature={record.source_task_1_final_signature}",
            f"operator_decision_record_created={record.operator_decision_record_created}",
            f"operator_decision_required={record.operator_decision_required}",
            f"operator_decision_received={record.operator_decision_received}",
            f"operator_decision_value={record.operator_decision_value}",
            f"operator_decision_recorded={record.operator_decision_recorded}",
            f"operator_decision_authorizes_implementation={record.operator_decision_authorizes_implementation}",
            f"implementation_authorized={record.implementation_authorized}",
            f"implementation_blocked={record.implementation_blocked}",
            f"runtime_activation_authorized={record.runtime_activation_authorized}",
            f"runtime_activation_performed={record.runtime_activation_performed}",
            f"implementation_performed={record.implementation_performed}",
            f"real_submission_allowed={record.real_submission_allowed}",
            f"legal_certification={record.legal_certification}",
            f"decision_record_check_count={record.decision_record_check_count}",
            f"decision_record_failure_count={record.decision_record_failure_count}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 15 - Task 2 - Operator Decision Record v1",
            "",
            f"Status: `{record.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{record.signature}`",
            f"Baseline commit: `{record.baseline_commit}`",
            "",
            "## Purpose",
            "",
            "This task records the operator decision state after the explicit decision gate.",
            "",
            "No operator decision has been received. No implementation authorization is created.",
            "",
            "## Record decision",
            "",
            f"- Record verdict: `{record.record_verdict}`",
            f"- Record decision: `{record.record_decision}`",
            f"- Block reason: `{record.block_reason}`",
            f"- Operator decision value: `{record.operator_decision_value}`",
            "",
            "## Boundary",
            "",
            f"- operator_decision_required: `{record.operator_decision_required}`",
            f"- operator_decision_received: `{record.operator_decision_received}`",
            f"- operator_decision_recorded: `{record.operator_decision_recorded}`",
            f"- operator_decision_authorizes_implementation: `{record.operator_decision_authorizes_implementation}`",
            f"- implementation_authorized: `{record.implementation_authorized}`",
            f"- implementation_blocked: `{record.implementation_blocked}`",
            f"- runtime_activation_authorized: `{record.runtime_activation_authorized}`",
            f"- runtime_activation_performed: `{record.runtime_activation_performed}`",
            f"- implementation_performed: `{record.implementation_performed}`",
            f"- real_submission_allowed: `{record.real_submission_allowed}`",
            f"- legal_certification: `{record.legal_certification}`",
            "",
        ]
    )

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text(manifest, encoding="utf-8")
    output_md.write_text(md, encoding="utf-8")
    doc_path.write_text(md, encoding="utf-8")

    return record, validation, {
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
    "RECORD_STATUS",
    "RECORD_VERDICT",
    "RECORD_DECISION",
    "BLOCK_REASON",
    "PREVIOUS_STAGE",
    "NEXT_STAGE",
    "Milestone15Task2OperatorDecisionRecord",
    "ValidationResult",
    "build_milestone_15_task_2_operator_decision_record",
    "validate_milestone_15_task_2_operator_decision_record",
    "write_milestone_15_task_2_operator_decision_record_artifacts",
]
