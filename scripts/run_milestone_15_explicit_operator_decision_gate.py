from __future__ import annotations

from hbce_arc_agi3.milestone_15_explicit_operator_decision_gate import (
    PIPELINE_READY,
    write_milestone_15_task_1_decision_gate_artifacts,
)


def main() -> int:
    gate, validation, paths = write_milestone_15_task_1_decision_gate_artifacts()

    print(PIPELINE_READY)
    print(gate.status)
    print(validation.status)
    print(gate.signature)
    print(gate.baseline_commit)
    print(gate.mode)
    print(gate.gate_status)
    print(gate.gate_verdict)
    print(gate.gate_decision)
    print(gate.block_reason)
    print(gate.previous_stage)
    print(gate.source_milestone_14_final_closure)
    print(gate.next_stage)
    print(f"source_milestone_14_final_baseline_commit={gate.source_milestone_14_final_baseline_commit}")
    print(f"source_milestone_14_final_signature={gate.source_milestone_14_final_signature}")
    print(f"milestone_15_opened={gate.milestone_15_opened}")
    print(f"explicit_operator_decision_gate_created={gate.explicit_operator_decision_gate_created}")
    print(f"operator_decision_required={gate.operator_decision_required}")
    print(f"operator_decision_received={gate.operator_decision_received}")
    print(f"operator_decision_value={gate.operator_decision_value}")
    print(f"operator_decision_recorded={gate.operator_decision_recorded}")
    print(f"no_implicit_authorization={gate.no_implicit_authorization}")
    print(f"implementation_authorized={gate.implementation_authorized}")
    print(f"implementation_blocked={gate.implementation_blocked}")
    print(f"runtime_activation_authorized={gate.runtime_activation_authorized}")
    print(f"runtime_activation_performed={gate.runtime_activation_performed}")
    print(f"implementation_performed={gate.implementation_performed}")
    print(f"real_submission_allowed={gate.real_submission_allowed}")
    print(f"legal_certification={gate.legal_certification}")
    print(f"decision_gate_check_count={gate.decision_gate_check_count}")
    print(f"decision_gate_failure_count={gate.decision_gate_failure_count}")
    print(paths["json"])
    print(paths["index"])
    print(paths["manifest"])
    print(paths["markdown"])
    print(paths["doc"])

    return 0 if validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
