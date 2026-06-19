"""Milestone #16 Task 9 - Operator Direction Cycle Status Review v1.

This module reviews the Task 8 operator-direction cycle status and confirms
that the cycle remains blocked pending explicit operator direction.

Boundary:
- review-only
- local-only
- deterministic
- public-safe
- no implementation
- no runtime activation
- no real evaluation
- no Kaggle submission
- no private core exposure
- no legal certification
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_16_TASK_9_OPERATOR_DIRECTION_CYCLE_STATUS_REVIEW_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

REVIEW_STATUS_MARKER = "MILESTONE_16_OPERATOR_DIRECTION_CYCLE_STATUS_REVIEW_READY"
REVIEW_VERDICT = "OPERATOR_DIRECTION_CYCLE_STATUS_REVIEW_PASS_CYCLE_BLOCK_CONFIRMED"
REVIEW_DECISION = "CONFIRM_CYCLE_STATUS_BLOCKED_PENDING_EXPLICIT_OPERATOR_DIRECTION"
REVIEW_REASON = "TASK_8_CYCLE_STATUS_CONFIRMED_WAIT_STATE_ACTIVE_DECISION_GATE_BLOCKED"

PREVIOUS_STAGE = "MILESTONE_16_TASK_8_OPERATOR_DIRECTION_CYCLE_STATUS_V1"
NEXT_STAGE = "MILESTONE_16_TASK_10_OPERATOR_DIRECTION_FINAL_WAIT_STATE_AUDIT_V1"

SOURCE_TASK_8_FINAL_BASELINE_COMMIT = "224999c"
SOURCE_TASK_8_FINAL_SIGNATURE = "EEE53EAAFCE839F9"

TASK_MODE = "MILESTONE_16_TASK_9_OPERATOR_DIRECTION_CYCLE_STATUS_REVIEW_V1_REVIEW_ONLY_LOCAL_ONLY"

ARTIFACT_DIR = Path("examples/milestone-16/operator-direction-cycle-status-review-v1")
DOC_PATH = Path("docs/milestone-16-operator-direction-cycle-status-review-v1.md")


BOUNDARY_FLAGS: dict[str, bool] = {
    "public_safe": True,
    "deterministic": True,
    "local_only": True,
    "status_only": False,
    "review_only": True,
    "dry_run_only": True,
    "external_api_dependency": False,
    "contains_api_keys": False,
    "cycle_status_ready": True,
    "cycle_status_passed": True,
    "cycle_status_closed": True,
    "cycle_status_review_ready": True,
    "cycle_status_review_passed": True,
    "cycle_status_review_closed": True,
    "wait_state_closure_closed": True,
    "wait_state_review_closed": True,
    "wait_state_ready": True,
    "wait_state_active": True,
    "wait_state_closed": False,
    "decision_gate_ready": True,
    "decision_gate_open": False,
    "decision_gate_blocked": True,
    "operator_direction_required": True,
    "operator_direction_received": False,
    "operator_decision_required": True,
    "operator_decision_received": False,
    "explicit_operator_authorization_required": True,
    "explicit_operator_authorization_received": False,
    "implementation_authorization_granted": False,
    "implementation_authorized": False,
    "implementation_blocked": True,
    "implementation_performed": False,
    "implementation_patch_created": False,
    "implementation_patch_applied": False,
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
    "private_core_exposure": False,
    "legal_certification": False,
    "fail_closed_required": True,
    "fail_closed_active": True,
}


REVIEW_CHECKS: tuple[str, ...] = (
    "task_8_source_commit_bound",
    "task_8_source_signature_bound",
    "cycle_status_ready_confirmed",
    "cycle_status_closed_confirmed",
    "wait_state_active_confirmed",
    "wait_state_not_closed_confirmed",
    "decision_gate_blocked_confirmed",
    "operator_direction_missing_confirmed",
    "operator_authorization_missing_confirmed",
    "implementation_blocked_confirmed",
    "runtime_solver_patch_blocked_confirmed",
    "runtime_wiring_blocked_confirmed",
    "runtime_activation_blocked_confirmed",
    "runtime_execution_blocked_confirmed",
    "real_evaluation_blocked_confirmed",
    "real_submission_blocked_confirmed",
    "kaggle_submission_not_sent_confirmed",
    "private_core_not_exposed_confirmed",
    "legal_certification_false_confirmed",
    "fail_closed_active_confirmed",
)


@dataclass(frozen=True)
class OperatorDirectionCycleStatusReview:
    """Canonical review payload for Milestone #16 Task 9."""

    task_name: str
    task_ready_marker: str
    task_valid_marker: str
    pipeline_ready_marker: str
    review_status_marker: str
    signature: str
    source_task_8_final_baseline_commit: str
    source_task_8_final_signature: str
    task_mode: str
    verdict: str
    decision: str
    review_reason: str
    previous_stage: str
    next_stage: str

    cycle_status_ready: bool
    cycle_status_passed: bool
    cycle_status_closed: bool
    cycle_status_review_ready: bool
    cycle_status_review_passed: bool
    cycle_status_review_closed: bool
    wait_state_closure_closed: bool
    wait_state_review_closed: bool
    wait_state_ready: bool
    wait_state_active: bool
    wait_state_closed: bool
    decision_gate_ready: bool
    decision_gate_open: bool
    decision_gate_blocked: bool

    direction_option_count: int
    direction_option_selected: bool
    selected_direction_option_id: str
    selected_direction_option_count: int
    operator_direction_required: bool
    operator_direction_received: bool
    operator_direction_value: str
    operator_decision_required: bool
    operator_decision_received: bool
    explicit_operator_authorization_required: bool
    explicit_operator_authorization_received: bool

    implementation_authorization_granted: bool
    implementation_authorized: bool
    implementation_blocked: bool
    implementation_performed: bool
    implementation_patch_created: bool
    implementation_patch_applied: bool
    runtime_solver_patch_allowed: bool
    runtime_solver_modified: bool
    ranker_runtime_patch_allowed: bool
    ranker_runtime_modified: bool
    candidate_generator_patch_allowed: bool
    candidate_generator_modified: bool
    runtime_wiring_allowed: bool
    runtime_wiring_performed: bool
    runtime_activation_authorized: bool
    runtime_activation_performed: bool
    runtime_execution_allowed: bool
    runtime_execution_performed: bool
    real_evaluation_allowed: bool
    real_submission_allowed: bool
    kaggle_submission_sent: bool
    private_core_exposure: bool
    legal_certification: bool
    fail_closed_required: bool
    fail_closed_active: bool

    review_check_count: int
    review_failure_count: int
    review_checks: tuple[str, ...]
    artifacts: tuple[str, ...]


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_cycle_status_review() -> OperatorDirectionCycleStatusReview:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_8_final_baseline_commit": SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        "source_task_8_final_signature": SOURCE_TASK_8_FINAL_SIGNATURE,
        "verdict": REVIEW_VERDICT,
        "decision": REVIEW_DECISION,
        "review_reason": REVIEW_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "direction_option_count": 5,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "real_submission_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-review-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-review-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-review-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-review-v1.md"),
        str(DOC_PATH),
    )

    return OperatorDirectionCycleStatusReview(
        task_name=TASK_NAME,
        task_ready_marker=TASK_READY_MARKER,
        task_valid_marker=TASK_VALID_MARKER,
        pipeline_ready_marker=PIPELINE_READY_MARKER,
        review_status_marker=REVIEW_STATUS_MARKER,
        signature=signature,
        source_task_8_final_baseline_commit=SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        source_task_8_final_signature=SOURCE_TASK_8_FINAL_SIGNATURE,
        task_mode=TASK_MODE,
        verdict=REVIEW_VERDICT,
        decision=REVIEW_DECISION,
        review_reason=REVIEW_REASON,
        previous_stage=PREVIOUS_STAGE,
        next_stage=NEXT_STAGE,
        cycle_status_ready=True,
        cycle_status_passed=True,
        cycle_status_closed=True,
        cycle_status_review_ready=True,
        cycle_status_review_passed=True,
        cycle_status_review_closed=True,
        wait_state_closure_closed=True,
        wait_state_review_closed=True,
        wait_state_ready=True,
        wait_state_active=True,
        wait_state_closed=False,
        decision_gate_ready=True,
        decision_gate_open=False,
        decision_gate_blocked=True,
        direction_option_count=5,
        direction_option_selected=False,
        selected_direction_option_id="NONE",
        selected_direction_option_count=0,
        operator_direction_required=True,
        operator_direction_received=False,
        operator_direction_value="PENDING_EXPLICIT_OPERATOR_DIRECTION",
        operator_decision_required=True,
        operator_decision_received=False,
        explicit_operator_authorization_required=True,
        explicit_operator_authorization_received=False,
        implementation_authorization_granted=False,
        implementation_authorized=False,
        implementation_blocked=True,
        implementation_performed=False,
        implementation_patch_created=False,
        implementation_patch_applied=False,
        runtime_solver_patch_allowed=False,
        runtime_solver_modified=False,
        ranker_runtime_patch_allowed=False,
        ranker_runtime_modified=False,
        candidate_generator_patch_allowed=False,
        candidate_generator_modified=False,
        runtime_wiring_allowed=False,
        runtime_wiring_performed=False,
        runtime_activation_authorized=False,
        runtime_activation_performed=False,
        runtime_execution_allowed=False,
        runtime_execution_performed=False,
        real_evaluation_allowed=False,
        real_submission_allowed=False,
        kaggle_submission_sent=False,
        private_core_exposure=False,
        legal_certification=False,
        fail_closed_required=True,
        fail_closed_active=True,
        review_check_count=len(REVIEW_CHECKS),
        review_failure_count=0,
        review_checks=REVIEW_CHECKS,
        artifacts=artifacts,
    )


def validate_cycle_status_review(status: OperatorDirectionCycleStatusReview) -> list[str]:
    issues: list[str] = []

    if status.task_name != TASK_NAME:
        issues.append("task_name mismatch")
    if status.task_ready_marker != TASK_READY_MARKER:
        issues.append("task_ready_marker mismatch")
    if status.task_valid_marker != TASK_VALID_MARKER:
        issues.append("task_valid_marker mismatch")
    if status.pipeline_ready_marker != PIPELINE_READY_MARKER:
        issues.append("pipeline_ready_marker mismatch")
    if status.review_status_marker != REVIEW_STATUS_MARKER:
        issues.append("review_status_marker mismatch")
    if status.source_task_8_final_baseline_commit != SOURCE_TASK_8_FINAL_BASELINE_COMMIT:
        issues.append("source_task_8_final_baseline_commit mismatch")
    if status.source_task_8_final_signature != SOURCE_TASK_8_FINAL_SIGNATURE:
        issues.append("source_task_8_final_signature mismatch")
    if status.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage mismatch")
    if status.next_stage != NEXT_STAGE:
        issues.append("next_stage mismatch")
    if status.verdict != REVIEW_VERDICT:
        issues.append("verdict mismatch")
    if status.decision != REVIEW_DECISION:
        issues.append("decision mismatch")
    if status.review_reason != REVIEW_REASON:
        issues.append("review_reason mismatch")

    required_true = {
        "cycle_status_ready": status.cycle_status_ready,
        "cycle_status_passed": status.cycle_status_passed,
        "cycle_status_closed": status.cycle_status_closed,
        "cycle_status_review_ready": status.cycle_status_review_ready,
        "cycle_status_review_passed": status.cycle_status_review_passed,
        "cycle_status_review_closed": status.cycle_status_review_closed,
        "wait_state_closure_closed": status.wait_state_closure_closed,
        "wait_state_review_closed": status.wait_state_review_closed,
        "wait_state_ready": status.wait_state_ready,
        "wait_state_active": status.wait_state_active,
        "decision_gate_ready": status.decision_gate_ready,
        "decision_gate_blocked": status.decision_gate_blocked,
        "operator_direction_required": status.operator_direction_required,
        "operator_decision_required": status.operator_decision_required,
        "explicit_operator_authorization_required": status.explicit_operator_authorization_required,
        "implementation_blocked": status.implementation_blocked,
        "fail_closed_required": status.fail_closed_required,
        "fail_closed_active": status.fail_closed_active,
    }

    required_false = {
        "wait_state_closed": status.wait_state_closed,
        "decision_gate_open": status.decision_gate_open,
        "direction_option_selected": status.direction_option_selected,
        "operator_direction_received": status.operator_direction_received,
        "operator_decision_received": status.operator_decision_received,
        "explicit_operator_authorization_received": status.explicit_operator_authorization_received,
        "implementation_authorization_granted": status.implementation_authorization_granted,
        "implementation_authorized": status.implementation_authorized,
        "implementation_performed": status.implementation_performed,
        "implementation_patch_created": status.implementation_patch_created,
        "implementation_patch_applied": status.implementation_patch_applied,
        "runtime_solver_patch_allowed": status.runtime_solver_patch_allowed,
        "runtime_solver_modified": status.runtime_solver_modified,
        "ranker_runtime_patch_allowed": status.ranker_runtime_patch_allowed,
        "ranker_runtime_modified": status.ranker_runtime_modified,
        "candidate_generator_patch_allowed": status.candidate_generator_patch_allowed,
        "candidate_generator_modified": status.candidate_generator_modified,
        "runtime_wiring_allowed": status.runtime_wiring_allowed,
        "runtime_wiring_performed": status.runtime_wiring_performed,
        "runtime_activation_authorized": status.runtime_activation_authorized,
        "runtime_activation_performed": status.runtime_activation_performed,
        "runtime_execution_allowed": status.runtime_execution_allowed,
        "runtime_execution_performed": status.runtime_execution_performed,
        "real_evaluation_allowed": status.real_evaluation_allowed,
        "real_submission_allowed": status.real_submission_allowed,
        "kaggle_submission_sent": status.kaggle_submission_sent,
        "private_core_exposure": status.private_core_exposure,
        "legal_certification": status.legal_certification,
    }

    for name, value in required_true.items():
        if value is not True:
            issues.append(f"{name} must be True")

    for name, value in required_false.items():
        if value is not False:
            issues.append(f"{name} must be False")

    if status.direction_option_count != 5:
        issues.append("direction_option_count mismatch")
    if status.selected_direction_option_id != "NONE":
        issues.append("selected_direction_option_id must be NONE")
    if status.selected_direction_option_count != 0:
        issues.append("selected_direction_option_count must be 0")
    if status.operator_direction_value != "PENDING_EXPLICIT_OPERATOR_DIRECTION":
        issues.append("operator_direction_value must remain pending")
    if status.review_check_count != len(REVIEW_CHECKS):
        issues.append("review_check_count mismatch")
    if status.review_failure_count != 0:
        issues.append("review_failure_count must be 0")
    if len(status.artifacts) != 5:
        issues.append("artifact count mismatch")

    return issues


def review_to_dict(status: OperatorDirectionCycleStatusReview) -> dict[str, Any]:
    return asdict(status)


def build_index_payload(status: OperatorDirectionCycleStatusReview) -> dict[str, Any]:
    return {
        "task_name": status.task_name,
        "status": status.review_status_marker,
        "signature": status.signature,
        "source_task_8_final_baseline_commit": status.source_task_8_final_baseline_commit,
        "source_task_8_final_signature": status.source_task_8_final_signature,
        "previous_stage": status.previous_stage,
        "next_stage": status.next_stage,
        "verdict": status.verdict,
        "decision": status.decision,
        "wait_state_active": status.wait_state_active,
        "wait_state_closed": status.wait_state_closed,
        "decision_gate_blocked": status.decision_gate_blocked,
        "operator_direction_received": status.operator_direction_received,
        "implementation_blocked": status.implementation_blocked,
        "runtime_execution_allowed": status.runtime_execution_allowed,
        "real_submission_allowed": status.real_submission_allowed,
        "kaggle_submission_sent": status.kaggle_submission_sent,
        "private_core_exposure": status.private_core_exposure,
        "legal_certification": status.legal_certification,
        "review_check_count": status.review_check_count,
        "review_failure_count": status.review_failure_count,
        "artifact_count": len(status.artifacts),
    }


def build_markdown(status: OperatorDirectionCycleStatusReview) -> str:
    return f"""# Milestone #16 Task 9 - Operator Direction Cycle Status Review v1

## Status

`{status.review_status_marker}`

## Canonical markers

- task: `{status.task_name}`
- ready: `{status.task_ready_marker}`
- valid: `{status.task_valid_marker}`
- pipeline: `{status.pipeline_ready_marker}`
- signature: `{status.signature}`
- mode: `{status.task_mode}`

## Source binding

- previous stage: `{status.previous_stage}`
- source Task 8 final baseline commit: `{status.source_task_8_final_baseline_commit}`
- source Task 8 final signature: `{status.source_task_8_final_signature}`
- next stage: `{status.next_stage}`

## Review verdict

`{status.verdict}`

## Review decision

`{status.decision}`

## Review reason

`{status.review_reason}`

## Confirmed cycle state

- cycle_status_ready: `{status.cycle_status_ready}`
- cycle_status_closed: `{status.cycle_status_closed}`
- cycle_status_review_ready: `{status.cycle_status_review_ready}`
- cycle_status_review_closed: `{status.cycle_status_review_closed}`
- wait_state_active: `{status.wait_state_active}`
- wait_state_closed: `{status.wait_state_closed}`
- decision_gate_blocked: `{status.decision_gate_blocked}`

## Operator direction

- direction_option_count: `{status.direction_option_count}`
- direction_option_selected: `{status.direction_option_selected}`
- selected_direction_option_id: `{status.selected_direction_option_id}`
- operator_direction_required: `{status.operator_direction_required}`
- operator_direction_received: `{status.operator_direction_received}`
- operator_direction_value: `{status.operator_direction_value}`

## Boundary

- implementation_blocked: `{status.implementation_blocked}`
- implementation_performed: `{status.implementation_performed}`
- runtime_solver_patch_allowed: `{status.runtime_solver_patch_allowed}`
- runtime_solver_modified: `{status.runtime_solver_modified}`
- runtime_wiring_allowed: `{status.runtime_wiring_allowed}`
- runtime_activation_authorized: `{status.runtime_activation_authorized}`
- runtime_execution_allowed: `{status.runtime_execution_allowed}`
- real_evaluation_allowed: `{status.real_evaluation_allowed}`
- real_submission_allowed: `{status.real_submission_allowed}`
- kaggle_submission_sent: `{status.kaggle_submission_sent}`
- private_core_exposure: `{status.private_core_exposure}`
- legal_certification: `{status.legal_certification}`
- fail_closed_required: `{status.fail_closed_required}`
- fail_closed_active: `{status.fail_closed_active}`

## Validation

- review_check_count: `{status.review_check_count}`
- review_failure_count: `{status.review_failure_count}`
"""


def build_manifest(status: OperatorDirectionCycleStatusReview) -> str:
    lines = [
        status.pipeline_ready_marker,
        status.task_ready_marker,
        status.task_valid_marker,
        status.review_status_marker,
        f"signature={status.signature}",
        f"source_task_8_final_baseline_commit={status.source_task_8_final_baseline_commit}",
        f"source_task_8_final_signature={status.source_task_8_final_signature}",
        f"task_mode={status.task_mode}",
        f"verdict={status.verdict}",
        f"decision={status.decision}",
        f"review_reason={status.review_reason}",
        f"previous_stage={status.previous_stage}",
        f"next_stage={status.next_stage}",
        f"cycle_status_ready={status.cycle_status_ready}",
        f"cycle_status_closed={status.cycle_status_closed}",
        f"wait_state_active={status.wait_state_active}",
        f"wait_state_closed={status.wait_state_closed}",
        f"decision_gate_blocked={status.decision_gate_blocked}",
        f"direction_option_count={status.direction_option_count}",
        f"direction_option_selected={status.direction_option_selected}",
        f"operator_direction_required={status.operator_direction_required}",
        f"operator_direction_received={status.operator_direction_received}",
        f"operator_direction_value={status.operator_direction_value}",
        f"implementation_blocked={status.implementation_blocked}",
        f"runtime_execution_allowed={status.runtime_execution_allowed}",
        f"real_submission_allowed={status.real_submission_allowed}",
        f"kaggle_submission_sent={status.kaggle_submission_sent}",
        f"private_core_exposure={status.private_core_exposure}",
        f"legal_certification={status.legal_certification}",
        f"fail_closed_active={status.fail_closed_active}",
        f"review_check_count={status.review_check_count}",
        f"review_failure_count={status.review_failure_count}",
    ]
    return "\n".join(lines) + "\n"


def write_cycle_status_review_artifacts(
    status: OperatorDirectionCycleStatusReview | None = None,
) -> OperatorDirectionCycleStatusReview:
    resolved = status or build_cycle_status_review()
    issues = validate_cycle_status_review(resolved)
    if issues:
        raise ValueError("Invalid cycle status review: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = review_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (
        ARTIFACT_DIR
        / "milestone-16-operator-direction-cycle-status-review-v1.json"
    ).write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (
        ARTIFACT_DIR
        / "milestone-16-operator-direction-cycle-status-review-index-v1.json"
    ).write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (
        ARTIFACT_DIR
        / "milestone-16-operator-direction-cycle-status-review-manifest-v1.txt"
    ).write_text(manifest, encoding="utf-8")
    (
        ARTIFACT_DIR
        / "milestone-16-operator-direction-cycle-status-review-v1.md"
    ).write_text(markdown, encoding="utf-8")
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_cycle_status_review_artifacts()

    print(status.pipeline_ready_marker)
    print(status.task_ready_marker)
    print(status.task_valid_marker)
    print(status.signature)
    print(status.source_task_8_final_baseline_commit)
    print(status.task_mode)
    print(status.review_status_marker)
    print(status.verdict)
    print(status.decision)
    print(status.review_reason)
    print(status.previous_stage)
    print(status.next_stage)
    print(f"source_task_8_final_baseline_commit={status.source_task_8_final_baseline_commit}")
    print(f"source_task_8_final_signature={status.source_task_8_final_signature}")
    print(f"cycle_status_ready={status.cycle_status_ready}")
    print(f"cycle_status_passed={status.cycle_status_passed}")
    print(f"cycle_status_closed={status.cycle_status_closed}")
    print(f"cycle_status_review_ready={status.cycle_status_review_ready}")
    print(f"cycle_status_review_passed={status.cycle_status_review_passed}")
    print(f"cycle_status_review_closed={status.cycle_status_review_closed}")
    print(f"wait_state_closure_closed={status.wait_state_closure_closed}")
    print(f"wait_state_review_closed={status.wait_state_review_closed}")
    print(f"wait_state_ready={status.wait_state_ready}")
    print(f"wait_state_active={status.wait_state_active}")
    print(f"wait_state_closed={status.wait_state_closed}")
    print(f"decision_gate_ready={status.decision_gate_ready}")
    print(f"decision_gate_open={status.decision_gate_open}")
    print(f"decision_gate_blocked={status.decision_gate_blocked}")
    print(f"direction_option_count={status.direction_option_count}")
    print(f"direction_option_selected={status.direction_option_selected}")
    print(f"selected_direction_option_id={status.selected_direction_option_id}")
    print(f"selected_direction_option_count={status.selected_direction_option_count}")
    print(f"operator_direction_required={status.operator_direction_required}")
    print(f"operator_direction_received={status.operator_direction_received}")
    print(f"operator_direction_value={status.operator_direction_value}")
    print(f"operator_decision_required={status.operator_decision_required}")
    print(f"operator_decision_received={status.operator_decision_received}")
    print(f"explicit_operator_authorization_required={status.explicit_operator_authorization_required}")
    print(f"explicit_operator_authorization_received={status.explicit_operator_authorization_received}")
    print(f"implementation_authorization_granted={status.implementation_authorization_granted}")
    print(f"implementation_authorized={status.implementation_authorized}")
    print(f"implementation_blocked={status.implementation_blocked}")
    print(f"implementation_performed={status.implementation_performed}")
    print(f"implementation_patch_created={status.implementation_patch_created}")
    print(f"implementation_patch_applied={status.implementation_patch_applied}")
    print(f"runtime_solver_patch_allowed={status.runtime_solver_patch_allowed}")
    print(f"runtime_solver_modified={status.runtime_solver_modified}")
    print(f"ranker_runtime_patch_allowed={status.ranker_runtime_patch_allowed}")
    print(f"ranker_runtime_modified={status.ranker_runtime_modified}")
    print(f"candidate_generator_patch_allowed={status.candidate_generator_patch_allowed}")
    print(f"candidate_generator_modified={status.candidate_generator_modified}")
    print(f"runtime_wiring_allowed={status.runtime_wiring_allowed}")
    print(f"runtime_wiring_performed={status.runtime_wiring_performed}")
    print(f"runtime_activation_authorized={status.runtime_activation_authorized}")
    print(f"runtime_activation_performed={status.runtime_activation_performed}")
    print(f"runtime_execution_allowed={status.runtime_execution_allowed}")
    print(f"runtime_execution_performed={status.runtime_execution_performed}")
    print(f"real_evaluation_allowed={status.real_evaluation_allowed}")
    print(f"real_submission_allowed={status.real_submission_allowed}")
    print(f"kaggle_submission_sent={status.kaggle_submission_sent}")
    print(f"private_core_exposure={status.private_core_exposure}")
    print(f"legal_certification={status.legal_certification}")
    print(f"fail_closed_required={status.fail_closed_required}")
    print(f"fail_closed_active={status.fail_closed_active}")
    print(f"review_check_count={status.review_check_count}")
    print(f"review_failure_count={status.review_failure_count}")
    for artifact in status.artifacts:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
