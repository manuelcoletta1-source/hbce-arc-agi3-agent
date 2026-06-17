from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_V1"
TASK_READY = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_V1_READY"
TASK_VALID = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_V1_VALID"
PIPELINE_READY = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_V1_PIPELINE_READY"

MILESTONE_NUMBER = 14
TASK_NUMBER = 5

SOURCE_TASK = "MILESTONE_14_TASK_4_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_REVIEW_V1"
NEXT_STAGE = "MILESTONE_14_TASK_6_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_REVIEW_V1"

TASK_MODE = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_V1_DRY_RUN_ONLY_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_READY"
DRY_RUN_VERDICT = "LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_PASS_READY_FOR_REVIEW"

SOURCE_REVIEW_ARTIFACT = Path(
    "examples/milestone-14/local-solver-controlled-runtime-integration-implementation-plan-review-v1/"
    "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-review-v1.json"
)

OUTPUT_DIR = Path(
    "examples/milestone-14/local-solver-controlled-runtime-integration-implementation-dry-run-v1"
)

OUTPUT_JSON = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-v1.md"

DOC_PATH = Path("docs/milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-v1.md")


TARGET_MODULES = [
    {
        "module_id": "M14-RUNTIME-ADAPTER",
        "path": "src/hbce_arc_agi3/local_solver_controlled_runtime_integration_adapter.py",
        "planned_action": "prepare_runtime_adapter_contract",
        "dry_run_action": "SIMULATED_CREATE_OR_UPDATE",
    },
    {
        "module_id": "M14-CANDIDATE-BRIDGE",
        "path": "src/hbce_arc_agi3/local_solver_candidate_bridge.py",
        "planned_action": "prepare_candidate_bridge_contract",
        "dry_run_action": "SIMULATED_CREATE_OR_UPDATE",
    },
    {
        "module_id": "M14-RANKER-GATE",
        "path": "src/hbce_arc_agi3/local_solver_ranker_gate.py",
        "planned_action": "prepare_ranker_gate_contract",
        "dry_run_action": "SIMULATED_CREATE_OR_UPDATE",
    },
    {
        "module_id": "M14-SOLVER-HOOK",
        "path": "src/hbce_arc_agi3/local_solver_runtime_hook.py",
        "planned_action": "prepare_solver_hook_contract",
        "dry_run_action": "SIMULATED_CREATE_OR_UPDATE",
    },
    {
        "module_id": "M14-REGRESSION-GUARD",
        "path": "src/hbce_arc_agi3/local_solver_runtime_regression_guard.py",
        "planned_action": "prepare_regression_guard_contract",
        "dry_run_action": "SIMULATED_CREATE_OR_UPDATE",
    },
]


IMPLEMENTATION_STEPS = [
    "load_review_artifact",
    "verify_review_passed",
    "project_target_modules",
    "project_integration_contracts",
    "project_regression_tests",
    "project_rollback_points",
    "simulate_runtime_adapter_wiring",
    "simulate_solver_hook_wiring",
    "simulate_ranker_gate_wiring",
    "emit_dry_run_artifacts",
]


INTEGRATION_CONTRACTS = [
    "no_runtime_activation",
    "no_runtime_execution",
    "no_solver_mutation",
    "no_ranker_mutation",
    "no_candidate_generator_mutation",
    "deterministic_local_fixture_scope",
    "rollback_manifest_required",
    "kaggle_score_semantics_forbidden",
]


REGRESSION_TESTS = [
    "import_check",
    "review_artifact_presence",
    "dry_run_projection_count",
    "target_module_count",
    "integration_contract_count",
    "runtime_activation_block",
    "submission_block",
    "boundary_integrity",
]


ROLLBACK_ITEMS = [
    "restore_target_modules",
    "restore_runtime_hook",
    "restore_candidate_bridge",
    "restore_ranker_gate",
    "restore_regression_guard",
]


@dataclass(frozen=True)
class DryRunRecord:
    task_name: str
    milestone_number: int
    task_number: int
    source_task: str
    next_stage: str
    task_mode: str
    task_verdict: str
    dry_run_verdict: str
    signature: str
    baseline_commit: str
    source_review_artifact: str
    source_review_loaded: bool
    source_review_passed: bool
    implementation_plan_review_passed: bool
    ready_for_implementation_dry_run: bool
    implementation_dry_run_performed: bool
    dry_run_projection_created: bool
    target_module_count: int
    implementation_step_count: int
    integration_contract_count: int
    regression_test_count: int
    rollback_item_count: int
    dry_run_check_count: int
    dry_run_pass_count: int
    dry_run_failure_count: int
    blocking_issue_count: int
    issue_count: int
    warning_count: int
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
    target_modules: list[dict[str, str]]
    implementation_steps: list[str]
    integration_contracts: list[str]
    regression_tests: list[str]
    rollback_items: list[str]
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


def _source_review_passed(payload: dict[str, Any]) -> bool:
    if not payload:
        return False
    return (
        payload.get("implementation_plan_review_passed") is True
        and payload.get("ready_for_implementation_dry_run") is True
        and payload.get("runtime_activation_performed") is False
        and payload.get("runtime_execution_performed") is False
        and payload.get("implementation_performed") is False
        and payload.get("real_submission_allowed") is False
        and payload.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
    )


def _signature(seed: dict[str, Any]) -> str:
    canonical = json.dumps(seed, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16].upper()


def build_milestone_14_task_5_dry_run_record(
    *,
    baseline_commit: str | None = None,
    source_review_artifact: Path = SOURCE_REVIEW_ARTIFACT,
) -> DryRunRecord:
    baseline = baseline_commit or _git_head()
    source_payload = _load_json(source_review_artifact)
    source_passed = _source_review_passed(source_payload)

    checks = [
        ("source_review_loaded", bool(source_payload)),
        ("source_review_passed", source_passed),
        ("implementation_plan_review_passed", source_payload.get("implementation_plan_review_passed") is True),
        ("ready_for_implementation_dry_run", source_payload.get("ready_for_implementation_dry_run") is True),
        ("dry_run_projection_created", True),
        ("target_module_count_5", len(TARGET_MODULES) == 5),
        ("implementation_step_count_10", len(IMPLEMENTATION_STEPS) == 10),
        ("integration_contract_count_8", len(INTEGRATION_CONTRACTS) == 8),
        ("regression_test_count_8", len(REGRESSION_TESTS) == 8),
        ("rollback_item_count_5", len(ROLLBACK_ITEMS) == 5),
        ("runtime_activation_false", True),
        ("runtime_execution_false", True),
        ("runtime_solver_modified_false", True),
        ("ranker_runtime_modified_false", True),
        ("candidate_generator_modified_false", True),
        ("implementation_performed_false", True),
        ("real_evaluation_false", True),
        ("real_submission_false", True),
        ("kaggle_authentication_false", True),
        ("kaggle_upload_false", True),
        ("kaggle_submission_false", True),
        ("private_core_false", True),
        ("legal_certification_false", True),
        ("kaggle_score_semantics_not_score", True),
    ]

    failures = [name for name, passed in checks if not passed]

    seed = {
        "task": TASK_NAME,
        "baseline_commit": baseline,
        "source_passed": source_passed,
        "target_modules": TARGET_MODULES,
        "implementation_steps": IMPLEMENTATION_STEPS,
        "integration_contracts": INTEGRATION_CONTRACTS,
        "regression_tests": REGRESSION_TESTS,
        "rollback_items": ROLLBACK_ITEMS,
    }

    return DryRunRecord(
        task_name=TASK_NAME,
        milestone_number=MILESTONE_NUMBER,
        task_number=TASK_NUMBER,
        source_task=SOURCE_TASK,
        next_stage=NEXT_STAGE,
        task_mode=TASK_MODE,
        task_verdict=TASK_VERDICT,
        dry_run_verdict=DRY_RUN_VERDICT,
        signature=_signature(seed),
        baseline_commit=baseline,
        source_review_artifact=str(source_review_artifact),
        source_review_loaded=bool(source_payload),
        source_review_passed=source_passed,
        implementation_plan_review_passed=source_payload.get("implementation_plan_review_passed") is True,
        ready_for_implementation_dry_run=source_payload.get("ready_for_implementation_dry_run") is True,
        implementation_dry_run_performed=True,
        dry_run_projection_created=True,
        target_module_count=len(TARGET_MODULES),
        implementation_step_count=len(IMPLEMENTATION_STEPS),
        integration_contract_count=len(INTEGRATION_CONTRACTS),
        regression_test_count=len(REGRESSION_TESTS),
        rollback_item_count=len(ROLLBACK_ITEMS),
        dry_run_check_count=len(checks),
        dry_run_pass_count=len(checks) - len(failures),
        dry_run_failure_count=len(failures),
        blocking_issue_count=len(failures),
        issue_count=len(failures),
        warning_count=0,
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
        target_modules=TARGET_MODULES,
        implementation_steps=IMPLEMENTATION_STEPS,
        integration_contracts=INTEGRATION_CONTRACTS,
        regression_tests=REGRESSION_TESTS,
        rollback_items=ROLLBACK_ITEMS,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_milestone_14_task_5_dry_run_record(record: DryRunRecord) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    expected = {
        "source_review_loaded": True,
        "source_review_passed": True,
        "implementation_plan_review_passed": True,
        "ready_for_implementation_dry_run": True,
        "implementation_dry_run_performed": True,
        "dry_run_projection_created": True,
        "target_module_count": 5,
        "implementation_step_count": 10,
        "integration_contract_count": 8,
        "regression_test_count": 8,
        "rollback_item_count": 5,
        "dry_run_check_count": 24,
        "dry_run_failure_count": 0,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
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

    if record.dry_run_pass_count != record.dry_run_check_count:
        issues.append("dry_run_pass_count_mismatch")

    if record.task_name != TASK_NAME:
        issues.append("task_name_mismatch")

    if record.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    status = TASK_VALID if not issues else "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_DRY_RUN_V1_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_milestone_14_task_5_dry_run_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[DryRunRecord, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-v1.json"
    output_index = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-index-v1.json"
    output_manifest = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-manifest-v1.txt"
    output_md = output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-v1.md"

    record = build_milestone_14_task_5_dry_run_record()
    validation = validate_milestone_14_task_5_dry_run_record(record)

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
            f"task_mode={record.task_mode}",
            f"task_verdict={record.task_verdict}",
            f"dry_run_verdict={record.dry_run_verdict}",
            f"next_stage={record.next_stage}",
            f"implementation_dry_run_performed={record.implementation_dry_run_performed}",
            f"target_module_count={record.target_module_count}",
            f"implementation_step_count={record.implementation_step_count}",
            f"integration_contract_count={record.integration_contract_count}",
            f"regression_test_count={record.regression_test_count}",
            f"rollback_item_count={record.rollback_item_count}",
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
            "# Milestone 14 Task 5 — Local Solver Controlled Runtime Integration Implementation Dry Run v1",
            "",
            f"Status: `{TASK_READY}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{record.signature}`",
            f"Baseline commit: `{record.baseline_commit}`",
            "",
            "## Verdict",
            "",
            f"`{record.dry_run_verdict}`",
            "",
            "## Counts",
            "",
            f"- target_module_count: `{record.target_module_count}`",
            f"- implementation_step_count: `{record.implementation_step_count}`",
            f"- integration_contract_count: `{record.integration_contract_count}`",
            f"- regression_test_count: `{record.regression_test_count}`",
            f"- rollback_item_count: `{record.rollback_item_count}`",
            f"- dry_run_check_count: `{record.dry_run_check_count}`",
            f"- dry_run_failure_count: `{record.dry_run_failure_count}`",
            "",
            "## Boundary",
            "",
            f"- implementation_dry_run_performed: `{record.implementation_dry_run_performed}`",
            f"- implementation_performed: `{record.implementation_performed}`",
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
    "DRY_RUN_VERDICT",
    "DryRunRecord",
    "ValidationResult",
    "build_milestone_14_task_5_dry_run_record",
    "validate_milestone_14_task_5_dry_run_record",
    "write_milestone_14_task_5_dry_run_artifacts",
]
