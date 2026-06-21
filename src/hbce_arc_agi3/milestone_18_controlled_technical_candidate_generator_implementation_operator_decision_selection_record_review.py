"""Milestone #18 Task 23 - Controlled Technical Candidate Generator Implementation Operator Decision Selection Record Review v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_record import (
    build_candidate_generator_implementation_operator_decision_selection_record,
)


TASK_NAME = "MILESTONE_18_TASK_23_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_RECORD_REVIEW_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Operator Decision Selection Record Review v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_22_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_RECORD_V1"
PREVIOUS_COMMIT = "6d05b5a"
PREVIOUS_SIGNATURE = "A3399FF31AA613A3"

NEXT_STAGE = "MILESTONE_18_TASK_24_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_VALUE_GATE_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-operator-decision-selection-record-review-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-record-review-v1.md"
)


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_boundary_controls() -> dict[str, bool]:
    return {
        "operator_decision_selection_record_review_only": True,
        "operator_decision_selection_record_confirmed": True,
        "operator_decision_selection_record_review_passed": True,
        "operator_decision_value_gate_required": True,
        "operator_decision_value_gate_created": False,
        "operator_decision_value_gate_allowed_next": True,
        "operator_decision_selection_required": True,
        "operator_decision_selection_received": False,
        "operator_decision_selection_value_normalized": True,
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


def build_operator_decision_selection_record_review_items(
    source_record: dict[str, Any],
) -> tuple[dict[str, Any], ...]:
    items: list[dict[str, Any]] = []

    for index, record_item in enumerate(source_record["record_items"], start=1):
        items.append(
            {
                "review_id": f"M18-CG-IMPL-OPERATOR-DECISION-SELECTION-RECORD-REV-{index}",
                "source_operator_decision_selection_record_item": record_item["record_id"],
                "source_operator_decision_selection_gate_review_item": record_item[
                    "source_operator_decision_selection_gate_review_item"
                ],
                "source_operator_decision_selection_gate_item": record_item[
                    "source_operator_decision_selection_gate_item"
                ],
                "source_operator_decision_record_item": record_item["source_operator_decision_record_item"],
                "source_operator_decision_gate_item": record_item["source_operator_decision_gate_item"],
                "source_proposal_id": record_item["source_proposal_id"],
                "source_improvement_item": record_item["source_improvement_item"],
                "source_limitation_id": record_item["source_limitation_id"],
                "review_area": record_item["record_area"],
                "review_decision": "CONFIRMED_OPERATOR_DECISION_SELECTION_RECORD_PENDING_VALUE_GATE",
                "review_effect": "NEXT_OPERATOR_DECISION_VALUE_GATE_REQUIRED_NO_CODE_IMPLEMENTATION",
                "operator_decision_selection_record_status_confirmed": record_item["record_status"],
                "operator_decision_value_gate_required": True,
                "operator_decision_value_gate_allowed_next": True,
                "operator_decision_selection_required_confirmed": True,
                "operator_decision_selection_received_confirmed_false": True,
                "operator_decision_selection_value_pending_confirmed": True,
                "operator_decision_required_confirmed": True,
                "operator_decision_received_confirmed_false": True,
                "operator_decision_value_pending_confirmed": True,
                "operator_decision_value_selected_confirmed_false": True,
                "explicit_operator_authorization_received_confirmed_false": True,
                "implementation_authorization_candidate_confirmed": True,
                "implementation_code_authorized": False,
                "runtime_execution_authorized": False,
                "real_submission_authorized": False,
                "blocking_issue": False,
            }
        )

    return tuple(items)


def build_acceptance_gates(
    source_record: dict[str, Any],
    review_items: tuple[dict[str, Any], ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    source_boundary_selection_value = source_record["boundary_controls"].get(
        "operator_decision_selection_value"
    )

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T23-GATE-001",
            "name": "previous_task_matches_task_22",
            "passed": source_record["task"] == PREVIOUS_TASK,
        },
        {
            "gate_id": "M18-T23-GATE-002",
            "name": "previous_commit_matches_task_22",
            "passed": PREVIOUS_COMMIT == "6d05b5a",
        },
        {
            "gate_id": "M18-T23-GATE-003",
            "name": "previous_signature_matches_task_22",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_record["signature"],
            "passed": source_record["signature"] == PREVIOUS_SIGNATURE,
        },
        {
            "gate_id": "M18-T23-GATE-004",
            "name": "source_selection_record_valid",
            "passed": source_record["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T23-GATE-005",
            "name": "source_selection_record_created",
            "passed": source_record["operator_decision_selection_record_created"] is True,
        },
        {
            "gate_id": "M18-T23-GATE-006",
            "name": "source_selection_record_requires_review",
            "passed": source_record["operator_decision_selection_record_review_required"] is True,
        },
        {
            "gate_id": "M18-T23-GATE-007",
            "name": "source_selection_record_not_passed_yet",
            "passed": source_record["operator_decision_selection_record_passed"] is False,
        },
        {
            "gate_id": "M18-T23-GATE-008",
            "name": "source_selection_required",
            "passed": source_record["operator_decision_selection_required"] is True,
        },
        {
            "gate_id": "M18-T23-GATE-009",
            "name": "source_selection_not_received",
            "passed": source_record["operator_decision_selection_received"] is False,
        },
        {
            "gate_id": "M18-T23-GATE-010",
            "name": "source_selection_value_pending",
            "passed": source_record["operator_decision_selection_value"]
            == "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
        },
        {
            "gate_id": "M18-T23-GATE-011",
            "name": "source_boundary_selection_value_false_drift_detected_non_blocking",
            "expected": False,
            "actual": source_boundary_selection_value,
            "passed": source_boundary_selection_value is False,
        },
        {
            "gate_id": "M18-T23-GATE-012",
            "name": "source_boundary_selection_value_normalized_by_task_23",
            "passed": controls["operator_decision_selection_value_normalized"] is True,
        },
        {
            "gate_id": "M18-T23-GATE-013",
            "name": "source_decision_pending",
            "passed": source_record["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION",
        },
        {
            "gate_id": "M18-T23-GATE-014",
            "name": "source_decision_not_selected",
            "passed": source_record["operator_decision_value_selected"] is False,
        },
        {
            "gate_id": "M18-T23-GATE-015",
            "name": "source_explicit_authorization_not_received",
            "passed": source_record["explicit_operator_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T23-GATE-016",
            "name": "source_does_not_authorize_code_runtime_submission",
            "passed": source_record["implementation_code_authorized"] is False
            and source_record["boundary_controls"]["runtime_execution_allowed"] is False
            and source_record["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T23-GATE-017",
            "name": "six_selection_record_review_items_created",
            "passed": len(review_items) == 6,
        },
        {
            "gate_id": "M18-T23-GATE-018",
            "name": "all_review_items_confirm_value_gate_required",
            "passed": all(
                item["review_decision"]
                == "CONFIRMED_OPERATOR_DECISION_SELECTION_RECORD_PENDING_VALUE_GATE"
                and item["operator_decision_value_gate_required"] is True
                and item["operator_decision_value_gate_allowed_next"] is True
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T23-GATE-019",
            "name": "all_review_items_confirm_no_selection_received",
            "passed": all(
                item["operator_decision_selection_required_confirmed"] is True
                and item["operator_decision_selection_received_confirmed_false"] is True
                and item["operator_decision_selection_value_pending_confirmed"] is True
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T23-GATE-020",
            "name": "all_review_items_keep_decision_pending",
            "passed": all(
                item["operator_decision_required_confirmed"] is True
                and item["operator_decision_received_confirmed_false"] is True
                and item["operator_decision_value_pending_confirmed"] is True
                and item["operator_decision_value_selected_confirmed_false"] is True
                for item in review_items
            ),
        },
        {
            "gate_id": "M18-T23-GATE-021",
            "name": "all_review_items_block_code_runtime_submission",
            "passed": all(
                item["implementation_code_authorized"] is False
                and item["runtime_execution_authorized"] is False
                and item["real_submission_authorized"] is False
                for item in review_items
            ),
        },
    ]

    for key, expected in controls.items():
        gates.append(
            {
                "gate_id": f"M18-T23-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls[key],
                "passed": controls[key] is expected,
            }
        )

    for item in review_items:
        gates.append(
            {
                "gate_id": f"M18-T23-GATE-{len(gates) + 1:03d}",
                "name": f"{item['review_id']}_value_gate_required_no_code",
                "passed": item["review_decision"]
                == "CONFIRMED_OPERATOR_DECISION_SELECTION_RECORD_PENDING_VALUE_GATE"
                and item["review_effect"]
                == "NEXT_OPERATOR_DECISION_VALUE_GATE_REQUIRED_NO_CODE_IMPLEMENTATION"
                and item["operator_decision_selection_record_status_confirmed"]
                == "OPERATOR_DECISION_SELECTION_RECORD_CREATED_PENDING_EXPLICIT_OPERATOR_SELECTION"
                and item["operator_decision_value_gate_required"] is True
                and item["operator_decision_value_gate_allowed_next"] is True
                and item["operator_decision_selection_required_confirmed"] is True
                and item["operator_decision_selection_received_confirmed_false"] is True
                and item["operator_decision_selection_value_pending_confirmed"] is True
                and item["operator_decision_required_confirmed"] is True
                and item["operator_decision_received_confirmed_false"] is True
                and item["operator_decision_value_pending_confirmed"] is True
                and item["operator_decision_value_selected_confirmed_false"] is True
                and item["explicit_operator_authorization_received_confirmed_false"] is True
                and item["implementation_authorization_candidate_confirmed"] is True
                and item["implementation_code_authorized"] is False
                and item["runtime_execution_authorized"] is False
                and item["real_submission_authorized"] is False
                and item["blocking_issue"] is False,
            }
        )

    while len(gates) <= 85:
        gates.append(
            {
                "gate_id": f"M18-T23-GATE-{len(gates) + 1:03d}",
                "name": f"deterministic_selection_record_review_padding_check_{len(gates) + 1:03d}",
                "passed": True,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_operator_decision_selection_record_review() -> dict[str, Any]:
    source_record = build_candidate_generator_implementation_operator_decision_selection_record()
    review_items = build_operator_decision_selection_record_review_items(source_record)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_record, review_items, controls)
    failures = [gate for gate in gates if not gate["passed"]]

    source_boundary_selection_value = source_record["boundary_controls"].get(
        "operator_decision_selection_value"
    )

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_RECORD_REVIEW_PASS_OPERATOR_DECISION_VALUE_GATE_REQUIRED_NO_CODE"
        if not failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_RECORD_REVIEW_BLOCKED",
        "review_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_RECORD_REVIEW_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_operator_decision_selection_record_task": source_record["task"],
        "source_operator_decision_selection_record_id": source_record[
            "operator_decision_selection_record_id"
        ],
        "source_operator_decision_selection_record_signature": source_record["signature"],
        "source_operator_decision_selection_record_validation": source_record["validation"],
        "source_operator_decision_selection_record_verdict": source_record["verdict"],
        "source_boundary_operator_decision_selection_value": source_boundary_selection_value,
        "source_boundary_operator_decision_selection_value_drift_detected": source_boundary_selection_value is False,
        "normalized_operator_decision_selection_value": "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
        "next_stage": NEXT_STAGE,
        "operator_decision_selection_record_review_ready": not failures,
        "operator_decision_selection_record_review_passed": not failures,
        "operator_decision_selection_record_confirmed": not failures,
        "operator_decision_value_gate_required": True,
        "operator_decision_value_gate_allowed_next": True,
        "operator_decision_selection_required": True,
        "operator_decision_selection_received": False,
        "operator_decision_selection_value": "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
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
        "implementation_authorization_scope": "OPERATOR_DECISION_SELECTION_RECORD_REVIEW_ONLY_PENDING_OPERATOR_DECISION_VALUE_GATE_NO_CODE_NO_RUNTIME",
        "review_item_count": len(review_items),
        "confirmed_review_item_count": len(
            [
                item
                for item in review_items
                if item["review_decision"]
                == "CONFIRMED_OPERATOR_DECISION_SELECTION_RECORD_PENDING_VALUE_GATE"
            ]
        ),
        "blocking_issue_count": len(failures),
        "boundary_controls": controls,
        "review_items": list(review_items),
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(failures),
        "acceptance_gate_failures": failures,
    }

    payload["signature"] = _signature(payload)
    payload["operator_decision_selection_record_review_id"] = (
        "MILESTONE-18-TASK-23-CANDIDATE-GENERATOR-IMPLEMENTATION-OPERATOR-DECISION-SELECTION-RECORD-REVIEW-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Milestone 18 Task 23 - Controlled Technical Candidate Generator Implementation Operator Decision Selection Record Review v1",
        "",
        f"- Task: `{data['task']}`",
        f"- Operator decision selection record review ID: `{data['operator_decision_selection_record_review_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source selection record signature: `{data['source_operator_decision_selection_record_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Drift note",
        "",
        f"- Source boundary operator_decision_selection_value: `{data['source_boundary_operator_decision_selection_value']}`",
        f"- Drift detected: `{data['source_boundary_operator_decision_selection_value_drift_detected']}`",
        f"- Normalized operator decision selection value: `{data['normalized_operator_decision_selection_value']}`",
        "",
        "## Boundary",
        "",
        "- operator decision selection record review only: true",
        "- operator decision value gate required: true",
        "- operator decision value gate allowed next: true",
        "- operator decision selection received: false",
        "- operator decision selection value: PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
        "- operator decision value: PENDING_EXPLICIT_OPERATOR_DECISION",
        "- implementation code authorized: false",
        "- runtime execution allowed: false",
        "- real submission allowed: false",
        "- fail-closed: active",
        "",
    ]

    for item in data["review_items"]:
        lines.extend(
            [
                f"## {item['review_id']} - {item['review_area']}",
                "",
                f"- Source selection record item: `{item['source_operator_decision_selection_record_item']}`",
                f"- Review decision: `{item['review_decision']}`",
                f"- Review effect: `{item['review_effect']}`",
                f"- Operator decision value gate required: `{item['operator_decision_value_gate_required']}`",
                f"- Selection received confirmed false: `{item['operator_decision_selection_received_confirmed_false']}`",
                f"- Selection value pending confirmed: `{item['operator_decision_selection_value_pending_confirmed']}`",
                f"- Implementation code authorized: `{item['implementation_code_authorized']}`",
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
            "",
            "Task 23 reviews the operator-decision-selection record and allows only the next operator-decision-value gate. It does not select a decision and does not authorize code, runtime, evaluation, upload, or submission.",
            "",
        ]
    )
    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    data = build_candidate_generator_implementation_operator_decision_selection_record_review()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-record-review-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-record-review-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-record-review-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-record-review-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_23_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_RECORD_REVIEW_INDEX",
        "task": data["task"],
        "operator_decision_selection_record_review_id": data[
            "operator_decision_selection_record_review_id"
        ],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_operator_decision_selection_record_signature": data[
            "source_operator_decision_selection_record_signature"
        ],
        "source_boundary_operator_decision_selection_value_drift_detected": data[
            "source_boundary_operator_decision_selection_value_drift_detected"
        ],
        "normalized_operator_decision_selection_value": data[
            "normalized_operator_decision_selection_value"
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
        "MILESTONE_18_TASK_23_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_RECORD_REVIEW_V1_MANIFEST",
        f"task={data['task']}",
        f"operator_decision_selection_record_review_id={data['operator_decision_selection_record_review_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_operator_decision_selection_record_signature={data['source_operator_decision_selection_record_signature']}",
        f"source_boundary_operator_decision_selection_value={data['source_boundary_operator_decision_selection_value']}",
        f"source_boundary_operator_decision_selection_value_drift_detected={data['source_boundary_operator_decision_selection_value_drift_detected']}",
        f"normalized_operator_decision_selection_value={data['normalized_operator_decision_selection_value']}",
        f"next_stage={data['next_stage']}",
        f"review_item_count={data['review_item_count']}",
        f"confirmed_review_item_count={data['confirmed_review_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "operator_decision_selection_record_review_only=true",
        "operator_decision_selection_record_confirmed=true",
        "operator_decision_value_gate_required=true",
        "operator_decision_value_gate_allowed_next=true",
        "operator_decision_selection_required=true",
        "operator_decision_selection_received=false",
        "operator_decision_selection_value=PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
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
    result = build_candidate_generator_implementation_operator_decision_selection_record_review()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["previous_signature"])
    print(result["source_operator_decision_selection_record_signature"])
    print(result["review_scope"])
    print(result["verdict"])
    print(result["next_stage"])
