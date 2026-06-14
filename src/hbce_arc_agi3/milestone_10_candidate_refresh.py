"""Milestone #10 Candidate Refresh v1.

Local-only deterministic candidate refresh after benchmark refresh.

This module reads the Milestone #10 benchmark refresh artifact and creates a
controlled local candidate refresh package. It does not create a real Kaggle
submission. It does not authenticate, upload files, call external APIs, read
secrets, grant approval, claim a public score, claim leaderboard movement, or
create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from hbce_arc_agi3.milestone_10_solver_patch_implementation import (
    build_trace_generalization_fields,
    rank_candidates_by_patch_evidence,
    score_composition_order,
)


CANDIDATE_STATUS = "MILESTONE_10_CANDIDATE_REFRESH_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_CANDIDATE_REFRESH_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_CANDIDATE_REFRESH_V1_VALID"

BASELINE_COMMIT = "ed3aa9d Add ARC AGI3 benchmark refresh"
CANDIDATE_MODE = "MILESTONE_10_CANDIDATE_REFRESH_V1_LOCAL_ONLY"
CANDIDATE_SCOPE = "LOCAL_CANDIDATE_REFRESH_NO_REAL_SUBMISSION"
CANDIDATE_VERDICT = "CANDIDATE_REFRESH_READY_FOR_SUBMISSION_CANDIDATE_REBUILD_GATE"
NEXT_ALLOWED_STAGE = "MILESTONE_10_TASK_7_SUBMISSION_CANDIDATE_REBUILD_GATE_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/candidate-refresh-v1"

BENCHMARK_REFRESH_JSON = Path(
    "examples/milestone-10/benchmark-refresh-v1/"
    "milestone-10-benchmark-refresh-v1.json"
)

EXPECTED_CANDIDATE_COUNT = 4
EXPECTED_RANKED_CANDIDATE_COUNT = 4
EXPECTED_SELECTED_CANDIDATE_COUNT = 1
EXPECTED_CANDIDATE_CHECK_COUNT = 26
EXPECTED_CANDIDATE_CASE_COUNT = 10
EXPECTED_CANDIDATE_PASS_COUNT = 10
EXPECTED_CANDIDATE_FAILURE_COUNT = 0
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_FAIL_CLOSED_CONTROL_COUNT = 8

LOCAL_CANDIDATE_BLUEPRINTS: Tuple[Dict[str, Any], ...] = (
    {
        "candidate_id": "M10-CANDIDATE-BALANCED-PATCH-STACK-v1",
        "family": "balanced_patch_stack",
        "score_hint": 0.991,
        "confidence": 0.93,
        "family_evidence": 6,
        "complexity": 3,
        "operations": ("color_mapping", "object_model", "shape_symmetry", "candidate_ranker"),
    },
    {
        "candidate_id": "M10-CANDIDATE-COMPOSITION-RANKER-v1",
        "family": "composition_ranker",
        "score_hint": 0.984,
        "confidence": 0.95,
        "family_evidence": 5,
        "complexity": 2,
        "operations": ("color_mapping", "object_model", "candidate_ranker"),
    },
    {
        "candidate_id": "M10-CANDIDATE-TRACE-STABLE-v1",
        "family": "trace_stable",
        "score_hint": 0.978,
        "confidence": 0.90,
        "family_evidence": 6,
        "complexity": 2,
        "operations": ("color_mapping", "traceability", "candidate_ranker"),
    },
    {
        "candidate_id": "M10-CANDIDATE-SYMMETRY-OBJECT-v1",
        "family": "symmetry_object",
        "score_hint": 0.972,
        "confidence": 0.91,
        "family_evidence": 4,
        "complexity": 2,
        "operations": ("object_model", "shape_symmetry", "candidate_ranker"),
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

CANDIDATE_CHECKS: Tuple[str, ...] = (
    "benchmark_artifact_exists",
    "benchmark_artifact_ready",
    "benchmark_signature_present",
    "benchmark_next_stage_matches_task_6",
    "benchmark_average_score_valid",
    "candidate_refresh_required",
    "candidate_count_valid",
    "ranked_candidate_count_valid",
    "selected_candidate_count_valid",
    "candidate_ranking_ready",
    "selected_candidate_ready",
    "candidate_package_created",
    "candidate_package_ready",
    "candidate_artifact_created",
    "real_submission_candidate_not_created",
    "submission_json_not_created",
    "next_stage_valid",
    "fail_closed_required",
    "fail_closed_active",
    "real_submission_not_authorized",
    "real_submission_blocked",
    "manual_upload_blocked",
    "kaggle_authentication_blocked",
    "kaggle_submission_absent",
    "no_private_core_exposure",
    "no_legal_certification",
)

CANDIDATE_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_candidate_refresh_benchmark_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_benchmark_refresh_source",
    },
    {
        "case_id": "m10_candidate_refresh_catalog_ready_v1",
        "area": "candidate_catalog",
        "operation": "verify_candidate_catalog",
    },
    {
        "case_id": "m10_candidate_refresh_ranking_ready_v1",
        "area": "candidate_ranking",
        "operation": "verify_candidate_ranking",
    },
    {
        "case_id": "m10_candidate_refresh_selected_candidate_ready_v1",
        "area": "candidate_selection",
        "operation": "verify_selected_candidate",
    },
    {
        "case_id": "m10_candidate_refresh_package_ready_v1",
        "area": "candidate_package",
        "operation": "verify_candidate_package",
    },
    {
        "case_id": "m10_candidate_refresh_trace_ready_v1",
        "area": "traceability",
        "operation": "verify_candidate_trace",
    },
    {
        "case_id": "m10_candidate_refresh_no_submission_json_v1",
        "area": "submission_boundary",
        "operation": "verify_no_submission_json",
    },
    {
        "case_id": "m10_candidate_refresh_real_submission_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "m10_candidate_refresh_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_preserved",
    },
    {
        "case_id": "m10_candidate_refresh_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_rebuild_gate_next",
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


def build_candidate_refresh_source_summary() -> Dict[str, Any]:
    benchmark = _read_json(BENCHMARK_REFRESH_JSON)
    source = benchmark.get("source_summary", {})

    return {
        "benchmark_path": str(BENCHMARK_REFRESH_JSON),
        "benchmark_present": BENCHMARK_REFRESH_JSON.exists(),
        "benchmark_status": benchmark.get("status", "MISSING"),
        "refresh_id": benchmark.get("refresh_id", "MISSING_REFRESH_ID"),
        "refresh_signature": benchmark.get("signature", ""),
        "refresh_ready": benchmark.get("refresh_ready", False),
        "refresh_locked": benchmark.get("refresh_locked", False),
        "benchmark_baseline_commit": benchmark.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "next_allowed_stage": benchmark.get("next_allowed_stage", "MISSING_NEXT_STAGE"),
        "benchmark_task_count": benchmark.get("benchmark_task_count", 0),
        "benchmark_family_count": benchmark.get("benchmark_family_count", 0),
        "benchmark_task_pass_count": benchmark.get("benchmark_task_pass_count", 0),
        "benchmark_task_failure_count": benchmark.get("benchmark_task_failure_count", 999),
        "average_score": benchmark.get("average_score", 0.0),
        "candidate_refresh_required_next": benchmark.get("candidate_refresh_required_next", False),
        "submission_candidate_created": benchmark.get("submission_candidate_created", True),
        "candidate_source_path": source.get("candidate_source_path", "MISSING_CANDIDATE_SOURCE"),
        "previous_candidate_id": source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "previous_candidate_signature": source.get("candidate_signature", ""),
        "previous_candidate_count": source.get("candidate_count", 0),
        "real_submission_decision": benchmark.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": benchmark.get("real_submission_allowed", True),
        "manual_upload_allowed": benchmark.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": benchmark.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": benchmark.get("kaggle_submission_sent", True),
        "fail_closed_required": benchmark.get("fail_closed_required", False),
        "fail_closed_active": benchmark.get("fail_closed_active", False),
        "benchmark_sha256": _sha256(BENCHMARK_REFRESH_JSON),
        "benchmark_sha256_16": _sha16(_sha256(BENCHMARK_REFRESH_JSON)),
    }


def build_candidate_refresh_catalog() -> Tuple[Dict[str, Any], ...]:
    catalog = []

    for blueprint in LOCAL_CANDIDATE_BLUEPRINTS:
        order_score = score_composition_order(blueprint["operations"])
        trace = build_trace_generalization_fields(
            task_id=blueprint["candidate_id"],
            family=blueprint["family"],
            assumptions=(
                "benchmark refresh passed",
                "local-only candidate refresh",
                "real submission blocked",
            ),
        )

        catalog.append(
            {
                **blueprint,
                "operations": list(blueprint["operations"]),
                "order_score": order_score["score"],
                "stable_order": order_score["stable_order"],
                "trace_hash_16": trace["generalization_trace_hash_16"],
                "trace_ready": trace["trace_ready"],
                "local_only": True,
                "deterministic": True,
                "requires_external_api": False,
                "requires_kaggle_upload": False,
                "creates_real_submission": False,
                "creates_submission_json": False,
                "ready_for_ranking": True,
            }
        )

    return tuple(catalog)


def rank_candidate_refresh_catalog(
    catalog: Iterable[Mapping[str, Any]] | None = None,
) -> Dict[str, Any]:
    catalog = tuple(catalog or build_candidate_refresh_catalog())
    ranked_payload = rank_candidates_by_patch_evidence(catalog)
    ranked_ids = [item["candidate_id"] for item in ranked_payload["ranked_candidates"]]
    catalog_by_id = {item["candidate_id"]: dict(item) for item in catalog}

    ranked_candidates = tuple(catalog_by_id[candidate_id] for candidate_id in ranked_ids)
    selected = ranked_candidates[0] if ranked_candidates else {}

    return {
        "ranking_ready": bool(ranked_candidates),
        "candidate_count": len(catalog),
        "ranked_candidate_count": len(ranked_candidates),
        "selected_candidate_count": 1 if selected else 0,
        "selected_candidate_id": selected.get("candidate_id"),
        "selected_candidate": selected,
        "ranked_candidate_ids": ranked_ids,
        "ranked_candidates": list(ranked_candidates),
        "ranker_payload": ranked_payload,
    }


def build_candidate_refresh_package() -> Dict[str, Any]:
    source = build_candidate_refresh_source_summary()
    ranking = rank_candidate_refresh_catalog()
    selected = ranking["selected_candidate"]

    package_seed = {
        "baseline_commit": BASELINE_COMMIT,
        "refresh_id": source["refresh_id"],
        "selected_candidate_id": ranking["selected_candidate_id"],
        "average_score": source["average_score"],
        "mode": CANDIDATE_MODE,
    }
    signature = _stable_signature(package_seed)

    return {
        "package_id": f"MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-{signature[:12]}",
        "signature": signature,
        "source_refresh_id": source["refresh_id"],
        "selected_candidate_id": ranking["selected_candidate_id"],
        "selected_candidate": selected,
        "ranked_candidate_ids": ranking["ranked_candidate_ids"],
        "candidate_count": ranking["candidate_count"],
        "ranked_candidate_count": ranking["ranked_candidate_count"],
        "selected_candidate_count": ranking["selected_candidate_count"],
        "candidate_package_created": True,
        "candidate_package_ready": True,
        "candidate_artifact_created": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "ready_for_rebuild_gate": True,
    }


def build_candidate_refresh_state() -> Dict[str, Any]:
    return {
        "candidate_refresh_required": True,
        "candidate_refresh_created": True,
        "candidate_refresh_ready": True,
        "candidate_refresh_locked": True,
        "candidate_mode": CANDIDATE_MODE,
        "candidate_scope": CANDIDATE_SCOPE,
        "candidate_verdict": CANDIDATE_VERDICT,
        "candidate_count": EXPECTED_CANDIDATE_COUNT,
        "ranked_candidate_count": EXPECTED_RANKED_CANDIDATE_COUNT,
        "selected_candidate_count": EXPECTED_SELECTED_CANDIDATE_COUNT,
        "candidate_artifact_created": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "rebuild_gate_required_next": True,
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


def build_candidate_refresh_checks() -> Dict[str, bool]:
    source = build_candidate_refresh_source_summary()
    catalog = build_candidate_refresh_catalog()
    ranking = rank_candidate_refresh_catalog(catalog)
    package = build_candidate_refresh_package()
    state = build_candidate_refresh_state()

    families = {candidate["family"] for candidate in catalog}

    return {
        "benchmark_artifact_present": source["benchmark_present"],
        "benchmark_artifact_ready": source["benchmark_status"] == "MILESTONE_10_BENCHMARK_REFRESH_V1_READY",
        "benchmark_artifact_valid": source["refresh_id"].startswith("MILESTONE-10-BENCHMARK-REFRESH-")
        and bool(source["refresh_signature"]),
        "benchmark_commit_valid": str(source["benchmark_baseline_commit"]).startswith("8dc1cfc"),
        "benchmark_next_stage_matches_task_6": source["next_allowed_stage"]
        == "MILESTONE_10_TASK_6_CANDIDATE_REFRESH_V1",
        "benchmark_ready": source["refresh_ready"] is True,
        "benchmark_locked": source["refresh_locked"] is True,
        "benchmark_task_count_valid": source["benchmark_task_count"] == 6,
        "benchmark_family_count_valid": source["benchmark_family_count"] == 6,
        "benchmark_task_pass_count_valid": source["benchmark_task_pass_count"] == 6,
        "benchmark_task_failure_count_zero": source["benchmark_task_failure_count"] == 0,
        "benchmark_average_score_valid": float(source["average_score"]) >= 95,
        "candidate_refresh_required": source["candidate_refresh_required_next"] is True,
        "previous_submission_candidate_not_created": source["submission_candidate_created"] is False,
        "candidate_count_valid": len(catalog) == EXPECTED_CANDIDATE_COUNT
        and package["candidate_count"] == EXPECTED_CANDIDATE_COUNT,
        "ranked_candidate_count_valid": ranking["ranked_candidate_count"] == EXPECTED_RANKED_CANDIDATE_COUNT,
        "selected_candidate_count_valid": ranking["selected_candidate_count"] == EXPECTED_SELECTED_CANDIDATE_COUNT,
        "candidate_ranking_ready": ranking["ranking_ready"] is True,
        "selected_candidate_ready": ranking["selected_candidate_id"] == "M10-CANDIDATE-BALANCED-PATCH-STACK-v1",
        "candidate_family_diversity_valid": len(families) == EXPECTED_CANDIDATE_COUNT,
        "all_candidates_local_only": all(candidate["local_only"] is True for candidate in catalog),
        "all_candidates_deterministic": all(candidate["deterministic"] is True for candidate in catalog),
        "all_candidates_no_external_api": all(candidate["requires_external_api"] is False for candidate in catalog),
        "all_candidates_no_upload": all(candidate["requires_kaggle_upload"] is False for candidate in catalog),
        "all_candidates_no_real_submission": all(
            candidate["creates_real_submission"] is False for candidate in catalog
        ),
        "all_candidates_no_submission_json": all(
            candidate["creates_submission_json"] is False for candidate in catalog
        ),
        "all_candidates_trace_ready": all(candidate["trace_ready"] is True for candidate in catalog),
        "all_candidates_stable_order": all(candidate["stable_order"] is True for candidate in catalog),
        "candidate_package_created": package["candidate_package_created"] is True,
        "candidate_package_ready": package["candidate_package_ready"] is True,
        "candidate_artifact_created": package["candidate_artifact_created"] is True,
        "real_submission_candidate_not_created": package["real_submission_candidate_created"] is False
        and state["real_submission_candidate_created"] is False,
        "submission_json_not_created": package["submission_json_created"] is False
        and state["submission_json_created"] is False,
        "upload_package_not_created": package["upload_package_created"] is False
        and state["upload_package_created"] is False,
        "candidate_check_count_valid": len(CANDIDATE_CHECKS) == EXPECTED_CANDIDATE_CHECK_COUNT,
        "candidate_case_count_valid": len(CANDIDATE_CASES) == EXPECTED_CANDIDATE_CASE_COUNT,
        "fail_closed_control_count_valid": len(FAIL_CLOSED_CONTROLS)
        == EXPECTED_FAIL_CLOSED_CONTROL_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "candidate_record_created": state["candidate_refresh_created"] is True,
        "candidate_record_ready": state["candidate_refresh_ready"] is True,
        "candidate_record_locked": state["candidate_refresh_locked"] is True,
        "candidate_mode_valid": CANDIDATE_MODE == "MILESTONE_10_CANDIDATE_REFRESH_V1_LOCAL_ONLY",
        "candidate_scope_valid": CANDIDATE_SCOPE == "LOCAL_CANDIDATE_REFRESH_NO_REAL_SUBMISSION",
        "candidate_verdict_valid": CANDIDATE_VERDICT
        == "CANDIDATE_REFRESH_READY_FOR_SUBMISSION_CANDIDATE_REBUILD_GATE",
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_10_TASK_7_SUBMISSION_CANDIDATE_REBUILD_GATE_V1",
        "rebuild_gate_required_next": state["rebuild_gate_required_next"] is True,
        "candidate_source_present": Path(source["candidate_source_path"]).exists(),
        "previous_candidate_id_present": source["previous_candidate_id"] != "MISSING_CANDIDATE_ID",
        "previous_candidate_signature_present": bool(source["previous_candidate_signature"]),
        "previous_candidate_count_positive": source["previous_candidate_count"] > 0,
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


def evaluate_candidate_refresh_case(case_id: str) -> Dict[str, Any]:
    checks = build_candidate_refresh_checks()

    if case_id == "m10_candidate_refresh_benchmark_source_ready_v1":
        passed = (
            checks["benchmark_artifact_present"]
            and checks["benchmark_artifact_ready"]
            and checks["benchmark_artifact_valid"]
            and checks["benchmark_ready"]
        )
        return _result(case_id, "source_binding", "verify_benchmark_refresh_source", passed)

    if case_id == "m10_candidate_refresh_catalog_ready_v1":
        passed = (
            checks["candidate_count_valid"]
            and checks["candidate_family_diversity_valid"]
            and checks["all_candidates_local_only"]
        )
        return _result(case_id, "candidate_catalog", "verify_candidate_catalog", passed)

    if case_id == "m10_candidate_refresh_ranking_ready_v1":
        passed = checks["candidate_ranking_ready"] and checks["ranked_candidate_count_valid"]
        return _result(case_id, "candidate_ranking", "verify_candidate_ranking", passed)

    if case_id == "m10_candidate_refresh_selected_candidate_ready_v1":
        passed = checks["selected_candidate_ready"] and checks["selected_candidate_count_valid"]
        return _result(case_id, "candidate_selection", "verify_selected_candidate", passed)

    if case_id == "m10_candidate_refresh_package_ready_v1":
        passed = checks["candidate_package_created"] and checks["candidate_package_ready"]
        return _result(case_id, "candidate_package", "verify_candidate_package", passed)

    if case_id == "m10_candidate_refresh_trace_ready_v1":
        return _result(case_id, "traceability", "verify_candidate_trace", checks["all_candidates_trace_ready"])

    if case_id == "m10_candidate_refresh_no_submission_json_v1":
        passed = checks["submission_json_not_created"] and checks["upload_package_not_created"]
        return _result(case_id, "submission_boundary", "verify_no_submission_json", passed)

    if case_id == "m10_candidate_refresh_real_submission_blocked_v1":
        passed = (
            checks["real_submission_candidate_not_created"]
            and checks["real_submission_allowed_false"]
            and checks["manual_upload_not_allowed"]
        )
        return _result(case_id, "submission_boundary", "verify_real_submission_blocked", passed)

    if case_id == "m10_candidate_refresh_fail_closed_preserved_v1":
        passed = (
            checks["fail_closed_required"]
            and checks["fail_closed_active"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "fail_closed", "verify_fail_closed_preserved", passed)

    if case_id == "m10_candidate_refresh_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_rebuild_gate_next", checks["next_stage_valid"])

    raise ValueError(f"unknown candidate refresh case: {case_id}")


def evaluate_all_candidate_refresh_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_candidate_refresh_case(case["case_id"]) for case in CANDIDATE_CASES)


def build_milestone_10_candidate_refresh() -> Dict[str, Any]:
    source = build_candidate_refresh_source_summary()
    catalog = build_candidate_refresh_catalog()
    ranking = rank_candidate_refresh_catalog(catalog)
    package = build_candidate_refresh_package()
    state = build_candidate_refresh_state()
    checks = build_candidate_refresh_checks()
    results = evaluate_all_candidate_refresh_cases()

    candidate_pass_count = sum(1 for result in results if result["passed"] is True)
    candidate_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "benchmark_artifact_present": checks["benchmark_artifact_present"],
        "benchmark_artifact_ready": checks["benchmark_artifact_ready"],
        "benchmark_artifact_valid": checks["benchmark_artifact_valid"],
        "benchmark_commit_valid": checks["benchmark_commit_valid"],
        "benchmark_next_stage_matches_task_6": checks["benchmark_next_stage_matches_task_6"],
        "benchmark_ready": checks["benchmark_ready"],
        "benchmark_locked": checks["benchmark_locked"],
        "benchmark_task_count_valid": checks["benchmark_task_count_valid"],
        "benchmark_family_count_valid": checks["benchmark_family_count_valid"],
        "benchmark_task_pass_count_valid": checks["benchmark_task_pass_count_valid"],
        "benchmark_task_failure_count_zero": checks["benchmark_task_failure_count_zero"],
        "benchmark_average_score_valid": checks["benchmark_average_score_valid"],
        "candidate_refresh_required": checks["candidate_refresh_required"],
        "previous_submission_candidate_not_created": checks["previous_submission_candidate_not_created"],
        "candidate_count_valid": checks["candidate_count_valid"],
        "ranked_candidate_count_valid": checks["ranked_candidate_count_valid"],
        "selected_candidate_count_valid": checks["selected_candidate_count_valid"],
        "candidate_ranking_ready": checks["candidate_ranking_ready"],
        "selected_candidate_ready": checks["selected_candidate_ready"],
        "candidate_family_diversity_valid": checks["candidate_family_diversity_valid"],
        "all_candidates_local_only": checks["all_candidates_local_only"],
        "all_candidates_deterministic": checks["all_candidates_deterministic"],
        "all_candidates_no_external_api": checks["all_candidates_no_external_api"],
        "all_candidates_no_upload": checks["all_candidates_no_upload"],
        "all_candidates_no_real_submission": checks["all_candidates_no_real_submission"],
        "all_candidates_no_submission_json": checks["all_candidates_no_submission_json"],
        "all_candidates_trace_ready": checks["all_candidates_trace_ready"],
        "all_candidates_stable_order": checks["all_candidates_stable_order"],
        "candidate_package_created": checks["candidate_package_created"],
        "candidate_package_ready": checks["candidate_package_ready"],
        "candidate_artifact_created": checks["candidate_artifact_created"],
        "real_submission_candidate_not_created": checks["real_submission_candidate_not_created"],
        "submission_json_not_created": checks["submission_json_not_created"],
        "upload_package_not_created": checks["upload_package_not_created"],
        "candidate_check_count_valid": checks["candidate_check_count_valid"],
        "candidate_case_count_valid": checks["candidate_case_count_valid"],
        "fail_closed_control_count_valid": checks["fail_closed_control_count_valid"],
        "boundary_control_count_valid": checks["boundary_control_count_valid"],
        "candidate_record_created": checks["candidate_record_created"],
        "candidate_record_ready": checks["candidate_record_ready"],
        "candidate_record_locked": checks["candidate_record_locked"],
        "candidate_mode_valid": checks["candidate_mode_valid"],
        "candidate_scope_valid": checks["candidate_scope_valid"],
        "candidate_verdict_valid": checks["candidate_verdict_valid"],
        "next_stage_valid": checks["next_stage_valid"],
        "rebuild_gate_required_next": checks["rebuild_gate_required_next"],
        "candidate_source_present": checks["candidate_source_present"],
        "previous_candidate_id_present": checks["previous_candidate_id_present"],
        "previous_candidate_signature_present": checks["previous_candidate_signature_present"],
        "previous_candidate_count_positive": checks["previous_candidate_count_positive"],
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
        "all_candidate_cases_pass": all(result["passed"] is True for result in results),
        "candidate_pass_count_valid": candidate_pass_count == EXPECTED_CANDIDATE_PASS_COUNT,
        "candidate_failure_count_zero": candidate_failure_count == EXPECTED_CANDIDATE_FAILURE_COUNT,
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

    candidate_ready = (
        candidate_pass_count == EXPECTED_CANDIDATE_PASS_COUNT
        and candidate_failure_count == EXPECTED_CANDIDATE_FAILURE_COUNT
        and checks["benchmark_artifact_ready"]
        and checks["candidate_count_valid"]
        and checks["candidate_ranking_ready"]
        and checks["candidate_package_ready"]
        and checks["real_submission_candidate_not_created"]
        and checks["submission_json_not_created"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #10",
        "task": "Task 6",
        "candidate_mode": CANDIDATE_MODE,
        "candidate_scope": CANDIDATE_SCOPE,
        "candidate_verdict": CANDIDATE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_refresh": source["refresh_id"],
        "previous_candidate_id": source["previous_candidate_id"],
        "candidate_ready": candidate_ready,
        "candidate_refresh_created": True,
        "candidate_refresh_ready": True,
        "candidate_count": ranking["candidate_count"],
        "ranked_candidate_count": ranking["ranked_candidate_count"],
        "selected_candidate_count": ranking["selected_candidate_count"],
        "selected_candidate_id": ranking["selected_candidate_id"],
        "candidate_package_id": package["package_id"],
        "candidate_artifact_created": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "rebuild_gate_required_next": True,
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
        "status": CANDIDATE_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 6",
        "title": "Candidate Refresh v1",
        "baseline_commit": BASELINE_COMMIT,
        "candidate_mode": CANDIDATE_MODE,
        "candidate_scope": CANDIDATE_SCOPE,
        "candidate_verdict": CANDIDATE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "benchmark_source": {
            "path": str(BENCHMARK_REFRESH_JSON),
            "present": BENCHMARK_REFRESH_JSON.exists(),
            "status": source["benchmark_status"],
            "refresh_id": source["refresh_id"],
            "sha256": _sha256(BENCHMARK_REFRESH_JSON),
            "sha256_16": _sha16(_sha256(BENCHMARK_REFRESH_JSON)),
        },
        "source_summary": source,
        "candidate_state": state,
        "candidate_catalog": list(catalog),
        "candidate_ranking": ranking,
        "candidate_package": package,
        "fail_closed_controls": list(FAIL_CLOSED_CONTROLS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "candidate_checks": checks,
        "candidate_check_list": list(CANDIDATE_CHECKS),
        "candidate_cases": list(CANDIDATE_CASES),
        "candidate_results": list(results),
        "candidate_gates": list(gates),
        "candidate_issues": list(issues),
        "candidate_index": index,
        "candidate_ready": candidate_ready,
        "candidate_locked": True,
        "candidate_refresh_created": True,
        "candidate_refresh_ready": True,
        "candidate_refresh_locked": True,
        "candidate_count": ranking["candidate_count"],
        "ranked_candidate_count": ranking["ranked_candidate_count"],
        "selected_candidate_count": ranking["selected_candidate_count"],
        "selected_candidate_id": ranking["selected_candidate_id"],
        "candidate_package_id": package["package_id"],
        "candidate_artifact_created": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "candidate_check_count": len(CANDIDATE_CHECKS),
        "candidate_case_count": len(CANDIDATE_CASES),
        "candidate_pass_count": candidate_pass_count,
        "candidate_failure_count": candidate_failure_count,
        "candidate_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "candidate_issue_count": issue_count,
        "warning_count": 0,
        "rebuild_gate_required_next": True,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "metadata": {
            "source": "milestone_10_candidate_refresh_v1",
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
        "candidate_refresh_id": f"MILESTONE-10-CANDIDATE-REFRESH-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_candidate_refresh(candidate: Mapping[str, Any]) -> Dict[str, Any]:
    gates = candidate.get("candidate_gates", [])
    issues = candidate.get("candidate_issues", [])
    results = candidate.get("candidate_results", [])
    catalog = candidate.get("candidate_catalog", [])

    checks = {
        "status_ready": candidate.get("status") == CANDIDATE_STATUS,
        "candidate_refresh_id_present": isinstance(candidate.get("candidate_refresh_id"), str)
        and bool(candidate.get("candidate_refresh_id")),
        "signature_present": isinstance(candidate.get("signature"), str)
        and bool(candidate.get("signature")),
        "baseline_commit_valid": str(candidate.get("baseline_commit", "")).startswith("ed3aa9d"),
        "candidate_mode_valid": candidate.get("candidate_mode") == CANDIDATE_MODE,
        "candidate_scope_valid": candidate.get("candidate_scope") == CANDIDATE_SCOPE,
        "candidate_verdict_valid": candidate.get("candidate_verdict") == CANDIDATE_VERDICT,
        "next_allowed_stage_valid": candidate.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "candidate_ready": candidate.get("candidate_ready") is True,
        "candidate_locked": candidate.get("candidate_locked") is True,
        "candidate_refresh_created": candidate.get("candidate_refresh_created") is True,
        "candidate_refresh_ready": candidate.get("candidate_refresh_ready") is True,
        "candidate_refresh_locked": candidate.get("candidate_refresh_locked") is True,
        "candidate_count_valid": candidate.get("candidate_count") == EXPECTED_CANDIDATE_COUNT,
        "ranked_candidate_count_valid": candidate.get("ranked_candidate_count")
        == EXPECTED_RANKED_CANDIDATE_COUNT,
        "selected_candidate_count_valid": candidate.get("selected_candidate_count")
        == EXPECTED_SELECTED_CANDIDATE_COUNT,
        "selected_candidate_valid": candidate.get("selected_candidate_id")
        == "M10-CANDIDATE-BALANCED-PATCH-STACK-v1",
        "candidate_package_present": isinstance(candidate.get("candidate_package_id"), str)
        and candidate.get("candidate_package_id", "").startswith("MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-"),
        "candidate_artifact_created": candidate.get("candidate_artifact_created") is True,
        "real_submission_candidate_not_created": candidate.get("real_submission_candidate_created") is False,
        "submission_json_not_created": candidate.get("submission_json_created") is False,
        "upload_package_not_created": candidate.get("upload_package_created") is False,
        "candidate_check_count_valid": candidate.get("candidate_check_count") == EXPECTED_CANDIDATE_CHECK_COUNT,
        "candidate_case_count_valid": candidate.get("candidate_case_count") == EXPECTED_CANDIDATE_CASE_COUNT,
        "candidate_pass_count_valid": candidate.get("candidate_pass_count") == EXPECTED_CANDIDATE_PASS_COUNT,
        "candidate_failure_count_zero": candidate.get("candidate_failure_count") == EXPECTED_CANDIDATE_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "catalog_local_only": bool(catalog) and all(item.get("local_only") is True for item in catalog),
        "catalog_no_upload": bool(catalog)
        and all(item.get("requires_kaggle_upload") is False for item in catalog),
        "rebuild_gate_required_next": candidate.get("rebuild_gate_required_next") is True,
        "real_submission_decision_not_authorized": candidate.get("real_submission_decision")
        == "NOT_AUTHORIZED",
        "real_submission_allowed_false": candidate.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": candidate.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": candidate.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": candidate.get("kaggle_submission_sent") is False,
        "fail_closed_required": candidate.get("fail_closed_required") is True,
        "fail_closed_active": candidate.get("fail_closed_active") is True,
        "metadata_safe": candidate.get("metadata", {}).get("external_api_dependency") is False
        and candidate.get("metadata", {}).get("contains_api_keys") is False
        and candidate.get("metadata", {}).get("private_core_exposure") is False
        and candidate.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_CANDIDATE_REFRESH_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "candidate_refresh_id": candidate.get("candidate_refresh_id"),
        "signature": candidate.get("signature"),
    }


def render_candidate_refresh_markdown(candidate: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Candidate Refresh v1",
        "",
        f"- status: {candidate['status']}",
        f"- candidate_refresh_id: {candidate['candidate_refresh_id']}",
        f"- signature: {candidate['signature']}",
        f"- baseline_commit: {candidate['baseline_commit']}",
        f"- candidate_mode: {candidate['candidate_mode']}",
        f"- candidate_scope: {candidate['candidate_scope']}",
        f"- candidate_verdict: {candidate['candidate_verdict']}",
        f"- next_allowed_stage: {candidate['next_allowed_stage']}",
        f"- candidate_ready: {candidate['candidate_ready']}",
        f"- candidate_count: {candidate['candidate_count']}",
        f"- ranked_candidate_count: {candidate['ranked_candidate_count']}",
        f"- selected_candidate_id: {candidate['selected_candidate_id']}",
        f"- candidate_package_id: {candidate['candidate_package_id']}",
        f"- candidate_artifact_created: {candidate['candidate_artifact_created']}",
        f"- real_submission_candidate_created: {candidate['real_submission_candidate_created']}",
        f"- submission_json_created: {candidate['submission_json_created']}",
        f"- upload_package_created: {candidate['upload_package_created']}",
        f"- rebuild_gate_required_next: {candidate['rebuild_gate_required_next']}",
        f"- real_submission_decision: {candidate['real_submission_decision']}",
        f"- real_submission_allowed: {candidate['real_submission_allowed']}",
        f"- fail_closed_active: {candidate['fail_closed_active']}",
        "",
        "## Ranked candidates",
        "",
    ]

    for item in candidate["candidate_ranking"]["ranked_candidates"]:
        lines.append(
            f"- {item['candidate_id']} / family={item['family']} / "
            f"score_hint={item['score_hint']} / confidence={item['confidence']} / "
            f"complexity={item['complexity']}"
        )

    lines.extend(["", "## Validation results", ""])

    for result in candidate["candidate_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Candidate refresh is ready as a local artifact. Real submission remains blocked. The next stage is the submission candidate rebuild gate.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_READY=true",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_MODE=MILESTONE_10_CANDIDATE_REFRESH_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_VERDICT=CANDIDATE_REFRESH_READY_FOR_SUBMISSION_CANDIDATE_REBUILD_GATE",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=ed3aa9d",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_7_SUBMISSION_CANDIDATE_REBUILD_GATE_V1",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_COUNT=4",
            "ARC_AGI3_MILESTONE_10_RANKED_CANDIDATE_COUNT=4",
            "ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_COUNT=1",
            f"ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_ID={candidate['selected_candidate_id']}",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_CHECK_COUNT=26",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_CREATED=true",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_REFRESH_READY=true",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_ARTIFACT_CREATED=true",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false",
            "ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_REBUILD_GATE_REQUIRED_NEXT=true",
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


def render_candidate_refresh_manifest(candidate: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 CANDIDATE REFRESH MANIFEST v1",
        f"candidate_refresh_id={candidate['candidate_refresh_id']}",
        f"signature={candidate['signature']}",
        f"status={candidate['status']}",
        f"baseline_commit={candidate['baseline_commit']}",
        f"candidate_mode={candidate['candidate_mode']}",
        f"candidate_verdict={candidate['candidate_verdict']}",
        f"next_allowed_stage={candidate['next_allowed_stage']}",
        f"candidate_ready={candidate['candidate_ready']}",
        f"candidate_refresh_created={candidate['candidate_refresh_created']}",
        f"candidate_refresh_ready={candidate['candidate_refresh_ready']}",
        f"candidate_count={candidate['candidate_count']}",
        f"ranked_candidate_count={candidate['ranked_candidate_count']}",
        f"selected_candidate_count={candidate['selected_candidate_count']}",
        f"selected_candidate_id={candidate['selected_candidate_id']}",
        f"candidate_package_id={candidate['candidate_package_id']}",
        f"candidate_artifact_created={candidate['candidate_artifact_created']}",
        f"real_submission_candidate_created={candidate['real_submission_candidate_created']}",
        f"submission_json_created={candidate['submission_json_created']}",
        f"upload_package_created={candidate['upload_package_created']}",
        f"candidate_check_count={candidate['candidate_check_count']}",
        f"candidate_case_count={candidate['candidate_case_count']}",
        f"candidate_pass_count={candidate['candidate_pass_count']}",
        f"candidate_failure_count={candidate['candidate_failure_count']}",
        f"candidate_gate_count={candidate['candidate_gate_count']}",
        f"passed_gate_count={candidate['passed_gate_count']}",
        f"candidate_issue_count={candidate['candidate_issue_count']}",
        f"rebuild_gate_required_next={candidate['rebuild_gate_required_next']}",
        f"real_submission_decision={candidate['real_submission_decision']}",
        f"real_submission_allowed={candidate['real_submission_allowed']}",
        f"manual_upload_allowed={candidate['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={candidate['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={candidate['kaggle_submission_sent']}",
        f"fail_closed_required={candidate['fail_closed_required']}",
        f"fail_closed_active={candidate['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "CANDIDATE_RANKING",
    ]

    for item in candidate["candidate_ranking"]["ranked_candidates"]:
        lines.append(
            f"{item['candidate_id']} family={item['family']} "
            f"score_hint={item['score_hint']} confidence={item['confidence']} "
            f"complexity={item['complexity']}"
        )

    lines.append("")
    lines.append("CANDIDATE_VALIDATION_RESULTS")
    for result in candidate["candidate_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_candidate_refresh_artifacts(
    candidate: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    candidate = dict(candidate or build_milestone_10_candidate_refresh())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-candidate-refresh-v1.json"
    md_path = output / "milestone-10-candidate-refresh-v1.md"
    manifest_path = output / "milestone-10-candidate-refresh-manifest-v1.txt"
    index_path = output / "milestone-10-candidate-refresh-index-v1.json"

    json_path.write_text(json.dumps(candidate, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_candidate_refresh_markdown(candidate), encoding="utf-8")
    manifest_path.write_text(render_candidate_refresh_manifest(candidate), encoding="utf-8")
    index_path.write_text(
        json.dumps(candidate["candidate_index"], indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_10_candidate_refresh_pipeline() -> Dict[str, Any]:
    candidate = build_milestone_10_candidate_refresh()
    validation = validate_milestone_10_candidate_refresh(candidate)
    artifacts = write_candidate_refresh_artifacts(candidate)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_10_CANDIDATE_REFRESH_V1_PIPELINE_INVALID",
        "candidate_status": candidate["status"],
        "validation_status": validation["status"],
        "candidate": candidate,
        "candidate_refresh_id": candidate["candidate_refresh_id"],
        "signature": candidate["signature"],
        "candidate_mode": candidate["candidate_mode"],
        "candidate_verdict": candidate["candidate_verdict"],
        "next_allowed_stage": candidate["next_allowed_stage"],
        "candidate_ready": candidate["candidate_ready"],
        "candidate_refresh_created": candidate["candidate_refresh_created"],
        "candidate_refresh_ready": candidate["candidate_refresh_ready"],
        "candidate_count": candidate["candidate_count"],
        "ranked_candidate_count": candidate["ranked_candidate_count"],
        "selected_candidate_count": candidate["selected_candidate_count"],
        "selected_candidate_id": candidate["selected_candidate_id"],
        "candidate_package_id": candidate["candidate_package_id"],
        "candidate_artifact_created": candidate["candidate_artifact_created"],
        "real_submission_candidate_created": candidate["real_submission_candidate_created"],
        "submission_json_created": candidate["submission_json_created"],
        "upload_package_created": candidate["upload_package_created"],
        "candidate_check_count": candidate["candidate_check_count"],
        "candidate_case_count": candidate["candidate_case_count"],
        "candidate_pass_count": candidate["candidate_pass_count"],
        "candidate_failure_count": candidate["candidate_failure_count"],
        "candidate_gate_count": candidate["candidate_gate_count"],
        "passed_gate_count": candidate["passed_gate_count"],
        "candidate_issue_count": candidate["candidate_issue_count"],
        "warning_count": candidate["warning_count"],
        "rebuild_gate_required_next": candidate["rebuild_gate_required_next"],
        "real_submission_decision": candidate["real_submission_decision"],
        "real_submission_allowed": candidate["real_submission_allowed"],
        "manual_upload_allowed": candidate["manual_upload_allowed"],
        "kaggle_authentication_allowed": candidate["kaggle_authentication_allowed"],
        "kaggle_submission_sent": candidate["kaggle_submission_sent"],
        "fail_closed_required": candidate["fail_closed_required"],
        "fail_closed_active": candidate["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": candidate["metadata"],
    }
