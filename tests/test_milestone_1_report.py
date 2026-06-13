from pathlib import Path


REPORT = Path("docs/milestone-1-report.md")


def test_milestone_1_report_exists_and_has_final_status():
    text = REPORT.read_text(encoding="utf-8")

    assert "# ARC-AGI-3 Milestone #1 Report" in text
    assert "MILESTONE_1_CLOSED_PASS" in text
    assert "ARC_AGI3_MILESTONE_1_CLOSED_PASS=true" in text
    assert "25 passed" in text


def test_milestone_1_report_records_commit_chain():
    text = REPORT.read_text(encoding="utf-8")

    expected_commits = [
        "9387cf1",
        "181d6e8",
        "d9c7a9d",
        "ffb8aab",
        "3eaf324",
        "225b324",
        "38d808e",
        "03a5b18",
        "6eecd1a",
        "85899c3",
    ]

    for commit in expected_commits:
        assert commit in text


def test_milestone_1_report_public_boundary_markers():
    text = REPORT.read_text(encoding="utf-8")

    expected_markers = [
        "ARC_AGI3_MILESTONE_1_REPORT_READY=true",
        "ARC_AGI3_MILESTONE_1_STATUS=MILESTONE_1_CLOSED_PASS",
        "ARC_AGI3_PUBLIC_BASELINE_READY=true",
        "ARC_AGI3_PIPELINE_READY=true",
        "ARC_AGI3_TESTS_PASSING=true",
        "ARC_AGI3_SUBMISSION_PACKAGE_SKELETON_READY=true",
        "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
        "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
        "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
        "legalCertification=false",
    ]

    for marker in expected_markers:
        assert marker in text
