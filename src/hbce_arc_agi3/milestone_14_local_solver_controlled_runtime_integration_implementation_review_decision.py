from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1"
TASK_READY = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1_READY"
TASK_VALID = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1_VALID"
PIPELINE_READY = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1_PIPELINE_READY"

MILESTONE_NUMBER = 14
TASK_NUMBER = 7

SOURCE_TASK = "MILESTONE_14_TASK_6_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1"
NEXT_STAGE = "MILESTONE_14_TASK_8_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1"

TASK_MODE = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1_DECISION_ONLY_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_READY"
DECISION_VERDICT = "IMPLEMENTATION_DECISION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL"
DECISION_STATUS = "REVIEW_PASSED_IMPLEMENTATION_NOT_AUTHORIZED"

SOURCE_REVIEW_ARTIFACT = Path(
    "examples/milestone-14/local-solver-controlled-runtime-integration-implementation-dry-run-review-v1/"
    "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-v1.json"
)

OUTPUT_DIR = Path(
    "examples/milestone-14/local-solver-controlled-runtime-integration-implementation-review-decision-v1"
)

OUTPUT_JSON = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-v1.md"

DOC_PATH = Path("docs/milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-v1.md")


DECISION_GATES = [
    "source_review_loaded",
    "source_review_valid",
    "dry_run_review_passed",
    "ready_for_review_decision",
    "review_gate_count_verified",
    "review_gate_failure_count_zero",
    "source_dry_run_valid",
    "kaggle_score_semantics_not_score",
    "runtime_activation_blocked",
    "runtime_execution_blocked",
    "runtime_solver_unmodified",
    "ranker_runtime_unmodified",
    "candidate_generator_unmodified",
    "implementation_not_performed",
    "real_submission_blocked",
    "operator_approval_required",
    "operator_approval_not_received",
    "decision_blocks_implementation",
    "next_stage_is_operator_approval_gate",
    "fail_closed_active",
]


DECISION_FINDINGS = [
    {
        "finding_id": "M14-T7-FINDING-001",
        "finding": "task_6_review_passed",
        "severity": "PASS",
    },
    {
        "finding_id": "M14-T7-FINDING-002",
        "finding": "dry_run_valid_but_not_authorizing_runtime_change",
        "severity": "PASS",
    },
    {
        "finding_id": "M14-T7-FINDING-003",
        "finding": "explicit_operator_approval_missing",
        "severity": "BLOCKING_BY_POLICY",
    },
    {
        "finding_id": "M14-T7-FINDING-004",
        "finding": "implementation_blocked_pending_operator_gate",
        "severity": "PASS",
    },
]


@dataclass(frozen=True)
class ReviewDecisionRecord:
    task_name: str
    milestone_number: int
    task_number: int
    source_task: str
    next_stage: str
    task_mode: str
    task_verdict: str
    decision_verdict: str
    decision_status: str
    signature: str
    baseline_commit: str
    source_review_artifact: str
    source_review_loaded: bool
    source_review_valid: bool
    source_review_signature: str
    source_review_baseline_commit: str
    source_dry_run_signature: str
    source_dry_run_baseline_commit: str
    dry_run_review_performed: bool
    dry_run_review_passed: bool
    ready_for_review_decision: bool
    implementation_review_decision_performed: bool
    implementation_review_decision_passed: bool
    implementation_authorized: bool
    implementation_blocked: bool
    implementation_block_reason: str
    operator_approval_gate_required_next: bool
    decision_gate_count: int
    decision_gate_pass_count: int
    decision_gate_failure_count: int
    decision_finding_count: int
    blocking_issue_count: int
    issue_count: int
    warning_count: int
    review_gate_count: int
    review_gate_failure_count: int
    review_only: bool
    decision_only: bool
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
    operator_approval_required: bool
    operator_approval_received: bool
    fail_closed_required: bool
    fail_closed_active: bool
    decision_gates: list[str]
    decision_findings: list[dict[str, str]]
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


def _source_review_valid(source: dict[str, dict[str, Any]]) -> bool:
    record = source["record"]
    validation = source["validation"]
    return (
        bool(record)
        and bool(validation)
        and validation.get("valid") is True
        and validation.get("status") == "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1_VALID"
        and record.get("dry_run_review_performed") is True
        and record.get("dry_run_review_passed") is True
        and record.get("ready_for_review_decision") is True
        and record.get("review_gate_count") == 27
        and record.get("review_gate_failure_count") == 0
        and record.get("source_dry_run_valid") is True
        and record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
        and record.get("runtime_activation_performed") is False
        and record.get("runtime_execution_performed") is False
        and record.get("runtime_solver_modified") is False
        and record.get("ranker_runtime_modified") is False
        and record.get("candidate_generator_modified") is False
        and record.get("implementation_performed") is False
        and record.get("real_submission_allowed") is False
        and record.get("operator_approval_received") is False
        and record.get("fail_closed_active") is True
    )


def _signature(seed: dict[str, Any]) -> str:
    canonical = json.dumps(seed, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16].upper()


def build_milestone_14_task_7_review_decision_record(
    *,
    baseline_commit: str | None = None,
    source_review_artifact: Path = SOURCE_REVIEW_ARTIFACT,
) -> ReviewDecisionRecord:
    baseline = baseline_commit or _git_head()
    source = _source_payload(source_review_artifact)
    source_record = source["record"]
    source_valid = _source_review_valid(source)

    gate_results = {
        "source_review_loaded": bool(source_record),
        "source_review_valid": source_valid,
        "dry_run_review_passed": source_record.get("dry_run_review_passed") is True,
        "ready_for_review_decision": source_record.get("ready_for_review_decision") is True,
        "review_gate_count_verified": source_record.get("review_gate_count") == 27,
        "review_gate_failure_count_zero": source_record.get("review_gate_failure_count") == 0,
        "source_dry_run_valid": source_record.get("source_dry_run_valid") is True,
        "kaggle_score_semantics_not_score": source_record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "runtime_activation_blocked": source_record.get("runtime_activation_performed") is False,
        "runtime_execution_blocked": source_record.get("runtime_execution_performed") is False,
        "runtime_solver_unmodified": source_record.get("runtime_solver_modified") is False,
        "ranker_runtime_unmodified": source_record.get("ranker_runtime_modified") is False,
        "candidate_generator_unmodified": source_record.get("candidate_generator_modified") is False,
        "implementation_not_performed": source_record.get("implementation_performed") is False,
        "real_submission_blocked": source_record.get("real_submission_allowed") is False,
        "operator_approval_required": True,
        "operator_approval_not_received": source_record.get("operator_approval_received") is False,
        "decision_blocks_implementation": True,
        "next_stage_is_operator_approval_gate": NEXT_STAGE.endswith("OPERATOR_APPROVAL_GATE_V1"),
        "fail_closed_active": source_record.get("fail_closed_active") is True,
    }

    failing = [name for name, passed in gate_results.items() if not passed]

    seed = {
        "task": TASK_NAME,
        "baseline_commit": baseline,
        "source_review_signature": source_record.get("signature", "NO_SOURCE_REVIEW_SIGNATURE"),
        "source_review_baseline": source_record.get("baseline_commit", "NO_SOURCE_REVIEW_BASELINE"),
        "decision_verdict": DECISION_VERDICT,
        "decision_status": DECISION_STATUS,
        "decision_gates": gate_results,
    }

    return ReviewDecisionRecord(
        task_name=TASK_NAME,
        milestone_number=MILESTONE_NUMBER,
        task_number=TASK_NUMBER,
        source_task=SOURCE_TASK,
        next_stage=NEXT_STAGE,
        task_mode=TASK_MODE,
        task_verdict=TASK_VERDICT,
        decision_verdict=DECISION_VERDICT,
        decision_status=DECISION_STATUS,
        signature=_signature(seed),
        baseline_commit=baseline,
        source_review_artifact=str(source_review_artifact),
        source_review_loaded=bool(source_record),
        source_review_valid=source_valid,
        source_review_signature=str(source_record.get("signature", "NO_SOURCE_REVIEW_SIGNATURE")),
        source_review_baseline_commit=str(source_record.get("baseline_commit", "NO_SOURCE_REVIEW_BASELINE")),
        source_dry_run_signature=str(source_record.get("source_dry_run_signature", "NO_SOURCE_DRY_RUN_SIGNATURE")),
        source_dry_run_baseline_commit=str(source_record.get("source_dry_run_baseline_commit", "NO_SOURCE_DRY_RUN_BASELINE")),
        dry_run_review_performed=source_record.get("dry_run_review_performed") is True,
        dry_run_review_passed=source_record.get("dry_run_review_passed") is True,
        ready_for_review_decision=source_record.get("ready_for_review_decision") is True,
        implementation_review_decision_performed=True,
        implementation_review_decision_passed=not failing,
        implementation_authorized=False,
        implementation_blocked=True,
        implementation_block_reason="EXPLICIT_OPERATOR_APPROVAL_NOT_RECEIVED",
        operator_approval_gate_required_next=True,
        decision_gate_count=len(gate_results),
        decision_gate_pass_count=len(gate_results) - len(failing),
        decision_gate_failure_count=len(failing),
        decision_finding_count=len(DECISION_FINDINGS),
        blocking_issue_count=0 if not failing else len(failing),
        issue_count=0 if not failing else len(failing),
        warning_count=0,
        review_gate_count=int(source_record.get("review_gate_count", 0)),
        review_gate_failure_count=int(source_record.get("review_gate_failure_count", 0)),
        review_only=True,
        decision_only=True,
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
        operator_approval_required=True,
        operator_approval_received=False,
        fail_closed_required=True,
        fail_closed_active=True,
        decision_gates=DECISION_GATES,
        decision_findings=DECISION_FINDINGS,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_14_task_7_review_decision_record(record: ReviewDecisionRecord) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected = {
        "source_review_loaded": True,
        "source_review_valid": True,
        "dry_run_review_performed": True,
        "dry_run_review_passed": True,
        "ready_for_review_decision": True,
        "implementation_review_decision_performed": True,
        "implementation_review_decision_passed": True,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_block_reason": "EXPLICIT_OPERATOR_APPROVAL_NOT_RECEIVED",
        "operator_approval_gate_required_next": True,
        "decision_gate_count": 20,
        "decision_gate_pass_count": 20,
        "decision_gate_failure_count": 0,
        "decision_finding_count": 4,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
        "review_gate_count": 27,
        "review_gate_failure_count": 0,
        "review_only": True,
        "decision_only": True,
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
        "operator_approval_required": True,
        "operator_approval_received": False,
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

    if record.decision_verdict != DECISION_VERDICT:
        issues.append("decision_verdict_mismatch")

    if record.decision_status != DECISION_STATUS:
        issues.append("decision_status_mismatch")

    status = TASK_VALID if not issues else "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_14_task_7_review_decision_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[ReviewDecisionRecord, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-v1.json"
    output_index = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-index-v1.json"
    output_manifest = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-manifest-v1.txt"
    output_md = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-v1.md"

    record = build_milestone_14_task_7_review_decision_record()
    validation = validate_milestone_14_task_7_review_decision_record(record)

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
        "source_review_signature": record.source_review_signature,
        "source_review_baseline_commit": record.source_review_baseline_commit,
        "decision_verdict": record.decision_verdict,
        "decision_status": record.decision_status,
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
            f"source_review_signature={record.source_review_signature}",
            f"source_review_baseline_commit={record.source_review_baseline_commit}",
            f"task_mode={record.task_mode}",
            f"task_verdict={record.task_verdict}",
            f"decision_verdict={record.decision_verdict}",
            f"decision_status={record.decision_status}",
            f"next_stage={record.next_stage}",
            f"implementation_review_decision_performed={record.implementation_review_decision_performed}",
            f"implementation_authorized={record.implementation_authorized}",
            f"implementation_blocked={record.implementation_blocked}",
            f"implementation_block_reason={record.implementation_block_reason}",
            f"operator_approval_required={record.operator_approval_required}",
            f"operator_approval_received={record.operator_approval_received}",
            f"decision_gate_count={record.decision_gate_count}",
            f"decision_gate_failure_count={record.decision_gate_failure_count}",
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
            "# Milestone 14 Task 7 — Local Solver Controlled Runtime Integration Implementation Review Decision v1",
            "",
            f"Status: `{TASK_READY}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{record.signature}`",
            f"Baseline commit: `{record.baseline_commit}`",
            "",
            "## Decision",
            "",
            f"`{record.decision_verdict}`",
            "",
            f"Decision status: `{record.decision_status}`",
            f"Implementation authorized: `{record.implementation_authorized}`",
            f"Implementation blocked: `{record.implementation_blocked}`",
            f"Block reason: `{record.implementation_block_reason}`",
            "",
            "## Source review",
            "",
            f"- source_review_signature: `{record.source_review_signature}`",
            f"- source_review_baseline_commit: `{record.source_review_baseline_commit}`",
            f"- source_review_valid: `{record.source_review_valid}`",
            f"- dry_run_review_passed: `{record.dry_run_review_passed}`",
            f"- ready_for_review_decision: `{record.ready_for_review_decision}`",
            "",
            "## Boundary",
            "",
            f"- review_only: `{record.review_only}`",
            f"- decision_only: `{record.decision_only}`",
            f"- dry_run_only: `{record.dry_run_only}`",
            f"- implementation_performed: `{record.implementation_performed}`",
            f"- implementation_authorized: `{record.implementation_authorized}`",
            f"- runtime_activation_performed: `{record.runtime_activation_performed}`",
            f"- runtime_execution_performed: `{record.runtime_execution_performed}`",
            f"- real_submission_allowed: `{record.real_submission_allowed}`",
            f"- operator_approval_required: `{record.operator_approval_required}`",
            f"- operator_approval_received: `{record.operator_approval_received}`",
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
    "DECISION_VERDICT",
    "DECISION_STATUS",
    "ReviewDecisionRecord",
    "ValidationResult",
    "build_milestone_14_task_7_review_decision_record",
    "validate_milestone_14_task_7_review_decision_record",
    "write_milestone_14_task_7_review_decision_artifacts",
]
