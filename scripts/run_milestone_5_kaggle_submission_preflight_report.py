from hbce_arc_agi3.milestone_5_kaggle_submission_preflight_report import (
    run_kaggle_submission_preflight_report_pipeline,
)


def main() -> None:
    payload = run_kaggle_submission_preflight_report_pipeline()
    report = payload["report"]

    print(payload["status"])
    print(payload["report_status"])
    print(payload["validation_status"])
    print(payload["report_id"])
    print(payload["signature"])
    print(report["baseline_commit"])
    print(report["safety_checklist_id"])
    print(report["safety_checklist_signature"])
    print(payload["required_source_count"])
    print(payload["ready_source_count"])
    print(payload["preflight_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["blocking_issue_count"])
    print(payload["warning_count"])
    print(payload["ready_for_local_submission_smoke_test"])
    print(payload["ready_for_submission_candidate_format_report"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(all(item["ready"] for item in report["source_statuses"]))
    print(all(item["passed"] for item in report["preflight_gates"]))
    print(all(item["active"] is False for item in report["blocking_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
