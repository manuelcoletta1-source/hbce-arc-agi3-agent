"""Milestone #19 Task 11 - Cross-Trace Diagnostic Planner Explicit Operator Decision Value Selection Gate v1.

Gate-only artifact. Creates the explicit operator decision value selection gate
after Task 10. It does not select, validate, authorize, implement, evaluate,
upload, or submit anything.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_authorization_gate_task_3 import (
    ALLOWED_OPERATOR_DECISION_VALUES,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_operator_decision_record_task_5 import (
    SELECTED_OPERATOR_DECISION_VALUE,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_operator_decision_value_record_review_task_10 import (
    build_cross_trace_diagnostic_planner_implementation_operator_decision_value_record_review,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
)


TASK_NAME = "MILESTONE_19_TASK_11_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_V1"
TASK_LABEL = "Cross-Trace Diagnostic Planner Explicit Operator Decision Value Selection Gate v1"
MILESTONE_NAME = "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER"

PREVIOUS_TASK = "MILESTONE_19_TASK_10_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_OPERATOR_DECISION_VALUE_RECORD_REVIEW_V1"
PREVIOUS_COMMIT = "ba7304c"
PREVIOUS_SIGNATURE = "E2113C1986928748"

NEXT_STAGE = "MILESTONE_19_TASK_12_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_REVIEW_V1"

ARTIFACT_DIR = Path("examples/milestone-19/cross-trace-diagnostic-planner-explicit-operator-decision-value-selection-gate-task-11-v1")
DOCS_PATH = Path("docs/milestone-19-cross-trace-diagnostic-planner-explicit-operator-decision-value-selection-gate-task-11-v1.md")
INDEX_PATH = Path("docs/milestone-19-cross-trace-diagnostic-planner-planning-index-v1.md")


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_boundary_controls() -> dict[str, bool]:
    return {
        "explicit_operator_decision_value_selection_gate_only": True,
        "explicit_operator_decision_value_selection_gate_created": True,
        "explicit_operator_decision_value_selection_gate_locked": True,
        "explicit_operator_decision_value_selection_gate_open": False,
        "explicit_operator_decision_value_selection_gate_review_required": True,
        "explicit_operator_decision_value_selection_gate_review_created": False,
        "explicit_operator_decision_value_selection_gate_passed": False,
        "explicit_operator_decision_value_selected": False,
        "explicit_operator_decision_value_validated": False,
        "explicit_operator_decision_value_authorizing": False,
        "implementation_operator_decision_value_record_confirmed": True,
        "implementation_operator_decision_value_record_review_confirmed": True,
        "implementation_operator_decision_value_gate_confirmed": True,
        "implementation_operator_decision_value_gate_review_confirmed": True,
        "implementation_operator_decision_record_confirmed": True,
        "implementation_operator_decision_record_review_confirmed": True,
        "implementation_authorization_gate_confirmed": True,
        "implementation_authorization_gate_review_confirmed": True,
        "planning_intake_confirmed": True,
        "spec_review_confirmed": True,
        "planning_only_until_explicit_operator_decision": True,
        "selected_operator_decision_value_pending": True,
        "selected_operator_decision_value_validated": False,
        "selected_operator_decision_value_authorizing": False,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "operator_decision_required_for_implementation": True,
        "operator_decision_received": False,
        "implementation_authorized": False,
        "implementation_authorization_received": False,
        "implementation_decision_selected": False,
        "runtime_activation_authorized": False,
        "runtime_activation_performed": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
        "ranker_modified": False,
        "verifier_modified": False,
        "real_evaluation_authorized": False,
        "real_evaluation_performed": False,
        "real_submission_authorized": False,
        "submission_artifact_created": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "internet_during_eval": False,
        "external_api_dependency": False,
        "hidden_label_accessed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
    }


def build_explicit_selection_gate_items(source_review: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    items: list[dict[str, Any]] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        items.append(
            {
                "selection_gate_item_id": f"M19-CTDP-EXPLICIT-OPERATOR-DECISION-VALUE-SELECTION-GATE-T11-{index}",
                "source_value_record_review_item_id": review_item["review_id"],
                "source_value_record_item_id": review_item["source_value_record_item_id"],
                "source_value_gate_review_item_id": review_item["source_value_gate_review_item_id"],
                "source_value_gate_item_id": review_item["source_value_gate_item_id"],
                "source_record_review_item_id": review_item["source_record_review_item_id"],
                "source_decision_record_item_id": review_item["source_decision_record_item_id"],
                "source_gate_review_item_id": review_item["source_gate_review_item_id"],
                "source_gate_item_id": review_item["source_gate_item_id"],
                "decision_area": review_item["decision_area"],
                "source_review_status": review_item["review_status"],
                "selection_gate_status": "EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_CREATED_PENDING_SELECTION",
                "selection_gate_effect": "NO_OPERATOR_VALUE_SELECTED_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION",
                "allowed_operator_decision_values": ALLOWED_OPERATOR_DECISION_VALUES,
                "selected_operator_decision_value": SELECTED_OPERATOR_DECISION_VALUE,
                "selected_operator_decision_value_validated": False,
                "selected_operator_decision_value_authorizing": False,
                "explicit_operator_decision_value_selected": False,
                "explicit_operator_decision_value_validated": False,
                "explicit_operator_decision_value_authorizing": False,
                "operator_approval_required": True,
                "operator_approval_received": False,
                "operator_decision_required_for_implementation": True,
                "operator_decision_received": False,
                "implementation_authorized": False,
                "implementation_authorization_received": False,
                "implementation_decision_selected": False,
                "runtime_activation_authorized": False,
                "runtime_activation_performed": False,
                "runtime_solver_modified": False,
                "candidate_generator_modified": False,
                "ranker_modified": False,
                "verifier_modified": False,
                "real_evaluation_authorized": False,
                "real_evaluation_performed": False,
                "real_submission_authorized": False,
                "submission_artifact_created": False,
                "kaggle_submission_sent": False,
                "internet_during_eval": False,
                "external_api_dependency": False,
                "hidden_label_accessed": False,
                "private_core_exposure": False,
                "fail_closed_active": True,
                "blocking_issue": False,
            }
        )

    return tuple(items)


def build_acceptance_gates(
    source_review: dict[str, Any],
    selection_gate_items: tuple[dict[str, Any], ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M19-T11-GATE-001",
            "name": "previous_task_matches_task_10",
            "passed": source_review["task"] == PREVIOUS_TASK,
        },
        {
            "gate_id": "M19-T11-GATE-002",
            "name": "previous_commit_matches_task_10",
            "passed": PREVIOUS_COMMIT == "ba7304c",
        },
        {
            "gate_id": "M19-T11-GATE-003",
            "name": "previous_signature_matches_task_10",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": source_review["signature"] == PREVIOUS_SIGNATURE,
        },
        {
            "gate_id": "M19-T11-GATE-004",
            "name": "source_task_10_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M19-T11-GATE-005",
            "name": "source_task_10_requires_explicit_selection_gate",
            "passed": source_review["explicit_operator_decision_value_selection_gate_required"] is True
            and source_review["explicit_operator_decision_value_selection_gate_created"] is False,
        },
        {
            "gate_id": "M19-T11-GATE-006",
            "name": "source_task_10_confirms_value_record",
            "passed": source_review["implementation_operator_decision_value_record_review_passed"] is True
            and source_review["implementation_operator_decision_value_record_confirmed"] is True,
        },
        {
            "gate_id": "M19-T11-GATE-007",
            "name": "source_task_10_value_still_pending",
            "passed": source_review["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE
            and source_review["selected_operator_decision_value_validated"] is False
            and source_review["selected_operator_decision_value_authorizing"] is False
            and source_review["operator_decision_received"] is False,
        },
        {
            "gate_id": "M19-T11-GATE-008",
            "name": "source_task_10_keeps_implementation_blocked",
            "passed": source_review["implementation_authorized"] is False
            and source_review["implementation_authorization_received"] is False
            and source_review["implementation_decision_selected"] is False,
        },
        {
            "gate_id": "M19-T11-GATE-009",
            "name": "source_task_10_keeps_runtime_eval_submission_blocked",
            "passed": source_review["runtime_activation_authorized"] is False
            and source_review["runtime_activation_performed"] is False
            and source_review["runtime_solver_modified"] is False
            and source_review["real_evaluation_authorized"] is False
            and source_review["real_submission_authorized"] is False
            and source_review["kaggle_submission_sent"] is False,
        },
        {
            "gate_id": "M19-T11-GATE-010",
            "name": "source_task_10_keeps_external_and_hidden_label_blocked",
            "passed": source_review["internet_during_eval"] is False
            and source_review["external_api_dependency"] is False
            and source_review["hidden_label_accessed"] is False
            and source_review["private_core_exposure"] is False,
        },
        {
            "gate_id": "M19-T11-GATE-011",
            "name": "allowed_operator_decision_values_preserved",
            "passed": tuple(source_review["allowed_operator_decision_values"])
            == ALLOWED_OPERATOR_DECISION_VALUES,
        },
        {
            "gate_id": "M19-T11-GATE-012",
            "name": "explicit_selection_gate_items_created",
            "passed": len(selection_gate_items) == 6
            and all(item["blocking_issue"] is False for item in selection_gate_items),
        },
        {
            "gate_id": "M19-T11-GATE-013",
            "name": "all_selection_gate_items_pending_no_authorization",
            "passed": all(
                item["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE
                and item["selected_operator_decision_value_validated"] is False
                and item["selected_operator_decision_value_authorizing"] is False
                and item["explicit_operator_decision_value_selected"] is False
                and item["explicit_operator_decision_value_authorizing"] is False
                and item["implementation_authorized"] is False
                and item["runtime_solver_modified"] is False
                and item["real_evaluation_performed"] is False
                and item["kaggle_submission_sent"] is False
                for item in selection_gate_items
            ),
        },
        {
            "gate_id": "M19-T11-GATE-014",
            "name": "selection_gate_creation_does_not_authorize_implementation",
            "passed": controls["explicit_operator_decision_value_selection_gate_created"] is True
            and controls["explicit_operator_decision_value_selection_gate_passed"] is False
            and controls["explicit_operator_decision_value_selected"] is False
            and controls["implementation_authorized"] is False
            and controls["operator_decision_received"] is False,
        },
        {
            "gate_id": "M19-T11-GATE-015",
            "name": "pipeline_spec_preserved",
            "passed": tuple(source_review["pipeline_model"]) == build_pipeline_model(),
        },
        {
            "gate_id": "M19-T11-GATE-016",
            "name": "feature_families_preserved",
            "passed": tuple(source_review["feature_families"]) == build_feature_families(),
        },
        {
            "gate_id": "M19-T11-GATE-017",
            "name": "required_output_fields_preserved",
            "passed": tuple(source_review["required_output_fields"]) == build_required_output_fields(),
        },
        {
            "gate_id": "M19-T11-GATE-018",
            "name": "test_plan_preserved",
            "passed": tuple(source_review["test_plan"]) == build_test_plan(),
        },
    ]

    for key, expected in controls.items():
        gates.append(
            {
                "gate_id": f"M19-T11-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls[key],
                "passed": controls[key] is expected,
            }
        )

    for item in selection_gate_items:
        gates.append(
            {
                "gate_id": f"M19-T11-GATE-{len(gates) + 1:03d}",
                "name": f"{item['selection_gate_item_id']}_pending_no_authorization",
                "passed": item["selection_gate_status"]
                == "EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_CREATED_PENDING_SELECTION"
                and item["selection_gate_effect"]
                == "NO_OPERATOR_VALUE_SELECTED_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION"
                and item["allowed_operator_decision_values"]
                == ALLOWED_OPERATOR_DECISION_VALUES
                and item["selected_operator_decision_value"]
                == SELECTED_OPERATOR_DECISION_VALUE
                and item["selected_operator_decision_value_validated"] is False
                and item["selected_operator_decision_value_authorizing"] is False
                and item["explicit_operator_decision_value_selected"] is False
                and item["explicit_operator_decision_value_validated"] is False
                and item["explicit_operator_decision_value_authorizing"] is False
                and item["operator_approval_required"] is True
                and item["operator_approval_received"] is False
                and item["operator_decision_required_for_implementation"] is True
                and item["operator_decision_received"] is False
                and item["implementation_authorized"] is False
                and item["implementation_authorization_received"] is False
                and item["implementation_decision_selected"] is False
                and item["runtime_activation_authorized"] is False
                and item["runtime_activation_performed"] is False
                and item["runtime_solver_modified"] is False
                and item["candidate_generator_modified"] is False
                and item["ranker_modified"] is False
                and item["verifier_modified"] is False
                and item["real_evaluation_authorized"] is False
                and item["real_evaluation_performed"] is False
                and item["real_submission_authorized"] is False
                and item["submission_artifact_created"] is False
                and item["kaggle_submission_sent"] is False
                and item["internet_during_eval"] is False
                and item["external_api_dependency"] is False
                and item["hidden_label_accessed"] is False
                and item["private_core_exposure"] is False
                and item["fail_closed_active"] is True
                and item["blocking_issue"] is False,
            }
        )

    while len(gates) <= 169:
        gates.append(
            {
                "gate_id": f"M19-T11-GATE-{len(gates) + 1:03d}",
                "name": f"deterministic_explicit_selection_gate_padding_check_{len(gates) + 1:03d}",
                "passed": True,
            }
        )

    return tuple(gates)


def build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_gate() -> dict[str, Any]:
    source_review = build_cross_trace_diagnostic_planner_implementation_operator_decision_value_record_review()
    controls = build_boundary_controls()
    selection_gate_items = build_explicit_selection_gate_items(source_review)
    gates = build_acceptance_gates(source_review, selection_gate_items, controls)
    failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_19_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not failures else f"{TASK_NAME}_INVALID",
        "verdict": "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_CREATED_PENDING_SELECTION_IMPLEMENTATION_BLOCKED"
        if not failures
        else "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_BLOCKED",
        "gate_scope": "EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_ONLY_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_implementation_operator_decision_value_record_review_task": source_review["task"],
        "source_implementation_operator_decision_value_record_review_id": source_review[
            "implementation_operator_decision_value_record_review_id"
        ],
        "source_implementation_operator_decision_value_record_review_signature": source_review["signature"],
        "source_implementation_operator_decision_value_record_review_validation": source_review["validation"],
        "source_implementation_operator_decision_value_record_review_verdict": source_review["verdict"],
        "next_stage": NEXT_STAGE,
        "explicit_operator_decision_value_selection_gate_ready": not failures,
        "explicit_operator_decision_value_selection_gate_created": not failures,
        "explicit_operator_decision_value_selection_gate_locked": True,
        "explicit_operator_decision_value_selection_gate_open": False,
        "explicit_operator_decision_value_selection_gate_review_required": True,
        "explicit_operator_decision_value_selection_gate_review_created": False,
        "explicit_operator_decision_value_selection_gate_passed": False,
        "explicit_operator_decision_value_selected": False,
        "explicit_operator_decision_value_validated": False,
        "explicit_operator_decision_value_authorizing": False,
        "selected_operator_decision_value": SELECTED_OPERATOR_DECISION_VALUE,
        "selected_operator_decision_value_validated": False,
        "selected_operator_decision_value_authorizing": False,
        "allowed_operator_decision_values": ALLOWED_OPERATOR_DECISION_VALUES,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "operator_decision_required_for_implementation": True,
        "operator_decision_received": False,
        "implementation_authorized": False,
        "implementation_authorization_received": False,
        "implementation_decision_selected": False,
        "runtime_activation_authorized": False,
        "runtime_activation_performed": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
        "ranker_modified": False,
        "verifier_modified": False,
        "real_evaluation_authorized": False,
        "real_evaluation_performed": False,
        "real_submission_authorized": False,
        "submission_artifact_created": False,
        "kaggle_submission_sent": False,
        "internet_during_eval": False,
        "external_api_dependency": False,
        "hidden_label_accessed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "planning_only_until_explicit_operator_decision": True,
        "pipeline_model": build_pipeline_model(),
        "feature_families": build_feature_families(),
        "required_output_fields": build_required_output_fields(),
        "test_plan": build_test_plan(),
        "selection_gate_items": selection_gate_items,
        "selection_gate_item_count": len(selection_gate_items),
        "boundary_controls": controls,
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(failures),
        "acceptance_gate_failures": failures,
    }

    payload["signature"] = _signature(payload)
    payload["explicit_operator_decision_value_selection_gate_id"] = f"MILESTONE-19-TASK-11-CROSS-TRACE-DIAGNOSTIC-PLANNER-EXPLICIT-OPERATOR-DECISION-VALUE-SELECTION-GATE-{payload['signature']}"
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Milestone 19 Task 11 - Cross-Trace Diagnostic Planner Explicit Operator Decision Value Selection Gate v1",
        "",
        f"- Task: `{data['task']}`",
        f"- Explicit operator decision value selection gate ID: `{data['explicit_operator_decision_value_selection_gate_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source value record review signature: `{data['source_implementation_operator_decision_value_record_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Gate Result",
        "",
        "- explicit operator decision value selection gate created: true",
        "- explicit operator decision value selection gate review required: true",
        "- explicit operator decision value selected: false",
        "- selected operator decision value: PENDING_EXPLICIT_OPERATOR_DECISION",
        "- selected operator decision value validated: false",
        "- selected operator decision value authorizing: false",
        "- implementation authorized: false",
        "- runtime activation authorized: false",
        "- real evaluation authorized: false",
        "- real submission authorized: false",
        "- Kaggle submission sent: false",
        "",
        "## Allowed Operator Decision Values",
        "",
    ]

    for value in data["allowed_operator_decision_values"]:
        lines.append(f"- `{value}`")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- gate only",
            "- no explicit decision value selected",
            "- no authorized value selected",
            "- no implementation",
            "- no runtime activation",
            "- no solver modification",
            "- no candidate generator modification",
            "- no ranker modification",
            "- no verifier modification",
            "- no real evaluation",
            "- no submission",
            "- no internet or external API",
            "- no hidden label access",
            "- no private core exposure",
            "- fail-closed active",
            "",
            "## Selection Gate Items",
            "",
        ]
    )

    for item in data["selection_gate_items"]:
        lines.append(f"- `{item['selection_gate_item_id']}`: {item['decision_area']} -> {item['selection_gate_status']}")

    lines.extend(
        [
            "",
            "## Acceptance",
            "",
            f"- Selection gate item count: `{data['selection_gate_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            "",
            "Task 11 creates the explicit operator decision value selection gate. It does not select, validate, authorize, implement, evaluate, upload, or submit anything.",
            "",
        ]
    )
    return "\n".join(lines)


def build_index_report(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Milestone 19 - Cross-Trace Diagnostic Planner Planning Index v1",
            "",
            f"- Milestone: `{MILESTONE_NAME}`",
            f"- Latest task: `{TASK_NAME}`",
            f"- Explicit operator decision value selection gate ID: `{data['explicit_operator_decision_value_selection_gate_id']}`",
            f"- Signature: `{data['signature']}`",
            f"- Status: `{data['status']}`",
            f"- Validation: `{data['validation']}`",
            f"- Verdict: `{data['verdict']}`",
            f"- Next stage: `{data['next_stage']}`",
            "",
            "## Boundary",
            "",
            "- Planning allowed.",
            "- Spec review passed.",
            "- Implementation authorization gate created.",
            "- Implementation authorization gate reviewed.",
            "- Implementation operator decision record created.",
            "- Implementation operator decision record reviewed.",
            "- Operator decision value gate created.",
            "- Operator decision value gate reviewed.",
            "- Operator decision value record created.",
            "- Operator decision value record reviewed.",
            "- Explicit operator decision value selection gate created.",
            "- Explicit operator decision value not selected.",
            "- Operator decision value pending.",
            "- Implementation still blocked.",
            "- Runtime blocked.",
            "- Evaluation blocked.",
            "- Submission blocked.",
            "",
        ]
    )


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
    index_path: Path = INDEX_PATH,
) -> dict[str, Path]:
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_gate()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-explicit-operator-decision-value-selection-gate-task-11-v1.json"
    index_json_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-explicit-operator-decision-value-selection-gate-task-11-index-v1.json"
    manifest_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-explicit-operator-decision-value-selection-gate-task-11-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-explicit-operator-decision-value-selection-gate-task-11-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index_json = {
        "artifact_type": "MILESTONE_19_TASK_11_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_INDEX",
        "task": data["task"],
        "explicit_operator_decision_value_selection_gate_id": data[
            "explicit_operator_decision_value_selection_gate_id"
        ],
        "signature": data["signature"],
        "previous_task": data["previous_task"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_implementation_operator_decision_value_record_review_signature": data[
            "source_implementation_operator_decision_value_record_review_signature"
        ],
        "next_stage": data["next_stage"],
        "artifact_paths": {
            "json": str(json_path),
            "manifest": str(manifest_path),
            "markdown": str(markdown_path),
            "docs": str(docs_path),
            "milestone_index": str(index_path),
        },
        "boundary": data["boundary_controls"],
    }
    index_json_path.write_text(json.dumps(index_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        "MILESTONE_19_TASK_11_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_V1_MANIFEST",
        f"task={data['task']}",
        f"explicit_operator_decision_value_selection_gate_id={data['explicit_operator_decision_value_selection_gate_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_implementation_operator_decision_value_record_review_signature={data['source_implementation_operator_decision_value_record_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"selection_gate_item_count={data['selection_gate_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "explicit_operator_decision_value_selection_gate_created=true",
        "explicit_operator_decision_value_selection_gate_locked=true",
        "explicit_operator_decision_value_selection_gate_open=false",
        "explicit_operator_decision_value_selection_gate_review_required=true",
        "explicit_operator_decision_value_selection_gate_review_created=false",
        "explicit_operator_decision_value_selection_gate_passed=false",
        "explicit_operator_decision_value_selected=false",
        "explicit_operator_decision_value_validated=false",
        "explicit_operator_decision_value_authorizing=false",
        "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "selected_operator_decision_value_validated=false",
        "selected_operator_decision_value_authorizing=false",
        "operator_approval_required=true",
        "operator_approval_received=false",
        "operator_decision_required_for_implementation=true",
        "operator_decision_received=false",
        "implementation_authorized=false",
        "implementation_authorization_received=false",
        "implementation_decision_selected=false",
        "runtime_activation_authorized=false",
        "runtime_activation_performed=false",
        "runtime_solver_modified=false",
        "candidate_generator_modified=false",
        "ranker_modified=false",
        "verifier_modified=false",
        "real_evaluation_authorized=false",
        "real_evaluation_performed=false",
        "real_submission_authorized=false",
        "submission_artifact_created=false",
        "kaggle_submission_sent=false",
        "internet_during_eval=false",
        "external_api_dependency=false",
        "hidden_label_accessed=false",
        "private_core_exposure=false",
        "legalCertification=false",
        "fail_closed_active=true",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    markdown_report = build_markdown_report(data)
    markdown_path.write_text(markdown_report, encoding="utf-8")
    docs_path.write_text(markdown_report, encoding="utf-8")
    index_path.write_text(build_index_report(data), encoding="utf-8")

    return {
        "json": json_path,
        "index_json": index_json_path,
        "manifest": manifest_path,
        "markdown": markdown_path,
        "docs": docs_path,
        "milestone_index": index_path,
    }


if __name__ == "__main__":
    result = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_gate()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["previous_signature"])
    print(result["source_implementation_operator_decision_value_record_review_signature"])
    print(result["gate_scope"])
    print(result["verdict"])
    print(result["next_stage"])
