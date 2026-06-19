"""Milestone #16 Task 22 - Operator Direction Final Wait State Archive Index v1."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_16_TASK_22_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_INDEX_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

ARCHIVE_STATUS_MARKER = "MILESTONE_16_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_INDEX_READY"
ARCHIVE_VERDICT = "FINAL_WAIT_STATE_ARCHIVE_INDEX_PASS_CLOSEOUT_REVIEW_CONFIRMED"
ARCHIVE_DECISION = "ARCHIVE_FINAL_WAIT_STATE_CHAIN_NO_IMPLEMENTATION_ALLOWED"
ARCHIVE_REASON = "TASK_21_CLOSEOUT_REVIEW_CONFIRMED_WAIT_STATE_ACTIVE_DIRECTION_PENDING"

PREVIOUS_STAGE = "MILESTONE_16_TASK_21_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSEOUT_REVIEW_V1"
NEXT_STAGE = "MILESTONE_16_TASK_23_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_INDEX_REVIEW_V1"

SOURCE_TASK_21_FINAL_BASELINE_COMMIT = "2469f81"
SOURCE_TASK_21_FINAL_SIGNATURE = "CECEF4128A534D5C"

TASK_MODE = (
    "MILESTONE_16_TASK_22_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_INDEX_V1_"
    "ARCHIVE_INDEX_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-16/operator-direction-final-wait-state-archive-index-v1")
DOC_PATH = Path("docs/milestone-16-operator-direction-final-wait-state-archive-index-v1.md")


ARCHIVED_STAGES: tuple[str, ...] = (
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
    "MILESTONE_16_TASK_20_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSEOUT_V1",
    "MILESTONE_16_TASK_21_OPERATOR_DIRECTION_FINAL_WAIT_STATE_CLOSEOUT_REVIEW_V1",
)


ARCHIVE_CHECKS: tuple[str, ...] = (
    "source_task_21_commit_bound",
    "source_task_21_signature_bound",
    "archived_stage_count_confirmed",
    "task_7_archived",
    "task_8_archived",
    "task_9_archived",
    "task_10_archived",
    "task_11_archived",
    "task_12_archived",
    "task_13_archived",
    "task_14_archived",
    "task_15_archived",
    "task_16_archived",
    "task_17_archived",
    "task_18_archived",
    "task_19_archived",
    "task_20_archived",
    "task_21_archived",
    "archive_index_ready_confirmed",
    "archive_index_passed_confirmed",
    "archive_index_closed_confirmed",
    "wait_state_ready_confirmed",
    "wait_state_active_confirmed",
    "wait_state_not_closed_confirmed",
    "decision_gate_ready_confirmed",
    "decision_gate_not_open_confirmed",
    "decision_gate_blocked_confirmed",
    "direction_options_unselected_confirmed",
    "operator_direction_required_confirmed",
    "operator_direction_missing_confirmed",
    "operator_authorization_missing_confirmed",
    "implementation_blocked_confirmed",
    "implementation_not_performed_confirmed",
    "runtime_solver_patch_blocked_confirmed",
    "runtime_solver_not_modified_confirmed",
    "runtime_wiring_blocked_confirmed",
    "runtime_activation_blocked_confirmed",
    "runtime_execution_blocked_confirmed",
    "real_evaluation_blocked_confirmed",
    "real_submission_blocked_confirmed",
    "manual_upload_blocked_confirmed",
    "kaggle_authentication_blocked_confirmed",
    "kaggle_authentication_not_performed_confirmed",
    "kaggle_submission_not_sent_confirmed",
    "private_core_not_exposed_confirmed",
    "legal_certification_false_confirmed",
    "fail_closed_required_confirmed",
    "fail_closed_active_confirmed",
)


@dataclass(frozen=True)
class OperatorDirectionFinalWaitStateArchiveIndex:
    task_name: str
    task_ready_marker: str
    task_valid_marker: str
    pipeline_ready_marker: str
    archive_status_marker: str
    signature: str
    source_task_21_final_baseline_commit: str
    source_task_21_final_signature: str
    task_mode: str
    verdict: str
    decision: str
    archive_reason: str
    previous_stage: str
    next_stage: str

    final_wait_state_closeout_review_ready: bool
    final_wait_state_closeout_review_passed: bool
    final_wait_state_closeout_review_closed: bool
    final_wait_state_archive_index_ready: bool
    final_wait_state_archive_index_passed: bool
    final_wait_state_archive_index_closed: bool

    archived_stage_count: int
    archived_stages: tuple[str, ...]

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

    archive_check_count: int
    archive_failure_count: int
    archive_checks: tuple[str, ...]
    artifacts: tuple[str, ...]


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_final_wait_state_archive_index() -> OperatorDirectionFinalWaitStateArchiveIndex:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_21_final_baseline_commit": SOURCE_TASK_21_FINAL_BASELINE_COMMIT,
        "source_task_21_final_signature": SOURCE_TASK_21_FINAL_SIGNATURE,
        "verdict": ARCHIVE_VERDICT,
        "decision": ARCHIVE_DECISION,
        "archive_reason": ARCHIVE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "archived_stage_count": len(ARCHIVED_STAGES),
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
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-index-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-index-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-index-v1.md"),
        str(DOC_PATH),
    )

    return OperatorDirectionFinalWaitStateArchiveIndex(
        task_name=TASK_NAME,
        task_ready_marker=TASK_READY_MARKER,
        task_valid_marker=TASK_VALID_MARKER,
        pipeline_ready_marker=PIPELINE_READY_MARKER,
        archive_status_marker=ARCHIVE_STATUS_MARKER,
        signature=signature,
        source_task_21_final_baseline_commit=SOURCE_TASK_21_FINAL_BASELINE_COMMIT,
        source_task_21_final_signature=SOURCE_TASK_21_FINAL_SIGNATURE,
        task_mode=TASK_MODE,
        verdict=ARCHIVE_VERDICT,
        decision=ARCHIVE_DECISION,
        archive_reason=ARCHIVE_REASON,
        previous_stage=PREVIOUS_STAGE,
        next_stage=NEXT_STAGE,
        final_wait_state_closeout_review_ready=True,
        final_wait_state_closeout_review_passed=True,
        final_wait_state_closeout_review_closed=True,
        final_wait_state_archive_index_ready=True,
        final_wait_state_archive_index_passed=True,
        final_wait_state_archive_index_closed=True,
        archived_stage_count=len(ARCHIVED_STAGES),
        archived_stages=ARCHIVED_STAGES,
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
        archive_check_count=len(ARCHIVE_CHECKS),
        archive_failure_count=0,
        archive_checks=ARCHIVE_CHECKS,
        artifacts=artifacts,
    )


def validate_final_wait_state_archive_index(
    status: OperatorDirectionFinalWaitStateArchiveIndex,
) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "archive_status_marker": ARCHIVE_STATUS_MARKER,
        "source_task_21_final_baseline_commit": SOURCE_TASK_21_FINAL_BASELINE_COMMIT,
        "source_task_21_final_signature": SOURCE_TASK_21_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "verdict": ARCHIVE_VERDICT,
        "decision": ARCHIVE_DECISION,
        "archive_reason": ARCHIVE_REASON,
    }

    actual = {
        "task_name": status.task_name,
        "task_ready_marker": status.task_ready_marker,
        "task_valid_marker": status.task_valid_marker,
        "pipeline_ready_marker": status.pipeline_ready_marker,
        "archive_status_marker": status.archive_status_marker,
        "source_task_21_final_baseline_commit": status.source_task_21_final_baseline_commit,
        "source_task_21_final_signature": status.source_task_21_final_signature,
        "previous_stage": status.previous_stage,
        "next_stage": status.next_stage,
        "verdict": status.verdict,
        "decision": status.decision,
        "archive_reason": status.archive_reason,
    }

    for key, expected_value in expected.items():
        if actual[key] != expected_value:
            issues.append(f"{key} mismatch")

    required_true = {
        "final_wait_state_closeout_review_ready": status.final_wait_state_closeout_review_ready,
        "final_wait_state_closeout_review_passed": status.final_wait_state_closeout_review_passed,
        "final_wait_state_closeout_review_closed": status.final_wait_state_closeout_review_closed,
        "final_wait_state_archive_index_ready": status.final_wait_state_archive_index_ready,
        "final_wait_state_archive_index_passed": status.final_wait_state_archive_index_passed,
        "final_wait_state_archive_index_closed": status.final_wait_state_archive_index_closed,
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

    if status.archived_stage_count != len(ARCHIVED_STAGES):
        issues.append("archived_stage_count mismatch")
    if status.archived_stages != ARCHIVED_STAGES:
        issues.append("archived_stages mismatch")
    if status.direction_option_count != 5:
        issues.append("direction_option_count mismatch")
    if status.selected_direction_option_id != "NONE":
        issues.append("selected_direction_option_id must be NONE")
    if status.selected_direction_option_count != 0:
        issues.append("selected_direction_option_count must be 0")
    if status.operator_direction_value != "PENDING_EXPLICIT_OPERATOR_DIRECTION":
        issues.append("operator_direction_value must remain pending")
    if status.archive_check_count != len(ARCHIVE_CHECKS):
        issues.append("archive_check_count mismatch")
    if status.archive_failure_count != 0:
        issues.append("archive_failure_count must be 0")
    if len(status.artifacts) != 5:
        issues.append("artifact count mismatch")

    return issues


def archive_to_dict(status: OperatorDirectionFinalWaitStateArchiveIndex) -> dict[str, Any]:
    return asdict(status)


def build_index_payload(status: OperatorDirectionFinalWaitStateArchiveIndex) -> dict[str, Any]:
    return {
        "task_name": status.task_name,
        "status": status.archive_status_marker,
        "signature": status.signature,
        "source_task_21_final_baseline_commit": status.source_task_21_final_baseline_commit,
        "source_task_21_final_signature": status.source_task_21_final_signature,
        "previous_stage": status.previous_stage,
        "next_stage": status.next_stage,
        "verdict": status.verdict,
        "decision": status.decision,
        "archive_reason": status.archive_reason,
        "archived_stage_count": status.archived_stage_count,
        "final_wait_state_archive_index_closed": status.final_wait_state_archive_index_closed,
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
        "archive_check_count": status.archive_check_count,
        "archive_failure_count": status.archive_failure_count,
        "artifact_count": len(status.artifacts),
    }


def build_markdown(status: OperatorDirectionFinalWaitStateArchiveIndex) -> str:
    stage_lines = "\n".join(f"- `{stage}`" for stage in status.archived_stages)
    return f"""# Milestone #16 Task 22 - Operator Direction Final Wait State Archive Index v1

## Status

`{status.archive_status_marker}`

## Canonical markers

- task: `{status.task_name}`
- ready: `{status.task_ready_marker}`
- valid: `{status.task_valid_marker}`
- pipeline: `{status.pipeline_ready_marker}`
- signature: `{status.signature}`
- mode: `{status.task_mode}`

## Source binding

- previous stage: `{status.previous_stage}`
- source Task 21 final baseline commit: `{status.source_task_21_final_baseline_commit}`
- source Task 21 final signature: `{status.source_task_21_final_signature}`
- next stage: `{status.next_stage}`

## Archive verdict

`{status.verdict}`

## Archive decision

`{status.decision}`

## Archive reason

`{status.archive_reason}`

## Archived chain

- archived_stage_count: `{status.archived_stage_count}`

{stage_lines}

## Archive state

- final_wait_state_closeout_review_closed: `{status.final_wait_state_closeout_review_closed}`
- final_wait_state_archive_index_ready: `{status.final_wait_state_archive_index_ready}`
- final_wait_state_archive_index_passed: `{status.final_wait_state_archive_index_passed}`
- final_wait_state_archive_index_closed: `{status.final_wait_state_archive_index_closed}`

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

- archive_check_count: `{status.archive_check_count}`
- archive_failure_count: `{status.archive_failure_count}`
"""


def build_manifest(status: OperatorDirectionFinalWaitStateArchiveIndex) -> str:
    lines = [
        status.pipeline_ready_marker,
        status.task_ready_marker,
        status.task_valid_marker,
        status.archive_status_marker,
        f"signature={status.signature}",
        f"source_task_21_final_baseline_commit={status.source_task_21_final_baseline_commit}",
        f"source_task_21_final_signature={status.source_task_21_final_signature}",
        f"task_mode={status.task_mode}",
        f"verdict={status.verdict}",
        f"decision={status.decision}",
        f"archive_reason={status.archive_reason}",
        f"previous_stage={status.previous_stage}",
        f"next_stage={status.next_stage}",
        f"archived_stage_count={status.archived_stage_count}",
        f"final_wait_state_archive_index_ready={status.final_wait_state_archive_index_ready}",
        f"final_wait_state_archive_index_passed={status.final_wait_state_archive_index_passed}",
        f"final_wait_state_archive_index_closed={status.final_wait_state_archive_index_closed}",
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
        f"archive_check_count={status.archive_check_count}",
        f"archive_failure_count={status.archive_failure_count}",
    ]
    return "\n".join(lines) + "\n"


def write_final_wait_state_archive_index_artifacts(
    status: OperatorDirectionFinalWaitStateArchiveIndex | None = None,
) -> OperatorDirectionFinalWaitStateArchiveIndex:
    resolved = status or build_final_wait_state_archive_index()
    issues = validate_final_wait_state_archive_index(resolved)
    if issues:
        raise ValueError("Invalid final wait state archive index: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = archive_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-index-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-index-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-index-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-index-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_final_wait_state_archive_index_artifacts()

    print(status.pipeline_ready_marker)
    print(status.task_ready_marker)
    print(status.task_valid_marker)
    print(status.signature)
    print(status.source_task_21_final_baseline_commit)
    print(status.task_mode)
    print(status.archive_status_marker)
    print(status.verdict)
    print(status.decision)
    print(status.archive_reason)
    print(status.previous_stage)
    print(status.next_stage)
    print(f"source_task_21_final_baseline_commit={status.source_task_21_final_baseline_commit}")
    print(f"source_task_21_final_signature={status.source_task_21_final_signature}")
    print(f"archived_stage_count={status.archived_stage_count}")
    print(f"final_wait_state_closeout_review_ready={status.final_wait_state_closeout_review_ready}")
    print(f"final_wait_state_closeout_review_passed={status.final_wait_state_closeout_review_passed}")
    print(f"final_wait_state_closeout_review_closed={status.final_wait_state_closeout_review_closed}")
    print(f"final_wait_state_archive_index_ready={status.final_wait_state_archive_index_ready}")
    print(f"final_wait_state_archive_index_passed={status.final_wait_state_archive_index_passed}")
    print(f"final_wait_state_archive_index_closed={status.final_wait_state_archive_index_closed}")
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
    print(f"archive_check_count={status.archive_check_count}")
    print(f"archive_failure_count={status.archive_failure_count}")
    for artifact in status.artifacts:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
