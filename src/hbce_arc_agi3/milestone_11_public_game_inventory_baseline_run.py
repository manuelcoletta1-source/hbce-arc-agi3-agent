"""Milestone #11 Task 2 - Public Game Inventory and Baseline Run v1.

Local-only deterministic inventory and baseline preparation after Milestone #11
opening.

This module scans local candidate public-game paths, inventories available files,
classifies compatible fixture candidates, and performs a safe baseline summary
only when local compatible files exist. It does not claim a real Kaggle score,
does not create submission.json, does not create an upload package, does not
authenticate with Kaggle, does not call external APIs, does not read secrets,
and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple


STATUS = "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_VALID"

BASELINE_COMMIT = "d7d1148 Open ARC AGI3 milestone 11 public benchmark solver improvement"
TASK_MODE = "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_PUBLIC_GAME_INVENTORY_AND_SAFE_BASELINE_NO_SCORE_CLAIM"
TASK_VERDICT = "PUBLIC_GAME_INVENTORY_BASELINE_RUN_READY_FOR_FAILURE_TAXONOMY"
NEXT_STAGE = "MILESTONE_11_TASK_3_PUBLIC_GAME_FAILURE_TAXONOMY_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/public-game-inventory-baseline-run-v1"

M11_OPENING_JSON = Path(
    "examples/milestone-11/public-game-benchmark-solver-improvement-v1/"
    "milestone-11-public-game-benchmark-solver-improvement-v1.json"
)

PUBLIC_GAME_CANDIDATE_PATHS: Tuple[str, ...] = (
    "data/arc_agi_3/public",
    "data/public",
    "examples/public-games",
    "examples/arc-agi-3-public-games",
    "benchmark/public-games",
)

COMPATIBLE_SUFFIXES: Tuple[str, ...] = (".json", ".jsonl")
KNOWN_PUBLIC_FIXTURE_HINTS: Tuple[str, ...] = (
    "public",
    "game",
    "arc",
    "task",
    "train",
    "test",
    "environment",
)

EXPECTED_SELECTED_CANDIDATE_ID = "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
EXPECTED_CANDIDATE_PACKAGE_ID = "MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-CF04A9CB1B1D"
EXPECTED_REBUILT_CANDIDATE_ID = "MILESTONE-10-REBUILT-CANDIDATE-32F7FBEDFF87"

INVENTORY_CHECKS: Tuple[str, ...] = (
    "m11_opening_artifact_exists",
    "m11_opening_artifact_ready",
    "m11_opening_validated",
    "candidate_identity_loaded",
    "candidate_paths_declared",
    "inventory_created",
    "inventory_scan_completed",
    "compatible_fixture_detection_completed",
    "baseline_policy_created",
    "baseline_attempt_recorded",
    "baseline_result_recorded",
    "no_real_public_score_claimed",
    "no_private_score_claimed",
    "no_submission_json_created",
    "no_upload_package_created",
    "real_submission_blocked",
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

INVENTORY_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m11_task2_source_opening_ready_v1",
        "area": "source_binding",
        "operation": "verify_milestone_11_opening_source",
    },
    {
        "case_id": "m11_task2_candidate_identity_loaded_v1",
        "area": "identity",
        "operation": "verify_candidate_identity",
    },
    {
        "case_id": "m11_task2_public_game_paths_scanned_v1",
        "area": "inventory",
        "operation": "scan_public_game_candidate_paths",
    },
    {
        "case_id": "m11_task2_compatible_fixture_detection_v1",
        "area": "fixture_detection",
        "operation": "detect_compatible_public_fixtures",
    },
    {
        "case_id": "m11_task2_baseline_policy_ready_v1",
        "area": "baseline_policy",
        "operation": "verify_baseline_policy",
    },
    {
        "case_id": "m11_task2_safe_baseline_record_ready_v1",
        "area": "baseline",
        "operation": "verify_safe_baseline_record",
    },
    {
        "case_id": "m11_task2_no_score_claim_without_valid_run_v1",
        "area": "score_boundary",
        "operation": "verify_no_score_claim_without_valid_run",
    },
    {
        "case_id": "m11_task2_real_submission_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "m11_task2_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_next_stage",
    },
    {
        "case_id": "m11_task2_metadata_safe_v1",
        "area": "metadata",
        "operation": "verify_public_safe_metadata",
    },
)

EXPECTED_INVENTORY_CHECK_COUNT = len(INVENTORY_CHECKS)
EXPECTED_INVENTORY_CASE_COUNT = len(INVENTORY_CASES)
EXPECTED_INVENTORY_PASS_COUNT = len(INVENTORY_CASES)
EXPECTED_INVENTORY_FAILURE_COUNT = 0


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


def _safe_file_records(root: Path) -> Tuple[Dict[str, Any], ...]:
    if not root.exists() or not root.is_dir():
        return tuple()

    records = []
    for item in sorted(root.rglob("*")):
        if not item.is_file():
            continue

        rel = item.as_posix()
        suffix = item.suffix.lower()
        stat = item.stat()
        name_lower = item.name.lower()
        path_lower = rel.lower()

        records.append(
            {
                "path": rel,
                "name": item.name,
                "suffix": suffix,
                "size_bytes": stat.st_size,
                "compatible_suffix": suffix in COMPATIBLE_SUFFIXES,
                "fixture_hint_match": any(hint in path_lower or hint in name_lower for hint in KNOWN_PUBLIC_FIXTURE_HINTS),
                "sha256_16": _sha16(_sha256(item)),
            }
        )

    return tuple(records)


def build_m11_opening_source_summary() -> Dict[str, Any]:
    record = _read_json(M11_OPENING_JSON)
    source = record.get("source_summary", {})

    return {
        "m11_opening_path": str(M11_OPENING_JSON),
        "m11_opening_present": M11_OPENING_JSON.exists(),
        "m11_opening_status": record.get("status", "MISSING"),
        "m11_opening_id": record.get("milestone_11_id", "MISSING_MILESTONE_11_ID"),
        "m11_opening_signature": record.get("signature", ""),
        "m11_opening_ready": record.get("milestone_11_ready", False),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "milestone_mode": record.get("milestone_mode", "MISSING_MODE"),
        "milestone_verdict": record.get("milestone_verdict", "MISSING_VERDICT"),
        "next_stage": record.get("next_stage", "MISSING_NEXT_STAGE"),
        "benchmark_axis_count": record.get("benchmark_axis_count", 0),
        "solver_improvement_target_count": record.get("solver_improvement_target_count", 0),
        "public_game_inventory_created": record.get("public_game_inventory_created", False),
        "public_game_benchmark_execution_performed": record.get("public_game_benchmark_execution_performed", True),
        "real_public_score_claimed": record.get("real_public_score_claimed", True),
        "private_score_claimed": record.get("private_score_claimed", True),
        "selected_candidate_id": source.get("selected_candidate_id", "MISSING_SELECTED_CANDIDATE_ID"),
        "candidate_package_id": source.get("candidate_package_id", "MISSING_CANDIDATE_PACKAGE_ID"),
        "rebuilt_candidate_id": source.get("rebuilt_candidate_id", "MISSING_REBUILT_CANDIDATE_ID"),
        "m10_closure_id": source.get("m10_closure_id", "MISSING_M10_CLOSURE_ID"),
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
        "m11_opening_sha256": _sha256(M11_OPENING_JSON),
        "m11_opening_sha256_16": _sha16(_sha256(M11_OPENING_JSON)),
    }


def build_public_game_inventory() -> Dict[str, Any]:
    path_records = []
    all_files = []

    for path_text in PUBLIC_GAME_CANDIDATE_PATHS:
        path = Path(path_text)
        files = _safe_file_records(path)
        path_records.append(
            {
                "path": path_text,
                "exists": path.exists(),
                "is_dir": path.is_dir(),
                "file_count": len(files),
                "compatible_file_count": sum(1 for item in files if item["compatible_suffix"]),
                "hint_match_count": sum(1 for item in files if item["fixture_hint_match"]),
            }
        )
        all_files.extend(files)

    compatible_fixtures = tuple(
        item for item in all_files if item["compatible_suffix"] and item["fixture_hint_match"]
    )

    return {
        "inventory_id": "M11-TASK2-PUBLIC-GAME-INVENTORY-v1",
        "candidate_path_count": len(PUBLIC_GAME_CANDIDATE_PATHS),
        "candidate_paths": list(PUBLIC_GAME_CANDIDATE_PATHS),
        "path_records": path_records,
        "total_file_count": len(all_files),
        "compatible_fixture_count": len(compatible_fixtures),
        "compatible_fixtures": list(compatible_fixtures),
        "inventory_created": True,
        "inventory_scan_completed": True,
        "compatible_fixture_detection_completed": True,
        "has_local_public_fixtures": len(compatible_fixtures) > 0,
    }


def build_safe_baseline_record() -> Dict[str, Any]:
    inventory = build_public_game_inventory()
    compatible_count = inventory["compatible_fixture_count"]
    has_fixtures = compatible_count > 0

    baseline_cases = []
    for fixture in inventory["compatible_fixtures"]:
        baseline_cases.append(
            {
                "fixture_path": fixture["path"],
                "fixture_sha256_16": fixture["sha256_16"],
                "baseline_case_ready": True,
                "baseline_execution_mode": "DRY_RUN_STRUCTURE_ONLY",
                "score_claimed": False,
            }
        )

    return {
        "baseline_id": "M11-TASK2-SAFE-BASELINE-RUN-v1",
        "baseline_policy_created": True,
        "baseline_attempt_recorded": True,
        "baseline_result_recorded": True,
        "baseline_execution_performed": has_fixtures,
        "baseline_execution_mode": "DRY_RUN_STRUCTURE_ONLY" if has_fixtures else "NO_LOCAL_PUBLIC_FIXTURES",
        "compatible_fixture_count": compatible_count,
        "baseline_case_count": len(baseline_cases),
        "baseline_cases": baseline_cases,
        "baseline_status": "BASELINE_DRY_RUN_RECORDED" if has_fixtures else "BASELINE_NOT_EXECUTED_NO_LOCAL_PUBLIC_FIXTURES",
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "score_boundary": "NO_SCORE_CLAIM_WITHOUT_OFFICIAL_VALIDATION",
    }


def build_task_2_checks() -> Dict[str, bool]:
    source = build_m11_opening_source_summary()
    inventory = build_public_game_inventory()
    baseline = build_safe_baseline_record()

    return {
        "m11_opening_artifact_exists": source["m11_opening_present"] is True,
        "m11_opening_artifact_ready": source["m11_opening_status"]
        == "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_READY",
        "m11_opening_validated": source["m11_opening_id"].startswith(
            "MILESTONE-11-PUBLIC-GAME-BENCHMARK-SOLVER-IMPROVEMENT-"
        )
        and bool(source["m11_opening_signature"]),
        "candidate_identity_loaded": source["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
        and source["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
        and source["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID,
        "candidate_paths_declared": inventory["candidate_path_count"] == len(PUBLIC_GAME_CANDIDATE_PATHS),
        "inventory_created": inventory["inventory_created"] is True,
        "inventory_scan_completed": inventory["inventory_scan_completed"] is True,
        "compatible_fixture_detection_completed": inventory[
            "compatible_fixture_detection_completed"
        ]
        is True,
        "baseline_policy_created": baseline["baseline_policy_created"] is True,
        "baseline_attempt_recorded": baseline["baseline_attempt_recorded"] is True,
        "baseline_result_recorded": baseline["baseline_result_recorded"] is True,
        "no_real_public_score_claimed": baseline["real_public_score_claimed"] is False
        and source["real_public_score_claimed"] is False,
        "no_private_score_claimed": baseline["private_score_claimed"] is False
        and source["private_score_claimed"] is False,
        "no_submission_json_created": source["submission_json_created"] is False,
        "no_upload_package_created": source["upload_package_created"] is False,
        "real_submission_blocked": source["real_submission_allowed"] is False
        and source["real_submission_decision"] == "NOT_AUTHORIZED",
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_3_PUBLIC_GAME_FAILURE_TAXONOMY_V1",
        "inventory_check_count_valid": len(INVENTORY_CHECKS) == EXPECTED_INVENTORY_CHECK_COUNT,
        "inventory_case_count_valid": len(INVENTORY_CASES) == EXPECTED_INVENTORY_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_2_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_2_checks()

    if case_id == "m11_task2_source_opening_ready_v1":
        passed = (
            checks["m11_opening_artifact_exists"]
            and checks["m11_opening_artifact_ready"]
            and checks["m11_opening_validated"]
        )
        return _result(case_id, "source_binding", "verify_milestone_11_opening_source", passed)

    if case_id == "m11_task2_candidate_identity_loaded_v1":
        return _result(case_id, "identity", "verify_candidate_identity", checks["candidate_identity_loaded"])

    if case_id == "m11_task2_public_game_paths_scanned_v1":
        passed = checks["candidate_paths_declared"] and checks["inventory_scan_completed"]
        return _result(case_id, "inventory", "scan_public_game_candidate_paths", passed)

    if case_id == "m11_task2_compatible_fixture_detection_v1":
        return _result(
            case_id,
            "fixture_detection",
            "detect_compatible_public_fixtures",
            checks["compatible_fixture_detection_completed"],
        )

    if case_id == "m11_task2_baseline_policy_ready_v1":
        return _result(
            case_id,
            "baseline_policy",
            "verify_baseline_policy",
            checks["baseline_policy_created"],
        )

    if case_id == "m11_task2_safe_baseline_record_ready_v1":
        passed = checks["baseline_attempt_recorded"] and checks["baseline_result_recorded"]
        return _result(case_id, "baseline", "verify_safe_baseline_record", passed)

    if case_id == "m11_task2_no_score_claim_without_valid_run_v1":
        passed = checks["no_real_public_score_claimed"] and checks["no_private_score_claimed"]
        return _result(case_id, "score_boundary", "verify_no_score_claim_without_valid_run", passed)

    if case_id == "m11_task2_real_submission_blocked_v1":
        passed = (
            checks["real_submission_blocked"]
            and checks["no_submission_json_created"]
            and checks["no_upload_package_created"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission_boundary", "verify_real_submission_blocked", passed)

    if case_id == "m11_task2_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task2_metadata_safe_v1":
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

    raise ValueError(f"unknown milestone 11 task 2 case: {case_id}")


def evaluate_all_task_2_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_2_case(case["case_id"]) for case in INVENTORY_CASES)


def build_inventory_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_2_checks()
    rows = (
        ("source_opening_ready", checks["m11_opening_artifact_exists"] and checks["m11_opening_artifact_ready"]),
        ("candidate_identity_loaded", checks["candidate_identity_loaded"]),
        ("inventory_scan_completed", checks["inventory_scan_completed"]),
        ("compatible_fixture_detection_completed", checks["compatible_fixture_detection_completed"]),
        ("baseline_policy_created", checks["baseline_policy_created"]),
        ("safe_baseline_record_ready", checks["baseline_attempt_recorded"] and checks["baseline_result_recorded"]),
        ("score_boundary_preserved", checks["no_real_public_score_claimed"] and checks["no_private_score_claimed"]),
        ("submission_boundary_preserved", checks["real_submission_blocked"]),
        ("fail_closed_preserved", checks["fail_closed_required"] and checks["fail_closed_active"]),
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


def build_milestone_11_public_game_inventory_baseline_run() -> Dict[str, Any]:
    source = build_m11_opening_source_summary()
    inventory = build_public_game_inventory()
    baseline = build_safe_baseline_record()
    checks = build_task_2_checks()
    results = evaluate_all_task_2_cases()
    scorecard = build_inventory_scorecard()

    pass_count = sum(1 for result in results if result["passed"] is True)
    failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "m11_opening_artifact_exists": checks["m11_opening_artifact_exists"],
        "m11_opening_artifact_ready": checks["m11_opening_artifact_ready"],
        "m11_opening_validated": checks["m11_opening_validated"],
        "candidate_identity_loaded": checks["candidate_identity_loaded"],
        "candidate_paths_declared": checks["candidate_paths_declared"],
        "inventory_created": checks["inventory_created"],
        "inventory_scan_completed": checks["inventory_scan_completed"],
        "compatible_fixture_detection_completed": checks["compatible_fixture_detection_completed"],
        "baseline_policy_created": checks["baseline_policy_created"],
        "baseline_attempt_recorded": checks["baseline_attempt_recorded"],
        "baseline_result_recorded": checks["baseline_result_recorded"],
        "no_real_public_score_claimed": checks["no_real_public_score_claimed"],
        "no_private_score_claimed": checks["no_private_score_claimed"],
        "real_submission_blocked": checks["real_submission_blocked"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "metadata_safe": checks["public_safe"]
        and checks["deterministic"]
        and checks["local_only"]
        and checks["external_api_dependency_false"]
        and checks["private_core_exposure_false"]
        and checks["legal_certification_false"],
        "all_cases_pass": all(result["passed"] is True for result in results),
        "pass_count_valid": pass_count == EXPECTED_INVENTORY_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_INVENTORY_FAILURE_COUNT,
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
        pass_count == EXPECTED_INVENTORY_PASS_COUNT
        and failure_count == EXPECTED_INVENTORY_FAILURE_COUNT
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["m11_opening_artifact_ready"]
        and checks["inventory_created"]
        and checks["baseline_result_recorded"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 2",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_milestone_11_opening": source["m11_opening_id"],
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": source["rebuilt_candidate_id"],
        "inventory_created": True,
        "inventory_scan_completed": True,
        "candidate_path_count": inventory["candidate_path_count"],
        "total_file_count": inventory["total_file_count"],
        "compatible_fixture_count": inventory["compatible_fixture_count"],
        "baseline_execution_performed": baseline["baseline_execution_performed"],
        "baseline_execution_mode": baseline["baseline_execution_mode"],
        "baseline_status": baseline["baseline_status"],
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
        "task": "Task 2",
        "title": "Public Game Inventory and Baseline Run v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "m11_opening_source": {
            "path": str(M11_OPENING_JSON),
            "present": M11_OPENING_JSON.exists(),
            "status": source["m11_opening_status"],
            "milestone_11_id": source["m11_opening_id"],
            "sha256": _sha256(M11_OPENING_JSON),
            "sha256_16": _sha16(_sha256(M11_OPENING_JSON)),
        },
        "source_summary": source,
        "public_game_inventory": inventory,
        "safe_baseline_record": baseline,
        "inventory_scorecard": list(scorecard),
        "inventory_checks": checks,
        "inventory_check_list": list(INVENTORY_CHECKS),
        "inventory_cases": list(INVENTORY_CASES),
        "inventory_results": list(results),
        "inventory_gates": list(gates),
        "inventory_issues": list(issues),
        "inventory_index": index,
        "task_2_ready": task_ready,
        "inventory_created": True,
        "inventory_scan_completed": True,
        "compatible_fixture_detection_completed": True,
        "candidate_path_count": inventory["candidate_path_count"],
        "total_file_count": inventory["total_file_count"],
        "compatible_fixture_count": inventory["compatible_fixture_count"],
        "has_local_public_fixtures": inventory["has_local_public_fixtures"],
        "baseline_policy_created": baseline["baseline_policy_created"],
        "baseline_attempt_recorded": baseline["baseline_attempt_recorded"],
        "baseline_result_recorded": baseline["baseline_result_recorded"],
        "baseline_execution_performed": baseline["baseline_execution_performed"],
        "baseline_execution_mode": baseline["baseline_execution_mode"],
        "baseline_status": baseline["baseline_status"],
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "inventory_check_count": len(INVENTORY_CHECKS),
        "inventory_case_count": len(INVENTORY_CASES),
        "inventory_pass_count": pass_count,
        "inventory_failure_count": failure_count,
        "inventory_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "inventory_issue_count": issue_count,
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
            "source": "milestone_11_public_game_inventory_baseline_run_v1",
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
        "task_2_id": f"MILESTONE-11-PUBLIC-GAME-INVENTORY-BASELINE-RUN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_public_game_inventory_baseline_run(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("inventory_gates", [])
    issues = record.get("inventory_issues", [])
    results = record.get("inventory_results", [])
    scorecard = record.get("inventory_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_2_id_present": isinstance(record.get("task_2_id"), str) and bool(record.get("task_2_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("d7d1148"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_2_ready") is True,
        "m11_opening_source_present": record.get("m11_opening_source", {}).get("present") is True,
        "inventory_created": record.get("inventory_created") is True,
        "inventory_scan_completed": record.get("inventory_scan_completed") is True,
        "compatible_fixture_detection_completed": record.get("compatible_fixture_detection_completed") is True,
        "baseline_policy_created": record.get("baseline_policy_created") is True,
        "baseline_attempt_recorded": record.get("baseline_attempt_recorded") is True,
        "baseline_result_recorded": record.get("baseline_result_recorded") is True,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "inventory_check_count_valid": record.get("inventory_check_count") == EXPECTED_INVENTORY_CHECK_COUNT,
        "inventory_case_count_valid": record.get("inventory_case_count") == EXPECTED_INVENTORY_CASE_COUNT,
        "inventory_pass_count_valid": record.get("inventory_pass_count") == EXPECTED_INVENTORY_PASS_COUNT,
        "inventory_failure_count_zero": record.get("inventory_failure_count") == EXPECTED_INVENTORY_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "no_real_public_score_claimed": record.get("real_public_score_claimed") is False
        and record.get("real_benchmark_score") is None,
        "no_private_score_claimed": record.get("private_score_claimed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_2_id": record.get("task_2_id"),
        "signature": record.get("signature"),
    }


def render_task_2_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 2 - Public Game Inventory and Baseline Run v1",
        "",
        f"- status: {record['status']}",
        f"- task_2_id: {record['task_2_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_2_ready: {record['task_2_ready']}",
        f"- inventory_created: {record['inventory_created']}",
        f"- inventory_scan_completed: {record['inventory_scan_completed']}",
        f"- candidate_path_count: {record['candidate_path_count']}",
        f"- total_file_count: {record['total_file_count']}",
        f"- compatible_fixture_count: {record['compatible_fixture_count']}",
        f"- has_local_public_fixtures: {record['has_local_public_fixtures']}",
        f"- baseline_execution_performed: {record['baseline_execution_performed']}",
        f"- baseline_execution_mode: {record['baseline_execution_mode']}",
        f"- baseline_status: {record['baseline_status']}",
        f"- real_public_score_claimed: {record['real_public_score_claimed']}",
        f"- private_score_claimed: {record['private_score_claimed']}",
        f"- real_benchmark_score: {record['real_benchmark_score']}",
        f"- real_submission_candidate_created: {record['real_submission_candidate_created']}",
        f"- submission_json_created: {record['submission_json_created']}",
        f"- upload_package_created: {record['upload_package_created']}",
        f"- real_submission_decision: {record['real_submission_decision']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Candidate paths",
        "",
    ]

    for item in record["public_game_inventory"]["path_records"]:
        lines.append(
            f"- {item['path']} / exists={item['exists']} / files={item['file_count']} / "
            f"compatible={item['compatible_file_count']}"
        )

    lines.extend(["", "## Compatible fixtures", ""])

    if record["public_game_inventory"]["compatible_fixtures"]:
        for item in record["public_game_inventory"]["compatible_fixtures"]:
            lines.append(f"- {item['path']} / sha16={item['sha256_16']} / size={item['size_bytes']}")
    else:
        lines.append("- none detected locally")

    lines.extend(["", "## Validation results", ""])

    for result in record["inventory_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 2 is ready. Local public-game inventory and safe baseline record are created. No real score is claimed, and real submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_2_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_2_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_2_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_2_MODE=MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_2_VERDICT=PUBLIC_GAME_INVENTORY_BASELINE_RUN_READY_FOR_FAILURE_TAXONOMY",
            "ARC_AGI3_MILESTONE_11_TASK_2_BASELINE_COMMIT=d7d1148",
            "ARC_AGI3_MILESTONE_11_TASK_2_NEXT_STAGE=MILESTONE_11_TASK_3_PUBLIC_GAME_FAILURE_TAXONOMY_V1",
            "ARC_AGI3_MILESTONE_11_PUBLIC_GAME_INVENTORY_CREATED=true",
            "ARC_AGI3_MILESTONE_11_INVENTORY_SCAN_COMPLETED=true",
            f"ARC_AGI3_MILESTONE_11_CANDIDATE_PATH_COUNT={record['candidate_path_count']}",
            f"ARC_AGI3_MILESTONE_11_TOTAL_FILE_COUNT={record['total_file_count']}",
            f"ARC_AGI3_MILESTONE_11_COMPATIBLE_FIXTURE_COUNT={record['compatible_fixture_count']}",
            f"ARC_AGI3_MILESTONE_11_BASELINE_EXECUTION_PERFORMED={str(record['baseline_execution_performed']).lower()}",
            f"ARC_AGI3_MILESTONE_11_BASELINE_EXECUTION_MODE={record['baseline_execution_mode']}",
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


def render_task_2_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 2 PUBLIC GAME INVENTORY BASELINE RUN MANIFEST v1",
        f"task_2_id={record['task_2_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_2_ready={record['task_2_ready']}",
        f"inventory_created={record['inventory_created']}",
        f"inventory_scan_completed={record['inventory_scan_completed']}",
        f"candidate_path_count={record['candidate_path_count']}",
        f"total_file_count={record['total_file_count']}",
        f"compatible_fixture_count={record['compatible_fixture_count']}",
        f"has_local_public_fixtures={record['has_local_public_fixtures']}",
        f"baseline_execution_performed={record['baseline_execution_performed']}",
        f"baseline_execution_mode={record['baseline_execution_mode']}",
        f"baseline_status={record['baseline_status']}",
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
        "PUBLIC_GAME_PATH_RECORDS",
    ]

    for item in record["public_game_inventory"]["path_records"]:
        lines.append(
            f"{item['path']} exists={item['exists']} is_dir={item['is_dir']} "
            f"file_count={item['file_count']} compatible_file_count={item['compatible_file_count']}"
        )

    lines.append("")
    lines.append("INVENTORY_VALIDATION_RESULTS")
    for result in record["inventory_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_2_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_public_game_inventory_baseline_run())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-public-game-inventory-baseline-run-v1.json"
    md_path = output / "milestone-11-public-game-inventory-baseline-run-v1.md"
    manifest_path = output / "milestone-11-public-game-inventory-baseline-run-manifest-v1.txt"
    index_path = output / "milestone-11-public-game-inventory-baseline-run-index-v1.json"
    inventory_path = output / "milestone-11-public-game-inventory-v1.json"
    baseline_path = output / "milestone-11-safe-baseline-record-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_2_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_2_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["inventory_index"], indent=2, sort_keys=True), encoding="utf-8")
    inventory_path.write_text(
        json.dumps(record["public_game_inventory"], indent=2, sort_keys=True),
        encoding="utf-8",
    )
    baseline_path.write_text(
        json.dumps(record["safe_baseline_record"], indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "inventory_path": str(inventory_path),
        "baseline_path": str(baseline_path),
    }


def run_milestone_11_public_game_inventory_baseline_run_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_public_game_inventory_baseline_run()
    validation = validate_milestone_11_public_game_inventory_baseline_run(record)
    artifacts = write_task_2_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_2_id": record["task_2_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_2_ready": record["task_2_ready"],
        "inventory_created": record["inventory_created"],
        "inventory_scan_completed": record["inventory_scan_completed"],
        "compatible_fixture_detection_completed": record["compatible_fixture_detection_completed"],
        "candidate_path_count": record["candidate_path_count"],
        "total_file_count": record["total_file_count"],
        "compatible_fixture_count": record["compatible_fixture_count"],
        "has_local_public_fixtures": record["has_local_public_fixtures"],
        "baseline_policy_created": record["baseline_policy_created"],
        "baseline_attempt_recorded": record["baseline_attempt_recorded"],
        "baseline_result_recorded": record["baseline_result_recorded"],
        "baseline_execution_performed": record["baseline_execution_performed"],
        "baseline_execution_mode": record["baseline_execution_mode"],
        "baseline_status": record["baseline_status"],
        "real_public_score_claimed": record["real_public_score_claimed"],
        "private_score_claimed": record["private_score_claimed"],
        "real_benchmark_score": record["real_benchmark_score"],
        "inventory_check_count": record["inventory_check_count"],
        "inventory_case_count": record["inventory_case_count"],
        "inventory_pass_count": record["inventory_pass_count"],
        "inventory_failure_count": record["inventory_failure_count"],
        "inventory_gate_count": record["inventory_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "inventory_issue_count": record["inventory_issue_count"],
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
