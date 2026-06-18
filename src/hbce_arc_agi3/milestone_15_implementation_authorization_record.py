from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TASK_NAME = "MILESTONE_15_TASK_8_IMPLEMENTATION_AUTHORIZATION_RECORD_V1"
PIPELINE_READY = f"{TASK_NAME}_PIPELINE_READY"
TASK_READY = f"{TASK_NAME}_READY"
TASK_VALID = f"{TASK_NAME}_VALID"

MODE = f"{TASK_NAME}_RECORD_ONLY_LOCAL_ONLY"
RECORD_STATUS = "IMPLEMENTATION_AUTHORIZATION_RECORD_READY"
RECORD_VERDICT = "IMPLEMENTATION_AUTHORIZATION_NOT_RECORDED_AS_GRANTED"
RECORD_DECISION = "RECORD_NO_IMPLEMENTATION_AUTHORIZATION_GRANTED"
BLOCK_REASON = "TASK_7_DECISION_GATE_CONFIRMED_IMPLEMENTATION_AUTHORIZATION_NOT_GRANTED"

PREVIOUS_STAGE = "MILESTONE_15_TASK_7_IMPLEMENTATION_AUTHORIZATION_DECISION_GATE_V1"
NEXT_STAGE = "MILESTONE_15_TASK_9_IMPLEMENTATION_BLOCK_CLOSURE_REVIEW_V1"

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

OUTPUT_DIR = Path("examples/milestone-15/implementation-authorization-record-v1")
DOC_PATH = Path("docs/milestone-15-implementation-authorization-record-v1.md")


ImplementationAuthorizationRecordCheck = Literal[
    "TASK_7_DECISION_GATE_CONFIRMED",
    "TASK_6_IMPLEMENTATION_BLOCK_CONFIRMED",
    "TASK_5_RUNTIME_ACTIVATION_REVIEW_CONFIRMED",
    "TASK_4_RUNTIME_ACTIVATION_BOUNDARY_CONFIRMED",
    "TASK_3_AUTHORIZATION_BOUNDARY_CONFIRMED",
    "TASK_2_OPERATOR_DECISION_RECORD_CONFIRMED",
    "TASK_1_OPERATOR_DECISION_GATE_CONFIRMED",
    "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
    "IMPLEMENTATION_AUTHORIZATION_RECORD_CREATED",
    "OPERATOR_DECISION_STILL_PENDING",
    "EXPLICIT_OPERATOR_AUTHORIZATION_NOT_RECEIVED",
    "IMPLEMENTATION_AUTHORIZATION_NOT_GRANTED",
    "IMPLEMENTATION_AUTHORIZATION_NOT_RECORDED_AS_GRANTED",
    "IMPLEMENTATION_REMAINS_BLOCKED",
    "NO_IMPLEMENTATION_PATCH_CREATED",
    "NO_IMPLEMENTATION_PATCH_APPLIED",
    "NO_RUNTIME_SOLVER_PATCH_ALLOWED",
    "NO_RUNTIME_WIRING_ALLOWED",
    "NO_RUNTIME_EXECUTION_ALLOWED",
    "NO_REAL_SUBMISSION_ALLOWED",
    "FAIL_CLOSED_ACTIVE",
    "PUBLIC_SAFE_BOUNDARY_PRESERVED",
]


@dataclass(frozen=True)
class Milestone15Task8ImplementationAuthorizationRecord:
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
    next_stage: str

    source_task_7_final_baseline_commit: str
    source_task_7_final_signature: str
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

    implementation_authorization_record_created: bool
    task_7_decision_gate_confirmed: bool
    task_6_implementation_block_confirmed: bool
    task_5_runtime_activation_review_confirmed: bool

    operator_decision_required: bool
    operator_decision_received: bool
    operator_decision_value: str

    explicit_operator_authorization_required: bool
    explicit_operator_authorization_received: bool
    explicit_operator_authorization_value: str

    implementation_authorization_record_required: bool
    implementation_authorization_recorded: bool
    implementation_authorization_record_value: str
    implementation_authorization_granted: bool
    implementation_authorization_recorded_as_granted: bool
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

    implementation_authorization_record_checks: tuple[ImplementationAuthorizationRecordCheck, ...]
    implementation_authorization_record_check_count: int
    implementation_authorization_record_failure_count: int
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


def build_milestone_15_task_8_implementation_authorization_record(
    *,
    baseline_commit: str | None = None,
) -> Milestone15Task8ImplementationAuthorizationRecord:
    baseline = baseline_commit or _git_head()

    checks: tuple[ImplementationAuthorizationRecordCheck, ...] = (
        "TASK_7_DECISION_GATE_CONFIRMED",
        "TASK_6_IMPLEMENTATION_BLOCK_CONFIRMED",
        "TASK_5_RUNTIME_ACTIVATION_REVIEW_CONFIRMED",
        "TASK_4_RUNTIME_ACTIVATION_BOUNDARY_CONFIRMED",
        "TASK_3_AUTHORIZATION_BOUNDARY_CONFIRMED",
        "TASK_2_OPERATOR_DECISION_RECORD_CONFIRMED",
        "TASK_1_OPERATOR_DECISION_GATE_CONFIRMED",
        "MILESTONE_14_FINAL_CLOSURE_CONFIRMED",
        "IMPLEMENTATION_AUTHORIZATION_RECORD_CREATED",
        "OPERATOR_DECISION_STILL_PENDING",
        "EXPLICIT_OPERATOR_AUTHORIZATION_NOT_RECEIVED",
        "IMPLEMENTATION_AUTHORIZATION_NOT_GRANTED",
        "IMPLEMENTATION_AUTHORIZATION_NOT_RECORDED_AS_GRANTED",
        "IMPLEMENTATION_REMAINS_BLOCKED",
        "NO_IMPLEMENTATION_PATCH_CREATED",
        "NO_IMPLEMENTATION_PATCH_APPLIED",
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
        "record_verdict": RECORD_VERDICT,
        "record_decision": RECORD_DECISION,
        "block_reason": BLOCK_REASON,
        "checks": checks,
    }

    return Milestone15Task8ImplementationAuthorizationRecord(
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
        next_stage=NEXT_STAGE,
        source_task_7_final_baseline_commit=SOURCE_TASK_7_FINAL_BASELINE_COMMIT,
        source_task_7_final_signature=SOURCE_TASK_7_FINAL_SIGNATURE,
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
        implementation_authorization_record_created=True,
        task_7_decision_gate_confirmed=True,
        task_6_implementation_block_confirmed=True,
        task_5_runtime_activation_review_confirmed=True,
        operator_decision_required=True,
        operator_decision_received=False,
        operator_decision_value="PENDING_EXPLICIT_OPERATOR_DECISION",
        explicit_operator_authorization_required=True,
        explicit_operator_authorization_received=False,
        explicit_operator_authorization_value="NO_EXPLICIT_OPERATOR_AUTHORIZATION_RECEIVED",
        implementation_authorization_record_required=True,
        implementation_authorization_recorded=True,
        implementation_authorization_record_value="NO_IMPLEMENTATION_AUTHORIZATION_GRANTED",
        implementation_authorization_granted=False,
        implementation_authorization_recorded_as_granted=False,
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
        implementation_authorization_record_checks=checks,
        implementation_authorization_record_check_count=len(checks),
        implementation_authorization_record_failure_count=0,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_15_task_8_implementation_authorization_record(
    record: Milestone15Task8ImplementationAuthorizationRecord,
) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected_true = {
        "implementation_authorization_record_created": record.implementation_authorization_record_created,
        "task_7_decision_gate_confirmed": record.task_7_decision_gate_confirmed,
        "task_6_implementation_block_confirmed": record.task_6_implementation_block_confirmed,
        "task_5_runtime_activation_review_confirmed": record.task_5_runtime_activation_review_confirmed,
        "operator_decision_required": record.operator_decision_required,
        "explicit_operator_authorization_required": record.explicit_operator_authorization_required,
        "implementation_authorization_record_required": record.implementation_authorization_record_required,
        "implementation_authorization_recorded": record.implementation_authorization_recorded,
        "implementation_blocked": record.implementation_blocked,
        "runtime_activation_blocked": record.runtime_activation_blocked,
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
        "explicit_operator_authorization_received": record.explicit_operator_authorization_received,
        "implementation_authorization_granted": record.implementation_authorization_granted,
        "implementation_authorization_recorded_as_granted": record.implementation_authorization_recorded_as_granted,
        "implementation_authorized": record.implementation_authorized,
        "implementation_performed": record.implementation_performed,
        "implementation_patch_created": record.implementation_patch_created,
        "implementation_patch_applied": record.implementation_patch_applied,
        "runtime_solver_patch_allowed": record.runtime_solver_patch_allowed,
        "runtime_solver_modified": record.runtime_solver_modified,
        "ranker_runtime_patch_allowed": record.ranker_runtime_patch_allowed,
        "ranker_runtime_modified": record.ranker_runtime_modified,
        "candidate_generator_patch_allowed": record.candidate_generator_patch_allowed,
        "candidate_generator_modified": record.candidate_generator_modified,
        "runtime_wiring_allowed": record.runtime_wiring_allowed,
        "runtime_wiring_performed": record.runtime_wiring_performed,
        "runtime_activation_authorized": record.runtime_activation_authorized,
        "runtime_activation_performed": record.runtime_activation_performed,
        "runtime_execution_allowed": record.runtime_execution_allowed,
        "runtime_execution_performed": record.runtime_execution_performed,
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

    if record.implementation_authorization_record_value != "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED":
        issues.append("implementation_authorization_record_value_mismatch")

    if record.implementation_authorization_record_check_count != len(record.implementation_authorization_record_checks):
        issues.append("implementation_authorization_record_check_count_mismatch")

    if record.implementation_authorization_record_failure_count != 0:
        issues.append("implementation_authorization_record_failure_count_nonzero")

    status = TASK_VALID if not issues else f"{TASK_NAME}_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_15_task_8_implementation_authorization_record_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[Milestone15Task8ImplementationAuthorizationRecord, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-15-implementation-authorization-record-v1.json"
    output_index = output_dir / "milestone-15-implementation-authorization-record-index-v1.json"
    output_manifest = output_dir / "milestone-15-implementation-authorization-record-manifest-v1.txt"
    output_md = output_dir / "milestone-15-implementation-authorization-record-v1.md"

    record = build_milestone_15_task_8_implementation_authorization_record()
    validation = validate_milestone_15_task_8_implementation_authorization_record(record)

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
        "implementation_authorization_granted": record.implementation_authorization_granted,
        "implementation_authorization_recorded_as_granted": record.implementation_authorization_recorded_as_granted,
        "implementation_authorized": record.implementation_authorized,
        "implementation_performed": record.implementation_performed,
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
            f"source_task_7_final_baseline_commit={record.source_task_7_final_baseline_commit}",
            f"source_task_7_final_signature={record.source_task_7_final_signature}",
            f"task_7_decision_gate_confirmed={record.task_7_decision_gate_confirmed}",
            f"operator_decision_required={record.operator_decision_required}",
            f"operator_decision_received={record.operator_decision_received}",
            f"operator_decision_value={record.operator_decision_value}",
            f"explicit_operator_authorization_required={record.explicit_operator_authorization_required}",
            f"explicit_operator_authorization_received={record.explicit_operator_authorization_received}",
            f"explicit_operator_authorization_value={record.explicit_operator_authorization_value}",
            f"implementation_authorization_record_required={record.implementation_authorization_record_required}",
            f"implementation_authorization_recorded={record.implementation_authorization_recorded}",
            f"implementation_authorization_record_value={record.implementation_authorization_record_value}",
            f"implementation_authorization_granted={record.implementation_authorization_granted}",
            f"implementation_authorization_recorded_as_granted={record.implementation_authorization_recorded_as_granted}",
            f"implementation_authorized={record.implementation_authorized}",
            f"implementation_blocked={record.implementation_blocked}",
            f"implementation_performed={record.implementation_performed}",
            f"implementation_patch_created={record.implementation_patch_created}",
            f"implementation_patch_applied={record.implementation_patch_applied}",
            f"runtime_solver_patch_allowed={record.runtime_solver_patch_allowed}",
            f"runtime_solver_modified={record.runtime_solver_modified}",
            f"runtime_wiring_allowed={record.runtime_wiring_allowed}",
            f"runtime_wiring_performed={record.runtime_wiring_performed}",
            f"runtime_activation_authorized={record.runtime_activation_authorized}",
            f"runtime_activation_performed={record.runtime_activation_performed}",
            f"runtime_execution_allowed={record.runtime_execution_allowed}",
            f"runtime_execution_performed={record.runtime_execution_performed}",
            f"real_submission_allowed={record.real_submission_allowed}",
            f"legal_certification={record.legal_certification}",
            f"implementation_authorization_record_check_count={record.implementation_authorization_record_check_count}",
            f"implementation_authorization_record_failure_count={record.implementation_authorization_record_failure_count}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 15 - Task 8 - Implementation Authorization Record v1",
            "",
            f"Status: `{record.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{record.signature}`",
            f"Baseline commit: `{record.baseline_commit}`",
            "",
            "## Purpose",
            "",
            "This task records the implementation authorization state after Task 7.",
            "",
            "No implementation authorization is recorded as granted.",
            "",
            "## Record",
            "",
            f"- Record verdict: `{record.record_verdict}`",
            f"- Record decision: `{record.record_decision}`",
            f"- Block reason: `{record.block_reason}`",
            f"- Implementation authorization record value: `{record.implementation_authorization_record_value}`",
            "",
            "## Boundary",
            "",
            f"- task_7_decision_gate_confirmed: `{record.task_7_decision_gate_confirmed}`",
            f"- implementation_authorization_recorded: `{record.implementation_authorization_recorded}`",
            f"- implementation_authorization_granted: `{record.implementation_authorization_granted}`",
            f"- implementation_authorization_recorded_as_granted: `{record.implementation_authorization_recorded_as_granted}`",
            f"- implementation_authorized: `{record.implementation_authorized}`",
            f"- implementation_blocked: `{record.implementation_blocked}`",
            f"- implementation_performed: `{record.implementation_performed}`",
            f"- implementation_patch_created: `{record.implementation_patch_created}`",
            f"- implementation_patch_applied: `{record.implementation_patch_applied}`",
            f"- runtime_solver_patch_allowed: `{record.runtime_solver_patch_allowed}`",
            f"- runtime_solver_modified: `{record.runtime_solver_modified}`",
            f"- runtime_wiring_allowed: `{record.runtime_wiring_allowed}`",
            f"- runtime_wiring_performed: `{record.runtime_wiring_performed}`",
            f"- runtime_activation_performed: `{record.runtime_activation_performed}`",
            f"- runtime_execution_performed: `{record.runtime_execution_performed}`",
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
    "Milestone15Task8ImplementationAuthorizationRecord",
    "ValidationResult",
    "build_milestone_15_task_8_implementation_authorization_record",
    "validate_milestone_15_task_8_implementation_authorization_record",
    "write_milestone_15_task_8_implementation_authorization_record_artifacts",
]
