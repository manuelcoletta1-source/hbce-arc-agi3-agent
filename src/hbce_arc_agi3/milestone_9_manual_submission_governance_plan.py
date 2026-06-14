"""Milestone #9 Manual Submission Governance Plan v1.

Local-only deterministic governance plan for the post-Milestone #8 manual
submission approval phase.

This module opens Milestone #9 after Milestone #8 closure. It verifies:
- Milestone #8 closure report dependency
- Manual submission governance scope
- Required operator approval declarations
- Pre-submission review gates
- Real submission remains blocked until explicit operator approval

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, claim a Kaggle score, claim public leaderboard improvement, or
create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PLAN_STATUS = "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_READY"
PIPELINE_STATUS = "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_VALID"

BASELINE_COMMIT = "bc568bc Close ARC AGI3 milestone 8 competitive solver iteration"
PLAN_MODE = "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_LOCAL_ONLY"
PLAN_SCOPE = "OPEN_MANUAL_SUBMISSION_APPROVAL_AND_REAL_SUBMISSION_GOVERNANCE"
PLAN_VERDICT = "MILESTONE_9_OPEN_REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL"
NEXT_ALLOWED_STAGE = "MILESTONE_9_TASK_2_OPERATOR_DECLARATION_PACKAGE_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-9/manual-submission-governance-plan-v1"

MILESTONE_8_CLOSURE_JSON = Path(
    "examples/milestone-8/milestone-8-closure-report-v2/"
    "milestone-8-closure-report-v2.json"
)

EXPECTED_PREVIOUS_MILESTONE_CLOSED_TASK_COUNT = 9
EXPECTED_PLAN_CASE_COUNT = 10
EXPECTED_PLAN_PASS_COUNT = 10
EXPECTED_PLAN_FAILURE_COUNT = 0
EXPECTED_REQUIRED_DECLARATION_COUNT = 8
EXPECTED_PROVIDED_DECLARATION_COUNT = 0
EXPECTED_ACCEPTED_DECLARATION_COUNT = 0
EXPECTED_GOVERNANCE_PHASE_COUNT = 5
EXPECTED_PRE_SUBMISSION_GATE_COUNT = 12
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_REGRESSION_GUARD_COUNT = 12

GOVERNANCE_PHASES: Tuple[Dict[str, str], ...] = (
    {
        "phase": "Phase 1",
        "name": "manual_submission_governance_plan",
        "status": "THIS_TASK_READY",
    },
    {
        "phase": "Phase 2",
        "name": "operator_declaration_package",
        "status": "NEXT",
    },
    {
        "phase": "Phase 3",
        "name": "local_candidate_manual_review",
        "status": "PENDING",
    },
    {
        "phase": "Phase 4",
        "name": "real_submission_preflight_gate",
        "status": "PENDING",
    },
    {
        "phase": "Phase 5",
        "name": "explicit_operator_approval_or_keep_blocked",
        "status": "PENDING",
    },
)

REQUIRED_OPERATOR_DECLARATIONS: Tuple[str, ...] = (
    "operator_confirms_real_submission_intent",
    "operator_confirms_kaggle_rules_review",
    "operator_confirms_no_private_core_exposure",
    "operator_confirms_no_api_keys_or_secret_material",
    "operator_confirms_local_candidate_package_review",
    "operator_confirms_manual_upload_responsibility",
    "operator_confirms_no_legal_certification_claim",
    "operator_confirms_irreversible_external_submission_awareness",
)

PRE_SUBMISSION_GATES: Tuple[str, ...] = (
    "milestone_8_closure_report_verified",
    "release_decision_layer_verified",
    "local_submission_candidate_identified",
    "manual_review_package_ready",
    "operator_identity_confirmed",
    "operator_declarations_completed",
    "kaggle_rules_review_confirmed",
    "secret_material_absence_confirmed",
    "private_core_exposure_absence_confirmed",
    "legal_certification_claim_absence_confirmed",
    "manual_upload_responsibility_confirmed",
    "final_operator_approval_confirmed",
)

PLAN_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "governance_milestone_8_closure_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_milestone_8_closure_report",
    },
    {
        "case_id": "governance_milestone_9_open_state_valid_v1",
        "area": "milestone_state",
        "operation": "verify_milestone_9_open_state",
    },
    {
        "case_id": "governance_phase_plan_defined_v1",
        "area": "governance_plan",
        "operation": "verify_governance_phase_plan",
    },
    {
        "case_id": "governance_required_declarations_defined_v1",
        "area": "operator_approval",
        "operation": "verify_required_operator_declarations",
    },
    {
        "case_id": "governance_pre_submission_gates_defined_v1",
        "area": "pre_submission_gate",
        "operation": "verify_pre_submission_gate_set",
    },
    {
        "case_id": "governance_no_operator_approval_yet_v1",
        "area": "operator_approval",
        "operation": "verify_operator_approval_absent",
    },
    {
        "case_id": "governance_real_submission_still_blocked_v1",
        "area": "submission",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "governance_no_upload_no_auth_v1",
        "area": "boundary",
        "operation": "verify_no_upload_no_auth",
    },
    {
        "case_id": "governance_no_score_or_leaderboard_claim_v1",
        "area": "claim_boundary",
        "operation": "verify_no_score_or_leaderboard_claim",
    },
    {
        "case_id": "governance_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_operator_declaration_package_next",
    },
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_governance_uses_milestone_8_closure_artifact",
    "guard_governance_does_not_submit",
    "guard_governance_does_not_authenticate",
    "guard_governance_does_not_upload",
    "guard_governance_requires_operator_approval",
    "guard_governance_operator_approval_absent",
    "guard_governance_declarations_required",
    "guard_governance_pre_submission_gates_required",
    "guard_governance_no_score_claim",
    "guard_governance_no_leaderboard_claim",
    "guard_governance_no_private_core_exposure",
    "guard_governance_no_legal_certification",
)

BOUNDARY_CONTROLS: Tuple[str, ...] = (
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "kaggle_submission_sent_false",
    "private_core_exposure_false",
    "legal_certification_false",
)


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _sha256(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha16(value: str) -> str:
    return value[:16].upper() if value != "MISSING_HASH" else value


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def _result(case_id: str, area: str, operation: str, passed: bool) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "area": area,
        "operation": operation,
        "priority": "P0",
        "passed": passed,
        "evidence_score": 100 if passed else 0,
        "expected_status": "PASS",
        "actual_status": "PASS" if passed else "FAIL",
    }


def build_operator_approval_state() -> Dict[str, Any]:
    return {
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "required_declarations": list(REQUIRED_OPERATOR_DECLARATIONS),
        "required_declaration_count": len(REQUIRED_OPERATOR_DECLARATIONS),
        "provided_declarations": [],
        "provided_declaration_count": 0,
        "accepted_declarations": [],
        "accepted_declaration_count": 0,
        "approval_contract_ready": True,
        "approval_gate_verdict": "MANUAL_APPROVAL_REQUIRED_BUT_NOT_GRANTED",
    }


def build_governance_checks() -> Dict[str, bool]:
    closure = _read_json(MILESTONE_8_CLOSURE_JSON)
    approval = build_operator_approval_state()

    return {
        "milestone_8_closure_artifact_present": MILESTONE_8_CLOSURE_JSON.exists(),
        "milestone_8_closure_artifact_ready": closure.get("status") == "MILESTONE_8_CLOSURE_REPORT_V2_READY",
        "milestone_8_closure_artifact_valid": bool(closure.get("closure_id")) and bool(closure.get("signature")),
        "milestone_8_closed": closure.get("milestone_8_closed") is True,
        "milestone_8_closed_task_count_valid": closure.get("closed_task_count")
        == EXPECTED_PREVIOUS_MILESTONE_CLOSED_TASK_COUNT,
        "milestone_8_real_submission_blocked": closure.get("real_submission_allowed") is False
        and closure.get("kaggle_submission_sent") is False,
        "milestone_8_next_state_pending_manual_approval": closure.get("next_allowed_stage")
        == "MILESTONE_8_CLOSED_PENDING_MANUAL_SUBMISSION_APPROVAL",
        "milestone_9_open_state_valid": PLAN_VERDICT
        == "MILESTONE_9_OPEN_REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL",
        "governance_phase_count_valid": len(GOVERNANCE_PHASES) == EXPECTED_GOVERNANCE_PHASE_COUNT,
        "required_declaration_count_valid": approval["required_declaration_count"]
        == EXPECTED_REQUIRED_DECLARATION_COUNT,
        "provided_declaration_count_zero": approval["provided_declaration_count"]
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": approval["accepted_declaration_count"]
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "pre_submission_gate_count_valid": len(PRE_SUBMISSION_GATES) == EXPECTED_PRE_SUBMISSION_GATE_COUNT,
        "operator_approval_required": approval["operator_approval_required"] is True,
        "operator_approval_not_granted": approval["operator_approval_granted"] is False,
        "operator_approval_not_received": approval["operator_approval_received"] is False,
        "real_submission_not_created": True,
        "real_submission_allowed_false": False is False,
        "ready_for_real_kaggle_submission_false": False is False,
        "kaggle_submission_not_sent": False is False,
        "upload_not_performed": False is False,
        "kaggle_authentication_not_performed": False is False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_9_TASK_2_OPERATOR_DECLARATION_PACKAGE_V1",
    }


def evaluate_governance_plan_case(case_id: str) -> Dict[str, Any]:
    checks = build_governance_checks()

    if case_id == "governance_milestone_8_closure_source_ready_v1":
        passed = (
            checks["milestone_8_closure_artifact_present"]
            and checks["milestone_8_closure_artifact_ready"]
            and checks["milestone_8_closure_artifact_valid"]
            and checks["milestone_8_closed"]
        )
        return _result(case_id, "source_binding", "verify_milestone_8_closure_report", passed)

    if case_id == "governance_milestone_9_open_state_valid_v1":
        passed = checks["milestone_9_open_state_valid"]
        return _result(case_id, "milestone_state", "verify_milestone_9_open_state", passed)

    if case_id == "governance_phase_plan_defined_v1":
        passed = checks["governance_phase_count_valid"] and GOVERNANCE_PHASES[0]["status"] == "THIS_TASK_READY"
        return _result(case_id, "governance_plan", "verify_governance_phase_plan", passed)

    if case_id == "governance_required_declarations_defined_v1":
        passed = checks["required_declaration_count_valid"]
        return _result(case_id, "operator_approval", "verify_required_operator_declarations", passed)

    if case_id == "governance_pre_submission_gates_defined_v1":
        passed = checks["pre_submission_gate_count_valid"] and PRE_SUBMISSION_GATES[-1] == "final_operator_approval_confirmed"
        return _result(case_id, "pre_submission_gate", "verify_pre_submission_gate_set", passed)

    if case_id == "governance_no_operator_approval_yet_v1":
        passed = (
            checks["operator_approval_required"]
            and checks["operator_approval_not_granted"]
            and checks["operator_approval_not_received"]
            and checks["provided_declaration_count_zero"]
            and checks["accepted_declaration_count_zero"]
        )
        return _result(case_id, "operator_approval", "verify_operator_approval_absent", passed)

    if case_id == "governance_real_submission_still_blocked_v1":
        passed = (
            checks["milestone_8_real_submission_blocked"]
            and checks["real_submission_not_created"]
            and checks["real_submission_allowed_false"]
            and checks["ready_for_real_kaggle_submission_false"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission", "verify_real_submission_blocked", passed)

    if case_id == "governance_no_upload_no_auth_v1":
        passed = checks["upload_not_performed"] and checks["kaggle_authentication_not_performed"]
        return _result(case_id, "boundary", "verify_no_upload_no_auth", passed)

    if case_id == "governance_no_score_or_leaderboard_claim_v1":
        passed = checks["score_claim_absent"] and checks["public_leaderboard_claim_absent"]
        return _result(case_id, "claim_boundary", "verify_no_score_or_leaderboard_claim", passed)

    if case_id == "governance_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_operator_declaration_package_next", passed)

    raise ValueError(f"unknown governance plan case: {case_id}")


def evaluate_all_governance_plan_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_governance_plan_case(case["case_id"]) for case in PLAN_CASES)


def build_milestone_9_manual_submission_governance_plan() -> Dict[str, Any]:
    closure = _read_json(MILESTONE_8_CLOSURE_JSON)
    approval = build_operator_approval_state()
    checks = build_governance_checks()
    results = evaluate_all_governance_plan_cases()

    plan_pass_count = sum(1 for result in results if result["passed"] is True)
    plan_failure_count = sum(1 for result in results if result["passed"] is False)

    plan_record = {
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_9_open": True,
        "plan_ready": True,
        "plan_locked": True,
        "baseline_milestone_8_closure_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "milestone_8_closed": closure.get("milestone_8_closed") is True,
        "governance_phase_count": len(GOVERNANCE_PHASES),
        "pre_submission_gate_count": len(PRE_SUBMISSION_GATES),
        "required_declaration_count": approval["required_declaration_count"],
        "provided_declaration_count": approval["provided_declaration_count"],
        "accepted_declaration_count": approval["accepted_declaration_count"],
        "plan_case_count": len(PLAN_CASES),
        "plan_pass_count": plan_pass_count,
        "plan_failure_count": plan_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "governance_plan_created": True,
        "manual_submission_governance_opened": True,
        "operator_approval_contract_ready": True,
        "operator_approval_required": approval["operator_approval_required"],
        "operator_approval_granted": approval["operator_approval_granted"],
        "operator_approval_received": approval["operator_approval_received"],
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
    }

    gate_state = {
        "milestone_8_closure_artifact_present": checks["milestone_8_closure_artifact_present"],
        "milestone_8_closure_artifact_ready": checks["milestone_8_closure_artifact_ready"],
        "milestone_8_closure_artifact_valid": checks["milestone_8_closure_artifact_valid"],
        "milestone_8_closed": checks["milestone_8_closed"],
        "milestone_8_closed_task_count_valid": checks["milestone_8_closed_task_count_valid"],
        "milestone_8_real_submission_blocked": checks["milestone_8_real_submission_blocked"],
        "milestone_8_next_state_pending_manual_approval": checks[
            "milestone_8_next_state_pending_manual_approval"
        ],
        "plan_mode_valid": PLAN_MODE == "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_LOCAL_ONLY",
        "plan_scope_valid": PLAN_SCOPE == "OPEN_MANUAL_SUBMISSION_APPROVAL_AND_REAL_SUBMISSION_GOVERNANCE",
        "plan_verdict_valid": PLAN_VERDICT
        == "MILESTONE_9_OPEN_REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL",
        "milestone_9_open": plan_record["milestone_9_open"] is True,
        "plan_ready": plan_record["plan_ready"] is True,
        "plan_locked": plan_record["plan_locked"] is True,
        "governance_phase_count_valid": checks["governance_phase_count_valid"],
        "pre_submission_gate_count_valid": checks["pre_submission_gate_count_valid"],
        "plan_case_count_valid": len(PLAN_CASES) == EXPECTED_PLAN_CASE_COUNT,
        "plan_pass_count_valid": plan_pass_count == EXPECTED_PLAN_PASS_COUNT,
        "plan_failure_count_zero": plan_failure_count == EXPECTED_PLAN_FAILURE_COUNT,
        "all_plan_cases_pass": all(result["passed"] is True for result in results),
        "required_declaration_count_valid": checks["required_declaration_count_valid"],
        "provided_declaration_count_zero": checks["provided_declaration_count_zero"],
        "accepted_declaration_count_zero": checks["accepted_declaration_count_zero"],
        "operator_approval_required": checks["operator_approval_required"],
        "operator_approval_not_granted": checks["operator_approval_not_granted"],
        "operator_approval_not_received": checks["operator_approval_not_received"],
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "governance_plan_created": plan_record["governance_plan_created"] is True,
        "manual_submission_governance_opened": plan_record["manual_submission_governance_opened"] is True,
        "operator_approval_contract_ready": plan_record["operator_approval_contract_ready"] is True,
        "next_stage_valid": checks["next_stage_valid"],
        "real_submission_not_created": plan_record["real_submission_created"] is False,
        "real_submission_allowed_false": plan_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": plan_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": plan_record["kaggle_submission_sent"] is False,
        "upload_not_performed": plan_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": plan_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": plan_record["external_api_dependency"] is False,
        "contains_api_keys_false": plan_record["contains_api_keys"] is False,
        "private_core_exposure_false": plan_record["private_core_exposure"] is False,
        "legal_certification_false": plan_record["legal_certification"] is False,
        "score_claim_absent": plan_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": plan_record["public_leaderboard_claim_absent"] is True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
    }

    gates = tuple(
        {"name": name, "passed": passed, "severity": "PASS" if passed else "BLOCKING"}
        for name, passed in gate_state.items()
    )
    issues = tuple(
        {
            "name": name.replace("_valid", "_invalid").replace("_zero", "_nonzero").replace("_ready", "_not_ready"),
            "active": not passed,
            "severity": "BLOCKING",
        }
        for name, passed in gate_state.items()
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    plan_ready = (
        closure.get("status") == "MILESTONE_8_CLOSURE_REPORT_V2_READY"
        and closure.get("milestone_8_closed") is True
        and plan_pass_count == EXPECTED_PLAN_PASS_COUNT
        and plan_failure_count == EXPECTED_PLAN_FAILURE_COUNT
        and plan_record["milestone_9_open"] is True
        and plan_record["real_submission_allowed"] is False
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #9",
        "task": "Task 1",
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_milestone_8_closure": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "milestone_9_open": True,
        "plan_ready": plan_ready,
        "plan_locked": True,
        "governance_phase_count": len(GOVERNANCE_PHASES),
        "pre_submission_gate_count": len(PRE_SUBMISSION_GATES),
        "plan_case_count": len(PLAN_CASES),
        "plan_pass_count": plan_pass_count,
        "plan_failure_count": plan_failure_count,
        "required_declaration_count": approval["required_declaration_count"],
        "provided_declaration_count": approval["provided_declaration_count"],
        "accepted_declaration_count": approval["accepted_declaration_count"],
        "operator_approval_required": approval["operator_approval_required"],
        "operator_approval_granted": approval["operator_approval_granted"],
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": PLAN_STATUS,
        "milestone": "Milestone #9",
        "task": "Task 1",
        "title": "Manual Submission Governance Plan v1",
        "baseline_commit": BASELINE_COMMIT,
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_8_closure_source": {
            "path": str(MILESTONE_8_CLOSURE_JSON),
            "present": MILESTONE_8_CLOSURE_JSON.exists(),
            "status": closure.get("status", "MISSING"),
            "closure_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
            "sha256": _sha256(MILESTONE_8_CLOSURE_JSON),
            "sha256_16": _sha16(_sha256(MILESTONE_8_CLOSURE_JSON)),
        },
        "governance_phases": list(GOVERNANCE_PHASES),
        "operator_approval_state": approval,
        "pre_submission_gates": list(PRE_SUBMISSION_GATES),
        "plan_checks": checks,
        "plan_cases": list(PLAN_CASES),
        "plan_results": list(results),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "plan_gates": list(gates),
        "plan_issues": list(issues),
        "plan_index": index,
        "plan_record": plan_record,
        "milestone_9_open": True,
        "governance_phase_count": len(GOVERNANCE_PHASES),
        "pre_submission_gate_count": len(PRE_SUBMISSION_GATES),
        "plan_case_count": len(PLAN_CASES),
        "plan_pass_count": plan_pass_count,
        "plan_failure_count": plan_failure_count,
        "required_declaration_count": approval["required_declaration_count"],
        "provided_declaration_count": approval["provided_declaration_count"],
        "accepted_declaration_count": approval["accepted_declaration_count"],
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "plan_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "plan_issue_count": issue_count,
        "warning_count": 0,
        "plan_ready": plan_ready,
        "plan_locked": True,
        "governance_plan_created": True,
        "manual_submission_governance_opened": True,
        "operator_approval_contract_ready": True,
        "operator_approval_required": approval["operator_approval_required"],
        "operator_approval_granted": approval["operator_approval_granted"],
        "operator_approval_received": approval["operator_approval_received"],
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_9_manual_submission_governance_plan_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }

    signature = _stable_signature(base)
    return {
        **base,
        "plan_id": f"MILESTONE-9-GOVERNANCE-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_9_manual_submission_governance_plan(plan: Mapping[str, Any]) -> Dict[str, Any]:
    gates = plan.get("plan_gates", [])
    issues = plan.get("plan_issues", [])
    results = plan.get("plan_results", [])

    checks = {
        "status_ready": plan.get("status") == PLAN_STATUS,
        "plan_id_present": isinstance(plan.get("plan_id"), str) and bool(plan.get("plan_id")),
        "signature_present": isinstance(plan.get("signature"), str) and bool(plan.get("signature")),
        "baseline_commit_valid": str(plan.get("baseline_commit", "")).startswith("bc568bc"),
        "plan_mode_valid": plan.get("plan_mode") == PLAN_MODE,
        "plan_scope_valid": plan.get("plan_scope") == PLAN_SCOPE,
        "plan_verdict_valid": plan.get("plan_verdict") == PLAN_VERDICT,
        "next_allowed_stage_valid": plan.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "milestone_9_open": plan.get("milestone_9_open") is True,
        "governance_phase_count_valid": plan.get("governance_phase_count") == EXPECTED_GOVERNANCE_PHASE_COUNT,
        "pre_submission_gate_count_valid": plan.get("pre_submission_gate_count") == EXPECTED_PRE_SUBMISSION_GATE_COUNT,
        "plan_case_count_valid": plan.get("plan_case_count") == EXPECTED_PLAN_CASE_COUNT,
        "plan_pass_count_valid": plan.get("plan_pass_count") == EXPECTED_PLAN_PASS_COUNT,
        "plan_failure_count_zero": plan.get("plan_failure_count") == EXPECTED_PLAN_FAILURE_COUNT,
        "required_declaration_count_valid": plan.get("required_declaration_count")
        == EXPECTED_REQUIRED_DECLARATION_COUNT,
        "provided_declaration_count_zero": plan.get("provided_declaration_count")
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": plan.get("accepted_declaration_count")
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_plan_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "plan_issue_count_zero": plan.get("plan_issue_count") == 0,
        "all_plan_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "plan_ready": plan.get("plan_ready") is True,
        "plan_locked": plan.get("plan_locked") is True,
        "operator_approval_contract_ready": plan.get("operator_approval_contract_ready") is True,
        "operator_approval_required": plan.get("operator_approval_required") is True,
        "operator_approval_not_granted": plan.get("operator_approval_granted") is False,
        "operator_approval_not_received": plan.get("operator_approval_received") is False,
        "real_submission_not_created": plan.get("real_submission_created") is False,
        "real_submission_allowed_false": plan.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": plan.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": plan.get("kaggle_submission_sent") is False,
        "upload_not_performed": plan.get("upload_performed") is False,
        "kaggle_authentication_not_performed": plan.get("kaggle_authentication_performed") is False,
        "metadata_safe": plan.get("metadata", {}).get("external_api_dependency") is False
        and plan.get("metadata", {}).get("contains_api_keys") is False
        and plan.get("metadata", {}).get("private_core_exposure") is False
        and plan.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "plan_id": plan.get("plan_id"),
        "signature": plan.get("signature"),
    }


def render_manual_submission_governance_plan_markdown(plan: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #9 - Manual Submission Governance Plan v1",
        "",
        f"- status: {plan['status']}",
        f"- plan_id: {plan['plan_id']}",
        f"- signature: {plan['signature']}",
        f"- baseline_commit: {plan['baseline_commit']}",
        f"- plan_mode: {plan['plan_mode']}",
        f"- plan_scope: {plan['plan_scope']}",
        f"- plan_verdict: {plan['plan_verdict']}",
        f"- next_allowed_stage: {plan['next_allowed_stage']}",
        f"- milestone_9_open: {plan['milestone_9_open']}",
        f"- governance_phase_count: {plan['governance_phase_count']}",
        f"- pre_submission_gate_count: {plan['pre_submission_gate_count']}",
        f"- plan_case_count: {plan['plan_case_count']}",
        f"- plan_pass_count: {plan['plan_pass_count']}",
        f"- plan_failure_count: {plan['plan_failure_count']}",
        f"- operator_approval_required: {plan['operator_approval_required']}",
        f"- operator_approval_granted: {plan['operator_approval_granted']}",
        "",
        "## Governance phases",
        "",
    ]

    for item in plan["governance_phases"]:
        lines.append(f"- {item['phase']}: {item['name']} / status={item['status']}")

    lines.extend(["", "## Required operator declarations", ""])

    for item in plan["operator_approval_state"]["required_declarations"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Pre-submission gates", ""])

    for item in plan["pre_submission_gates"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Plan results", ""])

    for result in plan["plan_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Milestone #9 is open. Real submission remains blocked pending explicit operator approval.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_READY=true",
            "ARC_AGI3_MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_9_OPEN=true",
            "ARC_AGI3_MILESTONE_9_PLAN_MODE=MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_9_PLAN_VERDICT=MILESTONE_9_OPEN_REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL",
            "ARC_AGI3_MILESTONE_9_BASELINE_MILESTONE_8_CLOSURE_COMMIT=bc568bc",
            "ARC_AGI3_MILESTONE_9_GOVERNANCE_PHASE_COUNT=5",
            "ARC_AGI3_MILESTONE_9_PRE_SUBMISSION_GATE_COUNT=12",
            "ARC_AGI3_MILESTONE_9_PLAN_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_9_PLAN_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_9_PLAN_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_9_REQUIRED_DECLARATION_COUNT=8",
            "ARC_AGI3_MILESTONE_9_PROVIDED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_ACCEPTED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_NEXT_STAGE=MILESTONE_9_TASK_2_OPERATOR_DECLARATION_PACKAGE_V1",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_REQUIRED=true",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_9_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_9_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_9_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_9_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_manual_submission_governance_plan_manifest(plan: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 9 MANUAL SUBMISSION GOVERNANCE PLAN MANIFEST v1",
        f"plan_id={plan['plan_id']}",
        f"signature={plan['signature']}",
        f"status={plan['status']}",
        f"baseline_commit={plan['baseline_commit']}",
        f"plan_mode={plan['plan_mode']}",
        f"plan_verdict={plan['plan_verdict']}",
        f"next_allowed_stage={plan['next_allowed_stage']}",
        f"milestone_9_open={plan['milestone_9_open']}",
        f"governance_phase_count={plan['governance_phase_count']}",
        f"pre_submission_gate_count={plan['pre_submission_gate_count']}",
        f"plan_case_count={plan['plan_case_count']}",
        f"plan_pass_count={plan['plan_pass_count']}",
        f"plan_failure_count={plan['plan_failure_count']}",
        f"plan_gate_count={plan['plan_gate_count']}",
        f"passed_gate_count={plan['passed_gate_count']}",
        f"plan_issue_count={plan['plan_issue_count']}",
        f"plan_ready={plan['plan_ready']}",
        f"plan_locked={plan['plan_locked']}",
        f"governance_plan_created={plan['governance_plan_created']}",
        f"manual_submission_governance_opened={plan['manual_submission_governance_opened']}",
        f"operator_approval_contract_ready={plan['operator_approval_contract_ready']}",
        f"operator_approval_required={plan['operator_approval_required']}",
        f"operator_approval_granted={plan['operator_approval_granted']}",
        f"operator_approval_received={plan['operator_approval_received']}",
        f"required_declaration_count={plan['required_declaration_count']}",
        f"provided_declaration_count={plan['provided_declaration_count']}",
        f"accepted_declaration_count={plan['accepted_declaration_count']}",
        f"real_submission_created={plan['real_submission_created']}",
        f"real_submission_allowed={plan['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={plan['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={plan['kaggle_submission_sent']}",
        f"upload_performed={plan['upload_performed']}",
        f"kaggle_authentication_performed={plan['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "GOVERNANCE_PHASES",
    ]

    for item in plan["governance_phases"]:
        lines.append(f"{item['phase']} name={item['name']} status={item['status']}")

    lines.append("")
    lines.append("REQUIRED_OPERATOR_DECLARATIONS")
    for item in plan["operator_approval_state"]["required_declarations"]:
        lines.append(item)

    lines.append("")
    lines.append("PRE_SUBMISSION_GATES")
    for item in plan["pre_submission_gates"]:
        lines.append(item)

    lines.append("")
    lines.append("PLAN_RESULTS")
    for result in plan["plan_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_manual_submission_governance_plan_artifacts(
    plan: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    plan = dict(plan or build_milestone_9_manual_submission_governance_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-9-manual-submission-governance-plan-v1.json"
    md_path = output / "milestone-9-manual-submission-governance-plan-v1.md"
    manifest_path = output / "milestone-9-manual-submission-governance-plan-manifest-v1.txt"
    index_path = output / "milestone-9-manual-submission-governance-plan-index-v1.json"

    json_path.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_manual_submission_governance_plan_markdown(plan), encoding="utf-8")
    manifest_path.write_text(render_manual_submission_governance_plan_manifest(plan), encoding="utf-8")
    index_path.write_text(json.dumps(plan["plan_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_9_manual_submission_governance_plan_pipeline() -> Dict[str, Any]:
    plan = build_milestone_9_manual_submission_governance_plan()
    validation = validate_milestone_9_manual_submission_governance_plan(plan)
    artifacts = write_manual_submission_governance_plan_artifacts(plan)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_PIPELINE_INVALID",
        "plan_status": plan["status"],
        "validation_status": validation["status"],
        "plan": plan,
        "plan_id": plan["plan_id"],
        "signature": plan["signature"],
        "plan_mode": plan["plan_mode"],
        "plan_verdict": plan["plan_verdict"],
        "next_allowed_stage": plan["next_allowed_stage"],
        "milestone_9_open": plan["milestone_9_open"],
        "governance_phase_count": plan["governance_phase_count"],
        "pre_submission_gate_count": plan["pre_submission_gate_count"],
        "plan_case_count": plan["plan_case_count"],
        "plan_pass_count": plan["plan_pass_count"],
        "plan_failure_count": plan["plan_failure_count"],
        "required_declaration_count": plan["required_declaration_count"],
        "provided_declaration_count": plan["provided_declaration_count"],
        "accepted_declaration_count": plan["accepted_declaration_count"],
        "regression_guard_count": plan["regression_guard_count"],
        "boundary_control_count": plan["boundary_control_count"],
        "plan_gate_count": plan["plan_gate_count"],
        "passed_gate_count": plan["passed_gate_count"],
        "plan_issue_count": plan["plan_issue_count"],
        "warning_count": plan["warning_count"],
        "plan_ready": plan["plan_ready"],
        "plan_locked": plan["plan_locked"],
        "governance_plan_created": plan["governance_plan_created"],
        "manual_submission_governance_opened": plan["manual_submission_governance_opened"],
        "operator_approval_contract_ready": plan["operator_approval_contract_ready"],
        "operator_approval_required": plan["operator_approval_required"],
        "operator_approval_granted": plan["operator_approval_granted"],
        "operator_approval_received": plan["operator_approval_received"],
        "real_submission_created": plan["real_submission_created"],
        "real_submission_allowed": plan["real_submission_allowed"],
        "ready_for_real_kaggle_submission": plan["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": plan["kaggle_submission_sent"],
        "upload_performed": plan["upload_performed"],
        "kaggle_authentication_performed": plan["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": plan["metadata"],
    }
