"""Milestone #21 Task 3 scoped operator decision handoff implementation validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_21_operator_decision_handoff import (
    build_operator_decision_handoff_package,
    validate_operator_decision_handoff_package,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-21-task-3-scoped-operator-decision-handoff-implementation-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_21_operator_decision_handoff.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_21_operator_decision_handoff.py"
MANIFEST = ROOT / "examples" / "milestone-21" / "scoped-operator-decision-handoff-implementation-v1" / "task-3-manifest.json"
INDEX = ROOT / "examples" / "milestone-21" / "scoped-operator-decision-handoff-implementation-v1" / "task-3-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-21" / "scoped-operator-decision-handoff-implementation-v1" / "task-3-operator-decision-handoff.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-21" / "scoped-operator-decision-handoff-implementation-v1" / "task-3-operator-decision-handoff.md"
TASK_2_DOC = ROOT / "docs" / "milestone-21-task-2-objective-selection-and-scope-lock-v1.md"
M20_CLOSURE = ROOT / "docs" / "milestone-20-task-7-milestone-closure-v1.md"


def test_task_3_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_2_DOC.exists()
    assert M20_CLOSURE.exists()


def test_task_3_dependencies_are_present() -> None:
    task2 = TASK_2_DOC.read_text(encoding="utf-8")
    milestone20 = M20_CLOSURE.read_text(encoding="utf-8")

    assert "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in task2
    assert "MILESTONE_21_TASK_2_SCOPE_LOCKED=true" in task2
    assert "MILESTONE_21_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in task2
    assert "MILESTONE_21_TASK_2_NEXT_STAGE=MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1" in task2
    assert "MILESTONE_20_TASK_7_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8" in milestone20
    assert "MILESTONE_20_TASK_7_TASK_8_USED=false" in milestone20


def test_task_3_handoff_contract() -> None:
    package = build_operator_decision_handoff_package()

    assert package.valid is True
    assert package.handoff_ok is True
    assert package.handoff_scope_id == "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
    assert package.task_budget_max == 8
    assert package.current_task_number == 3
    assert package.recommended_closure_task_number == 6
    assert len(package.carried_state_keys) == 9
    assert len(package.implementation_contract_items) == 6
    assert len(package.forbidden_actions) == 10
    assert validate_operator_decision_handoff_package(package) == ()


def test_task_3_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_21_TASK_3_HANDOFF_KIND=LOCAL_ONLY_OPERATOR_DECISION_HANDOFF_PACKAGE" in text
    assert "MILESTONE_21_TASK_3_HANDOFF_SCOPE_ID=MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY" in text
    assert "MILESTONE_21_TASK_3_SOURCE_MILESTONE_ID=MILESTONE_20" in text
    assert "MILESTONE_21_TASK_3_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_21_TASK_3_CURRENT_TASK_NUMBER=3" in text
    assert "MILESTONE_21_TASK_3_HANDOFF_PACKAGE_CREATED=true" in text
    assert "MILESTONE_21_TASK_3_HANDOFF_LOCAL_ONLY=true" in text
    assert "MILESTONE_21_TASK_3_HANDOFF_READY_FOR_VALIDATION_ARTIFACTS=true" in text
    assert "MILESTONE_21_TASK_3_MILESTONE_20_TASK_8_REQUIRED=false" in text
    assert "MILESTONE_21_TASK_3_NEXT_STAGE=MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in text


def test_task_3_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1"
    assert manifest["handoffKind"] == "LOCAL_ONLY_OPERATOR_DECISION_HANDOFF_PACKAGE"
    assert manifest["handoffScopeId"] == "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 3
    assert manifest["handoffPackageCreated"] is True
    assert manifest["handoffLocalOnly"] is True
    assert manifest["handoffBoundedDiagnosticOnly"] is True
    assert manifest["handoffReadyForValidationArtifacts"] is True
    assert manifest["forbiddenActionCount"] == 10
    assert artifact["valid"] is True
    assert artifact["handoffOk"] is True
    assert artifact["issues"] == []
