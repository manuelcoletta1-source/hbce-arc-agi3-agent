"""Milestone #17 Task 5 - Controlled Next Phase Option Selection Gate Review v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_5_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_REVIEW_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

GATE_REVIEW_STATUS_MARKER = "MILESTONE_17_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_REVIEW_READY"
GATE_REVIEW_VERDICT = "CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_REVIEW_PASS_NO_OPTION_SELECTED"
GATE_REVIEW_DECISION = "CONFIRM_OPTION_SELECTION_GATE_OPEN_NO_IMPLEMENTATION_ALLOWED"
GATE_REVIEW_REASON = "TASK_4_OPTION_SELECTION_GATE_CONFIRMED_OPEN_SELECTION_REQUIRED"

PREVIOUS_STAGE = "MILESTONE_17_TASK_4_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_V1"
NEXT_STAGE = "MILESTONE_17_TASK_6_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_WAIT_STATE_V1"

SOURCE_TASK_4_FINAL_BASELINE_COMMIT = "61b4c69"
SOURCE_TASK_4_FINAL_SIGNATURE = "E8D73B451B842D65"

OPERATOR_DIRECTION_RAW = "ok prosegui"
OPERATOR_DIRECTION_VALUE = "PROCEED_TO_CONTROLLED_NEXT_PHASE_PLANNING"
OPERATOR_DIRECTION_CLASS = "CONTROLLED_PLANNING_ONLY"

TASK_MODE = (
    "MILESTONE_17_TASK_5_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_GATE_REVIEW_V1_"
    "OPTION_SELECTION_GATE_REVIEW_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-next-phase-option-selection-gate-review-v1")
DOC_PATH = Path("docs/milestone-17-controlled-next-phase-option-selection-gate-review-v1.md")


REVIEWED_AVAILABLE_OPTIONS: tuple[dict[str, Any], ...] = (
    {
        "option_id": "M17-OPT-1",
        "name": "Controlled local solver improvement planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_SELECTION_CANDIDATE",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-2",
        "name": "Controlled diagnostic evaluation planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_SELECTION_CANDIDATE",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-3",
        "name": "Controlled primitive expansion planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_SELECTION_CANDIDATE",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-4",
        "name": "Controlled object-centric reasoning planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_SELECTION_CANDIDATE",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "option_id": "M17-OPT-5",
        "name": "Controlled submission readiness planning",
        "stage": "PLANNING_ONLY",
        "review_status": "CONFIRMED_SELECTION_CANDIDATE",
        "selection_allowed": True,
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
)


GATE_REVIEW_CHECKS: tuple[str, ...] = (
    "source_task_4_commit_bound",
    "source_task_4_signature_bound",
    "operator_direction_bound",
    "option_selection_gate_confirmed",
    "available_option_count_is_five",
    "available_option_ids_unique",
    "all_available_options_confirmed_as_selection_candidates",
    "all_available_options_are_planning_only",
    "selection_gate_review_ready",
    "selection_gate_review_passed",
    "selection_gate_review_closed",
    "option_selection_gate_open_confirmed",
    "option_selection_required_confirmed",
    "option_selection_not_received_confirmed",
    "selected_option_none_confirmed",
    "selected_option_count_zero_confirmed",
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


def build_controlled_next_phase_option_selection_gate_review() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_4_final_baseline_commit": SOURCE_TASK_4_FINAL_BASELINE_COMMIT,
        "source_task_4_final_signature": SOURCE_TASK_4_FINAL_SIGNATURE,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "available_option_count": len(REVIEWED_AVAILABLE_OPTIONS),
        "selected_option_id": "NONE",
        "selected_option_count": 0,
        "option_selection_received": False,
        "verdict": GATE_REVIEW_VERDICT,
        "decision": GATE_REVIEW_DECISION,
        "reason": GATE_REVIEW_REASON,
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
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-review-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-review-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-review-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-review-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "gate_review_status_marker": GATE_REVIEW_STATUS_MARKER,
        "signature": signature,
        "source_task_4_final_baseline_commit": SOURCE_TASK_4_FINAL_BASELINE_COMMIT,
        "source_task_4_final_signature": SOURCE_TASK_4_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": GATE_REVIEW_VERDICT,
        "decision": GATE_REVIEW_DECISION,
        "gate_review_reason": GATE_REVIEW_REASON,
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
        "controlled_next_phase_option_selection_gate_review_ready": True,
        "controlled_next_phase_option_selection_gate_review_passed": True,
        "controlled_next_phase_option_selection_gate_review_closed": True,
        "option_selection_gate_open": True,
        "option_selection_required": True,
        "option_selection_received": False,
        "available_option_count": len(REVIEWED_AVAILABLE_OPTIONS),
        "reviewed_available_options": REVIEWED_AVAILABLE_OPTIONS,
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
        "gate_review_check_count": len(GATE_REVIEW_CHECKS),
        "gate_review_failure_count": 0,
        "gate_review_checks": GATE_REVIEW_CHECKS,
        "artifacts": artifacts,
    }


def validate_controlled_next_phase_option_selection_gate_review(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "gate_review_status_marker": GATE_REVIEW_STATUS_MARKER,
        "source_task_4_final_baseline_commit": SOURCE_TASK_4_FINAL_BASELINE_COMMIT,
        "source_task_4_final_signature": SOURCE_TASK_4_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_raw": OPERATOR_DIRECTION_RAW,
        "operator_direction_value": OPERATOR_DIRECTION_VALUE,
        "operator_direction_class": OPERATOR_DIRECTION_CLASS,
        "verdict": GATE_REVIEW_VERDICT,
        "decision": GATE_REVIEW_DECISION,
        "gate_review_reason": GATE_REVIEW_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    options = tuple(status.get("reviewed_available_options", ()))
    option_ids = [option.get("option_id") for option in options]

    if status.get("available_option_count") != 5:
        issues.append("available_option_count must be 5")
    if len(options) != 5:
        issues.append("reviewed_available_options length must be 5")
    if len(option_ids) != len(set(option_ids)):
        issues.append("reviewed available option_ids must be unique")

    for option in options:
        if option.get("review_status") != "CONFIRMED_SELECTION_CANDIDATE":
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
        "controlled_next_phase_option_selection_gate_review_ready",
        "controlled_next_phase_option_selection_gate_review_passed",
        "controlled_next_phase_option_selection_gate_review_closed",
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
    if status.get("gate_review_check_count") != len(GATE_REVIEW_CHECKS):
        issues.append("gate_review_check_count mismatch")
    if status.get("gate_review_failure_count") != 0:
        issues.append("gate_review_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def gate_review_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["gate_review_status_marker"],
        "signature": status["signature"],
        "source_task_4_final_baseline_commit": status["source_task_4_final_baseline_commit"],
        "source_task_4_final_signature": status["source_task_4_final_signature"],
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
        "gate_review_check_count": status["gate_review_check_count"],
        "gate_review_failure_count": status["gate_review_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    option_lines = "\n".join(
        f"- `{option['option_id']}` — {option['name']} · `{option['stage']}` · `{option['review_status']}`"
        for option in status["reviewed_available_options"]
    )

    return f"""# Milestone #17 Task 5 - Controlled Next Phase Option Selection Gate Review v1

## Status

`{status["gate_review_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 4 final baseline commit: `{status["source_task_4_final_baseline_commit"]}`
- source Task 4 final signature: `{status["source_task_4_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Gate review

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

`{status["gate_review_reason"]}`

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

- gate_review_check_count: `{status["gate_review_check_count"]}`
- gate_review_failure_count: `{status["gate_review_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["gate_review_status_marker"],
        f"signature={status['signature']}",
        f"source_task_4_final_baseline_commit={status['source_task_4_final_baseline_commit']}",
        f"source_task_4_final_signature={status['source_task_4_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"gate_review_reason={status['gate_review_reason']}",
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
        f"gate_review_check_count={status['gate_review_check_count']}",
        f"gate_review_failure_count={status['gate_review_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_controlled_next_phase_option_selection_gate_review_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_next_phase_option_selection_gate_review()
    issues = validate_controlled_next_phase_option_selection_gate_review(resolved)
    if issues:
        raise ValueError("Invalid controlled next phase option selection gate review: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = gate_review_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-review-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-review-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-review-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-next-phase-option-selection-gate-review-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_next_phase_option_selection_gate_review_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_4_final_baseline_commit"])
    print(status["task_mode"])
    print(status["gate_review_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["gate_review_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_4_final_baseline_commit",
        "source_task_4_final_signature",
        "operator_direction_raw",
        "operator_direction_value",
        "operator_direction_class",
        "operator_direction_received",
        "controlled_next_phase_planning_opened",
        "controlled_next_phase_option_selection_gate_ready",
        "controlled_next_phase_option_selection_gate_passed",
        "controlled_next_phase_option_selection_gate_closed",
        "controlled_next_phase_option_selection_gate_review_ready",
        "controlled_next_phase_option_selection_gate_review_passed",
        "controlled_next_phase_option_selection_gate_review_closed",
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
        "gate_review_check_count",
        "gate_review_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for option in status["reviewed_available_options"]:
        print(f"reviewed_available_option={option['option_id']}|{option['stage']}|{option['review_status']}|{option['name']}")
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
