"""Milestone #22 Task 4 validation and artifacts validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_22_validation_artifacts import (
    build_milestone_22_validation_artifacts,
    validate_milestone_22_validation_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-22-task-4-validation-and-artifacts-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_22_validation_artifacts.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_22_validation_artifacts.py"
MANIFEST = ROOT / "examples" / "milestone-22" / "validation-and-artifacts-v1" / "task-4-manifest.json"
INDEX = ROOT / "examples" / "milestone-22" / "validation-and-artifacts-v1" / "task-4-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-22" / "validation-and-artifacts-v1" / "task-4-validation-artifacts.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-22" / "validation-and-artifacts-v1" / "task-4-validation-artifacts.md"
TASK_3_DOC = ROOT / "docs" / "milestone-22-task-3-fast-snapshot-dependency-guard-implementation-v1.md"


def test_task_4_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_3_DOC.exists()


def test_task_4_dependency_is_present() -> None:
    task3 = TASK_3_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_READY=true" in task3
    assert "MILESTONE_22_TASK_3_DEEP_RECURSIVE_TRAVERSAL_BLOCKED=true" in task3
    assert "MILESTONE_22_TASK_3_READY_FOR_VALIDATION_ARTIFACTS=true" in task3
    assert "MILESTONE_22_TASK_3_NEXT_STAGE=MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in task3


def test_task_4_validation_contract() -> None:
    artifacts = build_milestone_22_validation_artifacts()

    assert artifacts.valid is True
    assert artifacts.validation_ok is True
    assert artifacts.task_budget_max == 8
    assert artifacts.current_task_number == 4
    assert artifacts.recommended_closure_task_number == 6
    assert len(artifacts.validation_cases) == 10
    assert len(artifacts.generated_artifacts) == 4
    assert validate_milestone_22_validation_artifacts(artifacts) == ()


def test_task_4_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in text
    assert "MILESTONE_22_TASK_4_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_22_TASK_4_CURRENT_TASK_NUMBER=4" in text
    assert "MILESTONE_22_TASK_4_VALIDATION_ARTIFACTS_CREATED=true" in text
    assert "MILESTONE_22_TASK_4_GUARD_VALIDATED=true" in text
    assert "MILESTONE_22_TASK_4_SNAPSHOT_EVIDENCE_VALIDATED=true" in text
    assert "MILESTONE_22_TASK_4_FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED=true" in text
    assert "MILESTONE_22_TASK_4_READY_FOR_INTEGRATION_REGRESSION=true" in text
    assert "MILESTONE_22_TASK_4_M20_FINAL_TASK_NUMBER=7" in text
    assert "MILESTONE_22_TASK_4_M20_TASK_7_USED=true" in text
    assert "MILESTONE_22_TASK_4_M20_TASK_8_USED=false" in text
    assert "MILESTONE_22_TASK_4_NEXT_STAGE=MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_V1" in text


def test_task_4_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 4
    assert manifest["validationArtifactsReady"] is True
    assert manifest["validationArtifactsCreated"] is True
    assert manifest["guardValidated"] is True
    assert manifest["snapshotEvidenceValidated"] is True
    assert manifest["forbiddenTraversalDetectionValidated"] is True
    assert manifest["readyForIntegrationRegression"] is True
    assert manifest["m20FinalTaskNumber"] == 7
    assert manifest["m20Task7Used"] is True
    assert manifest["m20Task8Used"] is False
    assert artifact["valid"] is True
    assert artifact["validationOk"] is True
    assert artifact["issues"] == []
