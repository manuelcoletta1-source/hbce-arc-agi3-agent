"""Outcome Verification v1 for HBCE ARC-AGI-3 public baseline.

This module verifies candidate outputs against expected outputs when available.
If an expected output is unavailable, it returns an explicit deterministic
EXPECTED_OUTPUT_UNAVAILABLE result instead of pretending the task was solved.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Dict, List, Optional, Tuple


Grid = List[List[int]]


@dataclass(frozen=True)
class OutcomeVerification:
    status: str
    verification_status: str
    task_id: str
    expected_available: bool
    exact_match: bool
    shape_match: bool
    cell_accuracy: float
    matching_cells: int
    total_cells: int
    mismatch_count: int
    candidate_shape: Dict[str, int]
    expected_shape: Dict[str, int]
    mismatches: List[Dict[str, Any]]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_int_grid(grid: Any) -> Grid:
    if not isinstance(grid, list):
        raise ValueError("Grid must be a list")

    if not grid:
        return []

    expected_width: Optional[int] = None
    output: Grid = []

    for row in grid:
        if not isinstance(row, list):
            raise ValueError("Grid rows must be lists")

        if expected_width is None:
            expected_width = len(row)
        elif len(row) != expected_width:
            raise ValueError("Grid rows must have deterministic equal width")

        output_row: List[int] = []

        for value in row:
            if not isinstance(value, int):
                raise ValueError("Grid values must be integers")
            output_row.append(value)

        output.append(output_row)

    return output


def _shape(grid: Optional[Grid]) -> Dict[str, int]:
    if grid is None:
        return {"height": 0, "width": 0}

    height = len(grid)
    width = len(grid[0]) if height else 0

    return {"height": height, "width": width}


def _candidate_from_strategy(payload: Dict[str, Any]) -> Optional[Grid]:
    """Build a simple deterministic candidate from preserved input structure.

    This is intentionally conservative. It supports the current public planner
    strategy by preserving the input grid for preserve-style candidate actions.
    """

    strategy = payload.get("planner_strategy")
    if not isinstance(strategy, dict):
        return None

    action = strategy.get("selected_action")
    if action not in {
        "preserve_non_background_structure",
        "preserve_object_count",
        "transform_or_preserve_dominant_value",
    }:
        return None

    for key in ("grid", "input"):
        if key in payload:
            return _coerce_int_grid(payload[key])

    loaded_task = payload.get("loaded_task")
    if isinstance(loaded_task, dict):
        normalized = loaded_task.get("normalized")
        if isinstance(normalized, dict):
            for key in ("grid", "input"):
                if key in normalized:
                    return _coerce_int_grid(normalized[key])

    return None


def extract_candidate_output(payload: Any) -> Optional[Grid]:
    """Extract candidate/predicted output from supported public payload shapes."""

    if isinstance(payload, list):
        return _coerce_int_grid(payload)

    if not isinstance(payload, dict):
        raise ValueError("Outcome verification payload must be a grid or dictionary")

    for key in (
        "candidate_output",
        "predicted_output",
        "prediction",
        "proposed_output",
        "output_candidate",
        "candidate_grid",
    ):
        if key in payload:
            return _coerce_int_grid(payload[key])

    strategy_candidate = _candidate_from_strategy(payload)
    if strategy_candidate is not None:
        return strategy_candidate

    for nested_key in ("run", "result", "attempt", "loaded_task", "normalized"):
        nested = payload.get(nested_key)
        if isinstance(nested, dict):
            candidate = extract_candidate_output(nested)
            if candidate is not None:
                return candidate

    return None


def extract_expected_output(payload: Any) -> Optional[Grid]:
    """Extract expected output from supported public payload shapes."""

    if not isinstance(payload, dict):
        return None

    for key in (
        "expected_output",
        "expected",
        "target_output",
        "target",
        "answer",
        "ground_truth",
    ):
        if key in payload:
            return _coerce_int_grid(payload[key])

    for nested_key in ("run", "result", "attempt", "loaded_task", "normalized"):
        nested = payload.get(nested_key)
        if isinstance(nested, dict):
            expected = extract_expected_output(nested)
            if expected is not None:
                return expected

    return None


def _compare_grids(candidate: Grid, expected: Grid) -> Dict[str, Any]:
    candidate_shape = _shape(candidate)
    expected_shape = _shape(expected)
    shape_match = candidate_shape == expected_shape

    if not shape_match:
        return {
            "shape_match": False,
            "exact_match": False,
            "cell_accuracy": 0.0,
            "matching_cells": 0,
            "total_cells": expected_shape["height"] * expected_shape["width"],
            "mismatch_count": expected_shape["height"] * expected_shape["width"],
            "mismatches": [
                {
                    "type": "shape_mismatch",
                    "candidate_shape": candidate_shape,
                    "expected_shape": expected_shape,
                }
            ],
        }

    total_cells = candidate_shape["height"] * candidate_shape["width"]
    matching_cells = 0
    mismatches: List[Dict[str, Any]] = []

    for row_index, row in enumerate(expected):
        for col_index, expected_value in enumerate(row):
            candidate_value = candidate[row_index][col_index]

            if candidate_value == expected_value:
                matching_cells += 1
                continue

            mismatches.append(
                {
                    "row": row_index,
                    "col": col_index,
                    "candidate": candidate_value,
                    "expected": expected_value,
                }
            )

    mismatch_count = len(mismatches)
    exact_match = mismatch_count == 0
    cell_accuracy = round(matching_cells / total_cells, 6) if total_cells else 1.0

    return {
        "shape_match": shape_match,
        "exact_match": exact_match,
        "cell_accuracy": cell_accuracy,
        "matching_cells": matching_cells,
        "total_cells": total_cells,
        "mismatch_count": mismatch_count,
        "mismatches": mismatches[:25],
    }


def verify_outcome(
    payload: Any,
    *,
    task_id: Optional[str] = None,
) -> OutcomeVerification:
    """Verify a candidate output against expected output when available."""

    if isinstance(payload, dict):
        resolved_task_id = str(
            task_id
            or payload.get("task_id")
            or payload.get("id")
            or payload.get("task", "")
            or "anonymous-task"
        )
    else:
        resolved_task_id = str(task_id or "anonymous-task")

    candidate = extract_candidate_output(payload)
    expected = extract_expected_output(payload)

    if candidate is None:
        raise ValueError("Outcome verification requires a candidate output")

    if expected is None:
        candidate_shape = _shape(candidate)
        signature_basis = {
            "task_id": resolved_task_id,
            "candidate": candidate,
            "expected_available": False,
        }
        signature = _stable_signature(signature_basis)

        return OutcomeVerification(
            status="OUTCOME_VERIFICATION_READY",
            verification_status="EXPECTED_OUTPUT_UNAVAILABLE",
            task_id=resolved_task_id,
            expected_available=False,
            exact_match=False,
            shape_match=False,
            cell_accuracy=0.0,
            matching_cells=0,
            total_cells=0,
            mismatch_count=0,
            candidate_shape=candidate_shape,
            expected_shape={"height": 0, "width": 0},
            mismatches=[],
            signature=signature,
            metadata={
                "source": "outcome_verification_v1",
                "public_safe": True,
                "deterministic": True,
                "external_api_dependency": False,
                "executes_dataset_code": False,
                "contains_api_keys": False,
                "expected_output_available": False,
            },
        )

    comparison = _compare_grids(candidate, expected)
    verification_status = "OUTCOME_MATCH" if comparison["exact_match"] else "OUTCOME_MISMATCH"

    signature_basis = {
        "task_id": resolved_task_id,
        "candidate": candidate,
        "expected": expected,
        "comparison": comparison,
    }
    signature = _stable_signature(signature_basis)

    return OutcomeVerification(
        status="OUTCOME_VERIFICATION_READY",
        verification_status=verification_status,
        task_id=resolved_task_id,
        expected_available=True,
        exact_match=bool(comparison["exact_match"]),
        shape_match=bool(comparison["shape_match"]),
        cell_accuracy=float(comparison["cell_accuracy"]),
        matching_cells=int(comparison["matching_cells"]),
        total_cells=int(comparison["total_cells"]),
        mismatch_count=int(comparison["mismatch_count"]),
        candidate_shape=_shape(candidate),
        expected_shape=_shape(expected),
        mismatches=comparison["mismatches"],
        signature=signature,
        metadata={
            "source": "outcome_verification_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "expected_output_available": True,
        },
    )


def validate_outcome_verification(verification: OutcomeVerification | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Outcome Verification v1 public contract."""

    data = verification.to_dict() if isinstance(verification, OutcomeVerification) else dict(verification)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    checks = {
        "status_ready": data.get("status") == "OUTCOME_VERIFICATION_READY",
        "verification_status_present": bool(data.get("verification_status")),
        "task_id_present": bool(data.get("task_id")),
        "expected_available_boolean": isinstance(data.get("expected_available"), bool),
        "exact_match_boolean": isinstance(data.get("exact_match"), bool),
        "shape_match_boolean": isinstance(data.get("shape_match"), bool),
        "cell_accuracy_number": isinstance(data.get("cell_accuracy"), float),
        "signature_present": bool(data.get("signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
    }

    valid = all(checks.values())

    return {
        "status": "OUTCOME_VERIFICATION_VALID" if valid else "OUTCOME_VERIFICATION_INVALID",
        "valid": valid,
        "checks": checks,
        "verification_status": data.get("verification_status"),
        "task_id": data.get("task_id"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "outcome_verification_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def verify_and_validate_outcome(payload: Any, *, task_id: Optional[str] = None) -> Dict[str, Any]:
    """Compatibility wrapper for outcome verification and validation."""

    verification = verify_outcome(payload, task_id=task_id)
    validation = validate_outcome_verification(verification)

    return {
        "status": "OUTCOME_VERIFICATION_PIPELINE_READY",
        "outcome_verification": verification.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "outcome_verification_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
        },
    }
