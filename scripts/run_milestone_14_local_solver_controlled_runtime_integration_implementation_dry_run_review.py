from __future__ import annotations

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_implementation_dry_run_review import (
    PIPELINE_READY,
    TASK_READY,
    write_milestone_14_task_6_dry_run_review_artifacts,
)


def main() -> int:
    record, validation, paths = write_milestone_14_task_6_dry_run_review_artifacts()

    print(PIPELINE_READY)
    print(TASK_READY)
    print(validation.status)
    print(record.signature)
    print(record.baseline_commit)
    print(record.task_mode)
    print(record.task_verdict)
    print(record.review_verdict)
    print(record.next_stage)
    print(f"source_dry_run_signature={record.source_dry_run_signature}")
    print(f"source_dry_run_baseline_commit={record.source_dry_run_baseline_commit}")
    print(f"dry_run_review_performed={record.dry_run_review_performed}")
    print(f"dry_run_review_passed={record.dry_run_review_passed}")
    print(f"ready_for_review_decision={record.ready_for_review_decision}")
    print(f"review_gate_count={record.review_gate_count}")
    print(f"review_gate_failure_count={record.review_gate_failure_count}")
    print(f"kaggle_score_semantics={record.kaggle_score_semantics}")
    print(f"runtime_activation_performed={record.runtime_activation_performed}")
    print(f"runtime_execution_performed={record.runtime_execution_performed}")
    print(f"implementation_performed={record.implementation_performed}")
    print(f"implementation_review_decision_performed={record.implementation_review_decision_performed}")
    print(f"real_submission_allowed={record.real_submission_allowed}")
    print(paths["json"])
    print(paths["index"])
    print(paths["manifest"])
    print(paths["markdown"])
    print(paths["doc"])

    return 0 if validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
