from __future__ import annotations

from hbce_arc_agi3.milestone_15_operator_decision_record import (
    PIPELINE_READY,
    write_milestone_15_task_2_operator_decision_record_artifacts,
)


def main() -> int:
    record, validation, paths = write_milestone_15_task_2_operator_decision_record_artifacts()

    print(PIPELINE_READY)
    print(record.status)
    print(validation.status)
    print(record.signature)
    print(record.baseline_commit)
    print(record.mode)
    print(record.record_status)
    print(record.record_verdict)
    print(record.record_decision)
    print(record.block_reason)
    print(record.previous_stage)
    print(record.next_stage)
    print(f"source_task_1_final_baseline_commit={record.source_task_1_final_baseline_commit}")
    print(f"source_task_1_final_signature={record.source_task_1_final_signature}")
    print(f"operator_decision_record_created={record.operator_decision_record_created}")
    print(f"operator_decision_required={record.operator_decision_required}")
    print(f"operator_decision_received={record.operator_decision_received}")
    print(f"operator_decision_value={record.operator_decision_value}")
    print(f"operator_decision_recorded={record.operator_decision_recorded}")
    print(f"operator_decision_authorizes_implementation={record.operator_decision_authorizes_implementation}")
    print(f"implementation_authorized={record.implementation_authorized}")
    print(f"implementation_blocked={record.implementation_blocked}")
    print(f"runtime_activation_authorized={record.runtime_activation_authorized}")
    print(f"runtime_activation_performed={record.runtime_activation_performed}")
    print(f"implementation_performed={record.implementation_performed}")
    print(f"real_submission_allowed={record.real_submission_allowed}")
    print(f"legal_certification={record.legal_certification}")
    print(f"decision_record_check_count={record.decision_record_check_count}")
    print(f"decision_record_failure_count={record.decision_record_failure_count}")
    print(paths["json"])
    print(paths["index"])
    print(paths["manifest"])
    print(paths["markdown"])
    print(paths["doc"])

    return 0 if validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
