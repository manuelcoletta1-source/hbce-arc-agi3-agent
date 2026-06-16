"""Milestone #11 Task 33 - Controlled Runtime Wiring Closure Audit Report Review Decision v1.

This module records the formal decision on the Task 32 closure audit report review.
It authorizes only closure progression. It does not authorize real runtime wiring,
does not patch the runtime solver, does not create a Kaggle submission, does not
authenticate to Kaggle, and does not call external APIs.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_DECISION_V1"
TASK_NUMBER = 33
TASK_LABEL = "Milestone #11 Task 33 - Controlled Runtime Wiring Closure Audit Report Review Decision v1"

SOURCE_TASK = "MILESTONE_11_TASK_32_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_V1"
NEXT_STAGE = "MILESTONE_11_TASK_34_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_DECISION_CLOSURE_V1"

TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_DECISION_V1_LOCAL_ONLY"
TASK_SCOPE = "CLOSURE_AUDIT_REPORT_REVIEW_DECISION_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_DECISION_APPROVED_FOR_CLOSURE_REAL_EXECUTION_BLOCKED"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-v1"
)

SOURCE_REVIEW_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-v1"
    / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-v1.json"
)


DECIDED_TASK_CHAIN = [
    "MILESTONE_11_TASK_24_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_OPERATOR_APPROVAL_V1",
    "MILESTONE_11_TASK_25_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_CONTRACT_V1",
    "MILESTONE_11_TASK_26_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_DRY_RUN_V1",
    "MILESTONE_11_TASK_27_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_DRY_RUN_REVIEW_V1",
    "MILESTONE_11_TASK_28_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_REVIEW_DECISION_V1",
    "MILESTONE_11_TASK_29_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_REVIEW_DECISION_CLOSURE_V1",
    "MILESTONE_11_TASK_30_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_V1",
    "MILESTONE_11_TASK_31_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_V1",
    "MILESTONE_11_TASK_32_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_V1",
    "MILESTONE_11_TASK_33_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_DECISION_V1",
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


def _decision_check(name: str, status: bool, severity: str, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "status": bool(status),
        "severity": severity,
        "description": description,
    }


def _load_source_review_artifact() -> dict[str, Any] | None:
    if not SOURCE_REVIEW_ARTIFACT.exists():
        return None
    try:
        return json.loads(SOURCE_REVIEW_ARTIFACT.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_closure_audit_report_review_decision_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_present = SOURCE_REVIEW_ARTIFACT.exists()
    source = _load_source_review_artifact()

    source_parseable = source is not None
    source_ready = bool(source and source.get("closure_audit_report_review_ready") is True)
    source_valid = bool(source and source.get("closure_audit_report_review_valid") is True)
    source_passed = bool(source and source.get("closure_audit_report_review_passed") is True)
    source_review_pass_blocked = bool(
        source and source.get("closure_audit_report_review") == "REVIEW_PASS_READY_FOR_DECISION_REAL_EXECUTION_BLOCKED"
    )
    source_task_count_ok = bool(source and source.get("reviewed_task_count") == 9)

    source_summary = source.get("review_summary") if isinstance(source, dict) else None
    source_summary_ok = bool(
        isinstance(source_summary, dict)
        and source_summary.get("real_runtime_wiring") == "BLOCKED"
        and source_summary.get("runtime_solver_patch") == "BLOCKED"
        and source_summary.get("kaggle_submission") == "NOT_SENT"
        and source_summary.get("private_core") == "NOT_EXPOSED"
        and source_summary.get("legal_certification") == "FALSE"
        and source_summary.get("score_claim") == "NOT_ALLOWED"
        and source_summary.get("decision_required_next") is True
    )
    source_decision_required = bool(isinstance(source_summary, dict) and source_summary.get("decision_required_next") is True)

    source_checks_ok = bool(
        source
        and isinstance(source.get("review_checks"), list)
        and source.get("review_check_count") == len(source.get("review_checks"))
        and all(check.get("status") is True for check in source.get("review_checks"))
    )

    source_execution_blocked = bool(source and source.get("controlled_runtime_wiring_execution_allowed") is False)
    source_authorized_false = bool(source and source.get("controlled_runtime_wiring_authorized") is False)
    source_runtime_wiring_false = bool(source and source.get("runtime_wiring_performed") is False)
    source_patch_allowed_false = bool(source and source.get("runtime_solver_patch_allowed") is False)
    source_patch_applied_false = bool(source and source.get("runtime_solver_patch_applied") is False)
    source_runtime_solver_modified_false = bool(source and source.get("runtime_solver_modified") is False)
    source_ranker_modified_false = bool(source and source.get("ranker_runtime_modified") is False)
    source_submission_json_false = bool(source and source.get("submission_json_created") is False)
    source_real_candidate_false = bool(source and source.get("real_submission_candidate_created") is False)
    source_real_submission_allowed_false = bool(source and source.get("real_submission_allowed") is False)
    source_submission_false = bool(source and source.get("kaggle_submission_sent") is False)
    source_upload_false = bool(source and source.get("kaggle_upload_performed") is False)
    source_auth_false = bool(source and source.get("kaggle_authentication_performed") is False)
    source_external_false = bool(source and source.get("external_api_dependency") is False)
    source_keys_false = bool(source and source.get("contains_api_keys") is False)
    source_private_core_false = bool(source and source.get("private_core_exposure") is False)
    source_legal_false = bool(source and source.get("legal_certification") is False)
    source_issue_zero = bool(source and source.get("issue_count") == 0)
    source_warning_zero = bool(source and source.get("warning_count") == 0)
    source_local = bool(source and source.get("local_only") is True)
    source_dry = bool(source and source.get("dry_run_only") is True)
    source_diag = bool(source and source.get("diagnostic_only") is True)
    source_review_only = bool(source and source.get("audit_report_review_only") is True)

    closure_progression_authorized = all(
        [
            source_present,
            source_parseable,
            source_ready,
            source_valid,
            source_passed,
            source_review_pass_blocked,
            source_task_count_ok,
            source_summary_ok,
            source_decision_required,
            source_checks_ok,
            source_execution_blocked,
            source_authorized_false,
            source_runtime_wiring_false,
            source_patch_allowed_false,
            source_patch_applied_false,
            source_runtime_solver_modified_false,
            source_ranker_modified_false,
            source_submission_json_false,
            source_real_candidate_false,
            source_real_submission_allowed_false,
            source_submission_false,
            source_upload_false,
            source_auth_false,
            source_external_false,
            source_keys_false,
            source_private_core_false,
            source_legal_false,
            source_issue_zero,
            source_warning_zero,
            source_local,
            source_dry,
            source_diag,
            source_review_only,
        ]
    )

    decision_checks = [
        _decision_check("source_task_32_review_artifact_present", source_present, "PASS" if source_present else "BLOCKING", "Task 32 review artifact exists."),
        _decision_check("source_task_32_review_artifact_parseable", source_parseable, "PASS" if source_parseable else "BLOCKING", "Task 32 review artifact is parseable JSON."),
        _decision_check("source_task_32_review_ready", source_ready, "PASS" if source_ready else "BLOCKING", "Task 32 review is ready."),
        _decision_check("source_task_32_review_valid", source_valid, "PASS" if source_valid else "BLOCKING", "Task 32 review is valid."),
        _decision_check("source_task_32_review_passed", source_passed, "PASS" if source_passed else "BLOCKING", "Task 32 review passed."),
        _decision_check("source_task_32_review_real_execution_blocked", source_review_pass_blocked, "PASS" if source_review_pass_blocked else "BLOCKING", "Task 32 review keeps real execution blocked."),
        _decision_check("source_reviewed_task_count_ok", source_task_count_ok, "PASS" if source_task_count_ok else "BLOCKING", "Task 32 reviewed task count is correct."),
        _decision_check("source_review_summary_ok", source_summary_ok, "PASS" if source_summary_ok else "BLOCKING", "Task 32 review summary is coherent."),
        _decision_check("source_decision_required_next_true", source_decision_required, "PASS" if source_decision_required else "BLOCKING", "Task 32 explicitly requires a decision next."),
        _decision_check("source_review_checks_consistent", source_checks_ok, "PASS" if source_checks_ok else "BLOCKING", "Task 32 review checks are counted and passed."),
        _decision_check("controlled_runtime_wiring_execution_allowed_false", source_execution_blocked, "PASS" if source_execution_blocked else "BLOCKING", "Real controlled runtime wiring remains blocked."),
        _decision_check("controlled_runtime_wiring_authorized_false", source_authorized_false, "PASS" if source_authorized_false else "BLOCKING", "Controlled runtime wiring authorization remains false."),
        _decision_check("runtime_wiring_not_performed", source_runtime_wiring_false, "PASS" if source_runtime_wiring_false else "BLOCKING", "Runtime wiring was not performed."),
        _decision_check("runtime_solver_patch_allowed_false", source_patch_allowed_false, "PASS" if source_patch_allowed_false else "BLOCKING", "Runtime solver patching remains blocked."),
        _decision_check("runtime_solver_patch_not_applied", source_patch_applied_false, "PASS" if source_patch_applied_false else "BLOCKING", "Runtime solver patch was not applied."),
        _decision_check("runtime_solver_not_modified", source_runtime_solver_modified_false, "PASS" if source_runtime_solver_modified_false else "BLOCKING", "Runtime solver remains unmodified."),
        _decision_check("ranker_runtime_not_modified", source_ranker_modified_false, "PASS" if source_ranker_modified_false else "BLOCKING", "Ranker runtime remains unmodified."),
        _decision_check("submission_json_not_created", source_submission_json_false, "PASS" if source_submission_json_false else "BLOCKING", "Submission JSON was not created."),
        _decision_check("real_submission_candidate_not_created", source_real_candidate_false, "PASS" if source_real_candidate_false else "BLOCKING", "Real submission candidate was not created."),
        _decision_check("real_submission_allowed_false", source_real_submission_allowed_false, "PASS" if source_real_submission_allowed_false else "BLOCKING", "Real submission remains blocked."),
        _decision_check("kaggle_submission_not_sent", source_submission_false, "PASS" if source_submission_false else "BLOCKING", "Kaggle submission was not sent."),
        _decision_check("kaggle_upload_not_performed", source_upload_false, "PASS" if source_upload_false else "BLOCKING", "Kaggle upload was not performed."),
        _decision_check("kaggle_authentication_not_performed", source_auth_false, "PASS" if source_auth_false else "BLOCKING", "Kaggle authentication was not performed."),
        _decision_check("external_api_dependency_false", source_external_false, "PASS" if source_external_false else "BLOCKING", "External API dependency remains false."),
        _decision_check("contains_api_keys_false", source_keys_false, "PASS" if source_keys_false else "BLOCKING", "No API keys are contained."),
        _decision_check("private_core_exposure_false", source_private_core_false, "PASS" if source_private_core_false else "BLOCKING", "Private core exposure remains false."),
        _decision_check("legal_certification_false", source_legal_false, "PASS" if source_legal_false else "BLOCKING", "legal_certification remains false."),
        _decision_check("source_issue_count_zero", source_issue_zero, "PASS" if source_issue_zero else "BLOCKING", "Source review issue count is zero."),
        _decision_check("source_warning_count_zero", source_warning_zero, "PASS" if source_warning_zero else "WARNING", "Source review warning count is zero."),
        _decision_check("source_local_only_true", source_local, "PASS" if source_local else "BLOCKING", "Source review is local-only."),
        _decision_check("source_dry_run_only_true", source_dry, "PASS" if source_dry else "BLOCKING", "Source review is dry-run-only."),
        _decision_check("source_diagnostic_only_true", source_diag, "PASS" if source_diag else "BLOCKING", "Source review is diagnostic-only."),
        _decision_check("source_audit_report_review_only_true", source_review_only, "PASS" if source_review_only else "BLOCKING", "Source review is audit-report-review-only."),
        _decision_check("closure_progression_authorized", closure_progression_authorized, "PASS" if closure_progression_authorized else "BLOCKING", "Only closure progression is authorized."),
    ]

    decision_passed = all(check["status"] is True for check in decision_checks)

    decision_summary = {
        "decision_scope": TASK_SCOPE,
        "source_review": "TASK_32_CLOSURE_AUDIT_REPORT_REVIEW",
        "decided_chain": "TASK_24_THROUGH_TASK_33",
        "decision": "APPROVE_REVIEW_FOR_CLOSURE_REAL_EXECUTION_STILL_BLOCKED" if decision_passed else "FAIL_CLOSED",
        "closure_progression_authorized": decision_passed,
        "real_runtime_wiring": "BLOCKED",
        "real_runtime_wiring_authorized": False,
        "runtime_solver_patch": "BLOCKED",
        "runtime_solver_patch_authorized": False,
        "ranker_runtime_modification": "BLOCKED",
        "kaggle_submission": "NOT_SENT",
        "kaggle_upload": "NOT_PERFORMED",
        "kaggle_authentication": "NOT_PERFORMED",
        "external_api": "NOT_USED",
        "private_core": "NOT_EXPOSED",
        "legal_certification": "FALSE",
        "score_claim": "NOT_ALLOWED",
        "closure_required_next": True,
    }

    decision_notes = [
        "Task 33 records the formal decision on the Task 32 closure audit report review.",
        "The decision approves only progression to a closure artifact.",
        "The decision does not authorize real controlled runtime wiring.",
        "The decision does not authorize runtime solver patching.",
        "The decision does not authorize ranker runtime modification.",
        "No Kaggle submission, upload, or authentication is performed.",
        "No external API dependency is introduced.",
        "No API keys are contained.",
        "No private HBCE/JOKER-C2 core material is exposed.",
        "No score claim is made.",
        "legal_certification remains false.",
        "The next stage is a decision closure, not real execution.",
    ]

    gates = [
        _gate("source_task_32_review_artifact_present", source_present, True, "Task 32 review artifact is present."),
        _gate("source_task_32_review_artifact_parseable", source_parseable, True, "Task 32 review artifact is parseable."),
        _gate("source_task_32_review_ready", source_ready, True, "Task 32 review is ready."),
        _gate("source_task_32_review_valid", source_valid, True, "Task 32 review is valid."),
        _gate("source_task_32_review_passed", source_passed, True, "Task 32 review passed."),
        _gate("source_task_32_review_real_execution_blocked", source_review_pass_blocked, True, "Task 32 keeps real execution blocked."),
        _gate("source_reviewed_task_count_ok", source_task_count_ok, True, "Task 32 reviewed task count is correct."),
        _gate("source_review_summary_ok", source_summary_ok, True, "Task 32 review summary is coherent."),
        _gate("source_decision_required_next_true", source_decision_required, True, "Task 32 requires a decision next."),
        _gate("source_review_checks_consistent", source_checks_ok, True, "Task 32 review checks are consistent."),
        _gate("decision_ready", True, True, "Task 33 decision record is built."),
        _gate("decision_passed", decision_passed, True, "All required decision checks passed."),
        _gate("closure_progression_authorized_true", closure_progression_authorized, True, "Only closure progression is authorized."),
        _gate("decided_task_chain_declared", True, True, "Decided task chain 24 through 33 is declared."),
        _gate("next_stage_decision_closure_declared", True, True, "Next stage is closure audit report review decision closure."),
        _gate("runtime_wiring_performed_false", True, True, "Task 33 performs no runtime wiring."),
        _gate("runtime_solver_patch_allowed_false", True, True, "Runtime solver patching remains blocked."),
        _gate("runtime_solver_patch_applied_false", True, True, "Task 33 applies no runtime solver patch."),
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
        _gate("audit_report_review_decision_only_true", True, True, "The task remains audit-report-review-decision-only."),
        _gate("public_safe_true", True, True, "The artifact is public-safe."),
        _gate("deterministic_true", True, True, "The decision is deterministic."),
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
        "source_review_artifact": str(SOURCE_REVIEW_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_review_artifact_present": source_present,
        "source_review_artifact_parseable": source_parseable,
        "source_review_ready": source_ready,
        "source_review_valid": source_valid,
        "source_review_passed": source_passed,
        "source_review_real_execution_blocked": source_review_pass_blocked,
        "source_reviewed_task_count_ok": source_task_count_ok,
        "source_review_summary_ok": source_summary_ok,
        "source_decision_required_next": source_decision_required,
        "source_review_checks_consistent": source_checks_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "closure_audit_report_review_decision_ready": True,
        "closure_audit_report_review_decision_valid": decision_passed,
        "closure_audit_report_review_decision_passed": decision_passed,
        "closure_audit_report_review_decision": "APPROVE_REVIEW_FOR_CLOSURE_REAL_EXECUTION_STILL_BLOCKED" if decision_passed else "FAIL_CLOSED",
        "closure_progression_authorized": closure_progression_authorized,
        "real_execution_authorized": False,
        "decided_task_count": len(DECIDED_TASK_CHAIN),
        "decided_task_chain": DECIDED_TASK_CHAIN,
        "decision_summary": decision_summary,
        "decision_notes": decision_notes,
        "decision_check_count": len(decision_checks),
        "decision_checks": decision_checks,
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
        "audit_report_review_decision_only": True,
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
    record["task_id"] = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-CLOSURE-AUDIT-REPORT-REVIEW-DECISION-" + signature[:12]
    return record


def validate_closure_audit_report_review_decision_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "closure_audit_report_review_decision_ready",
        "closure_audit_report_review_decision_valid",
        "closure_audit_report_review_decision_passed",
        "closure_progression_authorized",
        "source_review_artifact_present",
        "source_review_artifact_parseable",
        "source_review_ready",
        "source_review_valid",
        "source_review_passed",
        "source_review_real_execution_blocked",
        "source_reviewed_task_count_ok",
        "source_review_summary_ok",
        "source_decision_required_next",
        "source_review_checks_consistent",
        "local_only",
        "dry_run_only",
        "diagnostic_only",
        "audit_report_review_decision_only",
        "public_safe",
        "deterministic",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "real_execution_authorized",
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

    if record.get("closure_audit_report_review_decision") != "APPROVE_REVIEW_FOR_CLOSURE_REAL_EXECUTION_STILL_BLOCKED":
        issues.append("CLOSURE_AUDIT_REPORT_REVIEW_DECISION_NOT_APPROVED_OR_BLOCKED")

    if record.get("decided_task_count") != 10:
        issues.append("DECIDED_TASK_COUNT_MISMATCH")

    decision_summary = record.get("decision_summary")
    if not isinstance(decision_summary, dict):
        issues.append("DECISION_SUMMARY_MISSING")
    else:
        if decision_summary.get("closure_progression_authorized") is not True:
            issues.append("DECISION_SUMMARY_CLOSURE_PROGRESSION_NOT_AUTHORIZED")
        if decision_summary.get("real_runtime_wiring") != "BLOCKED":
            issues.append("DECISION_SUMMARY_REAL_RUNTIME_WIRING_NOT_BLOCKED")
        if decision_summary.get("real_runtime_wiring_authorized") is not False:
            issues.append("DECISION_SUMMARY_REAL_RUNTIME_WIRING_AUTHORIZED")
        if decision_summary.get("closure_required_next") is not True:
            issues.append("DECISION_SUMMARY_CLOSURE_REQUIRED_NEXT_NOT_TRUE")

    decision_checks = record.get("decision_checks")
    if not isinstance(decision_checks, list) or not decision_checks:
        issues.append("DECISION_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in decision_checks):
        issues.append("DECISION_CHECK_FAILED")

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

    json_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-v1.json"
    index_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-index-v1.json"
    manifest_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-manifest-v1.txt"
    markdown_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "closure_audit_report_review_decision_ready": record["closure_audit_report_review_decision_ready"],
        "closure_audit_report_review_decision_passed": record["closure_audit_report_review_decision_passed"],
        "closure_audit_report_review_decision": record["closure_audit_report_review_decision"],
        "closure_progression_authorized": record["closure_progression_authorized"],
        "real_execution_authorized": record["real_execution_authorized"],
        "decided_task_count": record["decided_task_count"],
        "source_review_valid": record["source_review_valid"],
        "source_review_passed": record["source_review_passed"],
        "source_review_real_execution_blocked": record["source_review_real_execution_blocked"],
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
        f"closure_audit_report_review_decision_ready={record['closure_audit_report_review_decision_ready']}",
        f"closure_audit_report_review_decision_passed={record['closure_audit_report_review_decision_passed']}",
        f"closure_audit_report_review_decision={record['closure_audit_report_review_decision']}",
        f"closure_progression_authorized={record['closure_progression_authorized']}",
        f"real_execution_authorized={record['real_execution_authorized']}",
        f"decided_task_count={record['decided_task_count']}",
        f"source_review_valid={record['source_review_valid']}",
        f"source_review_passed={record['source_review_passed']}",
        f"source_review_real_execution_blocked={record['source_review_real_execution_blocked']}",
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
- closure_audit_report_review_decision: `{record['closure_audit_report_review_decision']}`
- next_stage: `{record['next_stage']}`

## Decision

The Task 32 review is approved only for closure progression.
This decision does not authorize real controlled runtime wiring.

## Boundary

- closure_progression_authorized: `{record['closure_progression_authorized']}`
- real_execution_authorized: `{record['real_execution_authorized']}`
- local_only: `{record['local_only']}`
- dry_run_only: `{record['dry_run_only']}`
- diagnostic_only: `{record['diagnostic_only']}`
- audit_report_review_decision_only: `{record['audit_report_review_decision_only']}`
- runtime_wiring_performed: `{record['runtime_wiring_performed']}`
- runtime_solver_patch_applied: `{record['runtime_solver_patch_applied']}`
- controlled_runtime_wiring_execution_allowed: `{record['controlled_runtime_wiring_execution_allowed']}`
- controlled_runtime_wiring_authorized: `{record['controlled_runtime_wiring_authorized']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`

## Decision conclusion

`{record['decision_summary']['decision']}`

## Gate status

- decided_task_count: `{record['decided_task_count']}`
- decision_check_count: `{record['decision_check_count']}`
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
    record = build_closure_audit_report_review_decision_record()
    issues = validate_closure_audit_report_review_decision_record(record)
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
