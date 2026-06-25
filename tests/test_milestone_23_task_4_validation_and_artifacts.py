"""Milestone #23 Task 4 validation artifacts validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_23_validation_artifacts import (
    build_milestone_23_validation_artifacts,
    validate_milestone_23_validation_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-23-task-4-validation-and-artifacts-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_23_validation_artifacts.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_23_validation_artifacts.py"
MANIFEST = ROOT / "examples" / "milestone-23" / "validation-and-artifacts-v1" / "task-4-manifest.json"
INDEX = ROOT / "examples" / "milestone-23" / "validation-and-artifacts-v1" / "task-4-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-23" / "validation-and-artifacts-v1" / "task-4-validation-artifacts.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-23" / "validation-and-artifacts-v1" / "task-4-validation-artifacts.md"
TASK_3_DOC = ROOT / "docs" / "milestone-23-task-3-closed-milestone-snapshot-registry-implementation-v1.md"


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

    assert "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_READY=true" in task3
    assert "MILESTONE_23_TASK_3_REGISTRY_IMPLEMENTED=true" in task3
    assert "MILESTONE_23_TASK_3_REGISTRY_LOOKUP_READY=true" in task3
    assert "MILESTONE_23_TASK_3_READY_FOR_VALIDATION_ARTIFACTS=true" in task3
    assert "MILESTONE_23_TASK_3_NEXT_STAGE=MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in task3


def test_task_4_validation_contract() -> None:
    artifacts = build_milestone_23_validation_artifacts()

    assert artifacts.valid is True
    assert artifacts.validation_ok is True
    assert artifacts.task_budget_max == 8
    assert artifacts.current_task_number == 4
    assert len(artifacts.validation_cases) == 12
    assert len(artifacts.generated_artifacts) == 4
    assert validate_milestone_23_validation_artifacts(artifacts) == ()


def test_task_4_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in text
    assert "MILESTONE_23_TASK_4_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_23_TASK_4_CURRENT_TASK_NUMBER=4" in text
    assert "MILESTONE_23_TASK_4_VALIDATION_ARTIFACTS_CREATED=true" in text
    assert "MILESTONE_23_TASK_4_REGISTRY_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_4_LOOKUP_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_4_SNAPSHOT_EVIDENCE_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_4_FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_4_BOUNDARY_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_4_READY_FOR_INTEGRATION_REGRESSION=true" in text
    assert "MILESTONE_23_TASK_4_REGISTRY_SNAPSHOT_COUNT=3" in text
    assert "MILESTONE_23_TASK_4_REGISTERED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_23_TASK_4_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_23_TASK_4_NEXT_STAGE=MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1" in text


def test_task_4_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert manifest["validationArtifactsCreated"] is True
    assert manifest["registryValidated"] is True
    assert manifest["lookupValidated"] is True
    assert manifest["snapshotEvidenceValidated"] is True
    assert manifest["forbiddenTraversalDetectionValidated"] is True
    assert manifest["boundaryValidated"] is True
    assert manifest["readyForIntegrationRegression"] is True
    assert manifest["registrySnapshotCount"] == 3
    assert manifest["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert artifact["valid"] is True
    assert artifact["validationOk"] is True
    assert artifact["registryValid"] is True
    assert artifact["registrySnapshotCount"] == 3
    assert artifact["issues"] == []
