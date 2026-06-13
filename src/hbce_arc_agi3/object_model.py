"""Object-level grid model for HBCE ARC-AGI-3 public baseline.

Object Model v1 extracts deterministic connected components from local
ARC-like grids. It is public-safe and purely data driven.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Dict, Iterable, List, Sequence, Tuple


Grid = List[List[int]]
Cell = Tuple[int, int]


@dataclass(frozen=True)
class GridObject:
    object_id: str
    value: int
    cells: List[Cell]
    cell_count: int
    bbox: Dict[str, int]
    width: int
    height: int
    area: int
    density: float
    centroid: Dict[str, float]
    signature: str

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["cells"] = [[row, col] for row, col in self.cells]
        return data


@dataclass(frozen=True)
class ObjectModel:
    status: str
    object_count: int
    background_value: int
    width: int
    height: int
    objects: List[GridObject]
    value_counts: Dict[str, int]
    occupied_cell_count: int
    grid_cell_count: int
    object_density: float
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["objects"] = [obj.to_dict() for obj in self.objects]
        return data


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_int_grid(grid: Any) -> Grid:
    if not isinstance(grid, list) or not grid:
        return []

    coerced: Grid = []
    expected_width: int | None = None

    for row in grid:
        if not isinstance(row, list):
            raise ValueError("Grid rows must be lists")

        if expected_width is None:
            expected_width = len(row)
        elif len(row) != expected_width:
            raise ValueError("Grid rows must have deterministic equal width")

        coerced_row: List[int] = []
        for value in row:
            if not isinstance(value, int):
                raise ValueError("Grid values must be integers")
            coerced_row.append(value)

        coerced.append(coerced_row)

    return coerced


def extract_grid(payload: Any) -> Grid:
    """Extract a grid from common public ARC-AGI-3 payload shapes."""

    if isinstance(payload, list):
        return _coerce_int_grid(payload)

    if not isinstance(payload, dict):
        raise ValueError("Object model payload must be a grid or dictionary")

    candidates = [
        payload.get("grid"),
        payload.get("input"),
    ]

    for candidate in candidates:
        if candidate is not None:
            return _coerce_int_grid(candidate)

    for nested_key in ("normalized", "agent_state", "loaded_task", "observation", "world_model", "run"):
        nested = payload.get(nested_key)
        if isinstance(nested, dict):
            try:
                return extract_grid(nested)
            except ValueError:
                pass

    raise ValueError("No grid found in payload")


def _neighbors(row: int, col: int) -> Iterable[Cell]:
    yield row - 1, col
    yield row + 1, col
    yield row, col - 1
    yield row, col + 1


def _object_from_cells(index: int, value: int, cells: List[Cell]) -> GridObject:
    ordered = sorted(cells)
    rows = [row for row, _ in ordered]
    cols = [col for _, col in ordered]

    min_row = min(rows)
    max_row = max(rows)
    min_col = min(cols)
    max_col = max(cols)

    width = max_col - min_col + 1
    height = max_row - min_row + 1
    area = width * height
    density = round(len(ordered) / area, 6) if area else 0.0

    centroid = {
        "row": round(sum(rows) / len(rows), 6),
        "col": round(sum(cols) / len(cols), 6),
    }

    basis = {
        "value": value,
        "cells": ordered,
        "bbox": [min_row, min_col, max_row, max_col],
    }
    signature = _stable_signature(basis)
    object_id = f"OBJ-{index:04d}-{signature[:8]}"

    return GridObject(
        object_id=object_id,
        value=value,
        cells=ordered,
        cell_count=len(ordered),
        bbox={
            "min_row": min_row,
            "min_col": min_col,
            "max_row": max_row,
            "max_col": max_col,
        },
        width=width,
        height=height,
        area=area,
        density=density,
        centroid=centroid,
        signature=signature,
    )


def build_object_model_from_grid(
    grid: Sequence[Sequence[int]],
    *,
    background_value: int = 0,
) -> ObjectModel:
    """Build a deterministic connected-component object model from a grid."""

    coerced = _coerce_int_grid([list(row) for row in grid])
    height = len(coerced)
    width = len(coerced[0]) if height else 0
    grid_cell_count = width * height

    visited: set[Cell] = set()
    objects: List[GridObject] = []
    value_counts: Dict[str, int] = {}

    for row in range(height):
        for col in range(width):
            value = coerced[row][col]
            value_counts[str(value)] = value_counts.get(str(value), 0) + 1

            if value == background_value or (row, col) in visited:
                continue

            stack: List[Cell] = [(row, col)]
            component: List[Cell] = []
            visited.add((row, col))

            while stack:
                current_row, current_col = stack.pop()
                component.append((current_row, current_col))

                for next_row, next_col in _neighbors(current_row, current_col):
                    if not (0 <= next_row < height and 0 <= next_col < width):
                        continue

                    if (next_row, next_col) in visited:
                        continue

                    if coerced[next_row][next_col] != value:
                        continue

                    visited.add((next_row, next_col))
                    stack.append((next_row, next_col))

            objects.append(_object_from_cells(len(objects) + 1, value, component))

    occupied_cell_count = sum(obj.cell_count for obj in objects)
    object_density = round(occupied_cell_count / grid_cell_count, 6) if grid_cell_count else 0.0

    signature_basis = {
        "background_value": background_value,
        "width": width,
        "height": height,
        "objects": [
            {
                "value": obj.value,
                "cells": obj.cells,
                "bbox": obj.bbox,
                "signature": obj.signature,
            }
            for obj in objects
        ],
    }

    return ObjectModel(
        status="OBJECT_MODEL_READY",
        object_count=len(objects),
        background_value=background_value,
        width=width,
        height=height,
        objects=objects,
        value_counts=dict(sorted(value_counts.items(), key=lambda item: int(item[0]))),
        occupied_cell_count=occupied_cell_count,
        grid_cell_count=grid_cell_count,
        object_density=object_density,
        signature=_stable_signature(signature_basis),
        metadata={
            "source": "object_model_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "connectivity": "4-neighbor",
            "background_value": background_value,
        },
    )


def build_object_model(payload: Any, *, background_value: int = 0) -> ObjectModel:
    """Build an object model from a grid or supported public pipeline payload."""

    grid = extract_grid(payload)
    return build_object_model_from_grid(grid, background_value=background_value)


def validate_object_model(model: ObjectModel | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Object Model v1 public contract."""

    data = model.to_dict() if isinstance(model, ObjectModel) else dict(model)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    checks = {
        "status_ready": data.get("status") == "OBJECT_MODEL_READY",
        "object_count_number": isinstance(data.get("object_count"), int),
        "objects_list": isinstance(data.get("objects"), list),
        "signature_present": bool(data.get("signature")),
        "value_counts_present": isinstance(data.get("value_counts"), dict),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
    }

    valid = all(checks.values())

    return {
        "status": "OBJECT_MODEL_VALID" if valid else "OBJECT_MODEL_INVALID",
        "valid": valid,
        "checks": checks,
        "object_count": data.get("object_count"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "object_model_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }
