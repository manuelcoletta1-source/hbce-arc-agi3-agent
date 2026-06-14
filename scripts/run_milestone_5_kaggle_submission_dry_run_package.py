from hbce_arc_agi3.milestone_5_kaggle_submission_dry_run_package import (
    run_kaggle_submission_dry_run_package_pipeline,
)


def main() -> None:
    payload = run_kaggle_submission_dry_run_package_pipeline()
    package = payload["package"]

    print(payload["status"])
    print(payload["package_status"])
    print(payload["validation_status"])
    print(payload["package_id"])
    print(payload["signature"])
    print(package["baseline_commit"])
    print(package["public_repo_index_id"])
    print(package["public_repo_index_signature"])
    print(payload["package_source_artifact_count"])
    print(payload["planned_release_file_count"])
    print(package["package_mode"])
    print(package["submission_mode"])
    print(package["real_submission_blocked"])
    print(payload["ready_for_submission_entrypoint_contract"])
    print(payload["kaggle_submission_sent"])
    print(all(item["present"] for item in package["source_artifacts"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
