import json
from pathlib import Path

import pytest

from hbce_arc_agi3.local_submission_candidate_builder import (
    build_local_submission_candidate_package,
    build_local_submission_candidate_task,
    generate_and_validate_local_submission_candidate_package,
    render_local_submission_candidate_markdown,
    validate_local_submission_candidate_package,
    write_local_submission_candidate_artifacts,
)
from hbce_arc_agi3.multi_task_outcome_aggregator import aggregate_multi_task_outcomes
from hbce_arc_agi3.failure_taxonomy import build_failure_taxonomy_report


def test_local_submission_candidate_builds_default_package():
    package = build_local_submission_candidate_package()
    validation = validate_local_submission_candidate_package(package)

    assert package.status == "LOCAL_SUBMISSION_CANDIDATE_BUILDER_READY"
    assert package.candidate_status == "LOCAL_SUBMISSION_CANDIDATE_VALID"
    assert package.submission_mode == "LOCAL_DRY_RUN_ONLY"
    assert package.task_count == 3
    assert package.eligible_task_count == 2
    assert package.blocked_task_count == 1
    assert package.remediation_required_count == 1
    assert package.ready_for_public_readiness_audit is True
    assert package.ready_for_kaggle_submission is False
    assert package.kaggle_submission_sent is False
    assert validation["status"] == "LOCAL_SUBMISSION_CANDIDATE_VALID"


def test_local_submission_candidate_pipeline_wrapper():
    result = generate_and_validate_local_submission_candidate_package()

    assert result["status"] == "LOCAL_SUBMISSION_CANDIDATE_PIPELINE_READY"
    assert result["local_submission_candidate"]["status"] == "LOCAL_SUBMISSION_CANDIDATE_BUILDER_READY"
    assert result["validation"]["status"] == "LOCAL_SUBMISSION_CANDIDATE_VALID"
    assert result["metadata"]["local_only"] is True
    assert result["metadata"]["dry_run_only"] is True


def test_local_submission_candidate_is_deterministic():
    first = build_local_submission_candidate_package()
    second = build_local_submission_candidate_package()

    assert first.to_dict() == second.to_dict()
    assert first.candidate_id == second.candidate_id
    assert first.signature == second.signature


def test_local_submission_candidate_task_classifies_exact_match_as_eligible():
    aggregate = aggregate_multi_task_outcomes()
    taxonomy = build_failure_taxonomy_report(aggregate)
    exact_record = next(record for record in aggregate.outcome_records if record["outcome_status"] == "OUTCOME_MATCH")
    taxonomy_entry = next(
        entry for entry in taxonomy.taxonomy_entries if entry["task_id"] == exact_record["task_id"]
    )

    task = build_local_submission_candidate_task(
        exact_record,
        taxonomy_entry,
        selected_strategy_id="STRATEGY-IDENTITY-BASELINE-v1",
        selected_strategy_name="identity_baseline_v1",
    )

    assert task.eligible_for_submission is True
    assert task.remediation_required is False
    assert task.local_output_status == "LOCAL_TASK_OUTPUT_ACCEPTED_BASELINE"


def test_local_submission_candidate_task_classifies_partial_as_blocked():
    aggregate = aggregate_multi_task_outcomes()
    taxonomy = build_failure_taxonomy_report(aggregate)
    partial_record = next(record for record in aggregate.outcome_records if record["outcome_status"] == "OUTCOME_PARTIAL")
    taxonomy_entry = next(
        entry for entry in taxonomy.taxonomy_entries if entry["task_id"] == partial_record["task_id"]
    )

    task = build_local_submission_candidate_task(
        partial_record,
        taxonomy_entry,
        selected_strategy_id="STRATEGY-IDENTITY-BASELINE-v1",
        selected_strategy_name="identity_baseline_v1",
    )

    assert task.eligible_for_submission is False
    assert task.remediation_required is True
    assert task.local_output_status == "LOCAL_TASK_OUTPUT_PARTIAL_REPAIR_REQUIRED"


def test_local_submission_candidate_payload_is_local_only():
    package = build_local_submission_candidate_package()
    payload = package.local_submission_payload

    assert payload["submission_mode"] == "LOCAL_DRY_RUN_ONLY"
    assert payload["kaggle_submission_sent"] is False
    assert payload["ready_for_kaggle_submission"] is False
    assert len(payload["tasks"]) == 3


def test_local_submission_candidate_rejects_invalid_report_index_payload():
    with pytest.raises(ValueError, match="REPORT_INDEX_VALID"):
        build_local_submission_candidate_package({"status": "BROKEN", "metadata": {}, "report_entries": []})


def test_local_submission_candidate_markdown_contains_boundary():
    package = build_local_submission_candidate_package()
    markdown = render_local_submission_candidate_markdown(package)

    assert "# ARC-AGI-3 Local Submission Candidate Builder v1" in markdown
    assert "local_only=true" in markdown
    assert "dry_run_only=true" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert package.signature in markdown


def test_local_submission_candidate_writes_artifacts(tmp_path: Path):
    package = build_local_submission_candidate_package()
    artifacts = write_local_submission_candidate_artifacts(package, output_dir=tmp_path / "candidate")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["task_count"] == 3
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Local Submission Candidate Builder v1")


def test_local_submission_candidate_validation_rejects_broken_contract():
    validation = validate_local_submission_candidate_package(
        {
            "status": "BROKEN",
            "metadata": {},
            "local_candidate_tasks": [],
        }
    )

    assert validation["status"] == "LOCAL_SUBMISSION_CANDIDATE_INVALID"
    assert validation["valid"] is False
