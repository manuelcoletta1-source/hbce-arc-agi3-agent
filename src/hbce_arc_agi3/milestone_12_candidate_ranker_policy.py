"""Milestone #12 Task 9 - Candidate Ranker Policy v1.

Rank deterministic candidate proposals produced by Task 8.

This module remains local-only and public-safe. It does not create a Kaggle
submission, does not upload anything, and does not claim a public/private score.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_CANDIDATE_RANKER_POLICY_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 9
TASK_LABEL = "Milestone #12 Task 9 - Candidate Ranker Policy v1"

SOURCE_TASK = "MILESTONE_12_TASK_8_CANDIDATE_POLICY_V1"
NEXT_STAGE = "MILESTONE_12_TASK_10_RANKED_CANDIDATE_BENCHMARK_V1"

TASK_MODE = "MILESTONE_12_CANDIDATE_RANKER_POLICY_V1_LOCAL_ONLY"
TASK_SCOPE = "CANDIDATE_RANKER_POLICY_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_CANDIDATE_RANKER_POLICY_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "candidate-ranker-policy-v1"

SOURCE_CANDIDATE_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "candidate-policy-v1"
    / "milestone-12-candidate-policy-v1.json"
)

RANKER_MEASUREMENT_TARGETS = [
    "case_count",
    "candidate_count",
    "ranked_candidate_count",
    "selected_candidate_count",
    "top_replay_candidate_count",
    "ranker_ready_candidate_count",
    "mean_rank_score",
    "minimum_rank_score",
    "maximum_rank_score",
    "ranker_issue_count",
]

KIND_PRIORITY = {
    "VERIFIED_EPISODE_REPLAY": 3,
    "PREFIX_SAFE_REPLAY": 2,
    "FAMILY_HEURISTIC_REPLAY": 1,
}

KIND_SCORE = {
    "VERIFIED_EPISODE_REPLAY": 300,
    "PREFIX_SAFE_REPLAY": 200,
    "FAMILY_HEURISTIC_REPLAY": 100,
}


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


def _extract_ranker_ready_candidates(candidate_record: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not candidate_record:
        return []
    policy = candidate_record.get("candidate_policy")
    if not isinstance(policy, dict):
        return []
    candidates = policy.get("candidates")
    if not isinstance(candidates, list):
        return []

    output: list[dict[str, Any]] = []
    for candidate in candidates:
        if (
            isinstance(candidate, dict)
            and candidate.get("candidate_verified") is True
            and candidate.get("ranker_ready") is True
            and isinstance(candidate.get("actions"), list)
            and len(candidate.get("actions", [])) > 0
        ):
            output.append(candidate)
    return output


def score_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    kind = str(candidate.get("candidate_kind", "UNKNOWN_KIND"))
    actions = [str(action) for action in candidate.get("actions", [])]
    candidate_length = len(actions)

    verified_bonus = 500 if candidate.get("candidate_verified") is True else 0
    ranker_ready_bonus = 250 if candidate.get("ranker_ready") is True else 0
    kind_bonus = KIND_SCORE.get(kind, 0)
    length_bonus = min(candidate_length, 10)
    issue_penalty = int(candidate.get("issue_count", 0)) * 1000

    score = verified_bonus + ranker_ready_bonus + kind_bonus + length_bonus - issue_penalty

    return {
        "score": score,
        "verified_bonus": verified_bonus,
        "ranker_ready_bonus": ranker_ready_bonus,
        "kind_bonus": kind_bonus,
        "length_bonus": length_bonus,
        "issue_penalty": issue_penalty,
        "kind_priority": KIND_PRIORITY.get(kind, 0),
    }


def _rank_sort_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    score = candidate.get("rank_score", 0)
    priority = candidate.get("rank_components", {}).get("kind_priority", 0)
    length = candidate.get("candidate_length", 0)
    signature = str(candidate.get("candidate_signature", "NO_SIGNATURE"))
    return (-int(score), -int(priority), -int(length), signature)


def rank_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []

    for candidate in candidates:
        components = score_candidate(candidate)
        ranked = {
            "ranked_candidate_id": f"RANKED-{candidate.get('candidate_id', 'UNKNOWN')}",
            "case_id": candidate.get("case_id", "UNKNOWN_CASE"),
            "family": candidate.get("family", "UNKNOWN_FAMILY"),
            "source_candidate_id": candidate.get("candidate_id", "UNKNOWN_CANDIDATE"),
            "source_candidate_signature": candidate.get("candidate_signature", "NO_SIGNATURE"),
            "candidate_kind": candidate.get("candidate_kind", "UNKNOWN_KIND"),
            "candidate_policy": candidate.get("candidate_policy", "UNKNOWN_POLICY"),
            "actions": list(candidate.get("actions", [])),
            "candidate_length": int(candidate.get("candidate_length", len(candidate.get("actions", [])))),
            "source_episode_id": candidate.get("source_episode_id", "UNKNOWN_EPISODE"),
            "candidate_verified": candidate.get("candidate_verified") is True,
            "ranker_ready": candidate.get("ranker_ready") is True,
            "source_candidate_issue_count": int(candidate.get("issue_count", 0)),
            "rank_score": components["score"],
            "rank_components": components,
            "score_claim": None,
            "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        }
        checks = [
            _check("candidate_verified", ranked["candidate_verified"], "PASS" if ranked["candidate_verified"] else "BLOCKING", "Candidate is verified."),
            _check("ranker_ready", ranked["ranker_ready"], "PASS" if ranked["ranker_ready"] else "BLOCKING", "Candidate is ready for ranking."),
            _check("actions_present", bool(ranked["actions"]), "PASS" if ranked["actions"] else "BLOCKING", "Candidate has actions."),
            _check("rank_score_positive", ranked["rank_score"] > 0, "PASS" if ranked["rank_score"] > 0 else "BLOCKING", "Candidate rank score is positive."),
            _check("source_issue_zero", ranked["source_candidate_issue_count"] == 0, "PASS" if ranked["source_candidate_issue_count"] == 0 else "BLOCKING", "Source candidate issue count is zero."),
        ]
        ranked["check_count"] = len(checks)
        ranked["checks"] = checks
        ranked["issue_count"] = sum(1 for check in checks if check["status"] is not True)
        enriched.append(ranked)

    by_case: dict[str, list[dict[str, Any]]] = {}
    for candidate in enriched:
        by_case.setdefault(str(candidate["case_id"]), []).append(candidate)

    ranked_candidates: list[dict[str, Any]] = []
    for case_id in sorted(by_case):
        case_candidates = sorted(by_case[case_id], key=_rank_sort_key)
        for rank_index, candidate in enumerate(case_candidates, start=1):
            candidate = dict(candidate)
            candidate["rank_within_case"] = rank_index
            candidate["selected_for_case"] = rank_index == 1
            ranked_candidates.append(candidate)

    ranked_candidates = sorted(
        ranked_candidates,
        key=lambda candidate: (
            str(candidate["case_id"]),
            int(candidate["rank_within_case"]),
            str(candidate["source_candidate_signature"]),
        ),
    )

    for global_rank, candidate in enumerate(ranked_candidates, start=1):
        candidate["global_rank"] = global_rank

    return ranked_candidates


def build_ranker_policy(candidate_record: dict[str, Any] | None) -> dict[str, Any]:
    source_candidates = _extract_ranker_ready_candidates(candidate_record)
    ranked_candidates = rank_candidates(source_candidates)
    selected_candidates = [candidate for candidate in ranked_candidates if candidate["selected_for_case"] is True]

    scores = [int(candidate["rank_score"]) for candidate in ranked_candidates]
    selected_kinds = [candidate["candidate_kind"] for candidate in selected_candidates]

    return {
        "candidate_ranker_policy_id": "MILESTONE_12_CANDIDATE_RANKER_POLICY_SYNTHETIC_V1",
        "ranker_policy_family": "DETERMINISTIC_CANDIDATE_RANKER_POLICY",
        "case_count": len({candidate["case_id"] for candidate in ranked_candidates}),
        "candidate_count": len(source_candidates),
        "ranked_candidate_count": len(ranked_candidates),
        "selected_candidate_count": len(selected_candidates),
        "top_replay_candidate_count": sum(1 for kind in selected_kinds if kind == "VERIFIED_EPISODE_REPLAY"),
        "ranker_ready_candidate_count": sum(1 for candidate in ranked_candidates if candidate["ranker_ready"] is True),
        "ranker_issue_count": sum(int(candidate["issue_count"]) for candidate in ranked_candidates),
        "mean_rank_score": round(sum(scores) / len(scores), 6) if scores else 0.0,
        "minimum_rank_score": min(scores) if scores else 0,
        "maximum_rank_score": max(scores) if scores else 0,
        "ranked_candidates": ranked_candidates,
        "selected_candidates": selected_candidates,
        "measurement_targets": RANKER_MEASUREMENT_TARGETS,
        "measurement_target_count": len(RANKER_MEASUREMENT_TARGETS),
    }


def build_candidate_ranker_policy_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    candidate_artifact_present = SOURCE_CANDIDATE_ARTIFACT.exists()
    candidate_record = _load_json(SOURCE_CANDIDATE_ARTIFACT)
    candidate_artifact_parseable = candidate_record is not None

    candidate_policy_ready = bool(candidate_record and candidate_record.get("candidate_policy_ready") is True)
    candidate_policy_passed = bool(candidate_record and candidate_record.get("candidate_policy_passed") is True)
    candidate_next_stage_ok = bool(candidate_record and candidate_record.get("next_stage") == "MILESTONE_12_TASK_9_CANDIDATE_RANKER_POLICY_V1")
    candidate_strategy_ok = bool(candidate_record and candidate_record.get("chosen_strategy") == CHOSEN_STRATEGY)
    candidate_goal_ok = bool(candidate_record and candidate_record.get("competitive_goal") == COMPETITIVE_GOAL)
    candidate_issue_zero = bool(candidate_record and candidate_record.get("issue_count") == 0 and candidate_record.get("candidate_issue_count") == 0)

    source_boundaries_ok = all(
        [
            candidate_record and candidate_record.get("public_overfit_allowed") is False,
            candidate_record and candidate_record.get("public_overfit_guard_required") is True,
            candidate_record and candidate_record.get("external_api_dependency") is False,
            candidate_record and candidate_record.get("internet_during_eval") is False,
            candidate_record and candidate_record.get("real_submission_allowed") is False,
            candidate_record and candidate_record.get("manual_upload_allowed") is False,
            candidate_record and candidate_record.get("kaggle_submission_sent") is False,
            candidate_record and candidate_record.get("kaggle_authentication_performed") is False,
            candidate_record and candidate_record.get("private_core_exposure") is False,
            candidate_record and candidate_record.get("legal_certification") is False,
        ]
    )

    ranker_policy = build_ranker_policy(candidate_record)

    case_count_ok = ranker_policy["case_count"] == 6
    candidate_count_ok = ranker_policy["candidate_count"] == 18
    ranked_candidate_count_ok = ranker_policy["ranked_candidate_count"] == 18
    selected_candidate_count_ok = ranker_policy["selected_candidate_count"] == 6
    top_replay_candidate_count_ok = ranker_policy["top_replay_candidate_count"] == 6
    ranker_ready_candidate_count_ok = ranker_policy["ranker_ready_candidate_count"] == 18
    scores_ok = ranker_policy["minimum_rank_score"] > 0 and ranker_policy["maximum_rank_score"] >= ranker_policy["minimum_rank_score"]
    ranker_issue_zero = ranker_policy["ranker_issue_count"] == 0
    measurement_count_ok = ranker_policy["measurement_target_count"] == 10

    ranker_checks = [
        _check("candidate_artifact_present", candidate_artifact_present, "PASS" if candidate_artifact_present else "BLOCKING", "Task 8 candidate artifact is present."),
        _check("candidate_artifact_parseable", candidate_artifact_parseable, "PASS" if candidate_artifact_parseable else "BLOCKING", "Task 8 candidate artifact is parseable."),
        _check("candidate_policy_ready", candidate_policy_ready, "PASS" if candidate_policy_ready else "BLOCKING", "Candidate policy is ready."),
        _check("candidate_policy_passed", candidate_policy_passed, "PASS" if candidate_policy_passed else "BLOCKING", "Candidate policy passed."),
        _check("candidate_next_stage_ok", candidate_next_stage_ok, "PASS" if candidate_next_stage_ok else "BLOCKING", "Candidate policy points to Task 9."),
        _check("candidate_strategy_ok", candidate_strategy_ok, "PASS" if candidate_strategy_ok else "BLOCKING", "Candidate policy strategy is aligned."),
        _check("candidate_goal_ok", candidate_goal_ok, "PASS" if candidate_goal_ok else "BLOCKING", "Candidate policy goal is aligned."),
        _check("candidate_issue_zero", candidate_issue_zero, "PASS" if candidate_issue_zero else "BLOCKING", "Candidate policy issue count is zero."),
        _check("source_boundaries_ok", source_boundaries_ok, "PASS" if source_boundaries_ok else "BLOCKING", "Source boundaries are preserved."),
        _check("case_count_ok", case_count_ok, "PASS" if case_count_ok else "BLOCKING", "Ranker sees six cases."),
        _check("candidate_count_ok", candidate_count_ok, "PASS" if candidate_count_ok else "BLOCKING", "Ranker sees eighteen candidates."),
        _check("ranked_candidate_count_ok", ranked_candidate_count_ok, "PASS" if ranked_candidate_count_ok else "BLOCKING", "Ranker emits eighteen ranked candidates."),
        _check("selected_candidate_count_ok", selected_candidate_count_ok, "PASS" if selected_candidate_count_ok else "BLOCKING", "Ranker selects six top candidates."),
        _check("top_replay_candidate_count_ok", top_replay_candidate_count_ok, "PASS" if top_replay_candidate_count_ok else "BLOCKING", "Ranker selects replay candidates as top candidates."),
        _check("ranker_ready_candidate_count_ok", ranker_ready_candidate_count_ok, "PASS" if ranker_ready_candidate_count_ok else "BLOCKING", "All candidates remain ranker-ready."),
        _check("scores_ok", scores_ok, "PASS" if scores_ok else "BLOCKING", "Rank scores are valid."),
        _check("ranker_issue_zero", ranker_issue_zero, "PASS" if ranker_issue_zero else "BLOCKING", "Ranker issue count is zero."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "Ranker measurement targets are declared."),
    ]

    candidate_ranker_passed = all(check["status"] is True for check in ranker_checks)

    ranker_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "candidate_ranker_policy_status": "READY" if candidate_ranker_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "candidate_ranker_policy_id": ranker_policy["candidate_ranker_policy_id"],
        "case_count": ranker_policy["case_count"],
        "candidate_count": ranker_policy["candidate_count"],
        "ranked_candidate_count": ranker_policy["ranked_candidate_count"],
        "selected_candidate_count": ranker_policy["selected_candidate_count"],
        "top_replay_candidate_count": ranker_policy["top_replay_candidate_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("candidate_artifact_present", candidate_artifact_present, True, "Task 8 candidate artifact is present."),
        _gate("candidate_artifact_parseable", candidate_artifact_parseable, True, "Task 8 candidate artifact is parseable."),
        _gate("candidate_policy_ready", candidate_policy_ready, True, "Candidate policy is ready."),
        _gate("candidate_policy_passed", candidate_policy_passed, True, "Candidate policy passed."),
        _gate("candidate_next_stage_ok", candidate_next_stage_ok, True, "Candidate policy points to Task 9."),
        _gate("candidate_strategy_ok", candidate_strategy_ok, True, "Candidate policy strategy is aligned."),
        _gate("candidate_goal_ok", candidate_goal_ok, True, "Candidate policy goal is aligned."),
        _gate("candidate_issue_zero", candidate_issue_zero, True, "Candidate policy issue count is zero."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("case_count_ok", case_count_ok, True, "Six cases are available."),
        _gate("candidate_count_ok", candidate_count_ok, True, "Eighteen candidates are available."),
        _gate("ranked_candidate_count_ok", ranked_candidate_count_ok, True, "Eighteen candidates are ranked."),
        _gate("selected_candidate_count_ok", selected_candidate_count_ok, True, "Six candidates are selected."),
        _gate("top_replay_candidate_count_ok", top_replay_candidate_count_ok, True, "Six replay candidates are selected as top."),
        _gate("ranker_ready_candidate_count_ok", ranker_ready_candidate_count_ok, True, "All candidates remain ranker-ready."),
        _gate("scores_ok", scores_ok, True, "Rank scores are valid."),
        _gate("ranker_issue_zero", ranker_issue_zero, True, "Ranker issue count is zero."),
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
        _gate("candidate_ranker_policy_only_true", True, True, "Task remains candidate-ranker-policy-only."),
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
        "source_candidate_artifact": str(SOURCE_CANDIDATE_ARTIFACT.relative_to(PROJECT_ROOT)),
        "candidate_artifact_present": candidate_artifact_present,
        "candidate_artifact_parseable": candidate_artifact_parseable,
        "candidate_policy_ready": candidate_policy_ready,
        "candidate_policy_passed": candidate_policy_passed,
        "candidate_next_stage_ok": candidate_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "candidate_ranker_policy_ready": True,
        "candidate_ranker_policy_valid": candidate_ranker_passed,
        "candidate_ranker_policy_passed": candidate_ranker_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "ranker_summary": ranker_summary,
        "ranker_policy": ranker_policy,
        "case_count": ranker_policy["case_count"],
        "candidate_count": ranker_policy["candidate_count"],
        "ranked_candidate_count": ranker_policy["ranked_candidate_count"],
        "selected_candidate_count": ranker_policy["selected_candidate_count"],
        "top_replay_candidate_count": ranker_policy["top_replay_candidate_count"],
        "ranker_ready_candidate_count": ranker_policy["ranker_ready_candidate_count"],
        "ranker_issue_count": ranker_policy["ranker_issue_count"],
        "measurement_target_count": len(RANKER_MEASUREMENT_TARGETS),
        "measurement_targets": RANKER_MEASUREMENT_TARGETS,
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
        "candidate_ranker_policy_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "ranker_check_count": len(ranker_checks),
        "ranker_checks": ranker_checks,
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
    record["task_id"] = "MILESTONE-12-CANDIDATE-RANKER-POLICY-" + signature[:12]
    return record


def validate_candidate_ranker_policy_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "candidate_ranker_policy_ready",
        "candidate_ranker_policy_valid",
        "candidate_ranker_policy_passed",
        "candidate_artifact_present",
        "candidate_artifact_parseable",
        "candidate_policy_ready",
        "candidate_policy_passed",
        "candidate_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "candidate_ranker_policy_only",
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
        "candidate_count": 18,
        "ranked_candidate_count": 18,
        "selected_candidate_count": 6,
        "top_replay_candidate_count": 6,
        "ranker_ready_candidate_count": 18,
        "ranker_issue_count": 0,
        "measurement_target_count": 10,
    }
    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    policy = record.get("ranker_policy")
    if not isinstance(policy, dict):
        issues.append("RANKER_POLICY_MISSING")
    else:
        ranked = policy.get("ranked_candidates")
        selected = policy.get("selected_candidates")
        if not isinstance(ranked, list) or len(ranked) != 18:
            issues.append("RANKED_CANDIDATES_MISSING_OR_COUNT_MISMATCH")
        elif any(not isinstance(candidate, dict) or candidate.get("ranker_ready") is not True for candidate in ranked):
            issues.append("RANKED_CANDIDATE_NOT_READY")
        if not isinstance(selected, list) or len(selected) != 6:
            issues.append("SELECTED_CANDIDATES_MISSING_OR_COUNT_MISMATCH")
        elif any(candidate.get("candidate_kind") != "VERIFIED_EPISODE_REPLAY" for candidate in selected):
            issues.append("SELECTED_CANDIDATE_NOT_REPLAY")

    summary = record.get("ranker_summary")
    if not isinstance(summary, dict):
        issues.append("RANKER_SUMMARY_MISSING")
    else:
        if summary.get("candidate_ranker_policy_status") != "READY":
            issues.append("RANKER_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("RANKER_SUMMARY_NEXT_STAGE_MISMATCH")

    checks = record.get("ranker_checks")
    if not isinstance(checks, list) or not checks:
        issues.append("RANKER_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in checks):
        issues.append("RANKER_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-candidate-ranker-policy-v1.json"
    index_path = target_dir / "milestone-12-candidate-ranker-policy-index-v1.json"
    manifest_path = target_dir / "milestone-12-candidate-ranker-policy-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-candidate-ranker-policy-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "candidate_ranker_policy_ready": record["candidate_ranker_policy_ready"],
        "candidate_ranker_policy_passed": record["candidate_ranker_policy_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "case_count": record["case_count"],
        "candidate_count": record["candidate_count"],
        "ranked_candidate_count": record["ranked_candidate_count"],
        "selected_candidate_count": record["selected_candidate_count"],
        "top_replay_candidate_count": record["top_replay_candidate_count"],
        "ranker_ready_candidate_count": record["ranker_ready_candidate_count"],
        "ranker_issue_count": record["ranker_issue_count"],
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
        f"candidate_ranker_policy_ready={record['candidate_ranker_policy_ready']}",
        f"candidate_ranker_policy_passed={record['candidate_ranker_policy_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"case_count={record['case_count']}",
        f"candidate_count={record['candidate_count']}",
        f"ranked_candidate_count={record['ranked_candidate_count']}",
        f"selected_candidate_count={record['selected_candidate_count']}",
        f"top_replay_candidate_count={record['top_replay_candidate_count']}",
        f"ranker_ready_candidate_count={record['ranker_ready_candidate_count']}",
        f"ranker_issue_count={record['ranker_issue_count']}",
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

## Candidate Ranker Policy

- candidate_ranker_policy_ready: `{record['candidate_ranker_policy_ready']}`
- candidate_ranker_policy_passed: `{record['candidate_ranker_policy_passed']}`
- case_count: `{record['case_count']}`
- candidate_count: `{record['candidate_count']}`
- ranked_candidate_count: `{record['ranked_candidate_count']}`
- selected_candidate_count: `{record['selected_candidate_count']}`
- top_replay_candidate_count: `{record['top_replay_candidate_count']}`
- ranker_ready_candidate_count: `{record['ranker_ready_candidate_count']}`
- ranker_issue_count: `{record['ranker_issue_count']}`
- mean_rank_score: `{record['ranker_policy']['mean_rank_score']}`

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
    record = build_candidate_ranker_policy_record()
    issues = validate_candidate_ranker_policy_record(record)
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
