"""Deterministic rule hypothesis generation for HBCE ARC-AGI-3 public baseline.

Rule Hypothesis v1 creates traceable candidate transformation hypotheses from
a local ARC-like grid and the public object model.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.object_model import ObjectModel, build_object_model, extract_grid


@dataclass(frozen=True)
class RuleHypothesis:
    hypothesis_id: str
    rule_type: str
    description: str
    confidence: float
    evidence: Dict[str, Any]
    parameters: Dict[str, Any]
    signature: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RuleHypothesisSet:
    status: str
    hypothesis_count: int
    task_id: str
    object_model_signature: str
    hypotheses: List[RuleHypothesis]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["hypotheses"] = [hypothesis.to_dict() for hypothesis in self.hypotheses]
        return data


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _make_hypothesis(
    index: int,
    *,
    rule_type: str,
    description: str,
    confidence: float,
    evidence: Dict[str, Any],
    parameters: Dict[str, Any],
) -> RuleHypothesis:
    basis = {
        "rule_type": rule_type,
        "description": description,
        "confidence": round(confidence, 6),
        "evidence": evidence,
        "parameters": parameters,
    }
    signature = _stable_signature(basis)

    return RuleHypothesis(
        hypothesis_id=f"RH-{index:04d}-{signature[:8]}",
        rule_type=rule_type,
        description=description,
        confidence=round(confidence, 6),
        evidence=evidence,
        parameters=parameters,
        signature=signature,
    )


def _task_id_from_payload(payload: Any) -> str:
    if isinstance(payload, dict):
        for key in ("task_id", "id"):
            value = payload.get(key)
            if value:
                return str(value)

        loaded_task = payload.get("loaded_task")
        if isinstance(loaded_task, dict):
            value = loaded_task.get("task_id")
            if value:
                return str(value)

        normalized = payload.get("normalized")
        if isinstance(normalized, dict):
            value = normalized.get("task_id") or normalized.get("id")
            if value:
                return str(value)

        run = payload.get("run")
        if isinstance(run, dict):
            value = run.get("task_id")
            if value:
                return str(value)

    return "anonymous-task"


def _model_data_from_payload(payload: Any, *, background_value: int = 0) -> Dict[str, Any]:
    if isinstance(payload, ObjectModel):
        return payload.to_dict()

    if isinstance(payload, dict) and payload.get("status") == "OBJECT_MODEL_READY":
        return payload

    return build_object_model(payload, background_value=background_value).to_dict()


def _try_extract_grid(payload: Any) -> Optional[List[List[int]]]:
    try:
        return extract_grid(payload)
    except ValueError:
        return None


def _is_horizontal_symmetric(grid: List[List[int]]) -> bool:
    return all(row == list(reversed(row)) for row in grid)


def _is_vertical_symmetric(grid: List[List[int]]) -> bool:
    return grid == list(reversed(grid))


def _dominant_non_background_value(value_counts: Dict[str, int], background_value: int) -> Optional[Dict[str, Any]]:
    candidates = [
        (int(value), count)
        for value, count in value_counts.items()
        if int(value) != background_value
    ]

    if not candidates:
        return None

    candidates.sort(key=lambda item: (-item[1], item[0]))
    value, count = candidates[0]

    return {"value": value, "count": count}


def generate_rule_hypotheses(
    payload: Any,
    *,
    background_value: int = 0,
) -> RuleHypothesisSet:
    """Generate deterministic public rule hypotheses from a grid/object model."""

    model = _model_data_from_payload(payload, background_value=background_value)
    grid = _try_extract_grid(payload)
    task_id = _task_id_from_payload(payload)

    object_count = int(model.get("object_count", 0))
    object_density = float(model.get("object_density", 0.0))
    value_counts = model.get("value_counts", {})
    objects = model.get("objects", [])
    model_signature = str(model.get("signature", "NO_OBJECT_MODEL_SIGNATURE"))

    hypotheses: List[RuleHypothesis] = []

    hypotheses.append(
        _make_hypothesis(
            len(hypotheses) + 1,
            rule_type="preserve_structure",
            description="Preserve the observed non-background object structure as the baseline candidate rule.",
            confidence=0.5 if object_count else 0.2,
            evidence={
                "object_count": object_count,
                "object_density": object_density,
                "object_model_signature": model_signature,
            },
            parameters={
                "background_value": background_value,
                "preserve_object_values": True,
                "preserve_connected_components": True,
            },
        )
    )

    hypotheses.append(
        _make_hypothesis(
            len(hypotheses) + 1,
            rule_type="object_count_invariant",
            description="Treat the number of detected objects as an invariant candidate.",
            confidence=0.45 if object_count else 0.15,
            evidence={
                "object_count": object_count,
                "connectivity": model.get("metadata", {}).get("connectivity"),
            },
            parameters={
                "expected_object_count": object_count,
            },
        )
    )

    dominant = _dominant_non_background_value(value_counts, background_value)
    if dominant is not None:
        hypotheses.append(
            _make_hypothesis(
                len(hypotheses) + 1,
                rule_type="dominant_value_focus",
                description="Prioritize the dominant non-background value as a candidate transformation anchor.",
                confidence=0.4,
                evidence={
                    "dominant_value": dominant["value"],
                    "dominant_count": dominant["count"],
                    "value_counts": value_counts,
                },
                parameters={
                    "anchor_value": dominant["value"],
                    "background_value": background_value,
                },
            )
        )

    if grid is not None:
        hypotheses.append(
            _make_hypothesis(
                len(hypotheses) + 1,
                rule_type="horizontal_symmetry_candidate",
                description="Evaluate horizontal mirror symmetry as a candidate transformation rule.",
                confidence=0.65 if _is_horizontal_symmetric(grid) else 0.25,
                evidence={
                    "horizontal_symmetric": _is_horizontal_symmetric(grid),
                    "width": len(grid[0]) if grid else 0,
                    "height": len(grid),
                },
                parameters={
                    "axis": "horizontal",
                    "operation": "mirror_or_preserve",
                },
            )
        )

        hypotheses.append(
            _make_hypothesis(
                len(hypotheses) + 1,
                rule_type="vertical_symmetry_candidate",
                description="Evaluate vertical mirror symmetry as a candidate transformation rule.",
                confidence=0.65 if _is_vertical_symmetric(grid) else 0.25,
                evidence={
                    "vertical_symmetric": _is_vertical_symmetric(grid),
                    "width": len(grid[0]) if grid else 0,
                    "height": len(grid),
                },
                parameters={
                    "axis": "vertical",
                    "operation": "mirror_or_preserve",
                },
            )
        )

    if objects:
        largest_object = sorted(
            objects,
            key=lambda item: (-int(item.get("cell_count", 0)), int(item.get("value", 0)), str(item.get("object_id", ""))),
        )[0]

        hypotheses.append(
            _make_hypothesis(
                len(hypotheses) + 1,
                rule_type="largest_object_anchor",
                description="Use the largest detected object as a candidate spatial anchor.",
                confidence=0.42,
                evidence={
                    "object_id": largest_object.get("object_id"),
                    "value": largest_object.get("value"),
                    "cell_count": largest_object.get("cell_count"),
                    "bbox": largest_object.get("bbox"),
                    "density": largest_object.get("density"),
                },
                parameters={
                    "anchor_object_id": largest_object.get("object_id"),
                    "anchor_value": largest_object.get("value"),
                    "operation": "copy_move_or_expand",
                },
            )
        )

    signature_basis = {
        "task_id": task_id,
        "object_model_signature": model_signature,
        "hypotheses": [hypothesis.signature for hypothesis in hypotheses],
    }

    return RuleHypothesisSet(
        status="RULE_HYPOTHESIS_READY",
        hypothesis_count=len(hypotheses),
        task_id=task_id,
        object_model_signature=model_signature,
        hypotheses=hypotheses,
        metadata={
            "source": "rule_hypothesis_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "background_value": background_value,
            "signature": _stable_signature(signature_basis),
        },
    )


def validate_rule_hypothesis_set(hypothesis_set: RuleHypothesisSet | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Rule Hypothesis v1 public contract."""

    data = hypothesis_set.to_dict() if isinstance(hypothesis_set, RuleHypothesisSet) else dict(hypothesis_set)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    hypotheses = data.get("hypotheses")

    checks = {
        "status_ready": data.get("status") == "RULE_HYPOTHESIS_READY",
        "hypothesis_count_number": isinstance(data.get("hypothesis_count"), int),
        "hypotheses_list": isinstance(hypotheses, list),
        "hypothesis_count_matches": isinstance(hypotheses, list) and len(hypotheses) == data.get("hypothesis_count"),
        "task_id_present": bool(data.get("task_id")),
        "object_model_signature_present": bool(data.get("object_model_signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
    }

    valid = all(checks.values())

    return {
        "status": "RULE_HYPOTHESIS_VALID" if valid else "RULE_HYPOTHESIS_INVALID",
        "valid": valid,
        "checks": checks,
        "hypothesis_count": data.get("hypothesis_count"),
        "task_id": data.get("task_id"),
        "metadata": {
            "source": "rule_hypothesis_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }
