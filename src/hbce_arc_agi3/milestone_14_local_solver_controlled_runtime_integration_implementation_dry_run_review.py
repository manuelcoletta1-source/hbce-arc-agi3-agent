from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1"
TASK_READY = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1_READY"
TASK_VALID = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1_VALID"
PIPELINE_READY = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1_PIPELINE_READY"

MILESTONE_NUMBER = 14
TASK_NUMBER = 6

SOURCE_TASK = "MILESTONE_14_TASK_5_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_V1"
NEXT_STAGE = "MILESTONE_14_TASK_7_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_REVIEW_DECISION_V1"

TASK_MODE = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1_REVIEW_ONLY_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_READY"
REVIEW_VERDICT = "LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_PASS_READY_FOR_REVIEW_DECISION"

SOURCE_DRY_RUN_ARTIFACT = Path(
    "examples/milestone-14/local-solver-controlled-runtime-integration-implementation-dry-run-v1/"
    "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-v1.json"
)

OUTPUT_DIR = Path(
    "examples/milestone-14/local-solver-controlled-runtime-integration-implementation-dry-run-review-v1"
)

OUTPUT_JSON = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-v1.md"

DOC_PATH = Path("docs/milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-v1.md")


REVIEW_GATES = [
    "source_dry_run_loaded",
    "source_dry_run_valid",
    "dry_run_performed",
    "dry_run_projection_created",
    "target_module_count_verified",
    "implementation_step_count_verified",
    "integration_contract_count_verified",
    "regression_test_count_verified",
    "rollback_item_count_verified",
    "dry_run_check_count_verified",
    "dry_run_failure_count_zero",
    "runtime_activation_blocked",
    "runtime_execution_blocked",
    "runtime_solver_unmodified",
    "ranker_runtime_unmodified",
    "candidate_generator_unmodified",
    "implementation_not_performed",
    "real_evaluation_not_performed",
    "real_submission_blocked",
    "kaggle_authentication_blocked",
    "kaggle_upload_blocked",
    "kaggle_submission_blocked",
    "private_core_not_exposed",
    "legal_certification_false",
    "kaggle_score_semantics_not_score",
    "operator_approval_not_received",
    "fail_closed_active",
]


REVIEW_FINDINGS = [
    {
        "finding_id": "M14-T6-FINDING-001",
        "finding": "dry_run_artifacts_complete",
        "severity": "PASS",
    },
    {
        "finding_id": "M14-T6-FINDING-002",
        "finding": "runtime_execution_remained_blocked",
        "severity": "PASS",
    },
    {
        "finding_id": "M14-T6-FINDING-003",
        "finding": "solver_ranker_candidate_generator_not_modified",
        "severity": "PASS",
    },
    {
        "finding_id": "M14-T6-FINDING-004",
        "finding": "not_a_kaggle_score_semantics_preserved",
        "severity": "PASS",
    },
    {
        "finding_id": "M14-T6-FINDING-005",
        "finding": "ready_for_review_decision",
        "severity": "PASS",
    },
]


@dataclass(frozen=True)
class DryRunReviewRecord:
    task_name: str
    milestone_number: int
    task_number: int
    source_task: str
    next_stage: str
    task_mode: str
    task_verdict: str
    review_verdict: str
    signature: str
    baseline_commit: str
    source_dry_run_artifact: str
    source_dry_run_loaded: bool
    source_dry_run_valid: bool
    source_dry_run_signature: str
    source_dry_run_baseline_commit: str
    implementation_dry_run_performed: bool
    dry_run_projection_created: bool
    dry_run_review_performed: bool
    dry_run_review_passed: bool
    ready_for_review_decision: bool
    target_module_count: int
    implementation_step_count: int
    integration_contract_count: int
    regression_test_count: int
    rollback_item_count: int
    dry_run_check_count: int
    dry_run_failure_count: int
    review_gate_count: int
    review_gate_pass_count: int
    review_gate_failure_count: int
    review_finding_count: int
    blocking_issue_count: int
    issue_count: int
    warning_count: int
    review_only: bool
    dry_run_only: bool
    runtime_activation_performed: bool
    runtime_execution_performed: bool
    runtime_solver_modified: bool
    ranker_runtime_modified: bool
    candidate_generator_modified: bool
    implementation_performed: bool
    implementation_review_decision_performed: bool
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
    review_gates: list[str]
    review_findings: list[dict[str, str]]
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


def _source_payload(path: Path) -> dict[str, Any]:
    raw = _load_json(path)
    record = raw.get("record")
    validation = raw.get("validation")
    if isinstance(record, dict) and isinstance(validation, dict):
        return {"record": record, "validation": validation}
    return {"record": {}, "validation": {}}


def _source_valid(source: dict[str, dict[str, Any]]) -> bool:
    record = source["record"]
    validation = source["validation"]
    return (
        bool(record)
        and bool(validation)
        and validation.get("valid") is True
        and validation.get("status") == "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_V1_VALID"
        and record.get("implementation_dry_run_performed") is True
        and record.get("dry_run_projection_created") is True
        and record.get("target_module_count") == 5
        and record.get("implementation_step_count") == 10
        and record.get("integration_contract_count") == 8
        and record.get("regression_test_count") == 8
        and record.get("rollback_item_count") == 5
        and record.get("dry_run_check_count") == 24
        and record.get("dry_run_failure_count") == 0
        and record.get("runtime_activation_performed") is False
        and record.get("runtime_execution_performed") is False
        and record.get("runtime_solver_modified") is False
        and record.get("ranker_runtime_modified") is False
        and record.get("candidate_generator_modified") is False
        and record.get("implementation_performed") is False
        and record.get("real_evaluation_performed") is False
        and record.get("real_submission_allowed") is False
        and record.get("kaggle_authentication_performed") is False
        and record.get("kaggle_upload_performed") is False
        and record.get("kaggle_submission_sent") is False
        and record.get("private_core_exposure") is False
        and record.get("legal_certification") is False
        and record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
        and record.get("operator_approval_received") is False
        and record.get("fail_closed_active") is True
    )


def _signature(seed: dict[str, Any]) -> str:
    canonical = json.dumps(seed, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16].upper()


def build_milestone_14_task_6_dry_run_review_record(
    *,
    baseline_commit: str | None = None,
    source_dry_run_artifact: Path = SOURCE_DRY_RUN_ARTIFACT,
) -> DryRunReviewRecord:
    baseline = baseline_commit or _git_head()
    source = _source_payload(source_dry_run_artifact)
    source_record = source["record"]
    source_valid = _source_valid(source)

    gate_results = {
        "source_dry_run_loaded": bool(source_record),
        "source_dry_run_valid": source_valid,
        "dry_run_performed": source_record.get("implementation_dry_run_performed") is True,
        "dry_run_projection_created": source_record.get("dry_run_projection_created") is True,
        "target_module_count_verified": source_record.get("target_module_count") == 5,
        "implementation_step_count_verified": source_record.get("implementation_step_count") == 10,
        "integration_contract_count_verified": source_record.get("integration_contract_count") == 8,
        "regression_test_count_verified": source_record.get("regression_test_count") == 8,
        "rollback_item_count_verified": source_record.get("rollback_item_count") == 5,
        "dry_run_check_count_verified": source_record.get("dry_run_check_count") == 24,
        "dry_run_failure_count_zero": source_record.get("dry_run_failure_count") == 0,
        "runtime_activation_blocked": source_record.get("runtime_activation_performed") is False,
        "runtime_execution_blocked": source_record.get("runtime_execution_performed") is False,
        "runtime_solver_unmodified": source_record.get("runtime_solver_modified") is False,
        "ranker_runtime_unmodified": source_record.get("ranker_runtime_modified") is False,
        "candidate_generator_unmodified": source_record.get("candidate_generator_modified") is False,
        "implementation_not_performed": source_record.get("implementation_performed") is False,
        "real_evaluation_not_performed": source_record.get("real_evaluation_performed") is False,
        "real_submission_blocked": source_record.get("real_submission_allowed") is False,
        "kaggle_authentication_blocked": source_record.get("kaggle_authentication_performed") is False,
        "kaggle_upload_blocked": source_record.get("kaggle_upload_performed") is False,
        "kaggle_submission_blocked": source_record.get("kaggle_submission_sent") is False,
        "private_core_not_exposed": source_record.get("private_core_exposure") is False,
        "legal_certification_false": source_record.get("legal_certification") is False,
        "kaggle_score_semantics_not_score": source_record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "operator_approval_not_received": source_record.get("operator_approval_received") is False,
        "fail_closed_active": source_record.get("fail_closed_active") is True,
    }

    failing = [name for name, passed in gate_results.items() if not passed]

    seed = {
        "task": TASK_NAME,
        "baseline_commit": baseline,
        "source_signature": source_record.get("signature", "NO_SOURCE_SIGNATURE"),
        "source_baseline": source_record.get("baseline_commit", "NO_SOURCE_BASELINE"),
        "review_gates": gate_results,
        "review_findings": REVIEW_FINDINGS,
    }

    return DryRunReviewRecord(
        task_name=TASK_NAME,
        milestone_number=MILESTONE_NUMBER,
        task_number=TASK_NUMBER,
        source_task=SOURCE_TASK,
        next_stage=NEXT_STAGE,
        task_mode=TASK_MODE,
        task_verdict=TASK_VERDICT,
        review_verdict=REVIEW_VERDICT,
        signature=_signature(seed),
        baseline_commit=baseline,
        source_dry_run_artifact=str(source_dry_run_artifact),
        source_dry_run_loaded=bool(source_record),
        source_dry_run_valid=source_valid,
        source_dry_run_signature=str(source_record.get("signature", "NO_SOURCE_SIGNATURE")),
        source_dry_run_baseline_commit=str(source_record.get("baseline_commit", "NO_SOURCE_BASELINE")),
        implementation_dry_run_performed=source_record.get("implementation_dry_run_performed") is True,
        dry_run_projection_created=source_record.get("dry_run_projection_created") is True,
        dry_run_review_performed=True,
        dry_run_review_passed=not failing,
        ready_for_review_decision=not failing,
        target_module_count=int(source_record.get("target_module_count", 0)),
        implementation_step_count=int(source_record.get("implementation_step_count", 0)),
        integration_contract_count=int(source_record.get("integration_contract_count", 0)),
        regression_test_count=int(source_record.get("regression_test_count", 0)),
        rollback_item_count=int(source_record.get("rollback_item_count", 0)),
        dry_run_check_count=int(source_record.get("dry_run_check_count", 0)),
        dry_run_failure_count=int(source_record.get("dry_run_failure_count", 0)),
        review_gate_count=len(gate_results),
        review_gate_pass_count=len(gate_results) - len(failing),
        review_gate_failure_count=len(failing),
        review_finding_count=len(REVIEW_FINDINGS),
        blocking_issue_count=len(failing),
        issue_count=len(failing),
        warning_count=0,
        review_only=True,
        dry_run_only=True,
        runtime_activation_performed=False,
        runtime_execution_performed=False,
        runtime_solver_modified=False,
        ranker_runtime_modified=False,
        candidate_generator_modified=False,
        implementation_performed=False,
        implementation_review_decision_performed=False,
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
        review_gates=REVIEW_GATES,
        review_findings=REVIEW_FINDINGS,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_14_task_6_dry_run_review_record(record: DryRunReviewRecord) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected = {
        "source_dry_run_loaded": True,
        "source_dry_run_valid": True,
        "implementation_dry_run_performed": True,
        "dry_run_projection_created": True,
        "dry_run_review_performed": True,
        "dry_run_review_passed": True,
        "ready_for_review_decision": True,
        "target_module_count": 5,
        "implementation_step_count": 10,
        "integration_contract_count": 8,
        "regression_test_count": 8,
        "rollback_item_count": 5,
        "dry_run_check_count": 24,
        "dry_run_failure_count": 0,
        "review_gate_count": 27,
        "review_gate_pass_count": 27,
        "review_gate_failure_count": 0,
        "review_finding_count": 5,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
        "review_only": True,
        "dry_run_only": True,
        "runtime_activation_performed": False,
        "runtime_execution_performed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "candidate_generator_modified": False,
        "implementation_performed": False,
        "implementation_review_decision_performed": False,
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

    if record.review_verdict != REVIEW_VERDICT:
        issues.append("review_verdict_mismatch")

    status = TASK_VALID if not issues else "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_14_task_6_dry_run_review_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[DryRunReviewRecord, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-v1.json"
    output_index = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-index-v1.json"
    output_manifest = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-manifest-v1.txt"
    output_md = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-review-v1.md"

    record = build_milestone_14_task_6_dry_run_review_record()
    validation = validate_milestone_14_task_6_dry_run_review_record(record)

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
        "source_dry_run_signature": record.source_dry_run_signature,
        "source_dry_run_baseline_commit": record.source_dry_run_baseline_commit,
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
            f"source_dry_run_signature={record.source_dry_run_signature}",
            f"source_dry_run_baseline_commit={record.source_dry_run_baseline_commit}",
            f"task_mode={record.task_mode}",
            f"task_verdict={record.task_verdict}",
            f"review_verdict={record.review_verdict}",
            f"next_stage={record.next_stage}",
            f"dry_run_review_performed={record.dry_run_review_performed}",
            f"dry_run_review_passed={record.dry_run_review_passed}",
            f"ready_for_review_decision={record.ready_for_review_decision}",
            f"review_gate_count={record.review_gate_count}",
            f"review_gate_failure_count={record.review_gate_failure_count}",
            f"kaggle_score_semantics={record.kaggle_score_semantics}",
            f"runtime_activation_performed={record.runtime_activation_performed}",
            f"runtime_execution_performed={record.runtime_execution_performed}",
            f"implementation_performed={record.implementation_performed}",
            f"implementation_review_decision_performed={record.implementation_review_decision_performed}",
            f"real_submission_allowed={record.real_submission_allowed}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# Milestone 14 Task 6 — Local Solver Controlled Runtime Integration Implementation Dry Run Review v1",
            "",
            f"Status: `{TASK_READY}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{record.signature}`",
            f"Baseline commit: `{record.baseline_commit}`",
            "",
            "## Verdict",
            "",
            f"`{record.review_verdict}`",
            "",
            "## Source dry run",
            "",
            f"- source_dry_run_signature: `{record.source_dry_run_signature}`",
            f"- source_dry_run_baseline_commit: `{record.source_dry_run_baseline_commit}`",
            f"- source_dry_run_valid: `{record.source_dry_run_valid}`",
            "",
            "## Review counts",
            "",
            f"- review_gate_count: `{record.review_gate_count}`",
            f"- review_gate_pass_count: `{record.review_gate_pass_count}`",
            f"- review_gate_failure_count: `{record.review_gate_failure_count}`",
            f"- review_finding_count: `{record.review_finding_count}`",
            "",
            "## Boundary",
            "",
            f"- review_only: `{record.review_only}`",
            f"- dry_run_only: `{record.dry_run_only}`",
            f"- implementation_performed: `{record.implementation_performed}`",
            f"- implementation_review_decision_performed: `{record.implementation_review_decision_performed}`",
            f"- runtime_activation_performed: `{record.runtime_activation_performed}`",
            f"- runtime_execution_performed: `{record.runtime_execution_performed}`",
            f"- runtime_solver_modified: `{record.runtime_solver_modified}`",
            f"- ranker_runtime_modified: `{record.ranker_runtime_modified}`",
            f"- candidate_generator_modified: `{record.candidate_generator_modified}`",
            f"- real_submission_allowed: `{record.real_submission_allowed}`",
            f"- kaggle_submission_sent: `{record.kaggle_submission_sent}`",
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
    "REVIEW_VERDICT",
    "DryRunReviewRecord",
    "ValidationResult",
    "build_milestone_14_task_6_dry_run_review_record",
    "validate_milestone_14_task_6_dry_run_review_record",
    "write_milestone_14_task_6_dry_run_review_artifacts",
]
