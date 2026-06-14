from pathlib import Path

from hbce_arc_agi3.milestone_5_public_readiness_audit import (
    AUDIT_STATUS,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    REQUIRED_PUBLIC_READINESS_ARTIFACTS,
    build_public_readiness_baseline_audit,
    render_public_readiness_baseline_audit_markdown,
    run_public_readiness_baseline_audit_pipeline,
    validate_public_readiness_baseline_audit,
    write_public_readiness_baseline_audit_artifacts,
)


def test_public_readiness_baseline_audit_ready():
    audit = build_public_readiness_baseline_audit()

    assert audit.status == AUDIT_STATUS
    assert audit.baseline_commit.startswith("f97b25d")
    assert audit.ready_for_public_readiness_phase is True
    assert audit.kaggle_submission_sent is False
    assert len(audit.required_artifacts) == len(REQUIRED_PUBLIC_READINESS_ARTIFACTS)
    assert all(audit.required_artifacts.values())


def test_public_readiness_baseline_audit_validation_passes():
    audit = build_public_readiness_baseline_audit()
    validation = validate_public_readiness_baseline_audit(audit)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_public_readiness_baseline_audit_pipeline_ready():
    payload = run_public_readiness_baseline_audit_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["audit_status"] == AUDIT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["ready_for_public_readiness_phase"] is True
    assert payload["kaggle_submission_sent"] is False


def test_public_readiness_baseline_audit_markdown_contains_markers():
    audit = build_public_readiness_baseline_audit()
    markdown = render_public_readiness_baseline_audit_markdown(audit)

    assert "ARC_AGI3_MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_PUBLIC_READINESS_PHASE=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_BASELINE_COMMIT=f97b25d" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_public_readiness_baseline_audit_writes_artifacts(tmp_path: Path):
    audit = build_public_readiness_baseline_audit()
    paths = write_public_readiness_baseline_audit_artifacts(
        audit,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert "MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_READY=true" in markdown_path.read_text(encoding="utf-8")


def test_required_public_readiness_artifacts_exist():
    missing = [
        artifact
        for artifact in REQUIRED_PUBLIC_READINESS_ARTIFACTS
        if not Path(artifact).exists()
    ]

    assert missing == []
