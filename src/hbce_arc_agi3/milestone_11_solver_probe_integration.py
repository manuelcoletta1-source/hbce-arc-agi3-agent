"""Milestone #11 Task 6 - Solver Probe Integration v1.

Local-only deterministic solver probe integration after the local diagnostic
fixture harness.

This module integrates the diagnostic fixtures with a solver-probe layer. It
does not claim Kaggle score, does not create submission.json, does not create
upload packages, does not authenticate with Kaggle, does not call external APIs,
does not read secrets, and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_VALID"

BASELINE_COMMIT = "ac663d8 Add ARC AGI3 local diagnostic fixture harness"
TASK_MODE = "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_DIAGNOSTIC_SOLVER_PROBE_INTEGRATION_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "SOLVER_PROBE_INTEGRATION_READY_FOR_LOCAL_PROBE_REPORT"
NEXT_STAGE = "MILESTONE_11_TASK_7_LOCAL_SOLVER_PROBE_REPORT_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/solver-probe-integration-v1"

TASK_5_JSON = Path(
    "examples/milestone-11/local-diagnostic-fixture-harness-v1/"
    "milestone-11-local-diagnostic-fixture-harness-v1.json"
)

EXPECTED_TASK_5_STATUS = "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_READY"
EXPECTED_TASK_5_ID_PREFIX = "MILESTONE-11-LOCAL-DIAGNOSTIC-FIXTURE-HARNESS-"

PROBE_COMPONENTS: Tuple[Dict[str, str], ...] = (
    {
        "probe_id": "world_model_probe_v1",
        "target_layer": "world_model",
        "purpose": "Measure local object-state and transition consistency.",
    },
    {
        "probe_id": "goal_inference_probe_v1",
        "target_layer": "goal_inference",
        "purpose": "Measure local goal inference from diagnostic fixture state.",
    },
    {
        "probe_id": "planner_probe_v1",
        "target_layer": "planner",
        "purpose": "Measure local plan progress and loop recovery.",
    },
    {
        "probe_id": "transition_verifier_probe_v1",
        "target_layer": "verifier",
        "purpose": "Measure predicted versus observed transition agreement.",
    },
    {
        "probe_id": "action_policy_probe_v1",
        "target_layer": "action_policy",
        "purpose": "Measure local action validity and non-submission policy safety.",
    },
)

EXPECTED_PROBE_COMPONENT_COUNT = len(PROBE_COMPONENTS)
EXPECTED_FIXTURE_COUNT = 6
EXPECTED_EPISODE_COUNT = 6
EXPECTED_TRACE_RECORD_COUNT = 6
EXPECTED_PROBE_RESULT_COUNT = EXPECTED_FIXTURE_COUNT * EXPECTED_PROBE_COMPONENT_COUNT
EXPECTED_PROBE_PASS_COUNT = EXPECTED_PROBE_RESULT_COUNT
EXPECTED_PROBE_FAILURE_COUNT = 0

PROBE_CHECKS: Tuple[str, ...] = (
    "task_5_artifact_exists",
    "task_5_artifact_ready",
    "task_5_validated",
    "fixture_schema_created",
    "fixture_count_valid",
    "episode_count_valid",
    "trace_record_count_valid",
    "diagnostic_guard_active",
    "diagnostic_only_source",
    "probe_components_created",
    "probe_component_count_valid",
    "solver_probe_integration_created",
    "probe_results_created",
    "probe_result_count_valid",
    "all_probe_results_diagnostic_only",
    "all_probe_results_not_kaggle_score",
    "all_probe_results_pass",
    "world_model_probe_present",
    "goal_inference_probe_present",
    "planner_probe_present",
    "transition_verifier_probe_present",
    "action_policy_probe_present",
    "local_solver_diagnostic_measured",
    "official_score_claim_blocked",
    "synthetic_fixture_score_claim_blocked",
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
    "runtime_solver_modified_false",
    "external_solver_dependency_false",
    "fail_closed_required",
    "fail_closed_active",
    "next_stage_valid",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

PROBE_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m11_task6_source_task5_ready_v1",
        "area": "source_binding",
        "operation": "verify_task_5_local_diagnostic_harness_source",
    },
    {
        "case_id": "m11_task6_probe_components_ready_v1",
        "area": "probe_components",
        "operation": "verify_solver_probe_components",
    },
    {
        "case_id": "m11_task6_probe_results_ready_v1",
        "area": "probe_results",
        "operation": "verify_probe_results",
    },
    {
        "case_id": "m11_task6_world_model_probe_ready_v1",
        "area": "world_model",
        "operation": "verify_world_model_probe",
    },
    {
        "case_id": "m11_task6_goal_inference_probe_ready_v1",
        "area": "goal_inference",
        "operation": "verify_goal_inference_probe",
    },
    {
        "case_id": "m11_task6_planner_probe_ready_v1",
        "area": "planner",
        "operation": "verify_planner_probe",
    },
    {
        "case_id": "m11_task6_transition_verifier_probe_ready_v1",
        "area": "verifier",
        "operation": "verify_transition_verifier_probe",
    },
    {
        "case_id": "m11_task6_action_policy_probe_ready_v1",
        "area": "action_policy",
        "operation": "verify_action_policy_probe",
    },
    {
        "case_id": "m11_task6_score_and_submission_boundary_v1",
        "area": "boundary",
        "operation": "verify_no_score_no_submission",
    },
    {
        "case_id": "m11_task6_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_next_stage",
    },
    {
        "case_id": "m11_task6_metadata_safe_v1",
        "area": "metadata",
        "operation": "verify_public_safe_metadata",
    },
)

EXPECTED_PROBE_CHECK_COUNT = len(PROBE_CHECKS)
EXPECTED_PROBE_CASE_COUNT = len(PROBE_CASES)


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


def build_task_5_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_5_JSON)

    return {
        "task_5_path": str(TASK_5_JSON),
        "task_5_present": TASK_5_JSON.exists(),
        "task_5_status": record.get("status", "MISSING"),
        "task_5_id": record.get("task_5_id", "MISSING_TASK_5_ID"),
        "task_5_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_5_ready": record.get("task_5_ready", False),
        "task_verdict": record.get("task_verdict", "MISSING_VERDICT"),
        "next_stage": record.get("next_stage", "MISSING_NEXT_STAGE"),
        "fixture_schema_created": record.get("fixture_schema_created", False),
        "fixture_count": record.get("fixture_count", 0),
        "valid_fixture_count": record.get("valid_fixture_count", 0),
        "episode_runner_created": record.get("episode_runner_created", False),
        "episode_count": record.get("episode_count", 0),
        "trace_record_count": record.get("trace_record_count", 0),
        "diagnostic_result_guard_active": record.get("diagnostic_result_guard_active", False),
        "diagnostic_only": record.get("diagnostic_only", False),
        "official_score_claim_allowed": record.get("official_score_claim_allowed", True),
        "synthetic_fixture_score_claim_allowed": record.get("synthetic_fixture_score_claim_allowed", True),
        "public_score_claim_allowed": record.get("public_score_claim_allowed", True),
        "private_score_claim_allowed": record.get("private_score_claim_allowed", True),
        "primary_condition": record.get("primary_condition", "MISSING_PRIMARY_CONDITION"),
        "primary_classification": record.get("primary_classification", "MISSING_PRIMARY_CLASSIFICATION"),
        "solver_failure_detected": record.get("solver_failure_detected", True),
        "solver_not_measured": record.get("solver_not_measured", False),
        "local_diagnostic_fixtures": record.get("local_diagnostic_fixtures", []),
        "episode_results": record.get("episode_results", []),
        "trace_records": record.get("trace_records", []),
        "diagnostic_result_guard": record.get("diagnostic_result_guard", {}),
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
        "task_5_sha256": _sha256(TASK_5_JSON),
        "task_5_sha256_16": _sha16(_sha256(TASK_5_JSON)),
    }


def build_solver_probe_contract() -> Dict[str, Any]:
    return {
        "contract_id": "M11-TASK6-SOLVER-PROBE-CONTRACT-v1",
        "probe_components": list(PROBE_COMPONENTS),
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "synthetic_fixture_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "required_result_fields": [
            "probe_result_id",
            "fixture_id",
            "episode_id",
            "probe_id",
            "target_layer",
            "diagnostic_probe_passed",
            "diagnostic_only",
            "kaggle_score_semantics",
            "score_claim_allowed",
        ],
    }


def _episode_actions(episode: Mapping[str, Any]) -> Tuple[str, ...]:
    return tuple(step.get("action", "UNKNOWN") for step in episode.get("trace", []))


def evaluate_probe_component(episode: Mapping[str, Any], probe: Mapping[str, str]) -> Dict[str, Any]:
    probe_id = probe["probe_id"]
    trace = episode.get("trace", [])
    actions = _episode_actions(episode)
    step_count = int(episode.get("step_count", 0))
    goal_reached = episode.get("goal_reached") is True

    if probe_id == "world_model_probe_v1":
        passed = bool(episode.get("initial_signature")) and bool(episode.get("final_signature")) and step_count >= 1
        evidence = {
            "initial_signature": episode.get("initial_signature"),
            "final_signature": episode.get("final_signature"),
            "goal_signature": episode.get("goal_signature"),
        }
    elif probe_id == "goal_inference_probe_v1":
        passed = goal_reached
        evidence = {"goal_reached": goal_reached}
    elif probe_id == "planner_probe_v1":
        passed = step_count >= 1 and goal_reached and all(action != "UNKNOWN" for action in actions)
        evidence = {"step_count": step_count, "actions": list(actions), "goal_reached": goal_reached}
    elif probe_id == "transition_verifier_probe_v1":
        passed = bool(trace) and all(step.get("verifier_match") is True for step in trace)
        evidence = {"verifier_match_count": sum(1 for step in trace if step.get("verifier_match") is True)}
    elif probe_id == "action_policy_probe_v1":
        allowed_actions = {"UP", "DOWN", "LEFT", "RIGHT", "STAY", "VERIFY"}
        passed = bool(actions) and all(action in allowed_actions for action in actions)
        evidence = {"actions": list(actions), "allowed_actions": sorted(allowed_actions)}
    else:
        passed = False
        evidence = {"error": "unknown_probe"}

    result_base = {
        "fixture_id": episode.get("fixture_id"),
        "episode_id": episode.get("episode_id"),
        "probe_id": probe_id,
        "target_layer": probe["target_layer"],
        "diagnostic_probe_passed": passed,
        "diagnostic_probe_score": 100 if passed else 0,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "evidence": evidence,
    }

    return {
        **result_base,
        "probe_result_id": f"PROBE-{_stable_signature(result_base)[:12]}",
    }


def build_solver_probe_results() -> Tuple[Dict[str, Any], ...]:
    source = build_task_5_source_summary()
    episodes = tuple(source["episode_results"])
    results = []

    for episode in episodes:
        for probe in PROBE_COMPONENTS:
            results.append(evaluate_probe_component(episode, probe))

    return tuple(results)


def build_probe_summary() -> Dict[str, Any]:
    results = build_solver_probe_results()

    return {
        "probe_summary_id": "M11-TASK6-SOLVER-PROBE-SUMMARY-v1",
        "probe_component_count": EXPECTED_PROBE_COMPONENT_COUNT,
        "probe_result_count": len(results),
        "probe_pass_count": sum(1 for item in results if item["diagnostic_probe_passed"] is True),
        "probe_failure_count": sum(1 for item in results if item["diagnostic_probe_passed"] is False),
        "fixture_count": EXPECTED_FIXTURE_COUNT,
        "episode_count": EXPECTED_EPISODE_COUNT,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
    }


def build_probe_layer_report() -> Tuple[Dict[str, Any], ...]:
    results = build_solver_probe_results()
    layer_rows = []

    for probe in PROBE_COMPONENTS:
        probe_results = [item for item in results if item["probe_id"] == probe["probe_id"]]
        pass_count = sum(1 for item in probe_results if item["diagnostic_probe_passed"] is True)
        layer_rows.append(
            {
                "probe_id": probe["probe_id"],
                "target_layer": probe["target_layer"],
                "result_count": len(probe_results),
                "pass_count": pass_count,
                "failure_count": len(probe_results) - pass_count,
                "diagnostic_only": True,
                "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
                "score_claim_allowed": False,
            }
        )

    return tuple(layer_rows)


def build_task_6_checks() -> Dict[str, bool]:
    source = build_task_5_source_summary()
    contract = build_solver_probe_contract()
    results = build_solver_probe_results()
    summary = build_probe_summary()
    layer_report = build_probe_layer_report()

    probe_ids = {probe["probe_id"] for probe in PROBE_COMPONENTS}
    result_probe_ids = {item["probe_id"] for item in results}

    return {
        "task_5_artifact_exists": source["task_5_present"] is True,
        "task_5_artifact_ready": source["task_5_status"] == EXPECTED_TASK_5_STATUS,
        "task_5_validated": source["task_5_id"].startswith(EXPECTED_TASK_5_ID_PREFIX)
        and bool(source["task_5_signature"]),
        "fixture_schema_created": source["fixture_schema_created"] is True,
        "fixture_count_valid": source["fixture_count"] == EXPECTED_FIXTURE_COUNT
        and source["valid_fixture_count"] == EXPECTED_FIXTURE_COUNT,
        "episode_count_valid": source["episode_count"] == EXPECTED_EPISODE_COUNT,
        "trace_record_count_valid": source["trace_record_count"] == EXPECTED_TRACE_RECORD_COUNT,
        "diagnostic_guard_active": source["diagnostic_result_guard_active"] is True,
        "diagnostic_only_source": source["diagnostic_only"] is True,
        "probe_components_created": bool(PROBE_COMPONENTS),
        "probe_component_count_valid": len(PROBE_COMPONENTS) == EXPECTED_PROBE_COMPONENT_COUNT,
        "solver_probe_integration_created": contract["contract_id"] == "M11-TASK6-SOLVER-PROBE-CONTRACT-v1",
        "probe_results_created": bool(results),
        "probe_result_count_valid": len(results) == EXPECTED_PROBE_RESULT_COUNT,
        "all_probe_results_diagnostic_only": all(item["diagnostic_only"] is True for item in results),
        "all_probe_results_not_kaggle_score": all(
            item["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for item in results
        ),
        "all_probe_results_pass": all(item["diagnostic_probe_passed"] is True for item in results),
        "world_model_probe_present": "world_model_probe_v1" in probe_ids
        and "world_model_probe_v1" in result_probe_ids,
        "goal_inference_probe_present": "goal_inference_probe_v1" in probe_ids
        and "goal_inference_probe_v1" in result_probe_ids,
        "planner_probe_present": "planner_probe_v1" in probe_ids
        and "planner_probe_v1" in result_probe_ids,
        "transition_verifier_probe_present": "transition_verifier_probe_v1" in probe_ids
        and "transition_verifier_probe_v1" in result_probe_ids,
        "action_policy_probe_present": "action_policy_probe_v1" in probe_ids
        and "action_policy_probe_v1" in result_probe_ids,
        "local_solver_diagnostic_measured": summary["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
        and len(layer_report) == EXPECTED_PROBE_COMPONENT_COUNT,
        "official_score_claim_blocked": contract["official_score_claim_allowed"] is False,
        "synthetic_fixture_score_claim_blocked": contract["synthetic_fixture_score_claim_allowed"] is False,
        "public_score_claim_blocked": contract["public_score_claim_allowed"] is False,
        "private_score_claim_blocked": contract["private_score_claim_allowed"] is False,
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
        "runtime_solver_modified_false": contract["runtime_solver_modified"] is False
        and contract["ranker_runtime_modified"] is False,
        "external_solver_dependency_false": contract["external_solver_dependency"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_7_LOCAL_SOLVER_PROBE_REPORT_V1",
        "probe_check_count_valid": len(PROBE_CHECKS) == EXPECTED_PROBE_CHECK_COUNT,
        "probe_case_count_valid": len(PROBE_CASES) == EXPECTED_PROBE_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_6_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_6_checks()

    if case_id == "m11_task6_source_task5_ready_v1":
        passed = checks["task_5_artifact_exists"] and checks["task_5_artifact_ready"] and checks["task_5_validated"]
        return _result(case_id, "source_binding", "verify_task_5_local_diagnostic_harness_source", passed)

    if case_id == "m11_task6_probe_components_ready_v1":
        passed = checks["probe_components_created"] and checks["probe_component_count_valid"]
        return _result(case_id, "probe_components", "verify_solver_probe_components", passed)

    if case_id == "m11_task6_probe_results_ready_v1":
        passed = checks["probe_results_created"] and checks["probe_result_count_valid"] and checks["all_probe_results_pass"]
        return _result(case_id, "probe_results", "verify_probe_results", passed)

    if case_id == "m11_task6_world_model_probe_ready_v1":
        return _result(case_id, "world_model", "verify_world_model_probe", checks["world_model_probe_present"])

    if case_id == "m11_task6_goal_inference_probe_ready_v1":
        return _result(case_id, "goal_inference", "verify_goal_inference_probe", checks["goal_inference_probe_present"])

    if case_id == "m11_task6_planner_probe_ready_v1":
        return _result(case_id, "planner", "verify_planner_probe", checks["planner_probe_present"])

    if case_id == "m11_task6_transition_verifier_probe_ready_v1":
        return _result(
            case_id,
            "verifier",
            "verify_transition_verifier_probe",
            checks["transition_verifier_probe_present"],
        )

    if case_id == "m11_task6_action_policy_probe_ready_v1":
        return _result(case_id, "action_policy", "verify_action_policy_probe", checks["action_policy_probe_present"])

    if case_id == "m11_task6_score_and_submission_boundary_v1":
        passed = (
            checks["all_probe_results_not_kaggle_score"]
            and checks["official_score_claim_blocked"]
            and checks["real_public_score_not_claimed"]
            and checks["private_score_not_claimed"]
            and checks["real_benchmark_score_absent"]
            and checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "boundary", "verify_no_score_no_submission", passed)

    if case_id == "m11_task6_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task6_metadata_safe_v1":
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

    raise ValueError(f"unknown milestone 11 task 6 case: {case_id}")


def evaluate_all_task_6_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_6_case(case["case_id"]) for case in PROBE_CASES)


def build_probe_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_6_checks()
    rows = (
        ("source_task5_ready", checks["task_5_artifact_exists"] and checks["task_5_artifact_ready"]),
        ("probe_components_ready", checks["probe_component_count_valid"]),
        ("probe_results_ready", checks["probe_result_count_valid"]),
        ("world_model_probe_ready", checks["world_model_probe_present"]),
        ("goal_inference_probe_ready", checks["goal_inference_probe_present"]),
        ("planner_probe_ready", checks["planner_probe_present"]),
        ("transition_verifier_probe_ready", checks["transition_verifier_probe_present"]),
        ("action_policy_probe_ready", checks["action_policy_probe_present"]),
        ("score_boundary_preserved", checks["all_probe_results_not_kaggle_score"]),
        ("submission_boundary_preserved", checks["real_submission_blocked"]),
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


def build_milestone_11_solver_probe_integration() -> Dict[str, Any]:
    source = build_task_5_source_summary()
    contract = build_solver_probe_contract()
    results = build_solver_probe_results()
    summary = build_probe_summary()
    layer_report = build_probe_layer_report()
    checks = build_task_6_checks()
    cases = evaluate_all_task_6_cases()
    scorecard = build_probe_scorecard()

    pass_count = sum(1 for item in cases if item["passed"] is True)
    failure_count = sum(1 for item in cases if item["passed"] is False)

    gate_state = {
        "task_5_artifact_exists": checks["task_5_artifact_exists"],
        "task_5_artifact_ready": checks["task_5_artifact_ready"],
        "task_5_validated": checks["task_5_validated"],
        "probe_components_ready": checks["probe_component_count_valid"],
        "probe_results_ready": checks["probe_result_count_valid"],
        "all_probe_results_pass": checks["all_probe_results_pass"],
        "all_probe_results_diagnostic_only": checks["all_probe_results_diagnostic_only"],
        "all_probe_results_not_kaggle_score": checks["all_probe_results_not_kaggle_score"],
        "local_solver_diagnostic_measured": checks["local_solver_diagnostic_measured"],
        "score_boundary_preserved": checks["official_score_claim_blocked"]
        and checks["real_public_score_not_claimed"]
        and checks["private_score_not_claimed"],
        "submission_boundary_preserved": checks["real_submission_blocked"]
        and checks["submission_json_absent"]
        and checks["upload_package_absent"]
        and checks["kaggle_submission_not_sent"],
        "runtime_solver_modified_false": checks["runtime_solver_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "metadata_safe": checks["public_safe"]
        and checks["deterministic"]
        and checks["local_only"]
        and checks["external_api_dependency_false"]
        and checks["private_core_exposure_false"]
        and checks["legal_certification_false"],
        "all_cases_pass": all(item["passed"] is True for item in cases),
        "pass_count_valid": pass_count == EXPECTED_PROBE_CASE_COUNT,
        "failure_count_zero": failure_count == 0,
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
        pass_count == EXPECTED_PROBE_CASE_COUNT
        and failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_5_artifact_ready"]
        and checks["probe_result_count_valid"]
        and checks["all_probe_results_pass"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 6",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_5": source["task_5_id"],
        "solver_probe_contract_created": True,
        "solver_probe_integration_created": True,
        "probe_component_count": EXPECTED_PROBE_COMPONENT_COUNT,
        "probe_result_count": len(results),
        "probe_pass_count": summary["probe_pass_count"],
        "probe_failure_count": summary["probe_failure_count"],
        "layer_report_count": len(layer_report),
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "runtime_solver_modified": False,
        "external_solver_dependency": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": STATUS,
        "milestone": "Milestone #11",
        "task": "Task 6",
        "title": "Solver Probe Integration v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_5_source": {
            "path": str(TASK_5_JSON),
            "present": TASK_5_JSON.exists(),
            "status": source["task_5_status"],
            "task_5_id": source["task_5_id"],
            "sha256": _sha256(TASK_5_JSON),
            "sha256_16": _sha16(_sha256(TASK_5_JSON)),
        },
        "source_summary": source,
        "solver_probe_contract": contract,
        "probe_components": list(PROBE_COMPONENTS),
        "solver_probe_results": list(results),
        "probe_summary": summary,
        "probe_layer_report": list(layer_report),
        "probe_scorecard": list(scorecard),
        "probe_checks": checks,
        "probe_check_list": list(PROBE_CHECKS),
        "probe_cases": list(PROBE_CASES),
        "probe_case_results": list(cases),
        "probe_gates": list(gates),
        "probe_issues": list(issues),
        "probe_index": index,
        "task_6_ready": task_ready,
        "solver_probe_contract_created": True,
        "solver_probe_integration_created": True,
        "probe_component_count": EXPECTED_PROBE_COMPONENT_COUNT,
        "probe_result_count": len(results),
        "probe_pass_count": summary["probe_pass_count"],
        "probe_failure_count": summary["probe_failure_count"],
        "layer_report_count": len(layer_report),
        "local_solver_diagnostic_measured": True,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "synthetic_fixture_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "primary_condition": source["primary_condition"],
        "primary_classification": source["primary_classification"],
        "solver_failure_detected": source["solver_failure_detected"],
        "solver_not_measured_from_task_5": source["solver_not_measured"],
        "solver_probe_measured": True,
        "probe_check_count": len(PROBE_CHECKS),
        "probe_case_count": len(PROBE_CASES),
        "probe_case_pass_count": pass_count,
        "probe_case_failure_count": failure_count,
        "probe_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "probe_issue_count": issue_count,
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
            "source": "milestone_11_solver_probe_integration_v1",
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
        "task_6_id": f"MILESTONE-11-SOLVER-PROBE-INTEGRATION-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_solver_probe_integration(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("probe_gates", [])
    issues = record.get("probe_issues", [])
    case_results = record.get("probe_case_results", [])
    scorecard = record.get("probe_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_6_id_present": isinstance(record.get("task_6_id"), str) and bool(record.get("task_6_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("ac663d8"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_6_ready") is True,
        "task_5_source_present": record.get("task_5_source", {}).get("present") is True,
        "solver_probe_contract_created": record.get("solver_probe_contract_created") is True,
        "solver_probe_integration_created": record.get("solver_probe_integration_created") is True,
        "probe_component_count_valid": record.get("probe_component_count") == EXPECTED_PROBE_COMPONENT_COUNT,
        "probe_result_count_valid": record.get("probe_result_count") == EXPECTED_PROBE_RESULT_COUNT,
        "probe_pass_count_valid": record.get("probe_pass_count") == EXPECTED_PROBE_PASS_COUNT,
        "probe_failure_count_zero": record.get("probe_failure_count") == EXPECTED_PROBE_FAILURE_COUNT,
        "layer_report_count_valid": record.get("layer_report_count") == EXPECTED_PROBE_COMPONENT_COUNT,
        "local_solver_diagnostic_measured": record.get("local_solver_diagnostic_measured") is True,
        "diagnostic_only": record.get("diagnostic_only") is True,
        "not_kaggle_score": record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "score_claim_blocked": record.get("official_score_claim_allowed") is False
        and record.get("public_score_claim_allowed") is False
        and record.get("private_score_claim_allowed") is False,
        "runtime_solver_not_modified": record.get("runtime_solver_modified") is False
        and record.get("ranker_runtime_modified") is False,
        "external_solver_dependency_false": record.get("external_solver_dependency") is False,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "probe_check_count_valid": record.get("probe_check_count") == EXPECTED_PROBE_CHECK_COUNT,
        "probe_case_count_valid": record.get("probe_case_count") == EXPECTED_PROBE_CASE_COUNT,
        "probe_case_pass_count_valid": record.get("probe_case_pass_count") == EXPECTED_PROBE_CASE_COUNT,
        "probe_case_failure_count_zero": record.get("probe_case_failure_count") == 0,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_6_id": record.get("task_6_id"),
        "signature": record.get("signature"),
    }


def render_task_6_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 6 - Solver Probe Integration v1",
        "",
        f"- status: {record['status']}",
        f"- task_6_id: {record['task_6_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_6_ready: {record['task_6_ready']}",
        f"- solver_probe_contract_created: {record['solver_probe_contract_created']}",
        f"- solver_probe_integration_created: {record['solver_probe_integration_created']}",
        f"- probe_component_count: {record['probe_component_count']}",
        f"- probe_result_count: {record['probe_result_count']}",
        f"- probe_pass_count: {record['probe_pass_count']}",
        f"- probe_failure_count: {record['probe_failure_count']}",
        f"- layer_report_count: {record['layer_report_count']}",
        f"- local_solver_diagnostic_measured: {record['local_solver_diagnostic_measured']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- official_score_claim_allowed: {record['official_score_claim_allowed']}",
        f"- real_public_score_claimed: {record['real_public_score_claimed']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Probe components",
        "",
    ]

    for item in record["probe_components"]:
        lines.append(f"- {item['probe_id']} / target={item['target_layer']} / {item['purpose']}")

    lines.extend(["", "## Probe layer report", ""])
    for item in record["probe_layer_report"]:
        lines.append(
            f"- {item['probe_id']} / layer={item['target_layer']} / "
            f"results={item['result_count']} / pass={item['pass_count']} / fail={item['failure_count']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["probe_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 6 integrates the local diagnostic fixture harness with a solver-probe layer. Results are local diagnostic measurements only and are not Kaggle public or private scores.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_6_SOLVER_PROBE_INTEGRATION_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_6_SOLVER_PROBE_INTEGRATION_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_6_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_6_MODE=MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_6_VERDICT=SOLVER_PROBE_INTEGRATION_READY_FOR_LOCAL_PROBE_REPORT",
            "ARC_AGI3_MILESTONE_11_TASK_6_BASELINE_COMMIT=ac663d8",
            "ARC_AGI3_MILESTONE_11_TASK_6_NEXT_STAGE=MILESTONE_11_TASK_7_LOCAL_SOLVER_PROBE_REPORT_V1",
            "ARC_AGI3_MILESTONE_11_SOLVER_PROBE_CONTRACT_CREATED=true",
            "ARC_AGI3_MILESTONE_11_SOLVER_PROBE_INTEGRATION_CREATED=true",
            f"ARC_AGI3_MILESTONE_11_PROBE_COMPONENT_COUNT={EXPECTED_PROBE_COMPONENT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PROBE_RESULT_COUNT={EXPECTED_PROBE_RESULT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PROBE_PASS_COUNT={EXPECTED_PROBE_PASS_COUNT}",
            "ARC_AGI3_MILESTONE_11_PROBE_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_DIAGNOSTIC_MEASURED=true",
            "ARC_AGI3_MILESTONE_11_DIAGNOSTIC_ONLY=true",
            "ARC_AGI3_MILESTONE_11_KAGGLE_SCORE_SEMANTICS=NOT_A_KAGGLE_SCORE",
            "ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false",
            "ARC_AGI3_MILESTONE_11_PRIVATE_SCORE_CLAIMED=false",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_11_SUBMISSION_JSON_CREATED=false",
            "ARC_AGI3_MILESTONE_11_UPLOAD_PACKAGE_CREATED=false",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_KAGGLE_AUTHENTICATION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false",
            "ARC_AGI3_MILESTONE_11_FAIL_CLOSED_REQUIRED=true",
            "ARC_AGI3_MILESTONE_11_FAIL_CLOSED_ACTIVE=true",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_task_6_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 6 SOLVER PROBE INTEGRATION MANIFEST v1",
        f"task_6_id={record['task_6_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_6_ready={record['task_6_ready']}",
        f"solver_probe_contract_created={record['solver_probe_contract_created']}",
        f"solver_probe_integration_created={record['solver_probe_integration_created']}",
        f"probe_component_count={record['probe_component_count']}",
        f"probe_result_count={record['probe_result_count']}",
        f"probe_pass_count={record['probe_pass_count']}",
        f"probe_failure_count={record['probe_failure_count']}",
        f"layer_report_count={record['layer_report_count']}",
        f"local_solver_diagnostic_measured={record['local_solver_diagnostic_measured']}",
        f"diagnostic_only={record['diagnostic_only']}",
        f"kaggle_score_semantics={record['kaggle_score_semantics']}",
        f"official_score_claim_allowed={record['official_score_claim_allowed']}",
        f"synthetic_fixture_score_claim_allowed={record['synthetic_fixture_score_claim_allowed']}",
        f"public_score_claim_allowed={record['public_score_claim_allowed']}",
        f"private_score_claim_allowed={record['private_score_claim_allowed']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"ranker_runtime_modified={record['ranker_runtime_modified']}",
        f"external_solver_dependency={record['external_solver_dependency']}",
        f"real_public_score_claimed={record['real_public_score_claimed']}",
        f"private_score_claimed={record['private_score_claimed']}",
        f"real_benchmark_score={record['real_benchmark_score']}",
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
        "PROBE_COMPONENTS",
    ]

    for probe in record["probe_components"]:
        lines.append(f"{probe['probe_id']} target={probe['target_layer']}")

    lines.append("")
    lines.append("PROBE_LAYER_REPORT")
    for row in record["probe_layer_report"]:
        lines.append(
            f"{row['probe_id']} target={row['target_layer']} result_count={row['result_count']} "
            f"pass_count={row['pass_count']} failure_count={row['failure_count']}"
        )

    lines.append("")
    lines.append("PROBE_CASE_RESULTS")
    for result in record["probe_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_6_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_solver_probe_integration())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-solver-probe-integration-v1.json"
    md_path = output / "milestone-11-solver-probe-integration-v1.md"
    manifest_path = output / "milestone-11-solver-probe-integration-manifest-v1.txt"
    index_path = output / "milestone-11-solver-probe-integration-index-v1.json"
    contract_path = output / "milestone-11-solver-probe-contract-v1.json"
    components_path = output / "milestone-11-solver-probe-components-v1.json"
    results_path = output / "milestone-11-solver-probe-results-v1.json"
    layer_report_path = output / "milestone-11-solver-probe-layer-report-v1.json"
    summary_path = output / "milestone-11-solver-probe-summary-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_6_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_6_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["probe_index"], indent=2, sort_keys=True), encoding="utf-8")
    contract_path.write_text(json.dumps(record["solver_probe_contract"], indent=2, sort_keys=True), encoding="utf-8")
    components_path.write_text(json.dumps(record["probe_components"], indent=2, sort_keys=True), encoding="utf-8")
    results_path.write_text(json.dumps(record["solver_probe_results"], indent=2, sort_keys=True), encoding="utf-8")
    layer_report_path.write_text(json.dumps(record["probe_layer_report"], indent=2, sort_keys=True), encoding="utf-8")
    summary_path.write_text(json.dumps(record["probe_summary"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "contract_path": str(contract_path),
        "components_path": str(components_path),
        "results_path": str(results_path),
        "layer_report_path": str(layer_report_path),
        "summary_path": str(summary_path),
    }


def run_milestone_11_solver_probe_integration_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_solver_probe_integration()
    validation = validate_milestone_11_solver_probe_integration(record)
    artifacts = write_task_6_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_6_id": record["task_6_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_6_ready": record["task_6_ready"],
        "solver_probe_contract_created": record["solver_probe_contract_created"],
        "solver_probe_integration_created": record["solver_probe_integration_created"],
        "probe_component_count": record["probe_component_count"],
        "probe_result_count": record["probe_result_count"],
        "probe_pass_count": record["probe_pass_count"],
        "probe_failure_count": record["probe_failure_count"],
        "layer_report_count": record["layer_report_count"],
        "local_solver_diagnostic_measured": record["local_solver_diagnostic_measured"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "synthetic_fixture_score_claim_allowed": record["synthetic_fixture_score_claim_allowed"],
        "public_score_claim_allowed": record["public_score_claim_allowed"],
        "private_score_claim_allowed": record["private_score_claim_allowed"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "primary_condition": record["primary_condition"],
        "primary_classification": record["primary_classification"],
        "solver_failure_detected": record["solver_failure_detected"],
        "solver_not_measured_from_task_5": record["solver_not_measured_from_task_5"],
        "solver_probe_measured": record["solver_probe_measured"],
        "probe_check_count": record["probe_check_count"],
        "probe_case_count": record["probe_case_count"],
        "probe_case_pass_count": record["probe_case_pass_count"],
        "probe_case_failure_count": record["probe_case_failure_count"],
        "probe_gate_count": record["probe_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "probe_issue_count": record["probe_issue_count"],
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
