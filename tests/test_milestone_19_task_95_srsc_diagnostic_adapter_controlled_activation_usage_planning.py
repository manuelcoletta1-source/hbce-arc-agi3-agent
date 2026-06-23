"""Milestone #19 Task 95 - SRSC controlled activation usage planning validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_94 = ROOT / "docs" / "milestone-19-task-94-srsc-diagnostic-adapter-controlled-activation-implementation-review-v1.md"
DOC_TASK_95 = ROOT / "docs" / "milestone-19-task-95-srsc-diagnostic-adapter-controlled-activation-usage-planning-v1.md"
ACTIVATION_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation.py"
ACTIVATION_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-planning-v1"
    / "task-95-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-planning-v1"
    / "task-95-index.txt"
)


def test_task_95_required_files_exist() -> None:
    assert DOC_TASK_94.exists()
    assert DOC_TASK_95.exists()
    assert ACTIVATION_MODULE.exists()
    assert ACTIVATION_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_95_dependency_markers() -> None:
    text = DOC_TASK_94.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_94_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_94_CONTROLLED_ACTIVATION_USAGE_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_94_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_94_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_94_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_94_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_94_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_94_SOLVER_RUNTIME_BINDING=false" in text


def test_task_95_canonical_markers() -> None:
    text = DOC_TASK_95.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_95_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_95_STATUS=CONTROLLED_ACTIVATION_USAGE_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_95_MODE=PLANNING_ONLY_NO_USAGE_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_95_DECISION=PLAN_CONTROLLED_ACTIVATION_USAGE_ONLY" in text
    assert "MILESTONE_19_TASK_95_CONTROLLED_ACTIVATION_USAGE_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_95_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_95_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_95_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_95_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_95_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_95_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_95_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_95_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_95_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_95_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_95_FAIL_CLOSED_ACTIVE=true" in text


def test_task_95_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_95_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_PLANNING_V1"
    assert manifest["status"] == "CONTROLLED_ACTIVATION_USAGE_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_USAGE_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_94_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_V1"
    assert manifest["decision"] == "PLAN_CONTROLLED_ACTIVATION_USAGE_ONLY"
    assert manifest["controlledActivationUsagePlanningPerformed"] is True
    assert manifest["controlledActivationUsageImplementationAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask95"] is False
    assert manifest["usageImplementedInTask95"] is False
    assert manifest["activationModifiedInTask95"] is False
    assert manifest["adapterModifiedInTask95"] is False
    assert manifest["runtimeActivationAuthorized"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["solverRuntimeBinding"] is False
    assert manifest["candidateGeneratorModified"] is False
    assert manifest["candidateGeneratorBinding"] is False
    assert manifest["rankerModified"] is False
    assert manifest["rankerBinding"] is False
    assert manifest["verifierModified"] is False
    assert manifest["verifierBinding"] is False
    assert manifest["benchmarkScoreClaimed"] is False
    assert manifest["benchmarkBinding"] is False
    assert manifest["realEvaluationPerformed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["kaggleSubmissionBinding"] is False
    assert manifest["internetDuringEval"] is False
    assert manifest["externalApiDependency"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedRequired"] is True
    assert manifest["failClosedActive"] is True


def test_task_95_usage_contexts_are_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    allowed = manifest["plannedAllowedUsageContexts"]
    forbidden = manifest["plannedForbiddenUsageContexts"]

    assert "local SRSC diagnostic report generation" in allowed
    assert "local milestone evidence packaging" in allowed
    assert "local cross-trace planner evidence attachment" in allowed

    assert "solver runtime execution" in forbidden
    assert "candidate generation" in forbidden
    assert "candidate ranking" in forbidden
    assert "verifier execution" in forbidden
    assert "benchmark execution" in forbidden
    assert "Kaggle submission packaging" in forbidden
    assert "network/API execution" in forbidden
    assert "legal certification workflows" in forbidden


def test_task_95_outputs_do_not_claim_scores_or_certification() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    allowed_outputs = manifest["plannedAllowedOutputs"]
    forbidden_outputs = manifest["plannedForbiddenOutputs"]

    assert "local technical evidence" in allowed_outputs
    assert "local deterministic JSON" in allowed_outputs
    assert "public-safe manifest fragments" in allowed_outputs

    assert "solver performance proof" in forbidden_outputs
    assert "benchmark proof" in forbidden_outputs
    assert "Kaggle evidence" in forbidden_outputs
    assert "legal certification evidence" in forbidden_outputs
    assert "production runtime evidence" in forbidden_outputs


def test_task_95_usage_contract_has_no_score_and_no_submission_markers() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    contracts = manifest["plannedUsageContracts"]

    assert "usage request identifier" in contracts
    assert "approved diagnostic call-site" in contracts
    assert "payload provenance" in contracts
    assert "audit marker emission" in contracts
    assert "evidence-chain linkage" in contracts
    assert "no-score claim marker" in contracts
    assert "no-submission marker" in contracts
