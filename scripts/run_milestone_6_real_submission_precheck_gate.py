from hbce_arc_agi3.milestone_6_real_submission_precheck_gate import (
    run_milestone_6_real_submission_precheck_gate_pipeline,
)


def main() -> None:
    payload = run_milestone_6_real_submission_precheck_gate_pipeline()
    precheck = payload["precheck"]

    print(payload["status"])
    print(payload["precheck_status"])
    print(payload["validation_status"])
    print(payload["precheck_id"])
    print(payload["signature"])
    print(precheck["baseline_commit"])
    print(precheck["operator_approval_declaration_id"])
    print(precheck["dry_run_package_id"])
    print(precheck["public_release_summary_id"])
    print(payload["precheck_mode"])
    print(payload["precheck_verdict"])
    print(payload["artifact_count"])
    print(payload["ready_artifact_count"])
    print(payload["precheck_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["precheck_issue_count"])
    print(payload["warning_count"])
    print(payload["precheck_gate_ready"])
    print(payload["precheck_passed"])
    print(payload["operator_approval_granted"])
    print(payload["manual_execution_gate_required"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(item["ready"] for item in precheck["artifact_statuses"]))
    print(all(item["passed"] for item in precheck["precheck_gates"]))
    print(all(item["active"] is False for item in precheck["precheck_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
