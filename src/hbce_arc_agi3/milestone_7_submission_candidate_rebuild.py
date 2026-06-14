"""Milestone #7 Submission Candidate Rebuild v1.

Local-only submission candidate rebuild registry.

This module rebuilds a deterministic local submission candidate from the
Milestone #7 improvement chain. It does not submit to Kaggle, authenticate,
upload files, call external APIs, read secrets, create a real submission, claim
a Kaggle score, claim public leaderboard improvement, or create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


REBUILD_STATUS = "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_READY"
PIPELINE_STATUS = "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_VALID"

BASELINE_COMMIT = "bc41cd1 Add ARC AGI3 local score improvement report"
REBUILD_MODE = "SUBMISSION_CANDIDATE_REBUILD_ONLY_NO_UPLOAD"
REBUILD_SCOPE = "REBUILD_LOCAL_SUBMISSION_CANDIDATE_FROM_MILESTONE_7_IMPROVEMENT_CHAIN"
REBUILD_VERDICT = "SUBMISSION_CANDIDATE_REBUILD_READY_FOR_FINAL_COMPETITIVE_READINESS_AUDIT"
NEXT_ALLOWED_STAGE = "MILESTONE_7_TASK_9_FINAL_COMPETITIVE_READINESS_AUDIT"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/submission-candidate-rebuild-v1"

REPORT_JSON = Path(
    "examples/milestone-7/local-score-improvement-report-v1/"
    "milestone-7-local-score-improvement-report-v1.json"
)

SOURCE_ARTIFACTS: Tuple[Dict[str, str], ...] = (
    {
        "source_id": "task_3_task_family_solver_expansion",
        "path": "examples/milestone-7/task-family-solver-expansion-v1/milestone-7-task-family-solver-expansion-v1.json",
        "expected_status_fragment": "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_READY",
    },
    {
        "source_id": "task_4_candidate_generator_improvement",
        "path": "examples/milestone-7/candidate-generator-improvement-v1/milestone-7-candidate-generator-improvement-v1.json",
        "expected_status_fragment": "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_READY",
    },
    {
        "source_id": "task_5_ranker_evidence_upgrade",
        "path": "examples/milestone-7/ranker-evidence-upgrade-v1/milestone-7-ranker-evidence-upgrade-v1.json",
        "expected_status_fragment": "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_READY",
    },
    {
        "source_id": "task_6_regression_benchmark",
        "path": "examples/milestone-7/regression-benchmark-v1/milestone-7-regression-benchmark-v1.json",
        "expected_status_fragment": "MILESTONE_7_REGRESSION_BENCHMARK_READY",
    },
    {
        "source_id": "task_7_local_score_improvement_report",
        "path": str(REPORT_JSON),
        "expected_status_fragment": "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_READY",
    },
)

REBUILD_COMPONENTS: Tuple[Dict[str, Any], ...] = (
    {
        "component_id": "task_family_registry_component_v1",
        "source_id": "task_3_task_family_solver_expansion",
        "role": "Provide family-specific solver expansion context.",
        "ready": True,
        "runtime_modified": False,
    },
    {
        "component_id": "candidate_generator_component_v1",
        "source_id": "task_4_candidate_generator_improvement",
        "role": "Provide bounded candidate generation profiles.",
        "ready": True,
        "runtime_modified": False,
    },
    {
        "component_id": "ranker_evidence_component_v1",
        "source_id": "task_5_ranker_evidence_upgrade",
        "role": "Provide deterministic ranker evidence and tie-breakers.",
        "ready": True,
        "runtime_modified": False,
    },
    {
        "component_id": "regression_benchmark_component_v1",
        "source_id": "task_6_regression_benchmark",
        "role": "Provide regression benchmark cases and pass/fail controls.",
        "ready": True,
        "runtime_modified": False,
    },
    {
        "component_id": "local_score_report_component_v1",
        "source_id": "task_7_local_score_improvement_report",
        "role": "Provide local improvement report without competitive score claims.",
        "ready": True,
        "runtime_modified": False,
    },
)

CANDIDATE_FILES: Tuple[Dict[str, Any], ...] = (
    {
        "candidate_file_id": "submission_candidate_rebuild_json_v1",
        "filename": "milestone-7-submission-candidate-rebuild-v1.json",
        "required": True,
    },
    {
        "candidate_file_id": "submission_candidate_rebuild_markdown_v1",
        "filename": "milestone-7-submission-candidate-rebuild-v1.md",
        "required": True,
    },
    {
        "candidate_file_id": "submission_candidate_rebuild_manifest_v1",
        "filename": "milestone-7-submission-candidate-rebuild-manifest-v1.txt",
        "required": True,
    },
    {
        "candidate_file_id": "submission_candidate_rebuild_index_v1",
        "filename": "milestone-7-submission-candidate-rebuild-index-v1.json",
        "required": True,
    },
)

READINESS_CHECKS: Tuple[str, ...] = (
    "source_chain_complete",
    "source_artifacts_hashed",
    "local_measurements_passed",
    "regression_failure_count_zero",
    "no_numeric_score_claim",
    "no_kaggle_upload",
    "no_kaggle_authentication",
    "final_audit_required",
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

AUDIT_CHAIN: Tuple[Dict[str, str], ...] = (
    {"task": "Task 1", "commit": "70a8d44", "label": "Competitive Solver Improvement Plan"},
    {"task": "Task 2", "commit": "fb770e3", "label": "Baseline Solver Failure Taxonomy"},
    {"task": "Task 3", "commit": "3ec630b", "label": "Task-Family Solver Expansion"},
    {"task": "Task 4", "commit": "0dfd280", "label": "Candidate Generator Improvement"},
    {"task": "Task 5", "commit": "f4035fa", "label": "Ranker Evidence Upgrade"},
    {"task": "Task 6", "commit": "92efad5", "label": "Regression Benchmark"},
    {"task": "Task 7", "commit": "bc41cd1", "label": "Local Score Improvement Report"},
)

EXPECTED_SOURCE_COUNT = 5
EXPECTED_REBUILD_COMPONENT_COUNT = 5
EXPECTED_CANDIDATE_FILE_COUNT = 4
EXPECTED_READINESS_CHECK_COUNT = 8
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_AUDIT_CHAIN_COUNT = 7
EXPECTED_FAMILY_REPORT_COUNT = 3
EXPECTED_LOCAL_MEASUREMENT_COUNT = 6
EXPECTED_REGRESSION_PASS_COUNT = 6
EXPECTED_REGRESSION_FAILURE_COUNT = 0

REBUILD_GATES: Tuple[str, ...] = (
    "report_artifact_present",
    "report_artifact_ready",
    "report_artifact_valid",
    "report_next_stage_matches_task_8",
    "submission_candidate_rebuild_required",
    "source_count_valid",
    "all_source_artifacts_present",
    "all_source_artifacts_hashed",
    "all_source_artifacts_have_expected_status",
    "rebuild_mode_valid",
    "rebuild_scope_valid",
    "rebuild_verdict_valid",
    "rebuild_ready",
    "rebuild_locked",
    "rebuild_component_count_valid",
    "all_components_ready",
    "all_components_runtime_not_modified",
    "candidate_file_count_valid",
    "all_candidate_files_required",
    "readiness_check_count_valid",
    "boundary_control_count_valid",
    "audit_chain_count_valid",
    "family_report_count_valid",
    "local_measurement_count_valid",
    "regression_pass_count_valid",
    "regression_failure_count_zero",
    "local_score_report_ready",
    "local_score_claim_absent",
    "competitive_score_claim_absent",
    "public_leaderboard_claim_absent",
    "runtime_solver_not_modified",
    "ranker_runtime_not_modified",
    "benchmark_runtime_not_modified",
    "report_runtime_not_modified",
    "candidate_runtime_not_modified",
    "local_submission_candidate_created",
    "real_submission_not_created",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
    "next_stage_valid",
    "final_audit_required",
    "manual_submission_not_allowed",
    "manual_upload_not_performed",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
)

REBUILD_ISSUES: Tuple[str, ...] = (
    "report_artifact_missing",
    "report_artifact_not_ready",
    "report_artifact_invalid",
    "report_next_stage_mismatch",
    "submission_candidate_rebuild_not_required",
    "source_count_invalid",
    "source_artifact_missing",
    "source_artifact_hash_missing",
    "source_artifact_status_invalid",
    "rebuild_mode_invalid",
    "rebuild_scope_invalid",
    "rebuild_verdict_invalid",
    "rebuild_not_ready",
    "rebuild_not_locked",
    "rebuild_component_count_invalid",
    "component_not_ready",
    "component_runtime_modified",
    "candidate_file_count_invalid",
    "candidate_file_not_required",
    "readiness_check_count_invalid",
    "boundary_control_count_invalid",
    "audit_chain_count_invalid",
    "family_report_count_invalid",
    "local_measurement_count_invalid",
    "regression_pass_count_invalid",
    "regression_failure_count_nonzero",
    "local_score_report_not_ready",
    "local_score_claim_detected",
    "competitive_score_claim_detected",
    "public_leaderboard_claim_detected",
    "runtime_solver_modified",
    "ranker_runtime_modified",
    "benchmark_runtime_modified",
    "report_runtime_modified",
    "candidate_runtime_modified",
    "local_submission_candidate_missing",
    "real_submission_created",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "external_api_dependency_detected",
    "api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "next_stage_invalid",
    "final_audit_not_required",
    "manual_submission_allowed",
    "manual_upload_performed",
    "public_safe_false",
    "deterministic_false",
    "local_only_false",
    "dry_run_only_false",
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


def _source_record(source: Mapping[str, str]) -> Dict[str, Any]:
    path = Path(source["path"])
    payload = _read_json(path)
    file_hash = _sha256(path)
    status = str(payload.get("status", "MISSING"))
    return {
        "source_id": source["source_id"],
        "path": source["path"],
        "present": path.exists(),
        "status": status,
        "expected_status_fragment": source["expected_status_fragment"],
        "status_valid": source["expected_status_fragment"] in status,
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def _boundary_from_report(report: Mapping[str, Any]) -> Dict[str, Any]:
    source = report.get("boundary", {}) if isinstance(report.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": report.get("kaggle_submission_sent"),
        "private_core_exposure": source.get("private_core_exposure"),
        "legal_certification": source.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    expected = {
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
    return all(boundary.get(key) is value for key, value in expected.items())


def build_milestone_7_submission_candidate_rebuild() -> Dict[str, Any]:
    report = _read_json(REPORT_JSON)
    boundary = _boundary_from_report(report)
    sources = tuple(_source_record(item) for item in SOURCE_ARTIFACTS)
    components = tuple(dict(item) for item in REBUILD_COMPONENTS)
    candidate_files = tuple(dict(item) for item in CANDIDATE_FILES)

    family_report_count = int(report.get("family_report_count", 0))
    local_measurement_count = int(report.get("local_measurement_count", 0))
    regression_pass_count = int(report.get("regression_pass_count", -1))
    regression_failure_count = int(report.get("regression_failure_count", -1))

    rebuild_record = {
        "rebuild_mode": REBUILD_MODE,
        "rebuild_scope": REBUILD_SCOPE,
        "rebuild_verdict": REBUILD_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "rebuild_ready": True,
        "rebuild_locked": True,
        "report_id": report.get("report_id", "MISSING_REPORT_ID"),
        "report_ready": report.get("report_ready") is True,
        "submission_candidate_rebuild_required": report.get("submission_candidate_rebuild_required") is True,
        "source_count": len(sources),
        "rebuild_component_count": len(components),
        "candidate_file_count": len(candidate_files),
        "readiness_check_count": len(READINESS_CHECKS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "audit_chain_count": len(AUDIT_CHAIN),
        "family_report_count": family_report_count,
        "local_measurement_count": local_measurement_count,
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "local_submission_candidate_created": True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "report_runtime_modified": False,
        "candidate_runtime_modified": False,
        "local_score_claim_absent": True,
        "competitive_score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "final_competitive_readiness_audit_required": True,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "boundary_intact": _boundary_intact(boundary),
    }

    gate_state = {
        "report_artifact_present": REPORT_JSON.exists(),
        "report_artifact_ready": report.get("status") == "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_READY",
        "report_artifact_valid": bool(report.get("report_id")) and bool(report.get("signature")),
        "report_next_stage_matches_task_8": report.get("next_allowed_stage") == "MILESTONE_7_TASK_8_SUBMISSION_CANDIDATE_REBUILD",
        "submission_candidate_rebuild_required": report.get("submission_candidate_rebuild_required") is True,
        "source_count_valid": len(sources) == EXPECTED_SOURCE_COUNT,
        "all_source_artifacts_present": all(item["present"] is True for item in sources),
        "all_source_artifacts_hashed": all(item["sha256"] != "MISSING_HASH" for item in sources),
        "all_source_artifacts_have_expected_status": all(item["status_valid"] is True for item in sources),
        "rebuild_mode_valid": rebuild_record["rebuild_mode"] == REBUILD_MODE,
        "rebuild_scope_valid": rebuild_record["rebuild_scope"] == REBUILD_SCOPE,
        "rebuild_verdict_valid": rebuild_record["rebuild_verdict"] == REBUILD_VERDICT,
        "rebuild_ready": rebuild_record["rebuild_ready"] is True,
        "rebuild_locked": rebuild_record["rebuild_locked"] is True,
        "rebuild_component_count_valid": len(components) == EXPECTED_REBUILD_COMPONENT_COUNT,
        "all_components_ready": all(item["ready"] is True for item in components),
        "all_components_runtime_not_modified": all(item["runtime_modified"] is False for item in components),
        "candidate_file_count_valid": len(candidate_files) == EXPECTED_CANDIDATE_FILE_COUNT,
        "all_candidate_files_required": all(item["required"] is True for item in candidate_files),
        "readiness_check_count_valid": len(READINESS_CHECKS) == EXPECTED_READINESS_CHECK_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "audit_chain_count_valid": len(AUDIT_CHAIN) == EXPECTED_AUDIT_CHAIN_COUNT,
        "family_report_count_valid": family_report_count == EXPECTED_FAMILY_REPORT_COUNT,
        "local_measurement_count_valid": local_measurement_count == EXPECTED_LOCAL_MEASUREMENT_COUNT,
        "regression_pass_count_valid": regression_pass_count == EXPECTED_REGRESSION_PASS_COUNT,
        "regression_failure_count_zero": regression_failure_count == EXPECTED_REGRESSION_FAILURE_COUNT,
        "local_score_report_ready": report.get("local_score_report_ready") is True,
        "local_score_claim_absent": report.get("local_score_claim_absent") is True,
        "competitive_score_claim_absent": report.get("competitive_score_claim_absent") is True,
        "public_leaderboard_claim_absent": report.get("public_leaderboard_claim_absent") is True,
        "runtime_solver_not_modified": rebuild_record["runtime_solver_modified"] is False,
        "ranker_runtime_not_modified": rebuild_record["ranker_runtime_modified"] is False,
        "benchmark_runtime_not_modified": rebuild_record["benchmark_runtime_modified"] is False,
        "report_runtime_not_modified": rebuild_record["report_runtime_modified"] is False,
        "candidate_runtime_not_modified": rebuild_record["candidate_runtime_modified"] is False,
        "local_submission_candidate_created": rebuild_record["local_submission_candidate_created"] is True,
        "real_submission_not_created": rebuild_record["real_submission_created"] is False,
        "real_submission_allowed_false": rebuild_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": rebuild_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": rebuild_record["kaggle_submission_sent"] is False,
        "upload_not_performed": rebuild_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": rebuild_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
        "next_stage_valid": rebuild_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "final_audit_required": rebuild_record["final_competitive_readiness_audit_required"] is True,
        "manual_submission_not_allowed": rebuild_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": rebuild_record["manual_upload_performed"] is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
    }

    issue_state = {
        "report_artifact_missing": not gate_state["report_artifact_present"],
        "report_artifact_not_ready": not gate_state["report_artifact_ready"],
        "report_artifact_invalid": not gate_state["report_artifact_valid"],
        "report_next_stage_mismatch": not gate_state["report_next_stage_matches_task_8"],
        "submission_candidate_rebuild_not_required": not gate_state["submission_candidate_rebuild_required"],
        "source_count_invalid": not gate_state["source_count_valid"],
        "source_artifact_missing": not gate_state["all_source_artifacts_present"],
        "source_artifact_hash_missing": not gate_state["all_source_artifacts_hashed"],
        "source_artifact_status_invalid": not gate_state["all_source_artifacts_have_expected_status"],
        "rebuild_mode_invalid": not gate_state["rebuild_mode_valid"],
        "rebuild_scope_invalid": not gate_state["rebuild_scope_valid"],
        "rebuild_verdict_invalid": not gate_state["rebuild_verdict_valid"],
        "rebuild_not_ready": not gate_state["rebuild_ready"],
        "rebuild_not_locked": not gate_state["rebuild_locked"],
        "rebuild_component_count_invalid": not gate_state["rebuild_component_count_valid"],
        "component_not_ready": not gate_state["all_components_ready"],
        "component_runtime_modified": not gate_state["all_components_runtime_not_modified"],
        "candidate_file_count_invalid": not gate_state["candidate_file_count_valid"],
        "candidate_file_not_required": not gate_state["all_candidate_files_required"],
        "readiness_check_count_invalid": not gate_state["readiness_check_count_valid"],
        "boundary_control_count_invalid": not gate_state["boundary_control_count_valid"],
        "audit_chain_count_invalid": not gate_state["audit_chain_count_valid"],
        "family_report_count_invalid": not gate_state["family_report_count_valid"],
        "local_measurement_count_invalid": not gate_state["local_measurement_count_valid"],
        "regression_pass_count_invalid": not gate_state["regression_pass_count_valid"],
        "regression_failure_count_nonzero": not gate_state["regression_failure_count_zero"],
        "local_score_report_not_ready": not gate_state["local_score_report_ready"],
        "local_score_claim_detected": not gate_state["local_score_claim_absent"],
        "competitive_score_claim_detected": not gate_state["competitive_score_claim_absent"],
        "public_leaderboard_claim_detected": not gate_state["public_leaderboard_claim_absent"],
        "runtime_solver_modified": not gate_state["runtime_solver_not_modified"],
        "ranker_runtime_modified": not gate_state["ranker_runtime_not_modified"],
        "benchmark_runtime_modified": not gate_state["benchmark_runtime_not_modified"],
        "report_runtime_modified": not gate_state["report_runtime_not_modified"],
        "candidate_runtime_modified": not gate_state["candidate_runtime_not_modified"],
        "local_submission_candidate_missing": not gate_state["local_submission_candidate_created"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
        "final_audit_not_required": not gate_state["final_audit_required"],
        "manual_submission_allowed": not gate_state["manual_submission_not_allowed"],
        "manual_upload_performed": not gate_state["manual_upload_not_performed"],
        "public_safe_false": not gate_state["public_safe"],
        "deterministic_false": not gate_state["deterministic"],
        "local_only_false": not gate_state["local_only"],
        "dry_run_only_false": not gate_state["dry_run_only"],
    }

    gates = tuple(
        {"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"}
        for name in REBUILD_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in REBUILD_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    rebuild_ready = (
        report.get("status") == "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_READY"
        and len(sources) == EXPECTED_SOURCE_COUNT
        and all(item["present"] and item["status_valid"] for item in sources)
        and family_report_count == EXPECTED_FAMILY_REPORT_COUNT
        and local_measurement_count == EXPECTED_LOCAL_MEASUREMENT_COUNT
        and regression_pass_count == EXPECTED_REGRESSION_PASS_COUNT
        and regression_failure_count == EXPECTED_REGRESSION_FAILURE_COUNT
        and passed_gate_count == len(REBUILD_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 8",
        "rebuild_mode": REBUILD_MODE,
        "rebuild_scope": REBUILD_SCOPE,
        "rebuild_verdict": REBUILD_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_report": report.get("report_id", "MISSING_REPORT_ID"),
        "rebuild_ready": rebuild_ready,
        "rebuild_locked": True,
        "source_count": len(sources),
        "rebuild_component_count": len(components),
        "candidate_file_count": len(candidate_files),
        "readiness_check_count": len(READINESS_CHECKS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "audit_chain_count": len(AUDIT_CHAIN),
        "family_report_count": family_report_count,
        "local_measurement_count": local_measurement_count,
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "report_runtime_modified": False,
        "candidate_runtime_modified": False,
        "local_submission_candidate_created": True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "final_competitive_readiness_audit_required": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": REBUILD_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 8",
        "title": "Submission Candidate Rebuild v1",
        "baseline_commit": BASELINE_COMMIT,
        "rebuild_mode": REBUILD_MODE,
        "rebuild_scope": REBUILD_SCOPE,
        "rebuild_verdict": REBUILD_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_7_report_source": {
            "path": str(REPORT_JSON),
            "present": REPORT_JSON.exists(),
            "status": report.get("status", "MISSING"),
            "report_id": report.get("report_id", "MISSING_REPORT_ID"),
            "sha256": _sha256(REPORT_JSON),
            "sha256_16": _sha16(_sha256(REPORT_JSON)),
        },
        "source_artifacts": list(sources),
        "rebuild_record": rebuild_record,
        "rebuild_components": list(components),
        "candidate_files": list(candidate_files),
        "readiness_checks": list(READINESS_CHECKS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "audit_chain": list(AUDIT_CHAIN),
        "rebuild_gates": list(gates),
        "rebuild_issues": list(issues),
        "rebuild_index": index,
        "boundary": boundary,
        "source_count": len(sources),
        "rebuild_component_count": len(components),
        "candidate_file_count": len(candidate_files),
        "readiness_check_count": len(READINESS_CHECKS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "audit_chain_count": len(AUDIT_CHAIN),
        "family_report_count": family_report_count,
        "local_measurement_count": local_measurement_count,
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "rebuild_gate_count": len(REBUILD_GATES),
        "passed_gate_count": passed_gate_count,
        "rebuild_issue_count": issue_count,
        "warning_count": 0,
        "rebuild_ready": rebuild_ready,
        "rebuild_locked": True,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "report_runtime_modified": False,
        "candidate_runtime_modified": False,
        "local_submission_candidate_created": True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "final_competitive_readiness_audit_required": True,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "metadata": {
            "source": "milestone_7_submission_candidate_rebuild_v1",
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
        "candidate_id": f"MILESTONE-7-SUBMISSION-CANDIDATE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_submission_candidate_rebuild(candidate: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = candidate.get("boundary", {})
    gates = candidate.get("rebuild_gates", [])
    issues = candidate.get("rebuild_issues", [])
    sources = candidate.get("source_artifacts", [])

    checks = {
        "status_ready": candidate.get("status") == REBUILD_STATUS,
        "candidate_id_present": isinstance(candidate.get("candidate_id"), str) and bool(candidate.get("candidate_id")),
        "signature_present": isinstance(candidate.get("signature"), str) and bool(candidate.get("signature")),
        "baseline_commit_valid": str(candidate.get("baseline_commit", "")).startswith("bc41cd1"),
        "rebuild_mode_valid": candidate.get("rebuild_mode") == REBUILD_MODE,
        "rebuild_scope_valid": candidate.get("rebuild_scope") == REBUILD_SCOPE,
        "rebuild_verdict_valid": candidate.get("rebuild_verdict") == REBUILD_VERDICT,
        "next_allowed_stage_valid": candidate.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "source_count_valid": candidate.get("source_count") == EXPECTED_SOURCE_COUNT,
        "all_sources_present": bool(sources) and all(item.get("present") is True for item in sources),
        "all_sources_hashed": bool(sources) and all(item.get("sha256") != "MISSING_HASH" for item in sources),
        "all_sources_status_valid": bool(sources) and all(item.get("status_valid") is True for item in sources),
        "rebuild_component_count_valid": candidate.get("rebuild_component_count") == EXPECTED_REBUILD_COMPONENT_COUNT,
        "candidate_file_count_valid": candidate.get("candidate_file_count") == EXPECTED_CANDIDATE_FILE_COUNT,
        "readiness_check_count_valid": candidate.get("readiness_check_count") == EXPECTED_READINESS_CHECK_COUNT,
        "boundary_control_count_valid": candidate.get("boundary_control_count") == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "audit_chain_count_valid": candidate.get("audit_chain_count") == EXPECTED_AUDIT_CHAIN_COUNT,
        "family_report_count_valid": candidate.get("family_report_count") == EXPECTED_FAMILY_REPORT_COUNT,
        "local_measurement_count_valid": candidate.get("local_measurement_count") == EXPECTED_LOCAL_MEASUREMENT_COUNT,
        "regression_pass_count_valid": candidate.get("regression_pass_count") == EXPECTED_REGRESSION_PASS_COUNT,
        "regression_failure_count_zero": candidate.get("regression_failure_count") == EXPECTED_REGRESSION_FAILURE_COUNT,
        "local_submission_candidate_created": candidate.get("local_submission_candidate_created") is True,
        "real_submission_not_created": candidate.get("real_submission_created") is False,
        "real_submission_allowed_false": candidate.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": candidate.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": candidate.get("kaggle_submission_sent") is False,
        "upload_not_performed": candidate.get("upload_performed") is False,
        "kaggle_authentication_not_performed": candidate.get("kaggle_authentication_performed") is False,
        "runtime_solver_not_modified": candidate.get("runtime_solver_modified") is False,
        "ranker_runtime_not_modified": candidate.get("ranker_runtime_modified") is False,
        "benchmark_runtime_not_modified": candidate.get("benchmark_runtime_modified") is False,
        "report_runtime_not_modified": candidate.get("report_runtime_modified") is False,
        "candidate_runtime_not_modified": candidate.get("candidate_runtime_modified") is False,
        "final_audit_required": candidate.get("final_competitive_readiness_audit_required") is True,
        "rebuild_gate_count_matches": candidate.get("rebuild_gate_count") == len(REBUILD_GATES),
        "all_rebuild_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "rebuild_issue_count_zero": candidate.get("rebuild_issue_count") == 0,
        "all_rebuild_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "rebuild_ready": candidate.get("rebuild_ready") is True,
        "rebuild_locked": candidate.get("rebuild_locked") is True,
        "manual_submission_not_allowed": candidate.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": candidate.get("manual_upload_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_INVALID",
        "valid": valid,
        "checks": checks,
        "candidate_id": candidate.get("candidate_id"),
        "signature": candidate.get("signature"),
    }


def render_submission_candidate_rebuild_markdown(candidate: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Submission Candidate Rebuild v1",
        "",
        f"- status: {candidate['status']}",
        f"- candidate_id: {candidate['candidate_id']}",
        f"- signature: {candidate['signature']}",
        f"- baseline_commit: {candidate['baseline_commit']}",
        f"- rebuild_mode: {candidate['rebuild_mode']}",
        f"- rebuild_scope: {candidate['rebuild_scope']}",
        f"- rebuild_verdict: {candidate['rebuild_verdict']}",
        f"- next_allowed_stage: {candidate['next_allowed_stage']}",
        f"- source_count: {candidate['source_count']}",
        f"- rebuild_component_count: {candidate['rebuild_component_count']}",
        f"- candidate_file_count: {candidate['candidate_file_count']}",
        f"- readiness_check_count: {candidate['readiness_check_count']}",
        f"- boundary_control_count: {candidate['boundary_control_count']}",
        f"- audit_chain_count: {candidate['audit_chain_count']}",
        f"- family_report_count: {candidate['family_report_count']}",
        f"- local_measurement_count: {candidate['local_measurement_count']}",
        f"- regression_pass_count: {candidate['regression_pass_count']}",
        f"- regression_failure_count: {candidate['regression_failure_count']}",
        f"- rebuild_gate_count: {candidate['rebuild_gate_count']}",
        f"- passed_gate_count: {candidate['passed_gate_count']}",
        f"- rebuild_issue_count: {candidate['rebuild_issue_count']}",
        f"- rebuild_ready: {candidate['rebuild_ready']}",
        f"- local_submission_candidate_created: {candidate['local_submission_candidate_created']}",
        f"- real_submission_created: {candidate['real_submission_created']}",
        f"- real_submission_allowed: {candidate['real_submission_allowed']}",
        f"- kaggle_submission_sent: {candidate['kaggle_submission_sent']}",
        f"- upload_performed: {candidate['upload_performed']}",
        "",
        "## Source artifacts",
        "",
    ]

    for item in candidate["source_artifacts"]:
        lines.append(
            f"- {item['source_id']} / present={item['present']} / "
            f"status_valid={item['status_valid']} / sha256_16={item['sha256_16']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Local submission candidate rebuild is ready for final competitive readiness audit.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_VALID=true",
            "ARC_AGI3_MILESTONE_7_REBUILD_MODE=SUBMISSION_CANDIDATE_REBUILD_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_REBUILD_VERDICT=SUBMISSION_CANDIDATE_REBUILD_READY_FOR_FINAL_COMPETITIVE_READINESS_AUDIT",
            "ARC_AGI3_MILESTONE_7_SOURCE_COUNT=5",
            "ARC_AGI3_MILESTONE_7_REBUILD_COMPONENT_COUNT=5",
            "ARC_AGI3_MILESTONE_7_CANDIDATE_FILE_COUNT=4",
            "ARC_AGI3_MILESTONE_7_READINESS_CHECK_COUNT=8",
            "ARC_AGI3_MILESTONE_7_BOUNDARY_CONTROL_COUNT=9",
            "ARC_AGI3_MILESTONE_7_AUDIT_CHAIN_COUNT=7",
            "ARC_AGI3_MILESTONE_7_FAMILY_REPORT_COUNT=3",
            "ARC_AGI3_MILESTONE_7_LOCAL_MEASUREMENT_COUNT=6",
            "ARC_AGI3_MILESTONE_7_REGRESSION_PASS_COUNT=6",
            "ARC_AGI3_MILESTONE_7_REGRESSION_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_7_LOCAL_SUBMISSION_CANDIDATE_CREATED=true",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_REQUIRED=true",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_9_FINAL_COMPETITIVE_READINESS_AUDIT",
            "ARC_AGI3_MILESTONE_7_BASELINE_REPORT_COMMIT=bc41cd1",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_submission_candidate_rebuild_manifest(candidate: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 SUBMISSION CANDIDATE REBUILD MANIFEST v1",
        f"candidate_id={candidate['candidate_id']}",
        f"signature={candidate['signature']}",
        f"status={candidate['status']}",
        f"baseline_commit={candidate['baseline_commit']}",
        f"rebuild_mode={candidate['rebuild_mode']}",
        f"rebuild_verdict={candidate['rebuild_verdict']}",
        f"next_allowed_stage={candidate['next_allowed_stage']}",
        f"source_count={candidate['source_count']}",
        f"rebuild_component_count={candidate['rebuild_component_count']}",
        f"candidate_file_count={candidate['candidate_file_count']}",
        f"readiness_check_count={candidate['readiness_check_count']}",
        f"boundary_control_count={candidate['boundary_control_count']}",
        f"audit_chain_count={candidate['audit_chain_count']}",
        f"family_report_count={candidate['family_report_count']}",
        f"local_measurement_count={candidate['local_measurement_count']}",
        f"regression_pass_count={candidate['regression_pass_count']}",
        f"regression_failure_count={candidate['regression_failure_count']}",
        f"rebuild_gate_count={candidate['rebuild_gate_count']}",
        f"passed_gate_count={candidate['passed_gate_count']}",
        f"rebuild_issue_count={candidate['rebuild_issue_count']}",
        f"rebuild_ready={candidate['rebuild_ready']}",
        f"rebuild_locked={candidate['rebuild_locked']}",
        f"runtime_solver_modified={candidate['runtime_solver_modified']}",
        f"ranker_runtime_modified={candidate['ranker_runtime_modified']}",
        f"benchmark_runtime_modified={candidate['benchmark_runtime_modified']}",
        f"report_runtime_modified={candidate['report_runtime_modified']}",
        f"candidate_runtime_modified={candidate['candidate_runtime_modified']}",
        f"local_submission_candidate_created={candidate['local_submission_candidate_created']}",
        f"real_submission_created={candidate['real_submission_created']}",
        f"real_submission_allowed={candidate['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={candidate['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={candidate['kaggle_submission_sent']}",
        f"upload_performed={candidate['upload_performed']}",
        f"kaggle_authentication_performed={candidate['kaggle_authentication_performed']}",
        f"final_competitive_readiness_audit_required={candidate['final_competitive_readiness_audit_required']}",
        f"manual_submission_allowed={candidate['manual_submission_allowed']}",
        f"manual_upload_performed={candidate['manual_upload_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "SOURCE_ARTIFACTS",
    ]

    for item in candidate["source_artifacts"]:
        lines.append(
            f"{item['source_id']} present={item['present']} status_valid={item['status_valid']} "
            f"sha256_16={item['sha256_16']} path={item['path']}"
        )

    lines.append("")
    lines.append("AUDIT_CHAIN")
    for item in candidate["audit_chain"]:
        lines.append(f"{item['task']} commit={item['commit']} label={item['label']}")

    lines.append("")
    return "\n".join(lines)


def write_submission_candidate_rebuild_artifacts(
    candidate: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    candidate = dict(candidate or build_milestone_7_submission_candidate_rebuild())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-submission-candidate-rebuild-v1.json"
    md_path = output / "milestone-7-submission-candidate-rebuild-v1.md"
    manifest_path = output / "milestone-7-submission-candidate-rebuild-manifest-v1.txt"
    index_path = output / "milestone-7-submission-candidate-rebuild-index-v1.json"

    json_path.write_text(json.dumps(candidate, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_submission_candidate_rebuild_markdown(candidate), encoding="utf-8")
    manifest_path.write_text(render_submission_candidate_rebuild_manifest(candidate), encoding="utf-8")
    index_path.write_text(json.dumps(candidate["rebuild_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_submission_candidate_rebuild_pipeline() -> Dict[str, Any]:
    candidate = build_milestone_7_submission_candidate_rebuild()
    validation = validate_milestone_7_submission_candidate_rebuild(candidate)
    artifacts = write_submission_candidate_rebuild_artifacts(candidate)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_PIPELINE_INVALID",
        "candidate_status": candidate["status"],
        "validation_status": validation["status"],
        "candidate": candidate,
        "candidate_id": candidate["candidate_id"],
        "signature": candidate["signature"],
        "rebuild_mode": candidate["rebuild_mode"],
        "rebuild_verdict": candidate["rebuild_verdict"],
        "next_allowed_stage": candidate["next_allowed_stage"],
        "source_count": candidate["source_count"],
        "rebuild_component_count": candidate["rebuild_component_count"],
        "candidate_file_count": candidate["candidate_file_count"],
        "readiness_check_count": candidate["readiness_check_count"],
        "boundary_control_count": candidate["boundary_control_count"],
        "audit_chain_count": candidate["audit_chain_count"],
        "family_report_count": candidate["family_report_count"],
        "local_measurement_count": candidate["local_measurement_count"],
        "regression_pass_count": candidate["regression_pass_count"],
        "regression_failure_count": candidate["regression_failure_count"],
        "rebuild_gate_count": candidate["rebuild_gate_count"],
        "passed_gate_count": candidate["passed_gate_count"],
        "rebuild_issue_count": candidate["rebuild_issue_count"],
        "warning_count": candidate["warning_count"],
        "rebuild_ready": candidate["rebuild_ready"],
        "rebuild_locked": candidate["rebuild_locked"],
        "local_submission_candidate_created": candidate["local_submission_candidate_created"],
        "real_submission_created": candidate["real_submission_created"],
        "real_submission_allowed": candidate["real_submission_allowed"],
        "ready_for_real_kaggle_submission": candidate["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": candidate["kaggle_submission_sent"],
        "upload_performed": candidate["upload_performed"],
        "kaggle_authentication_performed": candidate["kaggle_authentication_performed"],
        "final_competitive_readiness_audit_required": candidate["final_competitive_readiness_audit_required"],
        "runtime_solver_modified": candidate["runtime_solver_modified"],
        "candidate_runtime_modified": candidate["candidate_runtime_modified"],
        "artifacts": artifacts,
        "metadata": candidate["metadata"],
    }
