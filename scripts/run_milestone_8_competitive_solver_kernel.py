from hbce_arc_agi3.milestone_8_competitive_solver_kernel import (
    run_milestone_8_competitive_solver_kernel_pipeline,
)


def main() -> None:
    payload = run_milestone_8_competitive_solver_kernel_pipeline()
    kernel = payload["kernel"]

    print(payload["status"])
    print(payload["kernel_status"])
    print(payload["validation_status"])
    print(payload["kernel_id"])
    print(payload["signature"])
    print(kernel["baseline_commit"])
    print(payload["kernel_mode"])
    print(payload["kernel_verdict"])
    print(payload["next_allowed_stage"])
    print(payload["kernel_family_count"])
    print(payload["kernel_operation_count"])
    print(payload["sample_case_count"])
    print(payload["regression_guard_count"])
    print(payload["boundary_control_count"])
    print(payload["kernel_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["kernel_issue_count"])
    print(payload["warning_count"])
    print(payload["kernel_ready"])
    print(payload["kernel_locked"])
    print(payload["solver_kernel_v2_created"])
    print(payload["runtime_solver_iteration_performed"])
    print(payload["real_submission_created"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(kernel["sample_results"].values()))
    print(all(item["passed"] for item in kernel["kernel_gates"]))
    print(all(item["active"] is False for item in kernel["kernel_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
