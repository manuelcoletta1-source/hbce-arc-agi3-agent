from hbce_arc_agi3.milestone_5_public_readiness_audit import (
    run_public_readiness_baseline_audit_pipeline,
)


def main() -> None:
    payload = run_public_readiness_baseline_audit_pipeline()
    audit = payload["audit"]

    print(payload["status"])
    print(payload["audit_status"])
    print(payload["validation_status"])
    print(payload["audit_id"])
    print(payload["signature"])
    print(audit["baseline_commit"])
    print(audit["prior_closure_id"])
    print(audit["prior_closure_signature"])
    print(payload["ready_for_public_readiness_phase"])
    print(payload["kaggle_submission_sent"])
    print(len(audit["required_artifacts"]))
    print(all(audit["required_artifacts"].values()))
    print(len(audit["checks"]))
    print(all(audit["checks"].values()))
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
