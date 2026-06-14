from pathlib import Path

from hbce_arc_agi3.milestone_5_public_safety_boundary_checklist import (
    CHECKLIST_STATUS,
    MANDATORY_ALLOWED_ACTIONS,
    MANDATORY_BLOCKED_ACTIONS,
    PIPELINE_STATUS,
    PUBLIC_SAFETY_ASSERTIONS,
    REQUIRED_BOUNDARY_FLAGS,
    VALIDATION_STATUS,
    build_boundary_flags,
    build_public_safety_assertions,
    build_public_safety_boundary_checklist,
    render_public_safety_boundary_checklist_markdown,
    render_public_safety_boundary_manifest,
    run_public_safety_boundary_checklist_pipeline,
    validate_public_safety_boundary_checklist,
    write_public_safety_boundary_checklist_artifacts,
)


def test_public_safety_boundary_checklist_ready():
    checklist = build_public_safety_boundary_checklist()

    assert checklist.status == CHECKLIST_STATUS
    assert checklist.baseline_commit.startswith("77da7ae")
    assert len(checklist.boundary_flags) == len(REQUIRED_BOUNDARY_FLAGS)
    assert len(checklist.public_safety_assertions) == len(PUBLIC_SAFETY_ASSERTIONS)
    assert len(checklist.mandatory_blocked_actions) == len(MANDATORY_BLOCKED_ACTIONS)
    assert len(checklist.mandatory_allowed_actions) == len(MANDATORY_ALLOWED_ACTIONS)
    assert checklist.ready_for_kaggle_submission_preflight_report is True
    assert checklist.kaggle_submission_sent is False


def test_public_safety_boundary_checklist_blocks_required_actions():
    checklist = build_public_safety_boundary_checklist()

    assert "kaggle_api_authentication" in checklist.mandatory_blocked_actions
    assert "kaggle_api_submission" in checklist.mandatory_blocked_actions
    assert "network_upload" in checklist.mandatory_blocked_actions
    assert "external_api_call" in checklist.mandatory_blocked_actions
    assert "secret_or_token_read" in checklist.mandatory_blocked_actions
    assert "private_core_export" in checklist.mandatory_blocked_actions
    assert "legal_certification_claim" in checklist.mandatory_blocked_actions


def test_public_safety_boundary_checklist_validation_passes():
    checklist = build_public_safety_boundary_checklist()
    validation = validate_public_safety_boundary_checklist(checklist)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_public_safety_boundary_checklist_pipeline_ready():
    payload = run_public_safety_boundary_checklist_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["checklist_status"] == CHECKLIST_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["boundary_flag_count"] == len(REQUIRED_BOUNDARY_FLAGS)
    assert payload["public_safety_assertion_count"] == len(PUBLIC_SAFETY_ASSERTIONS)
    assert payload["blocked_action_count"] == len(MANDATORY_BLOCKED_ACTIONS)
    assert payload["allowed_action_count"] == len(MANDATORY_ALLOWED_ACTIONS)
    assert payload["ready_for_kaggle_submission_preflight_report"] is True
    assert payload["kaggle_submission_sent"] is False


def test_public_safety_boundary_checklist_markdown_contains_markers():
    checklist = build_public_safety_boundary_checklist()
    markdown = render_public_safety_boundary_checklist_markdown(checklist)

    assert "ARC_AGI3_MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_KAGGLE_SUBMISSION_PREFLIGHT_REPORT=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_KAGGLE_API_AUTHENTICATION_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_KAGGLE_API_SUBMISSION_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_NETWORK_UPLOAD_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_EXTERNAL_API_CALL_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_SECRET_OR_TOKEN_READ_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_PRIVATE_CORE_EXPORT_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_LEGAL_CERTIFICATION_CLAIM_BLOCKED=true" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_public_safety_boundary_manifest_contains_boundary():
    checklist = build_public_safety_boundary_checklist()
    manifest = render_public_safety_boundary_manifest(checklist)

    assert "ARC AGI3 PUBLIC SAFETY & BOUNDARY CHECKLIST MANIFEST v1" in manifest
    assert "ready_for_kaggle_submission_preflight_report=True" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "kaggle_api_submission" in manifest
    assert "network_upload" in manifest
    assert "external_api_call" in manifest
    assert "secret_or_token_read" in manifest
    assert "private_core_export" in manifest
    assert "legal_certification_claim" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_public_safety_boundary_checklist_writes_artifacts(tmp_path: Path):
    checklist = build_public_safety_boundary_checklist()
    paths = write_public_safety_boundary_checklist_artifacts(
        checklist,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 PUBLIC SAFETY & BOUNDARY CHECKLIST MANIFEST v1" in manifest_path.read_text(encoding="utf-8")


def test_public_safety_assertions_are_stable():
    assertions = build_public_safety_assertions()

    assert [item.name for item in assertions] == [
        "no_kaggle_upload",
        "no_kaggle_api_authentication",
        "no_external_api_call",
        "no_network_upload",
        "no_secret_or_token_read",
        "no_private_core_export",
        "no_legal_certification_claim",
        "local_dry_run_only",
        "public_artifacts_only",
        "human_review_required_before_real_submission",
    ]
    assert all(item.satisfied for item in assertions)


def test_boundary_flags_are_stable():
    boundary = {
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
    flags = build_boundary_flags(boundary)

    assert [item.name for item in flags] == [
        "public_safe",
        "deterministic",
        "local_only",
        "dry_run_only",
        "external_api_dependency",
        "contains_api_keys",
        "kaggle_submission_sent",
        "private_core_exposure",
        "legal_certification",
    ]
    assert all(item.valid for item in flags)
