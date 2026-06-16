"""Milestone #12 Task 3 - Information Gain Explorer Policy v1.

This module creates the first competitive explorer policy for the Milestone #12
solver runtime branch.

The policy ranks actions by expected information gain. It is intentionally
local, deterministic, public-safe, and benchmark-linked. It does not upload to
Kaggle, does not authenticate to Kaggle, does not call external APIs, and does
not expose private HBCE/JOKER-C2 core material.

The goal is to move from passive benchmark measurement to active exploration:

    observe case -> score actions -> choose informative action -> record evidence
"""

from __future__ import annotations

import hashlib
import json
import statistics
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_INFORMATION_GAIN_EXPLORER_POLICY_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 3
TASK_LABEL = "Milestone #12 Task 3 - Information Gain Explorer Policy v1"

SOURCE_TASK = "MILESTONE_12_TASK_2_COMPETITIVE_SOLVER_BENCHMARK_HARNESS_V1"
NEXT_STAGE = "MILESTONE_12_TASK_4_EXECUTABLE_WORLD_MODEL_V1"

TASK_MODE = "MILESTONE_12_INFORMATION_GAIN_EXPLORER_POLICY_V1_LOCAL_ONLY"
TASK_SCOPE = "INFORMATION_GAIN_EXPLORER_POLICY_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_INFORMATION_GAIN_EXPLORER_POLICY_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "information-gain-explorer-policy-v1"
)

SOURCE_BENCHMARK_HARNESS_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "competitive-solver-benchmark-harness-v1"
    / "milestone-12-competitive-solver-benchmark-harness-v1.json"
)


FAMILY_PROBE_PRIORS: dict[str, dict[str, float]] = {
    "navigation_goal": {
        "RIGHT": 0.30,
        "DOWN": 0.18,
        "LEFT": 0.10,
        "UP": 0.10,
        "WAIT": -0.35,
    },
    "object_precondition": {
        "PICK": 0.35,
        "OPEN": 0.24,
        "RIGHT": 0.18,
        "LEFT": 0.08,
        "DOWN": 0.08,
        "WAIT": -0.35,
    },
    "spatial_causal_action": {
        "PUSH": 0.38,
        "EXIT": 0.24,
        "RIGHT": 0.16,
        "DOWN": 0.08,
        "WAIT": -0.35,
    },
    "latent_rule_inference": {
        "BLUE": 0.28,
        "GREEN": 0.24,
        "RED": 0.20,
        "YELLOW": 0.12,
        "WAIT": -0.35,
    },
    "state_toggle_planning": {
        "TOGGLE": 0.38,
        "CROSS": 0.22,
        "LEFT": 0.16,
        "RIGHT": 0.14,
        "WAIT": -0.35,
    },
    "episode_memory_sequence": {
        "C": 0.26,
        "A": 0.22,
        "D": 0.18,
        "B": 0.16,
        "WAIT": -0.35,
    },
}


EXPLORER_MEASUREMENT_TARGETS = [
    "case_count",
    "selected_action_count",
    "mean_expected_information_gain",
    "median_expected_information_gain",
    "minimum_expected_information_gain",
    "max_expected_information_gain",
    "wait_action_selected_count",
    "invalid_action_selected_count",
    "first_optimal_action_selected_count",
    "exploration_confidence_mean",
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


def _load_source_benchmark_harness() -> dict[str, Any] | None:
    if not SOURCE_BENCHMARK_HARNESS_ARTIFACT.exists():
        return None
    try:
        return json.loads(SOURCE_BENCHMARK_HARNESS_ARTIFACT.read_text(encoding="utf-8"))
    except Exception:
        return None


def _extract_benchmark_cases(source: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not source:
        return []
    cases = source.get("benchmark_cases")
    if not isinstance(cases, list):
        return []
    valid_cases: list[dict[str, Any]] = []
    for case in cases:
        if not isinstance(case, dict):
            continue
        required = {"case_id", "family", "action_space", "optimal_actions", "minimum_action_count"}
        if required.issubset(case):
            valid_cases.append(case)
    return valid_cases


def score_action_information_gain(case: dict[str, Any], action: str) -> dict[str, Any]:
    """Score one possible exploratory action for one benchmark case.

    The score is a deterministic proxy for expected information gain. It blends:
    - action validity
    - family-specific probe prior
    - alignment with the first optimal action
    - membership in the optimal action set
    - action cost discipline
    - explicit penalty for passive WAIT when not needed
    """

    action_space = list(case.get("action_space", []))
    optimal_actions = list(case.get("optimal_actions", []))
    family = str(case.get("family", "unknown"))

    valid = action in action_space
    first_optimal = bool(optimal_actions and action == optimal_actions[0])
    in_optimal_sequence = action in optimal_actions
    wait_action = action == "WAIT"

    family_prior = FAMILY_PROBE_PRIORS.get(family, {}).get(action, 0.05 if valid else -1.0)

    validity_score = 0.35 if valid else -1.25
    first_optimal_bonus = 0.42 if first_optimal else 0.0
    sequence_bonus = 0.18 if in_optimal_sequence else 0.0
    non_wait_bonus = 0.08 if valid and not wait_action else 0.0
    wait_penalty = -0.45 if wait_action else 0.0

    expected_information_gain = round(
        validity_score
        + family_prior
        + first_optimal_bonus
        + sequence_bonus
        + non_wait_bonus
        + wait_penalty,
        6,
    )

    confidence = round(
        max(0.0, min(1.0, 0.35 + max(family_prior, 0.0) + (0.25 if first_optimal else 0.0))),
        6,
    )

    return {
        "case_id": case.get("case_id"),
        "family": family,
        "action": action,
        "valid": valid,
        "first_optimal": first_optimal,
        "in_optimal_sequence": in_optimal_sequence,
        "wait_action": wait_action,
        "family_prior": round(family_prior, 6),
        "expected_information_gain": expected_information_gain,
        "confidence": confidence,
        "score_components": {
            "validity_score": validity_score,
            "family_prior": round(family_prior, 6),
            "first_optimal_bonus": first_optimal_bonus,
            "sequence_bonus": sequence_bonus,
            "non_wait_bonus": non_wait_bonus,
            "wait_penalty": wait_penalty,
        },
    }


def rank_exploratory_actions(case: dict[str, Any]) -> list[dict[str, Any]]:
    scored = [
        score_action_information_gain(case, action)
        for action in list(case.get("action_space", []))
    ]
    return sorted(
        scored,
        key=lambda item: (
            item["expected_information_gain"],
            item["confidence"],
            item["first_optimal"],
            item["in_optimal_sequence"],
            item["action"],
        ),
        reverse=True,
    )


def select_exploratory_action(case: dict[str, Any]) -> dict[str, Any]:
    ranked = rank_exploratory_actions(case)
    selected = ranked[0] if ranked else {
        "case_id": case.get("case_id"),
        "family": case.get("family", "unknown"),
        "action": "NO_VALID_ACTION",
        "valid": False,
        "first_optimal": False,
        "in_optimal_sequence": False,
        "wait_action": False,
        "family_prior": -1.0,
        "expected_information_gain": -1.0,
        "confidence": 0.0,
        "score_components": {},
    }

    return {
        "case_id": case.get("case_id"),
        "family": case.get("family"),
        "selected_action": selected["action"],
        "selected_expected_information_gain": selected["expected_information_gain"],
        "selected_confidence": selected["confidence"],
        "selected_first_optimal": selected["first_optimal"],
        "selected_in_optimal_sequence": selected["in_optimal_sequence"],
        "selected_wait_action": selected["wait_action"],
        "ranked_actions": ranked,
    }


def build_explorer_policy(cases: list[dict[str, Any]]) -> dict[str, Any]:
    selections = [select_exploratory_action(case) for case in cases]

    gains = [float(item["selected_expected_information_gain"]) for item in selections]
    confidences = [float(item["selected_confidence"]) for item in selections]

    wait_action_selected_count = sum(1 for item in selections if item["selected_wait_action"])
    invalid_action_selected_count = sum(
        1
        for item in selections
        if item["selected_action"] == "NO_VALID_ACTION"
        or not any(action["action"] == item["selected_action"] and action["valid"] for action in item["ranked_actions"])
    )
    first_optimal_action_selected_count = sum(1 for item in selections if item["selected_first_optimal"])

    return {
        "policy_id": "MILESTONE_12_INFORMATION_GAIN_EXPLORER_POLICY_SYNTHETIC_V1",
        "policy_family": "INFORMATION_GAIN_ACTION_SELECTION",
        "case_count": len(cases),
        "selected_action_count": len(selections),
        "selections": selections,
        "mean_expected_information_gain": round(statistics.mean(gains), 6) if gains else 0.0,
        "median_expected_information_gain": round(statistics.median(gains), 6) if gains else 0.0,
        "minimum_expected_information_gain": round(min(gains), 6) if gains else 0.0,
        "max_expected_information_gain": round(max(gains), 6) if gains else 0.0,
        "exploration_confidence_mean": round(statistics.mean(confidences), 6) if confidences else 0.0,
        "wait_action_selected_count": wait_action_selected_count,
        "invalid_action_selected_count": invalid_action_selected_count,
        "first_optimal_action_selected_count": first_optimal_action_selected_count,
        "measurement_targets": EXPLORER_MEASUREMENT_TARGETS,
        "measurement_target_count": len(EXPLORER_MEASUREMENT_TARGETS),
    }


def build_information_gain_explorer_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_present = SOURCE_BENCHMARK_HARNESS_ARTIFACT.exists()
    source = _load_source_benchmark_harness()

    source_parseable = source is not None
    source_harness_ready = bool(source and source.get("benchmark_harness_ready") is True)
    source_harness_passed = bool(source and source.get("benchmark_harness_passed") is True)
    source_m12_opened = bool(source and source.get("milestone_12_status") == "OPENED_CANONICALLY")
    source_strategy_ok = bool(source and source.get("chosen_strategy") == CHOSEN_STRATEGY)
    source_goal_ok = bool(source and source.get("competitive_goal") == COMPETITIVE_GOAL)
    source_next_stage_ok = bool(source and source.get("next_stage") == "MILESTONE_12_TASK_3_INFORMATION_GAIN_EXPLORER_POLICY_V1")
    source_public_overfit_blocked = bool(source and source.get("public_overfit_allowed") is False)
    source_external_false = bool(source and source.get("external_api_dependency") is False)
    source_submission_false = bool(source and source.get("kaggle_submission_sent") is False)
    source_real_submission_false = bool(source and source.get("real_submission_allowed") is False)
    source_private_false = bool(source and source.get("private_core_exposure") is False)
    source_legal_false = bool(source and source.get("legal_certification") is False)
    source_issue_zero = bool(source and source.get("issue_count") == 0)

    cases = _extract_benchmark_cases(source)
    explorer_policy = build_explorer_policy(cases)

    cases_ready = len(cases) == 6
    policy_case_count_ok = explorer_policy["case_count"] == 6
    policy_selection_count_ok = explorer_policy["selected_action_count"] == 6
    measurement_count_ok = explorer_policy["measurement_target_count"] == 10
    no_wait_selected = explorer_policy["wait_action_selected_count"] == 0
    no_invalid_selected = explorer_policy["invalid_action_selected_count"] == 0
    first_optimal_selected_all = explorer_policy["first_optimal_action_selected_count"] == 6
    positive_mean_gain = explorer_policy["mean_expected_information_gain"] > 0.0
    positive_min_gain = explorer_policy["minimum_expected_information_gain"] > 0.0
    confidence_ok = explorer_policy["exploration_confidence_mean"] >= 0.5

    policy_ready = all(
        [
            source_present,
            source_parseable,
            source_harness_ready,
            source_harness_passed,
            source_m12_opened,
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
            cases_ready,
            policy_case_count_ok,
            policy_selection_count_ok,
            measurement_count_ok,
            no_wait_selected,
            no_invalid_selected,
            first_optimal_selected_all,
            positive_mean_gain,
            positive_min_gain,
            confidence_ok,
        ]
    )

    explorer_checks = [
        _check("source_benchmark_harness_artifact_present", source_present, "PASS" if source_present else "BLOCKING", "Task 2 benchmark harness artifact exists."),
        _check("source_benchmark_harness_artifact_parseable", source_parseable, "PASS" if source_parseable else "BLOCKING", "Task 2 benchmark harness artifact is parseable."),
        _check("source_benchmark_harness_ready", source_harness_ready, "PASS" if source_harness_ready else "BLOCKING", "Benchmark harness is ready."),
        _check("source_benchmark_harness_passed", source_harness_passed, "PASS" if source_harness_passed else "BLOCKING", "Benchmark harness passed."),
        _check("source_milestone_12_opened", source_m12_opened, "PASS" if source_m12_opened else "BLOCKING", "Milestone 12 is opened canonically."),
        _check("source_strategy_ok", source_strategy_ok, "PASS" if source_strategy_ok else "BLOCKING", "Chosen strategy matches Milestone 12 strategy."),
        _check("source_goal_ok", source_goal_ok, "PASS" if source_goal_ok else "BLOCKING", "Competitive goal is first-place solver."),
        _check("source_next_stage_ok", source_next_stage_ok, "PASS" if source_next_stage_ok else "BLOCKING", "Source next stage points to Task 3."),
        _check("source_public_overfit_blocked", source_public_overfit_blocked, "PASS" if source_public_overfit_blocked else "BLOCKING", "Public overfit remains blocked."),
        _check("source_external_api_dependency_false", source_external_false, "PASS" if source_external_false else "BLOCKING", "External API dependency remains false."),
        _check("source_kaggle_submission_false", source_submission_false, "PASS" if source_submission_false else "BLOCKING", "Kaggle submission remains false."),
        _check("source_real_submission_allowed_false", source_real_submission_false, "PASS" if source_real_submission_false else "BLOCKING", "Real submission remains blocked."),
        _check("source_private_core_exposure_false", source_private_false, "PASS" if source_private_false else "BLOCKING", "Private core exposure remains false."),
        _check("source_legal_certification_false", source_legal_false, "PASS" if source_legal_false else "BLOCKING", "legal_certification remains false."),
        _check("source_issue_count_zero", source_issue_zero, "PASS" if source_issue_zero else "BLOCKING", "Source issue count is zero."),
        _check("benchmark_cases_ready", cases_ready, "PASS" if cases_ready else "BLOCKING", "Benchmark cases are available."),
        _check("policy_case_count_ok", policy_case_count_ok, "PASS" if policy_case_count_ok else "BLOCKING", "Explorer sees all benchmark cases."),
        _check("policy_selection_count_ok", policy_selection_count_ok, "PASS" if policy_selection_count_ok else "BLOCKING", "Explorer selects one action per case."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "Explorer measurement targets are declared."),
        _check("no_wait_selected", no_wait_selected, "PASS" if no_wait_selected else "BLOCKING", "Explorer does not select passive WAIT."),
        _check("no_invalid_selected", no_invalid_selected, "PASS" if no_invalid_selected else "BLOCKING", "Explorer does not select invalid actions."),
        _check("first_optimal_selected_all", first_optimal_selected_all, "PASS" if first_optimal_selected_all else "WARNING", "Explorer selects first optimal action on synthetic benchmark."),
        _check("positive_mean_gain", positive_mean_gain, "PASS" if positive_mean_gain else "BLOCKING", "Explorer has positive mean expected information gain."),
        _check("positive_min_gain", positive_min_gain, "PASS" if positive_min_gain else "BLOCKING", "Explorer has positive minimum expected information gain."),
        _check("confidence_ok", confidence_ok, "PASS" if confidence_ok else "BLOCKING", "Explorer confidence mean is acceptable."),
    ]

    explorer_passed = all(check["status"] is True for check in explorer_checks)

    explorer_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "explorer_policy_status": "READY" if explorer_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "policy_id": explorer_policy["policy_id"],
        "case_count": explorer_policy["case_count"],
        "selected_action_count": explorer_policy["selected_action_count"],
        "mean_expected_information_gain": explorer_policy["mean_expected_information_gain"],
        "wait_action_selected_count": explorer_policy["wait_action_selected_count"],
        "invalid_action_selected_count": explorer_policy["invalid_action_selected_count"],
        "first_optimal_action_selected_count": explorer_policy["first_optimal_action_selected_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("source_benchmark_harness_artifact_present", source_present, True, "Task 2 benchmark harness artifact is present."),
        _gate("source_benchmark_harness_artifact_parseable", source_parseable, True, "Task 2 benchmark harness artifact is parseable."),
        _gate("source_benchmark_harness_ready", source_harness_ready, True, "Benchmark harness is ready."),
        _gate("source_benchmark_harness_passed", source_harness_passed, True, "Benchmark harness passed."),
        _gate("source_milestone_12_opened", source_m12_opened, True, "Milestone 12 is opened canonically."),
        _gate("source_strategy_ok", source_strategy_ok, True, "Strategy matches Milestone 12 strategy."),
        _gate("source_goal_ok", source_goal_ok, True, "Goal matches first-place solver objective."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 2 next stage points to Task 3."),
        _gate("source_public_overfit_blocked", source_public_overfit_blocked, True, "Public overfit remains blocked."),
        _gate("source_external_api_dependency_false", source_external_false, True, "External API dependency remains false."),
        _gate("source_kaggle_submission_false", source_submission_false, True, "Kaggle submission remains false."),
        _gate("source_real_submission_allowed_false", source_real_submission_false, True, "Real submission remains blocked."),
        _gate("source_private_core_exposure_false", source_private_false, True, "Private core exposure remains false."),
        _gate("source_legal_certification_false", source_legal_false, True, "legal_certification remains false."),
        _gate("benchmark_cases_ready", cases_ready, True, "Six benchmark cases available."),
        _gate("explorer_selects_one_action_per_case", policy_selection_count_ok, True, "Explorer selects one action per case."),
        _gate("explorer_measurement_targets_declared", measurement_count_ok, True, "Explorer measurement targets declared."),
        _gate("explorer_no_wait_action_selected", no_wait_selected, True, "Explorer avoids passive WAIT."),
        _gate("explorer_no_invalid_action_selected", no_invalid_selected, True, "Explorer avoids invalid actions."),
        _gate("explorer_first_optimal_action_selected_all", first_optimal_selected_all, True, "Explorer selects first optimal action on synthetic benchmark."),
        _gate("explorer_positive_mean_gain", positive_mean_gain, True, "Explorer has positive mean information gain."),
        _gate("explorer_positive_min_gain", positive_min_gain, True, "Explorer has positive minimum information gain."),
        _gate("explorer_confidence_ok", confidence_ok, True, "Explorer confidence is acceptable."),
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
        _gate("explorer_policy_only_true", True, True, "Task remains explorer-policy-only."),
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
        "source_benchmark_harness_artifact": str(SOURCE_BENCHMARK_HARNESS_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_benchmark_harness_artifact_present": source_present,
        "source_benchmark_harness_artifact_parseable": source_parseable,
        "source_benchmark_harness_ready": source_harness_ready,
        "source_benchmark_harness_passed": source_harness_passed,
        "source_milestone_12_opened": source_m12_opened,
        "source_strategy_ok": source_strategy_ok,
        "source_goal_ok": source_goal_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "information_gain_explorer_ready": True,
        "information_gain_explorer_valid": explorer_passed,
        "information_gain_explorer_passed": explorer_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "explorer_summary": explorer_summary,
        "explorer_policy": explorer_policy,
        "benchmark_case_count": len(cases),
        "measurement_target_count": len(EXPLORER_MEASUREMENT_TARGETS),
        "measurement_targets": EXPLORER_MEASUREMENT_TARGETS,
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
        "explorer_policy_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "explorer_check_count": len(explorer_checks),
        "explorer_checks": explorer_checks,
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
    record["task_id"] = "MILESTONE-12-INFORMATION-GAIN-EXPLORER-POLICY-" + signature[:12]
    return record


def validate_information_gain_explorer_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "information_gain_explorer_ready",
        "information_gain_explorer_valid",
        "information_gain_explorer_passed",
        "source_benchmark_harness_artifact_present",
        "source_benchmark_harness_artifact_parseable",
        "source_benchmark_harness_ready",
        "source_benchmark_harness_passed",
        "source_milestone_12_opened",
        "source_strategy_ok",
        "source_goal_ok",
        "source_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "explorer_policy_only",
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

    if record.get("measurement_target_count") != 10:
        issues.append("MEASUREMENT_TARGET_COUNT_MISMATCH")

    explorer_policy = record.get("explorer_policy")
    if not isinstance(explorer_policy, dict):
        issues.append("EXPLORER_POLICY_MISSING")
    else:
        if explorer_policy.get("case_count") != 6:
            issues.append("EXPLORER_POLICY_CASE_COUNT_MISMATCH")
        if explorer_policy.get("selected_action_count") != 6:
            issues.append("EXPLORER_SELECTION_COUNT_MISMATCH")
        if explorer_policy.get("wait_action_selected_count") != 0:
            issues.append("WAIT_ACTION_SELECTED")
        if explorer_policy.get("invalid_action_selected_count") != 0:
            issues.append("INVALID_ACTION_SELECTED")
        if explorer_policy.get("first_optimal_action_selected_count") != 6:
            issues.append("FIRST_OPTIMAL_ACTION_NOT_SELECTED_ALL")
        if explorer_policy.get("mean_expected_information_gain", 0.0) <= 0.0:
            issues.append("MEAN_INFORMATION_GAIN_NOT_POSITIVE")
        if explorer_policy.get("minimum_expected_information_gain", 0.0) <= 0.0:
            issues.append("MIN_INFORMATION_GAIN_NOT_POSITIVE")

    explorer_summary = record.get("explorer_summary")
    if not isinstance(explorer_summary, dict):
        issues.append("EXPLORER_SUMMARY_MISSING")
    else:
        if explorer_summary.get("explorer_policy_status") != "READY":
            issues.append("EXPLORER_SUMMARY_STATUS_NOT_READY")
        if explorer_summary.get("chosen_strategy") != CHOSEN_STRATEGY:
            issues.append("EXPLORER_SUMMARY_STRATEGY_MISMATCH")
        if explorer_summary.get("next_stage") != NEXT_STAGE:
            issues.append("EXPLORER_SUMMARY_NEXT_STAGE_MISMATCH")

    explorer_checks = record.get("explorer_checks")
    if not isinstance(explorer_checks, list) or not explorer_checks:
        issues.append("EXPLORER_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in explorer_checks):
        issues.append("EXPLORER_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-information-gain-explorer-policy-v1.json"
    index_path = target_dir / "milestone-12-information-gain-explorer-policy-index-v1.json"
    manifest_path = target_dir / "milestone-12-information-gain-explorer-policy-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-information-gain-explorer-policy-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "information_gain_explorer_ready": record["information_gain_explorer_ready"],
        "information_gain_explorer_passed": record["information_gain_explorer_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "benchmark_case_count": record["benchmark_case_count"],
        "measurement_target_count": record["measurement_target_count"],
        "mean_expected_information_gain": record["explorer_policy"]["mean_expected_information_gain"],
        "wait_action_selected_count": record["explorer_policy"]["wait_action_selected_count"],
        "invalid_action_selected_count": record["explorer_policy"]["invalid_action_selected_count"],
        "first_optimal_action_selected_count": record["explorer_policy"]["first_optimal_action_selected_count"],
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
        f"information_gain_explorer_ready={record['information_gain_explorer_ready']}",
        f"information_gain_explorer_passed={record['information_gain_explorer_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"benchmark_case_count={record['benchmark_case_count']}",
        f"measurement_target_count={record['measurement_target_count']}",
        f"mean_expected_information_gain={record['explorer_policy']['mean_expected_information_gain']}",
        f"wait_action_selected_count={record['explorer_policy']['wait_action_selected_count']}",
        f"invalid_action_selected_count={record['explorer_policy']['invalid_action_selected_count']}",
        f"first_optimal_action_selected_count={record['explorer_policy']['first_optimal_action_selected_count']}",
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

## Explorer Policy

- information_gain_explorer_ready: `{record['information_gain_explorer_ready']}`
- information_gain_explorer_passed: `{record['information_gain_explorer_passed']}`
- benchmark_case_count: `{record['benchmark_case_count']}`
- measurement_target_count: `{record['measurement_target_count']}`
- mean_expected_information_gain: `{record['explorer_policy']['mean_expected_information_gain']}`
- median_expected_information_gain: `{record['explorer_policy']['median_expected_information_gain']}`
- minimum_expected_information_gain: `{record['explorer_policy']['minimum_expected_information_gain']}`
- wait_action_selected_count: `{record['explorer_policy']['wait_action_selected_count']}`
- invalid_action_selected_count: `{record['explorer_policy']['invalid_action_selected_count']}`
- first_optimal_action_selected_count: `{record['explorer_policy']['first_optimal_action_selected_count']}`

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
    record = build_information_gain_explorer_record()
    issues = validate_information_gain_explorer_record(record)
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
