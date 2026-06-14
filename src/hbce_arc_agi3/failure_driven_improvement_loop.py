"""Failure-Driven Solver Improvement Loop v1 for ARC-AGI-3 Milestone #4 Task 8.

This module reads the Expanded Batch Benchmark v2 output and converts non-matching
task results into prioritized solver improvement recommendations.

Boundary:
public_safe=true
deterministic=true
local_only=true
dry_run_only=true
external_api_dependency=false
kaggle_submission_sent=false
private_core_exposure=false
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple


DEFAULT_BENCHMARK_PATH = "examples/milestone-4/expanded-batch-benchmark-v2/expanded-batch-benchmark-v2-smoke.json"


def _stable_signature(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16].upper()


@dataclass(frozen=True)
class SolverImprovementItem:
    task_id: str
    task_family: str
    failure_type: str
    observed_best_candidate: str
    observed_best_score: float
    expected_best_available: bool
    expected_match: bool
    improvement_target_module: str
    recommended_next_action: str
    priority: str
    rationale: str
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FailureDrivenImprovementReport:
    status: str
    improvement_loop_id: str
    source_benchmark_id: str
    source_benchmark_signature: str
    task_count: int
    analyzed_task_count: int
    matching_task_count: int
    failing_task_count: int
    improvement_item_count: int
    highest_priority: str
    improvement_items: Tuple[SolverImprovementItem, ...]
    next_solver_target: str
    item_signatures: Tuple[str, ...]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_expanded_batch_benchmark_payload(path: str = DEFAULT_BENCHMARK_PATH) -> Dict[str, Any]:
    payload_path = Path(path)
    if not payload_path.exists():
        raise FileNotFoundError(f"Benchmark payload not found: {path}")
    return json.loads(payload_path.read_text(encoding="utf-8"))


def classify_failure(task_result: Mapping[str, Any]) -> Dict[str, str]:
    task_family = str(task_result.get("task_family", "unknown"))
    best_candidate_type = str(task_result.get("best_candidate_type", "unknown"))
    expected_available = bool(task_result.get("expected_best_available"))
    expected_match = bool(task_result.get("best_candidate_matches_expected"))

    if expected_match:
        return {
            "failure_type": "NONE",
            "target_module": "none",
            "recommended_next_action": "No action required.",
            "priority": "NONE",
            "rationale": "The best ranked candidate matches the expected output.",
        }

    if not expected_available:
        return {
            "failure_type": "NO_EXPECTED_OUTPUT_AVAILABLE",
            "target_module": "expanded_batch_benchmark.py",
            "recommended_next_action": "Add expected output for this benchmark task before scoring solver quality.",
            "priority": "LOW",
            "rationale": "The benchmark cannot verify correctness without an expected best grid.",
        }

    if task_family == "color_transform" and best_candidate_type == "COLOR_SHAPE_COMBINED":
        return {
            "failure_type": "COLOR_ONLY_TASK_OVERRANKED_BY_COMBINED_CANDIDATE",
            "target_module": "candidate_ranker.py",
            "recommended_next_action": "Add ranker policy that penalizes COLOR_SHAPE_COMBINED on pure color_transform tasks when a simpler COLOR_REMAP candidate exists.",
            "priority": "HIGH",
            "rationale": "The benchmark indicates that the solver over-prefers a combined candidate even when the task family is pure color transformation.",
        }

    if task_family == "identity_baseline" and best_candidate_type != "IDENTITY":
        return {
            "failure_type": "IDENTITY_TASK_OVERRANKED_BY_NON_IDENTITY_CANDIDATE",
            "target_module": "candidate_ranker.py",
            "recommended_next_action": "Increase identity candidate weight on identity_baseline tasks or add task-family-aware ranking.",
            "priority": "MEDIUM",
            "rationale": "Identity tasks should prefer identity candidates when expected output matches input.",
        }

    return {
        "failure_type": "GENERIC_EXPECTED_MISMATCH",
        "target_module": "candidate_ranker.py",
        "recommended_next_action": "Inspect candidate ranking features and add task-family-aware scoring for this failure class.",
        "priority": "MEDIUM",
        "rationale": "The best ranked candidate did not match expected output.",
    }


def build_improvement_item(task_result: Mapping[str, Any]) -> Optional[SolverImprovementItem]:
    expected_match = bool(task_result.get("best_candidate_matches_expected"))
    if expected_match:
        return None

    classification = classify_failure(task_result)

    payload = {
        "task_id": str(task_result.get("task_id", "UNKNOWN_TASK")),
        "task_family": str(task_result.get("task_family", "unknown")),
        "failure_type": classification["failure_type"],
        "observed_best_candidate": str(task_result.get("best_candidate_type", "unknown")),
        "observed_best_score": float(task_result.get("best_candidate_score", 0.0)),
        "expected_best_available": bool(task_result.get("expected_best_available")),
        "expected_match": expected_match,
        "improvement_target_module": classification["target_module"],
        "recommended_next_action": classification["recommended_next_action"],
        "priority": classification["priority"],
        "rationale": classification["rationale"],
        "metadata": {
            "source": "failure_driven_improvement_loop_v1",
            "public_safe": True,
            "local_only": True,
            "dry_run_only": True,
        },
    }

    return SolverImprovementItem(
        **payload,
        signature=_stable_signature(payload),
    )


def run_failure_driven_improvement_loop(
    benchmark_payload: Optional[Mapping[str, Any]] = None,
    *,
    benchmark_path: str = DEFAULT_BENCHMARK_PATH,
) -> FailureDrivenImprovementReport:
    payload = dict(benchmark_payload) if benchmark_payload is not None else load_expanded_batch_benchmark_payload(benchmark_path)

    benchmark_report = dict(payload.get("benchmark_report", {}))
    task_results = list(benchmark_report.get("task_results", []))

    improvement_items = []
    matching_task_count = 0

    for task_result in task_results:
        if bool(task_result.get("best_candidate_matches_expected")):
            matching_task_count += 1
            continue

        item = build_improvement_item(task_result)
        if item is not None:
            improvement_items.append(item)

    priority_rank = {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
        "NONE": 0,
    }

    highest_priority = "NONE"
    for item in improvement_items:
        if priority_rank[item.priority] > priority_rank[highest_priority]:
            highest_priority = item.priority

    next_solver_target = (
        improvement_items[0].improvement_target_module
        if improvement_items
        else "none"
    )

    report_payload = {
        "status": "FAILURE_DRIVEN_IMPROVEMENT_LOOP_READY",
        "source_benchmark_id": str(payload.get("benchmark_id", benchmark_report.get("benchmark_id", "UNKNOWN_BENCHMARK"))),
        "source_benchmark_signature": str(payload.get("signature", benchmark_report.get("signature", "UNKNOWN_SIGNATURE"))),
        "task_count": int(payload.get("task_count", benchmark_report.get("task_count", len(task_results)))),
        "analyzed_task_count": len(task_results),
        "matching_task_count": matching_task_count,
        "failing_task_count": len(task_results) - matching_task_count,
        "improvement_item_count": len(improvement_items),
        "highest_priority": highest_priority,
        "next_solver_target": next_solver_target,
        "item_signatures": tuple(item.signature for item in improvement_items),
        "metadata": {
            "source": "failure_driven_improvement_loop_v1",
            "milestone": "Milestone #4",
            "task": "Task 8",
            "uses_expanded_batch_benchmark_v2": True,
            "failure_driven_solver_improvement": True,
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }

    signature = _stable_signature(report_payload)
    improvement_loop_id = f"FAILURE-DRIVEN-LOOP-{signature[:12]}"

    return FailureDrivenImprovementReport(
        improvement_loop_id=improvement_loop_id,
        signature=signature,
        improvement_items=tuple(improvement_items),
        **report_payload,
    )


def validate_failure_driven_improvement_report(
    report: FailureDrivenImprovementReport | Mapping[str, Any],
) -> Dict[str, Any]:
    data = report.to_dict() if isinstance(report, FailureDrivenImprovementReport) else dict(report)
    errors: List[str] = []

    if data.get("status") != "FAILURE_DRIVEN_IMPROVEMENT_LOOP_READY":
        errors.append("status must be FAILURE_DRIVEN_IMPROVEMENT_LOOP_READY")

    if int(data.get("analyzed_task_count", 0)) <= 0:
        errors.append("analyzed_task_count must be positive")

    if int(data.get("improvement_item_count", 0)) < 0:
        errors.append("improvement_item_count must not be negative")

    if data.get("highest_priority") not in {"HIGH", "MEDIUM", "LOW", "NONE"}:
        errors.append("highest_priority must be HIGH, MEDIUM, LOW or NONE")

    metadata = dict(data.get("metadata", {}))

    for key in [
        "uses_expanded_batch_benchmark_v2",
        "failure_driven_solver_improvement",
        "public_safe",
        "deterministic",
        "local_only",
        "dry_run_only",
        "score_oriented",
        "prize_oriented_solver_target",
    ]:
        if metadata.get(key) is not True:
            errors.append(f"metadata.{key} must be true")

    for key in [
        "external_api_dependency",
        "contains_api_keys",
        "kaggle_submission_sent",
        "private_core_exposure",
        "legal_certification",
    ]:
        if metadata.get(key) is not False:
            errors.append(f"metadata.{key} must be false")

    validation_status = (
        "FAILURE_DRIVEN_IMPROVEMENT_LOOP_VALID"
        if not errors
        else "FAILURE_DRIVEN_IMPROVEMENT_LOOP_INVALID"
    )

    return {
        "status": validation_status,
        "valid": not errors,
        "errors": errors,
        "improvement_loop_id": data.get("improvement_loop_id"),
        "source_benchmark_id": data.get("source_benchmark_id"),
        "improvement_item_count": data.get("improvement_item_count"),
        "highest_priority": data.get("highest_priority"),
        "next_solver_target": data.get("next_solver_target"),
        "signature": data.get("signature"),
    }


def render_failure_driven_improvement_markdown(payload: Mapping[str, Any]) -> str:
    report = dict(payload["improvement_report"])
    validation = dict(payload["validation"])

    lines = [
        "# ARC AGI3 Milestone #4 Task 8 - Failure-Driven Solver Improvement Loop v1",
        "",
        "## Status",
        "",
        f"- status: {payload['status']}",
        f"- validation: {validation['status']}",
        f"- improvement_loop_id: {report['improvement_loop_id']}",
        f"- source_benchmark_id: {report['source_benchmark_id']}",
        f"- signature: {report['signature']}",
        "",
        "## Metrics",
        "",
        f"- analyzed_task_count: {report['analyzed_task_count']}",
        f"- matching_task_count: {report['matching_task_count']}",
        f"- failing_task_count: {report['failing_task_count']}",
        f"- improvement_item_count: {report['improvement_item_count']}",
        f"- highest_priority: {report['highest_priority']}",
        f"- next_solver_target: {report['next_solver_target']}",
        "",
        "## Improvement items",
        "",
        "| task_id | failure_type | target_module | priority | observed_best_candidate |",
        "|---|---|---|---|---|",
    ]

    for item in report["improvement_items"]:
        lines.append(
            "| {task_id} | {failure_type} | {improvement_target_module} | {priority} | {observed_best_candidate} |".format(
                **item
            )
        )

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "public_safe=true",
            "deterministic=true",
            "local_only=true",
            "dry_run_only=true",
            "external_api_dependency=false",
            "contains_api_keys=false",
            "kaggle_submission_sent=false",
            "private_core_exposure=false",
            "legal_certification=false",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_4_TASK_8_FAILURE_DRIVEN_IMPROVEMENT_LOOP_V1_READY=true",
            "ARC_AGI3_MILESTONE_4_TASK_8_STATUS=FAILURE_DRIVEN_IMPROVEMENT_LOOP_READY",
            "ARC_AGI3_MILESTONE_4_TASK_8_VALIDATION=FAILURE_DRIVEN_IMPROVEMENT_LOOP_VALID",
            "ARC_AGI3_MILESTONE_4_TASK_8_USES_EXPANDED_BATCH_BENCHMARK_V2=true",
            "ARC_AGI3_MILESTONE_4_TASK_8_FAILURE_CLASSIFICATION_READY=true",
            "ARC_AGI3_MILESTONE_4_TASK_8_NEXT_SOLVER_TARGET_READY=true",
            "ARC_AGI3_MILESTONE_4_TASK_8_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def run_failure_driven_improvement_pipeline() -> Dict[str, Any]:
    report = run_failure_driven_improvement_loop()
    validation = validate_failure_driven_improvement_report(report)

    status = (
        "FAILURE_DRIVEN_IMPROVEMENT_PIPELINE_READY"
        if validation["valid"]
        else "FAILURE_DRIVEN_IMPROVEMENT_PIPELINE_INVALID"
    )

    return {
        "status": status,
        "report_status": report.status,
        "validation_status": validation["status"],
        "improvement_loop_id": report.improvement_loop_id,
        "source_benchmark_id": report.source_benchmark_id,
        "analyzed_task_count": report.analyzed_task_count,
        "matching_task_count": report.matching_task_count,
        "failing_task_count": report.failing_task_count,
        "improvement_item_count": report.improvement_item_count,
        "highest_priority": report.highest_priority,
        "next_solver_target": report.next_solver_target,
        "signature": report.signature,
        "improvement_report": report.to_dict(),
        "validation": validation,
        "metadata": report.metadata,
    }


def write_failure_driven_improvement_artifacts(
    payload: Optional[Mapping[str, Any]] = None,
    *,
    output_dir: str = "examples/milestone-4/failure-driven-improvement-loop-v1",
) -> Dict[str, str]:
    selected_payload = dict(payload) if payload is not None else run_failure_driven_improvement_pipeline()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "failure-driven-improvement-loop-v1-smoke.json"
    md_path = output_path / "failure-driven-improvement-loop-v1-smoke.md"

    json_path.write_text(
        json.dumps(selected_payload, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    md_path.write_text(
        render_failure_driven_improvement_markdown(selected_payload),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
    }
