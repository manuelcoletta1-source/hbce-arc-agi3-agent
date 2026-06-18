from __future__ import annotations

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_closure_review import (
    PIPELINE_READY,
    write_milestone_14_task_10_closure_review_artifacts,
)


def main() -> int:
    review, validation, paths = write_milestone_14_task_10_closure_review_artifacts()

    print(PIPELINE_READY)
    print(review.status)
    print(validation.status)
    print(review.signature)
    print(review.baseline_commit)
    print(review.mode)
    print(review.closure_status)
    print(review.closure_verdict)
    print(review.closure_decision)
    print(review.block_reason)
    print(review.previous_stage)
    print(review.source_operator_gate_stage)
    print(review.source_qiv_stage)
    print(review.next_stage)
    print(f"source_operator_gate_final_baseline_commit={review.source_operator_gate_final_baseline_commit}")
    print(f"source_qiv_final_baseline_commit={review.source_qiv_final_baseline_commit}")
    print(f"source_qiv_final_signature={review.source_qiv_final_signature}")
    print(f"source_authorization_review_final_baseline_commit={review.source_authorization_review_final_baseline_commit}")
    print(f"source_authorization_review_final_signature={review.source_authorization_review_final_signature}")
    print(f"closure_review_performed={review.closure_review_performed}")
    print(f"closure_review_passed={review.closure_review_passed}")
    print(f"review_chain_closed={review.review_chain_closed}")
    print(f"ready_for_final_closure={review.ready_for_final_closure}")
    print(f"implementation_authorized={review.implementation_authorized}")
    print(f"implementation_blocked={review.implementation_blocked}")
    print(f"operator_approval_received={review.operator_approval_received}")
    print(f"qiv_authorizes_implementation={review.qiv_authorizes_implementation}")
    print(f"qiv_overrides_operator_gate={review.qiv_overrides_operator_gate}")
    print(f"runtime_activation_performed={review.runtime_activation_performed}")
    print(f"implementation_performed={review.implementation_performed}")
    print(f"real_submission_allowed={review.real_submission_allowed}")
    print(f"legal_certification={review.legal_certification}")
    print(f"closure_gate_count={review.closure_gate_count}")
    print(f"closure_gate_failure_count={review.closure_gate_failure_count}")
    print(paths["json"])
    print(paths["index"])
    print(paths["manifest"])
    print(paths["markdown"])
    print(paths["doc"])

    return 0 if validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
