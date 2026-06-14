from hbce_arc_agi3.milestone_10_local_error_pattern_audit import (
    run_milestone_10_local_error_pattern_audit_pipeline,
)


def main() -> None:
    payload = run_milestone_10_local_error_pattern_audit_pipeline()
    audit = payload["audit"]

    print(payload["status"])
    print(payload["audit_status"])
    print(payload["validation_status"])
    print(payload["audit_id"])
    print(payload["signature"])
    print(audit["baseline_commit"])
    print(payload["audit_mode"])
    print(payload["audit_verdict"])
    print(payload["next_allowed_stage"])
    print(payload["audit_ready"])
    print(payload["local_error_pattern_audit_created"])
    print(payload["local_error_pattern_audit_ready"])
    print(payload["error_pattern_count"])
    print(payload["solver_target_count"])
    print(payload["audit_check_count"])
    print(payload["audit_case_count"])
    print(payload["audit_pass_count"])
    print(payload["audit_failure_count"])
    print(payload["audit_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["audit_issue_count"])
    print(payload["warning_count"])
    print(payload["real_submission_decision"])
    print(payload["real_submission_allowed"])
    print(payload["manual_upload_allowed"])
    print(payload["kaggle_authentication_allowed"])
    print(payload["kaggle_submission_sent"])
    print(payload["fail_closed_required"])
    print(payload["fail_closed_active"])
    print(audit["source_summary"]["baseline_id"])
    print(audit["source_summary"]["candidate_id"])
    print(audit["source_summary"]["candidate_signature"])
    print(all(result["passed"] for result in audit["audit_results"]))
    print(all(item["passed"] for item in audit["audit_gates"]))
    print(all(item["active"] is False for item in audit["audit_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
