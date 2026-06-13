import json
from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_3_closure_report import (
    build_milestone_3_closure_report,
    generate_and_validate_milestone_3_closure_report,
    render_milestone_3_closure_report_markdown,
    validate_milestone_3_closure_report,
    write_milestone_3_closure_report_artifacts,
)
from hbce_arc_agi3.milestone_3_dry_run_release_package import build_milestone_3_dry_run_release_package


def test_milestone_3_closure_report_builds_default_report():
    report = build_milestone_3_closure_report()
    validation = validate_milestone_3_closure_report(report)

    assert report.status == "MILESTONE_3_CLOSURE_REPORT_READY"
    assert report.closure_status == "MILESTONE_3_CLOSED_PASS"
    assert report.task_count == 10
    assert report.completed_task_count == 10
    assert report.failed_task_count == 0
    assert report.closure_blocking_issue_count == 0
    assert report.closure_warning_count == 0
    assert report.package_source_artifact_count == 24
    assert report.package_total_artifact_count == 26
    assert report.tests_passed_recorded == 198
    assert report.ready_for_next_milestone is True
    assert report.ready_for_kaggle_submission is False
    assert report.kaggle_submission_sent is False
    assert validation["status"] == "MILESTONE_3_CLOSURE_REPORT_VALID"


def test_milestone_3_closure_report_pipeline_wrapper():
    result = generate_and_validate_milestone_3_closure_report()

    assert result["status"] == "MILESTONE_3_CLOSURE_REPORT_PIPELINE_READY"
    assert result["milestone_3_closure_report"]["status"] == "MILESTONE_3_CLOSURE_REPORT_READY"
    assert result["validation"]["status"] == "MILESTONE_3_CLOSURE_REPORT_VALID"
    assert result["metadata"]["dry_run_only"] is True


def test_milestone_3_closure_report_is_deterministic():
    first = build_milestone_3_closure_report()
    second = build_milestone_3_closure_report()

    assert first.to_dict() == second.to_dict()
    assert first.closure_id == second.closure_id
    assert first.signature == second.signature


def test_milestone_3_closure_report_source_chain_ids_present():
    report = build_milestone_3_closure_report()

    assert report.package_id.startswith("MILESTONE-3-DRY-RUN-RELEASE-PACKAGE-")
    assert report.audit_id.startswith("PUBLIC-READINESS-AUDIT-")
    assert report.candidate_id.startswith("LOCAL-SUBMISSION-CANDIDATE-")
    assert report.report_index_id.startswith("REPORT-INDEX-")
    assert report.batch_id.startswith("BATCH-BENCHMARK-")
    assert report.registry_id.startswith("DATASET-SAMPLE-REGISTRY-")
    assert report.aggregate_id.startswith("MULTI-TASK-OUTCOME-")
    assert report.strategy_index_id.startswith("STRATEGY-SELECTION-INDEX-")
    assert report.failure_taxonomy_report_id.startswith("FAILURE-TAXONOMY-REPORT-")


def test_milestone_3_closure_report_has_ten_ordered_tasks():
    report = build_milestone_3_closure_report()

    assert [task["task_number"] for task in report.closure_tasks] == list(range(1, 11))
    assert all(task["completed"] is True for task in report.closure_tasks)
    assert all(task["pass_status"] == "PASS" for task in report.closure_tasks)
    assert report.closure_tasks[-1]["task_key"] == "MILESTONE_3_REPORT_CLOSURE_V1"


def test_milestone_3_closure_report_rejects_invalid_package():
    package = build_milestone_3_dry_run_release_package().to_dict()
    package["package_status"] = "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_INVALID"

    with pytest.raises(ValueError, match="MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_VALID"):
        build_milestone_3_closure_report(package)


def test_milestone_3_closure_report_metadata_boundary():
    report = build_milestone_3_closure_report()

    assert report.metadata["public_safe"] is True
    assert report.metadata["deterministic"] is True
    assert report.metadata["local_only"] is True
    assert report.metadata["dry_run_only"] is True
    assert report.metadata["external_api_dependency"] is False
    assert report.metadata["contains_api_keys"] is False
    assert report.metadata["private_core_exposure"] is False


def test_milestone_3_closure_report_markdown_contains_boundary():
    report = build_milestone_3_closure_report()
    markdown = render_milestone_3_closure_report_markdown(report)

    assert "# ARC-AGI-3 Milestone #3 Report / Closure v1" in markdown
    assert "local_only=true" in markdown
    assert "dry_run_only=true" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert report.signature in markdown


def test_milestone_3_closure_report_writes_artifacts(tmp_path: Path):
    report = build_milestone_3_closure_report()
    artifacts = write_milestone_3_closure_report_artifacts(report, output_dir=tmp_path / "closure")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["task_count"] == 10
    assert markdown_path.read_text(encoding="utf-8").startswith(
        "# ARC-AGI-3 Milestone #3 Report / Closure v1"
    )


def test_milestone_3_closure_report_validation_rejects_broken_contract():
    validation = validate_milestone_3_closure_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "closure_tasks": [],
        }
    )

    assert validation["status"] == "MILESTONE_3_CLOSURE_REPORT_INVALID"
    assert validation["valid"] is False
