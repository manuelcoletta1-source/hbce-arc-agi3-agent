"""Milestone #19 Task 85 - SRSC diagnostic reference schema local implementation validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_84 = ROOT / "docs" / "milestone-19-task-84-srsc-diagnostic-reference-record-schema-authorization-review-v1.md"
DOC_TASK_85 = ROOT / "docs" / "milestone-19-task-85-srsc-diagnostic-reference-record-schema-local-implementation-v1.md"
SCHEMA_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_reference.py"
SCHEMA_TEST = ROOT / "tests" / "test_srsc_diagnostic_reference.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-reference-record-schema-local-implementation-v1"
    / "task-85-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-reference-record-schema-local-implementation-v1"
    / "task-85-index.txt"
)


def test_task_85_required_files_exist() -> None:
    assert DOC_TASK_84.exists()
    assert DOC_TASK_85.exists()
    assert SCHEMA_MODULE.exists()
    assert SCHEMA_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_85_dependency_markers() -> None:
    text = DOC_TASK_84.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_84_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_84_SCHEMA_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_84_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_84_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_85_canonical_markers() -> None:
    text = DOC_TASK_85.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_85_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_85_STATUS=LOCAL_SCHEMA_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_85_MODE=LOCAL_STANDALONE_SCHEMA_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_85_SCHEMA_IMPLEMENTATION_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_85_LOCAL_STANDALONE_SCHEMA=true" in text
    assert "MILESTONE_19_TASK_85_DIAGNOSTIC_ADAPTER_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_85_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_85_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_85_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_85_FAIL_CLOSED_ACTIVE=true" in text


def test_task_85_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_85_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "LOCAL_SCHEMA_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_STANDALONE_SCHEMA_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_84_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_AUTHORIZATION_REVIEW_V1"
    assert manifest["schemaImplementationPerformed"] is True
    assert manifest["localStandaloneSchema"] is True
    assert manifest["diagnosticAdapterImplemented"] is False
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


def test_task_85_schema_module_is_schema_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["implementedModules"] == ["src/hbce_arc_agi3/srsc_diagnostic_reference.py"]
    assert manifest["implementedTests"] == ["tests/test_srsc_diagnostic_reference.py"]
    assert "DiagnosticReferenceSourceType" in manifest["implementedSchemaTypes"]
    assert "SrscDiagnosticReferenceRecord" in manifest["implementedSchemaTypes"]
    assert "DiagnosticReferenceBoundary" in manifest["implementedSchemaTypes"]
    assert "create_diagnostic_reference_record" in manifest["implementedSchemaTypes"]
