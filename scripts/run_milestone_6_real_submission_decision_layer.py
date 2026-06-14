from hbce_arc_agi3.milestone_6_real_submission_decision_layer import (
    run_milestone_6_real_submission_decision_layer_pipeline,
)


def main() -> None:
    payload = run_milestone_6_real_submission_decision_layer_pipeline()
    decision = payload["decision"]

    print(payload["status"])
    print(payload["decision_status"])
    print(payload["validation_status"])
    print(payload["decision_id"])
    print(payload["signature"])
    print(decision["baseline_commit"])
    print(decision["public_release_summary_id"])
    print(decision["submission_closure_id"])
    print(decision["dry_run_package_id"])
    print(payload["decision_mode"])
    print(payload["decision_verdict"])
    print(payload["artifact_count"])
    print(payload["ready_artifact_count"])
    print(payload["decision_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["decision_issue_count"])
    print(payload["warning_count"])
    print(payload["decision_layer_ready"])
    print(payload["operator_approval_required"])
    print(payload["operator_approval_received"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(all(item["ready"] for item in decision["artifact_statuses"]))
    print(all(item["passed"] for item in decision["decision_gates"]))
    print(all(item["active"] is False for item in decision["decision_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
