"""Milestone #24 Task 4 validation and artifacts validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_24_validation_artifacts import (
    build_boundary_report,
    build_milestone_24_validation_artifacts,
    build_query_evidence,
    validate_milestone_24_validation_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-24-task-4-validation-and-artifacts-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_24_validation_artifacts.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_24_validation_artifacts.py"
MANIFEST = ROOT / "examples" / "milestone-24" / "validation-and-artifacts-v1" / "task-4-manifest.json"
INDEX = ROOT / "examples" / "milestone-24" / "validation-and-artifacts-v1" / "task-4-index.txt"
VALIDATION_REPORT = ROOT / "examples" / "milestone-24" / "validation-and-artifacts-v1" / "task-4-validation-report.json"
BOUNDARY_REPORT = ROOT / "examples" / "milestone-24" / "validation-and-artifacts-v1" / "task-4-boundary-report.json"
QUERY_EVIDENCE = ROOT / "examples" / "milestone-24" / "validation-and-artifacts-v1" / "task-4-query-evidence.json"
MD_REPORT = ROOT / "examples" / "milestone-24" / "validation-and-artifacts-v1" / "task-4-validation-report.md"
SOURCE_DOC = ROOT / "docs" / "milestone-24-task-3-closed-milestone-snapshot-query-interface-implementation-v1.md"


def test_task_4_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert VALIDATION_REPORT.exists()
    assert BOUNDARY_REPORT.exists()
    assert QUERY_EVIDENCE.exists()
    assert MD_REPORT.exists()
    assert SOURCE_DOC.exists()


def test_task_4_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_READY=true" in source
    assert "MILESTONE_24_TASK_3_QUERY_INTERFACE_IMPLEMENTED=true" in source
    assert "MILESTONE_24_TASK_3_QUERY_INTERFACE_READ_ONLY=true" in source
    assert "MILESTONE_24_TASK_3_SNAPSHOT_COUNT=3" in source
    assert "MILESTONE_24_TASK_3_NEXT_STAGE=MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in source


def test_task_4_validation_contract() -> None:
    validation = build_milestone_24_validation_artifacts()

    assert validation.valid is True
    assert validation.validation_ok is True
    assert validation.task_budget_max == 8
    assert validation.current_task_number == 4
    assert len(validation.validation_cases) == 12
    assert len(validation.generated_artifacts) == 6
    assert validate_milestone_24_validation_artifacts(validation) == ()


def test_task_4_reports_are_valid() -> None:
    evidence = build_query_evidence()
    boundary = build_boundary_report()

    assert evidence["valid"] is True
    assert evidence["snapshotCount"] == 3
    assert evidence["missingSnapshotFound"] is False
    assert evidence["summaryM22Found"] is True
    assert boundary["valid"] is True
    assert boundary["validBoundaryPassCount"] == 3
    assert boundary["brokenBoundaryValid"] is False
    assert "TASK_8_USED" in boundary["brokenBoundaryIssues"]


def test_task_4_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in text
    assert "MILESTONE_24_TASK_4_SOURCE_TASK_ID=MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1" in text
    assert "MILESTONE_24_TASK_4_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_24_TASK_4_CURRENT_TASK_NUMBER=4" in text
    assert "MILESTONE_24_TASK_4_VALIDATION_ARTIFACTS_CREATED=true" in text
    assert "MILESTONE_24_TASK_4_QUERY_INTERFACE_VALIDATED=true" in text
    assert "MILESTONE_24_TASK_4_READY_FOR_INTEGRATION_REGRESSION=true" in text
    assert "MILESTONE_24_TASK_4_QUERY_EVIDENCE_VALID=true" in text
    assert "MILESTONE_24_TASK_4_BOUNDARY_REPORT_VALID=true" in text
    assert "MILESTONE_24_TASK_4_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_24_TASK_4_NEXT_STAGE=MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1" in text


def test_task_4_manifest_and_artifacts() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    report = json.loads(VALIDATION_REPORT.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY_REPORT.read_text(encoding="utf-8"))
    evidence = json.loads(QUERY_EVIDENCE.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert manifest["validationArtifactsCreated"] is True
    assert manifest["readyForIntegrationRegression"] is True
    assert manifest["queryEvidenceValid"] is True
    assert manifest["boundaryReportValid"] is True
    assert report["valid"] is True
    assert report["validationOk"] is True
    assert report["readyForIntegrationRegression"] is True
    assert boundary["valid"] is True
    assert evidence["valid"] is True
    assert report["issues"] == []
