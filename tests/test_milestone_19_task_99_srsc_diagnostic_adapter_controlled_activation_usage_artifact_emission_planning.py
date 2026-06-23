"""Milestone #19 Task 99 - SRSC controlled usage artifact emission planning validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_98 = ROOT / "docs" / "milestone-19-task-98-srsc-diagnostic-adapter-controlled-activation-usage-implementation-review-v1.md"
DOC_TASK_99 = ROOT / "docs" / "milestone-19-task-99-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-planning-v1.md"
USAGE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage.py"
USAGE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-planning-v1"
    / "task-99-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-planning-v1"
    / "task-99-index.txt"
)


def test_task_99_required_files_exist() -> None:
    assert DOC_TASK_98.exists()
    assert DOC_TASK_99.exists()
    assert USAGE_MODULE.exists()
    assert USAGE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_99_dependency_markers() -> None:
    text = DOC_TASK_98.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_98_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_98_CONTROLLED_USAGE_ARTIFACT_EMISSION_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_98_ARTIFACT_EMISSION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_98_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_98_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_98_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_98_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_98_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_98_SOLVER_RUNTIME_BINDING=false" in text


def test_task_99_canonical_markers() -> None:
    text = DOC_TASK_99.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_99_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_99_STATUS=CONTROLLED_USAGE_ARTIFACT_EMISSION_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_99_MODE=PLANNING_ONLY_NO_ARTIFACT_EMISSION_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_99_DECISION=PLAN_CONTROLLED_USAGE_ARTIFACT_EMISSION_ONLY" in text
    assert "MILESTONE_19_TASK_99_CONTROLLED_USAGE_ARTIFACT_EMISSION_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_99_CONTROLLED_USAGE_ARTIFACT_EMISSION_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_99_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_99_ARTIFACT_EMISSION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_99_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_99_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_99_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_99_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_99_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_99_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_99_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_99_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_99_FAIL_CLOSED_ACTIVE=true" in text


def test_task_99_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_99_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_PLANNING_V1"
    assert manifest["status"] == "CONTROLLED_USAGE_ARTIFACT_EMISSION_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_ARTIFACT_EMISSION_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_98_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_V1"
    assert manifest["decision"] == "PLAN_CONTROLLED_USAGE_ARTIFACT_EMISSION_ONLY"
    assert manifest["controlledUsageArtifactEmissionPlanningPerformed"] is True
    assert manifest["controlledUsageArtifactEmissionImplementationAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask99"] is False
    assert manifest["artifactEmissionImplementedInTask99"] is False
    assert manifest["usageModifiedInTask99"] is False
    assert manifest["activationModifiedInTask99"] is False
    assert manifest["adapterModifiedInTask99"] is False
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


def test_task_99_artifact_families_are_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    planned = manifest["plannedArtifactFamilies"]
    forbidden = manifest["forbiddenArtifactFamilies"]

    assert "local diagnostic report JSON" in planned
    assert "local diagnostic report Markdown" in planned
    assert "local milestone evidence package JSON" in planned
    assert "local public-safe audit summary JSON" in planned
    assert "local blocked usage report JSON" in planned
    assert "local cross-trace planner attachment JSON" in planned
    assert "local deterministic index TXT" in planned

    assert "solver performance proof" in forbidden
    assert "benchmark proof" in forbidden
    assert "Kaggle evidence" in forbidden
    assert "production runtime evidence" in forbidden
    assert "legal certification evidence" in forbidden
    assert "submission package" in forbidden
    assert "score report" in forbidden
    assert "private core evidence" in forbidden


def test_task_99_future_module_is_planning_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["plannedFutureModules"] == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emitter.py",
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emitter.py",
    ]
    assert "DiagnosticUsageArtifactEmissionRequest" in manifest["plannedFutureTypes"]
    assert "DiagnosticUsageArtifact" in manifest["plannedFutureTypes"]
    assert "DiagnosticUsageArtifactEmissionResult" in manifest["plannedFutureTypes"]
    assert "emit_controlled_usage_artifact" in manifest["plannedFutureTypes"]
    assert "emit_controlled_usage_artifact_batch" in manifest["plannedFutureTypes"]
    assert manifest["artifactEmissionImplementedInTask99"] is False


def test_task_99_forbidden_emission_contexts_block_score_and_submission_claims() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    forbidden = manifest["forbiddenEmissionContexts"]
    blocked = manifest["blockedBindings"]

    assert "solver performance emission" in forbidden
    assert "benchmark evidence emission" in forbidden
    assert "public score emission" in forbidden
    assert "private score emission" in forbidden
    assert "Kaggle submission package emission" in forbidden
    assert "legal certification emission" in forbidden
    assert "network/API evidence emission" in forbidden

    assert "artifact emission implementation in Task 99" in blocked
    assert "usage layer modification in Task 99" in blocked
    assert "solver runtime binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
