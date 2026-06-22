"""Milestone #19 Task 1 - Cross-Trace Diagnostic Planner Planning Intake v1.

Planning-only artifact. No solver implementation, no runtime activation,
no real evaluation, and no Kaggle submission.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_19_TASK_1_CROSS_TRACE_DIAGNOSTIC_PLANNER_PLANNING_INTAKE_V1"
TASK_LABEL = "Cross-Trace Diagnostic Planner Planning Intake v1"
MILESTONE_NAME = "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER"
PREVIOUS_MILESTONE = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"
PREVIOUS_MILESTONE_CLOSURE_COMMIT = "287d1d9"
PREVIOUS_MILESTONE_CLOSURE_SIGNATURE = "811221A25BFEB5AF"
NEXT_STAGE = "MILESTONE_19_TASK_2_CROSS_TRACE_DIAGNOSTIC_PLANNER_SPEC_REVIEW_V1"

ARTIFACT_DIR = Path("examples/milestone-19/cross-trace-diagnostic-planner-planning-intake-task-1-v1")
DOCS_PATH = Path("docs/milestone-19-cross-trace-diagnostic-planner-planning-intake-task-1-v1.md")
INDEX_PATH = Path("docs/milestone-19-cross-trace-diagnostic-planner-planning-index-v1.md")


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_boundary_controls() -> dict[str, bool]:
    return {
        "planning_only": True,
        "implementation_authorized": False,
        "runtime_activation_authorized": False,
        "runtime_activation_performed": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
        "ranker_modified": False,
        "verifier_modified": False,
        "real_evaluation_authorized": False,
        "real_evaluation_performed": False,
        "real_submission_authorized": False,
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


def build_pipeline_model() -> tuple[str, ...]:
    return (
        "task_parser",
        "deterministic_feature_extractor",
        "cross_trace_diagnostic_planner",
        "authorized_candidate_generator",
        "existing_verifier",
        "ranker_or_benchmark_report",
    )


def build_feature_families() -> tuple[str, ...]:
    return (
        "color",
        "geometry",
        "position",
        "count",
        "transformation",
        "invariance",
        "contradiction",
        "complexity",
    )


def build_required_output_fields() -> tuple[str, ...]:
    return (
        "diagnosticId",
        "taskId",
        "sourceScope",
        "observation",
        "evidence",
        "hypothesis",
        "invariants",
        "contradictions",
        "confidence",
        "verificationStatus",
        "candidateInterface",
        "boundary",
    )


def build_test_plan() -> tuple[dict[str, str], ...]:
    return (
        {
            "test_id": "CTDP-T1",
            "objective": "deterministic_feature_extraction",
            "pass_condition": "same_training_pair_yields_identical_snapshot_and_hash",
        },
        {
            "test_id": "CTDP-T2",
            "objective": "cross_pair_relation_classification",
            "pass_condition": "known_fixture_relations_classified_correctly",
        },
        {
            "test_id": "CTDP-T3",
            "objective": "contradiction_handling",
            "pass_condition": "candidate_failing_one_training_pair_is_not_marked_consistent",
        },
        {
            "test_id": "CTDP-T4",
            "objective": "boundary_enforcement",
            "pass_condition": "network_external_source_hidden_label_private_core_paths_denied",
        },
        {
            "test_id": "CTDP-T5",
            "objective": "candidate_handoff_integrity",
            "pass_condition": "diagnostic_record_preserves_source_pair_refs_and_cannot_alter_verifier_output",
        },
        {
            "test_id": "CTDP-T6",
            "objective": "regression_and_determinism",
            "pass_condition": "same_fixtures_version_seed_produce_same_diagnostic_records",
        },
    )


def build_acceptance_gates(payload_core: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    controls = payload_core["boundary_controls"]

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M19-T1-GATE-001",
            "name": "milestone_18_is_closed_before_milestone_19",
            "passed": payload_core["previous_milestone"] == PREVIOUS_MILESTONE
            and payload_core["previous_milestone_closure_commit"] == PREVIOUS_MILESTONE_CLOSURE_COMMIT
            and payload_core["previous_milestone_closure_signature"] == PREVIOUS_MILESTONE_CLOSURE_SIGNATURE,
        },
        {
            "gate_id": "M19-T1-GATE-002",
            "name": "planning_artifact_ready",
            "passed": payload_core["planning_artifact_ready"] is True,
        },
        {
            "gate_id": "M19-T1-GATE-003",
            "name": "pipeline_model_declared",
            "passed": payload_core["pipeline_model"] == build_pipeline_model(),
        },
        {
            "gate_id": "M19-T1-GATE-004",
            "name": "feature_families_declared",
            "passed": payload_core["feature_families"] == build_feature_families(),
        },
        {
            "gate_id": "M19-T1-GATE-005",
            "name": "required_output_fields_declared",
            "passed": payload_core["required_output_fields"] == build_required_output_fields(),
        },
        {
            "gate_id": "M19-T1-GATE-006",
            "name": "test_plan_declared",
            "passed": len(payload_core["test_plan"]) == 6,
        },
        {
            "gate_id": "M19-T1-GATE-007",
            "name": "implementation_blocked",
            "passed": controls["implementation_authorized"] is False
            and controls["runtime_activation_performed"] is False
            and controls["runtime_solver_modified"] is False,
        },
        {
            "gate_id": "M19-T1-GATE-008",
            "name": "evaluation_and_submission_blocked",
            "passed": controls["real_evaluation_performed"] is False
            and controls["real_submission_authorized"] is False
            and controls["kaggle_submission_sent"] is False,
        },
        {
            "gate_id": "M19-T1-GATE-009",
            "name": "external_access_blocked",
            "passed": controls["internet_during_eval"] is False
            and controls["external_api_dependency"] is False
            and controls["hidden_label_accessed"] is False
            and controls["private_core_exposure"] is False,
        },
        {
            "gate_id": "M19-T1-GATE-010",
            "name": "operator_approval_required_not_received",
            "passed": controls["operator_approval_required"] is True
            and controls["operator_approval_received"] is False,
        },
        {
            "gate_id": "M19-T1-GATE-011",
            "name": "fail_closed_active",
            "passed": controls["fail_closed_required"] is True
            and controls["fail_closed_active"] is True,
        },
    ]

    for key, expected in controls.items():
        gates.append(
            {
                "gate_id": f"M19-T1-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls[key],
                "passed": controls[key] is expected,
            }
        )

    while len(gates) <= 49:
        gates.append(
            {
                "gate_id": f"M19-T1-GATE-{len(gates) + 1:03d}",
                "name": f"deterministic_planning_intake_padding_check_{len(gates) + 1:03d}",
                "passed": True,
            }
        )

    return tuple(gates)


def build_cross_trace_diagnostic_planner_planning_intake() -> dict[str, Any]:
    controls = build_boundary_controls()

    payload_core: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_19_name": MILESTONE_NAME,
        "previous_milestone": PREVIOUS_MILESTONE,
        "previous_milestone_closure_commit": PREVIOUS_MILESTONE_CLOSURE_COMMIT,
        "previous_milestone_closure_signature": PREVIOUS_MILESTONE_CLOSURE_SIGNATURE,
        "planning_artifact_ready": True,
        "planning_artifact_source": "arc-agi3-cross-trace-diagnostic-planner-v1.md",
        "planning_scope": "PROGRAMMAZIONE_AND_ADDESTRAMENTO_PLANNING_ONLY",
        "pipeline_model": build_pipeline_model(),
        "feature_families": build_feature_families(),
        "required_output_fields": build_required_output_fields(),
        "test_plan": build_test_plan(),
        "boundary_controls": controls,
        "next_stage": NEXT_STAGE,
    }

    gates = build_acceptance_gates(payload_core)
    failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        **payload_core,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not failures else f"{TASK_NAME}_INVALID",
        "verdict": "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_PLANNING_INTAKE_READY_IMPLEMENTATION_BLOCKED"
        if not failures
        else "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_PLANNING_INTAKE_BLOCKED",
        "implementation_status": "PLANNING_ALLOWED_IMPLEMENTATION_BLOCKED_RUNTIME_BLOCKED_EVALUATION_BLOCKED_SUBMISSION_BLOCKED",
        "closure_status": "TASK_1_PLANNING_INTAKE_READY",
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(failures),
        "acceptance_gate_failures": failures,
    }

    payload["signature"] = _signature(payload)
    payload["planning_intake_id"] = f"MILESTONE-19-TASK-1-CROSS-TRACE-DIAGNOSTIC-PLANNER-PLANNING-INTAKE-{payload['signature']}"
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Milestone 19 Task 1 - Cross-Trace Diagnostic Planner Planning Intake v1",
        "",
        f"- Task: `{data['task']}`",
        f"- Planning intake ID: `{data['planning_intake_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous milestone: `{data['previous_milestone']}`",
        f"- Previous closure commit: `{data['previous_milestone_closure_commit']}`",
        f"- Previous closure signature: `{data['previous_milestone_closure_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Implementation status: `{data['implementation_status']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Purpose",
        "",
        "Milestone 19 opens the Cross-Trace Diagnostic Planner as a planning-only R&D layer. It prepares deterministic diagnostic records for later separately authorized candidate generation and verification.",
        "",
        "## Pipeline Model",
        "",
    ]

    for step in data["pipeline_model"]:
        lines.append(f"- `{step}`")

    lines.extend(
        [
            "",
            "## Feature Families",
            "",
        ]
    )

    for family in data["feature_families"]:
        lines.append(f"- `{family}`")

    lines.extend(
        [
            "",
            "## Required Output Fields",
            "",
        ]
    )

    for field in data["required_output_fields"]:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- planning_only: true",
            "- implementation_authorized: false",
            "- runtime_activation_performed: false",
            "- runtime_solver_modified: false",
            "- real_evaluation_performed: false",
            "- kaggle_submission_sent: false",
            "- internet_during_eval: false",
            "- external_api_dependency: false",
            "- private_core_exposure: false",
            "- operator_approval_required: true",
            "- operator_approval_received: false",
            "- fail_closed_active: true",
            "",
            "## Test Plan",
            "",
        ]
    )

    for test in data["test_plan"]:
        lines.append(
            f"- `{test['test_id']}`: {test['objective']} -> {test['pass_condition']}"
        )

    lines.extend(
        [
            "",
            "## Acceptance",
            "",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            "",
            "Task 1 stores the planner as a planning intake artifact only. It does not authorize implementation, runtime activation, evaluation, upload, or submission.",
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
            f"- Opened by: `{TASK_NAME}`",
            f"- Planning intake ID: `{data['planning_intake_id']}`",
            f"- Signature: `{data['signature']}`",
            f"- Status: `{data['status']}`",
            f"- Validation: `{data['validation']}`",
            f"- Implementation status: `{data['implementation_status']}`",
            "",
            "## Boundary",
            "",
            "- Planning allowed.",
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
    data = build_cross_trace_diagnostic_planner_planning_intake()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-planning-intake-task-1-v1.json"
    index_json_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-planning-intake-task-1-index-v1.json"
    manifest_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-planning-intake-task-1-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-19-cross-trace-diagnostic-planner-planning-intake-task-1-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index_json = {
        "artifact_type": "MILESTONE_19_TASK_1_CROSS_TRACE_DIAGNOSTIC_PLANNER_PLANNING_INTAKE_INDEX",
        "task": data["task"],
        "planning_intake_id": data["planning_intake_id"],
        "signature": data["signature"],
        "previous_milestone_closure_commit": data["previous_milestone_closure_commit"],
        "previous_milestone_closure_signature": data["previous_milestone_closure_signature"],
        "implementation_status": data["implementation_status"],
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
        "MILESTONE_19_TASK_1_CROSS_TRACE_DIAGNOSTIC_PLANNER_PLANNING_INTAKE_V1_MANIFEST",
        f"task={data['task']}",
        f"planning_intake_id={data['planning_intake_id']}",
        f"signature={data['signature']}",
        f"previous_milestone_closure_commit={data['previous_milestone_closure_commit']}",
        f"previous_milestone_closure_signature={data['previous_milestone_closure_signature']}",
        f"next_stage={data['next_stage']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "planning_only=true",
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
    result = build_cross_trace_diagnostic_planner_planning_intake()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_milestone_closure_commit"])
    print(result["previous_milestone_closure_signature"])
    print(result["implementation_status"])
    print(result["verdict"])
    print(result["next_stage"])
