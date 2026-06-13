from pathlib import Path


REPORT = Path("docs/milestone-2-plan.md")


def test_milestone_2_plan_exists_and_is_open():
    text = REPORT.read_text(encoding="utf-8")

    assert "# ARC-AGI-3 Milestone #2 Plan" in text
    assert "ARC_AGI3_MILESTONE_2_PLAN_READY=true" in text
    assert "ARC_AGI3_MILESTONE_2_STATUS=OPEN_PLANNED" in text
    assert "ARC_AGI3_MILESTONE_2_START_COMMIT=f7ee3c8" in text
    assert "ARC_AGI3_MILESTONE_2_PARENT_REGISTRY_COMMIT=5e70147" in text


def test_milestone_2_plan_records_task_chain():
    text = REPORT.read_text(encoding="utf-8")

    expected_terms = [
        "task_loader",
        "environment_harness",
        "object_model",
        "rule_hypothesis",
        "planner_strategy",
        "verification_scoring",
        "trace_schema",
        "dry_run_submission_package",
    ]

    for term in expected_terms:
        assert term in text


def test_milestone_2_plan_boundary_markers():
    text = REPORT.read_text(encoding="utf-8")

    expected_markers = [
        "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
        "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
        "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
        "legalCertification=false",
    ]

    for marker in expected_markers:
        assert marker in text
