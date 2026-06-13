"""Strategy Interface v2 for ARC-AGI-3 Milestone #4.

This module defines the public deterministic strategy contract for the
Milestone #4 Solver Engine.

It is intentionally local-only and dependency-free.
It does not send Kaggle submissions.
It does not call external APIs.
It does not read credentials.
It does not expose private HBCE/JOKER-C2 core logic.
"""

from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Dict, Iterable, List, Mapping, Optional, Protocol, Sequence, Tuple


Grid = Tuple[Tuple[int, ...], ...]


def _stable_signature(payload: Mapping[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def normalize_grid(grid: Sequence[Sequence[int]], *, field_name: str = "grid") -> Grid:
    """Normalize and validate an ARC-style grid."""

    if not isinstance(grid, Sequence) or isinstance(grid, (str, bytes)):
        raise ValueError(f"{field_name} must be a non-empty rectangular grid")

    if len(grid) == 0:
        raise ValueError(f"{field_name} must not be empty")

    normalized_rows: List[Tuple[int, ...]] = []
    expected_width: Optional[int] = None

    for row_index, row in enumerate(grid):
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)):
            raise ValueError(f"{field_name}[{row_index}] must be a sequence of integers")

        if len(row) == 0:
            raise ValueError(f"{field_name}[{row_index}] must not be empty")

        normalized_row: List[int] = []

        for col_index, value in enumerate(row):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(
                    f"{field_name}[{row_index}][{col_index}] must be an integer color value"
                )

            if value < 0 or value > 9:
                raise ValueError(
                    f"{field_name}[{row_index}][{col_index}] must be between 0 and 9"
                )

            normalized_row.append(value)

        width = len(normalized_row)

        if expected_width is None:
            expected_width = width
        elif width != expected_width:
            raise ValueError(f"{field_name} must be rectangular")

        normalized_rows.append(tuple(normalized_row))

    return tuple(normalized_rows)


def grid_to_lists(grid: Grid | Sequence[Sequence[int]]) -> List[List[int]]:
    normalized = normalize_grid(grid)
    return [list(row) for row in normalized]


def grid_shape(grid: Grid | Sequence[Sequence[int]]) -> Dict[str, int]:
    normalized = normalize_grid(grid)
    return {
        "height": len(normalized),
        "width": len(normalized[0]),
        "cell_count": len(normalized) * len(normalized[0]),
    }


def grid_signature(grid: Grid | Sequence[Sequence[int]]) -> str:
    normalized = normalize_grid(grid)
    return _stable_signature({"grid": normalized})


@dataclass(frozen=True)
class StrategyExample:
    """Training input/output example."""

    input_grid: Grid
    output_grid: Grid
    metadata: Dict[str, Any]

    @classmethod
    def build(
        cls,
        input_grid: Sequence[Sequence[int]],
        output_grid: Sequence[Sequence[int]],
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "StrategyExample":
        return cls(
            input_grid=normalize_grid(input_grid, field_name="input_grid"),
            output_grid=normalize_grid(output_grid, field_name="output_grid"),
            metadata=dict(metadata or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["input_grid"] = grid_to_lists(self.input_grid)
        data["output_grid"] = grid_to_lists(self.output_grid)
        data["input_shape"] = grid_shape(self.input_grid)
        data["output_shape"] = grid_shape(self.output_grid)
        data["input_signature"] = grid_signature(self.input_grid)
        data["output_signature"] = grid_signature(self.output_grid)
        return data


@dataclass(frozen=True)
class StrategyInput:
    """Normalized strategy input contract."""

    task_id: str
    train_pairs: Tuple[StrategyExample, ...]
    test_input: Grid
    metadata: Dict[str, Any]

    @classmethod
    def build(
        cls,
        *,
        task_id: str,
        train_pairs: Iterable[StrategyExample | Mapping[str, Any]],
        test_input: Sequence[Sequence[int]],
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "StrategyInput":
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("task_id must be a non-empty string")

        normalized_pairs: List[StrategyExample] = []

        for index, pair in enumerate(train_pairs):
            if isinstance(pair, StrategyExample):
                normalized_pairs.append(pair)
                continue

            if not isinstance(pair, Mapping):
                raise ValueError(f"train_pairs[{index}] must be StrategyExample or mapping")

            normalized_pairs.append(
                StrategyExample.build(
                    pair.get("input_grid") or pair.get("input") or pair.get("inputGrid"),
                    pair.get("output_grid") or pair.get("output") or pair.get("outputGrid"),
                    metadata=pair.get("metadata") if isinstance(pair.get("metadata"), Mapping) else {},
                )
            )

        if not normalized_pairs:
            raise ValueError("train_pairs must contain at least one example")

        return cls(
            task_id=task_id.strip(),
            train_pairs=tuple(normalized_pairs),
            test_input=normalize_grid(test_input, field_name="test_input"),
            metadata={
                **dict(metadata or {}),
                "source": "strategy_interface_v2",
                "milestone": "Milestone #4",
                "task": "Task 1",
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
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "train_pairs": [pair.to_dict() for pair in self.train_pairs],
            "test_input": grid_to_lists(self.test_input),
            "test_input_shape": grid_shape(self.test_input),
            "test_input_signature": grid_signature(self.test_input),
            "metadata": copy.deepcopy(self.metadata),
        }


@dataclass(frozen=True)
class StrategyDescriptor:
    """Public metadata describing one strategy."""

    strategy_id: str
    strategy_name: str
    strategy_version: str
    strategy_family: str
    deterministic: bool
    local_only: bool
    score_oriented: bool
    prize_oriented_solver_target: bool
    external_api_dependency: bool
    private_core_exposure: bool
    kaggle_submission_sent: bool
    description: str
    signature: str
    metadata: Dict[str, Any]

    @classmethod
    def build(
        cls,
        *,
        strategy_id: str,
        strategy_name: str,
        strategy_version: str,
        strategy_family: str,
        description: str,
    ) -> "StrategyDescriptor":
        basis = {
            "strategy_id": strategy_id,
            "strategy_name": strategy_name,
            "strategy_version": strategy_version,
            "strategy_family": strategy_family,
            "description": description,
            "deterministic": True,
            "local_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "external_api_dependency": False,
            "private_core_exposure": False,
            "kaggle_submission_sent": False,
        }

        return cls(
            strategy_id=strategy_id,
            strategy_name=strategy_name,
            strategy_version=strategy_version,
            strategy_family=strategy_family,
            deterministic=True,
            local_only=True,
            score_oriented=True,
            prize_oriented_solver_target=True,
            external_api_dependency=False,
            private_core_exposure=False,
            kaggle_submission_sent=False,
            description=description,
            signature=_stable_signature(basis),
            metadata={
                "source": "strategy_interface_v2",
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
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StrategyResult:
    """Deterministic candidate output produced by one strategy."""

    status: str
    strategy_id: str
    strategy_name: str
    strategy_version: str
    task_id: str
    candidate_grid: Grid
    confidence: float
    score_hint: float
    rank_hint: int
    reasoning_tags: Tuple[str, ...]
    candidate_signature: str
    result_signature: str
    metadata: Dict[str, Any]

    @classmethod
    def build(
        cls,
        *,
        strategy_descriptor: StrategyDescriptor,
        task_id: str,
        candidate_grid: Sequence[Sequence[int]],
        confidence: float,
        score_hint: float,
        rank_hint: int,
        reasoning_tags: Iterable[str],
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "StrategyResult":
        if confidence < 0.0 or confidence > 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

        if score_hint < 0.0 or score_hint > 1.0:
            raise ValueError("score_hint must be between 0.0 and 1.0")

        normalized_grid = normalize_grid(candidate_grid, field_name="candidate_grid")
        normalized_tags = tuple(sorted(str(tag) for tag in reasoning_tags))

        candidate_sig = grid_signature(normalized_grid)

        basis = {
            "strategy_id": strategy_descriptor.strategy_id,
            "task_id": task_id,
            "candidate_signature": candidate_sig,
            "confidence": round(float(confidence), 6),
            "score_hint": round(float(score_hint), 6),
            "rank_hint": int(rank_hint),
            "reasoning_tags": normalized_tags,
        }

        return cls(
            status="STRATEGY_RESULT_READY",
            strategy_id=strategy_descriptor.strategy_id,
            strategy_name=strategy_descriptor.strategy_name,
            strategy_version=strategy_descriptor.strategy_version,
            task_id=task_id,
            candidate_grid=normalized_grid,
            confidence=round(float(confidence), 6),
            score_hint=round(float(score_hint), 6),
            rank_hint=int(rank_hint),
            reasoning_tags=normalized_tags,
            candidate_signature=candidate_sig,
            result_signature=_stable_signature(basis),
            metadata={
                **dict(metadata or {}),
                "source": "strategy_interface_v2",
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
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["candidate_grid"] = grid_to_lists(self.candidate_grid)
        data["candidate_shape"] = grid_shape(self.candidate_grid)
        data["reasoning_tags"] = list(self.reasoning_tags)
        return data


class SolverStrategyV2(Protocol):
    """Protocol implemented by every Milestone #4 solver strategy."""

    descriptor: StrategyDescriptor

    def solve(self, strategy_input: StrategyInput) -> StrategyResult:
        """Return a deterministic candidate result."""


class IdentityBaselineStrategyV2:
    """Baseline strategy that returns the test input unchanged."""

    descriptor = StrategyDescriptor.build(
        strategy_id="STRATEGY-IDENTITY-BASELINE-v2",
        strategy_name="identity_baseline_v2",
        strategy_version="v2",
        strategy_family="BASELINE",
        description="Returns the test input unchanged as deterministic baseline candidate.",
    )

    def solve(self, strategy_input: StrategyInput) -> StrategyResult:
        return StrategyResult.build(
            strategy_descriptor=self.descriptor,
            task_id=strategy_input.task_id,
            candidate_grid=strategy_input.test_input,
            confidence=0.5,
            score_hint=0.5,
            rank_hint=100,
            reasoning_tags=[
                "baseline",
                "identity",
                "shape_preserving",
                "milestone_4_task_1",
            ],
            metadata={
                "uses_train_pairs": False,
                "candidate_policy": "RETURN_TEST_INPUT_UNCHANGED",
            },
        )


@dataclass
class StrategyRegistryV2:
    """Registry for deterministic Milestone #4 strategies."""

    strategies: List[SolverStrategyV2]

    @classmethod
    def build_default(cls) -> "StrategyRegistryV2":
        return cls(strategies=[IdentityBaselineStrategyV2()])

    def register(self, strategy: SolverStrategyV2) -> None:
        strategy_id = strategy.descriptor.strategy_id

        if any(item.descriptor.strategy_id == strategy_id for item in self.strategies):
            raise ValueError(f"duplicate strategy_id: {strategy_id}")

        self.strategies.append(strategy)

    def descriptors(self) -> List[Dict[str, Any]]:
        return [strategy.descriptor.to_dict() for strategy in self.strategies]

    def solve_all(self, strategy_input: StrategyInput) -> List[StrategyResult]:
        results = [strategy.solve(strategy_input) for strategy in self.strategies]
        return sorted(
            results,
            key=lambda result: (
                -result.score_hint,
                -result.confidence,
                result.rank_hint,
                result.strategy_id,
            ),
        )

    def select_best(self, strategy_input: StrategyInput) -> StrategyResult:
        results = self.solve_all(strategy_input)

        if not results:
            raise ValueError("strategy registry returned no results")

        return results[0]


def validate_strategy_descriptor(descriptor: StrategyDescriptor | Mapping[str, Any]) -> Dict[str, Any]:
    data = descriptor.to_dict() if isinstance(descriptor, StrategyDescriptor) else dict(descriptor)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), Mapping) else {}

    checks = {
        "strategy_id_present": isinstance(data.get("strategy_id"), str) and bool(data.get("strategy_id")),
        "strategy_name_present": isinstance(data.get("strategy_name"), str) and bool(data.get("strategy_name")),
        "strategy_version_present": isinstance(data.get("strategy_version"), str) and bool(data.get("strategy_version")),
        "strategy_family_present": isinstance(data.get("strategy_family"), str) and bool(data.get("strategy_family")),
        "deterministic_true": data.get("deterministic") is True,
        "local_only_true": data.get("local_only") is True,
        "score_oriented_true": data.get("score_oriented") is True,
        "prize_oriented_solver_target_true": data.get("prize_oriented_solver_target") is True,
        "external_api_dependency_false": data.get("external_api_dependency") is False,
        "private_core_exposure_false": data.get("private_core_exposure") is False,
        "kaggle_submission_sent_false": data.get("kaggle_submission_sent") is False,
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
    }

    valid = all(checks.values())

    return {
        "status": "STRATEGY_DESCRIPTOR_VALID" if valid else "STRATEGY_DESCRIPTOR_INVALID",
        "valid": valid,
        "checks": checks,
        "strategy_id": data.get("strategy_id"),
        "signature": data.get("signature"),
    }


def validate_strategy_result(
    result: StrategyResult | Mapping[str, Any],
    *,
    expected_task_id: Optional[str] = None,
) -> Dict[str, Any]:
    data = result.to_dict() if isinstance(result, StrategyResult) else dict(result)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), Mapping) else {}

    checks = {
        "status_ready": data.get("status") == "STRATEGY_RESULT_READY",
        "strategy_id_present": isinstance(data.get("strategy_id"), str) and bool(data.get("strategy_id")),
        "strategy_name_present": isinstance(data.get("strategy_name"), str) and bool(data.get("strategy_name")),
        "task_id_present": isinstance(data.get("task_id"), str) and bool(data.get("task_id")),
        "task_id_matches": expected_task_id is None or data.get("task_id") == expected_task_id,
        "candidate_grid_valid": _grid_data_is_valid(data.get("candidate_grid")),
        "confidence_valid": isinstance(data.get("confidence"), float) and 0.0 <= data.get("confidence") <= 1.0,
        "score_hint_valid": isinstance(data.get("score_hint"), float) and 0.0 <= data.get("score_hint") <= 1.0,
        "rank_hint_valid": isinstance(data.get("rank_hint"), int),
        "candidate_signature_present": isinstance(data.get("candidate_signature"), str) and bool(data.get("candidate_signature")),
        "result_signature_present": isinstance(data.get("result_signature"), str) and bool(data.get("result_signature")),
        "reasoning_tags_present": isinstance(data.get("reasoning_tags"), list) and bool(data.get("reasoning_tags")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
        "metadata_score_oriented": metadata.get("score_oriented") is True,
        "metadata_prize_oriented_solver_target": metadata.get("prize_oriented_solver_target") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
    }

    valid = all(checks.values())

    return {
        "status": "STRATEGY_RESULT_VALID" if valid else "STRATEGY_RESULT_INVALID",
        "valid": valid,
        "checks": checks,
        "strategy_id": data.get("strategy_id"),
        "task_id": data.get("task_id"),
        "candidate_signature": data.get("candidate_signature"),
        "result_signature": data.get("result_signature"),
    }


def _grid_data_is_valid(value: Any) -> bool:
    try:
        normalize_grid(value)
        return True
    except Exception:
        return False


def build_strategy_interface_v2_smoke_input() -> StrategyInput:
    return StrategyInput.build(
        task_id="MILESTONE-4-TASK-1-SMOKE",
        train_pairs=[
            StrategyExample.build(
                input_grid=[[1, 0], [0, 1]],
                output_grid=[[1, 0], [0, 1]],
                metadata={"example_id": "identity-smoke-1"},
            )
        ],
        test_input=[[2, 0], [0, 2]],
        metadata={
            "smoke_test": True,
            "baseline_reference": "MILESTONE_3_CLOSED_PASS",
            "prize_target_usd": 850000,
            "highest_score_prize_target_usd": 150000,
            "bonus_prize_target_usd": 700000,
            "final_submission_deadline": "2026-11-02",
        },
    )


def run_strategy_interface_v2_pipeline(
    strategy_input: Optional[StrategyInput] = None,
    registry: Optional[StrategyRegistryV2] = None,
) -> Dict[str, Any]:
    input_payload = strategy_input or build_strategy_interface_v2_smoke_input()
    strategy_registry = registry or StrategyRegistryV2.build_default()

    descriptors = strategy_registry.descriptors()
    results = strategy_registry.solve_all(input_payload)
    best = strategy_registry.select_best(input_payload)

    descriptor_validations = [
        validate_strategy_descriptor(descriptor) for descriptor in descriptors
    ]
    result_validations = [
        validate_strategy_result(result, expected_task_id=input_payload.task_id) for result in results
    ]

    valid = (
        bool(descriptors)
        and bool(results)
        and all(item["valid"] for item in descriptor_validations)
        and all(item["valid"] for item in result_validations)
        and validate_strategy_result(best, expected_task_id=input_payload.task_id)["valid"]
    )

    signature = _stable_signature(
        {
            "task_id": input_payload.task_id,
            "strategy_count": len(descriptors),
            "candidate_count": len(results),
            "best_strategy_id": best.strategy_id,
            "best_candidate_signature": best.candidate_signature,
            "valid": valid,
        }
    )

    return {
        "status": "STRATEGY_INTERFACE_V2_PIPELINE_READY",
        "interface_status": "STRATEGY_INTERFACE_V2_READY",
        "validation_status": "STRATEGY_INTERFACE_V2_VALID" if valid else "STRATEGY_INTERFACE_V2_INVALID",
        "task_id": input_payload.task_id,
        "strategy_count": len(descriptors),
        "candidate_count": len(results),
        "best_strategy_id": best.strategy_id,
        "best_candidate_signature": best.candidate_signature,
        "input": input_payload.to_dict(),
        "descriptors": descriptors,
        "results": [result.to_dict() for result in results],
        "best_result": best.to_dict(),
        "descriptor_validations": descriptor_validations,
        "result_validations": result_validations,
        "signature": signature,
        "metadata": {
            "source": "strategy_interface_v2",
            "milestone": "Milestone #4",
            "task": "Task 1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "result_required": True,
            "score_improvement_required": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    }


def write_strategy_interface_v2_artifacts(
    payload: Optional[Mapping[str, Any]] = None,
    *,
    output_dir: str = "examples/milestone-4/strategy-interface-v2",
) -> Dict[str, str]:
    data = dict(payload or run_strategy_interface_v2_pipeline())
    output_path = __import__("pathlib").Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "strategy-interface-v2-smoke.json"
    markdown_path = output_path / "strategy-interface-v2-smoke.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_strategy_interface_v2_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }


def render_strategy_interface_v2_markdown(payload: Mapping[str, Any]) -> str:
    data = dict(payload)

    lines = [
        "# ARC-AGI-3 Milestone #4 Task 1 — Strategy Interface v2 Smoke",
        "",
        f"Status: {data['status']}",
        f"Interface status: {data['interface_status']}",
        f"Validation status: {data['validation_status']}",
        f"Task ID: {data['task_id']}",
        f"Strategy count: {data['strategy_count']}",
        f"Candidate count: {data['candidate_count']}",
        f"Best strategy ID: {data['best_strategy_id']}",
        f"Best candidate signature: {data['best_candidate_signature']}",
        f"Signature: {data['signature']}",
        "",
        "## Boundary",
        "",
        "- public_safe=true",
        "- deterministic=true",
        "- local_only=true",
        "- dry_run_only=true",
        "- score_oriented=true",
        "- prize_oriented_solver_target=true",
        "- external_api_dependency=false",
        "- contains_api_keys=false",
        "- kaggle_submission_sent=false",
        "- private_core_exposure=false",
        "",
    ]

    return "\n".join(lines)


def validate_strategy_interface_v2_pipeline(payload: Mapping[str, Any]) -> Dict[str, Any]:
    data = dict(payload)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), Mapping) else {}

    checks = {
        "status_ready": data.get("status") == "STRATEGY_INTERFACE_V2_PIPELINE_READY",
        "interface_status_ready": data.get("interface_status") == "STRATEGY_INTERFACE_V2_READY",
        "validation_status_valid": data.get("validation_status") == "STRATEGY_INTERFACE_V2_VALID",
        "strategy_count_positive": isinstance(data.get("strategy_count"), int) and data.get("strategy_count") >= 1,
        "candidate_count_positive": isinstance(data.get("candidate_count"), int) and data.get("candidate_count") >= 1,
        "best_strategy_present": isinstance(data.get("best_strategy_id"), str) and bool(data.get("best_strategy_id")),
        "best_candidate_signature_present": isinstance(data.get("best_candidate_signature"), str) and bool(data.get("best_candidate_signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
        "metadata_score_oriented": metadata.get("score_oriented") is True,
        "metadata_prize_oriented_solver_target": metadata.get("prize_oriented_solver_target") is True,
        "metadata_result_required": metadata.get("result_required") is True,
        "metadata_score_improvement_required": metadata.get("score_improvement_required") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
    }

    valid = all(checks.values())

    return {
        "status": "STRATEGY_INTERFACE_V2_VALID" if valid else "STRATEGY_INTERFACE_V2_INVALID",
        "valid": valid,
        "checks": checks,
        "strategy_count": data.get("strategy_count"),
        "candidate_count": data.get("candidate_count"),
        "best_strategy_id": data.get("best_strategy_id"),
        "signature": data.get("signature"),
    }
