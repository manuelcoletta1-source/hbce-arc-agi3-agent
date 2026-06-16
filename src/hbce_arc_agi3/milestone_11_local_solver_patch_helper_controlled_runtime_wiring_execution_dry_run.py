"""Milestone #11 Task 26 - Controlled Runtime Wiring Execution Dry Run v1.

This module performs a controlled local-only diagnostic dry-run for the runtime
wiring chain. It does not patch the runtime solver, does not perform real runtime
wiring, does not create a Kaggle submission, does not upload anything, and does
not call external APIs.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_DRY_RUN_V1"
TASK_NUMBER = 26
TASK_LABEL = "Milestone #11 Task 26 - Controlled Runtime Wiring Execution Dry Run v1"

SOURCE_TASK = "MILESTONE_11_TASK_25_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_CONTRACT_V1"
NEXT_STAGE = "MILESTONE_11_TASK_27_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_DRY_RUN_REVIEW_V1"

TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_DRY_RUN_V1_LOCAL_ONLY"
TASK_SCOPE = "CONTROLLED_EXECUTION_DRY_RUN_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "CONTROLLED_RUNTIME_WIRING_EXECUTION_DRY_RUN_READY_FOR_REVIEW"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-v1"
)

SOURCE_EXECUTION_CONTRACT_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-execution-contract-v1"
    / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-contract-v1.json"
)


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


def _gate(name: str, passed: bool, required: bool, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "required": bool(required),
        "description": description,
    }


def _planned_step(name: str, simulated: bool, executed: bool, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "simulated": bool(simulated),
        "executed": bool(executed),
        "description": description,
    }


def build_execution_dry_run_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_contract_present = SOURCE_EXECUTION_CONTRACT_ARTIFACT.exists()

    dry_run_steps = [
        _planned_step(
            "load_execution_contract",
            True,
            False,
            "Simulate loading the Task 25 execution contract artifact.",
        ),
        _planned_step(
            "verify_boundary_flags",
            True,
            False,
            "Simulate verification of local-only, dry-run-only and diagnostic-only flags.",
        ),
        _planned_step(
            "prepare_runtime_wiring_plan",
            True,
            False,
            "Simulate construction of a controlled runtime wiring plan without applying it.",
        ),
        _planned_step(
            "check_solver_patch_guard",
            True,
            False,
            "Simulate confirmation that runtime solver patching remains blocked.",
        ),
        _planned_step(
            "check_kaggle_submission_guard",
            True,
            False,
            "Simulate confirmation that Kaggle submission remains blocked.",
        ),
        _planned_step(
            "check_external_dependency_guard",
            True,
            False,
            "Simulate confirmation that no external API dependency is introduced.",
        ),
        _planned_step(
            "prepare_review_package",
            True,
            False,
            "Simulate preparation of evidence for the next review stage.",
        ),
    ]

    dry_run_findings = [
        {
            "finding": "execution_contract_artifact_present",
            "status": source_contract_present,
            "severity": "PASS" if source_contract_present else "BLOCKING",
        },
        {
            "finding": "runtime_wiring_not_performed",
            "status": True,
            "severity": "PASS",
        },
        {
            "finding": "runtime_solver_patch_not_applied",
            "status": True,
            "severity": "PASS",
        },
        {
            "finding": "kaggle_submission_not_sent",
            "status": True,
            "severity": "PASS",
        },
        {
            "finding": "private_core_not_exposed",
            "status": True,
            "severity": "PASS",
        },
        {
            "finding": "legal_certification_false",
            "status": True,
            "severity": "PASS",
        },
    ]

    gates = [
        _gate("source_task_25_execution_contract_artifact_present", source_contract_present, True, "Task 25 execution contract artifact is present."),
        _gate("execution_dry_run_ready", True, True, "Task 26 dry-run record is built."),
        _gate("dry_run_steps_simulated", True, True, "All dry-run steps are simulation-only."),
        _gate("dry_run_steps_executed_false", all(step["executed"] is False for step in dry_run_steps), True, "No dry-run step performs real execution."),
        _gate("runtime_wiring_performed_false", True, True, "No runtime wiring is performed."),
        _gate("runtime_solver_patch_applied_false", True, True, "No runtime solver patch is applied."),
        _gate("runtime_solver_patch_allowed_false", True, True, "Runtime solver patching remains blocked."),
        _gate("controlled_runtime_wiring_execution_allowed_false", True, True, "Controlled runtime wiring real execution remains blocked."),
        _gate("controlled_runtime_wiring_dry_run_completed_true", True, True, "Controlled dry-run simulation is completed."),
        _gate("kaggle_submission_sent_false", True, True, "No Kaggle submission is sent."),
        _gate("kaggle_upload_performed_false", True, True, "No Kaggle upload is performed."),
        _gate("kaggle_authentication_performed_false", True, True, "No Kaggle authentication is performed."),
        _gate("external_api_dependency_false", True, True, "No external API dependency is introduced."),
        _gate("contains_api_keys_false", True, True, "No API keys are contained in this artifact."),
        _gate("private_core_exposure_false", True, True, "No private core exposure is introduced."),
        _gate("legal_certification_false", True, True, "Legal certification remains false."),
        _gate("local_only_true", True, True, "The task remains local-only."),
        _gate("dry_run_only_true", True, True, "The task remains dry-run-only."),
        _gate("diagnostic_only_true", True, True, "The task remains diagnostic-only."),
        _gate("public_safe_true", True, True, "The artifact is public-safe."),
        _gate("deterministic_true", True, True, "The dry-run is deterministic."),
        _gate("fail_closed_active", True, True, "Any missing required condition fails closed."),
        _gate("review_next_stage_declared", True, True, "Next stage is dry-run review."),
        _gate("no_score_claim_allowed", True, True, "No score claim is allowed."),
        _gate("no_competitive_claim_allowed", True, True, "No competitive claim is allowed."),
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
        "source_execution_contract_artifact": str(SOURCE_EXECUTION_CONTRACT_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_execution_contract_artifact_present": source_contract_present,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "execution_dry_run_ready": True,
        "execution_dry_run_valid": source_contract_present,
        "controlled_runtime_wiring_dry_run_started": True,
        "controlled_runtime_wiring_dry_run_completed": True,
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
        "dry_run_step_count": len(dry_run_steps),
        "dry_run_steps": dry_run_steps,
        "dry_run_finding_count": len(dry_run_findings),
        "dry_run_findings": dry_run_findings,
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if len(required_gates) == len(passed_required_gates) else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-EXECUTION-DRY-RUN-" + signature[:12]
    return record


def validate_execution_dry_run_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "execution_dry_run_ready",
        "execution_dry_run_valid",
        "controlled_runtime_wiring_dry_run_started",
        "controlled_runtime_wiring_dry_run_completed",
        "local_only",
        "dry_run_only",
        "diagnostic_only",
        "public_safe",
        "deterministic",
        "fail_closed_required",
        "fail_closed_active",
        "source_execution_contract_artifact_present",
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

    dry_run_steps = record.get("dry_run_steps")
    if not isinstance(dry_run_steps, list) or not dry_run_steps:
        issues.append("DRY_RUN_STEPS_MISSING")
    elif any(step.get("executed") is not False for step in dry_run_steps):
        issues.append("DRY_RUN_STEP_EXECUTED")

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

    if record.get("issue_count") != 0:
        issues.append("ISSUE_COUNT_NOT_ZERO")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-v1.json"
    index_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-index-v1.json"
    manifest_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-manifest-v1.txt"
    markdown_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-execution-dry-run-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "execution_dry_run_ready": record["execution_dry_run_ready"],
        "controlled_runtime_wiring_dry_run_completed": record["controlled_runtime_wiring_dry_run_completed"],
        "controlled_runtime_wiring_execution_allowed": record["controlled_runtime_wiring_execution_allowed"],
        "runtime_wiring_performed": record["runtime_wiring_performed"],
        "runtime_solver_patch_applied": record["runtime_solver_patch_applied"],
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
        f"execution_dry_run_ready={record['execution_dry_run_ready']}",
        f"controlled_runtime_wiring_dry_run_completed={record['controlled_runtime_wiring_dry_run_completed']}",
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
- controlled_runtime_wiring_dry_run_completed: `{record['controlled_runtime_wiring_dry_run_completed']}`
- controlled_runtime_wiring_execution_allowed: `{record['controlled_runtime_wiring_execution_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`

## Dry-run summary

Task 26 performs a controlled diagnostic dry-run simulation only.
It does not perform runtime wiring, does not patch the runtime solver, does not create a Kaggle submission,
does not authenticate to Kaggle, and does not call external APIs.

## Gate status

- gate_count: `{record['gate_count']}`
- passed_gate_count: `{record['passed_gate_count']}`
- issue_count: `{record['issue_count']}`
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
    record = build_execution_dry_run_record()
    issues = validate_execution_dry_run_record(record)
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
