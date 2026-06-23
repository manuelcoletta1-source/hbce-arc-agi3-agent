"""Tests for SRSC Diagnostic Adapter Controlled Activation Usage Artifact Emitter."""

from __future__ import annotations

import json

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage import run_controlled_activation_usage
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emitter import (
    ACTIVATION_WRAPPER_MODIFIED,
    ADAPTER_MODIFIED,
    ARTIFACT_EMITTER_REVISION,
    AUTHORIZED_ARTIFACT_FAMILIES,
    BENCHMARK_BINDING,
    BENCHMARK_SCORE_CLAIMED,
    CANDIDATE_GENERATOR_BINDING,
    CANDIDATE_GENERATOR_MODIFIED,
    CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED,
    DIAGNOSTIC_ARTIFACT_EMISSION_ONLY,
    FAIL_CLOSED_ACTIVE,
    FORBIDDEN_ARTIFACT_FAMILIES,
    KAGGLE_SUBMISSION_BINDING,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    PRIVATE_CORE_EXPOSURE,
    RANKER_BINDING,
    RANKER_MODIFIED,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    SOLVER_RUNTIME_BINDING,
    TASK_ID,
    USAGE_LAYER_MODIFIED,
    VERIFIER_BINDING,
    VERIFIER_MODIFIED,
    DiagnosticUsageArtifactEmissionRequest,
    emit_controlled_usage_artifact,
    emit_controlled_usage_artifact_batch,
)


def _valid_payload() -> dict[str, object]:
    return {
        "source_type": "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD",
        "source_path": "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        "diagnostic_scope": "Task 101 controlled artifact emitter",
        "srsc_claim_id": "SRSC-CLAIM-12619C6F83128C07",
        "srsc_gate_decision_id": "SRSC-GATE-447AC5ED3C956D7E",
        "claim_state": "VERIFIED",
        "evidence_state": "PRESENT",
        "evidence_refs": ("src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage.py",),
        "approved_for_record": True,
        "approved_as_verified": True,
        "metadata": {"source": "task-101"},
    }


def _usage_result():
    return run_controlled_activation_usage(
        _valid_payload(),
        usage_context="local SRSC diagnostic report generation",
        call_site="local diagnostic scripts",
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-local-implementation-v1/task-97-manifest.json",
        diagnostic_purpose="Task 101 local artifact emission",
    )


def test_artifact_emission_request_classifies_authorized_family() -> None:
    usage_result = _usage_result()
    request = DiagnosticUsageArtifactEmissionRequest(
        artifact_family="local diagnostic report JSON",
        usage_result=usage_result,
        output_name="task-101-diagnostic-report",
        source_usage_context="local SRSC diagnostic report generation",
        emission_purpose="Task 101 request classification",
    )

    assert request.request_id.startswith("SRSC-DIAG-USAGE-ARTIFACT-EMIT-REQ-")
    assert request.is_authorized_artifact_family is True
    assert request.is_forbidden_artifact_family is False
    assert request.canonical_artifact_family == "local diagnostic report JSON"
    assert request.to_public_dict()["noScoreClaimMarker"] is True
    assert request.to_public_dict()["noSubmissionMarker"] is True


def test_emit_json_artifact_from_usage_result() -> None:
    usage_result = _usage_result()
    result = emit_controlled_usage_artifact(
        usage_result,
        artifact_family="local diagnostic report JSON",
        output_name="task-101-diagnostic-report",
        source_usage_context="local SRSC diagnostic report generation",
        emission_purpose="Task 101 JSON artifact",
    )

    assert result.emitted_count == 1
    assert result.blocked_count == 0
    assert result.emission_ok is True

    artifact = result.artifacts[0]
    assert artifact.artifact_id.startswith("SRSC-DIAG-USAGE-ARTIFACT-")
    assert artifact.filename == "task-101-diagnostic-report.json"
    assert artifact.content_type == "application/json"

    decoded = json.loads(artifact.content)
    assert decoded["artifactFamily"] == "local diagnostic report JSON"
    assert decoded["sourceUsageResultId"] == usage_result.result_id
    assert decoded["acceptedCount"] == 1
    assert decoded["diagnosticArtifactEmissionOnly"] is True
    assert decoded["noScoreClaimMarker"] is True
    assert decoded["noSubmissionMarker"] is True
    assert decoded["legalCertification"] is False


def test_emit_markdown_artifact_from_usage_result() -> None:
    usage_result = _usage_result()
    result = emit_controlled_usage_artifact(
        usage_result,
        artifact_family="local diagnostic report Markdown",
        output_name="task-101-diagnostic-report",
        source_usage_context="local SRSC diagnostic report generation",
        emission_purpose="Task 101 Markdown artifact",
    )

    assert result.emitted_count == 1
    assert result.blocked_count == 0
    artifact = result.artifacts[0]
    assert artifact.filename == "task-101-diagnostic-report.md"
    assert artifact.content_type == "text/markdown"
    assert "# SRSC Diagnostic Usage Artifact" in artifact.content
    assert "Legal certification: False" in artifact.content


def test_emit_text_index_artifact_from_usage_result() -> None:
    usage_result = _usage_result()
    result = emit_controlled_usage_artifact(
        usage_result,
        artifact_family="local deterministic index TXT",
        output_name="task-101-index",
        source_usage_context="local deterministic index emission",
        emission_purpose="Task 101 index artifact",
    )

    assert result.emitted_count == 1
    assert result.blocked_count == 0
    artifact = result.artifacts[0]
    assert artifact.filename == "task-101-index.txt"
    assert artifact.content_type == "text/plain"
    assert "SRSC DIAGNOSTIC USAGE ARTIFACT INDEX" in artifact.content
    assert "legalCertification=false" in artifact.content


def test_emitter_blocks_forbidden_artifact_family() -> None:
    result = emit_controlled_usage_artifact(
        _usage_result(),
        artifact_family="benchmark proof",
        output_name="forbidden-benchmark-proof",
        source_usage_context="local SRSC diagnostic report generation",
        emission_purpose="Forbidden benchmark artifact",
    )

    assert result.emitted_count == 0
    assert result.blocked_count == 1
    assert result.blocked_requests[0].reason == "FORBIDDEN_ARTIFACT_FAMILY"
    assert result.emission_ok is True


def test_emitter_blocks_unknown_artifact_family() -> None:
    result = emit_controlled_usage_artifact(
        _usage_result(),
        artifact_family="mystery oracle scroll",
        output_name="unknown-artifact",
        source_usage_context="local SRSC diagnostic report generation",
        emission_purpose="Unknown artifact family",
    )

    assert result.emitted_count == 0
    assert result.blocked_count == 1
    assert result.blocked_requests[0].reason == "UNKNOWN_ARTIFACT_FAMILY"
    assert result.emission_ok is True


def test_emitter_batch_mixes_allowed_and_blocked_families() -> None:
    result = emit_controlled_usage_artifact_batch(
        _usage_result(),
        artifact_families=[
            "local diagnostic report JSON",
            "local manifest fragment JSON",
            "score report",
            "local deterministic index TXT",
        ],
        output_name_prefix="task-101-artifact",
        source_usage_context="local milestone evidence package emission",
        emission_purpose="Task 101 batch artifact emission",
    )

    assert result.emitted_count == 3
    assert result.blocked_count == 1
    assert result.blocked_requests[0].reason == "FORBIDDEN_ARTIFACT_FAMILY"
    assert result.emission_ok is True
    assert [artifact.content_type for artifact in result.artifacts] == [
        "application/json",
        "application/json",
        "text/plain",
    ]


def test_emission_result_json_is_deterministic_and_serializable() -> None:
    result = emit_controlled_usage_artifact(
        _usage_result(),
        artifact_family="local public-safe audit summary JSON",
        output_name="task-101-public-safe-audit-summary",
        source_usage_context="local public-safe audit summary emission",
        emission_purpose="Task 101 audit summary",
    )

    encoded = result.to_json()
    decoded = json.loads(encoded)

    assert decoded["resultId"] == result.result_id
    assert decoded["artifactEmitterRevision"] == ARTIFACT_EMITTER_REVISION
    assert decoded["emittedCount"] == 1
    assert decoded["blockedCount"] == 0
    assert decoded["controlledArtifactEmissionImplemented"] is True
    assert decoded["diagnosticArtifactEmissionOnly"] is True
    assert decoded["noScoreClaimMarker"] is True
    assert decoded["noSubmissionMarker"] is True


def test_artifact_emitter_boundary_flags_remain_closed() -> None:
    result = emit_controlled_usage_artifact(
        _usage_result(),
        artifact_family="local diagnostic report JSON",
        output_name="task-101-boundary",
        source_usage_context="local SRSC diagnostic report generation",
        emission_purpose="Task 101 boundary check",
    )
    payload = result.to_public_dict()

    assert CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED is True
    assert DIAGNOSTIC_ARTIFACT_EMISSION_ONLY is True
    assert USAGE_LAYER_MODIFIED is False
    assert ACTIVATION_WRAPPER_MODIFIED is False
    assert ADAPTER_MODIFIED is False
    assert RUNTIME_SOLVER_MODIFIED is False
    assert RUNTIME_WIRING_ALLOWED is False
    assert SOLVER_RUNTIME_BINDING is False
    assert CANDIDATE_GENERATOR_MODIFIED is False
    assert CANDIDATE_GENERATOR_BINDING is False
    assert RANKER_MODIFIED is False
    assert RANKER_BINDING is False
    assert VERIFIER_MODIFIED is False
    assert VERIFIER_BINDING is False
    assert BENCHMARK_SCORE_CLAIMED is False
    assert BENCHMARK_BINDING is False
    assert KAGGLE_SUBMISSION_SENT is False
    assert KAGGLE_SUBMISSION_BINDING is False
    assert PRIVATE_CORE_EXPOSURE is False
    assert LEGAL_CERTIFICATION is False
    assert FAIL_CLOSED_ACTIVE is True

    assert payload["controlledArtifactEmissionImplemented"] is True
    assert payload["diagnosticArtifactEmissionOnly"] is True
    assert payload["usageLayerModified"] is False
    assert payload["activationWrapperModified"] is False
    assert payload["adapterModified"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["solverRuntimeBinding"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True


def test_artifact_family_registry_is_explicit() -> None:
    assert "local diagnostic report JSON" in AUTHORIZED_ARTIFACT_FAMILIES
    assert "local diagnostic report Markdown" in AUTHORIZED_ARTIFACT_FAMILIES
    assert "local milestone evidence package JSON" in AUTHORIZED_ARTIFACT_FAMILIES
    assert "local public-safe audit summary JSON" in AUTHORIZED_ARTIFACT_FAMILIES
    assert "local blocked usage report JSON" in AUTHORIZED_ARTIFACT_FAMILIES
    assert "local cross-trace planner attachment JSON" in AUTHORIZED_ARTIFACT_FAMILIES
    assert "local manifest fragment JSON" in AUTHORIZED_ARTIFACT_FAMILIES
    assert "local deterministic index TXT" in AUTHORIZED_ARTIFACT_FAMILIES

    assert "solver performance proof" in FORBIDDEN_ARTIFACT_FAMILIES
    assert "benchmark proof" in FORBIDDEN_ARTIFACT_FAMILIES
    assert "Kaggle evidence" in FORBIDDEN_ARTIFACT_FAMILIES
    assert "legal certification evidence" in FORBIDDEN_ARTIFACT_FAMILIES
    assert "score report" in FORBIDDEN_ARTIFACT_FAMILIES


def test_artifact_emitter_task_markers() -> None:
    assert TASK_ID == "MILESTONE_19_TASK_101_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_LOCAL_IMPLEMENTATION_V1"
    assert ARTIFACT_EMITTER_REVISION == "SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_USAGE_ARTIFACT_EMITTER_LOCAL_STANDALONE_V1"
