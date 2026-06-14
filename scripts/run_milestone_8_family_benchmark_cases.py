from hbce_arc_agi3.milestone_8_family_benchmark_cases import (
    run_milestone_8_family_benchmark_cases_pipeline,
)


def main() -> None:
    payload = run_milestone_8_family_benchmark_cases_pipeline()
    benchmark = payload["benchmark"]

    print(payload["status"])
    print(payload["benchmark_status"])
    print(payload["validation_status"])
    print(payload["benchmark_id"])
    print(payload["signature"])
    print(benchmark["baseline_commit"])
    print(payload["benchmark_mode"])
    print(payload["benchmark_verdict"])
    print(payload["next_allowed_stage"])
    print(payload["family_count"])
    print(payload["benchmark_case_count"])
    print(payload["benchmark_pass_count"])
    print(payload["benchmark_failure_count"])
    print(payload["evidence_field_count"])
    print(payload["regression_guard_count"])
    print(payload["boundary_control_count"])
    print(payload["benchmark_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["benchmark_issue_count"])
    print(payload["warning_count"])
    print(payload["benchmark_ready"])
    print(payload["benchmark_locked"])
    print(payload["real_submission_created"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(result["passed"] for result in benchmark["benchmark_results"]))
    print(all(item["passed"] for item in benchmark["benchmark_gates"]))
    print(all(item["active"] is False for item in benchmark["benchmark_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
