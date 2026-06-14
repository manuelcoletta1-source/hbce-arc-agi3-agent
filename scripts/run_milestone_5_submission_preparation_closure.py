from hbce_arc_agi3.milestone_5_submission_preparation_closure import (
    run_milestone_5_submission_preparation_closure_pipeline,
)


def main() -> None:
    payload = run_milestone_5_submission_preparation_closure_pipeline()
    closure = payload["closure"]

    print(payload["status"])
    print(payload["closure_status"])
    print(payload["validation_status"])
    print(payload["closure_id"])
    print(payload["signature"])
    print(closure["baseline_commit"])
    print(closure["final_package_id"])
    print(closure["final_package_signature"])
    print(payload["closed_task_count"])
    print(payload["ready_task_count"])
    print(payload["closure_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["closure_issue_count"])
    print(payload["warning_count"])
    print(payload["submission_preparation_closed"])
    print(payload["ready_for_public_release_summary"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(all(item["ready"] for item in closure["task_statuses"]))
    print(all(item["passed"] for item in closure["closure_gates"]))
    print(all(item["active"] is False for item in closure["closure_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
