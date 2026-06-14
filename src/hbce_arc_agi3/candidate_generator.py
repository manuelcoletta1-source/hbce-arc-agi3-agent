"""Candidate Generator v1 for ARC-AGI-3 Milestone #4.

This module generates deterministic candidate output grids by combining:

- Strategy Interface v2
- Grid Object Extractor v1
- Color Transform Detector v1
- Shape / Symmetry Detector v1

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

from hbce_arc_agi3.color_transform_detector import (
    ColorTransformDetectionReport,
    apply_stable_color_mapping,
    detect_color_transforms,
)
from hbce_arc_agi3.grid_object_extractor import (
    GridObjectExtractionReport,
    extract_grid_objects,
)
from hbce_arc_agi3.shape_symmetry_detector import (
    ShapeSymmetryDetectionReport,
    detect_shape_symmetry_transforms,
    foreground_bbox,
    foreground_cells,
    foreground_mask,
    normalize_mask,
    reflect_mask_horizontal,
    reflect_mask_vertical,
    rotate_mask_90,
    rotate_mask_180,
    rotate_mask_270,
)
from hbce_arc_agi3.strategy_interface_v2 import (
    Grid,
    StrategyExample,
    grid_signature,
    grid_to_lists,
    normalize_grid,
)


Mask = Tuple[Tuple[int, ...], ...]
Cell = Tuple[int, int]


def _stable_signature(payload: Mapping[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def rotate_grid_90(grid: Sequence[Sequence[int]]) -> List[List[int]]:
    normalized = normalize_grid(grid)
    return [list(row) for row in zip(*normalized[::-1])]


def rotate_grid_180(grid: Sequence[Sequence[int]]) -> List[List[int]]:
    normalized = normalize_grid(grid)
    return [list(reversed(row)) for row in reversed(normalized)]


def rotate_grid_270(grid: Sequence[Sequence[int]]) -> List[List[int]]:
    normalized = normalize_grid(grid)
    return [list(row) for row in zip(*normalized)][::-1]


def reflect_grid_horizontal(grid: Sequence[Sequence[int]]) -> List[List[int]]:
    normalized = normalize_grid(grid)
    return [list(row) for row in reversed(normalized)]


def reflect_grid_vertical(grid: Sequence[Sequence[int]]) -> List[List[int]]:
    normalized = normalize_grid(grid)
    return [list(reversed(row)) for row in normalized]


def most_common_foreground_color(
    grid: Sequence[Sequence[int]],
    *,
    background_color: int = 0,
) -> int:
    normalized = normalize_grid(grid)
    counter: Counter[int] = Counter()

    for row in normalized:
        for value in row:
            if value != background_color:
                counter[value] += 1

    if not counter:
        return background_color

    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))[0][0]



def generalize_unseen_foreground_color_mapping(
    grid: Sequence[Sequence[int]],
    stable_mappings: Any,
    *,
    background_color: int = 0,
) -> Grid:
    """Map unseen foreground colors to the dominant learned foreground output.

    Accepts the detector's ColorMapping objects as well as plain dictionaries.
    If observed foreground source colors converge to one non-background target,
    unseen foreground colors in the test grid are mapped to that target.
    """

    normalized = normalize_grid(grid, field_name="grid")
    normalized_mappings: Dict[int, int] = {}

    if isinstance(stable_mappings, Mapping):
        for source, target in stable_mappings.items():
            normalized_mappings[int(source)] = int(target)
    else:
        for item in stable_mappings:
            if isinstance(item, Mapping):
                source = item.get("source_color")
                target = item.get("target_color")
            else:
                source = getattr(item, "source_color", None)
                target = getattr(item, "target_color", None)

            if source is None or target is None:
                continue

            normalized_mappings[int(source)] = int(target)

    foreground_targets = {
        target
        for source, target in normalized_mappings.items()
        if source != background_color and target != background_color
    }

    if len(foreground_targets) != 1:
        return normalized

    dominant_target = next(iter(foreground_targets))

    result: Grid = []
    for row in normalized:
        result_row = []
        for value in row:
            cell = int(value)
            if cell == background_color:
                result_row.append(background_color)
            elif cell in normalized_mappings:
                result_row.append(normalized_mappings[cell])
            else:
                result_row.append(dominant_target)
        result.append(result_row)

    return result

def transform_mask_by_type(mask: Sequence[Sequence[int]], transform_type: Optional[str]) -> Mask:
    normalized = normalize_mask(mask)

    if transform_type in (None, "SHAPE_IDENTITY"):
        return normalized

    if transform_type == "ROTATE_90":
        return rotate_mask_90(normalized)

    if transform_type == "ROTATE_180":
        return rotate_mask_180(normalized)

    if transform_type == "ROTATE_270":
        return rotate_mask_270(normalized)

    if transform_type == "REFLECT_HORIZONTAL":
        return reflect_mask_horizontal(normalized)

    if transform_type == "REFLECT_VERTICAL":
        return reflect_mask_vertical(normalized)

    return normalized


def apply_shape_transform_to_foreground(
    grid: Sequence[Sequence[int]],
    transform_type: Optional[str],
    *,
    background_color: int = 0,
    fill_color: Optional[int] = None,
) -> List[List[int]]:
    """Apply a foreground-mask shape transform inside the current foreground bbox.

    V1 deliberately uses a single fill color for transformed foreground cells.
    This makes the module deterministic and useful for early candidates while
    leaving multi-object/multi-color geometry for later milestone tasks.
    """

    normalized = normalize_grid(grid)
    height = len(normalized)
    width = len(normalized[0])

    if transform_type == "TRANSLATION":
        return grid_to_lists(normalized)

    cells = foreground_cells(normalized, background_color=background_color)
    bbox = foreground_bbox(cells)

    if bbox is None:
        return grid_to_lists(normalized)

    mask = foreground_mask(normalized, background_color=background_color)
    transformed_mask = transform_mask_by_type(mask, transform_type)

    chosen_fill = fill_color if fill_color is not None else most_common_foreground_color(
        normalized,
        background_color=background_color,
    )

    result = [[background_color for _ in range(width)] for _ in range(height)]

    start_row = int(bbox["min_row"])
    start_col = int(bbox["min_col"])

    for row_offset, mask_row in enumerate(transformed_mask):
        for col_offset, value in enumerate(mask_row):
            if value != 1:
                continue

            row = start_row + row_offset
            col = start_col + col_offset

            if 0 <= row < height and 0 <= col < width:
                result[row][col] = chosen_fill

    return result


@dataclass(frozen=True)
class GeneratedCandidate:
    """One generated candidate output grid."""

    status: str
    candidate_id: str
    candidate_type: str
    candidate_grid: Grid
    applied_transforms: Tuple[str, ...]
    confidence: float
    score_hint: float
    rank_hint: int
    signature: str
    metadata: Dict[str, Any]

    @classmethod
    def build(
        cls,
        *,
        candidate_type: str,
        candidate_grid: Sequence[Sequence[int]],
        applied_transforms: Iterable[str],
        confidence: float,
        score_hint: float,
        rank_hint: int,
    ) -> "GeneratedCandidate":
        normalized_grid = normalize_grid(candidate_grid, field_name="candidate_grid")
        transforms = tuple(applied_transforms)

        basis = {
            "candidate_type": candidate_type,
            "candidate_grid_signature": grid_signature(normalized_grid),
            "applied_transforms": transforms,
            "confidence": round(confidence, 6),
            "score_hint": round(score_hint, 6),
            "rank_hint": rank_hint,
        }
        signature = _stable_signature(basis)

        return cls(
            status="GENERATED_CANDIDATE_READY",
            candidate_id=f"ARC-AGI3-CANDIDATE-{signature[:12]}",
            candidate_type=candidate_type,
            candidate_grid=normalized_grid,
            applied_transforms=transforms,
            confidence=round(confidence, 6),
            score_hint=round(score_hint, 6),
            rank_hint=rank_hint,
            signature=signature,
            metadata={
                "source": "candidate_generator_v1",
                "milestone": "Milestone #4",
                "task": "Task 5",
                "public_safe": True,
                "deterministic": True,
                "local_only": True,
                "dry_run_only": True,
                "score_oriented": True,
                "prize_oriented_solver_target": True,
                "agentic_state_feature": True,
                "candidate_generator_output": True,
                "candidate_ranker_input": True,
                "external_api_dependency": False,
                "contains_api_keys": False,
                "kaggle_submission_sent": False,
                "private_core_exposure": False,
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "candidate_id": self.candidate_id,
            "candidate_type": self.candidate_type,
            "candidate_grid": grid_to_lists(self.candidate_grid),
            "applied_transforms": list(self.applied_transforms),
            "confidence": self.confidence,
            "score_hint": self.score_hint,
            "rank_hint": self.rank_hint,
            "signature": self.signature,
            "metadata": copy.deepcopy(self.metadata),
        }


@dataclass(frozen=True)
class CandidateGenerationReport:
    """Candidate generation report."""

    status: str
    generation_id: str
    task_id: str
    train_pair_count: int
    test_input: Grid
    test_input_signature: str
    object_extraction: Dict[str, Any]
    color_detection: Dict[str, Any]
    shape_detection: Dict[str, Any]
    candidate_count: int
    candidates: Tuple[GeneratedCandidate, ...]
    best_candidate: GeneratedCandidate
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "generation_id": self.generation_id,
            "task_id": self.task_id,
            "train_pair_count": self.train_pair_count,
            "test_input": grid_to_lists(self.test_input),
            "test_input_signature": self.test_input_signature,
            "object_extraction": copy.deepcopy(self.object_extraction),
            "color_detection": copy.deepcopy(self.color_detection),
            "shape_detection": copy.deepcopy(self.shape_detection),
            "candidate_count": self.candidate_count,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "best_candidate": self.best_candidate.to_dict(),
            "signature": self.signature,
            "metadata": copy.deepcopy(self.metadata),
        }


def _extract_pair_grids(pair: StrategyExample | Mapping[str, Any]) -> Tuple[Any, Any]:
    if isinstance(pair, StrategyExample):
        return pair.input_grid, pair.output_grid

    if isinstance(pair, Mapping):
        return (
            pair.get("input_grid") or pair.get("input") or pair.get("inputGrid"),
            pair.get("output_grid") or pair.get("output") or pair.get("outputGrid"),
        )

    raise ValueError("training pair must be StrategyExample or mapping")


def generate_candidates(
    train_pairs: Iterable[StrategyExample | Mapping[str, Any]],
    test_input: Sequence[Sequence[int]],
    *,
    task_id: str = "MILESTONE-4-TASK-5-SMOKE",
    background_color: int = 0,
) -> CandidateGenerationReport:
    pairs = list(train_pairs)

    if not pairs:
        raise ValueError("train_pairs must contain at least one pair")

    normalized_test = normalize_grid(test_input, field_name="test_input")

    object_report = extract_grid_objects(normalized_test, background_color=background_color)
    color_report = detect_color_transforms(pairs)
    shape_report = detect_shape_symmetry_transforms(pairs)

    identity_grid = grid_to_lists(normalized_test)

    color_grid = apply_stable_color_mapping(
        normalized_test,
        color_report.stable_mappings,
    )

    color_grid = generalize_unseen_foreground_color_mapping(
        color_grid,
        color_report.stable_mappings,
        background_color=background_color,
    )

    shape_transform = shape_report.stable_transform_type or shape_report.dominant_transform_type

    shape_grid = apply_shape_transform_to_foreground(
        normalized_test,
        shape_transform,
        background_color=background_color,
    )

    combined_fill_color = most_common_foreground_color(color_grid, background_color=background_color)
    combined_grid = apply_shape_transform_to_foreground(
        color_grid,
        shape_transform,
        background_color=background_color,
        fill_color=combined_fill_color,
    )

    candidates = [
        GeneratedCandidate.build(
            candidate_type="IDENTITY_BASELINE",
            candidate_grid=identity_grid,
            applied_transforms=("identity",),
            confidence=0.10,
            score_hint=0.10,
            rank_hint=400,
        ),
        GeneratedCandidate.build(
            candidate_type="COLOR_REMAP",
            candidate_grid=color_grid,
            applied_transforms=("stable_color_mapping",),
            confidence=color_report.confidence,
            score_hint=0.65,
            rank_hint=200,
        ),
        GeneratedCandidate.build(
            candidate_type="SHAPE_TRANSFORM",
            candidate_grid=shape_grid,
            applied_transforms=(shape_transform or "shape_identity",),
            confidence=shape_report.confidence,
            score_hint=0.70,
            rank_hint=150,
        ),
        GeneratedCandidate.build(
            candidate_type="COLOR_SHAPE_COMBINED",
            candidate_grid=combined_grid,
            applied_transforms=("stable_color_mapping", shape_transform or "shape_identity"),
            confidence=round((color_report.confidence + shape_report.confidence) / 2, 6),
            score_hint=0.95,
            rank_hint=50,
        ),
    ]

    ordered_candidates = tuple(
        sorted(
            candidates,
            key=lambda candidate: (
                -candidate.score_hint,
                -candidate.confidence,
                candidate.rank_hint,
                candidate.candidate_type,
                candidate.signature,
            ),
        )
    )

    best_candidate = ordered_candidates[0]

    object_summary = {
        "status": object_report.status,
        "extraction_id": object_report.extraction_id,
        "object_count": object_report.object_count,
        "object_density": object_report.object_density,
        "signature": object_report.signature,
    }
    color_summary = {
        "status": color_report.status,
        "detection_id": color_report.detection_id,
        "pair_count": color_report.pair_count,
        "stable_mapping_count": len(color_report.stable_mappings),
        "transform_type": color_report.transform_type,
        "confidence": color_report.confidence,
        "signature": color_report.signature,
    }
    shape_summary = {
        "status": shape_report.status,
        "detection_id": shape_report.detection_id,
        "pair_count": shape_report.pair_count,
        "dominant_transform_type": shape_report.dominant_transform_type,
        "stable_transform_type": shape_report.stable_transform_type,
        "confidence": shape_report.confidence,
        "signature": shape_report.signature,
    }

    basis = {
        "task_id": task_id,
        "test_input_signature": grid_signature(normalized_test),
        "object_signature": object_report.signature,
        "color_signature": color_report.signature,
        "shape_signature": shape_report.signature,
        "candidate_signatures": [candidate.signature for candidate in ordered_candidates],
    }
    signature = _stable_signature(basis)

    return CandidateGenerationReport(
        status="CANDIDATE_GENERATION_READY",
        generation_id=f"CANDIDATE-GENERATION-{signature[:12]}",
        task_id=task_id,
        train_pair_count=len(pairs),
        test_input=normalized_test,
        test_input_signature=grid_signature(normalized_test),
        object_extraction=object_summary,
        color_detection=color_summary,
        shape_detection=shape_summary,
        candidate_count=len(ordered_candidates),
        candidates=ordered_candidates,
        best_candidate=best_candidate,
        signature=signature,
        metadata={
            "source": "candidate_generator_v1",
            "milestone": "Milestone #4",
            "task": "Task 5",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "agentic_state_feature": True,
            "uses_strategy_interface_v2": True,
            "uses_grid_object_extractor_v1": True,
            "uses_color_transform_detector_v1": True,
            "uses_shape_symmetry_detector_v1": True,
            "candidate_generator_output": True,
            "candidate_ranker_input": True,
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


def validate_candidate_generation_report(
    report: CandidateGenerationReport | Mapping[str, Any],
) -> Dict[str, Any]:
    data = report.to_dict() if isinstance(report, CandidateGenerationReport) else dict(report)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), Mapping) else {}
    candidates = data.get("candidates") if isinstance(data.get("candidates"), list) else []
    best_candidate = data.get("best_candidate") if isinstance(data.get("best_candidate"), Mapping) else {}

    candidate_checks = []
    for candidate in candidates:
        candidate_metadata = candidate.get("metadata") if isinstance(candidate.get("metadata"), Mapping) else {}
        candidate_checks.append(
            candidate.get("status") == "GENERATED_CANDIDATE_READY"
            and isinstance(candidate.get("candidate_id"), str)
            and isinstance(candidate.get("candidate_type"), str)
            and _grid_data_is_valid(candidate.get("candidate_grid"))
            and isinstance(candidate.get("applied_transforms"), list)
            and isinstance(candidate.get("confidence"), float)
            and 0.0 <= candidate.get("confidence") <= 1.0
            and isinstance(candidate.get("score_hint"), float)
            and 0.0 <= candidate.get("score_hint") <= 1.0
            and isinstance(candidate.get("rank_hint"), int)
            and isinstance(candidate.get("signature"), str)
            and candidate_metadata.get("public_safe") is True
            and candidate_metadata.get("deterministic") is True
            and candidate_metadata.get("local_only") is True
            and candidate_metadata.get("dry_run_only") is True
            and candidate_metadata.get("candidate_generator_output") is True
            and candidate_metadata.get("candidate_ranker_input") is True
            and candidate_metadata.get("external_api_dependency") is False
            and candidate_metadata.get("contains_api_keys") is False
            and candidate_metadata.get("kaggle_submission_sent") is False
            and candidate_metadata.get("private_core_exposure") is False
        )

    checks = {
        "status_ready": data.get("status") == "CANDIDATE_GENERATION_READY",
        "generation_id_present": isinstance(data.get("generation_id"), str) and bool(data.get("generation_id")),
        "task_id_present": isinstance(data.get("task_id"), str) and bool(data.get("task_id")),
        "train_pair_count_valid": isinstance(data.get("train_pair_count"), int) and data.get("train_pair_count") >= 1,
        "test_input_valid": _grid_data_is_valid(data.get("test_input")),
        "test_input_signature_present": isinstance(data.get("test_input_signature"), str),
        "object_extraction_ready": isinstance(data.get("object_extraction"), Mapping)
        and data["object_extraction"].get("status") == "GRID_OBJECT_EXTRACTION_READY",
        "color_detection_ready": isinstance(data.get("color_detection"), Mapping)
        and data["color_detection"].get("status") == "COLOR_TRANSFORM_DETECTION_READY",
        "shape_detection_ready": isinstance(data.get("shape_detection"), Mapping)
        and data["shape_detection"].get("status") == "SHAPE_SYMMETRY_DETECTION_READY",
        "candidate_count_valid": isinstance(data.get("candidate_count"), int) and data.get("candidate_count") == len(candidates),
        "candidate_count_minimum": len(candidates) >= 4,
        "candidates_valid": bool(candidate_checks) and all(candidate_checks),
        "best_candidate_ready": best_candidate.get("status") == "GENERATED_CANDIDATE_READY",
        "best_candidate_type_combined": best_candidate.get("candidate_type") == "COLOR_SHAPE_COMBINED",
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
        "metadata_score_oriented": metadata.get("score_oriented") is True,
        "metadata_prize_oriented_solver_target": metadata.get("prize_oriented_solver_target") is True,
        "metadata_uses_strategy_interface": metadata.get("uses_strategy_interface_v2") is True,
        "metadata_uses_object_extractor": metadata.get("uses_grid_object_extractor_v1") is True,
        "metadata_uses_color_detector": metadata.get("uses_color_transform_detector_v1") is True,
        "metadata_uses_shape_detector": metadata.get("uses_shape_symmetry_detector_v1") is True,
        "metadata_candidate_generator_output": metadata.get("candidate_generator_output") is True,
        "metadata_candidate_ranker_input": metadata.get("candidate_ranker_input") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
    }

    valid = all(checks.values())

    return {
        "status": "CANDIDATE_GENERATION_VALID" if valid else "CANDIDATE_GENERATION_INVALID",
        "valid": valid,
        "checks": checks,
        "generation_id": data.get("generation_id"),
        "candidate_count": data.get("candidate_count"),
        "best_candidate_type": best_candidate.get("candidate_type"),
        "best_candidate_signature": best_candidate.get("signature"),
        "signature": data.get("signature"),
    }


def _grid_data_is_valid(value: Any) -> bool:
    try:
        normalize_grid(value)
        return True
    except Exception:
        return False


def build_candidate_generator_smoke_train_pairs() -> List[Dict[str, Any]]:
    return [
        {
            "input": [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 0],
            ],
            "output": [
                [0, 3, 3],
                [0, 3, 0],
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
                [6, 6, 0],
                [6, 0, 0],
                [0, 0, 0],
            ],
        },
    ]


def build_candidate_generator_smoke_test_input() -> List[List[int]]:
    return [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]


def build_candidate_generator_smoke_expected_best_grid() -> List[List[int]]:
    return [
        [0, 3, 3],
        [0, 3, 0],
        [0, 0, 0],
    ]


def run_candidate_generator_pipeline() -> Dict[str, Any]:
    report = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )
    validation = validate_candidate_generation_report(report)

    return {
        "status": "CANDIDATE_GENERATOR_PIPELINE_READY",
        "generator_status": report.status,
        "validation_status": validation["status"],
        "generation_report": report.to_dict(),
        "validation": validation,
        "candidate_count": report.candidate_count,
        "best_candidate_type": report.best_candidate.candidate_type,
        "best_candidate_signature": report.best_candidate.signature,
        "best_candidate_grid": grid_to_lists(report.best_candidate.candidate_grid),
        "expected_best_grid": build_candidate_generator_smoke_expected_best_grid(),
        "best_candidate_matches_expected_smoke": grid_to_lists(report.best_candidate.candidate_grid)
        == build_candidate_generator_smoke_expected_best_grid(),
        "signature": report.signature,
        "metadata": {
            "source": "candidate_generator_v1",
            "milestone": "Milestone #4",
            "task": "Task 5",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "score_oriented": True,
            "prize_oriented_solver_target": True,
            "agentic_state_feature": True,
            "uses_strategy_interface_v2": True,
            "uses_grid_object_extractor_v1": True,
            "uses_color_transform_detector_v1": True,
            "uses_shape_symmetry_detector_v1": True,
            "candidate_generator_output": True,
            "candidate_ranker_input": True,
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


def render_candidate_generator_markdown(payload: Mapping[str, Any]) -> str:
    data = dict(payload)
    report = data["generation_report"]

    lines = [
        "# ARC-AGI-3 Milestone #4 Task 5 — Candidate Generator v1 Smoke",
        "",
        f"Status: {data['status']}",
        f"Generator status: {data['generator_status']}",
        f"Validation status: {data['validation_status']}",
        f"Generation ID: {report['generation_id']}",
        f"Candidate count: {data['candidate_count']}",
        f"Best candidate type: {data['best_candidate_type']}",
        f"Best candidate signature: {data['best_candidate_signature']}",
        f"Best candidate matches expected smoke: {str(data['best_candidate_matches_expected_smoke']).lower()}",
        f"Signature: {data['signature']}",
        "",
        "## Candidate ranking",
        "",
    ]

    for candidate in report["candidates"]:
        lines.extend(
            [
                f"- {candidate['candidate_type']} "
                f"score_hint={candidate['score_hint']} "
                f"confidence={candidate['confidence']} "
                f"rank_hint={candidate['rank_hint']} "
                f"signature={candidate['signature']}",
            ]
        )

    lines.extend(
        [
            "",
            "## Best candidate grid",
            "",
            "```json",
            json.dumps(data["best_candidate_grid"]),
            "```",
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
            "- uses_strategy_interface_v2=true",
            "- uses_grid_object_extractor_v1=true",
            "- uses_color_transform_detector_v1=true",
            "- uses_shape_symmetry_detector_v1=true",
            "- candidate_generator_output=true",
            "- candidate_ranker_input=true",
            "- external_api_dependency=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_candidate_generator_artifacts(
    payload: Optional[Mapping[str, Any]] = None,
    *,
    output_dir: str = "examples/milestone-4/candidate-generator-v1",
) -> Dict[str, str]:
    data = dict(payload or run_candidate_generator_pipeline())
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "candidate-generator-v1-smoke.json"
    markdown_path = output_path / "candidate-generator-v1-smoke.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_candidate_generator_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
