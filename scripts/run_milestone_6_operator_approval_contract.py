from hbce_arc_agi3.milestone_6_operator_approval_contract import (
    run_milestone_6_operator_approval_contract_pipeline,
)


def main() -> None:
    payload = run_milestone_6_operator_approval_contract_pipeline()
    contract = payload["contract"]

    print(payload["status"])
    print(payload["contract_status"])
    print(payload["validation_status"])
    print(payload["contract_id"])
    print(payload["signature"])
    print(contract["baseline_commit"])
    print(contract["decision_layer_id"])
    print(payload["contract_mode"])
    print(payload["contract_verdict"])
    print(payload["required_declaration_count"])
    print(payload["provided_declaration_count"])
    print(payload["accepted_declaration_count"])
    print(payload["contract_gate_count"])
    print(payload["passed_gate_count"])
    print(payload["contract_issue_count"])
    print(payload["warning_count"])
    print(payload["operator_approval_contract_ready"])
    print(payload["operator_approval_required"])
    print(payload["operator_approval_granted"])
    print(payload["operator_approval_received"])
    print(payload["real_submission_allowed"])
    print(payload["ready_for_real_kaggle_submission"])
    print(payload["real_submission_created"])
    print(payload["kaggle_submission_sent"])
    print(payload["upload_performed"])
    print(all(item["provided"] is False for item in contract["contract_record"]["required_declarations"]))
    print(all(item["accepted"] is False for item in contract["contract_record"]["required_declarations"]))
    print(all(item["passed"] for item in contract["contract_gates"]))
    print(all(item["active"] is False for item in contract["contract_issues"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["artifacts"]["index_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
