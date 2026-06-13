"""Benchmark Report Generator v1 for HBCE ARC-AGI-3 public baseline.

This module turns Score Calibration v1 outputs into deterministic public
benchmark reports.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.score_calibration import (
    ScoreCalibration,
    calibrate_score,
    validate_score_calibration,
)


@dataclass(frozen=True)
class BenchmarkReport:
    status: str
    report_status: str
    task_id: str
    verification_status: str
    calibration_status: str
    raw_score: float
    calibrated_score: float
    grade: str
    quality_band: str
    confidence: float
    summary: Dict[str, Any]
    pipeline: Dict[str, Any]
    artifacts: Dict[str, Any]
    findings: List[str]
    markdown: str
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_score_calibration(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, ScoreCalibration):
        return payload.to_dict()

    if isinstance(payload, dict):
        if payload.get("status") == "SCORE_CALIBRATION_READY":
            return payload

        nested = payload.get("score_calibration")
        if isinstance(nested, dict) and nested.get("status") == "SCORE_CALIBRATION_READY":
            return nested

    return calibrate_score(payload).to_dict()


def _report_status_for_calibration(calibration: Dict[str, Any]) -> str:
    calibration_status = str(calibration.get("calibration_status"))
    grade = str(calibration.get("grade"))

    if calibration_status == "SCORE_CALIBRATED_MATCH":
        return "BENCHMARK_REPORT_MATCH"

    if calibration_status == "SCORE_CALIBRATED_PARTIAL":
        return "BENCHMARK_REPORT_PARTIAL"

    if calibration_status == "SCORE_CALIBRATED_SHAPE_MISMATCH":
        return "BENCHMARK_REPORT_FAILED"

    if grade == "UNVERIFIED":
        return "BENCHMARK_REPORT_UNVERIFIED"

    return "BENCHMARK_REPORT_READY"


def _findings_for_calibration(calibration: Dict[str, Any]) -> List[str]:
    findings: List[str] = []
    grade = str(calibration.get("grade"))
    quality_band = str(calibration.get("quality_band"))
    calibration_status = str(calibration.get("calibration_status"))

    if calibration_status == "SCORE_CALIBRATED_MATCH":
        findings.append("Candidate output exactly matches expected output.")

    elif calibration_status == "SCORE_CALIBRATED_PARTIAL":
        findings.append("Candidate output partially matches expected output.")

    elif calibration_status == "SCORE_CALIBRATED_SHAPE_MISMATCH":
        findings.append("Candidate output shape does not match expected output shape.")

    elif calibration_status == "SCORE_UNVERIFIED_EXPECTED_UNAVAILABLE":
        findings.append("Expected output is unavailable; result is not scored as proof of correctness.")

    findings.append(f"Calibrated grade is {grade}.")
    findings.append(f"Quality band is {quality_band}.")
    findings.append("Report is deterministic and public-safe.")

    return findings


def render_benchmark_report_markdown(report_data: Dict[str, Any]) -> str:
    """Render deterministic Markdown for a benchmark report."""

    lines = [
        "# ARC-AGI-3 Benchmark Report",
        "",
        f"Report status: {report_data['report_status']}",
        f"Task ID: {report_data['task_id']}",
        "",
        "## Score",
        "",
        f"- Verification status: {report_data['verification_status']}",
        f"- Calibration status: {report_data['calibration_status']}",
        f"- Raw score: {report_data['raw_score']}",
        f"- Calibrated score: {report_data['calibrated_score']}",
        f"- Grade: {report_data['grade']}",
        f"- Quality band: {report_data['quality_band']}",
        f"- Confidence: {report_data['confidence']}",
        "",
        "## Artifacts",
        "",
        f"- Score calibration signature: {report_data['artifacts'].get('score_calibration_signature')}",
        f"- Outcome verification signature: {report_data['artifacts'].get('outcome_verification_signature')}",
        "",
        "## Findings",
        "",
    ]

    for finding in report_data.get("findings", []):
        lines.append(f"- {finding}")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- external_api_dependency=false",
            "- executes_dataset_code=false",
            "- contains_api_keys=false",
            "- private_core_exposure=false",
            "- kaggle_submission_sent=false",
            "",
            f"Report signature: {report_data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def generate_benchmark_report(payload: Any) -> BenchmarkReport:
    """Generate a deterministic benchmark report from score calibration or raw payload."""

    calibration = _coerce_score_calibration(payload)
    calibration_validation = validate_score_calibration(calibration)

    if calibration_validation.get("status") != "SCORE_CALIBRATION_VALID":
        raise ValueError("Benchmark report requires a valid SCORE_CALIBRATION_READY payload")

    inputs = calibration.get("inputs") if isinstance(calibration.get("inputs"), dict) else {}

    task_id = str(calibration.get("task_id") or "anonymous-task")
    verification_status = str(calibration.get("verification_status"))
    calibration_status = str(calibration.get("calibration_status"))
    raw_score = round(float(calibration.get("raw_score", 0.0)), 6)
    calibrated_score = round(float(calibration.get("calibrated_score", 0.0)), 6)
    grade = str(calibration.get("grade"))
    quality_band = str(calibration.get("quality_band"))
    confidence = round(float(calibration.get("confidence", 0.0)), 6)
    report_status = _report_status_for_calibration(calibration)

    artifacts = {
        "score_calibration_signature": calibration.get("signature"),
        "outcome_verification_signature": inputs.get("verification_signature"),
    }

    summary = {
        "task_id": task_id,
        "report_status": report_status,
        "grade": grade,
        "quality_band": quality_band,
        "confidence": confidence,
        "calibrated_score": calibrated_score,
        "public_safe": True,
        "deterministic": True,
    }

    pipeline = {
        "uses_outcome_verification": True,
        "uses_score_calibration": True,
        "benchmark_report_generator": "benchmark_report_generator_v1",
        "kaggle_submission_sent": False,
    }

    findings = _findings_for_calibration(calibration)

    signature_basis = {
        "task_id": task_id,
        "report_status": report_status,
        "verification_status": verification_status,
        "calibration_status": calibration_status,
        "raw_score": raw_score,
        "calibrated_score": calibrated_score,
        "grade": grade,
        "quality_band": quality_band,
        "confidence": confidence,
        "artifacts": artifacts,
        "findings": findings,
    }
    signature = _stable_signature(signature_basis)

    report_data = {
        "report_status": report_status,
        "task_id": task_id,
        "verification_status": verification_status,
        "calibration_status": calibration_status,
        "raw_score": raw_score,
        "calibrated_score": calibrated_score,
        "grade": grade,
        "quality_band": quality_band,
        "confidence": confidence,
        "artifacts": artifacts,
        "findings": findings,
        "signature": signature,
    }

    markdown = render_benchmark_report_markdown(report_data)

    return BenchmarkReport(
        status="BENCHMARK_REPORT_READY",
        report_status=report_status,
        task_id=task_id,
        verification_status=verification_status,
        calibration_status=calibration_status,
        raw_score=raw_score,
        calibrated_score=calibrated_score,
        grade=grade,
        quality_band=quality_band,
        confidence=confidence,
        summary=summary,
        pipeline=pipeline,
        artifacts=artifacts,
        findings=findings,
        markdown=markdown,
        signature=signature,
        metadata={
            "source": "benchmark_report_generator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "uses_score_calibration": True,
            "uses_outcome_verification": True,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    )


def validate_benchmark_report(report: BenchmarkReport | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Benchmark Report Generator v1 public contract."""

    data = report.to_dict() if isinstance(report, BenchmarkReport) else dict(report)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    checks = {
        "status_ready": data.get("status") == "BENCHMARK_REPORT_READY",
        "report_status_present": bool(data.get("report_status")),
        "task_id_present": bool(data.get("task_id")),
        "verification_status_present": bool(data.get("verification_status")),
        "calibration_status_present": bool(data.get("calibration_status")),
        "raw_score_number": isinstance(data.get("raw_score"), float),
        "calibrated_score_number": isinstance(data.get("calibrated_score"), float),
        "grade_present": bool(data.get("grade")),
        "quality_band_present": bool(data.get("quality_band")),
        "confidence_number": isinstance(data.get("confidence"), float),
        "summary_dict": isinstance(data.get("summary"), dict),
        "pipeline_dict": isinstance(data.get("pipeline"), dict),
        "artifacts_dict": isinstance(data.get("artifacts"), dict),
        "findings_list": isinstance(data.get("findings"), list),
        "markdown_present": bool(data.get("markdown")),
        "signature_present": bool(data.get("signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "uses_score_calibration_true": metadata.get("uses_score_calibration") is True,
        "uses_outcome_verification_true": metadata.get("uses_outcome_verification") is True,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
    }

    valid = all(checks.values())

    return {
        "status": "BENCHMARK_REPORT_VALID" if valid else "BENCHMARK_REPORT_INVALID",
        "valid": valid,
        "checks": checks,
        "report_status": data.get("report_status"),
        "grade": data.get("grade"),
        "quality_band": data.get("quality_band"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "benchmark_report_generator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_benchmark_report(payload: Any) -> Dict[str, Any]:
    """Compatibility wrapper for benchmark report generation and validation."""

    report = generate_benchmark_report(payload)
    validation = validate_benchmark_report(report)

    return {
        "status": "BENCHMARK_REPORT_PIPELINE_READY",
        "benchmark_report": report.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "benchmark_report_generator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "uses_score_calibration": True,
            "uses_outcome_verification": True,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    }


def write_benchmark_report_markdown(report: BenchmarkReport | Dict[str, Any], path: str | Path) -> Path:
    """Write deterministic benchmark report Markdown to a local path."""

    data = report.to_dict() if isinstance(report, BenchmarkReport) else dict(report)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(str(data["markdown"]), encoding="utf-8")
    return output_path
