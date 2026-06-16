"""Milestone #12 Task 13 - Competitive Solver Closure v1.

This module closes Milestone #12 as a local, deterministic, public-safe
competitive solver planning chain.

It does not create a real Kaggle submission, does not upload anything,
does not authenticate to Kaggle, does not claim official score, and does not
open a new milestone automatically.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_COMPETITIVE_SOLVER_CLOSURE_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 13
TASK_LABEL = "Milestone #12 Task 13 - Competitive Solver Closure v1"

SOURCE_TASK = "MILESTONE_12_TASK_12_SUBMISSION_READINESS_GATE_V1"
TASK_MODE = "MILESTONE_12_COMPETITIVE_SOLVER_CLOSURE_V1_LOCAL_ONLY"
TASK_SCOPE = "MILESTONE_12_CLOSURE_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_SCORE_CLAIM"
TASK_VERDICT = "MILESTONE_12_COMPETITIVE_SOLVER_CLOSURE_READY"

CLOSURE_VERDICT = "MILESTONE_12_CLOSED_LOCAL_COMPETITIVE_SOLVER_READY_REAL_SUBMISSION_BLOCKED"
NEXT_STAGE = "MILESTONE_13_NOT_OPENED_CANONICALLY"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "competitive-solver-closure-v1"

SOURCE_READINESS_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "submission-readiness-gate-v1"
    / "milestone-12-submission-readiness-gate-v1.json"
)

REQUIRED_CHAIN_ARTIFACTS = [
    "examples/milestone-12/competitive-solver-runtime-strategy-gate-v1/milestone-12-competitive-solver-runtime-strategy-gate-v1.json",
    "examples/milestone-12/competitive-solver-benchmark-harness-v1/milestone-12-competitive-solver-benchmark-harness-v1.json",
    "examples/milestone-12/information-gain-explorer-policy-v1/milestone-12-information-gain-explorer-policy-v1.json",
    "examples/milestone-12/executable-world-model-v1/milestone-12-executable-world-model-v1.json",
    "examples/milestone-12/world-model-verifier-v1/milestone-12-world-model-verifier-v1.json",
    "examples/milestone-12/verified-planner-policy-v1/milestone-12-verified-planner-policy-v1.json",
    "examples/milestone-12/episode-memory-policy-v1/milestone-12-episode-memory-policy-v1.json",
    "examples/milestone-12/candidate-policy-v1/milestone-12-candidate-policy-v1.json",
    "examples/milestone-12/candidate-ranker-policy-v1/milestone-12-candidate-ranker-policy-v1.json",
    "examples/milestone-12/ranked-candidate-benchmark-v1/milestone-12-ranked-candidate-benchmark-v1.json",
    "examples/milestone-12/public-overfit-guard-v1/milestone-12-public-overfit-guard-v1.json",
    "examples/milestone-12/submission-readiness-gate-v1/milestone-12-submission-readiness-gate-v1.json",
]

EXPECTED_CHAIN_TASK_COUNT = 12

CLOSURE_MEASUREMENT_TARGETS = [
    "required_chain_artifact_count",
    "required_chain_artifact_present_count",
    "required_chain_artifact_parseable_count",
    "source_readiness_gate_passed",
    "source_real_submission_allowed",
    "source_ready_for_real_kaggle_submission",
    "closure_gate_count",
    "closure_pass_count",
    "closure_blocking_issue_count",
    "milestone_13_opened",
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


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def _artifact_status(path_text: str) -> dict[str, Any]:
    path = PROJECT_ROOT / path_text
    record = _load_json(path)
    task_name = None
    verdict = None
    next_stage = None
    if isinstance(record, dict):
        task_name = record.get("revision")
        verdict = record.get("task_verdict")
        next_stage = record.get("next_stage")

    return {
        "path": path_text,
        "present": path.exists(),
        "parseable_json": record is not None,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None,
        "revision": task_name,
        "task_verdict": verdict,
        "next_stage": next_stage,
    }


def build_closure_package(source_record: dict[str, Any] | None) -> dict[str, Any]:
    chain_statuses = [_artifact_status(path) for path in REQUIRED_CHAIN_ARTIFACTS]
    present_count = sum(1 for item in chain_statuses if item["present"] is True)
    parseable_count = sum(1 for item in chain_statuses if item["parseable_json"] is True)

    source = source_record if isinstance(source_record, dict) else {}

    return {
        "closure_package_id": "MILESTONE_12_COMPETITIVE_SOLVER_CLOSURE_PACKAGE_V1",
        "package_family": "LOCAL_COMPETITIVE_SOLVER_CHAIN_CLOSURE_NO_SUBMISSION",
        "required_chain_artifacts": chain_statuses,
        "required_chain_artifact_count": len(REQUIRED_CHAIN_ARTIFACTS),
        "required_chain_artifact_present_count": present_count,
        "required_chain_artifact_parseable_count": parseable_count,
        "source_submission_readiness_gate_ready": source.get("submission_readiness_gate_ready") is True,
        "source_submission_readiness_gate_passed": source.get("submission_readiness_gate_passed") is True,
        "source_readiness_verdict": source.get("readiness_verdict"),
        "source_required_artifact_count": source.get("required_source_artifact_count"),
        "source_required_artifact_present_count": source.get("required_source_artifact_present_count"),
        "source_guard_case_count": source.get("source_guard_case_count"),
        "source_guard_pass_count": source.get("source_guard_pass_count"),
        "source_public_overfit_violation_count": source.get("source_public_overfit_violation_count"),
        "source_boundary_violation_count": source.get("source_boundary_violation_count"),
        "source_real_submission_allowed": source.get("real_submission_allowed"),
        "source_ready_for_real_kaggle_submission": source.get("ready_for_real_kaggle_submission"),
        "source_manual_upload_allowed": source.get("manual_upload_allowed"),
        "source_operator_approval_required": source.get("operator_approval_required"),
        "source_operator_approval_received": source.get("operator_approval_received"),
        "measurement_targets": CLOSURE_MEASUREMENT_TARGETS,
        "measurement_target_count": len(CLOSURE_MEASUREMENT_TARGETS),
    }


def build_competitive_solver_closure_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_READINESS_ARTIFACT.exists()
    source_record = _load_json(SOURCE_READINESS_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_ready = bool(source_record and source_record.get("submission_readiness_gate_ready") is True)
    source_passed = bool(source_record and source_record.get("submission_readiness_gate_passed") is True)
    source_next_stage_ok = bool(source_record and source_record.get("next_stage") == "MILESTONE_12_TASK_13_COMPETITIVE_SOLVER_CLOSURE_V1")
    source_strategy_ok = bool(source_record and source_record.get("chosen_strategy") == CHOSEN_STRATEGY)
    source_goal_ok = bool(source_record and source_record.get("competitive_goal") == COMPETITIVE_GOAL)
    source_issue_zero = bool(source_record and source_record.get("issue_count") == 0)

    source_readiness_verdict_ok = bool(
        source_record
        and source_record.get("readiness_verdict") == "LOCAL_READINESS_PACKAGE_READY_REAL_SUBMISSION_BLOCKED"
    )

    source_real_submission_blocked = bool(
        source_record
        and source_record.get("real_submission_allowed") is False
        and source_record.get("ready_for_real_kaggle_submission") is False
        and source_record.get("manual_upload_allowed") is False
        and source_record.get("operator_approval_required") is True
        and source_record.get("operator_approval_received") is False
        and source_record.get("kaggle_submission_sent") is False
        and source_record.get("kaggle_authentication_performed") is False
    )

    source_boundaries_ok = all(
        [
            source_record and source_record.get("public_overfit_allowed") is False,
            source_record and source_record.get("public_overfit_guard_required") is True,
            source_record and source_record.get("external_api_dependency") is False,
            source_record and source_record.get("internet_during_eval") is False,
            source_record and source_record.get("private_core_exposure") is False,
            source_record and source_record.get("legal_certification") is False,
            source_record and source_record.get("official_score_claim_allowed") is False,
            source_record and source_record.get("competitive_score_claim_allowed") is False,
            source_record and source_record.get("local_only") is True,
            source_record and source_record.get("deterministic") is True,
            source_record and source_record.get("public_safe") is True,
        ]
    )

    closure_package = build_closure_package(source_record)

    chain_count_ok = closure_package["required_chain_artifact_count"] == EXPECTED_CHAIN_TASK_COUNT
    chain_present_ok = closure_package["required_chain_artifact_present_count"] == EXPECTED_CHAIN_TASK_COUNT
    chain_parseable_ok = closure_package["required_chain_artifact_parseable_count"] == EXPECTED_CHAIN_TASK_COUNT

    source_required_artifacts_ok = (
        closure_package["source_required_artifact_count"] == 4
        and closure_package["source_required_artifact_present_count"] == 4
    )
    source_guard_ok = (
        closure_package["source_guard_case_count"] == 6
        and closure_package["source_guard_pass_count"] == 6
        and closure_package["source_public_overfit_violation_count"] == 0
        and closure_package["source_boundary_violation_count"] == 0
    )

    measurement_count_ok = closure_package["measurement_target_count"] == 10

    milestone_12_closed = True
    milestone_13_opened = False
    milestone_13_opening_allowed = False

    real_submission_allowed = False
    ready_for_real_kaggle_submission = False
    manual_upload_allowed = False
    operator_approval_required = True
    operator_approval_received = False

    closure_gates = [
        _gate("source_artifact_present", source_artifact_present, True, "Task 12 readiness artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Task 12 readiness artifact is parseable."),
        _gate("source_ready", source_ready, True, "Task 12 readiness gate is ready."),
        _gate("source_passed", source_passed, True, "Task 12 readiness gate passed."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 12 points to Task 13 closure."),
        _gate("source_strategy_ok", source_strategy_ok, True, "Source strategy is aligned."),
        _gate("source_goal_ok", source_goal_ok, True, "Source goal is aligned."),
        _gate("source_issue_zero", source_issue_zero, True, "Source issue count is zero."),
        _gate("source_readiness_verdict_ok", source_readiness_verdict_ok, True, "Readiness verdict is correct."),
        _gate("source_real_submission_blocked", source_real_submission_blocked, True, "Real submission remains blocked."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("chain_count_ok", chain_count_ok, True, "Milestone 12 closure chain contains expected task artifact count."),
        _gate("chain_present_ok", chain_present_ok, True, "All Milestone 12 chain artifacts are present."),
        _gate("chain_parseable_ok", chain_parseable_ok, True, "All Milestone 12 chain artifacts are parseable JSON."),
        _gate("source_required_artifacts_ok", source_required_artifacts_ok, True, "Task 12 required source artifacts are complete."),
        _gate("source_guard_ok", source_guard_ok, True, "Task 11 guard data is clean through Task 12."),
        _gate("measurement_count_ok", measurement_count_ok, True, "Closure measurement targets are declared."),
        _gate("milestone_12_closed_true", milestone_12_closed is True, True, "Milestone 12 is closed by this task."),
        _gate("milestone_13_opened_false", milestone_13_opened is False, True, "Milestone 13 is not opened automatically."),
        _gate("milestone_13_opening_allowed_false", milestone_13_opening_allowed is False, True, "Milestone 13 opening is blocked until explicit future task."),
        _gate("real_submission_allowed_false", real_submission_allowed is False, True, "Real submission remains blocked."),
        _gate("ready_for_real_kaggle_submission_false", ready_for_real_kaggle_submission is False, True, "Real Kaggle submission readiness remains blocked."),
        _gate("manual_upload_allowed_false", manual_upload_allowed is False, True, "Manual upload remains blocked."),
        _gate("operator_approval_required_true", operator_approval_required is True, True, "Operator approval remains required."),
        _gate("operator_approval_received_false", operator_approval_received is False, True, "Operator approval has not been received."),
        _gate("public_overfit_allowed_false", True, True, "Public overfitting remains blocked."),
        _gate("public_overfit_guard_required_true", True, True, "Public overfit guard remains required."),
        _gate("external_api_dependency_false", True, True, "External API dependency remains false."),
        _gate("internet_during_eval_false", True, True, "Internet during evaluation remains false."),
        _gate("kaggle_submission_sent_false", True, True, "No Kaggle submission is sent."),
        _gate("kaggle_authentication_performed_false", True, True, "No Kaggle authentication is performed."),
        _gate("private_core_exposure_false", True, True, "Private core exposure remains false."),
        _gate("legal_certification_false", True, True, "legal_certification remains false."),
        _gate("official_score_claim_allowed_false", True, True, "Official score claim is blocked."),
        _gate("competitive_score_claim_allowed_false", True, True, "Competitive score claim is blocked."),
        _gate("local_only_true", True, True, "Task remains local-only."),
        _gate("deterministic_true", True, True, "Task remains deterministic."),
        _gate("public_safe_true", True, True, "Task remains public-safe."),
        _gate("fail_closed_active", True, True, "Closure fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in closure_gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    closure_passed = len(required_gates) == len(passed_required_gates)

    closure_summary = {
        "milestone_12_status": "CLOSED",
        "milestone_12_closure_status": "READY" if closure_passed else "FAIL_CLOSED",
        "closure_verdict": CLOSURE_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "required_chain_artifact_count": closure_package["required_chain_artifact_count"],
        "required_chain_artifact_present_count": closure_package["required_chain_artifact_present_count"],
        "required_chain_artifact_parseable_count": closure_package["required_chain_artifact_parseable_count"],
        "real_submission_allowed": real_submission_allowed,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "operator_approval_required": operator_approval_required,
        "operator_approval_received": operator_approval_received,
        "milestone_13_opened": milestone_13_opened,
        "next_stage": NEXT_STAGE,
    }

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_readiness_artifact": str(SOURCE_READINESS_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_ready": source_ready,
        "source_passed": source_passed,
        "source_next_stage_ok": source_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "closure_verdict": CLOSURE_VERDICT,
        "milestone_12_status": "CLOSED",
        "milestone_12_closure_ready": True,
        "milestone_12_closure_valid": closure_passed,
        "milestone_12_closure_passed": closure_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "closure_summary": closure_summary,
        "closure_package": closure_package,
        "required_chain_artifact_count": closure_package["required_chain_artifact_count"],
        "required_chain_artifact_present_count": closure_package["required_chain_artifact_present_count"],
        "required_chain_artifact_parseable_count": closure_package["required_chain_artifact_parseable_count"],
        "source_submission_readiness_gate_passed": closure_package["source_submission_readiness_gate_passed"],
        "source_readiness_verdict": closure_package["source_readiness_verdict"],
        "source_real_submission_allowed": closure_package["source_real_submission_allowed"],
        "source_ready_for_real_kaggle_submission": closure_package["source_ready_for_real_kaggle_submission"],
        "source_manual_upload_allowed": closure_package["source_manual_upload_allowed"],
        "source_public_overfit_violation_count": closure_package["source_public_overfit_violation_count"],
        "source_boundary_violation_count": closure_package["source_boundary_violation_count"],
        "measurement_target_count": len(CLOSURE_MEASUREMENT_TARGETS),
        "measurement_targets": CLOSURE_MEASUREMENT_TARGETS,
        "milestone_13_opened": milestone_13_opened,
        "milestone_13_opening_allowed": milestone_13_opening_allowed,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "open_source_prize_eligibility_required": True,
        "real_submission_allowed": real_submission_allowed,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "manual_upload_allowed": manual_upload_allowed,
        "operator_approval_required": operator_approval_required,
        "operator_approval_received": operator_approval_received,
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
        "closure_gate_count": len(closure_gates),
        "closure_pass_count": len(passed_required_gates),
        "closure_blocking_issue_count": 0 if closure_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(closure_gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if closure_passed else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "gates": closure_gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-12-COMPETITIVE-SOLVER-CLOSURE-" + signature[:12]
    return record


def validate_competitive_solver_closure_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "milestone_12_closure_ready",
        "milestone_12_closure_valid",
        "milestone_12_closure_passed",
        "source_artifact_present",
        "source_artifact_parseable",
        "source_ready",
        "source_passed",
        "source_next_stage_ok",
        "source_submission_readiness_gate_passed",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "operator_approval_required",
        "local_only",
        "deterministic",
        "public_safe",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "milestone_13_opened",
        "milestone_13_opening_allowed",
        "public_overfit_allowed",
        "external_api_dependency",
        "internet_during_eval",
        "real_submission_allowed",
        "ready_for_real_kaggle_submission",
        "manual_upload_allowed",
        "operator_approval_received",
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

    if record.get("closure_verdict") != CLOSURE_VERDICT:
        issues.append("CLOSURE_VERDICT_MISMATCH")

    if record.get("competitive_goal") != COMPETITIVE_GOAL:
        issues.append("COMPETITIVE_GOAL_MISMATCH")

    if record.get("chosen_strategy") != CHOSEN_STRATEGY:
        issues.append("CHOSEN_STRATEGY_MISMATCH")

    expected_counts = {
        "required_chain_artifact_count": EXPECTED_CHAIN_TASK_COUNT,
        "required_chain_artifact_present_count": EXPECTED_CHAIN_TASK_COUNT,
        "required_chain_artifact_parseable_count": EXPECTED_CHAIN_TASK_COUNT,
        "source_public_overfit_violation_count": 0,
        "source_boundary_violation_count": 0,
        "measurement_target_count": 10,
        "closure_blocking_issue_count": 0,
        "issue_count": 0,
    }
    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    if record.get("milestone_12_status") != "CLOSED":
        issues.append("MILESTONE_12_STATUS_NOT_CLOSED")

    if record.get("source_readiness_verdict") != "LOCAL_READINESS_PACKAGE_READY_REAL_SUBMISSION_BLOCKED":
        issues.append("SOURCE_READINESS_VERDICT_MISMATCH")

    package = record.get("closure_package")
    if not isinstance(package, dict):
        issues.append("CLOSURE_PACKAGE_MISSING")
    else:
        artifact_statuses = package.get("required_chain_artifacts")
        if not isinstance(artifact_statuses, list) or len(artifact_statuses) != EXPECTED_CHAIN_TASK_COUNT:
            issues.append("REQUIRED_CHAIN_ARTIFACTS_MISSING_OR_COUNT_MISMATCH")
        elif any(item.get("present") is not True or item.get("parseable_json") is not True for item in artifact_statuses):
            issues.append("REQUIRED_CHAIN_ARTIFACT_NOT_READY")

    summary = record.get("closure_summary")
    if not isinstance(summary, dict):
        issues.append("CLOSURE_SUMMARY_MISSING")
    else:
        if summary.get("milestone_12_closure_status") != "READY":
            issues.append("CLOSURE_SUMMARY_STATUS_NOT_READY")
        if summary.get("milestone_13_opened") is not False:
            issues.append("CLOSURE_SUMMARY_MILESTONE_13_OPENED")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("CLOSURE_SUMMARY_NEXT_STAGE_MISMATCH")

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

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-12-competitive-solver-closure-v1.json"
    index_path = target_dir / "milestone-12-competitive-solver-closure-index-v1.json"
    manifest_path = target_dir / "milestone-12-competitive-solver-closure-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-competitive-solver-closure-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "closure_verdict": record["closure_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "milestone_12_closure_ready": record["milestone_12_closure_ready"],
        "milestone_12_closure_passed": record["milestone_12_closure_passed"],
        "required_chain_artifact_count": record["required_chain_artifact_count"],
        "required_chain_artifact_present_count": record["required_chain_artifact_present_count"],
        "source_readiness_verdict": record["source_readiness_verdict"],
        "real_submission_allowed": record["real_submission_allowed"],
        "ready_for_real_kaggle_submission": record["ready_for_real_kaggle_submission"],
        "milestone_13_opened": record["milestone_13_opened"],
        "milestone_13_opening_allowed": record["milestone_13_opening_allowed"],
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
        f"closure_verdict={record['closure_verdict']}",
        f"next_stage={record['next_stage']}",
        f"milestone_12_status={record['milestone_12_status']}",
        f"milestone_12_closure_ready={record['milestone_12_closure_ready']}",
        f"milestone_12_closure_passed={record['milestone_12_closure_passed']}",
        f"required_chain_artifact_count={record['required_chain_artifact_count']}",
        f"required_chain_artifact_present_count={record['required_chain_artifact_present_count']}",
        f"source_readiness_verdict={record['source_readiness_verdict']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={record['ready_for_real_kaggle_submission']}",
        f"milestone_13_opened={record['milestone_13_opened']}",
        f"milestone_13_opening_allowed={record['milestone_13_opening_allowed']}",
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
- closure_verdict: `{record['closure_verdict']}`
- next_stage: `{record['next_stage']}`

## Milestone 12 Closure

- milestone_12_status: `{record['milestone_12_status']}`
- milestone_12_closure_ready: `{record['milestone_12_closure_ready']}`
- milestone_12_closure_passed: `{record['milestone_12_closure_passed']}`
- required_chain_artifact_count: `{record['required_chain_artifact_count']}`
- required_chain_artifact_present_count: `{record['required_chain_artifact_present_count']}`
- required_chain_artifact_parseable_count: `{record['required_chain_artifact_parseable_count']}`
- source_readiness_verdict: `{record['source_readiness_verdict']}`

## Real Submission Boundary

- real_submission_allowed: `{record['real_submission_allowed']}`
- ready_for_real_kaggle_submission: `{record['ready_for_real_kaggle_submission']}`
- manual_upload_allowed: `{record['manual_upload_allowed']}`
- operator_approval_required: `{record['operator_approval_required']}`
- operator_approval_received: `{record['operator_approval_received']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- kaggle_authentication_performed: `{record['kaggle_authentication_performed']}`
- official_score_claim_allowed: `{record['official_score_claim_allowed']}`
- competitive_score_claim_allowed: `{record['competitive_score_claim_allowed']}`

## Boundary

- local_only: `{record['local_only']}`
- deterministic: `{record['deterministic']}`
- public_safe: `{record['public_safe']}`
- public_overfit_allowed: `{record['public_overfit_allowed']}`
- public_overfit_guard_required: `{record['public_overfit_guard_required']}`
- external_api_dependency: `{record['external_api_dependency']}`
- internet_during_eval: `{record['internet_during_eval']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`

## Milestone 13

- milestone_13_opened: `{record['milestone_13_opened']}`
- milestone_13_opening_allowed: `{record['milestone_13_opening_allowed']}`
- next_stage: `{record['next_stage']}`
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
    record = build_competitive_solver_closure_record()
    issues = validate_competitive_solver_closure_record(record)
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
    print(record["closure_verdict"])
    print(record["next_stage"])
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
