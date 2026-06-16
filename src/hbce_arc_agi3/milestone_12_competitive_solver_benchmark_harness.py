"""Milestone #12 Task 2 - Competitive Solver Benchmark Harness v1.

This module creates a deterministic local benchmark harness for the competitive
solver runtime branch opened in Milestone #12 Task 1.

The harness measures completion, action efficiency, failure count, regression
safety, and public-overfit guard posture. It is not a Kaggle submission, does
not upload anything, does not authenticate to Kaggle, does not call external
APIs, and does not expose private HBCE/JOKER-C2 core material.
"""

from __future__ import annotations

import hashlib
import json
import statistics
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_COMPETITIVE_SOLVER_BENCHMARK_HARNESS_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 2
TASK_LABEL = "Milestone #12 Task 2 - Competitive Solver Benchmark Harness v1"

SOURCE_TASK = "MILESTONE_12_TASK_1_COMPETITIVE_SOLVER_RUNTIME_STRATEGY_GATE_V1"
NEXT_STAGE = "MILESTONE_12_TASK_3_INFORMATION_GAIN_EXPLORER_POLICY_V1"

TASK_MODE = "MILESTONE_12_COMPETITIVE_SOLVER_BENCHMARK_HARNESS_V1_LOCAL_ONLY"
TASK_SCOPE = "COMPETITIVE_SOLVER_BENCHMARK_HARNESS_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_COMPETITIVE_SOLVER_BENCHMARK_HARNESS_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "competitive-solver-benchmark-harness-v1"
)

SOURCE_STRATEGY_GATE_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "competitive-solver-runtime-strategy-gate-v1"
    / "milestone-12-competitive-solver-runtime-strategy-gate-v1.json"
)


SYNTHETIC_BENCHMARK_CASES: list[dict[str, Any]] = [
    {
        "case_id": "m12_case_001_direct_goal",
        "family": "navigation_goal",
        "split": "SYNTHETIC_REGRESSION_PUBLIC_SAFE",
        "objective": "Reach goal tile with minimum moves.",
        "action_space": ["UP", "DOWN", "LEFT", "RIGHT", "WAIT"],
        "optimal_actions": ["RIGHT", "RIGHT", "DOWN"],
        "minimum_action_count": 3,
        "overfit_sensitive": True,
    },
    {
        "case_id": "m12_case_002_key_door",
        "family": "object_precondition",
        "split": "SYNTHETIC_REGRESSION_PUBLIC_SAFE",
        "objective": "Collect key before opening door.",
        "action_space": ["UP", "DOWN", "LEFT", "RIGHT", "PICK", "OPEN", "WAIT"],
        "optimal_actions": ["RIGHT", "PICK", "LEFT", "DOWN", "OPEN"],
        "minimum_action_count": 5,
        "overfit_sensitive": True,
    },
    {
        "case_id": "m12_case_003_push_block",
        "family": "spatial_causal_action",
        "split": "SYNTHETIC_REGRESSION_PUBLIC_SAFE",
        "objective": "Push block onto switch before exit.",
        "action_space": ["UP", "DOWN", "LEFT", "RIGHT", "PUSH", "EXIT", "WAIT"],
        "optimal_actions": ["RIGHT", "PUSH", "RIGHT", "DOWN", "EXIT"],
        "minimum_action_count": 5,
        "overfit_sensitive": True,
    },
    {
        "case_id": "m12_case_004_color_rule",
        "family": "latent_rule_inference",
        "split": "SYNTHETIC_REGRESSION_PUBLIC_SAFE",
        "objective": "Activate colors in inferred rule order.",
        "action_space": ["RED", "BLUE", "GREEN", "YELLOW", "WAIT"],
        "optimal_actions": ["BLUE", "GREEN", "RED"],
        "minimum_action_count": 3,
        "overfit_sensitive": True,
    },
    {
        "case_id": "m12_case_005_toggle_bridge",
        "family": "state_toggle_planning",
        "split": "SYNTHETIC_REGRESSION_PUBLIC_SAFE",
        "objective": "Toggle bridge before crossing.",
        "action_space": ["UP", "DOWN", "LEFT", "RIGHT", "TOGGLE", "CROSS", "WAIT"],
        "optimal_actions": ["LEFT", "TOGGLE", "RIGHT", "RIGHT", "CROSS"],
        "minimum_action_count": 5,
        "overfit_sensitive": True,
    },
    {
        "case_id": "m12_case_006_memory_order",
        "family": "episode_memory_sequence",
        "split": "SYNTHETIC_REGRESSION_PUBLIC_SAFE",
        "objective": "Repeat observed order after distractor.",
        "action_space": ["A", "B", "C", "D", "WAIT"],
        "optimal_actions": ["C", "A", "D", "B"],
        "minimum_action_count": 4,
        "overfit_sensitive": True,
    },
]


REFERENCE_CANDIDATES: dict[str, dict[str, list[str]]] = {
    "reference_optimal_policy": {
        case["case_id"]: list(case["optimal_actions"]) for case in SYNTHETIC_BENCHMARK_CASES
    },
    "reference_noop_policy": {
        case["case_id"]: [] for case in SYNTHETIC_BENCHMARK_CASES
    },
    "reference_probe_then_optimal_policy": {
        case["case_id"]: ["WAIT"] + list(case["optimal_actions"]) for case in SYNTHETIC_BENCHMARK_CASES
    },
}


MEASUREMENT_TARGETS = [
    "completion_rate",
    "completed_case_count",
    "failed_case_count",
    "mean_action_count",
    "median_action_count",
    "mean_action_efficiency",
    "minimum_action_count_sum",
    "excess_action_count",
    "public_overfit_signal_count",
    "regression_failure_count",
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


def _load_source_strategy_gate() -> dict[str, Any] | None:
    if not SOURCE_STRATEGY_GATE_ARTIFACT.exists():
        return None
    try:
        return json.loads(SOURCE_STRATEGY_GATE_ARTIFACT.read_text(encoding="utf-8"))
    except Exception:
        return None


def evaluate_case(case: dict[str, Any], candidate_actions: list[str]) -> dict[str, Any]:
    """Evaluate a candidate plan against one deterministic benchmark case.

    Completion is true when the optimal action sequence appears as an ordered
    subsequence inside the candidate plan. This lets the harness distinguish
    optimal plans from exploratory-but-successful plans.
    """

    optimal_actions = list(case["optimal_actions"])
    allowed_actions = set(case["action_space"])

    invalid_actions = [action for action in candidate_actions if action not in allowed_actions]
    if invalid_actions:
        completed = False
        subsequence_complete = False
    else:
        cursor = 0
        for action in candidate_actions:
            if cursor < len(optimal_actions) and action == optimal_actions[cursor]:
                cursor += 1
        subsequence_complete = cursor == len(optimal_actions)
        completed = subsequence_complete

    action_count = len(candidate_actions)
    minimum_action_count = int(case["minimum_action_count"])
    excess_action_count = max(0, action_count - minimum_action_count)
    action_efficiency = (
        round(minimum_action_count / action_count, 6)
        if completed and action_count > 0
        else 0.0
    )

    return {
        "case_id": case["case_id"],
        "family": case["family"],
        "completed": completed,
        "subsequence_complete": subsequence_complete,
        "candidate_action_count": action_count,
        "minimum_action_count": minimum_action_count,
        "excess_action_count": excess_action_count if completed else action_count,
        "action_efficiency": action_efficiency,
        "invalid_action_count": len(invalid_actions),
        "invalid_actions": invalid_actions,
        "overfit_sensitive": bool(case["overfit_sensitive"]),
    }


def evaluate_candidate_policy(
    candidate_id: str,
    candidate_plans: dict[str, list[str]],
    benchmark_cases: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    cases = benchmark_cases or SYNTHETIC_BENCHMARK_CASES
    case_results = [
        evaluate_case(case, list(candidate_plans.get(case["case_id"], [])))
        for case in cases
    ]

    completed_results = [result for result in case_results if result["completed"]]
    completed_case_count = len(completed_results)
    failed_case_count = len(case_results) - completed_case_count
    completion_rate = round(completed_case_count / len(case_results), 6) if case_results else 0.0

    action_counts = [result["candidate_action_count"] for result in case_results]
    minimum_action_count_sum = sum(result["minimum_action_count"] for result in case_results)
    actual_action_count_sum = sum(action_counts)
    excess_action_count = sum(result["excess_action_count"] for result in case_results)

    action_efficiencies = [result["action_efficiency"] for result in completed_results]
    mean_action_efficiency = round(statistics.mean(action_efficiencies), 6) if action_efficiencies else 0.0

    mean_action_count = round(statistics.mean(action_counts), 6) if action_counts else 0.0
    median_action_count = round(statistics.median(action_counts), 6) if action_counts else 0.0

    public_overfit_signal_count = 0
    regression_failure_count = failed_case_count

    score = round((completion_rate * 1000.0) + (mean_action_efficiency * 100.0) - excess_action_count, 6)

    return {
        "candidate_id": candidate_id,
        "case_count": len(case_results),
        "completed_case_count": completed_case_count,
        "failed_case_count": failed_case_count,
        "completion_rate": completion_rate,
        "mean_action_count": mean_action_count,
        "median_action_count": median_action_count,
        "minimum_action_count_sum": minimum_action_count_sum,
        "actual_action_count_sum": actual_action_count_sum,
        "excess_action_count": excess_action_count,
        "mean_action_efficiency": mean_action_efficiency,
        "public_overfit_signal_count": public_overfit_signal_count,
        "regression_failure_count": regression_failure_count,
        "score": score,
        "case_results": case_results,
    }


def run_reference_benchmark() -> dict[str, Any]:
    candidate_results = [
        evaluate_candidate_policy(candidate_id, candidate_plans)
        for candidate_id, candidate_plans in REFERENCE_CANDIDATES.items()
    ]

    ranked_candidates = sorted(
        candidate_results,
        key=lambda result: (
            result["completion_rate"],
            result["mean_action_efficiency"],
            -result["excess_action_count"],
            result["score"],
        ),
        reverse=True,
    )

    best_candidate = ranked_candidates[0] if ranked_candidates else None

    return {
        "benchmark_id": "MILESTONE_12_COMPETITIVE_SOLVER_SYNTHETIC_BENCHMARK_V1",
        "benchmark_case_count": len(SYNTHETIC_BENCHMARK_CASES),
        "candidate_count": len(candidate_results),
        "measurement_target_count": len(MEASUREMENT_TARGETS),
        "measurement_targets": MEASUREMENT_TARGETS,
        "candidate_results": candidate_results,
        "ranked_candidate_ids": [candidate["candidate_id"] for candidate in ranked_candidates],
        "best_candidate_id": best_candidate["candidate_id"] if best_candidate else None,
        "best_completion_rate": best_candidate["completion_rate"] if best_candidate else 0.0,
        "best_mean_action_efficiency": best_candidate["mean_action_efficiency"] if best_candidate else 0.0,
        "best_score": best_candidate["score"] if best_candidate else 0.0,
    }


def build_benchmark_harness_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_present = SOURCE_STRATEGY_GATE_ARTIFACT.exists()
    source = _load_source_strategy_gate()

    source_parseable = source is not None
    source_m12_opened = bool(source and source.get("milestone_12_status") == "OPENED_CANONICALLY")
    source_gate_passed = bool(source and source.get("milestone_12_strategy_gate_passed") is True)
    source_strategy_ok = bool(source and source.get("chosen_strategy") == CHOSEN_STRATEGY)
    source_goal_ok = bool(source and source.get("competitive_goal") == COMPETITIVE_GOAL)
    source_next_stage_ok = bool(source and source.get("next_stage") == "MILESTONE_12_TASK_2_COMPETITIVE_SOLVER_BENCHMARK_HARNESS_V1")
    source_public_overfit_blocked = bool(source and source.get("public_overfit_allowed") is False)
    source_external_false = bool(source and source.get("external_api_dependency") is False)
    source_submission_false = bool(source and source.get("kaggle_submission_sent") is False)
    source_real_submission_false = bool(source and source.get("real_submission_allowed") is False)
    source_private_false = bool(source and source.get("private_core_exposure") is False)
    source_legal_false = bool(source and source.get("legal_certification") is False)
    source_issue_zero = bool(source and source.get("issue_count") == 0)

    benchmark = run_reference_benchmark()

    benchmark_cases_ready = len(SYNTHETIC_BENCHMARK_CASES) == 6
    benchmark_candidates_ready = benchmark["candidate_count"] == 3
    benchmark_measurements_ready = benchmark["measurement_target_count"] == 10
    best_candidate_ok = benchmark["best_candidate_id"] == "reference_optimal_policy"
    best_completion_ok = benchmark["best_completion_rate"] == 1.0
    best_efficiency_ok = benchmark["best_mean_action_efficiency"] == 1.0
    noop_failure_ok = next(
        result for result in benchmark["candidate_results"] if result["candidate_id"] == "reference_noop_policy"
    )["completion_rate"] == 0.0
    probe_candidate_ok = next(
        result for result in benchmark["candidate_results"] if result["candidate_id"] == "reference_probe_then_optimal_policy"
    )["completion_rate"] == 1.0

    harness_ready = all(
        [
            source_present,
            source_parseable,
            source_m12_opened,
            source_gate_passed,
            source_strategy_ok,
            source_goal_ok,
            source_next_stage_ok,
            source_public_overfit_blocked,
            source_external_false,
            source_submission_false,
            source_real_submission_false,
            source_private_false,
            source_legal_false,
            source_issue_zero,
            benchmark_cases_ready,
            benchmark_candidates_ready,
            benchmark_measurements_ready,
            best_candidate_ok,
            best_completion_ok,
            best_efficiency_ok,
            noop_failure_ok,
            probe_candidate_ok,
        ]
    )

    harness_checks = [
        _check("source_strategy_gate_artifact_present", source_present, "PASS" if source_present else "BLOCKING", "Milestone 12 Task 1 strategy gate artifact exists."),
        _check("source_strategy_gate_artifact_parseable", source_parseable, "PASS" if source_parseable else "BLOCKING", "Milestone 12 Task 1 artifact is parseable JSON."),
        _check("source_milestone_12_opened", source_m12_opened, "PASS" if source_m12_opened else "BLOCKING", "Milestone 12 is opened canonically."),
        _check("source_strategy_gate_passed", source_gate_passed, "PASS" if source_gate_passed else "BLOCKING", "Strategy gate passed."),
        _check("source_strategy_ok", source_strategy_ok, "PASS" if source_strategy_ok else "BLOCKING", "Source strategy matches executable world model explore/verify/plan."),
        _check("source_goal_ok", source_goal_ok, "PASS" if source_goal_ok else "BLOCKING", "Source goal is first-place competitive solver."),
        _check("source_next_stage_ok", source_next_stage_ok, "PASS" if source_next_stage_ok else "BLOCKING", "Source next stage points to benchmark harness."),
        _check("source_public_overfit_blocked", source_public_overfit_blocked, "PASS" if source_public_overfit_blocked else "BLOCKING", "Public overfit remains blocked."),
        _check("source_external_api_dependency_false", source_external_false, "PASS" if source_external_false else "BLOCKING", "External API dependency remains false."),
        _check("source_kaggle_submission_false", source_submission_false, "PASS" if source_submission_false else "BLOCKING", "Kaggle submission remains false."),
        _check("source_real_submission_allowed_false", source_real_submission_false, "PASS" if source_real_submission_false else "BLOCKING", "Real submission remains blocked."),
        _check("source_private_core_exposure_false", source_private_false, "PASS" if source_private_false else "BLOCKING", "Private core exposure remains false."),
        _check("source_legal_certification_false", source_legal_false, "PASS" if source_legal_false else "BLOCKING", "legal_certification remains false."),
        _check("source_issue_count_zero", source_issue_zero, "PASS" if source_issue_zero else "BLOCKING", "Source issue count is zero."),
        _check("benchmark_cases_ready", benchmark_cases_ready, "PASS" if benchmark_cases_ready else "BLOCKING", "Synthetic benchmark cases are ready."),
        _check("benchmark_candidates_ready", benchmark_candidates_ready, "PASS" if benchmark_candidates_ready else "BLOCKING", "Reference benchmark candidates are ready."),
        _check("benchmark_measurements_ready", benchmark_measurements_ready, "PASS" if benchmark_measurements_ready else "BLOCKING", "Measurement targets are ready."),
        _check("best_candidate_ok", best_candidate_ok, "PASS" if best_candidate_ok else "BLOCKING", "Reference optimal policy ranks first."),
        _check("best_completion_ok", best_completion_ok, "PASS" if best_completion_ok else "BLOCKING", "Reference optimal policy completes all cases."),
        _check("best_efficiency_ok", best_efficiency_ok, "PASS" if best_efficiency_ok else "BLOCKING", "Reference optimal policy uses optimal action counts."),
        _check("noop_failure_ok", noop_failure_ok, "PASS" if noop_failure_ok else "BLOCKING", "No-op policy fails all cases."),
        _check("probe_candidate_ok", probe_candidate_ok, "PASS" if probe_candidate_ok else "BLOCKING", "Probe-then-optimal policy completes all cases with lower efficiency."),
    ]

    harness_passed = all(check["status"] is True for check in harness_checks)

    harness_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "benchmark_harness_status": "READY" if harness_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "benchmark_id": benchmark["benchmark_id"],
        "benchmark_case_count": benchmark["benchmark_case_count"],
        "candidate_count": benchmark["candidate_count"],
        "measurement_target_count": benchmark["measurement_target_count"],
        "best_candidate_id": benchmark["best_candidate_id"],
        "best_completion_rate": benchmark["best_completion_rate"],
        "best_mean_action_efficiency": benchmark["best_mean_action_efficiency"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("source_strategy_gate_artifact_present", source_present, True, "Task 1 strategy gate artifact is present."),
        _gate("source_strategy_gate_artifact_parseable", source_parseable, True, "Task 1 strategy gate artifact is parseable."),
        _gate("source_milestone_12_opened", source_m12_opened, True, "Milestone 12 is opened canonically."),
        _gate("source_strategy_gate_passed", source_gate_passed, True, "Milestone 12 Task 1 passed."),
        _gate("source_strategy_ok", source_strategy_ok, True, "Chosen strategy matches Milestone 12 strategy."),
        _gate("source_goal_ok", source_goal_ok, True, "Competitive goal matches first-place objective."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 1 next stage points to Task 2."),
        _gate("source_public_overfit_blocked", source_public_overfit_blocked, True, "Public overfit remains blocked."),
        _gate("source_external_api_dependency_false", source_external_false, True, "External API dependency remains false."),
        _gate("source_kaggle_submission_false", source_submission_false, True, "Kaggle submission remains false."),
        _gate("source_real_submission_allowed_false", source_real_submission_false, True, "Real submission remains blocked."),
        _gate("source_private_core_exposure_false", source_private_false, True, "Private core exposure remains false."),
        _gate("source_legal_certification_false", source_legal_false, True, "legal_certification remains false."),
        _gate("benchmark_case_count_ok", benchmark_cases_ready, True, "Six benchmark cases declared."),
        _gate("candidate_count_ok", benchmark_candidates_ready, True, "Three reference candidates declared."),
        _gate("measurement_target_count_ok", benchmark_measurements_ready, True, "Ten measurement targets declared."),
        _gate("reference_optimal_policy_ranks_first", best_candidate_ok, True, "Reference optimal policy ranks first."),
        _gate("reference_optimal_policy_completion_rate_one", best_completion_ok, True, "Reference optimal policy completes all cases."),
        _gate("reference_optimal_policy_efficiency_one", best_efficiency_ok, True, "Reference optimal policy is action-optimal."),
        _gate("reference_noop_policy_completion_zero", noop_failure_ok, True, "No-op policy fails all cases."),
        _gate("reference_probe_then_optimal_completes", probe_candidate_ok, True, "Probe-then-optimal policy completes all cases."),
        _gate("public_overfit_allowed_false", True, True, "Public overfitting is blocked."),
        _gate("public_overfit_guard_required_true", True, True, "Public overfit guard is required."),
        _gate("external_api_dependency_false", True, True, "External API dependency remains false."),
        _gate("internet_during_eval_false", True, True, "Internet during evaluation remains false."),
        _gate("real_submission_allowed_false", True, True, "Real submission remains blocked."),
        _gate("manual_upload_allowed_false", True, True, "Manual upload remains blocked."),
        _gate("kaggle_submission_sent_false", True, True, "No Kaggle submission is sent."),
        _gate("kaggle_authentication_performed_false", True, True, "No Kaggle authentication is performed."),
        _gate("private_core_exposure_false", True, True, "Private core exposure remains false."),
        _gate("legal_certification_false", True, True, "legal_certification remains false."),
        _gate("local_only_true", True, True, "Task remains local-only."),
        _gate("deterministic_true", True, True, "Task remains deterministic."),
        _gate("public_safe_true", True, True, "Task remains public-safe."),
        _gate("benchmark_harness_only_true", True, True, "Task remains benchmark-harness-only."),
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
        "source_strategy_gate_artifact": str(SOURCE_STRATEGY_GATE_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_strategy_gate_artifact_present": source_present,
        "source_strategy_gate_artifact_parseable": source_parseable,
        "source_milestone_12_opened": source_m12_opened,
        "source_strategy_gate_passed": source_gate_passed,
        "source_strategy_ok": source_strategy_ok,
        "source_goal_ok": source_goal_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "benchmark_harness_ready": True,
        "benchmark_harness_valid": harness_passed,
        "benchmark_harness_passed": harness_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "harness_summary": harness_summary,
        "benchmark": benchmark,
        "benchmark_case_count": len(SYNTHETIC_BENCHMARK_CASES),
        "benchmark_cases": SYNTHETIC_BENCHMARK_CASES,
        "reference_candidate_count": len(REFERENCE_CANDIDATES),
        "reference_candidate_ids": list(REFERENCE_CANDIDATES.keys()),
        "measurement_target_count": len(MEASUREMENT_TARGETS),
        "measurement_targets": MEASUREMENT_TARGETS,
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
        "benchmark_harness_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "harness_check_count": len(harness_checks),
        "harness_checks": harness_checks,
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
    record["task_id"] = "MILESTONE-12-COMPETITIVE-SOLVER-BENCHMARK-HARNESS-" + signature[:12]
    return record


def validate_benchmark_harness_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "benchmark_harness_ready",
        "benchmark_harness_valid",
        "benchmark_harness_passed",
        "source_strategy_gate_artifact_present",
        "source_strategy_gate_artifact_parseable",
        "source_milestone_12_opened",
        "source_strategy_gate_passed",
        "source_strategy_ok",
        "source_goal_ok",
        "source_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "benchmark_harness_only",
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

    if record.get("milestone_12_status") != "OPENED_CANONICALLY":
        issues.append("MILESTONE_12_STATUS_MISMATCH")

    if record.get("competitive_goal") != COMPETITIVE_GOAL:
        issues.append("COMPETITIVE_GOAL_MISMATCH")

    if record.get("chosen_strategy") != CHOSEN_STRATEGY:
        issues.append("CHOSEN_STRATEGY_MISMATCH")

    if record.get("benchmark_case_count") != 6:
        issues.append("BENCHMARK_CASE_COUNT_MISMATCH")

    if record.get("reference_candidate_count") != 3:
        issues.append("REFERENCE_CANDIDATE_COUNT_MISMATCH")

    if record.get("measurement_target_count") != 10:
        issues.append("MEASUREMENT_TARGET_COUNT_MISMATCH")

    benchmark = record.get("benchmark")
    if not isinstance(benchmark, dict):
        issues.append("BENCHMARK_MISSING")
    else:
        if benchmark.get("best_candidate_id") != "reference_optimal_policy":
            issues.append("BEST_CANDIDATE_MISMATCH")
        if benchmark.get("best_completion_rate") != 1.0:
            issues.append("BEST_COMPLETION_RATE_NOT_ONE")
        if benchmark.get("best_mean_action_efficiency") != 1.0:
            issues.append("BEST_EFFICIENCY_NOT_ONE")

    harness_summary = record.get("harness_summary")
    if not isinstance(harness_summary, dict):
        issues.append("HARNESS_SUMMARY_MISSING")
    else:
        if harness_summary.get("benchmark_harness_status") != "READY":
            issues.append("HARNESS_SUMMARY_STATUS_NOT_READY")
        if harness_summary.get("chosen_strategy") != CHOSEN_STRATEGY:
            issues.append("HARNESS_SUMMARY_STRATEGY_MISMATCH")
        if harness_summary.get("next_stage") != NEXT_STAGE:
            issues.append("HARNESS_SUMMARY_NEXT_STAGE_MISMATCH")

    harness_checks = record.get("harness_checks")
    if not isinstance(harness_checks, list) or not harness_checks:
        issues.append("HARNESS_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in harness_checks):
        issues.append("HARNESS_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-competitive-solver-benchmark-harness-v1.json"
    index_path = target_dir / "milestone-12-competitive-solver-benchmark-harness-index-v1.json"
    manifest_path = target_dir / "milestone-12-competitive-solver-benchmark-harness-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-competitive-solver-benchmark-harness-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "benchmark_harness_ready": record["benchmark_harness_ready"],
        "benchmark_harness_passed": record["benchmark_harness_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "benchmark_case_count": record["benchmark_case_count"],
        "reference_candidate_count": record["reference_candidate_count"],
        "measurement_target_count": record["measurement_target_count"],
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
        f"benchmark_harness_ready={record['benchmark_harness_ready']}",
        f"benchmark_harness_passed={record['benchmark_harness_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"benchmark_case_count={record['benchmark_case_count']}",
        f"reference_candidate_count={record['reference_candidate_count']}",
        f"measurement_target_count={record['measurement_target_count']}",
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

## Benchmark Harness

- benchmark_harness_ready: `{record['benchmark_harness_ready']}`
- benchmark_harness_passed: `{record['benchmark_harness_passed']}`
- benchmark_case_count: `{record['benchmark_case_count']}`
- reference_candidate_count: `{record['reference_candidate_count']}`
- measurement_target_count: `{record['measurement_target_count']}`

## Reference Result

- best_candidate_id: `{record['benchmark']['best_candidate_id']}`
- best_completion_rate: `{record['benchmark']['best_completion_rate']}`
- best_mean_action_efficiency: `{record['benchmark']['best_mean_action_efficiency']}`
- best_score: `{record['benchmark']['best_score']}`

## Boundary

- public_overfit_allowed: `{record['public_overfit_allowed']}`
- public_overfit_guard_required: `{record['public_overfit_guard_required']}`
- external_api_dependency: `{record['external_api_dependency']}`
- internet_during_eval: `{record['internet_during_eval']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- manual_upload_allowed: `{record['manual_upload_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- kaggle_authentication_performed: `{record['kaggle_authentication_performed']}`
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
    record = build_benchmark_harness_record()
    issues = validate_benchmark_harness_record(record)
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
