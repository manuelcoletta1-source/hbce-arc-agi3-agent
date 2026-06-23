"""Milestone #19 Task 87 - SRSC diagnostic adapter planning validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_86 = ROOT / "docs" / "milestone-19-task-86-srsc-diagnostic-reference-record-schema-implementation-review-v1.md"
DOC_TASK_87 = ROOT / "docs" / "milestone-19-task-87-srsc-diagnostic-adapter-planning-v1.md"
SCHEMA_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_reference.py"
SCHEMA_TEST = ROOT / "tests" / "test_srsc_diagnostic_reference.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-planning-v1"
    / "task-87-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-planning-v1"
    / "task-87-index.txt"
)


def test_task_87_required_files_exist() -> None:
    assert DOC_TASK_86.exists()
    assert DOC_TASK_87.exists()
    assert SCHEMA_MODULE.exists()
    assert SCHEMA_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_87_dependency_markers() -> None:
    text = DOC_TASK_86.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_86_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_86_DIAGNOSTIC_ADAPTER_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_86_ADAPTER_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_86_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_86_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_87_canonical_markers() -> None:
    text = DOC_TASK_87.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_87_SRSC_DIAGNOSTIC_ADAPTER_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_87_STATUS=DIAGNOSTIC_ADAPTER_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_87_MODE=PLANNING_ONLY_NO_ADAPTER_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_87_DECISION=PLAN_LOCAL_DIAGNOSTIC_ADAPTER_ONLY" in text
    assert "MILESTONE_19_TASK_87_ADAPTER_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_87_ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_87_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_87_ADAPTER_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_87_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_87_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_87_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_87_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_87_FAIL_CLOSED_ACTIVE=true" in text


def test_task_87_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_87_SRSC_DIAGNOSTIC_ADAPTER_PLANNING_V1"
    assert manifest["status"] == "DIAGNOSTIC_ADAPTER_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_ADAPTER_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_86_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_IMPLEMENTATION_REVIEW_V1"
    assert manifest["decision"] == "PLAN_LOCAL_DIAGNOSTIC_ADAPTER_ONLY"
    assert manifest["adapterPlanningPerformed"] is True
    assert manifest["adapterImplementationAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask87"] is False
    assert manifest["adapterImplementedInTask87"] is False
    assert manifest["adapterActivatedInTask87"] is False
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


def test_task_87_future_targets_are_planning_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    targets = manifest["futurePlanningTargets"]
    blocked = manifest["blockedBindings"]

    assert targets == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter.py",
        "tests/test_srsc_diagnostic_adapter.py",
    ]

    assert "diagnostic adapter implementation" in blocked
    assert "diagnostic adapter activation" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked


def test_task_87_planned_io_is_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    inputs = manifest["plannedFutureAdapterInputs"]
    outputs = manifest["plannedFutureAdapterOutputs"]

    assert "DiagnosticReferenceSourceType" in inputs
    assert "srscClaimId" in inputs
    assert "srscGateDecisionId" in inputs
    assert "evidenceRefs" in inputs
    assert "SrscDiagnosticReferenceRecord" in outputs
    assert "blocked reference report" in outputs

    assert all("solver" not in item.lower() for item in inputs)
    assert all("kaggle" not in item.lower() for item in outputs)
