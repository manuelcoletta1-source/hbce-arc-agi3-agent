from hbce_arc_agi3.milestone_5_public_safety_boundary_checklist import (
    run_public_safety_boundary_checklist_pipeline,
)


def main() -> None:
    payload = run_public_safety_boundary_checklist_pipeline()
    checklist = payload["checklist"]

    print(payload["status"])
    print(payload["checklist_status"])
    print(payload["validation_status"])
    print(payload["checklist_id"])
    print(payload["signature"])
    print(checklist["baseline_commit"])
    print(checklist["entrypoint_contract_id"])
    print(checklist["entrypoint_contract_signature"])
    print(payload["boundary_flag_count"])
    print(payload["public_safety_assertion_count"])
    print(payload["blocked_action_count"])
    print(payload["allowed_action_count"])
    print(payload["ready_for_kaggle_submission_preflight_report"])
    print(payload["kaggle_submission_sent"])
    print(all(item["valid"] for item in checklist["boundary_flags"]))
    print(all(item["satisfied"] for item in checklist["public_safety_assertions"]))
    print("kaggle_api_submission" in checklist["mandatory_blocked_actions"])
    print("network_upload" in checklist["mandatory_blocked_actions"])
    print("external_api_call" in checklist["mandatory_blocked_actions"])
    print("secret_or_token_read" in checklist["mandatory_blocked_actions"])
    print("private_core_export" in checklist["mandatory_blocked_actions"])
    print("legal_certification_claim" in checklist["mandatory_blocked_actions"])
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
