from hbce_arc_agi3.public_readiness_audit import (
    generate_and_validate_public_readiness_audit_report,
    write_public_readiness_audit_artifacts,
)


def main() -> None:
    result = generate_and_validate_public_readiness_audit_report()
    report = result["public_readiness_audit"]
    validation = result["validation"]
    artifacts = write_public_readiness_audit_artifacts(report)

    print(result["status"])
    print(report["status"])
    print(validation["status"])
    print(report["audit_status"])
    print(report["audit_id"])
    print(report["candidate_id"])
    print(report["report_index_id"])
    print(report["submission_mode"])
    print(report["total_checks"])
    print(report["passed_checks"])
    print(report["failed_checks"])
    print(report["blocking_issue_count"])
    print(report["warning_count"])
    print(report["ready_for_release_package"])
    print(report["ready_for_kaggle_submission"])
    print(report["kaggle_submission_sent"])
    print(report["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(report["metadata"])


if __name__ == "__main__":
    main()
