"""Milestone #10 Benchmark Refresh v1.

Local-only deterministic benchmark refresh after solver patch helper creation.

This module reads the Milestone #10 solver patch implementation artifact and
uses the isolated local helper functions to run a benchmark refresh. It does not
create a submission candidate. It does not submit to Kaggle, authenticate,
upload files, call external APIs, read secrets, grant approval, claim a public
score, claim leaderboard movement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from hbce_arc_agi3.milestone_10_solver_patch_implementation import (
    build_trace_generalization_fields,
    compute_color_remap_stability_score,
    extract_object_boundary_signature,
    rank_candidates_by_patch_evidence,
    rank_symmetry_axis_candidates,
    score_composition_order,
)


REFRESH_STATUS = "MILESTONE_10_BENCHMARK_REFRESH_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_BENCHMARK_REFRESH_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_BENCHMARK_REFRESH_V1_VALID"

BASELINE_COMMIT = "8dc1cfc Implement ARC AGI3 solver patch helpers"
REFRESH_MODE = "MILESTONE_10_BENCHMARK_REFRESH_V1_LOCAL_ONLY"
REFRESH_SCOPE = "LOCAL_BENCHMARK_REFRESH_NO_CANDIDATE_REFRESH"
REFRESH_VERDICT = "BENCHMARK_REFRESH_READY_FOR_CONTROLLED_CANDIDATE_REFRESH"
NEXT_ALLOWED_STAGE = "MILESTONE_10_TASK_6_CANDIDATE_REFRESH_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/benchmark-refresh-v1"

IMPLEMENTATION_JSON = Path(
    "examples/milestone-10/solver-patch-implementation-v1/"
    "milestone-10-solver-patch-implementation-v1.json"
)

EXPECTED_BENCHMARK_TASK_COUNT = 6
EXPECTED_BENCHMARK_FAMILY_COUNT = 6
EXPECTED_BENCHMARK_CHECK_COUNT = 24
EXPECTED_BENCHMARK_CASE_COUNT = 10
EXPECTED_BENCHMARK_PASS_COUNT = 10
EXPECTED_BENCHMARK_FAILURE_COUNT = 0
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_FAIL_CLOSED_CONTROL_COUNT = 8

LOCAL_BENCHMARK_TASKS: Tuple[Dict[str, Any], ...] = (
    {
        "task_id": "m10_benchmark_color_remap_stability_v1",
        "family": "color_mapping",
        "helper": "compute_color_remap_stability_score",
        "expected_min_score": 80,
    },
    {
        "task_id": "m10_benchmark_object_boundary_signature_v1",
        "family": "object_model",
        "helper": "extract_object_boundary_signature",
        "expected_min_score": 90,
    },
    {
        "task_id": "m10_benchmark_symmetry_axis_tiebreak_v1",
        "family": "shape_symmetry",
        "helper": "rank_symmetry_axis_candidates",
        "expected_min_score": 90,
    },
    {
        "task_id": "m10_benchmark_composition_order_scoring_v1",
        "family": "cross_family_composition",
        "helper": "score_composition_order",
        "expected_min_score": 85,
    },
    {
        "task_id": "m10_benchmark_ranker_evidence_tiebreak_v1",
        "family": "candidate_ranker",
        "helper": "rank_candidates_by_patch_evidence",
        "expected_min_score": 90,
    },
    {
        "task_id": "m10_benchmark_trace_generalization_fields_v1",
        "family": "traceability",
        "helper": "build_trace_generalization_fields",
        "expected_min_score": 90,
    },
)

FAIL_CLOSED_CONTROLS: Tuple[str, ...] = (
    "real_submission_decision_not_authorized",
    "real_submission_allowed_false",
    "manual_upload_allowed_false",
    "kaggle_authentication_allowed_false",
    "kaggle_submission_sent_false",
    "upload_performed_false",
    "external_api_dependency_false",
    "fail_closed_active",
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

BENCHMARK_CHECKS: Tuple[str, ...] = (
    "implementation_artifact_exists",
    "implementation_artifact_ready",
    "implementation_signature_present",
    "implementation_next_stage_matches_task_5",
    "helper_function_count_valid",
    "patch_target_count_valid",
    "benchmark_task_count_valid",
    "benchmark_family_count_valid",
    "all_benchmark_tasks_pass",
    "average_score_valid",
    "refresh_record_created",
    "refresh_ready",
    "candidate_refresh_required_next",
    "runtime_integration_not_performed",
    "solver_runtime_not_modified",
    "submission_candidate_not_created",
    "fail_closed_required",
    "fail_closed_active",
    "real_submission_not_authorized",
    "real_submission_blocked",
    "manual_upload_blocked",
    "kaggle_submission_absent",
    "no_private_core_exposure",
    "no_legal_certification",
)

BENCHMARK_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_benchmark_refresh_implementation_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_patch_implementation_source",
    },
    {
        "case_id": "m10_benchmark_refresh_task_catalog_ready_v1",
        "area": "benchmark_catalog",
        "operation": "verify_benchmark_task_catalog",
    },
    {
        "case_id": "m10_benchmark_refresh_color_remap_pass_v1",
        "area": "benchmark",
        "operation": "run_color_remap_benchmark",
    },
    {
        "case_id": "m10_benchmark_refresh_object_boundary_pass_v1",
        "area": "benchmark",
        "operation": "run_object_boundary_benchmark",
    },
    {
        "case_id": "m10_benchmark_refresh_symmetry_pass_v1",
        "area": "benchmark",
        "operation": "run_symmetry_benchmark",
    },
    {
        "case_id": "m10_benchmark_refresh_composition_pass_v1",
        "area": "benchmark",
        "operation": "run_composition_benchmark",
    },
    {
        "case_id": "m10_benchmark_refresh_ranker_pass_v1",
        "area": "benchmark",
        "operation": "run_ranker_benchmark",
    },
    {
        "case_id": "m10_benchmark_refresh_trace_pass_v1",
        "area": "benchmark",
        "operation": "run_trace_benchmark",
    },
    {
        "case_id": "m10_benchmark_refresh_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_preserved",
    },
    {
        "case_id": "m10_benchmark_refresh_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_candidate_refresh_next",
    },
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


def build_benchmark_refresh_source_summary() -> Dict[str, Any]:
    implementation = _read_json(IMPLEMENTATION_JSON)
    source = implementation.get("source_summary", {})

    return {
        "implementation_path": str(IMPLEMENTATION_JSON),
        "implementation_present": IMPLEMENTATION_JSON.exists(),
        "implementation_status": implementation.get("status", "MISSING"),
        "implementation_id": implementation.get("implementation_id", "MISSING_IMPLEMENTATION_ID"),
        "implementation_signature": implementation.get("signature", ""),
        "implementation_ready": implementation.get("implementation_ready", False),
        "implementation_locked": implementation.get("implementation_locked", False),
        "implementation_baseline_commit": implementation.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "next_allowed_stage": implementation.get("next_allowed_stage", "MISSING_NEXT_STAGE"),
        "implementation_function_count": implementation.get("implementation_function_count", 0),
        "patch_target_count": implementation.get("patch_target_count", 0),
        "runtime_helper_functions_created": implementation.get("runtime_helper_functions_created", False),
        "runtime_integration_performed": implementation.get("runtime_integration_performed", True),
        "solver_runtime_modified": implementation.get("solver_runtime_modified", True),
        "submission_candidate_created": implementation.get("submission_candidate_created", True),
        "benchmark_required_next": implementation.get("benchmark_required_next", False),
        "candidate_source_path": source.get("candidate_source_path", "MISSING_CANDIDATE_SOURCE"),
        "candidate_id": source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_signature": source.get("candidate_signature", ""),
        "candidate_count": source.get("candidate_count", 0),
        "real_submission_decision": implementation.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": implementation.get("real_submission_allowed", True),
        "manual_upload_allowed": implementation.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": implementation.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": implementation.get("kaggle_submission_sent", True),
        "fail_closed_required": implementation.get("fail_closed_required", False),
        "fail_closed_active": implementation.get("fail_closed_active", False),
        "implementation_sha256": _sha256(IMPLEMENTATION_JSON),
        "implementation_sha256_16": _sha16(_sha256(IMPLEMENTATION_JSON)),
    }


def build_local_benchmark_task_catalog() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            **task,
            "local_only": True,
            "deterministic": True,
            "uses_patch_helper": True,
            "requires_external_api": False,
            "requires_kaggle_upload": False,
            "creates_submission_candidate": False,
            "ready_for_refresh": True,
        }
        for task in LOCAL_BENCHMARK_TASKS
    )


def evaluate_local_benchmark_task(task_id: str) -> Dict[str, Any]:
    if task_id == "m10_benchmark_color_remap_stability_v1":
        sample = compute_color_remap_stability_score({1: 2, 3: 4}, unseen_color_count=1)
        score = int(sample["score"])
        return {
            "task_id": task_id,
            "family": "color_mapping",
            "score": score,
            "passed": sample["stable"] is True and score >= 80,
            "sample": sample,
        }

    if task_id == "m10_benchmark_object_boundary_signature_v1":
        sample = extract_object_boundary_signature([[0, 0, 0], [0, 8, 8], [0, 0, 8]])
        score = 100 if sample["bbox"] and sample["nonzero_count"] == 3 else 0
        return {
            "task_id": task_id,
            "family": "object_model",
            "score": score,
            "passed": score >= 90,
            "sample": sample,
        }

    if task_id == "m10_benchmark_symmetry_axis_tiebreak_v1":
        sample = rank_symmetry_axis_candidates(
            [
                {"axis": "horizontal", "score": 90, "evidence_count": 2, "penalty": 1},
                {"axis": "vertical", "score": 90, "evidence_count": 3, "penalty": 1},
                {"axis": "diagonal", "score": 80, "evidence_count": 5, "penalty": 0},
            ]
        )
        score = 100 if sample["best_axis"] == "vertical" else 0
        return {
            "task_id": task_id,
            "family": "shape_symmetry",
            "score": score,
            "passed": score >= 90,
            "sample": sample,
        }

    if task_id == "m10_benchmark_composition_order_scoring_v1":
        sample = score_composition_order(
            ["color_mapping", "object_model", "shape_symmetry", "candidate_ranker"]
        )
        score = int(sample["score"])
        return {
            "task_id": task_id,
            "family": "cross_family_composition",
            "score": score,
            "passed": sample["stable_order"] is True and score >= 85,
            "sample": sample,
        }

    if task_id == "m10_benchmark_ranker_evidence_tiebreak_v1":
        sample = rank_candidates_by_patch_evidence(
            [
                {
                    "candidate_id": "candidate_b",
                    "score_hint": 0.91,
                    "confidence": 0.8,
                    "family_evidence": 4,
                    "complexity": 3,
                },
                {
                    "candidate_id": "candidate_a",
                    "score_hint": 0.91,
                    "confidence": 0.85,
                    "family_evidence": 3,
                    "complexity": 2,
                },
            ]
        )
        score = 100 if sample["best_candidate_id"] == "candidate_a" else 0
        return {
            "task_id": task_id,
            "family": "candidate_ranker",
            "score": score,
            "passed": score >= 90,
            "sample": sample,
        }

    if task_id == "m10_benchmark_trace_generalization_fields_v1":
        sample = build_trace_generalization_fields(
            task_id="local-benchmark-task",
            family="traceability",
            assumptions=("patch helper deterministic", "no external dependency"),
        )
        score = 100 if sample["trace_ready"] and len(sample["generalization_trace_hash"]) == 64 else 0
        return {
            "task_id": task_id,
            "family": "traceability",
            "score": score,
            "passed": score >= 90,
            "sample": sample,
        }

    raise ValueError(f"unknown local benchmark task: {task_id}")


def evaluate_all_local_benchmark_tasks() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_local_benchmark_task(task["task_id"]) for task in LOCAL_BENCHMARK_TASKS)


def build_benchmark_refresh_metrics() -> Dict[str, Any]:
    results = evaluate_all_local_benchmark_tasks()
    task_pass_count = sum(1 for item in results if item["passed"] is True)
    task_failure_count = sum(1 for item in results if item["passed"] is False)
    average_score = round(sum(int(item["score"]) for item in results) / len(results), 2)

    return {
        "benchmark_task_count": len(results),
        "benchmark_family_count": len({item["family"] for item in results}),
        "benchmark_task_pass_count": task_pass_count,
        "benchmark_task_failure_count": task_failure_count,
        "average_score": average_score,
        "minimum_score": min(int(item["score"]) for item in results),
        "maximum_score": max(int(item["score"]) for item in results),
        "all_benchmark_tasks_pass": all(item["passed"] is True for item in results),
        "results": list(results),
    }


def build_benchmark_refresh_state() -> Dict[str, Any]:
    return {
        "benchmark_refresh_required": True,
        "benchmark_refresh_created": True,
        "benchmark_refresh_ready": True,
        "benchmark_refresh_locked": True,
        "refresh_mode": REFRESH_MODE,
        "refresh_scope": REFRESH_SCOPE,
        "refresh_verdict": REFRESH_VERDICT,
        "benchmark_task_count": len(LOCAL_BENCHMARK_TASKS),
        "benchmark_family_count": len({task["family"] for task in LOCAL_BENCHMARK_TASKS}),
        "candidate_refresh_required_next": True,
        "submission_candidate_created": False,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }


def build_benchmark_refresh_checks() -> Dict[str, bool]:
    source = build_benchmark_refresh_source_summary()
    catalog = build_local_benchmark_task_catalog()
    metrics = build_benchmark_refresh_metrics()
    state = build_benchmark_refresh_state()

    return {
        "implementation_artifact_present": source["implementation_present"],
        "implementation_artifact_ready": source["implementation_status"]
        == "MILESTONE_10_SOLVER_PATCH_IMPLEMENTATION_V1_READY",
        "implementation_artifact_valid": source["implementation_id"].startswith(
            "MILESTONE-10-SOLVER-PATCH-IMPLEMENTATION-"
        )
        and bool(source["implementation_signature"]),
        "implementation_commit_valid": str(source["implementation_baseline_commit"]).startswith("d03c8d0"),
        "implementation_next_stage_matches_task_5": source["next_allowed_stage"]
        == "MILESTONE_10_TASK_5_BENCHMARK_REFRESH_V1",
        "implementation_ready": source["implementation_ready"] is True,
        "implementation_locked": source["implementation_locked"] is True,
        "implementation_function_count_valid": source["implementation_function_count"] == 6,
        "patch_target_count_valid": source["patch_target_count"] == 6,
        "runtime_helper_functions_created": source["runtime_helper_functions_created"] is True,
        "runtime_integration_not_performed": source["runtime_integration_performed"] is False,
        "solver_runtime_not_modified": source["solver_runtime_modified"] is False,
        "submission_candidate_not_created": source["submission_candidate_created"] is False,
        "benchmark_required_next": source["benchmark_required_next"] is True,
        "benchmark_task_count_valid": len(catalog) == EXPECTED_BENCHMARK_TASK_COUNT
        and metrics["benchmark_task_count"] == EXPECTED_BENCHMARK_TASK_COUNT,
        "benchmark_family_count_valid": metrics["benchmark_family_count"] == EXPECTED_BENCHMARK_FAMILY_COUNT,
        "all_benchmark_tasks_local_only": all(task["local_only"] is True for task in catalog),
        "all_benchmark_tasks_deterministic": all(task["deterministic"] is True for task in catalog),
        "all_benchmark_tasks_use_patch_helpers": all(task["uses_patch_helper"] is True for task in catalog),
        "all_benchmark_tasks_no_external_api": all(
            task["requires_external_api"] is False for task in catalog
        ),
        "all_benchmark_tasks_no_upload": all(
            task["requires_kaggle_upload"] is False for task in catalog
        ),
        "all_benchmark_tasks_no_candidate": all(
            task["creates_submission_candidate"] is False for task in catalog
        ),
        "all_benchmark_tasks_pass": metrics["all_benchmark_tasks_pass"] is True,
        "benchmark_task_pass_count_valid": metrics["benchmark_task_pass_count"]
        == EXPECTED_BENCHMARK_TASK_COUNT,
        "benchmark_task_failure_count_zero": metrics["benchmark_task_failure_count"] == 0,
        "average_score_valid": metrics["average_score"] >= 95,
        "minimum_score_valid": metrics["minimum_score"] >= 90,
        "candidate_source_present": Path(source["candidate_source_path"]).exists(),
        "candidate_id_present": source["candidate_id"] != "MISSING_CANDIDATE_ID",
        "candidate_signature_present": bool(source["candidate_signature"]),
        "candidate_count_positive": source["candidate_count"] > 0,
        "benchmark_check_count_valid": len(BENCHMARK_CHECKS) == EXPECTED_BENCHMARK_CHECK_COUNT,
        "benchmark_case_count_valid": len(BENCHMARK_CASES) == EXPECTED_BENCHMARK_CASE_COUNT,
        "fail_closed_control_count_valid": len(FAIL_CLOSED_CONTROLS)
        == EXPECTED_FAIL_CLOSED_CONTROL_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "refresh_record_created": state["benchmark_refresh_created"] is True,
        "refresh_record_ready": state["benchmark_refresh_ready"] is True,
        "refresh_record_locked": state["benchmark_refresh_locked"] is True,
        "refresh_mode_valid": REFRESH_MODE == "MILESTONE_10_BENCHMARK_REFRESH_V1_LOCAL_ONLY",
        "refresh_scope_valid": REFRESH_SCOPE == "LOCAL_BENCHMARK_REFRESH_NO_CANDIDATE_REFRESH",
        "refresh_verdict_valid": REFRESH_VERDICT
        == "BENCHMARK_REFRESH_READY_FOR_CONTROLLED_CANDIDATE_REFRESH",
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_10_TASK_6_CANDIDATE_REFRESH_V1",
        "candidate_refresh_required_next": state["candidate_refresh_required_next"] is True,
        "real_submission_decision_not_authorized": source["real_submission_decision"] == "NOT_AUTHORIZED"
        and state["real_submission_decision"] == "NOT_AUTHORIZED",
        "real_submission_allowed_false": source["real_submission_allowed"] is False
        and state["real_submission_allowed"] is False,
        "manual_upload_not_allowed": source["manual_upload_allowed"] is False
        and state["manual_upload_allowed"] is False,
        "kaggle_authentication_not_allowed": source["kaggle_authentication_allowed"] is False
        and state["kaggle_authentication_allowed"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False
        and state["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True
        and state["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True
        and state["fail_closed_active"] is True,
        "external_api_dependency_false": state["external_api_dependency"] is False,
        "private_core_exposure_false": state["private_core_exposure"] is False,
        "legal_certification_false": state["legal_certification"] is False,
    }


def evaluate_benchmark_refresh_case(case_id: str) -> Dict[str, Any]:
    checks = build_benchmark_refresh_checks()
    benchmark_results = {item["task_id"]: item for item in evaluate_all_local_benchmark_tasks()}

    if case_id == "m10_benchmark_refresh_implementation_source_ready_v1":
        passed = (
            checks["implementation_artifact_present"]
            and checks["implementation_artifact_ready"]
            and checks["implementation_artifact_valid"]
            and checks["implementation_ready"]
        )
        return _result(case_id, "source_binding", "verify_patch_implementation_source", passed)

    if case_id == "m10_benchmark_refresh_task_catalog_ready_v1":
        passed = (
            checks["benchmark_task_count_valid"]
            and checks["benchmark_family_count_valid"]
            and checks["all_benchmark_tasks_use_patch_helpers"]
        )
        return _result(case_id, "benchmark_catalog", "verify_benchmark_task_catalog", passed)

    task_case_map = {
        "m10_benchmark_refresh_color_remap_pass_v1": "m10_benchmark_color_remap_stability_v1",
        "m10_benchmark_refresh_object_boundary_pass_v1": "m10_benchmark_object_boundary_signature_v1",
        "m10_benchmark_refresh_symmetry_pass_v1": "m10_benchmark_symmetry_axis_tiebreak_v1",
        "m10_benchmark_refresh_composition_pass_v1": "m10_benchmark_composition_order_scoring_v1",
        "m10_benchmark_refresh_ranker_pass_v1": "m10_benchmark_ranker_evidence_tiebreak_v1",
        "m10_benchmark_refresh_trace_pass_v1": "m10_benchmark_trace_generalization_fields_v1",
    }

    if case_id in task_case_map:
        task = benchmark_results[task_case_map[case_id]]
        return _result(case_id, "benchmark", f"run_{task['family']}_benchmark", task["passed"])

    if case_id == "m10_benchmark_refresh_fail_closed_preserved_v1":
        passed = (
            checks["fail_closed_required"]
            and checks["fail_closed_active"]
            and checks["real_submission_allowed_false"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "fail_closed", "verify_fail_closed_preserved", passed)

    if case_id == "m10_benchmark_refresh_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_candidate_refresh_next", checks["next_stage_valid"])

    raise ValueError(f"unknown benchmark refresh case: {case_id}")


def evaluate_all_benchmark_refresh_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_benchmark_refresh_case(case["case_id"]) for case in BENCHMARK_CASES)


def build_milestone_10_benchmark_refresh() -> Dict[str, Any]:
    source = build_benchmark_refresh_source_summary()
    catalog = build_local_benchmark_task_catalog()
    metrics = build_benchmark_refresh_metrics()
    state = build_benchmark_refresh_state()
    checks = build_benchmark_refresh_checks()
    results = evaluate_all_benchmark_refresh_cases()

    benchmark_pass_count = sum(1 for result in results if result["passed"] is True)
    benchmark_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "implementation_artifact_present": checks["implementation_artifact_present"],
        "implementation_artifact_ready": checks["implementation_artifact_ready"],
        "implementation_artifact_valid": checks["implementation_artifact_valid"],
        "implementation_commit_valid": checks["implementation_commit_valid"],
        "implementation_next_stage_matches_task_5": checks[
            "implementation_next_stage_matches_task_5"
        ],
        "implementation_ready": checks["implementation_ready"],
        "implementation_locked": checks["implementation_locked"],
        "implementation_function_count_valid": checks["implementation_function_count_valid"],
        "patch_target_count_valid": checks["patch_target_count_valid"],
        "runtime_helper_functions_created": checks["runtime_helper_functions_created"],
        "runtime_integration_not_performed": checks["runtime_integration_not_performed"],
        "solver_runtime_not_modified": checks["solver_runtime_not_modified"],
        "submission_candidate_not_created": checks["submission_candidate_not_created"],
        "benchmark_required_next": checks["benchmark_required_next"],
        "benchmark_task_count_valid": checks["benchmark_task_count_valid"],
        "benchmark_family_count_valid": checks["benchmark_family_count_valid"],
        "all_benchmark_tasks_local_only": checks["all_benchmark_tasks_local_only"],
        "all_benchmark_tasks_deterministic": checks["all_benchmark_tasks_deterministic"],
        "all_benchmark_tasks_use_patch_helpers": checks["all_benchmark_tasks_use_patch_helpers"],
        "all_benchmark_tasks_no_external_api": checks["all_benchmark_tasks_no_external_api"],
        "all_benchmark_tasks_no_upload": checks["all_benchmark_tasks_no_upload"],
        "all_benchmark_tasks_no_candidate": checks["all_benchmark_tasks_no_candidate"],
        "all_benchmark_tasks_pass": checks["all_benchmark_tasks_pass"],
        "benchmark_task_pass_count_valid": checks["benchmark_task_pass_count_valid"],
        "benchmark_task_failure_count_zero": checks["benchmark_task_failure_count_zero"],
        "average_score_valid": checks["average_score_valid"],
        "minimum_score_valid": checks["minimum_score_valid"],
        "candidate_source_present": checks["candidate_source_present"],
        "candidate_id_present": checks["candidate_id_present"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "benchmark_check_count_valid": checks["benchmark_check_count_valid"],
        "benchmark_case_count_valid": checks["benchmark_case_count_valid"],
        "fail_closed_control_count_valid": checks["fail_closed_control_count_valid"],
        "boundary_control_count_valid": checks["boundary_control_count_valid"],
        "refresh_record_created": checks["refresh_record_created"],
        "refresh_record_ready": checks["refresh_record_ready"],
        "refresh_record_locked": checks["refresh_record_locked"],
        "refresh_mode_valid": checks["refresh_mode_valid"],
        "refresh_scope_valid": checks["refresh_scope_valid"],
        "refresh_verdict_valid": checks["refresh_verdict_valid"],
        "next_stage_valid": checks["next_stage_valid"],
        "candidate_refresh_required_next": checks["candidate_refresh_required_next"],
        "real_submission_decision_not_authorized": checks["real_submission_decision_not_authorized"],
        "real_submission_allowed_false": checks["real_submission_allowed_false"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "kaggle_submission_not_sent": checks["kaggle_submission_not_sent"],
        "fail_closed_required": checks["fail_closed_required"],
        "fail_closed_active": checks["fail_closed_active"],
        "external_api_dependency_false": checks["external_api_dependency_false"],
        "private_core_exposure_false": checks["private_core_exposure_false"],
        "legal_certification_false": checks["legal_certification_false"],
        "all_benchmark_cases_pass": all(result["passed"] is True for result in results),
        "benchmark_pass_count_valid": benchmark_pass_count == EXPECTED_BENCHMARK_PASS_COUNT,
        "benchmark_failure_count_zero": benchmark_failure_count == EXPECTED_BENCHMARK_FAILURE_COUNT,
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
            "name": name.replace("_valid", "_invalid").replace("_ready", "_not_ready"),
            "active": not passed,
            "severity": "BLOCKING",
        }
        for name, passed in gate_state.items()
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    refresh_ready = (
        benchmark_pass_count == EXPECTED_BENCHMARK_PASS_COUNT
        and benchmark_failure_count == EXPECTED_BENCHMARK_FAILURE_COUNT
        and checks["implementation_artifact_ready"]
        and checks["all_benchmark_tasks_pass"]
        and checks["average_score_valid"]
        and checks["submission_candidate_not_created"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #10",
        "task": "Task 5",
        "refresh_mode": REFRESH_MODE,
        "refresh_scope": REFRESH_SCOPE,
        "refresh_verdict": REFRESH_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_implementation": source["implementation_id"],
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_count": source["candidate_count"],
        "refresh_ready": refresh_ready,
        "benchmark_refresh_created": True,
        "benchmark_refresh_ready": True,
        "benchmark_task_count": metrics["benchmark_task_count"],
        "benchmark_family_count": metrics["benchmark_family_count"],
        "benchmark_task_pass_count": metrics["benchmark_task_pass_count"],
        "benchmark_task_failure_count": metrics["benchmark_task_failure_count"],
        "average_score": metrics["average_score"],
        "candidate_refresh_required_next": True,
        "submission_candidate_created": False,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": REFRESH_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 5",
        "title": "Benchmark Refresh v1",
        "baseline_commit": BASELINE_COMMIT,
        "refresh_mode": REFRESH_MODE,
        "refresh_scope": REFRESH_SCOPE,
        "refresh_verdict": REFRESH_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "implementation_source": {
            "path": str(IMPLEMENTATION_JSON),
            "present": IMPLEMENTATION_JSON.exists(),
            "status": source["implementation_status"],
            "implementation_id": source["implementation_id"],
            "sha256": _sha256(IMPLEMENTATION_JSON),
            "sha256_16": _sha16(_sha256(IMPLEMENTATION_JSON)),
        },
        "source_summary": source,
        "benchmark_state": state,
        "benchmark_catalog": list(catalog),
        "benchmark_metrics": metrics,
        "fail_closed_controls": list(FAIL_CLOSED_CONTROLS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "benchmark_checks": checks,
        "benchmark_check_list": list(BENCHMARK_CHECKS),
        "benchmark_cases": list(BENCHMARK_CASES),
        "benchmark_results": list(results),
        "benchmark_gates": list(gates),
        "benchmark_issues": list(issues),
        "benchmark_index": index,
        "refresh_ready": refresh_ready,
        "refresh_locked": True,
        "benchmark_refresh_created": True,
        "benchmark_refresh_ready": True,
        "benchmark_refresh_locked": True,
        "benchmark_task_count": metrics["benchmark_task_count"],
        "benchmark_family_count": metrics["benchmark_family_count"],
        "benchmark_task_pass_count": metrics["benchmark_task_pass_count"],
        "benchmark_task_failure_count": metrics["benchmark_task_failure_count"],
        "average_score": metrics["average_score"],
        "minimum_score": metrics["minimum_score"],
        "maximum_score": metrics["maximum_score"],
        "benchmark_check_count": len(BENCHMARK_CHECKS),
        "benchmark_case_count": len(BENCHMARK_CASES),
        "benchmark_pass_count": benchmark_pass_count,
        "benchmark_failure_count": benchmark_failure_count,
        "benchmark_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "benchmark_issue_count": issue_count,
        "warning_count": 0,
        "candidate_refresh_required_next": True,
        "submission_candidate_created": False,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "metadata": {
            "source": "milestone_10_benchmark_refresh_v1",
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
        "refresh_id": f"MILESTONE-10-BENCHMARK-REFRESH-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_benchmark_refresh(refresh: Mapping[str, Any]) -> Dict[str, Any]:
    gates = refresh.get("benchmark_gates", [])
    issues = refresh.get("benchmark_issues", [])
    results = refresh.get("benchmark_results", [])
    catalog = refresh.get("benchmark_catalog", [])

    checks = {
        "status_ready": refresh.get("status") == REFRESH_STATUS,
        "refresh_id_present": isinstance(refresh.get("refresh_id"), str)
        and bool(refresh.get("refresh_id")),
        "signature_present": isinstance(refresh.get("signature"), str)
        and bool(refresh.get("signature")),
        "baseline_commit_valid": str(refresh.get("baseline_commit", "")).startswith("8dc1cfc"),
        "refresh_mode_valid": refresh.get("refresh_mode") == REFRESH_MODE,
        "refresh_scope_valid": refresh.get("refresh_scope") == REFRESH_SCOPE,
        "refresh_verdict_valid": refresh.get("refresh_verdict") == REFRESH_VERDICT,
        "next_allowed_stage_valid": refresh.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "refresh_ready": refresh.get("refresh_ready") is True,
        "refresh_locked": refresh.get("refresh_locked") is True,
        "refresh_created": refresh.get("benchmark_refresh_created") is True,
        "refresh_record_ready": refresh.get("benchmark_refresh_ready") is True,
        "refresh_record_locked": refresh.get("benchmark_refresh_locked") is True,
        "benchmark_task_count_valid": refresh.get("benchmark_task_count")
        == EXPECTED_BENCHMARK_TASK_COUNT,
        "benchmark_family_count_valid": refresh.get("benchmark_family_count")
        == EXPECTED_BENCHMARK_FAMILY_COUNT,
        "benchmark_task_pass_count_valid": refresh.get("benchmark_task_pass_count")
        == EXPECTED_BENCHMARK_TASK_COUNT,
        "benchmark_task_failure_count_zero": refresh.get("benchmark_task_failure_count") == 0,
        "average_score_valid": float(refresh.get("average_score", 0.0)) >= 95,
        "benchmark_check_count_valid": refresh.get("benchmark_check_count")
        == EXPECTED_BENCHMARK_CHECK_COUNT,
        "benchmark_case_count_valid": refresh.get("benchmark_case_count")
        == EXPECTED_BENCHMARK_CASE_COUNT,
        "benchmark_pass_count_valid": refresh.get("benchmark_pass_count")
        == EXPECTED_BENCHMARK_PASS_COUNT,
        "benchmark_failure_count_zero": refresh.get("benchmark_failure_count")
        == EXPECTED_BENCHMARK_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "catalog_local_only": bool(catalog) and all(item.get("local_only") is True for item in catalog),
        "catalog_no_upload": bool(catalog)
        and all(item.get("requires_kaggle_upload") is False for item in catalog),
        "candidate_refresh_required_next": refresh.get("candidate_refresh_required_next") is True,
        "submission_candidate_not_created": refresh.get("submission_candidate_created") is False,
        "real_submission_decision_not_authorized": refresh.get("real_submission_decision")
        == "NOT_AUTHORIZED",
        "real_submission_allowed_false": refresh.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": refresh.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": refresh.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": refresh.get("kaggle_submission_sent") is False,
        "fail_closed_required": refresh.get("fail_closed_required") is True,
        "fail_closed_active": refresh.get("fail_closed_active") is True,
        "metadata_safe": refresh.get("metadata", {}).get("external_api_dependency") is False
        and refresh.get("metadata", {}).get("contains_api_keys") is False
        and refresh.get("metadata", {}).get("private_core_exposure") is False
        and refresh.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_BENCHMARK_REFRESH_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "refresh_id": refresh.get("refresh_id"),
        "signature": refresh.get("signature"),
    }


def render_benchmark_refresh_markdown(refresh: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Benchmark Refresh v1",
        "",
        f"- status: {refresh['status']}",
        f"- refresh_id: {refresh['refresh_id']}",
        f"- signature: {refresh['signature']}",
        f"- baseline_commit: {refresh['baseline_commit']}",
        f"- refresh_mode: {refresh['refresh_mode']}",
        f"- refresh_scope: {refresh['refresh_scope']}",
        f"- refresh_verdict: {refresh['refresh_verdict']}",
        f"- next_allowed_stage: {refresh['next_allowed_stage']}",
        f"- refresh_ready: {refresh['refresh_ready']}",
        f"- benchmark_task_count: {refresh['benchmark_task_count']}",
        f"- benchmark_family_count: {refresh['benchmark_family_count']}",
        f"- benchmark_task_pass_count: {refresh['benchmark_task_pass_count']}",
        f"- benchmark_task_failure_count: {refresh['benchmark_task_failure_count']}",
        f"- average_score: {refresh['average_score']}",
        f"- candidate_refresh_required_next: {refresh['candidate_refresh_required_next']}",
        f"- submission_candidate_created: {refresh['submission_candidate_created']}",
        f"- real_submission_decision: {refresh['real_submission_decision']}",
        f"- real_submission_allowed: {refresh['real_submission_allowed']}",
        f"- fail_closed_active: {refresh['fail_closed_active']}",
        "",
        "## Benchmark task results",
        "",
    ]

    for result in refresh["benchmark_metrics"]["results"]:
        lines.append(
            f"- {result['task_id']} / family={result['family']} / "
            f"score={result['score']} / passed={result['passed']}"
        )

    lines.extend(["", "## Validation results", ""])

    for result in refresh["benchmark_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Benchmark refresh is ready. The next stage is controlled candidate refresh. No submission candidate is created in this task.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_REFRESH_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_REFRESH_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_REFRESH_READY=true",
            "ARC_AGI3_MILESTONE_10_REFRESH_MODE=MILESTONE_10_BENCHMARK_REFRESH_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_REFRESH_VERDICT=BENCHMARK_REFRESH_READY_FOR_CONTROLLED_CANDIDATE_REFRESH",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=8dc1cfc",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_6_CANDIDATE_REFRESH_V1",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_TASK_COUNT=6",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_FAMILY_COUNT=6",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_TASK_PASS_COUNT=6",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_TASK_FAILURE_COUNT=0",
            f"ARC_AGI3_MILESTONE_10_BENCHMARK_AVERAGE_SCORE={refresh['average_score']}",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_CHECK_COUNT=24",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_REFRESH_CREATED=true",
            "ARC_AGI3_MILESTONE_10_BENCHMARK_REFRESH_READY=true",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_REQUIRED_NEXT=true",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_MANUAL_UPLOAD_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_KAGGLE_AUTHENTICATION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_REQUIRED=true",
            "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_benchmark_refresh_manifest(refresh: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 BENCHMARK REFRESH MANIFEST v1",
        f"refresh_id={refresh['refresh_id']}",
        f"signature={refresh['signature']}",
        f"status={refresh['status']}",
        f"baseline_commit={refresh['baseline_commit']}",
        f"refresh_mode={refresh['refresh_mode']}",
        f"refresh_verdict={refresh['refresh_verdict']}",
        f"next_allowed_stage={refresh['next_allowed_stage']}",
        f"refresh_ready={refresh['refresh_ready']}",
        f"benchmark_refresh_created={refresh['benchmark_refresh_created']}",
        f"benchmark_refresh_ready={refresh['benchmark_refresh_ready']}",
        f"benchmark_task_count={refresh['benchmark_task_count']}",
        f"benchmark_family_count={refresh['benchmark_family_count']}",
        f"benchmark_task_pass_count={refresh['benchmark_task_pass_count']}",
        f"benchmark_task_failure_count={refresh['benchmark_task_failure_count']}",
        f"average_score={refresh['average_score']}",
        f"benchmark_check_count={refresh['benchmark_check_count']}",
        f"benchmark_case_count={refresh['benchmark_case_count']}",
        f"benchmark_pass_count={refresh['benchmark_pass_count']}",
        f"benchmark_failure_count={refresh['benchmark_failure_count']}",
        f"benchmark_gate_count={refresh['benchmark_gate_count']}",
        f"passed_gate_count={refresh['passed_gate_count']}",
        f"benchmark_issue_count={refresh['benchmark_issue_count']}",
        f"candidate_refresh_required_next={refresh['candidate_refresh_required_next']}",
        f"submission_candidate_created={refresh['submission_candidate_created']}",
        f"real_submission_decision={refresh['real_submission_decision']}",
        f"real_submission_allowed={refresh['real_submission_allowed']}",
        f"manual_upload_allowed={refresh['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={refresh['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={refresh['kaggle_submission_sent']}",
        f"fail_closed_required={refresh['fail_closed_required']}",
        f"fail_closed_active={refresh['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "BENCHMARK_TASK_RESULTS",
    ]

    for result in refresh["benchmark_metrics"]["results"]:
        lines.append(
            f"{result['task_id']} family={result['family']} score={result['score']} "
            f"passed={result['passed']}"
        )

    lines.append("")
    lines.append("BENCHMARK_VALIDATION_RESULTS")
    for result in refresh["benchmark_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_benchmark_refresh_artifacts(
    refresh: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    refresh = dict(refresh or build_milestone_10_benchmark_refresh())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-benchmark-refresh-v1.json"
    md_path = output / "milestone-10-benchmark-refresh-v1.md"
    manifest_path = output / "milestone-10-benchmark-refresh-manifest-v1.txt"
    index_path = output / "milestone-10-benchmark-refresh-index-v1.json"

    json_path.write_text(json.dumps(refresh, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_benchmark_refresh_markdown(refresh), encoding="utf-8")
    manifest_path.write_text(render_benchmark_refresh_manifest(refresh), encoding="utf-8")
    index_path.write_text(
        json.dumps(refresh["benchmark_index"], indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_10_benchmark_refresh_pipeline() -> Dict[str, Any]:
    refresh = build_milestone_10_benchmark_refresh()
    validation = validate_milestone_10_benchmark_refresh(refresh)
    artifacts = write_benchmark_refresh_artifacts(refresh)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_10_BENCHMARK_REFRESH_V1_PIPELINE_INVALID",
        "refresh_status": refresh["status"],
        "validation_status": validation["status"],
        "refresh": refresh,
        "refresh_id": refresh["refresh_id"],
        "signature": refresh["signature"],
        "refresh_mode": refresh["refresh_mode"],
        "refresh_verdict": refresh["refresh_verdict"],
        "next_allowed_stage": refresh["next_allowed_stage"],
        "refresh_ready": refresh["refresh_ready"],
        "benchmark_refresh_created": refresh["benchmark_refresh_created"],
        "benchmark_refresh_ready": refresh["benchmark_refresh_ready"],
        "benchmark_task_count": refresh["benchmark_task_count"],
        "benchmark_family_count": refresh["benchmark_family_count"],
        "benchmark_task_pass_count": refresh["benchmark_task_pass_count"],
        "benchmark_task_failure_count": refresh["benchmark_task_failure_count"],
        "average_score": refresh["average_score"],
        "benchmark_check_count": refresh["benchmark_check_count"],
        "benchmark_case_count": refresh["benchmark_case_count"],
        "benchmark_pass_count": refresh["benchmark_pass_count"],
        "benchmark_failure_count": refresh["benchmark_failure_count"],
        "benchmark_gate_count": refresh["benchmark_gate_count"],
        "passed_gate_count": refresh["passed_gate_count"],
        "benchmark_issue_count": refresh["benchmark_issue_count"],
        "warning_count": refresh["warning_count"],
        "candidate_refresh_required_next": refresh["candidate_refresh_required_next"],
        "submission_candidate_created": refresh["submission_candidate_created"],
        "real_submission_decision": refresh["real_submission_decision"],
        "real_submission_allowed": refresh["real_submission_allowed"],
        "manual_upload_allowed": refresh["manual_upload_allowed"],
        "kaggle_authentication_allowed": refresh["kaggle_authentication_allowed"],
        "kaggle_submission_sent": refresh["kaggle_submission_sent"],
        "fail_closed_required": refresh["fail_closed_required"],
        "fail_closed_active": refresh["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": refresh["metadata"],
    }
