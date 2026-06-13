import pytest

from hbce_arc_agi3.outcome_verification import verify_outcome
from hbce_arc_agi3.score_calibration import (
    calibrate_and_validate_score,
    calibrate_score,
    validate_score_calibration,
)


def test_score_calibration_exact_match():
    payload = {
        "id": "score-exact",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 2]],
    }

    calibration = calibrate_score(payload)
    validation = validate_score_calibration(calibration)

    assert calibration.status == "SCORE_CALIBRATION_READY"
    assert calibration.calibration_status == "SCORE_CALIBRATED_MATCH"
    assert calibration.raw_score == 1.0
    assert calibration.calibrated_score == 1.0
    assert calibration.grade == "A_PLUS"
    assert calibration.quality_band == "PERFECT"
    assert calibration.confidence == 1.0
    assert validation["status"] == "SCORE_CALIBRATION_VALID"


def test_score_calibration_partial_mismatch():
    payload = {
        "id": "score-partial",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    calibration = calibrate_score(payload)

    assert calibration.calibration_status == "SCORE_CALIBRATED_PARTIAL"
    assert calibration.raw_score == 0.75
    assert calibration.calibrated_score == 0.75
    assert calibration.grade == "B"
    assert calibration.quality_band == "STRONG"
    assert calibration.confidence == 0.75


def test_score_calibration_expected_unavailable():
    payload = {
        "id": "score-unverified",
        "candidate_output": [[1, 0], [2, 2]],
    }

    calibration = calibrate_score(payload)

    assert calibration.calibration_status == "SCORE_UNVERIFIED_EXPECTED_UNAVAILABLE"
    assert calibration.expected_available is False
    assert calibration.raw_score == 0.0
    assert calibration.calibrated_score == 0.0
    assert calibration.grade == "UNVERIFIED"
    assert calibration.quality_band == "UNVERIFIED"
    assert calibration.confidence == 0.0


def test_score_calibration_shape_mismatch():
    payload = {
        "id": "score-shape",
        "candidate_output": [[1, 0]],
        "expected_output": [[1, 0], [2, 2]],
    }

    calibration = calibrate_score(payload)

    assert calibration.calibration_status == "SCORE_CALIBRATED_SHAPE_MISMATCH"
    assert calibration.shape_match is False
    assert calibration.calibrated_score == 0.0
    assert calibration.grade == "F"
    assert calibration.quality_band == "FAILED"
    assert calibration.confidence == 0.25


def test_score_calibration_accepts_verification_object():
    verification = verify_outcome(
        {
            "id": "verification-object",
            "candidate_output": [[1, 0], [2, 2]],
            "expected_output": [[1, 0], [2, 3]],
        }
    )

    calibration = calibrate_score(verification)

    assert calibration.status == "SCORE_CALIBRATION_READY"
    assert calibration.inputs["verification_signature"] == verification.signature
    assert calibration.metadata["uses_outcome_verification"] is True


def test_score_calibration_pipeline_wrapper():
    result = calibrate_and_validate_score(
        {
            "id": "score-wrapper",
            "candidate_output": [[1]],
            "expected_output": [[1]],
        }
    )

    assert result["status"] == "SCORE_CALIBRATION_PIPELINE_READY"
    assert result["score_calibration"]["grade"] == "A_PLUS"
    assert result["validation"]["status"] == "SCORE_CALIBRATION_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_score_calibration_is_deterministic():
    payload = {
        "id": "score-stable",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    first = calibrate_score(payload)
    second = calibrate_score(payload)

    assert first.to_dict() == second.to_dict()
    assert first.signature == second.signature


def test_score_calibration_rejects_invalid_contract():
    validation = validate_score_calibration(
        {
            "status": "BROKEN",
            "metadata": {},
        }
    )

    assert validation["status"] == "SCORE_CALIBRATION_INVALID"
    assert validation["valid"] is False


def test_score_calibration_requires_valid_outcome_payload():
    with pytest.raises(ValueError, match="candidate output"):
        calibrate_score({"id": "missing-candidate", "expected_output": [[1]]})
