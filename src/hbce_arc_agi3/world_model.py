"""World-model construction for the HBCE ARC-AGI-3 public baseline."""

from __future__ import annotations

from typing import Any, Dict


def build_world_model(observation: Dict[str, Any]) -> Dict[str, Any]:
    grid = observation.get("grid") or []
    objects = observation.get("objects") or []
    return {
        "status": "WORLD_MODEL_READY",
        "grid_height": len(grid),
        "grid_width": len(grid[0]) if grid and isinstance(grid[0], list) else 0,
        "object_count": len(objects),
        "goal_hint": observation.get("goal_hint"),
    }


# === HBCE ARC AGI3 WORLD MODEL UPGRADE v1 START ===


from dataclasses import asdict as _hbce_world_asdict
from dataclasses import dataclass as _hbce_world_dataclass
from typing import Any as _HbceWorldAny
from typing import Dict as _HbceWorldDict
from typing import List as _HbceWorldList


@_hbce_world_dataclass(frozen=True)
class HbceWorldModel:
    """Minimal symbolic world model for ARC-AGI-3 public baseline."""

    status: str
    task_id: str
    dimensions: _HbceWorldDict[str, int]
    symbol_inventory: _HbceWorldDict[str, int]
    object_count: int
    non_empty_cell_count: int
    density: float
    inferred_properties: _HbceWorldList[str]
    uncertainty_markers: _HbceWorldList[str]
    metadata: _HbceWorldDict[str, _HbceWorldAny]

    def to_dict(self) -> _HbceWorldDict[str, _HbceWorldAny]:
        return _hbce_world_asdict(self)


def build_world_model_from_observation(
    observation: _HbceWorldDict[str, _HbceWorldAny] | None = None,
) -> HbceWorldModel:
    """Build a deterministic world model from an observer dictionary."""

    observation = observation or {}

    width = int(observation.get("width") or 0)
    height = int(observation.get("height") or 0)
    cell_count = int(observation.get("cell_count") or 0)
    symbols = observation.get("symbols") if isinstance(observation.get("symbols"), dict) else {}
    objects = observation.get("objects") if isinstance(observation.get("objects"), list) else []
    non_empty_cells = (
        observation.get("non_empty_cells")
        if isinstance(observation.get("non_empty_cells"), list)
        else []
    )
    uncertainty = (
        observation.get("uncertainty_markers")
        if isinstance(observation.get("uncertainty_markers"), list)
        else []
    )

    non_empty_count = len(non_empty_cells)
    density = round(non_empty_count / cell_count, 6) if cell_count else 0.0

    inferred_properties: _HbceWorldList[str] = []
    if width and height:
        inferred_properties.append("GRID_DIMENSIONS_KNOWN")
    if symbols:
        inferred_properties.append("SYMBOL_INVENTORY_READY")
    if non_empty_count:
        inferred_properties.append("NON_EMPTY_CELLS_DETECTED")
    if objects:
        inferred_properties.append("OBJECT_LIST_AVAILABLE")
    if not inferred_properties:
        inferred_properties.append("MINIMAL_EMPTY_MODEL")

    return HbceWorldModel(
        status="WORLD_MODEL_READY",
        task_id=str(observation.get("task_id") or "anonymous-task"),
        dimensions={"width": width, "height": height, "cell_count": cell_count},
        symbol_inventory=dict(sorted((str(k), int(v)) for k, v in symbols.items())),
        object_count=len(objects),
        non_empty_cell_count=non_empty_count,
        density=density,
        inferred_properties=inferred_properties,
        uncertainty_markers=list(uncertainty),
        metadata={
            "source": "world_model_upgrade_v1",
            "public_safe": True,
            "derived_from": "observer_upgrade_v1",
        },
    )


def build_symbolic_world_model(
    observation: _HbceWorldDict[str, _HbceWorldAny] | None = None,
) -> _HbceWorldDict[str, _HbceWorldAny]:
    """Compatibility wrapper returning a plain dictionary world model."""

    return build_world_model_from_observation(observation).to_dict()


# === HBCE ARC AGI3 WORLD MODEL UPGRADE v1 END ===
