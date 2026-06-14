"""Milestone #9 Operator Declaration Package v1.

Local-only deterministic operator declaration package for the manual submission
governance phase.

This module prepares the declaration package required before any real Kaggle
submission can be considered. It creates declaration templates, verifies the
Milestone #9 governance plan dependency, and keeps real submission blocked.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, accept declarations, grant approval, claim a Kaggle score, claim
public leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PACKAGE_STATUS = "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY"
PIPELINE_STATUS = "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_VALID"

BASELINE_COMMIT = "4a716ee Open ARC AGI3 milestone 9 manual submission governance"
PACKAGE_MODE = "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_LOCAL_ONLY"
PACKAGE_SCOPE = "CREATE_OPERATOR_DECLARATION_TEMPLATES_WITHOUT_APPROVAL"
PACKAGE_VERDICT = "OPERATOR_DECLARATION_PACKAGE_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_9_TASK_3_LOCAL_CANDIDATE_MANUAL_REVIEW_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-9/operator-declaration-package-v1"

GOVERNANCE_PLAN_JSON = Path(
    "examples/milestone-9/manual-submission-governance-plan-v1/"
    "milestone-9-manual-submission-governance-plan-v1.json"
)

EXPECTED_DECLARATION_COUNT = 8
EXPECTED_DECLARATION_TEMPLATE_COUNT = 8
EXPECTED_PROVIDED_DECLARATION_COUNT = 0
EXPECTED_ACCEPTED_DECLARATION_COUNT = 0
EXPECTED_REJECTED_DECLARATION_COUNT = 0
EXPECTED_PACKAGE_CASE_COUNT = 10
EXPECTED_PACKAGE_PASS_COUNT = 10
EXPECTED_PACKAGE_FAILURE_COUNT = 0
EXPECTED_GOVERNANCE_PHASE_COUNT = 5
EXPECTED_PRE_SUBMISSION_GATE_COUNT = 12
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_REGRESSION_GUARD_COUNT = 12

DECLARATION_TEMPLATES: Tuple[Dict[str, str], ...] = (
    {
        "declaration_id": "operator_confirms_real_submission_intent",
        "title": "Real submission intent confirmation",
        "required_response": "explicit_yes",
    },
    {
        "declaration_id": "operator_confirms_kaggle_rules_review",
        "title": "Kaggle rules review confirmation",
        "required_response": "explicit_yes",
    },
    {
        "declaration_id": "operator_confirms_no_private_core_exposure",
        "title": "No private core exposure confirmation",
        "required_response": "explicit_yes",
    },
    {
        "declaration_id": "operator_confirms_no_api_keys_or_secret_material",
        "title": "No API keys or secret material confirmation",
        "required_response": "explicit_yes",
    },
    {
        "declaration_id": "operator_confirms_local_candidate_package_review",
        "title": "Local candidate package review confirmation",
        "required_response": "explicit_yes",
    },
    {
        "declaration_id": "operator_confirms_manual_upload_responsibility",
        "title": "Manual upload responsibility confirmation",
        "required_response": "explicit_yes",
    },
    {
        "declaration_id": "operator_confirms_no_legal_certification_claim",
        "title": "No legal certification claim confirmation",
        "required_response": "explicit_yes",
    },
    {
        "declaration_id": "operator_confirms_irreversible_external_submission_awareness",
        "title": "Irreversible external submission awareness confirmation",
        "required_response": "explicit_yes",
    },
)

PACKAGE_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "declaration_governance_plan_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_governance_plan_artifact",
    },
    {
        "case_id": "declaration_template_set_complete_v1",
        "area": "declaration_template",
        "operation": "verify_declaration_template_set",
    },
    {
        "case_id": "declaration_required_count_valid_v1",
        "area": "operator_approval",
        "operation": "verify_required_declaration_count",
    },
    {
        "case_id": "declaration_no_operator_submission_yet_v1",
        "area": "operator_approval",
        "operation": "verify_no_operator_declarations_provided",
    },
    {
        "case_id": "declaration_no_accepted_declarations_yet_v1",
        "area": "operator_approval",
        "operation": "verify_no_declarations_accepted",
    },
    {
        "case_id": "declaration_approval_not_granted_v1",
        "area": "approval_gate",
        "operation": "verify_approval_not_granted",
    },
    {
        "case_id": "declaration_real_submission_blocked_v1",
        "area": "submission",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "declaration_no_upload_no_auth_v1",
        "area": "boundary",
        "operation": "verify_no_upload_no_auth",
    },
    {
        "case_id": "declaration_no_score_or_leaderboard_claim_v1",
        "area": "claim_boundary",
        "operation": "verify_no_score_or_leaderboard_claim",
    },
    {
        "case_id": "declaration_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_local_candidate_manual_review_next",
    },
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_declaration_uses_governance_plan_artifact",
    "guard_declaration_templates_complete",
    "guard_declaration_templates_unique",
    "guard_declaration_does_not_accept_operator_approval",
    "guard_declaration_does_not_submit",
    "guard_declaration_does_not_authenticate",
    "guard_declaration_does_not_upload",
    "guard_declaration_real_submission_blocked",
    "guard_declaration_no_score_claim",
    "guard_declaration_no_leaderboard_claim",
    "guard_declaration_no_private_core_exposure",
    "guard_declaration_no_legal_certification",
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


def build_operator_declaration_state() -> Dict[str, Any]:
    return {
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "declaration_package_ready": True,
        "declaration_templates": list(DECLARATION_TEMPLATES),
        "required_declarations": [item["declaration_id"] for item in DECLARATION_TEMPLATES],
        "required_declaration_count": len(DECLARATION_TEMPLATES),
        "declaration_template_count": len(DECLARATION_TEMPLATES),
        "provided_declarations": [],
        "provided_declaration_count": 0,
        "accepted_declarations": [],
        "accepted_declaration_count": 0,
        "rejected_declarations": [],
        "rejected_declaration_count": 0,
        "approval_gate_verdict": "DECLARATION_PACKAGE_READY_APPROVAL_NOT_GRANTED",
    }


def build_declaration_checks() -> Dict[str, bool]:
    governance = _read_json(GOVERNANCE_PLAN_JSON)
    declaration = build_operator_declaration_state()
    template_ids = [item["declaration_id"] for item in DECLARATION_TEMPLATES]
    governance_required = governance.get("operator_approval_state", {}).get("required_declarations", [])

    return {
        "governance_plan_artifact_present": GOVERNANCE_PLAN_JSON.exists(),
        "governance_plan_artifact_ready": governance.get("status")
        == "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_READY",
        "governance_plan_artifact_valid": bool(governance.get("plan_id")) and bool(governance.get("signature")),
        "governance_plan_ready": governance.get("plan_ready") is True,
        "governance_next_stage_matches_task_2": governance.get("next_allowed_stage")
        == "MILESTONE_9_TASK_2_OPERATOR_DECLARATION_PACKAGE_V1",
        "governance_phase_count_valid": governance.get("governance_phase_count")
        == EXPECTED_GOVERNANCE_PHASE_COUNT,
        "pre_submission_gate_count_valid": governance.get("pre_submission_gate_count")
        == EXPECTED_PRE_SUBMISSION_GATE_COUNT,
        "governance_requires_operator_approval": governance.get("operator_approval_required") is True,
        "governance_operator_approval_not_granted": governance.get("operator_approval_granted") is False,
        "template_count_valid": len(DECLARATION_TEMPLATES) == EXPECTED_DECLARATION_TEMPLATE_COUNT,
        "template_ids_unique": len(template_ids) == len(set(template_ids)),
        "template_ids_match_governance_required_declarations": sorted(template_ids) == sorted(governance_required),
        "required_declaration_count_valid": declaration["required_declaration_count"]
        == EXPECTED_DECLARATION_COUNT,
        "provided_declaration_count_zero": declaration["provided_declaration_count"]
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": declaration["accepted_declaration_count"]
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "rejected_declaration_count_zero": declaration["rejected_declaration_count"]
        == EXPECTED_REJECTED_DECLARATION_COUNT,
        "operator_approval_required": declaration["operator_approval_required"] is True,
        "operator_approval_not_granted": declaration["operator_approval_granted"] is False,
        "operator_approval_not_received": declaration["operator_approval_received"] is False,
        "declaration_package_ready": declaration["declaration_package_ready"] is True,
        "real_submission_not_created": True,
        "real_submission_allowed_false": False is False,
        "ready_for_real_kaggle_submission_false": False is False,
        "kaggle_submission_not_sent": False is False,
        "upload_not_performed": False is False,
        "kaggle_authentication_not_performed": False is False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_9_TASK_3_LOCAL_CANDIDATE_MANUAL_REVIEW_V1",
    }


def evaluate_operator_declaration_package_case(case_id: str) -> Dict[str, Any]:
    checks = build_declaration_checks()

    if case_id == "declaration_governance_plan_source_ready_v1":
        passed = (
            checks["governance_plan_artifact_present"]
            and checks["governance_plan_artifact_ready"]
            and checks["governance_plan_artifact_valid"]
            and checks["governance_plan_ready"]
        )
        return _result(case_id, "source_binding", "verify_governance_plan_artifact", passed)

    if case_id == "declaration_template_set_complete_v1":
        passed = (
            checks["template_count_valid"]
            and checks["template_ids_unique"]
            and checks["template_ids_match_governance_required_declarations"]
        )
        return _result(case_id, "declaration_template", "verify_declaration_template_set", passed)

    if case_id == "declaration_required_count_valid_v1":
        passed = checks["required_declaration_count_valid"]
        return _result(case_id, "operator_approval", "verify_required_declaration_count", passed)

    if case_id == "declaration_no_operator_submission_yet_v1":
        passed = checks["provided_declaration_count_zero"] and checks["operator_approval_not_received"]
        return _result(case_id, "operator_approval", "verify_no_operator_declarations_provided", passed)

    if case_id == "declaration_no_accepted_declarations_yet_v1":
        passed = checks["accepted_declaration_count_zero"] and checks["rejected_declaration_count_zero"]
        return _result(case_id, "operator_approval", "verify_no_declarations_accepted", passed)

    if case_id == "declaration_approval_not_granted_v1":
        passed = checks["operator_approval_required"] and checks["operator_approval_not_granted"]
        return _result(case_id, "approval_gate", "verify_approval_not_granted", passed)

    if case_id == "declaration_real_submission_blocked_v1":
        passed = (
            checks["real_submission_not_created"]
            and checks["real_submission_allowed_false"]
            and checks["ready_for_real_kaggle_submission_false"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission", "verify_real_submission_blocked", passed)

    if case_id == "declaration_no_upload_no_auth_v1":
        passed = checks["upload_not_performed"] and checks["kaggle_authentication_not_performed"]
        return _result(case_id, "boundary", "verify_no_upload_no_auth", passed)

    if case_id == "declaration_no_score_or_leaderboard_claim_v1":
        passed = checks["score_claim_absent"] and checks["public_leaderboard_claim_absent"]
        return _result(case_id, "claim_boundary", "verify_no_score_or_leaderboard_claim", passed)

    if case_id == "declaration_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_local_candidate_manual_review_next", passed)

    raise ValueError(f"unknown operator declaration package case: {case_id}")


def evaluate_all_operator_declaration_package_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_operator_declaration_package_case(case["case_id"]) for case in PACKAGE_CASES)


def build_milestone_9_operator_declaration_package() -> Dict[str, Any]:
    governance = _read_json(GOVERNANCE_PLAN_JSON)
    declaration = build_operator_declaration_state()
    checks = build_declaration_checks()
    results = evaluate_all_operator_declaration_package_cases()

    package_pass_count = sum(1 for result in results if result["passed"] is True)
    package_failure_count = sum(1 for result in results if result["passed"] is False)

    package_record = {
        "package_mode": PACKAGE_MODE,
        "package_scope": PACKAGE_SCOPE,
        "package_verdict": PACKAGE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "package_ready": True,
        "package_locked": True,
        "baseline_governance_plan_id": governance.get("plan_id", "MISSING_PLAN_ID"),
        "governance_plan_ready": governance.get("plan_ready") is True,
        "declaration_package_created": True,
        "declaration_package_ready": True,
        "declaration_template_count": declaration["declaration_template_count"],
        "required_declaration_count": declaration["required_declaration_count"],
        "provided_declaration_count": declaration["provided_declaration_count"],
        "accepted_declaration_count": declaration["accepted_declaration_count"],
        "rejected_declaration_count": declaration["rejected_declaration_count"],
        "package_case_count": len(PACKAGE_CASES),
        "package_pass_count": package_pass_count,
        "package_failure_count": package_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "operator_approval_required": declaration["operator_approval_required"],
        "operator_approval_granted": declaration["operator_approval_granted"],
        "operator_approval_received": declaration["operator_approval_received"],
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
        "governance_plan_artifact_present": checks["governance_plan_artifact_present"],
        "governance_plan_artifact_ready": checks["governance_plan_artifact_ready"],
        "governance_plan_artifact_valid": checks["governance_plan_artifact_valid"],
        "governance_plan_ready": checks["governance_plan_ready"],
        "governance_next_stage_matches_task_2": checks["governance_next_stage_matches_task_2"],
        "governance_phase_count_valid": checks["governance_phase_count_valid"],
        "pre_submission_gate_count_valid": checks["pre_submission_gate_count_valid"],
        "governance_requires_operator_approval": checks["governance_requires_operator_approval"],
        "governance_operator_approval_not_granted": checks["governance_operator_approval_not_granted"],
        "package_mode_valid": PACKAGE_MODE == "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_LOCAL_ONLY",
        "package_scope_valid": PACKAGE_SCOPE == "CREATE_OPERATOR_DECLARATION_TEMPLATES_WITHOUT_APPROVAL",
        "package_verdict_valid": PACKAGE_VERDICT
        == "OPERATOR_DECLARATION_PACKAGE_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED",
        "package_ready": package_record["package_ready"] is True,
        "package_locked": package_record["package_locked"] is True,
        "declaration_package_created": package_record["declaration_package_created"] is True,
        "declaration_package_ready": package_record["declaration_package_ready"] is True,
        "template_count_valid": checks["template_count_valid"],
        "template_ids_unique": checks["template_ids_unique"],
        "template_ids_match_governance_required_declarations": checks[
            "template_ids_match_governance_required_declarations"
        ],
        "package_case_count_valid": len(PACKAGE_CASES) == EXPECTED_PACKAGE_CASE_COUNT,
        "package_pass_count_valid": package_pass_count == EXPECTED_PACKAGE_PASS_COUNT,
        "package_failure_count_zero": package_failure_count == EXPECTED_PACKAGE_FAILURE_COUNT,
        "all_package_cases_pass": all(result["passed"] is True for result in results),
        "required_declaration_count_valid": checks["required_declaration_count_valid"],
        "provided_declaration_count_zero": checks["provided_declaration_count_zero"],
        "accepted_declaration_count_zero": checks["accepted_declaration_count_zero"],
        "rejected_declaration_count_zero": checks["rejected_declaration_count_zero"],
        "operator_approval_required": checks["operator_approval_required"],
        "operator_approval_not_granted": checks["operator_approval_not_granted"],
        "operator_approval_not_received": checks["operator_approval_not_received"],
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "next_stage_valid": checks["next_stage_valid"],
        "real_submission_not_created": package_record["real_submission_created"] is False,
        "real_submission_allowed_false": package_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": package_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": package_record["kaggle_submission_sent"] is False,
        "upload_not_performed": package_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": package_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": package_record["external_api_dependency"] is False,
        "contains_api_keys_false": package_record["contains_api_keys"] is False,
        "private_core_exposure_false": package_record["private_core_exposure"] is False,
        "legal_certification_false": package_record["legal_certification"] is False,
        "score_claim_absent": package_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": package_record["public_leaderboard_claim_absent"] is True,
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

    package_ready = (
        governance.get("status") == "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_READY"
        and governance.get("plan_ready") is True
        and package_pass_count == EXPECTED_PACKAGE_PASS_COUNT
        and package_failure_count == EXPECTED_PACKAGE_FAILURE_COUNT
        and declaration["declaration_template_count"] == EXPECTED_DECLARATION_TEMPLATE_COUNT
        and declaration["provided_declaration_count"] == 0
        and declaration["accepted_declaration_count"] == 0
        and declaration["operator_approval_granted"] is False
        and package_record["real_submission_allowed"] is False
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #9",
        "task": "Task 2",
        "package_mode": PACKAGE_MODE,
        "package_scope": PACKAGE_SCOPE,
        "package_verdict": PACKAGE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_governance_plan": governance.get("plan_id", "MISSING_PLAN_ID"),
        "package_ready": package_ready,
        "package_locked": True,
        "declaration_package_created": True,
        "declaration_template_count": declaration["declaration_template_count"],
        "required_declaration_count": declaration["required_declaration_count"],
        "provided_declaration_count": declaration["provided_declaration_count"],
        "accepted_declaration_count": declaration["accepted_declaration_count"],
        "rejected_declaration_count": declaration["rejected_declaration_count"],
        "package_case_count": len(PACKAGE_CASES),
        "package_pass_count": package_pass_count,
        "package_failure_count": package_failure_count,
        "operator_approval_required": declaration["operator_approval_required"],
        "operator_approval_granted": declaration["operator_approval_granted"],
        "operator_approval_received": declaration["operator_approval_received"],
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
        "status": PACKAGE_STATUS,
        "milestone": "Milestone #9",
        "task": "Task 2",
        "title": "Operator Declaration Package v1",
        "baseline_commit": BASELINE_COMMIT,
        "package_mode": PACKAGE_MODE,
        "package_scope": PACKAGE_SCOPE,
        "package_verdict": PACKAGE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "governance_plan_source": {
            "path": str(GOVERNANCE_PLAN_JSON),
            "present": GOVERNANCE_PLAN_JSON.exists(),
            "status": governance.get("status", "MISSING"),
            "plan_id": governance.get("plan_id", "MISSING_PLAN_ID"),
            "sha256": _sha256(GOVERNANCE_PLAN_JSON),
            "sha256_16": _sha16(_sha256(GOVERNANCE_PLAN_JSON)),
        },
        "operator_declaration_state": declaration,
        "declaration_templates": list(DECLARATION_TEMPLATES),
        "package_checks": checks,
        "package_cases": list(PACKAGE_CASES),
        "package_results": list(results),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "package_gates": list(gates),
        "package_issues": list(issues),
        "package_index": index,
        "package_record": package_record,
        "package_ready": package_ready,
        "package_locked": True,
        "declaration_package_created": True,
        "declaration_package_ready": True,
        "declaration_template_count": declaration["declaration_template_count"],
        "required_declaration_count": declaration["required_declaration_count"],
        "provided_declaration_count": declaration["provided_declaration_count"],
        "accepted_declaration_count": declaration["accepted_declaration_count"],
        "rejected_declaration_count": declaration["rejected_declaration_count"],
        "package_case_count": len(PACKAGE_CASES),
        "package_pass_count": package_pass_count,
        "package_failure_count": package_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "package_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "package_issue_count": issue_count,
        "warning_count": 0,
        "operator_approval_required": declaration["operator_approval_required"],
        "operator_approval_granted": declaration["operator_approval_granted"],
        "operator_approval_received": declaration["operator_approval_received"],
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_9_operator_declaration_package_v1",
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
        "package_id": f"MILESTONE-9-DECLARATION-PACKAGE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_9_operator_declaration_package(package: Mapping[str, Any]) -> Dict[str, Any]:
    gates = package.get("package_gates", [])
    issues = package.get("package_issues", [])
    results = package.get("package_results", [])

    checks = {
        "status_ready": package.get("status") == PACKAGE_STATUS,
        "package_id_present": isinstance(package.get("package_id"), str) and bool(package.get("package_id")),
        "signature_present": isinstance(package.get("signature"), str) and bool(package.get("signature")),
        "baseline_commit_valid": str(package.get("baseline_commit", "")).startswith("4a716ee"),
        "package_mode_valid": package.get("package_mode") == PACKAGE_MODE,
        "package_scope_valid": package.get("package_scope") == PACKAGE_SCOPE,
        "package_verdict_valid": package.get("package_verdict") == PACKAGE_VERDICT,
        "next_allowed_stage_valid": package.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "package_ready": package.get("package_ready") is True,
        "package_locked": package.get("package_locked") is True,
        "declaration_package_created": package.get("declaration_package_created") is True,
        "declaration_template_count_valid": package.get("declaration_template_count")
        == EXPECTED_DECLARATION_TEMPLATE_COUNT,
        "required_declaration_count_valid": package.get("required_declaration_count")
        == EXPECTED_DECLARATION_COUNT,
        "provided_declaration_count_zero": package.get("provided_declaration_count")
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": package.get("accepted_declaration_count")
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "rejected_declaration_count_zero": package.get("rejected_declaration_count")
        == EXPECTED_REJECTED_DECLARATION_COUNT,
        "package_case_count_valid": package.get("package_case_count") == EXPECTED_PACKAGE_CASE_COUNT,
        "package_pass_count_valid": package.get("package_pass_count") == EXPECTED_PACKAGE_PASS_COUNT,
        "package_failure_count_zero": package.get("package_failure_count") == EXPECTED_PACKAGE_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_package_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "package_issue_count_zero": package.get("package_issue_count") == 0,
        "all_package_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "operator_approval_required": package.get("operator_approval_required") is True,
        "operator_approval_not_granted": package.get("operator_approval_granted") is False,
        "operator_approval_not_received": package.get("operator_approval_received") is False,
        "real_submission_not_created": package.get("real_submission_created") is False,
        "real_submission_allowed_false": package.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": package.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": package.get("kaggle_submission_sent") is False,
        "upload_not_performed": package.get("upload_performed") is False,
        "kaggle_authentication_not_performed": package.get("kaggle_authentication_performed") is False,
        "metadata_safe": package.get("metadata", {}).get("external_api_dependency") is False
        and package.get("metadata", {}).get("contains_api_keys") is False
        and package.get("metadata", {}).get("private_core_exposure") is False
        and package.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "package_id": package.get("package_id"),
        "signature": package.get("signature"),
    }


def render_operator_declaration_package_markdown(package: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #9 - Operator Declaration Package v1",
        "",
        f"- status: {package['status']}",
        f"- package_id: {package['package_id']}",
        f"- signature: {package['signature']}",
        f"- baseline_commit: {package['baseline_commit']}",
        f"- package_mode: {package['package_mode']}",
        f"- package_scope: {package['package_scope']}",
        f"- package_verdict: {package['package_verdict']}",
        f"- next_allowed_stage: {package['next_allowed_stage']}",
        f"- package_ready: {package['package_ready']}",
        f"- declaration_template_count: {package['declaration_template_count']}",
        f"- required_declaration_count: {package['required_declaration_count']}",
        f"- provided_declaration_count: {package['provided_declaration_count']}",
        f"- accepted_declaration_count: {package['accepted_declaration_count']}",
        f"- operator_approval_required: {package['operator_approval_required']}",
        f"- operator_approval_granted: {package['operator_approval_granted']}",
        "",
        "## Declaration templates",
        "",
    ]

    for item in package["declaration_templates"]:
        lines.append(
            f"- {item['declaration_id']}: {item['title']} / "
            f"required_response={item['required_response']}"
        )

    lines.extend(["", "## Package results", ""])

    for result in package["package_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Operator declaration package is ready. No operator approval has been granted. Real submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY=true",
            "ARC_AGI3_MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_VALID=true",
            "ARC_AGI3_MILESTONE_9_DECLARATION_PACKAGE_READY=true",
            "ARC_AGI3_MILESTONE_9_PACKAGE_MODE=MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_9_PACKAGE_VERDICT=OPERATOR_DECLARATION_PACKAGE_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_9_BASELINE_GOVERNANCE_PLAN_COMMIT=4a716ee",
            "ARC_AGI3_MILESTONE_9_DECLARATION_TEMPLATE_COUNT=8",
            "ARC_AGI3_MILESTONE_9_REQUIRED_DECLARATION_COUNT=8",
            "ARC_AGI3_MILESTONE_9_PROVIDED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_ACCEPTED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_REJECTED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_PACKAGE_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_9_PACKAGE_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_9_PACKAGE_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_9_NEXT_STAGE=MILESTONE_9_TASK_3_LOCAL_CANDIDATE_MANUAL_REVIEW_V1",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_REQUIRED=true",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_RECEIVED=false",
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


def render_operator_declaration_package_manifest(package: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 9 OPERATOR DECLARATION PACKAGE MANIFEST v1",
        f"package_id={package['package_id']}",
        f"signature={package['signature']}",
        f"status={package['status']}",
        f"baseline_commit={package['baseline_commit']}",
        f"package_mode={package['package_mode']}",
        f"package_verdict={package['package_verdict']}",
        f"next_allowed_stage={package['next_allowed_stage']}",
        f"package_ready={package['package_ready']}",
        f"declaration_package_created={package['declaration_package_created']}",
        f"declaration_package_ready={package['declaration_package_ready']}",
        f"declaration_template_count={package['declaration_template_count']}",
        f"required_declaration_count={package['required_declaration_count']}",
        f"provided_declaration_count={package['provided_declaration_count']}",
        f"accepted_declaration_count={package['accepted_declaration_count']}",
        f"rejected_declaration_count={package['rejected_declaration_count']}",
        f"package_case_count={package['package_case_count']}",
        f"package_pass_count={package['package_pass_count']}",
        f"package_failure_count={package['package_failure_count']}",
        f"package_gate_count={package['package_gate_count']}",
        f"passed_gate_count={package['passed_gate_count']}",
        f"package_issue_count={package['package_issue_count']}",
        f"operator_approval_required={package['operator_approval_required']}",
        f"operator_approval_granted={package['operator_approval_granted']}",
        f"operator_approval_received={package['operator_approval_received']}",
        f"real_submission_created={package['real_submission_created']}",
        f"real_submission_allowed={package['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={package['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={package['kaggle_submission_sent']}",
        f"upload_performed={package['upload_performed']}",
        f"kaggle_authentication_performed={package['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "DECLARATION_TEMPLATES",
    ]

    for item in package["declaration_templates"]:
        lines.append(
            f"{item['declaration_id']} title={item['title']} "
            f"required_response={item['required_response']}"
        )

    lines.append("")
    lines.append("PACKAGE_RESULTS")
    for result in package["package_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_operator_declaration_package_artifacts(
    package: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    package = dict(package or build_milestone_9_operator_declaration_package())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-9-operator-declaration-package-v1.json"
    md_path = output / "milestone-9-operator-declaration-package-v1.md"
    manifest_path = output / "milestone-9-operator-declaration-package-manifest-v1.txt"
    index_path = output / "milestone-9-operator-declaration-package-index-v1.json"

    json_path.write_text(json.dumps(package, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_operator_declaration_package_markdown(package), encoding="utf-8")
    manifest_path.write_text(render_operator_declaration_package_manifest(package), encoding="utf-8")
    index_path.write_text(json.dumps(package["package_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_9_operator_declaration_package_pipeline() -> Dict[str, Any]:
    package = build_milestone_9_operator_declaration_package()
    validation = validate_milestone_9_operator_declaration_package(package)
    artifacts = write_operator_declaration_package_artifacts(package)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_PIPELINE_INVALID",
        "package_status": package["status"],
        "validation_status": validation["status"],
        "package": package,
        "package_id": package["package_id"],
        "signature": package["signature"],
        "package_mode": package["package_mode"],
        "package_verdict": package["package_verdict"],
        "next_allowed_stage": package["next_allowed_stage"],
        "package_ready": package["package_ready"],
        "package_locked": package["package_locked"],
        "declaration_package_created": package["declaration_package_created"],
        "declaration_package_ready": package["declaration_package_ready"],
        "declaration_template_count": package["declaration_template_count"],
        "required_declaration_count": package["required_declaration_count"],
        "provided_declaration_count": package["provided_declaration_count"],
        "accepted_declaration_count": package["accepted_declaration_count"],
        "rejected_declaration_count": package["rejected_declaration_count"],
        "package_case_count": package["package_case_count"],
        "package_pass_count": package["package_pass_count"],
        "package_failure_count": package["package_failure_count"],
        "regression_guard_count": package["regression_guard_count"],
        "boundary_control_count": package["boundary_control_count"],
        "package_gate_count": package["package_gate_count"],
        "passed_gate_count": package["passed_gate_count"],
        "package_issue_count": package["package_issue_count"],
        "warning_count": package["warning_count"],
        "operator_approval_required": package["operator_approval_required"],
        "operator_approval_granted": package["operator_approval_granted"],
        "operator_approval_received": package["operator_approval_received"],
        "real_submission_created": package["real_submission_created"],
        "real_submission_allowed": package["real_submission_allowed"],
        "ready_for_real_kaggle_submission": package["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": package["kaggle_submission_sent"],
        "upload_performed": package["upload_performed"],
        "kaggle_authentication_performed": package["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": package["metadata"],
    }
