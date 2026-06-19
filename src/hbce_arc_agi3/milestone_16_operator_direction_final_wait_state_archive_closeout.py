"""Milestone #16 Task 24 - Operator Direction Final Wait State Archive Closeout v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_16_TASK_24_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_CLOSEOUT_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

ARCHIVE_CLOSEOUT_STATUS_MARKER = "MILESTONE_16_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_CLOSEOUT_READY"
ARCHIVE_CLOSEOUT_VERDICT = "FINAL_WAIT_STATE_ARCHIVE_CLOSEOUT_PASS_ARCHIVE_INDEX_REVIEW_CONFIRMED"
ARCHIVE_CLOSEOUT_DECISION = "ARCHIVE_CLOSEOUT_FINAL_WAIT_STATE_CHAIN_NO_IMPLEMENTATION_ALLOWED"
ARCHIVE_CLOSEOUT_REASON = "TASK_23_ARCHIVE_INDEX_REVIEW_CONFIRMED_WAIT_STATE_ACTIVE_DIRECTION_PENDING"

PREVIOUS_STAGE = "MILESTONE_16_TASK_23_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_INDEX_REVIEW_V1"
NEXT_STAGE = "MILESTONE_16_TASK_25_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_CLOSEOUT_REVIEW_V1"

SOURCE_TASK_23_FINAL_BASELINE_COMMIT = "9992af4"
SOURCE_TASK_23_FINAL_SIGNATURE = "32BBDA451C5FC138"

TASK_MODE = (
    "MILESTONE_16_TASK_24_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_CLOSEOUT_V1_"
    "ARCHIVE_CLOSEOUT_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-16/operator-direction-final-wait-state-archive-closeout-v1")
DOC_PATH = Path("docs/milestone-16-operator-direction-final-wait-state-archive-closeout-v1.md")


ARCHIVE_CLOSEOUT_STAGES: tuple[str, ...] = (
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
    "MILESTONE_16_TASK_22_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_INDEX_V1",
    "MILESTONE_16_TASK_23_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_INDEX_REVIEW_V1",
)


ARCHIVE_CLOSEOUT_CHECKS: tuple[str, ...] = (
    "source_task_23_commit_bound",
    "source_task_23_signature_bound",
    "archive_closeout_stage_count_confirmed",
    "task_7_archive_closeout_bound",
    "task_8_archive_closeout_bound",
    "task_9_archive_closeout_bound",
    "task_10_archive_closeout_bound",
    "task_11_archive_closeout_bound",
    "task_12_archive_closeout_bound",
    "task_13_archive_closeout_bound",
    "task_14_archive_closeout_bound",
    "task_15_archive_closeout_bound",
    "task_16_archive_closeout_bound",
    "task_17_archive_closeout_bound",
    "task_18_archive_closeout_bound",
    "task_19_archive_closeout_bound",
    "task_20_archive_closeout_bound",
    "task_21_archive_closeout_bound",
    "task_22_archive_closeout_bound",
    "task_23_archive_closeout_bound",
    "archive_index_review_ready_confirmed",
    "archive_index_review_passed_confirmed",
    "archive_index_review_closed_confirmed",
    "archive_closeout_ready_confirmed",
    "archive_closeout_passed_confirmed",
    "archive_closeout_closed_confirmed",
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
    "upload_not_performed_confirmed",
    "kaggle_authentication_blocked_confirmed",
    "kaggle_authentication_not_performed_confirmed",
    "kaggle_submission_not_sent_confirmed",
    "private_core_not_exposed_confirmed",
    "legal_certification_false_confirmed",
    "fail_closed_required_confirmed",
    "fail_closed_active_confirmed",
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_final_wait_state_archive_closeout() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_23_final_baseline_commit": SOURCE_TASK_23_FINAL_BASELINE_COMMIT,
        "source_task_23_final_signature": SOURCE_TASK_23_FINAL_SIGNATURE,
        "verdict": ARCHIVE_CLOSEOUT_VERDICT,
        "decision": ARCHIVE_CLOSEOUT_DECISION,
        "archive_closeout_reason": ARCHIVE_CLOSEOUT_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "archive_closeout_stage_count": len(ARCHIVE_CLOSEOUT_STAGES),
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
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-closeout-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-closeout-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-closeout-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-closeout-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "archive_closeout_status_marker": ARCHIVE_CLOSEOUT_STATUS_MARKER,
        "signature": signature,
        "source_task_23_final_baseline_commit": SOURCE_TASK_23_FINAL_BASELINE_COMMIT,
        "source_task_23_final_signature": SOURCE_TASK_23_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": ARCHIVE_CLOSEOUT_VERDICT,
        "decision": ARCHIVE_CLOSEOUT_DECISION,
        "archive_closeout_reason": ARCHIVE_CLOSEOUT_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_wait_state_archive_index_review_ready": True,
        "final_wait_state_archive_index_review_passed": True,
        "final_wait_state_archive_index_review_closed": True,
        "final_wait_state_archive_closeout_ready": True,
        "final_wait_state_archive_closeout_passed": True,
        "final_wait_state_archive_closeout_closed": True,
        "archive_closeout_stage_count": len(ARCHIVE_CLOSEOUT_STAGES),
        "archive_closeout_stages": ARCHIVE_CLOSEOUT_STAGES,
        "wait_state_ready": True,
        "wait_state_active": True,
        "wait_state_closed": False,
        "decision_gate_ready": True,
        "decision_gate_open": False,
        "decision_gate_blocked": True,
        "direction_option_count": 5,
        "direction_option_selected": False,
        "selected_direction_option_id": "NONE",
        "selected_direction_option_count": 0,
        "operator_direction_required": True,
        "operator_direction_received": False,
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "operator_decision_required": True,
        "operator_decision_received": False,
        "explicit_operator_authorization_required": True,
        "explicit_operator_authorization_received": False,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "runtime_solver_patch_allowed": False,
        "runtime_solver_modified": False,
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
        "archive_closeout_check_count": len(ARCHIVE_CLOSEOUT_CHECKS),
        "archive_closeout_failure_count": 0,
        "archive_closeout_checks": ARCHIVE_CLOSEOUT_CHECKS,
        "artifacts": artifacts,
    }


def validate_final_wait_state_archive_closeout(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "archive_closeout_status_marker": ARCHIVE_CLOSEOUT_STATUS_MARKER,
        "source_task_23_final_baseline_commit": SOURCE_TASK_23_FINAL_BASELINE_COMMIT,
        "source_task_23_final_signature": SOURCE_TASK_23_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "verdict": ARCHIVE_CLOSEOUT_VERDICT,
        "decision": ARCHIVE_CLOSEOUT_DECISION,
        "archive_closeout_reason": ARCHIVE_CLOSEOUT_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    required_true = (
        "final_wait_state_archive_index_review_ready",
        "final_wait_state_archive_index_review_passed",
        "final_wait_state_archive_index_review_closed",
        "final_wait_state_archive_closeout_ready",
        "final_wait_state_archive_closeout_passed",
        "final_wait_state_archive_closeout_closed",
        "wait_state_ready",
        "wait_state_active",
        "decision_gate_ready",
        "decision_gate_blocked",
        "operator_direction_required",
        "operator_decision_required",
        "explicit_operator_authorization_required",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
    )
    required_false = (
        "wait_state_closed",
        "decision_gate_open",
        "direction_option_selected",
        "operator_direction_received",
        "operator_decision_received",
        "explicit_operator_authorization_received",
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
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
        "private_core_exposure",
        "legal_certification",
    )

    for key in required_true:
        if status.get(key) is not True:
            issues.append(f"{key} must be True")
    for key in required_false:
        if status.get(key) is not False:
            issues.append(f"{key} must be False")

    if status.get("archive_closeout_stage_count") != len(ARCHIVE_CLOSEOUT_STAGES):
        issues.append("archive_closeout_stage_count mismatch")
    if tuple(status.get("archive_closeout_stages", ())) != ARCHIVE_CLOSEOUT_STAGES:
        issues.append("archive_closeout_stages mismatch")
    if status.get("direction_option_count") != 5:
        issues.append("direction_option_count mismatch")
    if status.get("selected_direction_option_id") != "NONE":
        issues.append("selected_direction_option_id must be NONE")
    if status.get("selected_direction_option_count") != 0:
        issues.append("selected_direction_option_count must be 0")
    if status.get("operator_direction_value") != "PENDING_EXPLICIT_OPERATOR_DIRECTION":
        issues.append("operator_direction_value must remain pending")
    if status.get("archive_closeout_check_count") != len(ARCHIVE_CLOSEOUT_CHECKS):
        issues.append("archive_closeout_check_count mismatch")
    if status.get("archive_closeout_failure_count") != 0:
        issues.append("archive_closeout_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def archive_closeout_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["archive_closeout_status_marker"],
        "signature": status["signature"],
        "source_task_23_final_baseline_commit": status["source_task_23_final_baseline_commit"],
        "source_task_23_final_signature": status["source_task_23_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "verdict": status["verdict"],
        "decision": status["decision"],
        "archive_closeout_reason": status["archive_closeout_reason"],
        "archive_closeout_stage_count": status["archive_closeout_stage_count"],
        "final_wait_state_archive_closeout_closed": status["final_wait_state_archive_closeout_closed"],
        "wait_state_active": status["wait_state_active"],
        "wait_state_closed": status["wait_state_closed"],
        "decision_gate_blocked": status["decision_gate_blocked"],
        "operator_direction_received": status["operator_direction_received"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "real_submission_allowed": status["real_submission_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "archive_closeout_check_count": status["archive_closeout_check_count"],
        "archive_closeout_failure_count": status["archive_closeout_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    stage_lines = "\n".join(f"- `{stage}`" for stage in status["archive_closeout_stages"])
    return f"""# Milestone #16 Task 24 - Operator Direction Final Wait State Archive Closeout v1

## Status

`{status["archive_closeout_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 23 final baseline commit: `{status["source_task_23_final_baseline_commit"]}`
- source Task 23 final signature: `{status["source_task_23_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Archive closeout verdict

`{status["verdict"]}`

## Archive closeout decision

`{status["decision"]}`

## Archive closeout reason

`{status["archive_closeout_reason"]}`

## Archive closeout chain

- archive_closeout_stage_count: `{status["archive_closeout_stage_count"]}`

{stage_lines}

## Archive closeout state

- final_wait_state_archive_index_review_closed: `{status["final_wait_state_archive_index_review_closed"]}`
- final_wait_state_archive_closeout_ready: `{status["final_wait_state_archive_closeout_ready"]}`
- final_wait_state_archive_closeout_passed: `{status["final_wait_state_archive_closeout_passed"]}`
- final_wait_state_archive_closeout_closed: `{status["final_wait_state_archive_closeout_closed"]}`

## Wait state

- wait_state_ready: `{status["wait_state_ready"]}`
- wait_state_active: `{status["wait_state_active"]}`
- wait_state_closed: `{status["wait_state_closed"]}`
- decision_gate_ready: `{status["decision_gate_ready"]}`
- decision_gate_open: `{status["decision_gate_open"]}`
- decision_gate_blocked: `{status["decision_gate_blocked"]}`

## Boundary

- implementation_blocked: `{status["implementation_blocked"]}`
- implementation_performed: `{status["implementation_performed"]}`
- runtime_solver_patch_allowed: `{status["runtime_solver_patch_allowed"]}`
- runtime_solver_modified: `{status["runtime_solver_modified"]}`
- runtime_wiring_allowed: `{status["runtime_wiring_allowed"]}`
- runtime_activation_authorized: `{status["runtime_activation_authorized"]}`
- runtime_execution_allowed: `{status["runtime_execution_allowed"]}`
- real_evaluation_allowed: `{status["real_evaluation_allowed"]}`
- real_submission_allowed: `{status["real_submission_allowed"]}`
- manual_upload_allowed: `{status["manual_upload_allowed"]}`
- kaggle_authentication_performed: `{status["kaggle_authentication_performed"]}`
- kaggle_submission_sent: `{status["kaggle_submission_sent"]}`
- private_core_exposure: `{status["private_core_exposure"]}`
- legal_certification: `{status["legal_certification"]}`
- fail_closed_required: `{status["fail_closed_required"]}`
- fail_closed_active: `{status["fail_closed_active"]}`

## Validation

- archive_closeout_check_count: `{status["archive_closeout_check_count"]}`
- archive_closeout_failure_count: `{status["archive_closeout_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["archive_closeout_status_marker"],
        f"signature={status['signature']}",
        f"source_task_23_final_baseline_commit={status['source_task_23_final_baseline_commit']}",
        f"source_task_23_final_signature={status['source_task_23_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"archive_closeout_reason={status['archive_closeout_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"archive_closeout_stage_count={status['archive_closeout_stage_count']}",
        f"final_wait_state_archive_closeout_ready={status['final_wait_state_archive_closeout_ready']}",
        f"final_wait_state_archive_closeout_passed={status['final_wait_state_archive_closeout_passed']}",
        f"final_wait_state_archive_closeout_closed={status['final_wait_state_archive_closeout_closed']}",
        f"wait_state_active={status['wait_state_active']}",
        f"wait_state_closed={status['wait_state_closed']}",
        f"decision_gate_blocked={status['decision_gate_blocked']}",
        f"operator_direction_received={status['operator_direction_received']}",
        f"operator_direction_value={status['operator_direction_value']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"real_submission_allowed={status['real_submission_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"archive_closeout_check_count={status['archive_closeout_check_count']}",
        f"archive_closeout_failure_count={status['archive_closeout_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_final_wait_state_archive_closeout_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_final_wait_state_archive_closeout()
    issues = validate_final_wait_state_archive_closeout(resolved)
    if issues:
        raise ValueError("Invalid final wait state archive closeout: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = archive_closeout_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-closeout-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-closeout-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-closeout-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-16-operator-direction-final-wait-state-archive-closeout-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_final_wait_state_archive_closeout_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_23_final_baseline_commit"])
    print(status["task_mode"])
    print(status["archive_closeout_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["archive_closeout_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])
    ordered_keys = (
        "source_task_23_final_baseline_commit",
        "source_task_23_final_signature",
        "archive_closeout_stage_count",
        "final_wait_state_archive_index_review_ready",
        "final_wait_state_archive_index_review_passed",
        "final_wait_state_archive_index_review_closed",
        "final_wait_state_archive_closeout_ready",
        "final_wait_state_archive_closeout_passed",
        "final_wait_state_archive_closeout_closed",
        "wait_state_ready",
        "wait_state_active",
        "wait_state_closed",
        "decision_gate_ready",
        "decision_gate_open",
        "decision_gate_blocked",
        "direction_option_count",
        "direction_option_selected",
        "selected_direction_option_id",
        "selected_direction_option_count",
        "operator_direction_required",
        "operator_direction_received",
        "operator_direction_value",
        "operator_decision_required",
        "operator_decision_received",
        "explicit_operator_authorization_required",
        "explicit_operator_authorization_received",
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_blocked",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
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
        "private_core_exposure",
        "legal_certification",
        "fail_closed_required",
        "fail_closed_active",
        "archive_closeout_check_count",
        "archive_closeout_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
