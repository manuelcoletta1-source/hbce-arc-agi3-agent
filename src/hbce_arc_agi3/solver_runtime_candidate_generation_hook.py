"""Controlled local solver runtime candidate generation hook.

This hook prepares candidate payloads for a future solver path, but it does
not activate runtime solving and does not perform real evaluation.
"""

from __future__ import annotations

from typing import Any, Iterable

from hbce_arc_agi3.program_synthesis_candidate_fixture_bridge import build_candidate_fixture_matrix
from hbce_arc_agi3.program_synthesis_candidate_generator_runtime_adapter import normalize_generated_candidates


def build_controlled_candidate_generation_hook_payload(
    generated_candidates: Iterable[dict[str, Any]],
    diagnostic_fixtures: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    runtime_candidates = normalize_generated_candidates(generated_candidates)
    fixture_matrix = build_candidate_fixture_matrix(runtime_candidates, diagnostic_fixtures)

    return {
        "hook_revision": "CONTROLLED_RUNTIME_CANDIDATE_GENERATION_HOOK_V1",
        "hook_mode": "LOCAL_ONLY_DIAGNOSTIC_CONTROLLED_IMPLEMENTATION",
        "runtime_candidates": runtime_candidates,
        "runtime_candidate_count": len(runtime_candidates),
        "candidate_fixture_matrix": fixture_matrix,
        "candidate_fixture_matrix_count": len(fixture_matrix),
        "controlled_implementation_performed": True,
        "runtime_activation_performed": False,
        "runtime_execution_performed": False,
        "real_evaluation_performed": False,
        "real_submission_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_upload_performed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
