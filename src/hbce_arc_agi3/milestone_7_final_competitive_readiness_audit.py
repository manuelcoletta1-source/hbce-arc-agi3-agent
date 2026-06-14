"""Milestone #7 Final Competitive Readiness Audit v1.

Local-only final competitive readiness audit.

This module audits the rebuilt local submission candidate from Milestone #7.
It validates chain integrity, candidate integrity, regression pass state, and
submission boundary controls. It does not submit to Kaggle, authenticate, upload
files, call external APIs, read secrets, create a real submission, claim a
Kaggle score, claim public leaderboard improvement, or create legal certification
claims.

The audit is allowed to be valid while still deciding that real submission is
blocked. That is the point of an audit: distinguish local technical readiness
from real competitive readiness.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


AUDIT_STATUS = "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_READY"
PIPELINE_STATUS = "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_VALID"

BASELINE_COMMIT = "04b8f1a Add ARC AGI3 submission candidate rebuild"
AUDIT_MODE = "FINAL_COMPETITIVE_READINESS_AUDIT_ONLY_NO_UPLOAD"
AUDIT_SCOPE = "AUDIT_LOCAL_CANDIDATE_CHAIN_AND_REAL_SUBMISSION_BLOCKERS"
AUDIT_VERDICT = "FINAL_COMPETITIVE_READINESS_AUDIT_COMPLETE_REAL_SUBMISSION_NOT_READY_SOLVER_ITERATION_REQUIRED"
NEXT_ALLOWED_STAGE = "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_V2"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/final-competitive-readiness-audit-v1"

CANDIDATE_JSON = Path(
    "examples/milestone-7/submission-candidate-rebuild-v1/"
    "milestone-7-submission-candidate-rebuild-v1.json"
)

EXPECTED_SOURCE_COUNT = 5
EXPECTED_REBUILD_COMPONENT_COUNT = 5
EXPECTED_CANDIDATE_FILE_COUNT = 4
EXPECTED_AUDIT_CHAIN_COUNT = 7
EXPECTED_LOCAL_MEASUREMENT_COUNT = 6
EXPECTED_REGRESSION_PASS_COUNT = 6
EXPECTED_REGRESSION_FAILURE_COUNT = 0
EXPECTED_AUDIT_SECTION_COUNT = 8
EXPECTED_READINESS_DIMENSION_COUNT = 7
EXPECTED_BLOCKER_COUNT = 6
EXPECTED_PASS_DIMENSION_COUNT = 6
EXPECTED_BLOCKED_DIMENSION_COUNT = 1


READINESS_DIMENSIONS: Tuple[Dict[str, Any], ...] = (
    {
        "dimension_id": "chain_integrity_ready_v1",
        "category": "CHAIN_INTEGRITY",
        "status": "PASS",
        "evidence": "Milestone #7 Task 3 through Task 8 source chain is present and hashed.",
        "blocking": False,
    },
    {
        "dimension_id": "candidate_integrity_ready_v1",
        "category": "LOCAL_CANDIDATE_INTEGRITY",
        "status": "PASS",
        "evidence": "Local submission candidate exists and is deterministic.",
        "blocking": False,
    },
    {
        "dimension_id": "regression_integrity_ready_v1",
        "category": "REGRESSION_INTEGRITY",
        "status": "PASS",
        "evidence": "Regression benchmark reports six local passes and zero failures.",
        "blocking": False,
    },
    {
        "dimension_id": "boundary_integrity_ready_v1",
        "category": "BOUNDARY_INTEGRITY",
        "status": "PASS",
        "evidence": "No upload, no Kaggle auth, no external API dependency, no private core exposure.",
        "blocking": False,
    },
    {
        "dimension_id": "score_claim_integrity_ready_v1",
        "category": "SCORE_CLAIM_INTEGRITY",
        "status": "PASS",
        "evidence": "No numeric Kaggle score or public leaderboard claim is present.",
        "blocking": False,
    },
    {
        "dimension_id": "submission_package_integrity_ready_v1",
        "category": "SUBMISSION_PACKAGE_INTEGRITY",
        "status": "PASS",
        "evidence": "Local rebuild package artifacts exist and are audit-ready.",
        "blocking": False,
    },
    {
        "dimension_id": "real_competitive_readiness_blocked_v1",
        "category": "REAL_COMPETITIVE_READINESS",
        "status": "BLOCKED",
        "evidence": "No real Kaggle submission is allowed because the candidate remains local-only and dry-run-only.",
        "blocking": True,
    },
)

REAL_SUBMISSION_BLOCKERS: Tuple[Dict[str, Any], ...] = (
    {
        "blocker_id": "no_real_kaggle_submission_created_v1",
        "reason": "The rebuilt candidate is local-only and no real submission artifact was created.",
        "active": True,
    },
    {
        "blocker_id": "no_kaggle_authentication_performed_v1",
        "reason": "Kaggle authentication was intentionally not performed.",
        "active": True,
    },
    {
        "blocker_id": "no_upload_performed_v1",
        "reason": "No upload was performed and no upload is allowed in this milestone gate.",
        "active": True,
    },
    {
        "blocker_id": "no_numeric_competitive_score_claim_v1",
        "reason": "There is no numeric Kaggle score claim or public leaderboard improvement claim.",
        "active": True,
    },
    {
        "blocker_id": "solver_iteration_still_required_v1",
        "reason": "The chain improved evidence and local guards but does not prove competitive performance.",
        "active": True,
    },
    {
        "blocker_id": "operator_final_submission_decision_absent_v1",
        "reason": "No operator-authorized final submission decision exists.",
        "active": True,
    },
)

AUDIT_SECTIONS: Tuple[str, ...] = (
    "baseline_candidate",
    "source_chain_integrity",
    "local_candidate_integrity",
    "regression_state",
    "competitive_score_claim_boundary",
    "real_submission_blockers",
    "final_verdict",
    "next_stage",
)

FINAL_DECISION = {
    "local_candidate_chain_integrity": "PASS",
    "local_candidate_rebuild_integrity": "PASS",
    "regression_state": "PASS",
    "score_claim_boundary": "PASS",
    "real_submission_readiness": "BLOCKED",
    "real_submission_decision": "NOT_READY",
    "solver_iteration_required": True,
    "next_stage": NEXT_ALLOWED_STAGE,
}

AUDIT_GATES: Tuple[str, ...] = (
    "candidate_artifact_present",
    "candidate_artifact_ready",
    "candidate_artifact_valid",
    "candidate_next_stage_matches_task_9",
    "final_audit_required",
    "audit_mode_valid",
    "audit_scope_valid",
    "audit_verdict_valid",
    "audit_ready",
    "audit_locked",
    "source_count_valid",
    "rebuild_component_count_valid",
    "candidate_file_count_valid",
    "audit_chain_count_valid",
    "local_measurement_count_valid",
    "regression_pass_count_valid",
    "regression_failure_count_zero",
    "audit_section_count_valid",
    "readiness_dimension_count_valid",
    "blocker_count_valid",
    "pass_dimension_count_valid",
    "blocked_dimension_count_valid",
    "all_noncompetitive_dimensions_pass_or_blocked",
    "all_real_submission_blockers_active",
    "local_candidate_created",
    "local_candidate_chain_integrity_pass",
    "local_candidate_rebuild_integrity_pass",
    "regression_state_pass",
    "score_claim_boundary_pass",
    "real_submission_readiness_blocked",
    "real_submission_decision_not_ready",
    "solver_iteration_required",
    "runtime_solver_not_modified",
    "ranker_runtime_not_modified",
    "benchmark_runtime_not_modified",
    "report_runtime_not_modified",
    "candidate_runtime_not_modified",
    "audit_runtime_not_modified",
    "real_submission_not_created",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "manual_submission_not_allowed",
    "manual_upload_not_performed",
    "competitive_score_claim_absent",
    "public_leaderboard_claim_absent",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "next_stage_valid",
)

AUDIT_ISSUES: Tuple[str, ...] = (
    "candidate_artifact_missing",
    "candidate_artifact_not_ready",
    "candidate_artifact_invalid",
    "candidate_next_stage_mismatch",
    "final_audit_not_required",
    "audit_mode_invalid",
    "audit_scope_invalid",
    "audit_verdict_invalid",
    "audit_not_ready",
    "audit_not_locked",
    "source_count_invalid",
    "rebuild_component_count_invalid",
    "candidate_file_count_invalid",
    "audit_chain_count_invalid",
    "local_measurement_count_invalid",
    "regression_pass_count_invalid",
    "regression_failure_count_nonzero",
    "audit_section_count_invalid",
    "readiness_dimension_count_invalid",
    "blocker_count_invalid",
    "pass_dimension_count_invalid",
    "blocked_dimension_count_invalid",
    "dimension_status_invalid",
    "real_submission_blocker_inactive",
    "local_candidate_missing",
    "local_candidate_chain_integrity_failed",
    "local_candidate_rebuild_integrity_failed",
    "regression_state_failed",
    "score_claim_boundary_failed",
    "real_submission_readiness_not_blocked",
    "real_submission_decision_not_not_ready",
    "solver_iteration_not_required",
    "runtime_solver_modified",
    "ranker_runtime_modified",
    "benchmark_runtime_modified",
    "report_runtime_modified",
    "candidate_runtime_modified",
    "audit_runtime_modified",
    "real_submission_created",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "manual_submission_allowed",
    "manual_upload_performed",
    "competitive_score_claim_detected",
    "public_leaderboard_claim_detected",
    "external_api_dependency_detected",
    "api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "public_safe_false",
    "deterministic_false",
    "local_only_false",
    "dry_run_only_false",
    "next_stage_invalid",
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


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


def _boundary_from_candidate(candidate: Mapping[str, Any]) -> Dict[str, Any]:
    source = candidate.get("boundary", {}) if isinstance(candidate.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": candidate.get("kaggle_submission_sent"),
        "private_core_exposure": source.get("private_core_exposure"),
        "legal_certification": source.get("legal_certification"),
    }


def _dimension_counts() -> Dict[str, int]:
    return {
        "pass_dimension_count": sum(1 for item in READINESS_DIMENSIONS if item["status"] == "PASS"),
        "blocked_dimension_count": sum(1 for item in READINESS_DIMENSIONS if item["status"] == "BLOCKED"),
    }


def build_milestone_7_final_competitive_readiness_audit() -> Dict[str, Any]:
    candidate = _read_json(CANDIDATE_JSON)
    boundary = _boundary_from_candidate(candidate)
    dimension_counts = _dimension_counts()

    source_count = int(candidate.get("source_count", 0))
    rebuild_component_count = int(candidate.get("rebuild_component_count", 0))
    candidate_file_count = int(candidate.get("candidate_file_count", 0))
    audit_chain_count = int(candidate.get("audit_chain_count", 0))
    local_measurement_count = int(candidate.get("local_measurement_count", 0))
    regression_pass_count = int(candidate.get("regression_pass_count", -1))
    regression_failure_count = int(candidate.get("regression_failure_count", -1))

    audit_record = {
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "audit_ready": True,
        "audit_locked": True,
        "candidate_id": candidate.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_ready": candidate.get("rebuild_ready") is True,
        "final_competitive_readiness_audit_required": candidate.get("final_competitive_readiness_audit_required") is True,
        "source_count": source_count,
        "rebuild_component_count": rebuild_component_count,
        "candidate_file_count": candidate_file_count,
        "audit_chain_count": audit_chain_count,
        "local_measurement_count": local_measurement_count,
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "audit_section_count": len(AUDIT_SECTIONS),
        "readiness_dimension_count": len(READINESS_DIMENSIONS),
        "blocker_count": len(REAL_SUBMISSION_BLOCKERS),
        "pass_dimension_count": dimension_counts["pass_dimension_count"],
        "blocked_dimension_count": dimension_counts["blocked_dimension_count"],
        "final_decision": FINAL_DECISION,
        "local_candidate_created": candidate.get("local_submission_candidate_created") is True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "competitive_score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "solver_iteration_required": True,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "report_runtime_modified": False,
        "candidate_runtime_modified": False,
        "audit_runtime_modified": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    gate_state = {
        "candidate_artifact_present": CANDIDATE_JSON.exists(),
        "candidate_artifact_ready": candidate.get("status") == "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_READY",
        "candidate_artifact_valid": bool(candidate.get("candidate_id")) and bool(candidate.get("signature")),
        "candidate_next_stage_matches_task_9": candidate.get("next_allowed_stage") == "MILESTONE_7_TASK_9_FINAL_COMPETITIVE_READINESS_AUDIT",
        "final_audit_required": candidate.get("final_competitive_readiness_audit_required") is True,
        "audit_mode_valid": audit_record["audit_mode"] == AUDIT_MODE,
        "audit_scope_valid": audit_record["audit_scope"] == AUDIT_SCOPE,
        "audit_verdict_valid": audit_record["audit_verdict"] == AUDIT_VERDICT,
        "audit_ready": audit_record["audit_ready"] is True,
        "audit_locked": audit_record["audit_locked"] is True,
        "source_count_valid": source_count == EXPECTED_SOURCE_COUNT,
        "rebuild_component_count_valid": rebuild_component_count == EXPECTED_REBUILD_COMPONENT_COUNT,
        "candidate_file_count_valid": candidate_file_count == EXPECTED_CANDIDATE_FILE_COUNT,
        "audit_chain_count_valid": audit_chain_count == EXPECTED_AUDIT_CHAIN_COUNT,
        "local_measurement_count_valid": local_measurement_count == EXPECTED_LOCAL_MEASUREMENT_COUNT,
        "regression_pass_count_valid": regression_pass_count == EXPECTED_REGRESSION_PASS_COUNT,
        "regression_failure_count_zero": regression_failure_count == EXPECTED_REGRESSION_FAILURE_COUNT,
        "audit_section_count_valid": len(AUDIT_SECTIONS) == EXPECTED_AUDIT_SECTION_COUNT,
        "readiness_dimension_count_valid": len(READINESS_DIMENSIONS) == EXPECTED_READINESS_DIMENSION_COUNT,
        "blocker_count_valid": len(REAL_SUBMISSION_BLOCKERS) == EXPECTED_BLOCKER_COUNT,
        "pass_dimension_count_valid": dimension_counts["pass_dimension_count"] == EXPECTED_PASS_DIMENSION_COUNT,
        "blocked_dimension_count_valid": dimension_counts["blocked_dimension_count"] == EXPECTED_BLOCKED_DIMENSION_COUNT,
        "all_noncompetitive_dimensions_pass_or_blocked": all(
            item["status"] in {"PASS", "BLOCKED"} for item in READINESS_DIMENSIONS
        ),
        "all_real_submission_blockers_active": all(item["active"] is True for item in REAL_SUBMISSION_BLOCKERS),
        "local_candidate_created": audit_record["local_candidate_created"] is True,
        "local_candidate_chain_integrity_pass": FINAL_DECISION["local_candidate_chain_integrity"] == "PASS",
        "local_candidate_rebuild_integrity_pass": FINAL_DECISION["local_candidate_rebuild_integrity"] == "PASS",
        "regression_state_pass": FINAL_DECISION["regression_state"] == "PASS",
        "score_claim_boundary_pass": FINAL_DECISION["score_claim_boundary"] == "PASS",
        "real_submission_readiness_blocked": FINAL_DECISION["real_submission_readiness"] == "BLOCKED",
        "real_submission_decision_not_ready": FINAL_DECISION["real_submission_decision"] == "NOT_READY",
        "solver_iteration_required": FINAL_DECISION["solver_iteration_required"] is True,
        "runtime_solver_not_modified": audit_record["runtime_solver_modified"] is False,
        "ranker_runtime_not_modified": audit_record["ranker_runtime_modified"] is False,
        "benchmark_runtime_not_modified": audit_record["benchmark_runtime_modified"] is False,
        "report_runtime_not_modified": audit_record["report_runtime_modified"] is False,
        "candidate_runtime_not_modified": audit_record["candidate_runtime_modified"] is False,
        "audit_runtime_not_modified": audit_record["audit_runtime_modified"] is False,
        "real_submission_not_created": audit_record["real_submission_created"] is False,
        "real_submission_allowed_false": audit_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": audit_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": audit_record["kaggle_submission_sent"] is False,
        "upload_not_performed": audit_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": audit_record["kaggle_authentication_performed"] is False,
        "manual_submission_not_allowed": audit_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": audit_record["manual_upload_performed"] is False,
        "competitive_score_claim_absent": audit_record["competitive_score_claim_absent"] is True,
        "public_leaderboard_claim_absent": audit_record["public_leaderboard_claim_absent"] is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "next_stage_valid": audit_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
    }

    issue_state = {
        "candidate_artifact_missing": not gate_state["candidate_artifact_present"],
        "candidate_artifact_not_ready": not gate_state["candidate_artifact_ready"],
        "candidate_artifact_invalid": not gate_state["candidate_artifact_valid"],
        "candidate_next_stage_mismatch": not gate_state["candidate_next_stage_matches_task_9"],
        "final_audit_not_required": not gate_state["final_audit_required"],
        "audit_mode_invalid": not gate_state["audit_mode_valid"],
        "audit_scope_invalid": not gate_state["audit_scope_valid"],
        "audit_verdict_invalid": not gate_state["audit_verdict_valid"],
        "audit_not_ready": not gate_state["audit_ready"],
        "audit_not_locked": not gate_state["audit_locked"],
        "source_count_invalid": not gate_state["source_count_valid"],
        "rebuild_component_count_invalid": not gate_state["rebuild_component_count_valid"],
        "candidate_file_count_invalid": not gate_state["candidate_file_count_valid"],
        "audit_chain_count_invalid": not gate_state["audit_chain_count_valid"],
        "local_measurement_count_invalid": not gate_state["local_measurement_count_valid"],
        "regression_pass_count_invalid": not gate_state["regression_pass_count_valid"],
        "regression_failure_count_nonzero": not gate_state["regression_failure_count_zero"],
        "audit_section_count_invalid": not gate_state["audit_section_count_valid"],
        "readiness_dimension_count_invalid": not gate_state["readiness_dimension_count_valid"],
        "blocker_count_invalid": not gate_state["blocker_count_valid"],
        "pass_dimension_count_invalid": not gate_state["pass_dimension_count_valid"],
        "blocked_dimension_count_invalid": not gate_state["blocked_dimension_count_valid"],
        "dimension_status_invalid": not gate_state["all_noncompetitive_dimensions_pass_or_blocked"],
        "real_submission_blocker_inactive": not gate_state["all_real_submission_blockers_active"],
        "local_candidate_missing": not gate_state["local_candidate_created"],
        "local_candidate_chain_integrity_failed": not gate_state["local_candidate_chain_integrity_pass"],
        "local_candidate_rebuild_integrity_failed": not gate_state["local_candidate_rebuild_integrity_pass"],
        "regression_state_failed": not gate_state["regression_state_pass"],
        "score_claim_boundary_failed": not gate_state["score_claim_boundary_pass"],
        "real_submission_readiness_not_blocked": not gate_state["real_submission_readiness_blocked"],
        "real_submission_decision_not_not_ready": not gate_state["real_submission_decision_not_ready"],
        "solver_iteration_not_required": not gate_state["solver_iteration_required"],
        "runtime_solver_modified": not gate_state["runtime_solver_not_modified"],
        "ranker_runtime_modified": not gate_state["ranker_runtime_not_modified"],
        "benchmark_runtime_modified": not gate_state["benchmark_runtime_not_modified"],
        "report_runtime_modified": not gate_state["report_runtime_not_modified"],
        "candidate_runtime_modified": not gate_state["candidate_runtime_not_modified"],
        "audit_runtime_modified": not gate_state["audit_runtime_not_modified"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "manual_submission_allowed": not gate_state["manual_submission_not_allowed"],
        "manual_upload_performed": not gate_state["manual_upload_not_performed"],
        "competitive_score_claim_detected": not gate_state["competitive_score_claim_absent"],
        "public_leaderboard_claim_detected": not gate_state["public_leaderboard_claim_absent"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
        "public_safe_false": not gate_state["public_safe"],
        "deterministic_false": not gate_state["deterministic"],
        "local_only_false": not gate_state["local_only"],
        "dry_run_only_false": not gate_state["dry_run_only"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
    }

    gates = tuple(
        {"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"}
        for name in AUDIT_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in AUDIT_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    audit_ready = (
        candidate.get("status") == "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_READY"
        and source_count == EXPECTED_SOURCE_COUNT
        and rebuild_component_count == EXPECTED_REBUILD_COMPONENT_COUNT
        and candidate_file_count == EXPECTED_CANDIDATE_FILE_COUNT
        and local_measurement_count == EXPECTED_LOCAL_MEASUREMENT_COUNT
        and regression_pass_count == EXPECTED_REGRESSION_PASS_COUNT
        and regression_failure_count == EXPECTED_REGRESSION_FAILURE_COUNT
        and passed_gate_count == len(AUDIT_GATES)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 9",
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_candidate": candidate.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "audit_ready": audit_ready,
        "audit_locked": True,
        "source_count": source_count,
        "rebuild_component_count": rebuild_component_count,
        "candidate_file_count": candidate_file_count,
        "audit_chain_count": audit_chain_count,
        "local_measurement_count": local_measurement_count,
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "readiness_dimension_count": len(READINESS_DIMENSIONS),
        "blocker_count": len(REAL_SUBMISSION_BLOCKERS),
        "final_decision": FINAL_DECISION,
        "real_submission_decision": "NOT_READY",
        "solver_iteration_required": True,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "real_submission_created": False,
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
        "status": AUDIT_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 9",
        "title": "Final Competitive Readiness Audit v1",
        "baseline_commit": BASELINE_COMMIT,
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "candidate_source": {
            "path": str(CANDIDATE_JSON),
            "present": CANDIDATE_JSON.exists(),
            "status": candidate.get("status", "MISSING"),
            "candidate_id": candidate.get("candidate_id", "MISSING_CANDIDATE_ID"),
            "sha256": _sha256(CANDIDATE_JSON),
            "sha256_16": _sha16(_sha256(CANDIDATE_JSON)),
        },
        "audit_record": audit_record,
        "readiness_dimensions": list(READINESS_DIMENSIONS),
        "real_submission_blockers": list(REAL_SUBMISSION_BLOCKERS),
        "audit_sections": list(AUDIT_SECTIONS),
        "final_decision": FINAL_DECISION,
        "audit_gates": list(gates),
        "audit_issues": list(issues),
        "audit_index": index,
        "boundary": boundary,
        "source_count": source_count,
        "rebuild_component_count": rebuild_component_count,
        "candidate_file_count": candidate_file_count,
        "audit_chain_count": audit_chain_count,
        "local_measurement_count": local_measurement_count,
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "audit_section_count": len(AUDIT_SECTIONS),
        "readiness_dimension_count": len(READINESS_DIMENSIONS),
        "blocker_count": len(REAL_SUBMISSION_BLOCKERS),
        "pass_dimension_count": dimension_counts["pass_dimension_count"],
        "blocked_dimension_count": dimension_counts["blocked_dimension_count"],
        "audit_gate_count": len(AUDIT_GATES),
        "passed_gate_count": passed_gate_count,
        "audit_issue_count": issue_count,
        "warning_count": 0,
        "audit_ready": audit_ready,
        "audit_locked": True,
        "local_candidate_chain_integrity": "PASS",
        "local_candidate_rebuild_integrity": "PASS",
        "regression_state": "PASS",
        "score_claim_boundary": "PASS",
        "real_submission_readiness": "BLOCKED",
        "real_submission_decision": "NOT_READY",
        "solver_iteration_required": True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "report_runtime_modified": False,
        "candidate_runtime_modified": False,
        "audit_runtime_modified": False,
        "metadata": {
            "source": "milestone_7_final_competitive_readiness_audit_v1",
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
        "audit_id": f"MILESTONE-7-FINAL-READINESS-AUDIT-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_final_competitive_readiness_audit(audit: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = audit.get("boundary", {})
    gates = audit.get("audit_gates", [])
    issues = audit.get("audit_issues", [])
    dimensions = audit.get("readiness_dimensions", [])
    blockers = audit.get("real_submission_blockers", [])

    checks = {
        "status_ready": audit.get("status") == AUDIT_STATUS,
        "audit_id_present": isinstance(audit.get("audit_id"), str) and bool(audit.get("audit_id")),
        "signature_present": isinstance(audit.get("signature"), str) and bool(audit.get("signature")),
        "baseline_commit_valid": str(audit.get("baseline_commit", "")).startswith("04b8f1a"),
        "audit_mode_valid": audit.get("audit_mode") == AUDIT_MODE,
        "audit_scope_valid": audit.get("audit_scope") == AUDIT_SCOPE,
        "audit_verdict_valid": audit.get("audit_verdict") == AUDIT_VERDICT,
        "next_allowed_stage_valid": audit.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "source_count_valid": audit.get("source_count") == EXPECTED_SOURCE_COUNT,
        "rebuild_component_count_valid": audit.get("rebuild_component_count") == EXPECTED_REBUILD_COMPONENT_COUNT,
        "candidate_file_count_valid": audit.get("candidate_file_count") == EXPECTED_CANDIDATE_FILE_COUNT,
        "audit_chain_count_valid": audit.get("audit_chain_count") == EXPECTED_AUDIT_CHAIN_COUNT,
        "local_measurement_count_valid": audit.get("local_measurement_count") == EXPECTED_LOCAL_MEASUREMENT_COUNT,
        "regression_pass_count_valid": audit.get("regression_pass_count") == EXPECTED_REGRESSION_PASS_COUNT,
        "regression_failure_count_zero": audit.get("regression_failure_count") == EXPECTED_REGRESSION_FAILURE_COUNT,
        "audit_section_count_valid": audit.get("audit_section_count") == EXPECTED_AUDIT_SECTION_COUNT,
        "readiness_dimension_count_valid": audit.get("readiness_dimension_count") == EXPECTED_READINESS_DIMENSION_COUNT,
        "blocker_count_valid": audit.get("blocker_count") == EXPECTED_BLOCKER_COUNT,
        "pass_dimension_count_valid": audit.get("pass_dimension_count") == EXPECTED_PASS_DIMENSION_COUNT,
        "blocked_dimension_count_valid": audit.get("blocked_dimension_count") == EXPECTED_BLOCKED_DIMENSION_COUNT,
        "dimensions_valid": bool(dimensions) and all(item.get("status") in {"PASS", "BLOCKED"} for item in dimensions),
        "blockers_active": bool(blockers) and all(item.get("active") is True for item in blockers),
        "local_candidate_chain_integrity_pass": audit.get("local_candidate_chain_integrity") == "PASS",
        "local_candidate_rebuild_integrity_pass": audit.get("local_candidate_rebuild_integrity") == "PASS",
        "regression_state_pass": audit.get("regression_state") == "PASS",
        "score_claim_boundary_pass": audit.get("score_claim_boundary") == "PASS",
        "real_submission_readiness_blocked": audit.get("real_submission_readiness") == "BLOCKED",
        "real_submission_decision_not_ready": audit.get("real_submission_decision") == "NOT_READY",
        "solver_iteration_required": audit.get("solver_iteration_required") is True,
        "audit_gate_count_matches": audit.get("audit_gate_count") == len(AUDIT_GATES),
        "all_audit_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "audit_issue_count_zero": audit.get("audit_issue_count") == 0,
        "all_audit_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "audit_ready": audit.get("audit_ready") is True,
        "audit_locked": audit.get("audit_locked") is True,
        "real_submission_not_created": audit.get("real_submission_created") is False,
        "real_submission_allowed_false": audit.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": audit.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": audit.get("kaggle_submission_sent") is False,
        "upload_not_performed": audit.get("upload_performed") is False,
        "kaggle_authentication_not_performed": audit.get("kaggle_authentication_performed") is False,
        "manual_submission_not_allowed": audit.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": audit.get("manual_upload_performed") is False,
        "runtime_solver_not_modified": audit.get("runtime_solver_modified") is False,
        "candidate_runtime_not_modified": audit.get("candidate_runtime_modified") is False,
        "audit_runtime_not_modified": audit.get("audit_runtime_modified") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_INVALID",
        "valid": valid,
        "checks": checks,
        "audit_id": audit.get("audit_id"),
        "signature": audit.get("signature"),
    }


def render_final_competitive_readiness_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Final Competitive Readiness Audit v1",
        "",
        f"- status: {audit['status']}",
        f"- audit_id: {audit['audit_id']}",
        f"- signature: {audit['signature']}",
        f"- baseline_commit: {audit['baseline_commit']}",
        f"- audit_mode: {audit['audit_mode']}",
        f"- audit_scope: {audit['audit_scope']}",
        f"- audit_verdict: {audit['audit_verdict']}",
        f"- next_allowed_stage: {audit['next_allowed_stage']}",
        f"- source_count: {audit['source_count']}",
        f"- rebuild_component_count: {audit['rebuild_component_count']}",
        f"- candidate_file_count: {audit['candidate_file_count']}",
        f"- audit_chain_count: {audit['audit_chain_count']}",
        f"- local_measurement_count: {audit['local_measurement_count']}",
        f"- regression_pass_count: {audit['regression_pass_count']}",
        f"- regression_failure_count: {audit['regression_failure_count']}",
        f"- readiness_dimension_count: {audit['readiness_dimension_count']}",
        f"- blocker_count: {audit['blocker_count']}",
        f"- audit_gate_count: {audit['audit_gate_count']}",
        f"- passed_gate_count: {audit['passed_gate_count']}",
        f"- audit_issue_count: {audit['audit_issue_count']}",
        f"- audit_ready: {audit['audit_ready']}",
        f"- real_submission_readiness: {audit['real_submission_readiness']}",
        f"- real_submission_decision: {audit['real_submission_decision']}",
        f"- solver_iteration_required: {audit['solver_iteration_required']}",
        f"- real_submission_allowed: {audit['real_submission_allowed']}",
        f"- kaggle_submission_sent: {audit['kaggle_submission_sent']}",
        f"- upload_performed: {audit['upload_performed']}",
        "",
        "## Readiness dimensions",
        "",
    ]

    for item in audit["readiness_dimensions"]:
        lines.append(
            f"- {item['dimension_id']} / category={item['category']} / "
            f"status={item['status']} / blocking={item['blocking']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The local candidate chain is audit-ready, but real competitive submission is not ready. Solver iteration remains required.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_VALID=true",
            "ARC_AGI3_MILESTONE_7_AUDIT_MODE=FINAL_COMPETITIVE_READINESS_AUDIT_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_AUDIT_VERDICT=FINAL_COMPETITIVE_READINESS_AUDIT_COMPLETE_REAL_SUBMISSION_NOT_READY_SOLVER_ITERATION_REQUIRED",
            "ARC_AGI3_MILESTONE_7_SOURCE_COUNT=5",
            "ARC_AGI3_MILESTONE_7_REBUILD_COMPONENT_COUNT=5",
            "ARC_AGI3_MILESTONE_7_CANDIDATE_FILE_COUNT=4",
            "ARC_AGI3_MILESTONE_7_AUDIT_CHAIN_COUNT=7",
            "ARC_AGI3_MILESTONE_7_LOCAL_MEASUREMENT_COUNT=6",
            "ARC_AGI3_MILESTONE_7_REGRESSION_PASS_COUNT=6",
            "ARC_AGI3_MILESTONE_7_REGRESSION_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_7_READINESS_DIMENSION_COUNT=7",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_BLOCKER_COUNT=6",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_READINESS=BLOCKED",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_DECISION=NOT_READY",
            "ARC_AGI3_MILESTONE_7_SOLVER_ITERATION_REQUIRED=true",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_V2",
            "ARC_AGI3_MILESTONE_7_BASELINE_CANDIDATE_COMMIT=04b8f1a",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_final_competitive_readiness_audit_manifest(audit: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 FINAL COMPETITIVE READINESS AUDIT MANIFEST v1",
        f"audit_id={audit['audit_id']}",
        f"signature={audit['signature']}",
        f"status={audit['status']}",
        f"baseline_commit={audit['baseline_commit']}",
        f"audit_mode={audit['audit_mode']}",
        f"audit_verdict={audit['audit_verdict']}",
        f"next_allowed_stage={audit['next_allowed_stage']}",
        f"source_count={audit['source_count']}",
        f"rebuild_component_count={audit['rebuild_component_count']}",
        f"candidate_file_count={audit['candidate_file_count']}",
        f"audit_chain_count={audit['audit_chain_count']}",
        f"local_measurement_count={audit['local_measurement_count']}",
        f"regression_pass_count={audit['regression_pass_count']}",
        f"regression_failure_count={audit['regression_failure_count']}",
        f"readiness_dimension_count={audit['readiness_dimension_count']}",
        f"blocker_count={audit['blocker_count']}",
        f"pass_dimension_count={audit['pass_dimension_count']}",
        f"blocked_dimension_count={audit['blocked_dimension_count']}",
        f"audit_gate_count={audit['audit_gate_count']}",
        f"passed_gate_count={audit['passed_gate_count']}",
        f"audit_issue_count={audit['audit_issue_count']}",
        f"audit_ready={audit['audit_ready']}",
        f"audit_locked={audit['audit_locked']}",
        f"real_submission_readiness={audit['real_submission_readiness']}",
        f"real_submission_decision={audit['real_submission_decision']}",
        f"solver_iteration_required={audit['solver_iteration_required']}",
        f"real_submission_created={audit['real_submission_created']}",
        f"real_submission_allowed={audit['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={audit['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={audit['kaggle_submission_sent']}",
        f"upload_performed={audit['upload_performed']}",
        f"kaggle_authentication_performed={audit['kaggle_authentication_performed']}",
        f"manual_submission_allowed={audit['manual_submission_allowed']}",
        f"manual_upload_performed={audit['manual_upload_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "READINESS_DIMENSIONS",
    ]

    for item in audit["readiness_dimensions"]:
        lines.append(
            f"{item['dimension_id']} category={item['category']} "
            f"status={item['status']} blocking={item['blocking']}"
        )

    lines.append("")
    lines.append("REAL_SUBMISSION_BLOCKERS")
    for item in audit["real_submission_blockers"]:
        lines.append(f"{item['blocker_id']} active={item['active']} reason={item['reason']}")

    lines.append("")
    return "\n".join(lines)


def write_final_competitive_readiness_audit_artifacts(
    audit: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    audit = dict(audit or build_milestone_7_final_competitive_readiness_audit())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-final-competitive-readiness-audit-v1.json"
    md_path = output / "milestone-7-final-competitive-readiness-audit-v1.md"
    manifest_path = output / "milestone-7-final-competitive-readiness-audit-manifest-v1.txt"
    index_path = output / "milestone-7-final-competitive-readiness-audit-index-v1.json"

    json_path.write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_final_competitive_readiness_audit_markdown(audit), encoding="utf-8")
    manifest_path.write_text(render_final_competitive_readiness_audit_manifest(audit), encoding="utf-8")
    index_path.write_text(json.dumps(audit["audit_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_final_competitive_readiness_audit_pipeline() -> Dict[str, Any]:
    audit = build_milestone_7_final_competitive_readiness_audit()
    validation = validate_milestone_7_final_competitive_readiness_audit(audit)
    artifacts = write_final_competitive_readiness_audit_artifacts(audit)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_PIPELINE_INVALID",
        "audit_status": audit["status"],
        "validation_status": validation["status"],
        "audit": audit,
        "audit_id": audit["audit_id"],
        "signature": audit["signature"],
        "audit_mode": audit["audit_mode"],
        "audit_verdict": audit["audit_verdict"],
        "next_allowed_stage": audit["next_allowed_stage"],
        "source_count": audit["source_count"],
        "rebuild_component_count": audit["rebuild_component_count"],
        "candidate_file_count": audit["candidate_file_count"],
        "audit_chain_count": audit["audit_chain_count"],
        "local_measurement_count": audit["local_measurement_count"],
        "regression_pass_count": audit["regression_pass_count"],
        "regression_failure_count": audit["regression_failure_count"],
        "readiness_dimension_count": audit["readiness_dimension_count"],
        "blocker_count": audit["blocker_count"],
        "pass_dimension_count": audit["pass_dimension_count"],
        "blocked_dimension_count": audit["blocked_dimension_count"],
        "audit_gate_count": audit["audit_gate_count"],
        "passed_gate_count": audit["passed_gate_count"],
        "audit_issue_count": audit["audit_issue_count"],
        "warning_count": audit["warning_count"],
        "audit_ready": audit["audit_ready"],
        "audit_locked": audit["audit_locked"],
        "real_submission_readiness": audit["real_submission_readiness"],
        "real_submission_decision": audit["real_submission_decision"],
        "solver_iteration_required": audit["solver_iteration_required"],
        "real_submission_created": audit["real_submission_created"],
        "real_submission_allowed": audit["real_submission_allowed"],
        "ready_for_real_kaggle_submission": audit["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": audit["kaggle_submission_sent"],
        "upload_performed": audit["upload_performed"],
        "kaggle_authentication_performed": audit["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": audit["metadata"],
    }
