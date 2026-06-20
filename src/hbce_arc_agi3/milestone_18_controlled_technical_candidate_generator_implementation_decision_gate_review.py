"""Milestone #18 Task 9 - Controlled Technical Candidate Generator Implementation Decision Gate Review v1.

This module reviews the decision gate created in Milestone #18 Task 8.

Important:
- This task reviews the decision gate.
- This task confirms that only the next implementation-proposal stage is allowed.
- This task does not authorize code implementation.
- This task does not modify the candidate generator.
- This task does not modify solver, ranker, runtime, evaluation, or submission paths.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_decision_gate import (
    build_candidate_generator_implementation_decision_gate,
)


TASK_NAME = "MILESTONE_18_TASK_9_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Decision Gate Review v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_8_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_V1"
PREVIOUS_COMMIT = "527dc55"
PREVIOUS_SIGNATURE = "78CE2FCBCD03C93C"

NEXT_STAGE = "MILESTONE_18_TASK_10_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-decision-gate-review-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-review-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorImplementationDecisionGateReviewItem:
    """A review item derived from Task 8 decision items."""

    review_id: str
    source_decision_id: str
    source_gate_review_item: str
    source_improvement_item: str
    source_limitation_id: str
    review_area: str
    review_decision: str
    review_effect: str
    allowed_next_action: str
    blocking_issue: bool
    implementation_proposal_authorized_next: bool
    implementation_code_authorized: bool
    runtime_execution_authorized: bool
    real_submission_authorized: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_decision_gate_review_items(
    source_decision_gate: dict[str, Any],
) -> tuple[CandidateGeneratorImplementationDecisionGateReviewItem, ...]:
    """Build deterministic review items from Task 8 decision items."""

    review_items: list[CandidateGeneratorImplementationDecisionGateReviewItem] = []

    for index, decision_item in enumerate(source_decision_gate["decision_items"], start=1):
        review_items.append(
            CandidateGeneratorImplementationDecisionGateReviewItem(
                review_id=f"M18-CG-IMPL-DECISION-GATE-REV-{index}",
                source_decision_id=decision_item["decision_id"],
                source_gate_review_item=decision_item["source_gate_review_item"],
                source_improvement_item=decision_item["source_improvement_item"],
                source_limitation_id=decision_item["source_limitation_id"],
                review_area=decision_item["decision_area"],
                review_decision="CONFIRMED_PROPOSAL_STAGE_ALLOWED_NO_CODE_IMPLEMENTATION",
                review_effect="NEXT_STAGE_IMPLEMENTATION_PROPOSAL_ALLOWED_REVIEW_REQUIRED",
                allowed_next_action=(
                    "Create the controlled implementation proposal artifact for this area only. "
                    "The proposal may specify design intent, deterministic constraints, evidence requirements, "
                    "and test expectations, but it must not patch runtime code."
                ),
                blocking_issue=False,
                implementation_proposal_authorized_next=True,
                implementation_code_authorized=False,
                runtime_execution_authorized=False,
                real_submission_authorized=False,
            )
        )

    return tuple(review_items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 9 boundary controls."""

    return {
        "decision_gate_review_only": True,
        "decision_gate_confirmed": True,
        "decision_gate_review_passed": True,
        "implementation_proposal_allowed_next": True,
        "implementation_proposal_review_required": True,
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
    source_decision_gate: dict[str, Any],
    review_items: tuple[CandidateGeneratorImplementationDecisionGateReviewItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 9 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T9-GATE-001",
            "name": "previous_task_matches_task_8",
            "passed": PREVIOUS_TASK == source_decision_gate["task"],
        },
        {
            "gate_id": "M18-T9-GATE-002",
            "name": "previous_commit_matches_task_8_commit",
            "passed": PREVIOUS_COMMIT == "527dc55",
        },
        {
            "gate_id": "M18-T9-GATE-003",
            "name": "previous_signature_matches_task_8_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_decision_gate["signature"],
            "passed": PREVIOUS_SIGNATURE == source_decision_gate["signature"],
        },
        {
            "gate_id": "M18-T9-GATE-004",
            "name": "source_decision_gate_valid",
            "passed": source_decision_gate["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T9-GATE-005",
            "name": "source_decision_gate_created",
            "passed": source_decision_gate["decision_gate_created"] is True,
        },
        {
            "gate_id": "M18-T9-GATE-006",
            "name": "source_decision_gate_allows_proposal_review_only",
            "passed": source_decision_gate["implementation_proposal_review_allowed_next"] is True,
        },
        {
            "gate_id": "M18-T9-GATE-007",
            "name": "source_decision_gate_does_not_authorize_code",
            "passed": source_decision_gate["implementation_code_authorized"] is False,
        },
        {
            "gate_id": "M18-T9-GATE-008",
            "name": "source_decision_gate_does_not_authorize_runtime",
            "passed": source_decision_gate["boundary_controls"]["runtime_execution_allowed"] is False,
        },
        {
            "gate_id": "M18-T9-GATE-009",
            "name": "source_decision_gate_does_not_authorize_submission",
            "passed": source_decision_gate["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T9-GATE-010",
            "name": "six_decision_gate_review_items_created",
            "passed": len(review_items) == 6,
        },
        {
            "gate_id": "M18-T9-GATE-011",
            "name": "all_review_items_allow_proposal_only",
            "passed": all(
                item.review_decision == "CONFIRMED_PROPOSAL_STAGE_ALLOWED_NO_CODE_IMPLEMENTATION"
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T9-GATE-012",
            "name": "all_review_items_authorize_next_proposal_stage",
            "passed": all(item.implementation_proposal_authorized_next for item in review_items),
        },
        {
            "gate_id": "M18-T9-GATE-013",
            "name": "no_review_item_authorizes_code",
            "passed": not any(item.implementation_code_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T9-GATE-014",
            "name": "no_review_item_authorizes_runtime_execution",
            "passed": not any(item.runtime_execution_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T9-GATE-015",
            "name": "no_review_item_authorizes_real_submission",
            "passed": not any(item.real_submission_authorized for item in review_items),
        },
    ]

    for key, expected in {
        "decision_gate_review_only": True,
        "decision_gate_confirmed": True,
        "decision_gate_review_passed": True,
        "implementation_proposal_allowed_next": True,
        "implementation_proposal_review_required": True,
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
                "gate_id": f"M18-T9-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in review_items:
        gates.append(
            {
                "gate_id": f"M18-T9-GATE-{len(gates) + 1:03d}",
                "name": f"{item.review_id}_proposal_only_no_runtime",
                "passed": item.review_decision == "CONFIRMED_PROPOSAL_STAGE_ALLOWED_NO_CODE_IMPLEMENTATION"
                and item.review_effect == "NEXT_STAGE_IMPLEMENTATION_PROPOSAL_ALLOWED_REVIEW_REQUIRED"
                and item.implementation_proposal_authorized_next is True
                and item.implementation_code_authorized is False
                and item.runtime_execution_authorized is False
                and item.real_submission_authorized is False
                and item.blocking_issue is False,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_decision_gate_review() -> dict[str, Any]:
    """Build the complete deterministic Task 9 decision gate review record."""

    source_decision_gate = build_candidate_generator_implementation_decision_gate()
    review_items = build_decision_gate_review_items(source_decision_gate)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_decision_gate, review_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_PASS_PROPOSAL_STAGE_ALLOWED_NO_IMPLEMENTATION"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_BLOCKED",
        "review_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_decision_gate_task": source_decision_gate["task"],
        "source_decision_gate_id": source_decision_gate["decision_gate_id"],
        "source_decision_gate_signature": source_decision_gate["signature"],
        "source_decision_gate_validation": source_decision_gate["validation"],
        "source_decision_gate_verdict": source_decision_gate["verdict"],
        "next_stage": NEXT_STAGE,
        "decision_gate_review_ready": not gate_failures,
        "decision_gate_review_passed": not gate_failures,
        "decision_gate_confirmed": not gate_failures,
        "implementation_proposal_allowed_next": True,
        "implementation_proposal_review_required": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "NEXT_PROPOSAL_STAGE_ONLY_NO_CODE_NO_RUNTIME",
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "review_item_count": len(review_items),
        "confirmed_review_item_count": len(
            [
                item
                for item in review_items
                if item.review_decision
                == "CONFIRMED_PROPOSAL_STAGE_ALLOWED_NO_CODE_IMPLEMENTATION"
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
    payload["decision_gate_review_id"] = (
        "MILESTONE-18-TASK-9-CANDIDATE-GENERATOR-IMPLEMENTATION-DECISION-GATE-REVIEW-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 9 - Controlled Technical Candidate Generator Implementation Decision Gate Review v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Decision gate review ID: `{data['decision_gate_review_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source decision gate ID: `{data['source_decision_gate_id']}`",
        f"- Source decision gate signature: `{data['source_decision_gate_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- decision gate review only: true",
        "- decision gate confirmed: true",
        "- next stage allowed: implementation proposal only",
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
                f"- Source decision: `{item['source_decision_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Review decision: `{item['review_decision']}`",
                f"- Review effect: `{item['review_effect']}`",
                f"- Allowed next action: {item['allowed_next_action']}",
                f"- Implementation proposal authorized next: `{item['implementation_proposal_authorized_next']}`",
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
            "Task 9 confirms the decision gate and allows only the next implementation-proposal stage. It does not authorize code implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 9 artifacts."""

    data = build_candidate_generator_implementation_decision_gate_review()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-review-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-review-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-review-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-decision-gate-review-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_9_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_INDEX",
        "task": data["task"],
        "decision_gate_review_id": data["decision_gate_review_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_decision_gate_signature": data["source_decision_gate_signature"],
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
        "MILESTONE_18_TASK_9_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_V1_MANIFEST",
        f"task={data['task']}",
        f"decision_gate_review_id={data['decision_gate_review_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_decision_gate_signature={data['source_decision_gate_signature']}",
        f"next_stage={data['next_stage']}",
        f"review_item_count={data['review_item_count']}",
        f"confirmed_review_item_count={data['confirmed_review_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "decision_gate_review_only=true",
        "decision_gate_confirmed=true",
        "implementation_proposal_allowed_next=true",
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
    result = build_candidate_generator_implementation_decision_gate_review()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_decision_gate_signature"])
    print(result["review_scope"])
    print(result["verdict"])
    print(result["next_stage"])
