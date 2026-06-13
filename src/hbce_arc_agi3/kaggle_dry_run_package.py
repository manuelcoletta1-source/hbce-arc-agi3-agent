"""Kaggle Dry-Run Package v1 for HBCE ARC-AGI-3 public baseline.

This module creates a deterministic local dry-run package for Kaggle-oriented
submission preparation without sending anything to Kaggle.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
It does not submit to Kaggle.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List

from hbce_arc_agi3.benchmark_report import (
    BenchmarkReport,
    generate_benchmark_report,
    validate_benchmark_report,
    write_benchmark_report_markdown,
)


@dataclass(frozen=True)
class KaggleDryRunPackage:
    status: str
    package_status: str
    package_id: str
    task_id: str
    output_dir: str
    manifest_path: str
    report_path: str
    boundary_path: str
    readme_path: str
    files: List[str]
    file_hashes: Dict[str, str]
    report_signature: str
    package_signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _coerce_report(payload: Any) -> BenchmarkReport:
    if isinstance(payload, BenchmarkReport):
        return payload

    if isinstance(payload, dict) and payload.get("status") == "BENCHMARK_REPORT_READY":
        return BenchmarkReport(**payload)

    nested = payload.get("benchmark_report") if isinstance(payload, dict) else None
    if isinstance(nested, dict) and nested.get("status") == "BENCHMARK_REPORT_READY":
        return BenchmarkReport(**nested)

    return generate_benchmark_report(payload)


def _boundary_payload() -> Dict[str, Any]:
    return {
        "public_safe": True,
        "deterministic": True,
        "external_api_dependency": False,
        "executes_dataset_code": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "kaggle_submission_sent": False,
        "raw_dataset_code_execution": False,
        "source": "kaggle_dry_run_package_v1",
    }


def _readme_text(package_id: str, task_id: str, report_signature: str) -> str:
    return "\n".join(
        [
            "# ARC-AGI-3 Kaggle Dry-Run Package",
            "",
            f"Package ID: {package_id}",
            f"Task ID: {task_id}",
            f"Report signature: {report_signature}",
            "",
            "## Boundary",
            "",
            "- This is a local dry-run package.",
            "- Kaggle submission was not sent.",
            "- No external API call was performed.",
            "- No dataset code was executed.",
            "- No API key or credential is included.",
            "- No private HBCE/JOKER-C2 runtime core is included.",
            "",
        ]
    )


def build_kaggle_dry_run_package(
    payload: Any,
    *,
    output_dir: str | Path = "examples/dry-run/kaggle-dry-run-smoke",
) -> KaggleDryRunPackage:
    """Build a deterministic local Kaggle dry-run package."""

    report = _coerce_report(payload)
    report_validation = validate_benchmark_report(report)

    if report_validation.get("status") != "BENCHMARK_REPORT_VALID":
        raise ValueError("Kaggle dry-run package requires a valid BENCHMARK_REPORT_READY payload")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    task_id = report.task_id
    package_basis = {
        "task_id": task_id,
        "report_signature": report.signature,
        "source": "kaggle_dry_run_package_v1",
    }
    package_signature = _stable_signature(package_basis)
    package_id = f"KAGGLE-DRYRUN-{package_signature[:12]}"

    report_path = output_path / "benchmark-report.md"
    boundary_path = output_path / "public-boundary.json"
    readme_path = output_path / "README.md"
    manifest_path = output_path / "manifest.json"

    write_benchmark_report_markdown(report, report_path)
    _write_json(boundary_path, _boundary_payload())
    readme_path.write_text(_readme_text(package_id, task_id, report.signature), encoding="utf-8")

    file_hashes = {
        "benchmark-report.md": _sha256_file(report_path),
        "public-boundary.json": _sha256_file(boundary_path),
        "README.md": _sha256_file(readme_path),
    }

    manifest_payload = {
        "status": "KAGGLE_DRY_RUN_PACKAGE_READY",
        "package_status": "KAGGLE_DRY_RUN_PACKAGE_VALID",
        "package_id": package_id,
        "task_id": task_id,
        "report_signature": report.signature,
        "package_signature": package_signature,
        "files": sorted(file_hashes.keys()),
        "file_hashes": file_hashes,
        "metadata": {
            "source": "kaggle_dry_run_package_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "uses_benchmark_report": True,
            "uses_score_calibration": True,
            "uses_outcome_verification": True,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    }
    _write_json(manifest_path, manifest_payload)

    file_hashes["manifest.json"] = _sha256_file(manifest_path)
    files = sorted(file_hashes.keys())

    return KaggleDryRunPackage(
        status="KAGGLE_DRY_RUN_PACKAGE_READY",
        package_status="KAGGLE_DRY_RUN_PACKAGE_VALID",
        package_id=package_id,
        task_id=task_id,
        output_dir=str(output_path),
        manifest_path=str(manifest_path),
        report_path=str(report_path),
        boundary_path=str(boundary_path),
        readme_path=str(readme_path),
        files=files,
        file_hashes=file_hashes,
        report_signature=report.signature,
        package_signature=package_signature,
        metadata={
            "source": "kaggle_dry_run_package_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "uses_benchmark_report": True,
            "uses_score_calibration": True,
            "uses_outcome_verification": True,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    )


def validate_kaggle_dry_run_package(package: KaggleDryRunPackage | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Kaggle Dry-Run Package v1 public contract."""

    data = package.to_dict() if isinstance(package, KaggleDryRunPackage) else dict(package)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    files = data.get("files")
    file_hashes = data.get("file_hashes")

    path_checks = {
        "manifest_exists": bool(data.get("manifest_path")) and Path(str(data.get("manifest_path"))).exists(),
        "report_exists": bool(data.get("report_path")) and Path(str(data.get("report_path"))).exists(),
        "boundary_exists": bool(data.get("boundary_path")) and Path(str(data.get("boundary_path"))).exists(),
        "readme_exists": bool(data.get("readme_path")) and Path(str(data.get("readme_path"))).exists(),
    }

    checks = {
        "status_ready": data.get("status") == "KAGGLE_DRY_RUN_PACKAGE_READY",
        "package_status_valid": data.get("package_status") == "KAGGLE_DRY_RUN_PACKAGE_VALID",
        "package_id_present": bool(data.get("package_id")),
        "task_id_present": bool(data.get("task_id")),
        "files_list": isinstance(files, list),
        "file_hashes_dict": isinstance(file_hashes, dict),
        "report_signature_present": bool(data.get("report_signature")),
        "package_signature_present": bool(data.get("package_signature")),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "uses_benchmark_report_true": metadata.get("uses_benchmark_report") is True,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        **path_checks,
    }

    valid = all(checks.values())

    return {
        "status": "KAGGLE_DRY_RUN_PACKAGE_VALID" if valid else "KAGGLE_DRY_RUN_PACKAGE_INVALID",
        "valid": valid,
        "checks": checks,
        "package_id": data.get("package_id"),
        "task_id": data.get("task_id"),
        "package_signature": data.get("package_signature"),
        "metadata": {
            "source": "kaggle_dry_run_package_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def build_and_validate_kaggle_dry_run_package(
    payload: Any,
    *,
    output_dir: str | Path = "examples/dry-run/kaggle-dry-run-smoke",
) -> Dict[str, Any]:
    """Compatibility wrapper for package generation and validation."""

    package = build_kaggle_dry_run_package(payload, output_dir=output_dir)
    validation = validate_kaggle_dry_run_package(package)

    return {
        "status": "KAGGLE_DRY_RUN_PACKAGE_PIPELINE_READY",
        "kaggle_dry_run_package": package.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "kaggle_dry_run_package_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "uses_benchmark_report": True,
            "uses_score_calibration": True,
            "uses_outcome_verification": True,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    }
