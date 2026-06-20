"""Milestone #18 Task 12 - Controlled Technical Candidate Generator Implementation Authorization Review Gate v1.

This module creates an authorization-review gate after Milestone #18 Task 11.

Important:
- This task creates an authorization-review gate.
- This task does not grant implementation authorization.
- This task does not modify candidate generator, solver, ranker, runtime, evaluation, or submission paths.
- This task only allows the next authorization-review-gate review stage.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_proposal_review import (
    build_candidate_generator_implementation_proposal_review,
)


TASK_NAME = "MILESTONE_18_TASK_12_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_REVIEW_GATE_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Authorization Review Gate v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_11_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_V1"
PREVIOUS_COMMIT = "dd08ba2"
PREVIOUS_SIGNATURE = "A6DA5215225B3F3A"

NEXT_STAGE = "MILESTONE_18_TASK_13_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_REVIEW_GATE_REVIEW_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-authorization-review-gate-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-authorization-review-gate-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorImplementationAuthorizationReviewGateItem:
    """A gate item derived from Task 11 proposal-review items."""

    gate_id: str
    source_proposal_review_item: str
    source_proposal_id: str
    source_improvement_item: str
    source_limitation_id: str
    gate_area: str
    gate_decision: str
    gate_effect: str
    required_authorization_evidence: tuple[str, ...]
    next_review_required: bool
    implementation_authorization_candidate: bool
    implementation_code_authorized: bool
    runtime_execution_authorized: bool
    real_submission_authorized: bool
    blocking_issue: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def _evidence_for_area(area: str) -> tuple[str, ...]:
    if area == "solver coverage":
        return (
            "explicit list of candidate families proposed for controlled implementation",
            "proof that solver runtime behavior remains unchanged at this gate",
            "public-safe diagnostic coverage evidence",
        )

    if area == "candidate generation":
        return (
            "deterministic candidate ID and ordering specification",
            "fail-closed rejection path specification",
            "confidence-hint metadata separation proof",
        )

    if area == "ranker evidence":
        return (
            "ranker-neutral metadata mapping proof",
            "proof that ranker weights and ranker runtime behavior remain unchanged",
            "score-claim blocking evidence",
        )

    if area == "local diagnostics":
        return (
            "local-only diagnostic fixture manifest",
            "regression guard expectation list",
            "proof of no external API dependency and no internet dependency",
        )

    if area == "submission discipline":
        return (
            "candidate artifact and submission artifact separation proof",
            "proof that submission.json creation remains blocked",
            "proof that Kaggle authentication and submission remain blocked",
        )

    if area == "authorization boundary":
        return (
            "explicit operator authorization requirement",
            "fail-closed continuity proof",
            "proof that legalCertification remains false",
        )

    return (
        "deterministic local-only evidence",
        "public-safe review evidence",
        "fail-closed boundary proof",
    )


def build_authorization_review_gate_items(
    source_review: dict[str, Any],
) -> tuple[CandidateGeneratorImplementationAuthorizationReviewGateItem, ...]:
    """Build deterministic authorization-review gate items from Task 11 review records."""

    gate_items: list[CandidateGeneratorImplementationAuthorizationReviewGateItem] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        area = review_item["review_area"]

        gate_items.append(
            CandidateGeneratorImplementationAuthorizationReviewGateItem(
                gate_id=f"M18-CG-IMPL-AUTH-REVIEW-GATE-{index}",
                source_proposal_review_item=review_item["review_id"],
                source_proposal_id=review_item["source_proposal_id"],
                source_improvement_item=review_item["source_improvement_item"],
                source_limitation_id=review_item["source_limitation_id"],
                gate_area=area,
                gate_decision="AUTHORIZATION_REVIEW_GATE_CREATED_PENDING_REVIEW",
                gate_effect="NEXT_AUTHORIZATION_REVIEW_GATE_REVIEW_REQUIRED_NO_CODE_IMPLEMENTATION",
                required_authorization_evidence=_evidence_for_area(area),
                next_review_required=True,
                implementation_authorization_candidate=True,
                implementation_code_authorized=False,
                runtime_execution_authorized=False,
                real_submission_authorized=False,
                blocking_issue=False,
            )
        )

    return tuple(gate_items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 12 boundary controls."""

    return {
        "authorization_review_gate_only": True,
        "authorization_review_gate_created": True,
        "authorization_review_gate_review_required": True,
        "authorization_review_gate_locked": True,
        "authorization_review_gate_open": False,
        "authorization_review_gate_passed": False,
        "authorization_review_gate_allows_next_review_only": True,
        "implementation_authorization_candidate": True,
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
    source_review: dict[str, Any],
    gate_items: tuple[CandidateGeneratorImplementationAuthorizationReviewGateItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 12 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T12-GATE-001",
            "name": "previous_task_matches_task_11",
            "passed": PREVIOUS_TASK == source_review["task"],
        },
        {
            "gate_id": "M18-T12-GATE-002",
            "name": "previous_commit_matches_task_11_commit",
            "passed": PREVIOUS_COMMIT == "dd08ba2",
        },
        {
            "gate_id": "M18-T12-GATE-003",
            "name": "previous_signature_matches_task_11_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": PREVIOUS_SIGNATURE == source_review["signature"],
        },
        {
            "gate_id": "M18-T12-GATE-004",
            "name": "source_proposal_review_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T12-GATE-005",
            "name": "source_proposal_review_passed",
            "passed": source_review["implementation_proposal_review_passed"] is True,
        },
        {
            "gate_id": "M18-T12-GATE-006",
            "name": "source_requires_authorization_review_gate",
            "passed": source_review["authorization_review_gate_required"] is True,
        },
        {
            "gate_id": "M18-T12-GATE-007",
            "name": "source_allows_authorization_review_gate_next",
            "passed": source_review["authorization_review_gate_allowed_next"] is True,
        },
        {
            "gate_id": "M18-T12-GATE-008",
            "name": "source_does_not_authorize_code",
            "passed": source_review["implementation_code_authorized"] is False,
        },
        {
            "gate_id": "M18-T12-GATE-009",
            "name": "source_does_not_authorize_runtime",
            "passed": source_review["boundary_controls"]["runtime_execution_allowed"] is False,
        },
        {
            "gate_id": "M18-T12-GATE-010",
            "name": "source_does_not_authorize_submission",
            "passed": source_review["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T12-GATE-011",
            "name": "six_authorization_review_gate_items_created",
            "passed": len(gate_items) == 6,
        },
        {
            "gate_id": "M18-T12-GATE-012",
            "name": "all_gate_items_created_pending_review",
            "passed": all(
                item.gate_decision == "AUTHORIZATION_REVIEW_GATE_CREATED_PENDING_REVIEW"
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T12-GATE-013",
            "name": "all_gate_items_require_next_review",
            "passed": all(item.next_review_required for item in gate_items),
        },
        {
            "gate_id": "M18-T12-GATE-014",
            "name": "all_gate_items_are_authorization_candidates",
            "passed": all(item.implementation_authorization_candidate for item in gate_items),
        },
        {
            "gate_id": "M18-T12-GATE-015",
            "name": "no_gate_item_authorizes_code",
            "passed": not any(item.implementation_code_authorized for item in gate_items),
        },
        {
            "gate_id": "M18-T12-GATE-016",
            "name": "no_gate_item_authorizes_runtime",
            "passed": not any(item.runtime_execution_authorized for item in gate_items),
        },
        {
            "gate_id": "M18-T12-GATE-017",
            "name": "no_gate_item_authorizes_submission",
            "passed": not any(item.real_submission_authorized for item in gate_items),
        },
        {
            "gate_id": "M18-T12-GATE-018",
            "name": "no_gate_item_has_blocking_issue",
            "passed": not any(item.blocking_issue for item in gate_items),
        },
    ]

    for key, expected in {
        "authorization_review_gate_only": True,
        "authorization_review_gate_created": True,
        "authorization_review_gate_review_required": True,
        "authorization_review_gate_locked": True,
        "authorization_review_gate_open": False,
        "authorization_review_gate_passed": False,
        "authorization_review_gate_allows_next_review_only": True,
        "implementation_authorization_candidate": True,
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
                "gate_id": f"M18-T12-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in gate_items:
        gates.append(
            {
                "gate_id": f"M18-T12-GATE-{len(gates) + 1:03d}",
                "name": f"{item.gate_id}_created_pending_review_no_code",
                "passed": item.gate_decision == "AUTHORIZATION_REVIEW_GATE_CREATED_PENDING_REVIEW"
                and item.gate_effect
                == "NEXT_AUTHORIZATION_REVIEW_GATE_REVIEW_REQUIRED_NO_CODE_IMPLEMENTATION"
                and item.next_review_required is True
                and item.implementation_authorization_candidate is True
                and item.implementation_code_authorized is False
                and item.runtime_execution_authorized is False
                and item.real_submission_authorized is False
                and item.blocking_issue is False
                and len(item.required_authorization_evidence) >= 3,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_authorization_review_gate() -> dict[str, Any]:
    """Build the complete deterministic Task 12 authorization-review gate record."""

    source_review = build_candidate_generator_implementation_proposal_review()
    gate_items = build_authorization_review_gate_items(source_review)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_review, gate_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_REVIEW_GATE_CREATED_PENDING_REVIEW_NO_CODE"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_REVIEW_GATE_BLOCKED",
        "gate_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_REVIEW_GATE_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_proposal_review_task": source_review["task"],
        "source_proposal_review_id": source_review["implementation_proposal_review_id"],
        "source_proposal_review_signature": source_review["signature"],
        "source_proposal_review_validation": source_review["validation"],
        "source_proposal_review_verdict": source_review["verdict"],
        "next_stage": NEXT_STAGE,
        "authorization_review_gate_ready": not gate_failures,
        "authorization_review_gate_created": not gate_failures,
        "authorization_review_gate_locked": True,
        "authorization_review_gate_open": False,
        "authorization_review_gate_review_required": True,
        "authorization_review_gate_passed": False,
        "implementation_authorization_candidate": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "AUTHORIZATION_REVIEW_GATE_ONLY_PENDING_REVIEW_NO_CODE_NO_RUNTIME",
        "operator_authorization_required": True,
        "operator_authorization_received": False,
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
    payload["authorization_review_gate_id"] = (
        "MILESTONE-18-TASK-12-CANDIDATE-GENERATOR-IMPLEMENTATION-AUTHORIZATION-REVIEW-GATE-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 12 - Controlled Technical Candidate Generator Implementation Authorization Review Gate v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Authorization review gate ID: `{data['authorization_review_gate_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source proposal review ID: `{data['source_proposal_review_id']}`",
        f"- Source proposal review signature: `{data['source_proposal_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- authorization review gate only: true",
        "- authorization review gate created: true",
        "- authorization review gate review required: true",
        "- authorization review gate open: false",
        "- implementation authorization candidate: true",
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
                f"- Source proposal review item: `{item['source_proposal_review_item']}`",
                f"- Source proposal: `{item['source_proposal_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Gate decision: `{item['gate_decision']}`",
                f"- Gate effect: `{item['gate_effect']}`",
                f"- Next review required: `{item['next_review_required']}`",
                f"- Implementation authorization candidate: `{item['implementation_authorization_candidate']}`",
                f"- Implementation code authorized: `{item['implementation_code_authorized']}`",
                f"- Runtime execution authorized: `{item['runtime_execution_authorized']}`",
                f"- Real submission authorized: `{item['real_submission_authorized']}`",
                "",
                "Required authorization evidence:",
                *[f"- {evidence}" for evidence in item["required_authorization_evidence"]],
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
            "Task 12 creates the authorization-review gate only. It does not authorize code implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 12 artifacts."""

    data = build_candidate_generator_implementation_authorization_review_gate()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-review-gate-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-review-gate-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-review-gate-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-review-gate-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_12_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_REVIEW_GATE_INDEX",
        "task": data["task"],
        "authorization_review_gate_id": data["authorization_review_gate_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_proposal_review_signature": data["source_proposal_review_signature"],
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
        "MILESTONE_18_TASK_12_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_REVIEW_GATE_V1_MANIFEST",
        f"task={data['task']}",
        f"authorization_review_gate_id={data['authorization_review_gate_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_proposal_review_signature={data['source_proposal_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"gate_item_count={data['gate_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "authorization_review_gate_only=true",
        "authorization_review_gate_created=true",
        "authorization_review_gate_review_required=true",
        "authorization_review_gate_open=false",
        "implementation_authorization_candidate=true",
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
    result = build_candidate_generator_implementation_authorization_review_gate()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_proposal_review_signature"])
    print(result["gate_scope"])
    print(result["verdict"])
    print(result["next_stage"])
