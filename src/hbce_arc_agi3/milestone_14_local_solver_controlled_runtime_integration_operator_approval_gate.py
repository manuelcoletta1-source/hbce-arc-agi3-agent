from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1"
TASK_READY = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1_READY"
TASK_VALID = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1_VALID"
PIPELINE_READY = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1_PIPELINE_READY"

MILESTONE_NUMBER = 14
TASK_NUMBER = 8

SOURCE_TASK = "MILESTONE_14_TASK_7_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1"
NEXT_STAGE = "MILESTONE_14_TASK_9_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"

TASK_MODE = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1_GATE_ONLY_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_READY"
GATE_VERDICT = "OPERATOR_APPROVAL_GATE_CLOSED_IMPLEMENTATION_NOT_AUTHORIZED"
GATE_STATUS = "WAITING_FOR_EXPLICIT_OPERATOR_APPROVAL"

SOURCE_DECISION_ARTIFACT = Path(
    "examples/milestone-14/local-solver-controlled-runtime-integration-implementation-review-decision-v1/"
    "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-v1.json"
)

OUTPUT_DIR = Path(
    "examples/milestone-14/local-solver-controlled-runtime-integration-operator-approval-gate-v1"
)

OUTPUT_JSON = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-v1.md"

DOC_PATH = Path("docs/milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-v1.md")


APPROVAL_REQUIREMENTS = [
    "explicit_operator_approval_statement_required",
    "operator_approval_received_must_be_true",
    "implementation_authorized_must_be_true_after_gate",
    "runtime_activation_must_remain_blocked_before_gate_pass",
    "kaggle_submission_must_remain_blocked",
    "public_overfit_guard_must_remain_active",
    "fail_closed_must_remain_active",
]


GATE_CHECKS = [
    "source_decision_loaded",
    "source_decision_valid",
    "implementation_decision_performed",
    "implementation_blocked_by_source",
    "operator_approval_required",
    "operator_approval_not_received",
    "gate_closed",
    "implementation_not_authorized",
    "runtime_activation_blocked",
    "runtime_execution_blocked",
    "implementation_not_performed",
    "real_submission_blocked",
    "kaggle_score_semantics_not_score",
    "private_core_not_exposed",
    "legal_certification_false",
    "fail_closed_active",
]


@dataclass(frozen=True)
class OperatorApprovalGateRecord:
    task_name: str
    milestone_number: int
    task_number: int
    source_task: str
    next_stage: str
    task_mode: str
    task_verdict: str
    gate_verdict: str
    gate_status: str
    signature: str
    baseline_commit: str
    source_decision_artifact: str
    source_decision_loaded: bool
    source_decision_valid: bool
    source_decision_signature: str
    source_decision_baseline_commit: str
    source_review_signature: str
    source_review_baseline_commit: str
    implementation_review_decision_performed: bool
    source_implementation_authorized: bool
    source_implementation_blocked: bool
    source_implementation_block_reason: str
    operator_approval_gate_performed: bool
    operator_approval_gate_open: bool
    operator_approval_gate_closed: bool
    operator_approval_required: bool
    operator_approval_received: bool
    operator_approval_statement_required: bool
    implementation_authorized: bool
    implementation_blocked: bool
    implementation_block_reason: str
    approval_requirement_count: int
    approval_requirement_pass_count: int
    approval_requirement_failure_count: int
    gate_check_count: int
    gate_check_pass_count: int
    gate_check_failure_count: int
    blocking_issue_count: int
    issue_count: int
    warning_count: int
    gate_only: bool
    decision_only: bool
    review_only: bool
    dry_run_only: bool
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
    kaggle_score_semantics: str
    local_only: bool
    deterministic: bool
    public_safe: bool
    public_overfit_allowed: bool
    public_overfit_guard_required: bool
    fail_closed_required: bool
    fail_closed_active: bool
    approval_requirements: list[str]
    gate_checks: list[str]
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


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _source_payload(path: Path) -> dict[str, dict[str, Any]]:
    raw = _load_json(path)
    record = raw.get("record")
    validation = raw.get("validation")
    if isinstance(record, dict) and isinstance(validation, dict):
        return {"record": record, "validation": validation}
    return {"record": {}, "validation": {}}


def _source_decision_valid(source: dict[str, dict[str, Any]]) -> bool:
    record = source["record"]
    validation = source["validation"]
    return (
        bool(record)
        and bool(validation)
        and validation.get("valid") is True
        and validation.get("status") == "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1_VALID"
        and record.get("implementation_review_decision_performed") is True
        and record.get("implementation_authorized") is False
        and record.get("implementation_blocked") is True
        and record.get("implementation_block_reason") == "EXPLICIT_OPERATOR_APPROVAL_NOT_RECEIVED"
        and record.get("operator_approval_required") is True
        and record.get("operator_approval_received") is False
        and record.get("runtime_activation_performed") is False
        and record.get("runtime_execution_performed") is False
        and record.get("implementation_performed") is False
        and record.get("real_submission_allowed") is False
        and record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
        and record.get("private_core_exposure") is False
        and record.get("legal_certification") is False
        and record.get("fail_closed_active") is True
    )


def _signature(seed: dict[str, Any]) -> str:
    canonical = json.dumps(seed, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16].upper()


def build_milestone_14_task_8_operator_approval_gate_record(
    *,
    baseline_commit: str | None = None,
    source_decision_artifact: Path = SOURCE_DECISION_ARTIFACT,
) -> OperatorApprovalGateRecord:
    baseline = baseline_commit or _git_head()
    source = _source_payload(source_decision_artifact)
    source_record = source["record"]
    source_valid = _source_decision_valid(source)

    gate_results = {
        "source_decision_loaded": bool(source_record),
        "source_decision_valid": source_valid,
        "implementation_decision_performed": source_record.get("implementation_review_decision_performed") is True,
        "implementation_blocked_by_source": source_record.get("implementation_blocked") is True,
        "operator_approval_required": source_record.get("operator_approval_required") is True,
        "operator_approval_not_received": source_record.get("operator_approval_received") is False,
        "gate_closed": True,
        "implementation_not_authorized": True,
        "runtime_activation_blocked": source_record.get("runtime_activation_performed") is False,
        "runtime_execution_blocked": source_record.get("runtime_execution_performed") is False,
        "implementation_not_performed": source_record.get("implementation_performed") is False,
        "real_submission_blocked": source_record.get("real_submission_allowed") is False,
        "kaggle_score_semantics_not_score": source_record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "private_core_not_exposed": source_record.get("private_core_exposure") is False,
        "legal_certification_false": source_record.get("legal_certification") is False,
        "fail_closed_active": source_record.get("fail_closed_active") is True,
    }

    failing = [name for name, passed in gate_results.items() if not passed]

    seed = {
        "task": TASK_NAME,
        "baseline_commit": baseline,
        "source_decision_signature": source_record.get("signature", "NO_SOURCE_DECISION_SIGNATURE"),
        "gate_verdict": GATE_VERDICT,
        "gate_status": GATE_STATUS,
        "gate_results": gate_results,
        "operator_approval_received": False,
    }

    return OperatorApprovalGateRecord(
        task_name=TASK_NAME,
        milestone_number=MILESTONE_NUMBER,
        task_number=TASK_NUMBER,
        source_task=SOURCE_TASK,
        next_stage=NEXT_STAGE,
        task_mode=TASK_MODE,
        task_verdict=TASK_VERDICT,
        gate_verdict=GATE_VERDICT,
        gate_status=GATE_STATUS,
        signature=_signature(seed),
        baseline_commit=baseline,
        source_decision_artifact=str(source_decision_artifact),
        source_decision_loaded=bool(source_record),
        source_decision_valid=source_valid,
        source_decision_signature=str(source_record.get("signature", "NO_SOURCE_DECISION_SIGNATURE")),
        source_decision_baseline_commit=str(source_record.get("baseline_commit", "NO_SOURCE_DECISION_BASELINE")),
        source_review_signature=str(source_record.get("source_review_signature", "NO_SOURCE_REVIEW_SIGNATURE")),
        source_review_baseline_commit=str(source_record.get("source_review_baseline_commit", "NO_SOURCE_REVIEW_BASELINE")),
        implementation_review_decision_performed=source_record.get("implementation_review_decision_performed") is True,
        source_implementation_authorized=source_record.get("implementation_authorized") is True,
        source_implementation_blocked=source_record.get("implementation_blocked") is True,
        source_implementation_block_reason=str(source_record.get("implementation_block_reason", "NO_SOURCE_BLOCK_REASON")),
        operator_approval_gate_performed=True,
        operator_approval_gate_open=False,
        operator_approval_gate_closed=True,
        operator_approval_required=True,
        operator_approval_received=False,
        operator_approval_statement_required=True,
        implementation_authorized=False,
        implementation_blocked=True,
        implementation_block_reason="OPERATOR_APPROVAL_GATE_CLOSED",
        approval_requirement_count=len(APPROVAL_REQUIREMENTS),
        approval_requirement_pass_count=len(APPROVAL_REQUIREMENTS),
        approval_requirement_failure_count=0,
        gate_check_count=len(gate_results),
        gate_check_pass_count=len(gate_results) - len(failing),
        gate_check_failure_count=len(failing),
        blocking_issue_count=0 if not failing else len(failing),
        issue_count=0 if not failing else len(failing),
        warning_count=0,
        gate_only=True,
        decision_only=True,
        review_only=True,
        dry_run_only=True,
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
        kaggle_score_semantics="NOT_A_KAGGLE_SCORE",
        local_only=True,
        deterministic=True,
        public_safe=True,
        public_overfit_allowed=False,
        public_overfit_guard_required=True,
        fail_closed_required=True,
        fail_closed_active=True,
        approval_requirements=APPROVAL_REQUIREMENTS,
        gate_checks=GATE_CHECKS,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_14_task_8_operator_approval_gate_record(record: OperatorApprovalGateRecord) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected = {
        "source_decision_loaded": True,
        "source_decision_valid": True,
        "implementation_review_decision_performed": True,
        "source_implementation_authorized": False,
        "source_implementation_blocked": True,
        "source_implementation_block_reason": "EXPLICIT_OPERATOR_APPROVAL_NOT_RECEIVED",
        "operator_approval_gate_performed": True,
        "operator_approval_gate_open": False,
        "operator_approval_gate_closed": True,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "operator_approval_statement_required": True,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_block_reason": "OPERATOR_APPROVAL_GATE_CLOSED",
        "approval_requirement_count": 7,
        "approval_requirement_pass_count": 7,
        "approval_requirement_failure_count": 0,
        "gate_check_count": 16,
        "gate_check_pass_count": 16,
        "gate_check_failure_count": 0,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
        "gate_only": True,
        "decision_only": True,
        "review_only": True,
        "dry_run_only": True,
        "runtime_activation_performed": False,
        "runtime_execution_performed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "candidate_generator_modified": False,
        "implementation_performed": False,
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
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
    }

    data = asdict(record)
    for key, value in expected.items():
        if data.get(key) != value:
            issues.append(f"{key}: expected {value!r}, got {data.get(key)!r}")

    if record.task_name != TASK_NAME:
        issues.append("task_name_mismatch")

    if record.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    if record.gate_verdict != GATE_VERDICT:
        issues.append("gate_verdict_mismatch")

    if record.gate_status != GATE_STATUS:
        issues.append("gate_status_mismatch")

    status = TASK_VALID if not issues else "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_14_task_8_operator_approval_gate_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[OperatorApprovalGateRecord, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-v1.json"
    output_index = output_dir / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-index-v1.json"
    output_manifest = output_dir / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-manifest-v1.txt"
    output_md = output_dir / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-v1.md"

    record = build_milestone_14_task_8_operator_approval_gate_record()
    validation = validate_milestone_14_task_8_operator_approval_gate_record(record)

    payload = {
        "record": asdict(record),
        "validation": asdict(validation),
    }

    index = {
        "task_name": record.task_name,
        "status": TASK_READY,
        "validation_status": validation.status,
        "valid": validation.valid,
        "signature": record.signature,
        "baseline_commit": record.baseline_commit,
        "source_decision_signature": record.source_decision_signature,
        "source_decision_baseline_commit": record.source_decision_baseline_commit,
        "gate_verdict": record.gate_verdict,
        "gate_status": record.gate_status,
        "operator_approval_required": record.operator_approval_required,
        "operator_approval_received": record.operator_approval_received,
        "implementation_authorized": record.implementation_authorized,
        "implementation_blocked": record.implementation_blocked,
        "next_stage": record.next_stage,
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
            f"status={TASK_READY}",
            f"validation_status={validation.status}",
            f"valid={validation.valid}",
            f"signature={record.signature}",
            f"baseline_commit={record.baseline_commit}",
            f"source_decision_signature={record.source_decision_signature}",
            f"source_decision_baseline_commit={record.source_decision_baseline_commit}",
            f"task_mode={record.task_mode}",
            f"task_verdict={record.task_verdict}",
            f"gate_verdict={record.gate_verdict}",
            f"gate_status={record.gate_status}",
            f"next_stage={record.next_stage}",
            f"operator_approval_gate_performed={record.operator_approval_gate_performed}",
            f"operator_approval_gate_open={record.operator_approval_gate_open}",
            f"operator_approval_gate_closed={record.operator_approval_gate_closed}",
            f"operator_approval_required={record.operator_approval_required}",
            f"operator_approval_received={record.operator_approval_received}",
            f"implementation_authorized={record.implementation_authorized}",
            f"implementation_blocked={record.implementation_blocked}",
            f"implementation_block_reason={record.implementation_block_reason}",
            f"gate_check_count={record.gate_check_count}",
            f"gate_check_failure_count={record.gate_check_failure_count}",
            f"kaggle_score_semantics={record.kaggle_score_semantics}",
            f"runtime_activation_performed={record.runtime_activation_performed}",
            f"runtime_execution_performed={record.runtime_execution_performed}",
            f"implementation_performed={record.implementation_performed}",
            f"real_submission_allowed={record.real_submission_allowed}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 14 Task 8 — Local Solver Controlled Runtime Integration Operator Approval Gate v1",
            "",
            f"Status: `{TASK_READY}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{record.signature}`",
            f"Baseline commit: `{record.baseline_commit}`",
            "",
            "## Gate",
            "",
            f"`{record.gate_verdict}`",
            "",
            f"Gate status: `{record.gate_status}`",
            f"Gate open: `{record.operator_approval_gate_open}`",
            f"Gate closed: `{record.operator_approval_gate_closed}`",
            f"Operator approval required: `{record.operator_approval_required}`",
            f"Operator approval received: `{record.operator_approval_received}`",
            f"Implementation authorized: `{record.implementation_authorized}`",
            f"Implementation blocked: `{record.implementation_blocked}`",
            f"Block reason: `{record.implementation_block_reason}`",
            "",
            "## Source decision",
            "",
            f"- source_decision_signature: `{record.source_decision_signature}`",
            f"- source_decision_baseline_commit: `{record.source_decision_baseline_commit}`",
            f"- source_decision_valid: `{record.source_decision_valid}`",
            "",
            "## Boundary",
            "",
            f"- gate_only: `{record.gate_only}`",
            f"- decision_only: `{record.decision_only}`",
            f"- review_only: `{record.review_only}`",
            f"- dry_run_only: `{record.dry_run_only}`",
            f"- implementation_performed: `{record.implementation_performed}`",
            f"- runtime_activation_performed: `{record.runtime_activation_performed}`",
            f"- runtime_execution_performed: `{record.runtime_execution_performed}`",
            f"- real_submission_allowed: `{record.real_submission_allowed}`",
            f"- kaggle_score_semantics: `{record.kaggle_score_semantics}`",
            "",
            "## Next stage",
            "",
            f"`{record.next_stage}`",
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
    "TASK_READY",
    "TASK_VALID",
    "PIPELINE_READY",
    "NEXT_STAGE",
    "TASK_MODE",
    "TASK_VERDICT",
    "GATE_VERDICT",
    "GATE_STATUS",
    "OperatorApprovalGateRecord",
    "ValidationResult",
    "build_milestone_14_task_8_operator_approval_gate_record",
    "validate_milestone_14_task_8_operator_approval_gate_record",
    "write_milestone_14_task_8_operator_approval_gate_artifacts",
]
