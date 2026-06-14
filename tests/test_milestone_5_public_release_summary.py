from pathlib import Path

from hbce_arc_agi3.milestone_5_public_release_summary import (
    BASELINE_COMMIT,
    PIPELINE_STATUS,
    PUBLIC_SUMMARY_GATES,
    PUBLIC_SUMMARY_ISSUES,
    RELEASE_SCOPE,
    SUMMARY_STATUS,
    VALIDATION_STATUS,
    build_milestone_5_public_release_summary,
    render_public_readme_snippet,
    render_public_release_manifest,
    render_public_release_summary_markdown,
    run_milestone_5_public_release_summary_pipeline,
    validate_milestone_5_public_release_summary,
    write_public_release_summary_artifacts,
)


def test_public_release_summary_ready():
    summary = build_milestone_5_public_release_summary()

    assert summary["status"] == SUMMARY_STATUS
    assert summary["baseline_commit"] == BASELINE_COMMIT
    assert summary["release_scope"] == RELEASE_SCOPE
    assert summary["closed_task_count"] == 9
    assert summary["ready_task_count"] == 9
    assert summary["summary_gate_count"] == len(PUBLIC_SUMMARY_GATES)
    assert summary["passed_gate_count"] == len(PUBLIC_SUMMARY_GATES)
    assert summary["summary_issue_count"] == 0
    assert summary["warning_count"] == 0
    assert summary["public_release_summary_ready"] is True
    assert summary["ready_for_real_kaggle_submission"] is False
    assert summary["kaggle_submission_sent"] is False


def test_public_release_summary_gates_pass():
    summary = build_milestone_5_public_release_summary()

    assert [gate["name"] for gate in summary["summary_gates"]] == list(PUBLIC_SUMMARY_GATES)
    assert all(gate["passed"] is True for gate in summary["summary_gates"])
    assert all(gate["severity"] == "PASS" for gate in summary["summary_gates"])


def test_public_release_summary_issues_inactive():
    summary = build_milestone_5_public_release_summary()

    assert [issue["name"] for issue in summary["summary_issues"]] == list(PUBLIC_SUMMARY_ISSUES)
    assert all(issue["active"] is False for issue in summary["summary_issues"])
    assert all(issue["severity"] == "BLOCKING" for issue in summary["summary_issues"])


def test_public_release_summary_claims_are_safe():
    summary = build_milestone_5_public_release_summary()
    claims = summary["public_claims"]

    assert claims["submission_preparation_closed"] is True
    assert claims["real_kaggle_submission_created"] is False
    assert claims["kaggle_submission_sent"] is False
    assert claims["external_api_dependency"] is False
    assert claims["private_core_exposure"] is False
    assert claims["legal_certification"] is False


def test_public_release_summary_boundary_is_intact():
    summary = build_milestone_5_public_release_summary()
    boundary = summary["boundary"]

    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_public_release_summary_validation_passes():
    summary = build_milestone_5_public_release_summary()
    validation = validate_milestone_5_public_release_summary(summary)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_public_release_summary_pipeline_ready():
    payload = run_milestone_5_public_release_summary_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["summary_status"] == SUMMARY_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["closed_task_count"] == 9
    assert payload["ready_task_count"] == 9
    assert payload["summary_gate_count"] == len(PUBLIC_SUMMARY_GATES)
    assert payload["passed_gate_count"] == len(PUBLIC_SUMMARY_GATES)
    assert payload["summary_issue_count"] == 0
    assert payload["warning_count"] == 0
    assert payload["public_release_summary_ready"] is True
    assert payload["ready_for_real_kaggle_submission"] is False
    assert payload["kaggle_submission_sent"] is False


def test_public_release_summary_markdown_contains_markers():
    summary = build_milestone_5_public_release_summary()
    markdown = render_public_release_summary_markdown(summary)

    assert "ARC_AGI3_MILESTONE_5_PUBLIC_RELEASE_SUMMARY_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_RELEASE_SUMMARY_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_CLOSED_TASK_COUNT=9" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_TASK_COUNT=9" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUMMARY_GATE_COUNT=18" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUMMARY_ISSUE_COUNT=0" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_public_release_manifest_contains_boundary():
    summary = build_milestone_5_public_release_summary()
    manifest = render_public_release_manifest(summary)

    assert "ARC AGI3 MILESTONE 5 PUBLIC RELEASE SUMMARY MANIFEST v1" in manifest
    assert "closed_task_count=9" in manifest
    assert "ready_task_count=9" in manifest
    assert "summary_issue_count=0" in manifest
    assert "public_release_summary_ready=True" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_public_readme_snippet_is_clean():
    summary = build_milestone_5_public_release_summary()
    snippet = render_public_readme_snippet(summary)

    assert "Milestone #5 is closed as local-only submission preparation." in snippet
    assert "real Kaggle submission: false" in snippet
    assert "Kaggle upload: false" in snippet
    assert "external API dependency: false" in snippet
    assert "private core exposure: false" in snippet
    assert "legal certification: false" in snippet


def test_public_release_summary_writes_artifacts(tmp_path: Path):
    summary = build_milestone_5_public_release_summary()
    paths = write_public_release_summary_artifacts(summary, output_dir=str(tmp_path))

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])
    index_path = Path(paths["index_path"])
    readme_snippet_path = Path(paths["readme_snippet_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()
    assert readme_snippet_path.exists()
    assert "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_RELEASE_SUMMARY_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 MILESTONE 5 PUBLIC RELEASE SUMMARY MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
    assert "PUBLIC_RELEASE_SUMMARY_ONLY_NO_SUBMISSION" in index_path.read_text(encoding="utf-8")
    assert "Milestone #5 is closed as local-only submission preparation." in readme_snippet_path.read_text(encoding="utf-8")
