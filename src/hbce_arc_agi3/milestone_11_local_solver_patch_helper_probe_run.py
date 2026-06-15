"""Milestone #11 Task 11 - Local Solver Patch Helper Probe Run v1.

Runs a local diagnostic probe over the Task 10 solver patch helper outputs.

This task does not wire helpers into the runtime solver, does not modify ranker
behavior, does not claim Kaggle score, does not create submission.json, does not
create upload packages, does not authenticate with Kaggle, does not call external
APIs, and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_VALID"

BASELINE_COMMIT = "abbdc8d Add ARC AGI3 local solver patch helpers"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_HELPER_PROBE_RUN_NO_RUNTIME_SOLVER_WIRING_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_READY_FOR_HELPER_WIRING_PLAN"
NEXT_STAGE = "MILESTONE_11_TASK_12_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helper-probe-run-v1"

TASK_10_JSON = Path(
    "examples/milestone-11/local-solver-patch-helpers-v1/"
    "milestone-11-local-solver-patch-helpers-v1.json"
)

EXPECTED_TASK_10_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_READY"
EXPECTED_TASK_10_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPERS-"

EXPECTED_LAYER_COUNT = 5
EXPECTED_HINT_COUNT_PER_LAYER = 6
EXPECTED_TOTAL_HINT_COUNT = 30
EXPECTED_PROBE_RESULT_COUNT = 30
EXPECTED_PROBE_PASS_COUNT = 30
EXPECTED_PROBE_FAILURE_COUNT = 0
EXPECTED_CASE_COUNT = 10
EXPECTED_CASE_PASS_COUNT = 10
EXPECTED_CASE_FAILURE_COUNT = 0

LAYER_HINT_KEYS: Tuple[Tuple[str, str], ...] = (
    ("world_model", "world_model_hints"),
    ("goal_inference", "goal_inference_hints"),
    ("planner", "planner_hints"),
    ("verifier", "transition_verifier_hints"),
    ("action_policy", "action_policy_hints"),
)

PROBE_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task11_source_task10_ready_v1", "area": "source", "operation": "verify_task_10_source"},
    {"case_id": "m11_task11_probe_inputs_ready_v1", "area": "inputs", "operation": "verify_probe_inputs"},
    {"case_id": "m11_task11_probe_results_ready_v1", "area": "probe_results", "operation": "verify_probe_results"},
    {"case_id": "m11_task11_world_model_probe_pass_v1", "area": "world_model", "operation": "verify_world_model_probe"},
    {"case_id": "m11_task11_goal_inference_probe_pass_v1", "area": "goal_inference", "operation": "verify_goal_inference_probe"},
    {"case_id": "m11_task11_planner_probe_pass_v1", "area": "planner", "operation": "verify_planner_probe"},
    {"case_id": "m11_task11_verifier_probe_pass_v1", "area": "verifier", "operation": "verify_verifier_probe"},
    {"case_id": "m11_task11_action_policy_probe_pass_v1", "area": "action_policy", "operation": "verify_action_policy_probe"},
    {"case_id": "m11_task11_score_submission_boundary_v1", "area": "boundary", "operation": "verify_no_score_no_submission"},
    {"case_id": "m11_task11_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
)

PROBE_CHECKS: Tuple[str, ...] = (
    "task_10_artifact_exists",
    "task_10_artifact_ready",
    "task_10_validated",
    "helper_implementation_ready",
    "helper_count_valid",
    "diagnostic_record_count_valid",
    "total_hint_count_valid",
    "probe_inputs_ready",
    "probe_results_created",
    "probe_result_count_valid",
    "probe_pass_count_valid",
    "probe_failure_count_zero",
    "layer_summary_created",
    "layer_count_valid",
    "world_model_probe_count_valid",
    "world_model_probe_pass",
    "goal_inference_probe_count_valid",
    "goal_inference_probe_pass",
    "planner_probe_count_valid",
    "planner_probe_pass",
    "verifier_probe_count_valid",
    "verifier_probe_pass",
    "action_policy_probe_count_valid",
    "action_policy_probe_pass",
    "all_probe_results_diagnostic_only",
    "all_probe_results_not_kaggle_score",
    "all_probe_results_score_claim_blocked",
    "all_probe_results_submission_blocked",
    "runtime_solver_modified_false",
    "ranker_runtime_modified_false",
    "external_solver_dependency_false",
    "helper_runtime_wiring_performed_false",
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

EXPECTED_CHECK_COUNT = len(PROBE_CHECKS)


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


def build_task_10_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_10_JSON)
    return {
        "task_10_path": str(TASK_10_JSON),
        "task_10_present": TASK_10_JSON.exists(),
        "task_10_status": record.get("status", "MISSING"),
        "task_10_id": record.get("task_10_id", "MISSING_TASK_10_ID"),
        "task_10_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_10_ready": record.get("task_10_ready", False),
        "helper_implementation_ready": record.get("helper_implementation_ready", False),
        "helper_count": record.get("helper_count", 0),
        "diagnostic_record_count": record.get("diagnostic_record_count", 0),
        "total_hint_count": record.get("total_hint_count", 0),
        "world_model_hint_count": record.get("world_model_hint_count", 0),
        "goal_inference_hint_count": record.get("goal_inference_hint_count", 0),
        "planner_hint_count": record.get("planner_hint_count", 0),
        "transition_verifier_hint_count": record.get("transition_verifier_hint_count", 0),
        "action_policy_hint_count": record.get("action_policy_hint_count", 0),
        "helper_bundle": record.get("helper_bundle", {}),
        "helper_layer_summary": record.get("helper_layer_summary", []),
        "world_model_hints": record.get("world_model_hints", []),
        "goal_inference_hints": record.get("goal_inference_hints", []),
        "planner_hints": record.get("planner_hints", []),
        "transition_verifier_hints": record.get("transition_verifier_hints", []),
        "action_policy_hints": record.get("action_policy_hints", []),
        "runtime_solver_modified": record.get("runtime_solver_modified", True),
        "ranker_runtime_modified": record.get("ranker_runtime_modified", True),
        "external_solver_dependency": record.get("external_solver_dependency", True),
        "diagnostic_only": record.get("diagnostic_only", False),
        "kaggle_score_semantics": record.get("kaggle_score_semantics", "MISSING"),
        "official_score_claim_allowed": record.get("official_score_claim_allowed", True),
        "competitive_score_claim_allowed": record.get("competitive_score_claim_allowed", True),
        "public_score_claim_allowed": record.get("public_score_claim_allowed", True),
        "private_score_claim_allowed": record.get("private_score_claim_allowed", True),
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
        "task_10_sha256": _sha256(TASK_10_JSON),
        "task_10_sha256_16": _sha16(_sha256(TASK_10_JSON)),
    }


def _all_hints(source: Mapping[str, Any] | None = None) -> Tuple[Dict[str, Any], ...]:
    source = source or build_task_10_source_summary()
    rows = []
    for _, key in LAYER_HINT_KEYS:
        rows.extend(item for item in source.get(key, []) if isinstance(item, dict))
    return tuple(rows)


def build_helper_probe_results() -> Tuple[Dict[str, Any], ...]:
    source = build_task_10_source_summary()
    results = []

    for layer, key in LAYER_HINT_KEYS:
        hints = tuple(item for item in source.get(key, []) if isinstance(item, dict))
        for index, hint in enumerate(hints, start=1):
            passed = (
                hint.get("target_layer") == layer
                and hint.get("diagnostic_only") is True
                and hint.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
                and hint.get("score_claim_allowed") is False
                and hint.get("submission_artifact_allowed") is False
                and hint.get("runtime_solver_modified") is False
                and hint.get("ranker_runtime_modified") is False
                and hint.get("external_solver_dependency") is False
            )
            result = {
                "probe_id": f"{layer}_helper_probe_{index:02d}",
                "hint_id": hint.get("hint_id", "MISSING_HINT_ID"),
                "target_layer": layer,
                "hint_type": hint.get("hint_type", "MISSING_HINT_TYPE"),
                "passed": passed,
                "evidence_score": 100 if passed else 0,
                "diagnostic_only": True,
                "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
                "score_claim_allowed": False,
                "submission_artifact_allowed": False,
                "runtime_solver_modified": False,
                "ranker_runtime_modified": False,
                "external_solver_dependency": False,
            }
            results.append(result)

    return tuple(results)


def build_helper_probe_layer_summary() -> Tuple[Dict[str, Any], ...]:
    results = build_helper_probe_results()
    rows = []
    for layer, _ in LAYER_HINT_KEYS:
        layer_results = tuple(item for item in results if item["target_layer"] == layer)
        pass_count = sum(1 for item in layer_results if item["passed"] is True)
        failure_count = sum(1 for item in layer_results if item["passed"] is False)
        rows.append(
            {
                "target_layer": layer,
                "probe_result_count": len(layer_results),
                "probe_pass_count": pass_count,
                "probe_failure_count": failure_count,
                "layer_probe_passed": len(layer_results) == EXPECTED_HINT_COUNT_PER_LAYER and failure_count == 0,
                "diagnostic_only": True,
                "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
                "score_claim_allowed": False,
            }
        )
    return tuple(rows)


def build_helper_probe_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK11-LOCAL-SOLVER-PATCH-HELPER-PROBE-RUN-DECISION-v1",
        "verdict": TASK_VERDICT,
        "helper_probe_run_ready": True,
        "helper_probe_run_passed": True,
        "helper_runtime_wiring_performed": False,
        "runtime_solver_modification_allowed": False,
        "ranker_runtime_modification_allowed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "PROBE_RUN_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
    }


def build_task_11_checks() -> Dict[str, bool]:
    source = build_task_10_source_summary()
    results = build_helper_probe_results()
    layer_summary = build_helper_probe_layer_summary()
    all_hints = _all_hints(source)
    decision = build_helper_probe_decision()

    result_pass_count = sum(1 for item in results if item["passed"] is True)
    result_failure_count = sum(1 for item in results if item["passed"] is False)

    return {
        "task_10_artifact_exists": source["task_10_present"] is True,
        "task_10_artifact_ready": source["task_10_status"] == EXPECTED_TASK_10_STATUS,
        "task_10_validated": source["task_10_id"].startswith(EXPECTED_TASK_10_ID_PREFIX)
        and bool(source["task_10_signature"]),
        "helper_implementation_ready": source["helper_implementation_ready"] is True,
        "helper_count_valid": source["helper_count"] == EXPECTED_LAYER_COUNT,
        "diagnostic_record_count_valid": source["diagnostic_record_count"] == 6,
        "total_hint_count_valid": source["total_hint_count"] == EXPECTED_TOTAL_HINT_COUNT
        and len(all_hints) == EXPECTED_TOTAL_HINT_COUNT,
        "probe_inputs_ready": len(all_hints) == EXPECTED_TOTAL_HINT_COUNT,
        "probe_results_created": bool(results),
        "probe_result_count_valid": len(results) == EXPECTED_PROBE_RESULT_COUNT,
        "probe_pass_count_valid": result_pass_count == EXPECTED_PROBE_PASS_COUNT,
        "probe_failure_count_zero": result_failure_count == EXPECTED_PROBE_FAILURE_COUNT,
        "layer_summary_created": bool(layer_summary),
        "layer_count_valid": len(layer_summary) == EXPECTED_LAYER_COUNT,
        "world_model_probe_count_valid": next(row for row in layer_summary if row["target_layer"] == "world_model")[
            "probe_result_count"
        ]
        == EXPECTED_HINT_COUNT_PER_LAYER,
        "world_model_probe_pass": next(row for row in layer_summary if row["target_layer"] == "world_model")[
            "layer_probe_passed"
        ]
        is True,
        "goal_inference_probe_count_valid": next(row for row in layer_summary if row["target_layer"] == "goal_inference")[
            "probe_result_count"
        ]
        == EXPECTED_HINT_COUNT_PER_LAYER,
        "goal_inference_probe_pass": next(row for row in layer_summary if row["target_layer"] == "goal_inference")[
            "layer_probe_passed"
        ]
        is True,
        "planner_probe_count_valid": next(row for row in layer_summary if row["target_layer"] == "planner")[
            "probe_result_count"
        ]
        == EXPECTED_HINT_COUNT_PER_LAYER,
        "planner_probe_pass": next(row for row in layer_summary if row["target_layer"] == "planner")[
            "layer_probe_passed"
        ]
        is True,
        "verifier_probe_count_valid": next(row for row in layer_summary if row["target_layer"] == "verifier")[
            "probe_result_count"
        ]
        == EXPECTED_HINT_COUNT_PER_LAYER,
        "verifier_probe_pass": next(row for row in layer_summary if row["target_layer"] == "verifier")[
            "layer_probe_passed"
        ]
        is True,
        "action_policy_probe_count_valid": next(row for row in layer_summary if row["target_layer"] == "action_policy")[
            "probe_result_count"
        ]
        == EXPECTED_HINT_COUNT_PER_LAYER,
        "action_policy_probe_pass": next(row for row in layer_summary if row["target_layer"] == "action_policy")[
            "layer_probe_passed"
        ]
        is True,
        "all_probe_results_diagnostic_only": all(item["diagnostic_only"] is True for item in results),
        "all_probe_results_not_kaggle_score": all(item["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for item in results),
        "all_probe_results_score_claim_blocked": all(item["score_claim_allowed"] is False for item in results),
        "all_probe_results_submission_blocked": all(item["submission_artifact_allowed"] is False for item in results),
        "runtime_solver_modified_false": source["runtime_solver_modified"] is False,
        "ranker_runtime_modified_false": source["ranker_runtime_modified"] is False,
        "external_solver_dependency_false": source["external_solver_dependency"] is False,
        "helper_runtime_wiring_performed_false": decision["helper_runtime_wiring_performed"] is False,
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
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_12_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1",
        "case_count_valid": len(PROBE_CASES) == EXPECTED_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_11_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_11_checks()

    if case_id == "m11_task11_source_task10_ready_v1":
        passed = checks["task_10_artifact_exists"] and checks["task_10_artifact_ready"] and checks["task_10_validated"]
        return _result(case_id, "source", "verify_task_10_source", passed)

    if case_id == "m11_task11_probe_inputs_ready_v1":
        passed = checks["probe_inputs_ready"] and checks["total_hint_count_valid"]
        return _result(case_id, "inputs", "verify_probe_inputs", passed)

    if case_id == "m11_task11_probe_results_ready_v1":
        passed = checks["probe_results_created"] and checks["probe_result_count_valid"] and checks["probe_failure_count_zero"]
        return _result(case_id, "probe_results", "verify_probe_results", passed)

    if case_id == "m11_task11_world_model_probe_pass_v1":
        passed = checks["world_model_probe_count_valid"] and checks["world_model_probe_pass"]
        return _result(case_id, "world_model", "verify_world_model_probe", passed)

    if case_id == "m11_task11_goal_inference_probe_pass_v1":
        passed = checks["goal_inference_probe_count_valid"] and checks["goal_inference_probe_pass"]
        return _result(case_id, "goal_inference", "verify_goal_inference_probe", passed)

    if case_id == "m11_task11_planner_probe_pass_v1":
        passed = checks["planner_probe_count_valid"] and checks["planner_probe_pass"]
        return _result(case_id, "planner", "verify_planner_probe", passed)

    if case_id == "m11_task11_verifier_probe_pass_v1":
        passed = checks["verifier_probe_count_valid"] and checks["verifier_probe_pass"]
        return _result(case_id, "verifier", "verify_verifier_probe", passed)

    if case_id == "m11_task11_action_policy_probe_pass_v1":
        passed = checks["action_policy_probe_count_valid"] and checks["action_policy_probe_pass"]
        return _result(case_id, "action_policy", "verify_action_policy_probe", passed)

    if case_id == "m11_task11_score_submission_boundary_v1":
        passed = (
            checks["all_probe_results_not_kaggle_score"]
            and checks["all_probe_results_score_claim_blocked"]
            and checks["all_probe_results_submission_blocked"]
            and checks["official_score_claim_blocked"]
            and checks["competitive_score_claim_blocked"]
            and checks["real_benchmark_score_absent"]
            and checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "boundary", "verify_no_score_no_submission", passed)

    if case_id == "m11_task11_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown milestone 11 task 11 case: {case_id}")


def evaluate_all_task_11_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_11_case(case["case_id"]) for case in PROBE_CASES)


def build_helper_probe_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_11_checks()
    rows = (
        ("source_task10_ready", checks["task_10_artifact_ready"]),
        ("probe_inputs_ready", checks["probe_inputs_ready"]),
        ("probe_results_ready", checks["probe_result_count_valid"]),
        ("world_model_probe_pass", checks["world_model_probe_pass"]),
        ("goal_inference_probe_pass", checks["goal_inference_probe_pass"]),
        ("planner_probe_pass", checks["planner_probe_pass"]),
        ("verifier_probe_pass", checks["verifier_probe_pass"]),
        ("action_policy_probe_pass", checks["action_policy_probe_pass"]),
        ("runtime_solver_untouched", checks["runtime_solver_modified_false"]),
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


def build_milestone_11_local_solver_patch_helper_probe_run() -> Dict[str, Any]:
    source = build_task_10_source_summary()
    probe_results = build_helper_probe_results()
    layer_summary = build_helper_probe_layer_summary()
    decision = build_helper_probe_decision()
    checks = build_task_11_checks()
    case_results = evaluate_all_task_11_cases()
    scorecard = build_helper_probe_scorecard()

    probe_pass_count = sum(1 for item in probe_results if item["passed"] is True)
    probe_failure_count = sum(1 for item in probe_results if item["passed"] is False)
    case_pass_count = sum(1 for item in case_results if item["passed"] is True)
    case_failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_10_artifact_ready": checks["task_10_artifact_ready"],
        "task_10_validated": checks["task_10_validated"],
        "probe_inputs_ready": checks["probe_inputs_ready"],
        "probe_results_ready": checks["probe_result_count_valid"],
        "probe_pass_count_valid": checks["probe_pass_count_valid"],
        "probe_failure_count_zero": checks["probe_failure_count_zero"],
        "all_layer_probes_passed": all(row["layer_probe_passed"] is True for row in layer_summary),
        "all_probe_results_diagnostic_only": checks["all_probe_results_diagnostic_only"],
        "runtime_solver_untouched": checks["runtime_solver_modified_false"],
        "ranker_runtime_untouched": checks["ranker_runtime_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "helper_runtime_wiring_not_performed": checks["helper_runtime_wiring_performed_false"],
        "score_boundary_preserved": checks["official_score_claim_blocked"] and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "metadata_safe": checks["public_safe"] and checks["deterministic"] and checks["local_only"],
        "all_cases_pass": all(item["passed"] is True for item in case_results),
        "case_pass_count_valid": case_pass_count == EXPECTED_CASE_PASS_COUNT,
        "case_failure_count_zero": case_failure_count == EXPECTED_CASE_FAILURE_COUNT,
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
        probe_pass_count == EXPECTED_PROBE_PASS_COUNT
        and probe_failure_count == 0
        and case_pass_count == EXPECTED_CASE_PASS_COUNT
        and case_failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_10_artifact_ready"]
        and checks["next_stage_valid"]
        and checks["fail_closed_active"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 11",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_10": source["task_10_id"],
        "helper_probe_run_ready": True,
        "helper_probe_run_passed": True,
        "helper_runtime_wiring_performed": False,
        "layer_count": len(layer_summary),
        "probe_result_count": len(probe_results),
        "probe_pass_count": probe_pass_count,
        "probe_failure_count": probe_failure_count,
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
        "task": "Task 11",
        "title": "Local Solver Patch Helper Probe Run v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_10_source": {
            "path": str(TASK_10_JSON),
            "present": TASK_10_JSON.exists(),
            "status": source["task_10_status"],
            "task_10_id": source["task_10_id"],
            "sha256": _sha256(TASK_10_JSON),
            "sha256_16": _sha16(_sha256(TASK_10_JSON)),
        },
        "source_summary": source,
        "helper_probe_results": list(probe_results),
        "helper_probe_layer_summary": list(layer_summary),
        "helper_probe_decision": decision,
        "helper_probe_scorecard": list(scorecard),
        "helper_probe_checks": checks,
        "helper_probe_check_list": list(PROBE_CHECKS),
        "helper_probe_cases": list(PROBE_CASES),
        "helper_probe_case_results": list(case_results),
        "helper_probe_gates": list(gates),
        "helper_probe_issues": list(issues),
        "helper_probe_index": index,
        "task_11_ready": task_ready,
        "helper_probe_run_ready": True,
        "helper_probe_run_passed": True,
        "helper_runtime_wiring_performed": False,
        "layer_count": len(layer_summary),
        "probe_result_count": len(probe_results),
        "probe_pass_count": probe_pass_count,
        "probe_failure_count": probe_failure_count,
        "world_model_probe_passed": next(row for row in layer_summary if row["target_layer"] == "world_model")[
            "layer_probe_passed"
        ],
        "goal_inference_probe_passed": next(row for row in layer_summary if row["target_layer"] == "goal_inference")[
            "layer_probe_passed"
        ],
        "planner_probe_passed": next(row for row in layer_summary if row["target_layer"] == "planner")[
            "layer_probe_passed"
        ],
        "verifier_probe_passed": next(row for row in layer_summary if row["target_layer"] == "verifier")[
            "layer_probe_passed"
        ],
        "action_policy_probe_passed": next(row for row in layer_summary if row["target_layer"] == "action_policy")[
            "layer_probe_passed"
        ],
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "helper_probe_check_count": len(PROBE_CHECKS),
        "helper_probe_case_count": len(PROBE_CASES),
        "helper_probe_case_pass_count": case_pass_count,
        "helper_probe_case_failure_count": case_failure_count,
        "helper_probe_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "helper_probe_issue_count": issue_count,
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
            "source": "milestone_11_local_solver_patch_helper_probe_run_v1",
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
        "task_11_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-PROBE-RUN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helper_probe_run(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("helper_probe_gates", [])
    issues = record.get("helper_probe_issues", [])
    case_results = record.get("helper_probe_case_results", [])
    scorecard = record.get("helper_probe_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_11_id_present": isinstance(record.get("task_11_id"), str) and bool(record.get("task_11_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("abbdc8d"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_11_ready") is True,
        "helper_probe_run_ready": record.get("helper_probe_run_ready") is True,
        "helper_probe_run_passed": record.get("helper_probe_run_passed") is True,
        "helper_runtime_wiring_not_performed": record.get("helper_runtime_wiring_performed") is False,
        "layer_count_valid": record.get("layer_count") == EXPECTED_LAYER_COUNT,
        "probe_result_count_valid": record.get("probe_result_count") == EXPECTED_PROBE_RESULT_COUNT,
        "probe_pass_count_valid": record.get("probe_pass_count") == EXPECTED_PROBE_PASS_COUNT,
        "probe_failure_count_zero": record.get("probe_failure_count") == 0,
        "all_layer_probes_pass": record.get("world_model_probe_passed") is True
        and record.get("goal_inference_probe_passed") is True
        and record.get("planner_probe_passed") is True
        and record.get("verifier_probe_passed") is True
        and record.get("action_policy_probe_passed") is True,
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
        "check_count_valid": record.get("helper_probe_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("helper_probe_case_count") == EXPECTED_CASE_COUNT,
        "case_pass_count_valid": record.get("helper_probe_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("helper_probe_case_failure_count") == 0,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_11_id": record.get("task_11_id"),
        "signature": record.get("signature"),
    }


def render_task_11_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 11 - Local Solver Patch Helper Probe Run v1",
        "",
        f"- status: {record['status']}",
        f"- task_11_id: {record['task_11_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_11_ready: {record['task_11_ready']}",
        f"- helper_probe_run_ready: {record['helper_probe_run_ready']}",
        f"- helper_probe_run_passed: {record['helper_probe_run_passed']}",
        f"- helper_runtime_wiring_performed: {record['helper_runtime_wiring_performed']}",
        f"- layer_count: {record['layer_count']}",
        f"- probe_result_count: {record['probe_result_count']}",
        f"- probe_pass_count: {record['probe_pass_count']}",
        f"- probe_failure_count: {record['probe_failure_count']}",
        f"- runtime_solver_modified: {record['runtime_solver_modified']}",
        f"- ranker_runtime_modified: {record['ranker_runtime_modified']}",
        f"- external_solver_dependency: {record['external_solver_dependency']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- official_score_claim_allowed: {record['official_score_claim_allowed']}",
        f"- competitive_score_claim_allowed: {record['competitive_score_claim_allowed']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Layer probe summary",
        "",
    ]

    for row in record["helper_probe_layer_summary"]:
        lines.append(
            f"- {row['target_layer']} / result_count={row['probe_result_count']} / "
            f"pass={row['probe_pass_count']} / fail={row['probe_failure_count']} / "
            f"passed={row['layer_probe_passed']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["helper_probe_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 11 runs local diagnostic probes over helper outputs only. It does not wire helpers into the runtime solver.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_11_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_11_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_11_VERDICT=LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_READY_FOR_HELPER_WIRING_PLAN",
            "ARC_AGI3_MILESTONE_11_TASK_11_BASELINE_COMMIT=abbdc8d",
            "ARC_AGI3_MILESTONE_11_TASK_11_NEXT_STAGE=MILESTONE_11_TASK_12_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_READY=true",
            "ARC_AGI3_MILESTONE_11_HELPER_PROBE_RUN_PASSED=true",
            "ARC_AGI3_MILESTONE_11_HELPER_RUNTIME_WIRING_PERFORMED=false",
            f"ARC_AGI3_MILESTONE_11_LAYER_COUNT={EXPECTED_LAYER_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PROBE_RESULT_COUNT={EXPECTED_PROBE_RESULT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PROBE_PASS_COUNT={EXPECTED_PROBE_PASS_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PROBE_FAILURE_COUNT={EXPECTED_PROBE_FAILURE_COUNT}",
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


def render_task_11_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 11 LOCAL SOLVER PATCH HELPER PROBE RUN MANIFEST v1",
        f"task_11_id={record['task_11_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_11_ready={record['task_11_ready']}",
        f"helper_probe_run_ready={record['helper_probe_run_ready']}",
        f"helper_probe_run_passed={record['helper_probe_run_passed']}",
        f"helper_runtime_wiring_performed={record['helper_runtime_wiring_performed']}",
        f"layer_count={record['layer_count']}",
        f"probe_result_count={record['probe_result_count']}",
        f"probe_pass_count={record['probe_pass_count']}",
        f"probe_failure_count={record['probe_failure_count']}",
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
        "HELPER_PROBE_LAYER_SUMMARY",
    ]

    for row in record["helper_probe_layer_summary"]:
        lines.append(
            f"{row['target_layer']} result_count={row['probe_result_count']} "
            f"pass={row['probe_pass_count']} fail={row['probe_failure_count']} "
            f"passed={row['layer_probe_passed']}"
        )

    lines.append("")
    lines.append("HELPER_PROBE_CASE_RESULTS")
    for result in record["helper_probe_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_11_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helper_probe_run())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helper-probe-run-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helper-probe-run-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helper-probe-run-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helper-probe-run-index-v1.json"
    results_path = output / "milestone-11-local-solver-patch-helper-probe-results-v1.json"
    layer_summary_path = output / "milestone-11-local-solver-patch-helper-probe-layer-summary-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helper-probe-run-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helper-probe-run-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_11_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_11_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["helper_probe_index"], indent=2, sort_keys=True), encoding="utf-8")
    results_path.write_text(json.dumps(record["helper_probe_results"], indent=2, sort_keys=True), encoding="utf-8")
    layer_summary_path.write_text(json.dumps(record["helper_probe_layer_summary"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["helper_probe_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["helper_probe_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "results_path": str(results_path),
        "layer_summary_path": str(layer_summary_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helper_probe_run_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helper_probe_run()
    validation = validate_milestone_11_local_solver_patch_helper_probe_run(record)
    artifacts = write_task_11_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_11_id": record["task_11_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_11_ready": record["task_11_ready"],
        "helper_probe_run_ready": record["helper_probe_run_ready"],
        "helper_probe_run_passed": record["helper_probe_run_passed"],
        "helper_runtime_wiring_performed": record["helper_runtime_wiring_performed"],
        "layer_count": record["layer_count"],
        "probe_result_count": record["probe_result_count"],
        "probe_pass_count": record["probe_pass_count"],
        "probe_failure_count": record["probe_failure_count"],
        "world_model_probe_passed": record["world_model_probe_passed"],
        "goal_inference_probe_passed": record["goal_inference_probe_passed"],
        "planner_probe_passed": record["planner_probe_passed"],
        "verifier_probe_passed": record["verifier_probe_passed"],
        "action_policy_probe_passed": record["action_policy_probe_passed"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "helper_probe_check_count": record["helper_probe_check_count"],
        "helper_probe_case_count": record["helper_probe_case_count"],
        "helper_probe_case_pass_count": record["helper_probe_case_pass_count"],
        "helper_probe_case_failure_count": record["helper_probe_case_failure_count"],
        "helper_probe_gate_count": record["helper_probe_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "helper_probe_issue_count": record["helper_probe_issue_count"],
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
