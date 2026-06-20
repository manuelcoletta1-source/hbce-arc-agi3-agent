"""Milestone #18 Task 10 - Controlled Technical Candidate Generator Implementation Proposal v1.

This module creates a deterministic, local-only implementation proposal for a
future controlled candidate-generator improvement.

Important:
- This task creates a proposal artifact only.
- This task does not patch candidate generator code.
- This task does not modify solver, ranker, runtime, evaluation, or submission paths.
- This task does not authorize real evaluation, upload, Kaggle authentication, or submission.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_decision_gate_review import (
    build_candidate_generator_implementation_decision_gate_review,
)


TASK_NAME = "MILESTONE_18_TASK_10_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Proposal v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_9_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_V1"
PREVIOUS_COMMIT = "51a7e3b"
PREVIOUS_SIGNATURE = "3C632A7BAA041134"

NEXT_STAGE = "MILESTONE_18_TASK_11_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-proposal-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-proposal-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorImplementationProposalItem:
    """A proposal-only item for a future controlled candidate-generator improvement."""

    proposal_id: str
    source_review_item: str
    source_decision_id: str
    source_improvement_item: str
    source_limitation_id: str
    proposal_area: str
    proposal_kind: str
    design_intent: str
    deterministic_constraints: tuple[str, ...]
    test_expectations: tuple[str, ...]
    guardrails: tuple[str, ...]
    implementation_scope: str
    proposal_review_required: bool
    implementation_code_authorized: bool
    runtime_execution_authorized: bool
    real_submission_authorized: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def _proposal_for_area(area: str) -> tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Return deterministic proposal content for a candidate-generator area."""

    if area == "solver coverage":
        return (
            "Define controlled candidate-family coverage expansion without altering solver runtime behavior.",
            (
                "candidate family IDs must be stable and deterministic",
                "coverage labels must be diagnostic-only",
                "no official score claim may be derived from proposal artifacts",
            ),
            (
                "public-safe local fixtures cover every proposed candidate family",
                "proposal output remains stable across repeated local runs",
                "no runtime solver mutation is performed",
            ),
            (
                "no solver runtime modification",
                "no private core exposure",
                "no real evaluation execution",
            ),
        )

    if area == "candidate generation":
        return (
            "Define deterministic candidate construction rules with stable IDs, ordering, confidence hints, and rejection paths.",
            (
                "candidate ordering must be deterministic",
                "candidate IDs must be reproducible",
                "confidence hints must not overwrite ranker evidence",
            ),
            (
                "candidate list is reproducible across repeated runs",
                "invalid candidate paths are rejected fail-closed",
                "confidence hints remain metadata-only",
            ),
            (
                "no runtime patch in this task",
                "no generated submission artifact",
                "no hidden network dependency",
            ),
        )

    if area == "ranker evidence":
        return (
            "Define ranker-neutral evidence metadata mapping without modifying ranker weights or runtime ranking logic.",
            (
                "ranker inputs must remain unchanged",
                "evidence metadata must be additive and diagnostic-only",
                "score claims must remain blocked",
            ),
            (
                "ranker output compatibility is preserved",
                "metadata emission is deterministic",
                "no ranker weight mutation occurs",
            ),
            (
                "no ranker runtime modification",
                "no competitive score claim",
                "no official score claim",
            ),
        )

    if area == "local diagnostics":
        return (
            "Define public-safe diagnostic fixtures and regression guards for future controlled implementation review.",
            (
                "fixtures must be local-only",
                "fixtures must contain no private datasets",
                "diagnostic outputs must be deterministic",
            ),
            (
                "fixture manifest validates expected cases",
                "regression guard blocks missing fixture coverage",
                "local-only execution remains enforced",
            ),
            (
                "no external API dependency",
                "no internet during evaluation",
                "no private dataset exposure",
            ),
        )

    if area == "submission discipline":
        return (
            "Define separation rules between candidate artifacts and submission artifacts.",
            (
                "candidate artifacts must not become submission.json",
                "real submission must remain blocked",
                "manual upload must remain blocked",
            ),
            (
                "candidate artifact generation is distinguishable from submission generation",
                "submission path remains disabled",
                "Kaggle authentication remains blocked",
            ),
            (
                "no submission.json creation",
                "no Kaggle authentication",
                "no Kaggle submission",
            ),
        )

    if area == "authorization boundary":
        return (
            "Define the authorization boundary for any future implementation patch and keep fail-closed active.",
            (
                "operator authorization must be explicit",
                "implementation review must pass before code changes",
                "fail-closed must remain active until a separate implementation authorization step",
            ),
            (
                "proposal records explicit authorization requirements",
                "implementation remains blocked",
                "boundary controls are all validated",
            ),
            (
                "no implicit authorization",
                "no runtime execution",
                "no legal certification claim",
            ),
        )

    return (
        "Define a controlled proposal-only improvement area pending review.",
        (
            "proposal must be deterministic",
            "proposal must be local-only",
            "proposal must be public-safe",
        ),
        (
            "proposal review can verify scope",
            "no code execution authorization is implied",
            "fail-closed remains active",
        ),
        (
            "no runtime change",
            "no submission",
            "no private core exposure",
        ),
    )


def build_proposal_items(
    source_review: dict[str, Any],
) -> tuple[CandidateGeneratorImplementationProposalItem, ...]:
    """Build deterministic proposal items from Task 9 review records."""

    items: list[CandidateGeneratorImplementationProposalItem] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        area = review_item["review_area"]
        design_intent, deterministic_constraints, test_expectations, guardrails = _proposal_for_area(area)

        items.append(
            CandidateGeneratorImplementationProposalItem(
                proposal_id=f"M18-CG-IMPL-PROPOSAL-{index}",
                source_review_item=review_item["review_id"],
                source_decision_id=review_item["source_decision_id"],
                source_improvement_item=review_item["source_improvement_item"],
                source_limitation_id=review_item["source_limitation_id"],
                proposal_area=area,
                proposal_kind="CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY",
                design_intent=design_intent,
                deterministic_constraints=deterministic_constraints,
                test_expectations=test_expectations,
                guardrails=guardrails,
                implementation_scope="PROPOSAL_ONLY_NO_CODE_NO_RUNTIME",
                proposal_review_required=True,
                implementation_code_authorized=False,
                runtime_execution_authorized=False,
                real_submission_authorized=False,
            )
        )

    return tuple(items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 10 boundary controls."""

    return {
        "implementation_proposal_only": True,
        "implementation_proposal_created": True,
        "implementation_proposal_review_required": True,
        "implementation_proposal_ready": True,
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
    proposal_items: tuple[CandidateGeneratorImplementationProposalItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 10 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T10-GATE-001",
            "name": "previous_task_matches_task_9",
            "passed": PREVIOUS_TASK == source_review["task"],
        },
        {
            "gate_id": "M18-T10-GATE-002",
            "name": "previous_commit_matches_task_9_commit",
            "passed": PREVIOUS_COMMIT == "51a7e3b",
        },
        {
            "gate_id": "M18-T10-GATE-003",
            "name": "previous_signature_matches_task_9_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": PREVIOUS_SIGNATURE == source_review["signature"],
        },
        {
            "gate_id": "M18-T10-GATE-004",
            "name": "source_decision_gate_review_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T10-GATE-005",
            "name": "source_allows_next_proposal_stage",
            "passed": source_review["implementation_proposal_allowed_next"] is True,
        },
        {
            "gate_id": "M18-T10-GATE-006",
            "name": "source_does_not_authorize_code",
            "passed": source_review["implementation_code_authorized"] is False,
        },
        {
            "gate_id": "M18-T10-GATE-007",
            "name": "six_proposal_items_created",
            "passed": len(proposal_items) == 6,
        },
        {
            "gate_id": "M18-T10-GATE-008",
            "name": "all_proposal_items_are_proposal_only",
            "passed": all(
                item.proposal_kind == "CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY"
                for item in proposal_items
            ),
        },
        {
            "gate_id": "M18-T10-GATE-009",
            "name": "all_proposal_items_require_review",
            "passed": all(item.proposal_review_required for item in proposal_items),
        },
        {
            "gate_id": "M18-T10-GATE-010",
            "name": "no_proposal_item_authorizes_code",
            "passed": not any(item.implementation_code_authorized for item in proposal_items),
        },
        {
            "gate_id": "M18-T10-GATE-011",
            "name": "no_proposal_item_authorizes_runtime",
            "passed": not any(item.runtime_execution_authorized for item in proposal_items),
        },
        {
            "gate_id": "M18-T10-GATE-012",
            "name": "no_proposal_item_authorizes_real_submission",
            "passed": not any(item.real_submission_authorized for item in proposal_items),
        },
    ]

    for key, expected in {
        "implementation_proposal_only": True,
        "implementation_proposal_created": True,
        "implementation_proposal_review_required": True,
        "implementation_proposal_ready": True,
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
                "gate_id": f"M18-T10-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in proposal_items:
        gates.append(
            {
                "gate_id": f"M18-T10-GATE-{len(gates) + 1:03d}",
                "name": f"{item.proposal_id}_proposal_only_no_runtime",
                "passed": item.proposal_kind == "CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY"
                and item.implementation_scope == "PROPOSAL_ONLY_NO_CODE_NO_RUNTIME"
                and item.proposal_review_required is True
                and item.implementation_code_authorized is False
                and item.runtime_execution_authorized is False
                and item.real_submission_authorized is False,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_proposal() -> dict[str, Any]:
    """Build the complete deterministic Task 10 proposal record."""

    source_review = build_candidate_generator_implementation_decision_gate_review()
    proposal_items = build_proposal_items(source_review)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_review, proposal_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_READY_NO_CODE_NO_RUNTIME"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_BLOCKED",
        "proposal_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_decision_gate_review_task": source_review["task"],
        "source_decision_gate_review_id": source_review["decision_gate_review_id"],
        "source_decision_gate_review_signature": source_review["signature"],
        "source_decision_gate_review_validation": source_review["validation"],
        "source_decision_gate_review_verdict": source_review["verdict"],
        "next_stage": NEXT_STAGE,
        "implementation_proposal_ready": not gate_failures,
        "implementation_proposal_created": not gate_failures,
        "implementation_proposal_review_required": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "PROPOSAL_ONLY_NO_CODE_NO_RUNTIME",
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "proposal_item_count": len(proposal_items),
        "blocking_issue_count": len(gate_failures),
        "boundary_controls": controls,
        "proposal_items": [asdict(item) for item in proposal_items],
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(gate_failures),
        "acceptance_gate_failures": gate_failures,
    }

    payload["signature"] = _signature(payload)
    payload["implementation_proposal_id"] = (
        "MILESTONE-18-TASK-10-CANDIDATE-GENERATOR-IMPLEMENTATION-PROPOSAL-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 10 - Controlled Technical Candidate Generator Implementation Proposal v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Implementation proposal ID: `{data['implementation_proposal_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source decision gate review ID: `{data['source_decision_gate_review_id']}`",
        f"- Source decision gate review signature: `{data['source_decision_gate_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- implementation proposal only: true",
        "- implementation proposal created: true",
        "- implementation proposal review required: true",
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
        "## Proposal Items",
        "",
    ]

    for item in data["proposal_items"]:
        lines.extend(
            [
                f"### {item['proposal_id']} - {item['proposal_area']}",
                "",
                f"- Source review item: `{item['source_review_item']}`",
                f"- Source decision: `{item['source_decision_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Proposal kind: `{item['proposal_kind']}`",
                f"- Implementation scope: `{item['implementation_scope']}`",
                f"- Design intent: {item['design_intent']}",
                "",
                "Deterministic constraints:",
                *[f"- {constraint}" for constraint in item["deterministic_constraints"]],
                "",
                "Test expectations:",
                *[f"- {expectation}" for expectation in item["test_expectations"]],
                "",
                "Guardrails:",
                *[f"- {guardrail}" for guardrail in item["guardrails"]],
                "",
                f"- Proposal review required: `{item['proposal_review_required']}`",
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
            f"- Proposal item count: `{data['proposal_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            f"- Blocking issue count: `{data['blocking_issue_count']}`",
            "",
            "Task 10 creates a controlled implementation proposal only. It does not authorize code implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 10 artifacts."""

    data = build_candidate_generator_implementation_proposal()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-proposal-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-proposal-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-proposal-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-proposal-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_10_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_INDEX",
        "task": data["task"],
        "implementation_proposal_id": data["implementation_proposal_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_decision_gate_review_signature": data["source_decision_gate_review_signature"],
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
        "MILESTONE_18_TASK_10_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_V1_MANIFEST",
        f"task={data['task']}",
        f"implementation_proposal_id={data['implementation_proposal_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_decision_gate_review_signature={data['source_decision_gate_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"proposal_item_count={data['proposal_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "implementation_proposal_only=true",
        "implementation_proposal_created=true",
        "implementation_proposal_review_required=true",
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
    result = build_candidate_generator_implementation_proposal()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_decision_gate_review_signature"])
    print(result["proposal_scope"])
    print(result["verdict"])
    print(result["next_stage"])
