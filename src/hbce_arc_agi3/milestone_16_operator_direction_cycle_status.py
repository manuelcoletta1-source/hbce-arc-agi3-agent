"""Milestone #16 Task 8 - Operator Direction Cycle Status v1.

This module records the current Milestone #16 operator-direction cycle state
after Task 7 closed the wait-state closure while preserving the active wait
state and the implementation block.

Boundary:
- status-only
- local-only
- deterministic
- public-safe
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


TASK_NAME = "MILESTONE_16_TASK_8_OPERATOR_DIRECTION_CYCLE_STATUS_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

CYCLE_STATUS_MARKER = "MILESTONE_16_OPERATOR_DIRECTION_CYCLE_STATUS_READY"
CYCLE_VERDICT = "OPERATOR_DIRECTION_CYCLE_STATUS_PASS_WAIT_STATE_ACTIVE_DECISION_GATE_BLOCKED"
CYCLE_DECISION = "CONFIRM_OPERATOR_DIRECTION_CYCLE_BLOCKED_PENDING_EXPLICIT_OPERATOR_DIRECTION"
BLOCK_REASON = "TASK_7_WAIT_STATE_CLOSURE_CONFIRMED_WAIT_STATE_ACTIVE"

PREVIOUS_STAGE = "MILESTONE_16_TASK_7_OPERATOR_DIRECTION_WAIT_STATE_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_16_TASK_9_OPERATOR_DIRECTION_CYCLE_STATUS_REVIEW_V1"

SOURCE_TASK_7_FINAL_BASELINE_COMMIT = "9b36b35"
SOURCE_TASK_7_FINAL_SIGNATURE = "3940900FE30D3C40"

TASK_MODE = "MILESTONE_16_TASK_8_OPERATOR_DIRECTION_CYCLE_STATUS_V1_STATUS_ONLY_LOCAL_ONLY"

ARTIFACT_DIR = Path("examples/milestone-16/operator-direction-cycle-status-v1")
DOC_PATH = Path("docs/milestone-16-operator-direction-cycle-status-v1.md")

BOUNDARY_FLAGS: dict[str, bool] = {
    "public_safe": True,
    "deterministic": True,
    "local_only": True,
    "status_only": True,
    "closure_only": False,
    "review_only": False,
    "dry_run_only": True,
    "external_api_dependency": False,
    "contains_api_keys": False,
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


DIRECTION_OPTIONS: tuple[dict[str, str], ...] = (
    {
        "id": "DIRECTION_OPTION_1_KEEP_WAIT_STATE_ACTIVE",
        "label": "Keep wait state active",
        "effect": "No implementation, no runtime activation, no real evaluation.",
    },
    {
        "id": "DIRECTION_OPTION_2_AUTHORIZE_STATUS_REVIEW_ONLY",
        "label": "Authorize status review only",
        "effect": "Review artifacts only, no implementation or runtime wiring.",
    },
    {
        "id": "DIRECTION_OPTION_3_AUTHORIZE_IMPLEMENTATION_PLAN_ONLY",
        "label": "Authorize implementation plan only",
        "effect": "Planning artifact only, no code-level runtime modification.",
    },
    {
        "id": "DIRECTION_OPTION_4_AUTHORIZE_LOCAL_RUNTIME_PATCH_CYCLE",
        "label": "Authorize local runtime patch cycle",
        "effect": "Requires explicit operator authorization before any patch.",
    },
    {
        "id": "DIRECTION_OPTION_5_CLOSE_MILESTONE_WITH_BLOCK_ACTIVE",
        "label": "Close milestone with block active",
        "effect": "Milestone closure while preserving implementation block.",
    },
)


@dataclass(frozen=True)
class OperatorDirectionCycleStatus:
    """Canonical status payload for Milestone #16 Task 8."""

    task_name: str
    task_ready_marker: str
    task_valid_marker: str
    pipeline_ready_marker: str
    cycle_status_marker: str
    signature: str
    source_task_7_final_baseline_commit: str
    source_task_7_final_signature: str
    task_mode: str
    verdict: str
    decision: str
    block_reason: str
    previous_stage: str
    next_stage: str

    cycle_status_ready: bool
    cycle_status_passed: bool
    cycle_status_closed: bool
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

    milestone_16_operator_direction_cycle_status_check_count: int
    milestone_16_operator_direction_cycle_status_failure_count: int

    direction_options: tuple[dict[str, str], ...]
    artifacts: tuple[str, ...]


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    """Return deterministic 16-char uppercase signature for the status payload."""
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_cycle_status() -> OperatorDirectionCycleStatus:
    """Build deterministic Milestone #16 Task 8 cycle status."""
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_7_final_baseline_commit": SOURCE_TASK_7_FINAL_BASELINE_COMMIT,
        "source_task_7_final_signature": SOURCE_TASK_7_FINAL_SIGNATURE,
        "verdict": CYCLE_VERDICT,
        "decision": CYCLE_DECISION,
        "block_reason": BLOCK_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "operator_direction_value": "PENDING_EXPLICIT_OPERATOR_DIRECTION",
        "direction_option_count": len(DIRECTION_OPTIONS),
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "real_evaluation_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-v1.md"),
        str(DOC_PATH),
    )

    return OperatorDirectionCycleStatus(
        task_name=TASK_NAME,
        task_ready_marker=TASK_READY_MARKER,
        task_valid_marker=TASK_VALID_MARKER,
        pipeline_ready_marker=PIPELINE_READY_MARKER,
        cycle_status_marker=CYCLE_STATUS_MARKER,
        signature=signature,
        source_task_7_final_baseline_commit=SOURCE_TASK_7_FINAL_BASELINE_COMMIT,
        source_task_7_final_signature=SOURCE_TASK_7_FINAL_SIGNATURE,
        task_mode=TASK_MODE,
        verdict=CYCLE_VERDICT,
        decision=CYCLE_DECISION,
        block_reason=BLOCK_REASON,
        previous_stage=PREVIOUS_STAGE,
        next_stage=NEXT_STAGE,
        cycle_status_ready=True,
        cycle_status_passed=True,
        cycle_status_closed=True,
        wait_state_closure_closed=True,
        wait_state_review_closed=True,
        wait_state_ready=True,
        wait_state_active=True,
        wait_state_closed=False,
        decision_gate_ready=True,
        decision_gate_open=False,
        decision_gate_blocked=True,
        direction_option_count=len(DIRECTION_OPTIONS),
        direction_option_selected=False,
        selected_direction_option_id="NONE",
        selected_direction_option_count=0,
        operator_direction_required=BOUNDARY_FLAGS["operator_direction_required"],
        operator_direction_received=BOUNDARY_FLAGS["operator_direction_received"],
        operator_direction_value="PENDING_EXPLICIT_OPERATOR_DIRECTION",
        operator_decision_required=BOUNDARY_FLAGS["operator_decision_required"],
        operator_decision_received=BOUNDARY_FLAGS["operator_decision_received"],
        explicit_operator_authorization_required=BOUNDARY_FLAGS[
            "explicit_operator_authorization_required"
        ],
        explicit_operator_authorization_received=BOUNDARY_FLAGS[
            "explicit_operator_authorization_received"
        ],
        implementation_authorization_granted=BOUNDARY_FLAGS[
            "implementation_authorization_granted"
        ],
        implementation_authorized=BOUNDARY_FLAGS["implementation_authorized"],
        implementation_blocked=BOUNDARY_FLAGS["implementation_blocked"],
        implementation_performed=BOUNDARY_FLAGS["implementation_performed"],
        implementation_patch_created=BOUNDARY_FLAGS["implementation_patch_created"],
        implementation_patch_applied=BOUNDARY_FLAGS["implementation_patch_applied"],
        runtime_solver_patch_allowed=BOUNDARY_FLAGS["runtime_solver_patch_allowed"],
        runtime_solver_modified=BOUNDARY_FLAGS["runtime_solver_modified"],
        ranker_runtime_patch_allowed=BOUNDARY_FLAGS["ranker_runtime_patch_allowed"],
        ranker_runtime_modified=BOUNDARY_FLAGS["ranker_runtime_modified"],
        candidate_generator_patch_allowed=BOUNDARY_FLAGS[
            "candidate_generator_patch_allowed"
        ],
        candidate_generator_modified=BOUNDARY_FLAGS["candidate_generator_modified"],
        runtime_wiring_allowed=BOUNDARY_FLAGS["runtime_wiring_allowed"],
        runtime_wiring_performed=BOUNDARY_FLAGS["runtime_wiring_performed"],
        runtime_activation_authorized=BOUNDARY_FLAGS[
            "runtime_activation_authorized"
        ],
        runtime_activation_performed=BOUNDARY_FLAGS["runtime_activation_performed"],
        runtime_execution_allowed=BOUNDARY_FLAGS["runtime_execution_allowed"],
        runtime_execution_performed=BOUNDARY_FLAGS["runtime_execution_performed"],
        real_evaluation_allowed=BOUNDARY_FLAGS["real_evaluation_allowed"],
        real_submission_allowed=BOUNDARY_FLAGS["real_submission_allowed"],
        kaggle_submission_sent=BOUNDARY_FLAGS["kaggle_submission_sent"],
        private_core_exposure=BOUNDARY_FLAGS["private_core_exposure"],
        legal_certification=BOUNDARY_FLAGS["legal_certification"],
        milestone_16_operator_direction_cycle_status_check_count=35,
        milestone_16_operator_direction_cycle_status_failure_count=0,
        direction_options=DIRECTION_OPTIONS,
        artifacts=artifacts,
    )


def validate_cycle_status(status: OperatorDirectionCycleStatus) -> list[str]:
    """Validate the cycle status and return issue strings."""
    issues: list[str] = []

    if status.task_name != TASK_NAME:
        issues.append("task_name mismatch")
    if status.task_ready_marker != TASK_READY_MARKER:
        issues.append("task_ready_marker mismatch")
    if status.task_valid_marker != TASK_VALID_MARKER:
        issues.append("task_valid_marker mismatch")
    if status.pipeline_ready_marker != PIPELINE_READY_MARKER:
        issues.append("pipeline_ready_marker mismatch")
    if status.cycle_status_marker != CYCLE_STATUS_MARKER:
        issues.append("cycle_status_marker mismatch")
    if status.source_task_7_final_baseline_commit != SOURCE_TASK_7_FINAL_BASELINE_COMMIT:
        issues.append("source_task_7_final_baseline_commit mismatch")
    if status.source_task_7_final_signature != SOURCE_TASK_7_FINAL_SIGNATURE:
        issues.append("source_task_7_final_signature mismatch")
    if status.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage mismatch")
    if status.next_stage != NEXT_STAGE:
        issues.append("next_stage mismatch")
    if status.verdict != CYCLE_VERDICT:
        issues.append("verdict mismatch")
    if status.decision != CYCLE_DECISION:
        issues.append("decision mismatch")
    if status.block_reason != BLOCK_REASON:
        issues.append("block_reason mismatch")

    required_true = {
        "cycle_status_ready": status.cycle_status_ready,
        "cycle_status_passed": status.cycle_status_passed,
        "cycle_status_closed": status.cycle_status_closed,
        "wait_state_closure_closed": status.wait_state_closure_closed,
        "wait_state_review_closed": status.wait_state_review_closed,
        "wait_state_ready": status.wait_state_ready,
        "wait_state_active": status.wait_state_active,
        "decision_gate_ready": status.decision_gate_ready,
        "decision_gate_blocked": status.decision_gate_blocked,
        "operator_direction_required": status.operator_direction_required,
        "operator_decision_required": status.operator_decision_required,
        "explicit_operator_authorization_required": (
            status.explicit_operator_authorization_required
        ),
        "implementation_blocked": status.implementation_blocked,
    }

    required_false = {
        "wait_state_closed": status.wait_state_closed,
        "decision_gate_open": status.decision_gate_open,
        "direction_option_selected": status.direction_option_selected,
        "operator_direction_received": status.operator_direction_received,
        "operator_decision_received": status.operator_decision_received,
        "explicit_operator_authorization_received": (
            status.explicit_operator_authorization_received
        ),
        "implementation_authorization_granted": (
            status.implementation_authorization_granted
        ),
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

    if status.direction_option_count != len(DIRECTION_OPTIONS):
        issues.append("direction_option_count mismatch")
    if status.selected_direction_option_id != "NONE":
        issues.append("selected_direction_option_id must be NONE")
    if status.selected_direction_option_count != 0:
        issues.append("selected_direction_option_count must be 0")
    if status.operator_direction_value != "PENDING_EXPLICIT_OPERATOR_DIRECTION":
        issues.append("operator_direction_value must remain pending")
    if status.milestone_16_operator_direction_cycle_status_check_count < 35:
        issues.append("cycle status check count too low")
    if status.milestone_16_operator_direction_cycle_status_failure_count != 0:
        issues.append("cycle status failure count must be 0")
    if len(status.artifacts) != 5:
        issues.append("artifact count mismatch")

    return issues


def status_to_dict(status: OperatorDirectionCycleStatus) -> dict[str, Any]:
    """Convert status dataclass to JSON-ready dict."""
    return asdict(status)


def build_index_payload(status: OperatorDirectionCycleStatus) -> dict[str, Any]:
    """Build compact index artifact."""
    return {
        "task_name": status.task_name,
        "status": status.cycle_status_marker,
        "signature": status.signature,
        "source_task_7_final_baseline_commit": (
            status.source_task_7_final_baseline_commit
        ),
        "source_task_7_final_signature": status.source_task_7_final_signature,
        "previous_stage": status.previous_stage,
        "next_stage": status.next_stage,
        "verdict": status.verdict,
        "decision": status.decision,
        "wait_state_active": status.wait_state_active,
        "decision_gate_blocked": status.decision_gate_blocked,
        "operator_direction_received": status.operator_direction_received,
        "implementation_blocked": status.implementation_blocked,
        "runtime_execution_allowed": status.runtime_execution_allowed,
        "real_evaluation_allowed": status.real_evaluation_allowed,
        "kaggle_submission_sent": status.kaggle_submission_sent,
        "private_core_exposure": status.private_core_exposure,
        "legal_certification": status.legal_certification,
        "artifact_count": len(status.artifacts),
    }


def build_markdown(status: OperatorDirectionCycleStatus) -> str:
    """Build markdown report."""
    return f"""# Milestone #16 Task 8 - Operator Direction Cycle Status v1

## Status

`{status.cycle_status_marker}`

## Canonical markers

- task: `{status.task_name}`
- ready: `{status.task_ready_marker}`
- valid: `{status.task_valid_marker}`
- pipeline: `{status.pipeline_ready_marker}`
- signature: `{status.signature}`
- mode: `{status.task_mode}`

## Source binding

- previous stage: `{status.previous_stage}`
- source Task 7 final baseline commit: `{status.source_task_7_final_baseline_commit}`
- source Task 7 final signature: `{status.source_task_7_final_signature}`
- next stage: `{status.next_stage}`

## Verdict

`{status.verdict}`

## Decision

`{status.decision}`

## Block reason

`{status.block_reason}`

## Cycle state

- wait_state_closure_closed: `{status.wait_state_closure_closed}`
- wait_state_review_closed: `{status.wait_state_review_closed}`
- wait_state_ready: `{status.wait_state_ready}`
- wait_state_active: `{status.wait_state_active}`
- wait_state_closed: `{status.wait_state_closed}`
- decision_gate_ready: `{status.decision_gate_ready}`
- decision_gate_open: `{status.decision_gate_open}`
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

## Validation

- check_count: `{status.milestone_16_operator_direction_cycle_status_check_count}`
- failure_count: `{status.milestone_16_operator_direction_cycle_status_failure_count}`
"""


def build_manifest(status: OperatorDirectionCycleStatus) -> str:
    """Build plain-text manifest."""
    lines = [
        status.pipeline_ready_marker,
        status.task_ready_marker,
        status.task_valid_marker,
        status.cycle_status_marker,
        f"signature={status.signature}",
        f"source_task_7_final_baseline_commit={status.source_task_7_final_baseline_commit}",
        f"source_task_7_final_signature={status.source_task_7_final_signature}",
        f"task_mode={status.task_mode}",
        f"verdict={status.verdict}",
        f"decision={status.decision}",
        f"block_reason={status.block_reason}",
        f"previous_stage={status.previous_stage}",
        f"next_stage={status.next_stage}",
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
        f"real_evaluation_allowed={status.real_evaluation_allowed}",
        f"kaggle_submission_sent={status.kaggle_submission_sent}",
        f"private_core_exposure={status.private_core_exposure}",
        f"legal_certification={status.legal_certification}",
        f"check_count={status.milestone_16_operator_direction_cycle_status_check_count}",
        f"failure_count={status.milestone_16_operator_direction_cycle_status_failure_count}",
    ]
    return "\n".join(lines) + "\n"


def write_cycle_status_artifacts(
    status: OperatorDirectionCycleStatus | None = None,
) -> OperatorDirectionCycleStatus:
    """Write all Task 8 artifacts and return status."""
    resolved = status or build_cycle_status()
    issues = validate_cycle_status(resolved)
    if issues:
        raise ValueError("Invalid cycle status: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = status_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (
        ARTIFACT_DIR
        / "milestone-16-operator-direction-cycle-status-index-v1.json"
    ).write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (
        ARTIFACT_DIR
        / "milestone-16-operator-direction-cycle-status-manifest-v1.txt"
    ).write_text(manifest, encoding="utf-8")
    (ARTIFACT_DIR / "milestone-16-operator-direction-cycle-status-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    """CLI entrypoint."""
    status = write_cycle_status_artifacts()

    print(status.pipeline_ready_marker)
    print(status.task_ready_marker)
    print(status.task_valid_marker)
    print(status.signature)
    print(status.source_task_7_final_baseline_commit)
    print(status.task_mode)
    print(status.cycle_status_marker)
    print(status.verdict)
    print(status.decision)
    print(status.block_reason)
    print(status.previous_stage)
    print(status.next_stage)
    print(f"source_task_7_final_baseline_commit={status.source_task_7_final_baseline_commit}")
    print(f"source_task_7_final_signature={status.source_task_7_final_signature}")
    print(f"cycle_status_ready={status.cycle_status_ready}")
    print(f"cycle_status_passed={status.cycle_status_passed}")
    print(f"cycle_status_closed={status.cycle_status_closed}")
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
    print(
        "explicit_operator_authorization_required="
        f"{status.explicit_operator_authorization_required}"
    )
    print(
        "explicit_operator_authorization_received="
        f"{status.explicit_operator_authorization_received}"
    )
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
    print(
        "milestone_16_operator_direction_cycle_status_check_count="
        f"{status.milestone_16_operator_direction_cycle_status_check_count}"
    )
    print(
        "milestone_16_operator_direction_cycle_status_failure_count="
        f"{status.milestone_16_operator_direction_cycle_status_failure_count}"
    )
    for artifact in status.artifacts:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
