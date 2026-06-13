"""Score Calibration v1 for HBCE ARC-AGI-3 public baseline.

This module converts Outcome Verification v1 results into deterministic
calibrated score, grade, quality band, and confidence.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Dict

from hbce_arc_agi3.outcome_verification import (
    OutcomeVerification,
    validate_outcome_verification,
    verify_outcome,
)


@dataclass(frozen=True)
class ScoreCalibration:
    status: str
    calibration_status: str
    task_id: str
    verification_status: str
    expected_available: bool
    exact_match: bool
    shape_match: bool
    raw_score: float
    calibrated_score: float
    grade: str
    quality_band: str
    confidence: float
    rationale: str
    inputs: Dict[str, Any]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_verification(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, OutcomeVerification):
        return payload.to_dict()

    if isinstance(payload, dict):
        if payload.get("status") == "OUTCOME_VERIFICATION_READY":
            return payload

        nested = payload.get("outcome_verification")
        if isinstance(nested, dict) and nested.get("status") == "OUTCOME_VERIFICATION_READY":
            return nested

    return verify_outcome(payload).to_dict()


def _grade_for_score(calibrated_score: float, *, expected_available: bool, exact_match: bool) -> str:
    if not expected_available:
        return "UNVERIFIED"

    if exact_match and calibrated_score == 1.0:
        return "A_PLUS"

    if calibrated_score >= 0.9:
        return "A"

    if calibrated_score >= 0.75:
        return "B"

    if calibrated_score >= 0.5:
        return "C"

    if calibrated_score > 0.0:
        return "D"

    return "F"


def _quality_band_for_grade(grade: str) -> str:
    return {
        "A_PLUS": "PERFECT",
        "A": "EXCELLENT",
        "B": "STRONG",
        "C": "PARTIAL",
        "D": "WEAK",
        "F": "FAILED",
        "UNVERIFIED": "UNVERIFIED",
    }.get(grade, "UNKNOWN")


def _calibrated_score_from_verification(verification: Dict[str, Any]) -> float:
    expected_available = bool(verification.get("expected_available"))
    exact_match = bool(verification.get("exact_match"))
    shape_match = bool(verification.get("shape_match"))
    raw_score = float(verification.get("cell_accuracy", 0.0))

    if not expected_available:
        return 0.0

    if exact_match:
        return 1.0

    if not shape_match:
        return 0.0

    return round(raw_score, 6)


def _confidence_from_verification(verification: Dict[str, Any], calibrated_score: float) -> float:
    expected_available = bool(verification.get("expected_available"))
    shape_match = bool(verification.get("shape_match"))
    exact_match = bool(verification.get("exact_match"))

    if not expected_available:
        return 0.0

    if exact_match:
        return 1.0

    if not shape_match:
        return 0.25

    return round(calibrated_score, 6)


def calibrate_score(payload: Any) -> ScoreCalibration:
    """Calibrate an outcome verification payload into score/grade/confidence."""

    verification = _coerce_verification(payload)
    validation = validate_outcome_verification(verification)

    if validation.get("status") != "OUTCOME_VERIFICATION_VALID":
        raise ValueError("Score calibration requires a valid OUTCOME_VERIFICATION_READY payload")

    expected_available = bool(verification.get("expected_available"))
    exact_match = bool(verification.get("exact_match"))
    shape_match = bool(verification.get("shape_match"))
    raw_score = round(float(verification.get("cell_accuracy", 0.0)), 6)
    calibrated_score = _calibrated_score_from_verification(verification)
    confidence = _confidence_from_verification(verification, calibrated_score)
    grade = _grade_for_score(
        calibrated_score,
        expected_available=expected_available,
        exact_match=exact_match,
    )
    quality_band = _quality_band_for_grade(grade)

    if not expected_available:
        calibration_status = "SCORE_UNVERIFIED_EXPECTED_UNAVAILABLE"
        rationale = "Expected output is unavailable; score is not treated as proof of correctness."
    elif exact_match:
        calibration_status = "SCORE_CALIBRATED_MATCH"
        rationale = "Candidate output exactly matches expected output."
    elif not shape_match:
        calibration_status = "SCORE_CALIBRATED_SHAPE_MISMATCH"
        rationale = "Candidate and expected outputs have incompatible shapes."
    else:
        calibration_status = "SCORE_CALIBRATED_PARTIAL"
        rationale = "Candidate output partially matches expected output by cell accuracy."

    signature_basis = {
        "task_id": verification.get("task_id"),
        "verification_status": verification.get("verification_status"),
        "expected_available": expected_available,
        "exact_match": exact_match,
        "shape_match": shape_match,
        "raw_score": raw_score,
        "calibrated_score": calibrated_score,
        "grade": grade,
        "quality_band": quality_band,
        "confidence": confidence,
        "verification_signature": verification.get("signature"),
    }
    signature = _stable_signature(signature_basis)

    return ScoreCalibration(
        status="SCORE_CALIBRATION_READY",
        calibration_status=calibration_status,
        task_id=str(verification.get("task_id") or "anonymous-task"),
        verification_status=str(verification.get("verification_status")),
        expected_available=expected_available,
        exact_match=exact_match,
        shape_match=shape_match,
        raw_score=raw_score,
        calibrated_score=calibrated_score,
        grade=grade,
        quality_band=quality_band,
        confidence=confidence,
        rationale=rationale,
        inputs={
            "verification_signature": verification.get("signature"),
            "cell_accuracy": raw_score,
            "matching_cells": verification.get("matching_cells"),
            "total_cells": verification.get("total_cells"),
            "mismatch_count": verification.get("mismatch_count"),
        },
        signature=signature,
        metadata={
            "source": "score_calibration_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "uses_outcome_verification": True,
        },
    )


def validate_score_calibration(calibration: ScoreCalibration | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Score Calibration v1 public contract."""

    data = calibration.to_dict() if isinstance(calibration, ScoreCalibration) else dict(calibration)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    checks = {
        "status_ready": data.get("status") == "SCORE_CALIBRATION_READY",
        "calibration_status_present": bool(data.get("calibration_status")),
        "task_id_present": bool(data.get("task_id")),
        "verification_status_present": bool(data.get("verification_status")),
        "expected_available_boolean": isinstance(data.get("expected_available"), bool),
        "exact_match_boolean": isinstance(data.get("exact_match"), bool),
        "shape_match_boolean": isinstance(data.get("shape_match"), bool),
        "raw_score_number": isinstance(data.get("raw_score"), float),
        "calibrated_score_number": isinstance(data.get("calibrated_score"), float),
        "grade_present": bool(data.get("grade")),
        "quality_band_present": bool(data.get("quality_band")),
        "confidence_number": isinstance(data.get("confidence"), float),
        "signature_present": bool(data.get("signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "uses_outcome_verification_true": metadata.get("uses_outcome_verification") is True,
    }

    valid = all(checks.values())

    return {
        "status": "SCORE_CALIBRATION_VALID" if valid else "SCORE_CALIBRATION_INVALID",
        "valid": valid,
        "checks": checks,
        "calibration_status": data.get("calibration_status"),
        "grade": data.get("grade"),
        "quality_band": data.get("quality_band"),
        "confidence": data.get("confidence"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "score_calibration_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def calibrate_and_validate_score(payload: Any) -> Dict[str, Any]:
    """Compatibility wrapper for score calibration and validation."""

    calibration = calibrate_score(payload)
    validation = validate_score_calibration(calibration)

    return {
        "status": "SCORE_CALIBRATION_PIPELINE_READY",
        "score_calibration": calibration.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "score_calibration_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "uses_outcome_verification": True,
        },
    }
