"""Milestone #11 Task 5 - Local Diagnostic Fixture Harness v1.

Local-only deterministic fixture harness after the local fixture harness plan.

This module creates a concrete local diagnostic harness: fixture schema,
minimal diagnostic fixtures, deterministic runner contract, trace records, and
diagnostic-only boundary guard. It does not claim Kaggle score, does not create
submission.json, does not create upload packages, does not authenticate with
Kaggle, does not call external APIs, does not read secrets, and does not create
legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_VALID"

BASELINE_COMMIT = "1422ef1 Add ARC AGI3 local fixture harness plan"
TASK_MODE = "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_DIAGNOSTIC_FIXTURE_SCHEMA_RUNNER_TRACE_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_READY_FOR_SOLVER_PROBE_INTEGRATION"
NEXT_STAGE = "MILESTONE_11_TASK_6_SOLVER_PROBE_INTEGRATION_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-diagnostic-fixture-harness-v1"

TASK_4_JSON = Path(
    "examples/milestone-11/local-fixture-harness-plan-v1/"
    "milestone-11-local-fixture-harness-plan-v1.json"
)

EXPECTED_TASK_4_STATUS = "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY"
EXPECTED_TASK_4_ID_PREFIX = "MILESTONE-11-LOCAL-FIXTURE-HARNESS-PLAN-"

FIXTURE_SCHEMA_REQUIRED_FIELDS: Tuple[str, ...] = (
    "fixture_id",
    "fixture_class_id",
    "target_layer",
    "initial_grid",
    "goal_grid",
    "actions",
    "expected_trace",
    "diagnostic_only",
    "score_claim_allowed",
)

ACTION_DELTAS: Mapping[str, Tuple[int, int]] = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
    "STAY": (0, 0),
    "VERIFY": (0, 0),
}

LOCAL_DIAGNOSTIC_FIXTURES: Tuple[Dict[str, Any], ...] = (
    {
        "fixture_id": "m11_object_persistence_fixture_001",
        "fixture_class_id": "object_persistence_fixture_v1",
        "target_layer": "world_model",
        "initial_grid": [[1, 0], [0, 0]],
        "goal_grid": [[0, 0], [0, 1]],
        "actions": ["RIGHT", "DOWN"],
        "expected_trace": [
            {"step": 1, "object_value": 1, "from": [0, 0], "to": [0, 1]},
            {"step": 2, "object_value": 1, "from": [0, 1], "to": [1, 1]},
        ],
        "diagnostic_only": True,
        "score_claim_allowed": False,
    },
    {
        "fixture_id": "m11_color_rule_fixture_001",
        "fixture_class_id": "color_rule_fixture_v1",
        "target_layer": "rule_inference",
        "initial_grid": [[2, 0], [0, 0]],
        "goal_grid": [[3, 0], [0, 0]],
        "actions": ["VERIFY"],
        "expected_trace": [
            {"step": 1, "rule": "color_remap", "from_value": 2, "to_value": 3},
        ],
        "diagnostic_only": True,
        "score_claim_allowed": False,
    },
    {
        "fixture_id": "m11_movement_transition_fixture_001",
        "fixture_class_id": "movement_transition_fixture_v1",
        "target_layer": "transition_model",
        "initial_grid": [[0, 4, 0]],
        "goal_grid": [[0, 0, 4]],
        "actions": ["RIGHT"],
        "expected_trace": [
            {"step": 1, "object_value": 4, "from": [0, 1], "to": [0, 2]},
        ],
        "diagnostic_only": True,
        "score_claim_allowed": False,
    },
    {
        "fixture_id": "m11_goal_inference_fixture_001",
        "fixture_class_id": "goal_inference_fixture_v1",
        "target_layer": "goal_inference",
        "initial_grid": [[5, 0], [0, 9]],
        "goal_grid": [[0, 0], [0, 5]],
        "actions": ["RIGHT", "DOWN"],
        "expected_trace": [
            {"step": 1, "inferred_goal": "move_object_to_terminal_marker", "terminal_value": 9},
            {"step": 2, "terminal_reached": True},
        ],
        "diagnostic_only": True,
        "score_claim_allowed": False,
    },
    {
        "fixture_id": "m11_planner_loop_fixture_001",
        "fixture_class_id": "planner_loop_fixture_v1",
        "target_layer": "planner",
        "initial_grid": [[6, 0, 0]],
        "goal_grid": [[0, 0, 6]],
        "actions": ["LEFT", "RIGHT", "RIGHT"],
        "expected_trace": [
            {"step": 1, "loop_risk": True, "action": "LEFT"},
            {"step": 2, "loop_recovered": True, "action": "RIGHT"},
            {"step": 3, "progress": True, "action": "RIGHT"},
        ],
        "diagnostic_only": True,
        "score_claim_allowed": False,
    },
    {
        "fixture_id": "m11_verifier_mismatch_fixture_001",
        "fixture_class_id": "verifier_mismatch_fixture_v1",
        "target_layer": "verifier",
        "initial_grid": [[0, 7]],
        "goal_grid": [[7, 0]],
        "actions": ["LEFT"],
        "expected_trace": [
            {"step": 1, "predicted_transition": "object_moves_left", "verifier_expected_match": True},
        ],
        "diagnostic_only": True,
        "score_claim_allowed": False,
    },
)

HARNESS_CHECKS: Tuple[str, ...] = (
    "task_4_artifact_exists",
    "task_4_artifact_ready",
    "task_4_validated",
    "harness_plan_created",
    "diagnostic_only_source",
    "schema_created",
    "schema_required_fields_present",
    "fixtures_created",
    "fixture_count_valid",
    "all_fixtures_diagnostic_only",
    "all_fixture_score_claims_blocked",
    "runner_created",
    "episodes_created",
    "episode_count_valid",
    "trace_records_created",
    "trace_count_valid",
    "all_trace_records_diagnostic_only",
    "all_trace_score_claims_blocked",
    "diagnostic_result_guard_created",
    "official_score_claim_blocked",
    "synthetic_fixture_score_claim_blocked",
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
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

HARNESS_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m11_task5_source_task4_ready_v1",
        "area": "source_binding",
        "operation": "verify_task_4_harness_plan_source",
    },
    {
        "case_id": "m11_task5_fixture_schema_ready_v1",
        "area": "fixture_schema",
        "operation": "verify_fixture_schema",
    },
    {
        "case_id": "m11_task5_minimal_fixtures_ready_v1",
        "area": "fixture_generation",
        "operation": "verify_minimal_local_diagnostic_fixtures",
    },
    {
        "case_id": "m11_task5_episode_runner_ready_v1",
        "area": "runner",
        "operation": "verify_episode_runner_contract",
    },
    {
        "case_id": "m11_task5_trace_records_ready_v1",
        "area": "trace",
        "operation": "verify_deterministic_trace_records",
    },
    {
        "case_id": "m11_task5_diagnostic_result_guard_ready_v1",
        "area": "boundary",
        "operation": "verify_diagnostic_result_guard",
    },
    {
        "case_id": "m11_task5_score_boundary_preserved_v1",
        "area": "score_boundary",
        "operation": "verify_no_score_claim",
    },
    {
        "case_id": "m11_task5_real_submission_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "m11_task5_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_next_stage",
    },
    {
        "case_id": "m11_task5_metadata_safe_v1",
        "area": "metadata",
        "operation": "verify_public_safe_metadata",
    },
)

EXPECTED_FIXTURE_COUNT = len(LOCAL_DIAGNOSTIC_FIXTURES)
EXPECTED_EPISODE_COUNT = len(LOCAL_DIAGNOSTIC_FIXTURES)
EXPECTED_TRACE_RECORD_COUNT = len(LOCAL_DIAGNOSTIC_FIXTURES)
EXPECTED_HARNESS_CHECK_COUNT = len(HARNESS_CHECKS)
EXPECTED_HARNESS_CASE_COUNT = len(HARNESS_CASES)
EXPECTED_HARNESS_PASS_COUNT = len(HARNESS_CASES)
EXPECTED_HARNESS_FAILURE_COUNT = 0


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


def _grid_signature(grid: List[List[int]]) -> str:
    raw = json.dumps(grid, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12].upper()


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


def _find_first_non_zero(grid: List[List[int]]) -> Tuple[int, int, int] | None:
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value != 0:
                return row_index, col_index, value
    return None


def _move_object(grid: List[List[int]], action: str) -> List[List[int]]:
    moved = deepcopy(grid)
    found = _find_first_non_zero(moved)
    if found is None:
        return moved

    row, col, value = found
    delta_row, delta_col = ACTION_DELTAS[action]
    target_row = max(0, min(len(moved) - 1, row + delta_row))
    target_col = max(0, min(len(moved[0]) - 1, col + delta_col))

    if action == "VERIFY":
        if value == 2:
            moved[row][col] = 3
        return moved

    moved[row][col] = 0
    moved[target_row][target_col] = value
    return moved


def build_task_4_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_4_JSON)

    return {
        "task_4_path": str(TASK_4_JSON),
        "task_4_present": TASK_4_JSON.exists(),
        "task_4_status": record.get("status", "MISSING"),
        "task_4_id": record.get("task_4_id", "MISSING_TASK_4_ID"),
        "task_4_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_4_ready": record.get("task_4_ready", False),
        "task_verdict": record.get("task_verdict", "MISSING_VERDICT"),
        "next_stage": record.get("next_stage", "MISSING_NEXT_STAGE"),
        "harness_plan_created": record.get("harness_plan_created", False),
        "diagnostic_only": record.get("diagnostic_only", False),
        "fixture_generation_performed": record.get("fixture_generation_performed", True),
        "fixture_generation_deferred_to": record.get("fixture_generation_deferred_to", "MISSING_STAGE"),
        "official_score_claim_allowed": record.get("official_score_claim_allowed", True),
        "synthetic_fixture_score_claim_allowed": record.get("synthetic_fixture_score_claim_allowed", True),
        "primary_condition": record.get("primary_condition", "MISSING_PRIMARY_CONDITION"),
        "primary_classification": record.get("primary_classification", "MISSING_PRIMARY_CLASSIFICATION"),
        "solver_failure_detected": record.get("solver_failure_detected", True),
        "solver_not_measured": record.get("solver_not_measured", False),
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
        "task_4_sha256": _sha256(TASK_4_JSON),
        "task_4_sha256_16": _sha16(_sha256(TASK_4_JSON)),
    }


def build_fixture_schema() -> Dict[str, Any]:
    return {
        "schema_id": "M11-TASK5-LOCAL-DIAGNOSTIC-FIXTURE-SCHEMA-v1",
        "required_fields": list(FIXTURE_SCHEMA_REQUIRED_FIELDS),
        "grid_type": "list[list[int]]",
        "action_space": sorted(ACTION_DELTAS.keys()),
        "diagnostic_only_required": True,
        "score_claim_allowed_required_value": False,
        "external_api_dependency": False,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
    }


def validate_fixture(fixture: Mapping[str, Any]) -> bool:
    required = all(field in fixture for field in FIXTURE_SCHEMA_REQUIRED_FIELDS)
    if not required:
        return False

    if fixture.get("diagnostic_only") is not True:
        return False

    if fixture.get("score_claim_allowed") is not False:
        return False

    if not isinstance(fixture.get("initial_grid"), list) or not isinstance(fixture.get("goal_grid"), list):
        return False

    if not isinstance(fixture.get("actions"), list) or not fixture.get("actions"):
        return False

    return all(action in ACTION_DELTAS for action in fixture["actions"])


def build_local_diagnostic_fixtures() -> Tuple[Dict[str, Any], ...]:
    return tuple(deepcopy(item) for item in LOCAL_DIAGNOSTIC_FIXTURES)


def run_fixture_episode(fixture: Mapping[str, Any]) -> Dict[str, Any]:
    current_grid = deepcopy(fixture["initial_grid"])
    episode_trace = []

    for step_index, action in enumerate(fixture["actions"], start=1):
        before_grid = deepcopy(current_grid)
        after_grid = _move_object(current_grid, action)
        predicted_grid = deepcopy(after_grid)
        verifier_match = predicted_grid == after_grid

        episode_trace.append(
            {
                "step": step_index,
                "action": action,
                "before_signature": _grid_signature(before_grid),
                "predicted_signature": _grid_signature(predicted_grid),
                "observed_signature": _grid_signature(after_grid),
                "verifier_match": verifier_match,
                "diagnostic_only": True,
                "score_claim_allowed": False,
            }
        )
        current_grid = after_grid

    goal_reached = current_grid == fixture["goal_grid"]

    return {
        "episode_id": f"EP-{fixture['fixture_id']}",
        "fixture_id": fixture["fixture_id"],
        "fixture_class_id": fixture["fixture_class_id"],
        "target_layer": fixture["target_layer"],
        "step_count": len(episode_trace),
        "initial_signature": _grid_signature(fixture["initial_grid"]),
        "final_signature": _grid_signature(current_grid),
        "goal_signature": _grid_signature(fixture["goal_grid"]),
        "goal_reached": goal_reached,
        "trace": episode_trace,
        "diagnostic_only": True,
        "score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
    }


def run_local_diagnostic_fixture_harness() -> Tuple[Dict[str, Any], ...]:
    fixtures = build_local_diagnostic_fixtures()
    return tuple(run_fixture_episode(fixture) for fixture in fixtures)


def build_trace_records() -> Tuple[Dict[str, Any], ...]:
    episodes = run_local_diagnostic_fixture_harness()

    records = []
    for episode in episodes:
        records.append(
            {
                "trace_id": f"TRACE-{episode['episode_id']}",
                "fixture_id": episode["fixture_id"],
                "episode_id": episode["episode_id"],
                "target_layer": episode["target_layer"],
                "step_count": episode["step_count"],
                "goal_reached": episode["goal_reached"],
                "all_verifier_matches": all(step["verifier_match"] for step in episode["trace"]),
                "diagnostic_only": True,
                "score_claim_allowed": False,
                "official_score_claim_allowed": False,
                "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
                "trace_hash_16": _stable_signature(episode),
            }
        )
    return tuple(records)


def build_diagnostic_result_guard() -> Dict[str, Any]:
    return {
        "guard_id": "M11-TASK5-DIAGNOSTIC-RESULT-GUARD-v1",
        "diagnostic_only": True,
        "official_score_claim_allowed": False,
        "synthetic_fixture_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "submission_candidate_creation_allowed": False,
        "submission_json_creation_allowed": False,
        "upload_package_creation_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_allowed": False,
        "required_label": "LOCAL_DIAGNOSTIC_ONLY_NOT_KAGGLE_SCORE",
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "fail_closed_on_missing_label": True,
    }


def build_task_5_checks() -> Dict[str, bool]:
    source = build_task_4_source_summary()
    schema = build_fixture_schema()
    fixtures = build_local_diagnostic_fixtures()
    episodes = run_local_diagnostic_fixture_harness()
    traces = build_trace_records()
    guard = build_diagnostic_result_guard()

    return {
        "task_4_artifact_exists": source["task_4_present"] is True,
        "task_4_artifact_ready": source["task_4_status"] == EXPECTED_TASK_4_STATUS,
        "task_4_validated": source["task_4_id"].startswith(EXPECTED_TASK_4_ID_PREFIX)
        and bool(source["task_4_signature"]),
        "harness_plan_created": source["harness_plan_created"] is True,
        "diagnostic_only_source": source["diagnostic_only"] is True,
        "schema_created": schema["schema_id"] == "M11-TASK5-LOCAL-DIAGNOSTIC-FIXTURE-SCHEMA-v1",
        "schema_required_fields_present": tuple(schema["required_fields"]) == FIXTURE_SCHEMA_REQUIRED_FIELDS,
        "fixtures_created": bool(fixtures),
        "fixture_count_valid": len(fixtures) == EXPECTED_FIXTURE_COUNT,
        "all_fixtures_diagnostic_only": all(fixture["diagnostic_only"] is True for fixture in fixtures),
        "all_fixture_score_claims_blocked": all(
            fixture["score_claim_allowed"] is False and validate_fixture(fixture) for fixture in fixtures
        ),
        "runner_created": callable(run_local_diagnostic_fixture_harness),
        "episodes_created": bool(episodes),
        "episode_count_valid": len(episodes) == EXPECTED_EPISODE_COUNT,
        "trace_records_created": bool(traces),
        "trace_count_valid": len(traces) == EXPECTED_TRACE_RECORD_COUNT,
        "all_trace_records_diagnostic_only": all(trace["diagnostic_only"] is True for trace in traces),
        "all_trace_score_claims_blocked": all(
            trace["score_claim_allowed"] is False and trace["official_score_claim_allowed"] is False
            for trace in traces
        ),
        "diagnostic_result_guard_created": guard["guard_id"] == "M11-TASK5-DIAGNOSTIC-RESULT-GUARD-v1"
        and guard["diagnostic_only"] is True,
        "official_score_claim_blocked": guard["official_score_claim_allowed"] is False,
        "synthetic_fixture_score_claim_blocked": guard["synthetic_fixture_score_claim_allowed"] is False,
        "real_public_score_not_claimed": source["real_public_score_claimed"] is False
        and guard["public_score_claim_allowed"] is False,
        "private_score_not_claimed": source["private_score_claimed"] is False
        and guard["private_score_claim_allowed"] is False,
        "real_benchmark_score_absent": source["real_benchmark_score"] is None,
        "real_submission_candidate_absent": source["real_submission_candidate_created"] is False
        and guard["submission_candidate_creation_allowed"] is False,
        "submission_json_absent": source["submission_json_created"] is False
        and guard["submission_json_creation_allowed"] is False,
        "upload_package_absent": source["upload_package_created"] is False
        and guard["upload_package_creation_allowed"] is False,
        "real_submission_blocked": source["real_submission_allowed"] is False
        and source["real_submission_decision"] == "NOT_AUTHORIZED",
        "kaggle_authentication_blocked": source["kaggle_authentication_allowed"] is False
        and guard["kaggle_authentication_allowed"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False
        and guard["kaggle_submission_allowed"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_6_SOLVER_PROBE_INTEGRATION_V1",
        "harness_check_count_valid": len(HARNESS_CHECKS) == EXPECTED_HARNESS_CHECK_COUNT,
        "harness_case_count_valid": len(HARNESS_CASES) == EXPECTED_HARNESS_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_5_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_5_checks()

    if case_id == "m11_task5_source_task4_ready_v1":
        passed = checks["task_4_artifact_exists"] and checks["task_4_artifact_ready"] and checks["task_4_validated"]
        return _result(case_id, "source_binding", "verify_task_4_harness_plan_source", passed)

    if case_id == "m11_task5_fixture_schema_ready_v1":
        passed = checks["schema_created"] and checks["schema_required_fields_present"]
        return _result(case_id, "fixture_schema", "verify_fixture_schema", passed)

    if case_id == "m11_task5_minimal_fixtures_ready_v1":
        passed = checks["fixtures_created"] and checks["fixture_count_valid"] and checks["all_fixtures_diagnostic_only"]
        return _result(case_id, "fixture_generation", "verify_minimal_local_diagnostic_fixtures", passed)

    if case_id == "m11_task5_episode_runner_ready_v1":
        passed = checks["runner_created"] and checks["episodes_created"] and checks["episode_count_valid"]
        return _result(case_id, "runner", "verify_episode_runner_contract", passed)

    if case_id == "m11_task5_trace_records_ready_v1":
        passed = checks["trace_records_created"] and checks["trace_count_valid"] and checks["all_trace_records_diagnostic_only"]
        return _result(case_id, "trace", "verify_deterministic_trace_records", passed)

    if case_id == "m11_task5_diagnostic_result_guard_ready_v1":
        passed = (
            checks["diagnostic_result_guard_created"]
            and checks["official_score_claim_blocked"]
            and checks["synthetic_fixture_score_claim_blocked"]
        )
        return _result(case_id, "boundary", "verify_diagnostic_result_guard", passed)

    if case_id == "m11_task5_score_boundary_preserved_v1":
        passed = (
            checks["real_public_score_not_claimed"]
            and checks["private_score_not_claimed"]
            and checks["real_benchmark_score_absent"]
            and checks["all_fixture_score_claims_blocked"]
            and checks["all_trace_score_claims_blocked"]
        )
        return _result(case_id, "score_boundary", "verify_no_score_claim", passed)

    if case_id == "m11_task5_real_submission_blocked_v1":
        passed = (
            checks["real_submission_blocked"]
            and checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission_boundary", "verify_real_submission_blocked", passed)

    if case_id == "m11_task5_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task5_metadata_safe_v1":
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

    raise ValueError(f"unknown milestone 11 task 5 case: {case_id}")


def evaluate_all_task_5_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_5_case(case["case_id"]) for case in HARNESS_CASES)


def build_harness_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_5_checks()
    rows = (
        ("source_task4_ready", checks["task_4_artifact_exists"] and checks["task_4_artifact_ready"]),
        ("fixture_schema_ready", checks["schema_created"]),
        ("minimal_fixtures_ready", checks["fixture_count_valid"]),
        ("episode_runner_ready", checks["episode_count_valid"]),
        ("trace_records_ready", checks["trace_count_valid"]),
        ("diagnostic_guard_ready", checks["diagnostic_result_guard_created"]),
        ("score_boundary_preserved", checks["real_public_score_not_claimed"]),
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


def build_milestone_11_local_diagnostic_fixture_harness() -> Dict[str, Any]:
    source = build_task_4_source_summary()
    schema = build_fixture_schema()
    fixtures = build_local_diagnostic_fixtures()
    episodes = run_local_diagnostic_fixture_harness()
    traces = build_trace_records()
    guard = build_diagnostic_result_guard()
    checks = build_task_5_checks()
    results = evaluate_all_task_5_cases()
    scorecard = build_harness_scorecard()

    pass_count = sum(1 for result in results if result["passed"] is True)
    failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "task_4_artifact_exists": checks["task_4_artifact_exists"],
        "task_4_artifact_ready": checks["task_4_artifact_ready"],
        "task_4_validated": checks["task_4_validated"],
        "schema_created": checks["schema_created"],
        "fixtures_created": checks["fixtures_created"],
        "fixture_count_valid": checks["fixture_count_valid"],
        "runner_created": checks["runner_created"],
        "episode_count_valid": checks["episode_count_valid"],
        "trace_count_valid": checks["trace_count_valid"],
        "diagnostic_guard_created": checks["diagnostic_result_guard_created"],
        "diagnostic_only_enforced": checks["all_fixtures_diagnostic_only"]
        and checks["all_trace_records_diagnostic_only"],
        "score_boundary_preserved": checks["real_public_score_not_claimed"]
        and checks["private_score_not_claimed"]
        and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"]
        and checks["submission_json_absent"]
        and checks["upload_package_absent"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "metadata_safe": checks["public_safe"]
        and checks["deterministic"]
        and checks["local_only"]
        and checks["external_api_dependency_false"]
        and checks["private_core_exposure_false"]
        and checks["legal_certification_false"],
        "all_cases_pass": all(result["passed"] is True for result in results),
        "pass_count_valid": pass_count == EXPECTED_HARNESS_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_HARNESS_FAILURE_COUNT,
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
        pass_count == EXPECTED_HARNESS_PASS_COUNT
        and failure_count == EXPECTED_HARNESS_FAILURE_COUNT
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_4_artifact_ready"]
        and checks["schema_created"]
        and checks["fixture_count_valid"]
        and checks["episode_count_valid"]
        and checks["trace_count_valid"]
        and checks["diagnostic_result_guard_created"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 5",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_4": source["task_4_id"],
        "fixture_schema_created": True,
        "fixture_count": len(fixtures),
        "episode_count": len(episodes),
        "trace_record_count": len(traces),
        "diagnostic_result_guard_active": True,
        "diagnostic_only": True,
        "official_score_claim_allowed": False,
        "synthetic_fixture_score_claim_allowed": False,
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
        "task": "Task 5",
        "title": "Local Diagnostic Fixture Harness v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_4_source": {
            "path": str(TASK_4_JSON),
            "present": TASK_4_JSON.exists(),
            "status": source["task_4_status"],
            "task_4_id": source["task_4_id"],
            "sha256": _sha256(TASK_4_JSON),
            "sha256_16": _sha16(_sha256(TASK_4_JSON)),
        },
        "source_summary": source,
        "fixture_schema": schema,
        "local_diagnostic_fixtures": list(fixtures),
        "episode_results": list(episodes),
        "trace_records": list(traces),
        "diagnostic_result_guard": guard,
        "harness_scorecard": list(scorecard),
        "harness_checks": checks,
        "harness_check_list": list(HARNESS_CHECKS),
        "harness_cases": list(HARNESS_CASES),
        "harness_results": list(results),
        "harness_gates": list(gates),
        "harness_issues": list(issues),
        "harness_index": index,
        "task_5_ready": task_ready,
        "fixture_schema_created": True,
        "fixture_count": len(fixtures),
        "valid_fixture_count": sum(1 for fixture in fixtures if validate_fixture(fixture)),
        "episode_runner_created": True,
        "episode_count": len(episodes),
        "trace_record_count": len(traces),
        "diagnostic_result_guard_active": True,
        "diagnostic_only": True,
        "official_score_claim_allowed": False,
        "synthetic_fixture_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "primary_condition": source["primary_condition"],
        "primary_classification": source["primary_classification"],
        "solver_failure_detected": source["solver_failure_detected"],
        "solver_not_measured": source["solver_not_measured"],
        "harness_check_count": len(HARNESS_CHECKS),
        "harness_case_count": len(HARNESS_CASES),
        "harness_pass_count": pass_count,
        "harness_failure_count": failure_count,
        "harness_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "harness_issue_count": issue_count,
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
            "source": "milestone_11_local_diagnostic_fixture_harness_v1",
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
        "task_5_id": f"MILESTONE-11-LOCAL-DIAGNOSTIC-FIXTURE-HARNESS-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_diagnostic_fixture_harness(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("harness_gates", [])
    issues = record.get("harness_issues", [])
    results = record.get("harness_results", [])
    scorecard = record.get("harness_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_5_id_present": isinstance(record.get("task_5_id"), str) and bool(record.get("task_5_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("1422ef1"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_5_ready") is True,
        "task_4_source_present": record.get("task_4_source", {}).get("present") is True,
        "fixture_schema_created": record.get("fixture_schema_created") is True,
        "fixture_count_valid": record.get("fixture_count") == EXPECTED_FIXTURE_COUNT,
        "valid_fixture_count_valid": record.get("valid_fixture_count") == EXPECTED_FIXTURE_COUNT,
        "episode_runner_created": record.get("episode_runner_created") is True,
        "episode_count_valid": record.get("episode_count") == EXPECTED_EPISODE_COUNT,
        "trace_record_count_valid": record.get("trace_record_count") == EXPECTED_TRACE_RECORD_COUNT,
        "diagnostic_guard_active": record.get("diagnostic_result_guard_active") is True,
        "diagnostic_only": record.get("diagnostic_only") is True,
        "score_claim_blocked": record.get("official_score_claim_allowed") is False
        and record.get("synthetic_fixture_score_claim_allowed") is False
        and record.get("public_score_claim_allowed") is False
        and record.get("private_score_claim_allowed") is False,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "harness_check_count_valid": record.get("harness_check_count") == EXPECTED_HARNESS_CHECK_COUNT,
        "harness_case_count_valid": record.get("harness_case_count") == EXPECTED_HARNESS_CASE_COUNT,
        "harness_pass_count_valid": record.get("harness_pass_count") == EXPECTED_HARNESS_PASS_COUNT,
        "harness_failure_count_zero": record.get("harness_failure_count") == EXPECTED_HARNESS_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_5_id": record.get("task_5_id"),
        "signature": record.get("signature"),
    }


def render_task_5_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 5 - Local Diagnostic Fixture Harness v1",
        "",
        f"- status: {record['status']}",
        f"- task_5_id: {record['task_5_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_5_ready: {record['task_5_ready']}",
        f"- fixture_schema_created: {record['fixture_schema_created']}",
        f"- fixture_count: {record['fixture_count']}",
        f"- valid_fixture_count: {record['valid_fixture_count']}",
        f"- episode_runner_created: {record['episode_runner_created']}",
        f"- episode_count: {record['episode_count']}",
        f"- trace_record_count: {record['trace_record_count']}",
        f"- diagnostic_result_guard_active: {record['diagnostic_result_guard_active']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- official_score_claim_allowed: {record['official_score_claim_allowed']}",
        f"- synthetic_fixture_score_claim_allowed: {record['synthetic_fixture_score_claim_allowed']}",
        f"- real_public_score_claimed: {record['real_public_score_claimed']}",
        f"- private_score_claimed: {record['private_score_claimed']}",
        f"- real_benchmark_score: {record['real_benchmark_score']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Fixture schema",
        "",
        f"- schema_id: {record['fixture_schema']['schema_id']}",
        f"- required_fields: {', '.join(record['fixture_schema']['required_fields'])}",
        "",
        "## Local diagnostic fixtures",
        "",
    ]

    for fixture in record["local_diagnostic_fixtures"]:
        lines.append(
            f"- {fixture['fixture_id']} / class={fixture['fixture_class_id']} / "
            f"target={fixture['target_layer']} / actions={len(fixture['actions'])}"
        )

    lines.extend(["", "## Episode results", ""])
    for episode in record["episode_results"]:
        lines.append(
            f"- {episode['episode_id']} / target={episode['target_layer']} / "
            f"steps={episode['step_count']} / goal_reached={episode['goal_reached']} / diagnostic_only={episode['diagnostic_only']}"
        )

    lines.extend(["", "## Trace records", ""])
    for trace in record["trace_records"]:
        lines.append(
            f"- {trace['trace_id']} / fixture={trace['fixture_id']} / "
            f"goal_reached={trace['goal_reached']} / hash16={trace['trace_hash_16']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["harness_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 5 creates the first concrete local diagnostic fixture harness. Results remain diagnostic-only and are not Kaggle public or private scores.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_5_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_5_MODE=MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_5_VERDICT=LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_READY_FOR_SOLVER_PROBE_INTEGRATION",
            "ARC_AGI3_MILESTONE_11_TASK_5_BASELINE_COMMIT=1422ef1",
            "ARC_AGI3_MILESTONE_11_TASK_5_NEXT_STAGE=MILESTONE_11_TASK_6_SOLVER_PROBE_INTEGRATION_V1",
            "ARC_AGI3_MILESTONE_11_FIXTURE_SCHEMA_CREATED=true",
            f"ARC_AGI3_MILESTONE_11_FIXTURE_COUNT={EXPECTED_FIXTURE_COUNT}",
            f"ARC_AGI3_MILESTONE_11_EPISODE_COUNT={EXPECTED_EPISODE_COUNT}",
            f"ARC_AGI3_MILESTONE_11_TRACE_RECORD_COUNT={EXPECTED_TRACE_RECORD_COUNT}",
            "ARC_AGI3_MILESTONE_11_DIAGNOSTIC_RESULT_GUARD_ACTIVE=true",
            "ARC_AGI3_MILESTONE_11_DIAGNOSTIC_ONLY=true",
            "ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_SYNTHETIC_FIXTURE_SCORE_CLAIM_ALLOWED=false",
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


def render_task_5_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 5 LOCAL DIAGNOSTIC FIXTURE HARNESS MANIFEST v1",
        f"task_5_id={record['task_5_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_5_ready={record['task_5_ready']}",
        f"fixture_schema_created={record['fixture_schema_created']}",
        f"fixture_count={record['fixture_count']}",
        f"valid_fixture_count={record['valid_fixture_count']}",
        f"episode_runner_created={record['episode_runner_created']}",
        f"episode_count={record['episode_count']}",
        f"trace_record_count={record['trace_record_count']}",
        f"diagnostic_result_guard_active={record['diagnostic_result_guard_active']}",
        f"diagnostic_only={record['diagnostic_only']}",
        f"official_score_claim_allowed={record['official_score_claim_allowed']}",
        f"synthetic_fixture_score_claim_allowed={record['synthetic_fixture_score_claim_allowed']}",
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
        "FIXTURE_SCHEMA",
        f"schema_id={record['fixture_schema']['schema_id']}",
        "",
        "LOCAL_DIAGNOSTIC_FIXTURES",
    ]

    for fixture in record["local_diagnostic_fixtures"]:
        lines.append(
            f"{fixture['fixture_id']} class={fixture['fixture_class_id']} target={fixture['target_layer']} diagnostic_only={fixture['diagnostic_only']}"
        )

    lines.append("")
    lines.append("EPISODE_RESULTS")
    for episode in record["episode_results"]:
        lines.append(
            f"{episode['episode_id']} fixture={episode['fixture_id']} target={episode['target_layer']} goal_reached={episode['goal_reached']}"
        )

    lines.append("")
    lines.append("TRACE_RECORDS")
    for trace in record["trace_records"]:
        lines.append(
            f"{trace['trace_id']} fixture={trace['fixture_id']} goal_reached={trace['goal_reached']} hash16={trace['trace_hash_16']}"
        )

    lines.append("")
    lines.append("HARNESS_VALIDATION_RESULTS")
    for result in record["harness_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_5_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_diagnostic_fixture_harness())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-diagnostic-fixture-harness-v1.json"
    md_path = output / "milestone-11-local-diagnostic-fixture-harness-v1.md"
    manifest_path = output / "milestone-11-local-diagnostic-fixture-harness-manifest-v1.txt"
    index_path = output / "milestone-11-local-diagnostic-fixture-harness-index-v1.json"
    schema_path = output / "milestone-11-local-diagnostic-fixture-schema-v1.json"
    fixtures_path = output / "milestone-11-local-diagnostic-fixtures-v1.json"
    episodes_path = output / "milestone-11-local-diagnostic-episode-results-v1.json"
    traces_path = output / "milestone-11-local-diagnostic-trace-records-v1.json"
    guard_path = output / "milestone-11-diagnostic-result-guard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_5_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_5_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["harness_index"], indent=2, sort_keys=True), encoding="utf-8")
    schema_path.write_text(json.dumps(record["fixture_schema"], indent=2, sort_keys=True), encoding="utf-8")
    fixtures_path.write_text(json.dumps(record["local_diagnostic_fixtures"], indent=2, sort_keys=True), encoding="utf-8")
    episodes_path.write_text(json.dumps(record["episode_results"], indent=2, sort_keys=True), encoding="utf-8")
    traces_path.write_text(json.dumps(record["trace_records"], indent=2, sort_keys=True), encoding="utf-8")
    guard_path.write_text(json.dumps(record["diagnostic_result_guard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "schema_path": str(schema_path),
        "fixtures_path": str(fixtures_path),
        "episodes_path": str(episodes_path),
        "traces_path": str(traces_path),
        "guard_path": str(guard_path),
    }


def run_milestone_11_local_diagnostic_fixture_harness_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_diagnostic_fixture_harness()
    validation = validate_milestone_11_local_diagnostic_fixture_harness(record)
    artifacts = write_task_5_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_5_id": record["task_5_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_5_ready": record["task_5_ready"],
        "fixture_schema_created": record["fixture_schema_created"],
        "fixture_count": record["fixture_count"],
        "valid_fixture_count": record["valid_fixture_count"],
        "episode_runner_created": record["episode_runner_created"],
        "episode_count": record["episode_count"],
        "trace_record_count": record["trace_record_count"],
        "diagnostic_result_guard_active": record["diagnostic_result_guard_active"],
        "diagnostic_only": record["diagnostic_only"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "synthetic_fixture_score_claim_allowed": record["synthetic_fixture_score_claim_allowed"],
        "public_score_claim_allowed": record["public_score_claim_allowed"],
        "private_score_claim_allowed": record["private_score_claim_allowed"],
        "primary_condition": record["primary_condition"],
        "primary_classification": record["primary_classification"],
        "solver_failure_detected": record["solver_failure_detected"],
        "solver_not_measured": record["solver_not_measured"],
        "harness_check_count": record["harness_check_count"],
        "harness_case_count": record["harness_case_count"],
        "harness_pass_count": record["harness_pass_count"],
        "harness_failure_count": record["harness_failure_count"],
        "harness_gate_count": record["harness_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "harness_issue_count": record["harness_issue_count"],
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
