from hbce_arc_agi3.milestone_6_solver_improvement_before_real_submission import (
    run_milestone_6_solver_improvement_before_real_submission_pipeline,
)


def main() -> None:
    payload = run_milestone_6_solver_improvement_before_real_submission_pipeline()
    improvement = payload["improvement"]

    print(payload["status"])
    print(payload["improvement_status"])
    print(payload["validation_status"])
    print(payload["improvement_id"])
    print(payload["signature"])
    print(improvement["baseline_commit"])
    print(payload["improvement_mode"])
    print(payload["improvement_verdict"])
    print(payload["improvement_target_count"])
    print(payload["required_target_count"])
    print(payload["priority_p0_count"])
    print(payload["measurement_count"])
    print(payload["improvement_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["improvement_issue_count"])
    print(payload["warning_count"])
    print(payload["improvement_ready"])
    print(payload["improvement_locked"])
    print(payload["solver_improvement_required"])
    print(payload["solver_improvement_started"])
    print(payload["solver_improvement_completed"])
    print(payload["competitive_claim_absent"])
    print(payload["manual_upload_required"])
    print(payload["manual_execution_performed"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(item["required_before_submission"] for item in improvement["improvement_targets"]))
    print(all(bool(item["measurement"]) for item in improvement["improvement_targets"]))
    print(all(item["passed"] for item in improvement["improvement_gates"]))
    print(all(item["active"] is False for item in improvement["improvement_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
