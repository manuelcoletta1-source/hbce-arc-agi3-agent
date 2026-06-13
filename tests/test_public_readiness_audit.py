import json
from pathlib import Path

import pytest

from hbce_arc_agi3.local_submission_candidate_builder import build_local_submission_candidate_package
from hbce_arc_agi3.public_readiness_audit import (
    build_public_readiness_audit_report,
    generate_and_validate_public_readiness_audit_report,
    render_public_readiness_audit_markdown,
    validate_public_readiness_audit_report,
    write_public_readiness_audit_artifacts,
)


def test_public_readiness_audit_builds_default_report():
    report = build_public_readiness_audit_report()
    validation = validate_public_readiness_audit_report(report)

    assert report.status == "PUBLIC_READINESS_AUDIT_READY"
    assert report.audit_status == "PUBLIC_READINESS_AUDIT_PASS"
    assert report.total_checks == 10
    assert report.passed_checks == 10
    assert report.failed_checks == 0
    assert report.blocking_issue_count == 0
    assert report.ready_for_release_package is True
    assert report.ready_for_kaggle_submission is False
    assert report.kaggle_submission_sent is False
    assert validation["status"] == "PUBLIC_READINESS_AUDIT_VALID"


def test_public_readiness_audit_pipeline_wrapper():
    result = generate_and_validate_public_readiness_audit_report()

    assert result["status"] == "PUBLIC_READINESS_AUDIT_PIPELINE_READY"
    assert result["public_readiness_audit"]["status"] == "PUBLIC_READINESS_AUDIT_READY"
    assert result["validation"]["status"] == "PUBLIC_READINESS_AUDIT_VALID"
    assert result["metadata"]["dry_run_only"] is True


def test_public_readiness_audit_is_deterministic():
    first = build_public_readiness_audit_report()
    second = build_public_readiness_audit_report()

    assert first.to_dict() == second.to_dict()
    assert first.audit_id == second.audit_id
    assert first.signature == second.signature


def test_public_readiness_audit_rejects_invalid_candidate():
    with pytest.raises(ValueError, match="LOCAL_SUBMISSION_CANDIDATE_VALID"):
        build_public_readiness_audit_report({"status": "BROKEN", "metadata": {}, "local_candidate_tasks": []})


def test_public_readiness_audit_detects_kaggle_submission_flag():
    candidate = build_local_submission_candidate_package().to_dict()
    candidate["kaggle_submission_sent"] = True

    report = build_public_readiness_audit_report(candidate)

    assert report.audit_status == "PUBLIC_READINESS_AUDIT_FAIL"
    assert report.blocking_issue_count >= 1
    assert report.ready_for_release_package is False


def test_public_readiness_audit_detects_external_dependency_flag():
    candidate = build_local_submission_candidate_package().to_dict()
    candidate["metadata"]["external_api_dependency"] = True

    report = build_public_readiness_audit_report(candidate)

    assert report.audit_status == "PUBLIC_READINESS_AUDIT_FAIL"
    assert report.blocking_issue_count >= 1


def test_public_readiness_audit_checks_are_public_safe():
    report = build_public_readiness_audit_report()

    assert all(check["status"] == "PUBLIC_READINESS_AUDIT_CHECK_READY" for check in report.audit_checks)
    assert all(check["metadata"]["public_safe"] is True for check in report.audit_checks)
    assert all(check["metadata"]["external_api_dependency"] is False for check in report.audit_checks)
    assert all(check["metadata"]["private_core_exposure"] is False for check in report.audit_checks)


def test_public_readiness_audit_markdown_contains_boundary():
    report = build_public_readiness_audit_report()
    markdown = render_public_readiness_audit_markdown(report)

    assert "# ARC-AGI-3 Public Readiness Audit v1" in markdown
    assert "local_only=true" in markdown
    assert "dry_run_only=true" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert report.signature in markdown


def test_public_readiness_audit_writes_artifacts(tmp_path: Path):
    report = build_public_readiness_audit_report()
    artifacts = write_public_readiness_audit_artifacts(report, output_dir=tmp_path / "audit")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["total_checks"] == 10
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Public Readiness Audit v1")


def test_public_readiness_audit_validation_rejects_broken_contract():
    validation = validate_public_readiness_audit_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "audit_checks": [],
        }
    )

    assert validation["status"] == "PUBLIC_READINESS_AUDIT_INVALID"
    assert validation["valid"] is False
