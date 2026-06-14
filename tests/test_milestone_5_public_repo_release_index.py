from pathlib import Path

from hbce_arc_agi3.milestone_5_public_repo_release_index import (
    INDEXED_PUBLIC_ARTIFACTS,
    INDEX_STATUS,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_indexed_artifacts,
    build_public_repo_release_index,
    render_public_repo_release_index_markdown,
    run_public_repo_release_index_pipeline,
    validate_public_repo_release_index,
    write_public_repo_release_index_artifacts,
)


def test_public_repo_release_index_ready():
    index = build_public_repo_release_index()

    assert index.status == INDEX_STATUS
    assert index.baseline_commit.startswith("2f02f5d")
    assert index.indexed_artifact_count == len(INDEXED_PUBLIC_ARTIFACTS)
    assert index.ready_for_public_index_release is True
    assert index.kaggle_submission_sent is False
    assert all(artifact.present for artifact in index.indexed_artifacts)


def test_public_repo_release_index_validation_passes():
    index = build_public_repo_release_index()
    validation = validate_public_repo_release_index(index)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_public_repo_release_index_pipeline_ready():
    payload = run_public_repo_release_index_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["index_status"] == INDEX_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["indexed_artifact_count"] == len(INDEXED_PUBLIC_ARTIFACTS)
    assert payload["ready_for_public_index_release"] is True
    assert payload["kaggle_submission_sent"] is False


def test_public_repo_release_index_markdown_contains_markers():
    index = build_public_repo_release_index()
    markdown = render_public_repo_release_index_markdown(index)

    assert "ARC_AGI3_MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_INDEX_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_BASELINE_AUDIT_COMMIT=2f02f5d" in markdown
    assert "ARC_AGI3_MILESTONE_5_INDEXED_ARTIFACTS_PRESENT=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_PREPARATION=true" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_public_repo_release_index_writes_artifacts(tmp_path: Path):
    index = build_public_repo_release_index()
    paths = write_public_repo_release_index_artifacts(
        index,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_V1_READY=true" in markdown_path.read_text(encoding="utf-8")


def test_indexed_public_artifacts_exist():
    artifacts = build_indexed_artifacts()
    missing = [artifact.path for artifact in artifacts if not artifact.present]

    assert missing == []


def test_public_repo_release_index_sections_are_stable():
    index = build_public_repo_release_index()

    assert index.release_sections == (
        "repository_root",
        "milestone_4_solver_engine_closure",
        "milestone_5_public_readiness",
        "candidate_generation_and_ranking",
        "benchmark_and_failure_loop",
        "public_boundary",
        "next_submission_preparation_steps",
    )
