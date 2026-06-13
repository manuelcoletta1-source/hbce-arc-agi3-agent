"""Color Transform Detector v1 for ARC-AGI-3 Milestone #4.

This module detects deterministic color transformation signals between
ARC-style input/output training pairs.

It is public-safe, local-only and dependency-free.
It does not send Kaggle submissions.
It does not call external APIs.
It does not read credentials.
It does not expose private HBCE/JOKER-C2 core logic.
"""

from __future__ import annotations

import copy
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from hbce_arc_agi3.grid_object_extractor import color_inventory, infer_background_color
from hbce_arc_agi3.strategy_interface_v2 import (
    Grid,
    StrategyExample,
    grid_shape,
    grid_signature,
    grid_to_lists,
    normalize_grid,
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


@dataclass(frozen=True)
class ColorMapping:
    """Dominant deterministic color mapping candidate."""

    source_color: int
    target_color: int
    count: int
    source_total: int
    confidence: float
    relation: str
    signature: str

    @classmethod
    def build(
        cls,
        *,
        source_color: int,
        target_color: int,
        count: int,
        source_total: int,
    ) -> "ColorMapping":
        if source_total <= 0:
            raise ValueError("source_total must be positive")

        confidence = round(count / source_total, 6)
        relation = "COLOR_PRESERVED" if source_color == target_color else "COLOR_REPLACED"

        basis = {
            "source_color": source_color,
            "target_color": target_color,
            "count": count,
            "source_total": source_total,
            "confidence": confidence,
            "relation": relation,
        }

        return cls(
            source_color=source_color,
            target_color=target_color,
            count=count,
            source_total=source_total,
            confidence=confidence,
            relation=relation,
            signature=_stable_signature(basis),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ColorTransformPairReport:
    """Color transformation report for one input/output training pair."""

    status: str
    pair_id: str
    input_grid: Grid
    output_grid: Grid
    input_shape: Dict[str, int]
    output_shape: Dict[str, int]
    input_signature: str
    output_signature: str
    shape_preserving: bool
    input_palette: Tuple[int, ...]
    output_palette: Tuple[int, ...]
    added_colors: Tuple[int, ...]
    removed_colors: Tuple[int, ...]
    preserved_colors: Tuple[int, ...]
    changed_source_colors: Tuple[int, ...]
    ambiguous_source_colors: Tuple[int, ...]
    ambiguous_target_colors: Tuple[int, ...]
    dominant_mappings: Tuple[ColorMapping, ...]
    background_mapping: Optional[ColorMapping]
    transform_type: str
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
            "shape_preserving": self.shape_preserving,
            "input_palette": list(self.input_palette),
            "output_palette": list(self.output_palette),
            "added_colors": list(self.added_colors),
            "removed_colors": list(self.removed_colors),
            "preserved_colors": list(self.preserved_colors),
            "changed_source_colors": list(self.changed_source_colors),
            "ambiguous_source_colors": list(self.ambiguous_source_colors),
            "ambiguous_target_colors": list(self.ambiguous_target_colors),
            "dominant_mappings": [mapping.to_dict() for mapping in self.dominant_mappings],
            "background_mapping": self.background_mapping.to_dict() if self.background_mapping else None,
            "transform_type": self.transform_type,
            "confidence": self.confidence,
            "signature": self.signature,
            "metadata": copy.deepcopy(self.metadata),
        }


@dataclass(frozen=True)
class ColorTransformDetectionReport:
    """Aggregated color transform detection report for one or more training pairs."""

    status: str
    detection_id: str
    pair_count: int
    pair_reports: Tuple[ColorTransformPairReport, ...]
    stable_mappings: Tuple[ColorMapping, ...]
    unstable_source_colors: Tuple[int, ...]
    global_input_palette: Tuple[int, ...]
    global_output_palette: Tuple[int, ...]
    global_added_colors: Tuple[int, ...]
    global_removed_colors: Tuple[int, ...]
    global_preserved_colors: Tuple[int, ...]
    has_ambiguous_mapping: bool
    has_palette_expansion: bool
    has_palette_reduction: bool
    transform_type: str
    confidence: float
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "detection_id": self.detection_id,
            "pair_count": self.pair_count,
            "pair_reports": [report.to_dict() for report in self.pair_reports],
            "stable_mappings": [mapping.to_dict() for mapping in self.stable_mappings],
            "unstable_source_colors": list(self.unstable_source_colors),
            "global_input_palette": list(self.global_input_palette),
            "global_output_palette": list(self.global_output_palette),
            "global_added_colors": list(self.global_added_colors),
            "global_removed_colors": list(self.global_removed_colors),
            "global_preserved_colors": list(self.global_preserved_colors),
            "has_ambiguous_mapping": self.has_ambiguous_mapping,
            "has_palette_expansion": self.has_palette_expansion,
            "has_palette_reduction": self.has_palette_reduction,
            "transform_type": self.transform_type,
            "confidence": self.confidence,
            "signature": self.signature,
            "metadata": copy.deepcopy(self.metadata),
        }


def _palette(grid: Grid) -> Tuple[int, ...]:
    return tuple(sorted(color_inventory(grid).keys()))


def _cellwise_mapping_counts(input_grid: Grid, output_grid: Grid) -> Dict[int, Counter[int]]:
    mapping_counts: Dict[int, Counter[int]] = defaultdict(Counter)

    for row_index, row in enumerate(input_grid):
        for col_index, source_color in enumerate(row):
            target_color = output_grid[row_index][col_index]
            mapping_counts[source_color][target_color] += 1

    return mapping_counts


def _dominant_mappings_from_counts(mapping_counts: Mapping[int, Counter[int]]) -> Tuple[ColorMapping, ...]:
    mappings: List[ColorMapping] = []

    for source_color, target_counter in sorted(mapping_counts.items()):
        source_total = sum(target_counter.values())
        target_color, count = sorted(
            target_counter.items(),
            key=lambda item: (-item[1], item[0]),
        )[0]

        mappings.append(
            ColorMapping.build(
                source_color=source_color,
                target_color=target_color,
                count=count,
                source_total=source_total,
            )
        )

    return tuple(mappings)


def _ambiguous_sources(mapping_counts: Mapping[int, Counter[int]]) -> Tuple[int, ...]:
    return tuple(
        sorted(source_color for source_color, targets in mapping_counts.items() if len(targets) > 1)
    )


def _ambiguous_targets(mappings: Iterable[ColorMapping]) -> Tuple[int, ...]:
    reverse: Dict[int, List[int]] = defaultdict(list)

    for mapping in mappings:
        reverse[mapping.target_color].append(mapping.source_color)

    return tuple(sorted(target for target, sources in reverse.items() if len(set(sources)) > 1))


def _classify_pair_transform(
    *,
    shape_preserving: bool,
    added_colors: Tuple[int, ...],
    removed_colors: Tuple[int, ...],
    changed_source_colors: Tuple[int, ...],
    ambiguous_source_colors: Tuple[int, ...],
) -> str:
    if not shape_preserving:
        return "SHAPE_CHANGED_PALETTE_ONLY"

    if ambiguous_source_colors:
        return "AMBIGUOUS_COLOR_MAPPING"

    # Solver-first precedence:
    # if a stable cell-wise source -> target mapping exists, classify it as a remap.
    # Added/removed palette colors can simply be the visible effect of that remap.
    if changed_source_colors and added_colors and removed_colors:
        return "COLOR_REMAP"

    if added_colors:
        return "PALETTE_EXPANSION"

    if removed_colors:
        return "PALETTE_REDUCTION"

    if changed_source_colors:
        return "COLOR_REMAP"

    return "COLOR_IDENTITY_OR_PRESERVED"


def detect_color_transform_pair(
    input_grid: Sequence[Sequence[int]],
    output_grid: Sequence[Sequence[int]],
    *,
    pair_id: str = "pair-0",
    input_background_color: Optional[int] = 0,
    output_background_color: Optional[int] = 0,
) -> ColorTransformPairReport:
    """Detect color transformation signals for one input/output pair."""

    normalized_input = normalize_grid(input_grid, field_name="input_grid")
    normalized_output = normalize_grid(output_grid, field_name="output_grid")

    input_shape = grid_shape(normalized_input)
    output_shape = grid_shape(normalized_output)
    shape_preserving = input_shape["height"] == output_shape["height"] and input_shape["width"] == output_shape["width"]

    input_palette = _palette(normalized_input)
    output_palette = _palette(normalized_output)

    input_set = set(input_palette)
    output_set = set(output_palette)

    added_colors = tuple(sorted(output_set - input_set))
    removed_colors = tuple(sorted(input_set - output_set))
    preserved_colors = tuple(sorted(input_set & output_set))

    dominant_mappings: Tuple[ColorMapping, ...] = tuple()
    ambiguous_sources: Tuple[int, ...] = tuple()
    ambiguous_targets: Tuple[int, ...] = tuple()
    changed_source_colors: Tuple[int, ...] = tuple()
    confidence = 0.0
    background_mapping: Optional[ColorMapping] = None

    if shape_preserving:
        counts = _cellwise_mapping_counts(normalized_input, normalized_output)
        dominant_mappings = _dominant_mappings_from_counts(counts)
        ambiguous_sources = _ambiguous_sources(counts)
        ambiguous_targets = _ambiguous_targets(dominant_mappings)
        changed_source_colors = tuple(
            sorted(mapping.source_color for mapping in dominant_mappings if mapping.source_color != mapping.target_color)
        )
        confidence = round(
            sum(mapping.confidence for mapping in dominant_mappings) / len(dominant_mappings),
            6,
        ) if dominant_mappings else 0.0

        input_bg = infer_background_color(normalized_input) if input_background_color is None else input_background_color
        output_bg = infer_background_color(normalized_output) if output_background_color is None else output_background_color

        if input_bg in counts:
            target_counter = counts[input_bg]
            source_total = sum(target_counter.values())
            target_color, count = sorted(target_counter.items(), key=lambda item: (-item[1], item[0]))[0]
            background_mapping = ColorMapping.build(
                source_color=input_bg,
                target_color=target_color,
                count=count,
                source_total=source_total,
            )

        _ = output_bg

    transform_type = _classify_pair_transform(
        shape_preserving=shape_preserving,
        added_colors=added_colors,
        removed_colors=removed_colors,
        changed_source_colors=changed_source_colors,
        ambiguous_source_colors=ambiguous_sources,
    )

    basis = {
        "pair_id": pair_id,
        "input_signature": grid_signature(normalized_input),
        "output_signature": grid_signature(normalized_output),
        "shape_preserving": shape_preserving,
        "dominant_mappings": [mapping.to_dict() for mapping in dominant_mappings],
        "added_colors": added_colors,
        "removed_colors": removed_colors,
        "transform_type": transform_type,
    }
    signature = _stable_signature(basis)

    return ColorTransformPairReport(
        status="COLOR_TRANSFORM_PAIR_READY",
        pair_id=pair_id,
        input_grid=normalized_input,
        output_grid=normalized_output,
        input_shape=input_shape,
        output_shape=output_shape,
        input_signature=grid_signature(normalized_input),
        output_signature=grid_signature(normalized_output),
        shape_preserving=shape_preserving,
        input_palette=input_palette,
        output_palette=output_palette,
        added_colors=added_colors,
        removed_colors=removed_colors,
        preserved_colors=preserved_colors,
        changed_source_colors=changed_source_colors,
        ambiguous_source_colors=ambiguous_sources,
        ambiguous_target_colors=ambiguous_targets,
        dominant_mappings=dominant_mappings,
        background_mapping=background_mapping,
        transform_type=transform_type,
        confidence=confidence,
        signature=signature,
        metadata={
            "source": "color_transform_detector_v1",
            "milestone": "Milestone #4",
            "task": "Task 3",
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


def detect_color_transforms(
    train_pairs: Iterable[StrategyExample | Mapping[str, Any]],
) -> ColorTransformDetectionReport:
    """Detect aggregate color transformations across training pairs."""

    pair_reports: List[ColorTransformPairReport] = []

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
            detect_color_transform_pair(
                input_grid,
                output_grid,
                pair_id=f"pair-{index}",
            )
        )

    if not pair_reports:
        raise ValueError("train_pairs must contain at least one pair")

    global_input_palette = tuple(sorted({color for report in pair_reports for color in report.input_palette}))
    global_output_palette = tuple(sorted({color for report in pair_reports for color in report.output_palette}))
    global_added_colors = tuple(sorted(set(global_output_palette) - set(global_input_palette)))
    global_removed_colors = tuple(sorted(set(global_input_palette) - set(global_output_palette)))
    global_preserved_colors = tuple(sorted(set(global_input_palette) & set(global_output_palette)))

    source_to_targets: Dict[int, set[int]] = defaultdict(set)
    source_counts: Dict[int, Counter[int]] = defaultdict(Counter)

    for report in pair_reports:
        for mapping in report.dominant_mappings:
            source_to_targets[mapping.source_color].add(mapping.target_color)
            source_counts[mapping.source_color][mapping.target_color] += mapping.count

    unstable_source_colors = tuple(
        sorted(source for source, targets in source_to_targets.items() if len(targets) > 1)
    )

    stable_counts = {
        source: targets
        for source, targets in source_counts.items()
        if source not in unstable_source_colors
    }
    stable_mappings = _dominant_mappings_from_counts(stable_counts) if stable_counts else tuple()

    has_ambiguous_mapping = any(report.ambiguous_source_colors for report in pair_reports) or bool(unstable_source_colors)
    has_palette_expansion = any(report.added_colors for report in pair_reports)
    has_palette_reduction = any(report.removed_colors for report in pair_reports)

    confidence_values = [report.confidence for report in pair_reports]
    confidence = round(sum(confidence_values) / len(confidence_values), 6)

    transform_type = _classify_detection_transform(
        pair_reports=pair_reports,
        has_ambiguous_mapping=has_ambiguous_mapping,
        has_palette_expansion=has_palette_expansion,
        has_palette_reduction=has_palette_reduction,
        stable_mappings=stable_mappings,
    )

    basis = {
        "pair_signatures": [report.signature for report in pair_reports],
        "stable_mappings": [mapping.to_dict() for mapping in stable_mappings],
        "unstable_source_colors": unstable_source_colors,
        "transform_type": transform_type,
    }
    signature = _stable_signature(basis)

    return ColorTransformDetectionReport(
        status="COLOR_TRANSFORM_DETECTION_READY",
        detection_id=f"COLOR-TRANSFORM-DETECTION-{signature[:12]}",
        pair_count=len(pair_reports),
        pair_reports=tuple(pair_reports),
        stable_mappings=stable_mappings,
        unstable_source_colors=unstable_source_colors,
        global_input_palette=global_input_palette,
        global_output_palette=global_output_palette,
        global_added_colors=global_added_colors,
        global_removed_colors=global_removed_colors,
        global_preserved_colors=global_preserved_colors,
        has_ambiguous_mapping=has_ambiguous_mapping,
        has_palette_expansion=has_palette_expansion,
        has_palette_reduction=has_palette_reduction,
        transform_type=transform_type,
        confidence=confidence,
        signature=signature,
        metadata={
            "source": "color_transform_detector_v1",
            "milestone": "Milestone #4",
            "task": "Task 3",
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


def _classify_detection_transform(
    *,
    pair_reports: Sequence[ColorTransformPairReport],
    has_ambiguous_mapping: bool,
    has_palette_expansion: bool,
    has_palette_reduction: bool,
    stable_mappings: Sequence[ColorMapping],
) -> str:
    if has_ambiguous_mapping:
        return "AGGREGATE_AMBIGUOUS_COLOR_MAPPING"

    # Solver-first precedence:
    # stable source -> target remaps are stronger candidate-generation signals
    # than generic palette expansion/reduction labels.
    if any(mapping.source_color != mapping.target_color for mapping in stable_mappings):
        return "AGGREGATE_STABLE_COLOR_REMAP"

    if has_palette_expansion and has_palette_reduction:
        return "AGGREGATE_PALETTE_REPLACEMENT"

    if has_palette_expansion:
        return "AGGREGATE_PALETTE_EXPANSION"

    if has_palette_reduction:
        return "AGGREGATE_PALETTE_REDUCTION"

    if all(report.transform_type == "COLOR_IDENTITY_OR_PRESERVED" for report in pair_reports):
        return "AGGREGATE_COLOR_IDENTITY_OR_PRESERVED"

    return "AGGREGATE_COLOR_TRANSFORM_SIGNAL"


def apply_stable_color_mapping(
    grid: Sequence[Sequence[int]],
    stable_mappings: Iterable[ColorMapping | Mapping[str, Any]],
) -> List[List[int]]:
    """Apply stable dominant color mappings to a grid."""

    normalized = normalize_grid(grid)
    mapping_dict: Dict[int, int] = {}

    for mapping in stable_mappings:
        if isinstance(mapping, ColorMapping):
            mapping_dict[mapping.source_color] = mapping.target_color
        elif isinstance(mapping, Mapping):
            mapping_dict[int(mapping["source_color"])] = int(mapping["target_color"])
        else:
            raise ValueError("stable_mappings must contain ColorMapping or mapping items")

    return [
        [mapping_dict.get(color, color) for color in row]
        for row in normalized
    ]


def validate_color_transform_detection_report(
    report: ColorTransformDetectionReport | Mapping[str, Any],
) -> Dict[str, Any]:
    data = report.to_dict() if isinstance(report, ColorTransformDetectionReport) else dict(report)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), Mapping) else {}
    pair_reports = data.get("pair_reports") if isinstance(data.get("pair_reports"), list) else []
    stable_mappings = data.get("stable_mappings") if isinstance(data.get("stable_mappings"), list) else []

    pair_checks = []
    for pair in pair_reports:
        pair_metadata = pair.get("metadata") if isinstance(pair.get("metadata"), Mapping) else {}
        pair_checks.append(
            pair.get("status") == "COLOR_TRANSFORM_PAIR_READY"
            and isinstance(pair.get("pair_id"), str)
            and isinstance(pair.get("input_palette"), list)
            and isinstance(pair.get("output_palette"), list)
            and isinstance(pair.get("added_colors"), list)
            and isinstance(pair.get("removed_colors"), list)
            and isinstance(pair.get("preserved_colors"), list)
            and isinstance(pair.get("changed_source_colors"), list)
            and isinstance(pair.get("ambiguous_source_colors"), list)
            and isinstance(pair.get("dominant_mappings"), list)
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

    mapping_checks = []
    for mapping in stable_mappings:
        mapping_checks.append(
            isinstance(mapping.get("source_color"), int)
            and isinstance(mapping.get("target_color"), int)
            and isinstance(mapping.get("count"), int)
            and isinstance(mapping.get("source_total"), int)
            and isinstance(mapping.get("confidence"), float)
            and isinstance(mapping.get("relation"), str)
            and isinstance(mapping.get("signature"), str)
        )

    checks = {
        "status_ready": data.get("status") == "COLOR_TRANSFORM_DETECTION_READY",
        "detection_id_present": isinstance(data.get("detection_id"), str) and bool(data.get("detection_id")),
        "pair_count_valid": isinstance(data.get("pair_count"), int) and data.get("pair_count") == len(pair_reports),
        "pair_reports_valid": bool(pair_checks) and all(pair_checks),
        "stable_mappings_valid": all(mapping_checks),
        "unstable_source_colors_list": isinstance(data.get("unstable_source_colors"), list),
        "global_input_palette_list": isinstance(data.get("global_input_palette"), list),
        "global_output_palette_list": isinstance(data.get("global_output_palette"), list),
        "global_added_colors_list": isinstance(data.get("global_added_colors"), list),
        "global_removed_colors_list": isinstance(data.get("global_removed_colors"), list),
        "global_preserved_colors_list": isinstance(data.get("global_preserved_colors"), list),
        "has_ambiguous_mapping_bool": isinstance(data.get("has_ambiguous_mapping"), bool),
        "has_palette_expansion_bool": isinstance(data.get("has_palette_expansion"), bool),
        "has_palette_reduction_bool": isinstance(data.get("has_palette_reduction"), bool),
        "transform_type_present": isinstance(data.get("transform_type"), str) and bool(data.get("transform_type")),
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
        "status": "COLOR_TRANSFORM_DETECTION_VALID" if valid else "COLOR_TRANSFORM_DETECTION_INVALID",
        "valid": valid,
        "checks": checks,
        "detection_id": data.get("detection_id"),
        "pair_count": data.get("pair_count"),
        "transform_type": data.get("transform_type"),
        "confidence": data.get("confidence"),
        "signature": data.get("signature"),
    }


def build_color_transform_detector_smoke_pairs() -> List[Dict[str, Any]]:
    return [
        {
            "input": [
                [0, 1, 1],
                [0, 2, 2],
            ],
            "output": [
                [0, 3, 3],
                [0, 2, 2],
            ],
        },
        {
            "input": [
                [1, 0],
                [2, 2],
            ],
            "output": [
                [3, 0],
                [2, 2],
            ],
        },
    ]


def run_color_transform_detector_pipeline() -> Dict[str, Any]:
    report = detect_color_transforms(build_color_transform_detector_smoke_pairs())
    validation = validate_color_transform_detection_report(report)

    return {
        "status": "COLOR_TRANSFORM_DETECTOR_PIPELINE_READY",
        "detector_status": report.status,
        "validation_status": validation["status"],
        "detection_report": report.to_dict(),
        "validation": validation,
        "pair_count": report.pair_count,
        "stable_mapping_count": len(report.stable_mappings),
        "transform_type": report.transform_type,
        "confidence": report.confidence,
        "signature": report.signature,
        "metadata": {
            "source": "color_transform_detector_v1",
            "milestone": "Milestone #4",
            "task": "Task 3",
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


def render_color_transform_detector_markdown(payload: Mapping[str, Any]) -> str:
    data = dict(payload)
    report = data["detection_report"]

    lines = [
        "# ARC-AGI-3 Milestone #4 Task 3 — Color Transform Detector v1 Smoke",
        "",
        f"Status: {data['status']}",
        f"Detector status: {data['detector_status']}",
        f"Validation status: {data['validation_status']}",
        f"Detection ID: {report['detection_id']}",
        f"Pair count: {data['pair_count']}",
        f"Stable mapping count: {data['stable_mapping_count']}",
        f"Transform type: {data['transform_type']}",
        f"Confidence: {data['confidence']}",
        f"Signature: {data['signature']}",
        "",
        "## Stable mappings",
        "",
    ]

    for mapping in report["stable_mappings"]:
        lines.extend(
            [
                f"- {mapping['source_color']} -> {mapping['target_color']} "
                f"confidence={mapping['confidence']} relation={mapping['relation']}",
            ]
        )

    lines.extend(
        [
            "",
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


def write_color_transform_detector_artifacts(
    payload: Optional[Mapping[str, Any]] = None,
    *,
    output_dir: str = "examples/milestone-4/color-transform-detector-v1",
) -> Dict[str, str]:
    data = dict(payload or run_color_transform_detector_pipeline())
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "color-transform-detector-v1-smoke.json"
    markdown_path = output_path / "color-transform-detector-v1-smoke.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_color_transform_detector_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
