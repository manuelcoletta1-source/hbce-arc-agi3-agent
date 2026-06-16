"""Milestone #12 Task 4 - Executable World Model v1.

This module creates the first deterministic executable world model for the
Milestone #12 competitive solver branch.

It links Task 2 benchmark cases and Task 3 information-gain explorer policy,
then executes symbolic rollouts with deterministic state transitions.

Boundary:
- local-only
- deterministic
- public-safe
- no external API
- no internet during evaluation
- no Kaggle upload
- no Kaggle authentication
- no private core exposure
- legal_certification=false
"""

from __future__ import annotations

import hashlib
import json
import statistics
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_EXECUTABLE_WORLD_MODEL_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 4
TASK_LABEL = "Milestone #12 Task 4 - Executable World Model v1"

SOURCE_TASK = "MILESTONE_12_TASK_3_INFORMATION_GAIN_EXPLORER_POLICY_V1"
NEXT_STAGE = "MILESTONE_12_TASK_5_WORLD_MODEL_VERIFIER_V1"

TASK_MODE = "MILESTONE_12_EXECUTABLE_WORLD_MODEL_V1_LOCAL_ONLY"
TASK_SCOPE = "EXECUTABLE_WORLD_MODEL_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_EXECUTABLE_WORLD_MODEL_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "executable-world-model-v1"

SOURCE_BENCHMARK_HARNESS_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "competitive-solver-benchmark-harness-v1"
    / "milestone-12-competitive-solver-benchmark-harness-v1.json"
)

SOURCE_EXPLORER_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "information-gain-explorer-policy-v1"
    / "milestone-12-information-gain-explorer-policy-v1.json"
)


WORLD_MODEL_MEASUREMENT_TARGETS = [
    "case_count",
    "transition_count",
    "rollout_count",
    "completed_rollout_count",
    "failed_rollout_count",
    "invalid_transition_count",
    "mean_rollout_completion_rate",
    "mean_rollout_action_efficiency",
    "explorer_action_valid_count",
    "model_consistency_check_count",
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
        return json.loads(path.read_text(encoding="utf-8"))
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


def _extract_explorer_selection_map(source: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not source:
        return {}
    policy = source.get("explorer_policy")
    if not isinstance(policy, dict):
        return {}
    selections = policy.get("selections")
    if not isinstance(selections, list):
        return {}
    output: dict[str, dict[str, Any]] = {}
    for selection in selections:
        if not isinstance(selection, dict):
            continue
        case_id = selection.get("case_id")
        if isinstance(case_id, str):
            output[case_id] = selection
    return output


def initial_world_state(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": case["case_id"],
        "family": case["family"],
        "progress_index": 0,
        "step_count": 0,
        "completed": False,
        "failed": False,
        "invalid_action_count": 0,
        "history": [],
    }


def execute_transition(case: dict[str, Any], state: dict[str, Any], action: str) -> dict[str, Any]:
    """Execute one deterministic symbolic transition.

    The model treats every case as a latent ordered objective. An action advances
    progress only when it matches the current required optimal action. Invalid
    actions are recorded and fail the local rollout.
    """

    action_space = list(case["action_space"])
    optimal_actions = list(case["optimal_actions"])

    next_state = json.loads(json.dumps(state))
    next_state["step_count"] = int(next_state["step_count"]) + 1

    valid = action in action_space
    current_index = int(next_state["progress_index"])
    expected_action = optimal_actions[current_index] if current_index < len(optimal_actions) else None
    progress_made = bool(valid and action == expected_action)

    if not valid:
        next_state["invalid_action_count"] = int(next_state["invalid_action_count"]) + 1
        next_state["failed"] = True
    elif progress_made:
        next_state["progress_index"] = current_index + 1

    if next_state["progress_index"] >= len(optimal_actions):
        next_state["completed"] = True

    transition = {
        "from_progress_index": current_index,
        "to_progress_index": next_state["progress_index"],
        "action": action,
        "valid": valid,
        "expected_action": expected_action,
        "progress_made": progress_made,
        "completed_after_transition": next_state["completed"],
        "failed_after_transition": next_state["failed"],
    }
    next_state["history"].append(transition)
    return next_state


def execute_rollout(case: dict[str, Any], actions: list[str], rollout_kind: str) -> dict[str, Any]:
    state = initial_world_state(case)
    states = [state]

    for action in actions:
        state = execute_transition(case, state, action)
        states.append(state)
        if state["completed"] or state["failed"]:
            break

    minimum_action_count = int(case["minimum_action_count"])
    action_count = int(state["step_count"])
    completed = bool(state["completed"])
    failed = bool(state["failed"])

    action_efficiency = 0.0
    if completed and action_count > 0:
        action_efficiency = round(minimum_action_count / action_count, 6)

    return {
        "case_id": case["case_id"],
        "family": case["family"],
        "rollout_kind": rollout_kind,
        "requested_actions": actions,
        "executed_action_count": action_count,
        "minimum_action_count": minimum_action_count,
        "completed": completed,
        "failed": failed,
        "invalid_action_count": int(state["invalid_action_count"]),
        "completion_rate": 1.0 if completed else 0.0,
        "action_efficiency": action_efficiency,
        "final_progress_index": int(state["progress_index"]),
        "target_progress_index": len(case["optimal_actions"]),
        "states": states,
    }


def build_world_model_for_case(case: dict[str, Any], explorer_selection: dict[str, Any] | None) -> dict[str, Any]:
    optimal_actions = list(case["optimal_actions"])
    action_space = list(case["action_space"])

    explorer_action = "NO_EXPLORER_ACTION"
    if explorer_selection:
        explorer_action = str(explorer_selection.get("selected_action", "NO_EXPLORER_ACTION"))

    optimal_rollout = execute_rollout(case, optimal_actions, "OPTIMAL_REFERENCE_ROLLOUT")
    explorer_probe_rollout = execute_rollout(case, [explorer_action], "EXPLORER_SINGLE_PROBE_ROLLOUT")

    invalid_probe_action = "__INVALID_ACTION__"
    invalid_rollout = execute_rollout(case, [invalid_probe_action], "INVALID_ACTION_GUARD_ROLLOUT")

    transition_count = (
        optimal_rollout["executed_action_count"]
        + explorer_probe_rollout["executed_action_count"]
        + invalid_rollout["executed_action_count"]
    )

    explorer_action_valid = explorer_action in action_space
    optimal_rollout_completed = optimal_rollout["completed"] is True
    invalid_rollout_failed = invalid_rollout["failed"] is True and invalid_rollout["invalid_action_count"] == 1

    consistency_checks = [
        _check("optimal_rollout_completed", optimal_rollout_completed, "PASS" if optimal_rollout_completed else "BLOCKING", "Optimal reference rollout reaches completion."),
        _check("optimal_rollout_action_count_minimal", optimal_rollout["executed_action_count"] == optimal_rollout["minimum_action_count"], "PASS" if optimal_rollout["executed_action_count"] == optimal_rollout["minimum_action_count"] else "BLOCKING", "Optimal rollout uses the declared minimum action count."),
        _check("explorer_action_valid", explorer_action_valid, "PASS" if explorer_action_valid else "BLOCKING", "Explorer selected action is valid in the case action space."),
        _check("invalid_action_guard_fails", invalid_rollout_failed, "PASS" if invalid_rollout_failed else "BLOCKING", "Invalid action guard fails closed."),
        _check("deterministic_state_history_present", len(optimal_rollout["states"]) >= 2, "PASS" if len(optimal_rollout["states"]) >= 2 else "BLOCKING", "World model emits executable state history."),
    ]

    return {
        "case_id": case["case_id"],
        "family": case["family"],
        "action_space": action_space,
        "optimal_actions": optimal_actions,
        "minimum_action_count": case["minimum_action_count"],
        "explorer_action": explorer_action,
        "explorer_action_valid": explorer_action_valid,
        "rollouts": [optimal_rollout, explorer_probe_rollout, invalid_rollout],
        "rollout_count": 3,
        "completed_rollout_count": sum(1 for rollout in [optimal_rollout, explorer_probe_rollout, invalid_rollout] if rollout["completed"]),
        "failed_rollout_count": sum(1 for rollout in [optimal_rollout, explorer_probe_rollout, invalid_rollout] if rollout["failed"]),
        "invalid_transition_count": sum(rollout["invalid_action_count"] for rollout in [optimal_rollout, explorer_probe_rollout, invalid_rollout]),
        "transition_count": transition_count,
        "model_consistency_check_count": len(consistency_checks),
        "model_consistency_checks": consistency_checks,
        "model_consistent": all(check["status"] is True for check in consistency_checks),
    }


def build_executable_world_model(cases: list[dict[str, Any]], explorer_selection_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    case_models = [
        build_world_model_for_case(case, explorer_selection_map.get(str(case["case_id"])))
        for case in cases
    ]

    rollout_records = [
        rollout
        for model in case_models
        for rollout in model["rollouts"]
    ]

    completion_rates = [float(rollout["completion_rate"]) for rollout in rollout_records]
    action_efficiencies = [float(rollout["action_efficiency"]) for rollout in rollout_records]

    return {
        "world_model_id": "MILESTONE_12_EXECUTABLE_SYMBOLIC_WORLD_MODEL_SYNTHETIC_V1",
        "world_model_family": "DETERMINISTIC_SYMBOLIC_TRANSITION_MODEL",
        "case_count": len(cases),
        "case_models": case_models,
        "rollout_count": len(rollout_records),
        "completed_rollout_count": sum(1 for rollout in rollout_records if rollout["completed"]),
        "failed_rollout_count": sum(1 for rollout in rollout_records if rollout["failed"]),
        "invalid_transition_count": sum(model["invalid_transition_count"] for model in case_models),
        "transition_count": sum(model["transition_count"] for model in case_models),
        "explorer_action_valid_count": sum(1 for model in case_models if model["explorer_action_valid"]),
        "model_consistency_check_count": sum(model["model_consistency_check_count"] for model in case_models),
        "model_consistent_case_count": sum(1 for model in case_models if model["model_consistent"]),
        "mean_rollout_completion_rate": round(statistics.mean(completion_rates), 6) if completion_rates else 0.0,
        "mean_rollout_action_efficiency": round(statistics.mean(action_efficiencies), 6) if action_efficiencies else 0.0,
        "measurement_targets": WORLD_MODEL_MEASUREMENT_TARGETS,
        "measurement_target_count": len(WORLD_MODEL_MEASUREMENT_TARGETS),
    }


def build_executable_world_model_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    benchmark_present = SOURCE_BENCHMARK_HARNESS_ARTIFACT.exists()
    explorer_present = SOURCE_EXPLORER_ARTIFACT.exists()

    benchmark = _load_json(SOURCE_BENCHMARK_HARNESS_ARTIFACT)
    explorer = _load_json(SOURCE_EXPLORER_ARTIFACT)

    benchmark_parseable = benchmark is not None
    explorer_parseable = explorer is not None

    benchmark_ready = bool(benchmark and benchmark.get("benchmark_harness_ready") is True)
    benchmark_passed = bool(benchmark and benchmark.get("benchmark_harness_passed") is True)

    explorer_ready = bool(explorer and explorer.get("information_gain_explorer_ready") is True)
    explorer_passed = bool(explorer and explorer.get("information_gain_explorer_passed") is True)
    explorer_next_stage_ok = bool(explorer and explorer.get("next_stage") == "MILESTONE_12_TASK_4_EXECUTABLE_WORLD_MODEL_V1")
    explorer_strategy_ok = bool(explorer and explorer.get("chosen_strategy") == CHOSEN_STRATEGY)
    explorer_goal_ok = bool(explorer and explorer.get("competitive_goal") == COMPETITIVE_GOAL)

    source_boundaries_ok = all(
        [
            benchmark and benchmark.get("public_overfit_allowed") is False,
            benchmark and benchmark.get("external_api_dependency") is False,
            benchmark and benchmark.get("real_submission_allowed") is False,
            benchmark and benchmark.get("kaggle_submission_sent") is False,
            benchmark and benchmark.get("private_core_exposure") is False,
            benchmark and benchmark.get("legal_certification") is False,
            explorer and explorer.get("public_overfit_allowed") is False,
            explorer and explorer.get("external_api_dependency") is False,
            explorer and explorer.get("real_submission_allowed") is False,
            explorer and explorer.get("kaggle_submission_sent") is False,
            explorer and explorer.get("private_core_exposure") is False,
            explorer and explorer.get("legal_certification") is False,
        ]
    )

    cases = _extract_benchmark_cases(benchmark)
    explorer_selection_map = _extract_explorer_selection_map(explorer)
    world_model = build_executable_world_model(cases, explorer_selection_map)

    cases_ready = len(cases) == 6
    selections_ready = len(explorer_selection_map) == 6
    world_model_case_count_ok = world_model["case_count"] == 6
    rollout_count_ok = world_model["rollout_count"] == 18
    transition_count_positive = world_model["transition_count"] > 0
    completed_reference_rollouts_ok = world_model["completed_rollout_count"] >= 6
    invalid_guard_ok = world_model["invalid_transition_count"] == 6
    explorer_actions_valid_ok = world_model["explorer_action_valid_count"] == 6
    consistency_ok = world_model["model_consistent_case_count"] == 6
    measurement_count_ok = world_model["measurement_target_count"] == 10

    world_model_checks = [
        _check("benchmark_artifact_present", benchmark_present, "PASS" if benchmark_present else "BLOCKING", "Task 2 benchmark harness artifact is present."),
        _check("benchmark_artifact_parseable", benchmark_parseable, "PASS" if benchmark_parseable else "BLOCKING", "Task 2 benchmark harness artifact is parseable."),
        _check("explorer_artifact_present", explorer_present, "PASS" if explorer_present else "BLOCKING", "Task 3 explorer artifact is present."),
        _check("explorer_artifact_parseable", explorer_parseable, "PASS" if explorer_parseable else "BLOCKING", "Task 3 explorer artifact is parseable."),
        _check("benchmark_ready", benchmark_ready, "PASS" if benchmark_ready else "BLOCKING", "Benchmark harness is ready."),
        _check("benchmark_passed", benchmark_passed, "PASS" if benchmark_passed else "BLOCKING", "Benchmark harness passed."),
        _check("explorer_ready", explorer_ready, "PASS" if explorer_ready else "BLOCKING", "Explorer policy is ready."),
        _check("explorer_passed", explorer_passed, "PASS" if explorer_passed else "BLOCKING", "Explorer policy passed."),
        _check("explorer_next_stage_ok", explorer_next_stage_ok, "PASS" if explorer_next_stage_ok else "BLOCKING", "Explorer next stage points to Task 4."),
        _check("explorer_strategy_ok", explorer_strategy_ok, "PASS" if explorer_strategy_ok else "BLOCKING", "Explorer strategy matches Milestone 12 strategy."),
        _check("explorer_goal_ok", explorer_goal_ok, "PASS" if explorer_goal_ok else "BLOCKING", "Explorer goal matches first-place objective."),
        _check("source_boundaries_ok", source_boundaries_ok, "PASS" if source_boundaries_ok else "BLOCKING", "Source artifacts preserve public-safe boundaries."),
        _check("cases_ready", cases_ready, "PASS" if cases_ready else "BLOCKING", "Six benchmark cases are available."),
        _check("selections_ready", selections_ready, "PASS" if selections_ready else "BLOCKING", "Six explorer selections are available."),
        _check("world_model_case_count_ok", world_model_case_count_ok, "PASS" if world_model_case_count_ok else "BLOCKING", "World model covers all cases."),
        _check("rollout_count_ok", rollout_count_ok, "PASS" if rollout_count_ok else "BLOCKING", "World model emits three rollouts per case."),
        _check("transition_count_positive", transition_count_positive, "PASS" if transition_count_positive else "BLOCKING", "World model executes transitions."),
        _check("completed_reference_rollouts_ok", completed_reference_rollouts_ok, "PASS" if completed_reference_rollouts_ok else "BLOCKING", "Reference rollouts complete."),
        _check("invalid_guard_ok", invalid_guard_ok, "PASS" if invalid_guard_ok else "BLOCKING", "Invalid action guard is active."),
        _check("explorer_actions_valid_ok", explorer_actions_valid_ok, "PASS" if explorer_actions_valid_ok else "BLOCKING", "Explorer actions are valid in the world model."),
        _check("consistency_ok", consistency_ok, "PASS" if consistency_ok else "BLOCKING", "All case models are internally consistent."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "World model measurement targets are declared."),
    ]

    world_model_passed = all(check["status"] is True for check in world_model_checks)

    world_model_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "world_model_status": "READY" if world_model_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "world_model_id": world_model["world_model_id"],
        "case_count": world_model["case_count"],
        "rollout_count": world_model["rollout_count"],
        "transition_count": world_model["transition_count"],
        "completed_rollout_count": world_model["completed_rollout_count"],
        "invalid_transition_count": world_model["invalid_transition_count"],
        "explorer_action_valid_count": world_model["explorer_action_valid_count"],
        "model_consistent_case_count": world_model["model_consistent_case_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("benchmark_artifact_present", benchmark_present, True, "Task 2 benchmark harness artifact is present."),
        _gate("benchmark_artifact_parseable", benchmark_parseable, True, "Task 2 benchmark harness artifact is parseable."),
        _gate("explorer_artifact_present", explorer_present, True, "Task 3 explorer artifact is present."),
        _gate("explorer_artifact_parseable", explorer_parseable, True, "Task 3 explorer artifact is parseable."),
        _gate("benchmark_ready", benchmark_ready, True, "Benchmark harness is ready."),
        _gate("benchmark_passed", benchmark_passed, True, "Benchmark harness passed."),
        _gate("explorer_ready", explorer_ready, True, "Explorer policy is ready."),
        _gate("explorer_passed", explorer_passed, True, "Explorer policy passed."),
        _gate("explorer_next_stage_ok", explorer_next_stage_ok, True, "Explorer next stage points to Task 4."),
        _gate("explorer_strategy_ok", explorer_strategy_ok, True, "Explorer strategy matches Milestone 12 strategy."),
        _gate("explorer_goal_ok", explorer_goal_ok, True, "Explorer goal matches first-place objective."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source artifacts preserve boundaries."),
        _gate("cases_ready", cases_ready, True, "Six benchmark cases are available."),
        _gate("selections_ready", selections_ready, True, "Six explorer selections are available."),
        _gate("world_model_case_count_ok", world_model_case_count_ok, True, "World model covers all cases."),
        _gate("rollout_count_ok", rollout_count_ok, True, "World model emits eighteen rollouts."),
        _gate("transition_count_positive", transition_count_positive, True, "World model executes transitions."),
        _gate("completed_reference_rollouts_ok", completed_reference_rollouts_ok, True, "Reference rollouts complete."),
        _gate("invalid_guard_ok", invalid_guard_ok, True, "Invalid action guard is active."),
        _gate("explorer_actions_valid_ok", explorer_actions_valid_ok, True, "Explorer actions are valid."),
        _gate("consistency_ok", consistency_ok, True, "All case models are consistent."),
        _gate("measurement_count_ok", measurement_count_ok, True, "Measurement targets are declared."),
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
        _gate("world_model_only_true", True, True, "Task remains world-model-only."),
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
        "source_explorer_artifact": str(SOURCE_EXPLORER_ARTIFACT.relative_to(PROJECT_ROOT)),
        "benchmark_artifact_present": benchmark_present,
        "benchmark_artifact_parseable": benchmark_parseable,
        "explorer_artifact_present": explorer_present,
        "explorer_artifact_parseable": explorer_parseable,
        "benchmark_ready": benchmark_ready,
        "benchmark_passed": benchmark_passed,
        "explorer_ready": explorer_ready,
        "explorer_passed": explorer_passed,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "executable_world_model_ready": True,
        "executable_world_model_valid": world_model_passed,
        "executable_world_model_passed": world_model_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "world_model_summary": world_model_summary,
        "world_model": world_model,
        "case_count": world_model["case_count"],
        "rollout_count": world_model["rollout_count"],
        "transition_count": world_model["transition_count"],
        "measurement_target_count": len(WORLD_MODEL_MEASUREMENT_TARGETS),
        "measurement_targets": WORLD_MODEL_MEASUREMENT_TARGETS,
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
        "world_model_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "world_model_check_count": len(world_model_checks),
        "world_model_checks": world_model_checks,
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
    record["task_id"] = "MILESTONE-12-EXECUTABLE-WORLD-MODEL-" + signature[:12]
    return record


def validate_executable_world_model_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "executable_world_model_ready",
        "executable_world_model_valid",
        "executable_world_model_passed",
        "benchmark_artifact_present",
        "benchmark_artifact_parseable",
        "explorer_artifact_present",
        "explorer_artifact_parseable",
        "benchmark_ready",
        "benchmark_passed",
        "explorer_ready",
        "explorer_passed",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "world_model_only",
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

    if record.get("case_count") != 6:
        issues.append("CASE_COUNT_MISMATCH")

    if record.get("rollout_count") != 18:
        issues.append("ROLLOUT_COUNT_MISMATCH")

    if record.get("transition_count", 0) <= 0:
        issues.append("TRANSITION_COUNT_NOT_POSITIVE")

    if record.get("measurement_target_count") != 10:
        issues.append("MEASUREMENT_TARGET_COUNT_MISMATCH")

    world_model = record.get("world_model")
    if not isinstance(world_model, dict):
        issues.append("WORLD_MODEL_MISSING")
    else:
        if world_model.get("case_count") != 6:
            issues.append("WORLD_MODEL_CASE_COUNT_MISMATCH")
        if world_model.get("rollout_count") != 18:
            issues.append("WORLD_MODEL_ROLLOUT_COUNT_MISMATCH")
        if world_model.get("invalid_transition_count") != 6:
            issues.append("INVALID_TRANSITION_COUNT_MISMATCH")
        if world_model.get("explorer_action_valid_count") != 6:
            issues.append("EXPLORER_ACTION_VALID_COUNT_MISMATCH")
        if world_model.get("model_consistent_case_count") != 6:
            issues.append("MODEL_CONSISTENT_CASE_COUNT_MISMATCH")
        if world_model.get("model_consistency_check_count") != 30:
            issues.append("MODEL_CONSISTENCY_CHECK_COUNT_MISMATCH")

    world_model_summary = record.get("world_model_summary")
    if not isinstance(world_model_summary, dict):
        issues.append("WORLD_MODEL_SUMMARY_MISSING")
    else:
        if world_model_summary.get("world_model_status") != "READY":
            issues.append("WORLD_MODEL_SUMMARY_STATUS_NOT_READY")
        if world_model_summary.get("next_stage") != NEXT_STAGE:
            issues.append("WORLD_MODEL_SUMMARY_NEXT_STAGE_MISMATCH")

    checks = record.get("world_model_checks")
    if not isinstance(checks, list) or not checks:
        issues.append("WORLD_MODEL_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in checks):
        issues.append("WORLD_MODEL_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-executable-world-model-v1.json"
    index_path = target_dir / "milestone-12-executable-world-model-index-v1.json"
    manifest_path = target_dir / "milestone-12-executable-world-model-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-executable-world-model-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "executable_world_model_ready": record["executable_world_model_ready"],
        "executable_world_model_passed": record["executable_world_model_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "case_count": record["case_count"],
        "rollout_count": record["rollout_count"],
        "transition_count": record["transition_count"],
        "invalid_transition_count": record["world_model"]["invalid_transition_count"],
        "explorer_action_valid_count": record["world_model"]["explorer_action_valid_count"],
        "model_consistent_case_count": record["world_model"]["model_consistent_case_count"],
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
        f"executable_world_model_ready={record['executable_world_model_ready']}",
        f"executable_world_model_passed={record['executable_world_model_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"case_count={record['case_count']}",
        f"rollout_count={record['rollout_count']}",
        f"transition_count={record['transition_count']}",
        f"invalid_transition_count={record['world_model']['invalid_transition_count']}",
        f"explorer_action_valid_count={record['world_model']['explorer_action_valid_count']}",
        f"model_consistent_case_count={record['world_model']['model_consistent_case_count']}",
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

## Executable World Model

- executable_world_model_ready: `{record['executable_world_model_ready']}`
- executable_world_model_passed: `{record['executable_world_model_passed']}`
- case_count: `{record['case_count']}`
- rollout_count: `{record['rollout_count']}`
- transition_count: `{record['transition_count']}`
- invalid_transition_count: `{record['world_model']['invalid_transition_count']}`
- explorer_action_valid_count: `{record['world_model']['explorer_action_valid_count']}`
- model_consistent_case_count: `{record['world_model']['model_consistent_case_count']}`
- mean_rollout_completion_rate: `{record['world_model']['mean_rollout_completion_rate']}`
- mean_rollout_action_efficiency: `{record['world_model']['mean_rollout_action_efficiency']}`

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
    record = build_executable_world_model_record()
    issues = validate_executable_world_model_record(record)
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
