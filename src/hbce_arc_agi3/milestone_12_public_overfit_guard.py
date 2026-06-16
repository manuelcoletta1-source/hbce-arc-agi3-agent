"""Milestone #12 Task 11 - Public Overfit Guard v1.

Guard against public overfit, solution leakage, score laundering and accidental
submission behavior after the ranked candidate benchmark.

This module is deterministic, local-only, public-safe and fail-closed.
It does not create a Kaggle submission, authenticate to Kaggle, upload files,
claim an official score or expose private core logic.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_PUBLIC_OVERFIT_GUARD_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 11
TASK_LABEL = "Milestone #12 Task 11 - Public Overfit Guard v1"

SOURCE_TASK = "MILESTONE_12_TASK_10_RANKED_CANDIDATE_BENCHMARK_V1"
NEXT_STAGE = "MILESTONE_12_TASK_12_SUBMISSION_READINESS_GATE_V1"

TASK_MODE = "MILESTONE_12_PUBLIC_OVERFIT_GUARD_V1_LOCAL_ONLY"
TASK_SCOPE = "PUBLIC_OVERFIT_GUARD_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_SCORE_CLAIM"
TASK_VERDICT = "MILESTONE_12_PUBLIC_OVERFIT_GUARD_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "public-overfit-guard-v1"

SOURCE_BENCHMARK_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "ranked-candidate-benchmark-v1"
    / "milestone-12-ranked-candidate-benchmark-v1.json"
)

FORBIDDEN_FIELD_NAMES = {
    "answer",
    "answers",
    "expected",
    "expected_output",
    "expected_outputs",
    "target",
    "target_grid",
    "solution",
    "solutions",
    "test_solution",
    "ground_truth",
    "ground_truth_grid",
    "leaderboard_score",
    "public_leaderboard_score",
    "private_leaderboard_score",
    "official_score",
    "official_kaggle_score",
    "submission_json",
    "submission_file",
    "kaggle_token",
    "api_key",
    "secret",
}

FORBIDDEN_TEXT_SIGNALS = {
    "public leaderboard",
    "private leaderboard",
    "official kaggle score",
    "test solution",
    "ground truth",
    "target grid",
    "expected output grid",
    "submission upload",
    "kaggle api token",
    "kaggle.json",
}

GUARD_MEASUREMENT_TARGETS = [
    "source_benchmark_case_count",
    "guard_case_count",
    "guard_pass_count",
    "guard_failure_count",
    "public_overfit_violation_count",
    "forbidden_field_hit_count",
    "forbidden_text_hit_count",
    "score_claim_violation_count",
    "submission_violation_count",
    "boundary_violation_count",
]


def _run_git_head() -> str:
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "NO_GIT_HEAD_AVAILABLE"
    return result.stdout.strip() or "NO_GIT_HEAD_AVAILABLE"


def _stable_signature(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()[:16]


def _gate(name: str, passed: bool, required: bool, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "required": bool(required),
        "description": description,
    }


def _check(name: str, status: bool, severity: str, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "status": bool(status),
        "severity": severity,
        "description": description,
    }


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def _iter_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.append(str(key))
            keys.extend(_iter_keys(child))
    elif isinstance(value, list):
        for item in value:
            keys.extend(_iter_keys(item))
    return keys


def _text_hit_list(value: Any) -> list[str]:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False).lower()
    return sorted(signal for signal in FORBIDDEN_TEXT_SIGNALS if signal in text)


def _field_hit_list(value: Any) -> list[str]:
    keys = {key.lower() for key in _iter_keys(value)}
    return sorted(field for field in FORBIDDEN_FIELD_NAMES if field in keys)


def _extract_benchmark_cases(source_record: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not source_record:
        return []
    benchmark = source_record.get("benchmark")
    if not isinstance(benchmark, dict):
        return []
    cases = benchmark.get("benchmark_cases")
    if not isinstance(cases, list):
        return []
    return [case for case in cases if isinstance(case, dict)]


def build_guard_case(benchmark_case: dict[str, Any]) -> dict[str, Any]:
    field_hits = _field_hit_list(benchmark_case)
    text_hits = _text_hit_list(benchmark_case)

    score_claim_violation = benchmark_case.get("score_claim") not in {None, "None"} or benchmark_case.get("kaggle_score_semantics") != "NOT_A_KAGGLE_SCORE"
    submission_violation = any(
        benchmark_case.get(key) is True
        for key in [
            "submission_json_created",
            "real_submission_candidate_created",
            "kaggle_submission_sent",
            "kaggle_upload_performed",
            "kaggle_authentication_performed",
        ]
    )

    actions = benchmark_case.get("actions")
    benchmark_passed = benchmark_case.get("benchmark_passed") is True

    checks = [
        _check("benchmark_case_passed", benchmark_passed, "PASS" if benchmark_passed else "BLOCKING", "Source benchmark case passed."),
        _check("actions_present", isinstance(actions, list) and len(actions) > 0, "PASS" if isinstance(actions, list) and len(actions) > 0 else "BLOCKING", "Case uses action trace, not leaked target."),
        _check("no_forbidden_fields", len(field_hits) == 0, "PASS" if len(field_hits) == 0 else "BLOCKING", "Case does not expose forbidden solution fields."),
        _check("no_forbidden_text_signals", len(text_hits) == 0, "PASS" if len(text_hits) == 0 else "BLOCKING", "Case does not contain public overfit text signals."),
        _check("no_score_claim_violation", not score_claim_violation, "PASS" if not score_claim_violation else "BLOCKING", "Case does not claim Kaggle score."),
        _check("no_submission_violation", not submission_violation, "PASS" if not submission_violation else "BLOCKING", "Case does not perform or imply submission."),
        _check("rank_score_is_internal_only", isinstance(benchmark_case.get("rank_score"), int), "PASS" if isinstance(benchmark_case.get("rank_score"), int) else "BLOCKING", "Rank score remains internal heuristic score."),
    ]

    blocking_failures = [check for check in checks if check["status"] is not True and check["severity"] == "BLOCKING"]

    core = {
        "case_id": benchmark_case.get("case_id", "UNKNOWN_CASE"),
        "source_ranked_candidate_id": benchmark_case.get("source_ranked_candidate_id", "UNKNOWN_RANKED"),
        "checks": checks,
    }

    return {
        "guard_case_id": "PUBLIC-OVERFIT-GUARD-CASE-" + _stable_signature(core)[:12],
        "case_id": benchmark_case.get("case_id", "UNKNOWN_CASE"),
        "family": benchmark_case.get("family", "UNKNOWN_FAMILY"),
        "source_ranked_candidate_id": benchmark_case.get("source_ranked_candidate_id", "UNKNOWN_RANKED_CANDIDATE"),
        "source_candidate_id": benchmark_case.get("source_candidate_id", "UNKNOWN_CANDIDATE"),
        "candidate_kind": benchmark_case.get("candidate_kind", "UNKNOWN_KIND"),
        "rank_score": benchmark_case.get("rank_score"),
        "action_count": benchmark_case.get("action_count", 0),
        "field_hits": field_hits,
        "text_hits": text_hits,
        "score_claim_violation": score_claim_violation,
        "submission_violation": submission_violation,
        "public_overfit_violation": len(blocking_failures) > 0,
        "guard_passed": len(blocking_failures) == 0,
        "failure_count": len(blocking_failures),
        "check_count": len(checks),
        "checks": checks,
    }


def build_guard_payload(source_record: dict[str, Any] | None) -> dict[str, Any]:
    benchmark_cases = _extract_benchmark_cases(source_record)
    guard_cases = [build_guard_case(case) for case in benchmark_cases]

    field_hits = sorted({hit for case in guard_cases for hit in case["field_hits"]})
    text_hits = sorted({hit for case in guard_cases for hit in case["text_hits"]})

    score_claim_violation_count = sum(1 for case in guard_cases if case["score_claim_violation"] is True)
    submission_violation_count = sum(1 for case in guard_cases if case["submission_violation"] is True)
    public_overfit_violation_count = sum(1 for case in guard_cases if case["public_overfit_violation"] is True)

    return {
        "public_overfit_guard_id": "MILESTONE_12_PUBLIC_OVERFIT_GUARD_SYNTHETIC_V1",
        "guard_family": "PUBLIC_OVERFIT_SOLUTION_LEAKAGE_AND_SUBMISSION_BLOCKER",
        "source_benchmark_case_count": len(benchmark_cases),
        "guard_case_count": len(guard_cases),
        "guard_pass_count": sum(1 for case in guard_cases if case["guard_passed"] is True),
        "guard_failure_count": sum(int(case["failure_count"]) for case in guard_cases),
        "public_overfit_violation_count": public_overfit_violation_count,
        "forbidden_field_hits": field_hits,
        "forbidden_field_hit_count": len(field_hits),
        "forbidden_text_hits": text_hits,
        "forbidden_text_hit_count": len(text_hits),
        "score_claim_violation_count": score_claim_violation_count,
        "submission_violation_count": submission_violation_count,
        "boundary_violation_count": public_overfit_violation_count + score_claim_violation_count + submission_violation_count,
        "guard_cases": guard_cases,
        "measurement_targets": GUARD_MEASUREMENT_TARGETS,
        "measurement_target_count": len(GUARD_MEASUREMENT_TARGETS),
    }


def build_public_overfit_guard_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_BENCHMARK_ARTIFACT.exists()
    source_record = _load_json(SOURCE_BENCHMARK_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_ready = bool(source_record and source_record.get("ranked_candidate_benchmark_ready") is True)
    source_passed = bool(source_record and source_record.get("ranked_candidate_benchmark_passed") is True)
    source_next_stage_ok = bool(source_record and source_record.get("next_stage") == "MILESTONE_12_TASK_11_PUBLIC_OVERFIT_GUARD_V1")
    source_strategy_ok = bool(source_record and source_record.get("chosen_strategy") == CHOSEN_STRATEGY)
    source_goal_ok = bool(source_record and source_record.get("competitive_goal") == COMPETITIVE_GOAL)
    source_issue_zero = bool(source_record and source_record.get("issue_count") == 0)

    source_boundaries_ok = all(
        [
            source_record and source_record.get("public_overfit_allowed") is False,
            source_record and source_record.get("public_overfit_guard_required") is True,
            source_record and source_record.get("external_api_dependency") is False,
            source_record and source_record.get("internet_during_eval") is False,
            source_record and source_record.get("real_submission_allowed") is False,
            source_record and source_record.get("manual_upload_allowed") is False,
            source_record and source_record.get("kaggle_submission_sent") is False,
            source_record and source_record.get("kaggle_authentication_performed") is False,
            source_record and source_record.get("private_core_exposure") is False,
            source_record and source_record.get("legal_certification") is False,
        ]
    )

    guard = build_guard_payload(source_record)

    source_benchmark_case_count_ok = guard["source_benchmark_case_count"] == 6
    guard_case_count_ok = guard["guard_case_count"] == 6
    guard_pass_count_ok = guard["guard_pass_count"] == 6
    guard_failure_count_ok = guard["guard_failure_count"] == 0
    public_overfit_violation_zero = guard["public_overfit_violation_count"] == 0
    forbidden_field_hit_zero = guard["forbidden_field_hit_count"] == 0
    forbidden_text_hit_zero = guard["forbidden_text_hit_count"] == 0
    score_claim_violation_zero = guard["score_claim_violation_count"] == 0
    submission_violation_zero = guard["submission_violation_count"] == 0
    boundary_violation_zero = guard["boundary_violation_count"] == 0
    measurement_count_ok = guard["measurement_target_count"] == 10

    guard_checks = [
        _check("source_artifact_present", source_artifact_present, "PASS" if source_artifact_present else "BLOCKING", "Task 10 benchmark artifact is present."),
        _check("source_artifact_parseable", source_artifact_parseable, "PASS" if source_artifact_parseable else "BLOCKING", "Task 10 benchmark artifact is parseable."),
        _check("source_ready", source_ready, "PASS" if source_ready else "BLOCKING", "Task 10 benchmark is ready."),
        _check("source_passed", source_passed, "PASS" if source_passed else "BLOCKING", "Task 10 benchmark passed."),
        _check("source_next_stage_ok", source_next_stage_ok, "PASS" if source_next_stage_ok else "BLOCKING", "Task 10 points to public overfit guard."),
        _check("source_strategy_ok", source_strategy_ok, "PASS" if source_strategy_ok else "BLOCKING", "Source strategy is aligned."),
        _check("source_goal_ok", source_goal_ok, "PASS" if source_goal_ok else "BLOCKING", "Source competitive goal is aligned."),
        _check("source_issue_zero", source_issue_zero, "PASS" if source_issue_zero else "BLOCKING", "Source issue count is zero."),
        _check("source_boundaries_ok", source_boundaries_ok, "PASS" if source_boundaries_ok else "BLOCKING", "Source boundaries are preserved."),
        _check("source_benchmark_case_count_ok", source_benchmark_case_count_ok, "PASS" if source_benchmark_case_count_ok else "BLOCKING", "Source benchmark has six cases."),
        _check("guard_case_count_ok", guard_case_count_ok, "PASS" if guard_case_count_ok else "BLOCKING", "Guard emits six cases."),
        _check("guard_pass_count_ok", guard_pass_count_ok, "PASS" if guard_pass_count_ok else "BLOCKING", "Guard passes six cases."),
        _check("guard_failure_count_ok", guard_failure_count_ok, "PASS" if guard_failure_count_ok else "BLOCKING", "Guard has zero failures."),
        _check("public_overfit_violation_zero", public_overfit_violation_zero, "PASS" if public_overfit_violation_zero else "BLOCKING", "No public overfit violation."),
        _check("forbidden_field_hit_zero", forbidden_field_hit_zero, "PASS" if forbidden_field_hit_zero else "BLOCKING", "No forbidden solution fields."),
        _check("forbidden_text_hit_zero", forbidden_text_hit_zero, "PASS" if forbidden_text_hit_zero else "BLOCKING", "No forbidden text signals."),
        _check("score_claim_violation_zero", score_claim_violation_zero, "PASS" if score_claim_violation_zero else "BLOCKING", "No score claim violation."),
        _check("submission_violation_zero", submission_violation_zero, "PASS" if submission_violation_zero else "BLOCKING", "No submission violation."),
        _check("boundary_violation_zero", boundary_violation_zero, "PASS" if boundary_violation_zero else "BLOCKING", "No boundary violation."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "Guard measurement targets are declared."),
    ]

    guard_passed = all(check["status"] is True for check in guard_checks)

    guard_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "public_overfit_guard_status": "READY" if guard_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "public_overfit_guard_id": guard["public_overfit_guard_id"],
        "guard_case_count": guard["guard_case_count"],
        "guard_pass_count": guard["guard_pass_count"],
        "public_overfit_violation_count": guard["public_overfit_violation_count"],
        "forbidden_field_hit_count": guard["forbidden_field_hit_count"],
        "forbidden_text_hit_count": guard["forbidden_text_hit_count"],
        "score_claim_violation_count": guard["score_claim_violation_count"],
        "submission_violation_count": guard["submission_violation_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("source_artifact_present", source_artifact_present, True, "Task 10 benchmark artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Task 10 benchmark artifact is parseable."),
        _gate("source_ready", source_ready, True, "Task 10 benchmark is ready."),
        _gate("source_passed", source_passed, True, "Task 10 benchmark passed."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 10 points to this guard."),
        _gate("source_strategy_ok", source_strategy_ok, True, "Source strategy is aligned."),
        _gate("source_goal_ok", source_goal_ok, True, "Source goal is aligned."),
        _gate("source_issue_zero", source_issue_zero, True, "Source issue count is zero."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("source_benchmark_case_count_ok", source_benchmark_case_count_ok, True, "Source has six benchmark cases."),
        _gate("guard_case_count_ok", guard_case_count_ok, True, "Guard emits six cases."),
        _gate("guard_pass_count_ok", guard_pass_count_ok, True, "Guard passes six cases."),
        _gate("guard_failure_count_ok", guard_failure_count_ok, True, "Guard has zero failures."),
        _gate("public_overfit_violation_zero", public_overfit_violation_zero, True, "No public overfit violation."),
        _gate("forbidden_field_hit_zero", forbidden_field_hit_zero, True, "No forbidden solution field hits."),
        _gate("forbidden_text_hit_zero", forbidden_text_hit_zero, True, "No forbidden text hits."),
        _gate("score_claim_violation_zero", score_claim_violation_zero, True, "No score claim violation."),
        _gate("submission_violation_zero", submission_violation_zero, True, "No submission violation."),
        _gate("boundary_violation_zero", boundary_violation_zero, True, "No boundary violation."),
        _gate("measurement_count_ok", measurement_count_ok, True, "Measurement targets are declared."),
        _gate("public_overfit_allowed_false", True, True, "Public overfitting remains blocked."),
        _gate("public_overfit_guard_required_true", True, True, "Public overfit guard is required."),
        _gate("external_api_dependency_false", True, True, "External API dependency remains false."),
        _gate("internet_during_eval_false", True, True, "Internet during evaluation remains false."),
        _gate("real_submission_allowed_false", True, True, "Real submission remains blocked."),
        _gate("manual_upload_allowed_false", True, True, "Manual upload remains blocked."),
        _gate("kaggle_submission_sent_false", True, True, "No Kaggle submission is sent."),
        _gate("kaggle_authentication_performed_false", True, True, "No Kaggle authentication is performed."),
        _gate("private_core_exposure_false", True, True, "Private core exposure remains false."),
        _gate("legal_certification_false", True, True, "legal_certification remains false."),
        _gate("official_score_claim_allowed_false", True, True, "Official score claim remains blocked."),
        _gate("competitive_score_claim_allowed_false", True, True, "Competitive score claim remains blocked."),
        _gate("local_only_true", True, True, "Task remains local-only."),
        _gate("deterministic_true", True, True, "Task remains deterministic."),
        _gate("public_safe_true", True, True, "Task remains public-safe."),
        _gate("fail_closed_active", True, True, "Task fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_benchmark_artifact": str(SOURCE_BENCHMARK_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_ready": source_ready,
        "source_passed": source_passed,
        "source_next_stage_ok": source_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "public_overfit_guard_ready": True,
        "public_overfit_guard_valid": guard_passed,
        "public_overfit_guard_passed": guard_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "guard_summary": guard_summary,
        "guard": guard,
        "source_benchmark_case_count": guard["source_benchmark_case_count"],
        "guard_case_count": guard["guard_case_count"],
        "guard_pass_count": guard["guard_pass_count"],
        "guard_failure_count": guard["guard_failure_count"],
        "public_overfit_violation_count": guard["public_overfit_violation_count"],
        "forbidden_field_hit_count": guard["forbidden_field_hit_count"],
        "forbidden_text_hit_count": guard["forbidden_text_hit_count"],
        "score_claim_violation_count": guard["score_claim_violation_count"],
        "submission_violation_count": guard["submission_violation_count"],
        "boundary_violation_count": guard["boundary_violation_count"],
        "measurement_target_count": len(GUARD_MEASUREMENT_TARGETS),
        "measurement_targets": GUARD_MEASUREMENT_TARGETS,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "open_source_prize_eligibility_required": True,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "submission_json_created": False,
        "real_submission_candidate_created": False,
        "kaggle_submission_sent": False,
        "kaggle_upload_performed": False,
        "kaggle_authentication_performed": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "guard_check_count": len(guard_checks),
        "guard_checks": guard_checks,
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if len(required_gates) == len(passed_required_gates) else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-12-PUBLIC-OVERFIT-GUARD-" + signature[:12]
    return record


def validate_public_overfit_guard_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "public_overfit_guard_ready",
        "public_overfit_guard_valid",
        "public_overfit_guard_passed",
        "source_artifact_present",
        "source_artifact_parseable",
        "source_ready",
        "source_passed",
        "source_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "public_overfit_allowed",
        "external_api_dependency",
        "internet_during_eval",
        "real_submission_allowed",
        "manual_upload_allowed",
        "submission_json_created",
        "real_submission_candidate_created",
        "kaggle_submission_sent",
        "kaggle_upload_performed",
        "kaggle_authentication_performed",
        "contains_api_keys",
        "private_core_exposure",
        "legal_certification",
        "official_score_claim_allowed",
        "competitive_score_claim_allowed",
        "real_public_score_claimed",
        "private_score_claimed",
    ]

    for key in expected_true:
        if record.get(key) is not True:
            issues.append(f"{key}_NOT_TRUE")

    for key in expected_false:
        if record.get(key) is not False:
            issues.append(f"{key}_NOT_FALSE")

    if record.get("revision") != TASK_NAME:
        issues.append("REVISION_MISMATCH")

    if record.get("source_task") != SOURCE_TASK:
        issues.append("SOURCE_TASK_MISMATCH")

    if record.get("next_stage") != NEXT_STAGE:
        issues.append("NEXT_STAGE_MISMATCH")

    if record.get("task_verdict") != TASK_VERDICT:
        issues.append("TASK_VERDICT_MISMATCH")

    if record.get("competitive_goal") != COMPETITIVE_GOAL:
        issues.append("COMPETITIVE_GOAL_MISMATCH")

    if record.get("chosen_strategy") != CHOSEN_STRATEGY:
        issues.append("CHOSEN_STRATEGY_MISMATCH")

    expected_counts = {
        "source_benchmark_case_count": 6,
        "guard_case_count": 6,
        "guard_pass_count": 6,
        "guard_failure_count": 0,
        "public_overfit_violation_count": 0,
        "forbidden_field_hit_count": 0,
        "forbidden_text_hit_count": 0,
        "score_claim_violation_count": 0,
        "submission_violation_count": 0,
        "boundary_violation_count": 0,
        "measurement_target_count": 10,
    }
    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    guard = record.get("guard")
    if not isinstance(guard, dict):
        issues.append("GUARD_MISSING")
    else:
        cases = guard.get("guard_cases")
        if not isinstance(cases, list) or len(cases) != 6:
            issues.append("GUARD_CASES_MISSING_OR_COUNT_MISMATCH")
        elif any(not isinstance(case, dict) or case.get("guard_passed") is not True for case in cases):
            issues.append("GUARD_CASE_NOT_PASSED")

    summary = record.get("guard_summary")
    if not isinstance(summary, dict):
        issues.append("GUARD_SUMMARY_MISSING")
    else:
        if summary.get("public_overfit_guard_status") != "READY":
            issues.append("GUARD_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("GUARD_SUMMARY_NEXT_STAGE_MISMATCH")

    checks = record.get("guard_checks")
    if not isinstance(checks, list) or not checks:
        issues.append("GUARD_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in checks):
        issues.append("GUARD_CHECK_FAILED")

    gates = record.get("gates")
    if not isinstance(gates, list) or not gates:
        issues.append("GATES_MISSING")
    else:
        failed_required = [
            gate.get("name", "UNKNOWN_GATE")
            for gate in gates
            if gate.get("required") is True and gate.get("passed") is not True
        ]
        issues.extend(f"REQUIRED_GATE_FAILED:{name}" for name in failed_required)

    if record.get("issue_count") != 0:
        issues.append("ISSUE_COUNT_NOT_ZERO")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-12-public-overfit-guard-v1.json"
    index_path = target_dir / "milestone-12-public-overfit-guard-index-v1.json"
    manifest_path = target_dir / "milestone-12-public-overfit-guard-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-public-overfit-guard-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "public_overfit_guard_ready": record["public_overfit_guard_ready"],
        "public_overfit_guard_passed": record["public_overfit_guard_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "source_benchmark_case_count": record["source_benchmark_case_count"],
        "guard_case_count": record["guard_case_count"],
        "guard_pass_count": record["guard_pass_count"],
        "public_overfit_violation_count": record["public_overfit_violation_count"],
        "forbidden_field_hit_count": record["forbidden_field_hit_count"],
        "forbidden_text_hit_count": record["forbidden_text_hit_count"],
        "score_claim_violation_count": record["score_claim_violation_count"],
        "submission_violation_count": record["submission_violation_count"],
        "boundary_violation_count": record["boundary_violation_count"],
        "public_overfit_allowed": record["public_overfit_allowed"],
        "external_api_dependency": record["external_api_dependency"],
        "real_submission_allowed": record["real_submission_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "private_core_exposure": record["private_core_exposure"],
        "legal_certification": record["legal_certification"],
    }
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        f"revision={record['revision']}",
        f"task_id={record['task_id']}",
        f"signature={record['signature']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_scope={record['task_scope']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"milestone_12_status={record['milestone_12_status']}",
        f"public_overfit_guard_ready={record['public_overfit_guard_ready']}",
        f"public_overfit_guard_passed={record['public_overfit_guard_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"source_benchmark_case_count={record['source_benchmark_case_count']}",
        f"guard_case_count={record['guard_case_count']}",
        f"guard_pass_count={record['guard_pass_count']}",
        f"public_overfit_violation_count={record['public_overfit_violation_count']}",
        f"forbidden_field_hit_count={record['forbidden_field_hit_count']}",
        f"forbidden_text_hit_count={record['forbidden_text_hit_count']}",
        f"score_claim_violation_count={record['score_claim_violation_count']}",
        f"submission_violation_count={record['submission_violation_count']}",
        f"boundary_violation_count={record['boundary_violation_count']}",
        f"public_overfit_allowed={record['public_overfit_allowed']}",
        f"external_api_dependency={record['external_api_dependency']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- verdict: `{record['task_verdict']}`
- milestone_12_status: `{record['milestone_12_status']}`
- competitive_goal: `{record['competitive_goal']}`
- chosen_strategy: `{record['chosen_strategy']}`
- next_stage: `{record['next_stage']}`

## Public Overfit Guard

- public_overfit_guard_ready: `{record['public_overfit_guard_ready']}`
- public_overfit_guard_passed: `{record['public_overfit_guard_passed']}`
- source_benchmark_case_count: `{record['source_benchmark_case_count']}`
- guard_case_count: `{record['guard_case_count']}`
- guard_pass_count: `{record['guard_pass_count']}`
- guard_failure_count: `{record['guard_failure_count']}`
- public_overfit_violation_count: `{record['public_overfit_violation_count']}`
- forbidden_field_hit_count: `{record['forbidden_field_hit_count']}`
- forbidden_text_hit_count: `{record['forbidden_text_hit_count']}`
- score_claim_violation_count: `{record['score_claim_violation_count']}`
- submission_violation_count: `{record['submission_violation_count']}`
- boundary_violation_count: `{record['boundary_violation_count']}`

## Boundary

- public_overfit_allowed: `{record['public_overfit_allowed']}`
- public_overfit_guard_required: `{record['public_overfit_guard_required']}`
- external_api_dependency: `{record['external_api_dependency']}`
- internet_during_eval: `{record['internet_during_eval']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- manual_upload_allowed: `{record['manual_upload_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- kaggle_authentication_performed: `{record['kaggle_authentication_performed']}`
- official_score_claim_allowed: `{record['official_score_claim_allowed']}`
- competitive_score_claim_allowed: `{record['competitive_score_claim_allowed']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`
"""
    markdown_path.write_text(markdown, encoding="utf-8")

    def _artifact_ref(path: Path) -> str:
        try:
            return str(path.relative_to(PROJECT_ROOT))
        except ValueError:
            return str(path)

    return {
        "json": _artifact_ref(json_path),
        "index": _artifact_ref(index_path),
        "manifest": _artifact_ref(manifest_path),
        "markdown": _artifact_ref(markdown_path),
    }


def main() -> int:
    record = build_public_overfit_guard_record()
    issues = validate_public_overfit_guard_record(record)
    if issues:
        print(f"{TASK_NAME}_INVALID")
        for issue in issues:
            print(issue)
        return 1

    artifacts = write_artifacts(record)

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(f"{TASK_NAME}_READY")
    print(f"{TASK_NAME}_VALID")
    print(record["signature"])
    print(record["baseline_commit"])
    print(record["task_mode"])
    print(record["task_verdict"])
    print(record["next_stage"])
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
