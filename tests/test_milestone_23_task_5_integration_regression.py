"""Milestone #23 Task 5 integration regression validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_23_integration_regression import (
    build_milestone_23_integration_regression,
    validate_milestone_23_integration_regression,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-23-task-5-integration-regression-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_23_integration_regression.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_23_integration_regression.py"
MANIFEST = ROOT / "examples" / "milestone-23" / "integration-regression-v1" / "task-5-manifest.json"
INDEX = ROOT / "examples" / "milestone-23" / "integration-regression-v1" / "task-5-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-23" / "integration-regression-v1" / "task-5-integration-regression.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-23" / "integration-regression-v1" / "task-5-integration-regression.md"
TASK_4_DOC = ROOT / "docs" / "milestone-23-task-4-validation-and-artifacts-v1.md"


def test_task_5_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_4_DOC.exists()


def test_task_5_dependency_is_present() -> None:
    task4 = TASK_4_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_READY=true" in task4
    assert "MILESTONE_23_TASK_4_REGISTRY_VALIDATED=true" in task4
    assert "MILESTONE_23_TASK_4_BOUNDARY_VALIDATED=true" in task4
    assert "MILESTONE_23_TASK_4_READY_FOR_INTEGRATION_REGRESSION=true" in task4
    assert "MILESTONE_23_TASK_4_NEXT_STAGE=MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1" in task4


def test_task_5_integration_contract() -> None:
    integration = build_milestone_23_integration_regression()

    assert integration.valid is True
    assert integration.integration_ok is True
    assert integration.task_budget_max == 8
    assert integration.current_task_number == 5
    assert len(integration.integration_cases) == 16
    assert len(integration.generated_artifacts) == 4
    assert validate_milestone_23_integration_regression(integration) == ()


def test_task_5_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_READY=true" in text
    assert "MILESTONE_23_TASK_5_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_23_TASK_5_CURRENT_TASK_NUMBER=5" in text
    assert "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_EXECUTED=true" in text
    assert "MILESTONE_23_TASK_5_TASK_CHAIN_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_5_REGISTRY_INTEGRATION_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_5_ARTIFACT_CHAIN_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_5_BOUNDARY_REGRESSION_VALIDATED=true" in text
    assert "MILESTONE_23_TASK_5_READY_FOR_MILESTONE_CLOSURE=true" in text
    assert "MILESTONE_23_TASK_5_REGISTRY_SNAPSHOT_COUNT=3" in text
    assert "MILESTONE_23_TASK_5_M20_TASK_7_USED=true" in text
    assert "MILESTONE_23_TASK_5_M20_TASK_8_USED=false" in text
    assert "MILESTONE_23_TASK_5_M21_TASK_7_USED=false" in text
    assert "MILESTONE_23_TASK_5_M22_TASK_7_USED=false" in text
    assert "MILESTONE_23_TASK_5_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_23_TASK_5_NEXT_STAGE=MILESTONE_23_TASK_6_MILESTONE_CLOSURE_V1" in text


def test_task_5_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1"
    assert manifest["integrationRegressionExecuted"] is True
    assert manifest["taskChainValidated"] is True
    assert manifest["registryIntegrationValidated"] is True
    assert manifest["artifactChainValidated"] is True
    assert manifest["boundaryRegressionValidated"] is True
    assert manifest["readyForMilestoneClosure"] is True
    assert manifest["registrySnapshotCount"] == 3
    assert manifest["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert artifact["valid"] is True
    assert artifact["integrationOk"] is True
    assert artifact["registryValid"] is True
    assert artifact["registrySnapshotCount"] == 3
    assert artifact["issues"] == []
