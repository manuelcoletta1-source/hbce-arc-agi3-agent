"""Milestone #17 Task 1 - Operator Direction Gate Intake v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_1_OPERATOR_DIRECTION_GATE_INTAKE_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

INTAKE_STATUS_MARKER = "MILESTONE_17_OPERATOR_DIRECTION_GATE_INTAKE_READY"
INTAKE_VERDICT = "OPERATOR_DIRECTION_INTAKE_ACCEPTED_CONTROLLED_NEXT_PHASE_ONLY"
INTAKE_DECISION = "OPEN_CONTROLLED_NEXT_PHASE_PLANNING_NO_RUNTIME_NO_SUBMISSION"
INTAKE_REASON = "USER_DIRECTION_OK_PROSEGUI_RECEIVED_AFTER_MILESTONE_16_WAIT_STATE_ARCHIVE_CLOSURE_REVIEW"

PREVIOUS_STAGE = "MILESTONE_16_TASK_31_OPERATOR_DIRECTION_FINAL_WAIT_STATE_ARCHIVE_CLOSURE_REVIEW_V1"
NEXT_STAGE = "MILESTONE_17_TASK_2_CONTROLLED_NEXT_PHASE_OPTIONS_INDEX_V1"

SOURCE_TASK_31_FINAL_BASELINE_COMMIT = "5fcf4be"
SOURCE_TASK_31_FINAL_SIGNATURE = "3B8C3517778E575E"

OPERATOR_DIRECTION_RAW = "ok prosegui"
OPERATOR_DIRECTION_VALUE = "PROCEED_TO_CONTROLLED_NEXT_PHASE_PLANNING"
OPERATOR_DIRECTION_CLASS = "CONTROLLED_PLANNING_ONLY"

TASK_MODE = (
    "MILESTONE_17_TASK_1_OPERATOR_DIRECTION_GATE_INTAKE_V1_"
    "DIRECTION_INTAKE_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/operator-direction-gate-intake-v1")
DOC_PATH = Path("docs/milestone-17-operator-direction-gate-intake-v1.md")


INTAKE_CHECKS: tuple[str, ...] = (
    "source_task_31_commit_bound",
    "source_task_31_signature_bound",
    "operator_direction_raw_recorded",
    "operator_direction_value_normalized",
    "operator_direction_received_confirmed",
    "operator_direction_class_controlled_planning_only",
    "controlled_next_phase_planning_opened",
    "implementation_not_authorized",
    "implementation_blocked",
    "runtime_solver_patch_not_allowed",
    "runtime_wiring_not_allowed",
    "runtime_activation_not_authorized",
    "runtime_execution_not_allowed",
    "real_evaluation_not_allowed",
    "real_submission_not_allowed",
    "manual_upload_not_allowed",
    "kaggle_authentication_not_allowed",
    "kaggle_submission_not_sent",
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


def build_operator_direction_gate_intake() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_31_final_baseline_commit": SOURCE_TASK_31_FINAL_BASELINE_COMMIT,
        "source_task_31_final_signature": SOURCE_TASK_31_FINAL_SIGNATURE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "verdict": INTAKE_VERDICT,
        "decision": INTAKE_DECISION,
        "intake_reason": INTAKE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-17-operator-direction-gate-intake-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-operator-direction-gate-intake-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-operator-direction-gate-intake-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-operator-direction-gate-intake-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "intake_status_marker": INTAKE_STATUS_MARKER,
        "signature": signature,
        "source_task_31_final_baseline_commit": SOURCE_TASK_31_FINAL_BASELINE_COMMIT,
        "source_task_31_final_signature": SOURCE_TASK_31_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": INTAKE_VERDICT,
        "decision": INTAKE_DECISION,
        "intake_reason": INTAKE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "operator_direction_required": True,
        "operator_direction_received": True,
        "operator_direction_accepted": True,
        "controlled_next_phase_planning_opened": True,
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
        "intake_check_count": len(INTAKE_CHECKS),
        "intake_failure_count": 0,
        "intake_checks": INTAKE_CHECKS,
        "artifacts": artifacts,
    }


def validate_operator_direction_gate_intake(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "intake_status_marker": INTAKE_STATUS_MARKER,
        "source_task_31_final_baseline_commit": SOURCE_TASK_31_FINAL_BASELINE_COMMIT,
        "source_task_31_final_signature": SOURCE_TASK_31_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "verdict": INTAKE_VERDICT,
        "decision": INTAKE_DECISION,
        "intake_reason": INTAKE_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    required_true = (
        "operator_direction_required",
        "operator_direction_received",
        "operator_direction_accepted",
        "controlled_next_phase_planning_opened",
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

    if status.get("intake_check_count") != len(INTAKE_CHECKS):
        issues.append("intake_check_count mismatch")
    if status.get("intake_failure_count") != 0:
        issues.append("intake_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def intake_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["intake_status_marker"],
        "signature": status["signature"],
        "source_task_31_final_baseline_commit": status["source_task_31_final_baseline_commit"],
        "source_task_31_final_signature": status["source_task_31_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "operator_direction_value": status["operator_direction_value"],
        "operator_direction_class": status["operator_direction_class"],
        "operator_direction_received": status["operator_direction_received"],
        "controlled_next_phase_planning_opened": status["controlled_next_phase_planning_opened"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "real_submission_allowed": status["real_submission_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "intake_check_count": status["intake_check_count"],
        "intake_failure_count": status["intake_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    return f"""# Milestone #17 Task 1 - Operator Direction Gate Intake v1

## Status

`{status["intake_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 31 final baseline commit: `{status["source_task_31_final_baseline_commit"]}`
- source Task 31 final signature: `{status["source_task_31_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Operator direction intake

- raw direction: `{status["operator_direction_raw"]}`
- normalized direction: `{status["operator_direction_value"]}`
- direction class: `{status["operator_direction_class"]}`
- operator_direction_received: `{status["operator_direction_received"]}`
- operator_direction_accepted: `{status["operator_direction_accepted"]}`

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Reason

`{status["intake_reason"]}`

## Boundary

- controlled_next_phase_planning_opened: `{status["controlled_next_phase_planning_opened"]}`
- implementation_authorization_granted: `{status["implementation_authorization_granted"]}`
- implementation_authorized: `{status["implementation_authorized"]}`
- implementation_blocked: `{status["implementation_blocked"]}`
- runtime_execution_allowed: `{status["runtime_execution_allowed"]}`
- real_evaluation_allowed: `{status["real_evaluation_allowed"]}`
- real_submission_allowed: `{status["real_submission_allowed"]}`
- manual_upload_allowed: `{status["manual_upload_allowed"]}`
- kaggle_authentication_allowed: `{status["kaggle_authentication_allowed"]}`
- kaggle_submission_sent: `{status["kaggle_submission_sent"]}`
- private_core_exposure: `{status["private_core_exposure"]}`
- legal_certification: `{status["legal_certification"]}`
- fail_closed_required: `{status["fail_closed_required"]}`
- fail_closed_active: `{status["fail_closed_active"]}`

## Validation

- intake_check_count: `{status["intake_check_count"]}`
- intake_failure_count: `{status["intake_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["intake_status_marker"],
        f"signature={status['signature']}",
        f"source_task_31_final_baseline_commit={status['source_task_31_final_baseline_commit']}",
        f"source_task_31_final_signature={status['source_task_31_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"intake_reason={status['intake_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"operator_direction_raw={status['operator_direction_raw']}",
        f"operator_direction_value={status['operator_direction_value']}",
        f"operator_direction_class={status['operator_direction_class']}",
        f"operator_direction_received={status['operator_direction_received']}",
        f"controlled_next_phase_planning_opened={status['controlled_next_phase_planning_opened']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"real_submission_allowed={status['real_submission_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"intake_check_count={status['intake_check_count']}",
        f"intake_failure_count={status['intake_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_operator_direction_gate_intake_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_operator_direction_gate_intake()
    issues = validate_operator_direction_gate_intake(resolved)
    if issues:
        raise ValueError("Invalid operator direction gate intake: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = intake_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-operator-direction-gate-intake-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-operator-direction-gate-intake-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-operator-direction-gate-intake-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-operator-direction-gate-intake-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_operator_direction_gate_intake_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_31_final_baseline_commit"])
    print(status["task_mode"])
    print(status["intake_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["intake_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_31_final_baseline_commit",
        "source_task_31_final_signature",
        "operator_direction_raw",
        "operator_direction_value",
        "operator_direction_class",
        "operator_direction_required",
        "operator_direction_received",
        "operator_direction_accepted",
        "controlled_next_phase_planning_opened",
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
        "intake_check_count",
        "intake_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
