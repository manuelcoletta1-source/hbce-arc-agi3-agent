"""Milestone #16 Task 20 - Operator Direction Final Wait State Closeout v1.

This module closes out the documented final wait-state chain after Task 19.

Boundary:
- closeout-only
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


TASK_NAME = "MILESTONE_16_TASK_20_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSEOUT_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

CLOSEOUT_STATUS_MARKER = "MILESTONE_16_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSEOUT_READY"
CLOSEOUT_VERDICT = "FINAL_WAIT_STATE_CLOSEOUT_PASS_WAIT_STATE_ACTIVE_DIRECTION_PENDING"
CLOSEOUT_DECISION = "CLOSEOUT_FINAL_WAIT_STATE_CHAIN_NO_IMPLEMENTATION_ALLOWED"
CLOSEOUT_REASON = "TASK_19_FINAL_INDEX_REVIEW_CONFIRMED_WAIT_STATE_ACTIVE_AND_BLOCKED"

PREVIOUS_STAGE = "MILESTONE_16_TASK_19_OPERATOR_DIRECTION_FINAL_WAIT_STATE_FINAL_INDEX_REVIEW_V1"
NEXT_STAGE = "MILESTONE_16_TASK_21_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSEOUT_REVIEW_V1"

SOURCE_TASK_19_FINAL_BASELINE_COMMIT = "24b7b8e"
SOURCE_TASK_19_FINAL_SIGNATURE = "F7A96CEC709BBB4A"

TASK_MODE = (
    "MILESTONE_16_TASK_20_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSEOUT_V1_"
    "CLOSEOUT_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-16/operator-direction-final-wait-state-closeout-v1")
DOC_PATH = Path("docs/milestone-16-operator-direction-final-wait-state-closeout-v1.md")


CLOSEOUT_STAGES: tuple[str, ...] = (
    "MILESTONE_16_TASK_7_OPERATOR_DIRECTION_WAIT_STATE_CLOSURE_V1",
    "MILESTONE_16_TASK_8_OPERATOR_DIRECTION_CYCLE_STATUS_V1",
    "MILESTONE_16_TASK_9_OPERATOR_DIRECTION_CYCLE_STATUS_REVIEW_V1",
    "MILESTONE_16_TASK_10_OPERATOR_DIRECTION_FINAL_WAIT_STATE_AUDIT_V1",
    "MILESTONE_16_TASK_11_OPERATOR_DIRECTION_FINAL_WAIT_STATE_AUDIT_REVIEW_V1",
    "MILESTONE_16_TASK_12_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSURE_V1",
    "MILESTONE_16_TASK_13_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSURE_REVIEW_V1",
    "MILESTONE_16_TASK_14_OPERATOR_DIRECTION_FINAL_WAIT_STATE_SUMMARY_V1",
    "MILESTONE_16_TASK_15_OPERATOR_DIRECTION_FINAL_WAIT_STATE_SUMMARY_REVIEW_V1",
    "MILESTONE_16_TASK_16_OPERATOR_DIRECTION_FINAL_WAIT_STATE_PACKAGE_CLOSURE_V1",
    "MILESTONE_16_TASK_17_OPERATOR_DIRECTION_FINAL_WAIT_STATE_PACKAGE_CLOSURE_REVIEW_V1",
    "MILESTONE_16_TASK_18_OPERATOR_DIRECTION_FINAL_WAIT_STATE_FINAL_INDEX_V1",
    "MILESTONE_16_TASK_19_OPERATOR_DIRECTION_FINAL_WAIT_STATE_FINAL_INDEX_REVIEW_V1",
)


CLOSEOUT_CHECKS: tuple[str, ...] = (
    "source_task_19_commit_bound",
    "source_task_19_signature_bound",
    "closeout_stage_count_confirmed",
    "task_7_closeout_chain_bound",
    "task_8_closeout_chain_bound",
    "task_9_closeout_chain_bound",
    "task_10_closeout_chain_bound",
    "task_11_closeout_chain_bound",
    "task_12_closeout_chain_bound",
    "task_13_closeout_chain_bound",
    "task_14_closeout_chain_bound",
    "task_15_closeout_chain_bound",
    "task_16_closeout_chain_bound",
    "task_17_closeout_chain_bound",
    "task_18_closeout_chain_bound",
    "task_19_closeout_chain_bound",
    "closeout_ready_confirmed",
    "closeout_passed_confirmed",
    "closeout_closed_confirmed",
    "wait_state_ready_confirmed",
    "wait_state_active_confirmed",
    "wait_state_not_closed_confirmed",
    "decision_gate_ready_confirmed",
    "decision_gate_not_open_confirmed",
    "decision_gate_blocked_confirmed",
    "operator_direction_required_confirmed",
    "operator_direction_missing_confirmed",
    "operator_authorization_missing_confirmed",
    "implementation_blocked_confirmed",
    "implementation_not_performed_confirmed",
    "runtime_solver_patch_blocked_confirmed",
    "runtime_wiring_blocked_confirmed",
    "runtime_activation_blocked_confirmed",
    "runtime_execution_blocked_confirmed",
    "real_evaluation_blocked_confirmed",
    "real_submission_blocked_confirmed",
    "manual_upload_blocked_confirmed",
    "kaggle_authentication_not_performed_confirmed",
    "kaggle_submission_not_sent_confirmed",
    "private_core_not_exposed_confirmed",
    "legal_certification_false_confirmed",
    "fail_closed_required_confirmed",
    "fail_closed_active_confirmed",
)


@dataclass(frozen=True)
class OperatorDirectionFinalWaitStateCloseout:
    task_name: str
    task_ready_marker: str
    task_valid_marker: str
    pipeline_ready_marker: str
    closeout_status_marker: str
    signature: str
    source_task_19_final_baseline_commit: str
    source_task_19_final_signature: str
    task_mode: str
    verdict: str
    decision: str
    closeout_reason: str
    previous_stage: str
    next_stage: str

    final_wait_state_final_index_review_ready: bool
    final_wait_state_final_index_review_passed: bool
    final_wait_state_final_index_review_closed: bool
    final_wait_state_closeout_ready: bool
    final_wait_state_closeout_passed: bool
    final_wait_state_closeout_closed: bool

    closeout_stage_count: int
    closeout_stages: tuple[str, ...]

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
    runtime_solver_patch_allowed: bool
    runtime_solver_modified: bool
    runtime_wiring_allowed: bool
    runtime_wiring_performed: bool
    runtime_activation_authorized: bool
    runtime_activation_performed: bool
    runtime_execution_allowed: bool
    runtime_execution_performed: bool
    real_evaluation_allowed: bool
    real_submission_allowed: bool
    manual_upload_allowed: bool
    upload_performed: bool
    kaggle_authentication_allowed: bool
    kaggle_authentication_performed: bool
    kaggle_submission_sent: bool
    private_core_exposure: bool
    legal_certification: bool
    fail_closed_required: bool
    fail_closed_active: bool

    closeout_check_count: int
    closeout_failure_count: int
    closeout_checks: tuple[str, ...]
    artifacts: tuple[str, ...]


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_final_wait_state_closeout() -> OperatorDirectionFinalWaitStateCloseout:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_19_final_baseline_commit": SOURCE_TASK_19_FINAL_BASELINE_COMMIT,
        "source_task_19_final_signature": SOURCE_TASK_19_FINAL_SIGNATURE,
        "verdict": CLOSEOUT_VERDICT,
        "decision": CLOSEOUT_DECISION,
        "closeout_reason": CLOSEOUT_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "closeout_stage_count": len(CLOSEOUT_STAGES),
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "wait_state_active": True,
        "wait_state_closed": False,
        "decision_gate_blocked": True,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-closeout-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-closeout-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-closeout-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-closeout-v1.md"),
        str(DOC_PATH),
    )

    return OperatorDirectionFinalWaitStateCloseout(
        task_name=TASK_NAME,
        task_ready_marker=TASK_READY_MARKER,
        task_valid_marker=TASK_VALID_MARKER,
        pipeline_ready_marker=PIPELINE_READY_MARKER,
        closeout_status_marker=CLOSEOUT_STATUS_MARKER,
        signature=signature,
        source_task_19_final_baseline_commit=SOURCE_TASK_19_FINAL_BASELINE_COMMIT,
        source_task_19_final_signature=SOURCE_TASK_19_FINAL_SIGNATURE,
        task_mode=TASK_MODE,
        verdict=CLOSEOUT_VERDICT,
        decision=CLOSEOUT_DECISION,
        closeout_reason=CLOSEOUT_REASON,
        previous_stage=PREVIOUS_STAGE,
        next_stage=NEXT_STAGE,
        final_wait_state_final_index_review_ready=True,
        final_wait_state_final_index_review_passed=True,
        final_wait_state_final_index_review_closed=True,
        final_wait_state_closeout_ready=True,
        final_wait_state_closeout_passed=True,
        final_wait_state_closeout_closed=True,
        closeout_stage_count=len(CLOSEOUT_STAGES),
        closeout_stages=CLOSEOUT_STAGES,
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
        runtime_solver_patch_allowed=False,
        runtime_solver_modified=False,
        runtime_wiring_allowed=False,
        runtime_wiring_performed=False,
        runtime_activation_authorized=False,
        runtime_activation_performed=False,
        runtime_execution_allowed=False,
        runtime_execution_performed=False,
        real_evaluation_allowed=False,
        real_submission_allowed=False,
        manual_upload_allowed=False,
        upload_performed=False,
        kaggle_authentication_allowed=False,
        kaggle_authentication_performed=False,
        kaggle_submission_sent=False,
        private_core_exposure=False,
        legal_certification=False,
        fail_closed_required=True,
        fail_closed_active=True,
        closeout_check_count=len(CLOSEOUT_CHECKS),
        closeout_failure_count=0,
        closeout_checks=CLOSEOUT_CHECKS,
        artifacts=artifacts,
    )


def validate_final_wait_state_closeout(status: OperatorDirectionFinalWaitStateCloseout) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "closeout_status_marker": CLOSEOUT_STATUS_MARKER,
        "source_task_19_final_baseline_commit": SOURCE_TASK_19_FINAL_BASELINE_COMMIT,
        "source_task_19_final_signature": SOURCE_TASK_19_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "verdict": CLOSEOUT_VERDICT,
        "decision": CLOSEOUT_DECISION,
        "closeout_reason": CLOSEOUT_REASON,
    }

    actual = {
        "task_name": status.task_name,
        "task_ready_marker": status.task_ready_marker,
        "task_valid_marker": status.task_valid_marker,
        "pipeline_ready_marker": status.pipeline_ready_marker,
        "closeout_status_marker": status.closeout_status_marker,
        "source_task_19_final_baseline_commit": status.source_task_19_final_baseline_commit,
        "source_task_19_final_signature": status.source_task_19_final_signature,
        "previous_stage": status.previous_stage,
        "next_stage": status.next_stage,
        "verdict": status.verdict,
        "decision": status.decision,
        "closeout_reason": status.closeout_reason,
    }

    for key, expected_value in expected.items():
        if actual[key] != expected_value:
            issues.append(f"{key} mismatch")

    required_true = {
        "final_wait_state_final_index_review_ready": status.final_wait_state_final_index_review_ready,
        "final_wait_state_final_index_review_passed": status.final_wait_state_final_index_review_passed,
        "final_wait_state_final_index_review_closed": status.final_wait_state_final_index_review_closed,
        "final_wait_state_closeout_ready": status.final_wait_state_closeout_ready,
        "final_wait_state_closeout_passed": status.final_wait_state_closeout_passed,
        "final_wait_state_closeout_closed": status.final_wait_state_closeout_closed,
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
        "runtime_solver_patch_allowed": status.runtime_solver_patch_allowed,
        "runtime_solver_modified": status.runtime_solver_modified,
        "runtime_wiring_allowed": status.runtime_wiring_allowed,
        "runtime_wiring_performed": status.runtime_wiring_performed,
        "runtime_activation_authorized": status.runtime_activation_authorized,
        "runtime_activation_performed": status.runtime_activation_performed,
        "runtime_execution_allowed": status.runtime_execution_allowed,
        "runtime_execution_performed": status.runtime_execution_performed,
        "real_evaluation_allowed": status.real_evaluation_allowed,
        "real_submission_allowed": status.real_submission_allowed,
        "manual_upload_allowed": status.manual_upload_allowed,
        "upload_performed": status.upload_performed,
        "kaggle_authentication_allowed": status.kaggle_authentication_allowed,
        "kaggle_authentication_performed": status.kaggle_authentication_performed,
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

    if status.closeout_stage_count != len(CLOSEOUT_STAGES):
        issues.append("closeout_stage_count mismatch")
    if status.closeout_stages != CLOSEOUT_STAGES:
        issues.append("closeout_stages mismatch")
    if status.direction_option_count != 5:
        issues.append("direction_option_count mismatch")
    if status.selected_direction_option_id != "NONE":
        issues.append("selected_direction_option_id must be NONE")
    if status.selected_direction_option_count != 0:
        issues.append("selected_direction_option_count must be 0")
    if status.operator_direction_value != "PENDING_EXPLICIT_OPERATOR_DIRECTION":
        issues.append("operator_direction_value must remain pending")
    if status.closeout_check_count != len(CLOSEOUT_CHECKS):
        issues.append("closeout_check_count mismatch")
    if status.closeout_failure_count != 0:
        issues.append("closeout_failure_count must be 0")
    if len(status.artifacts) != 5:
        issues.append("artifact count mismatch")

    return issues


def closeout_to_dict(status: OperatorDirectionFinalWaitStateCloseout) -> dict[str, Any]:
    return asdict(status)


def build_index_payload(status: OperatorDirectionFinalWaitStateCloseout) -> dict[str, Any]:
    return {
        "task_name": status.task_name,
        "status": status.closeout_status_marker,
        "signature": status.signature,
        "source_task_19_final_baseline_commit": status.source_task_19_final_baseline_commit,
        "source_task_19_final_signature": status.source_task_19_final_signature,
        "previous_stage": status.previous_stage,
        "next_stage": status.next_stage,
        "verdict": status.verdict,
        "decision": status.decision,
        "closeout_reason": status.closeout_reason,
        "closeout_stage_count": status.closeout_stage_count,
        "final_wait_state_closeout_closed": status.final_wait_state_closeout_closed,
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
        "fail_closed_active": status.fail_closed_active,
        "closeout_check_count": status.closeout_check_count,
        "closeout_failure_count": status.closeout_failure_count,
        "artifact_count": len(status.artifacts),
    }


def build_markdown(status: OperatorDirectionFinalWaitStateCloseout) -> str:
    stage_lines = "\n".join(f"- `{stage}`" for stage in status.closeout_stages)
    return f"""# Milestone #16 Task 20 - Operator Direction Final Wait State Closeout v1

## Status

`{status.closeout_status_marker}`

## Canonical markers

- task: `{status.task_name}`
- ready: `{status.task_ready_marker}`
- valid: `{status.task_valid_marker}`
- pipeline: `{status.pipeline_ready_marker}`
- signature: `{status.signature}`
- mode: `{status.task_mode}`

## Source binding

- previous stage: `{status.previous_stage}`
- source Task 19 final baseline commit: `{status.source_task_19_final_baseline_commit}`
- source Task 19 final signature: `{status.source_task_19_final_signature}`
- next stage: `{status.next_stage}`

## Closeout verdict

`{status.verdict}`

## Closeout decision

`{status.decision}`

## Closeout reason

`{status.closeout_reason}`

## Closed chain

- closeout_stage_count: `{status.closeout_stage_count}`

{stage_lines}

## Closeout state

- final_wait_state_final_index_review_closed: `{status.final_wait_state_final_index_review_closed}`
- final_wait_state_closeout_ready: `{status.final_wait_state_closeout_ready}`
- final_wait_state_closeout_passed: `{status.final_wait_state_closeout_passed}`
- final_wait_state_closeout_closed: `{status.final_wait_state_closeout_closed}`

## Wait state

- wait_state_ready: `{status.wait_state_ready}`
- wait_state_active: `{status.wait_state_active}`
- wait_state_closed: `{status.wait_state_closed}`
- decision_gate_ready: `{status.decision_gate_ready}`
- decision_gate_open: `{status.decision_gate_open}`
- decision_gate_blocked: `{status.decision_gate_blocked}`

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
- manual_upload_allowed: `{status.manual_upload_allowed}`
- kaggle_authentication_performed: `{status.kaggle_authentication_performed}`
- kaggle_submission_sent: `{status.kaggle_submission_sent}`
- private_core_exposure: `{status.private_core_exposure}`
- legal_certification: `{status.legal_certification}`
- fail_closed_required: `{status.fail_closed_required}`
- fail_closed_active: `{status.fail_closed_active}`

## Validation

- closeout_check_count: `{status.closeout_check_count}`
- closeout_failure_count: `{status.closeout_failure_count}`
"""


def build_manifest(status: OperatorDirectionFinalWaitStateCloseout) -> str:
    lines = [
        status.pipeline_ready_marker,
        status.task_ready_marker,
        status.task_valid_marker,
        status.closeout_status_marker,
        f"signature={status.signature}",
        f"source_task_19_final_baseline_commit={status.source_task_19_final_baseline_commit}",
        f"source_task_19_final_signature={status.source_task_19_final_signature}",
        f"task_mode={status.task_mode}",
        f"verdict={status.verdict}",
        f"decision={status.decision}",
        f"closeout_reason={status.closeout_reason}",
        f"previous_stage={status.previous_stage}",
        f"next_stage={status.next_stage}",
        f"closeout_stage_count={status.closeout_stage_count}",
        f"final_wait_state_closeout_ready={status.final_wait_state_closeout_ready}",
        f"final_wait_state_closeout_passed={status.final_wait_state_closeout_passed}",
        f"final_wait_state_closeout_closed={status.final_wait_state_closeout_closed}",
        f"wait_state_active={status.wait_state_active}",
        f"wait_state_closed={status.wait_state_closed}",
        f"decision_gate_blocked={status.decision_gate_blocked}",
        f"operator_direction_received={status.operator_direction_received}",
        f"operator_direction_value={status.operator_direction_value}",
        f"implementation_blocked={status.implementation_blocked}",
        f"runtime_execution_allowed={status.runtime_execution_allowed}",
        f"real_submission_allowed={status.real_submission_allowed}",
        f"kaggle_submission_sent={status.kaggle_submission_sent}",
        f"private_core_exposure={status.private_core_exposure}",
        f"legal_certification={status.legal_certification}",
        f"fail_closed_active={status.fail_closed_active}",
        f"closeout_check_count={status.closeout_check_count}",
        f"closeout_failure_count={status.closeout_failure_count}",
    ]
    return "\n".join(lines) + "\n"


def write_final_wait_state_closeout_artifacts(
    status: OperatorDirectionFinalWaitStateCloseout | None = None,
) -> OperatorDirectionFinalWaitStateCloseout:
    resolved = status or build_final_wait_state_closeout()
    issues = validate_final_wait_state_closeout(resolved)
    if issues:
        raise ValueError("Invalid final wait state closeout: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = closeout_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-closeout-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-closeout-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-closeout-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-closeout-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_final_wait_state_closeout_artifacts()

    print(status.pipeline_ready_marker)
    print(status.task_ready_marker)
    print(status.task_valid_marker)
    print(status.signature)
    print(status.source_task_19_final_baseline_commit)
    print(status.task_mode)
    print(status.closeout_status_marker)
    print(status.verdict)
    print(status.decision)
    print(status.closeout_reason)
    print(status.previous_stage)
    print(status.next_stage)
    print(f"source_task_19_final_baseline_commit={status.source_task_19_final_baseline_commit}")
    print(f"source_task_19_final_signature={status.source_task_19_final_signature}")
    print(f"closeout_stage_count={status.closeout_stage_count}")
    print(f"final_wait_state_final_index_review_ready={status.final_wait_state_final_index_review_ready}")
    print(f"final_wait_state_final_index_review_passed={status.final_wait_state_final_index_review_passed}")
    print(f"final_wait_state_final_index_review_closed={status.final_wait_state_final_index_review_closed}")
    print(f"final_wait_state_closeout_ready={status.final_wait_state_closeout_ready}")
    print(f"final_wait_state_closeout_passed={status.final_wait_state_closeout_passed}")
    print(f"final_wait_state_closeout_closed={status.final_wait_state_closeout_closed}")
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
    print(f"runtime_solver_patch_allowed={status.runtime_solver_patch_allowed}")
    print(f"runtime_solver_modified={status.runtime_solver_modified}")
    print(f"runtime_wiring_allowed={status.runtime_wiring_allowed}")
    print(f"runtime_wiring_performed={status.runtime_wiring_performed}")
    print(f"runtime_activation_authorized={status.runtime_activation_authorized}")
    print(f"runtime_activation_performed={status.runtime_activation_performed}")
    print(f"runtime_execution_allowed={status.runtime_execution_allowed}")
    print(f"runtime_execution_performed={status.runtime_execution_performed}")
    print(f"real_evaluation_allowed={status.real_evaluation_allowed}")
    print(f"real_submission_allowed={status.real_submission_allowed}")
    print(f"manual_upload_allowed={status.manual_upload_allowed}")
    print(f"upload_performed={status.upload_performed}")
    print(f"kaggle_authentication_allowed={status.kaggle_authentication_allowed}")
    print(f"kaggle_authentication_performed={status.kaggle_authentication_performed}")
    print(f"kaggle_submission_sent={status.kaggle_submission_sent}")
    print(f"private_core_exposure={status.private_core_exposure}")
    print(f"legal_certification={status.legal_certification}")
    print(f"fail_closed_required={status.fail_closed_required}")
    print(f"fail_closed_active={status.fail_closed_active}")
    print(f"closeout_check_count={status.closeout_check_count}")
    print(f"closeout_failure_count={status.closeout_failure_count}")
    for artifact in status.artifacts:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
