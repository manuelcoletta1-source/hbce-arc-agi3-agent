"""Milestone #17 Task 2 - Controlled Next Phase Options Index v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_2_CONTROLLED_NEXT_PHASE_OPTIONS_INDEX_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

OPTIONS_INDEX_STATUS_MARKER = "MILESTONE_17_CONTROLLED_NEXT_PHASE_OPTIONS_INDEX_READY"
OPTIONS_INDEX_VERDICT = "CONTROLLED_NEXT_PHASE_OPTIONS_INDEX_READY_PLANNING_ONLY"
OPTIONS_INDEX_DECISION = "INDEX_CONTROLLED_NEXT_PHASE_OPTIONS_NO_IMPLEMENTATION_ALLOWED"
OPTIONS_INDEX_REASON = "TASK_1_OPERATOR_DIRECTION_ACCEPTED_FOR_CONTROLLED_PLANNING_ONLY"

PREVIOUS_STAGE = "MILESTONE_17_TASK_1_OPERATOR_DIRECTION_GATE_INTAKE_V1"
NEXT_STAGE = "MILESTONE_17_TASK_3_CONTROLLED_NEXT_PHASE_OPTIONS_REVIEW_V1"

SOURCE_TASK_1_FINAL_BASELINE_COMMIT = "c0c771b"
SOURCE_TASK_1_FINAL_SIGNATURE = "A5CFBFD5F492BE49"

OPERATOR_DIRECTION_RAW = "ok prosegui"
OPERATOR_DIRECTION_VALUE = "PROCEED_TO_CONTROLLED_NEXT_PHASE_PLANNING"
OPERATOR_DIRECTION_CLASS = "CONTROLLED_PLANNING_ONLY"

TASK_MODE = (
    "MILESTONE_17_TASK_2_CONTROLLED_NEXT_PHASE_OPTIONS_INDEX_V1_"
    "OPTIONS_INDEX_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-next-phase-options-index-v1")
DOC_PATH = Path("docs/milestone-17-controlled-next-phase-options-index-v1.md")


CONTROLLED_OPTIONS: tuple[dict[str, Any], ...] = (
    {
        "option_id": "M17-OPT-1",
        "name": "Controlled local solver improvement planning",
        "stage": "PLANNING_ONLY",
        "description": "Prepare a controlled plan for local solver improvements without runtime wiring.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-2",
        "name": "Controlled diagnostic evaluation planning",
        "stage": "PLANNING_ONLY",
        "description": "Prepare local diagnostic evaluation planning without real Kaggle evaluation.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-3",
        "name": "Controlled primitive expansion planning",
        "stage": "PLANNING_ONLY",
        "description": "Prepare a safe index for future transformation primitive expansion.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-4",
        "name": "Controlled object-centric reasoning planning",
        "stage": "PLANNING_ONLY",
        "description": "Prepare object-centric reasoning planning without modifying runtime solver behavior.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-5",
        "name": "Controlled submission readiness planning",
        "stage": "PLANNING_ONLY",
        "description": "Prepare non-upload readiness planning while keeping Kaggle submission blocked.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
)


OPTIONS_INDEX_CHECKS: tuple[str, ...] = (
    "source_task_1_commit_bound",
    "source_task_1_signature_bound",
    "operator_direction_value_bound",
    "operator_direction_class_controlled_planning_only",
    "controlled_option_count_is_five",
    "option_ids_unique",
    "all_options_are_planning_only",
    "no_option_allows_implementation",
    "no_option_allows_runtime",
    "no_option_allows_submission",
    "controlled_next_phase_options_index_ready",
    "controlled_next_phase_options_index_passed",
    "controlled_next_phase_options_index_closed",
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


def build_controlled_next_phase_options_index() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_1_final_baseline_commit": SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
        "source_task_1_final_signature": SOURCE_TASK_1_FINAL_SIGNATURE,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "controlled_option_count": len(CONTROLLED_OPTIONS),
        "verdict": OPTIONS_INDEX_VERDICT,
        "decision": OPTIONS_INDEX_DECISION,
        "reason": OPTIONS_INDEX_REASON,
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
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-options-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-options-index-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-options-index-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-options-index-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "options_index_status_marker": OPTIONS_INDEX_STATUS_MARKER,
        "signature": signature,
        "source_task_1_final_baseline_commit": SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
        "source_task_1_final_signature": SOURCE_TASK_1_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": OPTIONS_INDEX_VERDICT,
        "decision": OPTIONS_INDEX_DECISION,
        "options_index_reason": OPTIONS_INDEX_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "operator_direction_received": True,
        "controlled_next_phase_planning_opened": True,
        "controlled_next_phase_options_index_ready": True,
        "controlled_next_phase_options_index_passed": True,
        "controlled_next_phase_options_index_closed": True,
        "controlled_option_count": len(CONTROLLED_OPTIONS),
        "controlled_options": CONTROLLED_OPTIONS,
        "selected_option_id": "NONE",
        "selected_option_count": 0,
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
        "options_index_check_count": len(OPTIONS_INDEX_CHECKS),
        "options_index_failure_count": 0,
        "options_index_checks": OPTIONS_INDEX_CHECKS,
        "artifacts": artifacts,
    }


def validate_controlled_next_phase_options_index(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "options_index_status_marker": OPTIONS_INDEX_STATUS_MARKER,
        "source_task_1_final_baseline_commit": SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
        "source_task_1_final_signature": SOURCE_TASK_1_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "verdict": OPTIONS_INDEX_VERDICT,
        "decision": OPTIONS_INDEX_DECISION,
        "options_index_reason": OPTIONS_INDEX_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    options = tuple(status.get("controlled_options", ()))
    option_ids = [option.get("option_id") for option in options]

    if status.get("controlled_option_count") != 5:
        issues.append("controlled_option_count must be 5")
    if len(options) != 5:
        issues.append("controlled_options length must be 5")
    if len(option_ids) != len(set(option_ids)):
        issues.append("option_ids must be unique")

    for option in options:
        if option.get("stage") != "PLANNING_ONLY":
            issues.append(f"{option.get('option_id')} must be PLANNING_ONLY")
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
        "controlled_next_phase_options_index_passed",
        "controlled_next_phase_options_index_closed",
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

    if status.get("selected_option_id") != "NONE":
        issues.append("selected_option_id must be NONE")
    if status.get("selected_option_count") != 0:
        issues.append("selected_option_count must be 0")
    if status.get("options_index_check_count") != len(OPTIONS_INDEX_CHECKS):
        issues.append("options_index_check_count mismatch")
    if status.get("options_index_failure_count") != 0:
        issues.append("options_index_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def options_index_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["options_index_status_marker"],
        "signature": status["signature"],
        "source_task_1_final_baseline_commit": status["source_task_1_final_baseline_commit"],
        "source_task_1_final_signature": status["source_task_1_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "operator_direction_value": status["operator_direction_value"],
        "controlled_option_count": status["controlled_option_count"],
        "selected_option_id": status["selected_option_id"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "real_submission_allowed": status["real_submission_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "options_index_check_count": status["options_index_check_count"],
        "options_index_failure_count": status["options_index_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    option_lines = "\n".join(
        f"- `{option['option_id']}` — {option['name']} · `{option['stage']}`"
        for option in status["controlled_options"]
    )

    return f"""# Milestone #17 Task 2 - Controlled Next Phase Options Index v1

## Status

`{status["options_index_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 1 final baseline commit: `{status["source_task_1_final_baseline_commit"]}`
- source Task 1 final signature: `{status["source_task_1_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Operator direction

- raw: `{status["operator_direction_raw"]}`
- value: `{status["operator_direction_value"]}`
- class: `{status["operator_direction_class"]}`

## Controlled options

- controlled_option_count: `{status["controlled_option_count"]}`
- selected_option_id: `{status["selected_option_id"]}`
- selected_option_count: `{status["selected_option_count"]}`

{option_lines}

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Reason

`{status["options_index_reason"]}`

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

- options_index_check_count: `{status["options_index_check_count"]}`
- options_index_failure_count: `{status["options_index_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["options_index_status_marker"],
        f"signature={status['signature']}",
        f"source_task_1_final_baseline_commit={status['source_task_1_final_baseline_commit']}",
        f"source_task_1_final_signature={status['source_task_1_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"options_index_reason={status['options_index_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"operator_direction_value={status['operator_direction_value']}",
        f"operator_direction_class={status['operator_direction_class']}",
        f"controlled_option_count={status['controlled_option_count']}",
        f"selected_option_id={status['selected_option_id']}",
        f"selected_option_count={status['selected_option_count']}",
        f"controlled_next_phase_options_index_ready={status['controlled_next_phase_options_index_ready']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"real_submission_allowed={status['real_submission_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"options_index_check_count={status['options_index_check_count']}",
        f"options_index_failure_count={status['options_index_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_controlled_next_phase_options_index_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_next_phase_options_index()
    issues = validate_controlled_next_phase_options_index(resolved)
    if issues:
        raise ValueError("Invalid controlled next phase options index: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = options_index_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-options-index-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-options-index-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-options-index-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-options-index-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_next_phase_options_index_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_1_final_baseline_commit"])
    print(status["task_mode"])
    print(status["options_index_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["options_index_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_1_final_baseline_commit",
        "source_task_1_final_signature",
        "operator_direction_raw",
        "operator_direction_value",
        "operator_direction_class",
        "operator_direction_received",
        "controlled_next_phase_planning_opened",
        "controlled_next_phase_options_index_ready",
        "controlled_next_phase_options_index_passed",
        "controlled_next_phase_options_index_closed",
        "controlled_option_count",
        "selected_option_id",
        "selected_option_count",
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
        "options_index_check_count",
        "options_index_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for option in status["controlled_options"]:
        print(f"controlled_option={option['option_id']}|{option['stage']}|{option['name']}")
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
