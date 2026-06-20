"""Milestone #18 Task 6 - Controlled Technical Candidate Generator Implementation Authorization Gate v1.

This module creates a deterministic, local-only authorization gate for a future
controlled candidate-generator implementation.

Important:
- This task creates the gate.
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

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_improvement_map_review import (
    build_candidate_generator_improvement_map_review,
)


TASK_NAME = "MILESTONE_18_TASK_6_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Authorization Gate v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_5_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_V1"
PREVIOUS_COMMIT = "1af8533"
PREVIOUS_SIGNATURE = "9EADD41F6C2BD263"

NEXT_STAGE = "MILESTONE_18_TASK_7_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-authorization-gate-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorAuthorizationGateCondition:
    """A gate condition required before any future implementation can be authorized."""

    condition_id: str
    source_review_item: str
    source_improvement_item: str
    source_limitation_id: str
    gate_area: str
    required_evidence: str
    gate_decision: str
    authorization_effect: str
    blocking_issue: bool
    implementation_authorized: bool
    runtime_execution_authorized: bool
    review_required_before_authorization: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_gate_conditions(
    source_review: dict[str, Any],
) -> tuple[CandidateGeneratorAuthorizationGateCondition, ...]:
    """Build deterministic gate conditions from Task 5 review items."""

    conditions: list[CandidateGeneratorAuthorizationGateCondition] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        gate_area = review_item["improvement_area"]

        if gate_area == "solver coverage":
            required_evidence = (
                "Future implementation request must specify the exact candidate families to enable "
                "and prove that solver coverage claims remain diagnostic-only."
            )
        elif gate_area == "candidate generation":
            required_evidence = (
                "Future implementation request must define deterministic candidate ordering, "
                "candidate identifiers, confidence hints, and rejection paths."
            )
        elif gate_area == "ranker evidence":
            required_evidence = (
                "Future implementation request must prove ranker-neutral metadata emission "
                "without modifying ranker weights or runtime ranking behavior."
            )
        elif gate_area == "local diagnostics":
            required_evidence = (
                "Future implementation request must include local public-safe fixtures and "
                "regression guards before any candidate generator patch is allowed."
            )
        elif gate_area == "submission discipline":
            required_evidence = (
                "Future implementation request must preserve separation between candidate artifacts "
                "and submission artifacts, with real_submission_allowed=false."
            )
        elif gate_area == "authorization boundary":
            required_evidence = (
                "Future implementation request must include explicit operator authorization and "
                "must keep fail-closed active until review passes."
            )
        else:
            required_evidence = (
                "Future implementation request must provide deterministic evidence for this area "
                "before any authorization can be considered."
            )

        conditions.append(
            CandidateGeneratorAuthorizationGateCondition(
                condition_id=f"M18-CG-AUTH-GATE-{index}",
                source_review_item=review_item["review_id"],
                source_improvement_item=review_item["source_item_id"],
                source_limitation_id=review_item["source_limitation_id"],
                gate_area=gate_area,
                required_evidence=required_evidence,
                gate_decision="GATE_CREATED_PENDING_REVIEW",
                authorization_effect="NO_IMPLEMENTATION_AUTHORIZATION_GRANTED",
                blocking_issue=False,
                implementation_authorized=False,
                runtime_execution_authorized=False,
                review_required_before_authorization=True,
            )
        )

    return tuple(conditions)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 6 boundary controls."""

    return {
        "authorization_gate_only": True,
        "authorization_gate_created": True,
        "authorization_gate_review_required": True,
        "authorization_gate_open": False,
        "authorization_gate_locked": True,
        "authorization_gate_passed": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
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
    gate_conditions: tuple[CandidateGeneratorAuthorizationGateCondition, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 6 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T6-GATE-001",
            "name": "previous_task_matches_task_5",
            "passed": PREVIOUS_TASK == source_review["task"],
        },
        {
            "gate_id": "M18-T6-GATE-002",
            "name": "previous_commit_matches_task_5_commit",
            "passed": PREVIOUS_COMMIT == "1af8533",
        },
        {
            "gate_id": "M18-T6-GATE-003",
            "name": "previous_signature_matches_task_5_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": PREVIOUS_SIGNATURE == source_review["signature"],
        },
        {
            "gate_id": "M18-T6-GATE-004",
            "name": "source_review_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T6-GATE-005",
            "name": "source_review_passed",
            "passed": source_review["review_passed"] is True,
        },
        {
            "gate_id": "M18-T6-GATE-006",
            "name": "source_review_no_acceptance_failures",
            "passed": source_review["acceptance_gate_failure_count"] == 0,
        },
        {
            "gate_id": "M18-T6-GATE-007",
            "name": "six_authorization_gate_conditions_created",
            "passed": len(gate_conditions) == 6,
        },
        {
            "gate_id": "M18-T6-GATE-008",
            "name": "all_conditions_require_review_before_authorization",
            "passed": all(condition.review_required_before_authorization for condition in gate_conditions),
        },
        {
            "gate_id": "M18-T6-GATE-009",
            "name": "no_condition_authorizes_implementation",
            "passed": not any(condition.implementation_authorized for condition in gate_conditions),
        },
        {
            "gate_id": "M18-T6-GATE-010",
            "name": "no_condition_authorizes_runtime_execution",
            "passed": not any(condition.runtime_execution_authorized for condition in gate_conditions),
        },
    ]

    for key, expected in {
        "authorization_gate_only": True,
        "authorization_gate_created": True,
        "authorization_gate_review_required": True,
        "authorization_gate_open": False,
        "authorization_gate_locked": True,
        "authorization_gate_passed": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
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
                "gate_id": f"M18-T6-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for condition in gate_conditions:
        gates.append(
            {
                "gate_id": f"M18-T6-GATE-{len(gates) + 1:03d}",
                "name": f"{condition.condition_id}_created_pending_review",
                "passed": condition.gate_decision == "GATE_CREATED_PENDING_REVIEW"
                and condition.authorization_effect == "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED"
                and condition.implementation_authorized is False
                and condition.runtime_execution_authorized is False
                and condition.blocking_issue is False,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_authorization_gate() -> dict[str, Any]:
    """Build the complete deterministic Task 6 authorization gate record."""

    source_review = build_candidate_generator_improvement_map_review()
    gate_conditions = build_gate_conditions(source_review)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_review, gate_conditions, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_CREATED_PENDING_REVIEW_NO_IMPLEMENTATION"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_BLOCKED",
        "gate_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_review_task": source_review["task"],
        "source_review_id": source_review["review_id"],
        "source_review_signature": source_review["signature"],
        "source_review_validation": source_review["validation"],
        "source_review_verdict": source_review["verdict"],
        "next_stage": NEXT_STAGE,
        "authorization_gate_ready": not gate_failures,
        "authorization_gate_created": not gate_failures,
        "authorization_gate_locked": True,
        "authorization_gate_open": False,
        "authorization_gate_review_required": True,
        "authorization_gate_passed": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "NOT_GRANTED_PENDING_GATE_REVIEW",
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "gate_condition_count": len(gate_conditions),
        "blocking_issue_count": len(gate_failures),
        "boundary_controls": controls,
        "gate_conditions": [asdict(condition) for condition in gate_conditions],
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(gate_failures),
        "acceptance_gate_failures": gate_failures,
    }

    payload["signature"] = _signature(payload)
    payload["authorization_gate_id"] = (
        "MILESTONE-18-TASK-6-CANDIDATE-GENERATOR-IMPLEMENTATION-AUTHORIZATION-GATE-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 6 — Controlled Technical Candidate Generator Implementation Authorization Gate v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Authorization gate ID: `{data['authorization_gate_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source review ID: `{data['source_review_id']}`",
        f"- Source review signature: `{data['source_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- authorization gate only: true",
        "- authorization gate created: true",
        "- authorization gate open: false",
        "- authorization gate review required: true",
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
        "## Gate Conditions",
        "",
    ]

    for condition in data["gate_conditions"]:
        lines.extend(
            [
                f"### {condition['condition_id']} — {condition['gate_area']}",
                "",
                f"- Source review item: `{condition['source_review_item']}`",
                f"- Source improvement item: `{condition['source_improvement_item']}`",
                f"- Source limitation: `{condition['source_limitation_id']}`",
                f"- Gate decision: `{condition['gate_decision']}`",
                f"- Authorization effect: `{condition['authorization_effect']}`",
                f"- Blocking issue: `{condition['blocking_issue']}`",
                f"- Implementation authorized: `{condition['implementation_authorized']}`",
                f"- Runtime execution authorized: `{condition['runtime_execution_authorized']}`",
                f"- Required evidence: {condition['required_evidence']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Acceptance",
            "",
            f"- Gate condition count: `{data['gate_condition_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            f"- Blocking issue count: `{data['blocking_issue_count']}`",
            "",
            "Task 6 creates an authorization gate only. It does not authorize implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 6 artifacts."""

    data = build_candidate_generator_implementation_authorization_gate()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-authorization-gate-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_6_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_INDEX",
        "task": data["task"],
        "authorization_gate_id": data["authorization_gate_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_review_signature": data["source_review_signature"],
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
        "MILESTONE_18_TASK_6_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_V1_MANIFEST",
        f"task={data['task']}",
        f"authorization_gate_id={data['authorization_gate_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_review_signature={data['source_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"gate_condition_count={data['gate_condition_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "authorization_gate_only=true",
        "authorization_gate_created=true",
        "authorization_gate_open=false",
        "authorization_gate_review_required=true",
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
    result = build_candidate_generator_implementation_authorization_gate()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_review_signature"])
    print(result["gate_scope"])
    print(result["verdict"])
    print(result["next_stage"])
