from hbce_arc_agi3.milestone_7_competitive_solver_improvement_plan import (
    run_milestone_7_competitive_solver_improvement_plan_pipeline,
)


def main() -> None:
    payload = run_milestone_7_competitive_solver_improvement_plan_pipeline()
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
    print(payload["workstream_count"])
    print(payload["required_workstream_count"])
    print(payload["priority_p0_count"])
    print(payload["measurement_count"])
    print(payload["task_count"])
    print(payload["plan_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["plan_issue_count"])
    print(payload["warning_count"])
    print(payload["plan_ready"])
    print(payload["plan_locked"])
    print(payload["milestone_7_open"])
    print(payload["solver_improvement_required"])
    print(payload["competitive_claim_absent"])
    print(payload["manual_submission_allowed"])
    print(payload["manual_upload_performed"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(item["required"] for item in plan["workstreams"]))
    print(all(bool(item["measurement"]) for item in plan["workstreams"]))
    print(all(item["passed"] for item in plan["plan_gates"]))
    print(all(item["active"] is False for item in plan["plan_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
