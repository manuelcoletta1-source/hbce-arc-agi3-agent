"""Milestone #26 Task 4 validation and artifacts validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_26_validation_artifacts import (
    build_milestone_26_validation_artifacts,
    validate_milestone_26_validation_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-26-task-4-validation-and-artifacts-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_26_validation_artifacts.py"
REPORT = ROOT / "examples" / "milestone-26" / "validation-and-artifacts-v1" / "task-4-validation-report.json"
MANIFEST = ROOT / "examples" / "milestone-26" / "validation-and-artifacts-v1" / "task-4-artifact-manifest.json"
BOUNDARY = ROOT / "examples" / "milestone-26" / "validation-and-artifacts-v1" / "task-4-boundary-validation.json"
INTEGRITY = ROOT / "examples" / "milestone-26" / "validation-and-artifacts-v1" / "task-4-integrity-validation.json"
SOURCE_DOC = ROOT / "docs" / "milestone-26-task-3-archive-index-implementation-v1.md"


def test_task_4_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert REPORT.exists()
    assert MANIFEST.exists()
    assert BOUNDARY.exists()
    assert INTEGRITY.exists()
    assert SOURCE_DOC.exists()


def test_task_4_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_READY=true" in source
    assert "MILESTONE_26_TASK_3_ARCHIVE_INDEX_VALID=true" in source
    assert "MILESTONE_26_TASK_3_READY_FOR_VALIDATION_ARTIFACTS=true" in source
    assert "MILESTONE_26_TASK_3_ARCHIVE_ITEM_COUNT=3" in source
    assert "MILESTONE_26_TASK_3_NEXT_STAGE=MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in source


def test_task_4_validation_contract() -> None:
    validation = build_milestone_26_validation_artifacts()
    assert validation.valid is True
    assert validation.validation_ok is True
    assert validation.current_task_number == 4
    assert validation.task_budget_max == 8
    assert validation.remaining_budget_after_current_task == 4
    assert len(validation.validation_cases) == 12
    assert len(validation.generated_artifacts) == 6
    assert validate_milestone_26_validation_artifacts(validation) == ()


def test_task_4_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in text
    assert "MILESTONE_26_TASK_4_ARCHIVE_INDEX_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_4_ARCHIVE_MANIFEST_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_4_BOUNDARY_REPORT_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_4_INTEGRITY_SUMMARY_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_4_READY_FOR_INTEGRATION_REGRESSION=true" in text
    assert "MILESTONE_26_TASK_4_ARCHIVE_ITEM_COUNT=3" in text
    assert "MILESTONE_26_TASK_4_ARCHIVED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_26_TASK_4_MISSING_ARCHIVE_ITEM_FOUND=false" in text
    assert "MILESTONE_26_TASK_4_INVALID_ARCHIVE_ITEM_FOUND=false" in text
    assert "MILESTONE_26_TASK_4_TASK_8_USED_FOUND=false" in text
    assert "MILESTONE_26_TASK_4_VALIDATION_CASE_COUNT=12" in text
    assert "MILESTONE_26_TASK_4_GENERATED_ARTIFACT_COUNT=6" in text
    assert "MILESTONE_26_TASK_4_CURRENT_TASK_NUMBER=4" in text
    assert "MILESTONE_26_TASK_4_FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT=true" in text
    assert "MILESTONE_26_TASK_4_NEXT_STAGE=MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_V1" in text


def test_task_4_artifacts() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    integrity = json.loads(INTEGRITY.read_text(encoding="utf-8"))

    assert report["valid"] is True
    assert report["validationOk"] is True
    assert report["issues"] == []
    assert report["readyForIntegrationRegression"] is True
    assert report["archiveItemCount"] == 3

    assert manifest["valid"] is True
    assert manifest["validationArtifactsCreated"] is True
    assert manifest["archiveIndexValidated"] is True
    assert manifest["readyForIntegrationRegression"] is True
    assert manifest["generatedArtifactCount"] == 6

    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert boundary["runtimeSolverModified"] is False
    assert boundary["kaggleSubmissionSent"] is False
    assert boundary["legalCertification"] is False

    assert integrity["valid"] is True
    assert integrity["issues"] == []
    assert integrity["readyForIntegrationRegression"] is True
    assert integrity["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
