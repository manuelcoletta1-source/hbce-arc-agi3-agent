from hbce_arc_agi3.milestone_5_public_repo_release_index import (
    run_public_repo_release_index_pipeline,
)


def main() -> None:
    payload = run_public_repo_release_index_pipeline()
    index = payload["index"]

    print(payload["status"])
    print(payload["index_status"])
    print(payload["validation_status"])
    print(payload["index_id"])
    print(payload["signature"])
    print(index["baseline_commit"])
    print(index["baseline_audit_id"])
    print(index["baseline_audit_signature"])
    print(payload["indexed_artifact_count"])
    print(payload["ready_for_public_index_release"])
    print(payload["kaggle_submission_sent"])
    print(all(item["present"] for item in index["indexed_artifacts"]))
    print(len(index["release_sections"]))
    print(len(index["next_actions"]))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
