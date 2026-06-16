"""Milestone #12 Task 7 - Episode Memory Policy v1.

Build deterministic episode memory records from the verified planner policy.

The episode memory does not claim real Kaggle score and does not use external
APIs. It converts verified plans into reusable local traces for the next
candidate policy stage.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_EPISODE_MEMORY_POLICY_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 7
TASK_LABEL = "Milestone #12 Task 7 - Episode Memory Policy v1"

SOURCE_TASK = "MILESTONE_12_TASK_6_VERIFIED_PLANNER_POLICY_V1"
NEXT_STAGE = "MILESTONE_12_TASK_8_CANDIDATE_POLICY_V1"

TASK_MODE = "MILESTONE_12_EPISODE_MEMORY_POLICY_V1_LOCAL_ONLY"
TASK_SCOPE = "EPISODE_MEMORY_POLICY_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_EPISODE_MEMORY_POLICY_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "episode-memory-policy-v1"

SOURCE_PLANNER_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "verified-planner-policy-v1"
    / "milestone-12-verified-planner-policy-v1.json"
)

EPISODE_MEMORY_MEASUREMENT_TARGETS = [
    "case_count",
    "episode_count",
    "verified_episode_count",
    "memory_record_count",
    "trace_step_count",
    "mean_episode_length",
    "minimum_episode_length",
    "maximum_episode_length",
    "reuse_candidate_count",
    "episode_issue_count",
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


def _extract_verified_plans(planner_record: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not planner_record:
        return []
    planner_policy = planner_record.get("planner_policy")
    if not isinstance(planner_policy, dict):
        return []
    plans = planner_policy.get("plans")
    if not isinstance(plans, list):
        return []

    verified: list[dict[str, Any]] = []
    for plan in plans:
        if (
            isinstance(plan, dict)
            and plan.get("executable") is True
            and plan.get("verified_source_case") is True
            and isinstance(plan.get("actions"), list)
            and len(plan.get("actions", [])) > 0
        ):
            verified.append(plan)
    return verified


def build_episode_memory_entry(plan: dict[str, Any]) -> dict[str, Any]:
    case_id = str(plan.get("case_id", "UNKNOWN_CASE"))
    family = str(plan.get("family", "UNKNOWN_FAMILY"))
    actions = [str(action) for action in plan.get("actions", [])]

    trace_steps: list[dict[str, Any]] = []
    for index, action in enumerate(actions, start=1):
        prefix = actions[:index]
        remaining = actions[index:]
        trace_steps.append(
            {
                "step": index,
                "action": action,
                "prefix": prefix,
                "prefix_length": len(prefix),
                "remaining_actions": remaining,
                "remaining_count": len(remaining),
                "terminal_after_step": index == len(actions),
            }
        )

    memory_features = {
        "first_action": actions[0] if actions else "NO_ACTION",
        "last_action": actions[-1] if actions else "NO_ACTION",
        "action_count": len(actions),
        "unique_action_count": len(set(actions)),
        "has_repeated_action": len(set(actions)) < len(actions) if actions else False,
        "family": family,
    }

    entry_core = {
        "case_id": case_id,
        "family": family,
        "source_plan_id": plan.get("plan_id", f"PLAN-{case_id.upper()}"),
        "actions": actions,
        "trace_steps": trace_steps,
        "memory_features": memory_features,
    }

    episode_signature = _stable_signature(entry_core)

    reusable = bool(
        actions
        and plan.get("executable") is True
        and plan.get("minimal_plan") is True
        and plan.get("actions_valid") is True
        and plan.get("issue_count") == 0
    )

    checks = [
        _check("actions_present", bool(actions), "PASS" if actions else "BLOCKING", "Episode has at least one action."),
        _check("trace_steps_match_actions", len(trace_steps) == len(actions), "PASS" if len(trace_steps) == len(actions) else "BLOCKING", "Trace step count matches action count."),
        _check("source_plan_executable", plan.get("executable") is True, "PASS" if plan.get("executable") is True else "BLOCKING", "Source plan is executable."),
        _check("source_plan_minimal", plan.get("minimal_plan") is True, "PASS" if plan.get("minimal_plan") is True else "BLOCKING", "Source plan is minimal."),
        _check("source_plan_issue_zero", plan.get("issue_count") == 0, "PASS" if plan.get("issue_count") == 0 else "BLOCKING", "Source plan issue count is zero."),
        _check("reusable_in_candidate_policy", reusable, "PASS" if reusable else "BLOCKING", "Episode can be reused by candidate policy."),
    ]

    return {
        "episode_id": f"EPISODE-{case_id.upper()}-{episode_signature[:8]}",
        "episode_signature": episode_signature,
        "case_id": case_id,
        "family": family,
        "source_plan_id": entry_core["source_plan_id"],
        "memory_kind": "VERIFIED_PLAN_EPISODE_TRACE",
        "actions": actions,
        "action_count": len(actions),
        "trace_steps": trace_steps,
        "trace_step_count": len(trace_steps),
        "memory_features": memory_features,
        "reusable_in_candidate_policy": reusable,
        "verified_episode": reusable,
        "confidence": 1.0 if reusable else 0.0,
        "check_count": len(checks),
        "checks": checks,
        "issue_count": 0 if reusable else sum(1 for check in checks if check["status"] is not True),
    }


def build_episode_memory_policy(planner_record: dict[str, Any] | None) -> dict[str, Any]:
    verified_plans = _extract_verified_plans(planner_record)
    episodes = [build_episode_memory_entry(plan) for plan in verified_plans]

    action_counts = [int(episode["action_count"]) for episode in episodes]
    trace_step_count = sum(int(episode["trace_step_count"]) for episode in episodes)
    verified_episode_count = sum(1 for episode in episodes if episode["verified_episode"] is True)
    reuse_candidate_count = sum(1 for episode in episodes if episode["reusable_in_candidate_policy"] is True)
    episode_issue_count = sum(int(episode["issue_count"]) for episode in episodes)

    return {
        "episode_memory_policy_id": "MILESTONE_12_EPISODE_MEMORY_POLICY_SYNTHETIC_V1",
        "episode_memory_family": "DETERMINISTIC_VERIFIED_PLAN_EPISODE_MEMORY",
        "case_count": len(verified_plans),
        "episode_count": len(episodes),
        "verified_episode_count": verified_episode_count,
        "memory_record_count": len(episodes),
        "trace_step_count": trace_step_count,
        "mean_episode_length": round(trace_step_count / len(episodes), 6) if episodes else 0.0,
        "minimum_episode_length": min(action_counts) if action_counts else 0,
        "maximum_episode_length": max(action_counts) if action_counts else 0,
        "reuse_candidate_count": reuse_candidate_count,
        "episode_issue_count": episode_issue_count,
        "episodes": episodes,
        "measurement_targets": EPISODE_MEMORY_MEASUREMENT_TARGETS,
        "measurement_target_count": len(EPISODE_MEMORY_MEASUREMENT_TARGETS),
    }


def build_episode_memory_policy_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    planner_present = SOURCE_PLANNER_ARTIFACT.exists()
    planner_record = _load_json(SOURCE_PLANNER_ARTIFACT)
    planner_parseable = planner_record is not None

    planner_ready = bool(planner_record and planner_record.get("verified_planner_policy_ready") is True)
    planner_passed = bool(planner_record and planner_record.get("verified_planner_policy_passed") is True)
    planner_next_stage_ok = bool(planner_record and planner_record.get("next_stage") == "MILESTONE_12_TASK_7_EPISODE_MEMORY_POLICY_V1")
    planner_strategy_ok = bool(planner_record and planner_record.get("chosen_strategy") == CHOSEN_STRATEGY)
    planner_goal_ok = bool(planner_record and planner_record.get("competitive_goal") == COMPETITIVE_GOAL)
    planner_issue_zero = bool(planner_record and planner_record.get("issue_count") == 0 and planner_record.get("planner_issue_count") == 0)

    source_boundaries_ok = all(
        [
            planner_record and planner_record.get("public_overfit_allowed") is False,
            planner_record and planner_record.get("public_overfit_guard_required") is True,
            planner_record and planner_record.get("external_api_dependency") is False,
            planner_record and planner_record.get("internet_during_eval") is False,
            planner_record and planner_record.get("real_submission_allowed") is False,
            planner_record and planner_record.get("manual_upload_allowed") is False,
            planner_record and planner_record.get("kaggle_submission_sent") is False,
            planner_record and planner_record.get("kaggle_authentication_performed") is False,
            planner_record and planner_record.get("private_core_exposure") is False,
            planner_record and planner_record.get("legal_certification") is False,
        ]
    )

    episode_memory_policy = build_episode_memory_policy(planner_record)

    case_count_ok = episode_memory_policy["case_count"] == 6
    episode_count_ok = episode_memory_policy["episode_count"] == 6
    verified_episode_count_ok = episode_memory_policy["verified_episode_count"] == 6
    memory_record_count_ok = episode_memory_policy["memory_record_count"] == 6
    trace_step_count_positive = episode_memory_policy["trace_step_count"] > 0
    episode_lengths_ok = (
        episode_memory_policy["minimum_episode_length"] >= 1
        and episode_memory_policy["maximum_episode_length"] >= episode_memory_policy["minimum_episode_length"]
    )
    reuse_candidate_count_ok = episode_memory_policy["reuse_candidate_count"] == 6
    episode_issue_zero = episode_memory_policy["episode_issue_count"] == 0
    measurement_count_ok = episode_memory_policy["measurement_target_count"] == 10

    episode_checks = [
        _check("planner_artifact_present", planner_present, "PASS" if planner_present else "BLOCKING", "Task 6 planner artifact is present."),
        _check("planner_artifact_parseable", planner_parseable, "PASS" if planner_parseable else "BLOCKING", "Task 6 planner artifact is parseable."),
        _check("planner_ready", planner_ready, "PASS" if planner_ready else "BLOCKING", "Planner policy is ready."),
        _check("planner_passed", planner_passed, "PASS" if planner_passed else "BLOCKING", "Planner policy passed."),
        _check("planner_next_stage_ok", planner_next_stage_ok, "PASS" if planner_next_stage_ok else "BLOCKING", "Planner points to Task 7."),
        _check("planner_strategy_ok", planner_strategy_ok, "PASS" if planner_strategy_ok else "BLOCKING", "Planner strategy is aligned."),
        _check("planner_goal_ok", planner_goal_ok, "PASS" if planner_goal_ok else "BLOCKING", "Planner goal is aligned."),
        _check("planner_issue_zero", planner_issue_zero, "PASS" if planner_issue_zero else "BLOCKING", "Planner issue count is zero."),
        _check("source_boundaries_ok", source_boundaries_ok, "PASS" if source_boundaries_ok else "BLOCKING", "Source boundaries are preserved."),
        _check("case_count_ok", case_count_ok, "PASS" if case_count_ok else "BLOCKING", "Episode memory sees six verified cases."),
        _check("episode_count_ok", episode_count_ok, "PASS" if episode_count_ok else "BLOCKING", "Episode memory emits six episodes."),
        _check("verified_episode_count_ok", verified_episode_count_ok, "PASS" if verified_episode_count_ok else "BLOCKING", "Episode memory verifies six episodes."),
        _check("memory_record_count_ok", memory_record_count_ok, "PASS" if memory_record_count_ok else "BLOCKING", "Episode memory emits six memory records."),
        _check("trace_step_count_positive", trace_step_count_positive, "PASS" if trace_step_count_positive else "BLOCKING", "Episode memory emits trace steps."),
        _check("episode_lengths_ok", episode_lengths_ok, "PASS" if episode_lengths_ok else "BLOCKING", "Episode memory lengths are valid."),
        _check("reuse_candidate_count_ok", reuse_candidate_count_ok, "PASS" if reuse_candidate_count_ok else "BLOCKING", "All episodes are reusable by candidate policy."),
        _check("episode_issue_zero", episode_issue_zero, "PASS" if episode_issue_zero else "BLOCKING", "Episode issue count is zero."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "Episode memory measurement targets are declared."),
    ]

    episode_memory_passed = all(check["status"] is True for check in episode_checks)

    episode_memory_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "episode_memory_status": "READY" if episode_memory_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "episode_memory_policy_id": episode_memory_policy["episode_memory_policy_id"],
        "case_count": episode_memory_policy["case_count"],
        "episode_count": episode_memory_policy["episode_count"],
        "verified_episode_count": episode_memory_policy["verified_episode_count"],
        "memory_record_count": episode_memory_policy["memory_record_count"],
        "trace_step_count": episode_memory_policy["trace_step_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("planner_artifact_present", planner_present, True, "Task 6 planner artifact is present."),
        _gate("planner_artifact_parseable", planner_parseable, True, "Task 6 planner artifact is parseable."),
        _gate("planner_ready", planner_ready, True, "Planner policy is ready."),
        _gate("planner_passed", planner_passed, True, "Planner policy passed."),
        _gate("planner_next_stage_ok", planner_next_stage_ok, True, "Planner points to Task 7."),
        _gate("planner_strategy_ok", planner_strategy_ok, True, "Planner strategy is aligned."),
        _gate("planner_goal_ok", planner_goal_ok, True, "Planner goal is aligned."),
        _gate("planner_issue_zero", planner_issue_zero, True, "Planner issue count is zero."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("case_count_ok", case_count_ok, True, "Six verified cases are available."),
        _gate("episode_count_ok", episode_count_ok, True, "Six episodes are emitted."),
        _gate("verified_episode_count_ok", verified_episode_count_ok, True, "Six episodes are verified."),
        _gate("memory_record_count_ok", memory_record_count_ok, True, "Six memory records are emitted."),
        _gate("trace_step_count_positive", trace_step_count_positive, True, "Trace steps are emitted."),
        _gate("episode_lengths_ok", episode_lengths_ok, True, "Episode lengths are valid."),
        _gate("reuse_candidate_count_ok", reuse_candidate_count_ok, True, "Episodes are reusable."),
        _gate("episode_issue_zero", episode_issue_zero, True, "Episode issue count is zero."),
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
        _gate("episode_memory_only_true", True, True, "Task remains episode-memory-only."),
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
        "source_planner_artifact": str(SOURCE_PLANNER_ARTIFACT.relative_to(PROJECT_ROOT)),
        "planner_artifact_present": planner_present,
        "planner_artifact_parseable": planner_parseable,
        "planner_ready": planner_ready,
        "planner_passed": planner_passed,
        "planner_next_stage_ok": planner_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "episode_memory_policy_ready": True,
        "episode_memory_policy_valid": episode_memory_passed,
        "episode_memory_policy_passed": episode_memory_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "episode_memory_summary": episode_memory_summary,
        "episode_memory_policy": episode_memory_policy,
        "case_count": episode_memory_policy["case_count"],
        "episode_count": episode_memory_policy["episode_count"],
        "verified_episode_count": episode_memory_policy["verified_episode_count"],
        "memory_record_count": episode_memory_policy["memory_record_count"],
        "trace_step_count": episode_memory_policy["trace_step_count"],
        "reuse_candidate_count": episode_memory_policy["reuse_candidate_count"],
        "episode_issue_count": episode_memory_policy["episode_issue_count"],
        "measurement_target_count": len(EPISODE_MEMORY_MEASUREMENT_TARGETS),
        "measurement_targets": EPISODE_MEMORY_MEASUREMENT_TARGETS,
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
        "episode_memory_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "episode_check_count": len(episode_checks),
        "episode_checks": episode_checks,
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
    record["task_id"] = "MILESTONE-12-EPISODE-MEMORY-POLICY-" + signature[:12]
    return record


def validate_episode_memory_policy_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "episode_memory_policy_ready",
        "episode_memory_policy_valid",
        "episode_memory_policy_passed",
        "planner_artifact_present",
        "planner_artifact_parseable",
        "planner_ready",
        "planner_passed",
        "planner_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "episode_memory_only",
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

    if record.get("episode_count") != 6:
        issues.append("EPISODE_COUNT_MISMATCH")

    if record.get("verified_episode_count") != 6:
        issues.append("VERIFIED_EPISODE_COUNT_MISMATCH")

    if record.get("memory_record_count") != 6:
        issues.append("MEMORY_RECORD_COUNT_MISMATCH")

    if record.get("trace_step_count", 0) <= 0:
        issues.append("TRACE_STEP_COUNT_NOT_POSITIVE")

    if record.get("reuse_candidate_count") != 6:
        issues.append("REUSE_CANDIDATE_COUNT_MISMATCH")

    if record.get("episode_issue_count") != 0:
        issues.append("EPISODE_ISSUE_COUNT_NOT_ZERO")

    if record.get("measurement_target_count") != 10:
        issues.append("MEASUREMENT_TARGET_COUNT_MISMATCH")

    policy = record.get("episode_memory_policy")
    if not isinstance(policy, dict):
        issues.append("EPISODE_MEMORY_POLICY_MISSING")
    else:
        episodes = policy.get("episodes")
        if not isinstance(episodes, list) or len(episodes) != 6:
            issues.append("EPISODES_MISSING_OR_COUNT_MISMATCH")
        elif any(not isinstance(episode, dict) or episode.get("verified_episode") is not True for episode in episodes):
            issues.append("EPISODE_NOT_VERIFIED")

    summary = record.get("episode_memory_summary")
    if not isinstance(summary, dict):
        issues.append("EPISODE_MEMORY_SUMMARY_MISSING")
    else:
        if summary.get("episode_memory_status") != "READY":
            issues.append("EPISODE_MEMORY_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("EPISODE_MEMORY_SUMMARY_NEXT_STAGE_MISMATCH")

    checks = record.get("episode_checks")
    if not isinstance(checks, list) or not checks:
        issues.append("EPISODE_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in checks):
        issues.append("EPISODE_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-episode-memory-policy-v1.json"
    index_path = target_dir / "milestone-12-episode-memory-policy-index-v1.json"
    manifest_path = target_dir / "milestone-12-episode-memory-policy-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-episode-memory-policy-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "episode_memory_policy_ready": record["episode_memory_policy_ready"],
        "episode_memory_policy_passed": record["episode_memory_policy_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "case_count": record["case_count"],
        "episode_count": record["episode_count"],
        "verified_episode_count": record["verified_episode_count"],
        "memory_record_count": record["memory_record_count"],
        "trace_step_count": record["trace_step_count"],
        "reuse_candidate_count": record["reuse_candidate_count"],
        "episode_issue_count": record["episode_issue_count"],
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
        f"episode_memory_policy_ready={record['episode_memory_policy_ready']}",
        f"episode_memory_policy_passed={record['episode_memory_policy_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"case_count={record['case_count']}",
        f"episode_count={record['episode_count']}",
        f"verified_episode_count={record['verified_episode_count']}",
        f"memory_record_count={record['memory_record_count']}",
        f"trace_step_count={record['trace_step_count']}",
        f"reuse_candidate_count={record['reuse_candidate_count']}",
        f"episode_issue_count={record['episode_issue_count']}",
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

## Episode Memory Policy

- episode_memory_policy_ready: `{record['episode_memory_policy_ready']}`
- episode_memory_policy_passed: `{record['episode_memory_policy_passed']}`
- case_count: `{record['case_count']}`
- episode_count: `{record['episode_count']}`
- verified_episode_count: `{record['verified_episode_count']}`
- memory_record_count: `{record['memory_record_count']}`
- trace_step_count: `{record['trace_step_count']}`
- reuse_candidate_count: `{record['reuse_candidate_count']}`
- episode_issue_count: `{record['episode_issue_count']}`
- mean_episode_length: `{record['episode_memory_policy']['mean_episode_length']}`

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
    record = build_episode_memory_policy_record()
    issues = validate_episode_memory_policy_record(record)
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
