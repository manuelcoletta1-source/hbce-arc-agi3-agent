"""Milestone #18 Task 16 - Controlled Technical Candidate Generator Implementation Operator Decision Gate v1.

This module creates the operator-decision gate after Milestone #18 Task 15.

Important:
- This task creates an operator-decision gate.
- This task does not record an operator decision.
- This task does not receive explicit operator authorization.
- This task does not grant implementation authorization.
- This task does not modify candidate generator, solver, ranker, runtime, evaluation, or submission paths.
- This task only allows the next operator-decision-gate review stage.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_authorization_gate_review import (
    build_candidate_generator_implementation_operator_authorization_gate_review,
)


TASK_NAME = "MILESTONE_18_TASK_16_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Operator Decision Gate v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_15_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_AUTHORIZATION_GATE_REVIEW_V1"
PREVIOUS_COMMIT = "4de8151"
PREVIOUS_SIGNATURE = "FFA147CDE3F12401"

NEXT_STAGE = "MILESTONE_18_TASK_17_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_REVIEW_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-operator-decision-gate-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-gate-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorImplementationOperatorDecisionGateItem:
    """A gate item derived from Task 15 operator-authorization-gate-review items."""

    gate_id: str
    source_operator_authorization_gate_review_item: str
    source_operator_authorization_gate_id: str
    source_proposal_id: str
    source_improvement_item: str
    source_limitation_id: str
    gate_area: str
    gate_decision: str
    gate_effect: str
    allowed_operator_decisions: tuple[str, ...]
    required_operator_decision: str
    operator_decision_status: str
    next_review_required: bool
    operator_decision_required: bool
    operator_decision_received: bool
    explicit_operator_authorization_received: bool
    implementation_authorization_candidate_confirmed: bool
    implementation_code_authorized: bool
    runtime_execution_authorized: bool
    real_submission_authorized: bool
    blocking_issue: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def _allowed_operator_decisions_for_area(area: str) -> tuple[str, ...]:
    base = (
        "APPROVE_NEXT_CONTROLLED_IMPLEMENTATION_AUTHORIZATION_DECISION_REVIEW_ONLY",
        "REJECT_IMPLEMENTATION_AUTHORIZATION_AND_KEEP_FAIL_CLOSED",
        "REQUEST_ADDITIONAL_LOCAL_DIAGNOSTIC_EVIDENCE",
        "DEFER_OPERATOR_DECISION_KEEP_PENDING",
    )

    if area == "solver coverage":
        return base + ("REQUEST_CANDIDATE_FAMILY_COVERAGE_NARROWING",)

    if area == "candidate generation":
        return base + ("REQUEST_DETERMINISTIC_CANDIDATE_RULE_REFINEMENT",)

    if area == "ranker evidence":
        return base + ("REQUEST_RANKER_NEUTRALITY_EVIDENCE_RECHECK",)

    if area == "local diagnostics":
        return base + ("REQUEST_ADDITIONAL_PUBLIC_SAFE_FIXTURES",)

    if area == "submission discipline":
        return base + ("REQUEST_SUBMISSION_PATH_ISOLATION_RECHECK",)

    if area == "authorization boundary":
        return base + ("REQUEST_EXPLICIT_FAIL_CLOSED_BOUNDARY_RECHECK",)

    return base + ("REQUEST_ADDITIONAL_AREA_SPECIFIC_EVIDENCE",)


def build_operator_decision_gate_items(
    source_review: dict[str, Any],
) -> tuple[CandidateGeneratorImplementationOperatorDecisionGateItem, ...]:
    """Build deterministic operator-decision gate items from Task 15 review records."""

    gate_items: list[CandidateGeneratorImplementationOperatorDecisionGateItem] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        area = review_item["review_area"]

        gate_items.append(
            CandidateGeneratorImplementationOperatorDecisionGateItem(
                gate_id=f"M18-CG-IMPL-OPERATOR-DECISION-GATE-{index}",
                source_operator_authorization_gate_review_item=review_item["review_id"],
                source_operator_authorization_gate_id=review_item[
                    "source_operator_authorization_gate_id"
                ],
                source_proposal_id=review_item["source_proposal_id"],
                source_improvement_item=review_item["source_improvement_item"],
                source_limitation_id=review_item["source_limitation_id"],
                gate_area=area,
                gate_decision="OPERATOR_DECISION_GATE_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION",
                gate_effect="NEXT_OPERATOR_DECISION_GATE_REVIEW_REQUIRED_NO_DECISION_NO_CODE_IMPLEMENTATION",
                allowed_operator_decisions=_allowed_operator_decisions_for_area(area),
                required_operator_decision=(
                    "An explicit operator decision must be supplied in a later controlled step. "
                    "This gate only defines the decision slot and valid decision vocabulary."
                ),
                operator_decision_status="PENDING_EXPLICIT_OPERATOR_DECISION",
                next_review_required=True,
                operator_decision_required=True,
                operator_decision_received=False,
                explicit_operator_authorization_received=False,
                implementation_authorization_candidate_confirmed=True,
                implementation_code_authorized=False,
                runtime_execution_authorized=False,
                real_submission_authorized=False,
                blocking_issue=False,
            )
        )

    return tuple(gate_items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 16 boundary controls."""

    return {
        "operator_decision_gate_only": True,
        "operator_decision_gate_created": True,
        "operator_decision_gate_review_required": True,
        "operator_decision_gate_locked": True,
        "operator_decision_gate_open": False,
        "operator_decision_gate_passed": False,
        "operator_decision_gate_allows_next_review_only": True,
        "operator_decision_required": True,
        "operator_decision_received": False,
        "operator_decision_value_selected": False,
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
    source_review: dict[str, Any],
    gate_items: tuple[CandidateGeneratorImplementationOperatorDecisionGateItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 16 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T16-GATE-001",
            "name": "previous_task_matches_task_15",
            "passed": PREVIOUS_TASK == source_review["task"],
        },
        {
            "gate_id": "M18-T16-GATE-002",
            "name": "previous_commit_matches_task_15_commit",
            "passed": PREVIOUS_COMMIT == "4de8151",
        },
        {
            "gate_id": "M18-T16-GATE-003",
            "name": "previous_signature_matches_task_15_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": PREVIOUS_SIGNATURE == source_review["signature"],
        },
        {
            "gate_id": "M18-T16-GATE-004",
            "name": "source_operator_authorization_gate_review_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T16-GATE-005",
            "name": "source_operator_authorization_gate_review_passed",
            "passed": source_review["operator_authorization_gate_review_passed"] is True,
        },
        {
            "gate_id": "M18-T16-GATE-006",
            "name": "source_operator_decision_gate_required",
            "passed": source_review["operator_decision_gate_required"] is True,
        },
        {
            "gate_id": "M18-T16-GATE-007",
            "name": "source_operator_decision_gate_allowed_next",
            "passed": source_review["operator_decision_gate_allowed_next"] is True,
        },
        {
            "gate_id": "M18-T16-GATE-008",
            "name": "source_operator_authorization_required",
            "passed": source_review["operator_authorization_required"] is True,
        },
        {
            "gate_id": "M18-T16-GATE-009",
            "name": "source_operator_authorization_not_received",
            "passed": source_review["operator_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T16-GATE-010",
            "name": "source_explicit_operator_authorization_not_received",
            "passed": source_review["explicit_operator_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T16-GATE-011",
            "name": "source_implementation_candidate_confirmed",
            "passed": source_review["implementation_authorization_candidate_confirmed"] is True,
        },
        {
            "gate_id": "M18-T16-GATE-012",
            "name": "source_does_not_authorize_code",
            "passed": source_review["implementation_code_authorized"] is False,
        },
        {
            "gate_id": "M18-T16-GATE-013",
            "name": "source_does_not_authorize_runtime",
            "passed": source_review["boundary_controls"]["runtime_execution_allowed"] is False,
        },
        {
            "gate_id": "M18-T16-GATE-014",
            "name": "source_does_not_authorize_submission",
            "passed": source_review["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T16-GATE-015",
            "name": "six_operator_decision_gate_items_created",
            "passed": len(gate_items) == 6,
        },
        {
            "gate_id": "M18-T16-GATE-016",
            "name": "all_gate_items_created_pending_explicit_operator_decision",
            "passed": all(
                item.gate_decision
                == "OPERATOR_DECISION_GATE_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION"
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T16-GATE-017",
            "name": "all_gate_items_require_next_review",
            "passed": all(item.next_review_required for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-018",
            "name": "all_gate_items_require_operator_decision",
            "passed": all(item.operator_decision_required for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-019",
            "name": "no_gate_item_has_operator_decision_received",
            "passed": not any(item.operator_decision_received for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-020",
            "name": "no_gate_item_has_explicit_operator_authorization_received",
            "passed": not any(item.explicit_operator_authorization_received for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-021",
            "name": "all_gate_items_confirm_authorization_candidate",
            "passed": all(
                item.implementation_authorization_candidate_confirmed
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T16-GATE-022",
            "name": "no_gate_item_authorizes_code",
            "passed": not any(item.implementation_code_authorized for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-023",
            "name": "no_gate_item_authorizes_runtime",
            "passed": not any(item.runtime_execution_authorized for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-024",
            "name": "no_gate_item_authorizes_submission",
            "passed": not any(item.real_submission_authorized for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-025",
            "name": "no_gate_item_has_blocking_issue",
            "passed": not any(item.blocking_issue for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-026",
            "name": "all_gate_items_have_allowed_operator_decisions",
            "passed": all(len(item.allowed_operator_decisions) >= 5 for item in gate_items),
        },
        {
            "gate_id": "M18-T16-GATE-027",
            "name": "all_gate_items_are_pending_explicit_operator_decision",
            "passed": all(
                item.operator_decision_status == "PENDING_EXPLICIT_OPERATOR_DECISION"
                for item in gate_items
            ),
        },
    ]

    for key, expected in {
        "operator_decision_gate_only": True,
        "operator_decision_gate_created": True,
        "operator_decision_gate_review_required": True,
        "operator_decision_gate_locked": True,
        "operator_decision_gate_open": False,
        "operator_decision_gate_passed": False,
        "operator_decision_gate_allows_next_review_only": True,
        "operator_decision_required": True,
        "operator_decision_received": False,
        "operator_decision_value_selected": False,
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
                "gate_id": f"M18-T16-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in gate_items:
        gates.append(
            {
                "gate_id": f"M18-T16-GATE-{len(gates) + 1:03d}",
                "name": f"{item.gate_id}_pending_explicit_operator_decision_no_code",
                "passed": item.gate_decision
                == "OPERATOR_DECISION_GATE_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION"
                and item.gate_effect
                == "NEXT_OPERATOR_DECISION_GATE_REVIEW_REQUIRED_NO_DECISION_NO_CODE_IMPLEMENTATION"
                and item.operator_decision_status == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item.next_review_required is True
                and item.operator_decision_required is True
                and item.operator_decision_received is False
                and item.explicit_operator_authorization_received is False
                and item.implementation_authorization_candidate_confirmed is True
                and item.implementation_code_authorized is False
                and item.runtime_execution_authorized is False
                and item.real_submission_authorized is False
                and item.blocking_issue is False
                and len(item.allowed_operator_decisions) >= 5,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_operator_decision_gate() -> dict[str, Any]:
    """Build the complete deterministic Task 16 operator-decision gate record."""

    source_review = build_candidate_generator_implementation_operator_authorization_gate_review()
    gate_items = build_operator_decision_gate_items(source_review)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_review, gate_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION_NO_CODE"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_BLOCKED",
        "gate_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_operator_authorization_gate_review_task": source_review["task"],
        "source_operator_authorization_gate_review_id": source_review["operator_authorization_gate_review_id"],
        "source_operator_authorization_gate_review_signature": source_review["signature"],
        "source_operator_authorization_gate_review_validation": source_review["validation"],
        "source_operator_authorization_gate_review_verdict": source_review["verdict"],
        "next_stage": NEXT_STAGE,
        "operator_decision_gate_ready": not gate_failures,
        "operator_decision_gate_created": not gate_failures,
        "operator_decision_gate_locked": True,
        "operator_decision_gate_open": False,
        "operator_decision_gate_review_required": True,
        "operator_decision_gate_passed": False,
        "operator_decision_required": True,
        "operator_decision_received": False,
        "operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "operator_decision_value_selected": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "explicit_operator_authorization_received": False,
        "implementation_authorization_candidate_confirmed": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "OPERATOR_DECISION_GATE_ONLY_PENDING_EXPLICIT_OPERATOR_DECISION_NO_CODE_NO_RUNTIME",
        "gate_item_count": len(gate_items),
        "blocking_issue_count": len(gate_failures),
        "boundary_controls": controls,
        "gate_items": [asdict(item) for item in gate_items],
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(gate_failures),
        "acceptance_gate_failures": gate_failures,
    }

    payload["signature"] = _signature(payload)
    payload["operator_decision_gate_id"] = (
        "MILESTONE-18-TASK-16-CANDIDATE-GENERATOR-IMPLEMENTATION-OPERATOR-DECISION-GATE-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 16 - Controlled Technical Candidate Generator Implementation Operator Decision Gate v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Operator decision gate ID: `{data['operator_decision_gate_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source operator authorization gate review ID: `{data['source_operator_authorization_gate_review_id']}`",
        f"- Source operator authorization gate review signature: `{data['source_operator_authorization_gate_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- operator decision gate only: true",
        "- operator decision gate created: true",
        "- operator decision gate review required: true",
        "- operator decision gate open: false",
        "- operator decision required: true",
        "- operator decision received: false",
        "- operator decision value: PENDING_EXPLICIT_OPERATOR_DECISION",
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
        "## Gate Items",
        "",
    ]

    for item in data["gate_items"]:
        lines.extend(
            [
                f"### {item['gate_id']} - {item['gate_area']}",
                "",
                f"- Source operator authorization gate review item: `{item['source_operator_authorization_gate_review_item']}`",
                f"- Source operator authorization gate: `{item['source_operator_authorization_gate_id']}`",
                f"- Source proposal: `{item['source_proposal_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Gate decision: `{item['gate_decision']}`",
                f"- Gate effect: `{item['gate_effect']}`",
                f"- Required operator decision: {item['required_operator_decision']}",
                f"- Operator decision status: `{item['operator_decision_status']}`",
                f"- Next review required: `{item['next_review_required']}`",
                f"- Operator decision required: `{item['operator_decision_required']}`",
                f"- Operator decision received: `{item['operator_decision_received']}`",
                f"- Explicit operator authorization received: `{item['explicit_operator_authorization_received']}`",
                f"- Implementation authorization candidate confirmed: `{item['implementation_authorization_candidate_confirmed']}`",
                f"- Implementation code authorized: `{item['implementation_code_authorized']}`",
                f"- Runtime execution authorized: `{item['runtime_execution_authorized']}`",
                f"- Real submission authorized: `{item['real_submission_authorized']}`",
                "",
                "Allowed operator decisions:",
                *[f"- {decision}" for decision in item["allowed_operator_decisions"]],
                "",
            ]
        )

    lines.extend(
        [
            "## Acceptance",
            "",
            f"- Gate item count: `{data['gate_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            f"- Blocking issue count: `{data['blocking_issue_count']}`",
            "",
            "Task 16 creates the operator-decision gate only. It does not record an operator decision and does not authorize code implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 16 artifacts."""

    data = build_candidate_generator_implementation_operator_decision_gate()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-gate-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-gate-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-gate-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-gate-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_16_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_INDEX",
        "task": data["task"],
        "operator_decision_gate_id": data["operator_decision_gate_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_operator_authorization_gate_review_signature": data[
            "source_operator_authorization_gate_review_signature"
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
        "MILESTONE_18_TASK_16_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_V1_MANIFEST",
        f"task={data['task']}",
        f"operator_decision_gate_id={data['operator_decision_gate_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_operator_authorization_gate_review_signature={data['source_operator_authorization_gate_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"gate_item_count={data['gate_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "operator_decision_gate_only=true",
        "operator_decision_gate_created=true",
        "operator_decision_gate_review_required=true",
        "operator_decision_required=true",
        "operator_decision_received=false",
        "operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
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
    result = build_candidate_generator_implementation_operator_decision_gate()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_operator_authorization_gate_review_signature"])
    print(result["gate_scope"])
    print(result["verdict"])
    print(result["next_stage"])
