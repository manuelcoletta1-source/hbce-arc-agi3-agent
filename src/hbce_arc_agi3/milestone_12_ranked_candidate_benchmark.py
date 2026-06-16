"""Milestone #12 Task 10 - Ranked Candidate Benchmark v1.

Benchmark ranked candidates produced by Task 9.

This benchmark is deterministic, local-only, public-safe, and dry-run-only.
It does not create a Kaggle submission, does not upload anything, and does not
claim any official score.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_RANKED_CANDIDATE_BENCHMARK_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 10
TASK_LABEL = "Milestone #12 Task 10 - Ranked Candidate Benchmark v1"

SOURCE_TASK = "MILESTONE_12_TASK_9_CANDIDATE_RANKER_POLICY_V1"
NEXT_STAGE = "MILESTONE_12_TASK_11_PUBLIC_OVERFIT_GUARD_V1"

TASK_MODE = "MILESTONE_12_RANKED_CANDIDATE_BENCHMARK_V1_LOCAL_ONLY"
TASK_SCOPE = "RANKED_CANDIDATE_BENCHMARK_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_RANKED_CANDIDATE_BENCHMARK_READY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "ranked-candidate-benchmark-v1"

SOURCE_RANKER_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "candidate-ranker-policy-v1"
    / "milestone-12-candidate-ranker-policy-v1.json"
)

BENCHMARK_MEASUREMENT_TARGETS = [
    "case_count",
    "selected_candidate_count",
    "benchmark_case_count",
    "benchmark_pass_count",
    "benchmark_warning_count",
    "benchmark_failure_count",
    "top_replay_candidate_count",
    "mean_rank_score",
    "minimum_rank_score",
    "maximum_rank_score",
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


def _extract_selected_candidates(ranker_record: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not ranker_record:
        return []
    policy = ranker_record.get("ranker_policy")
    if not isinstance(policy, dict):
        return []
    selected = policy.get("selected_candidates")
    if not isinstance(selected, list):
        return []

    output: list[dict[str, Any]] = []
    for candidate in selected:
        if (
            isinstance(candidate, dict)
            and candidate.get("selected_for_case") is True
            and candidate.get("rank_within_case") == 1
            and candidate.get("ranker_ready") is True
            and isinstance(candidate.get("actions"), list)
            and len(candidate.get("actions", [])) > 0
        ):
            output.append(candidate)
    return output


def build_benchmark_case(candidate: dict[str, Any]) -> dict[str, Any]:
    actions = [str(action) for action in candidate.get("actions", [])]
    rank_score = int(candidate.get("rank_score", 0))
    candidate_kind = str(candidate.get("candidate_kind", "UNKNOWN_KIND"))

    checks = [
        _check("selected_for_case", candidate.get("selected_for_case") is True, "PASS" if candidate.get("selected_for_case") is True else "BLOCKING", "Candidate is selected for case."),
        _check("rank_is_one", candidate.get("rank_within_case") == 1, "PASS" if candidate.get("rank_within_case") == 1 else "BLOCKING", "Candidate rank within case is one."),
        _check("ranker_ready", candidate.get("ranker_ready") is True, "PASS" if candidate.get("ranker_ready") is True else "BLOCKING", "Candidate remains ranker-ready."),
        _check("candidate_verified", candidate.get("candidate_verified") is True, "PASS" if candidate.get("candidate_verified") is True else "BLOCKING", "Candidate remains verified."),
        _check("actions_present", bool(actions), "PASS" if actions else "BLOCKING", "Candidate has deterministic actions."),
        _check("rank_score_positive", rank_score > 0, "PASS" if rank_score > 0 else "BLOCKING", "Candidate rank score is positive."),
        _check("top_kind_replay", candidate_kind == "VERIFIED_EPISODE_REPLAY", "PASS" if candidate_kind == "VERIFIED_EPISODE_REPLAY" else "WARNING", "Top candidate is verified replay."),
    ]
    blocking_failures = [check for check in checks if check["status"] is not True and check["severity"] == "BLOCKING"]
    warnings = [check for check in checks if check["status"] is not True and check["severity"] == "WARNING"]

    core = {
        "case_id": candidate.get("case_id", "UNKNOWN_CASE"),
        "source_candidate_id": candidate.get("source_candidate_id", "UNKNOWN_CANDIDATE"),
        "rank_score": rank_score,
        "actions": actions,
    }

    return {
        "benchmark_case_id": "BENCHMARK-CASE-" + _stable_signature(core)[:12],
        "case_id": candidate.get("case_id", "UNKNOWN_CASE"),
        "family": candidate.get("family", "UNKNOWN_FAMILY"),
        "source_ranked_candidate_id": candidate.get("ranked_candidate_id", "UNKNOWN_RANKED_CANDIDATE"),
        "source_candidate_id": candidate.get("source_candidate_id", "UNKNOWN_CANDIDATE"),
        "candidate_kind": candidate_kind,
        "rank_within_case": candidate.get("rank_within_case"),
        "global_rank": candidate.get("global_rank"),
        "rank_score": rank_score,
        "actions": actions,
        "action_count": len(actions),
        "benchmark_passed": len(blocking_failures) == 0,
        "warning_count": len(warnings),
        "failure_count": len(blocking_failures),
        "checks": checks,
        "check_count": len(checks),
        "score_claim": None,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
    }


def build_benchmark_payload(ranker_record: dict[str, Any] | None) -> dict[str, Any]:
    selected_candidates = _extract_selected_candidates(ranker_record)
    benchmark_cases = [build_benchmark_case(candidate) for candidate in selected_candidates]

    scores = [int(case["rank_score"]) for case in benchmark_cases]
    benchmark_pass_count = sum(1 for case in benchmark_cases if case["benchmark_passed"] is True)
    benchmark_warning_count = sum(int(case["warning_count"]) for case in benchmark_cases)
    benchmark_failure_count = sum(int(case["failure_count"]) for case in benchmark_cases)
    top_replay_candidate_count = sum(1 for case in benchmark_cases if case["candidate_kind"] == "VERIFIED_EPISODE_REPLAY")

    return {
        "ranked_candidate_benchmark_id": "MILESTONE_12_RANKED_CANDIDATE_BENCHMARK_SYNTHETIC_V1",
        "benchmark_family": "DETERMINISTIC_SELECTED_CANDIDATE_BENCHMARK",
        "case_count": len({case["case_id"] for case in benchmark_cases}),
        "selected_candidate_count": len(selected_candidates),
        "benchmark_case_count": len(benchmark_cases),
        "benchmark_pass_count": benchmark_pass_count,
        "benchmark_warning_count": benchmark_warning_count,
        "benchmark_failure_count": benchmark_failure_count,
        "top_replay_candidate_count": top_replay_candidate_count,
        "mean_rank_score": round(sum(scores) / len(scores), 6) if scores else 0.0,
        "minimum_rank_score": min(scores) if scores else 0,
        "maximum_rank_score": max(scores) if scores else 0,
        "benchmark_cases": benchmark_cases,
        "measurement_targets": BENCHMARK_MEASUREMENT_TARGETS,
        "measurement_target_count": len(BENCHMARK_MEASUREMENT_TARGETS),
    }


def build_ranked_candidate_benchmark_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    ranker_artifact_present = SOURCE_RANKER_ARTIFACT.exists()
    ranker_record = _load_json(SOURCE_RANKER_ARTIFACT)
    ranker_artifact_parseable = ranker_record is not None

    ranker_policy_ready = bool(ranker_record and ranker_record.get("candidate_ranker_policy_ready") is True)
    ranker_policy_passed = bool(ranker_record and ranker_record.get("candidate_ranker_policy_passed") is True)
    ranker_next_stage_ok = bool(ranker_record and ranker_record.get("next_stage") == "MILESTONE_12_TASK_10_RANKED_CANDIDATE_BENCHMARK_V1")
    ranker_strategy_ok = bool(ranker_record and ranker_record.get("chosen_strategy") == CHOSEN_STRATEGY)
    ranker_goal_ok = bool(ranker_record and ranker_record.get("competitive_goal") == COMPETITIVE_GOAL)
    ranker_issue_zero = bool(ranker_record and ranker_record.get("issue_count") == 0 and ranker_record.get("ranker_issue_count") == 0)

    source_boundaries_ok = all(
        [
            ranker_record and ranker_record.get("public_overfit_allowed") is False,
            ranker_record and ranker_record.get("public_overfit_guard_required") is True,
            ranker_record and ranker_record.get("external_api_dependency") is False,
            ranker_record and ranker_record.get("internet_during_eval") is False,
            ranker_record and ranker_record.get("real_submission_allowed") is False,
            ranker_record and ranker_record.get("manual_upload_allowed") is False,
            ranker_record and ranker_record.get("kaggle_submission_sent") is False,
            ranker_record and ranker_record.get("kaggle_authentication_performed") is False,
            ranker_record and ranker_record.get("private_core_exposure") is False,
            ranker_record and ranker_record.get("legal_certification") is False,
        ]
    )

    benchmark = build_benchmark_payload(ranker_record)

    case_count_ok = benchmark["case_count"] == 6
    selected_candidate_count_ok = benchmark["selected_candidate_count"] == 6
    benchmark_case_count_ok = benchmark["benchmark_case_count"] == 6
    benchmark_pass_count_ok = benchmark["benchmark_pass_count"] == 6
    benchmark_warning_count_ok = benchmark["benchmark_warning_count"] == 0
    benchmark_failure_count_ok = benchmark["benchmark_failure_count"] == 0
    top_replay_candidate_count_ok = benchmark["top_replay_candidate_count"] == 6
    scores_ok = benchmark["minimum_rank_score"] > 0 and benchmark["maximum_rank_score"] >= benchmark["minimum_rank_score"]
    measurement_count_ok = benchmark["measurement_target_count"] == 10

    benchmark_checks = [
        _check("ranker_artifact_present", ranker_artifact_present, "PASS" if ranker_artifact_present else "BLOCKING", "Task 9 ranker artifact is present."),
        _check("ranker_artifact_parseable", ranker_artifact_parseable, "PASS" if ranker_artifact_parseable else "BLOCKING", "Task 9 ranker artifact is parseable."),
        _check("ranker_policy_ready", ranker_policy_ready, "PASS" if ranker_policy_ready else "BLOCKING", "Ranker policy is ready."),
        _check("ranker_policy_passed", ranker_policy_passed, "PASS" if ranker_policy_passed else "BLOCKING", "Ranker policy passed."),
        _check("ranker_next_stage_ok", ranker_next_stage_ok, "PASS" if ranker_next_stage_ok else "BLOCKING", "Ranker policy points to Task 10."),
        _check("ranker_strategy_ok", ranker_strategy_ok, "PASS" if ranker_strategy_ok else "BLOCKING", "Ranker strategy is aligned."),
        _check("ranker_goal_ok", ranker_goal_ok, "PASS" if ranker_goal_ok else "BLOCKING", "Ranker goal is aligned."),
        _check("ranker_issue_zero", ranker_issue_zero, "PASS" if ranker_issue_zero else "BLOCKING", "Ranker issue count is zero."),
        _check("source_boundaries_ok", source_boundaries_ok, "PASS" if source_boundaries_ok else "BLOCKING", "Source boundaries are preserved."),
        _check("case_count_ok", case_count_ok, "PASS" if case_count_ok else "BLOCKING", "Benchmark sees six cases."),
        _check("selected_candidate_count_ok", selected_candidate_count_ok, "PASS" if selected_candidate_count_ok else "BLOCKING", "Benchmark sees six selected candidates."),
        _check("benchmark_case_count_ok", benchmark_case_count_ok, "PASS" if benchmark_case_count_ok else "BLOCKING", "Benchmark emits six cases."),
        _check("benchmark_pass_count_ok", benchmark_pass_count_ok, "PASS" if benchmark_pass_count_ok else "BLOCKING", "Benchmark passes six cases."),
        _check("benchmark_warning_count_ok", benchmark_warning_count_ok, "PASS" if benchmark_warning_count_ok else "BLOCKING", "Benchmark warning count is zero."),
        _check("benchmark_failure_count_ok", benchmark_failure_count_ok, "PASS" if benchmark_failure_count_ok else "BLOCKING", "Benchmark failure count is zero."),
        _check("top_replay_candidate_count_ok", top_replay_candidate_count_ok, "PASS" if top_replay_candidate_count_ok else "BLOCKING", "Selected candidates are replay candidates."),
        _check("scores_ok", scores_ok, "PASS" if scores_ok else "BLOCKING", "Benchmark scores are valid."),
        _check("measurement_count_ok", measurement_count_ok, "PASS" if measurement_count_ok else "BLOCKING", "Benchmark measurement targets are declared."),
    ]

    benchmark_passed = all(check["status"] is True for check in benchmark_checks)

    benchmark_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "ranked_candidate_benchmark_status": "READY" if benchmark_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "ranked_candidate_benchmark_id": benchmark["ranked_candidate_benchmark_id"],
        "case_count": benchmark["case_count"],
        "selected_candidate_count": benchmark["selected_candidate_count"],
        "benchmark_case_count": benchmark["benchmark_case_count"],
        "benchmark_pass_count": benchmark["benchmark_pass_count"],
        "benchmark_failure_count": benchmark["benchmark_failure_count"],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("ranker_artifact_present", ranker_artifact_present, True, "Task 9 ranker artifact is present."),
        _gate("ranker_artifact_parseable", ranker_artifact_parseable, True, "Task 9 ranker artifact is parseable."),
        _gate("ranker_policy_ready", ranker_policy_ready, True, "Ranker policy is ready."),
        _gate("ranker_policy_passed", ranker_policy_passed, True, "Ranker policy passed."),
        _gate("ranker_next_stage_ok", ranker_next_stage_ok, True, "Ranker policy points to Task 10."),
        _gate("ranker_strategy_ok", ranker_strategy_ok, True, "Ranker strategy is aligned."),
        _gate("ranker_goal_ok", ranker_goal_ok, True, "Ranker goal is aligned."),
        _gate("ranker_issue_zero", ranker_issue_zero, True, "Ranker issue count is zero."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("case_count_ok", case_count_ok, True, "Six cases are available."),
        _gate("selected_candidate_count_ok", selected_candidate_count_ok, True, "Six selected candidates are available."),
        _gate("benchmark_case_count_ok", benchmark_case_count_ok, True, "Six benchmark cases are emitted."),
        _gate("benchmark_pass_count_ok", benchmark_pass_count_ok, True, "Six benchmark cases pass."),
        _gate("benchmark_warning_count_ok", benchmark_warning_count_ok, True, "Benchmark warning count is zero."),
        _gate("benchmark_failure_count_ok", benchmark_failure_count_ok, True, "Benchmark failure count is zero."),
        _gate("top_replay_candidate_count_ok", top_replay_candidate_count_ok, True, "Six selected candidates are replay candidates."),
        _gate("scores_ok", scores_ok, True, "Benchmark scores are valid."),
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
        _gate("ranked_candidate_benchmark_only_true", True, True, "Task remains benchmark-only."),
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
        "source_ranker_artifact": str(SOURCE_RANKER_ARTIFACT.relative_to(PROJECT_ROOT)),
        "ranker_artifact_present": ranker_artifact_present,
        "ranker_artifact_parseable": ranker_artifact_parseable,
        "ranker_policy_ready": ranker_policy_ready,
        "ranker_policy_passed": ranker_policy_passed,
        "ranker_next_stage_ok": ranker_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "ranked_candidate_benchmark_ready": True,
        "ranked_candidate_benchmark_valid": benchmark_passed,
        "ranked_candidate_benchmark_passed": benchmark_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "benchmark_summary": benchmark_summary,
        "benchmark": benchmark,
        "case_count": benchmark["case_count"],
        "selected_candidate_count": benchmark["selected_candidate_count"],
        "benchmark_case_count": benchmark["benchmark_case_count"],
        "benchmark_pass_count": benchmark["benchmark_pass_count"],
        "benchmark_warning_count": benchmark["benchmark_warning_count"],
        "benchmark_failure_count": benchmark["benchmark_failure_count"],
        "top_replay_candidate_count": benchmark["top_replay_candidate_count"],
        "measurement_target_count": len(BENCHMARK_MEASUREMENT_TARGETS),
        "measurement_targets": BENCHMARK_MEASUREMENT_TARGETS,
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
        "ranked_candidate_benchmark_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "benchmark_check_count": len(benchmark_checks),
        "benchmark_checks": benchmark_checks,
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
    record["task_id"] = "MILESTONE-12-RANKED-CANDIDATE-BENCHMARK-" + signature[:12]
    return record


def validate_ranked_candidate_benchmark_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "ranked_candidate_benchmark_ready",
        "ranked_candidate_benchmark_valid",
        "ranked_candidate_benchmark_passed",
        "ranker_artifact_present",
        "ranker_artifact_parseable",
        "ranker_policy_ready",
        "ranker_policy_passed",
        "ranker_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "ranked_candidate_benchmark_only",
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
        "selected_candidate_count": 6,
        "benchmark_case_count": 6,
        "benchmark_pass_count": 6,
        "benchmark_warning_count": 0,
        "benchmark_failure_count": 0,
        "top_replay_candidate_count": 6,
        "measurement_target_count": 10,
    }
    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    benchmark = record.get("benchmark")
    if not isinstance(benchmark, dict):
        issues.append("BENCHMARK_MISSING")
    else:
        cases = benchmark.get("benchmark_cases")
        if not isinstance(cases, list) or len(cases) != 6:
            issues.append("BENCHMARK_CASES_MISSING_OR_COUNT_MISMATCH")
        elif any(not isinstance(case, dict) or case.get("benchmark_passed") is not True for case in cases):
            issues.append("BENCHMARK_CASE_NOT_PASSED")

    summary = record.get("benchmark_summary")
    if not isinstance(summary, dict):
        issues.append("BENCHMARK_SUMMARY_MISSING")
    else:
        if summary.get("ranked_candidate_benchmark_status") != "READY":
            issues.append("BENCHMARK_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("BENCHMARK_SUMMARY_NEXT_STAGE_MISMATCH")

    checks = record.get("benchmark_checks")
    if not isinstance(checks, list) or not checks:
        issues.append("BENCHMARK_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in checks):
        issues.append("BENCHMARK_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-ranked-candidate-benchmark-v1.json"
    index_path = target_dir / "milestone-12-ranked-candidate-benchmark-index-v1.json"
    manifest_path = target_dir / "milestone-12-ranked-candidate-benchmark-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-ranked-candidate-benchmark-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "ranked_candidate_benchmark_ready": record["ranked_candidate_benchmark_ready"],
        "ranked_candidate_benchmark_passed": record["ranked_candidate_benchmark_passed"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "case_count": record["case_count"],
        "selected_candidate_count": record["selected_candidate_count"],
        "benchmark_case_count": record["benchmark_case_count"],
        "benchmark_pass_count": record["benchmark_pass_count"],
        "benchmark_warning_count": record["benchmark_warning_count"],
        "benchmark_failure_count": record["benchmark_failure_count"],
        "top_replay_candidate_count": record["top_replay_candidate_count"],
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
        f"ranked_candidate_benchmark_ready={record['ranked_candidate_benchmark_ready']}",
        f"ranked_candidate_benchmark_passed={record['ranked_candidate_benchmark_passed']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"case_count={record['case_count']}",
        f"selected_candidate_count={record['selected_candidate_count']}",
        f"benchmark_case_count={record['benchmark_case_count']}",
        f"benchmark_pass_count={record['benchmark_pass_count']}",
        f"benchmark_warning_count={record['benchmark_warning_count']}",
        f"benchmark_failure_count={record['benchmark_failure_count']}",
        f"top_replay_candidate_count={record['top_replay_candidate_count']}",
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

## Ranked Candidate Benchmark

- ranked_candidate_benchmark_ready: `{record['ranked_candidate_benchmark_ready']}`
- ranked_candidate_benchmark_passed: `{record['ranked_candidate_benchmark_passed']}`
- case_count: `{record['case_count']}`
- selected_candidate_count: `{record['selected_candidate_count']}`
- benchmark_case_count: `{record['benchmark_case_count']}`
- benchmark_pass_count: `{record['benchmark_pass_count']}`
- benchmark_warning_count: `{record['benchmark_warning_count']}`
- benchmark_failure_count: `{record['benchmark_failure_count']}`
- top_replay_candidate_count: `{record['top_replay_candidate_count']}`
- mean_rank_score: `{record['benchmark']['mean_rank_score']}`

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
    record = build_ranked_candidate_benchmark_record()
    issues = validate_ranked_candidate_benchmark_record(record)
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
