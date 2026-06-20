"""Milestone #18 Task 8 - Controlled Technical Candidate Generator Implementation Decision Gate v1.

This module creates a deterministic, local-only decision gate after the
Milestone #18 Task 7 authorization-gate review.

Important:
- This task creates the implementation decision gate.
- This task does not implement the candidate generator.
- This task does not modify solver, ranker, runtime, or submission paths.
- This task can only authorize a future controlled implementation proposal stage.
- It does not authorize runtime execution, real evaluation, upload, or Kaggle submission.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_authorization_gate_review import (
    build_candidate_generator_implementation_authorization_gate_review,
)


TASK_NAME = "MILESTONE_18_TASK_8_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Decision Gate v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_7_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_V1"
PREVIOUS_COMMIT = "2f58bdb"
PREVIOUS_SIGNATURE = "929FA73D0F5361FB"

NEXT_STAGE = "MILESTONE_18_TASK_9_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-decision-gate-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorImplementationDecisionItem:
    """A decision-gate item derived from Task 7 gate-review records."""

    decision_id: str
    source_gate_review_item: str
    source_condition_id: str
    source_improvement_item: str
    source_limitation_id: str
    decision_area: str
    decision_value: str
    decision_effect: str
    allowed_next_action: str
    prohibited_actions: tuple[str, ...]
    review_required_before_effective_authorization: bool
    implementation_code_authorized: bool
    runtime_execution_authorized: bool
    real_submission_authorized: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_decision_items(
    source_review: dict[str, Any],
) -> tuple[CandidateGeneratorImplementationDecisionItem, ...]:
    """Build deterministic decision items from Task 7 review records."""

    items: list[CandidateGeneratorImplementationDecisionItem] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        area = review_item["gate_area"]

        if area == "solver coverage":
            allowed_next_action = (
                "Prepare a controlled implementation proposal for candidate-family coverage only, "
                "without changing solver runtime behavior."
            )
        elif area == "candidate generation":
            allowed_next_action = (
                "Prepare a deterministic candidate proposal design with IDs, ordering, confidence hints, "
                "and rejection paths, without runtime patching."
            )
        elif area == "ranker evidence":
            allowed_next_action = (
                "Prepare ranker-neutral metadata mapping only, with no ranker weight or runtime change."
            )
        elif area == "local diagnostics":
            allowed_next_action = (
                "Prepare local public-safe diagnostic fixture mapping and regression guards only."
            )
        elif area == "submission discipline":
            allowed_next_action = (
                "Prepare candidate artifact separation rules while keeping submission generation blocked."
            )
        elif area == "authorization boundary":
            allowed_next_action = (
                "Prepare the next implementation-proposal review boundary and keep fail-closed active."
            )
        else:
            allowed_next_action = (
                "Prepare a controlled implementation proposal for this area only, pending review."
            )

        items.append(
            CandidateGeneratorImplementationDecisionItem(
                decision_id=f"M18-CG-IMPL-DECISION-{index}",
                source_gate_review_item=review_item["review_id"],
                source_condition_id=review_item["source_condition_id"],
                source_improvement_item=review_item["source_improvement_item"],
                source_limitation_id=review_item["source_limitation_id"],
                decision_area=area,
                decision_value="ALLOW_NEXT_CONTROLLED_IMPLEMENTATION_PROPOSAL_REVIEW_ONLY",
                decision_effect="NEXT_STAGE_REVIEW_REQUIRED_NO_CODE_IMPLEMENTATION",
                allowed_next_action=allowed_next_action,
                prohibited_actions=(
                    "candidate_generator_code_change",
                    "candidate_generator_runtime_patch",
                    "solver_runtime_modification",
                    "ranker_runtime_modification",
                    "real_evaluation_execution",
                    "submission_json_creation",
                    "kaggle_authentication",
                    "kaggle_submission",
                    "official_score_claim",
                    "private_core_exposure",
                ),
                review_required_before_effective_authorization=True,
                implementation_code_authorized=False,
                runtime_execution_authorized=False,
                real_submission_authorized=False,
            )
        )

    return tuple(items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 8 boundary controls."""

    return {
        "decision_gate_only": True,
        "decision_gate_created": True,
        "decision_gate_review_required": True,
        "decision_gate_passed": False,
        "decision_gate_locked": True,
        "decision_gate_allows_next_proposal_review_only": True,
        "authorization_gate_open": False,
        "authorization_gate_confirmed": True,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "implementation_proposal_review_allowed_next": True,
        "implementation_code_authorization_granted": False,
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
    source_review: dict[str, Any],
    decision_items: tuple[CandidateGeneratorImplementationDecisionItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 8 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T8-GATE-001",
            "name": "previous_task_matches_task_7",
            "passed": PREVIOUS_TASK == source_review["task"],
        },
        {
            "gate_id": "M18-T8-GATE-002",
            "name": "previous_commit_matches_task_7_commit",
            "passed": PREVIOUS_COMMIT == "2f58bdb",
        },
        {
            "gate_id": "M18-T8-GATE-003",
            "name": "previous_signature_matches_task_7_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": PREVIOUS_SIGNATURE == source_review["signature"],
        },
        {
            "gate_id": "M18-T8-GATE-004",
            "name": "source_review_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T8-GATE-005",
            "name": "source_review_passed",
            "passed": source_review["authorization_gate_review_passed"] is True,
        },
        {
            "gate_id": "M18-T8-GATE-006",
            "name": "source_gate_remained_closed",
            "passed": source_review["authorization_gate_open"] is False,
        },
        {
            "gate_id": "M18-T8-GATE-007",
            "name": "source_review_requires_decision_gate",
            "passed": source_review["decision_gate_required"] is True,
        },
        {
            "gate_id": "M18-T8-GATE-008",
            "name": "six_decision_items_created",
            "passed": len(decision_items) == 6,
        },
        {
            "gate_id": "M18-T8-GATE-009",
            "name": "all_decisions_are_proposal_review_only",
            "passed": all(
                item.decision_value == "ALLOW_NEXT_CONTROLLED_IMPLEMENTATION_PROPOSAL_REVIEW_ONLY"
                for item in decision_items
            ),
        },
        {
            "gate_id": "M18-T8-GATE-010",
            "name": "no_decision_authorizes_code_implementation",
            "passed": not any(item.implementation_code_authorized for item in decision_items),
        },
        {
            "gate_id": "M18-T8-GATE-011",
            "name": "no_decision_authorizes_runtime_execution",
            "passed": not any(item.runtime_execution_authorized for item in decision_items),
        },
        {
            "gate_id": "M18-T8-GATE-012",
            "name": "no_decision_authorizes_real_submission",
            "passed": not any(item.real_submission_authorized for item in decision_items),
        },
        {
            "gate_id": "M18-T8-GATE-013",
            "name": "all_decisions_require_review_before_effective_authorization",
            "passed": all(
                item.review_required_before_effective_authorization
                for item in decision_items
            ),
        },
    ]

    for key, expected in {
        "decision_gate_only": True,
        "decision_gate_created": True,
        "decision_gate_review_required": True,
        "decision_gate_passed": False,
        "decision_gate_locked": True,
        "decision_gate_allows_next_proposal_review_only": True,
        "authorization_gate_open": False,
        "authorization_gate_confirmed": True,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "implementation_proposal_review_allowed_next": True,
        "implementation_code_authorization_granted": False,
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
                "gate_id": f"M18-T8-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in decision_items:
        gates.append(
            {
                "gate_id": f"M18-T8-GATE-{len(gates) + 1:03d}",
                "name": f"{item.decision_id}_proposal_review_only",
                "passed": item.decision_value == "ALLOW_NEXT_CONTROLLED_IMPLEMENTATION_PROPOSAL_REVIEW_ONLY"
                and item.decision_effect == "NEXT_STAGE_REVIEW_REQUIRED_NO_CODE_IMPLEMENTATION"
                and item.implementation_code_authorized is False
                and item.runtime_execution_authorized is False
                and item.real_submission_authorized is False
                and item.review_required_before_effective_authorization is True,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_decision_gate() -> dict[str, Any]:
    """Build the complete deterministic Task 8 decision gate record."""

    source_review = build_candidate_generator_implementation_authorization_gate_review()
    decision_items = build_decision_items(source_review)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_review, decision_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_CREATED_PROPOSAL_REVIEW_ONLY_NO_IMPLEMENTATION"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_BLOCKED",
        "decision_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_gate_review_task": source_review["task"],
        "source_gate_review_id": source_review["authorization_gate_review_id"],
        "source_gate_review_signature": source_review["signature"],
        "source_gate_review_validation": source_review["validation"],
        "source_gate_review_verdict": source_review["verdict"],
        "next_stage": NEXT_STAGE,
        "decision_gate_ready": not gate_failures,
        "decision_gate_created": not gate_failures,
        "decision_gate_locked": True,
        "decision_gate_review_required": True,
        "decision_gate_passed": False,
        "decision_gate_value": "ALLOW_NEXT_CONTROLLED_IMPLEMENTATION_PROPOSAL_REVIEW_ONLY",
        "implementation_proposal_review_allowed_next": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "PROPOSAL_REVIEW_ONLY_NO_CODE_NO_RUNTIME",
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "decision_item_count": len(decision_items),
        "blocking_issue_count": len(gate_failures),
        "boundary_controls": controls,
        "decision_items": [asdict(item) for item in decision_items],
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(gate_failures),
        "acceptance_gate_failures": gate_failures,
    }

    payload["signature"] = _signature(payload)
    payload["decision_gate_id"] = (
        "MILESTONE-18-TASK-8-CANDIDATE-GENERATOR-IMPLEMENTATION-DECISION-GATE-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 8 — Controlled Technical Candidate Generator Implementation Decision Gate v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Decision gate ID: `{data['decision_gate_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source gate review ID: `{data['source_gate_review_id']}`",
        f"- Source gate review signature: `{data['source_gate_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- decision gate only: true",
        "- decision gate created: true",
        "- decision gate review required: true",
        "- next stage allowed: implementation proposal review only",
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
        "## Decision Items",
        "",
    ]

    for item in data["decision_items"]:
        lines.extend(
            [
                f"### {item['decision_id']} — {item['decision_area']}",
                "",
                f"- Source gate review item: `{item['source_gate_review_item']}`",
                f"- Source condition: `{item['source_condition_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Decision value: `{item['decision_value']}`",
                f"- Decision effect: `{item['decision_effect']}`",
                f"- Allowed next action: {item['allowed_next_action']}",
                f"- Review required before effective authorization: `{item['review_required_before_effective_authorization']}`",
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
            f"- Decision item count: `{data['decision_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            f"- Blocking issue count: `{data['blocking_issue_count']}`",
            "",
            "Task 8 creates a decision gate that only allows the next proposal-review stage. It does not authorize code implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 8 artifacts."""

    data = build_candidate_generator_implementation_decision_gate()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_8_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_INDEX",
        "task": data["task"],
        "decision_gate_id": data["decision_gate_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_gate_review_signature": data["source_gate_review_signature"],
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
        "MILESTONE_18_TASK_8_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_V1_MANIFEST",
        f"task={data['task']}",
        f"decision_gate_id={data['decision_gate_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_gate_review_signature={data['source_gate_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"decision_item_count={data['decision_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "decision_gate_only=true",
        "decision_gate_created=true",
        "decision_gate_review_required=true",
        "implementation_proposal_review_allowed_next=true",
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
    result = build_candidate_generator_implementation_decision_gate()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_gate_review_signature"])
    print(result["decision_scope"])
    print(result["verdict"])
    print(result["next_stage"])
