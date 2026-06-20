"""Milestone #17 Task 59 - Controlled Local Solver Improvement Milestone 17 Final Project Final Audit Review v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_milestone_17_final_project_final_audit as task58


TASK_NAME = "MILESTONE_17_TASK_59_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_AUDIT_REVIEW_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

FINAL_PROJECT_FINAL_AUDIT_REVIEW_MARKER = (
    "MILESTONE_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_PROJECT_FINAL_AUDIT_REVIEW_READY"
)
FINAL_PROJECT_FINAL_AUDIT_REVIEW_VERDICT = (
    "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_AUDIT_REVIEW_PASS_AUDIT_CONFIRMED"
)
FINAL_PROJECT_FINAL_AUDIT_REVIEW_DECISION = (
    "REVIEW_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_AUDIT_NO_IMPLEMENTATION_AUTHORIZED"
)
FINAL_PROJECT_FINAL_AUDIT_REVIEW_REASON = (
    "TASK_58_AUDITED_FINAL_PROJECT_WITHOUT_IMPLEMENTATION_RUNTIME_OR_SUBMISSION"
)

PREVIOUS_STAGE = (
    "MILESTONE_17_TASK_58_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_AUDIT_V1"
)
NEXT_STAGE = (
    "MILESTONE_17_TASK_60_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_AUDIT_REVIEW_CLOSURE_V1"
)

SOURCE_TASK_58_FINAL_BASELINE_COMMIT = "f3a9827"
SOURCE_TASK_58_FINAL_SIGNATURE = "1B121B1B695D1B4F"

FINAL_PROJECT_FINAL_AUDIT_SCOPE = "FINAL_PROJECT_FINAL_AUDIT_ONLY"
FINAL_PROJECT_FINAL_AUDIT_REVIEW_SCOPE = "REVIEW_FINAL_PROJECT_FINAL_AUDIT_ONLY"
FINAL_PROJECT_FINAL_RECORD_SCOPE = "FINAL_PROJECT_FINAL_RECORD_ONLY"
FINAL_PROJECT_FINAL_RECORD_REVIEW_SCOPE = "REVIEW_FINAL_PROJECT_FINAL_RECORD_ONLY"
FINAL_PROJECT_FINAL_RECORD_REVIEW_CLOSURE_SCOPE = "CLOSE_FINAL_PROJECT_FINAL_RECORD_REVIEW_ONLY"
PLAN_AUTHORIZATION_SCOPE = "PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

TASK_MODE = (
    "MILESTONE_17_TASK_59_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_FINAL_PROJECT_FINAL_AUDIT_REVIEW_V1_"
    "REVIEW_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-v1")
DOC_PATH = Path("docs/milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-v1.md")


def _build_reviewed_final_project_final_audit_stages() -> tuple[dict[str, Any], ...]:
    task58_status = task58.build_controlled_local_solver_improvement_milestone_17_final_project_final_audit()
    stages: list[dict[str, Any]] = []

    for stage in task58_status["final_project_final_audit_stages"]:
        number = stage["stage_id"].split("-")[-1]
        stages.append(
            {
                "stage_id": f"M17-FINAL-PROJECT-FINAL-AUDIT-REVIEW-STAGE-{number}",
                "task": stage["task"],
                "commit": stage["commit"],
                "signature": stage["signature"],
                "review_status": f"REVIEWED_{stage['audit_status']}",
                "implementation_authorized": False,
                "runtime_execution_allowed": False,
                "submission_allowed": False,
            }
        )

    stages.append(
        {
            "stage_id": "M17-FINAL-PROJECT-FINAL-AUDIT-REVIEW-STAGE-48",
            "task": PREVIOUS_STAGE,
            "commit": SOURCE_TASK_58_FINAL_BASELINE_COMMIT,
            "signature": SOURCE_TASK_58_FINAL_SIGNATURE,
            "review_status": "FINAL_PROJECT_FINAL_AUDIT_REVIEW_CONFIRMED",
            "implementation_authorized": False,
            "runtime_execution_allowed": False,
            "submission_allowed": False,
        }
    )

    return tuple(stages)


REVIEWED_FINAL_PROJECT_FINAL_AUDIT_STAGES = _build_reviewed_final_project_final_audit_stages()


FINAL_PROJECT_FINAL_AUDIT_REVIEW_GATES: tuple[str, ...] = (
    "source_task_58_commit_bound",
    "source_task_58_signature_bound",
    "previous_stage_bound",
    "next_stage_declared",
    "final_project_final_audit_scope_confirmed",
    "final_project_final_audit_review_scope_confirmed",
    "final_project_final_record_scope_confirmed",
    "final_project_final_record_review_scope_confirmed",
    "final_project_final_record_review_closure_scope_confirmed",
    "plan_authorization_scope_plan_only",
    "implementation_authorization_scope_not_granted",
    "reviewed_final_project_final_audit_stage_count_forty_eight",
    "all_final_project_final_audit_stages_reviewed",
    "all_reviewed_final_project_final_audit_stages_have_commits",
    "all_reviewed_final_project_final_audit_stages_have_signatures",
    "all_reviewed_final_project_final_audit_stages_no_implementation",
    "all_reviewed_final_project_final_audit_stages_no_runtime_execution",
    "all_reviewed_final_project_final_audit_stages_no_submission",
    "final_project_final_audit_review_ready",
    "final_project_final_audit_review_passed",
    "final_project_final_audit_review_locked",
    "milestone_17_final_project_final_audit_reviewed",
    "controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed",
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
    "review_only_no_runtime",
    "review_only_no_submission",
    "review_only_no_score_claim",
    "audit_chain_preserved",
    "source_task_58_final_audit_signature_preserved",
    "final_project_final_audit_review_gate_count_monotonic",
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
    "final_audit_review_boundary_locked",
    "final_project_final_audit_review_source_commit_preserved",
    "final_project_final_audit_review_source_signature_preserved",
    "final_project_final_audit_review_scope_chain_confirmed",
    "final_project_final_audit_review_stage_chain_confirmed",
    "final_project_final_audit_review_gate_count_above_prior_audit",
    "final_audit_review_ready_for_closure",
    "audit_review_traceability_confirmed",
    "audit_review_source_commit_preserved",
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_controlled_local_solver_improvement_milestone_17_final_project_final_audit_review() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_58_final_baseline_commit": SOURCE_TASK_58_FINAL_BASELINE_COMMIT,
        "source_task_58_final_signature": SOURCE_TASK_58_FINAL_SIGNATURE,
        "final_project_final_audit_review_scope": FINAL_PROJECT_FINAL_AUDIT_REVIEW_SCOPE,
        "reviewed_final_project_final_audit_stage_count": len(REVIEWED_FINAL_PROJECT_FINAL_AUDIT_STAGES),
        "verdict": FINAL_PROJECT_FINAL_AUDIT_REVIEW_VERDICT,
        "decision": FINAL_PROJECT_FINAL_AUDIT_REVIEW_DECISION,
        "reason": FINAL_PROJECT_FINAL_AUDIT_REVIEW_REASON,
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
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "final_project_final_audit_review_marker": FINAL_PROJECT_FINAL_AUDIT_REVIEW_MARKER,
        "signature": signature,
        "source_task_58_final_baseline_commit": SOURCE_TASK_58_FINAL_BASELINE_COMMIT,
        "source_task_58_final_signature": SOURCE_TASK_58_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": FINAL_PROJECT_FINAL_AUDIT_REVIEW_VERDICT,
        "decision": FINAL_PROJECT_FINAL_AUDIT_REVIEW_DECISION,
        "final_project_final_audit_review_reason": FINAL_PROJECT_FINAL_AUDIT_REVIEW_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_project_final_audit_scope": FINAL_PROJECT_FINAL_AUDIT_SCOPE,
        "final_project_final_audit_review_scope": FINAL_PROJECT_FINAL_AUDIT_REVIEW_SCOPE,
        "final_project_final_record_scope": FINAL_PROJECT_FINAL_RECORD_SCOPE,
        "final_project_final_record_review_scope": FINAL_PROJECT_FINAL_RECORD_REVIEW_SCOPE,
        "final_project_final_record_review_closure_scope": FINAL_PROJECT_FINAL_RECORD_REVIEW_CLOSURE_SCOPE,
        "plan_authorized": True,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "controlled_local_solver_improvement_milestone_17_final_project_final_audit_review_ready": True,
        "controlled_local_solver_improvement_milestone_17_final_project_final_audit_review_passed": True,
        "controlled_local_solver_improvement_milestone_17_final_project_final_audit_review_locked": True,
        "milestone_17_final_project_final_audit_reviewed": True,
        "controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed": True,
        "reviewed_final_project_final_audit_stage_count": len(REVIEWED_FINAL_PROJECT_FINAL_AUDIT_STAGES),
        "reviewed_final_project_final_audit_stages": REVIEWED_FINAL_PROJECT_FINAL_AUDIT_STAGES,
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
        "final_project_final_audit_review_gate_count": len(FINAL_PROJECT_FINAL_AUDIT_REVIEW_GATES),
        "final_project_final_audit_review_gate_failure_count": 0,
        "final_project_final_audit_review_gates": FINAL_PROJECT_FINAL_AUDIT_REVIEW_GATES,
        "artifacts": artifacts,
    }


def validate_controlled_local_solver_improvement_milestone_17_final_project_final_audit_review(
    status: dict[str, Any],
) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "final_project_final_audit_review_marker": FINAL_PROJECT_FINAL_AUDIT_REVIEW_MARKER,
        "source_task_58_final_baseline_commit": SOURCE_TASK_58_FINAL_BASELINE_COMMIT,
        "source_task_58_final_signature": SOURCE_TASK_58_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_project_final_audit_scope": FINAL_PROJECT_FINAL_AUDIT_SCOPE,
        "final_project_final_audit_review_scope": FINAL_PROJECT_FINAL_AUDIT_REVIEW_SCOPE,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "verdict": FINAL_PROJECT_FINAL_AUDIT_REVIEW_VERDICT,
        "decision": FINAL_PROJECT_FINAL_AUDIT_REVIEW_DECISION,
        "final_project_final_audit_review_reason": FINAL_PROJECT_FINAL_AUDIT_REVIEW_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    stages = tuple(status.get("reviewed_final_project_final_audit_stages", ()))
    stage_ids = [stage.get("stage_id") for stage in stages]

    if status.get("reviewed_final_project_final_audit_stage_count") != 48:
        issues.append("reviewed_final_project_final_audit_stage_count must be 48")
    if len(stages) != 48:
        issues.append("reviewed_final_project_final_audit_stages length must be 48")
    if len(stage_ids) != len(set(stage_ids)):
        issues.append("reviewed final project final audit stage IDs must be unique")

    for stage in stages:
        if not stage.get("review_status"):
            issues.append(f"{stage.get('stage_id')} must have review_status")
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
        "controlled_local_solver_improvement_milestone_17_final_project_final_audit_review_ready",
        "controlled_local_solver_improvement_milestone_17_final_project_final_audit_review_passed",
        "controlled_local_solver_improvement_milestone_17_final_project_final_audit_review_locked",
        "milestone_17_final_project_final_audit_reviewed",
        "controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed",
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

    if status.get("final_project_final_audit_review_gate_count") != len(FINAL_PROJECT_FINAL_AUDIT_REVIEW_GATES):
        issues.append("final_project_final_audit_review_gate_count mismatch")
    if status.get("final_project_final_audit_review_gate_failure_count") != 0:
        issues.append("final_project_final_audit_review_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def final_project_final_audit_review_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["final_project_final_audit_review_marker"],
        "signature": status["signature"],
        "source_task_58_final_baseline_commit": status["source_task_58_final_baseline_commit"],
        "source_task_58_final_signature": status["source_task_58_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "final_project_final_audit_review_scope": status["final_project_final_audit_review_scope"],
        "reviewed_final_project_final_audit_stage_count": status["reviewed_final_project_final_audit_stage_count"],
        "milestone_17_final_project_final_audit_reviewed": status["milestone_17_final_project_final_audit_reviewed"],
        "controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed": status[
            "controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed"
        ],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "official_score_claim_allowed": status["official_score_claim_allowed"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "final_project_final_audit_review_gate_count": status["final_project_final_audit_review_gate_count"],
        "final_project_final_audit_review_gate_failure_count": status["final_project_final_audit_review_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["final_project_final_audit_review_marker"],
        f"signature={status['signature']}",
        f"source_task_58_final_baseline_commit={status['source_task_58_final_baseline_commit']}",
        f"source_task_58_final_signature={status['source_task_58_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"final_project_final_audit_review_reason={status['final_project_final_audit_review_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"final_project_final_audit_review_scope={status['final_project_final_audit_review_scope']}",
        f"reviewed_final_project_final_audit_stage_count={status['reviewed_final_project_final_audit_stage_count']}",
        f"milestone_17_final_project_final_audit_reviewed={status['milestone_17_final_project_final_audit_reviewed']}",
        f"controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed={status['controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"official_score_claim_allowed={status['official_score_claim_allowed']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"final_project_final_audit_review_gate_count={status['final_project_final_audit_review_gate_count']}",
        f"final_project_final_audit_review_gate_failure_count={status['final_project_final_audit_review_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def build_markdown(status: dict[str, Any]) -> str:
    stage_lines = "\n".join(
        f"- `{stage['stage_id']}` - `{stage['task']}` · commit `{stage['commit']}` · `{stage['review_status']}`"
        for stage in status["reviewed_final_project_final_audit_stages"]
    )

    return f"""# Milestone #17 Task 59 - Controlled Local Solver Improvement Milestone 17 Final Project Final Audit Review v1

## Status

`{status["final_project_final_audit_review_marker"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 58 final baseline commit: `{status["source_task_58_final_baseline_commit"]}`
- source Task 58 final signature: `{status["source_task_58_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Final project final audit review

- final_project_final_audit_scope: `{status["final_project_final_audit_scope"]}`
- final_project_final_audit_review_scope: `{status["final_project_final_audit_review_scope"]}`
- reviewed_final_project_final_audit_stage_count: `{status["reviewed_final_project_final_audit_stage_count"]}`
- milestone_17_final_project_final_audit_reviewed: `{status["milestone_17_final_project_final_audit_reviewed"]}`
- controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed: `{status["controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed"]}`

{stage_lines}

## Review statement

The Milestone #17 controlled local solver improvement final project final audit is reviewed as local-only, deterministic, public-safe documentation.
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


def write_controlled_local_solver_improvement_milestone_17_final_project_final_audit_review_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_local_solver_improvement_milestone_17_final_project_final_audit_review()
    issues = validate_controlled_local_solver_improvement_milestone_17_final_project_final_audit_review(resolved)
    if issues:
        raise ValueError(
            "Invalid controlled local solver improvement milestone 17 final project final audit review: "
            + "; ".join(issues)
        )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = final_project_final_audit_review_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-audit-review-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_local_solver_improvement_milestone_17_final_project_final_audit_review_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_58_final_baseline_commit"])
    print(status["task_mode"])
    print(status["final_project_final_audit_review_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["final_project_final_audit_review_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_58_final_baseline_commit",
        "source_task_58_final_signature",
        "final_project_final_audit_scope",
        "final_project_final_audit_review_scope",
        "final_project_final_record_scope",
        "final_project_final_record_review_scope",
        "final_project_final_record_review_closure_scope",
        "reviewed_final_project_final_audit_stage_count",
        "milestone_17_final_project_final_audit_reviewed",
        "controlled_local_solver_improvement_milestone_17_project_final_audit_reviewed",
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
        "final_project_final_audit_review_gate_count",
        "final_project_final_audit_review_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for stage in status["reviewed_final_project_final_audit_stages"]:
        print(
            f"reviewed_final_project_final_audit_stage={stage['stage_id']}|{stage['task']}|"
            f"{stage['commit']}|{stage['signature']}|{stage['review_status']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
