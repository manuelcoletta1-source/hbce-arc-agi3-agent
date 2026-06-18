from __future__ import annotations

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_implementation_authorization_review import (
    PIPELINE_READY,
    write_milestone_14_task_9_authorization_review_artifacts,
)


def main() -> int:
    review, validation, paths = write_milestone_14_task_9_authorization_review_artifacts()

    print(PIPELINE_READY)
    print(review.status)
    print(validation.status)
    print(review.signature)
    print(review.baseline_commit)
    print(review.mode)
    print(review.review_status)
    print(review.review_verdict)
    print(review.authorization_status)
    print(review.block_reason)
    print(review.previous_stage)
    print(review.qiv_stage)
    print(review.next_stage)
    print(f"source_gate_final_baseline_commit={review.source_gate_final_baseline_commit}")
    print(f"source_qiv_final_baseline_commit={review.source_qiv_final_baseline_commit}")
    print(f"source_qiv_final_signature={review.source_qiv_final_signature}")
    print(f"authorization_review_performed={review.authorization_review_performed}")
    print(f"authorization_review_passed={review.authorization_review_passed}")
    print(f"implementation_authorized={review.implementation_authorized}")
    print(f"implementation_blocked={review.implementation_blocked}")
    print(f"operator_approval_required={review.operator_approval_required}")
    print(f"operator_approval_received={review.operator_approval_received}")
    print(f"operator_approval_gate_closed={review.operator_approval_gate_closed}")
    print(f"qiv_constraint_link_present={review.qiv_constraint_link_present}")
    print(f"qiv_authorizes_implementation={review.qiv_authorizes_implementation}")
    print(f"qiv_overrides_operator_gate={review.qiv_overrides_operator_gate}")
    print(f"runtime_activation_performed={review.runtime_activation_performed}")
    print(f"implementation_performed={review.implementation_performed}")
    print(f"real_submission_allowed={review.real_submission_allowed}")
    print(f"legal_certification={review.legal_certification}")
    print(f"review_gate_count={review.review_gate_count}")
    print(f"review_gate_failure_count={review.review_gate_failure_count}")
    print(paths["json"])
    print(paths["index"])
    print(paths["manifest"])
    print(paths["markdown"])
    print(paths["doc"])

    return 0 if validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
