"""Milestone #14 Task 3 - Local Solver Controlled Runtime Integration Implementation Plan v1.

Creates the implementation plan after Task 2 plan review.

This is implementation-plan-only.
It does not modify solver runtime.
It does not execute runtime solving.
It does not authenticate, upload, submit, or claim Kaggle score.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_V1"
MILESTONE_NUMBER = 14
TASK_NUMBER = 3
TASK_LABEL = "Milestone #14 Task 3 - Local Solver Controlled Runtime Integration Implementation Plan v1"

SOURCE_TASK = "MILESTONE_14_TASK_2_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLAN_REVIEW_V1"
NEXT_STAGE = "MILESTONE_14_TASK_4_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_REVIEW_V1"

TASK_MODE = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_V1_PLAN_ONLY_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_READY"
IMPLEMENTATION_PLAN_VERDICT = "LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_READY_FOR_REVIEW"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-14"
    / "local-solver-controlled-runtime-integration-implementation-plan-v1"
)

SOURCE_PLAN_REVIEW_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-14"
    / "local-solver-controlled-runtime-integration-plan-review-v1"
    / "milestone-14-local-solver-controlled-runtime-integration-plan-review-v1.json"
)

TARGET_MODULES = [
    {
        "path": "src/hbce_arc_agi3/local_solver.py",
        "role": "future local solver integration target",
        "operation": "PLAN_ONLY_NO_MODIFICATION",
    },
    {
        "path": "src/hbce_arc_agi3/candidate_generator.py",
        "role": "program synthesis candidate source boundary",
        "operation": "PLAN_ONLY_NO_MODIFICATION",
    },
    {
        "path": "src/hbce_arc_agi3/candidate_ranker.py",
        "role": "candidate ranking compatibility boundary",
        "operation": "PLAN_ONLY_NO_MODIFICATION",
    },
    {
        "path": "src/hbce_arc_agi3/milestone_13_program_synthesis_candidate_generator_controlled_runtime_wiring_milestone_closure.py",
        "role": "source milestone closure contract",
        "operation": "READ_ONLY_REFERENCE",
    },
    {
        "path": "tests/",
        "role": "future deterministic regression harness",
        "operation": "PLAN_ONLY_NO_MODIFICATION",
    },
]

IMPLEMENTATION_STEPS = [
    "define local solver candidate intake DTO",
    "define candidate source provenance field",
    "define fail-closed solver integration guard",
    "define deterministic fixture compatibility check",
    "define NOT_A_KAGGLE_SCORE diagnostic result schema",
    "define no-runtime-execution dry-run path",
    "define rollback and disable switch",
    "define public-overfit guard assertion",
    "define targeted regression suite",
    "define full-suite closure rule before implementation",
]

INTEGRATION_CONTRACTS = [
    "input candidates must be deterministic",
    "candidate provenance must reference Milestone 13 closure",
    "solver integration must remain disabled until reviewed",
    "runtime execution must remain false in this task",
    "Kaggle authentication must remain false",
    "submission upload must remain false",
    "diagnostic score must remain NOT_A_KAGGLE_SCORE",
    "all generated artifacts must be public-safe",
]

REGRESSION_TEST_PLAN = [
    "test source plan review artifact is valid",
    "test implementation plan record validates",
    "test runtime execution cannot be true",
    "test implementation_performed cannot be true",
    "test Kaggle submission cannot be true",
    "test Kaggle score semantics cannot change",
    "test target module list is complete",
    "test artifacts are written",
]

ROLLBACK_PLAN = [
    "do not modify runtime modules during Task 3",
    "if implementation plan fails validation, do not commit",
    "if generated artifacts drift after post-push verify, refresh only Task 3 artifacts",
    "if full suite creates historical Milestone 11 drift, restore those files only",
    "if boundary flags change, fail closed and regenerate plan",
]

REVIEW_GATES = [
    "source Task 2 plan review passed",
    "implementation plan only",
    "target modules listed",
    "implementation steps complete",
    "contracts complete",
    "regression test plan complete",
    "rollback plan complete",
    "no runtime modification",
    "no runtime execution",
    "no Kaggle submission",
    "ready for Task 4 review",
]


def _run_git_head() -> str:
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "NO_GIT_HEAD_AVAILABLE"
    return result.stdout.strip() or "NO_GIT_HEAD_AVAILABLE"


def _stable_signature(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return loaded if isinstance(loaded, dict) else None


def review_source_plan_review_artifact() -> dict[str, Any]:
    source = _load_json(SOURCE_PLAN_REVIEW_ARTIFACT)

    if source is None:
        return {
            "source_plan_review_artifact_present": False,
            "source_plan_review_artifact_parseable": False,
            "source_plan_review_valid": False,
            "source_record": None,
        }

    valid = bool(
        source.get("plan_review_valid") is True
        and source.get("plan_review_passed") is True
        and source.get("ready_for_implementation_plan") is True
        and source.get("runtime_candidate_count") == 4
        and source.get("candidate_fixture_matrix_count") == 12
        and source.get("diagnostic_average_score") == 0.6875
        and source.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
        and source.get("review_only") is True
        and source.get("diagnostic_only") is True
        and source.get("runtime_activation_performed") is False
        and source.get("runtime_execution_performed") is False
        and source.get("implementation_performed") is False
        and source.get("real_submission_allowed") is False
        and source.get("kaggle_submission_sent") is False
        and source.get("private_core_exposure") is False
        and source.get("legal_certification") is False
        and source.get("next_stage")
        == "MILESTONE_14_TASK_3_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_V1"
    )

    return {
        "source_plan_review_artifact_present": True,
        "source_plan_review_artifact_parseable": True,
        "source_plan_review_valid": valid,
        "source_record": source,
    }


def build_implementation_plan_gate_map(source_record: dict[str, Any]) -> dict[str, bool]:
    return {
        "source_plan_review_passed": source_record.get("plan_review_passed") is True,
        "ready_for_implementation_plan": source_record.get("ready_for_implementation_plan") is True,
        "runtime_candidate_count_4": source_record.get("runtime_candidate_count") == 4,
        "candidate_fixture_matrix_count_12": source_record.get("candidate_fixture_matrix_count") == 12,
        "diagnostic_average_score_0_6875": source_record.get("diagnostic_average_score") == 0.6875,
        "not_kaggle_score": source_record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "review_only_source": source_record.get("review_only") is True,
        "diagnostic_only_source": source_record.get("diagnostic_only") is True,
        "runtime_activation_false": source_record.get("runtime_activation_performed") is False,
        "runtime_execution_false": source_record.get("runtime_execution_performed") is False,
        "implementation_false": source_record.get("implementation_performed") is False,
        "real_submission_false": source_record.get("real_submission_allowed") is False,
        "kaggle_submission_false": source_record.get("kaggle_submission_sent") is False,
        "private_core_false": source_record.get("private_core_exposure") is False,
        "legal_certification_false": source_record.get("legal_certification") is False,
    }


def build_implementation_plan_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_review = review_source_plan_review_artifact()
    source_record = source_review.get("source_record") if isinstance(source_review.get("source_record"), dict) else {}
    gates = build_implementation_plan_gate_map(source_record)

    checks = {
        "source_plan_review_artifact_present": source_review["source_plan_review_artifact_present"] is True,
        "source_plan_review_artifact_parseable": source_review["source_plan_review_artifact_parseable"] is True,
        "source_plan_review_valid": source_review["source_plan_review_valid"] is True,
        **gates,
    }

    blocking_issues = [name for name, passed in checks.items() if passed is not True]
    valid = len(blocking_issues) == 0

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_plan_review_artifact": str(SOURCE_PLAN_REVIEW_ARTIFACT.relative_to(PROJECT_ROOT)),
        "task_mode": TASK_MODE,
        "task_verdict": TASK_VERDICT,
        "implementation_plan_verdict": IMPLEMENTATION_PLAN_VERDICT,
        "implementation_plan_ready": True,
        "implementation_plan_valid": valid,
        "implementation_plan_passed": valid,
        "ready_for_implementation_plan_review": valid,
        "target_modules": TARGET_MODULES,
        "target_module_count": len(TARGET_MODULES),
        "implementation_steps": IMPLEMENTATION_STEPS,
        "implementation_step_count": len(IMPLEMENTATION_STEPS),
        "integration_contracts": INTEGRATION_CONTRACTS,
        "integration_contract_count": len(INTEGRATION_CONTRACTS),
        "regression_test_plan": REGRESSION_TEST_PLAN,
        "regression_test_count": len(REGRESSION_TEST_PLAN),
        "rollback_plan": ROLLBACK_PLAN,
        "rollback_item_count": len(ROLLBACK_PLAN),
        "review_gates": REVIEW_GATES,
        "review_gate_count": len(REVIEW_GATES),
        "source_review": source_review,
        "implementation_plan_gates": gates,
        "implementation_plan_gate_count": len(gates),
        "implementation_plan_checks": checks,
        "implementation_plan_check_count": len(checks),
        "implementation_plan_pass_count": len(checks) - len(blocking_issues),
        "implementation_plan_failure_count": len(blocking_issues),
        "blocking_issue_count": len(blocking_issues),
        "blocking_issues": blocking_issues,
        "runtime_candidate_count": source_record.get("runtime_candidate_count"),
        "candidate_fixture_matrix_count": source_record.get("candidate_fixture_matrix_count"),
        "diagnostic_average_score": source_record.get("diagnostic_average_score"),
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "implementation_plan_only": True,
        "diagnostic_only": True,
        "runtime_activation_performed": False,
        "runtime_execution_performed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "candidate_generator_modified": False,
        "implementation_performed": False,
        "real_evaluation_performed": False,
        "real_kaggle_evaluation_allowed": False,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_upload_allowed": False,
        "kaggle_upload_performed": False,
        "kaggle_submission_sent": False,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "issue_count": len(blocking_issues),
        "warning_count": 0,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-14-LOCAL-SOLVER-CONTROLLED-RUNTIME-INTEGRATION-IMPLEMENTATION-PLAN-" + signature[:12]
    return record


def validate_implementation_plan_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "implementation_plan_ready",
        "implementation_plan_valid",
        "implementation_plan_passed",
        "ready_for_implementation_plan_review",
        "implementation_plan_only",
        "diagnostic_only",
        "public_overfit_guard_required",
        "operator_approval_required",
        "local_only",
        "deterministic",
        "public_safe",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "runtime_activation_performed",
        "runtime_execution_performed",
        "runtime_solver_modified",
        "ranker_runtime_modified",
        "candidate_generator_modified",
        "implementation_performed",
        "real_evaluation_performed",
        "real_kaggle_evaluation_allowed",
        "public_overfit_allowed",
        "external_api_dependency",
        "internet_during_eval",
        "real_submission_allowed",
        "ready_for_real_kaggle_submission",
        "manual_upload_allowed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_upload_allowed",
        "kaggle_upload_performed",
        "kaggle_submission_sent",
        "operator_approval_received",
        "contains_api_keys",
        "private_core_exposure",
        "legal_certification",
        "official_score_claim_allowed",
        "competitive_score_claim_allowed",
    ]

    for key in expected_true:
        if record.get(key) is not True:
            issues.append(f"{key}_NOT_TRUE")

    for key in expected_false:
        if record.get(key) is not False:
            issues.append(f"{key}_NOT_FALSE")

    if record.get("revision") != TASK_NAME:
        issues.append("REVISION_MISMATCH")
    if record.get("source_task") != SOURCE_TASK:
        issues.append("SOURCE_TASK_MISMATCH")
    if record.get("next_stage") != NEXT_STAGE:
        issues.append("NEXT_STAGE_MISMATCH")
    if record.get("task_verdict") != TASK_VERDICT:
        issues.append("TASK_VERDICT_MISMATCH")
    if record.get("implementation_plan_verdict") != IMPLEMENTATION_PLAN_VERDICT:
        issues.append("IMPLEMENTATION_PLAN_VERDICT_MISMATCH")

    expected_counts = {
        "runtime_candidate_count": 4,
        "candidate_fixture_matrix_count": 12,
        "target_module_count": 5,
        "implementation_step_count": 10,
        "integration_contract_count": 8,
        "regression_test_count": 8,
        "rollback_item_count": 5,
        "review_gate_count": 11,
        "implementation_plan_gate_count": 15,
        "implementation_plan_failure_count": 0,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
    }

    for key, expected in expected_counts.items():
        if record.get(key) != expected:
            issues.append(f"{key.upper()}_MISMATCH")

    checks = record.get("implementation_plan_checks")
    if not isinstance(checks, dict):
        issues.append("IMPLEMENTATION_PLAN_CHECKS_MISSING")
    else:
        if record.get("implementation_plan_check_count") != len(checks):
            issues.append("IMPLEMENTATION_PLAN_CHECK_COUNT_MISMATCH")
        if record.get("implementation_plan_pass_count") != len(checks):
            issues.append("IMPLEMENTATION_PLAN_PASS_COUNT_MISMATCH")

    if record.get("diagnostic_average_score") != 0.6875:
        issues.append("DIAGNOSTIC_AVERAGE_SCORE_MISMATCH")
    if record.get("kaggle_score_semantics") != "NOT_A_KAGGLE_SCORE":
        issues.append("KAGGLE_SCORE_SEMANTICS_MISMATCH")

    source_review = record.get("source_review")
    if not isinstance(source_review, dict):
        issues.append("SOURCE_REVIEW_MISSING")
    else:
        if source_review.get("source_plan_review_valid") is not True:
            issues.append("SOURCE_PLAN_REVIEW_NOT_VALID")

    gates = record.get("implementation_plan_gates")
    if not isinstance(gates, dict):
        issues.append("IMPLEMENTATION_PLAN_GATES_MISSING")
    else:
        failed = [name for name, passed in gates.items() if passed is not True]
        if failed:
            issues.append("IMPLEMENTATION_PLAN_GATES_FAILED")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-v1.json"
    index_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-index-v1.json"
    manifest_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-manifest-v1.txt"
    markdown_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "implementation_plan_verdict": record["implementation_plan_verdict"],
        "next_stage": record["next_stage"],
        "implementation_plan_passed": record["implementation_plan_passed"],
        "ready_for_implementation_plan_review": record["ready_for_implementation_plan_review"],
        "target_module_count": record["target_module_count"],
        "implementation_step_count": record["implementation_step_count"],
        "integration_contract_count": record["integration_contract_count"],
        "regression_test_count": record["regression_test_count"],
        "rollback_item_count": record["rollback_item_count"],
        "review_gate_count": record["review_gate_count"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "runtime_activation_performed": record["runtime_activation_performed"],
        "runtime_execution_performed": record["runtime_execution_performed"],
        "implementation_performed": record["implementation_performed"],
        "real_submission_allowed": record["real_submission_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "private_core_exposure": record["private_core_exposure"],
        "legal_certification": record["legal_certification"],
    }
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        f"revision={record['revision']}",
        f"task_id={record['task_id']}",
        f"signature={record['signature']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"implementation_plan_verdict={record['implementation_plan_verdict']}",
        f"next_stage={record['next_stage']}",
        f"implementation_plan_passed={record['implementation_plan_passed']}",
        f"ready_for_implementation_plan_review={record['ready_for_implementation_plan_review']}",
        f"target_module_count={record['target_module_count']}",
        f"implementation_step_count={record['implementation_step_count']}",
        f"integration_contract_count={record['integration_contract_count']}",
        f"regression_test_count={record['regression_test_count']}",
        f"rollback_item_count={record['rollback_item_count']}",
        f"review_gate_count={record['review_gate_count']}",
        f"kaggle_score_semantics={record['kaggle_score_semantics']}",
        f"runtime_activation_performed={record['runtime_activation_performed']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
        f"implementation_performed={record['implementation_performed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    target_lines = "\n".join(
        f"- `{item['path']}`: {item['role']} / `{item['operation']}`"
        for item in record["target_modules"]
    )
    step_lines = "\n".join(f"- `{item}`" for item in record["implementation_steps"])
    contract_lines = "\n".join(f"- `{item}`" for item in record["integration_contracts"])
    test_lines = "\n".join(f"- `{item}`" for item in record["regression_test_plan"])
    rollback_lines = "\n".join(f"- `{item}`" for item in record["rollback_plan"])

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- implementation_plan_verdict: `{record['implementation_plan_verdict']}`
- next_stage: `{record['next_stage']}`

## Implementation plan

- implementation_plan_passed: `{record['implementation_plan_passed']}`
- ready_for_implementation_plan_review: `{record['ready_for_implementation_plan_review']}`

## Target modules

{target_lines}

## Implementation steps

{step_lines}

## Integration contracts

{contract_lines}

## Regression test plan

{test_lines}

## Rollback plan

{rollback_lines}

## Boundary

- implementation_plan_only: `{record['implementation_plan_only']}`
- diagnostic_only: `{record['diagnostic_only']}`
- runtime_activation_performed: `{record['runtime_activation_performed']}`
- runtime_execution_performed: `{record['runtime_execution_performed']}`
- implementation_performed: `{record['implementation_performed']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`
"""
    markdown_path.write_text(markdown, encoding="utf-8")

    def _artifact_ref(path: Path) -> str:
        try:
            return str(path.relative_to(PROJECT_ROOT))
        except ValueError:
            return str(path)

    return {
        "json": _artifact_ref(json_path),
        "index": _artifact_ref(index_path),
        "manifest": _artifact_ref(manifest_path),
        "markdown": _artifact_ref(markdown_path),
    }


def main() -> int:
    record = build_implementation_plan_record()
    issues = validate_implementation_plan_record(record)
    if issues:
        print(f"{TASK_NAME}_INVALID")
        for issue in issues:
            print(issue)
        return 1

    artifacts = write_artifacts(record)

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(f"{TASK_NAME}_READY")
    print(f"{TASK_NAME}_VALID")
    print(record["signature"])
    print(record["baseline_commit"])
    print(record["task_mode"])
    print(record["task_verdict"])
    print(record["implementation_plan_verdict"])
    print(record["next_stage"])
    print(f"implementation_plan_passed={record['implementation_plan_passed']}")
    print(f"ready_for_implementation_plan_review={record['ready_for_implementation_plan_review']}")
    print(f"target_module_count={record['target_module_count']}")
    print(f"implementation_step_count={record['implementation_step_count']}")
    print(f"integration_contract_count={record['integration_contract_count']}")
    print(f"regression_test_count={record['regression_test_count']}")
    print(f"rollback_item_count={record['rollback_item_count']}")
    print(f"review_gate_count={record['review_gate_count']}")
    print(f"kaggle_score_semantics={record['kaggle_score_semantics']}")
    print(f"runtime_activation_performed={record['runtime_activation_performed']}")
    print(f"runtime_execution_performed={record['runtime_execution_performed']}")
    print(f"implementation_performed={record['implementation_performed']}")
    print(f"real_submission_allowed={record['real_submission_allowed']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
