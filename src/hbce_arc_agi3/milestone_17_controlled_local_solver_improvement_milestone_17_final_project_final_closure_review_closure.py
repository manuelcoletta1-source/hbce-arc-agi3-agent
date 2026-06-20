"""Milestone #17 Task 54 - Controlled Local Solver Improvement Milestone 17 Final Project Final Closure Review Closure v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_milestone_17_final_project_final_closure_review as task53


TASK_NAME = "MILESTONE_17_TASK_54_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_MARKER = (
    "MILESTONE_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_READY"
)
FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_VERDICT = (
    "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_PASS_REVIEW_CLOSED"
)
FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_DECISION = (
    "CLOSE_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_NO_IMPLEMENTATION_AUTHORIZED"
)
FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_REASON = (
    "TASK_53_REVIEWED_FINAL_PROJECT_FINAL_CLOSURE_WITHOUT_IMPLEMENTATION_RUNTIME_OR_SUBMISSION"
)

PREVIOUS_STAGE = (
    "MILESTONE_17_TASK_53_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_V1"
)
NEXT_STAGE = (
    "MILESTONE_17_TASK_55_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_RECORD_V1"
)

SOURCE_TASK_53_FINAL_BASELINE_COMMIT = "4148b86"
SOURCE_TASK_53_FINAL_SIGNATURE = "E77962BE62031540"

FINAL_PROJECT_FINAL_CLOSURE_SCOPE = "FINAL_PROJECT_FINAL_CLOSURE_ONLY"
FINAL_PROJECT_FINAL_CLOSURE_REVIEW_SCOPE = "REVIEW_FINAL_PROJECT_FINAL_CLOSURE_ONLY"
FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_ONLY"
FINAL_PROJECT_FINAL_INDEX_SCOPE = "FINAL_PROJECT_FINAL_INDEX_ONLY"
FINAL_PROJECT_FINAL_INDEX_REVIEW_SCOPE = "REVIEW_FINAL_PROJECT_FINAL_INDEX_ONLY"
FINAL_PROJECT_FINAL_INDEX_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_PROJECT_FINAL_INDEX_REVIEW_ONLY"
FINAL_PROJECT_FINAL_SEAL_SCOPE = "FINAL_PROJECT_FINAL_SEAL_ONLY"
FINAL_PROJECT_FINAL_SEAL_REVIEW_SCOPE = "REVIEW_FINAL_PROJECT_FINAL_SEAL_ONLY"
FINAL_PROJECT_FINAL_SEAL_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_PROJECT_FINAL_SEAL_REVIEW_ONLY"
FINAL_PROJECT_CLOSEOUT_SCOPE = "FINAL_PROJECT_CLOSEOUT_ONLY"
FINAL_PROJECT_CLOSEOUT_REVIEW_SCOPE = "REVIEW_FINAL_PROJECT_CLOSEOUT_ONLY"
FINAL_PROJECT_CLOSEOUT_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_PROJECT_CLOSEOUT_REVIEW_ONLY"
FINAL_PROJECT_SUMMARY_SCOPE = "FINAL_PROJECT_SUMMARY_ONLY"
FINAL_PROJECT_SUMMARY_REVIEW_SCOPE = "REVIEW_FINAL_PROJECT_SUMMARY_ONLY"
FINAL_PROJECT_SUMMARY_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_PROJECT_SUMMARY_REVIEW_ONLY"
FINAL_RELEASE_NOTE_SCOPE = "FINAL_RELEASE_NOTE_ONLY"
FINAL_RELEASE_NOTE_REVIEW_SCOPE = "REVIEW_FINAL_RELEASE_NOTE_ONLY"
FINAL_RELEASE_NOTE_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_RELEASE_NOTE_REVIEW_ONLY"
FINAL_CLOSE_MARK_SCOPE = "MARK_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_CLOSED_ONLY"
FINAL_CLOSE_MARK_REVIEW_SCOPE = "REVIEW_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_CLOSE_MARK_ONLY"
FINAL_CLOSE_MARK_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_CLOSE_MARK_REVIEW_ONLY"
FINAL_SEAL_SCOPE = "SEAL_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_ONLY"
FINAL_SEAL_REVIEW_SCOPE = "REVIEW_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_SEAL_ONLY"
FINAL_SEAL_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_SEAL_REVIEW_ONLY"
FINAL_INDEX_SCOPE = "INDEX_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_ONLY"
FINAL_INDEX_REVIEW_SCOPE = "REVIEW_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_INDEX_ONLY"
FINAL_INDEX_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_INDEX_REVIEW_ONLY"
PLAN_AUTHORIZATION_SCOPE = "PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

TASK_MODE = (
    "MILESTONE_17_TASK_54_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_V1_"
    "CLOSURE_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-v1")
DOC_PATH = Path("docs/milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-v1.md")


def _build_closed_final_project_final_closure_review_stages() -> tuple[dict[str, Any], ...]:
    task53_status = task53.build_controlled_local_solver_improvement_milestone_17_final_project_final_closure_review()
    stages: list[dict[str, Any]] = []

    for stage in task53_status["reviewed_final_project_final_closure_stages"]:
        number = stage["stage_id"].split("-")[-1]
        stages.append(
            {
                "stage_id": f"M17-FINAL-PROJECT-FINAL-CLOSURE-REVIEW-CLOSURE-STAGE-{number}",
                "task": stage["task"],
                "commit": stage["commit"],
                "signature": stage["signature"],
                "closure_status": f"CLOSED_{stage['review_status']}",
                "implementation_authorized": False,
                "runtime_execution_allowed": False,
                "submission_allowed": False,
            }
        )

    stages.append(
        {
            "stage_id": "M17-FINAL-PROJECT-FINAL-CLOSURE-REVIEW-CLOSURE-STAGE-43",
            "task": PREVIOUS_STAGE,
            "commit": SOURCE_TASK_53_FINAL_BASELINE_COMMIT,
            "signature": SOURCE_TASK_53_FINAL_SIGNATURE,
            "closure_status": "FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSED",
            "implementation_authorized": False,
            "runtime_execution_allowed": False,
            "submission_allowed": False,
        }
    )

    return tuple(stages)


CLOSED_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_STAGES = _build_closed_final_project_final_closure_review_stages()


FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_GATES: tuple[str, ...] = (
    "source_task_53_commit_bound",
    "source_task_53_signature_bound",
    "previous_stage_bound",
    "next_stage_declared",
    "final_project_final_closure_scope_confirmed",
    "final_project_final_closure_review_scope_confirmed",
    "final_project_final_closure_review_closure_scope_confirmed",
    "final_project_final_index_scope_confirmed",
    "final_project_final_index_review_scope_confirmed",
    "final_project_final_index_review_closure_scope_confirmed",
    "final_project_final_seal_scope_confirmed",
    "final_project_final_seal_review_scope_confirmed",
    "final_project_final_seal_review_closure_scope_confirmed",
    "final_project_closeout_scope_confirmed",
    "final_project_closeout_review_scope_confirmed",
    "final_project_closeout_review_closure_scope_confirmed",
    "final_project_summary_scope_confirmed",
    "final_project_summary_review_scope_confirmed",
    "final_project_summary_review_closure_scope_confirmed",
    "final_release_note_scope_confirmed",
    "final_release_note_review_scope_confirmed",
    "final_release_note_review_closure_scope_confirmed",
    "final_close_mark_scope_confirmed",
    "final_close_mark_review_scope_confirmed",
    "final_close_mark_review_closure_scope_confirmed",
    "final_seal_scope_confirmed",
    "final_seal_review_scope_confirmed",
    "final_seal_review_closure_scope_confirmed",
    "final_index_scope_confirmed",
    "final_index_review_scope_confirmed",
    "final_index_review_closure_scope_confirmed",
    "plan_authorization_scope_plan_only",
    "implementation_authorization_scope_not_granted",
    "closed_final_project_final_closure_review_stage_count_forty_three",
    "all_final_project_final_closure_review_stages_closed",
    "all_closed_final_project_final_closure_review_stages_have_commits",
    "all_closed_final_project_final_closure_review_stages_have_signatures",
    "all_closed_final_project_final_closure_review_stages_no_implementation",
    "all_closed_final_project_final_closure_review_stages_no_runtime_execution",
    "all_closed_final_project_final_closure_review_stages_no_submission",
    "final_project_final_closure_review_closure_ready",
    "final_project_final_closure_review_closure_passed",
    "final_project_final_closure_review_closure_locked",
    "milestone_17_final_project_final_closure_review_closed",
    "controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed",
    "implementation_authorization_not_granted",
    "implementation_not_authorized",
    "implementation_blocked",
    "implementation_not_performed",
    "runtime_solver_patch_not_allowed",
    "runtime_solver_not_modified",
    "ranker_runtime_patch_not_allowed",
    "ranker_runtime_not_modified",
    "candidate_generator_patch_not_allowed",
    "candidate_generator_not_modified",
    "runtime_wiring_not_allowed",
    "runtime_wiring_not_performed",
    "runtime_activation_not_authorized",
    "runtime_activation_not_performed",
    "runtime_execution_not_allowed",
    "runtime_execution_not_performed",
    "real_evaluation_not_allowed",
    "real_submission_not_allowed",
    "manual_upload_not_allowed",
    "upload_not_performed",
    "kaggle_authentication_not_allowed",
    "kaggle_authentication_not_performed",
    "kaggle_submission_not_sent",
    "competitive_score_claim_not_allowed",
    "official_score_claim_not_allowed",
    "private_core_not_exposed",
    "legal_certification_false",
    "fail_closed_required",
    "fail_closed_active",
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_53_final_baseline_commit": SOURCE_TASK_53_FINAL_BASELINE_COMMIT,
        "source_task_53_final_signature": SOURCE_TASK_53_FINAL_SIGNATURE,
        "final_project_final_closure_review_closure_scope": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_SCOPE,
        "closed_final_project_final_closure_review_stage_count": len(CLOSED_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_STAGES),
        "verdict": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_VERDICT,
        "decision": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_DECISION,
        "reason": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "final_project_final_closure_review_closure_marker": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_MARKER,
        "signature": signature,
        "source_task_53_final_baseline_commit": SOURCE_TASK_53_FINAL_BASELINE_COMMIT,
        "source_task_53_final_signature": SOURCE_TASK_53_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_VERDICT,
        "decision": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_DECISION,
        "final_project_final_closure_review_closure_reason": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_project_final_closure_scope": FINAL_PROJECT_FINAL_CLOSURE_SCOPE,
        "final_project_final_closure_review_scope": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_SCOPE,
        "final_project_final_closure_review_closure_scope": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_SCOPE,
        "final_project_final_index_scope": FINAL_PROJECT_FINAL_INDEX_SCOPE,
        "final_project_final_index_review_scope": FINAL_PROJECT_FINAL_INDEX_REVIEW_SCOPE,
        "final_project_final_index_review_closure_scope": FINAL_PROJECT_FINAL_INDEX_REVIEW_CLOSURE_SCOPE,
        "final_project_final_seal_scope": FINAL_PROJECT_FINAL_SEAL_SCOPE,
        "final_project_final_seal_review_scope": FINAL_PROJECT_FINAL_SEAL_REVIEW_SCOPE,
        "final_project_final_seal_review_closure_scope": FINAL_PROJECT_FINAL_SEAL_REVIEW_CLOSURE_SCOPE,
        "final_project_closeout_scope": FINAL_PROJECT_CLOSEOUT_SCOPE,
        "final_project_closeout_review_scope": FINAL_PROJECT_CLOSEOUT_REVIEW_SCOPE,
        "final_project_closeout_review_closure_scope": FINAL_PROJECT_CLOSEOUT_REVIEW_CLOSURE_SCOPE,
        "final_project_summary_scope": FINAL_PROJECT_SUMMARY_SCOPE,
        "final_project_summary_review_scope": FINAL_PROJECT_SUMMARY_REVIEW_SCOPE,
        "final_project_summary_review_closure_scope": FINAL_PROJECT_SUMMARY_REVIEW_CLOSURE_SCOPE,
        "final_release_note_scope": FINAL_RELEASE_NOTE_SCOPE,
        "final_release_note_review_scope": FINAL_RELEASE_NOTE_REVIEW_SCOPE,
        "final_release_note_review_closure_scope": FINAL_RELEASE_NOTE_REVIEW_CLOSURE_SCOPE,
        "final_close_mark_scope": FINAL_CLOSE_MARK_SCOPE,
        "final_close_mark_review_scope": FINAL_CLOSE_MARK_REVIEW_SCOPE,
        "final_close_mark_review_closure_scope": FINAL_CLOSE_MARK_REVIEW_CLOSURE_SCOPE,
        "final_seal_scope": FINAL_SEAL_SCOPE,
        "final_seal_review_scope": FINAL_SEAL_REVIEW_SCOPE,
        "final_seal_review_closure_scope": FINAL_SEAL_REVIEW_CLOSURE_SCOPE,
        "final_index_scope": FINAL_INDEX_SCOPE,
        "final_index_review_scope": FINAL_INDEX_REVIEW_SCOPE,
        "final_index_review_closure_scope": FINAL_INDEX_REVIEW_CLOSURE_SCOPE,
        "plan_authorized": True,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure_ready": True,
        "controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure_passed": True,
        "controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure_locked": True,
        "milestone_17_final_project_final_closure_review_closed": True,
        "controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed": True,
        "closed_final_project_final_closure_review_stage_count": len(CLOSED_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_STAGES),
        "closed_final_project_final_closure_review_stages": CLOSED_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_STAGES,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "runtime_solver_patch_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_patch_allowed": False,
        "ranker_runtime_modified": False,
        "candidate_generator_patch_allowed": False,
        "candidate_generator_modified": False,
        "runtime_wiring_allowed": False,
        "runtime_wiring_performed": False,
        "runtime_activation_authorized": False,
        "runtime_activation_performed": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "final_project_final_closure_review_closure_gate_count": len(FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_GATES),
        "final_project_final_closure_review_closure_gate_failure_count": 0,
        "final_project_final_closure_review_closure_gates": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_GATES,
        "artifacts": artifacts,
    }


def validate_controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure(
    status: dict[str, Any],
) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "final_project_final_closure_review_closure_marker": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_MARKER,
        "source_task_53_final_baseline_commit": SOURCE_TASK_53_FINAL_BASELINE_COMMIT,
        "source_task_53_final_signature": SOURCE_TASK_53_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_project_final_closure_scope": FINAL_PROJECT_FINAL_CLOSURE_SCOPE,
        "final_project_final_closure_review_scope": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_SCOPE,
        "final_project_final_closure_review_closure_scope": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_SCOPE,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "verdict": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_VERDICT,
        "decision": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_DECISION,
        "final_project_final_closure_review_closure_reason": FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    stages = tuple(status.get("closed_final_project_final_closure_review_stages", ()))
    stage_ids = [stage.get("stage_id") for stage in stages]

    if status.get("closed_final_project_final_closure_review_stage_count") != 43:
        issues.append("closed_final_project_final_closure_review_stage_count must be 43")
    if len(stages) != 43:
        issues.append("closed_final_project_final_closure_review_stages length must be 43")
    if len(stage_ids) != len(set(stage_ids)):
        issues.append("closed final project final closure review stage IDs must be unique")

    for stage in stages:
        if not stage.get("closure_status"):
            issues.append(f"{stage.get('stage_id')} must have closure_status")
        if not stage.get("commit"):
            issues.append(f"{stage.get('stage_id')} must have commit")
        if not stage.get("signature"):
            issues.append(f"{stage.get('stage_id')} must have signature")
        if stage.get("implementation_authorized") is not False:
            issues.append(f"{stage.get('stage_id')} implementation_authorized must be False")
        if stage.get("runtime_execution_allowed") is not False:
            issues.append(f"{stage.get('stage_id')} runtime_execution_allowed must be False")
        if stage.get("submission_allowed") is not False:
            issues.append(f"{stage.get('stage_id')} submission_allowed must be False")

    required_true = (
        "plan_authorized",
        "controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure_ready",
        "controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure_passed",
        "controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure_locked",
        "milestone_17_final_project_final_closure_review_closed",
        "controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
    )
    required_false = (
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
        "ranker_runtime_patch_allowed",
        "ranker_runtime_modified",
        "candidate_generator_patch_allowed",
        "candidate_generator_modified",
        "runtime_wiring_allowed",
        "runtime_wiring_performed",
        "runtime_activation_authorized",
        "runtime_activation_performed",
        "runtime_execution_allowed",
        "runtime_execution_performed",
        "real_evaluation_allowed",
        "real_submission_allowed",
        "manual_upload_allowed",
        "upload_performed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_submission_sent",
        "competitive_score_claim_allowed",
        "official_score_claim_allowed",
        "private_core_exposure",
        "legal_certification",
    )

    for key in required_true:
        if status.get(key) is not True:
            issues.append(f"{key} must be True")
    for key in required_false:
        if status.get(key) is not False:
            issues.append(f"{key} must be False")

    if status.get("final_project_final_closure_review_closure_gate_count") != len(FINAL_PROJECT_FINAL_CLOSURE_REVIEW_CLOSURE_GATES):
        issues.append("final_project_final_closure_review_closure_gate_count mismatch")
    if status.get("final_project_final_closure_review_closure_gate_failure_count") != 0:
        issues.append("final_project_final_closure_review_closure_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def final_project_final_closure_review_closure_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["final_project_final_closure_review_closure_marker"],
        "signature": status["signature"],
        "source_task_53_final_baseline_commit": status["source_task_53_final_baseline_commit"],
        "source_task_53_final_signature": status["source_task_53_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "final_project_final_closure_review_closure_scope": status["final_project_final_closure_review_closure_scope"],
        "closed_final_project_final_closure_review_stage_count": status["closed_final_project_final_closure_review_stage_count"],
        "milestone_17_final_project_final_closure_review_closed": status["milestone_17_final_project_final_closure_review_closed"],
        "controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed": status[
            "controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed"
        ],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "official_score_claim_allowed": status["official_score_claim_allowed"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "final_project_final_closure_review_closure_gate_count": status["final_project_final_closure_review_closure_gate_count"],
        "final_project_final_closure_review_closure_gate_failure_count": status[
            "final_project_final_closure_review_closure_gate_failure_count"
        ],
        "artifact_count": len(status["artifacts"]),
    }


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["final_project_final_closure_review_closure_marker"],
        f"signature={status['signature']}",
        f"source_task_53_final_baseline_commit={status['source_task_53_final_baseline_commit']}",
        f"source_task_53_final_signature={status['source_task_53_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"final_project_final_closure_review_closure_reason={status['final_project_final_closure_review_closure_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"final_project_final_closure_review_closure_scope={status['final_project_final_closure_review_closure_scope']}",
        f"closed_final_project_final_closure_review_stage_count={status['closed_final_project_final_closure_review_stage_count']}",
        f"milestone_17_final_project_final_closure_review_closed={status['milestone_17_final_project_final_closure_review_closed']}",
        f"controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed={status['controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"official_score_claim_allowed={status['official_score_claim_allowed']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"final_project_final_closure_review_closure_gate_count={status['final_project_final_closure_review_closure_gate_count']}",
        f"final_project_final_closure_review_closure_gate_failure_count={status['final_project_final_closure_review_closure_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def build_markdown(status: dict[str, Any]) -> str:
    stage_lines = "\n".join(
        f"- `{stage['stage_id']}` - `{stage['task']}` · commit `{stage['commit']}` · `{stage['closure_status']}`"
        for stage in status["closed_final_project_final_closure_review_stages"]
    )

    return f"""# Milestone #17 Task 54 - Controlled Local Solver Improvement Milestone 17 Final Project Final Closure Review Closure v1

## Status

`{status["final_project_final_closure_review_closure_marker"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 53 final baseline commit: `{status["source_task_53_final_baseline_commit"]}`
- source Task 53 final signature: `{status["source_task_53_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Final project final closure review closure

- final_project_final_closure_scope: `{status["final_project_final_closure_scope"]}`
- final_project_final_closure_review_scope: `{status["final_project_final_closure_review_scope"]}`
- final_project_final_closure_review_closure_scope: `{status["final_project_final_closure_review_closure_scope"]}`
- closed_final_project_final_closure_review_stage_count: `{status["closed_final_project_final_closure_review_stage_count"]}`
- milestone_17_final_project_final_closure_review_closed: `{status["milestone_17_final_project_final_closure_review_closed"]}`
- controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed: `{status["controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed"]}`

{stage_lines}

## Closure statement

The Milestone #17 controlled local solver improvement final project final closure review is closed as local-only, deterministic, public-safe documentation.
No implementation authorization is granted.
No runtime execution is authorized.
No real evaluation is authorized.
No Kaggle submission is authorized.
No competitive or official score claim is authorized.

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Boundary

- implementation_authorized: `{status["implementation_authorized"]}`
- implementation_blocked: `{status["implementation_blocked"]}`
- runtime_execution_allowed: `{status["runtime_execution_allowed"]}`
- real_submission_allowed: `{status["real_submission_allowed"]}`
- kaggle_submission_sent: `{status["kaggle_submission_sent"]}`
- private_core_exposure: `{status["private_core_exposure"]}`
- legal_certification: `{status["legal_certification"]}`
- fail_closed_active: `{status["fail_closed_active"]}`
"""


def write_controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure()
    issues = validate_controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure(resolved)
    if issues:
        raise ValueError(
            "Invalid controlled local solver improvement milestone 17 final project final closure review closure: "
            + "; ".join(issues)
        )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = final_project_final_closure_review_closure_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-closure-review-closure-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_local_solver_improvement_milestone_17_final_project_final_closure_review_closure_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_53_final_baseline_commit"])
    print(status["task_mode"])
    print(status["final_project_final_closure_review_closure_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["final_project_final_closure_review_closure_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_53_final_baseline_commit",
        "source_task_53_final_signature",
        "final_project_final_closure_scope",
        "final_project_final_closure_review_scope",
        "final_project_final_closure_review_closure_scope",
        "final_project_final_index_scope",
        "final_project_final_index_review_scope",
        "final_project_final_index_review_closure_scope",
        "final_project_final_seal_scope",
        "final_project_final_seal_review_scope",
        "final_project_final_seal_review_closure_scope",
        "final_project_closeout_scope",
        "final_project_closeout_review_scope",
        "final_project_closeout_review_closure_scope",
        "final_project_summary_scope",
        "final_project_summary_review_scope",
        "final_project_summary_review_closure_scope",
        "final_release_note_scope",
        "final_release_note_review_scope",
        "final_release_note_review_closure_scope",
        "final_close_mark_scope",
        "final_close_mark_review_scope",
        "final_close_mark_review_closure_scope",
        "final_seal_scope",
        "final_seal_review_scope",
        "final_seal_review_closure_scope",
        "final_index_scope",
        "final_index_review_scope",
        "final_index_review_closure_scope",
        "closed_final_project_final_closure_review_stage_count",
        "milestone_17_final_project_final_closure_review_closed",
        "controlled_local_solver_improvement_milestone_17_project_final_closure_review_closed",
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_blocked",
        "implementation_performed",
        "runtime_execution_allowed",
        "runtime_execution_performed",
        "real_evaluation_allowed",
        "real_submission_allowed",
        "manual_upload_allowed",
        "upload_performed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_submission_sent",
        "competitive_score_claim_allowed",
        "official_score_claim_allowed",
        "private_core_exposure",
        "legal_certification",
        "fail_closed_required",
        "fail_closed_active",
        "final_project_final_closure_review_closure_gate_count",
        "final_project_final_closure_review_closure_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for stage in status["closed_final_project_final_closure_review_stages"]:
        print(
            f"closed_final_project_final_closure_review_stage={stage['stage_id']}|{stage['task']}|"
            f"{stage['commit']}|{stage['signature']}|{stage['closure_status']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
