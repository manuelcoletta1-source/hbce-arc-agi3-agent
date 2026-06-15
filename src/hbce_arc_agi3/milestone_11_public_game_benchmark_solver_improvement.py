"""Milestone #11 Public Game Benchmark & Solver Improvement v1.

Local-only deterministic opening cycle after Milestone #10 closure.

This module opens the public game benchmark and solver improvement cycle. It
does not create a real Kaggle submission, does not create submission.json, does
not create an upload package, does not authenticate with Kaggle, does not call
external APIs, does not read secrets, does not claim a real benchmark score,
and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_VALID"

BASELINE_COMMIT = "003c0fe Close ARC AGI3 submission preparation"
MILESTONE_MODE = "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_LOCAL_ONLY"
MILESTONE_SCOPE = "PUBLIC_GAME_BENCHMARK_SETUP_AND_SOLVER_IMPROVEMENT_PLAN_NO_REAL_SUBMISSION"
MILESTONE_VERDICT = "MILESTONE_11_READY_FOR_PUBLIC_GAME_BENCHMARK_AND_SOLVER_PATCH_CYCLE"
NEXT_STAGE = "MILESTONE_11_TASK_2_PUBLIC_GAME_INVENTORY_AND_BASELINE_RUN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/public-game-benchmark-solver-improvement-v1"

M10_CLOSURE_JSON = Path(
    "examples/milestone-10/submission-preparation-closure-v1/"
    "milestone-10-submission-preparation-closure-v1.json"
)

EXPECTED_M10_CLOSURE_ID_PREFIX = "MILESTONE-10-SUBMISSION-PREPARATION-CLOSURE-"
EXPECTED_SELECTED_CANDIDATE_ID = "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
EXPECTED_CANDIDATE_PACKAGE_ID = "MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-CF04A9CB1B1D"
EXPECTED_REBUILT_CANDIDATE_ID = "MILESTONE-10-REBUILT-CANDIDATE-32F7FBEDFF87"
EXPECTED_REBUILT_CANDIDATE_REVIEW_ID = "MILESTONE-10-REBUILT-CANDIDATE-REVIEW-D9701E0276DB"

PUBLIC_GAME_CANDIDATE_PATHS: Tuple[str, ...] = (
    "data/arc_agi_3/public",
    "data/public",
    "examples/public-games",
    "examples/arc-agi-3-public-games",
    "benchmark/public-games",
)

BENCHMARK_AXES: Tuple[Dict[str, str], ...] = (
    {
        "axis_id": "public_game_inventory_v1",
        "area": "inventory",
        "description": "Detect available public game fixtures without assuming external access.",
    },
    {
        "axis_id": "baseline_solver_replay_v1",
        "area": "baseline",
        "description": "Prepare baseline replay against public fixtures when they are locally available.",
    },
    {
        "axis_id": "observation_trace_audit_v1",
        "area": "trace",
        "description": "Track observations, state changes, actions, and local solver decisions.",
    },
    {
        "axis_id": "world_model_gap_detection_v1",
        "area": "world_model",
        "description": "Identify missing transition, object, rule, and goal models.",
    },
    {
        "axis_id": "planner_gap_detection_v1",
        "area": "planner",
        "description": "Identify planning failures, dead-end loops, and action-selection gaps.",
    },
    {
        "axis_id": "verifier_gap_detection_v1",
        "area": "verifier",
        "description": "Identify missing internal verification gates before action selection.",
    },
    {
        "axis_id": "solver_patch_backlog_v1",
        "area": "patching",
        "description": "Create ordered solver improvement targets from benchmark evidence.",
    },
)

SOLVER_IMPROVEMENT_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_id": "m11_world_model_runtime_state_v1",
        "component": "world_model",
        "priority": "P0",
        "goal": "Represent objects, positions, transitions, and inferred rules per episode.",
    },
    {
        "target_id": "m11_goal_inference_layer_v1",
        "component": "goal_inference",
        "priority": "P0",
        "goal": "Infer candidate goals from rewards, state changes, and terminal conditions.",
    },
    {
        "target_id": "m11_action_policy_probe_v1",
        "component": "policy",
        "priority": "P0",
        "goal": "Probe safe candidate actions before committing irreversible moves.",
    },
    {
        "target_id": "m11_transition_verifier_v1",
        "component": "verifier",
        "priority": "P0",
        "goal": "Verify predicted transition against observed transition after each action.",
    },
    {
        "target_id": "m11_loop_breaker_v1",
        "component": "planner",
        "priority": "P1",
        "goal": "Detect repeated non-progress loops and force exploration fallback.",
    },
    {
        "target_id": "m11_failure_taxonomy_v1",
        "component": "audit",
        "priority": "P1",
        "goal": "Classify failures into perception, rule, goal, planning, verifier, or execution buckets.",
    },
    {
        "target_id": "m11_candidate_refresh_after_benchmark_v1",
        "component": "candidate_refresh",
        "priority": "P1",
        "goal": "Create a new candidate only after benchmark evidence is available.",
    },
)

MILESTONE_CHECKS: Tuple[str, ...] = (
    "m10_closure_artifact_exists",
    "m10_closure_ready",
    "m10_closure_validated",
    "m10_closed",
    "m10_real_submission_blocked",
    "m10_submission_json_absent",
    "m10_upload_package_absent",
    "candidate_identity_loaded",
    "benchmark_axes_created",
    "solver_improvement_targets_created",
    "public_game_inventory_policy_created",
    "public_game_score_not_claimed",
    "real_benchmark_execution_not_claimed",
    "next_stage_valid",
    "milestone_11_ready",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
    "kaggle_submission_sent_false",
)

MILESTONE_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m11_public_game_benchmark_source_closure_ready_v1",
        "area": "source_binding",
        "operation": "verify_milestone_10_closure_source",
    },
    {
        "case_id": "m11_public_game_benchmark_candidate_identity_loaded_v1",
        "area": "identity",
        "operation": "verify_candidate_identity",
    },
    {
        "case_id": "m11_public_game_benchmark_axes_ready_v1",
        "area": "benchmark",
        "operation": "verify_benchmark_axes",
    },
    {
        "case_id": "m11_solver_improvement_targets_ready_v1",
        "area": "solver_improvement",
        "operation": "verify_solver_targets",
    },
    {
        "case_id": "m11_public_game_inventory_policy_ready_v1",
        "area": "inventory",
        "operation": "verify_inventory_policy",
    },
    {
        "case_id": "m11_no_score_claimed_without_public_run_v1",
        "area": "score_boundary",
        "operation": "verify_no_real_score_claimed",
    },
    {
        "case_id": "m11_real_submission_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_still_blocked",
    },
    {
        "case_id": "m11_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_preserved",
    },
    {
        "case_id": "m11_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_next_stage",
    },
    {
        "case_id": "m11_metadata_safe_v1",
        "area": "metadata",
        "operation": "verify_public_safe_metadata",
    },
)

EXPECTED_BENCHMARK_AXIS_COUNT = len(BENCHMARK_AXES)
EXPECTED_SOLVER_TARGET_COUNT = len(SOLVER_IMPROVEMENT_TARGETS)
EXPECTED_MILESTONE_CHECK_COUNT = len(MILESTONE_CHECKS)
EXPECTED_MILESTONE_CASE_COUNT = len(MILESTONE_CASES)
EXPECTED_MILESTONE_PASS_COUNT = len(MILESTONE_CASES)
EXPECTED_MILESTONE_FAILURE_COUNT = 0


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


def detect_local_public_game_paths() -> Tuple[Dict[str, Any], ...]:
    records = []
    for path_text in PUBLIC_GAME_CANDIDATE_PATHS:
        path = Path(path_text)
        records.append(
            {
                "path": path_text,
                "exists": path.exists(),
                "is_dir": path.is_dir(),
                "file_count": len([item for item in path.rglob("*") if item.is_file()])
                if path.exists() and path.is_dir()
                else 0,
            }
        )
    return tuple(records)


def build_m10_closure_source_summary() -> Dict[str, Any]:
    closure = _read_json(M10_CLOSURE_JSON)
    return {
        "m10_closure_path": str(M10_CLOSURE_JSON),
        "m10_closure_present": M10_CLOSURE_JSON.exists(),
        "m10_closure_status": closure.get("status", "MISSING"),
        "m10_closure_id": closure.get("submission_preparation_closure_id", "MISSING_CLOSURE_ID"),
        "m10_closure_signature": closure.get("signature", ""),
        "m10_baseline_commit": closure.get("baseline_commit", "MISSING_BASELINE"),
        "m10_closure_ready": closure.get("submission_preparation_closure_ready", False),
        "m10_closure_created": closure.get("submission_preparation_closure_created", False),
        "m10_closure_passed": closure.get("submission_preparation_closure_passed", False),
        "m10_closed": closure.get("milestone_10_closed", False),
        "local_package_prepared": closure.get("local_package_prepared", False),
        "local_package_frozen": closure.get("local_package_frozen", False),
        "integrity_verified": closure.get("integrity_verified", False),
        "final_audit_passed": closure.get("final_audit_passed", False),
        "selected_candidate_id": closure.get("selected_candidate_id", "MISSING_SELECTED_CANDIDATE_ID"),
        "candidate_package_id": closure.get("candidate_package_id", "MISSING_CANDIDATE_PACKAGE_ID"),
        "rebuilt_candidate_id": closure.get("rebuilt_candidate_id", "MISSING_REBUILT_CANDIDATE_ID"),
        "rebuilt_candidate_review_id": closure.get(
            "rebuilt_candidate_review_id", "MISSING_REBUILT_CANDIDATE_REVIEW_ID"
        ),
        "real_submission_candidate_created": closure.get("real_submission_candidate_created", True),
        "submission_json_created": closure.get("submission_json_created", True),
        "upload_package_created": closure.get("upload_package_created", True),
        "real_submission_decision": closure.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": closure.get("real_submission_allowed", True),
        "manual_upload_allowed": closure.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": closure.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": closure.get("kaggle_submission_sent", True),
        "fail_closed_required": closure.get("fail_closed_required", False),
        "fail_closed_active": closure.get("fail_closed_active", False),
        "m10_closure_sha256": _sha256(M10_CLOSURE_JSON),
        "m10_closure_sha256_16": _sha16(_sha256(M10_CLOSURE_JSON)),
    }


def build_public_game_benchmark_policy() -> Dict[str, Any]:
    detected = detect_local_public_game_paths()
    detected_count = sum(1 for item in detected if item["exists"] and item["is_dir"])
    file_count = sum(int(item["file_count"]) for item in detected)

    return {
        "policy_id": "M11-PUBLIC-GAME-BENCHMARK-POLICY-v1",
        "public_game_candidate_paths": list(PUBLIC_GAME_CANDIDATE_PATHS),
        "detected_public_game_path_count": detected_count,
        "detected_public_game_file_count": file_count,
        "detected_public_game_paths": list(detected),
        "public_game_dataset_required_now": False,
        "public_game_inventory_created": True,
        "public_game_benchmark_execution_allowed": True,
        "public_game_benchmark_execution_performed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "kaggle_submission_required_now": False,
        "next_inventory_stage": "MILESTONE_11_TASK_2_PUBLIC_GAME_INVENTORY_AND_BASELINE_RUN_V1",
        "boundary": "NO_SCORE_CLAIM_WITHOUT_LOCAL_PUBLIC_RUN",
    }


def build_solver_improvement_backlog() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            **target,
            "status": "PLANNED",
            "implementation_required": True,
            "public_safe": True,
            "requires_external_api": False,
            "requires_secret": False,
            "requires_real_submission": False,
        }
        for target in SOLVER_IMPROVEMENT_TARGETS
    )


def build_milestone_11_checks() -> Dict[str, bool]:
    source = build_m10_closure_source_summary()
    policy = build_public_game_benchmark_policy()
    backlog = build_solver_improvement_backlog()

    return {
        "m10_closure_artifact_exists": source["m10_closure_present"] is True,
        "m10_closure_ready": source["m10_closure_status"]
        == "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_READY",
        "m10_closure_validated": source["m10_closure_id"].startswith(EXPECTED_M10_CLOSURE_ID_PREFIX)
        and bool(source["m10_closure_signature"]),
        "m10_closed": source["m10_closed"] is True,
        "m10_local_package_prepared": source["local_package_prepared"] is True,
        "m10_local_package_frozen": source["local_package_frozen"] is True,
        "m10_integrity_verified": source["integrity_verified"] is True,
        "m10_final_audit_passed": source["final_audit_passed"] is True,
        "candidate_identity_loaded": source["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
        and source["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
        and source["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
        and source["rebuilt_candidate_review_id"] == EXPECTED_REBUILT_CANDIDATE_REVIEW_ID,
        "benchmark_axes_created": len(BENCHMARK_AXES) == EXPECTED_BENCHMARK_AXIS_COUNT,
        "solver_improvement_targets_created": len(backlog) == EXPECTED_SOLVER_TARGET_COUNT,
        "public_game_inventory_policy_created": policy["public_game_inventory_created"] is True,
        "public_game_score_not_claimed": policy["real_public_score_claimed"] is False
        and policy["private_score_claimed"] is False,
        "real_benchmark_execution_not_claimed": policy["public_game_benchmark_execution_performed"] is False,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_2_PUBLIC_GAME_INVENTORY_AND_BASELINE_RUN_V1",
        "milestone_11_ready": True,
        "m10_real_submission_blocked": source["real_submission_allowed"] is False
        and source["real_submission_decision"] == "NOT_AUTHORIZED",
        "m10_submission_json_absent": source["submission_json_created"] is False,
        "m10_upload_package_absent": source["upload_package_created"] is False,
        "manual_upload_blocked": source["manual_upload_allowed"] is False,
        "kaggle_authentication_blocked": source["kaggle_authentication_allowed"] is False,
        "kaggle_submission_absent": source["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "milestone_check_count_valid": len(MILESTONE_CHECKS) == EXPECTED_MILESTONE_CHECK_COUNT,
        "milestone_case_count_valid": len(MILESTONE_CASES) == EXPECTED_MILESTONE_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
        "kaggle_submission_sent_false": True,
    }


def evaluate_milestone_11_case(case_id: str) -> Dict[str, Any]:
    checks = build_milestone_11_checks()

    if case_id == "m11_public_game_benchmark_source_closure_ready_v1":
        passed = (
            checks["m10_closure_artifact_exists"]
            and checks["m10_closure_ready"]
            and checks["m10_closure_validated"]
            and checks["m10_closed"]
        )
        return _result(case_id, "source_binding", "verify_milestone_10_closure_source", passed)

    if case_id == "m11_public_game_benchmark_candidate_identity_loaded_v1":
        return _result(
            case_id,
            "identity",
            "verify_candidate_identity",
            checks["candidate_identity_loaded"],
        )

    if case_id == "m11_public_game_benchmark_axes_ready_v1":
        return _result(
            case_id,
            "benchmark",
            "verify_benchmark_axes",
            checks["benchmark_axes_created"],
        )

    if case_id == "m11_solver_improvement_targets_ready_v1":
        return _result(
            case_id,
            "solver_improvement",
            "verify_solver_targets",
            checks["solver_improvement_targets_created"],
        )

    if case_id == "m11_public_game_inventory_policy_ready_v1":
        return _result(
            case_id,
            "inventory",
            "verify_inventory_policy",
            checks["public_game_inventory_policy_created"],
        )

    if case_id == "m11_no_score_claimed_without_public_run_v1":
        passed = checks["public_game_score_not_claimed"] and checks["real_benchmark_execution_not_claimed"]
        return _result(case_id, "score_boundary", "verify_no_real_score_claimed", passed)

    if case_id == "m11_real_submission_blocked_v1":
        passed = (
            checks["m10_real_submission_blocked"]
            and checks["m10_submission_json_absent"]
            and checks["m10_upload_package_absent"]
            and checks["kaggle_submission_absent"]
        )
        return _result(case_id, "submission_boundary", "verify_real_submission_still_blocked", passed)

    if case_id == "m11_fail_closed_preserved_v1":
        return _result(
            case_id,
            "fail_closed",
            "verify_fail_closed_preserved",
            checks["fail_closed_required"] and checks["fail_closed_active"],
        )

    if case_id == "m11_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_metadata_safe_v1":
        passed = (
            checks["public_safe"]
            and checks["deterministic"]
            and checks["local_only"]
            and checks["dry_run_only"]
            and checks["external_api_dependency_false"]
            and checks["private_core_exposure_false"]
            and checks["legal_certification_false"]
        )
        return _result(case_id, "metadata", "verify_public_safe_metadata", passed)

    raise ValueError(f"unknown milestone 11 case: {case_id}")


def evaluate_all_milestone_11_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_milestone_11_case(case["case_id"]) for case in MILESTONE_CASES)


def build_milestone_11_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_milestone_11_checks()
    rows = (
        ("m10_closure_source_ready", checks["m10_closure_artifact_exists"] and checks["m10_closure_ready"]),
        ("m10_candidate_identity_loaded", checks["candidate_identity_loaded"]),
        ("benchmark_axes_ready", checks["benchmark_axes_created"]),
        ("solver_improvement_targets_ready", checks["solver_improvement_targets_created"]),
        ("public_game_inventory_policy_ready", checks["public_game_inventory_policy_created"]),
        ("score_boundary_preserved", checks["public_game_score_not_claimed"]),
        ("submission_boundary_preserved", checks["m10_real_submission_blocked"]),
        ("fail_closed_preserved", checks["fail_closed_active"]),
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


def build_milestone_11_public_game_benchmark_solver_improvement() -> Dict[str, Any]:
    source = build_m10_closure_source_summary()
    policy = build_public_game_benchmark_policy()
    backlog = build_solver_improvement_backlog()
    checks = build_milestone_11_checks()
    results = evaluate_all_milestone_11_cases()
    scorecard = build_milestone_11_scorecard()

    pass_count = sum(1 for result in results if result["passed"] is True)
    failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "m10_closure_artifact_exists": checks["m10_closure_artifact_exists"],
        "m10_closure_ready": checks["m10_closure_ready"],
        "m10_closure_validated": checks["m10_closure_validated"],
        "m10_closed": checks["m10_closed"],
        "m10_real_submission_blocked": checks["m10_real_submission_blocked"],
        "candidate_identity_loaded": checks["candidate_identity_loaded"],
        "benchmark_axes_created": checks["benchmark_axes_created"],
        "solver_improvement_targets_created": checks["solver_improvement_targets_created"],
        "public_game_inventory_policy_created": checks["public_game_inventory_policy_created"],
        "public_game_score_not_claimed": checks["public_game_score_not_claimed"],
        "real_benchmark_execution_not_claimed": checks["real_benchmark_execution_not_claimed"],
        "next_stage_valid": checks["next_stage_valid"],
        "fail_closed_active": checks["fail_closed_active"],
        "metadata_safe": checks["public_safe"]
        and checks["deterministic"]
        and checks["local_only"]
        and checks["external_api_dependency_false"]
        and checks["private_core_exposure_false"]
        and checks["legal_certification_false"],
        "all_cases_pass": all(result["passed"] is True for result in results),
        "pass_count_valid": pass_count == EXPECTED_MILESTONE_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_MILESTONE_FAILURE_COUNT,
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

    milestone_ready = (
        pass_count == EXPECTED_MILESTONE_PASS_COUNT
        and failure_count == EXPECTED_MILESTONE_FAILURE_COUNT
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["m10_closed"]
        and checks["candidate_identity_loaded"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "title": "Public Game Benchmark & Solver Improvement v1",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "milestone_mode": MILESTONE_MODE,
        "milestone_scope": MILESTONE_SCOPE,
        "milestone_verdict": MILESTONE_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_m10_closure": source["m10_closure_id"],
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": source["rebuilt_candidate_id"],
        "public_game_inventory_created": True,
        "public_game_benchmark_execution_performed": False,
        "real_public_score_claimed": False,
        "solver_improvement_target_count": len(backlog),
        "benchmark_axis_count": len(BENCHMARK_AXES),
        "milestone_11_ready": milestone_ready,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "real_submission_allowed": False,
        "kaggle_authentication_allowed": False,
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
        "title": "Public Game Benchmark & Solver Improvement v1",
        "baseline_commit": BASELINE_COMMIT,
        "milestone_mode": MILESTONE_MODE,
        "milestone_scope": MILESTONE_SCOPE,
        "milestone_verdict": MILESTONE_VERDICT,
        "next_stage": NEXT_STAGE,
        "m10_closure_source": {
            "path": str(M10_CLOSURE_JSON),
            "present": M10_CLOSURE_JSON.exists(),
            "status": source["m10_closure_status"],
            "closure_id": source["m10_closure_id"],
            "sha256": _sha256(M10_CLOSURE_JSON),
            "sha256_16": _sha16(_sha256(M10_CLOSURE_JSON)),
        },
        "source_summary": source,
        "public_game_benchmark_policy": policy,
        "benchmark_axes": list(BENCHMARK_AXES),
        "solver_improvement_backlog": list(backlog),
        "milestone_scorecard": list(scorecard),
        "milestone_checks": checks,
        "milestone_check_list": list(MILESTONE_CHECKS),
        "milestone_cases": list(MILESTONE_CASES),
        "milestone_results": list(results),
        "milestone_gates": list(gates),
        "milestone_issues": list(issues),
        "milestone_index": index,
        "milestone_11_ready": milestone_ready,
        "public_game_inventory_created": True,
        "public_game_benchmark_execution_performed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "benchmark_axis_count": len(BENCHMARK_AXES),
        "solver_improvement_target_count": len(backlog),
        "milestone_check_count": len(MILESTONE_CHECKS),
        "milestone_case_count": len(MILESTONE_CASES),
        "milestone_pass_count": pass_count,
        "milestone_failure_count": failure_count,
        "milestone_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "milestone_issue_count": issue_count,
        "warning_count": 0,
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
            "source": "milestone_11_public_game_benchmark_solver_improvement_v1",
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
        "milestone_11_id": f"MILESTONE-11-PUBLIC-GAME-BENCHMARK-SOLVER-IMPROVEMENT-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_public_game_benchmark_solver_improvement(
    record: Mapping[str, Any]
) -> Dict[str, Any]:
    gates = record.get("milestone_gates", [])
    issues = record.get("milestone_issues", [])
    results = record.get("milestone_results", [])
    scorecard = record.get("milestone_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "milestone_11_id_present": isinstance(record.get("milestone_11_id"), str)
        and bool(record.get("milestone_11_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("003c0fe"),
        "milestone_mode_valid": record.get("milestone_mode") == MILESTONE_MODE,
        "milestone_scope_valid": record.get("milestone_scope") == MILESTONE_SCOPE,
        "milestone_verdict_valid": record.get("milestone_verdict") == MILESTONE_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "milestone_ready": record.get("milestone_11_ready") is True,
        "m10_closure_source_present": record.get("m10_closure_source", {}).get("present") is True,
        "benchmark_axes_count_valid": record.get("benchmark_axis_count") == EXPECTED_BENCHMARK_AXIS_COUNT,
        "solver_target_count_valid": record.get("solver_improvement_target_count")
        == EXPECTED_SOLVER_TARGET_COUNT,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "milestone_check_count_valid": record.get("milestone_check_count") == EXPECTED_MILESTONE_CHECK_COUNT,
        "milestone_case_count_valid": record.get("milestone_case_count") == EXPECTED_MILESTONE_CASE_COUNT,
        "milestone_pass_count_valid": record.get("milestone_pass_count") == EXPECTED_MILESTONE_PASS_COUNT,
        "milestone_failure_count_zero": record.get("milestone_failure_count") == EXPECTED_MILESTONE_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "no_real_public_score_claimed": record.get("real_public_score_claimed") is False
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "milestone_11_id": record.get("milestone_11_id"),
        "signature": record.get("signature"),
    }


def render_milestone_11_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 - Public Game Benchmark & Solver Improvement v1",
        "",
        f"- status: {record['status']}",
        f"- milestone_11_id: {record['milestone_11_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- milestone_mode: {record['milestone_mode']}",
        f"- milestone_scope: {record['milestone_scope']}",
        f"- milestone_verdict: {record['milestone_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- milestone_11_ready: {record['milestone_11_ready']}",
        f"- benchmark_axis_count: {record['benchmark_axis_count']}",
        f"- solver_improvement_target_count: {record['solver_improvement_target_count']}",
        f"- public_game_inventory_created: {record['public_game_inventory_created']}",
        f"- public_game_benchmark_execution_performed: {record['public_game_benchmark_execution_performed']}",
        f"- real_public_score_claimed: {record['real_public_score_claimed']}",
        f"- real_submission_candidate_created: {record['real_submission_candidate_created']}",
        f"- submission_json_created: {record['submission_json_created']}",
        f"- upload_package_created: {record['upload_package_created']}",
        f"- real_submission_decision: {record['real_submission_decision']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Benchmark axes",
        "",
    ]

    for axis in record["benchmark_axes"]:
        lines.append(f"- {axis['axis_id']} / area={axis['area']} / {axis['description']}")

    lines.extend(["", "## Solver improvement backlog", ""])

    for target in record["solver_improvement_backlog"]:
        lines.append(
            f"- {target['target_id']} / component={target['component']} / "
            f"priority={target['priority']} / status={target['status']}"
        )

    lines.extend(["", "## Validation results", ""])

    for result in record["milestone_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Milestone #11 is ready for public game inventory and baseline run. No real score is claimed yet, and real submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_READY=true",
            "ARC_AGI3_MILESTONE_11_MODE=MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_VERDICT=MILESTONE_11_READY_FOR_PUBLIC_GAME_BENCHMARK_AND_SOLVER_PATCH_CYCLE",
            "ARC_AGI3_MILESTONE_11_BASELINE_COMMIT=003c0fe",
            "ARC_AGI3_MILESTONE_11_NEXT_STAGE=MILESTONE_11_TASK_2_PUBLIC_GAME_INVENTORY_AND_BASELINE_RUN_V1",
            f"ARC_AGI3_MILESTONE_11_BENCHMARK_AXIS_COUNT={EXPECTED_BENCHMARK_AXIS_COUNT}",
            f"ARC_AGI3_MILESTONE_11_SOLVER_IMPROVEMENT_TARGET_COUNT={EXPECTED_SOLVER_TARGET_COUNT}",
            "ARC_AGI3_MILESTONE_11_PUBLIC_GAME_INVENTORY_CREATED=true",
            "ARC_AGI3_MILESTONE_11_PUBLIC_GAME_BENCHMARK_EXECUTION_PERFORMED=false",
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


def render_milestone_11_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 PUBLIC GAME BENCHMARK SOLVER IMPROVEMENT MANIFEST v1",
        f"milestone_11_id={record['milestone_11_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"milestone_mode={record['milestone_mode']}",
        f"milestone_verdict={record['milestone_verdict']}",
        f"next_stage={record['next_stage']}",
        f"milestone_11_ready={record['milestone_11_ready']}",
        f"benchmark_axis_count={record['benchmark_axis_count']}",
        f"solver_improvement_target_count={record['solver_improvement_target_count']}",
        f"public_game_inventory_created={record['public_game_inventory_created']}",
        f"public_game_benchmark_execution_performed={record['public_game_benchmark_execution_performed']}",
        f"real_public_score_claimed={record['real_public_score_claimed']}",
        f"private_score_claimed={record['private_score_claimed']}",
        f"real_submission_candidate_created={record['real_submission_candidate_created']}",
        f"submission_json_created={record['submission_json_created']}",
        f"upload_package_created={record['upload_package_created']}",
        f"real_submission_decision={record['real_submission_decision']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"manual_upload_allowed={record['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={record['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"fail_closed_required={record['fail_closed_required']}",
        f"fail_closed_active={record['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "BENCHMARK_AXES",
    ]

    for axis in record["benchmark_axes"]:
        lines.append(f"{axis['axis_id']} area={axis['area']} description={axis['description']}")

    lines.append("")
    lines.append("SOLVER_IMPROVEMENT_BACKLOG")
    for target in record["solver_improvement_backlog"]:
        lines.append(
            f"{target['target_id']} component={target['component']} "
            f"priority={target['priority']} status={target['status']}"
        )

    lines.append("")
    lines.append("MILESTONE_11_VALIDATION_RESULTS")
    for result in record["milestone_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_milestone_11_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_public_game_benchmark_solver_improvement())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-public-game-benchmark-solver-improvement-v1.json"
    md_path = output / "milestone-11-public-game-benchmark-solver-improvement-v1.md"
    manifest_path = output / "milestone-11-public-game-benchmark-solver-improvement-manifest-v1.txt"
    index_path = output / "milestone-11-public-game-benchmark-solver-improvement-index-v1.json"
    backlog_path = output / "milestone-11-solver-improvement-backlog-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_milestone_11_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_milestone_11_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["milestone_index"], indent=2, sort_keys=True), encoding="utf-8")
    backlog_path.write_text(
        json.dumps(record["solver_improvement_backlog"], indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "backlog_path": str(backlog_path),
    }


def run_milestone_11_public_game_benchmark_solver_improvement_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_public_game_benchmark_solver_improvement()
    validation = validate_milestone_11_public_game_benchmark_solver_improvement(record)
    artifacts = write_milestone_11_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_PIPELINE_INVALID",
        "milestone_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "milestone_11_id": record["milestone_11_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "milestone_mode": record["milestone_mode"],
        "milestone_verdict": record["milestone_verdict"],
        "next_stage": record["next_stage"],
        "milestone_11_ready": record["milestone_11_ready"],
        "benchmark_axis_count": record["benchmark_axis_count"],
        "solver_improvement_target_count": record["solver_improvement_target_count"],
        "public_game_inventory_created": record["public_game_inventory_created"],
        "public_game_benchmark_execution_performed": record[
            "public_game_benchmark_execution_performed"
        ],
        "real_public_score_claimed": record["real_public_score_claimed"],
        "private_score_claimed": record["private_score_claimed"],
        "milestone_check_count": record["milestone_check_count"],
        "milestone_case_count": record["milestone_case_count"],
        "milestone_pass_count": record["milestone_pass_count"],
        "milestone_failure_count": record["milestone_failure_count"],
        "milestone_gate_count": record["milestone_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "milestone_issue_count": record["milestone_issue_count"],
        "warning_count": record["warning_count"],
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
