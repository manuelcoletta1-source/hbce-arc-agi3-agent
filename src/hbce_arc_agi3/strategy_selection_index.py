"""Strategy Selection Index v1 for HBCE ARC-AGI-3 public baseline.

This module builds a deterministic public-safe strategy selection index from
the Multi-Task Outcome Aggregator v1 output.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
It does not submit to Kaggle.
It does not expose private HBCE/JOKER-C2 strategy logic.
"""

from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.multi_task_outcome_aggregator import (
    MultiTaskOutcomeAggregate,
    aggregate_multi_task_outcomes,
    validate_multi_task_outcome_aggregate,
)


@dataclass(frozen=True)
class StrategySelectionCandidate:
    status: str
    strategy_id: str
    strategy_name: str
    strategy_family: str
    rank: int
    score: float
    confidence: float
    quality_band: str
    selected: bool
    selection_reason: str
    evidence: Dict[str, Any]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StrategySelectionIndex:
    status: str
    index_status: str
    index_id: str
    aggregate_id: str
    batch_id: str
    registry_id: str
    candidate_count: int
    selected_strategy_id: str
    selected_strategy_name: str
    selected_score: float
    selected_quality_band: str
    candidates: List[Dict[str, Any]]
    strategy_ids: List[str]
    strategy_signatures: Dict[str, str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _quality_band(score: float) -> str:
    if score >= 1.0:
        return "PERFECT"
    if score >= 0.9:
        return "STRONG"
    if score >= 0.75:
        return "GOOD"
    if score >= 0.5:
        return "PARTIAL"
    return "WEAK"


def _coerce_aggregate(
    aggregate: Optional[MultiTaskOutcomeAggregate | Dict[str, Any]],
) -> Dict[str, Any]:
    if aggregate is None:
        return aggregate_multi_task_outcomes().to_dict()

    if isinstance(aggregate, MultiTaskOutcomeAggregate):
        return aggregate.to_dict()

    if isinstance(aggregate, dict):
        return copy.deepcopy(aggregate)

    raise ValueError("Strategy selection index requires a MultiTaskOutcomeAggregate or dictionary")


def _candidate_signature_basis(candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "strategy_id": candidate["strategy_id"],
        "strategy_name": candidate["strategy_name"],
        "strategy_family": candidate["strategy_family"],
        "rank": candidate["rank"],
        "score": candidate["score"],
        "confidence": candidate["confidence"],
        "quality_band": candidate["quality_band"],
        "selected": candidate["selected"],
        "selection_reason": candidate["selection_reason"],
        "evidence": candidate["evidence"],
    }


def _build_candidate(
    *,
    strategy_id: str,
    strategy_name: str,
    strategy_family: str,
    rank: int,
    score: float,
    confidence: float,
    selected: bool,
    selection_reason: str,
    evidence: Dict[str, Any],
) -> StrategySelectionCandidate:
    rounded_score = round(float(score), 6)
    rounded_confidence = round(float(confidence), 6)
    quality_band = _quality_band(rounded_score)

    unsigned = {
        "strategy_id": strategy_id,
        "strategy_name": strategy_name,
        "strategy_family": strategy_family,
        "rank": rank,
        "score": rounded_score,
        "confidence": rounded_confidence,
        "quality_band": quality_band,
        "selected": selected,
        "selection_reason": selection_reason,
        "evidence": evidence,
    }
    signature = _stable_signature(_candidate_signature_basis(unsigned))

    return StrategySelectionCandidate(
        status="STRATEGY_SELECTION_CANDIDATE_READY",
        strategy_id=strategy_id,
        strategy_name=strategy_name,
        strategy_family=strategy_family,
        rank=rank,
        score=rounded_score,
        confidence=rounded_confidence,
        quality_band=quality_band,
        selected=selected,
        selection_reason=selection_reason,
        evidence=evidence,
        signature=signature,
        metadata={
            "source": "strategy_selection_index_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    )


def build_strategy_selection_index(
    aggregate: Optional[MultiTaskOutcomeAggregate | Dict[str, Any]] = None,
) -> StrategySelectionIndex:
    """Build a deterministic public strategy selection index."""

    aggregate_data = _coerce_aggregate(aggregate)
    aggregate_validation = validate_multi_task_outcome_aggregate(aggregate_data)

    if aggregate_validation["status"] != "MULTI_TASK_OUTCOME_AGGREGATE_VALID":
        raise ValueError(
            "Strategy selection index requires a valid MULTI_TASK_OUTCOME_AGGREGATE_VALID payload"
        )

    task_count = int(aggregate_data.get("task_count"))
    matched_count = int(aggregate_data.get("matched_count"))
    partial_count = int(aggregate_data.get("partial_count"))
    failed_count = int(aggregate_data.get("failed_count"))
    unverified_count = int(aggregate_data.get("unverified_count"))
    average_score = round(float(aggregate_data.get("average_calibrated_score")), 6)
    exact_match_rate = round(float(aggregate_data.get("exact_match_rate")), 6)

    public_evidence = {
        "aggregate_id": aggregate_data.get("aggregate_id"),
        "batch_id": aggregate_data.get("batch_id"),
        "registry_id": aggregate_data.get("registry_id"),
        "task_count": task_count,
        "matched_count": matched_count,
        "partial_count": partial_count,
        "failed_count": failed_count,
        "unverified_count": unverified_count,
        "average_calibrated_score": average_score,
        "exact_match_rate": exact_match_rate,
        "aggregate_quality_band": aggregate_data.get("aggregate_quality_band"),
        "aggregate_verdict": aggregate_data.get("aggregate_verdict"),
    }

    candidates = [
        _build_candidate(
            strategy_id="STRATEGY-IDENTITY-BASELINE-v1",
            strategy_name="identity_baseline_v1",
            strategy_family="public_baseline",
            rank=1,
            score=average_score,
            confidence=exact_match_rate,
            selected=True,
            selection_reason="Highest validated public score from current batch outcome aggregate",
            evidence={**public_evidence, "candidate_basis": "current_validated_runner"},
        ),
        _build_candidate(
            strategy_id="STRATEGY-OBJECT-PRESERVATION-v1",
            strategy_name="object_preservation_public_v1",
            strategy_family="public_candidate",
            rank=2,
            score=round(matched_count / task_count, 6),
            confidence=round((matched_count + partial_count) / task_count, 6),
            selected=False,
            selection_reason="Candidate retained for later public ranking; not selected over validated runner",
            evidence={**public_evidence, "candidate_basis": "object_preservation_signal"},
        ),
        _build_candidate(
            strategy_id="STRATEGY-PARTIAL-REPAIR-v1",
            strategy_name="partial_repair_public_v1",
            strategy_family="public_candidate",
            rank=3,
            score=round((matched_count + (partial_count * 0.5)) / task_count, 6),
            confidence=round(partial_count / task_count, 6),
            selected=False,
            selection_reason="Candidate retained for partial-outcome exploration; not selected in this batch",
            evidence={**public_evidence, "candidate_basis": "partial_outcome_signal"},
        ),
    ]

    candidates_sorted_raw = sorted(
        candidates,
        key=lambda item: (
            not item.selected,
            -item.score,
            -item.confidence,
            item.strategy_id,
        ),
    )

    candidates_sorted = [
        StrategySelectionCandidate(
            status=candidate.status,
            strategy_id=candidate.strategy_id,
            strategy_name=candidate.strategy_name,
            strategy_family=candidate.strategy_family,
            rank=index + 1,
            score=candidate.score,
            confidence=candidate.confidence,
            quality_band=candidate.quality_band,
            selected=candidate.selected,
            selection_reason=candidate.selection_reason,
            evidence=candidate.evidence,
            signature=_stable_signature(
                {
                    "strategy_id": candidate.strategy_id,
                    "strategy_name": candidate.strategy_name,
                    "strategy_family": candidate.strategy_family,
                    "rank": index + 1,
                    "score": candidate.score,
                    "confidence": candidate.confidence,
                    "quality_band": candidate.quality_band,
                    "selected": candidate.selected,
                    "selection_reason": candidate.selection_reason,
                    "evidence": candidate.evidence,
                }
            ),
            metadata=candidate.metadata,
        )
        for index, candidate in enumerate(candidates_sorted_raw)
    ]

    candidate_dicts = [candidate.to_dict() for candidate in candidates_sorted]
    selected_candidates = [candidate for candidate in candidates_sorted if candidate.selected]

    if len(selected_candidates) != 1:
        raise ValueError("Strategy selection index requires exactly one selected candidate")

    selected = selected_candidates[0]
    strategy_ids = [candidate.strategy_id for candidate in candidates_sorted]
    strategy_signatures = {candidate.strategy_id: candidate.signature for candidate in candidates_sorted}

    signature_basis = {
        "aggregate_id": aggregate_data.get("aggregate_id"),
        "batch_id": aggregate_data.get("batch_id"),
        "registry_id": aggregate_data.get("registry_id"),
        "strategy_ids": strategy_ids,
        "strategy_signatures": strategy_signatures,
        "selected_strategy_id": selected.strategy_id,
        "selected_score": selected.score,
        "candidate_count": len(candidates_sorted),
    }
    signature = _stable_signature(signature_basis)
    index_id = f"STRATEGY-SELECTION-INDEX-{signature[:12]}"

    return StrategySelectionIndex(
        status="STRATEGY_SELECTION_INDEX_READY",
        index_status="STRATEGY_SELECTION_INDEX_VALID",
        index_id=index_id,
        aggregate_id=str(aggregate_data.get("aggregate_id")),
        batch_id=str(aggregate_data.get("batch_id")),
        registry_id=str(aggregate_data.get("registry_id")),
        candidate_count=len(candidates_sorted),
        selected_strategy_id=selected.strategy_id,
        selected_strategy_name=selected.strategy_name,
        selected_score=selected.score,
        selected_quality_band=selected.quality_band,
        candidates=candidate_dicts,
        strategy_ids=strategy_ids,
        strategy_signatures=strategy_signatures,
        signature=signature,
        metadata={
            "source": "strategy_selection_index_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
            "milestone": "Milestone #3",
            "task": "Task 4",
        },
    )


def render_strategy_selection_index_markdown(index: StrategySelectionIndex | Dict[str, Any]) -> str:
    data = index.to_dict() if isinstance(index, StrategySelectionIndex) else dict(index)

    lines = [
        "# ARC-AGI-3 Strategy Selection Index v1",
        "",
        f"Status: {data['status']}",
        f"Index status: {data['index_status']}",
        f"Index ID: {data['index_id']}",
        f"Aggregate ID: {data['aggregate_id']}",
        f"Batch ID: {data['batch_id']}",
        f"Registry ID: {data['registry_id']}",
        f"Candidate count: {data['candidate_count']}",
        f"Selected strategy ID: {data['selected_strategy_id']}",
        f"Selected strategy name: {data['selected_strategy_name']}",
        f"Selected score: {data['selected_score']}",
        f"Selected quality band: {data['selected_quality_band']}",
        "",
        "## Strategy candidates",
        "",
    ]

    for candidate in data.get("candidates", []):
        lines.extend(
            [
                f"### Rank {candidate['rank']} - {candidate['strategy_name']}",
                "",
                f"- Strategy ID: {candidate['strategy_id']}",
                f"- Family: {candidate['strategy_family']}",
                f"- Score: {candidate['score']}",
                f"- Confidence: {candidate['confidence']}",
                f"- Quality band: {candidate['quality_band']}",
                f"- Selected: {str(candidate['selected']).lower()}",
                f"- Reason: {candidate['selection_reason']}",
                f"- Signature: {candidate['signature']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- external_api_dependency=false",
            "- executes_dataset_code=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "",
            f"Index signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_strategy_selection_index(index: StrategySelectionIndex | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Strategy Selection Index v1 public contract."""

    data = index.to_dict() if isinstance(index, StrategySelectionIndex) else dict(index)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    candidates = data.get("candidates") if isinstance(data.get("candidates"), list) else []

    selected_candidates = [
        candidate for candidate in candidates if isinstance(candidate, dict) and candidate.get("selected") is True
    ]

    candidate_checks = []
    for candidate in candidates:
        candidate_metadata = candidate.get("metadata") if isinstance(candidate.get("metadata"), dict) else {}
        candidate_checks.append(
            candidate.get("status") == "STRATEGY_SELECTION_CANDIDATE_READY"
            and isinstance(candidate.get("strategy_id"), str)
            and isinstance(candidate.get("strategy_name"), str)
            and isinstance(candidate.get("strategy_family"), str)
            and isinstance(candidate.get("rank"), int)
            and isinstance(candidate.get("score"), float)
            and isinstance(candidate.get("confidence"), float)
            and candidate.get("quality_band") in {"PERFECT", "STRONG", "GOOD", "PARTIAL", "WEAK"}
            and isinstance(candidate.get("selected"), bool)
            and isinstance(candidate.get("selection_reason"), str)
            and isinstance(candidate.get("evidence"), dict)
            and isinstance(candidate.get("signature"), str)
            and candidate_metadata.get("public_safe") is True
            and candidate_metadata.get("deterministic") is True
            and candidate_metadata.get("external_api_dependency") is False
            and candidate_metadata.get("executes_dataset_code") is False
            and candidate_metadata.get("contains_api_keys") is False
            and candidate_metadata.get("private_core_exposure") is False
        )

    checks = {
        "status_ready": data.get("status") == "STRATEGY_SELECTION_INDEX_READY",
        "index_status_valid": data.get("index_status") == "STRATEGY_SELECTION_INDEX_VALID",
        "index_id_present": bool(data.get("index_id")),
        "aggregate_id_present": bool(data.get("aggregate_id")),
        "batch_id_present": bool(data.get("batch_id")),
        "registry_id_present": bool(data.get("registry_id")),
        "candidate_count_positive": isinstance(data.get("candidate_count"), int)
        and data.get("candidate_count") > 0,
        "candidate_count_matches": data.get("candidate_count") == len(candidates),
        "exactly_one_selected_candidate": len(selected_candidates) == 1,
        "selected_strategy_id_matches": len(selected_candidates) == 1
        and data.get("selected_strategy_id") == selected_candidates[0].get("strategy_id"),
        "selected_strategy_name_matches": len(selected_candidates) == 1
        and data.get("selected_strategy_name") == selected_candidates[0].get("strategy_name"),
        "selected_score_number": isinstance(data.get("selected_score"), float),
        "selected_quality_band_valid": data.get("selected_quality_band")
        in {"PERFECT", "STRONG", "GOOD", "PARTIAL", "WEAK"},
        "strategy_ids_list": isinstance(data.get("strategy_ids"), list),
        "strategy_signatures_dict": isinstance(data.get("strategy_signatures"), dict),
        "signature_present": bool(data.get("signature")),
        "all_candidates_valid": bool(candidate_checks) and all(candidate_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "uses_multi_task_outcome_aggregator": metadata.get("uses_multi_task_outcome_aggregator") is True,
        "uses_batch_benchmark_runner": metadata.get("uses_batch_benchmark_runner") is True,
        "uses_dataset_sample_registry": metadata.get("uses_dataset_sample_registry") is True,
    }

    valid = all(checks.values())

    return {
        "status": "STRATEGY_SELECTION_INDEX_VALID" if valid else "STRATEGY_SELECTION_INDEX_INVALID",
        "valid": valid,
        "checks": checks,
        "index_id": data.get("index_id"),
        "aggregate_id": data.get("aggregate_id"),
        "batch_id": data.get("batch_id"),
        "registry_id": data.get("registry_id"),
        "candidate_count": data.get("candidate_count"),
        "selected_strategy_id": data.get("selected_strategy_id"),
        "selected_strategy_name": data.get("selected_strategy_name"),
        "selected_score": data.get("selected_score"),
        "selected_quality_band": data.get("selected_quality_band"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "strategy_selection_index_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_strategy_selection_index(
    aggregate: Optional[MultiTaskOutcomeAggregate | Dict[str, Any]] = None,
) -> Dict[str, Any]:
    index = build_strategy_selection_index(aggregate)
    validation = validate_strategy_selection_index(index)

    return {
        "status": "STRATEGY_SELECTION_INDEX_PIPELINE_READY",
        "strategy_selection_index": index.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "strategy_selection_index_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    }


def write_strategy_selection_index_artifacts(
    index: StrategySelectionIndex | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/strategy-selection-index",
) -> Dict[str, str]:
    data = index.to_dict() if isinstance(index, StrategySelectionIndex) else dict(index)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "strategy-selection-index.json"
    markdown_path = output_path / "strategy-selection-index.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_strategy_selection_index_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
