from hbce_arc_agi3.candidate_generator import (
    run_candidate_generator_pipeline,
    write_candidate_generator_artifacts,
)


def main() -> None:
    payload = run_candidate_generator_pipeline()
    artifacts = write_candidate_generator_artifacts(payload)
    report = payload["generation_report"]

    print(payload["status"])
    print(payload["generator_status"])
    print(payload["validation_status"])
    print(report["generation_id"])
    print(payload["candidate_count"])
    print(payload["best_candidate_type"])
    print(payload["best_candidate_matches_expected_smoke"])
    print(payload["best_candidate_signature"])
    print(payload["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
