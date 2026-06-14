from hbce_arc_agi3.milestone_6_manual_submission_execution_gate import (
    run_milestone_6_manual_submission_execution_gate_pipeline,
)


def main() -> None:
    payload = run_milestone_6_manual_submission_execution_gate_pipeline()
    gate = payload["gate"]

    print(payload["status"])
    print(payload["gate_status"])
    print(payload["validation_status"])
    print(payload["gate_id"])
    print(payload["signature"])
    print(gate["baseline_commit"])
    print(gate["precheck_id"])
    print(payload["gate_mode"])
    print(payload["gate_verdict"])
    print(payload["gate_count"])
    print(payload["passed_gate_count"])
    print(payload["issue_count"])
    print(payload["warning_count"])
    print(payload["manual_execution_gate_ready"])
    print(payload["manual_execution_gate_required"])
    print(payload["manual_execution_performed"])
    print(payload["operator_approval_granted"])
    print(payload["precheck_passed"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(item["passed"] for item in gate["manual_execution_gates"]))
    print(all(item["active"] is False for item in gate["manual_execution_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
