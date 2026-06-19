"""Milestone #17 Task 4 - Controlled Next Phase Option Selection Gate v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_4_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

OPTION_SELECTION_GATE_STATUS_MARKER = "MILESTONE_17_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_READY"
OPTION_SELECTION_GATE_VERDICT = "CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_READY_NO_OPTION_SELECTED"
OPTION_SELECTION_GATE_DECISION = "OPEN_OPTION_SELECTION_GATE_NO_IMPLEMENTATION_ALLOWED"
OPTION_SELECTION_GATE_REASON = "TASK_3_OPTIONS_REVIEW_CONFIRMED_NO_OPTION_SELECTED"

PREVIOUS_STAGE = "MILESTONE_17_TASK_3_CONTROLLED_NEXT_PHASE_OPTIONS_REVIEW_V1"
NEXT_STAGE = "MILESTONE_17_TASK_5_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_REVIEW_V1"

SOURCE_TASK_3_FINAL_BASELINE_COMMIT = "bc3c8fd"
SOURCE_TASK_3_FINAL_SIGNATURE = "52381D60053A3A36"

OPERATOR_DIRECTION_RAW = "ok prosegui"
OPERATOR_DIRECTION_VALUE = "PROCEED_TO_CONTROLLED_NEXT_PHASE_PLANNING"
OPERATOR_DIRECTION_CLASS = "CONTROLLED_PLANNING_ONLY"

TASK_MODE = (
    "MILESTONE_17_TASK_4_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_V1_"
    "OPTION_SELECTION_GATE_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-next-phase-option-selection-gate-v1")
DOC_PATH = Path("docs/milestone-17-controlled-next-phase-option-selection-gate-v1.md")


AVAILABLE_OPTIONS: tuple[dict[str, Any], ...] = (
    {
        "option_id": "M17-OPT-1",
        "name": "Controlled local solver improvement planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_CONTROLLED_OPTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-2",
        "name": "Controlled diagnostic evaluation planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_CONTROLLED_OPTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-3",
        "name": "Controlled primitive expansion planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_CONTROLLED_OPTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-4",
        "name": "Controlled object-centric reasoning planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_CONTROLLED_OPTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-5",
        "name": "Controlled submission readiness planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_CONTROLLED_OPTION",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
)


OPTION_SELECTION_GATE_CHECKS: tuple[str, ...] = (
    "source_task_3_commit_bound",
    "source_task_3_signature_bound",
    "operator_direction_bound",
    "options_review_confirmed",
    "available_option_count_is_five",
    "available_option_ids_unique",
    "all_available_options_confirmed",
    "all_available_options_are_planning_only",
    "selection_gate_ready",
    "selection_gate_passed",
    "selection_gate_closed",
    "selection_gate_open_for_operator_choice",
    "selection_required",
    "selection_not_received",
    "selected_option_none",
    "selected_option_count_zero",
    "no_option_selection_authorization",
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


def build_controlled_next_phase_option_selection_gate() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_3_final_baseline_commit": SOURCE_TASK_3_FINAL_BASELINE_COMMIT,
        "source_task_3_final_signature": SOURCE_TASK_3_FINAL_SIGNATURE,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "available_option_count": len(AVAILABLE_OPTIONS),
        "selected_option_id": "NONE",
        "selected_option_count": 0,
        "verdict": OPTION_SELECTION_GATE_VERDICT,
        "decision": OPTION_SELECTION_GATE_DECISION,
        "reason": OPTION_SELECTION_GATE_REASON,
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
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "option_selection_gate_status_marker": OPTION_SELECTION_GATE_STATUS_MARKER,
        "signature": signature,
        "source_task_3_final_baseline_commit": SOURCE_TASK_3_FINAL_BASELINE_COMMIT,
        "source_task_3_final_signature": SOURCE_TASK_3_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": OPTION_SELECTION_GATE_VERDICT,
        "decision": OPTION_SELECTION_GATE_DECISION,
        "option_selection_gate_reason": OPTION_SELECTION_GATE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "operator_direction_received": True,
        "controlled_next_phase_planning_opened": True,
        "controlled_next_phase_options_index_ready": True,
        "controlled_next_phase_options_review_ready": True,
        "controlled_next_phase_option_selection_gate_ready": True,
        "controlled_next_phase_option_selection_gate_passed": True,
        "controlled_next_phase_option_selection_gate_closed": True,
        "option_selection_gate_open": True,
        "option_selection_required": True,
        "option_selection_received": False,
        "available_option_count": len(AVAILABLE_OPTIONS),
        "available_options": AVAILABLE_OPTIONS,
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
        "option_selection_gate_check_count": len(OPTION_SELECTION_GATE_CHECKS),
        "option_selection_gate_failure_count": 0,
        "option_selection_gate_checks": OPTION_SELECTION_GATE_CHECKS,
        "artifacts": artifacts,
    }


def validate_controlled_next_phase_option_selection_gate(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "option_selection_gate_status_marker": OPTION_SELECTION_GATE_STATUS_MARKER,
        "source_task_3_final_baseline_commit": SOURCE_TASK_3_FINAL_BASELINE_COMMIT,
        "source_task_3_final_signature": SOURCE_TASK_3_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "verdict": OPTION_SELECTION_GATE_VERDICT,
        "decision": OPTION_SELECTION_GATE_DECISION,
        "option_selection_gate_reason": OPTION_SELECTION_GATE_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    options = tuple(status.get("available_options", ()))
    option_ids = [option.get("option_id") for option in options]

    if status.get("available_option_count") != 5:
        issues.append("available_option_count must be 5")
    if len(options) != 5:
        issues.append("available_options length must be 5")
    if len(option_ids) != len(set(option_ids)):
        issues.append("available option_ids must be unique")

    for option in options:
        if option.get("review_status") != "CONFIRMED_CONTROLLED_OPTION":
            issues.append(f"{option.get('option_id')} review_status mismatch")
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
        "controlled_next_phase_options_index_ready",
        "controlled_next_phase_options_review_ready",
        "controlled_next_phase_option_selection_gate_ready",
        "controlled_next_phase_option_selection_gate_passed",
        "controlled_next_phase_option_selection_gate_closed",
        "option_selection_gate_open",
        "option_selection_required",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
    )
    required_false = (
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
    if status.get("option_selection_gate_check_count") != len(OPTION_SELECTION_GATE_CHECKS):
        issues.append("option_selection_gate_check_count mismatch")
    if status.get("option_selection_gate_failure_count") != 0:
        issues.append("option_selection_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def option_selection_gate_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["option_selection_gate_status_marker"],
        "signature": status["signature"],
        "source_task_3_final_baseline_commit": status["source_task_3_final_baseline_commit"],
        "source_task_3_final_signature": status["source_task_3_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "operator_direction_value": status["operator_direction_value"],
        "available_option_count": status["available_option_count"],
        "selected_option_id": status["selected_option_id"],
        "option_selection_required": status["option_selection_required"],
        "option_selection_received": status["option_selection_received"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "real_submission_allowed": status["real_submission_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "option_selection_gate_check_count": status["option_selection_gate_check_count"],
        "option_selection_gate_failure_count": status["option_selection_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    option_lines = "\n".join(
        f"- `{option['option_id']}` — {option['name']} · `{option['stage']}` · selection_allowed=`{option['selection_allowed']}`"
        for option in status["available_options"]
    )

    return f"""# Milestone #17 Task 4 - Controlled Next Phase Option Selection Gate v1

## Status

`{status["option_selection_gate_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 3 final baseline commit: `{status["source_task_3_final_baseline_commit"]}`
- source Task 3 final signature: `{status["source_task_3_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Operator direction

- raw: `{status["operator_direction_raw"]}`
- value: `{status["operator_direction_value"]}`
- class: `{status["operator_direction_class"]}`

## Selection gate

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

`{status["option_selection_gate_reason"]}`

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

- option_selection_gate_check_count: `{status["option_selection_gate_check_count"]}`
- option_selection_gate_failure_count: `{status["option_selection_gate_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["option_selection_gate_status_marker"],
        f"signature={status['signature']}",
        f"source_task_3_final_baseline_commit={status['source_task_3_final_baseline_commit']}",
        f"source_task_3_final_signature={status['source_task_3_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"option_selection_gate_reason={status['option_selection_gate_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"operator_direction_value={status['operator_direction_value']}",
        f"operator_direction_class={status['operator_direction_class']}",
        f"available_option_count={status['available_option_count']}",
        f"option_selection_gate_open={status['option_selection_gate_open']}",
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
        f"option_selection_gate_check_count={status['option_selection_gate_check_count']}",
        f"option_selection_gate_failure_count={status['option_selection_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_controlled_next_phase_option_selection_gate_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_next_phase_option_selection_gate()
    issues = validate_controlled_next_phase_option_selection_gate(resolved)
    if issues:
        raise ValueError("Invalid controlled next phase option selection gate: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = option_selection_gate_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_next_phase_option_selection_gate_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_3_final_baseline_commit"])
    print(status["task_mode"])
    print(status["option_selection_gate_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["option_selection_gate_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_3_final_baseline_commit",
        "source_task_3_final_signature",
        "operator_direction_raw",
        "operator_direction_value",
        "operator_direction_class",
        "operator_direction_received",
        "controlled_next_phase_planning_opened",
        "controlled_next_phase_options_index_ready",
        "controlled_next_phase_options_review_ready",
        "controlled_next_phase_option_selection_gate_ready",
        "controlled_next_phase_option_selection_gate_passed",
        "controlled_next_phase_option_selection_gate_closed",
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
        "option_selection_gate_check_count",
        "option_selection_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for option in status["available_options"]:
        print(f"available_option={option['option_id']}|{option['stage']}|selection_allowed={option['selection_allowed']}|{option['name']}")
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
