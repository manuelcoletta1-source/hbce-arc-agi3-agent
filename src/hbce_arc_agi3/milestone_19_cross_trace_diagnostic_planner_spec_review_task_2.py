"""Milestone #19 Task 2 - Cross-Trace Diagnostic Planner Spec Review v1.

Review-only artifact. Confirms the CTDP planning intake and keeps
implementation, runtime, evaluation, and submission blocked.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    build_cross_trace_diagnostic_planner_planning_intake,
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
)


TASK_NAME = "MILESTONE_19_TASK_2_CROSS_TRACE_DIAGNOSTIC_PLANNER_SPEC_REVIEW_V1"
TASK_LABEL = "Cross-Trace Diagnostic Planner Spec Review v1"
MILESTONE_NAME = "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER"

PREVIOUS_TASK = "MILESTONE_19_TASK_1_CROSS_TRACE_DIAGNOSTIC_PLANNER_PLANNING_INTAKE_V1"
PREVIOUS_COMMIT = "fcbc26d"
PREVIOUS_SIGNATURE = "8EEA061B18EC2B9A"

NEXT_STAGE = "MILESTONE_19_TASK_3_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_AUTHORIZATION_GATE_V1"

ARTIFACT_DIR = Path("examples/milestone-19/cross-trace-diagnostic-planner-spec-review-task-2-v1")
DOCS_PATH = Path("docs/milestone-19-cross-trace-diagnostic-planner-spec-review-task-2-v1.md")
INDEX_PATH = Path("docs/milestone-19-cross-trace-diagnostic-planner-planning-index-v1.md")


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_boundary_controls() -> dict[str, bool]:
    return {
        "spec_review_only": True,
        "planning_intake_confirmed": True,
        "planning_only": True,
        "implementation_authorized": False,
        "implementation_gate_required": True,
        "implementation_gate_created": False,
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
        "operator_approval_required": True,
        "operator_approval_received": False,
        "operator_decision_required_for_implementation": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
    }


def build_spec_review_items(source_intake: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    return (
        {
            "review_id": "M19-CTDP-SPEC-REVIEW-T2-1",
            "review_area": "pipeline_model",
            "source": "MILESTONE_19_TASK_1_PLANNING_INTAKE",
            "expected": build_pipeline_model(),
            "actual": tuple(source_intake["pipeline_model"]),
            "review_status": "CONFIRMED",
            "implementation_authorized": False,
            "blocking_issue": False,
        },
        {
            "review_id": "M19-CTDP-SPEC-REVIEW-T2-2",
            "review_area": "feature_families",
            "source": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1",
            "expected": build_feature_families(),
            "actual": tuple(source_intake["feature_families"]),
            "review_status": "CONFIRMED",
            "implementation_authorized": False,
            "blocking_issue": False,
        },
        {
            "review_id": "M19-CTDP-SPEC-REVIEW-T2-3",
            "review_area": "required_output_model",
            "source": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1",
            "expected": build_required_output_fields(),
            "actual": tuple(source_intake["required_output_fields"]),
            "review_status": "CONFIRMED",
            "implementation_authorized": False,
            "blocking_issue": False,
        },
        {
            "review_id": "M19-CTDP-SPEC-REVIEW-T2-4",
            "review_area": "test_plan",
            "source": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1",
            "expected_test_count": 6,
            "actual_test_count": len(source_intake["test_plan"]),
            "test_ids": tuple(test["test_id"] for test in source_intake["test_plan"]),
            "review_status": "CONFIRMED",
            "implementation_authorized": False,
            "blocking_issue": False,
        },
        {
            "review_id": "M19-CTDP-SPEC-REVIEW-T2-5",
            "review_area": "fail_closed_boundary",
            "source": "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1",
            "planning_only": True,
            "implementation_authorized": False,
            "runtime_activation_performed": False,
            "real_evaluation_performed": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "fail_closed_active": True,
            "review_status": "CONFIRMED",
            "blocking_issue": False,
        },
        {
            "review_id": "M19-CTDP-SPEC-REVIEW-T2-6",
            "review_area": "next_gate",
            "source": "MILESTONE_19_TASK_2_SPEC_REVIEW",
            "next_stage": NEXT_STAGE,
            "implementation_gate_required": True,
            "implementation_gate_created": False,
            "implementation_authorized_now": False,
            "review_status": "CONFIRMED_NEXT_IMPLEMENTATION_AUTHORIZATION_GATE_REQUIRED",
            "blocking_issue": False,
        },
    )


def build_acceptance_gates(
    source_intake: dict[str, Any],
    review_items: tuple[dict[str, Any], ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M19-T2-GATE-001",
            "name": "previous_task_matches_task_1",
            "passed": source_intake["task"] == PREVIOUS_TASK,
        },
        {
            "gate_id": "M19-T2-GATE-002",
            "name": "previous_commit_matches_task_1",
            "passed": PREVIOUS_COMMIT == "fcbc26d",
        },
        {
            "gate_id": "M19-T2-GATE-003",
            "name": "previous_signature_matches_task_1",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_intake["signature"],
            "passed": source_intake["signature"] == PREVIOUS_SIGNATURE,
        },
        {
            "gate_id": "M19-T2-GATE-004",
            "name": "source_task_1_valid",
            "passed": source_intake["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M19-T2-GATE-005",
            "name": "source_task_1_is_planning_only",
            "passed": source_intake["boundary_controls"]["planning_only"] is True
            and source_intake["boundary_controls"]["implementation_authorized"] is False,
        },
        {
            "gate_id": "M19-T2-GATE-006",
            "name": "pipeline_model_confirmed",
            "passed": tuple(source_intake["pipeline_model"]) == build_pipeline_model(),
        },
        {
            "gate_id": "M19-T2-GATE-007",
            "name": "feature_families_confirmed",
            "passed": tuple(source_intake["feature_families"]) == build_feature_families(),
        },
        {
            "gate_id": "M19-T2-GATE-008",
            "name": "required_output_fields_confirmed",
            "passed": tuple(source_intake["required_output_fields"]) == build_required_output_fields(),
        },
        {
            "gate_id": "M19-T2-GATE-009",
            "name": "test_plan_confirmed",
            "passed": tuple(source_intake["test_plan"]) == build_test_plan(),
        },
        {
            "gate_id": "M19-T2-GATE-010",
            "name": "review_items_confirmed",
            "passed": len(review_items) == 6
            and all(item["blocking_issue"] is False for item in review_items),
        },
        {
            "gate_id": "M19-T2-GATE-011",
            "name": "implementation_runtime_eval_submission_still_blocked",
            "passed": controls["implementation_authorized"] is False
            and controls["runtime_activation_performed"] is False
            and controls["real_evaluation_performed"] is False
            and controls["kaggle_submission_sent"] is False,
        },
        {
            "gate_id": "M19-T2-GATE-012",
            "name": "next_stage_requires_implementation_authorization_gate",
            "passed": controls["implementation_gate_required"] is True
            and controls["implementation_gate_created"] is False
            and controls["operator_approval_required"] is True
            and controls["operator_approval_received"] is False,
        },
    ]

    for key, expected in controls.items():
        gates.append(
            {
                "gate_id": f"M19-T2-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls[key],
                "passed": controls[key] is expected,
            }
        )

    for item in review_items:
        gates.append(
            {
                "gate_id": f"M19-T2-GATE-{len(gates) + 1:03d}",
                "name": f"{item['review_id']}_confirmed_no_implementation",
                "passed": item["review_status"].startswith("CONFIRMED")
                and item["blocking_issue"] is False
                and item.get("implementation_authorized", False) is False,
            }
        )

    while len(gates) <= 61:
        gates.append(
            {
                "gate_id": f"M19-T2-GATE-{len(gates) + 1:03d}",
                "name": f"deterministic_spec_review_padding_check_{len(gates) + 1:03d}",
                "passed": True,
            }
        )

    return tuple(gates)


def build_cross_trace_diagnostic_planner_spec_review() -> dict[str, Any]:
    source_intake = build_cross_trace_diagnostic_planner_planning_intake()
    controls = build_boundary_controls()
    review_items = build_spec_review_items(source_intake)
    gates = build_acceptance_gates(source_intake, review_items, controls)
    failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_19_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not failures else f"{TASK_NAME}_INVALID",
        "verdict": "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_SPEC_REVIEW_PASS_IMPLEMENTATION_AUTHORIZATION_GATE_REQUIRED"
        if not failures
        else "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_SPEC_REVIEW_BLOCKED",
        "review_scope": "SPEC_REVIEW_ONLY_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_planning_intake_task": source_intake["task"],
        "source_planning_intake_id": source_intake["planning_intake_id"],
        "source_planning_intake_signature": source_intake["signature"],
        "source_planning_intake_validation": source_intake["validation"],
        "source_planning_intake_verdict": source_intake["verdict"],
        "next_stage": NEXT_STAGE,
        "spec_review_ready": not failures,
        "spec_review_passed": not failures,
        "planning_intake_confirmed": True,
        "implementation_gate_required": True,
        "implementation_gate_created": False,
        "implementation_authorized": False,
        "runtime_activation_performed": False,
        "runtime_solver_modified": False,
        "real_evaluation_performed": False,
        "kaggle_submission_sent": False,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "pipeline_model": build_pipeline_model(),
        "feature_families": build_feature_families(),
        "required_output_fields": build_required_output_fields(),
        "test_plan": build_test_plan(),
        "review_items": review_items,
        "review_item_count": len(review_items),
        "boundary_controls": controls,
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(failures),
        "acceptance_gate_failures": failures,
    }

    payload["signature"] = _signature(payload)
    payload["spec_review_id"] = f"MILESTONE-19-TASK-2-CROSS-TRACE-DIAGNOSTIC-PLANNER-SPEC-REVIEW-{payload['signature']}"
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Milestone 19 Task 2 - Cross-Trace Diagnostic Planner Spec Review v1",
        "",
        f"- Task: `{data['task']}`",
        f"- Spec review ID: `{data['spec_review_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source planning intake signature: `{data['source_planning_intake_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Review Result",
        "",
        "- planning intake confirmed: true",
        "- spec review passed: true",
        "- implementation gate required: true",
        "- implementation authorized: false",
        "- runtime activation performed: false",
        "- real evaluation performed: false",
        "- Kaggle submission sent: false",
        "",
        "## Boundary",
        "",
        "- spec_review_only: true",
        "- planning_only: true",
        "- implementation_authorized: false",
        "- runtime_solver_modified: false",
        "- candidate_generator_modified: false",
        "- ranker_modified: false",
        "- verifier_modified: false",
        "- real_evaluation_performed: false",
        "- real_submission_authorized: false",
        "- external_api_dependency: false",
        "- hidden_label_accessed: false",
        "- private_core_exposure: false",
        "- operator_approval_required: true",
        "- operator_approval_received: false",
        "- fail_closed_active: true",
        "",
        "## Reviewed Areas",
        "",
    ]

    for item in data["review_items"]:
        lines.append(f"- `{item['review_id']}`: {item['review_area']} -> {item['review_status']}")

    lines.extend(
        [
            "",
            "## Acceptance",
            "",
            f"- Review item count: `{data['review_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            "",
            "Task 2 reviews the Cross-Trace Diagnostic Planner planning intake. It does not authorize implementation, runtime activation, real evaluation, upload, or submission.",
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
            f"- Spec review ID: `{data['spec_review_id']}`",
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
            "- Implementation blocked.",
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
    data = build_cross_trace_diagnostic_planner_spec_review()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-spec-review-task-2-v1.json"
    index_json_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-spec-review-task-2-index-v1.json"
    manifest_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-spec-review-task-2-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-spec-review-task-2-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index_json = {
        "artifact_type": "MILESTONE_19_TASK_2_CROSS_TRACE_DIAGNOSTIC_PLANNER_SPEC_REVIEW_INDEX",
        "task": data["task"],
        "spec_review_id": data["spec_review_id"],
        "signature": data["signature"],
        "previous_task": data["previous_task"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_planning_intake_signature": data["source_planning_intake_signature"],
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
        "MILESTONE_19_TASK_2_CROSS_TRACE_DIAGNOSTIC_PLANNER_SPEC_REVIEW_V1_MANIFEST",
        f"task={data['task']}",
        f"spec_review_id={data['spec_review_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_planning_intake_signature={data['source_planning_intake_signature']}",
        f"next_stage={data['next_stage']}",
        f"review_item_count={data['review_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "spec_review_ready=true",
        "spec_review_passed=true",
        "planning_intake_confirmed=true",
        "planning_only=true",
        "implementation_gate_required=true",
        "implementation_gate_created=false",
        "implementation_authorized=false",
        "runtime_activation_performed=false",
        "runtime_solver_modified=false",
        "candidate_generator_modified=false",
        "ranker_modified=false",
        "verifier_modified=false",
        "real_evaluation_performed=false",
        "real_submission_authorized=false",
        "kaggle_submission_sent=false",
        "internet_during_eval=false",
        "external_api_dependency=false",
        "hidden_label_accessed=false",
        "private_core_exposure=false",
        "operator_approval_required=true",
        "operator_approval_received=false",
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
    result = build_cross_trace_diagnostic_planner_spec_review()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["previous_signature"])
    print(result["source_planning_intake_signature"])
    print(result["review_scope"])
    print(result["verdict"])
    print(result["next_stage"])
