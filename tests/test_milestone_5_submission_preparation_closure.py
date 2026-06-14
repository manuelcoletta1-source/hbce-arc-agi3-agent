from pathlib import Path

from hbce_arc_agi3.milestone_5_submission_preparation_closure import (
    CLOSURE_GATES,
    CLOSURE_ISSUES,
    CLOSURE_STATUS,
    PIPELINE_STATUS,
    TASK_ARTIFACT_SPECS,
    TASK_COMMIT_CHAIN,
    VALIDATION_STATUS,
    build_closure_task_statuses,
    build_milestone_5_submission_preparation_closure,
    render_milestone_5_submission_preparation_closure_manifest,
    render_milestone_5_submission_preparation_closure_markdown,
    run_milestone_5_submission_preparation_closure_pipeline,
    validate_milestone_5_submission_preparation_closure,
    write_milestone_5_submission_preparation_closure_artifacts,
)


def test_milestone_5_submission_preparation_closure_ready():
    closure = build_milestone_5_submission_preparation_closure()

    assert closure.status == CLOSURE_STATUS
    assert closure.baseline_commit.startswith("b632fc3")
    assert closure.closed_task_count == len(TASK_ARTIFACT_SPECS)
    assert closure.ready_task_count == len(TASK_ARTIFACT_SPECS)
    assert closure.closure_gate_count == len(CLOSURE_GATES)
    assert closure.passed_gate_count == len(CLOSURE_GATES)
    assert closure.closure_issue_count == 0
    assert closure.warning_count == 0
    assert closure.submission_preparation_closed is True
    assert closure.ready_for_public_release_summary is True
    assert closure.ready_for_real_kaggle_submission is False
    assert closure.kaggle_submission_sent is False


def test_closure_task_statuses_are_ready():
    statuses = build_closure_task_statuses()

    assert len(statuses) == len(TASK_ARTIFACT_SPECS)
    assert all(status.present for status in statuses)
    assert all(status.ready for status in statuses)
    assert all(status.sha256_16 != "MISSING_HASH" for status in statuses)


def test_closure_task_commit_chain_is_canonical():
    closure = build_milestone_5_submission_preparation_closure()

    assert tuple(item.commit for item in closure.task_statuses) == TASK_COMMIT_CHAIN
    assert closure.closure_index["commit_chain"] == list(TASK_COMMIT_CHAIN)


def test_closure_gates_pass():
    closure = build_milestone_5_submission_preparation_closure()

    assert [gate.name for gate in closure.closure_gates] == list(CLOSURE_GATES)
    assert all(gate.passed for gate in closure.closure_gates)
    assert all(gate.severity == "PASS" for gate in closure.closure_gates)


def test_closure_issues_inactive():
    closure = build_milestone_5_submission_preparation_closure()

    assert [issue.name for issue in closure.closure_issues] == list(CLOSURE_ISSUES)
    assert all(issue.active is False for issue in closure.closure_issues)
    assert all(issue.severity == "BLOCKING" for issue in closure.closure_issues)


def test_closure_boundary_is_intact():
    closure = build_milestone_5_submission_preparation_closure()
    boundary = closure.boundary

    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_closure_index_is_safe():
    closure = build_milestone_5_submission_preparation_closure()
    index = closure.closure_index

    assert index["task_count"] == len(TASK_ARTIFACT_SPECS)
    assert index["ready_task_count"] == len(TASK_ARTIFACT_SPECS)
    assert index["submission_preparation_closed"] is True
    assert index["real_kaggle_submission_created"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["external_api_dependency"] is False
    assert index["private_core_exposure"] is False
    assert index["legal_certification"] is False


def test_closure_validation_passes():
    closure = build_milestone_5_submission_preparation_closure()
    validation = validate_milestone_5_submission_preparation_closure(closure)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_closure_pipeline_ready():
    payload = run_milestone_5_submission_preparation_closure_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["closure_status"] == CLOSURE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["closed_task_count"] == len(TASK_ARTIFACT_SPECS)
    assert payload["ready_task_count"] == len(TASK_ARTIFACT_SPECS)
    assert payload["closure_gate_count"] == len(CLOSURE_GATES)
    assert payload["passed_gate_count"] == len(CLOSURE_GATES)
    assert payload["closure_issue_count"] == 0
    assert payload["warning_count"] == 0
    assert payload["submission_preparation_closed"] is True
    assert payload["ready_for_real_kaggle_submission"] is False
    assert payload["kaggle_submission_sent"] is False


def test_closure_markdown_contains_markers():
    closure = build_milestone_5_submission_preparation_closure()
    markdown = render_milestone_5_submission_preparation_closure_markdown(closure)

    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_CLOSED_TASK_COUNT=9" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_TASK_COUNT=9" in markdown
    assert "ARC_AGI3_MILESTONE_5_CLOSURE_GATE_COUNT=20" in markdown
    assert "ARC_AGI3_MILESTONE_5_CLOSURE_ISSUE_COUNT=0" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_closure_manifest_contains_boundary():
    closure = build_milestone_5_submission_preparation_closure()
    manifest = render_milestone_5_submission_preparation_closure_manifest(closure)

    assert "ARC AGI3 MILESTONE 5 SUBMISSION PREPARATION CLOSURE MANIFEST v1" in manifest
    assert "closed_task_count=9" in manifest
    assert "ready_task_count=9" in manifest
    assert "closure_issue_count=0" in manifest
    assert "submission_preparation_closed=True" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_closure_writes_artifacts(tmp_path: Path):
    closure = build_milestone_5_submission_preparation_closure()
    paths = write_milestone_5_submission_preparation_closure_artifacts(
        closure,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])
    index_path = Path(paths["index_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()
    assert "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 MILESTONE 5 SUBMISSION PREPARATION CLOSURE MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
    assert "SUBMISSION_PREPARATION_CLOSURE" in index_path.read_text(encoding="utf-8")
