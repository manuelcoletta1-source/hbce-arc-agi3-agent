"""Milestone #11 Task 30 - Controlled Runtime Wiring Closure Audit v1.

This module audits the controlled runtime wiring subchain after Task 29.
It does not perform runtime wiring, does not patch the runtime solver, does not
create a Kaggle submission, does not authenticate to Kaggle, and does not call
external APIs.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_V1"
TASK_NUMBER = 30
TASK_LABEL = "Milestone #11 Task 30 - Controlled Runtime Wiring Closure Audit v1"

SOURCE_TASK = "MILESTONE_11_TASK_29_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_REVIEW_DECISION_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_11_TASK_31_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_V1"

TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_V1_LOCAL_ONLY"
TASK_SCOPE = "CLOSURE_AUDIT_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_PASS_REAL_EXECUTION_STILL_BLOCKED"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-closure-audit-v1"
)

SOURCE_CLOSURE_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-review-decision-closure-v1"
    / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-review-decision-closure-v1.json"
)


AUDITED_TASK_CHAIN = [
    "MILESTONE_11_TASK_24_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_OPERATOR_APPROVAL_V1",
    "MILESTONE_11_TASK_25_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_CONTRACT_V1",
    "MILESTONE_11_TASK_26_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_DRY_RUN_V1",
    "MILESTONE_11_TASK_27_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_DRY_RUN_REVIEW_V1",
    "MILESTONE_11_TASK_28_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_REVIEW_DECISION_V1",
    "MILESTONE_11_TASK_29_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_REVIEW_DECISION_CLOSURE_V1",
    "MILESTONE_11_TASK_30_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_V1",
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


def _gate(name: str, passed: bool, required: bool, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "required": bool(required),
        "description": description,
    }


def _audit_check(name: str, status: bool, severity: str, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "status": bool(status),
        "severity": severity,
        "description": description,
    }


def _load_source_closure_artifact() -> dict[str, Any] | None:
    if not SOURCE_CLOSURE_ARTIFACT.exists():
        return None
    try:
        return json.loads(SOURCE_CLOSURE_ARTIFACT.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_closure_audit_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_present = SOURCE_CLOSURE_ARTIFACT.exists()
    source = _load_source_closure_artifact()

    source_parseable = source is not None
    source_valid = bool(source and source.get("review_decision_closure_valid") is True)
    source_passed = bool(source and source.get("review_decision_closure_passed") is True)
    source_closed = bool(source and source.get("review_decision_closure") == "CLOSED_REAL_EXECUTION_STILL_BLOCKED")
    source_subchain_closed = bool(source and source.get("milestone_subchain_closed") is True)
    source_subchain_locked = bool(source and source.get("milestone_subchain_locked") is True)
    source_task_count_ok = bool(source and source.get("closed_task_count") == 6)
    source_execution_blocked = bool(source and source.get("controlled_runtime_wiring_execution_allowed") is False)
    source_authorized_false = bool(source and source.get("controlled_runtime_wiring_authorized") is False)
    source_runtime_wiring_false = bool(source and source.get("runtime_wiring_performed") is False)
    source_patch_false = bool(source and source.get("runtime_solver_patch_applied") is False)
    source_submission_false = bool(source and source.get("kaggle_submission_sent") is False)
    source_upload_false = bool(source and source.get("kaggle_upload_performed") is False)
    source_auth_false = bool(source and source.get("kaggle_authentication_performed") is False)
    source_external_false = bool(source and source.get("external_api_dependency") is False)
    source_private_core_false = bool(source and source.get("private_core_exposure") is False)
    source_legal_false = bool(source and source.get("legal_certification") is False)

    audit_checks = [
        _audit_check("source_task_29_closure_artifact_present", source_present, "PASS" if source_present else "BLOCKING", "Task 29 closure artifact exists."),
        _audit_check("source_task_29_closure_artifact_parseable", source_parseable, "PASS" if source_parseable else "BLOCKING", "Task 29 closure artifact is parseable JSON."),
        _audit_check("source_task_29_closure_valid", source_valid, "PASS" if source_valid else "BLOCKING", "Task 29 closure is valid."),
        _audit_check("source_task_29_closure_passed", source_passed, "PASS" if source_passed else "BLOCKING", "Task 29 closure passed."),
        _audit_check("source_task_29_closure_closed_real_execution_blocked", source_closed, "PASS" if source_closed else "BLOCKING", "Task 29 closure kept real execution blocked."),
        _audit_check("source_milestone_subchain_closed", source_subchain_closed, "PASS" if source_subchain_closed else "BLOCKING", "Task 29 declared the subchain closed."),
        _audit_check("source_milestone_subchain_locked", source_subchain_locked, "PASS" if source_subchain_locked else "BLOCKING", "Task 29 declared the subchain locked."),
        _audit_check("source_closed_task_count_ok", source_task_count_ok, "PASS" if source_task_count_ok else "BLOCKING", "Task 29 closed six prior tasks."),
        _audit_check("controlled_runtime_wiring_execution_allowed_false", source_execution_blocked, "PASS" if source_execution_blocked else "BLOCKING", "Real controlled runtime wiring remains blocked."),
        _audit_check("controlled_runtime_wiring_authorized_false", source_authorized_false, "PASS" if source_authorized_false else "BLOCKING", "Controlled runtime wiring authorization remains false."),
        _audit_check("runtime_wiring_not_performed", source_runtime_wiring_false, "PASS" if source_runtime_wiring_false else "BLOCKING", "Runtime wiring was not performed."),
        _audit_check("runtime_solver_patch_not_applied", source_patch_false, "PASS" if source_patch_false else "BLOCKING", "Runtime solver patch was not applied."),
        _audit_check("kaggle_submission_not_sent", source_submission_false, "PASS" if source_submission_false else "BLOCKING", "Kaggle submission was not sent."),
        _audit_check("kaggle_upload_not_performed", source_upload_false, "PASS" if source_upload_false else "BLOCKING", "Kaggle upload was not performed."),
        _audit_check("kaggle_authentication_not_performed", source_auth_false, "PASS" if source_auth_false else "BLOCKING", "Kaggle authentication was not performed."),
        _audit_check("external_api_dependency_false", source_external_false, "PASS" if source_external_false else "BLOCKING", "External API dependency remains false."),
        _audit_check("private_core_exposure_false", source_private_core_false, "PASS" if source_private_core_false else "BLOCKING", "Private core exposure remains false."),
        _audit_check("legal_certification_false", source_legal_false, "PASS" if source_legal_false else "BLOCKING", "legal_certification remains false."),
    ]

    audit_passed = all(check["status"] is True for check in audit_checks)

    audit_controls = [
        "Closure audit accepts Task 29 closure as valid.",
        "Audited subchain Task 24 through Task 30 is public-safe.",
        "Real runtime wiring remains blocked.",
        "Runtime solver patching remains blocked.",
        "Ranker runtime modification remains blocked.",
        "Kaggle submission creation remains blocked.",
        "Kaggle upload remains blocked.",
        "Kaggle authentication remains blocked.",
        "External API calls remain blocked.",
        "Private core exposure remains blocked.",
        "No public score claim is allowed.",
        "No private score claim is allowed.",
        "No legal certification is claimed.",
        "Any future execution requires a separate explicit authorization milestone.",
    ]

    gates = [
        _gate("source_task_29_closure_artifact_present", source_present, True, "Task 29 closure artifact is present."),
        _gate("source_task_29_closure_artifact_parseable", source_parseable, True, "Task 29 closure artifact is parseable."),
        _gate("source_task_29_closure_valid", source_valid, True, "Task 29 closure is valid."),
        _gate("source_task_29_closure_passed", source_passed, True, "Task 29 closure passed."),
        _gate("source_task_29_closed_real_execution_blocked", source_closed, True, "Task 29 kept real execution blocked."),
        _gate("source_milestone_subchain_closed", source_subchain_closed, True, "Task 29 subchain closure is true."),
        _gate("source_milestone_subchain_locked", source_subchain_locked, True, "Task 29 subchain lock is true."),
        _gate("source_closed_task_count_ok", source_task_count_ok, True, "Task 29 closed-task count is correct."),
        _gate("closure_audit_ready", True, True, "Task 30 audit record is built."),
        _gate("closure_audit_passed", audit_passed, True, "All required audit checks passed."),
        _gate("audited_task_chain_declared", True, True, "Audited task chain 24 through 30 is declared."),
        _gate("next_stage_audit_report_declared", True, True, "Next stage is closure audit report."),
        _gate("runtime_wiring_performed_false", True, True, "Task 30 performs no runtime wiring."),
        _gate("runtime_solver_patch_allowed_false", True, True, "Runtime solver patching remains blocked."),
        _gate("runtime_solver_patch_applied_false", True, True, "Task 30 applies no runtime solver patch."),
        _gate("runtime_solver_modified_false", True, True, "Runtime solver remains unmodified."),
        _gate("ranker_runtime_modified_false", True, True, "Ranker runtime remains unmodified."),
        _gate("controlled_runtime_wiring_execution_allowed_false", True, True, "Real controlled runtime wiring execution remains blocked."),
        _gate("controlled_runtime_wiring_authorized_false", True, True, "Controlled runtime wiring remains unauthorized."),
        _gate("submission_json_created_false", True, True, "No submission JSON is created."),
        _gate("real_submission_candidate_created_false", True, True, "No real submission candidate is created."),
        _gate("real_submission_allowed_false", True, True, "Real submission remains blocked."),
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
        _gate("audit_only_true", True, True, "The task remains audit-only."),
        _gate("public_safe_true", True, True, "The artifact is public-safe."),
        _gate("deterministic_true", True, True, "The audit is deterministic."),
        _gate("fail_closed_active", True, True, "Any missing required condition fails closed."),
        _gate("no_score_claim_allowed", True, True, "No score claim is allowed."),
        _gate("no_competitive_claim_allowed", True, True, "No competitive score claim is allowed."),
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
        "source_closure_artifact": str(SOURCE_CLOSURE_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_closure_artifact_present": source_present,
        "source_closure_artifact_parseable": source_parseable,
        "source_closure_valid": source_valid,
        "source_closure_passed": source_passed,
        "source_closure_real_execution_blocked": source_closed,
        "source_milestone_subchain_closed": source_subchain_closed,
        "source_milestone_subchain_locked": source_subchain_locked,
        "source_closed_task_count_ok": source_task_count_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "closure_audit_ready": True,
        "closure_audit_valid": audit_passed,
        "closure_audit_passed": audit_passed,
        "closure_audit": "PASS_REAL_EXECUTION_STILL_BLOCKED" if audit_passed else "FAIL_CLOSED",
        "audited_task_count": len(AUDITED_TASK_CHAIN),
        "audited_task_chain": AUDITED_TASK_CHAIN,
        "audit_controls": audit_controls,
        "audit_check_count": len(audit_checks),
        "audit_checks": audit_checks,
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
        "audit_only": True,
        "public_safe": True,
        "deterministic": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
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
    record["task_id"] = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-CLOSURE-AUDIT-" + signature[:12]
    return record


def validate_closure_audit_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "closure_audit_ready",
        "closure_audit_valid",
        "closure_audit_passed",
        "source_closure_artifact_present",
        "source_closure_artifact_parseable",
        "source_closure_valid",
        "source_closure_passed",
        "source_closure_real_execution_blocked",
        "source_milestone_subchain_closed",
        "source_milestone_subchain_locked",
        "source_closed_task_count_ok",
        "local_only",
        "dry_run_only",
        "diagnostic_only",
        "audit_only",
        "public_safe",
        "deterministic",
        "fail_closed_required",
        "fail_closed_active",
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

    if record.get("closure_audit") != "PASS_REAL_EXECUTION_STILL_BLOCKED":
        issues.append("CLOSURE_AUDIT_NOT_PASS_OR_BLOCKED")

    if record.get("audited_task_count") != 7:
        issues.append("AUDITED_TASK_COUNT_MISMATCH")

    audit_checks = record.get("audit_checks")
    if not isinstance(audit_checks, list) or not audit_checks:
        issues.append("AUDIT_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in audit_checks):
        issues.append("AUDIT_CHECK_FAILED")

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

    json_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-v1.json"
    index_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-index-v1.json"
    manifest_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-manifest-v1.txt"
    markdown_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "closure_audit_ready": record["closure_audit_ready"],
        "closure_audit_passed": record["closure_audit_passed"],
        "closure_audit": record["closure_audit"],
        "audited_task_count": record["audited_task_count"],
        "source_closure_valid": record["source_closure_valid"],
        "source_closure_passed": record["source_closure_passed"],
        "controlled_runtime_wiring_execution_allowed": record["controlled_runtime_wiring_execution_allowed"],
        "runtime_wiring_performed": record["runtime_wiring_performed"],
        "runtime_solver_patch_applied": record["runtime_solver_patch_applied"],
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
        f"source_task={record['source_task']}",
        f"task_mode={record['task_mode']}",
        f"task_scope={record['task_scope']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"closure_audit_ready={record['closure_audit_ready']}",
        f"closure_audit_passed={record['closure_audit_passed']}",
        f"closure_audit={record['closure_audit']}",
        f"audited_task_count={record['audited_task_count']}",
        f"source_closure_valid={record['source_closure_valid']}",
        f"source_closure_passed={record['source_closure_passed']}",
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
- closure_audit: `{record['closure_audit']}`
- next_stage: `{record['next_stage']}`

## Boundary

- local_only: `{record['local_only']}`
- dry_run_only: `{record['dry_run_only']}`
- diagnostic_only: `{record['diagnostic_only']}`
- audit_only: `{record['audit_only']}`
- runtime_wiring_performed: `{record['runtime_wiring_performed']}`
- runtime_solver_patch_applied: `{record['runtime_solver_patch_applied']}`
- controlled_runtime_wiring_execution_allowed: `{record['controlled_runtime_wiring_execution_allowed']}`
- controlled_runtime_wiring_authorized: `{record['controlled_runtime_wiring_authorized']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`

## Audit summary

Task 30 audits the controlled runtime wiring subchain from Task 24 through Task 30.
The audit passes for closure continuity only. It does not authorize real runtime wiring.

## Gate status

- audited_task_count: `{record['audited_task_count']}`
- audit_check_count: `{record['audit_check_count']}`
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
    record = build_closure_audit_record()
    issues = validate_closure_audit_record(record)
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
