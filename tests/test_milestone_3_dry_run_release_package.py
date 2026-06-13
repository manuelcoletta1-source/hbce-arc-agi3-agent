import json
from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_3_dry_run_release_package import (
    build_milestone_3_dry_run_release_package,
    generate_and_validate_milestone_3_dry_run_release_package,
    render_milestone_3_dry_run_release_package_markdown,
    validate_milestone_3_dry_run_release_package,
    write_milestone_3_dry_run_release_package_artifacts,
)
from hbce_arc_agi3.public_readiness_audit import build_public_readiness_audit_report


def test_dry_run_release_package_builds_default_package():
    package = build_milestone_3_dry_run_release_package()
    validation = validate_milestone_3_dry_run_release_package(package)

    assert package.status == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_READY"
    assert package.package_status == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_VALID"
    assert package.release_mode == "MILESTONE_3_LOCAL_DRY_RUN_RELEASE_PACKAGE_ONLY"
    assert package.submission_mode == "LOCAL_DRY_RUN_ONLY"
    assert package.source_artifact_count == 24
    assert package.present_source_artifact_count == 24
    assert package.missing_source_artifact_count == 0
    assert package.generated_package_artifact_count == 2
    assert package.total_package_artifact_count == 26
    assert package.ready_for_milestone_3_closure is True
    assert package.ready_for_kaggle_submission is False
    assert package.kaggle_submission_sent is False
    assert validation["status"] == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_VALID"


def test_dry_run_release_package_pipeline_wrapper():
    result = generate_and_validate_milestone_3_dry_run_release_package()

    assert result["status"] == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_PIPELINE_READY"
    assert result["dry_run_release_package"]["status"] == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_READY"
    assert result["validation"]["status"] == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_VALID"
    assert result["metadata"]["dry_run_only"] is True


def test_dry_run_release_package_is_deterministic():
    first = build_milestone_3_dry_run_release_package()
    second = build_milestone_3_dry_run_release_package()

    assert first.to_dict() == second.to_dict()
    assert first.package_id == second.package_id
    assert first.signature == second.signature


def test_dry_run_release_package_source_chain_ids_are_present():
    package = build_milestone_3_dry_run_release_package()

    assert package.audit_id.startswith("PUBLIC-READINESS-AUDIT-")
    assert package.candidate_id.startswith("LOCAL-SUBMISSION-CANDIDATE-")
    assert package.report_index_id.startswith("REPORT-INDEX-")
    assert package.batch_id.startswith("BATCH-BENCHMARK-")
    assert package.registry_id.startswith("DATASET-SAMPLE-REGISTRY-")
    assert package.aggregate_id.startswith("MULTI-TASK-OUTCOME-")
    assert package.strategy_index_id.startswith("STRATEGY-SELECTION-INDEX-")
    assert package.failure_taxonomy_report_id.startswith("FAILURE-TAXONOMY-REPORT-")


def test_dry_run_release_package_rejects_invalid_audit():
    audit = build_public_readiness_audit_report().to_dict()
    audit["audit_status"] = "PUBLIC_READINESS_AUDIT_FAIL"

    with pytest.raises(ValueError, match="PUBLIC_READINESS_AUDIT_VALID"):
        build_milestone_3_dry_run_release_package(audit)


def test_dry_run_release_package_artifacts_are_present_and_hashed():
    package = build_milestone_3_dry_run_release_package()

    assert all(artifact["present"] is True for artifact in package.artifact_manifest)
    assert all(artifact["included_in_package"] is True for artifact in package.artifact_manifest)
    assert all(len(artifact["sha256"]) == 64 for artifact in package.artifact_manifest)
    assert all(artifact["size_bytes"] > 0 for artifact in package.artifact_manifest)


def test_dry_run_release_package_metadata_boundary():
    package = build_milestone_3_dry_run_release_package()

    assert package.metadata["public_safe"] is True
    assert package.metadata["deterministic"] is True
    assert package.metadata["local_only"] is True
    assert package.metadata["dry_run_only"] is True
    assert package.metadata["external_api_dependency"] is False
    assert package.metadata["contains_api_keys"] is False
    assert package.metadata["private_core_exposure"] is False


def test_dry_run_release_package_markdown_contains_boundary():
    package = build_milestone_3_dry_run_release_package()
    markdown = render_milestone_3_dry_run_release_package_markdown(package)

    assert "# ARC-AGI-3 Milestone #3 Dry-Run Release Package v1" in markdown
    assert "local_only=true" in markdown
    assert "dry_run_only=true" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert package.signature in markdown


def test_dry_run_release_package_writes_artifacts(tmp_path: Path):
    package = build_milestone_3_dry_run_release_package()
    artifacts = write_milestone_3_dry_run_release_package_artifacts(package, output_dir=tmp_path / "release-package")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["source_artifact_count"] == 24
    assert markdown_path.read_text(encoding="utf-8").startswith(
        "# ARC-AGI-3 Milestone #3 Dry-Run Release Package v1"
    )


def test_dry_run_release_package_validation_rejects_broken_contract():
    validation = validate_milestone_3_dry_run_release_package(
        {
            "status": "BROKEN",
            "metadata": {},
            "artifact_manifest": [],
        }
    )

    assert validation["status"] == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_INVALID"
    assert validation["valid"] is False
