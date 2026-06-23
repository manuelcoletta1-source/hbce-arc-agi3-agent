"""Milestone #19 Task 83 - SRSC diagnostic reference planning validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_82 = ROOT / "docs" / "milestone-19-task-82-srsc-local-ledger-integration-review-v1.md"
DOC_TASK_83 = ROOT / "docs" / "milestone-19-task-83-srsc-diagnostic-reference-planning-v1.md"
CLAIM_LEDGER = ROOT / "src" / "hbce_arc_agi3" / "srsc_claim_ledger.py"
EVIDENCE_GATE = ROOT / "src" / "hbce_arc_agi3" / "srsc_evidence_gate.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-reference-planning-v1"
    / "task-83-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-reference-planning-v1"
    / "task-83-index.txt"
)


def test_task_83_required_files_exist() -> None:
    assert DOC_TASK_82.exists()
    assert DOC_TASK_83.exists()
    assert CLAIM_LEDGER.exists()
    assert EVIDENCE_GATE.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_83_dependency_markers() -> None:
    text = DOC_TASK_82.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_82_SRSC_LOCAL_LEDGER_INTEGRATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_82_DECISION=AUTHORIZE_NEXT_TASK_DIAGNOSTIC_REFERENCE_PLANNING_ONLY" in text
    assert "MILESTONE_19_TASK_82_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_82_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_83_canonical_markers() -> None:
    text = DOC_TASK_83.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_83_SRSC_DIAGNOSTIC_REFERENCE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_83_STATUS=DIAGNOSTIC_REFERENCE_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_83_MODE=PLANNING_ONLY_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_83_DECISION=PLAN_DIAGNOSTIC_REFERENCE_RECORDS_ONLY" in text
    assert "MILESTONE_19_TASK_83_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_83_SCHEMA_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_83_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_83_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_83_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_83_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_83_FAIL_CLOSED_ACTIVE=true" in text


def test_task_83_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_83_SRSC_DIAGNOSTIC_REFERENCE_PLANNING_V1"
    assert manifest["status"] == "DIAGNOSTIC_REFERENCE_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_82_SRSC_LOCAL_LEDGER_INTEGRATION_REVIEW_V1"
    assert manifest["decision"] == "PLAN_DIAGNOSTIC_REFERENCE_RECORDS_ONLY"
    assert manifest["planningPerformed"] is True
    assert manifest["schemaAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask83"] is False
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


def test_task_83_planned_fields_and_blocked_bindings() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    fields = manifest["plannedDiagnosticReferenceFields"]
    assert "srscClaimId" in fields
    assert "srscGateDecisionId" in fields
    assert "claimState" in fields
    assert "evidenceState" in fields
    assert "diagnosticScope" in fields
    assert "boundaryState" in fields
    assert "runtimeSolverModified" in fields
    assert "runtimeWiringAllowed" in fields
    assert "failClosedActive" in fields

    blocked = manifest["blockedBindings"]
    assert "direct solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked


def test_task_83_allowed_source_types_are_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    allowed = manifest["allowedFutureSourceTypes"]

    assert "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD" in allowed
    assert "PUBLIC_SAFE_AUDIT_SUMMARY" in allowed
    assert "LOCAL_CLAIM_REVIEW_REPORT" in allowed
    assert "EVIDENCE_BOUND_DIAGNOSTIC_NOTE" in allowed
    assert "MILESTONE_CLOSURE_RECORD" in allowed
    assert "SOURCE_FILE_EVIDENCE_NOTE" in allowed

    assert all("SOLVER_RUNTIME" not in value for value in allowed)
    assert all("KAGGLE_SUBMISSION" not in value for value in allowed)
