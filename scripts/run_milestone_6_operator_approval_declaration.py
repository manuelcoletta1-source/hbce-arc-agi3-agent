from hbce_arc_agi3.milestone_6_operator_approval_declaration import (
    run_milestone_6_operator_approval_declaration_pipeline,
)


def main() -> None:
    payload = run_milestone_6_operator_approval_declaration_pipeline()
    declaration = payload["declaration"]

    print(payload["status"])
    print(payload["declaration_status"])
    print(payload["validation_status"])
    print(payload["declaration_id"])
    print(payload["signature"])
    print(declaration["baseline_commit"])
    print(declaration["operator_approval_contract_id"])
    print(payload["declaration_mode"])
    print(payload["declaration_verdict"])
    print(payload["required_declaration_count"])
    print(payload["declared_declaration_count"])
    print(payload["provided_declaration_count"])
    print(payload["accepted_declaration_count"])
    print(payload["declaration_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["declaration_issue_count"])
    print(payload["warning_count"])
    print(payload["operator_approval_declaration_ready"])
    print(payload["operator_approval_declared"])
    print(payload["operator_approval_received"])
    print(payload["operator_approval_granted"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(payload["precheck_gate_required"])
    print(all(item["declared"] for item in declaration["declaration_record"]["declared_operator_declarations"]))
    print(all(item["accepted"] for item in declaration["declaration_record"]["declared_operator_declarations"]))
    print(all(item["passed"] for item in declaration["declaration_gates"]))
    print(all(item["active"] is False for item in declaration["declaration_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
