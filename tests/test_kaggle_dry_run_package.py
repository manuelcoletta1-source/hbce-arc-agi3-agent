import json
from pathlib import Path

import pytest

from hbce_arc_agi3.benchmark_report import generate_benchmark_report
from hbce_arc_agi3.kaggle_dry_run_package import (
    build_and_validate_kaggle_dry_run_package,
    build_kaggle_dry_run_package,
    validate_kaggle_dry_run_package,
)


def _payload():
    return {
        "id": "dry-run-test",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }


def test_kaggle_dry_run_package_builds_files(tmp_path: Path):
    package = build_kaggle_dry_run_package(_payload(), output_dir=tmp_path / "dry-run")
    validation = validate_kaggle_dry_run_package(package)

    assert package.status == "KAGGLE_DRY_RUN_PACKAGE_READY"
    assert package.package_status == "KAGGLE_DRY_RUN_PACKAGE_VALID"
    assert validation["status"] == "KAGGLE_DRY_RUN_PACKAGE_VALID"
    assert Path(package.manifest_path).exists()
    assert Path(package.report_path).exists()
    assert Path(package.boundary_path).exists()
    assert Path(package.readme_path).exists()


def test_kaggle_dry_run_package_manifest_contains_boundary(tmp_path: Path):
    package = build_kaggle_dry_run_package(_payload(), output_dir=tmp_path / "dry-run")
    manifest = json.loads(Path(package.manifest_path).read_text(encoding="utf-8"))

    assert manifest["status"] == "KAGGLE_DRY_RUN_PACKAGE_READY"
    assert manifest["metadata"]["public_safe"] is True
    assert manifest["metadata"]["external_api_dependency"] is False
    assert manifest["metadata"]["executes_dataset_code"] is False
    assert manifest["metadata"]["contains_api_keys"] is False
    assert manifest["metadata"]["kaggle_submission_sent"] is False
    assert manifest["metadata"]["private_core_exposure"] is False


def test_kaggle_dry_run_package_boundary_json(tmp_path: Path):
    package = build_kaggle_dry_run_package(_payload(), output_dir=tmp_path / "dry-run")
    boundary = json.loads(Path(package.boundary_path).read_text(encoding="utf-8"))

    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["executes_dataset_code"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False


def test_kaggle_dry_run_package_report_is_written(tmp_path: Path):
    package = build_kaggle_dry_run_package(_payload(), output_dir=tmp_path / "dry-run")
    report_text = Path(package.report_path).read_text(encoding="utf-8")

    assert "# ARC-AGI-3 Benchmark Report" in report_text
    assert "Report status: BENCHMARK_REPORT_PARTIAL" in report_text
    assert "kaggle_submission_sent=false" in report_text


def test_kaggle_dry_run_package_accepts_benchmark_report_object(tmp_path: Path):
    report = generate_benchmark_report(_payload())
    package = build_kaggle_dry_run_package(report, output_dir=tmp_path / "dry-run")

    assert package.report_signature == report.signature
    assert package.metadata["uses_benchmark_report"] is True
    assert package.metadata["private_core_exposure"] is False


def test_kaggle_dry_run_package_pipeline_wrapper(tmp_path: Path):
    result = build_and_validate_kaggle_dry_run_package(_payload(), output_dir=tmp_path / "dry-run")

    assert result["status"] == "KAGGLE_DRY_RUN_PACKAGE_PIPELINE_READY"
    assert result["kaggle_dry_run_package"]["status"] == "KAGGLE_DRY_RUN_PACKAGE_READY"
    assert result["validation"]["status"] == "KAGGLE_DRY_RUN_PACKAGE_VALID"
    assert result["metadata"]["kaggle_submission_sent"] is False


def test_kaggle_dry_run_package_is_deterministic(tmp_path: Path):
    first = build_kaggle_dry_run_package(_payload(), output_dir=tmp_path / "dry-run-a")
    second = build_kaggle_dry_run_package(_payload(), output_dir=tmp_path / "dry-run-b")

    assert first.package_id == second.package_id
    assert first.package_signature == second.package_signature
    assert first.report_signature == second.report_signature
    assert first.file_hashes["benchmark-report.md"] == second.file_hashes["benchmark-report.md"]
    assert first.file_hashes["public-boundary.json"] == second.file_hashes["public-boundary.json"]


def test_kaggle_dry_run_package_file_hashes_present(tmp_path: Path):
    package = build_kaggle_dry_run_package(_payload(), output_dir=tmp_path / "dry-run")

    assert "benchmark-report.md" in package.file_hashes
    assert "public-boundary.json" in package.file_hashes
    assert "README.md" in package.file_hashes
    assert "manifest.json" in package.file_hashes
    assert all(len(value) == 64 for value in package.file_hashes.values())


def test_kaggle_dry_run_package_validation_rejects_broken_contract():
    validation = validate_kaggle_dry_run_package(
        {
            "status": "BROKEN",
            "metadata": {},
        }
    )

    assert validation["status"] == "KAGGLE_DRY_RUN_PACKAGE_INVALID"
    assert validation["valid"] is False


def test_kaggle_dry_run_package_requires_valid_report_input():
    with pytest.raises(ValueError, match="candidate output"):
        build_kaggle_dry_run_package({"id": "missing-candidate", "expected_output": [[1]]})
