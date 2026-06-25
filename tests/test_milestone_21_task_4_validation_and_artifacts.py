"""Milestone #21 Task 4 validation and artifacts validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_21_validation_artifacts import (
    build_handoff_validation_artifacts,
    validate_handoff_validation_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-21-task-4-validation-and-artifacts-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_21_validation_artifacts.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_21_validation_artifacts.py"
MANIFEST = ROOT / "examples" / "milestone-21" / "validation-and-artifacts-v1" / "task-4-manifest.json"
INDEX = ROOT / "examples" / "milestone-21" / "validation-and-artifacts-v1" / "task-4-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-21" / "validation-and-artifacts-v1" / "task-4-validation-artifacts.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-21" / "validation-and-artifacts-v1" / "task-4-validation-artifacts.md"
TASK_3_DOC = ROOT / "docs" / "milestone-21-task-3-scoped-operator-decision-handoff-implementation-v1.md"
TASK_2_DOC = ROOT / "docs" / "milestone-21-task-2-objective-selection-and-scope-lock-v1.md"
M20_CLOSURE = ROOT / "docs" / "milestone-20-task-7-milestone-closure-v1.md"


def test_task_4_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_3_DOC.exists()
    assert TASK_2_DOC.exists()
    assert M20_CLOSURE.exists()


def test_task_4_dependencies_are_present() -> None:
    task3 = TASK_3_DOC.read_text(encoding="utf-8")
    task2 = TASK_2_DOC.read_text(encoding="utf-8")
    milestone20 = M20_CLOSURE.read_text(encoding="utf-8")

    assert "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_READY=true" in task3
    assert "MILESTONE_21_TASK_3_HANDOFF_READY_FOR_VALIDATION_ARTIFACTS=true" in task3
    assert "MILESTONE_21_TASK_3_NEXT_STAGE=MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in task3
    assert "MILESTONE_21_TASK_2_SCOPE_LOCKED=true" in task2
    assert "MILESTONE_20_TASK_7_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8" in milestone20
    assert "MILESTONE_20_TASK_7_TASK_8_USED=false" in milestone20


def test_task_4_validation_artifacts_contract() -> None:
    artifacts = build_handoff_validation_artifacts()

    assert artifacts.valid is True
    assert artifacts.validation_ok is True
    assert artifacts.task_budget_max == 8
    assert artifacts.current_task_number == 4
    assert artifacts.recommended_closure_task_number == 6
    assert len(artifacts.validation_checks) == 8
    assert len(artifacts.artifact_names) == 4
    assert len(artifacts.carried_boundary_markers) == 7
    assert validate_handoff_validation_artifacts(artifacts) == ()


def test_task_4_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in text
    assert "MILESTONE_21_TASK_4_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_21_TASK_4_CURRENT_TASK_NUMBER=4" in text
    assert "MILESTONE_21_TASK_4_VALIDATION_ARTIFACTS_READY=true" in text
    assert "MILESTONE_21_TASK_4_HANDOFF_PACKAGE_VALIDATED=true" in text
    assert "MILESTONE_21_TASK_4_VALIDATION_ARTIFACTS_CREATED=true" in text
    assert "MILESTONE_21_TASK_4_ARTIFACTS_LOCAL_ONLY=true" in text
    assert "MILESTONE_21_TASK_4_ARTIFACTS_DETERMINISTIC=true" in text
    assert "MILESTONE_21_TASK_4_ARTIFACTS_PUBLIC_SAFE=true" in text
    assert "MILESTONE_21_TASK_4_ARTIFACTS_READY_FOR_INTEGRATION_REGRESSION=true" in text
    assert "MILESTONE_21_TASK_4_MILESTONE_20_TASK_8_REQUIRED=false" in text
    assert "MILESTONE_21_TASK_4_NEXT_STAGE=MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1" in text


def test_task_4_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 4
    assert manifest["validationArtifactsReady"] is True
    assert manifest["handoffPackageValidated"] is True
    assert manifest["validationArtifactsCreated"] is True
    assert manifest["artifactsReadyForIntegrationRegression"] is True
    assert manifest["validationCheckCount"] == 8
    assert manifest["artifactNameCount"] == 4
    assert artifact["valid"] is True
    assert artifact["validationOk"] is True
    assert artifact["issues"] == []
