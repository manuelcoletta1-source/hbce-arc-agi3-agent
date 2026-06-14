from hbce_arc_agi3.milestone_6_real_submission_package_freeze import (
    run_milestone_6_real_submission_package_freeze_pipeline,
)


def main() -> None:
    payload = run_milestone_6_real_submission_package_freeze_pipeline()
    freeze = payload["freeze"]

    print(payload["status"])
    print(payload["freeze_status"])
    print(payload["validation_status"])
    print(payload["freeze_id"])
    print(payload["signature"])
    print(freeze["baseline_commit"])
    print(payload["freeze_mode"])
    print(payload["freeze_verdict"])
    print(payload["frozen_artifact_count"])
    print(payload["ready_artifact_count"])
    print(payload["freeze_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["freeze_issue_count"])
    print(payload["warning_count"])
    print(payload["freeze_ready"])
    print(payload["freeze_locked"])
    print(payload["manual_execution_performed"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["kaggle_authentication_performed"])
    print(all(item["ready"] for item in freeze["frozen_artifacts"]))
    print(all(item["sha256"] != "MISSING_HASH" for item in freeze["frozen_artifacts"]))
    print(all(item["passed"] for item in freeze["freeze_gates"]))
    print(all(item["active"] is False for item in freeze["freeze_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
