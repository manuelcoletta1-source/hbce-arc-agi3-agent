"""Milestone #19 Task 82 - SRSC local ledger integration review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_81 = ROOT / "docs" / "milestone-19-task-81-srsc-claim-ledger-evidence-gate-local-implementation-v1.md"
DOC_TASK_82 = ROOT / "docs" / "milestone-19-task-82-srsc-local-ledger-integration-review-v1.md"
CLAIM_LEDGER = ROOT / "src" / "hbce_arc_agi3" / "srsc_claim_ledger.py"
EVIDENCE_GATE = ROOT / "src" / "hbce_arc_agi3" / "srsc_evidence_gate.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-local-ledger-integration-review-v1"
    / "task-82-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-local-ledger-integration-review-v1"
    / "task-82-index.txt"
)


def test_task_82_required_files_exist() -> None:
    assert DOC_TASK_81.exists()
    assert DOC_TASK_82.exists()
    assert CLAIM_LEDGER.exists()
    assert EVIDENCE_GATE.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_82_dependency_markers() -> None:
    text = DOC_TASK_81.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_81_SRSC_CLAIM_LEDGER_EVIDENCE_GATE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_81_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_81_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_82_canonical_decision_markers() -> None:
    text = DOC_TASK_82.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_82_SRSC_LOCAL_LEDGER_INTEGRATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_82_STATUS=INTEGRATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_82_MODE=REVIEW_ONLY_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_82_DECISION=AUTHORIZE_NEXT_TASK_DIAGNOSTIC_REFERENCE_PLANNING_ONLY" in text
    assert "MILESTONE_19_TASK_82_INTEGRATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_82_DIAGNOSTIC_REFERENCE_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_82_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_82_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_82_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_82_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_82_FAIL_CLOSED_ACTIVE=true" in text


def test_task_82_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_82_SRSC_LOCAL_LEDGER_INTEGRATION_REVIEW_V1"
    assert manifest["status"] == "INTEGRATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_81_SRSC_CLAIM_LEDGER_EVIDENCE_GATE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_DIAGNOSTIC_REFERENCE_PLANNING_ONLY"
    assert manifest["integrationReviewPerformed"] is True
    assert manifest["diagnosticReferencePlanningAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask82"] is False
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


def test_task_82_reviewed_modules_are_srsc_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["reviewedModules"] == [
        "src/hbce_arc_agi3/srsc_claim_ledger.py",
        "src/hbce_arc_agi3/srsc_evidence_gate.py",
    ]
    blocked = manifest["blockedIntegrations"]
    assert "solver runtime wiring" in blocked
    assert "candidate generator mutation" in blocked
    assert "ranker scoring mutation" in blocked
    assert "verifier mutation" in blocked
    assert "Kaggle submission flow" in blocked
