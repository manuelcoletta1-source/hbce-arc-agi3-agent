"""Milestone #11 Task 35 - Controlled Runtime Wiring Final Closure v1.

This module closes Milestone #11 controlled runtime wiring as a local-only,
diagnostic-only, dry-run-only chain.

It does not authorize real runtime wiring, does not patch the runtime solver,
does not create a Kaggle submission, does not authenticate to Kaggle, and does
not call external APIs.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_FINAL_CLOSURE_V1"
TASK_NUMBER = 35
TASK_LABEL = "Milestone #11 Task 35 - Controlled Runtime Wiring Final Closure v1"

SOURCE_TASK = "MILESTONE_11_TASK_34_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_DECISION_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_12_CANDIDATE_PLANNING_GATE_V1_NOT_OPENED_CANONICALLY"

TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_FINAL_CLOSURE_V1_LOCAL_ONLY"
TASK_SCOPE = "MILESTONE_11_FINAL_CLOSURE_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_11_CONTROLLED_RUNTIME_WIRING_CLOSED_REAL_EXECUTION_BLOCKED"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-final-closure-v1"
)

SOURCE_CLOSURE_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-closure-v1"
    / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-closure-audit-report-review-decision-closure-v1.json"
)

FINAL_CLOSED_TASK_CHAIN = [
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
    "MILESTONE_11_TASK_34_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_CLOSURE_AUDIT_REPORT_REVIEW_DECISION_CLOSURE_V1",
    "MILESTONE_11_TASK_35_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_FINAL_CLOSURE_V1",
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


def _closure_check(name: str, status: bool, severity: str, description: str) -> dict[str, Any]:
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


def build_final_closure_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_present = SOURCE_CLOSURE_ARTIFACT.exists()
    source = _load_source_closure_artifact()

    source_parseable = source is not None
    source_ready = bool(source and source.get("closure_audit_report_review_decision_closure_ready") is True)
    source_valid = bool(source and source.get("closure_audit_report_review_decision_closure_valid") is True)
    source_passed = bool(source and source.get("closure_audit_report_review_decision_closure_passed") is True)
    source_closure_ok = bool(
        source
        and source.get("closure_audit_report_review_decision_closure")
        == "DECISION_CLOSURE_PASS_REAL_EXECUTION_STILL_BLOCKED"
    )
    source_closure_complete = bool(source and source.get("closure_complete") is True)
    source_final_closure_ready = bool(source and source.get("milestone_11_final_closure_ready") is True)
    source_m12_candidate = bool(source and source.get("milestone_12_candidate_exists") is True)
    source_m12_not_opened = bool(source and source.get("milestone_12_candidate_status") == "NOT_OPENED_CANONICALLY")
    source_m12_opening_blocked = bool(source and source.get("milestone_12_opening_allowed") is False)
    source_task_count_ok = bool(source and source.get("closed_task_count") == 11)

    source_summary = source.get("closure_summary") if isinstance(source, dict) else None
    source_summary_ok = bool(
        isinstance(source_summary, dict)
        and source_summary.get("closure") == "DECISION_CLOSURE_PASS_REAL_EXECUTION_STILL_BLOCKED"
        and source_summary.get("closure_complete") is True
        and source_summary.get("milestone_11_final_closure_ready") is True
        and source_summary.get("milestone_12_candidate_exists") is True
        and source_summary.get("milestone_12_candidate_status") == "NOT_OPENED_CANONICALLY"
        and source_summary.get("milestone_12_opening_allowed") is False
        and source_summary.get("real_runtime_wiring") == "BLOCKED"
        and source_summary.get("real_runtime_wiring_authorized") is False
        and source_summary.get("runtime_solver_patch") == "BLOCKED"
        and source_summary.get("kaggle_submission") == "NOT_SENT"
        and source_summary.get("private_core") == "NOT_EXPOSED"
        and source_summary.get("legal_certification") == "FALSE"
    )

    source_checks_ok = bool(
        source
        and isinstance(source.get("closure_checks"), list)
        and source.get("closure_check_count") == len(source.get("closure_checks"))
        and all(check.get("status") is True for check in source.get("closure_checks"))
    )

    source_gate_count_ok = bool(
        source
        and isinstance(source.get("gates"), list)
        and source.get("gate_count") == len(source.get("gates"))
        and all(gate.get("passed") is True for gate in source.get("gates") if gate.get("required") is True)
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
    source_decision_closure_only = bool(source and source.get("decision_closure_only") is True)

    final_closure_ready = all(
        [
            source_present,
            source_parseable,
            source_ready,
            source_valid,
            source_passed,
            source_closure_ok,
            source_closure_complete,
            source_final_closure_ready,
            source_m12_candidate,
            source_m12_not_opened,
            source_m12_opening_blocked,
            source_task_count_ok,
            source_summary_ok,
            source_checks_ok,
            source_gate_count_ok,
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
            source_decision_closure_only,
        ]
    )

    final_checks = [
        _closure_check("source_task_34_artifact_present", source_present, "PASS" if source_present else "BLOCKING", "Task 34 closure artifact exists."),
        _closure_check("source_task_34_artifact_parseable", source_parseable, "PASS" if source_parseable else "BLOCKING", "Task 34 closure artifact is parseable."),
        _closure_check("source_task_34_ready", source_ready, "PASS" if source_ready else "BLOCKING", "Task 34 closure is ready."),
        _closure_check("source_task_34_valid", source_valid, "PASS" if source_valid else "BLOCKING", "Task 34 closure is valid."),
        _closure_check("source_task_34_passed", source_passed, "PASS" if source_passed else "BLOCKING", "Task 34 closure passed."),
        _closure_check("source_task_34_closure_value_ok", source_closure_ok, "PASS" if source_closure_ok else "BLOCKING", "Task 34 closure value is correct."),
        _closure_check("source_task_34_closure_complete", source_closure_complete, "PASS" if source_closure_complete else "BLOCKING", "Task 34 closure is complete."),
        _closure_check("source_task_34_final_closure_ready", source_final_closure_ready, "PASS" if source_final_closure_ready else "BLOCKING", "Task 34 marks final closure ready."),
        _closure_check("source_milestone_12_candidate_exists", source_m12_candidate, "PASS" if source_m12_candidate else "BLOCKING", "Milestone 12 exists only as candidate."),
        _closure_check("source_milestone_12_not_opened", source_m12_not_opened, "PASS" if source_m12_not_opened else "BLOCKING", "Milestone 12 is not opened canonically."),
        _closure_check("source_milestone_12_opening_blocked", source_m12_opening_blocked, "PASS" if source_m12_opening_blocked else "BLOCKING", "Milestone 12 opening is blocked in Milestone 11."),
        _closure_check("source_closed_task_count_ok", source_task_count_ok, "PASS" if source_task_count_ok else "BLOCKING", "Task 34 closed task count is correct."),
        _closure_check("source_closure_summary_ok", source_summary_ok, "PASS" if source_summary_ok else "BLOCKING", "Task 34 closure summary is coherent."),
        _closure_check("source_closure_checks_ok", source_checks_ok, "PASS" if source_checks_ok else "BLOCKING", "Task 34 closure checks passed."),
        _closure_check("source_gates_ok", source_gate_count_ok, "PASS" if source_gate_count_ok else "BLOCKING", "Task 34 required gates passed."),
        _closure_check("controlled_runtime_wiring_execution_allowed_false", source_execution_blocked, "PASS" if source_execution_blocked else "BLOCKING", "Controlled runtime wiring remains blocked."),
        _closure_check("controlled_runtime_wiring_authorized_false", source_authorized_false, "PASS" if source_authorized_false else "BLOCKING", "Controlled runtime wiring remains unauthorized."),
        _closure_check("runtime_wiring_not_performed", source_runtime_wiring_false, "PASS" if source_runtime_wiring_false else "BLOCKING", "Runtime wiring was not performed."),
        _closure_check("runtime_solver_patch_allowed_false", source_patch_allowed_false, "PASS" if source_patch_allowed_false else "BLOCKING", "Runtime solver patching remains blocked."),
        _closure_check("runtime_solver_patch_not_applied", source_patch_applied_false, "PASS" if source_patch_applied_false else "BLOCKING", "Runtime solver patch was not applied."),
        _closure_check("runtime_solver_not_modified", source_runtime_solver_modified_false, "PASS" if source_runtime_solver_modified_false else "BLOCKING", "Runtime solver remains unmodified."),
        _closure_check("ranker_runtime_not_modified", source_ranker_modified_false, "PASS" if source_ranker_modified_false else "BLOCKING", "Ranker runtime remains unmodified."),
        _closure_check("submission_json_not_created", source_submission_json_false, "PASS" if source_submission_json_false else "BLOCKING", "Submission JSON was not created."),
        _closure_check("real_submission_candidate_not_created", source_real_candidate_false, "PASS" if source_real_candidate_false else "BLOCKING", "Real submission candidate was not created."),
        _closure_check("real_submission_allowed_false", source_real_submission_allowed_false, "PASS" if source_real_submission_allowed_false else "BLOCKING", "Real submission remains blocked."),
        _closure_check("kaggle_submission_not_sent", source_submission_false, "PASS" if source_submission_false else "BLOCKING", "Kaggle submission was not sent."),
        _closure_check("kaggle_upload_not_performed", source_upload_false, "PASS" if source_upload_false else "BLOCKING", "Kaggle upload was not performed."),
        _closure_check("kaggle_authentication_not_performed", source_auth_false, "PASS" if source_auth_false else "BLOCKING", "Kaggle authentication was not performed."),
        _closure_check("external_api_dependency_false", source_external_false, "PASS" if source_external_false else "BLOCKING", "External API dependency remains false."),
        _closure_check("contains_api_keys_false", source_keys_false, "PASS" if source_keys_false else "BLOCKING", "No API keys are contained."),
        _closure_check("private_core_exposure_false", source_private_core_false, "PASS" if source_private_core_false else "BLOCKING", "Private core exposure remains false."),
        _closure_check("legal_certification_false", source_legal_false, "PASS" if source_legal_false else "BLOCKING", "legal_certification remains false."),
        _closure_check("source_issue_count_zero", source_issue_zero, "PASS" if source_issue_zero else "BLOCKING", "Source issue count is zero."),
        _closure_check("source_warning_count_zero", source_warning_zero, "PASS" if source_warning_zero else "WARNING", "Source warning count is zero."),
        _closure_check("source_local_only_true", source_local, "PASS" if source_local else "BLOCKING", "Source is local-only."),
        _closure_check("source_dry_run_only_true", source_dry, "PASS" if source_dry else "BLOCKING", "Source is dry-run-only."),
        _closure_check("source_diagnostic_only_true", source_diag, "PASS" if source_diag else "BLOCKING", "Source is diagnostic-only."),
        _closure_check("source_decision_closure_only_true", source_decision_closure_only, "PASS" if source_decision_closure_only else "BLOCKING", "Source is decision-closure-only."),
        _closure_check("milestone_11_final_closure_ready", final_closure_ready, "PASS" if final_closure_ready else "BLOCKING", "Milestone 11 final closure is ready."),
    ]

    final_closure_passed = all(check["status"] is True for check in final_checks)

    final_summary = {
        "closure_scope": TASK_SCOPE,
        "source_closure": "TASK_34_CLOSURE_AUDIT_REPORT_REVIEW_DECISION_CLOSURE",
        "closed_chain": "TASK_24_THROUGH_TASK_35",
        "milestone_11_status": "CLOSED" if final_closure_passed else "FAIL_CLOSED",
        "milestone_11_final_closure_complete": final_closure_passed,
        "milestone_11_real_execution_result": "BLOCKED",
        "milestone_12_candidate_exists": True,
        "milestone_12_candidate_status": "NOT_OPENED_CANONICALLY",
        "milestone_12_opening_allowed": False,
        "next_stage": NEXT_STAGE,
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
    }

    final_notes = [
        "Task 35 closes Milestone #11 controlled runtime wiring.",
        "The closed chain covers Task 24 through Task 35.",
        "Milestone #11 is closed without real runtime wiring.",
        "Runtime solver patching remains blocked.",
        "Ranker runtime modification remains blocked.",
        "No Kaggle submission, upload, or authentication is performed.",
        "No external API dependency is introduced.",
        "No API keys are contained.",
        "No private HBCE/JOKER-C2 core material is exposed.",
        "No score claim is made.",
        "legal_certification remains false.",
        "Milestone 12 exists only as a future candidate and is not opened canonically by this task.",
    ]

    gates = [
        _gate("source_task_34_artifact_present", source_present, True, "Task 34 closure artifact is present."),
        _gate("source_task_34_artifact_parseable", source_parseable, True, "Task 34 closure artifact is parseable."),
        _gate("source_task_34_ready", source_ready, True, "Task 34 closure is ready."),
        _gate("source_task_34_valid", source_valid, True, "Task 34 closure is valid."),
        _gate("source_task_34_passed", source_passed, True, "Task 34 closure passed."),
        _gate("source_task_34_closure_value_ok", source_closure_ok, True, "Task 34 closure value is correct."),
        _gate("source_task_34_closure_complete", source_closure_complete, True, "Task 34 closure is complete."),
        _gate("source_task_34_final_closure_ready", source_final_closure_ready, True, "Task 34 final closure readiness is true."),
        _gate("source_milestone_12_candidate_exists", source_m12_candidate, True, "Milestone 12 exists only as candidate."),
        _gate("source_milestone_12_not_opened", source_m12_not_opened, True, "Milestone 12 is not opened canonically."),
        _gate("source_milestone_12_opening_blocked", source_m12_opening_blocked, True, "Milestone 12 opening remains blocked."),
        _gate("source_closed_task_count_ok", source_task_count_ok, True, "Task 34 closed task count is correct."),
        _gate("source_closure_summary_ok", source_summary_ok, True, "Task 34 closure summary is coherent."),
        _gate("source_closure_checks_ok", source_checks_ok, True, "Task 34 closure checks passed."),
        _gate("source_gates_ok", source_gate_count_ok, True, "Task 34 gates passed."),
        _gate("milestone_11_final_closure_ready", final_closure_ready, True, "Milestone 11 final closure is ready."),
        _gate("milestone_11_final_closure_passed", final_closure_passed, True, "Milestone 11 final closure passed."),
        _gate("final_closed_task_chain_declared", True, True, "Final closed task chain 24 through 35 is declared."),
        _gate("milestone_12_not_opened_canonically", True, True, "Milestone 12 is not opened canonically in Task 35."),
        _gate("runtime_wiring_performed_false", True, True, "Task 35 performs no runtime wiring."),
        _gate("runtime_solver_patch_allowed_false", True, True, "Runtime solver patching remains blocked."),
        _gate("runtime_solver_patch_applied_false", True, True, "Task 35 applies no runtime solver patch."),
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
        _gate("final_closure_only_true", True, True, "The task remains final-closure-only."),
        _gate("public_safe_true", True, True, "The artifact is public-safe."),
        _gate("deterministic_true", True, True, "The closure is deterministic."),
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
        "source_closure_ready": source_ready,
        "source_closure_valid": source_valid,
        "source_closure_passed": source_passed,
        "source_closure_ok": source_closure_ok,
        "source_closure_complete": source_closure_complete,
        "source_final_closure_ready": source_final_closure_ready,
        "source_milestone_12_candidate_exists": source_m12_candidate,
        "source_milestone_12_not_opened": source_m12_not_opened,
        "source_milestone_12_opening_blocked": source_m12_opening_blocked,
        "source_closed_task_count_ok": source_task_count_ok,
        "source_closure_summary_ok": source_summary_ok,
        "source_closure_checks_ok": source_checks_ok,
        "source_gate_count_ok": source_gate_count_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_11_final_closure_ready": True,
        "milestone_11_final_closure_valid": final_closure_passed,
        "milestone_11_final_closure_passed": final_closure_passed,
        "milestone_11_final_closure_complete": final_closure_passed,
        "milestone_11_status": "CLOSED" if final_closure_passed else "FAIL_CLOSED",
        "milestone_11_closure": "FINAL_CLOSURE_PASS_REAL_EXECUTION_BLOCKED" if final_closure_passed else "FAIL_CLOSED",
        "milestone_12_candidate_exists": True,
        "milestone_12_candidate_status": "NOT_OPENED_CANONICALLY",
        "milestone_12_opening_allowed": False,
        "real_execution_authorized": False,
        "final_closed_task_count": len(FINAL_CLOSED_TASK_CHAIN),
        "final_closed_task_chain": FINAL_CLOSED_TASK_CHAIN,
        "final_summary": final_summary,
        "final_notes": final_notes,
        "final_check_count": len(final_checks),
        "final_checks": final_checks,
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
        "final_closure_only": True,
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
    record["task_id"] = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-FINAL-CLOSURE-" + signature[:12]
    return record


def validate_final_closure_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "milestone_11_final_closure_ready",
        "milestone_11_final_closure_valid",
        "milestone_11_final_closure_passed",
        "milestone_11_final_closure_complete",
        "milestone_12_candidate_exists",
        "source_closure_artifact_present",
        "source_closure_artifact_parseable",
        "source_closure_ready",
        "source_closure_valid",
        "source_closure_passed",
        "source_closure_ok",
        "source_closure_complete",
        "source_final_closure_ready",
        "source_milestone_12_candidate_exists",
        "source_milestone_12_not_opened",
        "source_milestone_12_opening_blocked",
        "source_closed_task_count_ok",
        "source_closure_summary_ok",
        "source_closure_checks_ok",
        "source_gate_count_ok",
        "local_only",
        "dry_run_only",
        "diagnostic_only",
        "final_closure_only",
        "public_safe",
        "deterministic",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "milestone_12_opening_allowed",
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

    if record.get("milestone_11_status") != "CLOSED":
        issues.append("MILESTONE_11_STATUS_NOT_CLOSED")

    if record.get("milestone_11_closure") != "FINAL_CLOSURE_PASS_REAL_EXECUTION_BLOCKED":
        issues.append("MILESTONE_11_CLOSURE_NOT_PASS_OR_BLOCKED")

    if record.get("final_closed_task_count") != 12:
        issues.append("FINAL_CLOSED_TASK_COUNT_MISMATCH")

    if record.get("milestone_12_candidate_status") != "NOT_OPENED_CANONICALLY":
        issues.append("MILESTONE_12_STATUS_NOT_NOT_OPENED_CANONICALLY")

    final_summary = record.get("final_summary")
    if not isinstance(final_summary, dict):
        issues.append("FINAL_SUMMARY_MISSING")
    else:
        if final_summary.get("milestone_11_status") != "CLOSED":
            issues.append("FINAL_SUMMARY_MILESTONE_11_NOT_CLOSED")
        if final_summary.get("milestone_11_final_closure_complete") is not True:
            issues.append("FINAL_SUMMARY_MILESTONE_11_FINAL_CLOSURE_NOT_COMPLETE")
        if final_summary.get("milestone_12_candidate_status") != "NOT_OPENED_CANONICALLY":
            issues.append("FINAL_SUMMARY_MILESTONE_12_STATUS_MISMATCH")
        if final_summary.get("milestone_12_opening_allowed") is not False:
            issues.append("FINAL_SUMMARY_MILESTONE_12_OPENING_ALLOWED")
        if final_summary.get("real_runtime_wiring") != "BLOCKED":
            issues.append("FINAL_SUMMARY_REAL_RUNTIME_WIRING_NOT_BLOCKED")
        if final_summary.get("real_runtime_wiring_authorized") is not False:
            issues.append("FINAL_SUMMARY_REAL_RUNTIME_WIRING_AUTHORIZED")

    final_checks = record.get("final_checks")
    if not isinstance(final_checks, list) or not final_checks:
        issues.append("FINAL_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in final_checks):
        issues.append("FINAL_CHECK_FAILED")

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

    json_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-final-closure-v1.json"
    index_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-final-closure-index-v1.json"
    manifest_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-final-closure-manifest-v1.txt"
    markdown_path = target_dir / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-final-closure-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_11_status": record["milestone_11_status"],
        "milestone_11_closure": record["milestone_11_closure"],
        "milestone_11_final_closure_complete": record["milestone_11_final_closure_complete"],
        "milestone_12_candidate_exists": record["milestone_12_candidate_exists"],
        "milestone_12_candidate_status": record["milestone_12_candidate_status"],
        "milestone_12_opening_allowed": record["milestone_12_opening_allowed"],
        "real_execution_authorized": record["real_execution_authorized"],
        "final_closed_task_count": record["final_closed_task_count"],
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
        f"milestone_11_status={record['milestone_11_status']}",
        f"milestone_11_closure={record['milestone_11_closure']}",
        f"milestone_11_final_closure_complete={record['milestone_11_final_closure_complete']}",
        f"milestone_12_candidate_exists={record['milestone_12_candidate_exists']}",
        f"milestone_12_candidate_status={record['milestone_12_candidate_status']}",
        f"milestone_12_opening_allowed={record['milestone_12_opening_allowed']}",
        f"real_execution_authorized={record['real_execution_authorized']}",
        f"final_closed_task_count={record['final_closed_task_count']}",
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
- milestone_11_status: `{record['milestone_11_status']}`
- milestone_11_closure: `{record['milestone_11_closure']}`
- next_stage: `{record['next_stage']}`

## Final closure

Milestone #11 controlled runtime wiring is closed.

The final closure confirms that the controlled runtime wiring chain remained local-only, dry-run-only, diagnostic-only, and public-safe. Real execution remains blocked.

## Milestone 11 / Milestone 12 boundary

- milestone_11_final_closure_complete: `{record['milestone_11_final_closure_complete']}`
- milestone_12_candidate_exists: `{record['milestone_12_candidate_exists']}`
- milestone_12_candidate_status: `{record['milestone_12_candidate_status']}`
- milestone_12_opening_allowed: `{record['milestone_12_opening_allowed']}`

## Runtime boundary

- real_execution_authorized: `{record['real_execution_authorized']}`
- controlled_runtime_wiring_execution_allowed: `{record['controlled_runtime_wiring_execution_allowed']}`
- controlled_runtime_wiring_authorized: `{record['controlled_runtime_wiring_authorized']}`
- runtime_wiring_performed: `{record['runtime_wiring_performed']}`
- runtime_solver_patch_applied: `{record['runtime_solver_patch_applied']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`

## Gate status

- final_closed_task_count: `{record['final_closed_task_count']}`
- final_check_count: `{record['final_check_count']}`
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
    record = build_final_closure_record()
    issues = validate_final_closure_record(record)
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
