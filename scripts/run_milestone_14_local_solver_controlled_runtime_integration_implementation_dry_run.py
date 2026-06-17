from __future__ import annotations

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_implementation_dry_run import (
    PIPELINE_READY,
    TASK_READY,
    write_milestone_14_task_5_dry_run_artifacts,
)


def main() -> int:
    record, validation, paths = write_milestone_14_task_5_dry_run_artifacts()

    print(PIPELINE_READY)
    print(TASK_READY)
    print(validation.status)
    print(record.signature)
    print(record.baseline_commit)
    print(record.task_mode)
    print(record.task_verdict)
    print(record.dry_run_verdict)
    print(record.next_stage)
    print(f"implementation_dry_run_performed={record.implementation_dry_run_performed}")
    print(f"dry_run_projection_created={record.dry_run_projection_created}")
    print(f"target_module_count={record.target_module_count}")
    print(f"implementation_step_count={record.implementation_step_count}")
    print(f"integration_contract_count={record.integration_contract_count}")
    print(f"regression_test_count={record.regression_test_count}")
    print(f"rollback_item_count={record.rollback_item_count}")
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
