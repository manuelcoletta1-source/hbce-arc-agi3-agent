from hbce_arc_agi3.milestone_5_local_submission_smoke_test import (
    run_local_submission_smoke_test_pipeline,
)


def main() -> None:
    payload = run_local_submission_smoke_test_pipeline()
    smoke_test = payload["smoke_test"]

    print(payload["status"])
    print(payload["smoke_status"])
    print(payload["validation_status"])
    print(payload["smoke_id"])
    print(payload["signature"])
    print(smoke_test["baseline_commit"])
    print(smoke_test["preflight_report_id"])
    print(smoke_test["preflight_report_signature"])
    print(payload["smoke_mode"])
    print(payload["candidate_kind"])
    print(payload["expected_submission_filename"])
    print(payload["smoke_case_count"])
    print(payload["smoke_case_passed_count"])
    print(payload["candidate_task_count"])
    print(payload["ready_for_submission_candidate_format_report"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(all(item["passed"] for item in smoke_test["smoke_cases"]))
    print(smoke_test["local_submission_candidate"]["kaggle_submission_sent"])
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["candidate_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
