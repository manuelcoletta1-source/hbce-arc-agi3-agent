from pathlib import Path

import pytest

from hbce_arc_agi3.benchmark_report import (
    generate_and_validate_benchmark_report,
    generate_benchmark_report,
    validate_benchmark_report,
    write_benchmark_report_markdown,
)
from hbce_arc_agi3.score_calibration import calibrate_score


def test_benchmark_report_generates_partial_report():
    payload = {
        "id": "report-partial",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    report = generate_benchmark_report(payload)
    validation = validate_benchmark_report(report)

    assert report.status == "BENCHMARK_REPORT_READY"
    assert report.report_status == "BENCHMARK_REPORT_PARTIAL"
    assert report.grade == "B"
    assert report.quality_band == "STRONG"
    assert report.confidence == 0.75
    assert report.metadata["uses_score_calibration"] is True
    assert validation["status"] == "BENCHMARK_REPORT_VALID"


def test_benchmark_report_exact_match():
    payload = {
        "id": "report-match",
        "candidate_output": [[1]],
        "expected_output": [[1]],
    }

    report = generate_benchmark_report(payload)

    assert report.report_status == "BENCHMARK_REPORT_MATCH"
    assert report.grade == "A_PLUS"
    assert report.quality_band == "PERFECT"
    assert "exactly matches" in report.findings[0]


def test_benchmark_report_unverified_expected_unavailable():
    payload = {
        "id": "report-unverified",
        "candidate_output": [[1, 0]],
    }

    report = generate_benchmark_report(payload)

    assert report.report_status == "BENCHMARK_REPORT_UNVERIFIED"
    assert report.grade == "UNVERIFIED"
    assert report.quality_band == "UNVERIFIED"
    assert report.metadata["kaggle_submission_sent"] is False


def test_benchmark_report_accepts_score_calibration_object():
    calibration = calibrate_score(
        {
            "id": "report-calibration-object",
            "candidate_output": [[1, 0], [2, 2]],
            "expected_output": [[1, 0], [2, 3]],
        }
    )

    report = generate_benchmark_report(calibration)

    assert report.status == "BENCHMARK_REPORT_READY"
    assert report.artifacts["score_calibration_signature"] == calibration.signature
    assert report.metadata["private_core_exposure"] is False


def test_benchmark_report_pipeline_wrapper():
    result = generate_and_validate_benchmark_report(
        {
            "id": "report-wrapper",
            "candidate_output": [[1]],
            "expected_output": [[1]],
        }
    )

    assert result["status"] == "BENCHMARK_REPORT_PIPELINE_READY"
    assert result["benchmark_report"]["status"] == "BENCHMARK_REPORT_READY"
    assert result["validation"]["status"] == "BENCHMARK_REPORT_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_benchmark_report_markdown_contains_public_boundary():
    report = generate_benchmark_report(
        {
            "id": "report-markdown",
            "candidate_output": [[1]],
            "expected_output": [[1]],
        }
    )

    assert "# ARC-AGI-3 Benchmark Report" in report.markdown
    assert "public_safe=true" in report.markdown
    assert "external_api_dependency=false" in report.markdown
    assert "kaggle_submission_sent=false" in report.markdown
    assert report.signature in report.markdown


def test_benchmark_report_write_markdown(tmp_path: Path):
    report = generate_benchmark_report(
        {
            "id": "report-write",
            "candidate_output": [[1]],
            "expected_output": [[1]],
        }
    )

    output_path = write_benchmark_report_markdown(report, tmp_path / "report.md")

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Benchmark Report")


def test_benchmark_report_is_deterministic():
    payload = {
        "id": "report-stable",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    first = generate_benchmark_report(payload)
    second = generate_benchmark_report(payload)

    assert first.to_dict() == second.to_dict()
    assert first.signature == second.signature


def test_benchmark_report_validation_rejects_broken_contract():
    validation = validate_benchmark_report(
        {
            "status": "BROKEN",
            "metadata": {},
        }
    )

    assert validation["status"] == "BENCHMARK_REPORT_INVALID"
    assert validation["valid"] is False


def test_benchmark_report_requires_valid_score_input():
    with pytest.raises(ValueError, match="candidate output"):
        generate_benchmark_report({"id": "missing-candidate", "expected_output": [[1]]})
