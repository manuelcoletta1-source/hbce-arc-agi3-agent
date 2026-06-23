"""Milestone #19 Task 86 - SRSC diagnostic reference schema implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_85 = ROOT / "docs" / "milestone-19-task-85-srsc-diagnostic-reference-record-schema-local-implementation-v1.md"
DOC_TASK_86 = ROOT / "docs" / "milestone-19-task-86-srsc-diagnostic-reference-record-schema-implementation-review-v1.md"
SCHEMA_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_reference.py"
SCHEMA_TEST = ROOT / "tests" / "test_srsc_diagnostic_reference.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-reference-record-schema-implementation-review-v1"
    / "task-86-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-reference-record-schema-implementation-review-v1"
    / "task-86-index.txt"
)


def test_task_86_required_files_exist() -> None:
    assert DOC_TASK_85.exists()
    assert DOC_TASK_86.exists()
    assert SCHEMA_MODULE.exists()
    assert SCHEMA_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_86_dependency_markers() -> None:
    text = DOC_TASK_85.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_85_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_85_LOCAL_STANDALONE_SCHEMA=true" in text
    assert "MILESTONE_19_TASK_85_DIAGNOSTIC_ADAPTER_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_85_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_85_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_86_canonical_markers() -> None:
    text = DOC_TASK_86.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_86_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_86_STATUS=IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_86_MODE=REVIEW_ONLY_NO_ADAPTER_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_86_DECISION=AUTHORIZE_NEXT_TASK_DIAGNOSTIC_ADAPTER_PLANNING_ONLY" in text
    assert "MILESTONE_19_TASK_86_SCHEMA_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_86_DIAGNOSTIC_ADAPTER_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_86_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_86_ADAPTER_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_86_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_86_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_86_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_86_FAIL_CLOSED_ACTIVE=true" in text


def test_task_86_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_86_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_ADAPTER_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_85_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_LOCAL_IMPLEMENTATION_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_DIAGNOSTIC_ADAPTER_PLANNING_ONLY"
    assert manifest["schemaImplementationReviewPerformed"] is True
    assert manifest["diagnosticAdapterPlanningAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask86"] is False
    assert manifest["adapterImplementedInTask86"] is False
    assert manifest["runtimeActivationAuthorized"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["candidateGeneratorModified"] is False
    assert manifest["rankerModified"] is False
    assert manifest["verifierModified"] is False
    assert manifest["benchmarkScoreClaimed"] is False
    assert manifest["realEvaluationPerformed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["internetDuringEval"] is False
    assert manifest["externalApiDependency"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedRequired"] is True
    assert manifest["failClosedActive"] is True


def test_task_86_future_targets_are_planning_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    targets = manifest["futurePlanningTargets"]
    blocked = manifest["blockedBindings"]

    assert targets == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter.py",
        "tests/test_srsc_diagnostic_adapter.py",
    ]
    assert "diagnostic adapter implementation" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
