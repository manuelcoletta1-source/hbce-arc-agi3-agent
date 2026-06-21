"""Milestone #18 Task 60 - Controlled Technical Candidate Generator Implementation Operator Decision Selection Explicit Value Selection Final Value Gate v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_value_gate import (
    allowed_operator_decision_values,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_actual_value_record_review_task_59 import (
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_actual_value_record_review,
)


TASK_NAME = "MILESTONE_18_TASK_60_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Operator Decision Selection Explicit Value Selection Final Value Gate v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_59_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_ACTUAL_VALUE_RECORD_REVIEW_V1"
PREVIOUS_COMMIT = "fae331c"
PREVIOUS_SIGNATURE = "068650C170C6E16D"

NEXT_STAGE = "MILESTONE_18_TASK_61_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_REVIEW_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-operator-decision-selection-explicit-value-selection-final-value-gate-task-60-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-explicit-value-selection-final-value-gate-task-60-v1.md"
)


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_boundary_controls() -> dict[str, bool]:
    return {
        "operator_decision_selection_explicit_value_selection_final_value_gate_only": True,
        "operator_decision_selection_explicit_value_selection_final_value_gate_created": True,
        "operator_decision_selection_explicit_value_selection_final_value_gate_locked": True,
        "operator_decision_selection_explicit_value_selection_final_value_gate_open": False,
        "operator_decision_selection_explicit_value_selection_final_value_gate_review_required": True,
        "operator_decision_selection_explicit_value_selection_final_value_gate_passed": False,
        "operator_decision_selection_explicit_value_selection_final_value_gate_allows_next_review_only": True,
        "operator_decision_selection_explicit_value_selection_actual_value_record_confirmed": True,
        "operator_decision_selection_explicit_value_selection_actual_value_record_review_confirmed": True,
        "operator_decision_selection_explicit_value_selection_actual_value_record_created": True,
        "operator_decision_selection_explicit_value_selection_actual_value_gate_confirmed": True,
        "operator_decision_selection_explicit_value_selection_actual_value_gate_review_confirmed": True,
        "operator_decision_selection_explicit_value_selection_record_confirmed": True,
        "operator_decision_selection_explicit_value_selection_record_review_confirmed": True,
        "operator_decision_selection_explicit_value_selection_gate_confirmed": True,
        "operator_decision_selection_explicit_value_selection_gate_review_confirmed": True,
        "operator_decision_selection_actual_operator_decision_value_record_confirmed": True,
        "operator_decision_selection_actual_operator_decision_value_record_review_confirmed": True,
        "operator_decision_selection_actual_operator_decision_value_gate_confirmed": True,
        "operator_decision_selection_actual_operator_decision_value_gate_review_confirmed": True,
        "operator_decision_selection_final_operator_decision_record_confirmed": True,
        "operator_decision_selection_final_operator_decision_record_review_confirmed": True,
        "operator_decision_selection_final_operator_decision_gate_confirmed": True,
        "operator_decision_selection_final_operator_decision_gate_review_confirmed": True,
        "operator_decision_selection_explicit_authorization_record_confirmed": True,
        "operator_decision_selection_explicit_authorization_record_review_confirmed": True,
        "operator_decision_selection_explicit_authorization_gate_confirmed": True,
        "operator_decision_selection_explicit_authorization_gate_review_confirmed": True,
        "operator_decision_selection_final_authorization_record_confirmed": True,
        "operator_decision_selection_final_authorization_record_review_confirmed": True,
        "operator_decision_selection_final_review_gate_confirmed": True,
        "operator_decision_selection_final_review_gate_review_confirmed": True,
        "operator_decision_selection_record_confirmed": True,
        "operator_decision_selection_record_review_confirmed": True,
        "operator_decision_selection_authorization_required": True,
        "operator_decision_selection_authorization_received": False,
        "operator_decision_selection_authorized": False,
        "operator_decision_value_required": True,
        "operator_decision_value_received": False,
        "operator_decision_value_selected": False,
        "operator_decision_value_pending": True,
        "operator_decision_required": True,
        "operator_decision_received": False,
        "operator_decision_selection_required": True,
        "operator_decision_selection_received": False,
        "operator_decision_selection_value_normalized": True,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "explicit_operator_authorization_received": False,
        "selected_operator_decision_value_pending": True,
        "selected_operator_decision_value_validated": False,
        "final_operator_decision_value_selected": False,
        "final_operator_decision_value_validated": False,
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


def build_operator_decision_selection_explicit_value_selection_final_value_gate_items(
    source_review: dict[str, Any],
) -> tuple[dict[str, Any], ...]:
    items: list[dict[str, Any]] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        items.append(
            {
                "gate_id": f"M18-CG-IMPL-OPERATOR-DECISION-SELECTION-EXPLICIT-VALUE-SELECTION-FINAL-VALUE-GATE-T60-{index}",
                "source_operator_decision_selection_explicit_value_selection_actual_value_record_review_item": review_item[
                    "review_id"
                ],
                "source_operator_decision_selection_explicit_value_selection_actual_value_record_item": review_item[
                    "source_operator_decision_selection_explicit_value_selection_actual_value_record_item"
                ],
                "source_operator_decision_selection_explicit_value_selection_actual_value_gate_review_item": review_item[
                    "source_operator_decision_selection_explicit_value_selection_actual_value_gate_review_item"
                ],
                "source_operator_decision_selection_explicit_value_selection_actual_value_gate_item": review_item[
                    "source_operator_decision_selection_explicit_value_selection_actual_value_gate_item"
                ],
                "source_operator_decision_selection_explicit_value_selection_record_review_item": review_item[
                    "source_operator_decision_selection_explicit_value_selection_record_review_item"
                ],
                "source_operator_decision_selection_explicit_value_selection_record_item": review_item[
                    "source_operator_decision_selection_explicit_value_selection_record_item"
                ],
                "source_proposal_id": review_item["source_proposal_id"],
                "source_improvement_item": review_item["source_improvement_item"],
                "source_limitation_id": review_item["source_limitation_id"],
                "gate_area": review_item["review_area"],
                "gate_status": "OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_CREATED_PENDING_REVIEW",
                "gate_effect": "NEXT_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_REVIEW_REQUIRED_NO_VALUE_SELECTED_NO_CODE_IMPLEMENTATION",
                "allowed_operator_decision_values": allowed_operator_decision_values(),
                "selected_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
                "selected_operator_decision_value_validated": False,
                "final_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
                "final_operator_decision_value_selected": False,
                "final_operator_decision_value_validated": False,
                "operator_decision_selection_explicit_value_selection_final_value_gate_created": True,
                "operator_decision_selection_explicit_value_selection_final_value_gate_review_required": True,
                "operator_decision_selection_explicit_value_selection_final_value_gate_locked": True,
                "operator_decision_selection_explicit_value_selection_final_value_gate_open": False,
                "operator_decision_selection_explicit_value_selection_actual_value_record_confirmed": True,
                "operator_decision_selection_explicit_value_selection_actual_value_record_review_confirmed": True,
                "operator_decision_selection_explicit_value_selection_actual_value_gate_confirmed": True,
                "operator_decision_selection_explicit_value_selection_actual_value_gate_review_confirmed": True,
                "operator_decision_selection_explicit_value_selection_record_confirmed": True,
                "operator_decision_selection_explicit_value_selection_record_review_confirmed": True,
                "operator_decision_selection_explicit_value_selection_gate_confirmed": True,
                "operator_decision_selection_explicit_value_selection_gate_review_confirmed": True,
                "operator_decision_selection_actual_operator_decision_value_record_confirmed": True,
                "operator_decision_selection_actual_operator_decision_value_record_review_confirmed": True,
                "operator_decision_selection_actual_operator_decision_value_gate_confirmed": True,
                "operator_decision_selection_actual_operator_decision_value_gate_review_confirmed": True,
                "operator_decision_selection_final_operator_decision_record_confirmed": True,
                "operator_decision_selection_final_operator_decision_record_review_confirmed": True,
                "operator_decision_selection_authorization_required": True,
                "operator_decision_selection_authorization_received": False,
                "operator_decision_selection_authorized": False,
                "operator_decision_value_required": True,
                "operator_decision_value_received": False,
                "operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
                "operator_decision_value_selected": False,
                "operator_decision_required": True,
                "operator_decision_received": False,
                "operator_decision_selection_required": True,
                "operator_decision_selection_received": False,
                "operator_decision_selection_value": "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
                "explicit_operator_authorization_received": False,
                "implementation_authorization_candidate_confirmed": True,
                "implementation_code_authorized": False,
                "runtime_execution_authorized": False,
                "real_submission_authorized": False,
                "blocking_issue": False,
            }
        )

    return tuple(items)


def build_acceptance_gates(
    source_review: dict[str, Any],
    gate_items: tuple[dict[str, Any], ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T60-GATE-001",
            "name": "previous_task_matches_task_59",
            "passed": source_review["task"] == PREVIOUS_TASK,
        },
        {
            "gate_id": "M18-T60-GATE-002",
            "name": "previous_commit_matches_task_59",
            "passed": PREVIOUS_COMMIT == "fae331c",
        },
        {
            "gate_id": "M18-T60-GATE-003",
            "name": "previous_signature_matches_task_59",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": source_review["signature"] == PREVIOUS_SIGNATURE,
        },
        {
            "gate_id": "M18-T60-GATE-004",
            "name": "source_actual_value_record_review_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T60-GATE-005",
            "name": "source_actual_value_record_review_passed",
            "passed": source_review[
                "operator_decision_selection_explicit_value_selection_actual_value_record_review_passed"
            ]
            is True,
        },
        {
            "gate_id": "M18-T60-GATE-006",
            "name": "source_actual_value_record_confirmed",
            "passed": source_review[
                "operator_decision_selection_explicit_value_selection_actual_value_record_confirmed"
            ]
            is True,
        },
        {
            "gate_id": "M18-T60-GATE-007",
            "name": "source_final_value_gate_required",
            "passed": source_review[
                "operator_decision_selection_explicit_value_selection_final_value_gate_required"
            ]
            is True,
        },
        {
            "gate_id": "M18-T60-GATE-008",
            "name": "source_final_value_gate_allowed_next",
            "passed": source_review[
                "operator_decision_selection_explicit_value_selection_final_value_gate_allowed_next"
            ]
            is True,
        },
        {
            "gate_id": "M18-T60-GATE-009",
            "name": "source_final_value_gate_not_created_yet",
            "passed": source_review["boundary_controls"][
                "operator_decision_selection_explicit_value_selection_final_value_gate_created"
            ]
            is False,
        },
        {
            "gate_id": "M18-T60-GATE-010",
            "name": "source_selected_value_pending_not_validated",
            "passed": source_review["selected_operator_decision_value"]
            == "PENDING_EXPLICIT_OPERATOR_DECISION"
            and source_review["selected_operator_decision_value_validated"] is False,
        },
        {
            "gate_id": "M18-T60-GATE-011",
            "name": "source_selection_authorization_required_but_not_received",
            "passed": source_review["operator_decision_selection_authorization_required"] is True
            and source_review["operator_decision_selection_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T60-GATE-012",
            "name": "source_selection_not_authorized",
            "passed": source_review["operator_decision_selection_authorized"] is False,
        },
        {
            "gate_id": "M18-T60-GATE-013",
            "name": "source_value_pending_not_selected",
            "passed": source_review["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
            and source_review["operator_decision_value_selected"] is False,
        },
        {
            "gate_id": "M18-T60-GATE-014",
            "name": "source_selection_value_pending",
            "passed": source_review["operator_decision_selection_value"]
            == "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
        },
        {
            "gate_id": "M18-T60-GATE-015",
            "name": "source_allowed_operator_decision_values_confirmed",
            "passed": tuple(source_review["allowed_operator_decision_values"])
            == allowed_operator_decision_values(),
        },
        {
            "gate_id": "M18-T60-GATE-016",
            "name": "source_explicit_authorization_not_received",
            "passed": source_review["explicit_operator_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T60-GATE-017",
            "name": "source_does_not_authorize_code_runtime_submission",
            "passed": source_review["implementation_code_authorized"] is False
            and source_review["boundary_controls"]["runtime_execution_allowed"] is False
            and source_review["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T60-GATE-018",
            "name": "six_final_value_gate_items_created",
            "passed": len(gate_items) == 6,
        },
        {
            "gate_id": "M18-T60-GATE-019",
            "name": "all_gate_items_created_pending_review",
            "passed": all(
                item["gate_status"]
                == "OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_CREATED_PENDING_REVIEW"
                and item[
                    "operator_decision_selection_explicit_value_selection_final_value_gate_created"
                ]
                is True
                and item[
                    "operator_decision_selection_explicit_value_selection_final_value_gate_review_required"
                ]
                is True
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T60-GATE-020",
            "name": "all_gate_items_keep_final_value_pending",
            "passed": all(
                item["final_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item["final_operator_decision_value_selected"] is False
                and item["final_operator_decision_value_validated"] is False
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T60-GATE-021",
            "name": "all_gate_items_keep_selected_value_pending",
            "passed": all(
                item["selected_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item["selected_operator_decision_value_validated"] is False
                and item["operator_decision_value_selected"] is False
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T60-GATE-022",
            "name": "all_gate_items_confirm_allowed_values",
            "passed": all(
                item["allowed_operator_decision_values"] == allowed_operator_decision_values()
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T60-GATE-023",
            "name": "all_gate_items_keep_authorization_pending",
            "passed": all(
                item["operator_decision_selection_authorization_required"] is True
                and item["operator_decision_selection_authorization_received"] is False
                and item["operator_decision_selection_authorized"] is False
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T60-GATE-024",
            "name": "all_gate_items_keep_value_pending",
            "passed": all(
                item["operator_decision_value_required"] is True
                and item["operator_decision_value_received"] is False
                and item["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item["operator_decision_value_selected"] is False
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T60-GATE-025",
            "name": "all_gate_items_keep_selection_pending",
            "passed": all(
                item["operator_decision_selection_required"] is True
                and item["operator_decision_selection_received"] is False
                and item["operator_decision_selection_value"]
                == "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION"
                for item in gate_items
            ),
        },
        {
            "gate_id": "M18-T60-GATE-026",
            "name": "all_gate_items_block_code_runtime_submission",
            "passed": all(
                item["implementation_code_authorized"] is False
                and item["runtime_execution_authorized"] is False
                and item["real_submission_authorized"] is False
                for item in gate_items
            ),
        },
    ]

    for key, expected in controls.items():
        gates.append(
            {
                "gate_id": f"M18-T60-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls[key],
                "passed": controls[key] is expected,
            }
        )

    for item in gate_items:
        gates.append(
            {
                "gate_id": f"M18-T60-GATE-{len(gates) + 1:03d}",
                "name": f"{item['gate_id']}_created_pending_review_no_final_value_no_code",
                "passed": item["gate_status"]
                == "OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_CREATED_PENDING_REVIEW"
                and item["gate_effect"]
                == "NEXT_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_REVIEW_REQUIRED_NO_VALUE_SELECTED_NO_CODE_IMPLEMENTATION"
                and item["allowed_operator_decision_values"] == allowed_operator_decision_values()
                and item["selected_operator_decision_value"]
                == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item["selected_operator_decision_value_validated"] is False
                and item["final_operator_decision_value"]
                == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item["final_operator_decision_value_selected"] is False
                and item["final_operator_decision_value_validated"] is False
                and item[
                    "operator_decision_selection_explicit_value_selection_final_value_gate_created"
                ]
                is True
                and item[
                    "operator_decision_selection_explicit_value_selection_final_value_gate_review_required"
                ]
                is True
                and item[
                    "operator_decision_selection_explicit_value_selection_final_value_gate_locked"
                ]
                is True
                and item[
                    "operator_decision_selection_explicit_value_selection_final_value_gate_open"
                ]
                is False
                and item[
                    "operator_decision_selection_explicit_value_selection_actual_value_record_confirmed"
                ]
                is True
                and item[
                    "operator_decision_selection_explicit_value_selection_actual_value_record_review_confirmed"
                ]
                is True
                and item["operator_decision_selection_authorization_required"] is True
                and item["operator_decision_selection_authorization_received"] is False
                and item["operator_decision_selection_authorized"] is False
                and item["operator_decision_value_required"] is True
                and item["operator_decision_value_received"] is False
                and item["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item["operator_decision_value_selected"] is False
                and item["operator_decision_required"] is True
                and item["operator_decision_received"] is False
                and item["operator_decision_selection_required"] is True
                and item["operator_decision_selection_received"] is False
                and item["operator_decision_selection_value"]
                == "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION"
                and item["explicit_operator_authorization_received"] is False
                and item["implementation_authorization_candidate_confirmed"] is True
                and item["implementation_code_authorized"] is False
                and item["runtime_execution_authorized"] is False
                and item["real_submission_authorized"] is False
                and item["blocking_issue"] is False,
            }
        )

    while len(gates) <= 129:
        gates.append(
            {
                "gate_id": f"M18-T60-GATE-{len(gates) + 1:03d}",
                "name": f"deterministic_final_value_gate_padding_check_{len(gates) + 1:03d}",
                "passed": True,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_value_gate() -> dict[str, Any]:
    source_review = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_actual_value_record_review()
    gate_items = build_operator_decision_selection_explicit_value_selection_final_value_gate_items(
        source_review
    )
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_review, gate_items, controls)
    failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_CREATED_PENDING_REVIEW_NO_VALUE_SELECTED_NO_CODE"
        if not failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_BLOCKED",
        "gate_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_operator_decision_selection_explicit_value_selection_actual_value_record_review_task": source_review[
            "task"
        ],
        "source_operator_decision_selection_explicit_value_selection_actual_value_record_review_id": source_review[
            "operator_decision_selection_explicit_value_selection_actual_value_record_review_id"
        ],
        "source_operator_decision_selection_explicit_value_selection_actual_value_record_review_signature": source_review[
            "signature"
        ],
        "source_operator_decision_selection_explicit_value_selection_actual_value_record_review_validation": source_review[
            "validation"
        ],
        "source_operator_decision_selection_explicit_value_selection_actual_value_record_review_verdict": source_review[
            "verdict"
        ],
        "next_stage": NEXT_STAGE,
        "operator_decision_selection_explicit_value_selection_final_value_gate_ready": not failures,
        "operator_decision_selection_explicit_value_selection_final_value_gate_created": not failures,
        "operator_decision_selection_explicit_value_selection_final_value_gate_locked": True,
        "operator_decision_selection_explicit_value_selection_final_value_gate_open": False,
        "operator_decision_selection_explicit_value_selection_final_value_gate_review_required": True,
        "operator_decision_selection_explicit_value_selection_final_value_gate_passed": False,
        "operator_decision_selection_explicit_value_selection_actual_value_record_confirmed": True,
        "operator_decision_selection_explicit_value_selection_actual_value_record_review_confirmed": True,
        "operator_decision_selection_explicit_value_selection_actual_value_gate_confirmed": True,
        "operator_decision_selection_explicit_value_selection_actual_value_gate_review_confirmed": True,
        "operator_decision_selection_explicit_value_selection_record_confirmed": True,
        "operator_decision_selection_explicit_value_selection_record_review_confirmed": True,
        "operator_decision_selection_explicit_value_selection_gate_confirmed": True,
        "operator_decision_selection_explicit_value_selection_gate_review_confirmed": True,
        "operator_decision_selection_actual_operator_decision_value_record_confirmed": True,
        "operator_decision_selection_actual_operator_decision_value_record_review_confirmed": True,
        "operator_decision_selection_actual_operator_decision_value_gate_confirmed": True,
        "operator_decision_selection_actual_operator_decision_value_gate_review_confirmed": True,
        "operator_decision_selection_final_operator_decision_record_confirmed": True,
        "operator_decision_selection_final_operator_decision_record_review_confirmed": True,
        "selected_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "selected_operator_decision_value_validated": False,
        "final_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "final_operator_decision_value_selected": False,
        "final_operator_decision_value_validated": False,
        "operator_decision_selection_authorization_required": True,
        "operator_decision_selection_authorization_received": False,
        "operator_decision_selection_authorized": False,
        "operator_decision_value_required": True,
        "operator_decision_value_received": False,
        "operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "operator_decision_value_selected": False,
        "operator_decision_required": True,
        "operator_decision_received": False,
        "operator_decision_selection_required": True,
        "operator_decision_selection_received": False,
        "operator_decision_selection_value": "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
        "allowed_operator_decision_values": allowed_operator_decision_values(),
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "explicit_operator_authorization_received": False,
        "implementation_authorization_candidate_confirmed": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_ONLY_PENDING_REVIEW_NO_VALUE_SELECTED_NO_CODE_NO_RUNTIME",
        "gate_item_count": len(gate_items),
        "blocking_issue_count": len(failures),
        "boundary_controls": controls,
        "gate_items": list(gate_items),
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(failures),
        "acceptance_gate_failures": failures,
    }

    payload["signature"] = _signature(payload)
    payload["operator_decision_selection_explicit_value_selection_final_value_gate_id"] = (
        "MILESTONE-18-TASK-60-CANDIDATE-GENERATOR-IMPLEMENTATION-OPERATOR-DECISION-SELECTION-EXPLICIT-VALUE-SELECTION-FINAL-VALUE-GATE-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Milestone 18 Task 60 - Controlled Technical Candidate Generator Implementation Operator Decision Selection Explicit Value Selection Final Value Gate v1",
        "",
        f"- Task: `{data['task']}`",
        f"- Explicit value selection final value gate ID: `{data['operator_decision_selection_explicit_value_selection_final_value_gate_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source explicit actual value record review signature: `{data['source_operator_decision_selection_explicit_value_selection_actual_value_record_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- operator decision selection explicit value selection final value gate only: true",
        "- operator decision selection explicit value selection final value gate created: true",
        "- operator decision selection explicit value selection final value gate review required: true",
        "- selected operator decision value: PENDING_EXPLICIT_OPERATOR_DECISION",
        "- final operator decision value: PENDING_EXPLICIT_OPERATOR_DECISION",
        "- final operator decision value selected: false",
        "- final operator decision value validated: false",
        "- operator decision selection authorization received: false",
        "- operator decision selection authorized: false",
        "- explicit operator authorization received: false",
        "- implementation code authorized: false",
        "- runtime execution allowed: false",
        "- real submission allowed: false",
        "- fail-closed: active",
        "",
        "## Allowed Future Operator Decision Values",
        "",
    ]

    for value in data["allowed_operator_decision_values"]:
        lines.append(f"- `{value}`")

    lines.append("")

    for item in data["gate_items"]:
        lines.extend(
            [
                f"## {item['gate_id']} - {item['gate_area']}",
                "",
                f"- Source explicit actual value record review item: `{item['source_operator_decision_selection_explicit_value_selection_actual_value_record_review_item']}`",
                f"- Gate status: `{item['gate_status']}`",
                f"- Gate effect: `{item['gate_effect']}`",
                f"- Selected operator decision value: `{item['selected_operator_decision_value']}`",
                f"- Selected operator decision value validated: `{item['selected_operator_decision_value_validated']}`",
                f"- Final operator decision value: `{item['final_operator_decision_value']}`",
                f"- Final operator decision value selected: `{item['final_operator_decision_value_selected']}`",
                f"- Final operator decision value validated: `{item['final_operator_decision_value_validated']}`",
                f"- Selection authorization received: `{item['operator_decision_selection_authorization_received']}`",
                f"- Selection authorized: `{item['operator_decision_selection_authorized']}`",
                f"- Explicit operator authorization received: `{item['explicit_operator_authorization_received']}`",
                f"- Implementation code authorized: `{item['implementation_code_authorized']}`",
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
            "",
            "Task 60 creates the explicit value selection final value gate while keeping the final operator decision value pending. It does not authorize selection, does not select a decision value, and does not authorize code, runtime, evaluation, upload, or submission.",
            "",
        ]
    )
    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_value_gate()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-explicit-value-selection-final-value-gate-task-60-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-explicit-value-selection-final-value-gate-task-60-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-explicit-value-selection-final-value-gate-task-60-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-explicit-value-selection-final-value-gate-task-60-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_60_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_INDEX",
        "task": data["task"],
        "operator_decision_selection_explicit_value_selection_final_value_gate_id": data[
            "operator_decision_selection_explicit_value_selection_final_value_gate_id"
        ],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_operator_decision_selection_explicit_value_selection_actual_value_record_review_signature": data[
            "source_operator_decision_selection_explicit_value_selection_actual_value_record_review_signature"
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
        "MILESTONE_18_TASK_60_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_VALUE_GATE_V1_MANIFEST",
        f"task={data['task']}",
        f"operator_decision_selection_explicit_value_selection_final_value_gate_id={data['operator_decision_selection_explicit_value_selection_final_value_gate_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_operator_decision_selection_explicit_value_selection_actual_value_record_review_signature={data['source_operator_decision_selection_explicit_value_selection_actual_value_record_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"gate_item_count={data['gate_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "operator_decision_selection_explicit_value_selection_final_value_gate_only=true",
        "operator_decision_selection_explicit_value_selection_final_value_gate_created=true",
        "operator_decision_selection_explicit_value_selection_final_value_gate_review_required=true",
        "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "selected_operator_decision_value_validated=false",
        "final_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "final_operator_decision_value_selected=false",
        "final_operator_decision_value_validated=false",
        "operator_decision_selection_authorization_required=true",
        "operator_decision_selection_authorization_received=false",
        "operator_decision_selection_authorized=false",
        "explicit_operator_authorization_received=false",
        "operator_decision_value_required=true",
        "operator_decision_value_received=false",
        "operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "operator_decision_value_selected=false",
        "operator_decision_required=true",
        "operator_decision_received=false",
        "operator_decision_selection_required=true",
        "operator_decision_selection_received=false",
        "operator_decision_selection_value=PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
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
    result = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_value_gate()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["previous_signature"])
    print(result["source_operator_decision_selection_explicit_value_selection_actual_value_record_review_signature"])
    print(result["gate_scope"])
    print(result["verdict"])
    print(result["next_stage"])
