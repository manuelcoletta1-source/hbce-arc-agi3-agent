import pytest

from hbce_arc_agi3.outcome_verification import (
    extract_candidate_output,
    extract_expected_output,
    validate_outcome_verification,
    verify_and_validate_outcome,
    verify_outcome,
)


def test_outcome_verification_exact_match():
    payload = {
        "id": "exact-demo",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 2]],
    }

    verification = verify_outcome(payload)
    validation = validate_outcome_verification(verification)

    assert verification.status == "OUTCOME_VERIFICATION_READY"
    assert verification.verification_status == "OUTCOME_MATCH"
    assert verification.expected_available is True
    assert verification.exact_match is True
    assert verification.shape_match is True
    assert verification.cell_accuracy == 1.0
    assert verification.mismatch_count == 0
    assert validation["status"] == "OUTCOME_VERIFICATION_VALID"


def test_outcome_verification_mismatch_accuracy():
    payload = {
        "id": "mismatch-demo",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    verification = verify_outcome(payload)

    assert verification.verification_status == "OUTCOME_MISMATCH"
    assert verification.expected_available is True
    assert verification.exact_match is False
    assert verification.shape_match is True
    assert verification.cell_accuracy == 0.75
    assert verification.matching_cells == 3
    assert verification.total_cells == 4
    assert verification.mismatch_count == 1
    assert verification.mismatches[0] == {"row": 1, "col": 1, "candidate": 2, "expected": 3}


def test_outcome_verification_shape_mismatch():
    payload = {
        "id": "shape-demo",
        "candidate_output": [[1, 0]],
        "expected_output": [[1, 0], [2, 2]],
    }

    verification = verify_outcome(payload)

    assert verification.verification_status == "OUTCOME_MISMATCH"
    assert verification.shape_match is False
    assert verification.cell_accuracy == 0.0
    assert verification.mismatches[0]["type"] == "shape_mismatch"


def test_outcome_verification_expected_unavailable():
    payload = {
        "id": "no-expected-demo",
        "candidate_output": [[1, 0], [2, 2]],
    }

    verification = verify_outcome(payload)

    assert verification.status == "OUTCOME_VERIFICATION_READY"
    assert verification.verification_status == "EXPECTED_OUTPUT_UNAVAILABLE"
    assert verification.expected_available is False
    assert verification.total_cells == 0
    assert verification.metadata["expected_output_available"] is False


def test_outcome_verification_pipeline_wrapper():
    payload = {
        "id": "wrapper-demo",
        "candidate_output": [[1]],
        "expected_output": [[1]],
    }

    result = verify_and_validate_outcome(payload)

    assert result["status"] == "OUTCOME_VERIFICATION_PIPELINE_READY"
    assert result["outcome_verification"]["verification_status"] == "OUTCOME_MATCH"
    assert result["validation"]["status"] == "OUTCOME_VERIFICATION_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_outcome_verification_extracts_strategy_candidate():
    payload = {
        "id": "strategy-preserve-demo",
        "grid": [[1, 0], [2, 2]],
        "planner_strategy": {
            "selected_action": "preserve_non_background_structure",
        },
        "expected_output": [[1, 0], [2, 2]],
    }

    assert extract_candidate_output(payload) == [[1, 0], [2, 2]]
    assert extract_expected_output(payload) == [[1, 0], [2, 2]]

    verification = verify_outcome(payload)

    assert verification.verification_status == "OUTCOME_MATCH"


def test_outcome_verification_is_deterministic():
    payload = {
        "id": "stable-outcome",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    first = verify_outcome(payload)
    second = verify_outcome(payload)

    assert first.to_dict() == second.to_dict()
    assert first.signature == second.signature


def test_outcome_verification_requires_candidate_output():
    with pytest.raises(ValueError, match="candidate output"):
        verify_outcome({"id": "missing-candidate", "expected_output": [[1]]})


def test_outcome_verification_rejects_invalid_shape():
    with pytest.raises(ValueError, match="equal width"):
        verify_outcome(
            {
                "id": "invalid-shape",
                "candidate_output": [[1], [2, 3]],
                "expected_output": [[1]],
            }
        )
