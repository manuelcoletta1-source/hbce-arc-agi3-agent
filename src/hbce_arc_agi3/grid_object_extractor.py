"""Grid Object Extractor v1 for ARC-AGI-3 Milestone #4.

This module extracts deterministic object/state features from ARC-style grids.

It is public-safe, local-only and dependency-free.
It does not send Kaggle submissions.
It does not call external APIs.
It does not read credentials.
It does not expose private HBCE/JOKER-C2 core logic.
"""

from __future__ import annotations

import copy
import json
from collections import Counter, deque
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

from hbce_arc_agi3.strategy_interface_v2 import (
    Grid,
    grid_shape,
    grid_signature,
    grid_to_lists,
    normalize_grid,
)


Cell = Tuple[int, int]


def _stable_signature(payload: Mapping[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _neighbors(cell: Cell, *, height: int, width: int, connectivity: int) -> Iterable[Cell]:
    row, col = cell

    deltas_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    deltas_8 = deltas_4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in deltas_8 if connectivity == 8 else deltas_4:
        nr = row + dr
        nc = col + dc

        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc


def color_inventory(grid: Sequence[Sequence[int]]) -> Dict[int, int]:
    normalized = normalize_grid(grid)
    counts: Counter[int] = Counter()

    for row in normalized:
        counts.update(row)

    return dict(sorted(counts.items()))


def infer_background_color(grid: Sequence[Sequence[int]], *, preferred: int = 0) -> int:
    inventory = color_inventory(grid)

    if preferred in inventory:
        return preferred

    return sorted(inventory.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _build_binary_mask(cells: Tuple[Cell, ...], bbox: Dict[str, int]) -> Tuple[Tuple[int, ...], ...]:
    cell_set = set(cells)
    mask_rows: List[Tuple[int, ...]] = []

    for row in range(bbox["min_row"], bbox["max_row"] + 1):
        mask_row: List[int] = []

        for col in range(bbox["min_col"], bbox["max_col"] + 1):
            mask_row.append(1 if (row, col) in cell_set else 0)

        mask_rows.append(tuple(mask_row))

    return tuple(mask_rows)


@dataclass(frozen=True)
class GridObject:
    """One connected same-color object extracted from a grid."""

    status: str
    object_id: str
    color: int
    cells: Tuple[Cell, ...]
    area: int
    bounding_box: Dict[str, int]
    centroid: Dict[str, float]
    touches_border: bool
    mask: Tuple[Tuple[int, ...], ...]
    signature: str
    metadata: Dict[str, Any]

    @classmethod
    def build(
        cls,
        *,
        color: int,
        cells: Iterable[Cell],
        grid_height: int,
        grid_width: int,
        connectivity: int,
        background_color: int,
    ) -> "GridObject":
        normalized_cells = tuple(sorted(set(cells)))

        if not normalized_cells:
            raise ValueError("GridObject requires at least one cell")

        rows = [cell[0] for cell in normalized_cells]
        cols = [cell[1] for cell in normalized_cells]

        bbox = {
            "min_row": min(rows),
            "min_col": min(cols),
            "max_row": max(rows),
            "max_col": max(cols),
            "height": max(rows) - min(rows) + 1,
            "width": max(cols) - min(cols) + 1,
        }

        centroid = {
            "row": round(sum(rows) / len(rows), 6),
            "col": round(sum(cols) / len(cols), 6),
        }

        touches_border = any(
            row == 0 or col == 0 or row == grid_height - 1 or col == grid_width - 1
            for row, col in normalized_cells
        )

        mask = _build_binary_mask(normalized_cells, bbox)

        basis = {
            "color": color,
            "cells": normalized_cells,
            "bounding_box": bbox,
            "connectivity": connectivity,
            "background_color": background_color,
        }
        signature = _stable_signature(basis)

        return cls(
            status="GRID_OBJECT_READY",
            object_id=f"GRID-OBJ-{signature[:12]}",
            color=color,
            cells=normalized_cells,
            area=len(normalized_cells),
            bounding_box=bbox,
            centroid=centroid,
            touches_border=touches_border,
            mask=mask,
            signature=signature,
            metadata={
                "source": "grid_object_extractor_v1",
                "milestone": "Milestone #4",
                "task": "Task 2",
                "public_safe": True,
                "deterministic": True,
                "local_only": True,
                "dry_run_only": True,
                "score_oriented": True,
                "prize_oriented_solver_target": True,
                "agentic_state_feature": True,
                "connectivity": connectivity,
                "background_color": background_color,
                "external_api_dependency": False,
                "contains_api_keys": False,
                "kaggle_submission_sent": False,
                "private_core_exposure": False,
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["cells"] = [[row, col] for row, col in self.cells]
        data["mask"] = [list(row) for row in self.mask]
        return data


@dataclass(frozen=True)
class GridObjectExtractionReport:
    """Complete object extraction report for one grid."""

    status: str
    extraction_id: str
    source_grid: Grid
    source_grid_shape: Dict[str, int]
    source_grid_signature: str
    background_color: int
    connectivity: int
    include_background: bool
    color_inventory: Dict[int, int]
    object_count: int
    object_density: float
    objects: Tuple[GridObject, ...]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "extraction_id": self.extraction_id,
            "source_grid": grid_to_lists(self.source_grid),
            "source_grid_shape": copy.deepcopy(self.source_grid_shape),
            "source_grid_signature": self.source_grid_signature,
            "background_color": self.background_color,
            "connectivity": self.connectivity,
            "include_background": self.include_background,
            "color_inventory": dict(self.color_inventory),
            "object_count": self.object_count,
            "object_density": self.object_density,
            "objects": [item.to_dict() for item in self.objects],
            "signature": self.signature,
            "metadata": copy.deepcopy(self.metadata),
        }


def extract_grid_objects(
    grid: Sequence[Sequence[int]],
    *,
    background_color: Optional[int] = 0,
    connectivity: int = 4,
    include_background: bool = False,
) -> GridObjectExtractionReport:
    """Extract connected same-color objects from a grid."""

    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")

    normalized = normalize_grid(grid)
    height = len(normalized)
    width = len(normalized[0])
    bg = infer_background_color(normalized) if background_color is None else background_color

    if isinstance(bg, bool) or not isinstance(bg, int) or bg < 0 or bg > 9:
        raise ValueError("background_color must be an integer between 0 and 9")

    visited: Set[Cell] = set()
    objects: List[GridObject] = []

    for row in range(height):
        for col in range(width):
            cell = (row, col)

            if cell in visited:
                continue

            color = normalized[row][col]

            if color == bg and include_background is False:
                visited.add(cell)
                continue

            queue: deque[Cell] = deque([cell])
            component: Set[Cell] = set()
            visited.add(cell)

            while queue:
                current = queue.popleft()
                component.add(current)

                for nr, nc in _neighbors(current, height=height, width=width, connectivity=connectivity):
                    neighbor = (nr, nc)

                    if neighbor in visited:
                        continue

                    if normalized[nr][nc] != color:
                        continue

                    visited.add(neighbor)
                    queue.append(neighbor)

            objects.append(
                GridObject.build(
                    color=color,
                    cells=component,
                    grid_height=height,
                    grid_width=width,
                    connectivity=connectivity,
                    background_color=bg,
                )
            )

    objects_sorted = tuple(
        sorted(
            objects,
            key=lambda obj: (
                obj.bounding_box["min_row"],
                obj.bounding_box["min_col"],
                obj.color,
                obj.signature,
            ),
        )
    )

    non_background_cells = sum(
        count for color, count in color_inventory(normalized).items()
        if include_background or color != bg
    )

    density = round(non_background_cells / (height * width), 6)

    basis = {
        "grid_signature": grid_signature(normalized),
        "background_color": bg,
        "connectivity": connectivity,
        "include_background": include_background,
        "object_signatures": [obj.signature for obj in objects_sorted],
    }
    signature = _stable_signature(basis)

    return GridObjectExtractionReport(
        status="GRID_OBJECT_EXTRACTION_READY",
        extraction_id=f"GRID-OBJECT-EXTRACTION-{signature[:12]}",
        source_grid=normalized,
        source_grid_shape=grid_shape(normalized),
        source_grid_signature=grid_signature(normalized),
        background_color=bg,
        connectivity=connectivity,
        include_background=include_background,
        color_inventory=color_inventory(normalized),
        object_count=len(objects_sorted),
        object_density=density,
        objects=objects_sorted,
        signature=signature,
        metadata={
            "source": "grid_object_extractor_v1",
            "milestone": "Milestone #4",
            "task": "Task 2",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "agentic_state_feature": True,
            "leaderboard_target_top_10_entry_score": 0.60,
            "leaderboard_target_top_5_score": 0.65,
            "leaderboard_target_podium_attack_score": 0.68,
            "leaderboard_target_leader_score": 1.30,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    )


def validate_grid_object_extraction_report(
    report: GridObjectExtractionReport | Mapping[str, Any],
) -> Dict[str, Any]:
    data = report.to_dict() if isinstance(report, GridObjectExtractionReport) else dict(report)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), Mapping) else {}
    objects = data.get("objects") if isinstance(data.get("objects"), list) else []

    object_checks = []
    for obj in objects:
        obj_metadata = obj.get("metadata") if isinstance(obj.get("metadata"), Mapping) else {}
        object_checks.append(
            obj.get("status") == "GRID_OBJECT_READY"
            and isinstance(obj.get("object_id"), str)
            and isinstance(obj.get("color"), int)
            and isinstance(obj.get("cells"), list)
            and len(obj.get("cells")) >= 1
            and isinstance(obj.get("area"), int)
            and obj.get("area") == len(obj.get("cells"))
            and isinstance(obj.get("bounding_box"), Mapping)
            and isinstance(obj.get("centroid"), Mapping)
            and isinstance(obj.get("touches_border"), bool)
            and isinstance(obj.get("mask"), list)
            and isinstance(obj.get("signature"), str)
            and obj_metadata.get("public_safe") is True
            and obj_metadata.get("deterministic") is True
            and obj_metadata.get("local_only") is True
            and obj_metadata.get("dry_run_only") is True
            and obj_metadata.get("agentic_state_feature") is True
            and obj_metadata.get("external_api_dependency") is False
            and obj_metadata.get("contains_api_keys") is False
            and obj_metadata.get("kaggle_submission_sent") is False
            and obj_metadata.get("private_core_exposure") is False
        )

    checks = {
        "status_ready": data.get("status") == "GRID_OBJECT_EXTRACTION_READY",
        "extraction_id_present": isinstance(data.get("extraction_id"), str) and bool(data.get("extraction_id")),
        "source_grid_valid": _grid_data_is_valid(data.get("source_grid")),
        "shape_present": isinstance(data.get("source_grid_shape"), Mapping),
        "grid_signature_present": isinstance(data.get("source_grid_signature"), str) and bool(data.get("source_grid_signature")),
        "background_color_valid": isinstance(data.get("background_color"), int),
        "connectivity_valid": data.get("connectivity") in (4, 8),
        "include_background_bool": isinstance(data.get("include_background"), bool),
        "color_inventory_present": isinstance(data.get("color_inventory"), Mapping),
        "object_count_valid": isinstance(data.get("object_count"), int) and data.get("object_count") == len(objects),
        "object_density_valid": isinstance(data.get("object_density"), float) and 0.0 <= data.get("object_density") <= 1.0,
        "objects_valid": bool(object_checks) and all(object_checks),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
        "metadata_score_oriented": metadata.get("score_oriented") is True,
        "metadata_prize_oriented_solver_target": metadata.get("prize_oriented_solver_target") is True,
        "metadata_agentic_state_feature": metadata.get("agentic_state_feature") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
    }

    valid = all(checks.values())

    return {
        "status": "GRID_OBJECT_EXTRACTION_VALID" if valid else "GRID_OBJECT_EXTRACTION_INVALID",
        "valid": valid,
        "checks": checks,
        "extraction_id": data.get("extraction_id"),
        "object_count": data.get("object_count"),
        "object_density": data.get("object_density"),
        "signature": data.get("signature"),
    }


def _grid_data_is_valid(value: Any) -> bool:
    try:
        normalize_grid(value)
        return True
    except Exception:
        return False


def build_grid_object_extractor_smoke_grid() -> List[List[int]]:
    return [
        [0, 1, 1, 0],
        [0, 1, 0, 2],
        [3, 0, 2, 2],
    ]


def run_grid_object_extractor_pipeline() -> Dict[str, Any]:
    report = extract_grid_objects(build_grid_object_extractor_smoke_grid(), background_color=0, connectivity=4)
    validation = validate_grid_object_extraction_report(report)

    return {
        "status": "GRID_OBJECT_EXTRACTOR_PIPELINE_READY",
        "extractor_status": report.status,
        "validation_status": validation["status"],
        "extraction_report": report.to_dict(),
        "validation": validation,
        "object_count": report.object_count,
        "object_density": report.object_density,
        "signature": report.signature,
        "metadata": {
            "source": "grid_object_extractor_v1",
            "milestone": "Milestone #4",
            "task": "Task 2",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "agentic_state_feature": True,
            "leaderboard_target_top_10_entry_score": 0.60,
            "leaderboard_target_top_5_score": 0.65,
            "leaderboard_target_podium_attack_score": 0.68,
            "leaderboard_target_leader_score": 1.30,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    }


def render_grid_object_extractor_markdown(payload: Mapping[str, Any]) -> str:
    data = dict(payload)
    report = data["extraction_report"]

    lines = [
        "# ARC-AGI-3 Milestone #4 Task 2 — Grid Object Extractor v1 Smoke",
        "",
        f"Status: {data['status']}",
        f"Extractor status: {data['extractor_status']}",
        f"Validation status: {data['validation_status']}",
        f"Extraction ID: {report['extraction_id']}",
        f"Object count: {data['object_count']}",
        f"Object density: {data['object_density']}",
        f"Signature: {data['signature']}",
        "",
        "## Objects",
        "",
    ]

    for obj in report["objects"]:
        lines.extend(
            [
                f"### {obj['object_id']}",
                "",
                f"- color={obj['color']}",
                f"- area={obj['area']}",
                f"- bbox={obj['bounding_box']}",
                f"- centroid={obj['centroid']}",
                f"- touches_border={str(obj['touches_border']).lower()}",
                f"- signature={obj['signature']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- local_only=true",
            "- dry_run_only=true",
            "- score_oriented=true",
            "- prize_oriented_solver_target=true",
            "- agentic_state_feature=true",
            "- external_api_dependency=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_grid_object_extractor_artifacts(
    payload: Optional[Mapping[str, Any]] = None,
    *,
    output_dir: str = "examples/milestone-4/grid-object-extractor-v1",
) -> Dict[str, str]:
    data = dict(payload or run_grid_object_extractor_pipeline())
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "grid-object-extractor-v1-smoke.json"
    markdown_path = output_path / "grid-object-extractor-v1-smoke.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_grid_object_extractor_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
