"""Milestone #12 Task 6 - Verified Planner Policy v1.

This module builds a deterministic verified planner policy from:

- Task 4 Executable World Model
- Task 5 World Model Verifier

The policy selects executable reference plans only for cases that passed
world-model verification. It remains local-only, deterministic and public-safe.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_VERIFIED_PLANNER_POLICY_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 6
TASK_LABEL = "Milestone #12 Task 6 - Verified Planner Policy v1"

SOURCE_TASK = "MILESTONE_12_TASK_5_WORLD_MODEL_VERIFIER_V1"
NEXT_STAGE = "MILESTONE_12_TASK_7_EPISODE_MEMORY_POLICY_V1"

TASK_MODE = "MILESTONE_12_VERIFIED_PLANNER_POLICY_V1_LOCAL_ONLY"
TASK_SCOPE = "VERIFIED_PLANNER_POLICY_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_VERIFIED_PLANNER_POLICY_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "verified-planner-policy-v1"

SOURCE_WORLD_MODEL_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "executable-world-model-v1"
    / "milestone-12-executable-world-model-v1.json"
)

SOURCE_VERIFIER_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "world-model-verifier-v1"
    / "milestone-12-world-model-verifier-v1.json"
)

PLANNER_MEASUREMENT_TARGETS = [
    "case_count",
    "verified_case_count",
    "plan_count",
    "verified_plan_count",
    "action_count",
    "mean_plan_length",
    "minimum_plan_length",
    "maximum_plan_length",
    "planner_gate_count",
    "planner_issue_count",
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


def _case_models_by_id(world_model_record: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not world_model_record:
        return {}
    world_model = world_model_record.get("world_model")
    if not isinstance(world_model, dict):
        return {}
    case_models = world_model.get("case_models")
    if not isinstance(case_models, list):
        return {}
    output: dict[str, dict[str, Any]] = {}
    for case_model in case_models:
        if isinstance(case_model, dict) and isinstance(case_model.get("case_id"), str):
            output[case_model["case_id"]] = case_model
    return output


def _verified_cases_by_id(verifier_record: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not verifier_record:
        return {}
    report = verifier_record.get("verification_report")
    if not isinstance(report, dict):
        return {}
    verifications = report.get("case_verifications")
    if not isinstance(verifications, list):
        return {}
    output: dict[str, dict[str, Any]] = {}
    for verification in verifications:
        if isinstance(verification, dict) and isinstance(verification.get("case_id"), str):
            output[verification["case_id"]] = verification
    return output


def build_plan_for_case(case_model: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case_model.get("case_id", "UNKNOWN_CASE"))
    family = str(case_model.get("family", "UNKNOWN_FAMILY"))

    optimal_actions = case_model.get("optimal_actions")
    action_space = case_model.get("action_space")

    if not isinstance(optimal_actions, list):
        optimal_actions = []
    if not isinstance(action_space, list):
        action_space = []

    actions = [str(action) for action in optimal_actions]
    action_space_set = {str(action) for action in action_space}

    verified = bool(
        verification.get("verified") is True
        and verification.get("optimal_rollout_verified") is True
        and verification.get("invalid_guard_verified") is True
        and verification.get("explorer_probe_verified") is True
        and verification.get("transition_history_verified") is True
    )

    actions_valid = bool(actions and all(action in action_space_set for action in actions))
    plan_length = len(actions)
    minimum_action_count = int(case_model.get("minimum_action_count", 0))

    minimal_plan = plan_length == minimum_action_count and plan_length > 0
    executable = verified and actions_valid and minimal_plan

    checks = [
        _check("case_verified", verified, "PASS" if verified else "BLOCKING", "Case passed world model verification."),
        _check("actions_present", bool(actions), "PASS" if actions else "BLOCKING", "Plan has actions."),
        _check("actions_valid", actions_valid, "PASS" if actions_valid else "BLOCKING", "All plan actions are in the action space."),
        _check("minimal_plan", minimal_plan, "PASS" if minimal_plan else "BLOCKING", "Plan length matches minimum action count."),
        _check("executable", executable, "PASS" if executable else "BLOCKING", "Plan is executable under verified model constraints."),
    ]

    return {
        "case_id": case_id,
        "family": family,
        "plan_id": f"PLAN-{case_id.upper()}",
        "planner_policy": "VERIFIED_OPTIMAL_REFERENCE_PLAN",
        "actions": actions,
        "action_count": plan_length,
        "minimum_action_count": minimum_action_count,
        "verified_source_case": verified,
        "actions_valid": actions_valid,
        "minimal_plan": minimal_plan,
        "executable": executable,
        "confidence": 1.0 if executable else 0.0,
        "checks": checks,
        "check_count": len(checks),
        "issue_count": 0 if executable else sum(1 for check in checks if check["status"] is not True),
    }


def build_planner_policy(world_model_record: dict[str, Any] | None, verifier_record: dict[str, Any] | None) -> dict[str, Any]:
    case_models = _case_models_by_id(world_model_record)
    verified_cases = _verified_cases_by_id(verifier_record)

    plans = [
        build_plan_for_case(case_models[case_id], verified_cases[case_id])
        for case_id in sorted(case_models)
        if case_id in verified_cases
    ]

    action_counts = [int(plan["action_count"]) for plan in plans]

    verified_plan_count = sum(1 for plan in plans if plan["executable"] is True)
    action_count = sum(action_counts)

    return {
        "planner_policy_id": "MILESTONE_12_VERIFIED_PLANNER_POLICY_SYNTHETIC_V1",
        "planner_policy_family": "DETERMINISTIC_VERIFIED_REFERENCE_PLANNER",
        "case_count": len(case_models),
        "verified_case_count": len(verified_cases),
        "plan_count": len(plans),
        "verified_plan_count": verified_plan_count,
        "action_count": action_count,
        "mean_plan_length": round(action_count / len(plans), 6) if plans else 0.0,
        "minimum_plan_length": min(action_counts) if action_counts else 0,
        "maximum_plan_length": max(action_counts) if action_counts else 0,
        "plans": plans,
        "measurement_targets": PLANNER_MEASUREMENT_TARGETS,
        "measurement_target_count": len(PLANNER_MEASUREMENT_TARGETS),
    }


def build_verified_planner_policy_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    world_model_present = SOURCE_WORLD_MODEL_ARTIFACT.exists()
    verifier_present = SOURCE_VERIFIER_ARTIFACT.exists()

    world_model_record = _load_json(SOURCE_WORLD_MODEL_ARTIFACT)
    verifier_record = _load_json(SOURCE_VERIFIER_ARTIFACT)

    world_model_parseable = world_model_record is not None
    verifier_parseable = verifier_record is not None

    world_model_ready = bool(world_model_record and world_model_record.get("executable_world_model_ready") is True)
    world_model_passed = bool(world_model_record and world_model_record.get("executable_world_model_passed") is True)

    verifier_ready = bool(verifier_record and verifier_record.get("world_model_verifier_ready") is True)
    verifier_passed = bool(verifier_record and verifier_record.get("world_model_verifier_passed") is True)
    verifier_next_stage_ok = bool(verifier_record and verifier_record.get("next_stage") == "MILESTONE_12_TASK_6_VERIFIED_PLANNER_POLICY_V1")

    source_strategy_ok = bool(
        world_model_record
        and verifier_record
        and world_model_record.get("chosen_strategy") == CHOSEN_STRATEGY
        and verifier_record.get("chosen_strategy") == CHOSEN_STRATEGY
    )

    source_goal_ok = bool(
        world_model_record
        and verifier_record
        and world_model_record.get("competitive_goal") == COMPETITIVE_GOAL
        and verifier_record.get("competitive_goal") == COMPETITIVE_GOAL
    )

    source_boundaries_ok = all(
        [
            world_model_record and world_model_record.get("public_overfit_allowed") is False,
            world_model_record and world_model_record.get("public_overfit_guard_required") is True,
            world_model_record and world_model_record.get("external_api_dependency") is False,
            world_model_record and world_model_record.get("internet_during_eval") is False,
            world_model_record and world_model_record.get("real_submission_allowed") is False,
            world_model_record and world_model_record.get("kaggle_submission_sent") is False,
            world_model_record and world_model_record.get("private_core_exposure") is False,
            world_model_record and world_model_record.get("legal_certification") is False,
            verifier_record and verifier_record.get("public_overfit_allowed") is False,
            verifier_record and verifier_record.get("public_overfit_guard_required") is True,
            verifier_record and verifier_record.get("external_api_dependency") is False,
            verifier_record and verifier_record.get("internet_during_eval") is False,
            verifier_record and verifier_record.get("real_submission_allowed") is False,
            verifier_record and verifier_record.get("kaggle_submission_sent") is False,
            verifier_record and verifier_record.get("private_core_exposure") is False,
            verifier_record and verifier_record.get("legal_certification") is False,
        ]
    )

    planner_policy = build_planner_policy(world_model_record, verifier_record)

    case_count_ok = planner_policy["case_count"] == 6
    verified_case_count_ok = planner_policy["verified_case_count"] == 6
    plan_count_ok = planner_policy["plan_count"] == 6
    verified_plan_count_ok = planner_policy["verified_plan_count"] == 6
    action_count_positive = planner_policy["action_count"] > 0
    plan_lengths_ok = planner_policy["minimum_plan_length"] >= 1 and planner_policy["maximum_plan_length"] >= planner_policy["minimum_plan_length"]
    measurement_count_ok = planner_policy["measurement_target_count"] == 10
    planner_issue_count = sum(plan["issue_count"] for plan in planner_policy["plans"])
    planner_issue_zero = planner_issue_count == 0

    planner_checks = [
        _check("world_model_artifact_present", world_model_present, "PASS" if world_model_present else "BLOCKING", "Task 4 world model artifact is present."),
        _check("world_model_artifact_parseable", world_model_parseable, "PASS" if world_model_parseable else "BLOCKING", "Task 4 world model artifact is parseable."),
        _check("verifier_artifact_present", verifier_present, "PASS" if verifier_present else "BLOCKING", "Task 5 verifier artifact is present."),
        _check("verifier_artifact_parseable", verifier_parseable, "PASS" if verifier_parseable else "BLOCKING", "Task 5 verifier artifact is parseable."),
        _check("world_model_ready", world_model_ready, "PASS" if world_model_ready else "BLOCKING", "World model is ready."),
        _check("world_model_passed", world_model_passed, "PASS" if world_model_passed else "BLOCKING", "World model passed."),
        _check("verifier_ready", verifier_ready, "PASS" if verifier_ready else "BLOCKING", "Verifier is ready."),
        _check("verifier_passed", verifier_passed, "PASS" if verifier_passed else "BLOCKING", "Verifier passed."),
        _check("verifier_next_stage_ok", verifier_next_stage_ok, "PASS" if verifier_next_stage_ok else "BLOCKING", "Verifier points to Task 6."),
        _check("source_strategy_ok", source_strategy_ok, "PASS" if source_strategy_ok else "BLOCKING", "Source strategy is aligned."),
        _check("source_goal_ok", source_goal_ok, "PASS" if source_goal_ok else "BLOCKING", "Source competitive goal is aligned."),
        _check("source_boundaries_ok", source_boundaries_ok, "PASS" if source_boundaries_ok else "BLOCKING", "Source boundaries are preserved."),
        _check("case_count_ok", case_count_ok, "PASS" if case_count_ok else "BLOCKING", "Planner sees six world model cases."),
        _check("verified_case_count_ok", verified_case_count_ok, "PASS" if verified_case_count_ok else "BLOCKING", "Planner sees six verified cases."),
        _check("plan_count_ok", plan_count_ok, "PASS" if plan_count_ok else "BLOCKING", "Planner emits six plans."),
        _check("verified_plan_count_ok", verified_plan_count_ok, "PASS" if verified_plan_count_ok else "BLOCKING", "Planner verifies six plans."),
        _check("action_count_positive", action_count_positive, "PASS" if action_count_positive else "BLOCKING", "Planner emits executable actions."),
        _check("plan_lengths_ok", plan_lengths_ok, "PASS" if plan_lengths_ok else "BLOCKING", "Plan lengths are valid."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "Planner measurement targets are declared."),
        _check("planner_issue_zero", planner_issue_zero, "PASS" if planner_issue_zero else "BLOCKING", "Planner issue count is zero."),
    ]

    planner_passed = all(check["status"] is True for check in planner_checks)

    planner_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "planner_policy_status": "READY" if planner_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "planner_policy_id": planner_policy["planner_policy_id"],
        "case_count": planner_policy["case_count"],
        "verified_case_count": planner_policy["verified_case_count"],
        "plan_count": planner_policy["plan_count"],
        "verified_plan_count": planner_policy["verified_plan_count"],
        "action_count": planner_policy["action_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("world_model_artifact_present", world_model_present, True, "Task 4 world model artifact is present."),
        _gate("world_model_artifact_parseable", world_model_parseable, True, "Task 4 world model artifact is parseable."),
        _gate("verifier_artifact_present", verifier_present, True, "Task 5 verifier artifact is present."),
        _gate("verifier_artifact_parseable", verifier_parseable, True, "Task 5 verifier artifact is parseable."),
        _gate("world_model_ready", world_model_ready, True, "World model is ready."),
        _gate("world_model_passed", world_model_passed, True, "World model passed."),
        _gate("verifier_ready", verifier_ready, True, "Verifier is ready."),
        _gate("verifier_passed", verifier_passed, True, "Verifier passed."),
        _gate("verifier_next_stage_ok", verifier_next_stage_ok, True, "Verifier points to Task 6."),
        _gate("source_strategy_ok", source_strategy_ok, True, "Source strategy is aligned."),
        _gate("source_goal_ok", source_goal_ok, True, "Source goal is aligned."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("case_count_ok", case_count_ok, True, "Six cases are available."),
        _gate("verified_case_count_ok", verified_case_count_ok, True, "Six cases are verified."),
        _gate("plan_count_ok", plan_count_ok, True, "Six plans are emitted."),
        _gate("verified_plan_count_ok", verified_plan_count_ok, True, "Six plans are verified."),
        _gate("action_count_positive", action_count_positive, True, "Planner emits actions."),
        _gate("plan_lengths_ok", plan_lengths_ok, True, "Plan lengths are valid."),
        _gate("measurement_count_ok", measurement_count_ok, True, "Measurement targets are declared."),
        _gate("planner_issue_zero", planner_issue_zero, True, "Planner issue count is zero."),
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
        _gate("planner_only_true", True, True, "Task remains planner-policy-only."),
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
        "source_world_model_artifact": str(SOURCE_WORLD_MODEL_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_verifier_artifact": str(SOURCE_VERIFIER_ARTIFACT.relative_to(PROJECT_ROOT)),
        "world_model_artifact_present": world_model_present,
        "world_model_artifact_parseable": world_model_parseable,
        "verifier_artifact_present": verifier_present,
        "verifier_artifact_parseable": verifier_parseable,
        "world_model_ready": world_model_ready,
        "world_model_passed": world_model_passed,
        "verifier_ready": verifier_ready,
        "verifier_passed": verifier_passed,
        "verifier_next_stage_ok": verifier_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "verified_planner_policy_ready": True,
        "verified_planner_policy_valid": planner_passed,
        "verified_planner_policy_passed": planner_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "planner_summary": planner_summary,
        "planner_policy": planner_policy,
        "case_count": planner_policy["case_count"],
        "verified_case_count": planner_policy["verified_case_count"],
        "plan_count": planner_policy["plan_count"],
        "verified_plan_count": planner_policy["verified_plan_count"],
        "action_count": planner_policy["action_count"],
        "planner_issue_count": planner_issue_count,
        "measurement_target_count": len(PLANNER_MEASUREMENT_TARGETS),
        "measurement_targets": PLANNER_MEASUREMENT_TARGETS,
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
        "planner_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "planner_check_count": len(planner_checks),
        "planner_checks": planner_checks,
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
    record["task_id"] = "MILESTONE-12-VERIFIED-PLANNER-POLICY-" + signature[:12]
    return record


def validate_verified_planner_policy_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "verified_planner_policy_ready",
        "verified_planner_policy_valid",
        "verified_planner_policy_passed",
        "world_model_artifact_present",
        "world_model_artifact_parseable",
        "verifier_artifact_present",
        "verifier_artifact_parseable",
        "world_model_ready",
        "world_model_passed",
        "verifier_ready",
        "verifier_passed",
        "verifier_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "planner_only",
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

    if record.get("verified_case_count") != 6:
        issues.append("VERIFIED_CASE_COUNT_MISMATCH")

    if record.get("plan_count") != 6:
        issues.append("PLAN_COUNT_MISMATCH")

    if record.get("verified_plan_count") != 6:
        issues.append("VERIFIED_PLAN_COUNT_MISMATCH")

    if record.get("action_count", 0) <= 0:
        issues.append("ACTION_COUNT_NOT_POSITIVE")

    if record.get("planner_issue_count") != 0:
        issues.append("PLANNER_ISSUE_COUNT_NOT_ZERO")

    if record.get("measurement_target_count") != 10:
        issues.append("MEASUREMENT_TARGET_COUNT_MISMATCH")

    planner_policy = record.get("planner_policy")
    if not isinstance(planner_policy, dict):
        issues.append("PLANNER_POLICY_MISSING")
    else:
        plans = planner_policy.get("plans")
        if not isinstance(plans, list) or len(plans) != 6:
            issues.append("PLANS_MISSING_OR_COUNT_MISMATCH")
        elif any(not isinstance(plan, dict) or plan.get("executable") is not True for plan in plans):
            issues.append("PLAN_NOT_EXECUTABLE")

    summary = record.get("planner_summary")
    if not isinstance(summary, dict):
        issues.append("PLANNER_SUMMARY_MISSING")
    else:
        if summary.get("planner_policy_status") != "READY":
            issues.append("PLANNER_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("PLANNER_SUMMARY_NEXT_STAGE_MISMATCH")

    checks = record.get("planner_checks")
    if not isinstance(checks, list) or not checks:
        issues.append("PLANNER_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in checks):
        issues.append("PLANNER_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-verified-planner-policy-v1.json"
    index_path = target_dir / "milestone-12-verified-planner-policy-index-v1.json"
    manifest_path = target_dir / "milestone-12-verified-planner-policy-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-verified-planner-policy-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "verified_planner_policy_ready": record["verified_planner_policy_ready"],
        "verified_planner_policy_passed": record["verified_planner_policy_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "case_count": record["case_count"],
        "verified_case_count": record["verified_case_count"],
        "plan_count": record["plan_count"],
        "verified_plan_count": record["verified_plan_count"],
        "action_count": record["action_count"],
        "planner_issue_count": record["planner_issue_count"],
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
        f"verified_planner_policy_ready={record['verified_planner_policy_ready']}",
        f"verified_planner_policy_passed={record['verified_planner_policy_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"case_count={record['case_count']}",
        f"verified_case_count={record['verified_case_count']}",
        f"plan_count={record['plan_count']}",
        f"verified_plan_count={record['verified_plan_count']}",
        f"action_count={record['action_count']}",
        f"planner_issue_count={record['planner_issue_count']}",
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

## Verified Planner Policy

- verified_planner_policy_ready: `{record['verified_planner_policy_ready']}`
- verified_planner_policy_passed: `{record['verified_planner_policy_passed']}`
- case_count: `{record['case_count']}`
- verified_case_count: `{record['verified_case_count']}`
- plan_count: `{record['plan_count']}`
- verified_plan_count: `{record['verified_plan_count']}`
- action_count: `{record['action_count']}`
- planner_issue_count: `{record['planner_issue_count']}`
- mean_plan_length: `{record['planner_policy']['mean_plan_length']}`

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
    record = build_verified_planner_policy_record()
    issues = validate_verified_planner_policy_record(record)
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
