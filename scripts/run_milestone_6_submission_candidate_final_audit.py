from hbce_arc_agi3.milestone_6_submission_candidate_final_audit import (
    run_milestone_6_submission_candidate_final_audit_pipeline,
)


def main() -> None:
    payload = run_milestone_6_submission_candidate_final_audit_pipeline()
    audit = payload["audit"]

    print(payload["status"])
    print(payload["audit_status"])
    print(payload["validation_status"])
    print(payload["audit_id"])
    print(payload["signature"])
    print(audit["baseline_commit"])
    print(payload["audit_mode"])
    print(payload["audit_verdict"])
    print(payload["audited_source_count"])
    print(payload["ready_source_count"])
    print(payload["source_hash_count"])
    print(payload["audit_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["audit_issue_count"])
    print(payload["warning_count"])
    print(payload["audit_ready"])
    print(payload["audit_locked"])
    print(payload["solver_improvement_required"])
    print(payload["competitive_claim_absent"])
    print(payload["manual_upload_required"])
    print(payload["manual_execution_performed"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(item["ready"] for item in audit["audited_sources"]))
    print(all(item["sha256"] != "MISSING_HASH" for item in audit["audited_sources"]))
    print(all(item["passed"] for item in audit["audit_gates"]))
    print(all(item["active"] is False for item in audit["audit_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
