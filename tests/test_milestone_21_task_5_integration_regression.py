"""Milestone #21 Task 5 integration regression validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_21_integration_regression import (
    build_milestone_21_integration_regression,
    validate_milestone_21_integration_regression,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-21-task-5-integration-regression-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_21_integration_regression.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_21_integration_regression.py"
MANIFEST = ROOT / "examples" / "milestone-21" / "integration-regression-v1" / "task-5-manifest.json"
INDEX = ROOT / "examples" / "milestone-21" / "integration-regression-v1" / "task-5-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-21" / "integration-regression-v1" / "task-5-integration-regression.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-21" / "integration-regression-v1" / "task-5-integration-regression.md"
TASK_4_DOC = ROOT / "docs" / "milestone-21-task-4-validation-and-artifacts-v1.md"
TASK_3_DOC = ROOT / "docs" / "milestone-21-task-3-scoped-operator-decision-handoff-implementation-v1.md"
TASK_2_DOC = ROOT / "docs" / "milestone-21-task-2-objective-selection-and-scope-lock-v1.md"
TASK_1_DOC = ROOT / "docs" / "milestone-21-task-1-governed-opening-with-task-budget-v1.md"
M20_CLOSURE = ROOT / "docs" / "milestone-20-task-7-milestone-closure-v1.md"


def test_task_5_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_4_DOC.exists()
    assert TASK_3_DOC.exists()
    assert TASK_2_DOC.exists()
    assert TASK_1_DOC.exists()
    assert M20_CLOSURE.exists()


def test_task_5_dependencies_are_present() -> None:
    task4 = TASK_4_DOC.read_text(encoding="utf-8")
    task3 = TASK_3_DOC.read_text(encoding="utf-8")
    task2 = TASK_2_DOC.read_text(encoding="utf-8")
    task1 = TASK_1_DOC.read_text(encoding="utf-8")
    milestone20 = M20_CLOSURE.read_text(encoding="utf-8")

    assert "MILESTONE_21_TASK_4_ARTIFACTS_READY_FOR_INTEGRATION_REGRESSION=true" in task4
    assert "MILESTONE_21_TASK_4_NEXT_STAGE=MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1" in task4
    assert "MILESTONE_21_TASK_3_HANDOFF_PACKAGE_CREATED=true" in task3
    assert "MILESTONE_21_TASK_2_SCOPE_LOCKED=true" in task2
    assert "MILESTONE_21_TASK_1_TASK_BUDGET_MAX=8" in task1
    assert "MILESTONE_20_TASK_7_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8" in milestone20
    assert "MILESTONE_20_TASK_7_TASK_8_USED=false" in milestone20


def test_task_5_integration_regression_contract() -> None:
    regression = build_milestone_21_integration_regression()

    assert regression.valid is True
    assert regression.integration_ok is True
    assert regression.task_budget_max == 8
    assert regression.current_task_number == 5
    assert regression.recommended_closure_task_number == 6
    assert len(regression.integrated_task_labels) == 5
    assert len(regression.regression_checks) == 9
    assert len(regression.regression_artifacts) == 4
    assert validate_milestone_21_integration_regression(regression) == ()


def test_task_5_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_READY=true" in text
    assert "MILESTONE_21_TASK_5_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_21_TASK_5_CURRENT_TASK_NUMBER=5" in text
    assert "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_READY=true" in text
    assert "MILESTONE_21_TASK_5_TASK_CHAIN_INTEGRATED=true" in text
    assert "MILESTONE_21_TASK_5_REGRESSION_CHECKS_CREATED=true" in text
    assert "MILESTONE_21_TASK_5_REGRESSION_CHECKS_PASSED=true" in text
    assert "MILESTONE_21_TASK_5_READY_FOR_MILESTONE_CLOSURE=true" in text
    assert "MILESTONE_21_TASK_5_MILESTONE_20_TASK_8_REQUIRED=false" in text
    assert "MILESTONE_21_TASK_5_NEXT_STAGE=MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1" in text


def test_task_5_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 5
    assert manifest["integrationRegressionReady"] is True
    assert manifest["taskChainIntegrated"] is True
    assert manifest["regressionChecksCreated"] is True
    assert manifest["regressionChecksPassed"] is True
    assert manifest["readyForMilestoneClosure"] is True
    assert manifest["regressionCheckCount"] == 9
    assert artifact["valid"] is True
    assert artifact["integrationOk"] is True
    assert artifact["issues"] == []
