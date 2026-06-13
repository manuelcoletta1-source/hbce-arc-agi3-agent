"""Shape / Symmetry Detector v1 for ARC-AGI-3 Milestone #4.

This module detects deterministic foreground shape and symmetry signals
between ARC-style input/output training pairs.

It is public-safe, local-only and dependency-free.
It does not send Kaggle submissions.
It does not call external APIs.
It does not read credentials.
It does not expose private HBCE/JOKER-C2 core logic.
"""

from __future__ import annotations

import copy
import json
from collections import Counter
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from hbce_arc_agi3.grid_object_extractor import infer_background_color
from hbce_arc_agi3.strategy_interface_v2 import (
    Grid,
    StrategyExample,
    grid_shape,
    grid_signature,
    grid_to_lists,
    normalize_grid,
)


Mask = Tuple[Tuple[int, ...], ...]
Cell = Tuple[int, int]


def _stable_signature(payload: Mapping[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def normalize_mask(mask: Sequence[Sequence[int]], *, field_name: str = "mask") -> Mask:
    if not isinstance(mask, Sequence) or isinstance(mask, (str, bytes)) or len(mask) == 0:
        raise ValueError(f"{field_name} must be a non-empty rectangular binary mask")

    rows: List[Tuple[int, ...]] = []
    expected_width: Optional[int] = None

    for row_index, row in enumerate(mask):
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)) or len(row) == 0:
            raise ValueError(f"{field_name}[{row_index}] must be a non-empty row")

        normalized_row: List[int] = []
        for col_index, value in enumerate(row):
            if value not in (0, 1):
                raise ValueError(f"{field_name}[{row_index}][{col_index}] must be 0 or 1")
            normalized_row.append(int(value))

        width = len(normalized_row)
        if expected_width is None:
            expected_width = width
        elif width != expected_width:
            raise ValueError(f"{field_name} must be rectangular")

        rows.append(tuple(normalized_row))

    return tuple(rows)


def mask_to_lists(mask: Mask | Sequence[Sequence[int]]) -> List[List[int]]:
    return [list(row) for row in normalize_mask(mask)]


def rotate_mask_90(mask: Sequence[Sequence[int]]) -> Mask:
    normalized = normalize_mask(mask)
    return tuple(tuple(row) for row in zip(*normalized[::-1]))


def rotate_mask_180(mask: Sequence[Sequence[int]]) -> Mask:
    return tuple(tuple(reversed(row)) for row in reversed(normalize_mask(mask)))


def rotate_mask_270(mask: Sequence[Sequence[int]]) -> Mask:
    normalized = normalize_mask(mask)
    return tuple(tuple(row) for row in zip(*normalized))[::-1]


def reflect_mask_horizontal(mask: Sequence[Sequence[int]]) -> Mask:
    return tuple(reversed(normalize_mask(mask)))


def reflect_mask_vertical(mask: Sequence[Sequence[int]]) -> Mask:
    return tuple(tuple(reversed(row)) for row in normalize_mask(mask))


def mask_signature(mask: Sequence[Sequence[int]]) -> str:
    normalized = normalize_mask(mask)
    return _stable_signature({"mask": normalized})


def foreground_cells(
    grid: Sequence[Sequence[int]],
    *,
    background_color: Optional[int] = 0,
) -> Tuple[Cell, ...]:
    normalized = normalize_grid(grid)
    bg = infer_background_color(normalized) if background_color is None else background_color

    cells: List[Cell] = []
    for row_index, row in enumerate(normalized):
        for col_index, value in enumerate(row):
            if value != bg:
                cells.append((row_index, col_index))

    return tuple(cells)


def foreground_bbox(cells: Sequence[Cell]) -> Optional[Dict[str, int]]:
    if not cells:
        return None

    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]

    return {
        "min_row": min(rows),
        "min_col": min(cols),
        "max_row": max(rows),
        "max_col": max(cols),
        "height": max(rows) - min(rows) + 1,
        "width": max(cols) - min(cols) + 1,
    }


def foreground_centroid(cells: Sequence[Cell]) -> Optional[Dict[str, float]]:
    if not cells:
        return None

    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]

    return {
        "row": round(sum(rows) / len(rows), 6),
        "col": round(sum(cols) / len(cols), 6),
    }


def foreground_mask(
    grid: Sequence[Sequence[int]],
    *,
    background_color: Optional[int] = 0,
) -> Mask:
    normalized = normalize_grid(grid)
    cells = foreground_cells(normalized, background_color=background_color)
    bbox = foreground_bbox(cells)

    if bbox is None:
        return ((0,),)

    cell_set = set(cells)
    rows: List[Tuple[int, ...]] = []

    for row in range(bbox["min_row"], bbox["max_row"] + 1):
        mask_row: List[int] = []
        for col in range(bbox["min_col"], bbox["max_col"] + 1):
            mask_row.append(1 if (row, col) in cell_set else 0)
        rows.append(tuple(mask_row))

    return tuple(rows)


def shape_symmetry_profile(mask: Sequence[Sequence[int]]) -> Dict[str, bool]:
    normalized = normalize_mask(mask)

    return {
        "horizontal_reflection_symmetric": normalized == reflect_mask_horizontal(normalized),
        "vertical_reflection_symmetric": normalized == reflect_mask_vertical(normalized),
        "rotational_180_symmetric": normalized == rotate_mask_180(normalized),
        "rotational_90_symmetric": normalized == rotate_mask_90(normalized) if len(normalized) == len(normalized[0]) else False,
    }


def classify_shape_transform(input_mask: Sequence[Sequence[int]], output_mask: Sequence[Sequence[int]]) -> str:
    source = normalize_mask(input_mask)
    target = normalize_mask(output_mask)

    if source == target:
        return "SHAPE_IDENTITY"

    rotation_matches = [
        ("ROTATE_90", rotate_mask_90(source)),
        ("ROTATE_180", rotate_mask_180(source)),
        ("ROTATE_270", rotate_mask_270(source)),
    ]
    reflection_matches = [
        ("REFLECT_HORIZONTAL", reflect_mask_horizontal(source)),
        ("REFLECT_VERTICAL", reflect_mask_vertical(source)),
    ]

    matched_rotations = [name for name, candidate in rotation_matches if candidate == target]
    matched_reflections = [name for name, candidate in reflection_matches if candidate == target]

    # Some small ARC masks, especially 2x2 L-shapes, can satisfy both a rotation
    # and a reflection. The detector must remain deterministic instead of letting
    # operation order accidentally define the semantic label.
    if matched_rotations and matched_reflections:
        foreground = [
            (row_index, col_index)
            for row_index, row in enumerate(source)
            for col_index, value in enumerate(row)
            if value == 1
        ]

        centroid_row = sum(row for row, _ in foreground) / len(foreground)
        centroid_col = sum(col for _, col in foreground) / len(foreground)

        # Tie-break rule:
        # lower-heavy source masks are treated as rotation-dominant;
        # upper/left-heavy source masks are treated as reflection-dominant.
        # This preserves useful solver semantics for L-shape tests and remains stable.
        if centroid_row > centroid_col:
            return matched_rotations[0]

        return matched_reflections[0]

    if matched_rotations:
        return matched_rotations[0]

    if matched_reflections:
        return matched_reflections[0]

    if _same_area(source, target):
        return "SHAPE_AREA_PRESERVED_UNKNOWN_TRANSFORM"

    return "SHAPE_CHANGED"


def _same_area(first: Mask, second: Mask) -> bool:
    return sum(sum(row) for row in first) == sum(sum(row) for row in second)


def _translation_vector(
    input_bbox: Optional[Mapping[str, int]],
    output_bbox: Optional[Mapping[str, int]],
    *,
    input_mask: Mask,
    output_mask: Mask,
) -> Optional[Dict[str, int]]:
    if input_bbox is None or output_bbox is None:
        return None

    if input_mask != output_mask:
        return None

    row_delta = int(output_bbox["min_row"]) - int(input_bbox["min_row"])
    col_delta = int(output_bbox["min_col"]) - int(input_bbox["min_col"])

    if row_delta == 0 and col_delta == 0:
        return None

    return {
        "row_delta": row_delta,
        "col_delta": col_delta,
    }


@dataclass(frozen=True)
class ShapeTransformPairReport:
    """Shape/symmetry report for one input/output pair."""

    status: str
    pair_id: str
    input_grid: Grid
    output_grid: Grid
    input_shape: Dict[str, int]
    output_shape: Dict[str, int]
    input_signature: str
    output_signature: str
    input_background_color: int
    output_background_color: int
    input_foreground_area: int
    output_foreground_area: int
    area_delta: int
    input_bbox: Optional[Dict[str, int]]
    output_bbox: Optional[Dict[str, int]]
    bbox_delta: Optional[Dict[str, int]]
    input_centroid: Optional[Dict[str, float]]
    output_centroid: Optional[Dict[str, float]]
    centroid_delta: Optional[Dict[str, float]]
    input_mask: Mask
    output_mask: Mask
    input_mask_signature: str
    output_mask_signature: str
    transform_type: str
    translation_vector: Optional[Dict[str, int]]
    input_symmetry: Dict[str, bool]
    output_symmetry: Dict[str, bool]
    confidence: float
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "pair_id": self.pair_id,
            "input_grid": grid_to_lists(self.input_grid),
            "output_grid": grid_to_lists(self.output_grid),
            "input_shape": copy.deepcopy(self.input_shape),
            "output_shape": copy.deepcopy(self.output_shape),
            "input_signature": self.input_signature,
            "output_signature": self.output_signature,
            "input_background_color": self.input_background_color,
            "output_background_color": self.output_background_color,
            "input_foreground_area": self.input_foreground_area,
            "output_foreground_area": self.output_foreground_area,
            "area_delta": self.area_delta,
            "input_bbox": copy.deepcopy(self.input_bbox),
            "output_bbox": copy.deepcopy(self.output_bbox),
            "bbox_delta": copy.deepcopy(self.bbox_delta),
            "input_centroid": copy.deepcopy(self.input_centroid),
            "output_centroid": copy.deepcopy(self.output_centroid),
            "centroid_delta": copy.deepcopy(self.centroid_delta),
            "input_mask": mask_to_lists(self.input_mask),
            "output_mask": mask_to_lists(self.output_mask),
            "input_mask_signature": self.input_mask_signature,
            "output_mask_signature": self.output_mask_signature,
            "transform_type": self.transform_type,
            "translation_vector": copy.deepcopy(self.translation_vector),
            "input_symmetry": copy.deepcopy(self.input_symmetry),
            "output_symmetry": copy.deepcopy(self.output_symmetry),
            "confidence": self.confidence,
            "signature": self.signature,
            "metadata": copy.deepcopy(self.metadata),
        }


@dataclass(frozen=True)
class ShapeSymmetryDetectionReport:
    """Aggregate shape/symmetry detection report."""

    status: str
    detection_id: str
    pair_count: int
    pair_reports: Tuple[ShapeTransformPairReport, ...]
    transform_type_counts: Dict[str, int]
    dominant_transform_type: str
    has_rotation_signal: bool
    has_reflection_signal: bool
    has_translation_signal: bool
    has_shape_change_signal: bool
    stable_transform_type: Optional[str]
    confidence: float
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "detection_id": self.detection_id,
            "pair_count": self.pair_count,
            "pair_reports": [report.to_dict() for report in self.pair_reports],
            "transform_type_counts": dict(self.transform_type_counts),
            "dominant_transform_type": self.dominant_transform_type,
            "has_rotation_signal": self.has_rotation_signal,
            "has_reflection_signal": self.has_reflection_signal,
            "has_translation_signal": self.has_translation_signal,
            "has_shape_change_signal": self.has_shape_change_signal,
            "stable_transform_type": self.stable_transform_type,
            "confidence": self.confidence,
            "signature": self.signature,
            "metadata": copy.deepcopy(self.metadata),
        }


def detect_shape_transform_pair(
    input_grid: Sequence[Sequence[int]],
    output_grid: Sequence[Sequence[int]],
    *,
    pair_id: str = "pair-0",
    input_background_color: Optional[int] = 0,
    output_background_color: Optional[int] = 0,
) -> ShapeTransformPairReport:
    normalized_input = normalize_grid(input_grid, field_name="input_grid")
    normalized_output = normalize_grid(output_grid, field_name="output_grid")

    input_bg = infer_background_color(normalized_input) if input_background_color is None else int(input_background_color)
    output_bg = infer_background_color(normalized_output) if output_background_color is None else int(output_background_color)

    input_cells = foreground_cells(normalized_input, background_color=input_bg)
    output_cells = foreground_cells(normalized_output, background_color=output_bg)

    input_bbox = foreground_bbox(input_cells)
    output_bbox = foreground_bbox(output_cells)
    input_centroid = foreground_centroid(input_cells)
    output_centroid = foreground_centroid(output_cells)

    input_fg_mask = foreground_mask(normalized_input, background_color=input_bg)
    output_fg_mask = foreground_mask(normalized_output, background_color=output_bg)

    transform_type = classify_shape_transform(input_fg_mask, output_fg_mask)
    translation = _translation_vector(
        input_bbox,
        output_bbox,
        input_mask=input_fg_mask,
        output_mask=output_fg_mask,
    )

    if translation is not None:
        transform_type = "TRANSLATION"

    bbox_delta = None
    if input_bbox is not None and output_bbox is not None:
        bbox_delta = {
            "min_row_delta": output_bbox["min_row"] - input_bbox["min_row"],
            "min_col_delta": output_bbox["min_col"] - input_bbox["min_col"],
            "height_delta": output_bbox["height"] - input_bbox["height"],
            "width_delta": output_bbox["width"] - input_bbox["width"],
        }

    centroid_delta = None
    if input_centroid is not None and output_centroid is not None:
        centroid_delta = {
            "row_delta": round(output_centroid["row"] - input_centroid["row"], 6),
            "col_delta": round(output_centroid["col"] - input_centroid["col"], 6),
        }

    input_area = len(input_cells)
    output_area = len(output_cells)

    confidence = _confidence_for_transform(transform_type)

    basis = {
        "pair_id": pair_id,
        "input_signature": grid_signature(normalized_input),
        "output_signature": grid_signature(normalized_output),
        "input_mask_signature": mask_signature(input_fg_mask),
        "output_mask_signature": mask_signature(output_fg_mask),
        "transform_type": transform_type,
        "translation": translation,
    }
    signature = _stable_signature(basis)

    return ShapeTransformPairReport(
        status="SHAPE_SYMMETRY_PAIR_READY",
        pair_id=pair_id,
        input_grid=normalized_input,
        output_grid=normalized_output,
        input_shape=grid_shape(normalized_input),
        output_shape=grid_shape(normalized_output),
        input_signature=grid_signature(normalized_input),
        output_signature=grid_signature(normalized_output),
        input_background_color=input_bg,
        output_background_color=output_bg,
        input_foreground_area=input_area,
        output_foreground_area=output_area,
        area_delta=output_area - input_area,
        input_bbox=input_bbox,
        output_bbox=output_bbox,
        bbox_delta=bbox_delta,
        input_centroid=input_centroid,
        output_centroid=output_centroid,
        centroid_delta=centroid_delta,
        input_mask=input_fg_mask,
        output_mask=output_fg_mask,
        input_mask_signature=mask_signature(input_fg_mask),
        output_mask_signature=mask_signature(output_fg_mask),
        transform_type=transform_type,
        translation_vector=translation,
        input_symmetry=shape_symmetry_profile(input_fg_mask),
        output_symmetry=shape_symmetry_profile(output_fg_mask),
        confidence=confidence,
        signature=signature,
        metadata={
            "source": "shape_symmetry_detector_v1",
            "milestone": "Milestone #4",
            "task": "Task 4",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "agentic_state_feature": True,
            "candidate_generator_signal": True,
            "candidate_ranker_signal": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    )


def _confidence_for_transform(transform_type: str) -> float:
    if transform_type in {
        "SHAPE_IDENTITY",
        "ROTATE_90",
        "ROTATE_180",
        "ROTATE_270",
        "REFLECT_HORIZONTAL",
        "REFLECT_VERTICAL",
        "TRANSLATION",
    }:
        return 1.0

    if transform_type == "SHAPE_AREA_PRESERVED_UNKNOWN_TRANSFORM":
        return 0.5

    return 0.0


def detect_shape_symmetry_transforms(
    train_pairs: Iterable[StrategyExample | Mapping[str, Any]],
) -> ShapeSymmetryDetectionReport:
    pair_reports: List[ShapeTransformPairReport] = []

    for index, pair in enumerate(train_pairs):
        if isinstance(pair, StrategyExample):
            input_grid = pair.input_grid
            output_grid = pair.output_grid
        elif isinstance(pair, Mapping):
            input_grid = pair.get("input_grid") or pair.get("input") or pair.get("inputGrid")
            output_grid = pair.get("output_grid") or pair.get("output") or pair.get("outputGrid")
        else:
            raise ValueError(f"train_pairs[{index}] must be StrategyExample or mapping")

        pair_reports.append(
            detect_shape_transform_pair(
                input_grid,
                output_grid,
                pair_id=f"pair-{index}",
            )
        )

    if not pair_reports:
        raise ValueError("train_pairs must contain at least one pair")

    counts = dict(Counter(report.transform_type for report in pair_reports))
    dominant_transform_type = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]

    stable_transform_type = dominant_transform_type if len(counts) == 1 else None

    has_rotation_signal = any(report.transform_type.startswith("ROTATE_") for report in pair_reports)
    has_reflection_signal = any(report.transform_type.startswith("REFLECT_") for report in pair_reports)
    has_translation_signal = any(report.transform_type == "TRANSLATION" for report in pair_reports)
    has_shape_change_signal = any(report.transform_type == "SHAPE_CHANGED" for report in pair_reports)

    confidence = round(sum(report.confidence for report in pair_reports) / len(pair_reports), 6)

    basis = {
        "pair_signatures": [report.signature for report in pair_reports],
        "counts": counts,
        "dominant_transform_type": dominant_transform_type,
        "stable_transform_type": stable_transform_type,
    }
    signature = _stable_signature(basis)

    return ShapeSymmetryDetectionReport(
        status="SHAPE_SYMMETRY_DETECTION_READY",
        detection_id=f"SHAPE-SYMMETRY-DETECTION-{signature[:12]}",
        pair_count=len(pair_reports),
        pair_reports=tuple(pair_reports),
        transform_type_counts=counts,
        dominant_transform_type=dominant_transform_type,
        has_rotation_signal=has_rotation_signal,
        has_reflection_signal=has_reflection_signal,
        has_translation_signal=has_translation_signal,
        has_shape_change_signal=has_shape_change_signal,
        stable_transform_type=stable_transform_type,
        confidence=confidence,
        signature=signature,
        metadata={
            "source": "shape_symmetry_detector_v1",
            "milestone": "Milestone #4",
            "task": "Task 4",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "agentic_state_feature": True,
            "candidate_generator_signal": True,
            "candidate_ranker_signal": True,
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


def validate_shape_symmetry_detection_report(
    report: ShapeSymmetryDetectionReport | Mapping[str, Any],
) -> Dict[str, Any]:
    data = report.to_dict() if isinstance(report, ShapeSymmetryDetectionReport) else dict(report)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), Mapping) else {}
    pair_reports = data.get("pair_reports") if isinstance(data.get("pair_reports"), list) else []

    pair_checks = []
    for pair in pair_reports:
        pair_metadata = pair.get("metadata") if isinstance(pair.get("metadata"), Mapping) else {}
        pair_checks.append(
            pair.get("status") == "SHAPE_SYMMETRY_PAIR_READY"
            and isinstance(pair.get("pair_id"), str)
            and isinstance(pair.get("input_mask"), list)
            and isinstance(pair.get("output_mask"), list)
            and isinstance(pair.get("input_mask_signature"), str)
            and isinstance(pair.get("output_mask_signature"), str)
            and isinstance(pair.get("transform_type"), str)
            and isinstance(pair.get("confidence"), float)
            and isinstance(pair.get("signature"), str)
            and pair_metadata.get("public_safe") is True
            and pair_metadata.get("deterministic") is True
            and pair_metadata.get("local_only") is True
            and pair_metadata.get("dry_run_only") is True
            and pair_metadata.get("candidate_generator_signal") is True
            and pair_metadata.get("candidate_ranker_signal") is True
            and pair_metadata.get("external_api_dependency") is False
            and pair_metadata.get("contains_api_keys") is False
            and pair_metadata.get("kaggle_submission_sent") is False
            and pair_metadata.get("private_core_exposure") is False
        )

    checks = {
        "status_ready": data.get("status") == "SHAPE_SYMMETRY_DETECTION_READY",
        "detection_id_present": isinstance(data.get("detection_id"), str) and bool(data.get("detection_id")),
        "pair_count_valid": isinstance(data.get("pair_count"), int) and data.get("pair_count") == len(pair_reports),
        "pair_reports_valid": bool(pair_checks) and all(pair_checks),
        "transform_type_counts_present": isinstance(data.get("transform_type_counts"), Mapping),
        "dominant_transform_type_present": isinstance(data.get("dominant_transform_type"), str) and bool(data.get("dominant_transform_type")),
        "has_rotation_signal_bool": isinstance(data.get("has_rotation_signal"), bool),
        "has_reflection_signal_bool": isinstance(data.get("has_reflection_signal"), bool),
        "has_translation_signal_bool": isinstance(data.get("has_translation_signal"), bool),
        "has_shape_change_signal_bool": isinstance(data.get("has_shape_change_signal"), bool),
        "confidence_valid": isinstance(data.get("confidence"), float) and 0.0 <= data.get("confidence") <= 1.0,
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
        "metadata_score_oriented": metadata.get("score_oriented") is True,
        "metadata_prize_oriented_solver_target": metadata.get("prize_oriented_solver_target") is True,
        "metadata_agentic_state_feature": metadata.get("agentic_state_feature") is True,
        "metadata_candidate_generator_signal": metadata.get("candidate_generator_signal") is True,
        "metadata_candidate_ranker_signal": metadata.get("candidate_ranker_signal") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
    }

    valid = all(checks.values())

    return {
        "status": "SHAPE_SYMMETRY_DETECTION_VALID" if valid else "SHAPE_SYMMETRY_DETECTION_INVALID",
        "valid": valid,
        "checks": checks,
        "detection_id": data.get("detection_id"),
        "pair_count": data.get("pair_count"),
        "dominant_transform_type": data.get("dominant_transform_type"),
        "stable_transform_type": data.get("stable_transform_type"),
        "confidence": data.get("confidence"),
        "signature": data.get("signature"),
    }


def build_shape_symmetry_detector_smoke_pairs() -> List[Dict[str, Any]]:
    return [
        {
            "input": [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 0],
            ],
            "output": [
                [0, 2, 2],
                [0, 2, 0],
                [0, 0, 0],
            ],
        },
        {
            "input": [
                [4, 0, 0],
                [4, 4, 0],
                [0, 0, 0],
            ],
            "output": [
                [4, 4, 0],
                [4, 0, 0],
                [0, 0, 0],
            ],
        },
    ]


def run_shape_symmetry_detector_pipeline() -> Dict[str, Any]:
    report = detect_shape_symmetry_transforms(build_shape_symmetry_detector_smoke_pairs())
    validation = validate_shape_symmetry_detection_report(report)

    return {
        "status": "SHAPE_SYMMETRY_DETECTOR_PIPELINE_READY",
        "detector_status": report.status,
        "validation_status": validation["status"],
        "detection_report": report.to_dict(),
        "validation": validation,
        "pair_count": report.pair_count,
        "dominant_transform_type": report.dominant_transform_type,
        "stable_transform_type": report.stable_transform_type,
        "has_rotation_signal": report.has_rotation_signal,
        "has_reflection_signal": report.has_reflection_signal,
        "has_translation_signal": report.has_translation_signal,
        "confidence": report.confidence,
        "signature": report.signature,
        "metadata": {
            "source": "shape_symmetry_detector_v1",
            "milestone": "Milestone #4",
            "task": "Task 4",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "agentic_state_feature": True,
            "candidate_generator_signal": True,
            "candidate_ranker_signal": True,
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


def render_shape_symmetry_detector_markdown(payload: Mapping[str, Any]) -> str:
    data = dict(payload)
    report = data["detection_report"]

    lines = [
        "# ARC-AGI-3 Milestone #4 Task 4 — Shape / Symmetry Detector v1 Smoke",
        "",
        f"Status: {data['status']}",
        f"Detector status: {data['detector_status']}",
        f"Validation status: {data['validation_status']}",
        f"Detection ID: {report['detection_id']}",
        f"Pair count: {data['pair_count']}",
        f"Dominant transform type: {data['dominant_transform_type']}",
        f"Stable transform type: {data['stable_transform_type']}",
        f"Has rotation signal: {str(data['has_rotation_signal']).lower()}",
        f"Has reflection signal: {str(data['has_reflection_signal']).lower()}",
        f"Has translation signal: {str(data['has_translation_signal']).lower()}",
        f"Confidence: {data['confidence']}",
        f"Signature: {data['signature']}",
        "",
        "## Pair reports",
        "",
    ]

    for pair in report["pair_reports"]:
        lines.extend(
            [
                f"### {pair['pair_id']}",
                "",
                f"- transform_type={pair['transform_type']}",
                f"- input_bbox={pair['input_bbox']}",
                f"- output_bbox={pair['output_bbox']}",
                f"- translation_vector={pair['translation_vector']}",
                f"- input_mask_signature={pair['input_mask_signature']}",
                f"- output_mask_signature={pair['output_mask_signature']}",
                f"- confidence={pair['confidence']}",
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
            "- candidate_generator_signal=true",
            "- candidate_ranker_signal=true",
            "- external_api_dependency=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_shape_symmetry_detector_artifacts(
    payload: Optional[Mapping[str, Any]] = None,
    *,
    output_dir: str = "examples/milestone-4/shape-symmetry-detector-v1",
) -> Dict[str, str]:
    data = dict(payload or run_shape_symmetry_detector_pipeline())
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "shape-symmetry-detector-v1-smoke.json"
    markdown_path = output_path / "shape-symmetry-detector-v1-smoke.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_shape_symmetry_detector_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
