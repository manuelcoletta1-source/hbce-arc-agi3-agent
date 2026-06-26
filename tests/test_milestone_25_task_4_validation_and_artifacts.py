"""Milestone #25 Task 4 validation and artifacts validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_25_validation_artifacts import (
    build_milestone_25_validation_artifacts,
    validate_milestone_25_validation_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-25-task-4-validation-and-artifacts-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_25_validation_artifacts.py"
MANIFEST = ROOT / "examples" / "milestone-25" / "validation-and-artifacts-v1" / "task-4-artifact-manifest.json"
REPORT = ROOT / "examples" / "milestone-25" / "validation-and-artifacts-v1" / "task-4-validation-report.json"
BOUNDARY = ROOT / "examples" / "milestone-25" / "validation-and-artifacts-v1" / "task-4-boundary-validation.json"
INTEGRITY = ROOT / "examples" / "milestone-25" / "validation-and-artifacts-v1" / "task-4-integrity-validation.json"
SOURCE_DOC = ROOT / "docs" / "milestone-25-task-3-evidence-bundle-implementation-v1.md"


def test_task_4_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MANIFEST.exists()
    assert REPORT.exists()
    assert BOUNDARY.exists()
    assert INTEGRITY.exists()
    assert SOURCE_DOC.exists()


def test_task_4_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_READY=true" in source
    assert "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_VALID=true" in source
    assert "MILESTONE_25_TASK_3_MANIFEST_GENERATED=true" in source
    assert "MILESTONE_25_TASK_3_BOUNDARY_REPORT_VALID=true" in source
    assert "MILESTONE_25_TASK_3_INTEGRITY_SUMMARY_VALID=true" in source
    assert "MILESTONE_25_TASK_3_NEXT_STAGE=MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in source


def test_task_4_validation_contract() -> None:
    validation = build_milestone_25_validation_artifacts()
    assert validation.valid is True
    assert validation.validation_ok is True
    assert validation.current_task_number == 4
    assert validation.task_budget_max == 8
    assert validation.remaining_budget_after_current_task == 4
    assert len(validation.validation_cases) == 12
    assert len(validation.generated_artifacts) == 6
    assert validate_milestone_25_validation_artifacts(validation) == ()


def test_task_4_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in text
    assert "MILESTONE_25_TASK_4_EVIDENCE_BUNDLE_VALIDATED=true" in text
    assert "MILESTONE_25_TASK_4_EVIDENCE_MANIFEST_VALIDATED=true" in text
    assert "MILESTONE_25_TASK_4_BOUNDARY_REPORT_VALIDATED=true" in text
    assert "MILESTONE_25_TASK_4_INTEGRITY_SUMMARY_VALIDATED=true" in text
    assert "MILESTONE_25_TASK_4_READY_FOR_INTEGRATION_REGRESSION=true" in text
    assert "MILESTONE_25_TASK_4_QUERY_RESULT_ITEM_COUNT=3" in text
    assert "MILESTONE_25_TASK_4_REGISTERED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_25_TASK_4_FAST_SOURCE_EVIDENCE_BUNDLE_SNAPSHOT=true" in text
    assert "MILESTONE_25_TASK_4_NEXT_STAGE=MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1" in text


def test_task_4_manifest_and_artifacts() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    integrity = json.loads(INTEGRITY.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert manifest["validationArtifactsCreated"] is True
    assert manifest["evidenceBundleValidated"] is True
    assert manifest["readyForIntegrationRegression"] is True
    assert manifest["nextStage"] == "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"

    assert report["valid"] is True
    assert report["validationOk"] is True
    assert report["issues"] == []
    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert integrity["valid"] is True
    assert integrity["readyForIntegrationRegression"] is True
    assert integrity["issues"] == []
