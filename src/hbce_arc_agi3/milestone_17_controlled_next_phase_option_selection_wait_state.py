"""Milestone #17 Task 6 - Controlled Next Phase Option Selection Wait State v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_6_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_WAIT_STATE_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

WAIT_STATE_STATUS_MARKER = "MILESTONE_17_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_WAIT_STATE_READY"
WAIT_STATE_VERDICT = "CONTROLLED_NEXT_PHASE_OPTION_SELECTION_WAIT_STATE_ACTIVE_SELECTION_REQUIRED"
WAIT_STATE_DECISION = "WAIT_FOR_EXPLICIT_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_NO_IMPLEMENTATION_ALLOWED"
WAIT_STATE_REASON = "TASK_5_GATE_REVIEW_CONFIRMED_SELECTION_REQUIRED_NO_OPTION_SELECTED"

PREVIOUS_STAGE = "MILESTONE_17_TASK_5_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_REVIEW_V1"
NEXT_STAGE = "PENDING_EXPLICIT_CONTROLLED_NEXT_PHASE_OPTION_SELECTION"

SOURCE_TASK_5_FINAL_BASELINE_COMMIT = "c552e0d"
SOURCE_TASK_5_FINAL_SIGNATURE = "9E999303503BB4AB"

OPERATOR_DIRECTION_RAW = "ok prosegui"
OPERATOR_DIRECTION_VALUE = "PROCEED_TO_CONTROLLED_NEXT_PHASE_PLANNING"
OPERATOR_DIRECTION_CLASS = "CONTROLLED_PLANNING_ONLY"

TASK_MODE = (
    "MILESTONE_17_TASK_6_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_WAIT_STATE_V1_"
    "WAIT_STATE_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-next-phase-option-selection-wait-state-v1")
DOC_PATH = Path("docs/milestone-17-controlled-next-phase-option-selection-wait-state-v1.md")


WAIT_STATE_OPTIONS: tuple[dict[str, Any], ...] = (
    {
        "option_id": "M17-OPT-1",
        "name": "Controlled local solver improvement planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "AWAITING_EXPLICIT_SELECTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-2",
        "name": "Controlled diagnostic evaluation planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "AWAITING_EXPLICIT_SELECTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-3",
        "name": "Controlled primitive expansion planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "AWAITING_EXPLICIT_SELECTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-4",
        "name": "Controlled object-centric reasoning planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "AWAITING_EXPLICIT_SELECTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-5",
        "name": "Controlled submission readiness planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "AWAITING_EXPLICIT_SELECTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
)


WAIT_STATE_CHECKS: tuple[str, ...] = (
    "source_task_5_commit_bound",
    "source_task_5_signature_bound",
    "operator_direction_bound",
    "gate_review_confirmed",
    "wait_state_ready",
    "wait_state_active",
    "wait_state_not_closed",
    "option_selection_gate_open",
    "option_selection_required",
    "option_selection_not_received",
    "available_option_count_is_five",
    "available_option_ids_unique",
    "all_options_await_explicit_selection",
    "all_options_are_planning_only",
    "all_options_selection_allowed",
    "selected_option_none",
    "selected_option_count_zero",
    "selected_option_not_authorized",
    "no_available_option_allows_implementation",
    "no_available_option_allows_runtime",
    "no_available_option_allows_submission",
    "implementation_authorization_not_granted",
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


def build_controlled_next_phase_option_selection_wait_state() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_5_final_baseline_commit": SOURCE_TASK_5_FINAL_BASELINE_COMMIT,
        "source_task_5_final_signature": SOURCE_TASK_5_FINAL_SIGNATURE,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "available_option_count": len(WAIT_STATE_OPTIONS),
        "selected_option_id": "NONE",
        "selected_option_count": 0,
        "option_selection_received": False,
        "wait_state_active": True,
        "wait_state_closed": False,
        "verdict": WAIT_STATE_VERDICT,
        "decision": WAIT_STATE_DECISION,
        "reason": WAIT_STATE_REASON,
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
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-wait-state-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-wait-state-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-wait-state-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-wait-state-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "wait_state_status_marker": WAIT_STATE_STATUS_MARKER,
        "signature": signature,
        "source_task_5_final_baseline_commit": SOURCE_TASK_5_FINAL_BASELINE_COMMIT,
        "source_task_5_final_signature": SOURCE_TASK_5_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": WAIT_STATE_VERDICT,
        "decision": WAIT_STATE_DECISION,
        "wait_state_reason": WAIT_STATE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "operator_direction_received": True,
        "controlled_next_phase_planning_opened": True,
        "controlled_next_phase_option_selection_gate_ready": True,
        "controlled_next_phase_option_selection_gate_review_ready": True,
        "controlled_next_phase_option_selection_wait_state_ready": True,
        "controlled_next_phase_option_selection_wait_state_active": True,
        "controlled_next_phase_option_selection_wait_state_closed": False,
        "option_selection_gate_open": True,
        "option_selection_required": True,
        "option_selection_received": False,
        "available_option_count": len(WAIT_STATE_OPTIONS),
        "wait_state_options": WAIT_STATE_OPTIONS,
        "selected_option_id": "NONE",
        "selected_option_count": 0,
        "selected_option_authorized": False,
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
        "wait_state_check_count": len(WAIT_STATE_CHECKS),
        "wait_state_failure_count": 0,
        "wait_state_checks": WAIT_STATE_CHECKS,
        "artifacts": artifacts,
    }


def validate_controlled_next_phase_option_selection_wait_state(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "wait_state_status_marker": WAIT_STATE_STATUS_MARKER,
        "source_task_5_final_baseline_commit": SOURCE_TASK_5_FINAL_BASELINE_COMMIT,
        "source_task_5_final_signature": SOURCE_TASK_5_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "verdict": WAIT_STATE_VERDICT,
        "decision": WAIT_STATE_DECISION,
        "wait_state_reason": WAIT_STATE_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    options = tuple(status.get("wait_state_options", ()))
    option_ids = [option.get("option_id") for option in options]

    if status.get("available_option_count") != 5:
        issues.append("available_option_count must be 5")
    if len(options) != 5:
        issues.append("wait_state_options length must be 5")
    if len(option_ids) != len(set(option_ids)):
        issues.append("wait_state option_ids must be unique")

    for option in options:
        if option.get("wait_state_status") != "AWAITING_EXPLICIT_SELECTION":
            issues.append(f"{option.get('option_id')} wait_state_status mismatch")
        if option.get("stage") != "PLANNING_ONLY":
            issues.append(f"{option.get('option_id')} must be PLANNING_ONLY")
        if option.get("selection_allowed") is not True:
            issues.append(f"{option.get('option_id')} selection_allowed must be True")
        if option.get("implementation_allowed") is not False:
            issues.append(f"{option.get('option_id')} implementation_allowed must be False")
        if option.get("runtime_allowed") is not False:
            issues.append(f"{option.get('option_id')} runtime_allowed must be False")
        if option.get("submission_allowed") is not False:
            issues.append(f"{option.get('option_id')} submission_allowed must be False")

    required_true = (
        "operator_direction_received",
        "controlled_next_phase_planning_opened",
        "controlled_next_phase_option_selection_gate_ready",
        "controlled_next_phase_option_selection_gate_review_ready",
        "controlled_next_phase_option_selection_wait_state_ready",
        "controlled_next_phase_option_selection_wait_state_active",
        "option_selection_gate_open",
        "option_selection_required",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
    )
    required_false = (
        "controlled_next_phase_option_selection_wait_state_closed",
        "option_selection_received",
        "selected_option_authorized",
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

    if status.get("selected_option_id") != "NONE":
        issues.append("selected_option_id must be NONE")
    if status.get("selected_option_count") != 0:
        issues.append("selected_option_count must be 0")
    if status.get("wait_state_check_count") != len(WAIT_STATE_CHECKS):
        issues.append("wait_state_check_count mismatch")
    if status.get("wait_state_failure_count") != 0:
        issues.append("wait_state_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def wait_state_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["wait_state_status_marker"],
        "signature": status["signature"],
        "source_task_5_final_baseline_commit": status["source_task_5_final_baseline_commit"],
        "source_task_5_final_signature": status["source_task_5_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "operator_direction_value": status["operator_direction_value"],
        "available_option_count": status["available_option_count"],
        "selected_option_id": status["selected_option_id"],
        "option_selection_required": status["option_selection_required"],
        "option_selection_received": status["option_selection_received"],
        "wait_state_active": status["controlled_next_phase_option_selection_wait_state_active"],
        "wait_state_closed": status["controlled_next_phase_option_selection_wait_state_closed"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "real_submission_allowed": status["real_submission_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "wait_state_check_count": status["wait_state_check_count"],
        "wait_state_failure_count": status["wait_state_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    option_lines = "\n".join(
        f"- `{option['option_id']}` — {option['name']} · `{option['stage']}` · `{option['wait_state_status']}`"
        for option in status["wait_state_options"]
    )

    return f"""# Milestone #17 Task 6 - Controlled Next Phase Option Selection Wait State v1

## Status

`{status["wait_state_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 5 final baseline commit: `{status["source_task_5_final_baseline_commit"]}`
- source Task 5 final signature: `{status["source_task_5_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Wait state

- wait_state_ready: `{status["controlled_next_phase_option_selection_wait_state_ready"]}`
- wait_state_active: `{status["controlled_next_phase_option_selection_wait_state_active"]}`
- wait_state_closed: `{status["controlled_next_phase_option_selection_wait_state_closed"]}`
- option_selection_gate_open: `{status["option_selection_gate_open"]}`
- option_selection_required: `{status["option_selection_required"]}`
- option_selection_received: `{status["option_selection_received"]}`
- available_option_count: `{status["available_option_count"]}`
- selected_option_id: `{status["selected_option_id"]}`
- selected_option_count: `{status["selected_option_count"]}`
- selected_option_authorized: `{status["selected_option_authorized"]}`

{option_lines}

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Reason

`{status["wait_state_reason"]}`

## Boundary

- implementation_authorization_granted: `{status["implementation_authorization_granted"]}`
- implementation_authorized: `{status["implementation_authorized"]}`
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
- kaggle_authentication_allowed: `{status["kaggle_authentication_allowed"]}`
- kaggle_submission_sent: `{status["kaggle_submission_sent"]}`
- private_core_exposure: `{status["private_core_exposure"]}`
- legal_certification: `{status["legal_certification"]}`
- fail_closed_required: `{status["fail_closed_required"]}`
- fail_closed_active: `{status["fail_closed_active"]}`

## Validation

- wait_state_check_count: `{status["wait_state_check_count"]}`
- wait_state_failure_count: `{status["wait_state_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["wait_state_status_marker"],
        f"signature={status['signature']}",
        f"source_task_5_final_baseline_commit={status['source_task_5_final_baseline_commit']}",
        f"source_task_5_final_signature={status['source_task_5_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"wait_state_reason={status['wait_state_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"operator_direction_value={status['operator_direction_value']}",
        f"operator_direction_class={status['operator_direction_class']}",
        f"available_option_count={status['available_option_count']}",
        f"wait_state_active={status['controlled_next_phase_option_selection_wait_state_active']}",
        f"wait_state_closed={status['controlled_next_phase_option_selection_wait_state_closed']}",
        f"option_selection_required={status['option_selection_required']}",
        f"option_selection_received={status['option_selection_received']}",
        f"selected_option_id={status['selected_option_id']}",
        f"selected_option_count={status['selected_option_count']}",
        f"selected_option_authorized={status['selected_option_authorized']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"real_submission_allowed={status['real_submission_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"wait_state_check_count={status['wait_state_check_count']}",
        f"wait_state_failure_count={status['wait_state_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_controlled_next_phase_option_selection_wait_state_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_next_phase_option_selection_wait_state()
    issues = validate_controlled_next_phase_option_selection_wait_state(resolved)
    if issues:
        raise ValueError("Invalid controlled next phase option selection wait state: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = wait_state_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-wait-state-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-wait-state-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-wait-state-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-wait-state-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_next_phase_option_selection_wait_state_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_5_final_baseline_commit"])
    print(status["task_mode"])
    print(status["wait_state_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["wait_state_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_5_final_baseline_commit",
        "source_task_5_final_signature",
        "operator_direction_raw",
        "operator_direction_value",
        "operator_direction_class",
        "operator_direction_received",
        "controlled_next_phase_planning_opened",
        "controlled_next_phase_option_selection_gate_ready",
        "controlled_next_phase_option_selection_gate_review_ready",
        "controlled_next_phase_option_selection_wait_state_ready",
        "controlled_next_phase_option_selection_wait_state_active",
        "controlled_next_phase_option_selection_wait_state_closed",
        "option_selection_gate_open",
        "option_selection_required",
        "option_selection_received",
        "available_option_count",
        "selected_option_id",
        "selected_option_count",
        "selected_option_authorized",
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
        "wait_state_check_count",
        "wait_state_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for option in status["wait_state_options"]:
        print(f"wait_state_option={option['option_id']}|{option['stage']}|{option['wait_state_status']}|{option['name']}")
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
