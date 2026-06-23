"""Milestone #19 Task 89 - SRSC diagnostic adapter local implementation validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_88 = ROOT / "docs" / "milestone-19-task-88-srsc-diagnostic-adapter-implementation-authorization-review-v1.md"
DOC_TASK_89 = ROOT / "docs" / "milestone-19-task-89-srsc-diagnostic-adapter-local-implementation-v1.md"
ADAPTER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter.py"
ADAPTER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-local-implementation-v1"
    / "task-89-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-local-implementation-v1"
    / "task-89-index.txt"
)


def test_task_89_required_files_exist() -> None:
    assert DOC_TASK_88.exists()
    assert DOC_TASK_89.exists()
    assert ADAPTER_MODULE.exists()
    assert ADAPTER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_89_dependency_markers() -> None:
    text = DOC_TASK_88.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_88_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_88_ADAPTER_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_88_ADAPTER_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_88_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_88_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_88_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_89_canonical_markers() -> None:
    text = DOC_TASK_89.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_89_SRSC_DIAGNOSTIC_ADAPTER_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_89_STATUS=LOCAL_ADAPTER_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_89_MODE=LOCAL_STANDALONE_ADAPTER_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_89_ADAPTER_IMPLEMENTATION_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_89_LOCAL_STANDALONE_ADAPTER=true" in text
    assert "MILESTONE_19_TASK_89_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_89_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_89_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_89_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_89_FAIL_CLOSED_ACTIVE=true" in text


def test_task_89_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_89_SRSC_DIAGNOSTIC_ADAPTER_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "LOCAL_ADAPTER_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_STANDALONE_ADAPTER_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_88_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["adapterImplementationPerformed"] is True
    assert manifest["localStandaloneAdapter"] is True
    assert manifest["adapterActivated"] is False
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


def test_task_89_adapter_module_is_local_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["implementedModules"] == ["src/hbce_arc_agi3/srsc_diagnostic_adapter.py"]
    assert manifest["implementedTests"] == ["tests/test_srsc_diagnostic_adapter.py"]
    assert "DiagnosticAdapterInput" in manifest["implementedAdapterTypes"]
    assert "DiagnosticAdapterResult" in manifest["implementedAdapterTypes"]
    assert "DiagnosticAdapterBlockedReference" in manifest["implementedAdapterTypes"]
    assert "adapt_diagnostic_input_to_reference" in manifest["implementedAdapterTypes"]
    assert "adapt_diagnostic_inputs_to_references" in manifest["implementedAdapterTypes"]
