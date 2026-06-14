from hbce_arc_agi3.milestone_8_competitive_solver_iteration_plan import (
    run_milestone_8_competitive_solver_iteration_plan_pipeline,
)


def main() -> None:
    payload = run_milestone_8_competitive_solver_iteration_plan_pipeline()
    plan = payload["plan"]

    print(payload["status"])
    print(payload["plan_status"])
    print(payload["validation_status"])
    print(payload["plan_id"])
    print(payload["signature"])
    print(plan["baseline_commit"])
    print(payload["plan_mode"])
    print(payload["plan_verdict"])
    print(payload["next_allowed_stage"])
    print(payload["audit_real_submission_readiness"])
    print(payload["audit_real_submission_decision"])
    print(payload["iteration_family_count"])
    print(payload["solver_iteration_count"])
    print(payload["benchmark_target_count"])
    print(payload["regression_guard_count"])
    print(payload["control_count"])
    print(payload["plan_section_count"])
    print(payload["task_queue_count"])
    print(payload["plan_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["plan_issue_count"])
    print(payload["warning_count"])
    print(payload["plan_ready"])
    print(payload["plan_locked"])
    print(payload["runtime_solver_iteration_required"])
    print(payload["real_submission_created"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(item["ready_for_kernel_v2"] for item in plan["iteration_families"]))
    print(all(item["runtime_solver_target"] for item in plan["solver_iterations"]))
    print(all(item["passed"] for item in plan["plan_gates"]))
    print(all(item["active"] is False for item in plan["plan_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
