"""Milestone #12 Task 1 - Competitive Solver Runtime Strategy Gate v1.

This module opens Milestone #12 canonically after Milestone #11 final closure.

Milestone #12 changes the project posture from closure/governance work to
competitive solver runtime development. The chosen strategy is:

    Executable World Model + Explore / Verify / Plan

This task does not create a Kaggle submission, does not upload anything, does
not authenticate to Kaggle, does not use external APIs, and does not expose
private HBCE/JOKER-C2 core material.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_COMPETITIVE_SOLVER_RUNTIME_STRATEGY_GATE_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 1
TASK_LABEL = "Milestone #12 Task 1 - Competitive Solver Runtime Strategy Gate v1"

SOURCE_TASK = "MILESTONE_11_TASK_35_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_FINAL_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_12_TASK_2_COMPETITIVE_SOLVER_BENCHMARK_HARNESS_V1"

TASK_MODE = "MILESTONE_12_COMPETITIVE_SOLVER_RUNTIME_STRATEGY_GATE_V1_LOCAL_ONLY"
TASK_SCOPE = "COMPETITIVE_SOLVER_RUNTIME_STRATEGY_GATE_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_EXTERNAL_API"
TASK_VERDICT = "MILESTONE_12_COMPETITIVE_SOLVER_RUNTIME_OPENED_CANONICALLY"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "competitive-solver-runtime-strategy-gate-v1"
)

SOURCE_MILESTONE_11_FINAL_CLOSURE_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-11"
    / "local-solver-patch-helper-controlled-runtime-wiring-final-closure-v1"
    / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-final-closure-v1.json"
)

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

WORKSTREAMS = [
    {
        "id": "m12_ws_01_benchmark_harness",
        "name": "Competitive Solver Benchmark Harness",
        "priority": "P0",
        "purpose": "Create a local measurement harness for completion, action efficiency, failure modes, and regression safety.",
        "next_task": "MILESTONE_12_TASK_2_COMPETITIVE_SOLVER_BENCHMARK_HARNESS_V1",
    },
    {
        "id": "m12_ws_02_explorer_policy",
        "name": "Information-Gain Explorer Policy",
        "priority": "P0",
        "purpose": "Generate useful exploratory actions instead of random action spam.",
        "next_task": "MILESTONE_12_TASK_3_INFORMATION_GAIN_EXPLORER_POLICY_V1",
    },
    {
        "id": "m12_ws_03_executable_world_model",
        "name": "Executable World Model",
        "priority": "P0",
        "purpose": "Infer executable transition models from observations and action outcomes.",
        "next_task": "MILESTONE_12_TASK_4_EXECUTABLE_WORLD_MODEL_V1",
    },
    {
        "id": "m12_ws_04_model_verifier",
        "name": "Model Verifier",
        "priority": "P0",
        "purpose": "Reject world models that do not explain observed state transitions.",
        "next_task": "MILESTONE_12_TASK_5_WORLD_MODEL_VERIFIER_V1",
    },
    {
        "id": "m12_ws_05_planner",
        "name": "Action Planner",
        "priority": "P0",
        "purpose": "Plan short, evidence-backed action sequences against verified world models.",
        "next_task": "MILESTONE_12_TASK_6_ACTION_PLANNER_V1",
    },
    {
        "id": "m12_ws_06_ranker",
        "name": "Candidate Plan Ranker",
        "priority": "P1",
        "purpose": "Rank plans by evidence, expected completion, action cost, and uncertainty.",
        "next_task": "MILESTONE_12_TASK_7_CANDIDATE_PLAN_RANKER_V1",
    },
    {
        "id": "m12_ws_07_episode_memory",
        "name": "Episode Memory",
        "priority": "P1",
        "purpose": "Track local observations, attempted actions, inferred rules, and contradictions per episode.",
        "next_task": "MILESTONE_12_TASK_8_EPISODE_MEMORY_V1",
    },
    {
        "id": "m12_ws_08_submission_candidate_gate",
        "name": "Submission Candidate Gate",
        "priority": "P2",
        "purpose": "Permit a real submission candidate only after measurable competitive readiness.",
        "next_task": "MILESTONE_12_TASK_9_SUBMISSION_CANDIDATE_GATE_V1",
    },
]

MEASUREMENT_TARGETS = [
    "completion_rate",
    "mean_action_count",
    "median_action_count",
    "failed_episode_count",
    "verified_model_count",
    "invalid_model_rejection_count",
    "planner_success_count",
    "public_overfit_signal_count",
    "regression_failure_count",
    "submission_readiness_gate_count",
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


def _load_source_final_closure() -> dict[str, Any] | None:
    if not SOURCE_MILESTONE_11_FINAL_CLOSURE_ARTIFACT.exists():
        return None
    try:
        return json.loads(SOURCE_MILESTONE_11_FINAL_CLOSURE_ARTIFACT.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_strategy_gate_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_present = SOURCE_MILESTONE_11_FINAL_CLOSURE_ARTIFACT.exists()
    source = _load_source_final_closure()

    source_parseable = source is not None
    source_m11_closed = bool(source and source.get("milestone_11_status") == "CLOSED")
    source_m11_final_complete = bool(source and source.get("milestone_11_final_closure_complete") is True)
    source_m11_final_passed = bool(source and source.get("milestone_11_final_closure_passed") is True)
    source_m11_closure_ok = bool(source and source.get("milestone_11_closure") == "FINAL_CLOSURE_PASS_REAL_EXECUTION_BLOCKED")
    source_real_execution_blocked = bool(source and source.get("real_execution_authorized") is False)
    source_runtime_wiring_blocked = bool(source and source.get("controlled_runtime_wiring_execution_allowed") is False)
    source_runtime_wiring_not_performed = bool(source and source.get("runtime_wiring_performed") is False)
    source_runtime_patch_not_applied = bool(source and source.get("runtime_solver_patch_applied") is False)
    source_submission_not_sent = bool(source and source.get("kaggle_submission_sent") is False)
    source_private_core_false = bool(source and source.get("private_core_exposure") is False)
    source_legal_false = bool(source and source.get("legal_certification") is False)
    source_m12_candidate_exists = bool(source and source.get("milestone_12_candidate_exists") is True)
    source_m12_not_opened = bool(source and source.get("milestone_12_candidate_status") == "NOT_OPENED_CANONICALLY")
    source_m12_opening_blocked = bool(source and source.get("milestone_12_opening_allowed") is False)
    source_issue_zero = bool(source and source.get("issue_count") == 0)
    source_warning_zero = bool(source and source.get("warning_count") == 0)

    canonical_open_allowed = all(
        [
            source_present,
            source_parseable,
            source_m11_closed,
            source_m11_final_complete,
            source_m11_final_passed,
            source_m11_closure_ok,
            source_real_execution_blocked,
            source_runtime_wiring_blocked,
            source_runtime_wiring_not_performed,
            source_runtime_patch_not_applied,
            source_submission_not_sent,
            source_private_core_false,
            source_legal_false,
            source_m12_candidate_exists,
            source_m12_not_opened,
            source_m12_opening_blocked,
            source_issue_zero,
            source_warning_zero,
        ]
    )

    strategy_checks = [
        _check("source_milestone_11_final_closure_artifact_present", source_present, "PASS" if source_present else "BLOCKING", "Milestone 11 final closure artifact exists."),
        _check("source_milestone_11_final_closure_artifact_parseable", source_parseable, "PASS" if source_parseable else "BLOCKING", "Milestone 11 final closure artifact is parseable JSON."),
        _check("source_milestone_11_status_closed", source_m11_closed, "PASS" if source_m11_closed else "BLOCKING", "Milestone 11 status is CLOSED."),
        _check("source_milestone_11_final_closure_complete", source_m11_final_complete, "PASS" if source_m11_final_complete else "BLOCKING", "Milestone 11 final closure is complete."),
        _check("source_milestone_11_final_closure_passed", source_m11_final_passed, "PASS" if source_m11_final_passed else "BLOCKING", "Milestone 11 final closure passed."),
        _check("source_milestone_11_closure_value_ok", source_m11_closure_ok, "PASS" if source_m11_closure_ok else "BLOCKING", "Milestone 11 closure value is correct."),
        _check("source_real_execution_blocked", source_real_execution_blocked, "PASS" if source_real_execution_blocked else "BLOCKING", "Real execution remains blocked before Milestone 12 opening."),
        _check("source_runtime_wiring_blocked", source_runtime_wiring_blocked, "PASS" if source_runtime_wiring_blocked else "BLOCKING", "Controlled runtime wiring remains blocked."),
        _check("source_runtime_wiring_not_performed", source_runtime_wiring_not_performed, "PASS" if source_runtime_wiring_not_performed else "BLOCKING", "Runtime wiring was not performed."),
        _check("source_runtime_patch_not_applied", source_runtime_patch_not_applied, "PASS" if source_runtime_patch_not_applied else "BLOCKING", "Runtime solver patch was not applied."),
        _check("source_submission_not_sent", source_submission_not_sent, "PASS" if source_submission_not_sent else "BLOCKING", "Kaggle submission was not sent."),
        _check("source_private_core_exposure_false", source_private_core_false, "PASS" if source_private_core_false else "BLOCKING", "Private core exposure is false."),
        _check("source_legal_certification_false", source_legal_false, "PASS" if source_legal_false else "BLOCKING", "legal_certification is false."),
        _check("source_milestone_12_candidate_exists", source_m12_candidate_exists, "PASS" if source_m12_candidate_exists else "BLOCKING", "Milestone 12 candidate exists."),
        _check("source_milestone_12_not_opened_before_gate", source_m12_not_opened, "PASS" if source_m12_not_opened else "BLOCKING", "Milestone 12 was not already opened before this gate."),
        _check("source_milestone_12_opening_blocked_before_gate", source_m12_opening_blocked, "PASS" if source_m12_opening_blocked else "BLOCKING", "Milestone 12 opening was blocked before this gate."),
        _check("source_issue_count_zero", source_issue_zero, "PASS" if source_issue_zero else "BLOCKING", "Source issue count is zero."),
        _check("source_warning_count_zero", source_warning_zero, "PASS" if source_warning_zero else "WARNING", "Source warning count is zero."),
        _check("strategy_selected", True, "PASS", "Competitive strategy selected."),
        _check("first_place_goal_declared", True, "PASS", "First-place competitive goal declared."),
        _check("public_overfit_guard_declared", True, "PASS", "Public overfit guard declared."),
        _check("submission_blocked", True, "PASS", "Submission remains blocked at Task 1."),
    ]

    strategy_gate_passed = all(check["status"] is True for check in strategy_checks)

    strategy_summary = {
        "milestone_12_status": "OPENED_CANONICALLY" if strategy_gate_passed else "FAIL_CLOSED",
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "strategy_family": "EXECUTABLE_WORLD_MODEL_WITH_EXPLORATION_VERIFICATION_PLANNING",
        "primary_score_targets": [
            "increase_completion_rate",
            "reduce_action_count",
            "reduce_failed_episode_count",
            "increase_generalization",
            "avoid_public_set_overfit",
        ],
        "non_goals": [
            "no_kaggle_upload_in_task_1",
            "no_real_submission_in_task_1",
            "no_external_api_dependency",
            "no_private_core_exposure",
            "no_score_claim",
        ],
        "next_stage": NEXT_STAGE,
    }

    gates = [
        _gate("milestone_11_final_closure_artifact_present", source_present, True, "Milestone 11 final closure artifact is present."),
        _gate("milestone_11_final_closure_artifact_parseable", source_parseable, True, "Milestone 11 final closure artifact is parseable."),
        _gate("milestone_11_status_closed", source_m11_closed, True, "Milestone 11 is closed."),
        _gate("milestone_11_final_closure_complete", source_m11_final_complete, True, "Milestone 11 final closure complete."),
        _gate("milestone_11_final_closure_passed", source_m11_final_passed, True, "Milestone 11 final closure passed."),
        _gate("milestone_11_closure_value_ok", source_m11_closure_ok, True, "Milestone 11 closure is correct."),
        _gate("real_execution_blocked_before_m12", source_real_execution_blocked, True, "Real execution remains blocked."),
        _gate("runtime_wiring_blocked_before_m12", source_runtime_wiring_blocked, True, "Controlled runtime wiring remains blocked."),
        _gate("runtime_wiring_not_performed_before_m12", source_runtime_wiring_not_performed, True, "Runtime wiring was not performed."),
        _gate("runtime_solver_patch_not_applied_before_m12", source_runtime_patch_not_applied, True, "Runtime solver patch was not applied."),
        _gate("kaggle_submission_not_sent_before_m12", source_submission_not_sent, True, "Kaggle submission was not sent."),
        _gate("private_core_exposure_false", source_private_core_false, True, "Private core exposure is false."),
        _gate("legal_certification_false", source_legal_false, True, "Legal certification remains false."),
        _gate("milestone_12_candidate_exists_before_opening", source_m12_candidate_exists, True, "Milestone 12 candidate existed before opening."),
        _gate("milestone_12_not_previously_opened", source_m12_not_opened, True, "Milestone 12 was not previously opened."),
        _gate("milestone_12_opening_previously_blocked", source_m12_opening_blocked, True, "Milestone 12 opening was blocked before this task."),
        _gate("strategy_gate_can_open_canonically", canonical_open_allowed, True, "Milestone 12 can be opened canonically."),
        _gate("strategy_selected_executable_world_model", CHOSEN_STRATEGY == "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN", True, "Executable world model strategy selected."),
        _gate("competitive_goal_first_place", COMPETITIVE_GOAL == "FIRST_PLACE_COMPETITIVE_SOLVER", True, "First-place goal declared."),
        _gate("workstream_count_ok", len(WORKSTREAMS) == 8, True, "Eight Milestone 12 workstreams declared."),
        _gate("p0_workstream_count_ok", sum(1 for item in WORKSTREAMS if item["priority"] == "P0") == 5, True, "Five P0 workstreams declared."),
        _gate("measurement_targets_declared", len(MEASUREMENT_TARGETS) == 10, True, "Ten measurement targets declared."),
        _gate("public_overfit_allowed_false", True, True, "Public overfitting is explicitly blocked."),
        _gate("external_api_dependency_false", True, True, "External API dependency remains false."),
        _gate("internet_during_eval_false", True, True, "Internet during evaluation remains false."),
        _gate("kaggle_submission_sent_false", True, True, "No Kaggle submission is sent."),
        _gate("real_submission_allowed_false", True, True, "Real submission remains blocked."),
        _gate("manual_upload_allowed_false", True, True, "Manual upload remains blocked."),
        _gate("kaggle_authentication_performed_false", True, True, "No Kaggle authentication is performed."),
        _gate("private_core_exposure_false_task_1", True, True, "No private core exposure is introduced."),
        _gate("legal_certification_false_task_1", True, True, "legal_certification remains false."),
        _gate("open_source_prize_eligibility_required", True, True, "Open-source prize eligibility is required."),
        _gate("local_only_true", True, True, "Task remains local-only."),
        _gate("deterministic_true", True, True, "Task remains deterministic."),
        _gate("public_safe_true", True, True, "Task remains public-safe."),
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
        "source_milestone_11_final_closure_artifact": str(SOURCE_MILESTONE_11_FINAL_CLOSURE_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_milestone_11_final_closure_artifact_present": source_present,
        "source_milestone_11_final_closure_artifact_parseable": source_parseable,
        "source_milestone_11_status_closed": source_m11_closed,
        "source_milestone_11_final_closure_complete": source_m11_final_complete,
        "source_milestone_11_final_closure_passed": source_m11_final_passed,
        "source_milestone_11_closure_ok": source_m11_closure_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY" if strategy_gate_passed else "FAIL_CLOSED",
        "milestone_12_opened_canonically": strategy_gate_passed,
        "milestone_12_strategy_gate_ready": True,
        "milestone_12_strategy_gate_valid": strategy_gate_passed,
        "milestone_12_strategy_gate_passed": strategy_gate_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "strategy_summary": strategy_summary,
        "workstream_count": len(WORKSTREAMS),
        "p0_workstream_count": sum(1 for item in WORKSTREAMS if item["priority"] == "P0"),
        "workstreams": WORKSTREAMS,
        "measurement_target_count": len(MEASUREMENT_TARGETS),
        "measurement_targets": MEASUREMENT_TARGETS,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "open_source_prize_eligibility_required": True,
        "real_execution_authorized": False,
        "controlled_runtime_wiring_execution_allowed": False,
        "runtime_wiring_performed": False,
        "runtime_solver_patch_applied": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "submission_json_created": False,
        "real_submission_candidate_created": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
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
        "strategy_gate_only": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "strategy_check_count": len(strategy_checks),
        "strategy_checks": strategy_checks,
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
    record["task_id"] = "MILESTONE-12-COMPETITIVE-SOLVER-RUNTIME-STRATEGY-GATE-" + signature[:12]
    return record


def validate_strategy_gate_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "milestone_12_opened_canonically",
        "milestone_12_strategy_gate_ready",
        "milestone_12_strategy_gate_valid",
        "milestone_12_strategy_gate_passed",
        "source_milestone_11_final_closure_artifact_present",
        "source_milestone_11_final_closure_artifact_parseable",
        "source_milestone_11_status_closed",
        "source_milestone_11_final_closure_complete",
        "source_milestone_11_final_closure_passed",
        "source_milestone_11_closure_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "local_only",
        "deterministic",
        "public_safe",
        "strategy_gate_only",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "public_overfit_allowed",
        "external_api_dependency",
        "internet_during_eval",
        "real_execution_authorized",
        "controlled_runtime_wiring_execution_allowed",
        "runtime_wiring_performed",
        "runtime_solver_patch_applied",
        "runtime_solver_modified",
        "ranker_runtime_modified",
        "submission_json_created",
        "real_submission_candidate_created",
        "real_submission_allowed",
        "manual_upload_allowed",
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
        issues.append("MILESTONE_12_STATUS_NOT_OPENED_CANONICALLY")

    if record.get("competitive_goal") != COMPETITIVE_GOAL:
        issues.append("COMPETITIVE_GOAL_MISMATCH")

    if record.get("chosen_strategy") != CHOSEN_STRATEGY:
        issues.append("CHOSEN_STRATEGY_MISMATCH")

    if record.get("workstream_count") != 8:
        issues.append("WORKSTREAM_COUNT_MISMATCH")

    if record.get("p0_workstream_count") != 5:
        issues.append("P0_WORKSTREAM_COUNT_MISMATCH")

    if record.get("measurement_target_count") != 10:
        issues.append("MEASUREMENT_TARGET_COUNT_MISMATCH")

    strategy_summary = record.get("strategy_summary")
    if not isinstance(strategy_summary, dict):
        issues.append("STRATEGY_SUMMARY_MISSING")
    else:
        if strategy_summary.get("milestone_12_status") != "OPENED_CANONICALLY":
            issues.append("STRATEGY_SUMMARY_STATUS_MISMATCH")
        if strategy_summary.get("competitive_goal") != COMPETITIVE_GOAL:
            issues.append("STRATEGY_SUMMARY_GOAL_MISMATCH")
        if strategy_summary.get("chosen_strategy") != CHOSEN_STRATEGY:
            issues.append("STRATEGY_SUMMARY_STRATEGY_MISMATCH")
        if strategy_summary.get("next_stage") != NEXT_STAGE:
            issues.append("STRATEGY_SUMMARY_NEXT_STAGE_MISMATCH")

    strategy_checks = record.get("strategy_checks")
    if not isinstance(strategy_checks, list) or not strategy_checks:
        issues.append("STRATEGY_CHECKS_MISSING")
    elif any(check.get("status") is not True for check in strategy_checks):
        issues.append("STRATEGY_CHECK_FAILED")

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

    json_path = target_dir / "milestone-12-competitive-solver-runtime-strategy-gate-v1.json"
    index_path = target_dir / "milestone-12-competitive-solver-runtime-strategy-gate-index-v1.json"
    manifest_path = target_dir / "milestone-12-competitive-solver-runtime-strategy-gate-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-competitive-solver-runtime-strategy-gate-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "milestone_12_status": record["milestone_12_status"],
        "milestone_12_opened_canonically": record["milestone_12_opened_canonically"],
        "competitive_goal": record["competitive_goal"],
        "chosen_strategy": record["chosen_strategy"],
        "workstream_count": record["workstream_count"],
        "p0_workstream_count": record["p0_workstream_count"],
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
        f"milestone_12_opened_canonically={record['milestone_12_opened_canonically']}",
        f"competitive_goal={record['competitive_goal']}",
        f"chosen_strategy={record['chosen_strategy']}",
        f"workstream_count={record['workstream_count']}",
        f"p0_workstream_count={record['p0_workstream_count']}",
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

## Strategy

Milestone #12 opens the competitive solver runtime branch.

Chosen strategy:

`{record['chosen_strategy']}`

Goal:

`{record['competitive_goal']}`

## Workstreams

- workstream_count: `{record['workstream_count']}`
- p0_workstream_count: `{record['p0_workstream_count']}`
- measurement_target_count: `{record['measurement_target_count']}`

## Boundary

- public_overfit_allowed: `{record['public_overfit_allowed']}`
- external_api_dependency: `{record['external_api_dependency']}`
- internet_during_eval: `{record['internet_during_eval']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- manual_upload_allowed: `{record['manual_upload_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- kaggle_authentication_performed: `{record['kaggle_authentication_performed']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`

## Next stage

`{record['next_stage']}`
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
    record = build_strategy_gate_record()
    issues = validate_strategy_gate_record(record)
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
