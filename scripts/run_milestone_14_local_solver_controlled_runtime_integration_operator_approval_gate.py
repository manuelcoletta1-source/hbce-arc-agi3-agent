from __future__ import annotations

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_operator_approval_gate import (
    PIPELINE_READY,
    TASK_READY,
    write_milestone_14_task_8_operator_approval_gate_artifacts,
)


def main() -> int:
    record, validation, paths = write_milestone_14_task_8_operator_approval_gate_artifacts()

    print(PIPELINE_READY)
    print(TASK_READY)
    print(validation.status)
    print(record.signature)
    print(record.baseline_commit)
    print(record.task_mode)
    print(record.task_verdict)
    print(record.gate_verdict)
    print(record.gate_status)
    print(record.next_stage)
    print(f"source_decision_signature={record.source_decision_signature}")
    print(f"source_decision_baseline_commit={record.source_decision_baseline_commit}")
    print(f"operator_approval_gate_performed={record.operator_approval_gate_performed}")
    print(f"operator_approval_gate_open={record.operator_approval_gate_open}")
    print(f"operator_approval_gate_closed={record.operator_approval_gate_closed}")
    print(f"operator_approval_required={record.operator_approval_required}")
    print(f"operator_approval_received={record.operator_approval_received}")
    print(f"implementation_authorized={record.implementation_authorized}")
    print(f"implementation_blocked={record.implementation_blocked}")
    print(f"implementation_block_reason={record.implementation_block_reason}")
    print(f"gate_check_count={record.gate_check_count}")
    print(f"gate_check_failure_count={record.gate_check_failure_count}")
    print(f"kaggle_score_semantics={record.kaggle_score_semantics}")
    print(f"runtime_activation_performed={record.runtime_activation_performed}")
    print(f"runtime_execution_performed={record.runtime_execution_performed}")
    print(f"implementation_performed={record.implementation_performed}")
    print(f"real_submission_allowed={record.real_submission_allowed}")
    print(paths["json"])
    print(paths["index"])
    print(paths["manifest"])
    print(paths["markdown"])
    print(paths["doc"])

    return 0 if validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
