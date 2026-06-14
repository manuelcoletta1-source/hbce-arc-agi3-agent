from hbce_arc_agi3.milestone_7_task_family_solver_expansion import (
    run_milestone_7_task_family_solver_expansion_pipeline,
)


def main() -> None:
    payload = run_milestone_7_task_family_solver_expansion_pipeline()
    expansion = payload["expansion"]

    print(payload["status"])
    print(payload["expansion_status"])
    print(payload["validation_status"])
    print(payload["expansion_id"])
    print(payload["signature"])
    print(expansion["baseline_commit"])
    print(payload["expansion_mode"])
    print(payload["expansion_verdict"])
    print(payload["next_allowed_stage"])
    print(payload["family_count"])
    print(payload["source_failure_count"])
    print(payload["strategy_count"])
    print(payload["regression_guard_count"])
    print(payload["expansion_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["expansion_issue_count"])
    print(payload["warning_count"])
    print(payload["expansion_ready"])
    print(payload["expansion_locked"])
    print(payload["runtime_solver_modified"])
    print(payload["solver_family_registry_ready"])
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
    print(all(item["implemented_as_registry"] for item in expansion["family_expansions"]))
    print(all(item["runtime_solver_modified"] is False for item in expansion["family_expansions"]))
    print(all(item["ready_for_task_4"] for item in expansion["family_expansions"]))
    print(all(item["passed"] for item in expansion["expansion_gates"]))
    print(all(item["active"] is False for item in expansion["expansion_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
