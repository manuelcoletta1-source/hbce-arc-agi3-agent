"""Local-only program synthesis candidate generator runtime adapter.

This module is deliberately small and deterministic. It normalizes generated
candidate dictionaries into a stable runtime-adjacent candidate contract.

It does not call external services.
It does not perform Kaggle evaluation.
It does not submit anything.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class RuntimeCandidate:
    candidate_id: str
    family: str
    operation: str
    program: tuple[str, ...]
    confidence: float
    source: str = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR"
    runtime_activation_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "family": self.family,
            "operation": self.operation,
            "program": list(self.program),
            "confidence": self.confidence,
            "source": self.source,
            "runtime_activation_allowed": self.runtime_activation_allowed,
        }


def _stable_id(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "RUNTIME-CANDIDATE-" + hashlib.sha256(encoded).hexdigest().upper()[:12]


def normalize_generated_candidate(candidate: dict[str, Any], *, index: int = 0) -> RuntimeCandidate:
    """Normalize a generated candidate into the runtime candidate contract."""

    family = str(candidate.get("family") or candidate.get("candidate_family") or "UNKNOWN_FAMILY")
    operation = str(candidate.get("operation") or candidate.get("name") or "UNKNOWN_OPERATION")

    raw_program = candidate.get("program")
    if isinstance(raw_program, str):
        program = (raw_program,)
    elif isinstance(raw_program, Iterable):
        program = tuple(str(step) for step in raw_program)
    else:
        program = (operation,)

    confidence_raw = candidate.get("confidence", candidate.get("score_hint", 0.0))
    try:
        confidence = float(confidence_raw)
    except (TypeError, ValueError):
        confidence = 0.0

    confidence = max(0.0, min(1.0, confidence))

    id_payload = {
        "index": index,
        "family": family,
        "operation": operation,
        "program": program,
        "confidence": confidence,
    }

    return RuntimeCandidate(
        candidate_id=_stable_id(id_payload),
        family=family,
        operation=operation,
        program=program,
        confidence=confidence,
        runtime_activation_allowed=False,
    )


def normalize_generated_candidates(candidates: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize all generated candidates in deterministic order."""

    normalized = [
        normalize_generated_candidate(candidate, index=index).to_dict()
        for index, candidate in enumerate(candidates)
        if isinstance(candidate, dict)
    ]

    return sorted(
        normalized,
        key=lambda item: (
            item["family"],
            item["operation"],
            item["candidate_id"],
        ),
    )
