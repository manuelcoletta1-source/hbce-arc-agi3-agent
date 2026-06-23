"""Milestone #19 Task 80 - SRSC Claim Ledger authorization review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_79 = ROOT / "docs" / "milestone-19-task-79-srsc-cross-trace-framework-alignment-v1.md"
DOC_SRSC = ROOT / "docs" / "srsc-ai-framework-anti-allucinazioni-v1-0.md"
DOC_TASK_80 = ROOT / "docs" / "milestone-19-task-80-srsc-claim-ledger-implementation-authorization-review-v1.md"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-claim-ledger-implementation-authorization-review-v1"
    / "task-80-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-claim-ledger-implementation-authorization-review-v1"
    / "task-80-index.txt"
)


def test_task_80_documents_exist() -> None:
    assert DOC_TASK_79.exists()
    assert DOC_SRSC.exists()
    assert DOC_TASK_80.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_80_dependency_markers() -> None:
    task_79 = DOC_TASK_79.read_text(encoding="utf-8")
    srsc = DOC_SRSC.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_79_SRSC_CROSS_TRACE_FRAMEWORK_ALIGNMENT_READY=true" in task_79
    assert "SRSC_AI_FRAMEWORK_ANTI_ALLUCINAZIONI_V1_0_READY=true" in srsc


def test_task_80_canonical_decision_markers() -> None:
    text = DOC_TASK_80.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_80_SRSC_CLAIM_LEDGER_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_80_STATUS=AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_80_MODE=REVIEW_ONLY_NO_RUNTIME_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_80_DECISION=AUTHORIZE_NEXT_TASK_LOCAL_STANDALONE_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_80_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_80_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_80_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_80_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_80_FAIL_CLOSED_ACTIVE=true" in text


def test_task_80_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_80_SRSC_CLAIM_LEDGER_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_RUNTIME_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_79_SRSC_CROSS_TRACE_FRAMEWORK_ALIGNMENT_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_LOCAL_STANDALONE_IMPLEMENTATION_ONLY"
    assert manifest["implementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask80"] is False
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


def test_task_80_authorized_future_modules_are_standalone_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    modules = manifest["authorizedFutureModules"]
    assert "src/hbce_arc_agi3/srsc_claim_ledger.py" in modules
    assert "src/hbce_arc_agi3/srsc_evidence_gate.py" in modules
    assert "tests/test_srsc_claim_ledger.py" in modules
    assert "tests/test_srsc_evidence_gate.py" in modules
    assert all("solver" not in module for module in modules)
    assert all("ranker" not in module for module in modules)
