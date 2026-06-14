from hbce_arc_agi3.candidate_ranker import (
    run_candidate_ranker_pipeline,
    write_candidate_ranker_artifacts,
)


def main() -> None:
    payload = run_candidate_ranker_pipeline()
    artifacts = write_candidate_ranker_artifacts(payload)
    report = payload["ranking_report"]

    print(payload["status"])
    print(payload["ranker_status"])
    print(payload["validation_status"])
    print(report["ranking_id"])
    print(report["generation_id"])
    print(payload["candidate_count"])
    print(payload["best_candidate_type"])
    print(payload["best_candidate_score"])
    print(payload["best_candidate_matches_expected_smoke"])
    print(payload["evidence_score"])
    print(payload["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
