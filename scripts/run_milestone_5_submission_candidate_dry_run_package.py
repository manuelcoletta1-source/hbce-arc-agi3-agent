from hbce_arc_agi3.milestone_5_submission_candidate_dry_run_package import (
    run_submission_candidate_dry_run_package_pipeline,
)


def main() -> None:
    payload = run_submission_candidate_dry_run_package_pipeline()
    package = payload["package"]

    print(payload["status"])
    print(payload["package_status"])
    print(payload["validation_status"])
    print(payload["package_id"])
    print(payload["signature"])
    print(package["baseline_commit"])
    print(package["format_report_id"])
    print(package["format_report_signature"])
    print(package["local_smoke_id"])
    print(package["local_smoke_signature"])
    print(payload["package_mode"])
    print(payload["candidate_kind"])
    print(payload["submission_filename"])
    print(payload["submission_mode"])
    print(payload["package_artifact_count"])
    print(payload["ready_artifact_count"])
    print(payload["package_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["package_issue_count"])
    print(payload["warning_count"])
    print(payload["candidate_task_count"])
    print(payload["dry_run_package_ready"])
    print(payload["ready_for_milestone_5_closure"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(all(item["ready"] for item in package["artifact_statuses"]))
    print(all(item["passed"] for item in package["package_gates"]))
    print(all(item["active"] is False for item in package["package_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["artifacts"]["preview_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
