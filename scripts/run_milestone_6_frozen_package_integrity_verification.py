from hbce_arc_agi3.milestone_6_frozen_package_integrity_verification import (
    run_milestone_6_frozen_package_integrity_verification_pipeline,
)


def main() -> None:
    payload = run_milestone_6_frozen_package_integrity_verification_pipeline()
    verification = payload["verification"]

    print(payload["status"])
    print(payload["integrity_status"])
    print(payload["validation_status"])
    print(payload["integrity_id"])
    print(payload["signature"])
    print(verification["baseline_commit"])
    print(payload["integrity_mode"])
    print(payload["integrity_verdict"])
    print(payload["frozen_artifact_count"])
    print(payload["verified_artifact_count"])
    print(payload["matched_hash_count"])
    print(payload["integrity_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["integrity_issue_count"])
    print(payload["warning_count"])
    print(payload["integrity_ready"])
    print(payload["integrity_verified"])
    print(payload["integrity_locked"])
    print(payload["manual_execution_performed"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(item["hash_match"] for item in verification["artifact_integrity_checks"]))
    print(all(item["passed"] for item in verification["integrity_gates"]))
    print(all(item["active"] is False for item in verification["integrity_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
