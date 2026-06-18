from __future__ import annotations

from hbce_arc_agi3.milestone_15_operator_decision_authorization_boundary import (
    PIPELINE_READY,
    write_milestone_15_task_3_authorization_boundary_artifacts,
)


def main() -> int:
    boundary, validation, paths = write_milestone_15_task_3_authorization_boundary_artifacts()

    print(PIPELINE_READY)
    print(boundary.status)
    print(validation.status)
    print(boundary.signature)
    print(boundary.baseline_commit)
    print(boundary.mode)
    print(boundary.boundary_status)
    print(boundary.boundary_verdict)
    print(boundary.boundary_decision)
    print(boundary.block_reason)
    print(boundary.previous_stage)
    print(boundary.next_stage)
    print(f"source_task_2_final_baseline_commit={boundary.source_task_2_final_baseline_commit}")
    print(f"source_task_2_final_signature={boundary.source_task_2_final_signature}")
    print(f"operator_decision_required={boundary.operator_decision_required}")
    print(f"operator_decision_received={boundary.operator_decision_received}")
    print(f"operator_decision_value={boundary.operator_decision_value}")
    print(f"pending_decision_is_authorization={boundary.pending_decision_is_authorization}")
    print(f"operator_decision_authorizes_implementation={boundary.operator_decision_authorizes_implementation}")
    print(f"explicit_authorization_required={boundary.explicit_authorization_required}")
    print(f"explicit_authorization_received={boundary.explicit_authorization_received}")
    print(f"implementation_authorized={boundary.implementation_authorized}")
    print(f"implementation_blocked={boundary.implementation_blocked}")
    print(f"runtime_activation_authorized={boundary.runtime_activation_authorized}")
    print(f"runtime_activation_performed={boundary.runtime_activation_performed}")
    print(f"implementation_performed={boundary.implementation_performed}")
    print(f"real_submission_allowed={boundary.real_submission_allowed}")
    print(f"legal_certification={boundary.legal_certification}")
    print(f"authorization_boundary_check_count={boundary.authorization_boundary_check_count}")
    print(f"authorization_boundary_failure_count={boundary.authorization_boundary_failure_count}")
    print(paths["json"])
    print(paths["index"])
    print(paths["manifest"])
    print(paths["markdown"])
    print(paths["doc"])

    return 0 if validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
