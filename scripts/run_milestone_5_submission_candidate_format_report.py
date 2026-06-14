from hbce_arc_agi3.milestone_5_submission_candidate_format_report import (
    run_submission_candidate_format_report_pipeline,
)


def main() -> None:
    payload = run_submission_candidate_format_report_pipeline()
    report = payload["report"]

    print(payload["status"])
    print(payload["report_status"])
    print(payload["validation_status"])
    print(payload["report_id"])
    print(payload["signature"])
    print(report["baseline_commit"])
    print(report["local_smoke_id"])
    print(report["local_smoke_signature"])
    print(payload["candidate_kind"])
    print(payload["submission_filename"])
    print(payload["submission_mode"])
    print(payload["candidate_task_count"])
    print(payload["valid_task_count"])
    print(payload["format_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["format_issue_count"])
    print(payload["warning_count"])
    print(payload["ready_for_submission_candidate_dry_run"])
    print(payload["ready_for_milestone_5_closure"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(all(item["valid"] for item in report["task_format_statuses"]))
    print(all(item["passed"] for item in report["format_gates"]))
    print(all(item["active"] is False for item in report["format_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["preview_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
