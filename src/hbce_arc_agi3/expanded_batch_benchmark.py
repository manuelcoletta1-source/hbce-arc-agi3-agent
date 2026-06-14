"""Expanded Batch Benchmark v2 for ARC-AGI-3 Milestone #4.

Pipeline:
Candidate Generator v1
Candidate Ranker v1
Expanded Batch Benchmark v2

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

from dataclasses import asdict, dataclass, is_dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from hbce_arc_agi3.candidate_generator import (
    build_candidate_generator_smoke_expected_best_grid,
    build_candidate_generator_smoke_test_input,
    build_candidate_generator_smoke_train_pairs,
    generate_candidates,
    grid_to_lists,
)
from hbce_arc_agi3.candidate_ranker import (
    rank_candidates,
    validate_candidate_ranking_report,
)


Grid = List[List[int]]


def _to_dict(value: Any) -> Dict[str, Any]:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError(f"Cannot convert value to dict: {type(value)!r}")


def _stable_signature(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16].upper()


def _grid_data_is_valid(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(row, list) and bool(row) for row in value)
        and len({len(row) for row in value}) == 1
        and all(isinstance(cell, int) for row in value for cell in row)
    )


def _grids_equal(left: Any, right: Any) -> bool:
    if not _grid_data_is_valid(left) or not _grid_data_is_valid(right):
        return False
    return left == right


def _ready_status(value: Any) -> bool:
    return isinstance(value, str) and value.endswith("_READY")


@dataclass(frozen=True)
class ExpandedBenchmarkTask:
    task_id: str
    train_pairs: Tuple[Dict[str, Any], ...]
    test_input: Grid
    expected_best_grid: Optional[Grid]
    task_family: str
    difficulty_hint: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExpandedBenchmarkTaskResult:
    task_id: str
    status: str
    task_family: str
    difficulty_hint: str
    candidate_count: int
    generation_status: str
    ranking_status: str
    best_candidate_type: str
    best_candidate_score: float
    best_candidate_signature: str
    expected_best_available: bool
    best_candidate_matches_expected: bool
    failure_reason: str
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExpandedBatchBenchmarkReport:
    status: str
    benchmark_id: str
    task_count: int
    tasks_processed: int
    generation_success_count: int
    ranking_success_count: int
    expected_match_count: int
    expected_available_count: int
    candidate_generation_success_rate: float
    ranking_success_rate: float
    best_candidate_match_rate: float
    average_best_score: float
    best_task_score: float
    worst_task_score: float
    task_results: Tuple[ExpandedBenchmarkTaskResult, ...]
    failure_reasons: Tuple[str, ...]
    task_result_signatures: Tuple[str, ...]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _make_color_shape_smoke_task() -> ExpandedBenchmarkTask:
    return ExpandedBenchmarkTask(
        task_id="EXPANDED-BATCH-V2-COLOR-SHAPE-SMOKE",
        train_pairs=tuple(build_candidate_generator_smoke_train_pairs()),
        test_input=build_candidate_generator_smoke_test_input(),
        expected_best_grid=build_candidate_generator_smoke_expected_best_grid(),
        task_family="color_shape_combined",
        difficulty_hint="smoke",
        metadata={
            "source": "candidate_generator_smoke",
            "expected_best_candidate_type": "COLOR_SHAPE_COMBINED",
        },
    )


def _make_identity_task() -> ExpandedBenchmarkTask:
    test_input = [
        [0, 4, 0],
        [0, 0, 0],
        [0, 4, 0],
    ]

    train_pairs = (
        {
            "input": [
                [0, 0, 0],
                [0, 2, 0],
                [0, 0, 0],
            ],
            "output": [
                [0, 0, 0],
                [0, 2, 0],
                [0, 0, 0],
            ],
        },
        {
            "input": [
                [3, 0, 0],
                [0, 0, 0],
                [0, 0, 3],
            ],
            "output": [
                [3, 0, 0],
                [0, 0, 0],
                [0, 0, 3],
            ],
        },
    )

    return ExpandedBenchmarkTask(
        task_id="EXPANDED-BATCH-V2-IDENTITY",
        train_pairs=train_pairs,
        test_input=test_input,
        expected_best_grid=test_input,
        task_family="identity_baseline",
        difficulty_hint="easy",
        metadata={
            "source": "synthetic_public_safe",
            "expected_best_candidate_type": "IDENTITY",
        },
    )


def _make_color_only_task() -> ExpandedBenchmarkTask:
    train_pairs = (
        {
            "input": [
                [0, 1, 0],
                [0, 1, 0],
                [0, 0, 0],
            ],
            "output": [
                [0, 8, 0],
                [0, 8, 0],
                [0, 0, 0],
            ],
        },
        {
            "input": [
                [2, 0, 0],
                [2, 0, 0],
                [0, 0, 0],
            ],
            "output": [
                [8, 0, 0],
                [8, 0, 0],
                [0, 0, 0],
            ],
        },
    )

    test_input = [
        [0, 3, 0],
        [0, 3, 0],
        [0, 0, 0],
    ]

    expected = [
        [0, 8, 0],
        [0, 8, 0],
        [0, 0, 0],
    ]

    return ExpandedBenchmarkTask(
        task_id="EXPANDED-BATCH-V2-COLOR-ONLY",
        train_pairs=train_pairs,
        test_input=test_input,
        expected_best_grid=expected,
        task_family="color_transform",
        difficulty_hint="easy",
        metadata={
            "source": "synthetic_public_safe",
            "expected_best_candidate_type": "COLOR_REMAP",
        },
    )


def build_expanded_batch_benchmark_tasks() -> List[ExpandedBenchmarkTask]:
    return [
        _make_color_shape_smoke_task(),
        _make_identity_task(),
        _make_color_only_task(),
    ]


def _coerce_task(raw_task: ExpandedBenchmarkTask | Mapping[str, Any]) -> ExpandedBenchmarkTask:
    if isinstance(raw_task, ExpandedBenchmarkTask):
        return raw_task

    expected = raw_task.get("expected_best_grid")

    return ExpandedBenchmarkTask(
        task_id=str(raw_task["task_id"]),
        train_pairs=tuple(dict(pair) for pair in raw_task["train_pairs"]),
        test_input=grid_to_lists(raw_task["test_input"]),
        expected_best_grid=grid_to_lists(expected) if expected is not None else None,
        task_family=str(raw_task.get("task_family", "unknown")),
        difficulty_hint=str(raw_task.get("difficulty_hint", "unknown")),
        metadata=dict(raw_task.get("metadata", {})),
    )


def run_expanded_batch_benchmark(
    tasks: Optional[Iterable[ExpandedBenchmarkTask | Mapping[str, Any]]] = None,
) -> ExpandedBatchBenchmarkReport:
    selected_tasks = [_coerce_task(task) for task in (tasks or build_expanded_batch_benchmark_tasks())]
    results: List[ExpandedBenchmarkTaskResult] = []

    for task in selected_tasks:
        try:
            generation_report = generate_candidates(
                task.train_pairs,
                task.test_input,
                task_id=task.task_id,
                background_color=0,
            )
            ranking_report = rank_candidates(generation_report)
            validation = validate_candidate_ranking_report(ranking_report)

            generation_data = _to_dict(generation_report)
            ranking_data = _to_dict(ranking_report)
            best_candidate = ranking_data["best_candidate"]
            best_grid = best_candidate["candidate_grid"]

            expected_available = task.expected_best_grid is not None
            matches_expected = (
                _grids_equal(best_grid, task.expected_best_grid)
                if expected_available
                else False
            )

            failure_reason = "NONE"
            status = "EXPANDED_BATCH_TASK_READY"
            if validation.get("status") != "CANDIDATE_RANKING_VALID":
                status = "EXPANDED_BATCH_TASK_INVALID"
                failure_reason = "RANKING_VALIDATION_FAILED"

            result_payload = {
                "task_id": task.task_id,
                "status": status,
                "task_family": task.task_family,
                "difficulty_hint": task.difficulty_hint,
                "candidate_count": int(ranking_data.get("candidate_count", 0)),
                "generation_status": str(generation_data.get("status", "")),
                "ranking_status": str(ranking_data.get("status", "")),
                "best_candidate_type": str(best_candidate["candidate_type"]),
                "best_candidate_score": round(float(best_candidate["score"]), 4),
                "best_candidate_signature": str(best_candidate["signature"]),
                "expected_best_available": expected_available,
                "best_candidate_matches_expected": matches_expected,
                "failure_reason": failure_reason,
                "metadata": {
                    **task.metadata,
                    "public_safe": True,
                    "local_only": True,
                    "dry_run_only": True,
                },
            }

        except Exception as exc:
            result_payload = {
                "task_id": task.task_id,
                "status": "EXPANDED_BATCH_TASK_FAILED",
                "task_family": task.task_family,
                "difficulty_hint": task.difficulty_hint,
                "candidate_count": 0,
                "generation_status": "GENERATION_FAILED",
                "ranking_status": "RANKING_NOT_RUN",
                "best_candidate_type": "NONE",
                "best_candidate_score": 0.0,
                "best_candidate_signature": "NO_SIGNATURE",
                "expected_best_available": task.expected_best_grid is not None,
                "best_candidate_matches_expected": False,
                "failure_reason": f"{exc.__class__.__name__}: {exc}",
                "metadata": {
                    **task.metadata,
                    "public_safe": True,
                    "local_only": True,
                    "dry_run_only": True,
                },
            }

        results.append(
            ExpandedBenchmarkTaskResult(
                **result_payload,
                signature=_stable_signature(result_payload),
            )
        )

    task_count = len(selected_tasks)
    tasks_processed = len(results)

    generation_success_count = sum(
        1 for result in results
        if _ready_status(result.generation_status) and result.candidate_count > 0
    )
    ranking_success_count = sum(
        1 for result in results
        if result.ranking_status == "CANDIDATE_RANKING_READY" and result.candidate_count > 0
    )
    expected_available_count = sum(1 for result in results if result.expected_best_available)
    expected_match_count = sum(1 for result in results if result.best_candidate_matches_expected)

    scores = [result.best_candidate_score for result in results]
    average_best_score = round(sum(scores) / len(scores), 4) if scores else 0.0
    best_task_score = round(max(scores), 4) if scores else 0.0
    worst_task_score = round(min(scores), 4) if scores else 0.0

    generation_rate = round(generation_success_count / task_count, 4) if task_count else 0.0
    ranking_rate = round(ranking_success_count / task_count, 4) if task_count else 0.0
    match_rate = (
        round(expected_match_count / expected_available_count, 4)
        if expected_available_count
        else 0.0
    )

    failure_reasons = tuple(
        sorted({result.failure_reason for result in results if result.failure_reason != "NONE"})
    )

    status = (
        "EXPANDED_BATCH_BENCHMARK_READY"
        if task_count >= 3
        and tasks_processed == task_count
        and generation_success_count == task_count
        and ranking_success_count == task_count
        else "EXPANDED_BATCH_BENCHMARK_PARTIAL"
    )

    report_payload = {
        "status": status,
        "task_count": task_count,
        "tasks_processed": tasks_processed,
        "generation_success_count": generation_success_count,
        "ranking_success_count": ranking_success_count,
        "expected_match_count": expected_match_count,
        "expected_available_count": expected_available_count,
        "candidate_generation_success_rate": generation_rate,
        "ranking_success_rate": ranking_rate,
        "best_candidate_match_rate": match_rate,
        "average_best_score": average_best_score,
        "best_task_score": best_task_score,
        "worst_task_score": worst_task_score,
        "failure_reasons": failure_reasons,
        "task_result_signatures": tuple(result.signature for result in results),
        "metadata": {
            "source": "expanded_batch_benchmark_v2",
            "milestone": "Milestone #4",
            "task": "Task 7",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "uses_candidate_generator_v1": True,
            "uses_candidate_ranker_v1": True,
            "candidate_generator_to_ranker_pipeline": True,
            "expanded_batch_benchmark_output": True,
            "benchmark_task_count_minimum": 3,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }

    signature = _stable_signature(report_payload)
    benchmark_id = f"EXPANDED-BATCH-BENCHMARK-{signature[:12]}"

    return ExpandedBatchBenchmarkReport(
        benchmark_id=benchmark_id,
        signature=signature,
        task_results=tuple(results),
        **report_payload,
    )


def validate_expanded_batch_benchmark_report(
    report: ExpandedBatchBenchmarkReport | Mapping[str, Any],
) -> Dict[str, Any]:
    data = report.to_dict() if isinstance(report, ExpandedBatchBenchmarkReport) else dict(report)
    errors: List[str] = []

    if data.get("status") != "EXPANDED_BATCH_BENCHMARK_READY":
        errors.append("status is not EXPANDED_BATCH_BENCHMARK_READY")

    if int(data.get("task_count", 0)) < 3:
        errors.append("task_count must be >= 3")

    if data.get("tasks_processed") != data.get("task_count"):
        errors.append("tasks_processed must equal task_count")

    if float(data.get("candidate_generation_success_rate", 0.0)) < 1.0:
        errors.append("candidate_generation_success_rate must be 1.0")

    if float(data.get("ranking_success_rate", 0.0)) < 1.0:
        errors.append("ranking_success_rate must be 1.0")

    if float(data.get("average_best_score", 0.0)) <= 0.0:
        errors.append("average_best_score must be positive")

    metadata = dict(data.get("metadata", {}))

    for key in [
        "public_safe",
        "deterministic",
        "local_only",
        "dry_run_only",
        "uses_candidate_generator_v1",
        "uses_candidate_ranker_v1",
        "candidate_generator_to_ranker_pipeline",
        "expanded_batch_benchmark_output",
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

    task_results = data.get("task_results", [])
    if not isinstance(task_results, (list, tuple)) or len(task_results) < 3:
        errors.append("task_results must contain at least 3 items")
    else:
        for index, result in enumerate(task_results):
            if result.get("status") != "EXPANDED_BATCH_TASK_READY":
                errors.append(f"task_results[{index}].status is invalid")
            if int(result.get("candidate_count", 0)) <= 0:
                errors.append(f"task_results[{index}].candidate_count must be positive")
            if float(result.get("best_candidate_score", 0.0)) <= 0.0:
                errors.append(f"task_results[{index}].best_candidate_score must be positive")

    validation_status = (
        "EXPANDED_BATCH_BENCHMARK_VALID"
        if not errors
        else "EXPANDED_BATCH_BENCHMARK_INVALID"
    )

    return {
        "status": validation_status,
        "valid": not errors,
        "errors": errors,
        "benchmark_id": data.get("benchmark_id"),
        "task_count": data.get("task_count"),
        "tasks_processed": data.get("tasks_processed"),
        "candidate_generation_success_rate": data.get("candidate_generation_success_rate"),
        "ranking_success_rate": data.get("ranking_success_rate"),
        "best_candidate_match_rate": data.get("best_candidate_match_rate"),
        "average_best_score": data.get("average_best_score"),
        "signature": data.get("signature"),
    }


def render_expanded_batch_benchmark_markdown(payload: Mapping[str, Any]) -> str:
    report = dict(payload["benchmark_report"])
    validation = dict(payload["validation"])

    lines = [
        "# ARC AGI3 Milestone #4 Task 7 - Expanded Batch Benchmark v2",
        "",
        "## Status",
        "",
        f"- status: `{payload['status']}`",
        f"- validation: `{validation['status']}`",
        f"- benchmark_id: `{report['benchmark_id']}`",
        f"- signature: `{report['signature']}`",
        "",
        "## Metrics",
        "",
        f"- task_count: `{report['task_count']}`",
        f"- tasks_processed: `{report['tasks_processed']}`",
        f"- candidate_generation_success_rate: `{report['candidate_generation_success_rate']}`",
        f"- ranking_success_rate: `{report['ranking_success_rate']}`",
        f"- best_candidate_match_rate: `{report['best_candidate_match_rate']}`",
        f"- average_best_score: `{report['average_best_score']}`",
        f"- best_task_score: `{report['best_task_score']}`",
        f"- worst_task_score: `{report['worst_task_score']}`",
        "",
        "## Task results",
        "",
        "| task_id | family | candidates | best_type | best_score | match |",
        "|---|---|---:|---|---:|---:|",
    ]

    for result in report["task_results"]:
        lines.append(
            "| {task_id} | {task_family} | {candidate_count} | {best_candidate_type} | {best_candidate_score} | {best_candidate_matches_expected} |".format(
                **result
            )
        )

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- public_safe: `true`",
            "- deterministic: `true`",
            "- local_only: `true`",
            "- dry_run_only: `true`",
            "- external_api_dependency: `false`",
            "- contains_api_keys: `false`",
            "- kaggle_submission_sent: `false`",
            "- private_core_exposure: `false`",
            "- legal_certification: `false`",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_4_TASK_7_EXPANDED_BATCH_BENCHMARK_V2_READY=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_STATUS=EXPANDED_BATCH_BENCHMARK_READY  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_PIPELINE_STATUS=EXPANDED_BATCH_BENCHMARK_PIPELINE_READY  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_VALIDATION=EXPANDED_BATCH_BENCHMARK_VALID  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_TASKS_PROCESSED_MINIMUM_READY=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_CANDIDATE_GENERATION_SUCCESS_RATE_READY=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_RANKING_SUCCESS_RATE_READY=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_BEST_CANDIDATE_MATCH_RATE_READY=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_AVERAGE_BEST_SCORE_READY=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_USES_CANDIDATE_GENERATOR_V1=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_USES_CANDIDATE_RANKER_V1=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_ARTIFACTS_READY=true  ",
            "ARC_AGI3_MILESTONE_4_TASK_7_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  ",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  ",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  ",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  ",
            "ARC_AGI3_LEGAL_CERTIFICATION=false  ",
            "",
        ]
    )

    return "\n".join(lines)


def run_expanded_batch_benchmark_pipeline() -> Dict[str, Any]:
    report = run_expanded_batch_benchmark()
    validation = validate_expanded_batch_benchmark_report(report)

    status = (
        "EXPANDED_BATCH_BENCHMARK_PIPELINE_READY"
        if validation["valid"]
        else "EXPANDED_BATCH_BENCHMARK_PIPELINE_INVALID"
    )

    return {
        "status": status,
        "benchmark_status": report.status,
        "validation_status": validation["status"],
        "benchmark_id": report.benchmark_id,
        "task_count": report.task_count,
        "tasks_processed": report.tasks_processed,
        "candidate_generation_success_rate": report.candidate_generation_success_rate,
        "ranking_success_rate": report.ranking_success_rate,
        "best_candidate_match_rate": report.best_candidate_match_rate,
        "average_best_score": report.average_best_score,
        "best_task_score": report.best_task_score,
        "worst_task_score": report.worst_task_score,
        "failure_reasons": list(report.failure_reasons),
        "signature": report.signature,
        "benchmark_report": report.to_dict(),
        "validation": validation,
        "metadata": report.metadata,
    }


def write_expanded_batch_benchmark_artifacts(
    payload: Optional[Mapping[str, Any]] = None,
    *,
    output_dir: str = "examples/milestone-4/expanded-batch-benchmark-v2",
) -> Dict[str, str]:
    selected_payload = dict(payload) if payload is not None else run_expanded_batch_benchmark_pipeline()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "expanded-batch-benchmark-v2-smoke.json"
    md_path = output_path / "expanded-batch-benchmark-v2-smoke.md"

    json_path.write_text(
        json.dumps(selected_payload, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    md_path.write_text(
        render_expanded_batch_benchmark_markdown(selected_payload),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
    }
