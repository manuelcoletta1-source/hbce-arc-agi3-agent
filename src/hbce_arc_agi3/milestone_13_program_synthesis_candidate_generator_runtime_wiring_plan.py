"""Milestone #13 Task 10 - Program Synthesis Candidate Generator Runtime Wiring Plan v1.

This task creates a controlled wiring plan only.

It does not wire the runtime solver.
It does not modify candidate generator runtime behavior.
It does not run real Kaggle evaluation.
It does not authenticate, upload, or submit.

Humanity survives another JSON document.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 10
TASK_LABEL = "Milestone #13 Task 10 - Program Synthesis Candidate Generator Runtime Wiring Plan v1"

SOURCE_TASK = "MILESTONE_13_TASK_9_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REVIEW_V1"
NEXT_STAGE = "MILESTONE_13_TASK_11_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_REVIEW_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_V1_LOCAL_ONLY"
TASK_SCOPE = "RUNTIME_WIRING_PLAN_ONLY_NO_RUNTIME_WIRING_NO_REAL_EVAL_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_READY"
PLAN_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_READY_FOR_REVIEW"

COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"
CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-runtime-wiring-plan-v1"
)

SOURCE_REVIEW_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-local-diagnostic-harness-review-v1"
    / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-v1.json"
)

WIRING_TARGETS = [
    {
        "target_id": "WIRING-TARGET-01",
        "name": "candidate_generation_entrypoint_adapter",
        "planned_module": "src/hbce_arc_agi3/program_synthesis_candidate_generator_runtime_adapter.py",
        "purpose": "Expose reviewed candidate generator output behind a local deterministic adapter.",
        "runtime_modification_now": False,
        "requires_review_before_implementation": True,
    },
    {
        "target_id": "WIRING-TARGET-02",
        "name": "local_candidate_generation_call_site",
        "planned_module": "src/hbce_arc_agi3/solver_runtime_candidate_generation_hook.py",
        "purpose": "Define a future local-only call site for candidate generation inside solver exploration.",
        "runtime_modification_now": False,
        "requires_review_before_implementation": True,
    },
    {
        "target_id": "WIRING-TARGET-03",
        "name": "candidate_fixture_matrix_bridge",
        "planned_module": "src/hbce_arc_agi3/program_synthesis_candidate_fixture_bridge.py",
        "purpose": "Map candidate generator results into diagnostic harness compatible records.",
        "runtime_modification_now": False,
        "requires_review_before_implementation": True,
    },
    {
        "target_id": "WIRING-TARGET-04",
        "name": "ranker_input_contract_extension",
        "planned_module": "src/hbce_arc_agi3/candidate_ranker.py",
        "purpose": "Plan future ranker input contract extension without changing runtime ranking now.",
        "runtime_modification_now": False,
        "requires_review_before_implementation": True,
    },
]

WIRING_STEPS = [
    {
        "step_id": "WIRING-PLAN-STEP-01",
        "name": "freeze_reviewed_harness_contract",
        "description": "Use Task 9 review artifact as the frozen prerequisite for wiring design.",
        "implementation_allowed_now": False,
    },
    {
        "step_id": "WIRING-PLAN-STEP-02",
        "name": "define_adapter_interface",
        "description": "Define deterministic local adapter interface for generated candidates.",
        "implementation_allowed_now": False,
    },
    {
        "step_id": "WIRING-PLAN-STEP-03",
        "name": "define_solver_call_site_boundary",
        "description": "Define future solver call site without modifying solver runtime.",
        "implementation_allowed_now": False,
    },
    {
        "step_id": "WIRING-PLAN-STEP-04",
        "name": "define_ranker_contract_extension",
        "description": "Define future ranker extension contract without changing ranker runtime.",
        "implementation_allowed_now": False,
    },
    {
        "step_id": "WIRING-PLAN-STEP-05",
        "name": "define_diagnostic_only_acceptance_gate",
        "description": "Require local diagnostic harness pass before any controlled implementation.",
        "implementation_allowed_now": False,
    },
    {
        "step_id": "WIRING-PLAN-STEP-06",
        "name": "defer_runtime_wiring_to_reviewed_task",
        "description": "Defer actual wiring until plan review authorizes a controlled implementation task.",
        "implementation_allowed_now": False,
    },
]

ACCEPTANCE_GATES = [
    "source_review_artifact_present",
    "source_review_artifact_parseable",
    "source_review_passed",
    "source_runtime_wiring_plan_authorized",
    "source_runtime_wiring_not_performed",
    "source_candidate_generator_wiring_not_performed",
    "source_real_eval_not_performed",
    "wiring_targets_defined",
    "wiring_steps_defined",
    "no_target_runtime_modification_now",
    "no_step_implementation_allowed_now",
    "runtime_wiring_plan_created",
    "runtime_wiring_plan_review_required",
    "controlled_implementation_deferred",
    "real_submission_blocked",
]

RISK_CONTROLS = [
    "NO_REAL_KAGGLE_EVALUATION",
    "NO_RUNTIME_SOLVER_WIRING_IN_THIS_TASK",
    "NO_CANDIDATE_GENERATOR_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_RANKER_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_PUBLIC_SET_MEMORIZATION",
    "NO_EXTERNAL_API_DEPENDENCY",
    "NO_INTERNET_DURING_EVAL",
    "NO_KAGGLE_AUTHENTICATION",
    "NO_UPLOAD",
    "NO_SUBMISSION",
    "PLAN_ONLY_NO_CODEPATH_ACTIVATION",
]

QUALITY_TARGETS = [
    "runtime_wiring_plan_is_deterministic",
    "source_review_artifact_is_verified",
    "wiring_targets_are_explicit",
    "wiring_steps_are_explicit",
    "implementation_is_deferred",
    "runtime_wiring_remains_blocked",
    "next_task_is_plan_review",
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


def build_wiring_plan(source_record: dict[str, Any] | None) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}

    return {
        "wiring_plan_id": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_SPEC_V1",
        "plan_mode": "PLAN_ONLY",
        "source_revision": source.get("revision"),
        "source_review_verdict": source.get("review_verdict"),
        "source_runtime_wiring_plan_authorized": source.get("runtime_wiring_plan_authorized") is True,
        "candidate_count": source.get("candidate_count"),
        "candidate_family_count": source.get("candidate_family_count"),
        "diagnostic_fixture_count": source.get("diagnostic_fixture_count"),
        "candidate_fixture_matrix_count": source.get("candidate_fixture_matrix_count"),
        "wiring_targets": WIRING_TARGETS,
        "wiring_target_count": len(WIRING_TARGETS),
        "wiring_steps": WIRING_STEPS,
        "wiring_step_count": len(WIRING_STEPS),
        "acceptance_gates": ACCEPTANCE_GATES,
        "acceptance_gate_count": len(ACCEPTANCE_GATES),
        "runtime_modification_allowed_now": False,
        "candidate_generator_runtime_modification_allowed_now": False,
        "ranker_runtime_modification_allowed_now": False,
        "implementation_deferred_to_next_reviewed_stage": True,
        "review_required_before_implementation": True,
        "next_stage": NEXT_STAGE,
    }


def build_runtime_wiring_plan_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_review_artifact_present = SOURCE_REVIEW_ARTIFACT.exists()
    source_record = _load_json(SOURCE_REVIEW_ARTIFACT)
    source_review_artifact_parseable = source_record is not None

    source_review_passed = bool(
        source_record
        and source_record.get("local_diagnostic_harness_review_passed") is True
        and source_record.get("runtime_wiring_plan_authorized") is True
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_10_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_V1"
    )

    source_boundaries_ok = bool(
        source_record
        and source_record.get("runtime_execution_performed") is False
        and source_record.get("candidate_generator_wiring_authorized") is False
        and source_record.get("runtime_wiring_authorized") is False
        and source_record.get("runtime_solver_modified") is False
        and source_record.get("candidate_generator_modified") is False
        and source_record.get("ranker_runtime_modified") is False
        and source_record.get("real_evaluation_performed") is False
        and source_record.get("real_submission_allowed") is False
        and source_record.get("ready_for_real_kaggle_submission") is False
        and source_record.get("kaggle_authentication_allowed") is False
        and source_record.get("kaggle_authentication_performed") is False
        and source_record.get("kaggle_upload_allowed") is False
        and source_record.get("kaggle_submission_sent") is False
        and source_record.get("private_core_exposure") is False
        and source_record.get("legal_certification") is False
    )

    wiring_plan = build_wiring_plan(source_record)

    no_target_runtime_modification_now = all(
        target.get("runtime_modification_now") is False for target in WIRING_TARGETS
    )
    no_step_implementation_allowed_now = all(
        step.get("implementation_allowed_now") is False for step in WIRING_STEPS
    )
    all_targets_require_review = all(
        target.get("requires_review_before_implementation") is True for target in WIRING_TARGETS
    )

    runtime_wiring_plan_created = True
    runtime_wiring_plan_ready = True
    runtime_wiring_plan_review_required = True
    controlled_implementation_deferred = True

    runtime_execution_performed = False
    runtime_wiring_authorized = False
    candidate_generator_wiring_authorized = False
    runtime_solver_modified = False
    candidate_generator_modified = False
    ranker_runtime_modified = False
    real_evaluation_performed = False
    real_submission_allowed = False
    ready_for_real_kaggle_submission = False
    kaggle_authentication_allowed = False
    kaggle_authentication_performed = False
    kaggle_upload_allowed = False
    kaggle_submission_sent = False

    gates = [
        _gate("source_review_artifact_present", source_review_artifact_present, True, "Task 9 review artifact is present."),
        _gate("source_review_artifact_parseable", source_review_artifact_parseable, True, "Task 9 review artifact is parseable."),
        _gate("source_review_passed", source_review_passed, True, "Task 9 review passed and authorizes wiring plan."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Task 9 boundaries are preserved."),
        _gate("wiring_targets_defined", len(WIRING_TARGETS) == 4, True, "Four wiring targets are defined."),
        _gate("wiring_steps_defined", len(WIRING_STEPS) == 6, True, "Six wiring steps are defined."),
        _gate("all_targets_require_review", all_targets_require_review, True, "All wiring targets require review before implementation."),
        _gate("no_target_runtime_modification_now", no_target_runtime_modification_now, True, "No target modifies runtime now."),
        _gate("no_step_implementation_allowed_now", no_step_implementation_allowed_now, True, "No step implements wiring now."),
        _gate("runtime_wiring_plan_created", runtime_wiring_plan_created, True, "Runtime wiring plan is created."),
        _gate("runtime_wiring_plan_ready", runtime_wiring_plan_ready, True, "Runtime wiring plan is ready."),
        _gate("runtime_wiring_plan_review_required", runtime_wiring_plan_review_required, True, "Runtime wiring plan requires review."),
        _gate("controlled_implementation_deferred", controlled_implementation_deferred, True, "Controlled implementation is deferred."),
        _gate("runtime_execution_performed_false", runtime_execution_performed is False, True, "No runtime execution is performed."),
        _gate("candidate_generator_wiring_authorized_false", candidate_generator_wiring_authorized is False, True, "Candidate generator wiring remains blocked."),
        _gate("runtime_wiring_authorized_false", runtime_wiring_authorized is False, True, "Runtime wiring remains blocked."),
        _gate("runtime_solver_modified_false", runtime_solver_modified is False, True, "Runtime solver is not modified."),
        _gate("candidate_generator_modified_false", candidate_generator_modified is False, True, "Candidate generator is not modified."),
        _gate("ranker_runtime_modified_false", ranker_runtime_modified is False, True, "Ranker runtime is not modified."),
        _gate("real_evaluation_performed_false", real_evaluation_performed is False, True, "No real evaluation is performed."),
        _gate("real_submission_allowed_false", real_submission_allowed is False, True, "Real submission remains blocked."),
        _gate("ready_for_real_kaggle_submission_false", ready_for_real_kaggle_submission is False, True, "Real submission readiness remains blocked."),
        _gate("kaggle_authentication_allowed_false", kaggle_authentication_allowed is False, True, "Kaggle authentication remains blocked."),
        _gate("kaggle_authentication_performed_false", kaggle_authentication_performed is False, True, "Kaggle authentication is not performed."),
        _gate("kaggle_upload_allowed_false", kaggle_upload_allowed is False, True, "Kaggle upload remains blocked."),
        _gate("kaggle_submission_sent_false", kaggle_submission_sent is False, True, "No Kaggle submission is sent."),
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
        _gate("fail_closed_active", True, True, "Plan fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    record_passed = len(required_gates) == len(passed_required_gates)

    plan_summary = {
        "plan_status": "READY" if record_passed else "FAIL_CLOSED",
        "plan_verdict": PLAN_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "wiring_target_count": len(WIRING_TARGETS),
        "wiring_step_count": len(WIRING_STEPS),
        "acceptance_gate_count": len(ACCEPTANCE_GATES),
        "runtime_wiring_plan_created": runtime_wiring_plan_created,
        "runtime_wiring_plan_ready": runtime_wiring_plan_ready,
        "runtime_wiring_plan_review_required": runtime_wiring_plan_review_required,
        "runtime_wiring_authorized": False,
        "candidate_generator_wiring_authorized": False,
        "controlled_implementation_deferred": controlled_implementation_deferred,
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
        "source_review_artifact": str(SOURCE_REVIEW_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_review_artifact_present": source_review_artifact_present,
        "source_review_artifact_parseable": source_review_artifact_parseable,
        "source_review_passed": source_review_passed,
        "source_boundaries_ok": source_boundaries_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "plan_verdict": PLAN_VERDICT,
        "runtime_wiring_plan_created": runtime_wiring_plan_created,
        "runtime_wiring_plan_ready": runtime_wiring_plan_ready,
        "runtime_wiring_plan_valid": record_passed,
        "runtime_wiring_plan_review_required": runtime_wiring_plan_review_required,
        "controlled_implementation_deferred": controlled_implementation_deferred,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "plan_summary": plan_summary,
        "wiring_plan": wiring_plan,
        "wiring_targets": WIRING_TARGETS,
        "wiring_target_count": len(WIRING_TARGETS),
        "wiring_steps": WIRING_STEPS,
        "wiring_step_count": len(WIRING_STEPS),
        "acceptance_gates": ACCEPTANCE_GATES,
        "acceptance_gate_count": len(ACCEPTANCE_GATES),
        "all_targets_require_review": all_targets_require_review,
        "no_target_runtime_modification_now": no_target_runtime_modification_now,
        "no_step_implementation_allowed_now": no_step_implementation_allowed_now,
        "implementation_allowed_now": False,
        "runtime_execution_performed": runtime_execution_performed,
        "candidate_generator_wiring_authorized": candidate_generator_wiring_authorized,
        "runtime_wiring_authorized": runtime_wiring_authorized,
        "runtime_solver_modified": runtime_solver_modified,
        "candidate_generator_modified": candidate_generator_modified,
        "ranker_runtime_modified": ranker_runtime_modified,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "program_synthesis_candidate_generator_runtime_wiring_plan_allowed": True,
        "real_kaggle_evaluation_allowed": False,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "open_source_prize_eligibility_required": True,
        "real_submission_allowed": real_submission_allowed,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": kaggle_authentication_allowed,
        "kaggle_authentication_performed": kaggle_authentication_performed,
        "kaggle_upload_allowed": kaggle_upload_allowed,
        "kaggle_submission_sent": kaggle_submission_sent,
        "operator_approval_required": True,
        "operator_approval_received": False,
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
        "plan_gate_count": len(gates),
        "plan_pass_count": len(passed_required_gates),
        "plan_blocking_issue_count": 0 if record_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if record_passed else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "risk_controls": RISK_CONTROLS,
        "risk_control_count": len(RISK_CONTROLS),
        "quality_targets": QUALITY_TARGETS,
        "quality_target_count": len(QUALITY_TARGETS),
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-RUNTIME-WIRING-PLAN-" + signature[:12]
    return record


def validate_runtime_wiring_plan_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_review_artifact_present",
        "source_review_artifact_parseable",
        "source_review_passed",
        "source_boundaries_ok",
        "runtime_wiring_plan_created",
        "runtime_wiring_plan_ready",
        "runtime_wiring_plan_valid",
        "runtime_wiring_plan_review_required",
        "controlled_implementation_deferred",
        "all_targets_require_review",
        "no_target_runtime_modification_now",
        "no_step_implementation_allowed_now",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "program_synthesis_candidate_generator_runtime_wiring_plan_allowed",
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
        "implementation_allowed_now",
        "runtime_execution_performed",
        "candidate_generator_wiring_authorized",
        "runtime_wiring_authorized",
        "runtime_solver_modified",
        "candidate_generator_modified",
        "ranker_runtime_modified",
        "real_evaluation_performed",
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

    if record.get("plan_verdict") != PLAN_VERDICT:
        issues.append("PLAN_VERDICT_MISMATCH")

    expected_counts = {
        "wiring_target_count": 4,
        "wiring_step_count": 6,
        "acceptance_gate_count": 15,
        "plan_blocking_issue_count": 0,
        "issue_count": 0,
        "risk_control_count": 11,
        "quality_target_count": 7,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    wiring_plan = record.get("wiring_plan")
    if not isinstance(wiring_plan, dict):
        issues.append("WIRING_PLAN_MISSING")
    else:
        if wiring_plan.get("plan_mode") != "PLAN_ONLY":
            issues.append("WIRING_PLAN_MODE_MISMATCH")
        if wiring_plan.get("runtime_modification_allowed_now") is not False:
            issues.append("WIRING_PLAN_RUNTIME_MODIFICATION_NOT_FALSE")
        if wiring_plan.get("implementation_deferred_to_next_reviewed_stage") is not True:
            issues.append("WIRING_PLAN_IMPLEMENTATION_NOT_DEFERRED")
        if wiring_plan.get("next_stage") != NEXT_STAGE:
            issues.append("WIRING_PLAN_NEXT_STAGE_MISMATCH")

    targets = record.get("wiring_targets")
    if not isinstance(targets, list) or len(targets) != 4:
        issues.append("WIRING_TARGETS_MISSING_OR_COUNT_MISMATCH")
    else:
        for target in targets:
            if target.get("runtime_modification_now") is not False:
                issues.append(f"WIRING_TARGET_RUNTIME_MODIFICATION_NOT_FALSE:{target.get('target_id')}")
            if target.get("requires_review_before_implementation") is not True:
                issues.append(f"WIRING_TARGET_REVIEW_NOT_REQUIRED:{target.get('target_id')}")

    steps = record.get("wiring_steps")
    if not isinstance(steps, list) or len(steps) != 6:
        issues.append("WIRING_STEPS_MISSING_OR_COUNT_MISMATCH")
    else:
        for step in steps:
            if step.get("implementation_allowed_now") is not False:
                issues.append(f"WIRING_STEP_IMPLEMENTATION_NOT_FALSE:{step.get('step_id')}")

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

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "plan_verdict": record["plan_verdict"],
        "next_stage": record["next_stage"],
        "source_review_passed": record["source_review_passed"],
        "runtime_wiring_plan_created": record["runtime_wiring_plan_created"],
        "runtime_wiring_plan_ready": record["runtime_wiring_plan_ready"],
        "runtime_wiring_plan_valid": record["runtime_wiring_plan_valid"],
        "runtime_wiring_plan_review_required": record["runtime_wiring_plan_review_required"],
        "controlled_implementation_deferred": record["controlled_implementation_deferred"],
        "wiring_target_count": record["wiring_target_count"],
        "wiring_step_count": record["wiring_step_count"],
        "acceptance_gate_count": record["acceptance_gate_count"],
        "implementation_allowed_now": record["implementation_allowed_now"],
        "runtime_execution_performed": record["runtime_execution_performed"],
        "candidate_generator_wiring_authorized": record["candidate_generator_wiring_authorized"],
        "runtime_wiring_authorized": record["runtime_wiring_authorized"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "candidate_generator_modified": record["candidate_generator_modified"],
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
        f"plan_verdict={record['plan_verdict']}",
        f"next_stage={record['next_stage']}",
        f"source_review_passed={record['source_review_passed']}",
        f"runtime_wiring_plan_created={record['runtime_wiring_plan_created']}",
        f"runtime_wiring_plan_ready={record['runtime_wiring_plan_ready']}",
        f"runtime_wiring_plan_valid={record['runtime_wiring_plan_valid']}",
        f"runtime_wiring_plan_review_required={record['runtime_wiring_plan_review_required']}",
        f"controlled_implementation_deferred={record['controlled_implementation_deferred']}",
        f"wiring_target_count={record['wiring_target_count']}",
        f"wiring_step_count={record['wiring_step_count']}",
        f"acceptance_gate_count={record['acceptance_gate_count']}",
        f"implementation_allowed_now={record['implementation_allowed_now']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
        f"candidate_generator_wiring_authorized={record['candidate_generator_wiring_authorized']}",
        f"runtime_wiring_authorized={record['runtime_wiring_authorized']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"candidate_generator_modified={record['candidate_generator_modified']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    target_lines = "\n".join(
        [
            f"- `{target['target_id']}` `{target['name']}` planned module `{target['planned_module']}` runtime_modification_now=`{target['runtime_modification_now']}`"
            for target in record["wiring_targets"]
        ]
    )
    step_lines = "\n".join(
        [
            f"- `{step['step_id']}` `{step['name']}` implementation_allowed_now=`{step['implementation_allowed_now']}`"
            for step in record["wiring_steps"]
        ]
    )

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- plan_verdict: `{record['plan_verdict']}`
- next_stage: `{record['next_stage']}`

## Plan Summary

- source_review_passed: `{record['source_review_passed']}`
- runtime_wiring_plan_created: `{record['runtime_wiring_plan_created']}`
- runtime_wiring_plan_ready: `{record['runtime_wiring_plan_ready']}`
- runtime_wiring_plan_valid: `{record['runtime_wiring_plan_valid']}`
- runtime_wiring_plan_review_required: `{record['runtime_wiring_plan_review_required']}`
- controlled_implementation_deferred: `{record['controlled_implementation_deferred']}`
- wiring_target_count: `{record['wiring_target_count']}`
- wiring_step_count: `{record['wiring_step_count']}`
- acceptance_gate_count: `{record['acceptance_gate_count']}`

## Wiring Targets

{target_lines}

## Wiring Steps

{step_lines}

## Boundary

- implementation_allowed_now: `{record['implementation_allowed_now']}`
- runtime_execution_performed: `{record['runtime_execution_performed']}`
- candidate_generator_wiring_authorized: `{record['candidate_generator_wiring_authorized']}`
- runtime_wiring_authorized: `{record['runtime_wiring_authorized']}`
- runtime_solver_modified: `{record['runtime_solver_modified']}`
- candidate_generator_modified: `{record['candidate_generator_modified']}`
- ranker_runtime_modified: `{record['ranker_runtime_modified']}`
- real_evaluation_performed: `{record['real_evaluation_performed']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- ready_for_real_kaggle_submission: `{record['ready_for_real_kaggle_submission']}`
- kaggle_authentication_allowed: `{record['kaggle_authentication_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
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
    record = build_runtime_wiring_plan_record()
    issues = validate_runtime_wiring_plan_record(record)
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
    print(record["plan_verdict"])
    print(record["next_stage"])
    print(f"wiring_target_count={record['wiring_target_count']}")
    print(f"wiring_step_count={record['wiring_step_count']}")
    print(f"acceptance_gate_count={record['acceptance_gate_count']}")
    print(f"runtime_wiring_plan_review_required={record['runtime_wiring_plan_review_required']}")
    print(f"controlled_implementation_deferred={record['controlled_implementation_deferred']}")
    print(f"implementation_allowed_now={record['implementation_allowed_now']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
