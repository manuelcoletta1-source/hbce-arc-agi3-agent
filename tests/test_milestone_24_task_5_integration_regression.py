"""Milestone #24 Task 5 integration regression validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_24_integration_regression import (
    build_boundary_regression,
    build_milestone_24_integration_regression,
    build_regression_evidence,
    validate_milestone_24_integration_regression,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-24-task-5-integration-regression-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_24_integration_regression.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_24_integration_regression.py"
MANIFEST = ROOT / "examples" / "milestone-24" / "integration-regression-v1" / "task-5-manifest.json"
INDEX = ROOT / "examples" / "milestone-24" / "integration-regression-v1" / "task-5-index.txt"
REGRESSION_REPORT = ROOT / "examples" / "milestone-24" / "integration-regression-v1" / "task-5-integration-regression.json"
REGRESSION_EVIDENCE = ROOT / "examples" / "milestone-24" / "integration-regression-v1" / "task-5-regression-evidence.json"
BOUNDARY_REGRESSION = ROOT / "examples" / "milestone-24" / "integration-regression-v1" / "task-5-boundary-regression.json"
MD_REPORT = ROOT / "examples" / "milestone-24" / "integration-regression-v1" / "task-5-integration-regression.md"
SOURCE_DOC = ROOT / "docs" / "milestone-24-task-4-validation-and-artifacts-v1.md"


def test_task_5_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert REGRESSION_REPORT.exists()
    assert REGRESSION_EVIDENCE.exists()
    assert BOUNDARY_REGRESSION.exists()
    assert MD_REPORT.exists()
    assert SOURCE_DOC.exists()


def test_task_5_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in source
    assert "MILESTONE_24_TASK_4_READY_FOR_INTEGRATION_REGRESSION=true" in source
    assert "MILESTONE_24_TASK_4_QUERY_EVIDENCE_VALID=true" in source
    assert "MILESTONE_24_TASK_4_BOUNDARY_REPORT_VALID=true" in source
    assert "MILESTONE_24_TASK_4_NEXT_STAGE=MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1" in source


def test_task_5_integration_contract() -> None:
    regression = build_milestone_24_integration_regression()

    assert regression.valid is True
    assert regression.integration_ok is True
    assert regression.task_budget_max == 8
    assert regression.current_task_number == 5
    assert len(regression.regression_cases) == 12
    assert len(regression.generated_artifacts) == 6
    assert validate_milestone_24_integration_regression(regression) == ()


def test_task_5_regression_reports_are_valid() -> None:
    evidence = build_regression_evidence()
    boundary = build_boundary_regression()

    assert evidence["valid"] is True
    assert evidence["snapshotCount"] == 3
    assert evidence["missingSnapshotFound"] is False
    assert evidence["summaryM22Valid"] is True
    assert boundary["valid"] is True
    assert boundary["validBoundaryPassCount"] == 3
    assert boundary["brokenBoundaryValid"] is False
    assert "TASK_8_USED" in boundary["brokenBoundaryIssues"]


def test_task_5_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_READY=true" in text
    assert "MILESTONE_24_TASK_5_MODE=TASK_CHAIN_AND_QUERY_INTERFACE_REGRESSION_FAST_SOURCE_VALIDATION_SNAPSHOT" in text
    assert "MILESTONE_24_TASK_5_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_24_TASK_5_CURRENT_TASK_NUMBER=5" in text
    assert "MILESTONE_24_TASK_5_TASK_CHAIN_VALIDATED=true" in text
    assert "MILESTONE_24_TASK_5_SOURCE_ARTIFACTS_VALIDATED=true" in text
    assert "MILESTONE_24_TASK_5_QUERY_INTERFACE_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_24_TASK_5_BOUNDARY_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_24_TASK_5_NO_MUTATION_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_24_TASK_5_READY_FOR_MILESTONE_CLOSURE=true" in text
    assert "MILESTONE_24_TASK_5_TASK1_VALID=true" in text
    assert "MILESTONE_24_TASK_5_TASK2_VALID=true" in text
    assert "MILESTONE_24_TASK_5_TASK3_VALID=true" in text
    assert "MILESTONE_24_TASK_5_TASK4_VALID=true" in text
    assert "MILESTONE_24_TASK_5_MISSING_SNAPSHOT_FOUND=false" in text
    assert "MILESTONE_24_TASK_5_FAST_SOURCE_VALIDATION_SNAPSHOT=true" in text
    assert "MILESTONE_24_TASK_5_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_24_TASK_5_NEXT_STAGE=MILESTONE_24_TASK_6_MILESTONE_CLOSURE_V1" in text


def test_task_5_manifest_and_artifacts() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    report = json.loads(REGRESSION_REPORT.read_text(encoding="utf-8"))
    evidence = json.loads(REGRESSION_EVIDENCE.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY_REGRESSION.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1"
    assert manifest["mode"] == "TASK_CHAIN_AND_QUERY_INTERFACE_REGRESSION_FAST_SOURCE_VALIDATION_SNAPSHOT"
    assert manifest["integrationRegressionExecuted"] is True
    assert manifest["taskChainValidated"] is True
    assert manifest["readyForMilestoneClosure"] is True
    assert manifest["regressionEvidenceValid"] is True
    assert manifest["boundaryRegressionValid"] is True
    assert manifest["fastSourceValidationSnapshot"] is True
    assert report["valid"] is True
    assert report["integrationOk"] is True
    assert report["readyForMilestoneClosure"] is True
    assert report["fastSourceValidationSnapshot"] is True
    assert evidence["valid"] is True
    assert boundary["valid"] is True
    assert report["issues"] == []
