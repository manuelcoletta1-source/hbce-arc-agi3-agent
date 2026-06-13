import json
from pathlib import Path

from hbce_arc_agi3.milestone_2_closure import (
    MILESTONE_2_TASKS,
    generate_and_validate_milestone_2_closure_report,
    generate_milestone_2_closure_report,
    validate_milestone_2_closure_report,
    write_milestone_2_closure_artifacts,
)


def test_milestone_2_closure_generates_pass_report():
    report = generate_milestone_2_closure_report(dry_run_manifest_path=None)
    validation = validate_milestone_2_closure_report(report)

    assert report.status == "MILESTONE_2_CLOSURE_READY"
    assert report.closure_status == "MILESTONE_2_CLOSED_PASS"
    assert report.milestone_status == "READY_FOR_PHASE_NEXT"
    assert report.total_tasks == 9
    assert report.closed_tasks == 9
    assert validation["status"] == "MILESTONE_2_CLOSURE_VALID"


def test_milestone_2_closure_task_chain_contains_all_tasks():
    report = generate_milestone_2_closure_report(dry_run_manifest_path=None)

    assert len(report.task_chain) == 9
    assert [item["status"] for item in report.task_chain] == ["CLOSED_PASS"] * 9
    assert report.task_chain[-1]["commit"] == "a9c7d03"


def test_milestone_2_closure_commit_chain_is_ordered():
    report = generate_milestone_2_closure_report(dry_run_manifest_path=None)

    assert report.commit_chain == [item["commit"] for item in MILESTONE_2_TASKS]
    assert report.commit_chain[0] == "8dee4c3"
    assert report.commit_chain[-1] == "a9c7d03"


def test_milestone_2_closure_uses_dry_run_package_manifest(tmp_path: Path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "status": "KAGGLE_DRY_RUN_PACKAGE_READY",
                "package_status": "KAGGLE_DRY_RUN_PACKAGE_VALID",
                "package_id": "KAGGLE-DRYRUN-TEST",
                "package_signature": "TESTSIGNATURE",
                "metadata": {
                    "public_safe": True,
                    "deterministic": True,
                    "external_api_dependency": False,
                    "executes_dataset_code": False,
                    "contains_api_keys": False,
                    "kaggle_submission_sent": False,
                    "private_core_exposure": False,
                },
            }
        ),
        encoding="utf-8",
    )

    report = generate_milestone_2_closure_report(dry_run_manifest_path=manifest_path)

    assert report.dry_run_package["package_id"] == "KAGGLE-DRYRUN-TEST"
    assert report.dry_run_package["package_status"] == "KAGGLE_DRY_RUN_PACKAGE_VALID"


def test_milestone_2_closure_markdown_contains_boundary():
    report = generate_milestone_2_closure_report(dry_run_manifest_path=None)

    assert "# ARC-AGI-3 Milestone #2 Report / Closure" in report.markdown
    assert "MILESTONE_2_CLOSED_PASS" in report.markdown
    assert "public_safe=true" in report.markdown
    assert "kaggle_submission_sent=false" in report.markdown
    assert "legalCertification=false" in report.markdown


def test_milestone_2_closure_pipeline_wrapper():
    result = generate_and_validate_milestone_2_closure_report(dry_run_manifest_path=None)

    assert result["status"] == "MILESTONE_2_CLOSURE_PIPELINE_READY"
    assert result["milestone_2_closure"]["status"] == "MILESTONE_2_CLOSURE_READY"
    assert result["validation"]["status"] == "MILESTONE_2_CLOSURE_VALID"
    assert result["metadata"]["private_core_exposure"] is False


def test_milestone_2_closure_writes_artifacts(tmp_path: Path):
    report = generate_milestone_2_closure_report(dry_run_manifest_path=None)
    artifacts = write_milestone_2_closure_artifacts(report, output_dir=tmp_path / "closure")

    markdown_path = Path(artifacts["markdown_path"])
    json_path = Path(artifacts["json_path"])

    assert markdown_path.exists()
    assert json_path.exists()
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Milestone #2")
    assert json.loads(json_path.read_text(encoding="utf-8"))["closure_status"] == "MILESTONE_2_CLOSED_PASS"


def test_milestone_2_closure_is_deterministic():
    first = generate_milestone_2_closure_report(dry_run_manifest_path=None)
    second = generate_milestone_2_closure_report(dry_run_manifest_path=None)

    assert first.to_dict() == second.to_dict()
    assert first.signature == second.signature


def test_milestone_2_closure_validation_rejects_broken_contract():
    validation = validate_milestone_2_closure_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "boundary": {},
            "dry_run_package": {},
        }
    )

    assert validation["status"] == "MILESTONE_2_CLOSURE_INVALID"
    assert validation["valid"] is False


def test_milestone_2_closure_boundary_is_public_safe():
    report = generate_milestone_2_closure_report(dry_run_manifest_path=None)

    assert report.boundary["public_safe"] is True
    assert report.boundary["deterministic"] is True
    assert report.boundary["external_api_dependency"] is False
    assert report.boundary["executes_dataset_code"] is False
    assert report.boundary["contains_api_keys"] is False
    assert report.boundary["kaggle_submission_sent"] is False
    assert report.boundary["private_core_exposure"] is False
    assert report.boundary["legalCertification"] is False
