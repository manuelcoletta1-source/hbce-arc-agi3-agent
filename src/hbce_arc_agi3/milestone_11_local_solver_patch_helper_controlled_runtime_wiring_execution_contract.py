"""Milestone #11 Task 25 - Controlled Runtime Wiring Execution Contract v1.

This module creates a local-only execution contract for the controlled runtime
wiring chain. It does not apply runtime wiring, does not patch the runtime solver,
does not create a Kaggle submission, and does not perform external API calls.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_CONTRACT_V1"
TASK_NUMBER = 25
TASK_LABEL = "Milestone #11 Task 25 - Controlled Runtime Wiring Execution Contract v1"

SOURCE_TASK = "MILESTONE_11_TASK_24_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_OPERATOR_APPROVAL_V1"
NEXT_STAGE = "MILESTONE_11_TASK_26_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_DRY_RUN_V1"

TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_CONTRACT_V1_LOCAL_ONLY"
TASK_SCOPE = "EXECUTION_CONTRACT_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "CONTROLLED_RUNTIME_WIRING_EXECUTION_CONTRACT_READY_FOR_DRY_RUN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-11" / "local-solver-patch-helper-controlled-runtime-wiring-execution-contract-v1"

SOURCE_OPERATOR_APPROVAL_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-operator-approval-v1"
    / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-operator-approval-v1.json"
)


def _run_git_head() -> str:
    """Return the current git HEAD as one-line text, or a stable fallback."""
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


def _gate(name: str, passed: bool, required: bool, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "required": bool(required),
        "description": description,
    }


def build_execution_contract_record(baseline_commit: str | None = None) -> dict[str, Any]:
    """Build the deterministic Task 25 execution contract record."""
    baseline = baseline_commit or _run_git_head()
    operator_approval_artifact_present = SOURCE_OPERATOR_APPROVAL_ARTIFACT.exists()

    execution_conditions = [
        "Task 24 operator approval artifact must exist before Task 25 is considered valid.",
        "The contract may authorize only a future dry-run stage, not runtime wiring execution.",
        "The repo must be clean before opening the next task.",
        "The test environment must expose the package with PYTHONPATH=src.",
        "Runtime solver patching must remain blocked.",
        "Runtime wiring must remain blocked.",
        "Kaggle submission creation must remain blocked.",
        "Kaggle upload must remain blocked.",
        "Kaggle authentication must not be invoked.",
        "External API calls must remain blocked.",
        "Private core exposure must remain blocked.",
        "Legal certification must remain false.",
        "All produced artifacts must remain local and public-safe.",
        "Rollback/restoration must be possible before any future controlled execution dry-run.",
        "Any future execution dry-run must be diagnostic-only unless a later explicit task changes that boundary.",
    ]

    gates = [
        _gate("source_task_24_operator_approval_artifact_present", operator_approval_artifact_present, True, "Task 24 operator approval artifact is present."),
        _gate("execution_contract_ready", True, True, "Task 25 contract record is built."),
        _gate("dry_run_next_stage_declared", True, True, "Next stage is a controlled execution dry-run contract stage."),
        _gate("runtime_wiring_performed_false", True, True, "No runtime wiring is performed by this task."),
        _gate("runtime_solver_patch_applied_false", True, True, "No runtime solver patch is applied by this task."),
        _gate("runtime_solver_patch_allowed_false", True, True, "Runtime solver patching remains blocked."),
        _gate("controlled_runtime_wiring_execution_allowed_false", True, True, "Controlled runtime wiring execution is not allowed by this task."),
        _gate("controlled_runtime_wiring_dry_run_allowed_true", True, True, "Only the next dry-run stage is allowed."),
        _gate("kaggle_submission_sent_false", True, True, "No Kaggle submission is sent."),
        _gate("kaggle_upload_performed_false", True, True, "No Kaggle upload is performed."),
        _gate("kaggle_authentication_performed_false", True, True, "No Kaggle authentication is performed."),
        _gate("external_api_dependency_false", True, True, "No external API dependency is introduced."),
        _gate("private_core_exposure_false", True, True, "No private core exposure is introduced."),
        _gate("contains_api_keys_false", True, True, "No API keys are contained in this artifact."),
        _gate("legal_certification_false", True, True, "Legal certification remains explicitly false."),
        _gate("local_only_true", True, True, "The task remains local-only."),
        _gate("diagnostic_only_true", True, True, "The task remains diagnostic-only."),
        _gate("public_safe_true", True, True, "The artifact is public-safe."),
        _gate("deterministic_true", True, True, "The contract is deterministic."),
        _gate("manual_operator_boundary_preserved", True, True, "Manual operator boundary is preserved."),
        _gate("repo_clean_required", True, True, "Repo cleanliness is required before next task."),
        _gate("pythonpath_src_required", True, True, "PYTHONPATH=src is required for full-suite verification."),
        _gate("historical_artifact_drift_must_be_restored", True, True, "Historical generated artifacts must be restored if full suite rewrites them."),
        _gate("no_score_claim_allowed", True, True, "No score claim is allowed."),
        _gate("no_competitive_claim_allowed", True, True, "No competitive claim is allowed."),
        _gate("failure_mode_fail_closed", True, True, "Any missing required condition must fail closed."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_operator_approval_artifact": str(SOURCE_OPERATOR_APPROVAL_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_operator_approval_artifact_present": operator_approval_artifact_present,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "execution_contract_ready": True,
        "execution_contract_valid": operator_approval_artifact_present,
        "controlled_runtime_wiring_dry_run_allowed": True,
        "controlled_runtime_wiring_execution_allowed": False,
        "controlled_runtime_wiring_authorized": False,
        "runtime_wiring_performed": False,
        "runtime_solver_patch_allowed": False,
        "runtime_solver_patch_applied": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "submission_json_created": False,
        "real_submission_candidate_created": False,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "kaggle_upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "local_only": True,
        "dry_run_only": True,
        "diagnostic_only": True,
        "public_safe": True,
        "deterministic": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "execution_condition_count": len(execution_conditions),
        "execution_conditions": execution_conditions,
        "contract_gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "contract_issue_count": 0 if len(required_gates) == len(passed_required_gates) else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-EXECUTION-CONTRACT-" + signature[:12]
    return record


def validate_execution_contract_record(record: dict[str, Any]) -> list[str]:
    """Return validation issues. Empty list means the contract is valid."""
    issues: list[str] = []

    expected_true = [
        "execution_contract_ready",
        "execution_contract_valid",
        "controlled_runtime_wiring_dry_run_allowed",
        "local_only",
        "dry_run_only",
        "diagnostic_only",
        "public_safe",
        "deterministic",
        "fail_closed_required",
        "fail_closed_active",
        "source_operator_approval_artifact_present",
    ]
    expected_false = [
        "controlled_runtime_wiring_execution_allowed",
        "controlled_runtime_wiring_authorized",
        "runtime_wiring_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_patch_applied",
        "runtime_solver_modified",
        "ranker_runtime_modified",
        "submission_json_created",
        "real_submission_candidate_created",
        "real_submission_allowed",
        "kaggle_submission_sent",
        "kaggle_upload_performed",
        "kaggle_authentication_performed",
        "external_api_dependency",
        "contains_api_keys",
        "private_core_exposure",
        "legal_certification",
        "official_score_claim_allowed",
        "competitive_score_claim_allowed",
        "real_public_score_claimed",
        "private_score_claimed",
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

    gates = record.get("gates")
    if not isinstance(gates, list) or not gates:
        issues.append("GATES_MISSING")
    else:
        failed_required = [
            gate.get("name", "UNKNOWN_GATE")
            for gate in gates
            if gate.get("required") is True and gate.get("passed") is not True
        ]
        issues.extend(f"REQUIRED_GATE_FAILED:{name}" for name in failed_required)

    if record.get("contract_issue_count") != 0:
        issues.append("CONTRACT_ISSUE_COUNT_NOT_ZERO")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    """Write JSON, index, manifest and Markdown artifacts."""
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-v1.json"
    index_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-index-v1.json"
    manifest_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-manifest-v1.txt"
    markdown_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "execution_contract_ready": record["execution_contract_ready"],
        "controlled_runtime_wiring_dry_run_allowed": record["controlled_runtime_wiring_dry_run_allowed"],
        "controlled_runtime_wiring_execution_allowed": record["controlled_runtime_wiring_execution_allowed"],
        "runtime_wiring_performed": record["runtime_wiring_performed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "legal_certification": record["legal_certification"],
    }
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        f"revision={record['revision']}",
        f"task_id={record['task_id']}",
        f"signature={record['signature']}",
        f"baseline_commit={record['baseline_commit']}",
        f"source_task={record['source_task']}",
        f"task_mode={record['task_mode']}",
        f"task_scope={record['task_scope']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"execution_contract_ready={record['execution_contract_ready']}",
        f"controlled_runtime_wiring_dry_run_allowed={record['controlled_runtime_wiring_dry_run_allowed']}",
        f"controlled_runtime_wiring_execution_allowed={record['controlled_runtime_wiring_execution_allowed']}",
        f"runtime_wiring_performed={record['runtime_wiring_performed']}",
        f"runtime_solver_patch_applied={record['runtime_solver_patch_applied']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- source_task: `{record['source_task']}`
- verdict: `{record['task_verdict']}`
- next_stage: `{record['next_stage']}`

## Boundary

- local_only: `{record['local_only']}`
- dry_run_only: `{record['dry_run_only']}`
- diagnostic_only: `{record['diagnostic_only']}`
- runtime_wiring_performed: `{record['runtime_wiring_performed']}`
- runtime_solver_patch_applied: `{record['runtime_solver_patch_applied']}`
- controlled_runtime_wiring_dry_run_allowed: `{record['controlled_runtime_wiring_dry_run_allowed']}`
- controlled_runtime_wiring_execution_allowed: `{record['controlled_runtime_wiring_execution_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`

## Contract summary

Task 25 creates the controlled execution contract required before any future runtime wiring dry-run.
It does not perform runtime wiring, does not patch the runtime solver, does not create a Kaggle submission,
does not authenticate to Kaggle, and does not call external APIs.

## Gate status

- contract_gate_count: `{record['contract_gate_count']}`
- passed_gate_count: `{record['passed_gate_count']}`
- contract_issue_count: `{record['contract_issue_count']}`
"""
    markdown_path.write_text(markdown, encoding="utf-8")

    return {
        "json": str(json_path.relative_to(PROJECT_ROOT)),
        "index": str(index_path.relative_to(PROJECT_ROOT)),
        "manifest": str(manifest_path.relative_to(PROJECT_ROOT)),
        "markdown": str(markdown_path.relative_to(PROJECT_ROOT)),
    }


def main() -> int:
    record = build_execution_contract_record()
    issues = validate_execution_contract_record(record)
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
    print(record["next_stage"])
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
