"""Milestone #19 Task 88 - SRSC diagnostic adapter implementation authorization review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_87 = ROOT / "docs" / "milestone-19-task-87-srsc-diagnostic-adapter-planning-v1.md"
DOC_TASK_88 = ROOT / "docs" / "milestone-19-task-88-srsc-diagnostic-adapter-implementation-authorization-review-v1.md"
SCHEMA_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_reference.py"
SCHEMA_TEST = ROOT / "tests" / "test_srsc_diagnostic_reference.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-implementation-authorization-review-v1"
    / "task-88-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-implementation-authorization-review-v1"
    / "task-88-index.txt"
)


def test_task_88_required_files_exist() -> None:
    assert DOC_TASK_87.exists()
    assert DOC_TASK_88.exists()
    assert SCHEMA_MODULE.exists()
    assert SCHEMA_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_88_dependency_markers() -> None:
    text = DOC_TASK_87.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_87_SRSC_DIAGNOSTIC_ADAPTER_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_87_ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_87_ADAPTER_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_87_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_87_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_87_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_88_canonical_markers() -> None:
    text = DOC_TASK_88.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_88_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_88_STATUS=ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_88_MODE=REVIEW_ONLY_NO_ADAPTER_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_88_DECISION=AUTHORIZE_NEXT_TASK_LOCAL_ADAPTER_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_88_ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_88_ADAPTER_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_88_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_88_ADAPTER_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_88_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_88_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_88_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_88_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_88_FAIL_CLOSED_ACTIVE=true" in text


def test_task_88_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_88_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_ADAPTER_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_87_SRSC_DIAGNOSTIC_ADAPTER_PLANNING_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_LOCAL_ADAPTER_IMPLEMENTATION_ONLY"
    assert manifest["adapterImplementationAuthorizationReviewPerformed"] is True
    assert manifest["adapterImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask88"] is False
    assert manifest["adapterImplementedInTask88"] is False
    assert manifest["adapterActivatedInTask88"] is False
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


def test_task_88_authorized_future_modules_are_adapter_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    modules = manifest["authorizedFutureModules"]

    assert modules == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter.py",
        "tests/test_srsc_diagnostic_adapter.py",
    ]
    assert all("solver" not in module for module in modules)
    assert all("ranker" not in module for module in modules)
    assert all("verifier" not in module for module in modules)


def test_task_88_authorized_types_and_blocked_bindings() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    adapter_types = manifest["authorizedFutureAdapterTypes"]
    blocked = manifest["blockedBindings"]

    assert "DiagnosticAdapterInput" in adapter_types
    assert "DiagnosticAdapterResult" in adapter_types
    assert "DiagnosticAdapterBlockedReference" in adapter_types
    assert "adapt_diagnostic_input_to_reference" in adapter_types
    assert "adapt_diagnostic_inputs_to_references" in adapter_types

    assert "diagnostic adapter activation" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
