from hbce_arc_agi3.milestone_3_dry_run_release_package import (
    generate_and_validate_milestone_3_dry_run_release_package,
    write_milestone_3_dry_run_release_package_artifacts,
)


def main() -> None:
    result = generate_and_validate_milestone_3_dry_run_release_package()
    package = result["dry_run_release_package"]
    validation = result["validation"]
    artifacts = write_milestone_3_dry_run_release_package_artifacts(package)

    print(result["status"])
    print(package["status"])
    print(validation["status"])
    print(package["package_status"])
    print(package["package_id"])
    print(package["audit_id"])
    print(package["candidate_id"])
    print(package["report_index_id"])
    print(package["release_mode"])
    print(package["submission_mode"])
    print(package["source_artifact_count"])
    print(package["present_source_artifact_count"])
    print(package["missing_source_artifact_count"])
    print(package["generated_package_artifact_count"])
    print(package["total_package_artifact_count"])
    print(package["blocking_issue_count"])
    print(package["warning_count"])
    print(package["ready_for_milestone_3_closure"])
    print(package["ready_for_kaggle_submission"])
    print(package["kaggle_submission_sent"])
    print(package["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(package["metadata"])


if __name__ == "__main__":
    main()
