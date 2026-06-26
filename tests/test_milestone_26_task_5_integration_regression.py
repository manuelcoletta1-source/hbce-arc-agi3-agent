"""Milestone #26 Task 5 integration regression validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_26_integration_regression import (
    build_milestone_26_integration_regression,
    validate_milestone_26_integration_regression,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-26-task-5-integration-regression-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_26_integration_regression.py"
REPORT = ROOT / "examples" / "milestone-26" / "integration-regression-v1" / "task-5-integration-regression.json"
MANIFEST = ROOT / "examples" / "milestone-26" / "integration-regression-v1" / "task-5-manifest.json"
BOUNDARY = ROOT / "examples" / "milestone-26" / "integration-regression-v1" / "task-5-regression-boundary.json"
SOURCE_DOC = ROOT / "docs" / "milestone-26-task-4-validation-and-artifacts-v1.md"


def test_task_5_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert REPORT.exists()
    assert MANIFEST.exists()
    assert BOUNDARY.exists()
    assert SOURCE_DOC.exists()


def test_task_5_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in source
    assert "MILESTONE_26_TASK_4_READY_FOR_INTEGRATION_REGRESSION=true" in source
    assert "MILESTONE_26_TASK_4_ARCHIVE_ITEM_COUNT=3" in source
    assert "MILESTONE_26_TASK_4_FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT=true" in source
    assert "MILESTONE_26_TASK_4_NEXT_STAGE=MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_V1" in source


def test_task_5_regression_contract() -> None:
    regression = build_milestone_26_integration_regression()
    assert regression.valid is True
    assert regression.regression_ok is True
    assert regression.current_task_number == 5
    assert regression.task_budget_max == 8
    assert regression.remaining_budget_after_current_task == 3
    assert len(regression.regression_checks) == 14
    assert len(regression.generated_artifacts) == 5
    assert validate_milestone_26_integration_regression(regression) == ()


def test_task_5_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_READY=true" in text
    assert "MILESTONE_26_TASK_5_TASK_CHAIN_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_5_SOURCE_ARTIFACTS_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_5_ARCHIVE_INDEX_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_5_ARCHIVE_MANIFEST_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_5_BOUNDARY_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_5_INTEGRITY_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_5_NO_MUTATION_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_26_TASK_5_READY_FOR_MILESTONE_CLOSURE=true" in text
    assert "MILESTONE_26_TASK_5_TASK1_VALID=true" in text
    assert "MILESTONE_26_TASK_5_TASK2_VALID=true" in text
    assert "MILESTONE_26_TASK_5_TASK3_VALID=true" in text
    assert "MILESTONE_26_TASK_5_TASK4_VALID=true" in text
    assert "MILESTONE_26_TASK_5_ARCHIVE_ITEM_COUNT=3" in text
    assert "MILESTONE_26_TASK_5_ARCHIVED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_26_TASK_5_CURRENT_TASK_NUMBER=5" in text
    assert "MILESTONE_26_TASK_5_FAST_SOURCE_VALIDATION_SNAPSHOT=true" in text
    assert "MILESTONE_26_TASK_5_NEXT_STAGE=MILESTONE_26_TASK_6_MILESTONE_CLOSURE_V1" in text


def test_task_5_artifacts() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))

    assert report["valid"] is True
    assert report["regressionOk"] is True
    assert report["issues"] == []
    assert report["readyForMilestoneClosure"] is True
    assert report["taskChainValidated"] is True
    assert report["sourceArtifactsValidated"] is True

    assert manifest["taskId"] == "MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_V1"
    assert manifest["readyForMilestoneClosure"] is True
    assert manifest["task1Valid"] is True
    assert manifest["task2Valid"] is True
    assert manifest["task3Valid"] is True
    assert manifest["task4Valid"] is True
    assert manifest["nextStage"] == "MILESTONE_26_TASK_6_MILESTONE_CLOSURE_V1"

    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert boundary["runtimeSolverModified"] is False
    assert boundary["kaggleSubmissionSent"] is False
    assert boundary["legalCertification"] is False
