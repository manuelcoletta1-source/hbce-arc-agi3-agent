from hbce_arc_agi3.milestone_3_closure_report import (
    generate_and_validate_milestone_3_closure_report,
    write_milestone_3_closure_report_artifacts,
)


def main() -> None:
    result = generate_and_validate_milestone_3_closure_report()
    report = result["milestone_3_closure_report"]
    validation = result["validation"]
    artifacts = write_milestone_3_closure_report_artifacts(report)

    print(result["status"])
    print(report["status"])
    print(validation["status"])
    print(report["closure_status"])
    print(report["closure_id"])
    print(report["package_id"])
    print(report["audit_id"])
    print(report["candidate_id"])
    print(report["report_index_id"])
    print(report["release_mode"])
    print(report["submission_mode"])
    print(report["task_count"])
    print(report["completed_task_count"])
    print(report["failed_task_count"])
    print(report["closure_blocking_issue_count"])
    print(report["closure_warning_count"])
    print(report["package_source_artifact_count"])
    print(report["package_total_artifact_count"])
    print(report["tests_passed_recorded"])
    print(report["ready_for_next_milestone"])
    print(report["ready_for_kaggle_submission"])
    print(report["kaggle_submission_sent"])
    print(report["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(report["metadata"])


if __name__ == "__main__":
    main()
