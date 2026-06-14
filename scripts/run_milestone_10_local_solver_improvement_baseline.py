from hbce_arc_agi3.milestone_10_local_solver_improvement_baseline import (
    run_milestone_10_local_solver_improvement_baseline_pipeline,
)


def main() -> None:
    payload = run_milestone_10_local_solver_improvement_baseline_pipeline()
    baseline = payload["baseline"]

    print(payload["status"])
    print(payload["baseline_status"])
    print(payload["validation_status"])
    print(payload["baseline_id"])
    print(payload["signature"])
    print(baseline["baseline_commit"])
    print(payload["baseline_mode"])
    print(payload["baseline_verdict"])
    print(payload["next_allowed_stage"])
    print(payload["baseline_ready"])
    print(payload["milestone_10_open"])
    print(payload["local_solver_improvement_cycle_created"])
    print(payload["local_solver_improvement_cycle_ready"])
    print(payload["local_improvement_stage_count"])
    print(payload["baseline_check_count"])
    print(payload["baseline_case_count"])
    print(payload["baseline_pass_count"])
    print(payload["baseline_failure_count"])
    print(payload["baseline_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["baseline_issue_count"])
    print(payload["warning_count"])
    print(payload["real_submission_decision"])
    print(payload["real_submission_allowed"])
    print(payload["manual_upload_allowed"])
    print(payload["kaggle_authentication_allowed"])
    print(payload["kaggle_submission_sent"])
    print(payload["fail_closed_required"])
    print(payload["fail_closed_active"])
    print(baseline["source_summary"]["milestone_9_closure_id"])
    print(baseline["source_summary"]["candidate_id"])
    print(baseline["source_summary"]["candidate_signature"])
    print(all(result["passed"] for result in baseline["baseline_results"]))
    print(all(item["passed"] for item in baseline["baseline_gates"]))
    print(all(item["active"] is False for item in baseline["baseline_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
