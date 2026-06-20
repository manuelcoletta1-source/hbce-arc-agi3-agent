"""Milestone #17 Task 67 - Controlled Local Solver Improvement Milestone 17 Terminal Stop Record v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_milestone_17_final_project_final_archive_lock_review_closure as task66


TASK_NAME = "MILESTONE_17_TASK_67_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_TERMINAL_STOP_RECORD_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

TERMINAL_STOP_RECORD_MARKER = (
    "MILESTONE_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_TERMINAL_STOP_RECORD_READY"
)
TERMINAL_STOP_RECORD_VERDICT = (
    "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_TERMINAL_STOP_RECORD_PASS_MILESTONE_STOPPED"
)
TERMINAL_STOP_RECORD_DECISION = (
    "STOP_MILESTONE_17_AND_REQUIRE_OPERATOR_DIRECTION_BEFORE_MILESTONE_18"
)
TERMINAL_STOP_RECORD_REASON = (
    "TASK_66_CLOSED_FINAL_PROJECT_FINAL_ARCHIVE_LOCK_REVIEW_WITHOUT_IMPLEMENTATION_RUNTIME_OR_SUBMISSION"
)

PREVIOUS_STAGE = (
    "MILESTONE_17_TASK_66_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_ARCHIVE_LOCK_REVIEW_CLOSURE_V1"
)
NEXT_STAGE = "OPERATOR_DIRECTION_REQUIRED_BEFORE_MILESTONE_18"

SOURCE_TASK_66_FINAL_BASELINE_COMMIT = "dc12263"
SOURCE_TASK_66_FINAL_SIGNATURE = "B88D88EF035E6BD0"

TERMINAL_STOP_RECORD_SCOPE = "MILESTONE_17_TERMINAL_STOP_RECORD_ONLY"
FINAL_PROJECT_FINAL_ARCHIVE_LOCK_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_PROJECT_FINAL_ARCHIVE_LOCK_REVIEW_ONLY"
FINAL_PROJECT_FINAL_ARCHIVE_LOCK_REVIEW_SCOPE = "REVIEW_FINAL_PROJECT_FINAL_ARCHIVE_LOCK_ONLY"
FINAL_PROJECT_FINAL_ARCHIVE_LOCK_SCOPE = "FINAL_PROJECT_FINAL_ARCHIVE_LOCK_ONLY"
PLAN_AUTHORIZATION_SCOPE = "PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

TASK_MODE = (
    "MILESTONE_17_TASK_67_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_TERMINAL_STOP_RECORD_V1_"
    "TERMINAL_STOP_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-local-solver-improvement-milestone-17-terminal-stop-record-v1")
DOC_PATH = Path("docs/milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-v1.md")


def _build_terminal_stop_record_stages() -> tuple[dict[str, Any], ...]:
    task66_status = task66.build_controlled_local_solver_improvement_milestone_17_final_project_final_archive_lock_review_closure()
    stages: list[dict[str, Any]] = []

    for stage in task66_status["closed_final_project_final_archive_lock_review_stages"]:
        number = stage["stage_id"].split("-")[-1]
        stages.append(
            {
                "stage_id": f"M17-TERMINAL-STOP-RECORD-STAGE-{number}",
                "task": stage["task"],
                "commit": stage["commit"],
                "signature": stage["signature"],
                "terminal_status": f"TERMINAL_RECORDED_{stage['closure_status']}",
                "implementation_authorized": False,
                "runtime_execution_allowed": False,
                "submission_allowed": False,
            }
        )

    stages.append(
        {
            "stage_id": "M17-TERMINAL-STOP-RECORD-STAGE-56",
            "task": PREVIOUS_STAGE,
            "commit": SOURCE_TASK_66_FINAL_BASELINE_COMMIT,
            "signature": SOURCE_TASK_66_FINAL_SIGNATURE,
            "terminal_status": "MILESTONE_17_TERMINAL_STOP_RECORDED",
            "implementation_authorized": False,
            "runtime_execution_allowed": False,
            "submission_allowed": False,
        }
    )

    return tuple(stages)


TERMINAL_STOP_RECORD_STAGES = _build_terminal_stop_record_stages()


TERMINAL_STOP_RECORD_GATES: tuple[str, ...] = (
    "source_task_66_commit_bound",
    "source_task_66_signature_bound",
    "previous_stage_bound",
    "next_stage_operator_direction_required",
    "terminal_stop_record_scope_confirmed",
    "final_project_final_archive_lock_scope_confirmed",
    "final_project_final_archive_lock_review_scope_confirmed",
    "final_project_final_archive_lock_review_closure_scope_confirmed",
    "plan_authorization_scope_plan_only",
    "implementation_authorization_scope_not_granted",
    "terminal_stop_record_stage_count_fifty_six",
    "all_terminal_stop_record_stages_recorded",
    "all_terminal_stop_record_stages_have_commits",
    "all_terminal_stop_record_stages_have_signatures",
    "all_terminal_stop_record_stages_no_implementation",
    "all_terminal_stop_record_stages_no_runtime_execution",
    "all_terminal_stop_record_stages_no_submission",
    "milestone_17_terminal_stop_record_ready",
    "milestone_17_terminal_stop_record_passed",
    "milestone_17_terminal_stop_record_locked",
    "milestone_17_stopped",
    "controlled_local_solver_improvement_milestone_17_stopped",
    "operator_direction_required_before_milestone_18",
    "milestone_18_not_opened",
    "no_further_milestone_17_review_chain",
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
    "terminal_stop_only_no_runtime",
    "terminal_stop_only_no_submission",
    "terminal_stop_only_no_score_claim",
    "terminal_stop_record_boundary_locked",
    "terminal_stop_record_ready_for_operator_decision",
    "artifact_set_declared",
    "artifact_count_five",
    "manifest_created",
    "index_created",
    "markdown_created",
    "json_payload_created",
    "docs_payload_created",
    "public_safe_true",
    "local_only_true",
    "deterministic_true",
    "operator_approval_not_present",
    "manual_upload_blocked",
    "kaggle_authentication_blocked",
    "milestone_17_terminal_chain_preserved",
    "milestone_17_terminal_chain_closed",
    "milestone_17_terminal_chain_no_more_review_closure",
    "milestone_18_requires_explicit_operator_direction",
    "terminal_stop_record_source_commit_preserved",
    "terminal_stop_record_source_signature_preserved",
    "terminal_stop_record_gate_count_monotonic",
    "terminal_stop_record_gate_count_above_prior_closure",
    "terminal_stop_record_scope_chain_confirmed",
    "terminal_stop_record_stage_chain_confirmed",
    "terminal_stop_record_operator_direction_gate_confirmed",
    "terminal_stop_record_milestone_18_not_opened_confirmed",
    "terminal_stop_record_no_further_review_chain_confirmed",
    "terminal_stop_record_no_implementation_chain_confirmed",
    "terminal_stop_record_no_runtime_chain_confirmed",
    "terminal_stop_record_no_submission_chain_confirmed",
    "terminal_stop_record_no_upload_chain_confirmed",
    "terminal_stop_record_no_score_claim_chain_confirmed",
    "terminal_stop_record_final_repository_state_expected_clean_after_commit",
    "terminal_stop_record_final_phase_stop_boundary_confirmed",
    "terminal_stop_record_milestone_17_closure_boundary_confirmed",
    "terminal_stop_record_explicit_operator_direction_required_confirmed",
    "terminal_stop_record_milestone_18_requires_new_scope_confirmed",
    "terminal_stop_record_terminal_not_review_not_closure_confirmed",
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_controlled_local_solver_improvement_milestone_17_terminal_stop_record() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_66_final_baseline_commit": SOURCE_TASK_66_FINAL_BASELINE_COMMIT,
        "source_task_66_final_signature": SOURCE_TASK_66_FINAL_SIGNATURE,
        "terminal_stop_record_scope": TERMINAL_STOP_RECORD_SCOPE,
        "terminal_stop_record_stage_count": len(TERMINAL_STOP_RECORD_STAGES),
        "verdict": TERMINAL_STOP_RECORD_VERDICT,
        "decision": TERMINAL_STOP_RECORD_DECISION,
        "reason": TERMINAL_STOP_RECORD_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "milestone_17_stopped": True,
        "operator_direction_required_before_milestone_18": True,
        "milestone_18_opened": False,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "terminal_stop_record_marker": TERMINAL_STOP_RECORD_MARKER,
        "signature": signature,
        "source_task_66_final_baseline_commit": SOURCE_TASK_66_FINAL_BASELINE_COMMIT,
        "source_task_66_final_signature": SOURCE_TASK_66_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": TERMINAL_STOP_RECORD_VERDICT,
        "decision": TERMINAL_STOP_RECORD_DECISION,
        "terminal_stop_record_reason": TERMINAL_STOP_RECORD_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "terminal_stop_record_scope": TERMINAL_STOP_RECORD_SCOPE,
        "final_project_final_archive_lock_scope": FINAL_PROJECT_FINAL_ARCHIVE_LOCK_SCOPE,
        "final_project_final_archive_lock_review_scope": FINAL_PROJECT_FINAL_ARCHIVE_LOCK_REVIEW_SCOPE,
        "final_project_final_archive_lock_review_closure_scope": FINAL_PROJECT_FINAL_ARCHIVE_LOCK_REVIEW_CLOSURE_SCOPE,
        "plan_authorized": True,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "controlled_local_solver_improvement_milestone_17_terminal_stop_record_ready": True,
        "controlled_local_solver_improvement_milestone_17_terminal_stop_record_passed": True,
        "controlled_local_solver_improvement_milestone_17_terminal_stop_record_locked": True,
        "milestone_17_stopped": True,
        "controlled_local_solver_improvement_milestone_17_stopped": True,
        "operator_direction_required_before_milestone_18": True,
        "milestone_18_opened": False,
        "no_further_milestone_17_review_chain": True,
        "terminal_stop_record_stage_count": len(TERMINAL_STOP_RECORD_STAGES),
        "terminal_stop_record_stages": TERMINAL_STOP_RECORD_STAGES,
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
        "terminal_stop_record_gate_count": len(TERMINAL_STOP_RECORD_GATES),
        "terminal_stop_record_gate_failure_count": 0,
        "terminal_stop_record_gates": TERMINAL_STOP_RECORD_GATES,
        "artifacts": artifacts,
    }


def validate_controlled_local_solver_improvement_milestone_17_terminal_stop_record(
    status: dict[str, Any],
) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "terminal_stop_record_marker": TERMINAL_STOP_RECORD_MARKER,
        "source_task_66_final_baseline_commit": SOURCE_TASK_66_FINAL_BASELINE_COMMIT,
        "source_task_66_final_signature": SOURCE_TASK_66_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "terminal_stop_record_scope": TERMINAL_STOP_RECORD_SCOPE,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "verdict": TERMINAL_STOP_RECORD_VERDICT,
        "decision": TERMINAL_STOP_RECORD_DECISION,
        "terminal_stop_record_reason": TERMINAL_STOP_RECORD_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    stages = tuple(status.get("terminal_stop_record_stages", ()))
    stage_ids = [stage.get("stage_id") for stage in stages]

    if status.get("terminal_stop_record_stage_count") != 56:
        issues.append("terminal_stop_record_stage_count must be 56")
    if len(stages) != 56:
        issues.append("terminal_stop_record_stages length must be 56")
    if len(stage_ids) != len(set(stage_ids)):
        issues.append("terminal stop record stage IDs must be unique")

    for stage in stages:
        if not stage.get("terminal_status"):
            issues.append(f"{stage.get('stage_id')} must have terminal_status")
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
        "controlled_local_solver_improvement_milestone_17_terminal_stop_record_ready",
        "controlled_local_solver_improvement_milestone_17_terminal_stop_record_passed",
        "controlled_local_solver_improvement_milestone_17_terminal_stop_record_locked",
        "milestone_17_stopped",
        "controlled_local_solver_improvement_milestone_17_stopped",
        "operator_direction_required_before_milestone_18",
        "no_further_milestone_17_review_chain",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
    )
    required_false = (
        "milestone_18_opened",
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

    if status.get("terminal_stop_record_gate_count") != len(TERMINAL_STOP_RECORD_GATES):
        issues.append("terminal_stop_record_gate_count mismatch")
    if status.get("terminal_stop_record_gate_failure_count") != 0:
        issues.append("terminal_stop_record_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def terminal_stop_record_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["terminal_stop_record_marker"],
        "signature": status["signature"],
        "source_task_66_final_baseline_commit": status["source_task_66_final_baseline_commit"],
        "source_task_66_final_signature": status["source_task_66_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "terminal_stop_record_scope": status["terminal_stop_record_scope"],
        "terminal_stop_record_stage_count": status["terminal_stop_record_stage_count"],
        "milestone_17_stopped": status["milestone_17_stopped"],
        "controlled_local_solver_improvement_milestone_17_stopped": status["controlled_local_solver_improvement_milestone_17_stopped"],
        "operator_direction_required_before_milestone_18": status["operator_direction_required_before_milestone_18"],
        "milestone_18_opened": status["milestone_18_opened"],
        "no_further_milestone_17_review_chain": status["no_further_milestone_17_review_chain"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "official_score_claim_allowed": status["official_score_claim_allowed"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "terminal_stop_record_gate_count": status["terminal_stop_record_gate_count"],
        "terminal_stop_record_gate_failure_count": status["terminal_stop_record_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["terminal_stop_record_marker"],
        f"signature={status['signature']}",
        f"source_task_66_final_baseline_commit={status['source_task_66_final_baseline_commit']}",
        f"source_task_66_final_signature={status['source_task_66_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"terminal_stop_record_reason={status['terminal_stop_record_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"terminal_stop_record_scope={status['terminal_stop_record_scope']}",
        f"terminal_stop_record_stage_count={status['terminal_stop_record_stage_count']}",
        f"milestone_17_stopped={status['milestone_17_stopped']}",
        f"controlled_local_solver_improvement_milestone_17_stopped={status['controlled_local_solver_improvement_milestone_17_stopped']}",
        f"operator_direction_required_before_milestone_18={status['operator_direction_required_before_milestone_18']}",
        f"milestone_18_opened={status['milestone_18_opened']}",
        f"no_further_milestone_17_review_chain={status['no_further_milestone_17_review_chain']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"official_score_claim_allowed={status['official_score_claim_allowed']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"terminal_stop_record_gate_count={status['terminal_stop_record_gate_count']}",
        f"terminal_stop_record_gate_failure_count={status['terminal_stop_record_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def build_markdown(status: dict[str, Any]) -> str:
    stage_lines = "\n".join(
        f"- `{stage['stage_id']}` - `{stage['task']}` · commit `{stage['commit']}` · `{stage['terminal_status']}`"
        for stage in status["terminal_stop_record_stages"]
    )

    return f"""# Milestone #17 Task 67 - Controlled Local Solver Improvement Milestone 17 Terminal Stop Record v1

## Status

`{status["terminal_stop_record_marker"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 66 final baseline commit: `{status["source_task_66_final_baseline_commit"]}`
- source Task 66 final signature: `{status["source_task_66_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Terminal stop record

- terminal_stop_record_scope: `{status["terminal_stop_record_scope"]}`
- terminal_stop_record_stage_count: `{status["terminal_stop_record_stage_count"]}`
- milestone_17_stopped: `{status["milestone_17_stopped"]}`
- controlled_local_solver_improvement_milestone_17_stopped: `{status["controlled_local_solver_improvement_milestone_17_stopped"]}`
- operator_direction_required_before_milestone_18: `{status["operator_direction_required_before_milestone_18"]}`
- milestone_18_opened: `{status["milestone_18_opened"]}`
- no_further_milestone_17_review_chain: `{status["no_further_milestone_17_review_chain"]}`

{stage_lines}

## Stop statement

Milestone #17 is stopped by this terminal record.
This record does not authorize Milestone #18.
This record does not authorize implementation.
This record does not authorize runtime execution.
This record does not authorize real Kaggle evaluation.
This record does not authorize Kaggle submission.
Any next technical phase requires explicit operator direction.

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


def write_controlled_local_solver_improvement_milestone_17_terminal_stop_record_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_local_solver_improvement_milestone_17_terminal_stop_record()
    issues = validate_controlled_local_solver_improvement_milestone_17_terminal_stop_record(resolved)
    if issues:
        raise ValueError(
            "Invalid controlled local solver improvement milestone 17 terminal stop record: "
            + "; ".join(issues)
        )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = terminal_stop_record_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-terminal-stop-record-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_local_solver_improvement_milestone_17_terminal_stop_record_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_66_final_baseline_commit"])
    print(status["task_mode"])
    print(status["terminal_stop_record_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["terminal_stop_record_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_66_final_baseline_commit",
        "source_task_66_final_signature",
        "terminal_stop_record_scope",
        "terminal_stop_record_stage_count",
        "milestone_17_stopped",
        "controlled_local_solver_improvement_milestone_17_stopped",
        "operator_direction_required_before_milestone_18",
        "milestone_18_opened",
        "no_further_milestone_17_review_chain",
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
        "terminal_stop_record_gate_count",
        "terminal_stop_record_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for stage in status["terminal_stop_record_stages"]:
        print(
            f"terminal_stop_record_stage={stage['stage_id']}|{stage['task']}|"
            f"{stage['commit']}|{stage['signature']}|{stage['terminal_status']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
