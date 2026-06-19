"""Milestone #17 Task 43 - Controlled Local Solver Improvement Milestone 17 Final Project Closeout v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_43_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_CLOSEOUT_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

FINAL_PROJECT_CLOSEOUT_MARKER = "MILESTONE_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_PROJECT_CLOSEOUT_READY"
FINAL_PROJECT_CLOSEOUT_VERDICT = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_CLOSEOUT_PASS_CLOSED"
FINAL_PROJECT_CLOSEOUT_DECISION = (
    "CLOSEOUT_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_PROJECT_NO_IMPLEMENTATION_AUTHORIZED"
)
FINAL_PROJECT_CLOSEOUT_REASON = (
    "TASK_42_CLOSED_FINAL_PROJECT_SUMMARY_REVIEW_WITHOUT_IMPLEMENTATION_RUNTIME_OR_SUBMISSION"
)

PREVIOUS_STAGE = "MILESTONE_17_TASK_42_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_SUMMARY_REVIEW_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_17_TASK_44_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_CLOSEOUT_REVIEW_V1"

SOURCE_TASK_42_FINAL_BASELINE_COMMIT = "9e5881a"
SOURCE_TASK_42_FINAL_SIGNATURE = "D8DA51222260A7DE"

FINAL_PROJECT_CLOSEOUT_SCOPE = "FINAL_PROJECT_CLOSEOUT_ONLY"
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
    "MILESTONE_17_TASK_43_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_CLOSEOUT_V1_"
    "CLOSEOUT_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-local-solver-improvement-milestone-17-final-project-closeout-v1")
DOC_PATH = Path("docs/milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-v1.md")


_STAGE_SOURCE: tuple[tuple[str, str, str, str, str], ...] = (
    ("1", "MILESTONE_17_TASK_11_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_V1", "566dad4", "6380B16C08C60A41", "FINAL_PROJECT_CLOSEOUT_PLAN_CONFIRMED"),
    ("2", "MILESTONE_17_TASK_12_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_REVIEW_V1", "ee29733", "B83CF1D86F83BDE8", "FINAL_PROJECT_CLOSEOUT_PLAN_REVIEW_CONFIRMED"),
    ("3", "MILESTONE_17_TASK_13_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_CLOSURE_V1", "e3b6528", "D992AEA3A992CA7F", "FINAL_PROJECT_CLOSEOUT_PLAN_CLOSURE_CONFIRMED"),
    ("4", "MILESTONE_17_TASK_14_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_V1", "a04d19e", "F32F27EF4D9D20E8", "FINAL_PROJECT_CLOSEOUT_CYCLE_STATUS_REVIEW_CONFIRMED"),
    ("5", "MILESTONE_17_TASK_15_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_CLOSURE_V1", "36e2084", "416DA88ECB7960B9", "FINAL_PROJECT_CLOSEOUT_CYCLE_STATUS_REVIEW_CLOSURE_CONFIRMED"),
    ("6", "MILESTONE_17_TASK_16_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_ARCHIVE_V1", "b6a494e", "45575F06C7ED5E24", "FINAL_PROJECT_CLOSEOUT_FINAL_CYCLE_ARCHIVE_CONFIRMED"),
    ("7", "MILESTONE_17_TASK_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_ARCHIVE_REVIEW_V1", "879ad75", "B66AA97FFE0C8BD8", "FINAL_PROJECT_CLOSEOUT_ARCHIVE_REVIEW_CONFIRMED"),
    ("8", "MILESTONE_17_TASK_18_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_ARCHIVE_REVIEW_CLOSURE_V1", "473fdca", "A75818655560BAD7", "FINAL_PROJECT_CLOSEOUT_ARCHIVE_REVIEW_CLOSURE_CONFIRMED"),
    ("9", "MILESTONE_17_TASK_19_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_V1", "9d65af4", "6CEF8B7CAD046107", "FINAL_PROJECT_CLOSEOUT_FINAL_CYCLE_CLOSURE_CONFIRMED"),
    ("10", "MILESTONE_17_TASK_20_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_REVIEW_V1", "8dc2d30", "B804FD3E5DB9E083", "FINAL_PROJECT_CLOSEOUT_FINAL_CYCLE_CLOSURE_REVIEW_CONFIRMED"),
    ("11", "MILESTONE_17_TASK_21_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_REVIEW_CLOSURE_V1", "717c924", "A3E1BE3B64387C85", "FINAL_PROJECT_CLOSEOUT_FINAL_CYCLE_CLOSURE_REVIEW_CLOSURE_CONFIRMED"),
    ("12", "MILESTONE_17_TASK_22_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_V1", "1625a79", "E649BFA06ECAF02A", "FINAL_PROJECT_CLOSEOUT_FINAL_ARCHIVE_INDEX_CONFIRMED"),
    ("13", "MILESTONE_17_TASK_23_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_REVIEW_V1", "9dd6a7f", "A0CB85185EAC8AC5", "FINAL_PROJECT_CLOSEOUT_FINAL_ARCHIVE_INDEX_REVIEW_CONFIRMED"),
    ("14", "MILESTONE_17_TASK_24_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_REVIEW_CLOSURE_V1", "a504ef8", "CE3EDC58EE745A70", "FINAL_PROJECT_CLOSEOUT_FINAL_ARCHIVE_INDEX_REVIEW_CLOSURE_CONFIRMED"),
    ("15", "MILESTONE_17_TASK_25_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CLOSEOUT_V1", "e89d382", "036839E5AF646B0E", "FINAL_PROJECT_CLOSEOUT_FINAL_CLOSEOUT_CONFIRMED"),
    ("16", "MILESTONE_17_TASK_26_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CLOSEOUT_REVIEW_V1", "0853737", "334370C6A210F71C", "FINAL_PROJECT_CLOSEOUT_FINAL_CLOSEOUT_REVIEW_CONFIRMED"),
    ("17", "MILESTONE_17_TASK_27_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CLOSEOUT_REVIEW_CLOSURE_V1", "2ac9df1", "DFC3BE428A8C9461", "FINAL_PROJECT_CLOSEOUT_FINAL_CLOSEOUT_REVIEW_CLOSURE_CONFIRMED"),
    ("18", "MILESTONE_17_TASK_28_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_INDEX_V1", "40fcc44", "5F1EF5CAC20531BE", "FINAL_PROJECT_CLOSEOUT_FINAL_INDEX_CONFIRMED"),
    ("19", "MILESTONE_17_TASK_29_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_INDEX_REVIEW_V1", "12ce723", "2195100C31190A26", "FINAL_PROJECT_CLOSEOUT_FINAL_INDEX_REVIEW_CONFIRMED"),
    ("20", "MILESTONE_17_TASK_30_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_INDEX_REVIEW_CLOSURE_V1", "788ae8b", "545738D85C2208D6", "FINAL_PROJECT_CLOSEOUT_FINAL_INDEX_REVIEW_CLOSURE_CONFIRMED"),
    ("21", "MILESTONE_17_TASK_31_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_SEAL_V1", "0820084", "9CA5D744BEE000D0", "FINAL_PROJECT_CLOSEOUT_FINAL_SEAL_CONFIRMED"),
    ("22", "MILESTONE_17_TASK_32_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_SEAL_REVIEW_V1", "b5dd90b", "9CC51E059F9418E0", "FINAL_PROJECT_CLOSEOUT_FINAL_SEAL_REVIEW_CONFIRMED"),
    ("23", "MILESTONE_17_TASK_33_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_SEAL_REVIEW_CLOSURE_V1", "44fb48b", "A0DA78A5AF2153EE", "FINAL_PROJECT_CLOSEOUT_FINAL_SEAL_REVIEW_CLOSURE_CONFIRMED"),
    ("24", "MILESTONE_17_TASK_34_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_CLOSE_MARK_V1", "d9cdeb3", "8A6102D1AEF35F69", "FINAL_PROJECT_CLOSEOUT_FINAL_CLOSE_MARK_CONFIRMED"),
    ("25", "MILESTONE_17_TASK_35_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_CLOSE_MARK_REVIEW_V1", "e02dd9c", "BF71CDD07B0AF8FD", "FINAL_PROJECT_CLOSEOUT_FINAL_CLOSE_MARK_REVIEW_CONFIRMED"),
    ("26", "MILESTONE_17_TASK_36_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_CLOSE_MARK_REVIEW_CLOSURE_V1", "6ca2fb7", "43FA24D850688BA9", "FINAL_PROJECT_CLOSEOUT_FINAL_CLOSE_MARK_REVIEW_CLOSURE_CONFIRMED"),
    ("27", "MILESTONE_17_TASK_37_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_RELEASE_NOTE_V1", "42d7d19", "D641B35ACCF92D61", "FINAL_PROJECT_CLOSEOUT_FINAL_RELEASE_NOTE_CONFIRMED"),
    ("28", "MILESTONE_17_TASK_38_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_RELEASE_NOTE_REVIEW_V1", "b43345a", "A3FEE095B06869EC", "FINAL_PROJECT_CLOSEOUT_FINAL_RELEASE_NOTE_REVIEW_CONFIRMED"),
    ("29", "MILESTONE_17_TASK_39_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_RELEASE_NOTE_REVIEW_CLOSURE_V1", "4147958", "8D08185FCDF4A33E", "FINAL_PROJECT_CLOSEOUT_FINAL_RELEASE_NOTE_REVIEW_CLOSURE_CONFIRMED"),
    ("30", "MILESTONE_17_TASK_40_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_SUMMARY_V1", "8f8f633", "B5B4C40DE2D0AC8B", "FINAL_PROJECT_CLOSEOUT_FINAL_PROJECT_SUMMARY_CONFIRMED"),
    ("31", "MILESTONE_17_TASK_41_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_SUMMARY_REVIEW_V1", "44cad5b", "C4BFEFA2C3270DE2", "FINAL_PROJECT_CLOSEOUT_FINAL_PROJECT_SUMMARY_REVIEW_CONFIRMED"),
    ("32", "MILESTONE_17_TASK_42_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_SUMMARY_REVIEW_CLOSURE_V1", "9e5881a", "D8DA51222260A7DE", "FINAL_PROJECT_CLOSEOUT_SOURCE_CONFIRMED"),
)


def _build_final_project_closeout_stages() -> tuple[dict[str, Any], ...]:
    stages: list[dict[str, Any]] = []
    for number, task, commit, signature, closeout_status in _STAGE_SOURCE:
        stages.append(
            {
                "stage_id": f"M17-FINAL-PROJECT-CLOSEOUT-STAGE-{number}",
                "task": task,
                "commit": commit,
                "signature": signature,
                "closeout_status": closeout_status,
                "implementation_authorized": False,
                "runtime_execution_allowed": False,
                "submission_allowed": False,
            }
        )
    return tuple(stages)


FINAL_PROJECT_CLOSEOUT_STAGES = _build_final_project_closeout_stages()


FINAL_PROJECT_CLOSEOUT_GATES: tuple[str, ...] = (
    "source_task_42_commit_bound",
    "source_task_42_signature_bound",
    "previous_stage_bound",
    "next_stage_declared",
    "final_project_closeout_scope_confirmed",
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
    "final_project_closeout_stage_count_thirty_two",
    "all_final_project_closeout_stages_recorded",
    "all_final_project_closeout_stages_have_commits",
    "all_final_project_closeout_stages_have_signatures",
    "all_final_project_closeout_stages_no_implementation",
    "all_final_project_closeout_stages_no_runtime_execution",
    "all_final_project_closeout_stages_no_submission",
    "final_project_closeout_ready",
    "final_project_closeout_passed",
    "final_project_closeout_locked",
    "milestone_17_final_project_closeout_ready",
    "controlled_local_solver_improvement_milestone_17_project_closeout_ready",
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


def build_controlled_local_solver_improvement_milestone_17_final_project_closeout() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_42_final_baseline_commit": SOURCE_TASK_42_FINAL_BASELINE_COMMIT,
        "source_task_42_final_signature": SOURCE_TASK_42_FINAL_SIGNATURE,
        "final_project_closeout_scope": FINAL_PROJECT_CLOSEOUT_SCOPE,
        "final_project_closeout_stage_count": len(FINAL_PROJECT_CLOSEOUT_STAGES),
        "verdict": FINAL_PROJECT_CLOSEOUT_VERDICT,
        "decision": FINAL_PROJECT_CLOSEOUT_DECISION,
        "reason": FINAL_PROJECT_CLOSEOUT_REASON,
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
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "final_project_closeout_marker": FINAL_PROJECT_CLOSEOUT_MARKER,
        "signature": signature,
        "source_task_42_final_baseline_commit": SOURCE_TASK_42_FINAL_BASELINE_COMMIT,
        "source_task_42_final_signature": SOURCE_TASK_42_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": FINAL_PROJECT_CLOSEOUT_VERDICT,
        "decision": FINAL_PROJECT_CLOSEOUT_DECISION,
        "final_project_closeout_reason": FINAL_PROJECT_CLOSEOUT_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_project_closeout_scope": FINAL_PROJECT_CLOSEOUT_SCOPE,
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
        "controlled_local_solver_improvement_milestone_17_final_project_closeout_ready": True,
        "controlled_local_solver_improvement_milestone_17_final_project_closeout_passed": True,
        "controlled_local_solver_improvement_milestone_17_final_project_closeout_locked": True,
        "milestone_17_final_project_closeout_ready": True,
        "controlled_local_solver_improvement_milestone_17_project_closeout_ready": True,
        "final_project_closeout_stage_count": len(FINAL_PROJECT_CLOSEOUT_STAGES),
        "final_project_closeout_stages": FINAL_PROJECT_CLOSEOUT_STAGES,
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
        "final_project_closeout_gate_count": len(FINAL_PROJECT_CLOSEOUT_GATES),
        "final_project_closeout_gate_failure_count": 0,
        "final_project_closeout_gates": FINAL_PROJECT_CLOSEOUT_GATES,
        "artifacts": artifacts,
    }


def validate_controlled_local_solver_improvement_milestone_17_final_project_closeout(
    status: dict[str, Any],
) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "final_project_closeout_marker": FINAL_PROJECT_CLOSEOUT_MARKER,
        "source_task_42_final_baseline_commit": SOURCE_TASK_42_FINAL_BASELINE_COMMIT,
        "source_task_42_final_signature": SOURCE_TASK_42_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_project_closeout_scope": FINAL_PROJECT_CLOSEOUT_SCOPE,
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
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "verdict": FINAL_PROJECT_CLOSEOUT_VERDICT,
        "decision": FINAL_PROJECT_CLOSEOUT_DECISION,
        "final_project_closeout_reason": FINAL_PROJECT_CLOSEOUT_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    stages = tuple(status.get("final_project_closeout_stages", ()))
    stage_ids = [stage.get("stage_id") for stage in stages]

    if status.get("final_project_closeout_stage_count") != 32:
        issues.append("final_project_closeout_stage_count must be 32")
    if len(stages) != 32:
        issues.append("final_project_closeout_stages length must be 32")
    if len(stage_ids) != len(set(stage_ids)):
        issues.append("final project closeout stage IDs must be unique")

    for stage in stages:
        if not stage.get("closeout_status"):
            issues.append(f"{stage.get('stage_id')} must have closeout_status")
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
        "controlled_local_solver_improvement_milestone_17_final_project_closeout_ready",
        "controlled_local_solver_improvement_milestone_17_final_project_closeout_passed",
        "controlled_local_solver_improvement_milestone_17_final_project_closeout_locked",
        "milestone_17_final_project_closeout_ready",
        "controlled_local_solver_improvement_milestone_17_project_closeout_ready",
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

    if status.get("final_project_closeout_gate_count") != len(FINAL_PROJECT_CLOSEOUT_GATES):
        issues.append("final_project_closeout_gate_count mismatch")
    if status.get("final_project_closeout_gate_failure_count") != 0:
        issues.append("final_project_closeout_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def final_project_closeout_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["final_project_closeout_marker"],
        "signature": status["signature"],
        "source_task_42_final_baseline_commit": status["source_task_42_final_baseline_commit"],
        "source_task_42_final_signature": status["source_task_42_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "final_project_closeout_scope": status["final_project_closeout_scope"],
        "final_project_closeout_stage_count": status["final_project_closeout_stage_count"],
        "milestone_17_final_project_closeout_ready": status["milestone_17_final_project_closeout_ready"],
        "controlled_local_solver_improvement_milestone_17_project_closeout_ready": status[
            "controlled_local_solver_improvement_milestone_17_project_closeout_ready"
        ],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "official_score_claim_allowed": status["official_score_claim_allowed"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "final_project_closeout_gate_count": status["final_project_closeout_gate_count"],
        "final_project_closeout_gate_failure_count": status["final_project_closeout_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["final_project_closeout_marker"],
        f"signature={status['signature']}",
        f"source_task_42_final_baseline_commit={status['source_task_42_final_baseline_commit']}",
        f"source_task_42_final_signature={status['source_task_42_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"final_project_closeout_reason={status['final_project_closeout_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"final_project_closeout_scope={status['final_project_closeout_scope']}",
        f"final_project_closeout_stage_count={status['final_project_closeout_stage_count']}",
        f"milestone_17_final_project_closeout_ready={status['milestone_17_final_project_closeout_ready']}",
        f"controlled_local_solver_improvement_milestone_17_project_closeout_ready={status['controlled_local_solver_improvement_milestone_17_project_closeout_ready']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"official_score_claim_allowed={status['official_score_claim_allowed']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"final_project_closeout_gate_count={status['final_project_closeout_gate_count']}",
        f"final_project_closeout_gate_failure_count={status['final_project_closeout_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def build_markdown(status: dict[str, Any]) -> str:
    stage_lines = "\n".join(
        f"- `{stage['stage_id']}` — `{stage['task']}` · commit `{stage['commit']}` · `{stage['closeout_status']}`"
        for stage in status["final_project_closeout_stages"]
    )

    return f"""# Milestone #17 Task 43 - Controlled Local Solver Improvement Milestone 17 Final Project Closeout v1

## Status

`{status["final_project_closeout_marker"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 42 final baseline commit: `{status["source_task_42_final_baseline_commit"]}`
- source Task 42 final signature: `{status["source_task_42_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Final project closeout

- final_project_closeout_scope: `{status["final_project_closeout_scope"]}`
- final_project_closeout_stage_count: `{status["final_project_closeout_stage_count"]}`
- milestone_17_final_project_closeout_ready: `{status["milestone_17_final_project_closeout_ready"]}`
- controlled_local_solver_improvement_milestone_17_project_closeout_ready: `{status["controlled_local_solver_improvement_milestone_17_project_closeout_ready"]}`

{stage_lines}

## Closeout statement

Milestone #17 controlled local solver improvement is closed out as local-only, deterministic, public-safe documentation.
The closeout records the full controlled chain from plan through final project summary review closure.
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


def write_controlled_local_solver_improvement_milestone_17_final_project_closeout_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_local_solver_improvement_milestone_17_final_project_closeout()
    issues = validate_controlled_local_solver_improvement_milestone_17_final_project_closeout(resolved)
    if issues:
        raise ValueError(
            "Invalid controlled local solver improvement milestone 17 final project closeout: "
            + "; ".join(issues)
        )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = final_project_closeout_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-closeout-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_local_solver_improvement_milestone_17_final_project_closeout_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_42_final_baseline_commit"])
    print(status["task_mode"])
    print(status["final_project_closeout_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["final_project_closeout_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_42_final_baseline_commit",
        "source_task_42_final_signature",
        "final_project_closeout_scope",
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
        "final_project_closeout_stage_count",
        "milestone_17_final_project_closeout_ready",
        "controlled_local_solver_improvement_milestone_17_project_closeout_ready",
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
        "final_project_closeout_gate_count",
        "final_project_closeout_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for stage in status["final_project_closeout_stages"]:
        print(
            f"final_project_closeout_stage={stage['stage_id']}|{stage['task']}|"
            f"{stage['commit']}|{stage['signature']}|{stage['closeout_status']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
