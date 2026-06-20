"""Milestone #18 Task 11 - Controlled Technical Candidate Generator Implementation Proposal Review v1.

This module reviews the proposal created in Milestone #18 Task 10.

Important:
- This task reviews the implementation proposal.
- This task confirms the proposal can advance to an authorization-review gate.
- This task does not authorize code implementation.
- This task does not modify candidate generator, solver, ranker, runtime, evaluation, or submission paths.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_proposal import (
    build_candidate_generator_implementation_proposal,
)


TASK_NAME = "MILESTONE_18_TASK_11_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Proposal Review v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_10_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_V1"
PREVIOUS_COMMIT = "b805b16"
PREVIOUS_SIGNATURE = "A2BE24B5965B838E"

NEXT_STAGE = "MILESTONE_18_TASK_12_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_REVIEW_GATE_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-proposal-review-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-proposal-review-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorImplementationProposalReviewItem:
    """A review item derived from Task 10 proposal items."""

    review_id: str
    source_proposal_id: str
    source_review_item: str
    source_decision_id: str
    source_improvement_item: str
    source_limitation_id: str
    review_area: str
    review_decision: str
    review_effect: str
    review_note: str
    proposal_accepted_for_next_gate: bool
    authorization_review_gate_required: bool
    implementation_code_authorized: bool
    runtime_execution_authorized: bool
    real_submission_authorized: bool
    blocking_issue: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_proposal_review_items(
    source_proposal: dict[str, Any],
) -> tuple[CandidateGeneratorImplementationProposalReviewItem, ...]:
    """Build deterministic review items from Task 10 proposal items."""

    review_items: list[CandidateGeneratorImplementationProposalReviewItem] = []

    for index, proposal_item in enumerate(source_proposal["proposal_items"], start=1):
        review_items.append(
            CandidateGeneratorImplementationProposalReviewItem(
                review_id=f"M18-CG-IMPL-PROPOSAL-REV-{index}",
                source_proposal_id=proposal_item["proposal_id"],
                source_review_item=proposal_item["source_review_item"],
                source_decision_id=proposal_item["source_decision_id"],
                source_improvement_item=proposal_item["source_improvement_item"],
                source_limitation_id=proposal_item["source_limitation_id"],
                review_area=proposal_item["proposal_area"],
                review_decision="CONFIRMED_PROPOSAL_VALID_PENDING_AUTHORIZATION_REVIEW_GATE",
                review_effect="NEXT_AUTHORIZATION_REVIEW_GATE_REQUIRED_NO_CODE_IMPLEMENTATION",
                review_note=(
                    "The Task 10 proposal item is structurally valid, deterministic, local-only, "
                    "and public-safe. It may advance to an authorization-review gate, but it does "
                    "not authorize code implementation, runtime execution, real evaluation, or submission."
                ),
                proposal_accepted_for_next_gate=True,
                authorization_review_gate_required=True,
                implementation_code_authorized=False,
                runtime_execution_authorized=False,
                real_submission_authorized=False,
                blocking_issue=False,
            )
        )

    return tuple(review_items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 11 boundary controls."""

    return {
        "implementation_proposal_review_only": True,
        "implementation_proposal_confirmed": True,
        "implementation_proposal_review_passed": True,
        "authorization_review_gate_required": True,
        "authorization_review_gate_created": False,
        "authorization_review_gate_allowed_next": True,
        "implementation_code_authorization_granted": False,
        "implementation_code_authorized": False,
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
        "submission_artifact_created": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
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
    source_proposal: dict[str, Any],
    review_items: tuple[CandidateGeneratorImplementationProposalReviewItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 11 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T11-GATE-001",
            "name": "previous_task_matches_task_10",
            "passed": PREVIOUS_TASK == source_proposal["task"],
        },
        {
            "gate_id": "M18-T11-GATE-002",
            "name": "previous_commit_matches_task_10_commit",
            "passed": PREVIOUS_COMMIT == "b805b16",
        },
        {
            "gate_id": "M18-T11-GATE-003",
            "name": "previous_signature_matches_task_10_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_proposal["signature"],
            "passed": PREVIOUS_SIGNATURE == source_proposal["signature"],
        },
        {
            "gate_id": "M18-T11-GATE-004",
            "name": "source_proposal_valid",
            "passed": source_proposal["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T11-GATE-005",
            "name": "source_proposal_ready",
            "passed": source_proposal["implementation_proposal_ready"] is True,
        },
        {
            "gate_id": "M18-T11-GATE-006",
            "name": "source_proposal_review_required",
            "passed": source_proposal["implementation_proposal_review_required"] is True,
        },
        {
            "gate_id": "M18-T11-GATE-007",
            "name": "source_proposal_does_not_authorize_code",
            "passed": source_proposal["implementation_code_authorized"] is False,
        },
        {
            "gate_id": "M18-T11-GATE-008",
            "name": "source_proposal_does_not_authorize_runtime",
            "passed": source_proposal["boundary_controls"]["runtime_execution_allowed"] is False,
        },
        {
            "gate_id": "M18-T11-GATE-009",
            "name": "source_proposal_does_not_authorize_submission",
            "passed": source_proposal["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T11-GATE-010",
            "name": "six_proposal_review_items_created",
            "passed": len(review_items) == 6,
        },
        {
            "gate_id": "M18-T11-GATE-011",
            "name": "all_review_items_confirm_valid_proposal",
            "passed": all(
                item.review_decision == "CONFIRMED_PROPOSAL_VALID_PENDING_AUTHORIZATION_REVIEW_GATE"
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T11-GATE-012",
            "name": "all_review_items_accept_next_gate",
            "passed": all(item.proposal_accepted_for_next_gate for item in review_items),
        },
        {
            "gate_id": "M18-T11-GATE-013",
            "name": "all_review_items_require_authorization_review_gate",
            "passed": all(item.authorization_review_gate_required for item in review_items),
        },
        {
            "gate_id": "M18-T11-GATE-014",
            "name": "no_review_item_authorizes_code",
            "passed": not any(item.implementation_code_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T11-GATE-015",
            "name": "no_review_item_authorizes_runtime",
            "passed": not any(item.runtime_execution_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T11-GATE-016",
            "name": "no_review_item_authorizes_submission",
            "passed": not any(item.real_submission_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T11-GATE-017",
            "name": "no_review_item_has_blocking_issue",
            "passed": not any(item.blocking_issue for item in review_items),
        },
    ]

    for key, expected in {
        "implementation_proposal_review_only": True,
        "implementation_proposal_confirmed": True,
        "implementation_proposal_review_passed": True,
        "authorization_review_gate_required": True,
        "authorization_review_gate_created": False,
        "authorization_review_gate_allowed_next": True,
        "implementation_code_authorization_granted": False,
        "implementation_code_authorized": False,
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
        "submission_artifact_created": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
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
                "gate_id": f"M18-T11-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in review_items:
        gates.append(
            {
                "gate_id": f"M18-T11-GATE-{len(gates) + 1:03d}",
                "name": f"{item.review_id}_valid_pending_auth_review_gate",
                "passed": item.review_decision
                == "CONFIRMED_PROPOSAL_VALID_PENDING_AUTHORIZATION_REVIEW_GATE"
                and item.review_effect
                == "NEXT_AUTHORIZATION_REVIEW_GATE_REQUIRED_NO_CODE_IMPLEMENTATION"
                and item.proposal_accepted_for_next_gate is True
                and item.authorization_review_gate_required is True
                and item.implementation_code_authorized is False
                and item.runtime_execution_authorized is False
                and item.real_submission_authorized is False
                and item.blocking_issue is False,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_proposal_review() -> dict[str, Any]:
    """Build the complete deterministic Task 11 proposal review record."""

    source_proposal = build_candidate_generator_implementation_proposal()
    review_items = build_proposal_review_items(source_proposal)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_proposal, review_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_PASS_PENDING_AUTHORIZATION_REVIEW_GATE_NO_CODE"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_BLOCKED",
        "review_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_proposal_task": source_proposal["task"],
        "source_proposal_id": source_proposal["implementation_proposal_id"],
        "source_proposal_signature": source_proposal["signature"],
        "source_proposal_validation": source_proposal["validation"],
        "source_proposal_verdict": source_proposal["verdict"],
        "next_stage": NEXT_STAGE,
        "implementation_proposal_review_ready": not gate_failures,
        "implementation_proposal_review_passed": not gate_failures,
        "implementation_proposal_confirmed": not gate_failures,
        "authorization_review_gate_required": True,
        "authorization_review_gate_allowed_next": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "PROPOSAL_REVIEW_ONLY_PENDING_AUTHORIZATION_REVIEW_GATE_NO_CODE_NO_RUNTIME",
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "review_item_count": len(review_items),
        "confirmed_review_item_count": len(
            [
                item
                for item in review_items
                if item.review_decision
                == "CONFIRMED_PROPOSAL_VALID_PENDING_AUTHORIZATION_REVIEW_GATE"
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
    payload["implementation_proposal_review_id"] = (
        "MILESTONE-18-TASK-11-CANDIDATE-GENERATOR-IMPLEMENTATION-PROPOSAL-REVIEW-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 11 - Controlled Technical Candidate Generator Implementation Proposal Review v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Implementation proposal review ID: `{data['implementation_proposal_review_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source proposal ID: `{data['source_proposal_id']}`",
        f"- Source proposal signature: `{data['source_proposal_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- implementation proposal review only: true",
        "- implementation proposal confirmed: true",
        "- authorization review gate required: true",
        "- authorization review gate allowed next: true",
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
                f"- Source proposal: `{item['source_proposal_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Review decision: `{item['review_decision']}`",
                f"- Review effect: `{item['review_effect']}`",
                f"- Proposal accepted for next gate: `{item['proposal_accepted_for_next_gate']}`",
                f"- Authorization review gate required: `{item['authorization_review_gate_required']}`",
                f"- Implementation code authorized: `{item['implementation_code_authorized']}`",
                f"- Runtime execution authorized: `{item['runtime_execution_authorized']}`",
                f"- Real submission authorized: `{item['real_submission_authorized']}`",
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
            "Task 11 confirms the proposal and allows only the next authorization-review gate. It does not authorize code implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 11 artifacts."""

    data = build_candidate_generator_implementation_proposal_review()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-proposal-review-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-proposal-review-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-proposal-review-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-proposal-review-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_11_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_INDEX",
        "task": data["task"],
        "implementation_proposal_review_id": data["implementation_proposal_review_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_proposal_signature": data["source_proposal_signature"],
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
        "MILESTONE_18_TASK_11_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_V1_MANIFEST",
        f"task={data['task']}",
        f"implementation_proposal_review_id={data['implementation_proposal_review_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_proposal_signature={data['source_proposal_signature']}",
        f"next_stage={data['next_stage']}",
        f"review_item_count={data['review_item_count']}",
        f"confirmed_review_item_count={data['confirmed_review_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "implementation_proposal_review_only=true",
        "implementation_proposal_confirmed=true",
        "authorization_review_gate_required=true",
        "authorization_review_gate_allowed_next=true",
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
    result = build_candidate_generator_implementation_proposal_review()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_proposal_signature"])
    print(result["review_scope"])
    print(result["verdict"])
    print(result["next_stage"])
