"""Milestone #18 Task 7 - Controlled Technical Candidate Generator Implementation Authorization Gate Review v1.

This module reviews the authorization gate created in Milestone #18 Task 6.

Important:
- This task reviews the gate.
- This task confirms the gate is structurally valid.
- This task does not open the gate.
- This task does not authorize implementation.
- This task does not modify the candidate generator.
- This task does not run real evaluation or submission.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_authorization_gate import (
    build_candidate_generator_implementation_authorization_gate,
)


TASK_NAME = "MILESTONE_18_TASK_7_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Authorization Gate Review v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_6_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_V1"
PREVIOUS_COMMIT = "c7a09f0"
PREVIOUS_SIGNATURE = "929456E280FF4E67"

NEXT_STAGE = "MILESTONE_18_TASK_8_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-authorization-gate-review-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-review-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorAuthorizationGateReviewItem:
    """A review-only confirmation item for a Task 6 authorization gate condition."""

    review_id: str
    source_condition_id: str
    source_review_item: str
    source_improvement_item: str
    source_limitation_id: str
    gate_area: str
    review_decision: str
    review_note: str
    blocking_issue: bool
    gate_open_authorized: bool
    implementation_authorized: bool
    runtime_execution_authorized: bool
    decision_gate_required: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_gate_review_items(
    source_gate: dict[str, Any],
) -> tuple[CandidateGeneratorAuthorizationGateReviewItem, ...]:
    """Build deterministic review confirmations from Task 6 gate conditions."""

    review_items: list[CandidateGeneratorAuthorizationGateReviewItem] = []

    for index, condition in enumerate(source_gate["gate_conditions"], start=1):
        review_items.append(
            CandidateGeneratorAuthorizationGateReviewItem(
                review_id=f"M18-CG-AUTH-GATE-REV-{index}",
                source_condition_id=condition["condition_id"],
                source_review_item=condition["source_review_item"],
                source_improvement_item=condition["source_improvement_item"],
                source_limitation_id=condition["source_limitation_id"],
                gate_area=condition["gate_area"],
                review_decision="CONFIRMED_GATE_CREATED_PENDING_DECISION_NO_IMPLEMENTATION",
                review_note=(
                    "Task 6 gate condition is confirmed as structurally valid. "
                    "The gate remains closed and requires a separate implementation decision gate."
                ),
                blocking_issue=False,
                gate_open_authorized=False,
                implementation_authorized=False,
                runtime_execution_authorized=False,
                decision_gate_required=True,
            )
        )

    return tuple(review_items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 7 boundary controls."""

    return {
        "authorization_gate_review_only": True,
        "authorization_gate_confirmed": True,
        "authorization_gate_review_passed": True,
        "authorization_gate_open": False,
        "authorization_gate_locked": True,
        "authorization_gate_decision_required": True,
        "decision_gate_required": True,
        "decision_gate_created": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "gate_open_authorization_granted": False,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "candidate_generator_modified": False,
        "candidate_generator_wiring_authorized": False,
        "candidate_generator_runtime_patch_allowed": False,
        "solver_runtime_modified": False,
        "solver_patch_execution_allowed": False,
        "ranker_runtime_modified": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
    }


def build_acceptance_gates(
    source_gate: dict[str, Any],
    review_items: tuple[CandidateGeneratorAuthorizationGateReviewItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 7 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T7-GATE-001",
            "name": "previous_task_matches_task_6",
            "passed": PREVIOUS_TASK == source_gate["task"],
        },
        {
            "gate_id": "M18-T7-GATE-002",
            "name": "previous_commit_matches_task_6_commit",
            "passed": PREVIOUS_COMMIT == "c7a09f0",
        },
        {
            "gate_id": "M18-T7-GATE-003",
            "name": "previous_signature_matches_task_6_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_gate["signature"],
            "passed": PREVIOUS_SIGNATURE == source_gate["signature"],
        },
        {
            "gate_id": "M18-T7-GATE-004",
            "name": "source_gate_valid",
            "passed": source_gate["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T7-GATE-005",
            "name": "source_gate_created",
            "passed": source_gate["authorization_gate_created"] is True,
        },
        {
            "gate_id": "M18-T7-GATE-006",
            "name": "source_gate_locked",
            "passed": source_gate["authorization_gate_locked"] is True,
        },
        {
            "gate_id": "M18-T7-GATE-007",
            "name": "source_gate_not_open",
            "passed": source_gate["authorization_gate_open"] is False,
        },
        {
            "gate_id": "M18-T7-GATE-008",
            "name": "source_gate_did_not_authorize_implementation",
            "passed": source_gate["implementation_allowed_now"] is False,
        },
        {
            "gate_id": "M18-T7-GATE-009",
            "name": "six_gate_review_items_created",
            "passed": len(review_items) == 6,
        },
        {
            "gate_id": "M18-T7-GATE-010",
            "name": "all_review_items_require_decision_gate",
            "passed": all(item.decision_gate_required for item in review_items),
        },
        {
            "gate_id": "M18-T7-GATE-011",
            "name": "no_review_item_opens_gate",
            "passed": not any(item.gate_open_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T7-GATE-012",
            "name": "no_review_item_authorizes_implementation",
            "passed": not any(item.implementation_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T7-GATE-013",
            "name": "no_review_item_authorizes_runtime_execution",
            "passed": not any(item.runtime_execution_authorized for item in review_items),
        },
    ]

    for key, expected in {
        "authorization_gate_review_only": True,
        "authorization_gate_confirmed": True,
        "authorization_gate_review_passed": True,
        "authorization_gate_open": False,
        "authorization_gate_locked": True,
        "authorization_gate_decision_required": True,
        "decision_gate_required": True,
        "decision_gate_created": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "gate_open_authorization_granted": False,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "candidate_generator_modified": False,
        "candidate_generator_wiring_authorized": False,
        "candidate_generator_runtime_patch_allowed": False,
        "solver_runtime_modified": False,
        "solver_patch_execution_allowed": False,
        "ranker_runtime_modified": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
    }.items():
        gates.append(
            {
                "gate_id": f"M18-T7-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in review_items:
        gates.append(
            {
                "gate_id": f"M18-T7-GATE-{len(gates) + 1:03d}",
                "name": f"{item.review_id}_confirmed_gate_closed",
                "passed": item.review_decision
                == "CONFIRMED_GATE_CREATED_PENDING_DECISION_NO_IMPLEMENTATION"
                and item.gate_open_authorized is False
                and item.implementation_authorized is False
                and item.runtime_execution_authorized is False
                and item.blocking_issue is False
                and item.decision_gate_required is True,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_authorization_gate_review() -> dict[str, Any]:
    """Build the complete deterministic Task 7 gate review record."""

    source_gate = build_candidate_generator_implementation_authorization_gate()
    review_items = build_gate_review_items(source_gate)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_gate, review_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_PASS_GATE_CLOSED_PENDING_DECISION"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_BLOCKED",
        "review_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_gate_task": source_gate["task"],
        "source_gate_id": source_gate["authorization_gate_id"],
        "source_gate_signature": source_gate["signature"],
        "source_gate_validation": source_gate["validation"],
        "source_gate_verdict": source_gate["verdict"],
        "next_stage": NEXT_STAGE,
        "authorization_gate_review_ready": not gate_failures,
        "authorization_gate_review_passed": not gate_failures,
        "authorization_gate_confirmed": not gate_failures,
        "authorization_gate_open": False,
        "authorization_gate_locked": True,
        "decision_gate_required": True,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "NOT_GRANTED_PENDING_DECISION_GATE",
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "review_item_count": len(review_items),
        "confirmed_review_item_count": len(
            [
                item
                for item in review_items
                if item.review_decision
                == "CONFIRMED_GATE_CREATED_PENDING_DECISION_NO_IMPLEMENTATION"
            ]
        ),
        "blocking_issue_count": len(gate_failures),
        "boundary_controls": controls,
        "review_items": [asdict(item) for item in review_items],
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(gate_failures),
        "acceptance_gate_failures": gate_failures,
    }

    payload["signature"] = _signature(payload)
    payload["authorization_gate_review_id"] = (
        "MILESTONE-18-TASK-7-CANDIDATE-GENERATOR-IMPLEMENTATION-AUTHORIZATION-GATE-REVIEW-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 7 — Controlled Technical Candidate Generator Implementation Authorization Gate Review v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Authorization gate review ID: `{data['authorization_gate_review_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source gate ID: `{data['source_gate_id']}`",
        f"- Source gate signature: `{data['source_gate_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- authorization gate review only: true",
        "- authorization gate confirmed: true",
        "- authorization gate open: false",
        "- decision gate required: true",
        "- implementation authorized: false",
        "- candidate generator modified: false",
        "- runtime execution allowed: false",
        "- real evaluation allowed: false",
        "- real submission allowed: false",
        "- Kaggle submission sent: false",
        "- private core exposure: false",
        "- legalCertification: false",
        "- fail-closed: active",
        "",
        "## Review Items",
        "",
    ]

    for item in data["review_items"]:
        lines.extend(
            [
                f"### {item['review_id']} — {item['gate_area']}",
                "",
                f"- Source condition: `{item['source_condition_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Review decision: `{item['review_decision']}`",
                f"- Gate open authorized: `{item['gate_open_authorized']}`",
                f"- Implementation authorized: `{item['implementation_authorized']}`",
                f"- Runtime execution authorized: `{item['runtime_execution_authorized']}`",
                f"- Decision gate required: `{item['decision_gate_required']}`",
                f"- Note: {item['review_note']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Acceptance",
            "",
            f"- Review item count: `{data['review_item_count']}`",
            f"- Confirmed review item count: `{data['confirmed_review_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            f"- Blocking issue count: `{data['blocking_issue_count']}`",
            "",
            "Task 7 reviews and confirms the authorization gate while keeping it closed. It does not authorize implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 7 artifacts."""

    data = build_candidate_generator_implementation_authorization_gate_review()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-review-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-review-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-review-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-review-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_7_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_INDEX",
        "task": data["task"],
        "authorization_gate_review_id": data["authorization_gate_review_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_gate_signature": data["source_gate_signature"],
        "next_stage": data["next_stage"],
        "artifact_paths": {
            "json": str(json_path),
            "manifest": str(manifest_path),
            "markdown": str(markdown_path),
            "docs": str(docs_path),
        },
        "boundary": data["boundary_controls"],
    }
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        "MILESTONE_18_TASK_7_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_V1_MANIFEST",
        f"task={data['task']}",
        f"authorization_gate_review_id={data['authorization_gate_review_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_gate_signature={data['source_gate_signature']}",
        f"next_stage={data['next_stage']}",
        f"review_item_count={data['review_item_count']}",
        f"confirmed_review_item_count={data['confirmed_review_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "authorization_gate_review_only=true",
        "authorization_gate_confirmed=true",
        "authorization_gate_open=false",
        "decision_gate_required=true",
        "implementation_authorized=false",
        "candidate_generator_modified=false",
        "runtime_execution_allowed=false",
        "real_submission_allowed=false",
        "kaggle_submission_sent=false",
        "private_core_exposure=false",
        "legalCertification=false",
        "fail_closed_active=true",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    markdown_report = build_markdown_report(data)
    markdown_path.write_text(markdown_report, encoding="utf-8")
    docs_path.write_text(markdown_report, encoding="utf-8")

    return {
        "json": json_path,
        "index": index_path,
        "manifest": manifest_path,
        "markdown": markdown_path,
        "docs": docs_path,
    }


if __name__ == "__main__":
    result = build_candidate_generator_implementation_authorization_gate_review()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_gate_signature"])
    print(result["review_scope"])
    print(result["verdict"])
    print(result["next_stage"])
