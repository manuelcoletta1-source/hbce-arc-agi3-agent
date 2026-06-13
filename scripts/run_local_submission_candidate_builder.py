from hbce_arc_agi3.local_submission_candidate_builder import (
    generate_and_validate_local_submission_candidate_package,
    write_local_submission_candidate_artifacts,
)


def main() -> None:
    result = generate_and_validate_local_submission_candidate_package()
    package = result["local_submission_candidate"]
    validation = result["validation"]
    artifacts = write_local_submission_candidate_artifacts(package)

    print(result["status"])
    print(package["status"])
    print(validation["status"])
    print(package["candidate_status"])
    print(package["candidate_id"])
    print(package["report_index_id"])
    print(package["batch_id"])
    print(package["registry_id"])
    print(package["aggregate_id"])
    print(package["strategy_index_id"])
    print(package["failure_taxonomy_report_id"])
    print(package["selected_strategy_id"])
    print(package["selected_strategy_name"])
    print(package["submission_mode"])
    print(package["task_count"])
    print(package["eligible_task_count"])
    print(package["blocked_task_count"])
    print(package["remediation_required_count"])
    print(package["ready_for_public_readiness_audit"])
    print(package["ready_for_kaggle_submission"])
    print(package["kaggle_submission_sent"])
    print(package["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(package["metadata"])


if __name__ == "__main__":
    main()
