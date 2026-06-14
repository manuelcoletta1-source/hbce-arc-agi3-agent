from hbce_arc_agi3.milestone_7_baseline_solver_failure_taxonomy import (
    run_milestone_7_baseline_solver_failure_taxonomy_pipeline,
)


def main() -> None:
    payload = run_milestone_7_baseline_solver_failure_taxonomy_pipeline()
    taxonomy = payload["taxonomy"]

    print(payload["status"])
    print(payload["taxonomy_status"])
    print(payload["validation_status"])
    print(payload["taxonomy_id"])
    print(payload["signature"])
    print(taxonomy["baseline_commit"])
    print(payload["taxonomy_mode"])
    print(payload["taxonomy_verdict"])
    print(payload["next_allowed_stage"])
    print(payload["failure_class_count"])
    print(payload["open_failure_count"])
    print(payload["closed_failure_count"])
    print(payload["priority_p0_count"])
    print(payload["target_task_count"])
    print(payload["taxonomy_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["taxonomy_issue_count"])
    print(payload["warning_count"])
    print(payload["taxonomy_ready"])
    print(payload["taxonomy_locked"])
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
    print(all(item["open"] for item in taxonomy["failure_classes"]))
    print(all(item["closed"] is False for item in taxonomy["failure_classes"]))
    print(all(bool(item["measurement"]) for item in taxonomy["failure_classes"]))
    print(all(item["passed"] for item in taxonomy["taxonomy_gates"]))
    print(all(item["active"] is False for item in taxonomy["taxonomy_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
