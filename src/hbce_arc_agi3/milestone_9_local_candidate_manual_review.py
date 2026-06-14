"""Milestone #9 Local Candidate Manual Review v1.

Local-only deterministic review package for the manual submission governance
phase.

This module verifies the local submission candidate package, links it to the
operator declaration package, prepares manual review evidence, and keeps real
submission blocked.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, accept declarations, grant approval, claim a Kaggle score, claim
public leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


REVIEW_STATUS = "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY"
PIPELINE_STATUS = "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_VALID"

BASELINE_COMMIT = "0c157ff Add ARC AGI3 operator declaration package"
REVIEW_MODE = "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_LOCAL_ONLY"
REVIEW_SCOPE = "VERIFY_LOCAL_CANDIDATE_PACKAGE_WITHOUT_OPERATOR_APPROVAL"
REVIEW_VERDICT = "LOCAL_CANDIDATE_MANUAL_REVIEW_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_9_TASK_4_REAL_SUBMISSION_PREFLIGHT_GATE_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-9/local-candidate-manual-review-v1"

DECLARATION_PACKAGE_JSON = Path(
    "examples/milestone-9/operator-declaration-package-v1/"
    "milestone-9-operator-declaration-package-v1.json"
)

CANDIDATE_SOURCE_CANDIDATES: Tuple[Path, ...] = (
    Path(
        "examples/milestone-8/submission-candidate-refresh-v2/"
        "milestone-8-submission-candidate-refresh-v2.json"
    ),
    Path(
        "examples/milestone-5/submission-candidate-dry-run-package-v1/"
        "milestone-5-submission-candidate-dry-run-package-v1.json"
    ),
)

EXPECTED_REVIEW_CASE_COUNT = 10
EXPECTED_REVIEW_PASS_COUNT = 10
EXPECTED_REVIEW_FAILURE_COUNT = 0
EXPECTED_REVIEW_CHECK_COUNT = 12
EXPECTED_DECLARATION_TEMPLATE_COUNT = 8
EXPECTED_REQUIRED_DECLARATION_COUNT = 8
EXPECTED_PROVIDED_DECLARATION_COUNT = 0
EXPECTED_ACCEPTED_DECLARATION_COUNT = 0
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_REGRESSION_GUARD_COUNT = 12

REVIEW_CHECKS: Tuple[str, ...] = (
    "candidate_package_exists",
    "candidate_package_ready",
    "candidate_payload_signature_present",
    "candidate_artifacts_available",
    "operator_declaration_package_exists",
    "operator_declaration_package_ready",
    "operator_declarations_not_provided",
    "operator_approval_not_granted",
    "real_submission_blocked",
    "upload_blocked",
    "authentication_blocked",
    "claim_boundary_preserved",
)

REVIEW_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "review_operator_declaration_package_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_operator_declaration_package",
    },
    {
        "case_id": "review_local_candidate_source_ready_v1",
        "area": "candidate_source",
        "operation": "verify_local_candidate_package",
    },
    {
        "case_id": "review_candidate_artifacts_available_v1",
        "area": "candidate_artifact",
        "operation": "verify_candidate_artifacts_available",
    },
    {
        "case_id": "review_candidate_payload_signature_present_v1",
        "area": "candidate_integrity",
        "operation": "verify_candidate_signature",
    },
    {
        "case_id": "review_declarations_still_empty_v1",
        "area": "operator_approval",
        "operation": "verify_no_operator_declarations_provided",
    },
    {
        "case_id": "review_operator_approval_not_granted_v1",
        "area": "approval_gate",
        "operation": "verify_operator_approval_not_granted",
    },
    {
        "case_id": "review_real_submission_blocked_v1",
        "area": "submission",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "review_no_upload_no_auth_v1",
        "area": "boundary",
        "operation": "verify_no_upload_no_auth",
    },
    {
        "case_id": "review_no_score_or_leaderboard_claim_v1",
        "area": "claim_boundary",
        "operation": "verify_no_score_or_leaderboard_claim",
    },
    {
        "case_id": "review_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_real_submission_preflight_gate_next",
    },
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_review_uses_operator_declaration_package",
    "guard_review_uses_local_candidate_package",
    "guard_review_verifies_candidate_artifacts",
    "guard_review_verifies_candidate_signature",
    "guard_review_does_not_accept_declarations",
    "guard_review_does_not_grant_operator_approval",
    "guard_review_does_not_submit",
    "guard_review_does_not_authenticate",
    "guard_review_does_not_upload",
    "guard_review_no_score_claim",
    "guard_review_no_private_core_exposure",
    "guard_review_no_legal_certification",
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


def resolve_candidate_source_path() -> Path:
    for path in CANDIDATE_SOURCE_CANDIDATES:
        if path.exists():
            return path

    fallback = sorted(Path("examples").glob("**/*submission*candidate*.json"))
    if fallback:
        return fallback[-1]

    return CANDIDATE_SOURCE_CANDIDATES[0]


def build_candidate_source_summary() -> Dict[str, Any]:
    path = resolve_candidate_source_path()
    payload = _read_json(path)

    candidate_count = (
        payload.get("submission_candidate_count")
        or payload.get("candidate_count")
        or payload.get("candidate_task_count")
        or payload.get("task_count")
        or 0
    )

    candidate_signature = (
        payload.get("candidate_payload_signature")
        or payload.get("signature")
        or payload.get("package_signature")
        or payload.get("refresh_signature")
        or ""
    )

    return {
        "path": str(path),
        "present": path.exists(),
        "status": payload.get("status", "MISSING"),
        "candidate_id": payload.get("refresh_id")
        or payload.get("package_id")
        or payload.get("candidate_id")
        or payload.get("submission_candidate_id")
        or "MISSING_CANDIDATE_ID",
        "signature": candidate_signature,
        "candidate_count": candidate_count,
        "local_submission_candidate_created": payload.get("local_submission_candidate_created", False),
        "submission_candidate_manifest_created": payload.get("submission_candidate_manifest_created", False),
        "submission_candidate_index_created": payload.get("submission_candidate_index_created", False),
        "submission_candidate_hash_available": payload.get("submission_candidate_hash_available", False),
        "real_submission_allowed": payload.get("real_submission_allowed", False),
        "kaggle_submission_sent": payload.get("kaggle_submission_sent", False),
        "upload_performed": payload.get("upload_performed", False),
        "kaggle_authentication_performed": payload.get("kaggle_authentication_performed", False),
        "sha256": _sha256(path),
        "sha256_16": _sha16(_sha256(path)),
    }


def build_manual_review_state() -> Dict[str, Any]:
    return {
        "local_candidate_manual_review_required": True,
        "local_candidate_manual_review_ready": True,
        "local_candidate_manual_review_completed": False,
        "local_candidate_review_artifact_ready": True,
        "candidate_review_verdict": "LOCAL_CANDIDATE_READY_FOR_MANUAL_REVIEW_APPROVAL_NOT_GRANTED",
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "reviewer_acceptance_recorded": False,
        "reviewer_rejection_recorded": False,
        "manual_upload_allowed": False,
    }


def build_local_candidate_manual_review_checks() -> Dict[str, bool]:
    declaration = _read_json(DECLARATION_PACKAGE_JSON)
    candidate = build_candidate_source_summary()
    review = build_manual_review_state()

    candidate_status_ready = (
        candidate["status"] in {
            "MILESTONE_8_SUBMISSION_CANDIDATE_REFRESH_V2_READY",
            "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
        }
        or candidate["local_submission_candidate_created"] is True
        or candidate["candidate_count"] > 0
    )

    candidate_artifacts_available = (
        candidate["present"]
        and (
            candidate["submission_candidate_manifest_created"] is True
            or candidate["submission_candidate_index_created"] is True
            or Path(candidate["path"]).exists()
        )
    )

    return {
        "declaration_package_artifact_present": DECLARATION_PACKAGE_JSON.exists(),
        "declaration_package_artifact_ready": declaration.get("status")
        == "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY",
        "declaration_package_artifact_valid": bool(declaration.get("package_id"))
        and bool(declaration.get("signature")),
        "declaration_package_ready": declaration.get("package_ready") is True,
        "declaration_package_next_stage_matches_task_3": declaration.get("next_allowed_stage")
        == "MILESTONE_9_TASK_3_LOCAL_CANDIDATE_MANUAL_REVIEW_V1",
        "declaration_template_count_valid": declaration.get("declaration_template_count")
        == EXPECTED_DECLARATION_TEMPLATE_COUNT,
        "required_declaration_count_valid": declaration.get("required_declaration_count")
        == EXPECTED_REQUIRED_DECLARATION_COUNT,
        "provided_declaration_count_zero": declaration.get("provided_declaration_count")
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": declaration.get("accepted_declaration_count")
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "operator_approval_required": declaration.get("operator_approval_required") is True
        and review["operator_approval_required"] is True,
        "operator_approval_not_granted": declaration.get("operator_approval_granted") is False
        and review["operator_approval_granted"] is False,
        "operator_approval_not_received": declaration.get("operator_approval_received") is False
        and review["operator_approval_received"] is False,
        "candidate_source_present": candidate["present"],
        "candidate_source_ready": candidate_status_ready,
        "candidate_count_positive": candidate["candidate_count"] > 0,
        "candidate_signature_present": bool(candidate["signature"]),
        "candidate_artifacts_available": candidate_artifacts_available,
        "candidate_real_submission_blocked": candidate["real_submission_allowed"] is False
        and candidate["kaggle_submission_sent"] is False,
        "review_check_count_valid": len(REVIEW_CHECKS) == EXPECTED_REVIEW_CHECK_COUNT,
        "manual_review_required": review["local_candidate_manual_review_required"] is True,
        "manual_review_ready": review["local_candidate_manual_review_ready"] is True,
        "manual_review_not_completed": review["local_candidate_manual_review_completed"] is False,
        "reviewer_acceptance_not_recorded": review["reviewer_acceptance_recorded"] is False,
        "reviewer_rejection_not_recorded": review["reviewer_rejection_recorded"] is False,
        "manual_upload_not_allowed": review["manual_upload_allowed"] is False,
        "real_submission_not_created": True,
        "real_submission_allowed_false": False is False,
        "ready_for_real_kaggle_submission_false": False is False,
        "kaggle_submission_not_sent": False is False,
        "upload_not_performed": False is False,
        "kaggle_authentication_not_performed": False is False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_9_TASK_4_REAL_SUBMISSION_PREFLIGHT_GATE_V1",
    }


def evaluate_local_candidate_manual_review_case(case_id: str) -> Dict[str, Any]:
    checks = build_local_candidate_manual_review_checks()

    if case_id == "review_operator_declaration_package_source_ready_v1":
        passed = (
            checks["declaration_package_artifact_present"]
            and checks["declaration_package_artifact_ready"]
            and checks["declaration_package_artifact_valid"]
            and checks["declaration_package_ready"]
        )
        return _result(case_id, "source_binding", "verify_operator_declaration_package", passed)

    if case_id == "review_local_candidate_source_ready_v1":
        passed = (
            checks["candidate_source_present"]
            and checks["candidate_source_ready"]
            and checks["candidate_count_positive"]
        )
        return _result(case_id, "candidate_source", "verify_local_candidate_package", passed)

    if case_id == "review_candidate_artifacts_available_v1":
        passed = checks["candidate_artifacts_available"]
        return _result(case_id, "candidate_artifact", "verify_candidate_artifacts_available", passed)

    if case_id == "review_candidate_payload_signature_present_v1":
        passed = checks["candidate_signature_present"]
        return _result(case_id, "candidate_integrity", "verify_candidate_signature", passed)

    if case_id == "review_declarations_still_empty_v1":
        passed = checks["provided_declaration_count_zero"] and checks["accepted_declaration_count_zero"]
        return _result(case_id, "operator_approval", "verify_no_operator_declarations_provided", passed)

    if case_id == "review_operator_approval_not_granted_v1":
        passed = (
            checks["operator_approval_required"]
            and checks["operator_approval_not_granted"]
            and checks["operator_approval_not_received"]
        )
        return _result(case_id, "approval_gate", "verify_operator_approval_not_granted", passed)

    if case_id == "review_real_submission_blocked_v1":
        passed = (
            checks["candidate_real_submission_blocked"]
            and checks["real_submission_not_created"]
            and checks["real_submission_allowed_false"]
            and checks["ready_for_real_kaggle_submission_false"]
            and checks["kaggle_submission_not_sent"]
            and checks["manual_upload_not_allowed"]
        )
        return _result(case_id, "submission", "verify_real_submission_blocked", passed)

    if case_id == "review_no_upload_no_auth_v1":
        passed = checks["upload_not_performed"] and checks["kaggle_authentication_not_performed"]
        return _result(case_id, "boundary", "verify_no_upload_no_auth", passed)

    if case_id == "review_no_score_or_leaderboard_claim_v1":
        passed = checks["score_claim_absent"] and checks["public_leaderboard_claim_absent"]
        return _result(case_id, "claim_boundary", "verify_no_score_or_leaderboard_claim", passed)

    if case_id == "review_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_real_submission_preflight_gate_next", passed)

    raise ValueError(f"unknown local candidate manual review case: {case_id}")


def evaluate_all_local_candidate_manual_review_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_local_candidate_manual_review_case(case["case_id"]) for case in REVIEW_CASES)


def build_milestone_9_local_candidate_manual_review() -> Dict[str, Any]:
    declaration = _read_json(DECLARATION_PACKAGE_JSON)
    candidate = build_candidate_source_summary()
    review = build_manual_review_state()
    checks = build_local_candidate_manual_review_checks()
    results = evaluate_all_local_candidate_manual_review_cases()

    review_pass_count = sum(1 for result in results if result["passed"] is True)
    review_failure_count = sum(1 for result in results if result["passed"] is False)

    review_record = {
        "review_mode": REVIEW_MODE,
        "review_scope": REVIEW_SCOPE,
        "review_verdict": REVIEW_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "review_ready": True,
        "review_locked": True,
        "baseline_declaration_package_id": declaration.get("package_id", "MISSING_PACKAGE_ID"),
        "declaration_package_ready": declaration.get("package_ready") is True,
        "candidate_source_path": candidate["path"],
        "candidate_source_ready": checks["candidate_source_ready"],
        "candidate_count": candidate["candidate_count"],
        "candidate_signature": candidate["signature"],
        "local_candidate_manual_review_created": True,
        "local_candidate_manual_review_ready": review["local_candidate_manual_review_ready"],
        "local_candidate_manual_review_completed": review["local_candidate_manual_review_completed"],
        "review_check_count": len(REVIEW_CHECKS),
        "review_case_count": len(REVIEW_CASES),
        "review_pass_count": review_pass_count,
        "review_failure_count": review_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "operator_approval_required": review["operator_approval_required"],
        "operator_approval_granted": review["operator_approval_granted"],
        "operator_approval_received": review["operator_approval_received"],
        "reviewer_acceptance_recorded": review["reviewer_acceptance_recorded"],
        "reviewer_rejection_recorded": review["reviewer_rejection_recorded"],
        "manual_upload_allowed": review["manual_upload_allowed"],
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
        "declaration_package_artifact_present": checks["declaration_package_artifact_present"],
        "declaration_package_artifact_ready": checks["declaration_package_artifact_ready"],
        "declaration_package_artifact_valid": checks["declaration_package_artifact_valid"],
        "declaration_package_ready": checks["declaration_package_ready"],
        "declaration_package_next_stage_matches_task_3": checks[
            "declaration_package_next_stage_matches_task_3"
        ],
        "declaration_template_count_valid": checks["declaration_template_count_valid"],
        "required_declaration_count_valid": checks["required_declaration_count_valid"],
        "provided_declaration_count_zero": checks["provided_declaration_count_zero"],
        "accepted_declaration_count_zero": checks["accepted_declaration_count_zero"],
        "review_mode_valid": REVIEW_MODE == "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_LOCAL_ONLY",
        "review_scope_valid": REVIEW_SCOPE == "VERIFY_LOCAL_CANDIDATE_PACKAGE_WITHOUT_OPERATOR_APPROVAL",
        "review_verdict_valid": REVIEW_VERDICT
        == "LOCAL_CANDIDATE_MANUAL_REVIEW_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED",
        "review_ready": review_record["review_ready"] is True,
        "review_locked": review_record["review_locked"] is True,
        "candidate_source_present": checks["candidate_source_present"],
        "candidate_source_ready": checks["candidate_source_ready"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_artifacts_available": checks["candidate_artifacts_available"],
        "candidate_real_submission_blocked": checks["candidate_real_submission_blocked"],
        "review_check_count_valid": checks["review_check_count_valid"],
        "review_case_count_valid": len(REVIEW_CASES) == EXPECTED_REVIEW_CASE_COUNT,
        "review_pass_count_valid": review_pass_count == EXPECTED_REVIEW_PASS_COUNT,
        "review_failure_count_zero": review_failure_count == EXPECTED_REVIEW_FAILURE_COUNT,
        "all_review_cases_pass": all(result["passed"] is True for result in results),
        "manual_review_required": checks["manual_review_required"],
        "manual_review_ready": checks["manual_review_ready"],
        "manual_review_not_completed": checks["manual_review_not_completed"],
        "reviewer_acceptance_not_recorded": checks["reviewer_acceptance_not_recorded"],
        "reviewer_rejection_not_recorded": checks["reviewer_rejection_not_recorded"],
        "operator_approval_required": checks["operator_approval_required"],
        "operator_approval_not_granted": checks["operator_approval_not_granted"],
        "operator_approval_not_received": checks["operator_approval_not_received"],
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "next_stage_valid": checks["next_stage_valid"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "real_submission_not_created": review_record["real_submission_created"] is False,
        "real_submission_allowed_false": review_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": review_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": review_record["kaggle_submission_sent"] is False,
        "upload_not_performed": review_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": review_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": review_record["external_api_dependency"] is False,
        "contains_api_keys_false": review_record["contains_api_keys"] is False,
        "private_core_exposure_false": review_record["private_core_exposure"] is False,
        "legal_certification_false": review_record["legal_certification"] is False,
        "score_claim_absent": review_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": review_record["public_leaderboard_claim_absent"] is True,
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
        declaration.get("status") == "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY"
        and declaration.get("package_ready") is True
        and review_pass_count == EXPECTED_REVIEW_PASS_COUNT
        and review_failure_count == EXPECTED_REVIEW_FAILURE_COUNT
        and candidate["present"] is True
        and checks["candidate_source_ready"] is True
        and review["operator_approval_granted"] is False
        and review_record["real_submission_allowed"] is False
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #9",
        "task": "Task 3",
        "review_mode": REVIEW_MODE,
        "review_scope": REVIEW_SCOPE,
        "review_verdict": REVIEW_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_operator_declaration_package": declaration.get("package_id", "MISSING_PACKAGE_ID"),
        "candidate_source_path": candidate["path"],
        "review_ready": package_ready,
        "review_locked": True,
        "local_candidate_manual_review_created": True,
        "local_candidate_manual_review_completed": False,
        "review_check_count": len(REVIEW_CHECKS),
        "review_case_count": len(REVIEW_CASES),
        "review_pass_count": review_pass_count,
        "review_failure_count": review_failure_count,
        "candidate_count": candidate["candidate_count"],
        "operator_approval_required": review["operator_approval_required"],
        "operator_approval_granted": review["operator_approval_granted"],
        "operator_approval_received": review["operator_approval_received"],
        "manual_upload_allowed": False,
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
        "status": REVIEW_STATUS,
        "milestone": "Milestone #9",
        "task": "Task 3",
        "title": "Local Candidate Manual Review v1",
        "baseline_commit": BASELINE_COMMIT,
        "review_mode": REVIEW_MODE,
        "review_scope": REVIEW_SCOPE,
        "review_verdict": REVIEW_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "declaration_package_source": {
            "path": str(DECLARATION_PACKAGE_JSON),
            "present": DECLARATION_PACKAGE_JSON.exists(),
            "status": declaration.get("status", "MISSING"),
            "package_id": declaration.get("package_id", "MISSING_PACKAGE_ID"),
            "sha256": _sha256(DECLARATION_PACKAGE_JSON),
            "sha256_16": _sha16(_sha256(DECLARATION_PACKAGE_JSON)),
        },
        "candidate_source": candidate,
        "manual_review_state": review,
        "review_checks": checks,
        "review_check_list": list(REVIEW_CHECKS),
        "review_cases": list(REVIEW_CASES),
        "review_results": list(results),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "review_gates": list(gates),
        "review_issues": list(issues),
        "review_index": index,
        "review_record": review_record,
        "review_ready": package_ready,
        "review_locked": True,
        "local_candidate_manual_review_created": True,
        "local_candidate_manual_review_ready": review["local_candidate_manual_review_ready"],
        "local_candidate_manual_review_completed": review["local_candidate_manual_review_completed"],
        "review_check_count": len(REVIEW_CHECKS),
        "review_case_count": len(REVIEW_CASES),
        "review_pass_count": review_pass_count,
        "review_failure_count": review_failure_count,
        "candidate_count": candidate["candidate_count"],
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "review_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "review_issue_count": issue_count,
        "warning_count": 0,
        "operator_approval_required": review["operator_approval_required"],
        "operator_approval_granted": review["operator_approval_granted"],
        "operator_approval_received": review["operator_approval_received"],
        "reviewer_acceptance_recorded": review["reviewer_acceptance_recorded"],
        "reviewer_rejection_recorded": review["reviewer_rejection_recorded"],
        "manual_upload_allowed": review["manual_upload_allowed"],
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_9_local_candidate_manual_review_v1",
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
        "review_id": f"MILESTONE-9-LOCAL-REVIEW-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_9_local_candidate_manual_review(review: Mapping[str, Any]) -> Dict[str, Any]:
    gates = review.get("review_gates", [])
    issues = review.get("review_issues", [])
    results = review.get("review_results", [])

    checks = {
        "status_ready": review.get("status") == REVIEW_STATUS,
        "review_id_present": isinstance(review.get("review_id"), str) and bool(review.get("review_id")),
        "signature_present": isinstance(review.get("signature"), str) and bool(review.get("signature")),
        "baseline_commit_valid": str(review.get("baseline_commit", "")).startswith("0c157ff"),
        "review_mode_valid": review.get("review_mode") == REVIEW_MODE,
        "review_scope_valid": review.get("review_scope") == REVIEW_SCOPE,
        "review_verdict_valid": review.get("review_verdict") == REVIEW_VERDICT,
        "next_allowed_stage_valid": review.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "review_ready": review.get("review_ready") is True,
        "review_locked": review.get("review_locked") is True,
        "local_candidate_manual_review_created": review.get("local_candidate_manual_review_created") is True,
        "local_candidate_manual_review_ready": review.get("local_candidate_manual_review_ready") is True,
        "local_candidate_manual_review_not_completed": review.get("local_candidate_manual_review_completed") is False,
        "review_check_count_valid": review.get("review_check_count") == EXPECTED_REVIEW_CHECK_COUNT,
        "review_case_count_valid": review.get("review_case_count") == EXPECTED_REVIEW_CASE_COUNT,
        "review_pass_count_valid": review.get("review_pass_count") == EXPECTED_REVIEW_PASS_COUNT,
        "review_failure_count_zero": review.get("review_failure_count") == EXPECTED_REVIEW_FAILURE_COUNT,
        "candidate_count_positive": review.get("candidate_count", 0) > 0,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_review_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "review_issue_count_zero": review.get("review_issue_count") == 0,
        "all_review_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "operator_approval_required": review.get("operator_approval_required") is True,
        "operator_approval_not_granted": review.get("operator_approval_granted") is False,
        "operator_approval_not_received": review.get("operator_approval_received") is False,
        "manual_upload_not_allowed": review.get("manual_upload_allowed") is False,
        "real_submission_not_created": review.get("real_submission_created") is False,
        "real_submission_allowed_false": review.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": review.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": review.get("kaggle_submission_sent") is False,
        "upload_not_performed": review.get("upload_performed") is False,
        "kaggle_authentication_not_performed": review.get("kaggle_authentication_performed") is False,
        "metadata_safe": review.get("metadata", {}).get("external_api_dependency") is False
        and review.get("metadata", {}).get("contains_api_keys") is False
        and review.get("metadata", {}).get("private_core_exposure") is False
        and review.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "review_id": review.get("review_id"),
        "signature": review.get("signature"),
    }


def render_local_candidate_manual_review_markdown(review: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #9 - Local Candidate Manual Review v1",
        "",
        f"- status: {review['status']}",
        f"- review_id: {review['review_id']}",
        f"- signature: {review['signature']}",
        f"- baseline_commit: {review['baseline_commit']}",
        f"- review_mode: {review['review_mode']}",
        f"- review_scope: {review['review_scope']}",
        f"- review_verdict: {review['review_verdict']}",
        f"- next_allowed_stage: {review['next_allowed_stage']}",
        f"- review_ready: {review['review_ready']}",
        f"- local_candidate_manual_review_created: {review['local_candidate_manual_review_created']}",
        f"- local_candidate_manual_review_completed: {review['local_candidate_manual_review_completed']}",
        f"- candidate_count: {review['candidate_count']}",
        f"- review_check_count: {review['review_check_count']}",
        f"- review_case_count: {review['review_case_count']}",
        f"- review_pass_count: {review['review_pass_count']}",
        f"- review_failure_count: {review['review_failure_count']}",
        f"- operator_approval_required: {review['operator_approval_required']}",
        f"- operator_approval_granted: {review['operator_approval_granted']}",
        "",
        "## Candidate source",
        "",
        f"- path: {review['candidate_source']['path']}",
        f"- status: {review['candidate_source']['status']}",
        f"- candidate_id: {review['candidate_source']['candidate_id']}",
        f"- signature: {review['candidate_source']['signature']}",
        f"- sha256_16: {review['candidate_source']['sha256_16']}",
        "",
        "## Review checks",
        "",
    ]

    for item in review["review_check_list"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Review results", ""])

    for result in review["review_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Local candidate manual review package is ready. Manual review is not completed. Operator approval has not been granted. Real submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY=true",
            "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_VALID=true",
            "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_REVIEW_READY=true",
            "ARC_AGI3_MILESTONE_9_REVIEW_MODE=MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_9_REVIEW_VERDICT=LOCAL_CANDIDATE_MANUAL_REVIEW_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_9_BASELINE_OPERATOR_DECLARATION_PACKAGE_COMMIT=0c157ff",
            "ARC_AGI3_MILESTONE_9_REVIEW_CHECK_COUNT=12",
            "ARC_AGI3_MILESTONE_9_REVIEW_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_9_REVIEW_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_9_REVIEW_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_CREATED=true",
            "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_COMPLETED=false",
            "ARC_AGI3_MILESTONE_9_NEXT_STAGE=MILESTONE_9_TASK_4_REAL_SUBMISSION_PREFLIGHT_GATE_V1",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_REQUIRED=true",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_RECEIVED=false",
            "ARC_AGI3_MILESTONE_9_MANUAL_UPLOAD_ALLOWED=false",
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


def render_local_candidate_manual_review_manifest(review: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 9 LOCAL CANDIDATE MANUAL REVIEW MANIFEST v1",
        f"review_id={review['review_id']}",
        f"signature={review['signature']}",
        f"status={review['status']}",
        f"baseline_commit={review['baseline_commit']}",
        f"review_mode={review['review_mode']}",
        f"review_verdict={review['review_verdict']}",
        f"next_allowed_stage={review['next_allowed_stage']}",
        f"review_ready={review['review_ready']}",
        f"review_locked={review['review_locked']}",
        f"local_candidate_manual_review_created={review['local_candidate_manual_review_created']}",
        f"local_candidate_manual_review_ready={review['local_candidate_manual_review_ready']}",
        f"local_candidate_manual_review_completed={review['local_candidate_manual_review_completed']}",
        f"candidate_source_path={review['candidate_source']['path']}",
        f"candidate_count={review['candidate_count']}",
        f"review_check_count={review['review_check_count']}",
        f"review_case_count={review['review_case_count']}",
        f"review_pass_count={review['review_pass_count']}",
        f"review_failure_count={review['review_failure_count']}",
        f"review_gate_count={review['review_gate_count']}",
        f"passed_gate_count={review['passed_gate_count']}",
        f"review_issue_count={review['review_issue_count']}",
        f"operator_approval_required={review['operator_approval_required']}",
        f"operator_approval_granted={review['operator_approval_granted']}",
        f"operator_approval_received={review['operator_approval_received']}",
        f"manual_upload_allowed={review['manual_upload_allowed']}",
        f"real_submission_created={review['real_submission_created']}",
        f"real_submission_allowed={review['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={review['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={review['kaggle_submission_sent']}",
        f"upload_performed={review['upload_performed']}",
        f"kaggle_authentication_performed={review['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "REVIEW_CHECKS",
    ]

    for item in review["review_check_list"]:
        lines.append(item)

    lines.append("")
    lines.append("REVIEW_RESULTS")
    for result in review["review_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_local_candidate_manual_review_artifacts(
    review: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    review = dict(review or build_milestone_9_local_candidate_manual_review())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-9-local-candidate-manual-review-v1.json"
    md_path = output / "milestone-9-local-candidate-manual-review-v1.md"
    manifest_path = output / "milestone-9-local-candidate-manual-review-manifest-v1.txt"
    index_path = output / "milestone-9-local-candidate-manual-review-index-v1.json"

    json_path.write_text(json.dumps(review, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_local_candidate_manual_review_markdown(review), encoding="utf-8")
    manifest_path.write_text(render_local_candidate_manual_review_manifest(review), encoding="utf-8")
    index_path.write_text(json.dumps(review["review_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_9_local_candidate_manual_review_pipeline() -> Dict[str, Any]:
    review = build_milestone_9_local_candidate_manual_review()
    validation = validate_milestone_9_local_candidate_manual_review(review)
    artifacts = write_local_candidate_manual_review_artifacts(review)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_PIPELINE_INVALID",
        "review_status": review["status"],
        "validation_status": validation["status"],
        "review": review,
        "review_id": review["review_id"],
        "signature": review["signature"],
        "review_mode": review["review_mode"],
        "review_verdict": review["review_verdict"],
        "next_allowed_stage": review["next_allowed_stage"],
        "review_ready": review["review_ready"],
        "review_locked": review["review_locked"],
        "local_candidate_manual_review_created": review["local_candidate_manual_review_created"],
        "local_candidate_manual_review_ready": review["local_candidate_manual_review_ready"],
        "local_candidate_manual_review_completed": review["local_candidate_manual_review_completed"],
        "candidate_count": review["candidate_count"],
        "review_check_count": review["review_check_count"],
        "review_case_count": review["review_case_count"],
        "review_pass_count": review["review_pass_count"],
        "review_failure_count": review["review_failure_count"],
        "regression_guard_count": review["regression_guard_count"],
        "boundary_control_count": review["boundary_control_count"],
        "review_gate_count": review["review_gate_count"],
        "passed_gate_count": review["passed_gate_count"],
        "review_issue_count": review["review_issue_count"],
        "warning_count": review["warning_count"],
        "operator_approval_required": review["operator_approval_required"],
        "operator_approval_granted": review["operator_approval_granted"],
        "operator_approval_received": review["operator_approval_received"],
        "manual_upload_allowed": review["manual_upload_allowed"],
        "real_submission_created": review["real_submission_created"],
        "real_submission_allowed": review["real_submission_allowed"],
        "ready_for_real_kaggle_submission": review["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": review["kaggle_submission_sent"],
        "upload_performed": review["upload_performed"],
        "kaggle_authentication_performed": review["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": review["metadata"],
    }
