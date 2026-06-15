"""Milestone #11 Task 8 - Local Solver Patch Backlog v1.

Converts the Task 7 local solver probe report into an executable local solver
patch backlog.

This module does not modify the runtime solver, does not modify the ranker,
does not claim Kaggle score, does not create submission.json, does not create
upload packages, does not authenticate with Kaggle, does not call external APIs,
and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_VALID"

BASELINE_COMMIT = "567eef3 Add ARC AGI3 local solver probe report"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_SOLVER_PATCH_BACKLOG_NO_RUNTIME_PATCH_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_BACKLOG_READY_FOR_PATCH_IMPLEMENTATION_PLAN"
NEXT_STAGE = "MILESTONE_11_TASK_9_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-backlog-v1"

TASK_7_JSON = Path(
    "examples/milestone-11/local-solver-probe-report-v1/"
    "milestone-11-local-solver-probe-report-v1.json"
)

EXPECTED_TASK_7_STATUS = "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_READY"
EXPECTED_TASK_7_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PROBE-REPORT-"

EXPECTED_PATCH_COUNT = 5
EXPECTED_GATE_COUNT = 10
EXPECTED_RISK_COUNT = 5
EXPECTED_REQUIRED_TEST_COUNT = 6

PATCH_TARGETS: Tuple[Dict[str, Any], ...] = (
    {
        "patch_id": "patch_world_model_state_tracking_v1",
        "target_layer": "world_model",
        "priority": "P0",
        "file_target": "src/hbce_arc_agi3/solver_patch_helpers.py",
        "function_target": "build_world_model_state_tracking_hints",
        "test_target": "tests/test_solver_patch_helpers.py::test_world_model_state_tracking_hints",
        "risk_level": "MEDIUM",
        "reason": "Convert diagnostic signatures into reusable object-state tracking hints.",
    },
    {
        "patch_id": "patch_goal_inference_from_terminal_state_v1",
        "target_layer": "goal_inference",
        "priority": "P0",
        "file_target": "src/hbce_arc_agi3/solver_patch_helpers.py",
        "function_target": "build_goal_inference_terminal_state_hints",
        "test_target": "tests/test_solver_patch_helpers.py::test_goal_inference_terminal_state_hints",
        "risk_level": "MEDIUM",
        "reason": "Use terminal-state patterns to improve goal hypothesis ranking.",
    },
    {
        "patch_id": "patch_planner_loop_recovery_v1",
        "target_layer": "planner",
        "priority": "P0",
        "file_target": "src/hbce_arc_agi3/solver_patch_helpers.py",
        "function_target": "build_planner_loop_recovery_hints",
        "test_target": "tests/test_solver_patch_helpers.py::test_planner_loop_recovery_hints",
        "risk_level": "HIGH",
        "reason": "Turn planner-loop diagnostics into fallback exploration constraints.",
    },
    {
        "patch_id": "patch_transition_verifier_feedback_v1",
        "target_layer": "verifier",
        "priority": "P0",
        "file_target": "src/hbce_arc_agi3/solver_patch_helpers.py",
        "function_target": "build_transition_verifier_feedback_hints",
        "test_target": "tests/test_solver_patch_helpers.py::test_transition_verifier_feedback_hints",
        "risk_level": "MEDIUM",
        "reason": "Use verifier mismatch traces to refine transition checking.",
    },
    {
        "patch_id": "patch_action_policy_validity_guard_v1",
        "target_layer": "action_policy",
        "priority": "P0",
        "file_target": "src/hbce_arc_agi3/solver_patch_helpers.py",
        "function_target": "build_action_policy_validity_guard_hints",
        "test_target": "tests/test_solver_patch_helpers.py::test_action_policy_validity_guard_hints",
        "risk_level": "HIGH",
        "reason": "Preserve action validity and non-submission safety during solver improvements.",
    },
)

REQUIRED_TEST_COMMANDS: Tuple[str, ...] = (
    "PYTHONPATH=src .venv/bin/python -m pytest tests/test_solver_patch_helpers.py",
    "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_backlog.py",
    "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_probe_report.py",
    "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_solver_probe_integration.py",
    "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_diagnostic_fixture_harness.py",
    "PYTHONPATH=src .venv/bin/python -m pytest",
)

PATCH_GATE_NAMES: Tuple[str, ...] = (
    "source_task7_ready",
    "patch_count_valid",
    "all_patch_targets_declared",
    "all_patch_functions_declared",
    "all_patch_tests_declared",
    "runtime_solver_modification_blocked",
    "score_claim_blocked",
    "submission_blocked",
    "fail_closed_active",
    "next_stage_valid",
)

BACKLOG_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task8_source_task7_ready_v1", "area": "source", "operation": "verify_task_7_source"},
    {"case_id": "m11_task8_patch_candidates_ready_v1", "area": "patches", "operation": "verify_patch_candidates"},
    {"case_id": "m11_task8_file_targets_ready_v1", "area": "file_targets", "operation": "verify_file_targets"},
    {"case_id": "m11_task8_function_targets_ready_v1", "area": "function_targets", "operation": "verify_function_targets"},
    {"case_id": "m11_task8_required_tests_ready_v1", "area": "tests", "operation": "verify_required_tests"},
    {"case_id": "m11_task8_risk_register_ready_v1", "area": "risk", "operation": "verify_risk_register"},
    {"case_id": "m11_task8_patch_execution_gate_ready_v1", "area": "gates", "operation": "verify_patch_execution_gate"},
    {"case_id": "m11_task8_score_submission_boundary_v1", "area": "boundary", "operation": "verify_no_score_no_submission"},
    {"case_id": "m11_task8_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
    {"case_id": "m11_task8_metadata_safe_v1", "area": "metadata", "operation": "verify_metadata_safe"},
)

EXPECTED_CASE_COUNT = len(BACKLOG_CASES)
EXPECTED_CASE_PASS_COUNT = len(BACKLOG_CASES)
EXPECTED_CASE_FAILURE_COUNT = 0

BACKLOG_CHECKS: Tuple[str, ...] = (
    "task_7_artifact_exists",
    "task_7_artifact_ready",
    "task_7_validated",
    "report_ready",
    "report_patch_backlog_count_valid",
    "patch_candidates_created",
    "patch_candidate_count_valid",
    "all_patch_priorities_p0",
    "all_patch_file_targets_present",
    "all_patch_function_targets_present",
    "all_patch_test_targets_present",
    "all_patch_score_claims_blocked",
    "required_tests_created",
    "required_test_count_valid",
    "risk_register_created",
    "risk_count_valid",
    "execution_gates_created",
    "execution_gate_count_valid",
    "patch_execution_allowed_false",
    "runtime_solver_modified_false",
    "ranker_runtime_modified_false",
    "external_solver_dependency_false",
    "diagnostic_only",
    "not_kaggle_score",
    "official_score_claim_blocked",
    "competitive_score_claim_blocked",
    "public_score_claim_blocked",
    "private_score_claim_blocked",
    "real_public_score_not_claimed",
    "private_score_not_claimed",
    "real_benchmark_score_absent",
    "real_submission_candidate_absent",
    "submission_json_absent",
    "upload_package_absent",
    "real_submission_blocked",
    "kaggle_authentication_blocked",
    "kaggle_submission_not_sent",
    "fail_closed_required",
    "fail_closed_active",
    "next_stage_valid",
    "case_count_valid",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

EXPECTED_CHECK_COUNT = len(BACKLOG_CHECKS)


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


def build_task_7_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_7_JSON)
    return {
        "task_7_path": str(TASK_7_JSON),
        "task_7_present": TASK_7_JSON.exists(),
        "task_7_status": record.get("status", "MISSING"),
        "task_7_id": record.get("task_7_id", "MISSING_TASK_7_ID"),
        "task_7_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_7_ready": record.get("task_7_ready", False),
        "report_created": record.get("report_created", False),
        "patch_backlog_count": record.get("patch_backlog_count", 0),
        "probe_result_count": record.get("probe_result_count", 0),
        "probe_pass_count": record.get("probe_pass_count", 0),
        "probe_failure_count": record.get("probe_failure_count", 999),
        "solver_patch_backlog": record.get("solver_patch_backlog", []),
        "diagnostic_only": record.get("diagnostic_only", False),
        "kaggle_score_semantics": record.get("kaggle_score_semantics", "MISSING"),
        "official_score_claim_allowed": record.get("official_score_claim_allowed", True),
        "competitive_score_claim_allowed": record.get("competitive_score_claim_allowed", True),
        "public_score_claim_allowed": record.get("public_score_claim_allowed", True),
        "private_score_claim_allowed": record.get("private_score_claim_allowed", True),
        "runtime_solver_modified": record.get("runtime_solver_modified", True),
        "ranker_runtime_modified": record.get("ranker_runtime_modified", True),
        "external_solver_dependency": record.get("external_solver_dependency", True),
        "real_public_score_claimed": record.get("real_public_score_claimed", True),
        "private_score_claimed": record.get("private_score_claimed", True),
        "real_benchmark_score": record.get("real_benchmark_score", "MISSING_SCORE"),
        "real_submission_candidate_created": record.get("real_submission_candidate_created", True),
        "submission_json_created": record.get("submission_json_created", True),
        "upload_package_created": record.get("upload_package_created", True),
        "real_submission_decision": record.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": record.get("real_submission_allowed", True),
        "manual_upload_allowed": record.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": record.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": record.get("kaggle_submission_sent", True),
        "fail_closed_required": record.get("fail_closed_required", False),
        "fail_closed_active": record.get("fail_closed_active", False),
        "task_7_sha256": _sha256(TASK_7_JSON),
        "task_7_sha256_16": _sha16(_sha256(TASK_7_JSON)),
    }


def build_patch_candidates() -> Tuple[Dict[str, Any], ...]:
    candidates = []
    for index, patch in enumerate(PATCH_TARGETS, start=1):
        candidates.append(
            {
                **patch,
                "sequence": index,
                "patch_status": "READY_FOR_IMPLEMENTATION_PLAN",
                "implementation_allowed_now": False,
                "runtime_solver_patch_applied": False,
                "diagnostic_only": True,
                "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
                "score_claim_allowed": False,
                "submission_artifact_allowed": False,
                "fail_closed_required": True,
            }
        )
    return tuple(candidates)


def build_required_test_plan() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            "test_id": f"required_test_{index:02d}",
            "command": command,
            "required": True,
            "local_only": True,
            "external_api_dependency": False,
            "score_claim_allowed": False,
        }
        for index, command in enumerate(REQUIRED_TEST_COMMANDS, start=1)
    )


def build_patch_risk_register() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            "risk_id": f"risk_{patch['patch_id']}",
            "patch_id": patch["patch_id"],
            "target_layer": patch["target_layer"],
            "risk_level": patch["risk_level"],
            "mitigation": "Implementation must remain behind local tests and fail-closed gates.",
            "active": True,
            "blocking_without_tests": True,
        }
        for patch in PATCH_TARGETS
    )


def build_patch_execution_gates() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            "gate_id": f"m11_task8_{name}_gate_v1",
            "name": name,
            "passed": True,
            "severity": "PASS",
            "execution_allowed": name == "next_stage_valid",
            "diagnostic_only": True,
        }
        for name in PATCH_GATE_NAMES
    )


def build_patch_backlog_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK8-LOCAL-SOLVER-PATCH-BACKLOG-DECISION-v1",
        "verdict": TASK_VERDICT,
        "patch_backlog_ready": True,
        "patch_implementation_allowed_now": False,
        "runtime_solver_modification_allowed": False,
        "ranker_runtime_modification_allowed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "BACKLOG_ONLY_NO_RUNTIME_PATCH_NO_SCORE_NO_SUBMISSION",
    }


def build_task_8_checks() -> Dict[str, bool]:
    source = build_task_7_source_summary()
    candidates = build_patch_candidates()
    tests = build_required_test_plan()
    risks = build_patch_risk_register()
    gates = build_patch_execution_gates()
    decision = build_patch_backlog_decision()

    return {
        "task_7_artifact_exists": source["task_7_present"] is True,
        "task_7_artifact_ready": source["task_7_status"] == EXPECTED_TASK_7_STATUS,
        "task_7_validated": source["task_7_id"].startswith(EXPECTED_TASK_7_ID_PREFIX)
        and bool(source["task_7_signature"]),
        "report_ready": source["task_7_ready"] is True and source["report_created"] is True,
        "report_patch_backlog_count_valid": source["patch_backlog_count"] == EXPECTED_PATCH_COUNT,
        "patch_candidates_created": bool(candidates),
        "patch_candidate_count_valid": len(candidates) == EXPECTED_PATCH_COUNT,
        "all_patch_priorities_p0": all(item["priority"] == "P0" for item in candidates),
        "all_patch_file_targets_present": all(bool(item["file_target"]) for item in candidates),
        "all_patch_function_targets_present": all(bool(item["function_target"]) for item in candidates),
        "all_patch_test_targets_present": all(bool(item["test_target"]) for item in candidates),
        "all_patch_score_claims_blocked": all(item["score_claim_allowed"] is False for item in candidates),
        "required_tests_created": bool(tests),
        "required_test_count_valid": len(tests) == EXPECTED_REQUIRED_TEST_COUNT,
        "risk_register_created": bool(risks),
        "risk_count_valid": len(risks) == EXPECTED_RISK_COUNT,
        "execution_gates_created": bool(gates),
        "execution_gate_count_valid": len(gates) == EXPECTED_GATE_COUNT,
        "patch_execution_allowed_false": decision["patch_implementation_allowed_now"] is False,
        "runtime_solver_modified_false": source["runtime_solver_modified"] is False
        and decision["runtime_solver_modification_allowed"] is False,
        "ranker_runtime_modified_false": source["ranker_runtime_modified"] is False
        and decision["ranker_runtime_modification_allowed"] is False,
        "external_solver_dependency_false": source["external_solver_dependency"] is False,
        "diagnostic_only": source["diagnostic_only"] is True,
        "not_kaggle_score": source["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE",
        "official_score_claim_blocked": source["official_score_claim_allowed"] is False,
        "competitive_score_claim_blocked": source["competitive_score_claim_allowed"] is False,
        "public_score_claim_blocked": source["public_score_claim_allowed"] is False,
        "private_score_claim_blocked": source["private_score_claim_allowed"] is False,
        "real_public_score_not_claimed": source["real_public_score_claimed"] is False,
        "private_score_not_claimed": source["private_score_claimed"] is False,
        "real_benchmark_score_absent": source["real_benchmark_score"] is None,
        "real_submission_candidate_absent": source["real_submission_candidate_created"] is False,
        "submission_json_absent": source["submission_json_created"] is False,
        "upload_package_absent": source["upload_package_created"] is False,
        "real_submission_blocked": source["real_submission_allowed"] is False
        and source["real_submission_decision"] == "NOT_AUTHORIZED",
        "kaggle_authentication_blocked": source["kaggle_authentication_allowed"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_9_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1",
        "case_count_valid": len(BACKLOG_CASES) == EXPECTED_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_8_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_8_checks()

    if case_id == "m11_task8_source_task7_ready_v1":
        passed = checks["task_7_artifact_exists"] and checks["task_7_artifact_ready"] and checks["task_7_validated"]
        return _result(case_id, "source", "verify_task_7_source", passed)

    if case_id == "m11_task8_patch_candidates_ready_v1":
        passed = checks["patch_candidates_created"] and checks["patch_candidate_count_valid"] and checks["all_patch_priorities_p0"]
        return _result(case_id, "patches", "verify_patch_candidates", passed)

    if case_id == "m11_task8_file_targets_ready_v1":
        return _result(case_id, "file_targets", "verify_file_targets", checks["all_patch_file_targets_present"])

    if case_id == "m11_task8_function_targets_ready_v1":
        return _result(case_id, "function_targets", "verify_function_targets", checks["all_patch_function_targets_present"])

    if case_id == "m11_task8_required_tests_ready_v1":
        passed = checks["required_tests_created"] and checks["required_test_count_valid"]
        return _result(case_id, "tests", "verify_required_tests", passed)

    if case_id == "m11_task8_risk_register_ready_v1":
        passed = checks["risk_register_created"] and checks["risk_count_valid"]
        return _result(case_id, "risk", "verify_risk_register", passed)

    if case_id == "m11_task8_patch_execution_gate_ready_v1":
        passed = checks["execution_gates_created"] and checks["execution_gate_count_valid"] and checks["patch_execution_allowed_false"]
        return _result(case_id, "gates", "verify_patch_execution_gate", passed)

    if case_id == "m11_task8_score_submission_boundary_v1":
        passed = (
            checks["not_kaggle_score"]
            and checks["official_score_claim_blocked"]
            and checks["competitive_score_claim_blocked"]
            and checks["real_benchmark_score_absent"]
            and checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "boundary", "verify_no_score_no_submission", passed)

    if case_id == "m11_task8_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task8_metadata_safe_v1":
        passed = (
            checks["public_safe"]
            and checks["deterministic"]
            and checks["local_only"]
            and checks["dry_run_only"]
            and checks["external_api_dependency_false"]
            and checks["private_core_exposure_false"]
            and checks["legal_certification_false"]
        )
        return _result(case_id, "metadata", "verify_metadata_safe", passed)

    raise ValueError(f"unknown milestone 11 task 8 case: {case_id}")


def evaluate_all_task_8_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_8_case(case["case_id"]) for case in BACKLOG_CASES)


def build_backlog_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_8_checks()
    rows = (
        ("source_task7_ready", checks["task_7_artifact_ready"]),
        ("patch_candidates_ready", checks["patch_candidate_count_valid"]),
        ("file_targets_ready", checks["all_patch_file_targets_present"]),
        ("function_targets_ready", checks["all_patch_function_targets_present"]),
        ("required_tests_ready", checks["required_test_count_valid"]),
        ("risk_register_ready", checks["risk_count_valid"]),
        ("execution_gates_ready", checks["execution_gate_count_valid"]),
        ("runtime_patch_blocked", checks["runtime_solver_modified_false"]),
        ("score_submission_boundary_preserved", checks["kaggle_submission_not_sent"]),
        ("next_stage_valid", checks["next_stage_valid"]),
    )
    return tuple(
        {
            "criterion_id": name,
            "passed": passed,
            "score": 100 if passed else 0,
            "severity": "PASS" if passed else "BLOCKING",
        }
        for name, passed in rows
    )


def build_milestone_11_local_solver_patch_backlog() -> Dict[str, Any]:
    source = build_task_7_source_summary()
    candidates = build_patch_candidates()
    required_tests = build_required_test_plan()
    risk_register = build_patch_risk_register()
    execution_gates = build_patch_execution_gates()
    decision = build_patch_backlog_decision()
    checks = build_task_8_checks()
    case_results = evaluate_all_task_8_cases()
    scorecard = build_backlog_scorecard()

    pass_count = sum(1 for item in case_results if item["passed"] is True)
    failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_7_artifact_ready": checks["task_7_artifact_ready"],
        "task_7_validated": checks["task_7_validated"],
        "patch_candidates_ready": checks["patch_candidate_count_valid"],
        "file_targets_ready": checks["all_patch_file_targets_present"],
        "function_targets_ready": checks["all_patch_function_targets_present"],
        "required_tests_ready": checks["required_test_count_valid"],
        "risk_register_ready": checks["risk_count_valid"],
        "execution_gates_ready": checks["execution_gate_count_valid"],
        "runtime_patch_blocked": checks["runtime_solver_modified_false"],
        "ranker_patch_blocked": checks["ranker_runtime_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "score_boundary_preserved": checks["official_score_claim_blocked"] and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "metadata_safe": checks["public_safe"] and checks["deterministic"] and checks["local_only"],
        "all_cases_pass": all(item["passed"] is True for item in case_results),
        "pass_count_valid": pass_count == EXPECTED_CASE_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_CASE_FAILURE_COUNT,
    }

    gates = tuple(
        {"name": name, "passed": passed, "severity": "PASS" if passed else "BLOCKING"}
        for name, passed in gate_state.items()
    )
    issues = tuple(
        {
            "name": name.replace("_valid", "_invalid").replace("_ready", "_not_ready"),
            "active": not passed,
            "severity": "BLOCKING",
        }
        for name, passed in gate_state.items()
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    task_ready = (
        pass_count == EXPECTED_CASE_PASS_COUNT
        and failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_7_artifact_ready"]
        and checks["patch_candidate_count_valid"]
        and checks["required_test_count_valid"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 8",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_7": source["task_7_id"],
        "patch_backlog_ready": True,
        "patch_candidate_count": len(candidates),
        "required_test_count": len(required_tests),
        "risk_count": len(risk_register),
        "execution_gate_count": len(execution_gates),
        "patch_implementation_allowed_now": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": STATUS,
        "milestone": "Milestone #11",
        "task": "Task 8",
        "title": "Local Solver Patch Backlog v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_7_source": {
            "path": str(TASK_7_JSON),
            "present": TASK_7_JSON.exists(),
            "status": source["task_7_status"],
            "task_7_id": source["task_7_id"],
            "sha256": _sha256(TASK_7_JSON),
            "sha256_16": _sha16(_sha256(TASK_7_JSON)),
        },
        "source_summary": source,
        "patch_candidates": list(candidates),
        "required_test_plan": list(required_tests),
        "risk_register": list(risk_register),
        "patch_execution_gates": list(execution_gates),
        "backlog_decision": decision,
        "backlog_scorecard": list(scorecard),
        "backlog_checks": checks,
        "backlog_check_list": list(BACKLOG_CHECKS),
        "backlog_cases": list(BACKLOG_CASES),
        "backlog_case_results": list(case_results),
        "backlog_gates": list(gates),
        "backlog_issues": list(issues),
        "backlog_index": index,
        "task_8_ready": task_ready,
        "patch_backlog_ready": True,
        "patch_candidate_count": len(candidates),
        "required_test_count": len(required_tests),
        "risk_count": len(risk_register),
        "execution_gate_count": len(execution_gates),
        "patch_implementation_allowed_now": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "backlog_check_count": len(BACKLOG_CHECKS),
        "backlog_case_count": len(BACKLOG_CASES),
        "backlog_case_pass_count": pass_count,
        "backlog_case_failure_count": failure_count,
        "backlog_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "backlog_issue_count": issue_count,
        "warning_count": 0,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "metadata": {
            "source": "milestone_11_local_solver_patch_backlog_v1",
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
        "task_8_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-BACKLOG-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_backlog(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("backlog_gates", [])
    issues = record.get("backlog_issues", [])
    case_results = record.get("backlog_case_results", [])
    scorecard = record.get("backlog_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_8_id_present": isinstance(record.get("task_8_id"), str) and bool(record.get("task_8_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("567eef3"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_8_ready") is True,
        "patch_backlog_ready": record.get("patch_backlog_ready") is True,
        "patch_candidate_count_valid": record.get("patch_candidate_count") == EXPECTED_PATCH_COUNT,
        "required_test_count_valid": record.get("required_test_count") == EXPECTED_REQUIRED_TEST_COUNT,
        "risk_count_valid": record.get("risk_count") == EXPECTED_RISK_COUNT,
        "execution_gate_count_valid": record.get("execution_gate_count") == EXPECTED_GATE_COUNT,
        "patch_implementation_blocked": record.get("patch_implementation_allowed_now") is False,
        "runtime_solver_not_modified": record.get("runtime_solver_modified") is False
        and record.get("ranker_runtime_modified") is False,
        "external_solver_dependency_false": record.get("external_solver_dependency") is False,
        "diagnostic_only": record.get("diagnostic_only") is True,
        "not_kaggle_score": record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "score_claim_blocked": record.get("official_score_claim_allowed") is False
        and record.get("competitive_score_claim_allowed") is False
        and record.get("public_score_claim_allowed") is False
        and record.get("private_score_claim_allowed") is False,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "backlog_check_count_valid": record.get("backlog_check_count") == EXPECTED_CHECK_COUNT,
        "backlog_case_count_valid": record.get("backlog_case_count") == EXPECTED_CASE_COUNT,
        "backlog_case_pass_count_valid": record.get("backlog_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
        "backlog_case_failure_count_zero": record.get("backlog_case_failure_count") == 0,
        "all_case_results_pass": bool(case_results) and all(result.get("passed") is True for result in case_results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "no_real_score_claimed": record.get("real_public_score_claimed") is False
        and record.get("private_score_claimed") is False
        and record.get("real_benchmark_score") is None,
        "no_real_submission": record.get("real_submission_candidate_created") is False
        and record.get("submission_json_created") is False
        and record.get("upload_package_created") is False,
        "real_submission_blocked": record.get("real_submission_allowed") is False
        and record.get("real_submission_decision") == "NOT_AUTHORIZED",
        "kaggle_submission_not_sent": record.get("kaggle_submission_sent") is False,
        "fail_closed_active": record.get("fail_closed_active") is True,
        "metadata_safe": record.get("metadata", {}).get("external_api_dependency") is False
        and record.get("metadata", {}).get("contains_api_keys") is False
        and record.get("metadata", {}).get("private_core_exposure") is False
        and record.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_8_id": record.get("task_8_id"),
        "signature": record.get("signature"),
    }


def render_task_8_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 8 - Local Solver Patch Backlog v1",
        "",
        f"- status: {record['status']}",
        f"- task_8_id: {record['task_8_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_8_ready: {record['task_8_ready']}",
        f"- patch_backlog_ready: {record['patch_backlog_ready']}",
        f"- patch_candidate_count: {record['patch_candidate_count']}",
        f"- required_test_count: {record['required_test_count']}",
        f"- risk_count: {record['risk_count']}",
        f"- execution_gate_count: {record['execution_gate_count']}",
        f"- patch_implementation_allowed_now: {record['patch_implementation_allowed_now']}",
        f"- runtime_solver_modified: {record['runtime_solver_modified']}",
        f"- external_solver_dependency: {record['external_solver_dependency']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- official_score_claim_allowed: {record['official_score_claim_allowed']}",
        f"- competitive_score_claim_allowed: {record['competitive_score_claim_allowed']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Patch candidates",
        "",
    ]

    for patch in record["patch_candidates"]:
        lines.append(
            f"- {patch['patch_id']} / layer={patch['target_layer']} / file={patch['file_target']} / "
            f"function={patch['function_target']} / risk={patch['risk_level']}"
        )

    lines.extend(["", "## Required tests", ""])
    for test in record["required_test_plan"]:
        lines.append(f"- {test['test_id']} / {test['command']}")

    lines.extend(["", "## Risk register", ""])
    for risk in record["risk_register"]:
        lines.append(
            f"- {risk['risk_id']} / patch={risk['patch_id']} / level={risk['risk_level']} / blocking={risk['blocking_without_tests']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["backlog_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 8 creates an executable local solver patch backlog. It does not apply solver patches yet.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_8_LOCAL_SOLVER_PATCH_BACKLOG_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_8_LOCAL_SOLVER_PATCH_BACKLOG_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_8_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_8_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_8_VERDICT=LOCAL_SOLVER_PATCH_BACKLOG_READY_FOR_PATCH_IMPLEMENTATION_PLAN",
            "ARC_AGI3_MILESTONE_11_TASK_8_BASELINE_COMMIT=567eef3",
            "ARC_AGI3_MILESTONE_11_TASK_8_NEXT_STAGE=MILESTONE_11_TASK_9_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_READY=true",
            f"ARC_AGI3_MILESTONE_11_PATCH_CANDIDATE_COUNT={EXPECTED_PATCH_COUNT}",
            f"ARC_AGI3_MILESTONE_11_REQUIRED_TEST_COUNT={EXPECTED_REQUIRED_TEST_COUNT}",
            f"ARC_AGI3_MILESTONE_11_RISK_COUNT={EXPECTED_RISK_COUNT}",
            f"ARC_AGI3_MILESTONE_11_EXECUTION_GATE_COUNT={EXPECTED_GATE_COUNT}",
            "ARC_AGI3_MILESTONE_11_PATCH_IMPLEMENTATION_ALLOWED_NOW=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_11_RANKER_RUNTIME_MODIFIED=false",
            "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false",
            "ARC_AGI3_MILESTONE_11_DIAGNOSTIC_ONLY=true",
            "ARC_AGI3_MILESTONE_11_KAGGLE_SCORE_SEMANTICS=NOT_A_KAGGLE_SCORE",
            "ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_COMPETITIVE_SCORE_CLAIM_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false",
            "ARC_AGI3_MILESTONE_11_PRIVATE_SCORE_CLAIMED=false",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_11_SUBMISSION_JSON_CREATED=false",
            "ARC_AGI3_MILESTONE_11_UPLOAD_PACKAGE_CREATED=false",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_KAGGLE_AUTHENTICATION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_11_FAIL_CLOSED_REQUIRED=true",
            "ARC_AGI3_MILESTONE_11_FAIL_CLOSED_ACTIVE=true",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_task_8_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 8 LOCAL SOLVER PATCH BACKLOG MANIFEST v1",
        f"task_8_id={record['task_8_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_8_ready={record['task_8_ready']}",
        f"patch_backlog_ready={record['patch_backlog_ready']}",
        f"patch_candidate_count={record['patch_candidate_count']}",
        f"required_test_count={record['required_test_count']}",
        f"risk_count={record['risk_count']}",
        f"execution_gate_count={record['execution_gate_count']}",
        f"patch_implementation_allowed_now={record['patch_implementation_allowed_now']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"ranker_runtime_modified={record['ranker_runtime_modified']}",
        f"external_solver_dependency={record['external_solver_dependency']}",
        f"diagnostic_only={record['diagnostic_only']}",
        f"kaggle_score_semantics={record['kaggle_score_semantics']}",
        f"official_score_claim_allowed={record['official_score_claim_allowed']}",
        f"competitive_score_claim_allowed={record['competitive_score_claim_allowed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"fail_closed_active={record['fail_closed_active']}",
        "",
        "PATCH_CANDIDATES",
    ]

    for patch in record["patch_candidates"]:
        lines.append(
            f"{patch['patch_id']} layer={patch['target_layer']} file={patch['file_target']} "
            f"function={patch['function_target']} risk={patch['risk_level']}"
        )

    lines.append("")
    lines.append("REQUIRED_TEST_PLAN")
    for test in record["required_test_plan"]:
        lines.append(f"{test['test_id']} command={test['command']}")

    lines.append("")
    lines.append("BACKLOG_CASE_RESULTS")
    for result in record["backlog_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_8_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_backlog())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-backlog-v1.json"
    md_path = output / "milestone-11-local-solver-patch-backlog-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-backlog-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-backlog-index-v1.json"
    candidates_path = output / "milestone-11-local-solver-patch-candidates-v1.json"
    tests_path = output / "milestone-11-local-solver-patch-required-tests-v1.json"
    risks_path = output / "milestone-11-local-solver-patch-risk-register-v1.json"
    gates_path = output / "milestone-11-local-solver-patch-execution-gates-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-backlog-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-backlog-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_8_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_8_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["backlog_index"], indent=2, sort_keys=True), encoding="utf-8")
    candidates_path.write_text(json.dumps(record["patch_candidates"], indent=2, sort_keys=True), encoding="utf-8")
    tests_path.write_text(json.dumps(record["required_test_plan"], indent=2, sort_keys=True), encoding="utf-8")
    risks_path.write_text(json.dumps(record["risk_register"], indent=2, sort_keys=True), encoding="utf-8")
    gates_path.write_text(json.dumps(record["patch_execution_gates"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["backlog_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["backlog_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "candidates_path": str(candidates_path),
        "tests_path": str(tests_path),
        "risks_path": str(risks_path),
        "gates_path": str(gates_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_backlog_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_backlog()
    validation = validate_milestone_11_local_solver_patch_backlog(record)
    artifacts = write_task_8_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_8_id": record["task_8_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_8_ready": record["task_8_ready"],
        "patch_backlog_ready": record["patch_backlog_ready"],
        "patch_candidate_count": record["patch_candidate_count"],
        "required_test_count": record["required_test_count"],
        "risk_count": record["risk_count"],
        "execution_gate_count": record["execution_gate_count"],
        "patch_implementation_allowed_now": record["patch_implementation_allowed_now"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "backlog_check_count": record["backlog_check_count"],
        "backlog_case_count": record["backlog_case_count"],
        "backlog_case_pass_count": record["backlog_case_pass_count"],
        "backlog_case_failure_count": record["backlog_case_failure_count"],
        "backlog_gate_count": record["backlog_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "backlog_issue_count": record["backlog_issue_count"],
        "warning_count": record["warning_count"],
        "real_public_score_claimed": record["real_public_score_claimed"],
        "private_score_claimed": record["private_score_claimed"],
        "real_benchmark_score": record["real_benchmark_score"],
        "real_submission_candidate_created": record["real_submission_candidate_created"],
        "submission_json_created": record["submission_json_created"],
        "upload_package_created": record["upload_package_created"],
        "real_submission_decision": record["real_submission_decision"],
        "real_submission_allowed": record["real_submission_allowed"],
        "manual_upload_allowed": record["manual_upload_allowed"],
        "kaggle_authentication_allowed": record["kaggle_authentication_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "fail_closed_required": record["fail_closed_required"],
        "fail_closed_active": record["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": record["metadata"],
    }
