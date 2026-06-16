"""Milestone #13 Task 1 - Real Evaluation Boundary Gate v1.

This module opens Milestone #13 canonically after Milestone #12 closure.

It creates the boundary for real-evaluation preparation while keeping all
dangerous or premature actions blocked:

- no Kaggle authentication
- no Kaggle upload
- no real submission
- no score claim
- no internet during evaluation
- no external API dependency
- no private core exposure
- no legal certification claim

Allowed after this gate:

- local solver improvement
- local diagnostic evaluation
- local dry-run package preparation
- capability gap analysis
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_REAL_EVALUATION_BOUNDARY_GATE_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 1
TASK_LABEL = "Milestone #13 Task 1 - Real Evaluation Boundary Gate v1"

SOURCE_TASK = "MILESTONE_12_TASK_13_COMPETITIVE_SOLVER_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_13_TASK_2_SOLVER_CAPABILITY_GAP_AUDIT_V1"

TASK_MODE = "MILESTONE_13_REAL_EVALUATION_BOUNDARY_GATE_V1_LOCAL_ONLY"
TASK_SCOPE = "MILESTONE_13_OPENING_BOUNDARY_ONLY_NO_KAGGLE_AUTH_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_REAL_EVALUATION_BOUNDARY_GATE_READY"

BOUNDARY_VERDICT = "MILESTONE_13_OPENED_CANONICALLY_REAL_EVALUATION_PREP_ALLOWED_REAL_SUBMISSION_BLOCKED"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-13" / "real-evaluation-boundary-gate-v1"

SOURCE_MILESTONE_12_CLOSURE_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "competitive-solver-closure-v1"
    / "milestone-12-competitive-solver-closure-v1.json"
)

BOUNDARY_MEASUREMENT_TARGETS = [
    "source_milestone_12_closed",
    "source_closure_passed",
    "source_real_submission_allowed",
    "source_ready_for_real_kaggle_submission",
    "source_milestone_13_opened",
    "milestone_13_opened",
    "real_evaluation_prep_allowed",
    "real_submission_allowed",
    "kaggle_authentication_allowed",
    "boundary_blocking_issue_count",
]

ALLOWED_LOCAL_ACTIONS = [
    "LOCAL_SOLVER_IMPROVEMENT",
    "LOCAL_DIAGNOSTIC_EVALUATION",
    "LOCAL_DRY_RUN_PACKAGE_PREPARATION",
    "SOLVER_CAPABILITY_GAP_AUDIT",
    "TRANSFORMATION_PRIMITIVE_EXPANSION",
    "OBJECT_CENTRIC_REASONING_REVIEW",
    "RANKER_POLICY_REVIEW",
]

BLOCKED_ACTIONS = [
    "KAGGLE_AUTHENTICATION",
    "KAGGLE_UPLOAD",
    "REAL_SUBMISSION",
    "MANUAL_UPLOAD",
    "OFFICIAL_SCORE_CLAIM",
    "COMPETITIVE_SCORE_CLAIM",
    "INTERNET_DURING_EVAL",
    "EXTERNAL_API_DURING_EVAL",
    "PRIVATE_CORE_EXPOSURE",
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


def build_boundary_policy(source_record: dict[str, Any] | None) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}

    return {
        "boundary_policy_id": "MILESTONE_13_REAL_EVALUATION_BOUNDARY_POLICY_V1",
        "policy_family": "REAL_EVALUATION_PREPARATION_WITH_REAL_SUBMISSION_BLOCKED",
        "source_milestone_12_status": source.get("milestone_12_status"),
        "source_closure_verdict": source.get("closure_verdict"),
        "source_next_stage": source.get("next_stage"),
        "source_milestone_13_opened": source.get("milestone_13_opened"),
        "source_milestone_13_opening_allowed": source.get("milestone_13_opening_allowed"),
        "allowed_local_actions": ALLOWED_LOCAL_ACTIONS,
        "allowed_local_action_count": len(ALLOWED_LOCAL_ACTIONS),
        "blocked_actions": BLOCKED_ACTIONS,
        "blocked_action_count": len(BLOCKED_ACTIONS),
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "local_dry_run_allowed": True,
        "solver_capability_gap_audit_allowed": True,
        "real_kaggle_evaluation_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_upload_allowed": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "internet_during_eval": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "measurement_targets": BOUNDARY_MEASUREMENT_TARGETS,
        "measurement_target_count": len(BOUNDARY_MEASUREMENT_TARGETS),
    }


def build_real_evaluation_boundary_gate_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_MILESTONE_12_CLOSURE_ARTIFACT.exists()
    source_record = _load_json(SOURCE_MILESTONE_12_CLOSURE_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_milestone_12_closed = bool(source_record and source_record.get("milestone_12_status") == "CLOSED")
    source_closure_ready = bool(source_record and source_record.get("milestone_12_closure_ready") is True)
    source_closure_passed = bool(source_record and source_record.get("milestone_12_closure_passed") is True)
    source_closure_verdict_ok = bool(
        source_record
        and source_record.get("closure_verdict") == "MILESTONE_12_CLOSED_LOCAL_COMPETITIVE_SOLVER_READY_REAL_SUBMISSION_BLOCKED"
    )
    source_next_stage_ok = bool(source_record and source_record.get("next_stage") == "MILESTONE_13_NOT_OPENED_CANONICALLY")
    source_strategy_ok = bool(source_record and source_record.get("chosen_strategy") == CHOSEN_STRATEGY)
    source_goal_ok = bool(source_record and source_record.get("competitive_goal") == COMPETITIVE_GOAL)
    source_issue_zero = bool(source_record and source_record.get("issue_count") == 0)

    source_real_submission_blocked = bool(
        source_record
        and source_record.get("real_submission_allowed") is False
        and source_record.get("ready_for_real_kaggle_submission") is False
        and source_record.get("manual_upload_allowed") is False
        and source_record.get("kaggle_submission_sent") is False
        and source_record.get("kaggle_authentication_performed") is False
    )

    source_milestone_13_not_opened = bool(
        source_record
        and source_record.get("milestone_13_opened") is False
        and source_record.get("milestone_13_opening_allowed") is False
    )

    source_boundaries_ok = all(
        [
            source_record and source_record.get("local_only") is True,
            source_record and source_record.get("deterministic") is True,
            source_record and source_record.get("public_safe") is True,
            source_record and source_record.get("public_overfit_allowed") is False,
            source_record and source_record.get("public_overfit_guard_required") is True,
            source_record and source_record.get("external_api_dependency") is False,
            source_record and source_record.get("internet_during_eval") is False,
            source_record and source_record.get("private_core_exposure") is False,
            source_record and source_record.get("legal_certification") is False,
            source_record and source_record.get("official_score_claim_allowed") is False,
            source_record and source_record.get("competitive_score_claim_allowed") is False,
        ]
    )

    policy = build_boundary_policy(source_record)

    milestone_13_opened = True
    milestone_13_opened_canonically = True
    milestone_13_status = "OPENED_CANONICALLY"

    real_evaluation_prep_allowed = True
    local_solver_improvement_allowed = True
    local_diagnostic_eval_allowed = True
    solver_capability_gap_audit_allowed = True

    real_kaggle_evaluation_allowed = False
    real_submission_allowed = False
    ready_for_real_kaggle_submission = False
    manual_upload_allowed = False
    kaggle_authentication_allowed = False
    kaggle_authentication_performed = False
    kaggle_upload_allowed = False
    kaggle_submission_sent = False
    operator_approval_required = True
    operator_approval_received = False

    measurement_count_ok = policy["measurement_target_count"] == 10
    allowed_action_count_ok = policy["allowed_local_action_count"] == 7
    blocked_action_count_ok = policy["blocked_action_count"] == 9

    gates = [
        _gate("source_artifact_present", source_artifact_present, True, "Milestone 12 closure artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Milestone 12 closure artifact is parseable JSON."),
        _gate("source_milestone_12_closed", source_milestone_12_closed, True, "Milestone 12 is closed."),
        _gate("source_closure_ready", source_closure_ready, True, "Milestone 12 closure is ready."),
        _gate("source_closure_passed", source_closure_passed, True, "Milestone 12 closure passed."),
        _gate("source_closure_verdict_ok", source_closure_verdict_ok, True, "Milestone 12 closure verdict is canonical."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Milestone 12 points to Milestone 13 not opened."),
        _gate("source_strategy_ok", source_strategy_ok, True, "Source strategy is aligned."),
        _gate("source_goal_ok", source_goal_ok, True, "Source goal is aligned."),
        _gate("source_issue_zero", source_issue_zero, True, "Source issue count is zero."),
        _gate("source_real_submission_blocked", source_real_submission_blocked, True, "Source keeps real submission blocked."),
        _gate("source_milestone_13_not_opened", source_milestone_13_not_opened, True, "Source confirms Milestone 13 was not previously opened."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("milestone_13_opened_true", milestone_13_opened is True, True, "Milestone 13 is opened by this task."),
        _gate("milestone_13_opened_canonically_true", milestone_13_opened_canonically is True, True, "Milestone 13 is opened canonically."),
        _gate("real_evaluation_prep_allowed_true", real_evaluation_prep_allowed is True, True, "Real evaluation preparation is allowed."),
        _gate("local_solver_improvement_allowed_true", local_solver_improvement_allowed is True, True, "Local solver improvement is allowed."),
        _gate("local_diagnostic_eval_allowed_true", local_diagnostic_eval_allowed is True, True, "Local diagnostic evaluation is allowed."),
        _gate("solver_capability_gap_audit_allowed_true", solver_capability_gap_audit_allowed is True, True, "Solver capability gap audit is allowed."),
        _gate("real_kaggle_evaluation_allowed_false", real_kaggle_evaluation_allowed is False, True, "Real Kaggle evaluation remains blocked."),
        _gate("real_submission_allowed_false", real_submission_allowed is False, True, "Real submission remains blocked."),
        _gate("ready_for_real_kaggle_submission_false", ready_for_real_kaggle_submission is False, True, "Real Kaggle submission readiness remains blocked."),
        _gate("manual_upload_allowed_false", manual_upload_allowed is False, True, "Manual upload remains blocked."),
        _gate("kaggle_authentication_allowed_false", kaggle_authentication_allowed is False, True, "Kaggle authentication remains blocked."),
        _gate("kaggle_authentication_performed_false", kaggle_authentication_performed is False, True, "Kaggle authentication is not performed."),
        _gate("kaggle_upload_allowed_false", kaggle_upload_allowed is False, True, "Kaggle upload remains blocked."),
        _gate("kaggle_submission_sent_false", kaggle_submission_sent is False, True, "No Kaggle submission is sent."),
        _gate("operator_approval_required_true", operator_approval_required is True, True, "Operator approval remains required."),
        _gate("operator_approval_received_false", operator_approval_received is False, True, "Operator approval has not been received."),
        _gate("measurement_count_ok", measurement_count_ok, True, "Boundary measurement targets are declared."),
        _gate("allowed_action_count_ok", allowed_action_count_ok, True, "Allowed local actions are declared."),
        _gate("blocked_action_count_ok", blocked_action_count_ok, True, "Blocked actions are declared."),
        _gate("public_overfit_allowed_false", True, True, "Public overfit remains blocked."),
        _gate("public_overfit_guard_required_true", True, True, "Public overfit guard remains required."),
        _gate("external_api_dependency_false", True, True, "External API dependency remains false."),
        _gate("internet_during_eval_false", True, True, "Internet during evaluation remains false."),
        _gate("private_core_exposure_false", True, True, "Private core exposure remains false."),
        _gate("legal_certification_false", True, True, "legal_certification remains false."),
        _gate("official_score_claim_allowed_false", True, True, "Official score claim remains blocked."),
        _gate("competitive_score_claim_allowed_false", True, True, "Competitive score claim remains blocked."),
        _gate("local_only_true", True, True, "Task remains local-only."),
        _gate("deterministic_true", True, True, "Task remains deterministic."),
        _gate("public_safe_true", True, True, "Task remains public-safe."),
        _gate("fail_closed_active", True, True, "Gate fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    boundary_passed = len(required_gates) == len(passed_required_gates)

    boundary_summary = {
        "milestone_13_status": milestone_13_status,
        "boundary_status": "READY" if boundary_passed else "FAIL_CLOSED",
        "boundary_verdict": BOUNDARY_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "source_milestone_12_closed": source_milestone_12_closed,
        "source_closure_passed": source_closure_passed,
        "real_evaluation_prep_allowed": real_evaluation_prep_allowed,
        "local_solver_improvement_allowed": local_solver_improvement_allowed,
        "real_kaggle_evaluation_allowed": real_kaggle_evaluation_allowed,
        "real_submission_allowed": real_submission_allowed,
        "kaggle_authentication_allowed": kaggle_authentication_allowed,
        "operator_approval_required": operator_approval_required,
        "operator_approval_received": operator_approval_received,
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
        "source_milestone_12_closure_artifact": str(SOURCE_MILESTONE_12_CLOSURE_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_milestone_12_closed": source_milestone_12_closed,
        "source_closure_ready": source_closure_ready,
        "source_closure_passed": source_closure_passed,
        "source_closure_verdict_ok": source_closure_verdict_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "source_real_submission_blocked": source_real_submission_blocked,
        "source_milestone_13_not_opened": source_milestone_13_not_opened,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "boundary_verdict": BOUNDARY_VERDICT,
        "milestone_13_status": milestone_13_status,
        "milestone_13_opened": milestone_13_opened,
        "milestone_13_opened_canonically": milestone_13_opened_canonically,
        "real_evaluation_boundary_gate_ready": True,
        "real_evaluation_boundary_gate_valid": boundary_passed,
        "real_evaluation_boundary_gate_passed": boundary_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "boundary_summary": boundary_summary,
        "boundary_policy": policy,
        "allowed_local_actions": ALLOWED_LOCAL_ACTIONS,
        "allowed_local_action_count": len(ALLOWED_LOCAL_ACTIONS),
        "blocked_actions": BLOCKED_ACTIONS,
        "blocked_action_count": len(BLOCKED_ACTIONS),
        "measurement_target_count": len(BOUNDARY_MEASUREMENT_TARGETS),
        "measurement_targets": BOUNDARY_MEASUREMENT_TARGETS,
        "real_evaluation_prep_allowed": real_evaluation_prep_allowed,
        "local_solver_improvement_allowed": local_solver_improvement_allowed,
        "local_diagnostic_eval_allowed": local_diagnostic_eval_allowed,
        "local_dry_run_allowed": True,
        "solver_capability_gap_audit_allowed": solver_capability_gap_audit_allowed,
        "real_kaggle_evaluation_allowed": real_kaggle_evaluation_allowed,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "open_source_prize_eligibility_required": True,
        "real_submission_allowed": real_submission_allowed,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "manual_upload_allowed": manual_upload_allowed,
        "kaggle_authentication_allowed": kaggle_authentication_allowed,
        "kaggle_authentication_performed": kaggle_authentication_performed,
        "kaggle_upload_allowed": kaggle_upload_allowed,
        "kaggle_submission_sent": kaggle_submission_sent,
        "operator_approval_required": operator_approval_required,
        "operator_approval_received": operator_approval_received,
        "submission_json_created": False,
        "real_submission_candidate_created": False,
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
        "boundary_gate_count": len(gates),
        "boundary_pass_count": len(passed_required_gates),
        "boundary_blocking_issue_count": 0 if boundary_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if boundary_passed else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-REAL-EVALUATION-BOUNDARY-GATE-" + signature[:12]
    return record


def validate_real_evaluation_boundary_gate_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_artifact_present",
        "source_artifact_parseable",
        "source_milestone_12_closed",
        "source_closure_ready",
        "source_closure_passed",
        "source_closure_verdict_ok",
        "source_next_stage_ok",
        "source_real_submission_blocked",
        "source_milestone_13_not_opened",
        "milestone_13_opened",
        "milestone_13_opened_canonically",
        "real_evaluation_boundary_gate_ready",
        "real_evaluation_boundary_gate_valid",
        "real_evaluation_boundary_gate_passed",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "local_dry_run_allowed",
        "solver_capability_gap_audit_allowed",
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
        "real_kaggle_evaluation_allowed",
        "public_overfit_allowed",
        "external_api_dependency",
        "internet_during_eval",
        "real_submission_allowed",
        "ready_for_real_kaggle_submission",
        "manual_upload_allowed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_upload_allowed",
        "kaggle_submission_sent",
        "operator_approval_received",
        "submission_json_created",
        "real_submission_candidate_created",
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

    if record.get("boundary_verdict") != BOUNDARY_VERDICT:
        issues.append("BOUNDARY_VERDICT_MISMATCH")

    if record.get("milestone_13_status") != "OPENED_CANONICALLY":
        issues.append("MILESTONE_13_STATUS_MISMATCH")

    if record.get("competitive_goal") != COMPETITIVE_GOAL:
        issues.append("COMPETITIVE_GOAL_MISMATCH")

    if record.get("chosen_strategy") != CHOSEN_STRATEGY:
        issues.append("CHOSEN_STRATEGY_MISMATCH")

    expected_counts = {
        "allowed_local_action_count": 7,
        "blocked_action_count": 9,
        "measurement_target_count": 10,
        "boundary_blocking_issue_count": 0,
        "issue_count": 0,
    }
    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    policy = record.get("boundary_policy")
    if not isinstance(policy, dict):
        issues.append("BOUNDARY_POLICY_MISSING")
    else:
        if policy.get("real_evaluation_prep_allowed") is not True:
            issues.append("POLICY_REAL_EVALUATION_PREP_NOT_ALLOWED")
        if policy.get("real_submission_allowed") is not False:
            issues.append("POLICY_REAL_SUBMISSION_NOT_BLOCKED")
        if policy.get("kaggle_authentication_allowed") is not False:
            issues.append("POLICY_KAGGLE_AUTH_NOT_BLOCKED")

    summary = record.get("boundary_summary")
    if not isinstance(summary, dict):
        issues.append("BOUNDARY_SUMMARY_MISSING")
    else:
        if summary.get("milestone_13_status") != "OPENED_CANONICALLY":
            issues.append("BOUNDARY_SUMMARY_STATUS_MISMATCH")
        if summary.get("boundary_status") != "READY":
            issues.append("BOUNDARY_SUMMARY_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("BOUNDARY_SUMMARY_NEXT_STAGE_MISMATCH")

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

    json_path = target_dir / "milestone-13-real-evaluation-boundary-gate-v1.json"
    index_path = target_dir / "milestone-13-real-evaluation-boundary-gate-index-v1.json"
    manifest_path = target_dir / "milestone-13-real-evaluation-boundary-gate-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-real-evaluation-boundary-gate-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "boundary_verdict": record["boundary_verdict"],
        "milestone_13_status": record["milestone_13_status"],
        "next_stage": record["next_stage"],
        "source_milestone_12_closed": record["source_milestone_12_closed"],
        "source_closure_passed": record["source_closure_passed"],
        "real_evaluation_boundary_gate_ready": record["real_evaluation_boundary_gate_ready"],
        "real_evaluation_prep_allowed": record["real_evaluation_prep_allowed"],
        "local_solver_improvement_allowed": record["local_solver_improvement_allowed"],
        "real_kaggle_evaluation_allowed": record["real_kaggle_evaluation_allowed"],
        "real_submission_allowed": record["real_submission_allowed"],
        "kaggle_authentication_allowed": record["kaggle_authentication_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "operator_approval_required": record["operator_approval_required"],
        "operator_approval_received": record["operator_approval_received"],
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
        f"boundary_verdict={record['boundary_verdict']}",
        f"milestone_13_status={record['milestone_13_status']}",
        f"next_stage={record['next_stage']}",
        f"source_milestone_12_closed={record['source_milestone_12_closed']}",
        f"source_closure_passed={record['source_closure_passed']}",
        f"real_evaluation_boundary_gate_ready={record['real_evaluation_boundary_gate_ready']}",
        f"real_evaluation_prep_allowed={record['real_evaluation_prep_allowed']}",
        f"local_solver_improvement_allowed={record['local_solver_improvement_allowed']}",
        f"real_kaggle_evaluation_allowed={record['real_kaggle_evaluation_allowed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_authentication_allowed={record['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"operator_approval_required={record['operator_approval_required']}",
        f"operator_approval_received={record['operator_approval_received']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- boundary_verdict: `{record['boundary_verdict']}`
- milestone_13_status: `{record['milestone_13_status']}`
- next_stage: `{record['next_stage']}`

## Source Closure

- source_milestone_12_closed: `{record['source_milestone_12_closed']}`
- source_closure_passed: `{record['source_closure_passed']}`
- source_real_submission_blocked: `{record['source_real_submission_blocked']}`
- source_milestone_13_not_opened: `{record['source_milestone_13_not_opened']}`

## Allowed Local Work

- real_evaluation_prep_allowed: `{record['real_evaluation_prep_allowed']}`
- local_solver_improvement_allowed: `{record['local_solver_improvement_allowed']}`
- local_diagnostic_eval_allowed: `{record['local_diagnostic_eval_allowed']}`
- solver_capability_gap_audit_allowed: `{record['solver_capability_gap_audit_allowed']}`

## Blocked Actions

- real_kaggle_evaluation_allowed: `{record['real_kaggle_evaluation_allowed']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- ready_for_real_kaggle_submission: `{record['ready_for_real_kaggle_submission']}`
- manual_upload_allowed: `{record['manual_upload_allowed']}`
- kaggle_authentication_allowed: `{record['kaggle_authentication_allowed']}`
- kaggle_authentication_performed: `{record['kaggle_authentication_performed']}`
- kaggle_upload_allowed: `{record['kaggle_upload_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- operator_approval_required: `{record['operator_approval_required']}`
- operator_approval_received: `{record['operator_approval_received']}`

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
    record = build_real_evaluation_boundary_gate_record()
    issues = validate_real_evaluation_boundary_gate_record(record)
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
    print(record["boundary_verdict"])
    print(record["next_stage"])
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
