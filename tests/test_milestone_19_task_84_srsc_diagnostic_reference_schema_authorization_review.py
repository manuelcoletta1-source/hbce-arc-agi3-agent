"""Milestone #19 Task 84 - SRSC diagnostic reference schema authorization review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_83 = ROOT / "docs" / "milestone-19-task-83-srsc-diagnostic-reference-planning-v1.md"
DOC_TASK_84 = ROOT / "docs" / "milestone-19-task-84-srsc-diagnostic-reference-record-schema-authorization-review-v1.md"
CLAIM_LEDGER = ROOT / "src" / "hbce_arc_agi3" / "srsc_claim_ledger.py"
EVIDENCE_GATE = ROOT / "src" / "hbce_arc_agi3" / "srsc_evidence_gate.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-reference-record-schema-authorization-review-v1"
    / "task-84-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-reference-record-schema-authorization-review-v1"
    / "task-84-index.txt"
)


def test_task_84_required_files_exist() -> None:
    assert DOC_TASK_83.exists()
    assert DOC_TASK_84.exists()
    assert CLAIM_LEDGER.exists()
    assert EVIDENCE_GATE.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_84_dependency_markers() -> None:
    text = DOC_TASK_83.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_83_SRSC_DIAGNOSTIC_REFERENCE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_83_SCHEMA_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_83_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_83_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_84_canonical_markers() -> None:
    text = DOC_TASK_84.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_84_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_84_STATUS=SCHEMA_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_84_MODE=REVIEW_ONLY_NO_SCHEMA_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_84_DECISION=AUTHORIZE_NEXT_TASK_LOCAL_SCHEMA_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_84_SCHEMA_AUTHORIZATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_84_SCHEMA_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_84_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_84_SCHEMA_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_84_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_84_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_84_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_84_FAIL_CLOSED_ACTIVE=true" in text


def test_task_84_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_84_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "SCHEMA_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_SCHEMA_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_83_SRSC_DIAGNOSTIC_REFERENCE_PLANNING_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_LOCAL_SCHEMA_IMPLEMENTATION_ONLY"
    assert manifest["schemaAuthorizationReviewPerformed"] is True
    assert manifest["schemaImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask84"] is False
    assert manifest["schemaImplementedInTask84"] is False
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


def test_task_84_authorized_future_modules_are_schema_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    modules = manifest["authorizedFutureModules"]
    assert modules == [
        "src/hbce_arc_agi3/srsc_diagnostic_reference.py",
        "tests/test_srsc_diagnostic_reference.py",
    ]
    assert all("solver" not in module for module in modules)
    assert all("ranker" not in module for module in modules)
    assert all("verifier" not in module for module in modules)


def test_task_84_required_schema_types_and_blocked_bindings() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    schema_types = manifest["requiredFutureSchemaTypes"]
    blocked = manifest["blockedBindings"]

    assert "DiagnosticReferenceSourceType" in schema_types
    assert "SrscDiagnosticReferenceRecord" in schema_types
    assert "DiagnosticReferenceBoundary" in schema_types
    assert "create_diagnostic_reference_record" in schema_types

    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
