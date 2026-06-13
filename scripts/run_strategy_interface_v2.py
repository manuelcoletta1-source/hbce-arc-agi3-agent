from hbce_arc_agi3.strategy_interface_v2 import (
    run_strategy_interface_v2_pipeline,
    validate_strategy_interface_v2_pipeline,
    write_strategy_interface_v2_artifacts,
)


def main() -> None:
    payload = run_strategy_interface_v2_pipeline()
    validation = validate_strategy_interface_v2_pipeline(payload)
    artifacts = write_strategy_interface_v2_artifacts(payload)

    print(payload["status"])
    print(payload["interface_status"])
    print(payload["validation_status"])
    print(validation["status"])
    print(payload["task_id"])
    print(payload["strategy_count"])
    print(payload["candidate_count"])
    print(payload["best_strategy_id"])
    print(payload["best_candidate_signature"])
    print(payload["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
