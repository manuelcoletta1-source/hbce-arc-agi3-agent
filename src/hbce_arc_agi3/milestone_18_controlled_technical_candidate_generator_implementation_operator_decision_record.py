"""Milestone #18 Task 18 - Controlled Technical Candidate Generator Implementation Operator Decision Record v1.

This module creates the operator-decision record after Milestone #18 Task 17.

Important:
- This task creates the decision-record container.
- This task does not select or record a real operator decision.
- This task keeps the decision value pending.
- This task does not receive explicit operator authorization.
- This task does not grant implementation authorization.
- This task does not modify candidate generator, solver, ranker, runtime, evaluation, or submission paths.
- This task only allows the next operator-decision-record review stage.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_gate_review import (
    build_candidate_generator_implementation_operator_decision_gate_review,
)


TASK_NAME = "MILESTONE_18_TASK_18_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_RECORD_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Operator Decision Record v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_17_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_GATE_REVIEW_V1"
PREVIOUS_COMMIT = "dcc5195"
PREVIOUS_SIGNATURE = "B6562BE15E923085"

NEXT_STAGE = "MILESTONE_18_TASK_19_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_RECORD_REVIEW_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-operator-decision-record-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-record-v1.md"
)


@dataclass(frozen=True)
class CandidateGeneratorImplementationOperatorDecisionRecordItem:
    """A record item derived from Task 17 operator-decision-gate-review items."""

    record_id: str
    source_operator_decision_gate_review_item: str
    source_operator_decision_gate_item: str
    source_proposal_id: str
    source_improvement_item: str
    source_limitation_id: str
    record_area: str
    record_status: str
    record_effect: str
    operator_decision_value: str
    operator_decision_value_selected: bool
    operator_decision_received: bool
    explicit_operator_authorization_received: bool
    operator_decision_record_review_required: bool
    implementation_authorization_candidate_confirmed: bool
    implementation_code_authorized: bool
    runtime_execution_authorized: bool
    real_submission_authorized: bool
    blocking_issue: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_operator_decision_record_items(
    source_review: dict[str, Any],
) -> tuple[CandidateGeneratorImplementationOperatorDecisionRecordItem, ...]:
    """Build deterministic pending operator-decision record items from Task 17 review items."""

    record_items: list[CandidateGeneratorImplementationOperatorDecisionRecordItem] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        record_items.append(
            CandidateGeneratorImplementationOperatorDecisionRecordItem(
                record_id=f"M18-CG-IMPL-OPERATOR-DECISION-RECORD-{index}",
                source_operator_decision_gate_review_item=review_item["review_id"],
                source_operator_decision_gate_item=review_item["source_operator_decision_gate_item"],
                source_proposal_id=review_item["source_proposal_id"],
                source_improvement_item=review_item["source_improvement_item"],
                source_limitation_id=review_item["source_limitation_id"],
                record_area=review_item["review_area"],
                record_status="OPERATOR_DECISION_RECORD_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION",
                record_effect="NEXT_OPERATOR_DECISION_RECORD_REVIEW_REQUIRED_NO_DECISION_NO_CODE_IMPLEMENTATION",
                operator_decision_value="PENDING_EXPLICIT_OPERATOR_DECISION",
                operator_decision_value_selected=False,
                operator_decision_received=False,
                explicit_operator_authorization_received=False,
                operator_decision_record_review_required=True,
                implementation_authorization_candidate_confirmed=True,
                implementation_code_authorized=False,
                runtime_execution_authorized=False,
                real_submission_authorized=False,
                blocking_issue=False,
            )
        )

    return tuple(record_items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 18 boundary controls."""

    return {
        "operator_decision_record_only": True,
        "operator_decision_record_created": True,
        "operator_decision_record_review_required": True,
        "operator_decision_record_locked": True,
        "operator_decision_record_open": False,
        "operator_decision_record_passed": False,
        "operator_decision_record_allows_next_review_only": True,
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
    record_items: tuple[CandidateGeneratorImplementationOperatorDecisionRecordItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 18 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T18-GATE-001",
            "name": "previous_task_matches_task_17",
            "passed": PREVIOUS_TASK == source_review["task"],
        },
        {
            "gate_id": "M18-T18-GATE-002",
            "name": "previous_commit_matches_task_17_commit",
            "passed": PREVIOUS_COMMIT == "dcc5195",
        },
        {
            "gate_id": "M18-T18-GATE-003",
            "name": "previous_signature_matches_task_17_signature",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": PREVIOUS_SIGNATURE == source_review["signature"],
        },
        {
            "gate_id": "M18-T18-GATE-004",
            "name": "source_operator_decision_gate_review_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T18-GATE-005",
            "name": "source_operator_decision_gate_review_passed",
            "passed": source_review["operator_decision_gate_review_passed"] is True,
        },
        {
            "gate_id": "M18-T18-GATE-006",
            "name": "source_operator_decision_record_required",
            "passed": source_review["operator_decision_record_required"] is True,
        },
        {
            "gate_id": "M18-T18-GATE-007",
            "name": "source_operator_decision_record_allowed_next",
            "passed": source_review["operator_decision_record_allowed_next"] is True,
        },
        {
            "gate_id": "M18-T18-GATE-008",
            "name": "source_operator_decision_required",
            "passed": source_review["operator_decision_required"] is True,
        },
        {
            "gate_id": "M18-T18-GATE-009",
            "name": "source_operator_decision_not_received",
            "passed": source_review["operator_decision_received"] is False,
        },
        {
            "gate_id": "M18-T18-GATE-010",
            "name": "source_operator_decision_value_pending",
            "passed": source_review["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION",
        },
        {
            "gate_id": "M18-T18-GATE-011",
            "name": "source_operator_decision_value_not_selected",
            "passed": source_review["operator_decision_value_selected"] is False,
        },
        {
            "gate_id": "M18-T18-GATE-012",
            "name": "source_explicit_operator_authorization_not_received",
            "passed": source_review["explicit_operator_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T18-GATE-013",
            "name": "source_implementation_candidate_confirmed",
            "passed": source_review["implementation_authorization_candidate_confirmed"] is True,
        },
        {
            "gate_id": "M18-T18-GATE-014",
            "name": "source_does_not_authorize_code",
            "passed": source_review["implementation_code_authorized"] is False,
        },
        {
            "gate_id": "M18-T18-GATE-015",
            "name": "source_does_not_authorize_runtime",
            "passed": source_review["boundary_controls"]["runtime_execution_allowed"] is False,
        },
        {
            "gate_id": "M18-T18-GATE-016",
            "name": "source_does_not_authorize_submission",
            "passed": source_review["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T18-GATE-017",
            "name": "six_operator_decision_record_items_created",
            "passed": len(record_items) == 6,
        },
        {
            "gate_id": "M18-T18-GATE-018",
            "name": "all_record_items_created_pending_explicit_operator_decision",
            "passed": all(
                item.record_status
                == "OPERATOR_DECISION_RECORD_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION"
                for item in record_items
            ),
        },
        {
            "gate_id": "M18-T18-GATE-019",
            "name": "all_record_items_require_record_review",
            "passed": all(item.operator_decision_record_review_required for item in record_items),
        },
        {
            "gate_id": "M18-T18-GATE-020",
            "name": "all_record_items_keep_operator_decision_pending",
            "passed": all(
                item.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"
                for item in record_items
            ),
        },
        {
            "gate_id": "M18-T18-GATE-021",
            "name": "no_record_item_has_decision_selected",
            "passed": not any(item.operator_decision_value_selected for item in record_items),
        },
        {
            "gate_id": "M18-T18-GATE-022",
            "name": "no_record_item_has_decision_received",
            "passed": not any(item.operator_decision_received for item in record_items),
        },
        {
            "gate_id": "M18-T18-GATE-023",
            "name": "no_record_item_has_explicit_operator_authorization_received",
            "passed": not any(item.explicit_operator_authorization_received for item in record_items),
        },
        {
            "gate_id": "M18-T18-GATE-024",
            "name": "all_record_items_confirm_implementation_candidate",
            "passed": all(
                item.implementation_authorization_candidate_confirmed
                for item in record_items
            ),
        },
        {
            "gate_id": "M18-T18-GATE-025",
            "name": "no_record_item_authorizes_code",
            "passed": not any(item.implementation_code_authorized for item in record_items),
        },
        {
            "gate_id": "M18-T18-GATE-026",
            "name": "no_record_item_authorizes_runtime",
            "passed": not any(item.runtime_execution_authorized for item in record_items),
        },
        {
            "gate_id": "M18-T18-GATE-027",
            "name": "no_record_item_authorizes_submission",
            "passed": not any(item.real_submission_authorized for item in record_items),
        },
        {
            "gate_id": "M18-T18-GATE-028",
            "name": "no_record_item_has_blocking_issue",
            "passed": not any(item.blocking_issue for item in record_items),
        },
    ]

    for key, expected in {
        "operator_decision_record_only": True,
        "operator_decision_record_created": True,
        "operator_decision_record_review_required": True,
        "operator_decision_record_locked": True,
        "operator_decision_record_open": False,
        "operator_decision_record_passed": False,
        "operator_decision_record_allows_next_review_only": True,
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
                "gate_id": f"M18-T18-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in record_items:
        gates.append(
            {
                "gate_id": f"M18-T18-GATE-{len(gates) + 1:03d}",
                "name": f"{item.record_id}_pending_explicit_operator_decision_no_code",
                "passed": item.record_status
                == "OPERATOR_DECISION_RECORD_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION"
                and item.record_effect
                == "NEXT_OPERATOR_DECISION_RECORD_REVIEW_REQUIRED_NO_DECISION_NO_CODE_IMPLEMENTATION"
                and item.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item.operator_decision_value_selected is False
                and item.operator_decision_received is False
                and item.explicit_operator_authorization_received is False
                and item.operator_decision_record_review_required is True
                and item.implementation_authorization_candidate_confirmed is True
                and item.implementation_code_authorized is False
                and item.runtime_execution_authorized is False
                and item.real_submission_authorized is False
                and item.blocking_issue is False,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_operator_decision_record() -> dict[str, Any]:
    """Build the complete deterministic Task 18 operator-decision record."""

    source_review = build_candidate_generator_implementation_operator_decision_gate_review()
    record_items = build_operator_decision_record_items(source_review)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_review, record_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_RECORD_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION_NO_CODE"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_RECORD_BLOCKED",
        "record_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_RECORD_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_operator_decision_gate_review_task": source_review["task"],
        "source_operator_decision_gate_review_id": source_review["operator_decision_gate_review_id"],
        "source_operator_decision_gate_review_signature": source_review["signature"],
        "source_operator_decision_gate_review_validation": source_review["validation"],
        "source_operator_decision_gate_review_verdict": source_review["verdict"],
        "next_stage": NEXT_STAGE,
        "operator_decision_record_ready": not gate_failures,
        "operator_decision_record_created": not gate_failures,
        "operator_decision_record_locked": True,
        "operator_decision_record_open": False,
        "operator_decision_record_review_required": True,
        "operator_decision_record_passed": False,
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
        "implementation_authorization_scope": "OPERATOR_DECISION_RECORD_ONLY_PENDING_EXPLICIT_OPERATOR_DECISION_NO_CODE_NO_RUNTIME",
        "record_item_count": len(record_items),
        "blocking_issue_count": len(gate_failures),
        "boundary_controls": controls,
        "record_items": [asdict(item) for item in record_items],
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(gate_failures),
        "acceptance_gate_failures": gate_failures,
    }

    payload["signature"] = _signature(payload)
    payload["operator_decision_record_id"] = (
        "MILESTONE-18-TASK-18-CANDIDATE-GENERATOR-IMPLEMENTATION-OPERATOR-DECISION-RECORD-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 18 - Controlled Technical Candidate Generator Implementation Operator Decision Record v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Operator decision record ID: `{data['operator_decision_record_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source operator decision gate review ID: `{data['source_operator_decision_gate_review_id']}`",
        f"- Source operator decision gate review signature: `{data['source_operator_decision_gate_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- operator decision record only: true",
        "- operator decision record created: true",
        "- operator decision record review required: true",
        "- operator decision record open: false",
        "- operator decision required: true",
        "- operator decision received: false",
        "- operator decision value: PENDING_EXPLICIT_OPERATOR_DECISION",
        "- operator decision value selected: false",
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
        "## Record Items",
        "",
    ]

    for item in data["record_items"]:
        lines.extend(
            [
                f"### {item['record_id']} - {item['record_area']}",
                "",
                f"- Source operator decision gate review item: `{item['source_operator_decision_gate_review_item']}`",
                f"- Source operator decision gate item: `{item['source_operator_decision_gate_item']}`",
                f"- Source proposal: `{item['source_proposal_id']}`",
                f"- Source improvement item: `{item['source_improvement_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Record status: `{item['record_status']}`",
                f"- Record effect: `{item['record_effect']}`",
                f"- Operator decision value: `{item['operator_decision_value']}`",
                f"- Operator decision value selected: `{item['operator_decision_value_selected']}`",
                f"- Operator decision received: `{item['operator_decision_received']}`",
                f"- Explicit operator authorization received: `{item['explicit_operator_authorization_received']}`",
                f"- Operator decision record review required: `{item['operator_decision_record_review_required']}`",
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
            f"- Record item count: `{data['record_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            f"- Blocking issue count: `{data['blocking_issue_count']}`",
            "",
            "Task 18 creates a pending operator-decision record. It does not select or receive an operator decision and does not authorize code implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 18 artifacts."""

    data = build_candidate_generator_implementation_operator_decision_record()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-record-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-record-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-record-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-record-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_18_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_RECORD_INDEX",
        "task": data["task"],
        "operator_decision_record_id": data["operator_decision_record_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_operator_decision_gate_review_signature": data["source_operator_decision_gate_review_signature"],
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
        "MILESTONE_18_TASK_18_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_RECORD_V1_MANIFEST",
        f"task={data['task']}",
        f"operator_decision_record_id={data['operator_decision_record_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_operator_decision_gate_review_signature={data['source_operator_decision_gate_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"record_item_count={data['record_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "operator_decision_record_only=true",
        "operator_decision_record_created=true",
        "operator_decision_record_review_required=true",
        "operator_decision_required=true",
        "operator_decision_received=false",
        "operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "operator_decision_value_selected=false",
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
    result = build_candidate_generator_implementation_operator_decision_record()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_operator_decision_gate_review_signature"])
    print(result["record_scope"])
    print(result["verdict"])
    print(result["next_stage"])
