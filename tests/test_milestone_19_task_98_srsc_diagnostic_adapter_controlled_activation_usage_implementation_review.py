"""Milestone #19 Task 98 - SRSC controlled activation usage implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_97 = ROOT / "docs" / "milestone-19-task-97-srsc-diagnostic-adapter-controlled-activation-usage-local-implementation-v1.md"
DOC_TASK_98 = ROOT / "docs" / "milestone-19-task-98-srsc-diagnostic-adapter-controlled-activation-usage-implementation-review-v1.md"
USAGE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage.py"
USAGE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-implementation-review-v1"
    / "task-98-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-implementation-review-v1"
    / "task-98-index.txt"
)


def test_task_98_required_files_exist() -> None:
    assert DOC_TASK_97.exists()
    assert DOC_TASK_98.exists()
    assert USAGE_MODULE.exists()
    assert USAGE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_98_dependency_markers() -> None:
    text = DOC_TASK_97.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_97_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_97_CONTROLLED_USAGE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_97_DIAGNOSTIC_USAGE_ONLY=true" in text
    assert "MILESTONE_19_TASK_97_ACTIVATION_WRAPPER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_97_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_97_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_97_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_97_SOLVER_RUNTIME_BINDING=false" in text


def test_task_98_canonical_markers() -> None:
    text = DOC_TASK_98.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_98_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_98_STATUS=CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_98_MODE=REVIEW_ONLY_NO_USAGE_MODIFICATION" in text
    assert "MILESTONE_19_TASK_98_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_USAGE_ARTIFACT_EMISSION_PLANNING_ONLY" in text
    assert "MILESTONE_19_TASK_98_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_98_CONTROLLED_USAGE_ARTIFACT_EMISSION_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_98_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_98_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_98_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_98_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_98_ARTIFACT_EMISSION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_98_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_98_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_98_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_98_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_98_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_98_FAIL_CLOSED_ACTIVE=true" in text


def test_task_98_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_98_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_USAGE_MODIFICATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_97_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_USAGE_ARTIFACT_EMISSION_PLANNING_ONLY"
    assert manifest["controlledActivationUsageImplementationReviewPerformed"] is True
    assert manifest["controlledUsageArtifactEmissionPlanningAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask98"] is False
    assert manifest["usageModifiedInTask98"] is False
    assert manifest["activationModifiedInTask98"] is False
    assert manifest["adapterModifiedInTask98"] is False
    assert manifest["artifactEmissionImplementedInTask98"] is False
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


def test_task_98_reviewed_usage_layer_is_not_runtime_wiring() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["reviewedModule"] == "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage.py"
    assert "tests/test_srsc_diagnostic_adapter_activation_usage.py" in manifest["reviewedTests"]
    assert manifest["futurePlanningTarget"] == "MILESTONE_19_TASK_99_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_PLANNING_V1"
    assert "usage runtime wiring" in manifest["blockedBindings"]
    assert "solver runtime binding" in manifest["blockedBindings"]
    assert "candidate generator binding" in manifest["blockedBindings"]
    assert "benchmark score binding" in manifest["blockedBindings"]
    assert "Kaggle submission binding" in manifest["blockedBindings"]


def test_task_98_reviewed_usage_contract_is_preserved() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    usage_types = manifest["reviewedUsageTypes"]
    allowed = manifest["reviewedAllowedUsageContexts"]
    forbidden = manifest["reviewedForbiddenUsageContexts"]

    assert "DiagnosticActivationUsageRequest" in usage_types
    assert "DiagnosticActivationUsageResult" in usage_types
    assert "run_controlled_activation_usage" in usage_types
    assert "run_controlled_activation_usage_batch" in usage_types

    assert "local SRSC diagnostic report generation" in allowed
    assert "local milestone evidence packaging" in allowed
    assert "local cross-trace planner evidence attachment" in allowed

    assert "solver runtime execution" in forbidden
    assert "candidate generation" in forbidden
    assert "candidate ranking" in forbidden
    assert "verifier execution" in forbidden
    assert "benchmark execution" in forbidden
    assert "Kaggle submission packaging" in forbidden
