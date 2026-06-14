from hbce_arc_agi3.milestone_5_public_release_summary import (
    run_milestone_5_public_release_summary_pipeline,
)


def main() -> None:
    payload = run_milestone_5_public_release_summary_pipeline()
    summary = payload["summary"]

    print(payload["status"])
    print(payload["summary_status"])
    print(payload["validation_status"])
    print(payload["summary_id"])
    print(payload["signature"])
    print(summary["baseline_commit"])
    print(summary["closure_id"])
    print(summary["closure_signature"])
    print(summary["final_package_id"])
    print(summary["release_scope"])
    print(summary["milestone_status"])
    print(payload["closed_task_count"])
    print(payload["ready_task_count"])
    print(payload["summary_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["summary_issue_count"])
    print(payload["warning_count"])
    print(payload["public_release_summary_ready"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(all(item["passed"] for item in summary["summary_gates"]))
    print(all(item["active"] is False for item in summary["summary_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["artifacts"]["readme_snippet_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
