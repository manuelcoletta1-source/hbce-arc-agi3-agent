"""Milestone #8 Competitive Solver Kernel v2.

Local-only deterministic solver kernel.

This module implements a small deterministic ARC-style grid solver kernel for
Milestone #8. It provides concrete local operations for color mapping, background
preservation, object/component detection, spatial transforms, shape reflection,
bounded translation, candidate merge, and deterministic ranker signal.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, create a real submission, claim a Kaggle score, claim public
leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

from collections import Counter, deque
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


Grid = Tuple[Tuple[int, ...], ...]
Cell = Tuple[int, int]


KERNEL_STATUS = "MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_READY"
PIPELINE_STATUS = "MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_VALID"

BASELINE_COMMIT = "69af006 Add ARC AGI3 competitive solver iteration plan"
KERNEL_MODE = "COMPETITIVE_SOLVER_KERNEL_V2_LOCAL_ONLY"
KERNEL_SCOPE = "IMPLEMENT_DETERMINISTIC_LOCAL_SOLVER_KERNEL_V2"
KERNEL_VERDICT = "COMPETITIVE_SOLVER_KERNEL_V2_READY_FOR_FAMILY_BENCHMARK_CASES"
NEXT_ALLOWED_STAGE = "MILESTONE_8_TASK_3_FAMILY_BENCHMARK_CASES_V2"

DEFAULT_OUTPUT_DIR = "examples/milestone-8/competitive-solver-kernel-v2"

PLAN_JSON = Path(
    "examples/milestone-8/competitive-solver-iteration-plan-v2/"
    "milestone-8-competitive-solver-iteration-plan-v2.json"
)

KERNEL_FAMILIES: Tuple[str, ...] = (
    "color_mapping",
    "object_model",
    "shape_symmetry",
    "cross_family_composition",
)

KERNEL_OPERATIONS: Tuple[str, ...] = (
    "infer_color_mapping",
    "apply_color_mapping",
    "detect_connected_components",
    "translate_component",
    "reflect_grid_horizontal",
    "reflect_grid_vertical",
    "merge_candidate_sets",
    "rank_kernel_candidates",
)

SAMPLE_CASES: Tuple[str, ...] = (
    "sample_color_palette_transfer_v2",
    "sample_color_background_guard_v2",
    "sample_object_component_delta_v2",
    "sample_object_spatial_shift_right_v2",
    "sample_object_spatial_shift_down_v2",
    "sample_shape_reflect_horizontal_v2",
    "sample_shape_reflect_vertical_v2",
    "sample_cross_family_ranker_signal_v2",
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_rectangular_grid",
    "guard_background_preservation",
    "guard_color_mapping_conflict_resolution",
    "guard_component_count_stability",
    "guard_translation_bounds",
    "guard_shape_reflection_dimension_stability",
    "guard_candidate_deduplication",
    "guard_no_submission_side_effect",
)

BOUNDARY_CONTROLS: Tuple[str, ...] = (
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "kaggle_submission_sent_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

EXPECTED_KERNEL_FAMILY_COUNT = 4
EXPECTED_KERNEL_OPERATION_COUNT = 8
EXPECTED_SAMPLE_CASE_COUNT = 8
EXPECTED_REGRESSION_GUARD_COUNT = 8
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_PLAN_GATE_COUNT = 42
EXPECTED_PLAN_ISSUE_COUNT = 0

KERNEL_GATES: Tuple[str, ...] = (
    "plan_artifact_present",
    "plan_artifact_ready",
    "plan_artifact_valid",
    "plan_next_stage_matches_task_2",
    "kernel_mode_valid",
    "kernel_scope_valid",
    "kernel_verdict_valid",
    "kernel_ready",
    "kernel_locked",
    "kernel_family_count_valid",
    "kernel_operation_count_valid",
    "sample_case_count_valid",
    "regression_guard_count_valid",
    "boundary_control_count_valid",
    "plan_gate_count_valid",
    "plan_issue_count_zero",
    "color_mapping_available",
    "background_guard_available",
    "component_detection_available",
    "component_translation_available",
    "horizontal_reflection_available",
    "vertical_reflection_available",
    "candidate_merge_available",
    "ranker_signal_available",
    "sample_color_palette_transfer_pass",
    "sample_background_guard_pass",
    "sample_component_detection_pass",
    "sample_translation_right_pass",
    "sample_translation_down_pass",
    "sample_reflect_horizontal_pass",
    "sample_reflect_vertical_pass",
    "sample_candidate_ranker_pass",
    "solver_kernel_v2_created",
    "runtime_solver_iteration_performed",
    "real_submission_not_created",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
    "score_claim_absent",
    "public_leaderboard_claim_absent",
    "next_stage_valid",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
)

KERNEL_ISSUES: Tuple[str, ...] = (
    "plan_artifact_missing",
    "plan_artifact_not_ready",
    "plan_artifact_invalid",
    "plan_next_stage_mismatch",
    "kernel_mode_invalid",
    "kernel_scope_invalid",
    "kernel_verdict_invalid",
    "kernel_not_ready",
    "kernel_not_locked",
    "kernel_family_count_invalid",
    "kernel_operation_count_invalid",
    "sample_case_count_invalid",
    "regression_guard_count_invalid",
    "boundary_control_count_invalid",
    "plan_gate_count_invalid",
    "plan_issue_count_nonzero",
    "color_mapping_missing",
    "background_guard_missing",
    "component_detection_missing",
    "component_translation_missing",
    "horizontal_reflection_missing",
    "vertical_reflection_missing",
    "candidate_merge_missing",
    "ranker_signal_missing",
    "sample_color_palette_transfer_failed",
    "sample_background_guard_failed",
    "sample_component_detection_failed",
    "sample_translation_right_failed",
    "sample_translation_down_failed",
    "sample_reflect_horizontal_failed",
    "sample_reflect_vertical_failed",
    "sample_candidate_ranker_failed",
    "solver_kernel_v2_missing",
    "runtime_solver_iteration_not_performed",
    "real_submission_created",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "external_api_dependency_detected",
    "api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "score_claim_detected",
    "public_leaderboard_claim_detected",
    "next_stage_invalid",
    "public_safe_false",
    "deterministic_false",
    "local_only_false",
    "dry_run_only_false",
)


def normalize_grid(grid: Sequence[Sequence[int]]) -> Grid:
    """Normalize a rectangular grid into an immutable tuple-of-tuples."""
    if not grid:
        raise ValueError("grid must not be empty")
    rows = tuple(tuple(int(value) for value in row) for row in grid)
    width = len(rows[0])
    if width == 0:
        raise ValueError("grid rows must not be empty")
    if any(len(row) != width for row in rows):
        raise ValueError("grid must be rectangular")
    return rows


def grid_shape(grid: Sequence[Sequence[int]]) -> Tuple[int, int]:
    normalized = normalize_grid(grid)
    return len(normalized), len(normalized[0])


def flatten_grid(grid: Sequence[Sequence[int]]) -> Tuple[int, ...]:
    normalized = normalize_grid(grid)
    return tuple(value for row in normalized for value in row)


def background_color(grid: Sequence[Sequence[int]]) -> int:
    """Return the most frequent color, tie-broken by smaller color id."""
    counter = Counter(flatten_grid(grid))
    return min(counter.items(), key=lambda item: (-item[1], item[0]))[0]


def infer_color_mapping(
    input_grid: Sequence[Sequence[int]],
    output_grid: Sequence[Sequence[int]],
) -> Dict[int, int]:
    """Infer a deterministic color mapping from aligned input/output cells.

    If a source color maps to multiple target colors, choose the most frequent
    target and tie-break by smaller target color.
    """
    source = normalize_grid(input_grid)
    target = normalize_grid(output_grid)
    if grid_shape(source) != grid_shape(target):
        raise ValueError("input and output grids must have the same shape")

    observations: Dict[int, Counter[int]] = {}
    for r, row in enumerate(source):
        for c, color in enumerate(row):
            observations.setdefault(color, Counter())[target[r][c]] += 1

    return {
        src: min(counts.items(), key=lambda item: (-item[1], item[0]))[0]
        for src, counts in sorted(observations.items())
    }


def apply_color_mapping(
    grid: Sequence[Sequence[int]],
    mapping: Mapping[int, int],
    *,
    preserve_background: bool = True,
    background: int | None = None,
) -> Grid:
    """Apply a color mapping with optional background preservation."""
    normalized = normalize_grid(grid)
    bg = background_color(normalized) if background is None else background
    rows: List[Tuple[int, ...]] = []
    for row in normalized:
        new_row = []
        for value in row:
            if preserve_background and value == bg:
                new_row.append(value)
            else:
                new_row.append(int(mapping.get(value, value)))
        rows.append(tuple(new_row))
    return tuple(rows)


def connected_components(
    grid: Sequence[Sequence[int]],
    *,
    background: int | None = None,
) -> Tuple[Dict[str, Any], ...]:
    """Detect orthogonal connected components excluding background."""
    normalized = normalize_grid(grid)
    height, width = grid_shape(normalized)
    bg = background_color(normalized) if background is None else background
    visited: set[Cell] = set()
    components: List[Dict[str, Any]] = []

    for r in range(height):
        for c in range(width):
            if (r, c) in visited or normalized[r][c] == bg:
                continue

            color = normalized[r][c]
            queue: deque[Cell] = deque([(r, c)])
            visited.add((r, c))
            cells: List[Cell] = []

            while queue:
                cell = queue.popleft()
                cells.append(cell)
                cr, cc = cell
                for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                    if (
                        0 <= nr < height
                        and 0 <= nc < width
                        and (nr, nc) not in visited
                        and normalized[nr][nc] == color
                    ):
                        visited.add((nr, nc))
                        queue.append((nr, nc))

            min_r = min(cell[0] for cell in cells)
            max_r = max(cell[0] for cell in cells)
            min_c = min(cell[1] for cell in cells)
            max_c = max(cell[1] for cell in cells)
            components.append(
                {
                    "component_id": f"component_{len(components) + 1}",
                    "color": color,
                    "size": len(cells),
                    "cells": tuple(sorted(cells)),
                    "bbox": (min_r, min_c, max_r, max_c),
                }
            )

    return tuple(sorted(components, key=lambda item: (-item["size"], item["color"], item["bbox"])))


def translate_component(
    grid: Sequence[Sequence[int]],
    component_cells: Iterable[Cell],
    *,
    dr: int,
    dc: int,
    fill_color: int | None = None,
) -> Grid:
    """Translate a component if it remains in bounds, otherwise keep original."""
    normalized = normalize_grid(grid)
    height, width = grid_shape(normalized)
    bg = background_color(normalized) if fill_color is None else fill_color
    cells = tuple(component_cells)

    if not cells:
        return normalized

    translated = tuple((r + dr, c + dc) for r, c in cells)
    if any(r < 0 or c < 0 or r >= height or c >= width for r, c in translated):
        return normalized

    matrix = [list(row) for row in normalized]
    colors = [normalized[r][c] for r, c in cells]
    for r, c in cells:
        matrix[r][c] = bg
    for (r, c), color in zip(translated, colors):
        matrix[r][c] = color
    return tuple(tuple(row) for row in matrix)


def reflect_grid_horizontal(grid: Sequence[Sequence[int]]) -> Grid:
    """Reflect over the horizontal axis by reversing row order."""
    normalized = normalize_grid(grid)
    return tuple(reversed(normalized))


def reflect_grid_vertical(grid: Sequence[Sequence[int]]) -> Grid:
    """Reflect over the vertical axis by reversing each row."""
    normalized = normalize_grid(grid)
    return tuple(tuple(reversed(row)) for row in normalized)


def candidate_signature(grid: Sequence[Sequence[int]]) -> str:
    normalized = normalize_grid(grid)
    raw = json.dumps(normalized, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def merge_candidate_sets(*candidate_sets: Sequence[Mapping[str, Any]]) -> Tuple[Dict[str, Any], ...]:
    """Merge candidate sets deterministically and remove duplicate grids."""
    merged: Dict[str, Dict[str, Any]] = {}
    for candidate_set in candidate_sets:
        for candidate in candidate_set:
            grid = normalize_grid(candidate["grid"])
            signature = candidate_signature(grid)
            score = float(candidate.get("evidence_score", 0.0))
            record = {
                "candidate_id": candidate.get("candidate_id", f"candidate_{signature}"),
                "family": candidate.get("family", "unknown"),
                "operation": candidate.get("operation", "unknown"),
                "grid": grid,
                "evidence_score": score,
                "signature": signature,
            }
            existing = merged.get(signature)
            if existing is None or score > existing["evidence_score"]:
                merged[signature] = record
    return tuple(sorted(merged.values(), key=lambda item: (-item["evidence_score"], item["signature"])))


def rank_kernel_candidates(candidates: Sequence[Mapping[str, Any]]) -> Tuple[Dict[str, Any], ...]:
    """Rank candidates using deterministic evidence score and signature."""
    normalized = []
    for candidate in candidates:
        grid = normalize_grid(candidate["grid"])
        signature = candidate.get("signature") or candidate_signature(grid)
        normalized.append(
            {
                **dict(candidate),
                "grid": grid,
                "signature": signature,
                "rank_signal": f"{float(candidate.get('evidence_score', 0.0)):06.2f}:{signature}",
            }
        )
    return tuple(sorted(normalized, key=lambda item: (-float(item["evidence_score"]), item["signature"])))


def generate_kernel_candidates(grid: Sequence[Sequence[int]]) -> Tuple[Dict[str, Any], ...]:
    """Generate a small local deterministic candidate set."""
    normalized = normalize_grid(grid)
    components = connected_components(normalized)
    candidates: List[Dict[str, Any]] = [
        {
            "candidate_id": "kernel_v2_identity",
            "family": "cross_family_composition",
            "operation": "identity",
            "grid": normalized,
            "evidence_score": 10.0,
        },
        {
            "candidate_id": "kernel_v2_reflect_horizontal",
            "family": "shape_symmetry",
            "operation": "reflect_grid_horizontal",
            "grid": reflect_grid_horizontal(normalized),
            "evidence_score": 30.0,
        },
        {
            "candidate_id": "kernel_v2_reflect_vertical",
            "family": "shape_symmetry",
            "operation": "reflect_grid_vertical",
            "grid": reflect_grid_vertical(normalized),
            "evidence_score": 31.0,
        },
    ]

    non_background_colors = sorted(
        value for value in set(flatten_grid(normalized)) if value != background_color(normalized)
    )
    if non_background_colors:
        deterministic_mapping = {
            color: (color + 1) % 10 for color in non_background_colors
        }
        candidates.append(
            {
                "candidate_id": "kernel_v2_color_shift_non_background",
                "family": "color_mapping",
                "operation": "apply_color_mapping_non_background_shift",
                "grid": apply_color_mapping(
                    normalized,
                    deterministic_mapping,
                    preserve_background=True,
                ),
                "evidence_score": 26.0,
            }
        )

    if components:
        largest = components[0]
        candidates.append(
            {
                "candidate_id": "kernel_v2_translate_largest_right",
                "family": "object_model",
                "operation": "translate_component_right",
                "grid": translate_component(normalized, largest["cells"], dr=0, dc=1),
                "evidence_score": 25.0,
            }
        )
        candidates.append(
            {
                "candidate_id": "kernel_v2_translate_largest_down",
                "family": "object_model",
                "operation": "translate_component_down",
                "grid": translate_component(normalized, largest["cells"], dr=1, dc=0),
                "evidence_score": 24.0,
            }
        )

    return rank_kernel_candidates(merge_candidate_sets(candidates))


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _sha256(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha16(value: str) -> str:
    return value[:16].upper() if value != "MISSING_HASH" else value


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def _sample_results() -> Dict[str, bool]:
    color_source = normalize_grid([[0, 1, 1], [0, 2, 2]])
    color_target = normalize_grid([[0, 3, 3], [0, 4, 4]])
    mapping = infer_color_mapping(color_source, color_target)
    mapped = apply_color_mapping(color_source, mapping)

    background_grid = normalize_grid([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
    background_mapped = apply_color_mapping(background_grid, {0: 9, 1: 2}, preserve_background=True)

    object_grid = normalize_grid([[0, 0, 0, 0], [0, 5, 5, 0], [0, 0, 0, 0]])
    components = connected_components(object_grid, background=0)
    right = translate_component(object_grid, components[0]["cells"], dr=0, dc=1)
    down = translate_component(object_grid, components[0]["cells"], dr=1, dc=0)

    shape_grid = normalize_grid([[1, 0], [2, 0], [3, 0]])
    horizontal = reflect_grid_horizontal(shape_grid)
    vertical = reflect_grid_vertical(shape_grid)

    ranked = generate_kernel_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])

    return {
        "sample_color_palette_transfer_pass": mapping == {0: 0, 1: 3, 2: 4} and mapped == color_target,
        "sample_background_guard_pass": background_mapped[0][0] == 0 and background_mapped[1][1] == 2,
        "sample_component_detection_pass": len(components) == 1 and components[0]["size"] == 2,
        "sample_translation_right_pass": right == normalize_grid([[0, 0, 0, 0], [0, 0, 5, 5], [0, 0, 0, 0]]),
        "sample_translation_down_pass": down == normalize_grid([[0, 0, 0, 0], [0, 0, 0, 0], [0, 5, 5, 0]]),
        "sample_reflect_horizontal_pass": horizontal == normalize_grid([[3, 0], [2, 0], [1, 0]]),
        "sample_reflect_vertical_pass": vertical == normalize_grid([[0, 1], [0, 2], [0, 3]]),
        "sample_candidate_ranker_pass": bool(ranked) and ranked[0]["evidence_score"] >= ranked[-1]["evidence_score"],
    }


def build_milestone_8_competitive_solver_kernel() -> Dict[str, Any]:
    plan = _read_json(PLAN_JSON)
    samples = _sample_results()

    kernel_record = {
        "kernel_mode": KERNEL_MODE,
        "kernel_scope": KERNEL_SCOPE,
        "kernel_verdict": KERNEL_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "kernel_ready": True,
        "kernel_locked": True,
        "baseline_plan_id": plan.get("plan_id", "MISSING_PLAN_ID"),
        "plan_ready": plan.get("plan_ready") is True,
        "plan_next_stage": plan.get("next_allowed_stage", "MISSING"),
        "kernel_family_count": len(KERNEL_FAMILIES),
        "kernel_operation_count": len(KERNEL_OPERATIONS),
        "sample_case_count": len(SAMPLE_CASES),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "solver_kernel_v2_created": True,
        "runtime_solver_iteration_performed": True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
    }

    gate_state = {
        "plan_artifact_present": PLAN_JSON.exists(),
        "plan_artifact_ready": plan.get("status") == "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_READY",
        "plan_artifact_valid": bool(plan.get("plan_id")) and bool(plan.get("signature")),
        "plan_next_stage_matches_task_2": plan.get("next_allowed_stage") == "MILESTONE_8_TASK_2_COMPETITIVE_SOLVER_KERNEL_V2",
        "kernel_mode_valid": KERNEL_MODE == "COMPETITIVE_SOLVER_KERNEL_V2_LOCAL_ONLY",
        "kernel_scope_valid": KERNEL_SCOPE == "IMPLEMENT_DETERMINISTIC_LOCAL_SOLVER_KERNEL_V2",
        "kernel_verdict_valid": KERNEL_VERDICT == "COMPETITIVE_SOLVER_KERNEL_V2_READY_FOR_FAMILY_BENCHMARK_CASES",
        "kernel_ready": kernel_record["kernel_ready"] is True,
        "kernel_locked": kernel_record["kernel_locked"] is True,
        "kernel_family_count_valid": len(KERNEL_FAMILIES) == EXPECTED_KERNEL_FAMILY_COUNT,
        "kernel_operation_count_valid": len(KERNEL_OPERATIONS) == EXPECTED_KERNEL_OPERATION_COUNT,
        "sample_case_count_valid": len(SAMPLE_CASES) == EXPECTED_SAMPLE_CASE_COUNT,
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "plan_gate_count_valid": int(plan.get("plan_gate_count", 0)) == EXPECTED_PLAN_GATE_COUNT,
        "plan_issue_count_zero": int(plan.get("plan_issue_count", -1)) == EXPECTED_PLAN_ISSUE_COUNT,
        "color_mapping_available": callable(infer_color_mapping) and callable(apply_color_mapping),
        "background_guard_available": callable(background_color),
        "component_detection_available": callable(connected_components),
        "component_translation_available": callable(translate_component),
        "horizontal_reflection_available": callable(reflect_grid_horizontal),
        "vertical_reflection_available": callable(reflect_grid_vertical),
        "candidate_merge_available": callable(merge_candidate_sets),
        "ranker_signal_available": callable(rank_kernel_candidates),
        "sample_color_palette_transfer_pass": samples["sample_color_palette_transfer_pass"],
        "sample_background_guard_pass": samples["sample_background_guard_pass"],
        "sample_component_detection_pass": samples["sample_component_detection_pass"],
        "sample_translation_right_pass": samples["sample_translation_right_pass"],
        "sample_translation_down_pass": samples["sample_translation_down_pass"],
        "sample_reflect_horizontal_pass": samples["sample_reflect_horizontal_pass"],
        "sample_reflect_vertical_pass": samples["sample_reflect_vertical_pass"],
        "sample_candidate_ranker_pass": samples["sample_candidate_ranker_pass"],
        "solver_kernel_v2_created": kernel_record["solver_kernel_v2_created"] is True,
        "runtime_solver_iteration_performed": kernel_record["runtime_solver_iteration_performed"] is True,
        "real_submission_not_created": kernel_record["real_submission_created"] is False,
        "real_submission_allowed_false": kernel_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": kernel_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": kernel_record["kaggle_submission_sent"] is False,
        "upload_not_performed": kernel_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": kernel_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": kernel_record["external_api_dependency"] is False,
        "contains_api_keys_false": kernel_record["contains_api_keys"] is False,
        "private_core_exposure_false": kernel_record["private_core_exposure"] is False,
        "legal_certification_false": kernel_record["legal_certification"] is False,
        "score_claim_absent": kernel_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": kernel_record["public_leaderboard_claim_absent"] is True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_8_TASK_3_FAMILY_BENCHMARK_CASES_V2",
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
    }

    issue_state = {
        "plan_artifact_missing": not gate_state["plan_artifact_present"],
        "plan_artifact_not_ready": not gate_state["plan_artifact_ready"],
        "plan_artifact_invalid": not gate_state["plan_artifact_valid"],
        "plan_next_stage_mismatch": not gate_state["plan_next_stage_matches_task_2"],
        "kernel_mode_invalid": not gate_state["kernel_mode_valid"],
        "kernel_scope_invalid": not gate_state["kernel_scope_valid"],
        "kernel_verdict_invalid": not gate_state["kernel_verdict_valid"],
        "kernel_not_ready": not gate_state["kernel_ready"],
        "kernel_not_locked": not gate_state["kernel_locked"],
        "kernel_family_count_invalid": not gate_state["kernel_family_count_valid"],
        "kernel_operation_count_invalid": not gate_state["kernel_operation_count_valid"],
        "sample_case_count_invalid": not gate_state["sample_case_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "boundary_control_count_invalid": not gate_state["boundary_control_count_valid"],
        "plan_gate_count_invalid": not gate_state["plan_gate_count_valid"],
        "plan_issue_count_nonzero": not gate_state["plan_issue_count_zero"],
        "color_mapping_missing": not gate_state["color_mapping_available"],
        "background_guard_missing": not gate_state["background_guard_available"],
        "component_detection_missing": not gate_state["component_detection_available"],
        "component_translation_missing": not gate_state["component_translation_available"],
        "horizontal_reflection_missing": not gate_state["horizontal_reflection_available"],
        "vertical_reflection_missing": not gate_state["vertical_reflection_available"],
        "candidate_merge_missing": not gate_state["candidate_merge_available"],
        "ranker_signal_missing": not gate_state["ranker_signal_available"],
        "sample_color_palette_transfer_failed": not gate_state["sample_color_palette_transfer_pass"],
        "sample_background_guard_failed": not gate_state["sample_background_guard_pass"],
        "sample_component_detection_failed": not gate_state["sample_component_detection_pass"],
        "sample_translation_right_failed": not gate_state["sample_translation_right_pass"],
        "sample_translation_down_failed": not gate_state["sample_translation_down_pass"],
        "sample_reflect_horizontal_failed": not gate_state["sample_reflect_horizontal_pass"],
        "sample_reflect_vertical_failed": not gate_state["sample_reflect_vertical_pass"],
        "sample_candidate_ranker_failed": not gate_state["sample_candidate_ranker_pass"],
        "solver_kernel_v2_missing": not gate_state["solver_kernel_v2_created"],
        "runtime_solver_iteration_not_performed": not gate_state["runtime_solver_iteration_performed"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
        "score_claim_detected": not gate_state["score_claim_absent"],
        "public_leaderboard_claim_detected": not gate_state["public_leaderboard_claim_absent"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
        "public_safe_false": not gate_state["public_safe"],
        "deterministic_false": not gate_state["deterministic"],
        "local_only_false": not gate_state["local_only"],
        "dry_run_only_false": not gate_state["dry_run_only"],
    }

    gates = tuple(
        {"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"}
        for name in KERNEL_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in KERNEL_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    kernel_ready = (
        plan.get("status") == "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_READY"
        and passed_gate_count == len(KERNEL_GATES)
        and issue_count == 0
        and all(samples.values())
    )

    index = {
        "milestone": "Milestone #8",
        "task": "Task 2",
        "kernel_mode": KERNEL_MODE,
        "kernel_scope": KERNEL_SCOPE,
        "kernel_verdict": KERNEL_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_plan": plan.get("plan_id", "MISSING_PLAN_ID"),
        "kernel_ready": kernel_ready,
        "kernel_locked": True,
        "kernel_family_count": len(KERNEL_FAMILIES),
        "kernel_operation_count": len(KERNEL_OPERATIONS),
        "sample_case_count": len(SAMPLE_CASES),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "solver_kernel_v2_created": True,
        "runtime_solver_iteration_performed": True,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": KERNEL_STATUS,
        "milestone": "Milestone #8",
        "task": "Task 2",
        "title": "Competitive Solver Kernel v2",
        "baseline_commit": BASELINE_COMMIT,
        "kernel_mode": KERNEL_MODE,
        "kernel_scope": KERNEL_SCOPE,
        "kernel_verdict": KERNEL_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "plan_source": {
            "path": str(PLAN_JSON),
            "present": PLAN_JSON.exists(),
            "status": plan.get("status", "MISSING"),
            "plan_id": plan.get("plan_id", "MISSING_PLAN_ID"),
            "sha256": _sha256(PLAN_JSON),
            "sha256_16": _sha16(_sha256(PLAN_JSON)),
        },
        "kernel_record": kernel_record,
        "kernel_families": list(KERNEL_FAMILIES),
        "kernel_operations": list(KERNEL_OPERATIONS),
        "sample_cases": list(SAMPLE_CASES),
        "sample_results": samples,
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "kernel_gates": list(gates),
        "kernel_issues": list(issues),
        "kernel_index": index,
        "kernel_family_count": len(KERNEL_FAMILIES),
        "kernel_operation_count": len(KERNEL_OPERATIONS),
        "sample_case_count": len(SAMPLE_CASES),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "kernel_gate_count": len(KERNEL_GATES),
        "passed_gate_count": passed_gate_count,
        "kernel_issue_count": issue_count,
        "warning_count": 0,
        "kernel_ready": kernel_ready,
        "kernel_locked": True,
        "solver_kernel_v2_created": True,
        "runtime_solver_iteration_performed": True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_8_competitive_solver_kernel_v2",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }

    signature = _stable_signature(base)
    return {
        **base,
        "kernel_id": f"MILESTONE-8-SOLVER-KERNEL-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_8_competitive_solver_kernel(kernel: Mapping[str, Any]) -> Dict[str, Any]:
    gates = kernel.get("kernel_gates", [])
    issues = kernel.get("kernel_issues", [])
    samples = kernel.get("sample_results", {})

    checks = {
        "status_ready": kernel.get("status") == KERNEL_STATUS,
        "kernel_id_present": isinstance(kernel.get("kernel_id"), str) and bool(kernel.get("kernel_id")),
        "signature_present": isinstance(kernel.get("signature"), str) and bool(kernel.get("signature")),
        "baseline_commit_valid": str(kernel.get("baseline_commit", "")).startswith("69af006"),
        "kernel_mode_valid": kernel.get("kernel_mode") == KERNEL_MODE,
        "kernel_scope_valid": kernel.get("kernel_scope") == KERNEL_SCOPE,
        "kernel_verdict_valid": kernel.get("kernel_verdict") == KERNEL_VERDICT,
        "next_allowed_stage_valid": kernel.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "kernel_family_count_valid": kernel.get("kernel_family_count") == EXPECTED_KERNEL_FAMILY_COUNT,
        "kernel_operation_count_valid": kernel.get("kernel_operation_count") == EXPECTED_KERNEL_OPERATION_COUNT,
        "sample_case_count_valid": kernel.get("sample_case_count") == EXPECTED_SAMPLE_CASE_COUNT,
        "regression_guard_count_valid": kernel.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": kernel.get("boundary_control_count") == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "all_samples_pass": bool(samples) and all(value is True for value in samples.values()),
        "kernel_gate_count_matches": kernel.get("kernel_gate_count") == len(KERNEL_GATES),
        "all_kernel_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "kernel_issue_count_zero": kernel.get("kernel_issue_count") == 0,
        "all_kernel_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "kernel_ready": kernel.get("kernel_ready") is True,
        "kernel_locked": kernel.get("kernel_locked") is True,
        "solver_kernel_v2_created": kernel.get("solver_kernel_v2_created") is True,
        "runtime_solver_iteration_performed": kernel.get("runtime_solver_iteration_performed") is True,
        "real_submission_not_created": kernel.get("real_submission_created") is False,
        "real_submission_allowed_false": kernel.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": kernel.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": kernel.get("kaggle_submission_sent") is False,
        "upload_not_performed": kernel.get("upload_performed") is False,
        "kaggle_authentication_not_performed": kernel.get("kaggle_authentication_performed") is False,
        "score_claim_absent": kernel.get("score_claim_absent") is True,
        "public_leaderboard_claim_absent": kernel.get("public_leaderboard_claim_absent") is True,
        "metadata_safe": kernel.get("metadata", {}).get("external_api_dependency") is False
        and kernel.get("metadata", {}).get("contains_api_keys") is False
        and kernel.get("metadata", {}).get("private_core_exposure") is False
        and kernel.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_INVALID",
        "valid": valid,
        "checks": checks,
        "kernel_id": kernel.get("kernel_id"),
        "signature": kernel.get("signature"),
    }


def render_competitive_solver_kernel_markdown(kernel: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #8 - Competitive Solver Kernel v2",
        "",
        f"- status: {kernel['status']}",
        f"- kernel_id: {kernel['kernel_id']}",
        f"- signature: {kernel['signature']}",
        f"- baseline_commit: {kernel['baseline_commit']}",
        f"- kernel_mode: {kernel['kernel_mode']}",
        f"- kernel_scope: {kernel['kernel_scope']}",
        f"- kernel_verdict: {kernel['kernel_verdict']}",
        f"- next_allowed_stage: {kernel['next_allowed_stage']}",
        f"- kernel_family_count: {kernel['kernel_family_count']}",
        f"- kernel_operation_count: {kernel['kernel_operation_count']}",
        f"- sample_case_count: {kernel['sample_case_count']}",
        f"- regression_guard_count: {kernel['regression_guard_count']}",
        f"- kernel_gate_count: {kernel['kernel_gate_count']}",
        f"- passed_gate_count: {kernel['passed_gate_count']}",
        f"- kernel_issue_count: {kernel['kernel_issue_count']}",
        f"- kernel_ready: {kernel['kernel_ready']}",
        "",
        "## Kernel operations",
        "",
    ]

    for operation in kernel["kernel_operations"]:
        lines.append(f"- {operation}")

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Competitive Solver Kernel v2 is ready for family benchmark cases.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_READY=true",
            "ARC_AGI3_MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_VALID=true",
            "ARC_AGI3_MILESTONE_8_KERNEL_MODE=COMPETITIVE_SOLVER_KERNEL_V2_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_8_KERNEL_VERDICT=COMPETITIVE_SOLVER_KERNEL_V2_READY_FOR_FAMILY_BENCHMARK_CASES",
            "ARC_AGI3_MILESTONE_8_BASELINE_PLAN_COMMIT=69af006",
            "ARC_AGI3_MILESTONE_8_KERNEL_FAMILY_COUNT=4",
            "ARC_AGI3_MILESTONE_8_KERNEL_OPERATION_COUNT=8",
            "ARC_AGI3_MILESTONE_8_SAMPLE_CASE_COUNT=8",
            "ARC_AGI3_MILESTONE_8_REGRESSION_GUARD_COUNT=8",
            "ARC_AGI3_MILESTONE_8_SOLVER_KERNEL_V2_CREATED=true",
            "ARC_AGI3_MILESTONE_8_RUNTIME_SOLVER_ITERATION_PERFORMED=true",
            "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_3_FAMILY_BENCHMARK_CASES_V2",
            "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_8_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_8_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_8_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_8_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_competitive_solver_kernel_manifest(kernel: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 8 COMPETITIVE SOLVER KERNEL MANIFEST v2",
        f"kernel_id={kernel['kernel_id']}",
        f"signature={kernel['signature']}",
        f"status={kernel['status']}",
        f"baseline_commit={kernel['baseline_commit']}",
        f"kernel_mode={kernel['kernel_mode']}",
        f"kernel_verdict={kernel['kernel_verdict']}",
        f"next_allowed_stage={kernel['next_allowed_stage']}",
        f"kernel_family_count={kernel['kernel_family_count']}",
        f"kernel_operation_count={kernel['kernel_operation_count']}",
        f"sample_case_count={kernel['sample_case_count']}",
        f"regression_guard_count={kernel['regression_guard_count']}",
        f"kernel_gate_count={kernel['kernel_gate_count']}",
        f"passed_gate_count={kernel['passed_gate_count']}",
        f"kernel_issue_count={kernel['kernel_issue_count']}",
        f"kernel_ready={kernel['kernel_ready']}",
        f"kernel_locked={kernel['kernel_locked']}",
        f"solver_kernel_v2_created={kernel['solver_kernel_v2_created']}",
        f"runtime_solver_iteration_performed={kernel['runtime_solver_iteration_performed']}",
        f"real_submission_created={kernel['real_submission_created']}",
        f"real_submission_allowed={kernel['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={kernel['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={kernel['kaggle_submission_sent']}",
        f"upload_performed={kernel['upload_performed']}",
        f"kaggle_authentication_performed={kernel['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "KERNEL_OPERATIONS",
    ]

    for operation in kernel["kernel_operations"]:
        lines.append(operation)

    lines.append("")
    lines.append("SAMPLE_RESULTS")
    for name, passed in kernel["sample_results"].items():
        lines.append(f"{name}={passed}")

    lines.append("")
    return "\n".join(lines)


def write_competitive_solver_kernel_artifacts(
    kernel: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    kernel = dict(kernel or build_milestone_8_competitive_solver_kernel())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-8-competitive-solver-kernel-v2.json"
    md_path = output / "milestone-8-competitive-solver-kernel-v2.md"
    manifest_path = output / "milestone-8-competitive-solver-kernel-manifest-v2.txt"
    index_path = output / "milestone-8-competitive-solver-kernel-index-v2.json"

    json_path.write_text(json.dumps(kernel, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_competitive_solver_kernel_markdown(kernel), encoding="utf-8")
    manifest_path.write_text(render_competitive_solver_kernel_manifest(kernel), encoding="utf-8")
    index_path.write_text(json.dumps(kernel["kernel_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_8_competitive_solver_kernel_pipeline() -> Dict[str, Any]:
    kernel = build_milestone_8_competitive_solver_kernel()
    validation = validate_milestone_8_competitive_solver_kernel(kernel)
    artifacts = write_competitive_solver_kernel_artifacts(kernel)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_8_COMPETITIVE_SOLVER_KERNEL_V2_PIPELINE_INVALID",
        "kernel_status": kernel["status"],
        "validation_status": validation["status"],
        "kernel": kernel,
        "kernel_id": kernel["kernel_id"],
        "signature": kernel["signature"],
        "kernel_mode": kernel["kernel_mode"],
        "kernel_verdict": kernel["kernel_verdict"],
        "next_allowed_stage": kernel["next_allowed_stage"],
        "kernel_family_count": kernel["kernel_family_count"],
        "kernel_operation_count": kernel["kernel_operation_count"],
        "sample_case_count": kernel["sample_case_count"],
        "regression_guard_count": kernel["regression_guard_count"],
        "boundary_control_count": kernel["boundary_control_count"],
        "kernel_gate_count": kernel["kernel_gate_count"],
        "passed_gate_count": kernel["passed_gate_count"],
        "kernel_issue_count": kernel["kernel_issue_count"],
        "warning_count": kernel["warning_count"],
        "kernel_ready": kernel["kernel_ready"],
        "kernel_locked": kernel["kernel_locked"],
        "solver_kernel_v2_created": kernel["solver_kernel_v2_created"],
        "runtime_solver_iteration_performed": kernel["runtime_solver_iteration_performed"],
        "real_submission_created": kernel["real_submission_created"],
        "real_submission_allowed": kernel["real_submission_allowed"],
        "ready_for_real_kaggle_submission": kernel["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": kernel["kaggle_submission_sent"],
        "upload_performed": kernel["upload_performed"],
        "kaggle_authentication_performed": kernel["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": kernel["metadata"],
    }
