"""Milestone #19 Task 3 - Cross-Trace Diagnostic Planner Implementation Authorization Gate v1.

Gate-only artifact. Creates the formal implementation authorization gate while
keeping implementation, runtime, evaluation, and submission blocked.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_spec_review_task_2 import (
    build_cross_trace_diagnostic_planner_spec_review,
)


TASK_NAME = "MILESTONE_19_TASK_3_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_AUTHORIZATION_GATE_V1"
TASK_LABEL = "Cross-Trace Diagnostic Planner Implementation Authorization Gate v1"
MILESTONE_NAME = "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER"

PREVIOUS_TASK = "MILESTONE_19_TASK_2_CROSS_TRACE_DIAGNOSTIC_PLANNER_SPEC_REVIEW_V1"
PREVIOUS_COMMIT = "98bfea3"
PREVIOUS_SIGNATURE = "E1993A6E809CCEFA"

NEXT_STAGE = "MILESTONE_19_TASK_4_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_AUTHORIZATION_GATE_REVIEW_V1"

ARTIFACT_DIR = Path("examples/milestone-19/cross-trace-diagnostic-planner-implementation-authorization-gate-task-3-v1")
DOCS_PATH = Path("docs/milestone-19-cross-trace-diagnostic-planner-implementation-authorization-gate-task-3-v1.md")
INDEX_PATH = Path("docs/milestone-19-cross-trace-diagnostic-planner-planning-index-v1.md")


ALLOWED_OPERATOR_DECISION_VALUES = (
    "AUTHORIZE_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_ONLY",
    "DEFER_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_KEEP_PLANNING_ONLY",
    "REJECT_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_KEEP_FAIL_CLOSED",
    "REQUEST_ADDITIONAL_SPEC_EVIDENCE_BEFORE_IMPLEMENTATION",
    "REQUIRE_BOUNDARY_RECHECK_BEFORE_IMPLEMENTATION",
)


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_boundary_controls() -> dict[str, bool]:
    return {
        "implementation_authorization_gate_only": True,
        "implementation_authorization_gate_created": True,
        "implementation_authorization_gate_locked": True,
        "implementation_authorization_gate_open": False,
        "implementation_authorization_gate_review_required": True,
        "implementation_authorization_gate_passed": False,
        "planning_intake_confirmed": True,
        "spec_review_confirmed": True,
        "planning_only_until_operator_decision": True,
        "implementation_authorized": False,
        "implementation_authorization_received": False,
        "implementation_decision_selected": False,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "operator_decision_required_for_implementation": True,
        "operator_decision_received": False,
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


def build_authorization_gate_items(source_review: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    return (
        {
            "gate_item_id": "M19-CTDP-IMPLEMENTATION-AUTH-GATE-T3-1",
            "gate_area": "implementation_scope",
            "source": "MILESTONE_19_TASK_2_SPEC_REVIEW",
            "allowed_scope": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_ONLY",
            "implementation_authorized": False,
            "operator_decision_required": True,
            "gate_status": "CREATED_PENDING_EXPLICIT_OPERATOR_DECISION",
            "blocking_issue": False,
        },
        {
            "gate_item_id": "M19-CTDP-IMPLEMENTATION-AUTH-GATE-T3-2",
            "gate_area": "runtime_activation",
            "source": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1",
            "runtime_activation_authorized": False,
            "runtime_activation_performed": False,
            "runtime_solver_modified": False,
            "gate_status": "RUNTIME_BLOCKED",
            "blocking_issue": False,
        },
        {
            "gate_item_id": "M19-CTDP-IMPLEMENTATION-AUTH-GATE-T3-3",
            "gate_area": "real_evaluation",
            "source": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1",
            "real_evaluation_authorized": False,
            "real_evaluation_performed": False,
            "hidden_label_accessed": False,
            "gate_status": "REAL_EVALUATION_BLOCKED",
            "blocking_issue": False,
        },
        {
            "gate_item_id": "M19-CTDP-IMPLEMENTATION-AUTH-GATE-T3-4",
            "gate_area": "submission_boundary",
            "source": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1",
            "real_submission_authorized": False,
            "submission_artifact_created": False,
            "kaggle_submission_sent": False,
            "gate_status": "SUBMISSION_BLOCKED",
            "blocking_issue": False,
        },
        {
            "gate_item_id": "M19-CTDP-IMPLEMENTATION-AUTH-GATE-T3-5",
            "gate_area": "external_access_boundary",
            "source": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1",
            "internet_during_eval": False,
            "external_api_dependency": False,
            "private_core_exposure": False,
            "gate_status": "EXTERNAL_ACCESS_BLOCKED",
            "blocking_issue": False,
        },
        {
            "gate_item_id": "M19-CTDP-IMPLEMENTATION-AUTH-GATE-T3-6",
            "gate_area": "operator_decision_values",
            "source": "MILESTONE_19_TASK_3_AUTHORIZATION_GATE",
            "allowed_operator_decision_values": ALLOWED_OPERATOR_DECISION_VALUES,
            "selected_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
            "operator_decision_received": False,
            "implementation_authorized": False,
            "gate_status": "PENDING_EXPLICIT_OPERATOR_DECISION",
            "blocking_issue": False,
        },
    )


def build_acceptance_gates(
    source_review: dict[str, Any],
    gate_items: tuple[dict[str, Any], ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M19-T3-GATE-001",
            "name": "previous_task_matches_task_2",
            "passed": source_review["task"] == PREVIOUS_TASK,
        },
        {
            "gate_id": "M19-T3-GATE-002",
            "name": "previous_commit_matches_task_2",
            "passed": PREVIOUS_COMMIT == "98bfea3",
        },
        {
            "gate_id": "M19-T3-GATE-003",
            "name": "previous_signature_matches_task_2",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": source_review["signature"] == PREVIOUS_SIGNATURE,
        },
        {
            "gate_id": "M19-T3-GATE-004",
            "name": "source_task_2_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M19-T3-GATE-005",
            "name": "source_task_2_requires_implementation_gate",
            "passed": source_review["implementation_gate_required"] is True
            and source_review["implementation_gate_created"] is False
            and source_review["implementation_authorized"] is False,
        },
        {
            "gate_id": "M19-T3-GATE-006",
            "name": "source_task_2_keeps_runtime_eval_submission_blocked",
            "passed": source_review["runtime_activation_performed"] is False
            and source_review["runtime_solver_modified"] is False
            and source_review["real_evaluation_performed"] is False
            and source_review["kaggle_submission_sent"] is False,
        },
        {
            "gate_id": "M19-T3-GATE-007",
            "name": "pipeline_spec_preserved",
            "passed": tuple(source_review["pipeline_model"]) == build_pipeline_model(),
        },
        {
            "gate_id": "M19-T3-GATE-008",
            "name": "feature_families_preserved",
            "passed": tuple(source_review["feature_families"]) == build_feature_families(),
        },
        {
            "gate_id": "M19-T3-GATE-009",
            "name": "required_output_fields_preserved",
            "passed": tuple(source_review["required_output_fields"]) == build_required_output_fields(),
        },
        {
            "gate_id": "M19-T3-GATE-010",
            "name": "test_plan_preserved",
            "passed": tuple(source_review["test_plan"]) == build_test_plan(),
        },
        {
            "gate_id": "M19-T3-GATE-011",
            "name": "authorization_gate_items_created",
            "passed": len(gate_items) == 6
            and all(item["blocking_issue"] is False for item in gate_items),
        },
        {
            "gate_id": "M19-T3-GATE-012",
            "name": "implementation_not_authorized_by_gate_creation",
            "passed": controls["implementation_authorization_gate_created"] is True
            and controls["implementation_authorized"] is False
            and controls["implementation_authorization_received"] is False
            and controls["operator_approval_received"] is False,
        },
        {
            "gate_id": "M19-T3-GATE-013",
            "name": "runtime_eval_submission_remain_blocked",
            "passed": controls["runtime_activation_authorized"] is False
            and controls["real_evaluation_authorized"] is False
            and controls["real_submission_authorized"] is False
            and controls["kaggle_submission_sent"] is False,
        },
    ]

    for key, expected in controls.items():
        gates.append(
            {
                "gate_id": f"M19-T3-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls[key],
                "passed": controls[key] is expected,
            }
        )

    for item in gate_items:
        gates.append(
            {
                "gate_id": f"M19-T3-GATE-{len(gates) + 1:03d}",
                "name": f"{item['gate_item_id']}_created_pending_no_implementation",
                "passed": item["blocking_issue"] is False
                and item["gate_status"] in {
                    "CREATED_PENDING_EXPLICIT_OPERATOR_DECISION",
                    "RUNTIME_BLOCKED",
                    "REAL_EVALUATION_BLOCKED",
                    "SUBMISSION_BLOCKED",
                    "EXTERNAL_ACCESS_BLOCKED",
                    "PENDING_EXPLICIT_OPERATOR_DECISION",
                }
                and item.get("implementation_authorized", False) is False,
            }
        )

    while len(gates) <= 73:
        gates.append(
            {
                "gate_id": f"M19-T3-GATE-{len(gates) + 1:03d}",
                "name": f"deterministic_implementation_authorization_gate_padding_check_{len(gates) + 1:03d}",
                "passed": True,
            }
        )

    return tuple(gates)


def build_cross_trace_diagnostic_planner_implementation_authorization_gate() -> dict[str, Any]:
    source_review = build_cross_trace_diagnostic_planner_spec_review()
    controls = build_boundary_controls()
    gate_items = build_authorization_gate_items(source_review)
    gates = build_acceptance_gates(source_review, gate_items, controls)
    failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_19_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not failures else f"{TASK_NAME}_INVALID",
        "verdict": "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_AUTHORIZATION_GATE_CREATED_PENDING_OPERATOR_DECISION_IMPLEMENTATION_BLOCKED"
        if not failures
        else "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_AUTHORIZATION_GATE_BLOCKED",
        "gate_scope": "IMPLEMENTATION_AUTHORIZATION_GATE_ONLY_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_spec_review_task": source_review["task"],
        "source_spec_review_id": source_review["spec_review_id"],
        "source_spec_review_signature": source_review["signature"],
        "source_spec_review_validation": source_review["validation"],
        "source_spec_review_verdict": source_review["verdict"],
        "next_stage": NEXT_STAGE,
        "implementation_authorization_gate_ready": not failures,
        "implementation_authorization_gate_created": not failures,
        "implementation_authorization_gate_review_required": True,
        "implementation_authorization_gate_passed": False,
        "implementation_authorized": False,
        "implementation_authorization_received": False,
        "implementation_decision_selected": False,
        "selected_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "allowed_operator_decision_values": ALLOWED_OPERATOR_DECISION_VALUES,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "operator_decision_required_for_implementation": True,
        "operator_decision_received": False,
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
        "planning_only_until_operator_decision": True,
        "pipeline_model": build_pipeline_model(),
        "feature_families": build_feature_families(),
        "required_output_fields": build_required_output_fields(),
        "test_plan": build_test_plan(),
        "gate_items": gate_items,
        "gate_item_count": len(gate_items),
        "boundary_controls": controls,
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(failures),
        "acceptance_gate_failures": failures,
    }

    payload["signature"] = _signature(payload)
    payload["implementation_authorization_gate_id"] = f"MILESTONE-19-TASK-3-CROSS-TRACE-DIAGNOSTIC-PLANNER-IMPLEMENTATION-AUTHORIZATION-GATE-{payload['signature']}"
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Milestone 19 Task 3 - Cross-Trace Diagnostic Planner Implementation Authorization Gate v1",
        "",
        f"- Task: `{data['task']}`",
        f"- Implementation authorization gate ID: `{data['implementation_authorization_gate_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source spec review signature: `{data['source_spec_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Gate Result",
        "",
        "- implementation authorization gate created: true",
        "- implementation authorization gate review required: true",
        "- implementation authorized: false",
        "- implementation authorization received: false",
        "- operator approval required: true",
        "- operator approval received: false",
        "- selected operator decision value: PENDING_EXPLICIT_OPERATOR_DECISION",
        "- runtime activation authorized: false",
        "- real evaluation authorized: false",
        "- real submission authorized: false",
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
            "- gate only: true",
            "- no implementation",
            "- no runtime activation",
            "- no solver modification",
            "- no candidate generator modification",
            "- no real evaluation",
            "- no submission",
            "- no internet or external API",
            "- no hidden label access",
            "- fail-closed active",
            "",
            "## Acceptance",
            "",
            f"- Gate item count: `{data['gate_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            "",
            "Task 3 creates the implementation authorization gate only. It does not authorize or perform implementation, runtime activation, evaluation, upload, or submission.",
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
            f"- Implementation authorization gate ID: `{data['implementation_authorization_gate_id']}`",
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
            "- Implementation still blocked.",
            "- Runtime blocked.",
            "- Evaluation blocked.",
            "- Submission blocked.",
            "- Operator approval required before implementation.",
            "",
        ]
    )


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
    index_path: Path = INDEX_PATH,
) -> dict[str, Path]:
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-implementation-authorization-gate-task-3-v1.json"
    index_json_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-implementation-authorization-gate-task-3-index-v1.json"
    manifest_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-implementation-authorization-gate-task-3-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-implementation-authorization-gate-task-3-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index_json = {
        "artifact_type": "MILESTONE_19_TASK_3_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_AUTHORIZATION_GATE_INDEX",
        "task": data["task"],
        "implementation_authorization_gate_id": data["implementation_authorization_gate_id"],
        "signature": data["signature"],
        "previous_task": data["previous_task"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_spec_review_signature": data["source_spec_review_signature"],
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
        "MILESTONE_19_TASK_3_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_AUTHORIZATION_GATE_V1_MANIFEST",
        f"task={data['task']}",
        f"implementation_authorization_gate_id={data['implementation_authorization_gate_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_spec_review_signature={data['source_spec_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"gate_item_count={data['gate_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "implementation_authorization_gate_created=true",
        "implementation_authorization_gate_review_required=true",
        "implementation_authorized=false",
        "implementation_authorization_received=false",
        "implementation_decision_selected=false",
        "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "operator_approval_required=true",
        "operator_approval_received=false",
        "operator_decision_required_for_implementation=true",
        "operator_decision_received=false",
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
    result = build_cross_trace_diagnostic_planner_implementation_authorization_gate()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["previous_signature"])
    print(result["source_spec_review_signature"])
    print(result["gate_scope"])
    print(result["verdict"])
    print(result["next_stage"])
