from __future__ import annotations

from hbce_arc_agi3.qiv_runtime_constraints import (
    QIV_PIPELINE_READY,
    write_qiv_runtime_constraint_link_artifacts,
)


def main() -> int:
    link, validation, paths = write_qiv_runtime_constraint_link_artifacts()

    print(QIV_PIPELINE_READY)
    print(link.status)
    print(validation.status)
    print(link.signature)
    print(link.baseline_commit)
    print(link.source_document_title)
    print(link.source_document_version)
    print(link.source_document_module)
    print(link.previous_stage)
    print(link.link_stage)
    print(link.next_stage)
    print(f"qiv_linked_to_programming={link.qiv_linked_to_programming}")
    print(f"qiv_linked_to_training={link.qiv_linked_to_training}")
    print(f"qiv_linked_to_runtime_audit={link.qiv_linked_to_runtime_audit}")
    print(f"qiv_linked_to_fail_closed={link.qiv_linked_to_fail_closed}")
    print(f"qiv_linked_to_arc_agi3_diagnostics={link.qiv_linked_to_arc_agi3_diagnostics}")
    print(f"qiv_is_solver_direct={link.qiv_is_solver_direct}")
    print(f"qiv_changes_runtime_solver={link.qiv_changes_runtime_solver}")
    print(f"qiv_authorizes_implementation={link.qiv_authorizes_implementation}")
    print(f"qiv_overrides_operator_gate={link.qiv_overrides_operator_gate}")
    print(f"runtime_activation_performed={link.runtime_activation_performed}")
    print(f"implementation_performed={link.implementation_performed}")
    print(f"real_submission_allowed={link.real_submission_allowed}")
    print(f"legal_certification={link.legal_certification}")
    print(paths["json"])
    print(paths["index"])
    print(paths["manifest"])
    print(paths["markdown"])
    print(paths["doc"])

    return 0 if validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
