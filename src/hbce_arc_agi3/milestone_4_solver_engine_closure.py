"""Milestone #4 Solver Engine Closure Report v1.

This module closes ARC-AGI-3 Milestone #4 as a deterministic, public-safe,
local-only solver engine milestone report.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CLOSURE_STATUS = "MILESTONE_4_SOLVER_ENGINE_CLOSURE_READY"
PIPELINE_STATUS = "MILESTONE_4_SOLVER_ENGINE_CLOSURE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_4_SOLVER_ENGINE_CLOSURE_VALID"

DEFAULT_OUTPUT_DIR = "examples/closures/milestone-4"


def _stable_signature(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16].upper()


@dataclass(frozen=True)
class Milestone4TaskClosure:
    task_number: int
    title: str
    status: str
    commit: str
    artifact_hint: str
    result: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_number": self.task_number,
            "title": self.title,
            "status": self.status,
            "commit": self.commit,
            "artifact_hint": self.artifact_hint,
            "result": self.result,
        }


@dataclass(frozen=True)
class Milestone4SolverEngineClosure:
    status: str
    closure_id: str
    signature: str
    milestone: str
    title: str
    closed_task_count: int
    tasks: Tuple[Milestone4TaskClosure, ...]
    planning_commits: Tuple[str, ...]
    final_commit: str
    final_test_count_before_closure: int
    final_test_status: str
    ready_for_next_phase: bool
    kaggle_submission_sent: bool
    solver_engine_result: Dict[str, Any]
    boundary: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "closure_id": self.closure_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "title": self.title,
            "closed_task_count": self.closed_task_count,
            "tasks": [task.to_dict() for task in self.tasks],
            "planning_commits": list(self.planning_commits),
            "final_commit": self.final_commit,
            "final_test_count_before_closure": self.final_test_count_before_closure,
            "final_test_status": self.final_test_status,
            "ready_for_next_phase": self.ready_for_next_phase,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "solver_engine_result": copy.deepcopy(self.solver_engine_result),
            "boundary": copy.deepcopy(self.boundary),
            "metadata": copy.deepcopy(self.metadata),
        }


def build_milestone_4_tasks() -> Tuple[Milestone4TaskClosure, ...]:
    return (
        Milestone4TaskClosure(
            task_number=1,
            title="Strategy Interface v2",
            status="CLOSED_PASS",
            commit="e08f204",
            artifact_hint="milestone-4 strategy interface",
            result="Milestone #4 solver strategy interface established.",
        ),
        Milestone4TaskClosure(
            task_number=2,
            title="Grid Object Extractor v1",
            status="CLOSED_PASS",
            commit="ea7ef2b",
            artifact_hint="grid object extraction artifacts",
            result="Grid object structure extraction available for downstream solvers.",
        ),
        Milestone4TaskClosure(
            task_number=3,
            title="Color Transform Detector v1",
            status="CLOSED_PASS",
            commit="cf897c1",
            artifact_hint="color transform detector artifacts",
            result="Stable color remap and palette signals detected deterministically.",
        ),
        Milestone4TaskClosure(
            task_number=4,
            title="Shape / Symmetry Detector v1",
            status="CLOSED_PASS",
            commit="c7b203d",
            artifact_hint="shape symmetry detector artifacts",
            result="Shape, symmetry and transform evidence connected to candidate generation.",
        ),
        Milestone4TaskClosure(
            task_number=5,
            title="Candidate Generator v1",
            status="CLOSED_PASS",
            commit="308f4ad",
            artifact_hint="candidate generator artifacts",
            result="Deterministic candidate grids generated from color and shape evidence.",
        ),
        Milestone4TaskClosure(
            task_number=6,
            title="Candidate Ranker v1",
            status="CLOSED_PASS",
            commit="fa03713",
            artifact_hint="candidate ranker artifacts",
            result="Candidate scoring and deterministic ranking pipeline established.",
        ),
        Milestone4TaskClosure(
            task_number=7,
            title="Expanded Batch Benchmark v2",
            status="CLOSED_PASS",
            commit="5f6be77",
            artifact_hint="examples/milestone-4/expanded-batch-benchmark-v2",
            result="Batch benchmark coverage expanded and measurable.",
        ),
        Milestone4TaskClosure(
            task_number=8,
            title="Failure-Driven Solver Improvement Loop v1",
            status="CLOSED_PASS",
            commit="9d9db93",
            artifact_hint="examples/milestone-4/failure-driven-improvement-loop-v1",
            result="Failure loop isolated solver improvement targets.",
        ),
        Milestone4TaskClosure(
            task_number=9,
            title="Candidate Ranker Task-Family Policy Fix v1",
            status="CLOSED_PASS",
            commit="4fbae99",
            artifact_hint="examples/milestone-4/candidate-ranker-task-family-policy-fix-v1",
            result="Color-only task fixed: COLOR_REMAP selected and benchmark match rate reached 1.0.",
        ),
    )


def build_milestone_4_solver_engine_closure() -> Milestone4SolverEngineClosure:
    tasks = build_milestone_4_tasks()

    boundary = {
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    solver_engine_result = {
        "expanded_best_candidate_match_rate": 1.0,
        "failure_loop_improvement_item_count": 0,
        "failure_loop_next_solver_target": "none",
        "final_color_only_best_candidate": "COLOR_REMAP",
        "final_color_only_match": True,
        "ready_for_phase_next": True,
    }

    base_payload = {
        "status": CLOSURE_STATUS,
        "milestone": "Milestone #4",
        "title": "Solver Engine Milestone Closure Report v1",
        "closed_task_count": len(tasks),
        "tasks": [task.to_dict() for task in tasks],
        "planning_commits": [
            "efa5f86 Open ARC AGI3 milestone 4 solver engine plan",
            "b0c200f Add prize and deadline targets to ARC AGI3 milestone 4",
        ],
        "final_commit": "4fbae99 Add ARC AGI3 candidate ranker task family policy fix",
        "final_test_count_before_closure": 337,
        "final_test_status": "PASS",
        "ready_for_next_phase": True,
        "kaggle_submission_sent": False,
        "solver_engine_result": solver_engine_result,
        "boundary": boundary,
        "metadata": {
            "source": "milestone_4_solver_engine_closure_v1",
            "milestone": "Milestone #4",
            "task": "Task 10",
            "closure_kind": "SOLVER_ENGINE_MILESTONE_CLOSURE",
            "score_oriented": True,
            "phase_next_ready": True,
        },
    }

    signature = _stable_signature(base_payload)
    closure_id = f"MILESTONE-4-SOLVER-CLOSURE-{signature[:12]}"

    return Milestone4SolverEngineClosure(
        status=CLOSURE_STATUS,
        closure_id=closure_id,
        signature=signature,
        milestone=base_payload["milestone"],
        title=base_payload["title"],
        closed_task_count=base_payload["closed_task_count"],
        tasks=tasks,
        planning_commits=tuple(base_payload["planning_commits"]),
        final_commit=base_payload["final_commit"],
        final_test_count_before_closure=base_payload["final_test_count_before_closure"],
        final_test_status=base_payload["final_test_status"],
        ready_for_next_phase=True,
        kaggle_submission_sent=False,
        solver_engine_result=solver_engine_result,
        boundary=boundary,
        metadata=base_payload["metadata"],
    )


def validate_milestone_4_solver_engine_closure(
    closure: Milestone4SolverEngineClosure | Mapping[str, Any],
) -> Dict[str, Any]:
    data = closure.to_dict() if hasattr(closure, "to_dict") else dict(closure)

    tasks = data.get("tasks") if isinstance(data.get("tasks"), list) else []
    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    solver = data.get("solver_engine_result") if isinstance(data.get("solver_engine_result"), Mapping) else {}

    checks = {
        "status_ready": data.get("status") == CLOSURE_STATUS,
        "closure_id_present": isinstance(data.get("closure_id"), str) and bool(data.get("closure_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "closed_task_count_is_9": data.get("closed_task_count") == 9,
        "tasks_len_is_9": len(tasks) == 9,
        "all_tasks_closed_pass": bool(tasks) and all(task.get("status") == "CLOSED_PASS" for task in tasks),
        "final_test_count_recorded": data.get("final_test_count_before_closure") == 337,
        "final_test_status_pass": data.get("final_test_status") == "PASS",
        "ready_for_next_phase": data.get("ready_for_next_phase") is True,
        "kaggle_submission_not_sent": data.get("kaggle_submission_sent") is False,
        "expanded_match_rate_fixed": solver.get("expanded_best_candidate_match_rate") == 1.0,
        "failure_loop_closed": solver.get("failure_loop_improvement_item_count") == 0,
        "next_solver_target_none": solver.get("failure_loop_next_solver_target") == "none",
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(checks.values())

    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_4_SOLVER_ENGINE_CLOSURE_INVALID",
        "valid": valid,
        "checks": checks,
        "closure_id": data.get("closure_id"),
        "signature": data.get("signature"),
    }


def render_milestone_4_solver_engine_closure_markdown(
    closure: Milestone4SolverEngineClosure | Mapping[str, Any],
) -> str:
    data = closure.to_dict() if hasattr(closure, "to_dict") else dict(closure)

    lines = [
        "# ARC AGI3 Milestone #4 - Solver Engine Closure Report v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- closure_id: {data['closure_id']}",
        f"- signature: {data['signature']}",
        f"- closed_task_count: {data['closed_task_count']}",
        f"- final_test_count_before_closure: {data['final_test_count_before_closure']}",
        f"- final_test_status: {data['final_test_status']}",
        f"- ready_for_next_phase: {data['ready_for_next_phase']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Closed Tasks",
        "",
    ]

    for task in data["tasks"]:
        lines.append(
            f"{task['task_number']}. {task['title']} - {task['status']} - {task['commit']}"
        )

    lines.extend(
        [
            "",
            "## Solver Engine Result",
            "",
            f"- expanded_best_candidate_match_rate: {data['solver_engine_result']['expanded_best_candidate_match_rate']}",
            f"- failure_loop_improvement_item_count: {data['solver_engine_result']['failure_loop_improvement_item_count']}",
            f"- failure_loop_next_solver_target: {data['solver_engine_result']['failure_loop_next_solver_target']}",
            f"- final_color_only_best_candidate: {data['solver_engine_result']['final_color_only_best_candidate']}",
            f"- final_color_only_match: {data['solver_engine_result']['final_color_only_match']}",
            "",
            "## Boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- local_only=true",
            "- dry_run_only=true",
            "- external_api_dependency=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "- legal_certification=false",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_4_SOLVER_ENGINE_CLOSURE_V1_READY=true",
            "ARC_AGI3_MILESTONE_4_CLOSURE_STATUS=MILESTONE_4_SOLVER_ENGINE_CLOSURE_READY",
            "ARC_AGI3_MILESTONE_4_CLOSURE_VALIDATION=MILESTONE_4_SOLVER_ENGINE_CLOSURE_VALID",
            "ARC_AGI3_MILESTONE_4_TASKS_CLOSED=9",
            "ARC_AGI3_MILESTONE_4_FINAL_TESTS_PASS=337",
            "ARC_AGI3_MILESTONE_4_EXPANDED_BATCH_MATCH_RATE=1.0",
            "ARC_AGI3_MILESTONE_4_FAILURE_LOOP_CLOSED=true",
            "ARC_AGI3_MILESTONE_4_READY_FOR_NEXT_PHASE=true",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_milestone_4_solver_engine_closure_artifacts(
    closure: Milestone4SolverEngineClosure | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    closure = closure or build_milestone_4_solver_engine_closure()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "milestone-4-solver-engine-closure.json"
    markdown_path = output_path / "milestone-4-solver-engine-closure.md"

    json_path.write_text(json.dumps(closure.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_milestone_4_solver_engine_closure_markdown(closure), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }


def run_milestone_4_solver_engine_closure_pipeline() -> Dict[str, Any]:
    closure = build_milestone_4_solver_engine_closure()
    validation = validate_milestone_4_solver_engine_closure(closure)
    artifacts = write_milestone_4_solver_engine_closure_artifacts(closure)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_4_SOLVER_ENGINE_CLOSURE_PIPELINE_INVALID",
        "closure_status": closure.status,
        "validation_status": validation["status"],
        "closure": closure.to_dict(),
        "closure_id": closure.closure_id,
        "signature": closure.signature,
        "closed_task_count": closure.closed_task_count,
        "final_test_count_before_closure": closure.final_test_count_before_closure,
        "ready_for_next_phase": closure.ready_for_next_phase,
        "kaggle_submission_sent": closure.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_4_solver_engine_closure_pipeline_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }
