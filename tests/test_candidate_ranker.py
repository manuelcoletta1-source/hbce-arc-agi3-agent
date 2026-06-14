import json
from pathlib import Path

import pytest

from hbce_arc_agi3.candidate_generator import (
    build_candidate_generator_smoke_expected_best_grid,
    build_candidate_generator_smoke_test_input,
    build_candidate_generator_smoke_train_pairs,
    generate_candidates,
)
from hbce_arc_agi3.candidate_ranker import (
    CANDIDATE_TYPE_WEIGHTS,
    candidate_penalties,
    candidate_type_weight,
    evidence_score_from_generation_report,
    penalty_weight,
    rank_candidates,
    rank_one_candidate,
    render_candidate_ranker_markdown,
    run_candidate_ranker_pipeline,
    validate_candidate_ranking_report,
    write_candidate_ranker_artifacts,
)


def test_candidate_type_weight_known_values():
    assert candidate_type_weight("COLOR_SHAPE_COMBINED") == 1.0
    assert candidate_type_weight("SHAPE_TRANSFORM") == 0.82
    assert candidate_type_weight("COLOR_REMAP") == 0.75
    assert candidate_type_weight("IDENTITY_BASELINE") == 0.15


def test_candidate_type_weight_unknown_fallback():
    assert candidate_type_weight("SOME_NEW_CANDIDATE") == 0.25


def test_candidate_penalties_identity_baseline():
    penalties = candidate_penalties(
        {
            "candidate_type": "IDENTITY_BASELINE",
            "candidate_grid": [[0]],
            "applied_transforms": ["identity"],
            "confidence": 0.1,
            "score_hint": 0.1,
        }
    )

    assert "IDENTITY_BASELINE_LOW_PRIORITY" in penalties
    assert "LOW_CONFIDENCE" in penalties
    assert "LOW_SCORE_HINT" in penalties


def test_penalty_weight_is_deterministic():
    assert penalty_weight(["LOW_CONFIDENCE", "LOW_SCORE_HINT"]) == 0.18


def test_evidence_score_from_generation_report_is_full_for_smoke():
    report = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )

    assert evidence_score_from_generation_report(report.to_dict()) == 1.0


def test_rank_one_candidate_ready():
    generation = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )
    candidate = generation.best_candidate
    ranked = rank_one_candidate(candidate, evidence_score=1.0, rank=1)

    assert ranked.status == "RANKED_CANDIDATE_READY"
    assert ranked.rank == 1
    assert ranked.candidate_type == "COLOR_SHAPE_COMBINED"
    assert ranked.score > 0.9
    assert ranked.metadata["candidate_ranker_output"] is True


def test_rank_candidates_report_ready():
    generation = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )
    ranking = rank_candidates(generation)

    assert ranking.status == "CANDIDATE_RANKING_READY"
    assert ranking.candidate_count == 4
    assert ranking.best_candidate.candidate_type == "COLOR_SHAPE_COMBINED"
    assert ranking.evidence_score == 1.0


def test_rank_candidates_scores_descending():
    generation = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )
    ranking = rank_candidates(generation)

    scores = [candidate.score for candidate in ranking.ranked_candidates]

    assert scores == sorted(scores, reverse=True)


def test_rank_candidates_best_grid_matches_expected():
    generation = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )
    ranking = rank_candidates(generation)

    assert ranking.best_candidate.candidate_grid == tuple(
        tuple(row) for row in build_candidate_generator_smoke_expected_best_grid()
    )


def test_rank_candidates_rejects_empty_candidates():
    with pytest.raises(ValueError, match="at least one candidate"):
        rank_candidates(
            {
                "generation_id": "broken",
                "task_id": "broken",
                "candidates": [],
            }
        )


def test_candidate_ranking_validation_passes():
    generation = generate_candidates(
        build_candidate_generator_smoke_train_pairs(),
        build_candidate_generator_smoke_test_input(),
    )
    ranking = rank_candidates(generation)
    validation = validate_candidate_ranking_report(ranking)

    assert validation["status"] == "CANDIDATE_RANKING_VALID"
    assert validation["valid"] is True
    assert validation["candidate_count"] == 4
    assert validation["best_candidate_type"] == "COLOR_SHAPE_COMBINED"


def test_candidate_ranking_validation_rejects_broken_payload():
    validation = validate_candidate_ranking_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "ranked_candidates": [],
            "best_candidate": {},
        }
    )

    assert validation["status"] == "CANDIDATE_RANKING_INVALID"
    assert validation["valid"] is False


def test_candidate_ranker_pipeline_is_valid():
    payload = run_candidate_ranker_pipeline()

    assert payload["status"] == "CANDIDATE_RANKER_PIPELINE_READY"
    assert payload["ranker_status"] == "CANDIDATE_RANKING_READY"
    assert payload["validation_status"] == "CANDIDATE_RANKING_VALID"
    assert payload["candidate_count"] == 4
    assert payload["best_candidate_type"] == "COLOR_SHAPE_COMBINED"
    assert payload["best_candidate_matches_expected_smoke"] is True
    assert payload["metadata"]["uses_candidate_generator_v1"] is True


def test_candidate_ranker_pipeline_is_deterministic():
    first = run_candidate_ranker_pipeline()
    second = run_candidate_ranker_pipeline()

    assert first == second
    assert first["signature"] == second["signature"]


def test_candidate_ranker_markdown_contains_boundary():
    payload = run_candidate_ranker_pipeline()
    markdown = render_candidate_ranker_markdown(payload)

    assert "# ARC-AGI-3 Milestone #4 Task 6" in markdown
    assert "candidate_ranker_output=true" in markdown
    assert "expanded_batch_benchmark_input=true" in markdown
    assert "kaggle_submission_sent=false" in markdown


def test_candidate_ranker_writes_artifacts(tmp_path: Path):
    payload = run_candidate_ranker_pipeline()
    artifacts = write_candidate_ranker_artifacts(payload, output_dir=str(tmp_path / "ranker"))

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["validation_status"] == "CANDIDATE_RANKING_VALID"
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Milestone #4 Task 6")
