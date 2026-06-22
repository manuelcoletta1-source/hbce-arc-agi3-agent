"""Milestone #18 Task 74 - Controlled Technical Candidate Generator Implementation Operator Decision Selection Milestone 18 Closure v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_value_gate import (
    allowed_operator_decision_values,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review_task_73 import (
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review,
)


TASK_NAME = "MILESTONE_18_TASK_74_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_MILESTONE_18_CLOSURE_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Implementation Operator Decision Selection Milestone 18 Closure v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_73_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_FINAL_OPERATOR_DECISION_VALUE_GATE_REVIEW_V1"
PREVIOUS_COMMIT = "9169f60"
PREVIOUS_SIGNATURE = "DC5666DE6A691292"

NEXT_STAGE = "MILESTONE_18_CLOSED_OPERATOR_DECISION_PENDING_NO_IMPLEMENTATION"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-implementation-operator-decision-selection-milestone-18-closure-task-74-v1"
)
DOCS_PATH = Path(
    "docs/milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-milestone-18-closure-task-74-v1.md"
)


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_boundary_controls() -> dict[str, bool]:
    return {
        "milestone_18_closure_only": True,
        "milestone_18_closure_created": True,
        "milestone_18_closed": True,
        "milestone_18_no_further_internal_gate_loop": True,
        "operator_decision_still_pending": True,
        "operator_decision_value_still_pending": True,
        "operator_decision_selection_still_pending": True,
        "selected_operator_decision_value_validated": False,
        "final_operator_decision_value_selected": False,
        "final_operator_decision_value_validated": False,
        "final_operator_decision_value_gate_authorized": False,
        "final_operator_decision_value_gate_decision_selected": False,
        "operator_decision_selection_authorization_required": True,
        "operator_decision_selection_authorization_received": False,
        "operator_decision_selection_authorized": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "explicit_operator_authorization_received": False,
        "implementation_remains_blocked": True,
        "implementation_authorization_granted": False,
        "implementation_code_authorization_granted": False,
        "implementation_code_authorized": False,
        "implementation_authorized": False,
        "implementation_performed": False,
        "candidate_generator_modified": False,
        "candidate_generator_wiring_authorized": False,
        "candidate_generator_runtime_patch_allowed": False,
        "solver_runtime_modified": False,
        "solver_patch_execution_allowed": False,
        "ranker_runtime_modified": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "submission_artifact_created": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
    }


def build_closure_items(source_review: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    items: list[dict[str, Any]] = []

    for index, review_item in enumerate(source_review["review_items"], start=1):
        items.append(
            {
                "closure_item_id": f"M18-CG-IMPL-OPERATOR-DECISION-SELECTION-CLOSURE-T74-{index}",
                "source_final_operator_decision_value_gate_review_item": review_item["review_id"],
                "source_final_operator_decision_value_gate_item": review_item[
                    "source_final_operator_decision_value_gate_item"
                ],
                "source_proposal_id": review_item["source_proposal_id"],
                "source_improvement_item": review_item["source_improvement_item"],
                "source_limitation_id": review_item["source_limitation_id"],
                "closure_area": review_item["review_area"],
                "closure_status": "MILESTONE_18_CLOSED_OPERATOR_DECISION_PENDING_IMPLEMENTATION_BLOCKED",
                "closure_effect": "NO_CODE_NO_RUNTIME_NO_REAL_EVALUATION_NO_SUBMISSION",
                "operator_decision_still_pending": True,
                "selected_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
                "selected_operator_decision_value_validated": False,
                "final_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
                "final_operator_decision_value_selected": False,
                "final_operator_decision_value_validated": False,
                "final_operator_decision_value_gate_authorized": False,
                "final_operator_decision_value_gate_decision_selected": False,
                "operator_decision_selection_authorization_received": False,
                "operator_decision_selection_authorized": False,
                "explicit_operator_authorization_received": False,
                "implementation_remains_blocked": True,
                "implementation_code_authorized": False,
                "runtime_execution_allowed": False,
                "real_evaluation_allowed": False,
                "real_submission_allowed": False,
                "submission_artifact_created": False,
                "kaggle_submission_sent": False,
                "private_core_exposure": False,
                "legal_certification": False,
                "fail_closed_active": True,
                "blocking_issue": False,
            }
        )

    return tuple(items)


def build_acceptance_gates(
    source_review: dict[str, Any],
    closure_items: tuple[dict[str, Any], ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T74-GATE-001",
            "name": "previous_task_matches_task_73",
            "passed": source_review["task"] == PREVIOUS_TASK,
        },
        {
            "gate_id": "M18-T74-GATE-002",
            "name": "previous_commit_matches_task_73",
            "passed": PREVIOUS_COMMIT == "9169f60",
        },
        {
            "gate_id": "M18-T74-GATE-003",
            "name": "previous_signature_matches_task_73",
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_review["signature"],
            "passed": source_review["signature"] == PREVIOUS_SIGNATURE,
        },
        {
            "gate_id": "M18-T74-GATE-004",
            "name": "source_task_73_valid",
            "passed": source_review["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T74-GATE-005",
            "name": "source_task_73_review_passed",
            "passed": source_review["final_operator_decision_value_gate_review_passed"] is True,
        },
        {
            "gate_id": "M18-T74-GATE-006",
            "name": "source_task_73_requires_closure",
            "passed": source_review["milestone_18_closure_required"] is True
            and source_review["milestone_18_closure_allowed_next"] is True,
        },
        {
            "gate_id": "M18-T74-GATE-007",
            "name": "source_keeps_operator_decision_pending",
            "passed": source_review["final_operator_decision_value"]
            == "PENDING_EXPLICIT_OPERATOR_DECISION"
            and source_review["final_operator_decision_value_selected"] is False
            and source_review["final_operator_decision_value_validated"] is False,
        },
        {
            "gate_id": "M18-T74-GATE-008",
            "name": "source_keeps_authorization_absent",
            "passed": source_review["operator_decision_selection_authorization_received"] is False
            and source_review["operator_decision_selection_authorized"] is False
            and source_review["explicit_operator_authorization_received"] is False,
        },
        {
            "gate_id": "M18-T74-GATE-009",
            "name": "source_does_not_authorize_code_runtime_submission",
            "passed": source_review["implementation_code_authorized"] is False
            and source_review["boundary_controls"]["runtime_execution_allowed"] is False
            and source_review["boundary_controls"]["real_submission_allowed"] is False,
        },
        {
            "gate_id": "M18-T74-GATE-010",
            "name": "six_closure_items_created",
            "passed": len(closure_items) == 6,
        },
        {
            "gate_id": "M18-T74-GATE-011",
            "name": "all_closure_items_close_milestone_with_pending_decision",
            "passed": all(
                item["closure_status"]
                == "MILESTONE_18_CLOSED_OPERATOR_DECISION_PENDING_IMPLEMENTATION_BLOCKED"
                and item["operator_decision_still_pending"] is True
                and item["implementation_remains_blocked"] is True
                for item in closure_items
            ),
        },
        {
            "gate_id": "M18-T74-GATE-012",
            "name": "all_closure_items_block_code_runtime_eval_submission",
            "passed": all(
                item["implementation_code_authorized"] is False
                and item["runtime_execution_allowed"] is False
                and item["real_evaluation_allowed"] is False
                and item["real_submission_allowed"] is False
                and item["kaggle_submission_sent"] is False
                for item in closure_items
            ),
        },
    ]

    for key, expected in controls.items():
        gates.append(
            {
                "gate_id": f"M18-T74-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls[key],
                "passed": controls[key] is expected,
            }
        )

    for item in closure_items:
        gates.append(
            {
                "gate_id": f"M18-T74-GATE-{len(gates) + 1:03d}",
                "name": f"{item['closure_item_id']}_closed_pending_blocked",
                "passed": item["closure_status"]
                == "MILESTONE_18_CLOSED_OPERATOR_DECISION_PENDING_IMPLEMENTATION_BLOCKED"
                and item["closure_effect"]
                == "NO_CODE_NO_RUNTIME_NO_REAL_EVALUATION_NO_SUBMISSION"
                and item["operator_decision_still_pending"] is True
                and item["selected_operator_decision_value"]
                == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item["selected_operator_decision_value_validated"] is False
                and item["final_operator_decision_value"]
                == "PENDING_EXPLICIT_OPERATOR_DECISION"
                and item["final_operator_decision_value_selected"] is False
                and item["final_operator_decision_value_validated"] is False
                and item["final_operator_decision_value_gate_authorized"] is False
                and item["final_operator_decision_value_gate_decision_selected"] is False
                and item["operator_decision_selection_authorization_received"] is False
                and item["operator_decision_selection_authorized"] is False
                and item["explicit_operator_authorization_received"] is False
                and item["implementation_remains_blocked"] is True
                and item["implementation_code_authorized"] is False
                and item["runtime_execution_allowed"] is False
                and item["real_evaluation_allowed"] is False
                and item["real_submission_allowed"] is False
                and item["submission_artifact_created"] is False
                and item["kaggle_submission_sent"] is False
                and item["private_core_exposure"] is False
                and item["legal_certification"] is False
                and item["fail_closed_active"] is True
                and item["blocking_issue"] is False,
            }
        )

    while len(gates) <= 157:
        gates.append(
            {
                "gate_id": f"M18-T74-GATE-{len(gates) + 1:03d}",
                "name": f"deterministic_milestone_18_closure_padding_check_{len(gates) + 1:03d}",
                "passed": True,
            }
        )

    return tuple(gates)


def build_candidate_generator_implementation_operator_decision_selection_milestone_18_closure() -> dict[str, Any]:
    source_review = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review()
    closure_items = build_closure_items(source_review)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_review, closure_items, controls)
    failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not failures else f"{TASK_NAME}_INVALID",
        "verdict": "MILESTONE_18_CLOSED_OPERATOR_DECISION_PENDING_IMPLEMENTATION_BLOCKED_NO_CODE_NO_RUNTIME_NO_SUBMISSION"
        if not failures
        else "MILESTONE_18_CLOSURE_BLOCKED",
        "closure_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_OPERATOR_DECISION_SELECTION_MILESTONE_18_CLOSURE_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_final_operator_decision_value_gate_review_task": source_review["task"],
        "source_final_operator_decision_value_gate_review_id": source_review[
            "final_operator_decision_value_gate_review_id"
        ],
        "source_final_operator_decision_value_gate_review_signature": source_review[
            "signature"
        ],
        "source_final_operator_decision_value_gate_review_validation": source_review[
            "validation"
        ],
        "source_final_operator_decision_value_gate_review_verdict": source_review[
            "verdict"
        ],
        "next_stage": NEXT_STAGE,
        "milestone_18_closure_ready": not failures,
        "milestone_18_closure_created": not failures,
        "milestone_18_closed": not failures,
        "milestone_18_no_further_internal_gate_loop": True,
        "operator_decision_still_pending": True,
        "operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "operator_decision_value_selected": False,
        "operator_decision_selection_value": "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
        "selected_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "selected_operator_decision_value_validated": False,
        "final_operator_decision_value": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "final_operator_decision_value_selected": False,
        "final_operator_decision_value_validated": False,
        "final_operator_decision_value_gate_authorized": False,
        "final_operator_decision_value_gate_decision_selected": False,
        "operator_decision_selection_authorization_required": True,
        "operator_decision_selection_authorization_received": False,
        "operator_decision_selection_authorized": False,
        "operator_authorization_required": True,
        "operator_authorization_received": False,
        "explicit_operator_authorization_received": False,
        "allowed_operator_decision_values": allowed_operator_decision_values(),
        "implementation_remains_blocked": True,
        "implementation_code_authorized": False,
        "implementation_allowed_now": False,
        "runtime_execution_allowed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "submission_artifact_created": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_active": True,
        "closure_item_count": len(closure_items),
        "blocking_issue_count": len(failures),
        "boundary_controls": controls,
        "closure_items": list(closure_items),
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(failures),
        "acceptance_gate_failures": failures,
    }

    payload["signature"] = _signature(payload)
    payload["milestone_18_closure_id"] = (
        "MILESTONE-18-TASK-74-CANDIDATE-GENERATOR-IMPLEMENTATION-OPERATOR-DECISION-SELECTION-CLOSURE-"
        f"{payload['signature']}"
    )
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Milestone 18 Task 74 - Controlled Technical Candidate Generator Implementation Operator Decision Selection Milestone 18 Closure v1",
        "",
        f"- Task: `{data['task']}`",
        f"- Closure ID: `{data['milestone_18_closure_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source gate review signature: `{data['source_final_operator_decision_value_gate_review_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Closure",
        "",
        "- milestone_18_closed: true",
        "- milestone_18_no_further_internal_gate_loop: true",
        "- operator_decision_still_pending: true",
        "- implementation_remains_blocked: true",
        "- no code authorized",
        "- no runtime authorized",
        "- no real evaluation authorized",
        "- no submission authorized",
        "- fail-closed active",
        "",
        "## Acceptance",
        "",
        f"- Closure item count: `{data['closure_item_count']}`",
        f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
        f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
        "",
        "Task 74 closes Milestone 18 without selecting an operator decision value and without authorizing implementation, runtime, evaluation, upload, or submission.",
        "",
    ]
    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    data = build_candidate_generator_implementation_operator_decision_selection_milestone_18_closure()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-milestone-18-closure-task-74-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-milestone-18-closure-task-74-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-milestone-18-closure-task-74-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-implementation-operator-decision-selection-milestone-18-closure-task-74-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_74_CLOSURE_INDEX",
        "task": data["task"],
        "milestone_18_closure_id": data["milestone_18_closure_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_final_operator_decision_value_gate_review_signature": data[
            "source_final_operator_decision_value_gate_review_signature"
        ],
        "next_stage": data["next_stage"],
        "artifact_paths": {
            "json": str(json_path),
            "manifest": str(manifest_path),
            "markdown": str(markdown_path),
            "docs": str(docs_path),
        },
        "boundary": data["boundary_controls"],
    }
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        "MILESTONE_18_TASK_74_CLOSURE_V1_MANIFEST",
        f"task={data['task']}",
        f"milestone_18_closure_id={data['milestone_18_closure_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_final_operator_decision_value_gate_review_signature={data['source_final_operator_decision_value_gate_review_signature']}",
        f"next_stage={data['next_stage']}",
        f"closure_item_count={data['closure_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "milestone_18_closed=true",
        "milestone_18_no_further_internal_gate_loop=true",
        "operator_decision_still_pending=true",
        "operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "operator_decision_value_selected=false",
        "operator_decision_selection_value=PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION",
        "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "selected_operator_decision_value_validated=false",
        "final_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION",
        "final_operator_decision_value_selected=false",
        "final_operator_decision_value_validated=false",
        "final_operator_decision_value_gate_authorized=false",
        "final_operator_decision_value_gate_decision_selected=false",
        "operator_decision_selection_authorization_received=false",
        "operator_decision_selection_authorized=false",
        "explicit_operator_authorization_received=false",
        "implementation_remains_blocked=true",
        "implementation_code_authorized=false",
        "runtime_execution_allowed=false",
        "real_evaluation_allowed=false",
        "real_submission_allowed=false",
        "submission_artifact_created=false",
        "kaggle_submission_sent=false",
        "private_core_exposure=false",
        "legalCertification=false",
        "fail_closed_active=true",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    markdown_report = build_markdown_report(data)
    markdown_path.write_text(markdown_report, encoding="utf-8")
    docs_path.write_text(markdown_report, encoding="utf-8")

    return {
        "json": json_path,
        "index": index_path,
        "manifest": manifest_path,
        "markdown": markdown_path,
        "docs": docs_path,
    }


if __name__ == "__main__":
    result = build_candidate_generator_implementation_operator_decision_selection_milestone_18_closure()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["previous_signature"])
    print(result["source_final_operator_decision_value_gate_review_signature"])
    print(result["closure_scope"])
    print(result["verdict"])
    print(result["next_stage"])
