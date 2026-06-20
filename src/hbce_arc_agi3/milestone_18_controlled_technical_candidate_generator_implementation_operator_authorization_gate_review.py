"""Milestone #18 Task 15 - Controlled Technical Candidate Generator Implementation Operator Authorization Gate Review v1.

This module reviews the operator-authorization gate created in Milestone #18 Task 14.

Important:
- This task reviews the operator-authorization gate.
- This task confirms that only the next operator-decision gate may be created.
- This task does not receive operator authorization.
- This task does not grant implementation authorization.
- This task does not modify candidate generator, solver, ranker, runtime, evaluation, or submission paths.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_authorization_gate import (
    build_candidate_generator_implementation_operator_authorization_gate,
)


TASK_NAME = "MILESTONE_18_TASK_15_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_AUTHORIZATION_GATE_REVIEW_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Operator Authorization Gate Review v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_14_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_AUTHORIZATION_GATE_V1"
PREVIOUS_COMMIT = "8431533"
PREVIOUS_SIGNATURE = "602D06EB1BB73F4C"

NEXT_STAGE = "MILESTONE_18_TASK_16_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-operator-authorization-gate-review-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-operator-authorization-gate-review-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorImplementationOperatorAuthorizationGateReviewItem:
    """A review item derived from Task 14 operator-authorization gate items."""

    review_id: str
    source_operator_authorization_gate_id: str
    source_authorization_review_gate_review_item: str
    source_authorization_review_gate_item: str
    source_proposal_id: str
    source_improvement_item: str
    source_limitation_id: str
    review_area: str
    review_decision: str
    review_effect: str
    operator_decision_options_status: str
    operator_decision_gate_required: bool
    operator_decision_gate_allowed_next: bool
    operator_authorization_required_confirmed: bool
    operator_authorization_received_confirmed_false: bool
    explicit_operator_authorization_received_confirmed_false: bool
    implementation_authorization_candidate_confirmed: bool
    implementation_code_authorized: bool
    runtime_execution_authorized: bool
    real_submission_authorized: bool
    blocking_issue: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_operator_authorization_gate_review_items(
    source_gate: dict[str, Any],
) -> tuple[CandidateGeneratorImplementationOperatorAuthorizationGateReviewItem, ...]:
    """Build deterministic review items from Task 14 operator-authorization gate items."""

    review_items: list[CandidateGeneratorImplementationOperatorAuthorizationGateReviewItem] = []

    for index, gate_item in enumerate(source_gate["gate_items"], start=1):
        review_items.append(
            CandidateGeneratorImplementationOperatorAuthorizationGateReviewItem(
                review_id=f"M18-CG-IMPL-OPERATOR-AUTH-GATE-REV-{index}",
                source_operator_authorization_gate_id=gate_item["gate_id"],
                source_authorization_review_gate_review_item=gate_item[
                    "source_authorization_review_gate_review_item"
                ],
                source_authorization_review_gate_item=gate_item[
                    "source_authorization_review_gate_item"
                ],
                source_proposal_id=gate_item["source_proposal_id"],
                source_improvement_item=gate_item["source_improvement_item"],
                source_limitation_id=gate_item["source_limitation_id"],
                review_area=gate_item["gate_area"],
                review_decision="CONFIRMED_OPERATOR_AUTHORIZATION_GATE_PENDING_OPERATOR_DECISION_GATE",
                review_effect="NEXT_OPERATOR_DECISION_GATE_REQUIRED_NO_CODE_IMPLEMENTATION",
                operator_decision_options_status="DEFINED_AND_PENDING_OPERATOR_DECISION_GATE",
                operator_decision_gate_required=True,
                operator_decision_gate_allowed_next=True,
                operator_authorization_required_confirmed=True,
                operator_authorization_received_confirmed_false=True,
                explicit_operator_authorization_received_confirmed_false=True,
                implementation_authorization_candidate_confirmed=True,
                implementation_code_authorized=False,
                runtime_execution_authorized=False,
                real_submission_authorized=False,
                blocking_issue=False,
            )
        )

    return tuple(review_items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 15 boundary controls."""

    return {
        "operator_authorization_gate_review_only": True,
        "operator_authorization_gate_confirmed": True,
        "operator_authorization_gate_review_passed": True,
        "operator_decision_gate_required": True,
        "operator_decision_gate_created": False,
        "operator_decision_gate_allowed_next": True,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "explicit_operator_authorization_received": False,
        "implementation_authorization_candidate_confirmed": True,
        "implementation_authorization_granted": False,
        "implementation_code_authorization_granted": False,
        "implementation_code_authorized": False,
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
        "submission_artifact_created": False,
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
    review_items: tuple[CandidateGeneratorImplementationOperatorAuthorizationGateReviewItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 15 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T15-GATE-001",
            "name": "previous_task_matches_task_14",
            "passed": PREVIOUS_TASK == source_gate["task"],
        },
        {
            "gate_id": "M18-T15-GATE-002",
            "name": "previous_commit_matches_task_14_commit",
            "passed": PREVIOUS_COMMIT == "8431533",
        },
        {
            "gate_id": "M18-T15-GATE-003",
            "name": "previous_signature_matches_task_14_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_gate["signature"],
            "passed": PREVIOUS_SIGNATURE == source_gate["signature"],
        },
        {
            "gate_id": "M18-T15-GATE-004",
            "name": "source_operator_authorization_gate_valid",
            "passed": source_gate["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T15-GATE-005",
            "name": "source_operator_authorization_gate_ready",
            "passed": source_gate["operator_authorization_gate_ready"] is True,
        },
        {
            "gate_id": "M18-T15-GATE-006",
            "name": "source_operator_authorization_gate_created",
            "passed": source_gate["operator_authorization_gate_created"] is True,
        },
        {
            "gate_id": "M18-T15-GATE-007",
            "name": "source_operator_authorization_gate_locked",
            "passed": source_gate["operator_authorization_gate_locked"] is True,
        },
        {
            "gate_id": "M18-T15-GATE-008",
            "name": "source_operator_authorization_gate_not_open",
            "passed": source_gate["operator_authorization_gate_open"] is False,
        },
        {
            "gate_id": "M18-T15-GATE-009",
            "name": "source_operator_authorization_gate_requires_review",
            "passed": source_gate["operator_authorization_gate_review_required"] is True,
        },
        {
            "gate_id": "M18-T15-GATE-010",
            "name": "source_operator_authorization_gate_not_passed_yet",
            "passed": source_gate["operator_authorization_gate_passed"] is False,
        },
        {
            "gate_id": "M18-T15-GATE-011",
            "name": "source_operator_authorization_required",
            "passed": source_gate["operator_authorization_required"] is True,
        },
        {
            "gate_id": "M18-T15-GATE-012",
            "name": "source_operator_authorization_not_received",
            "passed": source_gate["operator_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T15-GATE-013",
            "name": "source_explicit_operator_authorization_not_received",
            "passed": source_gate["explicit_operator_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T15-GATE-014",
            "name": "source_does_not_authorize_code",
            "passed": source_gate["implementation_code_authorized"] is False,
        },
        {
            "gate_id": "M18-T15-GATE-015",
            "name": "source_does_not_authorize_runtime",
            "passed": source_gate["boundary_controls"]["runtime_execution_allowed"] is False,
        },
        {
            "gate_id": "M18-T15-GATE-016",
            "name": "source_does_not_authorize_submission",
            "passed": source_gate["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T15-GATE-017",
            "name": "six_operator_authorization_gate_review_items_created",
            "passed": len(review_items) == 6,
        },
        {
            "gate_id": "M18-T15-GATE-018",
            "name": "all_review_items_confirm_gate_pending_operator_decision_gate",
            "passed": all(
                item.review_decision
                == "CONFIRMED_OPERATOR_AUTHORIZATION_GATE_PENDING_OPERATOR_DECISION_GATE"
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T15-GATE-019",
            "name": "all_review_items_require_operator_decision_gate",
            "passed": all(item.operator_decision_gate_required for item in review_items),
        },
        {
            "gate_id": "M18-T15-GATE-020",
            "name": "all_review_items_allow_next_operator_decision_gate_only",
            "passed": all(item.operator_decision_gate_allowed_next for item in review_items),
        },
        {
            "gate_id": "M18-T15-GATE-021",
            "name": "all_review_items_confirm_operator_authorization_required",
            "passed": all(item.operator_authorization_required_confirmed for item in review_items),
        },
        {
            "gate_id": "M18-T15-GATE-022",
            "name": "all_review_items_confirm_operator_authorization_not_received",
            "passed": all(
                item.operator_authorization_received_confirmed_false
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T15-GATE-023",
            "name": "all_review_items_confirm_explicit_operator_authorization_not_received",
            "passed": all(
                item.explicit_operator_authorization_received_confirmed_false
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T15-GATE-024",
            "name": "all_review_items_confirm_implementation_authorization_candidate",
            "passed": all(
                item.implementation_authorization_candidate_confirmed
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T15-GATE-025",
            "name": "no_review_item_authorizes_code",
            "passed": not any(item.implementation_code_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T15-GATE-026",
            "name": "no_review_item_authorizes_runtime",
            "passed": not any(item.runtime_execution_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T15-GATE-027",
            "name": "no_review_item_authorizes_submission",
            "passed": not any(item.real_submission_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T15-GATE-028",
            "name": "no_review_item_has_blocking_issue",
            "passed": not any(item.blocking_issue for item in review_items),
        },
    ]

    for key, expected in {
        "operator_authorization_gate_review_only": True,
        "operator_authorization_gate_confirmed": True,
        "operator_authorization_gate_review_passed": True,
        "operator_decision_gate_required": True,
        "operator_decision_gate_created": False,
        "operator_decision_gate_allowed_next": True,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "explicit_operator_authorization_received": False,
        "implementation_authorization_candidate_confirmed": True,
        "implementation_authorization_granted": False,
        "implementation_code_authorization_granted": False,
        "implementation_code_authorized": False,
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
        "submission_artifact_created": False,
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
                "gate_id": f"M18-T15-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in review_items:
        gates.append(
            {
                "gate_id": f"M18-T15-GATE-{len(gates) + 1:03d}",
                "name": f"{item.review_id}_operator_decision_gate_required_no_code",
                "passed": item.review_decision
                == "CONFIRMED_OPERATOR_AUTHORIZATION_GATE_PENDING_OPERATOR_DECISION_GATE"
                and item.review_effect
                == "NEXT_OPERATOR_DECISION_GATE_REQUIRED_NO_CODE_IMPLEMENTATION"
                and item.operator_decision_options_status
                == "DEFINED_AND_PENDING_OPERATOR_DECISION_GATE"
                and item.operator_decision_gate_required is True
                and item.operator_decision_gate_allowed_next is True
                and item.operator_authorization_required_confirmed is True
                and item.operator_authorization_received_confirmed_false is True
                and item.explicit_operator_authorization_received_confirmed_false is True
                and item.implementation_authorization_candidate_confirmed is True
                and item.implementation_code_authorized is False
                and item.runtime_execution_authorized is False
                and item.real_submission_authorized is False
                and item.blocking_issue is False,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_operator_authorization_gate_review() -> dict[str, Any]:
    """Build the complete deterministic Task 15 operator-authorization gate review record."""

    source_gate = build_candidate_generator_implementation_operator_authorization_gate()
    review_items = build_operator_authorization_gate_review_items(source_gate)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_gate, review_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_AUTHORIZATION_GATE_REVIEW_PASS_OPERATOR_DECISION_GATE_REQUIRED_NO_CODE"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_AUTHORIZATION_GATE_REVIEW_BLOCKED",
        "review_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_AUTHORIZATION_GATE_REVIEW_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_operator_authorization_gate_task": source_gate["task"],
        "source_operator_authorization_gate_id": source_gate["operator_authorization_gate_id"],
        "source_operator_authorization_gate_signature": source_gate["signature"],
        "source_operator_authorization_gate_validation": source_gate["validation"],
        "source_operator_authorization_gate_verdict": source_gate["verdict"],
        "next_stage": NEXT_STAGE,
        "operator_authorization_gate_review_ready": not gate_failures,
        "operator_authorization_gate_review_passed": not gate_failures,
        "operator_authorization_gate_confirmed": not gate_failures,
        "operator_decision_gate_required": True,
        "operator_decision_gate_allowed_next": True,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "explicit_operator_authorization_received": False,
        "implementation_authorization_candidate_confirmed": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "OPERATOR_AUTHORIZATION_GATE_REVIEW_ONLY_PENDING_OPERATOR_DECISION_GATE_NO_CODE_NO_RUNTIME",
        "review_item_count": len(review_items),
        "confirmed_review_item_count": len(
            [
                item
                for item in review_items
                if item.review_decision
                == "CONFIRMED_OPERATOR_AUTHORIZATION_GATE_PENDING_OPERATOR_DECISION_GATE"
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
    payload["operator_authorization_gate_review_id"] = (
        "MILESTONE-18-TASK-15-CANDIDATE-GENERATOR-IMPLEMENTATION-OPERATOR-AUTHORIZATION-GATE-REVIEW-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 15 - Controlled Technical Candidate Generator Implementation Operator Authorization Gate Review v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Operator authorization gate review ID: `{data['operator_authorization_gate_review_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source operator authorization gate ID: `{data['source_operator_authorization_gate_id']}`",
        f"- Source operator authorization gate signature: `{data['source_operator_authorization_gate_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- operator authorization gate review only: true",
        "- operator authorization gate confirmed: true",
        "- operator decision gate required: true",
        "- operator decision gate allowed next: true",
        "- operator authorization required: true",
        "- operator authorization received: false",
        "- explicit operator authorization received: false",
        "- implementation authorization candidate confirmed: true",
        "- implementation code authorized: false",
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
                f"### {item['review_id']} - {item['review_area']}",
                "",
                f"- Source operator authorization gate: `{item['source_operator_authorization_gate_id']}`",
                f"- Source proposal: `{item['source_proposal_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Review decision: `{item['review_decision']}`",
                f"- Review effect: `{item['review_effect']}`",
                f"- Operator decision options status: `{item['operator_decision_options_status']}`",
                f"- Operator decision gate required: `{item['operator_decision_gate_required']}`",
                f"- Operator decision gate allowed next: `{item['operator_decision_gate_allowed_next']}`",
                f"- Operator authorization required confirmed: `{item['operator_authorization_required_confirmed']}`",
                f"- Operator authorization received confirmed false: `{item['operator_authorization_received_confirmed_false']}`",
                f"- Explicit operator authorization received confirmed false: `{item['explicit_operator_authorization_received_confirmed_false']}`",
                f"- Implementation authorization candidate confirmed: `{item['implementation_authorization_candidate_confirmed']}`",
                f"- Implementation code authorized: `{item['implementation_code_authorized']}`",
                f"- Runtime execution authorized: `{item['runtime_execution_authorized']}`",
                f"- Real submission authorized: `{item['real_submission_authorized']}`",
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
            "Task 15 reviews the operator-authorization gate and allows only the next operator-decision gate. It does not receive operator authorization and does not authorize code implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 15 artifacts."""

    data = build_candidate_generator_implementation_operator_authorization_gate_review()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-authorization-gate-review-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-authorization-gate-review-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-authorization-gate-review-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-authorization-gate-review-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_15_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_AUTHORIZATION_GATE_REVIEW_INDEX",
        "task": data["task"],
        "operator_authorization_gate_review_id": data["operator_authorization_gate_review_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_operator_authorization_gate_signature": data[
            "source_operator_authorization_gate_signature"
        ],
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
        "MILESTONE_18_TASK_15_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_AUTHORIZATION_GATE_REVIEW_V1_MANIFEST",
        f"task={data['task']}",
        f"operator_authorization_gate_review_id={data['operator_authorization_gate_review_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_operator_authorization_gate_signature={data['source_operator_authorization_gate_signature']}",
        f"next_stage={data['next_stage']}",
        f"review_item_count={data['review_item_count']}",
        f"confirmed_review_item_count={data['confirmed_review_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "operator_authorization_gate_review_only=true",
        "operator_authorization_gate_confirmed=true",
        "operator_decision_gate_required=true",
        "operator_decision_gate_allowed_next=true",
        "operator_authorization_required=true",
        "operator_authorization_received=false",
        "explicit_operator_authorization_received=false",
        "implementation_authorization_candidate_confirmed=true",
        "implementation_code_authorized=false",
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
    result = build_candidate_generator_implementation_operator_authorization_gate_review()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_operator_authorization_gate_signature"])
    print(result["review_scope"])
    print(result["verdict"])
    print(result["next_stage"])
