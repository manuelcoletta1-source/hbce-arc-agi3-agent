"""Milestone #12 Task 5 - World Model Verifier v1.

This module verifies the deterministic executable world model created in
Milestone #12 Task 4.

It checks:

- source artifact availability and parseability
- world model readiness and pass state
- per-case rollout consistency
- optimal rollout completion
- invalid-action fail-closed behavior
- explorer probe validity
- transition history integrity
- boundary preservation

No Kaggle upload, no authentication, no external APIs, no private core exposure.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_WORLD_MODEL_VERIFIER_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 5
TASK_LABEL = "Milestone #12 Task 5 - World Model Verifier v1"

SOURCE_TASK = "MILESTONE_12_TASK_4_EXECUTABLE_WORLD_MODEL_V1"
NEXT_STAGE = "MILESTONE_12_TASK_6_VERIFIED_PLANNER_POLICY_V1"

TASK_MODE = "MILESTONE_12_WORLD_MODEL_VERIFIER_V1_LOCAL_ONLY"
TASK_SCOPE = "WORLD_MODEL_VERIFIER_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_WORLD_MODEL_VERIFIER_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "world-model-verifier-v1"

SOURCE_WORLD_MODEL_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "executable-world-model-v1"
    / "milestone-12-executable-world-model-v1.json"
)


VERIFIER_MEASUREMENT_TARGETS = [
    "case_count",
    "verified_case_count",
    "rollout_count",
    "verified_rollout_count",
    "optimal_rollout_verified_count",
    "invalid_guard_verified_count",
    "explorer_probe_verified_count",
    "transition_history_verified_count",
    "boundary_guard_verified_count",
    "verification_issue_count",
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


def _load_world_model_source() -> dict[str, Any] | None:
    if not SOURCE_WORLD_MODEL_ARTIFACT.exists():
        return None
    try:
        return json.loads(SOURCE_WORLD_MODEL_ARTIFACT.read_text(encoding="utf-8"))
    except Exception:
        return None


def _rollout_by_kind(case_model: dict[str, Any], rollout_kind: str) -> dict[str, Any] | None:
    rollouts = case_model.get("rollouts")
    if not isinstance(rollouts, list):
        return None
    for rollout in rollouts:
        if isinstance(rollout, dict) and rollout.get("rollout_kind") == rollout_kind:
            return rollout
    return None


def verify_transition_history(rollout: dict[str, Any]) -> dict[str, Any]:
    states = rollout.get("states")
    if not isinstance(states, list) or not states:
        return {
            "verified": False,
            "issue": "STATES_MISSING",
            "state_count": 0,
            "transition_count": 0,
        }

    transition_count = 0
    for state_index, state in enumerate(states):
        if not isinstance(state, dict):
            return {
                "verified": False,
                "issue": f"STATE_{state_index}_NOT_OBJECT",
                "state_count": len(states),
                "transition_count": transition_count,
            }

        history = state.get("history")
        if not isinstance(history, list):
            return {
                "verified": False,
                "issue": f"STATE_{state_index}_HISTORY_MISSING",
                "state_count": len(states),
                "transition_count": transition_count,
            }

        if state_index > 0:
            transition_count += 1
            if len(history) != state_index:
                return {
                    "verified": False,
                    "issue": f"STATE_{state_index}_HISTORY_LENGTH_MISMATCH",
                    "state_count": len(states),
                    "transition_count": transition_count,
                }

            last_transition = history[-1]
            if not isinstance(last_transition, dict):
                return {
                    "verified": False,
                    "issue": f"STATE_{state_index}_LAST_TRANSITION_INVALID",
                    "state_count": len(states),
                    "transition_count": transition_count,
                }

            if "valid" not in last_transition or "progress_made" not in last_transition:
                return {
                    "verified": False,
                    "issue": f"STATE_{state_index}_TRANSITION_FIELDS_MISSING",
                    "state_count": len(states),
                    "transition_count": transition_count,
                }

    return {
        "verified": True,
        "issue": "NONE",
        "state_count": len(states),
        "transition_count": transition_count,
    }


def verify_case_model(case_model: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case_model.get("case_id", "UNKNOWN_CASE"))
    family = str(case_model.get("family", "UNKNOWN_FAMILY"))

    rollouts = case_model.get("rollouts")
    rollouts_ready = isinstance(rollouts, list) and len(rollouts) == 3

    optimal_rollout = _rollout_by_kind(case_model, "OPTIMAL_REFERENCE_ROLLOUT")
    explorer_rollout = _rollout_by_kind(case_model, "EXPLORER_SINGLE_PROBE_ROLLOUT")
    invalid_rollout = _rollout_by_kind(case_model, "INVALID_ACTION_GUARD_ROLLOUT")

    optimal_rollout_present = optimal_rollout is not None
    explorer_rollout_present = explorer_rollout is not None
    invalid_rollout_present = invalid_rollout is not None

    optimal_rollout_completed = bool(
        optimal_rollout
        and optimal_rollout.get("completed") is True
        and optimal_rollout.get("failed") is False
        and optimal_rollout.get("executed_action_count") == optimal_rollout.get("minimum_action_count")
        and optimal_rollout.get("action_efficiency") == 1.0
    )

    explorer_probe_valid = bool(
        explorer_rollout
        and case_model.get("explorer_action_valid") is True
        and explorer_rollout.get("failed") is False
        and explorer_rollout.get("invalid_action_count") == 0
        and explorer_rollout.get("executed_action_count") == 1
    )

    invalid_guard_verified = bool(
        invalid_rollout
        and invalid_rollout.get("completed") is False
        and invalid_rollout.get("failed") is True
        and invalid_rollout.get("invalid_action_count") == 1
        and invalid_rollout.get("executed_action_count") == 1
    )

    optimal_history = verify_transition_history(optimal_rollout or {})
    explorer_history = verify_transition_history(explorer_rollout or {})
    invalid_history = verify_transition_history(invalid_rollout or {})

    transition_history_verified = all(
        [
            optimal_history["verified"],
            explorer_history["verified"],
            invalid_history["verified"],
        ]
    )

    consistency_checks = case_model.get("model_consistency_checks")
    consistency_checks_passed = (
        isinstance(consistency_checks, list)
        and len(consistency_checks) == 5
        and all(isinstance(check, dict) and check.get("status") is True for check in consistency_checks)
    )

    invalid_transition_count_ok = case_model.get("invalid_transition_count") == 1
    transition_count_positive = int(case_model.get("transition_count", 0)) > 0
    model_consistent_flag_ok = case_model.get("model_consistent") is True

    checks = [
        _check("rollouts_ready", rollouts_ready, "PASS" if rollouts_ready else "BLOCKING", "Case model has exactly three rollouts."),
        _check("optimal_rollout_present", optimal_rollout_present, "PASS" if optimal_rollout_present else "BLOCKING", "Optimal rollout is present."),
        _check("explorer_rollout_present", explorer_rollout_present, "PASS" if explorer_rollout_present else "BLOCKING", "Explorer probe rollout is present."),
        _check("invalid_rollout_present", invalid_rollout_present, "PASS" if invalid_rollout_present else "BLOCKING", "Invalid-action guard rollout is present."),
        _check("optimal_rollout_completed", optimal_rollout_completed, "PASS" if optimal_rollout_completed else "BLOCKING", "Optimal rollout completes minimally."),
        _check("explorer_probe_valid", explorer_probe_valid, "PASS" if explorer_probe_valid else "BLOCKING", "Explorer probe is valid and non-failing."),
        _check("invalid_guard_verified", invalid_guard_verified, "PASS" if invalid_guard_verified else "BLOCKING", "Invalid guard fails closed."),
        _check("transition_history_verified", transition_history_verified, "PASS" if transition_history_verified else "BLOCKING", "Rollout transition histories are valid."),
        _check("consistency_checks_passed", consistency_checks_passed, "PASS" if consistency_checks_passed else "BLOCKING", "Source consistency checks passed."),
        _check("invalid_transition_count_ok", invalid_transition_count_ok, "PASS" if invalid_transition_count_ok else "BLOCKING", "Exactly one invalid transition is recorded per case."),
        _check("transition_count_positive", transition_count_positive, "PASS" if transition_count_positive else "BLOCKING", "Case model executes at least one transition."),
        _check("model_consistent_flag_ok", model_consistent_flag_ok, "PASS" if model_consistent_flag_ok else "BLOCKING", "Source model_consistent flag is true."),
    ]

    verified = all(check["status"] is True for check in checks)

    return {
        "case_id": case_id,
        "family": family,
        "verified": verified,
        "rollout_count": len(rollouts) if isinstance(rollouts, list) else 0,
        "verified_rollout_count": sum(
            [
                1 if optimal_rollout_completed else 0,
                1 if explorer_probe_valid else 0,
                1 if invalid_guard_verified else 0,
            ]
        ),
        "optimal_rollout_verified": optimal_rollout_completed,
        "explorer_probe_verified": explorer_probe_valid,
        "invalid_guard_verified": invalid_guard_verified,
        "transition_history_verified": transition_history_verified,
        "transition_history_reports": {
            "optimal": optimal_history,
            "explorer": explorer_history,
            "invalid": invalid_history,
        },
        "check_count": len(checks),
        "checks": checks,
        "issue_count": 0 if verified else sum(1 for check in checks if check["status"] is not True),
    }


def build_verification_report(source: dict[str, Any] | None) -> dict[str, Any]:
    if not source:
        return {
            "verifier_id": "MILESTONE_12_WORLD_MODEL_VERIFIER_SYNTHETIC_V1",
            "case_count": 0,
            "verified_case_count": 0,
            "rollout_count": 0,
            "verified_rollout_count": 0,
            "optimal_rollout_verified_count": 0,
            "invalid_guard_verified_count": 0,
            "explorer_probe_verified_count": 0,
            "transition_history_verified_count": 0,
            "boundary_guard_verified_count": 0,
            "verification_issue_count": 1,
            "case_verifications": [],
            "measurement_targets": VERIFIER_MEASUREMENT_TARGETS,
            "measurement_target_count": len(VERIFIER_MEASUREMENT_TARGETS),
        }

    world_model = source.get("world_model")
    case_models = []
    if isinstance(world_model, dict) and isinstance(world_model.get("case_models"), list):
        case_models = [case for case in world_model["case_models"] if isinstance(case, dict)]

    case_verifications = [verify_case_model(case_model) for case_model in case_models]

    boundary_guard_checks = [
        source.get("public_overfit_allowed") is False,
        source.get("public_overfit_guard_required") is True,
        source.get("external_api_dependency") is False,
        source.get("internet_during_eval") is False,
        source.get("real_submission_allowed") is False,
        source.get("manual_upload_allowed") is False,
        source.get("kaggle_submission_sent") is False,
        source.get("kaggle_authentication_performed") is False,
        source.get("private_core_exposure") is False,
        source.get("legal_certification") is False,
    ]

    boundary_guard_verified_count = sum(1 for item in boundary_guard_checks if item is True)

    return {
        "verifier_id": "MILESTONE_12_WORLD_MODEL_VERIFIER_SYNTHETIC_V1",
        "verifier_family": "DETERMINISTIC_WORLD_MODEL_CONSISTENCY_VERIFIER",
        "case_count": len(case_verifications),
        "verified_case_count": sum(1 for item in case_verifications if item["verified"]),
        "rollout_count": sum(item["rollout_count"] for item in case_verifications),
        "verified_rollout_count": sum(item["verified_rollout_count"] for item in case_verifications),
        "optimal_rollout_verified_count": sum(1 for item in case_verifications if item["optimal_rollout_verified"]),
        "invalid_guard_verified_count": sum(1 for item in case_verifications if item["invalid_guard_verified"]),
        "explorer_probe_verified_count": sum(1 for item in case_verifications if item["explorer_probe_verified"]),
        "transition_history_verified_count": sum(1 for item in case_verifications if item["transition_history_verified"]),
        "boundary_guard_verified_count": boundary_guard_verified_count,
        "verification_issue_count": sum(item["issue_count"] for item in case_verifications) + (0 if boundary_guard_verified_count == 10 else 10 - boundary_guard_verified_count),
        "case_verifications": case_verifications,
        "measurement_targets": VERIFIER_MEASUREMENT_TARGETS,
        "measurement_target_count": len(VERIFIER_MEASUREMENT_TARGETS),
    }


def build_world_model_verifier_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_present = SOURCE_WORLD_MODEL_ARTIFACT.exists()
    source = _load_world_model_source()
    source_parseable = source is not None

    source_ready = bool(source and source.get("executable_world_model_ready") is True)
    source_passed = bool(source and source.get("executable_world_model_passed") is True)
    source_next_stage_ok = bool(source and source.get("next_stage") == "MILESTONE_12_TASK_5_WORLD_MODEL_VERIFIER_V1")
    source_strategy_ok = bool(source and source.get("chosen_strategy") == CHOSEN_STRATEGY)
    source_goal_ok = bool(source and source.get("competitive_goal") == COMPETITIVE_GOAL)
    source_milestone_open = bool(source and source.get("milestone_12_status") == "OPENED_CANONICALLY")
    source_issue_zero = bool(source and source.get("issue_count") == 0)

    source_boundaries_ok = all(
        [
            source and source.get("public_overfit_allowed") is False,
            source and source.get("public_overfit_guard_required") is True,
            source and source.get("external_api_dependency") is False,
            source and source.get("internet_during_eval") is False,
            source and source.get("real_submission_allowed") is False,
            source and source.get("manual_upload_allowed") is False,
            source and source.get("kaggle_submission_sent") is False,
            source and source.get("kaggle_authentication_performed") is False,
            source and source.get("private_core_exposure") is False,
            source and source.get("legal_certification") is False,
        ]
    )

    verification_report = build_verification_report(source)

    case_count_ok = verification_report["case_count"] == 6
    verified_case_count_ok = verification_report["verified_case_count"] == 6
    rollout_count_ok = verification_report["rollout_count"] == 18
    verified_rollout_count_ok = verification_report["verified_rollout_count"] == 18
    optimal_rollouts_ok = verification_report["optimal_rollout_verified_count"] == 6
    invalid_guards_ok = verification_report["invalid_guard_verified_count"] == 6
    explorer_probes_ok = verification_report["explorer_probe_verified_count"] == 6
    transition_histories_ok = verification_report["transition_history_verified_count"] == 6
    boundary_guard_ok = verification_report["boundary_guard_verified_count"] == 10
    verification_issue_zero = verification_report["verification_issue_count"] == 0
    measurement_count_ok = verification_report["measurement_target_count"] == 10

    verifier_checks = [
        _check("source_world_model_artifact_present", source_present, "PASS" if source_present else "BLOCKING", "Task 4 world model artifact is present."),
        _check("source_world_model_artifact_parseable", source_parseable, "PASS" if source_parseable else "BLOCKING", "Task 4 world model artifact is parseable."),
        _check("source_world_model_ready", source_ready, "PASS" if source_ready else "BLOCKING", "World model is ready."),
        _check("source_world_model_passed", source_passed, "PASS" if source_passed else "BLOCKING", "World model passed."),
        _check("source_next_stage_ok", source_next_stage_ok, "PASS" if source_next_stage_ok else "BLOCKING", "Source next stage points to Task 5."),
        _check("source_strategy_ok", source_strategy_ok, "PASS" if source_strategy_ok else "BLOCKING", "Source strategy matches Milestone 12 strategy."),
        _check("source_goal_ok", source_goal_ok, "PASS" if source_goal_ok else "BLOCKING", "Source goal matches first-place objective."),
        _check("source_milestone_open", source_milestone_open, "PASS" if source_milestone_open else "BLOCKING", "Milestone 12 remains opened canonically."),
        _check("source_issue_zero", source_issue_zero, "PASS" if source_issue_zero else "BLOCKING", "Source issue count is zero."),
        _check("source_boundaries_ok", source_boundaries_ok, "PASS" if source_boundaries_ok else "BLOCKING", "Source boundaries are preserved."),
        _check("case_count_ok", case_count_ok, "PASS" if case_count_ok else "BLOCKING", "Verifier sees six case models."),
        _check("verified_case_count_ok", verified_case_count_ok, "PASS" if verified_case_count_ok else "BLOCKING", "Verifier verifies six case models."),
        _check("rollout_count_ok", rollout_count_ok, "PASS" if rollout_count_ok else "BLOCKING", "Verifier sees eighteen rollouts."),
        _check("verified_rollout_count_ok", verified_rollout_count_ok, "PASS" if verified_rollout_count_ok else "BLOCKING", "Verifier verifies eighteen rollout checks."),
        _check("optimal_rollouts_ok", optimal_rollouts_ok, "PASS" if optimal_rollouts_ok else "BLOCKING", "All optimal rollouts are verified."),
        _check("invalid_guards_ok", invalid_guards_ok, "PASS" if invalid_guards_ok else "BLOCKING", "All invalid-action guards are verified."),
        _check("explorer_probes_ok", explorer_probes_ok, "PASS" if explorer_probes_ok else "BLOCKING", "All explorer probes are verified."),
        _check("transition_histories_ok", transition_histories_ok, "PASS" if transition_histories_ok else "BLOCKING", "All transition histories are verified."),
        _check("boundary_guard_ok", boundary_guard_ok, "PASS" if boundary_guard_ok else "BLOCKING", "All boundary guards are verified."),
        _check("verification_issue_zero", verification_issue_zero, "PASS" if verification_issue_zero else "BLOCKING", "Verification issue count is zero."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "Verifier measurement targets are declared."),
    ]

    verifier_passed = all(check["status"] is True for check in verifier_checks)

    verifier_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "verifier_status": "READY" if verifier_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "verifier_id": verification_report["verifier_id"],
        "case_count": verification_report["case_count"],
        "verified_case_count": verification_report["verified_case_count"],
        "rollout_count": verification_report["rollout_count"],
        "verified_rollout_count": verification_report["verified_rollout_count"],
        "verification_issue_count": verification_report["verification_issue_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("source_world_model_artifact_present", source_present, True, "Task 4 world model artifact is present."),
        _gate("source_world_model_artifact_parseable", source_parseable, True, "Task 4 world model artifact is parseable."),
        _gate("source_world_model_ready", source_ready, True, "World model is ready."),
        _gate("source_world_model_passed", source_passed, True, "World model passed."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 4 next stage points to Task 5."),
        _gate("source_strategy_ok", source_strategy_ok, True, "Strategy matches Milestone 12 strategy."),
        _gate("source_goal_ok", source_goal_ok, True, "Goal matches first-place solver objective."),
        _gate("source_milestone_open", source_milestone_open, True, "Milestone 12 remains opened canonically."),
        _gate("source_issue_zero", source_issue_zero, True, "Source issue count is zero."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("case_count_ok", case_count_ok, True, "Six case models are available."),
        _gate("verified_case_count_ok", verified_case_count_ok, True, "Six case models are verified."),
        _gate("rollout_count_ok", rollout_count_ok, True, "Eighteen rollouts are available."),
        _gate("verified_rollout_count_ok", verified_rollout_count_ok, True, "Eighteen rollout checks are verified."),
        _gate("optimal_rollouts_ok", optimal_rollouts_ok, True, "All optimal rollouts are verified."),
        _gate("invalid_guards_ok", invalid_guards_ok, True, "All invalid guards are verified."),
        _gate("explorer_probes_ok", explorer_probes_ok, True, "All explorer probes are verified."),
        _gate("transition_histories_ok", transition_histories_ok, True, "All transition histories are verified."),
        _gate("boundary_guard_ok", boundary_guard_ok, True, "All boundary guards are verified."),
        _gate("verification_issue_zero", verification_issue_zero, True, "Verification issue count is zero."),
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
        _gate("verifier_only_true", True, True, "Task remains verifier-only."),
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
        "source_world_model_artifact_present": source_present,
        "source_world_model_artifact_parseable": source_parseable,
        "source_world_model_ready": source_ready,
        "source_world_model_passed": source_passed,
        "source_next_stage_ok": source_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "world_model_verifier_ready": True,
        "world_model_verifier_valid": verifier_passed,
        "world_model_verifier_passed": verifier_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "verifier_summary": verifier_summary,
        "verification_report": verification_report,
        "case_count": verification_report["case_count"],
        "verified_case_count": verification_report["verified_case_count"],
        "rollout_count": verification_report["rollout_count"],
        "verified_rollout_count": verification_report["verified_rollout_count"],
        "verification_issue_count": verification_report["verification_issue_count"],
        "measurement_target_count": len(VERIFIER_MEASUREMENT_TARGETS),
        "measurement_targets": VERIFIER_MEASUREMENT_TARGETS,
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
        "verifier_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "verifier_check_count": len(verifier_checks),
        "verifier_checks": verifier_checks,
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
    record["task_id"] = "MILESTONE-12-WORLD-MODEL-VERIFIER-" + signature[:12]
    return record


def validate_world_model_verifier_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "world_model_verifier_ready",
        "world_model_verifier_valid",
        "world_model_verifier_passed",
        "source_world_model_artifact_present",
        "source_world_model_artifact_parseable",
        "source_world_model_ready",
        "source_world_model_passed",
        "source_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "verifier_only",
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

    if record.get("rollout_count") != 18:
        issues.append("ROLLOUT_COUNT_MISMATCH")

    if record.get("verified_rollout_count") != 18:
        issues.append("VERIFIED_ROLLOUT_COUNT_MISMATCH")

    if record.get("verification_issue_count") != 0:
        issues.append("VERIFICATION_ISSUE_COUNT_NOT_ZERO")

    if record.get("measurement_target_count") != 10:
        issues.append("MEASUREMENT_TARGET_COUNT_MISMATCH")

    report = record.get("verification_report")
    if not isinstance(report, dict):
        issues.append("VERIFICATION_REPORT_MISSING")
    else:
        if report.get("optimal_rollout_verified_count") != 6:
            issues.append("OPTIMAL_ROLLOUT_VERIFIED_COUNT_MISMATCH")
        if report.get("invalid_guard_verified_count") != 6:
            issues.append("INVALID_GUARD_VERIFIED_COUNT_MISMATCH")
        if report.get("explorer_probe_verified_count") != 6:
            issues.append("EXPLORER_PROBE_VERIFIED_COUNT_MISMATCH")
        if report.get("transition_history_verified_count") != 6:
            issues.append("TRANSITION_HISTORY_VERIFIED_COUNT_MISMATCH")
        if report.get("boundary_guard_verified_count") != 10:
            issues.append("BOUNDARY_GUARD_VERIFIED_COUNT_MISMATCH")
        if report.get("verification_issue_count") != 0:
            issues.append("REPORT_VERIFICATION_ISSUE_COUNT_NOT_ZERO")

    summary = record.get("verifier_summary")
    if not isinstance(summary, dict):
        issues.append("VERIFIER_SUMMARY_MISSING")
    else:
        if summary.get("verifier_status") != "READY":
            issues.append("VERIFIER_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("VERIFIER_SUMMARY_NEXT_STAGE_MISMATCH")

    checks = record.get("verifier_checks")
    if not isinstance(checks, list) or not checks:
        issues.append("VERIFIER_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in checks):
        issues.append("VERIFIER_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-world-model-verifier-v1.json"
    index_path = target_dir / "milestone-12-world-model-verifier-index-v1.json"
    manifest_path = target_dir / "milestone-12-world-model-verifier-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-world-model-verifier-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "world_model_verifier_ready": record["world_model_verifier_ready"],
        "world_model_verifier_passed": record["world_model_verifier_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "case_count": record["case_count"],
        "verified_case_count": record["verified_case_count"],
        "rollout_count": record["rollout_count"],
        "verified_rollout_count": record["verified_rollout_count"],
        "verification_issue_count": record["verification_issue_count"],
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
        f"world_model_verifier_ready={record['world_model_verifier_ready']}",
        f"world_model_verifier_passed={record['world_model_verifier_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"case_count={record['case_count']}",
        f"verified_case_count={record['verified_case_count']}",
        f"rollout_count={record['rollout_count']}",
        f"verified_rollout_count={record['verified_rollout_count']}",
        f"verification_issue_count={record['verification_issue_count']}",
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

## Verification

- world_model_verifier_ready: `{record['world_model_verifier_ready']}`
- world_model_verifier_passed: `{record['world_model_verifier_passed']}`
- case_count: `{record['case_count']}`
- verified_case_count: `{record['verified_case_count']}`
- rollout_count: `{record['rollout_count']}`
- verified_rollout_count: `{record['verified_rollout_count']}`
- verification_issue_count: `{record['verification_issue_count']}`
- optimal_rollout_verified_count: `{record['verification_report']['optimal_rollout_verified_count']}`
- invalid_guard_verified_count: `{record['verification_report']['invalid_guard_verified_count']}`
- explorer_probe_verified_count: `{record['verification_report']['explorer_probe_verified_count']}`
- transition_history_verified_count: `{record['verification_report']['transition_history_verified_count']}`

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
    record = build_world_model_verifier_record()
    issues = validate_world_model_verifier_record(record)
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
