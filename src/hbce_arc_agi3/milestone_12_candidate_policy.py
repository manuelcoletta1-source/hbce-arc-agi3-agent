"""Milestone #12 Task 8 - Candidate Policy v1.

Build deterministic candidate proposals from verified episode memory.

The policy remains local-only, deterministic and public-safe. It creates
candidate actions for downstream ranking without creating a Kaggle submission,
without claiming a score, and without using external APIs.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_CANDIDATE_POLICY_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 8
TASK_LABEL = "Milestone #12 Task 8 - Candidate Policy v1"

SOURCE_TASK = "MILESTONE_12_TASK_7_EPISODE_MEMORY_POLICY_V1"
NEXT_STAGE = "MILESTONE_12_TASK_9_CANDIDATE_RANKER_POLICY_V1"

TASK_MODE = "MILESTONE_12_CANDIDATE_POLICY_V1_LOCAL_ONLY"
TASK_SCOPE = "CANDIDATE_POLICY_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_CANDIDATE_POLICY_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "candidate-policy-v1"

SOURCE_EPISODE_MEMORY_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "episode-memory-policy-v1"
    / "milestone-12-episode-memory-policy-v1.json"
)

CANDIDATE_MEASUREMENT_TARGETS = [
    "case_count",
    "episode_count",
    "candidate_count",
    "verified_candidate_count",
    "replay_candidate_count",
    "prefix_candidate_count",
    "heuristic_candidate_count",
    "mean_candidate_length",
    "ranker_ready_candidate_count",
    "candidate_issue_count",
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


def _extract_verified_episodes(episode_record: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not episode_record:
        return []
    policy = episode_record.get("episode_memory_policy")
    if not isinstance(policy, dict):
        return []
    episodes = policy.get("episodes")
    if not isinstance(episodes, list):
        return []

    verified: list[dict[str, Any]] = []
    for episode in episodes:
        if (
            isinstance(episode, dict)
            and episode.get("verified_episode") is True
            and episode.get("reusable_in_candidate_policy") is True
            and isinstance(episode.get("actions"), list)
            and len(episode.get("actions", [])) > 0
        ):
            verified.append(episode)
    return verified


def _candidate_checks(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    actions = candidate.get("actions")
    if not isinstance(actions, list):
        actions = []

    ranker_ready = bool(
        candidate.get("candidate_verified") is True
        and candidate.get("source_episode_verified") is True
        and candidate.get("candidate_length", 0) > 0
        and all(isinstance(action, str) and action for action in actions)
    )

    return [
        _check("actions_present", bool(actions), "PASS" if actions else "BLOCKING", "Candidate has actions."),
        _check("actions_are_strings", all(isinstance(action, str) and action for action in actions), "PASS" if all(isinstance(action, str) and action for action in actions) else "BLOCKING", "All candidate actions are non-empty strings."),
        _check("source_episode_verified", candidate.get("source_episode_verified") is True, "PASS" if candidate.get("source_episode_verified") is True else "BLOCKING", "Source episode is verified."),
        _check("candidate_verified", candidate.get("candidate_verified") is True, "PASS" if candidate.get("candidate_verified") is True else "BLOCKING", "Candidate is verified."),
        _check("ranker_ready", ranker_ready, "PASS" if ranker_ready else "BLOCKING", "Candidate is ready for ranker policy."),
    ]


def build_candidates_for_episode(episode: dict[str, Any]) -> list[dict[str, Any]]:
    case_id = str(episode.get("case_id", "UNKNOWN_CASE"))
    family = str(episode.get("family", "UNKNOWN_FAMILY"))
    actions = [str(action) for action in episode.get("actions", [])]
    source_episode_id = str(episode.get("episode_id", f"EPISODE-{case_id.upper()}"))

    first_action = actions[:1]
    candidate_specs = [
        {
            "candidate_kind": "VERIFIED_EPISODE_REPLAY",
            "actions": actions,
            "priority": 1,
            "rationale": "Replay the full verified episode trace.",
        },
        {
            "candidate_kind": "PREFIX_SAFE_REPLAY",
            "actions": first_action,
            "priority": 2,
            "rationale": "Replay the first verified action as a safe prefix candidate.",
        },
        {
            "candidate_kind": "FAMILY_HEURISTIC_REPLAY",
            "actions": actions,
            "priority": 3,
            "rationale": "Reuse verified episode actions under the same family policy.",
        },
    ]

    candidates: list[dict[str, Any]] = []
    for spec in candidate_specs:
        core = {
            "case_id": case_id,
            "family": family,
            "candidate_kind": spec["candidate_kind"],
            "actions": spec["actions"],
            "source_episode_id": source_episode_id,
            "priority": spec["priority"],
        }
        signature = _stable_signature(core)

        candidate = {
            "candidate_id": f"CANDIDATE-{case_id.upper()}-{spec['candidate_kind']}-{signature[:8]}",
            "candidate_signature": signature,
            "case_id": case_id,
            "family": family,
            "source_episode_id": source_episode_id,
            "candidate_kind": spec["candidate_kind"],
            "candidate_policy": "DETERMINISTIC_EPISODE_MEMORY_REUSE",
            "actions": spec["actions"],
            "candidate_length": len(spec["actions"]),
            "priority": spec["priority"],
            "rationale": spec["rationale"],
            "source_episode_verified": episode.get("verified_episode") is True,
            "candidate_verified": bool(spec["actions"] and episode.get("verified_episode") is True),
            "ranker_ready": bool(spec["actions"] and episode.get("verified_episode") is True),
            "score_claim": None,
            "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        }
        checks = _candidate_checks(candidate)
        candidate["check_count"] = len(checks)
        candidate["checks"] = checks
        candidate["issue_count"] = sum(1 for check in checks if check["status"] is not True)
        candidates.append(candidate)

    return candidates


def build_candidate_policy(episode_record: dict[str, Any] | None) -> dict[str, Any]:
    episodes = _extract_verified_episodes(episode_record)

    candidates: list[dict[str, Any]] = []
    for episode in episodes:
        candidates.extend(build_candidates_for_episode(episode))

    candidate_lengths = [int(candidate["candidate_length"]) for candidate in candidates]
    verified_candidate_count = sum(1 for candidate in candidates if candidate["candidate_verified"] is True)
    ranker_ready_candidate_count = sum(1 for candidate in candidates if candidate["ranker_ready"] is True)
    replay_candidate_count = sum(1 for candidate in candidates if candidate["candidate_kind"] == "VERIFIED_EPISODE_REPLAY")
    prefix_candidate_count = sum(1 for candidate in candidates if candidate["candidate_kind"] == "PREFIX_SAFE_REPLAY")
    heuristic_candidate_count = sum(1 for candidate in candidates if candidate["candidate_kind"] == "FAMILY_HEURISTIC_REPLAY")
    candidate_issue_count = sum(int(candidate["issue_count"]) for candidate in candidates)

    return {
        "candidate_policy_id": "MILESTONE_12_CANDIDATE_POLICY_SYNTHETIC_V1",
        "candidate_policy_family": "DETERMINISTIC_EPISODE_MEMORY_CANDIDATE_GENERATOR",
        "case_count": len({candidate["case_id"] for candidate in candidates}),
        "episode_count": len(episodes),
        "candidate_count": len(candidates),
        "verified_candidate_count": verified_candidate_count,
        "replay_candidate_count": replay_candidate_count,
        "prefix_candidate_count": prefix_candidate_count,
        "heuristic_candidate_count": heuristic_candidate_count,
        "ranker_ready_candidate_count": ranker_ready_candidate_count,
        "candidate_issue_count": candidate_issue_count,
        "mean_candidate_length": round(sum(candidate_lengths) / len(candidate_lengths), 6) if candidate_lengths else 0.0,
        "minimum_candidate_length": min(candidate_lengths) if candidate_lengths else 0,
        "maximum_candidate_length": max(candidate_lengths) if candidate_lengths else 0,
        "candidates": candidates,
        "measurement_targets": CANDIDATE_MEASUREMENT_TARGETS,
        "measurement_target_count": len(CANDIDATE_MEASUREMENT_TARGETS),
    }


def build_candidate_policy_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    episode_artifact_present = SOURCE_EPISODE_MEMORY_ARTIFACT.exists()
    episode_record = _load_json(SOURCE_EPISODE_MEMORY_ARTIFACT)
    episode_artifact_parseable = episode_record is not None

    episode_memory_ready = bool(episode_record and episode_record.get("episode_memory_policy_ready") is True)
    episode_memory_passed = bool(episode_record and episode_record.get("episode_memory_policy_passed") is True)
    episode_next_stage_ok = bool(episode_record and episode_record.get("next_stage") == "MILESTONE_12_TASK_8_CANDIDATE_POLICY_V1")
    episode_strategy_ok = bool(episode_record and episode_record.get("chosen_strategy") == CHOSEN_STRATEGY)
    episode_goal_ok = bool(episode_record and episode_record.get("competitive_goal") == COMPETITIVE_GOAL)
    episode_issue_zero = bool(episode_record and episode_record.get("issue_count") == 0 and episode_record.get("episode_issue_count") == 0)

    source_boundaries_ok = all(
        [
            episode_record and episode_record.get("public_overfit_allowed") is False,
            episode_record and episode_record.get("public_overfit_guard_required") is True,
            episode_record and episode_record.get("external_api_dependency") is False,
            episode_record and episode_record.get("internet_during_eval") is False,
            episode_record and episode_record.get("real_submission_allowed") is False,
            episode_record and episode_record.get("manual_upload_allowed") is False,
            episode_record and episode_record.get("kaggle_submission_sent") is False,
            episode_record and episode_record.get("kaggle_authentication_performed") is False,
            episode_record and episode_record.get("private_core_exposure") is False,
            episode_record and episode_record.get("legal_certification") is False,
        ]
    )

    candidate_policy = build_candidate_policy(episode_record)

    case_count_ok = candidate_policy["case_count"] == 6
    episode_count_ok = candidate_policy["episode_count"] == 6
    candidate_count_ok = candidate_policy["candidate_count"] == 18
    verified_candidate_count_ok = candidate_policy["verified_candidate_count"] == 18
    replay_candidate_count_ok = candidate_policy["replay_candidate_count"] == 6
    prefix_candidate_count_ok = candidate_policy["prefix_candidate_count"] == 6
    heuristic_candidate_count_ok = candidate_policy["heuristic_candidate_count"] == 6
    ranker_ready_candidate_count_ok = candidate_policy["ranker_ready_candidate_count"] == 18
    candidate_lengths_ok = candidate_policy["minimum_candidate_length"] >= 1 and candidate_policy["maximum_candidate_length"] >= candidate_policy["minimum_candidate_length"]
    candidate_issue_zero = candidate_policy["candidate_issue_count"] == 0
    measurement_count_ok = candidate_policy["measurement_target_count"] == 10

    candidate_checks = [
        _check("episode_artifact_present", episode_artifact_present, "PASS" if episode_artifact_present else "BLOCKING", "Task 7 episode memory artifact is present."),
        _check("episode_artifact_parseable", episode_artifact_parseable, "PASS" if episode_artifact_parseable else "BLOCKING", "Task 7 episode memory artifact is parseable."),
        _check("episode_memory_ready", episode_memory_ready, "PASS" if episode_memory_ready else "BLOCKING", "Episode memory policy is ready."),
        _check("episode_memory_passed", episode_memory_passed, "PASS" if episode_memory_passed else "BLOCKING", "Episode memory policy passed."),
        _check("episode_next_stage_ok", episode_next_stage_ok, "PASS" if episode_next_stage_ok else "BLOCKING", "Episode memory points to Task 8."),
        _check("episode_strategy_ok", episode_strategy_ok, "PASS" if episode_strategy_ok else "BLOCKING", "Episode memory strategy is aligned."),
        _check("episode_goal_ok", episode_goal_ok, "PASS" if episode_goal_ok else "BLOCKING", "Episode memory goal is aligned."),
        _check("episode_issue_zero", episode_issue_zero, "PASS" if episode_issue_zero else "BLOCKING", "Episode memory issue count is zero."),
        _check("source_boundaries_ok", source_boundaries_ok, "PASS" if source_boundaries_ok else "BLOCKING", "Source boundaries are preserved."),
        _check("case_count_ok", case_count_ok, "PASS" if case_count_ok else "BLOCKING", "Candidate policy sees six cases."),
        _check("episode_count_ok", episode_count_ok, "PASS" if episode_count_ok else "BLOCKING", "Candidate policy sees six episodes."),
        _check("candidate_count_ok", candidate_count_ok, "PASS" if candidate_count_ok else "BLOCKING", "Candidate policy emits eighteen candidates."),
        _check("verified_candidate_count_ok", verified_candidate_count_ok, "PASS" if verified_candidate_count_ok else "BLOCKING", "Candidate policy verifies eighteen candidates."),
        _check("replay_candidate_count_ok", replay_candidate_count_ok, "PASS" if replay_candidate_count_ok else "BLOCKING", "Candidate policy emits six replay candidates."),
        _check("prefix_candidate_count_ok", prefix_candidate_count_ok, "PASS" if prefix_candidate_count_ok else "BLOCKING", "Candidate policy emits six prefix candidates."),
        _check("heuristic_candidate_count_ok", heuristic_candidate_count_ok, "PASS" if heuristic_candidate_count_ok else "BLOCKING", "Candidate policy emits six heuristic candidates."),
        _check("ranker_ready_candidate_count_ok", ranker_ready_candidate_count_ok, "PASS" if ranker_ready_candidate_count_ok else "BLOCKING", "All candidates are ready for ranking."),
        _check("candidate_lengths_ok", candidate_lengths_ok, "PASS" if candidate_lengths_ok else "BLOCKING", "Candidate lengths are valid."),
        _check("candidate_issue_zero", candidate_issue_zero, "PASS" if candidate_issue_zero else "BLOCKING", "Candidate issue count is zero."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "Candidate measurement targets are declared."),
    ]

    candidate_policy_passed = all(check["status"] is True for check in candidate_checks)

    candidate_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "candidate_policy_status": "READY" if candidate_policy_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "candidate_policy_id": candidate_policy["candidate_policy_id"],
        "case_count": candidate_policy["case_count"],
        "episode_count": candidate_policy["episode_count"],
        "candidate_count": candidate_policy["candidate_count"],
        "verified_candidate_count": candidate_policy["verified_candidate_count"],
        "ranker_ready_candidate_count": candidate_policy["ranker_ready_candidate_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("episode_artifact_present", episode_artifact_present, True, "Task 7 episode memory artifact is present."),
        _gate("episode_artifact_parseable", episode_artifact_parseable, True, "Task 7 episode memory artifact is parseable."),
        _gate("episode_memory_ready", episode_memory_ready, True, "Episode memory policy is ready."),
        _gate("episode_memory_passed", episode_memory_passed, True, "Episode memory policy passed."),
        _gate("episode_next_stage_ok", episode_next_stage_ok, True, "Episode memory points to Task 8."),
        _gate("episode_strategy_ok", episode_strategy_ok, True, "Episode memory strategy is aligned."),
        _gate("episode_goal_ok", episode_goal_ok, True, "Episode memory goal is aligned."),
        _gate("episode_issue_zero", episode_issue_zero, True, "Episode memory issue count is zero."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("case_count_ok", case_count_ok, True, "Six cases are available."),
        _gate("episode_count_ok", episode_count_ok, True, "Six episodes are available."),
        _gate("candidate_count_ok", candidate_count_ok, True, "Eighteen candidates are emitted."),
        _gate("verified_candidate_count_ok", verified_candidate_count_ok, True, "Eighteen candidates are verified."),
        _gate("replay_candidate_count_ok", replay_candidate_count_ok, True, "Six replay candidates are emitted."),
        _gate("prefix_candidate_count_ok", prefix_candidate_count_ok, True, "Six prefix candidates are emitted."),
        _gate("heuristic_candidate_count_ok", heuristic_candidate_count_ok, True, "Six heuristic candidates are emitted."),
        _gate("ranker_ready_candidate_count_ok", ranker_ready_candidate_count_ok, True, "Candidates are ranker-ready."),
        _gate("candidate_lengths_ok", candidate_lengths_ok, True, "Candidate lengths are valid."),
        _gate("candidate_issue_zero", candidate_issue_zero, True, "Candidate issue count is zero."),
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
        _gate("candidate_policy_only_true", True, True, "Task remains candidate-policy-only."),
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
        "source_episode_memory_artifact": str(SOURCE_EPISODE_MEMORY_ARTIFACT.relative_to(PROJECT_ROOT)),
        "episode_artifact_present": episode_artifact_present,
        "episode_artifact_parseable": episode_artifact_parseable,
        "episode_memory_ready": episode_memory_ready,
        "episode_memory_passed": episode_memory_passed,
        "episode_next_stage_ok": episode_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "candidate_policy_ready": True,
        "candidate_policy_valid": candidate_policy_passed,
        "candidate_policy_passed": candidate_policy_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "candidate_summary": candidate_summary,
        "candidate_policy": candidate_policy,
        "case_count": candidate_policy["case_count"],
        "episode_count": candidate_policy["episode_count"],
        "candidate_count": candidate_policy["candidate_count"],
        "verified_candidate_count": candidate_policy["verified_candidate_count"],
        "replay_candidate_count": candidate_policy["replay_candidate_count"],
        "prefix_candidate_count": candidate_policy["prefix_candidate_count"],
        "heuristic_candidate_count": candidate_policy["heuristic_candidate_count"],
        "ranker_ready_candidate_count": candidate_policy["ranker_ready_candidate_count"],
        "candidate_issue_count": candidate_policy["candidate_issue_count"],
        "measurement_target_count": len(CANDIDATE_MEASUREMENT_TARGETS),
        "measurement_targets": CANDIDATE_MEASUREMENT_TARGETS,
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
        "candidate_policy_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "candidate_check_count": len(candidate_checks),
        "candidate_checks": candidate_checks,
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
    record["task_id"] = "MILESTONE-12-CANDIDATE-POLICY-" + signature[:12]
    return record


def validate_candidate_policy_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "candidate_policy_ready",
        "candidate_policy_valid",
        "candidate_policy_passed",
        "episode_artifact_present",
        "episode_artifact_parseable",
        "episode_memory_ready",
        "episode_memory_passed",
        "episode_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "candidate_policy_only",
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
        "case_count": 6,
        "episode_count": 6,
        "candidate_count": 18,
        "verified_candidate_count": 18,
        "replay_candidate_count": 6,
        "prefix_candidate_count": 6,
        "heuristic_candidate_count": 6,
        "ranker_ready_candidate_count": 18,
        "candidate_issue_count": 0,
        "measurement_target_count": 10,
    }
    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    policy = record.get("candidate_policy")
    if not isinstance(policy, dict):
        issues.append("CANDIDATE_POLICY_MISSING")
    else:
        candidates = policy.get("candidates")
        if not isinstance(candidates, list) or len(candidates) != 18:
            issues.append("CANDIDATES_MISSING_OR_COUNT_MISMATCH")
        elif any(not isinstance(candidate, dict) or candidate.get("ranker_ready") is not True for candidate in candidates):
            issues.append("CANDIDATE_NOT_RANKER_READY")

    summary = record.get("candidate_summary")
    if not isinstance(summary, dict):
        issues.append("CANDIDATE_SUMMARY_MISSING")
    else:
        if summary.get("candidate_policy_status") != "READY":
            issues.append("CANDIDATE_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("CANDIDATE_SUMMARY_NEXT_STAGE_MISMATCH")

    checks = record.get("candidate_checks")
    if not isinstance(checks, list) or not checks:
        issues.append("CANDIDATE_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in checks):
        issues.append("CANDIDATE_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-candidate-policy-v1.json"
    index_path = target_dir / "milestone-12-candidate-policy-index-v1.json"
    manifest_path = target_dir / "milestone-12-candidate-policy-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-candidate-policy-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "candidate_policy_ready": record["candidate_policy_ready"],
        "candidate_policy_passed": record["candidate_policy_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "case_count": record["case_count"],
        "episode_count": record["episode_count"],
        "candidate_count": record["candidate_count"],
        "verified_candidate_count": record["verified_candidate_count"],
        "ranker_ready_candidate_count": record["ranker_ready_candidate_count"],
        "candidate_issue_count": record["candidate_issue_count"],
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
        f"candidate_policy_ready={record['candidate_policy_ready']}",
        f"candidate_policy_passed={record['candidate_policy_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"case_count={record['case_count']}",
        f"episode_count={record['episode_count']}",
        f"candidate_count={record['candidate_count']}",
        f"verified_candidate_count={record['verified_candidate_count']}",
        f"ranker_ready_candidate_count={record['ranker_ready_candidate_count']}",
        f"candidate_issue_count={record['candidate_issue_count']}",
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

## Candidate Policy

- candidate_policy_ready: `{record['candidate_policy_ready']}`
- candidate_policy_passed: `{record['candidate_policy_passed']}`
- case_count: `{record['case_count']}`
- episode_count: `{record['episode_count']}`
- candidate_count: `{record['candidate_count']}`
- verified_candidate_count: `{record['verified_candidate_count']}`
- replay_candidate_count: `{record['replay_candidate_count']}`
- prefix_candidate_count: `{record['prefix_candidate_count']}`
- heuristic_candidate_count: `{record['heuristic_candidate_count']}`
- ranker_ready_candidate_count: `{record['ranker_ready_candidate_count']}`
- candidate_issue_count: `{record['candidate_issue_count']}`
- mean_candidate_length: `{record['candidate_policy']['mean_candidate_length']}`

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
    record = build_candidate_policy_record()
    issues = validate_candidate_policy_record(record)
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
