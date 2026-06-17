"""Local-only bridge between generated candidates and diagnostic fixtures."""

from __future__ import annotations

from typing import Any, Iterable


def build_candidate_fixture_matrix(
    runtime_candidates: Iterable[dict[str, Any]],
    diagnostic_fixtures: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build deterministic candidate/fixture matrix rows.

    The bridge is diagnostic-only. It does not execute candidates against
    Kaggle, does not upload, and does not claim official scores.
    """

    candidates = [candidate for candidate in runtime_candidates if isinstance(candidate, dict)]
    fixtures = [fixture for fixture in diagnostic_fixtures if isinstance(fixture, dict)]

    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        for fixture in fixtures:
            rows.append(
                {
                    "candidate_id": candidate.get("candidate_id", "UNKNOWN_CANDIDATE"),
                    "candidate_family": candidate.get("family", "UNKNOWN_FAMILY"),
                    "candidate_operation": candidate.get("operation", "UNKNOWN_OPERATION"),
                    "fixture_id": fixture.get("fixture_id", "UNKNOWN_FIXTURE"),
                    "fixture_family": fixture.get("family", "UNKNOWN_FIXTURE_FAMILY"),
                    "diagnostic_only": True,
                    "runtime_execution_performed": False,
                    "real_evaluation_performed": False,
                }
            )

    return sorted(
        rows,
        key=lambda row: (
            str(row["fixture_id"]),
            str(row["candidate_family"]),
            str(row["candidate_operation"]),
            str(row["candidate_id"]),
        ),
    )
