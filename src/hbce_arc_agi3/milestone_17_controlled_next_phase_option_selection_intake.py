"""Milestone #17 Task 7 - Controlled Next Phase Option Selection Intake v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_7_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_INTAKE_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

SELECTION_INTAKE_STATUS_MARKER = "MILESTONE_17_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_INTAKE_READY"
SELECTION_INTAKE_VERDICT = "CONTROLLED_NEXT_PHASE_OPTION_SELECTION_INTAKE_ACCEPTED_PLANNING_ONLY"
SELECTION_INTAKE_DECISION = "ACCEPT_M17_OPT_1_FOR_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING_ONLY"
SELECTION_INTAKE_REASON = "EXPLICIT_OPERATOR_SELECTED_M17_OPT_1_FROM_TASK_6_WAIT_STATE"

PREVIOUS_STAGE = "MILESTONE_17_TASK_6_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_WAIT_STATE_V1"
NEXT_STAGE = "MILESTONE_17_TASK_8_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_INTAKE_REVIEW_V1"

SOURCE_TASK_6_FINAL_BASELINE_COMMIT = "7320fb1"
SOURCE_TASK_6_FINAL_SIGNATURE = "677D8B81D0D0FD16"

OPERATOR_SELECTION_RAW = "M17-OPT-1 Controlled local solver improvement planning"
SELECTED_OPTION_ID = "M17-OPT-1"
SELECTED_OPTION_NAME = "Controlled local solver improvement planning"
SELECTED_OPTION_VALUE = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING"
SELECTED_OPTION_CLASS = "CONTROLLED_PLANNING_ONLY"

TASK_MODE = (
    "MILESTONE_17_TASK_7_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_INTAKE_V1_"
    "SELECTION_INTAKE_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-next-phase-option-selection-intake-v1")
DOC_PATH = Path("docs/milestone-17-controlled-next-phase-option-selection-intake-v1.md")


AVAILABLE_OPTIONS: tuple[dict[str, Any], ...] = (
    {
        "option_id": "M17-OPT-1",
        "name": "Controlled local solver improvement planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "SELECTED_BY_EXPLICIT_OPERATOR",
        "selection_received": True,
        "selection_allowed": True,
        "selected": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-2",
        "name": "Controlled diagnostic evaluation planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "NOT_SELECTED",
        "selection_received": False,
        "selection_allowed": True,
        "selected": False,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-3",
        "name": "Controlled primitive expansion planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "NOT_SELECTED",
        "selection_received": False,
        "selection_allowed": True,
        "selected": False,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-4",
        "name": "Controlled object-centric reasoning planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "NOT_SELECTED",
        "selection_received": False,
        "selection_allowed": True,
        "selected": False,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-5",
        "name": "Controlled submission readiness planning",
        "stage": "PLANNING_ONLY",
        "wait_state_status": "NOT_SELECTED",
        "selection_received": False,
        "selection_allowed": True,
        "selected": False,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
)


SELECTION_INTAKE_CHECKS: tuple[str, ...] = (
    "source_task_6_commit_bound",
    "source_task_6_signature_bound",
    "operator_selection_raw_bound",
    "selected_option_id_is_m17_opt_1",
    "selected_option_name_bound",
    "selected_option_value_bound",
    "selected_option_class_planning_only",
    "wait_state_was_active",
    "wait_state_was_not_closed",
    "option_selection_required",
    "option_selection_received",
    "available_option_count_is_five",
    "available_option_ids_unique",
    "exactly_one_option_selected",
    "selected_option_authorized_for_planning_only",
    "selected_option_not_authorized_for_implementation",
    "selected_option_not_authorized_for_runtime",
    "selected_option_not_authorized_for_submission",
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


def build_controlled_next_phase_option_selection_intake() -> dict[str, Any]:
    selected_options = [option for option in AVAILABLE_OPTIONS if option["selected"]]

    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_6_final_baseline_commit": SOURCE_TASK_6_FINAL_BASELINE_COMMIT,
        "source_task_6_final_signature": SOURCE_TASK_6_FINAL_SIGNATURE,
        "operator_selection_raw": OPERATOR_SELECTION_RAW,
        "selected_option_id": SELECTED_OPTION_ID,
        "selected_option_name": SELECTED_OPTION_NAME,
        "selected_option_value": SELECTED_OPTION_VALUE,
        "selected_option_class": SELECTED_OPTION_CLASS,
        "selected_option_count": len(selected_options),
        "selection_intake_verdict": SELECTION_INTAKE_VERDICT,
        "selection_intake_decision": SELECTION_INTAKE_DECISION,
        "selection_intake_reason": SELECTION_INTAKE_REASON,
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
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-intake-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-intake-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-intake-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-intake-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "selection_intake_status_marker": SELECTION_INTAKE_STATUS_MARKER,
        "signature": signature,
        "source_task_6_final_baseline_commit": SOURCE_TASK_6_FINAL_BASELINE_COMMIT,
        "source_task_6_final_signature": SOURCE_TASK_6_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": SELECTION_INTAKE_VERDICT,
        "decision": SELECTION_INTAKE_DECISION,
        "selection_intake_reason": SELECTION_INTAKE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_selection_raw": OPERATOR_SELECTION_RAW,
        "selected_option_id": SELECTED_OPTION_ID,
        "selected_option_name": SELECTED_OPTION_NAME,
        "selected_option_value": SELECTED_OPTION_VALUE,
        "selected_option_class": SELECTED_OPTION_CLASS,
        "controlled_next_phase_option_selection_wait_state_ready": True,
        "controlled_next_phase_option_selection_wait_state_active": True,
        "controlled_next_phase_option_selection_wait_state_closed": False,
        "controlled_next_phase_option_selection_intake_ready": True,
        "controlled_next_phase_option_selection_intake_passed": True,
        "controlled_next_phase_option_selection_intake_closed": True,
        "option_selection_gate_open": True,
        "option_selection_required": True,
        "option_selection_received": True,
        "available_option_count": len(AVAILABLE_OPTIONS),
        "available_options": AVAILABLE_OPTIONS,
        "selected_option_count": len(selected_options),
        "selected_option_authorized": True,
        "selected_option_authorization_scope": "PLANNING_ONLY",
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
        "selection_intake_check_count": len(SELECTION_INTAKE_CHECKS),
        "selection_intake_failure_count": 0,
        "selection_intake_checks": SELECTION_INTAKE_CHECKS,
        "artifacts": artifacts,
    }


def validate_controlled_next_phase_option_selection_intake(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "selection_intake_status_marker": SELECTION_INTAKE_STATUS_MARKER,
        "source_task_6_final_baseline_commit": SOURCE_TASK_6_FINAL_BASELINE_COMMIT,
        "source_task_6_final_signature": SOURCE_TASK_6_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_selection_raw": OPERATOR_SELECTION_RAW,
        "selected_option_id": SELECTED_OPTION_ID,
        "selected_option_name": SELECTED_OPTION_NAME,
        "selected_option_value": SELECTED_OPTION_VALUE,
        "selected_option_class": SELECTED_OPTION_CLASS,
        "verdict": SELECTION_INTAKE_VERDICT,
        "decision": SELECTION_INTAKE_DECISION,
        "selection_intake_reason": SELECTION_INTAKE_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    options = tuple(status.get("available_options", ()))
    selected_options = [option for option in options if option.get("selected") is True]
    option_ids = [option.get("option_id") for option in options]

    if status.get("available_option_count") != 5:
        issues.append("available_option_count must be 5")
    if len(options) != 5:
        issues.append("available_options length must be 5")
    if len(option_ids) != len(set(option_ids)):
        issues.append("available option_ids must be unique")
    if len(selected_options) != 1:
        issues.append("exactly one option must be selected")
    if selected_options and selected_options[0].get("option_id") != SELECTED_OPTION_ID:
        issues.append("selected option must be M17-OPT-1")

    for option in options:
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
        "controlled_next_phase_option_selection_wait_state_ready",
        "controlled_next_phase_option_selection_wait_state_active",
        "controlled_next_phase_option_selection_intake_ready",
        "controlled_next_phase_option_selection_intake_passed",
        "controlled_next_phase_option_selection_intake_closed",
        "option_selection_gate_open",
        "option_selection_required",
        "option_selection_received",
        "selected_option_authorized",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
    )
    required_false = (
        "controlled_next_phase_option_selection_wait_state_closed",
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

    if status.get("selected_option_count") != 1:
        issues.append("selected_option_count must be 1")
    if status.get("selected_option_authorization_scope") != "PLANNING_ONLY":
        issues.append("selected_option_authorization_scope must be PLANNING_ONLY")
    if status.get("selection_intake_check_count") != len(SELECTION_INTAKE_CHECKS):
        issues.append("selection_intake_check_count mismatch")
    if status.get("selection_intake_failure_count") != 0:
        issues.append("selection_intake_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def selection_intake_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["selection_intake_status_marker"],
        "signature": status["signature"],
        "source_task_6_final_baseline_commit": status["source_task_6_final_baseline_commit"],
        "source_task_6_final_signature": status["source_task_6_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "operator_selection_raw": status["operator_selection_raw"],
        "selected_option_id": status["selected_option_id"],
        "selected_option_name": status["selected_option_name"],
        "selected_option_value": status["selected_option_value"],
        "selected_option_class": status["selected_option_class"],
        "selected_option_count": status["selected_option_count"],
        "selected_option_authorization_scope": status["selected_option_authorization_scope"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "real_submission_allowed": status["real_submission_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "selection_intake_check_count": status["selection_intake_check_count"],
        "selection_intake_failure_count": status["selection_intake_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    option_lines = "\n".join(
        f"- `{option['option_id']}` — {option['name']} · selected=`{option['selected']}` · `{option['wait_state_status']}`"
        for option in status["available_options"]
    )

    return f"""# Milestone #17 Task 7 - Controlled Next Phase Option Selection Intake v1

## Status

`{status["selection_intake_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 6 final baseline commit: `{status["source_task_6_final_baseline_commit"]}`
- source Task 6 final signature: `{status["source_task_6_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Operator selection

- raw: `{status["operator_selection_raw"]}`
- selected_option_id: `{status["selected_option_id"]}`
- selected_option_name: `{status["selected_option_name"]}`
- selected_option_value: `{status["selected_option_value"]}`
- selected_option_class: `{status["selected_option_class"]}`
- selected_option_count: `{status["selected_option_count"]}`
- selected_option_authorized: `{status["selected_option_authorized"]}`
- selected_option_authorization_scope: `{status["selected_option_authorization_scope"]}`

{option_lines}

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Reason

`{status["selection_intake_reason"]}`

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

- selection_intake_check_count: `{status["selection_intake_check_count"]}`
- selection_intake_failure_count: `{status["selection_intake_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["selection_intake_status_marker"],
        f"signature={status['signature']}",
        f"source_task_6_final_baseline_commit={status['source_task_6_final_baseline_commit']}",
        f"source_task_6_final_signature={status['source_task_6_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"selection_intake_reason={status['selection_intake_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"operator_selection_raw={status['operator_selection_raw']}",
        f"selected_option_id={status['selected_option_id']}",
        f"selected_option_name={status['selected_option_name']}",
        f"selected_option_value={status['selected_option_value']}",
        f"selected_option_class={status['selected_option_class']}",
        f"selected_option_count={status['selected_option_count']}",
        f"selected_option_authorized={status['selected_option_authorized']}",
        f"selected_option_authorization_scope={status['selected_option_authorization_scope']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"real_submission_allowed={status['real_submission_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"selection_intake_check_count={status['selection_intake_check_count']}",
        f"selection_intake_failure_count={status['selection_intake_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_controlled_next_phase_option_selection_intake_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_next_phase_option_selection_intake()
    issues = validate_controlled_next_phase_option_selection_intake(resolved)
    if issues:
        raise ValueError("Invalid controlled next phase option selection intake: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = selection_intake_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-intake-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-intake-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-intake-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-intake-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_next_phase_option_selection_intake_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_6_final_baseline_commit"])
    print(status["task_mode"])
    print(status["selection_intake_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["selection_intake_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_6_final_baseline_commit",
        "source_task_6_final_signature",
        "operator_selection_raw",
        "selected_option_id",
        "selected_option_name",
        "selected_option_value",
        "selected_option_class",
        "controlled_next_phase_option_selection_wait_state_ready",
        "controlled_next_phase_option_selection_wait_state_active",
        "controlled_next_phase_option_selection_wait_state_closed",
        "controlled_next_phase_option_selection_intake_ready",
        "controlled_next_phase_option_selection_intake_passed",
        "controlled_next_phase_option_selection_intake_closed",
        "option_selection_gate_open",
        "option_selection_required",
        "option_selection_received",
        "available_option_count",
        "selected_option_count",
        "selected_option_authorized",
        "selected_option_authorization_scope",
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
        "selection_intake_check_count",
        "selection_intake_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for option in status["available_options"]:
        print(f"available_option={option['option_id']}|selected={option['selected']}|{option['wait_state_status']}|{option['name']}")
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
