from hbce_arc_agi3.milestone_5_submission_entrypoint_contract import (
    run_submission_entrypoint_contract_pipeline,
)


def main() -> None:
    payload = run_submission_entrypoint_contract_pipeline()
    contract = payload["contract"]

    print(payload["status"])
    print(payload["contract_status"])
    print(payload["validation_status"])
    print(payload["contract_id"])
    print(payload["signature"])
    print(contract["baseline_commit"])
    print(contract["dry_run_package_id"])
    print(contract["dry_run_package_signature"])
    print(payload["entrypoint_name"])
    print(payload["entrypoint_mode"])
    print(payload["entrypoint_runtime"])
    print(payload["expected_output_file"])
    print(payload["blocked_action_count"])
    print(payload["allowed_action_count"])
    print(payload["ready_for_local_submission_smoke_test"])
    print(payload["kaggle_submission_sent"])
    print("kaggle_api_submission" in contract["blocked_actions"])
    print("network_upload" in contract["blocked_actions"])
    print("external_api_call" in contract["blocked_actions"])
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["artifacts"]["manifest_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
