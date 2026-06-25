"""Milestone #22 Task 3 fast snapshot dependency guard validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_22_fast_snapshot_dependency_guard import (
    build_fast_snapshot_dependency_guard,
    detect_forbidden_runtime_traversal,
    validate_fast_snapshot_dependency_guard,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-22-task-3-fast-snapshot-dependency-guard-implementation-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_22_fast_snapshot_dependency_guard.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_22_fast_snapshot_dependency_guard.py"
MANIFEST = ROOT / "examples" / "milestone-22" / "fast-snapshot-dependency-guard-implementation-v1" / "task-3-manifest.json"
INDEX = ROOT / "examples" / "milestone-22" / "fast-snapshot-dependency-guard-implementation-v1" / "task-3-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-22" / "fast-snapshot-dependency-guard-implementation-v1" / "task-3-fast-snapshot-dependency-guard.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-22" / "fast-snapshot-dependency-guard-implementation-v1" / "task-3-fast-snapshot-dependency-guard.md"
TASK_2_DOC = ROOT / "docs" / "milestone-22-task-2-objective-selection-and-scope-lock-v1.md"


def test_task_3_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_2_DOC.exists()


def test_task_3_dependency_is_present() -> None:
    task2 = TASK_2_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in task2
    assert "MILESTONE_22_TASK_2_SCOPE_LOCK_ID=MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY" in task2
    assert "MILESTONE_22_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in task2
    assert "MILESTONE_22_TASK_2_FAST_SNAPSHOT_PATTERN_REQUIRED=true" in task2
    assert "MILESTONE_22_TASK_2_DEEP_RECURSIVE_SERIALIZATION_FORBIDDEN=true" in task2
    assert "MILESTONE_22_TASK_2_NEXT_STAGE=MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1" in task2


def test_task_3_guard_contract() -> None:
    guard = build_fast_snapshot_dependency_guard()

    assert guard.valid is True
    assert guard.guard_ok is True
    assert guard.task_budget_max == 8
    assert guard.current_task_number == 3
    assert guard.recommended_closure_task_number == 6
    assert guard.snapshot_count == 2
    assert len(guard.guard_checks) == 10
    assert validate_fast_snapshot_dependency_guard(guard) == ()


def test_task_3_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_22_TASK_3_SCOPE_LOCK_ID=MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY" in text
    assert "MILESTONE_22_TASK_3_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_22_TASK_3_CURRENT_TASK_NUMBER=3" in text
    assert "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTED=true" in text
    assert "MILESTONE_22_TASK_3_LOCAL_ONLY_GUARD=true" in text
    assert "MILESTONE_22_TASK_3_SNAPSHOT_PATTERN_ENFORCED=true" in text
    assert "MILESTONE_22_TASK_3_DEEP_RECURSIVE_TRAVERSAL_BLOCKED=true" in text
    assert "MILESTONE_22_TASK_3_READY_FOR_VALIDATION_ARTIFACTS=true" in text
    assert "MILESTONE_22_TASK_3_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_22_TASK_3_NEXT_STAGE=MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in text


def test_task_3_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1"
    assert manifest["scopeLockId"] == "MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 3
    assert manifest["fastSnapshotDependencyGuardReady"] is True
    assert manifest["fastSnapshotDependencyGuardImplemented"] is True
    assert manifest["localOnlyGuard"] is True
    assert manifest["snapshotPatternEnforced"] is True
    assert manifest["deepRecursiveTraversalBlocked"] is True
    assert manifest["readyForValidationArtifacts"] is True
    assert artifact["valid"] is True
    assert artifact["guardOk"] is True
    assert artifact["issues"] == []


def test_task_3_detects_forbidden_traversal() -> None:
    detected = detect_forbidden_runtime_traversal(
        [
            "safe_static_snapshot",
            "closed_milestone.valid",
            "historical_milestone_revalidation_as_runtime_traversal",
        ]
    )

    assert detected == (
        "closed_milestone.valid",
        "historical_milestone_revalidation_as_runtime_traversal",
    )
