"""Milestone #18 Task 3 - Controlled Technical Solver Limitation Inventory Review v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_18_TASK_3_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

REVIEW_MARKER = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_READY"
REVIEW_VERDICT = "CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_PASS_NO_IMPLEMENTATION"
REVIEW_DECISION = "REVIEW_AND_CONFIRM_SOLVER_LIMITATION_INVENTORY_PLAN_ONLY"
REVIEW_REASON = "TASK_2_LIMITATION_INVENTORY_REQUIRES_REVIEW_BEFORE_TECHNICAL_MAPPING"

MILESTONE_18_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

SOURCE_TASK_2_COMMIT = "34372a5"
SOURCE_TASK_2_SIGNATURE = "15D8A0172179B3EB"
SOURCE_TASK_2_STAGE = "MILESTONE_18_TASK_2_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_V1"

PREVIOUS_STAGE = SOURCE_TASK_2_STAGE
NEXT_STAGE = "MILESTONE_18_TASK_4_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_V1"

TASK_MODE = (
    "MILESTONE_18_TASK_3_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_V1_"
    "REVIEW_ONLY_LOCAL_ONLY"
)

REVIEW_SCOPE = "CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_ONLY"
MILESTONE_18_SCOPE = "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"
RUNTIME_AUTHORIZATION_SCOPE = "NOT_GRANTED"
SUBMISSION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

ARTIFACT_DIR = Path("examples/milestone-18/controlled-technical-solver-limitation-inventory-review-v1")
DOC_PATH = Path("docs/milestone-18-controlled-technical-solver-limitation-inventory-review-v1.md")


REVIEW_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "review_id": "M18-REV-1",
        "source_limitation_id": "M18-LIM-1",
        "area": "solver coverage",
        "review_status": "CONFIRMED",
        "review_note": "Solver coverage limitation is valid and must precede implementation planning.",
        "blocking_issue": False,
        "implementation_authorized": False,
    },
    {
        "review_id": "M18-REV-2",
        "source_limitation_id": "M18-LIM-2",
        "area": "candidate generation",
        "review_status": "CONFIRMED",
        "review_note": "Candidate generator limitation is valid and should feed controlled improvement mapping.",
        "blocking_issue": False,
        "implementation_authorized": False,
    },
    {
        "review_id": "M18-REV-3",
        "source_limitation_id": "M18-LIM-3",
        "area": "ranker evidence",
        "review_status": "CONFIRMED",
        "review_note": "Ranker evidence limitation is valid and should remain evidence-first.",
        "blocking_issue": False,
        "implementation_authorized": False,
    },
    {
        "review_id": "M18-REV-4",
        "source_limitation_id": "M18-LIM-4",
        "area": "local diagnostics",
        "review_status": "CONFIRMED",
        "review_note": "Local diagnostics limitation is valid and protects deterministic regression behavior.",
        "blocking_issue": False,
        "implementation_authorized": False,
    },
    {
        "review_id": "M18-REV-5",
        "source_limitation_id": "M18-LIM-5",
        "area": "submission discipline",
        "review_status": "CONFIRMED",
        "review_note": "Submission discipline limitation is valid and prevents format readiness from becoming score claim theater.",
        "blocking_issue": False,
        "implementation_authorized": False,
    },
    {
        "review_id": "M18-REV-6",
        "source_limitation_id": "M18-LIM-6",
        "area": "authorization boundary",
        "review_status": "CONFIRMED",
        "review_note": "Authorization boundary limitation is valid and keeps implementation/runtime/submission blocked.",
        "blocking_issue": False,
        "implementation_authorized": False,
    },
)

REVIEW_GATES: tuple[str, ...] = (
    "source_task_2_commit_bound",
    "source_task_2_signature_bound",
    "source_task_2_stage_bound",
    "milestone_18_name_confirmed",
    "previous_stage_task_2_inventory",
    "next_stage_candidate_generator_map_declared",
    "review_scope_confirmed",
    "milestone_18_scope_plan_only",
    "implementation_authorization_not_granted",
    "runtime_authorization_not_granted",
    "submission_authorization_not_granted",
    "review_ready",
    "review_passed",
    "review_locked",
    "review_count_six",
    "all_review_items_have_ids",
    "all_review_items_have_source_limitation_ids",
    "all_review_items_confirmed",
    "blocking_issue_count_zero",
    "all_review_items_no_implementation",
    "solver_coverage_review_confirmed",
    "candidate_generation_review_confirmed",
    "ranker_evidence_review_confirmed",
    "local_diagnostics_review_confirmed",
    "submission_discipline_review_confirmed",
    "authorization_boundary_review_confirmed",
    "review_only_true",
    "planning_only_true",
    "implementation_not_authorized",
    "implementation_blocked",
    "implementation_not_performed",
    "runtime_solver_patch_not_allowed",
    "runtime_solver_not_modified",
    "candidate_generator_patch_not_allowed",
    "candidate_generator_not_modified",
    "ranker_patch_not_allowed",
    "ranker_not_modified",
    "runtime_wiring_not_allowed",
    "runtime_wiring_not_performed",
    "runtime_activation_not_authorized",
    "runtime_activation_not_performed",
    "runtime_execution_not_allowed",
    "runtime_execution_not_performed",
    "real_evaluation_not_allowed",
    "real_submission_not_allowed",
    "manual_upload_not_allowed",
    "upload_not_performed",
    "kaggle_authentication_not_allowed",
    "kaggle_authentication_not_performed",
    "kaggle_submission_not_sent",
    "competitive_score_claim_not_allowed",
    "official_score_claim_not_allowed",
    "private_core_not_exposed",
    "legal_certification_false",
    "fail_closed_required",
    "fail_closed_active",
    "local_only_true",
    "deterministic_true",
    "public_safe_true",
    "external_api_dependency_false",
    "internet_during_eval_false",
    "artifact_set_declared",
    "artifact_count_five",
    "manifest_created",
    "index_created",
    "markdown_created",
    "json_payload_created",
    "docs_payload_created",
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_milestone_18_controlled_technical_solver_limitation_inventory_review() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_task_2_commit": SOURCE_TASK_2_COMMIT,
        "source_task_2_signature": SOURCE_TASK_2_SIGNATURE,
        "review_scope": REVIEW_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "review_count": len(REVIEW_ITEMS),
        "verdict": REVIEW_VERDICT,
        "decision": REVIEW_DECISION,
        "reason": REVIEW_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-review-v1.json"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-review-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-review-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-review-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "review_marker": REVIEW_MARKER,
        "signature": signature,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_task_2_commit": SOURCE_TASK_2_COMMIT,
        "source_task_2_signature": SOURCE_TASK_2_SIGNATURE,
        "source_task_2_stage": SOURCE_TASK_2_STAGE,
        "task_mode": TASK_MODE,
        "verdict": REVIEW_VERDICT,
        "decision": REVIEW_DECISION,
        "review_reason": REVIEW_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "review_scope": REVIEW_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "runtime_authorization_scope": RUNTIME_AUTHORIZATION_SCOPE,
        "submission_authorization_scope": SUBMISSION_AUTHORIZATION_SCOPE,
        "controlled_technical_solver_limitation_inventory_review_ready": True,
        "controlled_technical_solver_limitation_inventory_review_passed": True,
        "controlled_technical_solver_limitation_inventory_review_locked": True,
        "review_only": True,
        "planning_only": True,
        "review_count": len(REVIEW_ITEMS),
        "blocking_issue_count": 0,
        "review_items": REVIEW_ITEMS,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "runtime_solver_patch_allowed": False,
        "runtime_solver_modified": False,
        "candidate_generator_patch_allowed": False,
        "candidate_generator_modified": False,
        "ranker_patch_allowed": False,
        "ranker_modified": False,
        "runtime_wiring_allowed": False,
        "runtime_wiring_performed": False,
        "runtime_activation_authorized": False,
        "runtime_activation_performed": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
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
        "review_gate_count": len(REVIEW_GATES),
        "review_gate_failure_count": 0,
        "review_gates": REVIEW_GATES,
        "artifacts": artifacts,
    }


def validate_milestone_18_controlled_technical_solver_limitation_inventory_review(
    status: dict[str, Any],
) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "review_marker": REVIEW_MARKER,
        "milestone_18_name": MILESTONE_18_NAME,
        "source_task_2_commit": SOURCE_TASK_2_COMMIT,
        "source_task_2_signature": SOURCE_TASK_2_SIGNATURE,
        "source_task_2_stage": SOURCE_TASK_2_STAGE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "review_scope": REVIEW_SCOPE,
        "milestone_18_scope": MILESTONE_18_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "runtime_authorization_scope": RUNTIME_AUTHORIZATION_SCOPE,
        "submission_authorization_scope": SUBMISSION_AUTHORIZATION_SCOPE,
        "verdict": REVIEW_VERDICT,
        "decision": REVIEW_DECISION,
        "review_reason": REVIEW_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    required_true = (
        "controlled_technical_solver_limitation_inventory_review_ready",
        "controlled_technical_solver_limitation_inventory_review_passed",
        "controlled_technical_solver_limitation_inventory_review_locked",
        "review_only",
        "planning_only",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
        "local_only",
        "deterministic",
        "public_safe",
    )
    required_false = (
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
        "candidate_generator_patch_allowed",
        "candidate_generator_modified",
        "ranker_patch_allowed",
        "ranker_modified",
        "runtime_wiring_allowed",
        "runtime_wiring_performed",
        "runtime_activation_authorized",
        "runtime_activation_performed",
        "runtime_execution_allowed",
        "runtime_execution_performed",
        "real_evaluation_allowed",
        "real_submission_allowed",
        "manual_upload_allowed",
        "upload_performed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_submission_sent",
        "competitive_score_claim_allowed",
        "official_score_claim_allowed",
        "private_core_exposure",
        "legal_certification",
        "external_api_dependency",
        "internet_during_eval",
    )

    for key in required_true:
        if status.get(key) is not True:
            issues.append(f"{key} must be True")
    for key in required_false:
        if status.get(key) is not False:
            issues.append(f"{key} must be False")

    items = tuple(status.get("review_items", ()))
    if status.get("review_count") != 6:
        issues.append("review_count must be 6")
    if len(items) != 6:
        issues.append("review_items length must be 6")
    if status.get("blocking_issue_count") != 0:
        issues.append("blocking_issue_count must be 0")

    for item in items:
        for key in ("review_id", "source_limitation_id", "area", "review_status", "review_note"):
            if not item.get(key):
                issues.append(f"{item.get('review_id')} missing {key}")
        if item.get("review_status") != "CONFIRMED":
            issues.append(f"{item.get('review_id')} review_status must be CONFIRMED")
        if item.get("blocking_issue") is not False:
            issues.append(f"{item.get('review_id')} blocking_issue must be False")
        if item.get("implementation_authorized") is not False:
            issues.append(f"{item.get('review_id')} implementation_authorized must be False")

    if status.get("review_gate_count") != len(REVIEW_GATES):
        issues.append("review_gate_count mismatch")
    if status.get("review_gate_failure_count") != 0:
        issues.append("review_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def review_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["review_marker"],
        "signature": status["signature"],
        "milestone_18_name": status["milestone_18_name"],
        "source_task_2_commit": status["source_task_2_commit"],
        "source_task_2_signature": status["source_task_2_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "review_scope": status["review_scope"],
        "milestone_18_scope": status["milestone_18_scope"],
        "review_only": status["review_only"],
        "planning_only": status["planning_only"],
        "review_count": status["review_count"],
        "blocking_issue_count": status["blocking_issue_count"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "review_gate_count": status["review_gate_count"],
        "review_gate_failure_count": status["review_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["review_marker"],
        f"signature={status['signature']}",
        f"milestone_18_name={status['milestone_18_name']}",
        f"source_task_2_commit={status['source_task_2_commit']}",
        f"source_task_2_signature={status['source_task_2_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"review_reason={status['review_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"review_scope={status['review_scope']}",
        f"milestone_18_scope={status['milestone_18_scope']}",
        f"review_only={status['review_only']}",
        f"planning_only={status['planning_only']}",
        f"review_count={status['review_count']}",
        f"blocking_issue_count={status['blocking_issue_count']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"review_gate_count={status['review_gate_count']}",
        f"review_gate_failure_count={status['review_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def build_markdown(status: dict[str, Any]) -> str:
    review_lines = "\n".join(
        (
            f"- `{item['review_id']}` reviews `{item['source_limitation_id']}` "
            f"({item['area']}): `{item['review_status']}`. "
            f"{item['review_note']} blocking_issue=`{item['blocking_issue']}` "
            f"implementation_authorized=`{item['implementation_authorized']}`"
        )
        for item in status["review_items"]
    )

    return f"""# Milestone #18 Task 3 - Controlled Technical Solver Limitation Inventory Review v1

## Status

`{status["review_marker"]}`

## Source binding

- source Task 2 commit: `{status["source_task_2_commit"]}`
- source Task 2 signature: `{status["source_task_2_signature"]}`
- source stage: `{status["source_task_2_stage"]}`
- previous stage: `{status["previous_stage"]}`
- next stage: `{status["next_stage"]}`

## Review

- review_scope: `{status["review_scope"]}`
- milestone_18_scope: `{status["milestone_18_scope"]}`
- review_only: `{status["review_only"]}`
- planning_only: `{status["planning_only"]}`
- review_count: `{status["review_count"]}`
- blocking_issue_count: `{status["blocking_issue_count"]}`

{review_lines}

## Boundary

This limitation inventory review authorizes review and planning only.
It does not authorize implementation.
It does not authorize runtime execution.
It does not authorize real evaluation.
It does not authorize Kaggle authentication, upload, or submission.
It does not authorize competitive or official score claims.
It does not expose private HBCE/JOKER-C2 core material.

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`
"""


def write_milestone_18_controlled_technical_solver_limitation_inventory_review_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_milestone_18_controlled_technical_solver_limitation_inventory_review()
    issues = validate_milestone_18_controlled_technical_solver_limitation_inventory_review(resolved)
    if issues:
        raise ValueError(
            "Invalid milestone 18 controlled technical solver limitation inventory review: "
            + "; ".join(issues)
        )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = review_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    manifest = build_manifest(resolved)
    markdown = build_markdown(resolved)

    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-review-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-review-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-review-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-18-controlled-technical-solver-limitation-inventory-review-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_milestone_18_controlled_technical_solver_limitation_inventory_review_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_2_commit"])
    print(status["task_mode"])
    print(status["review_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["review_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "milestone_18_name",
        "source_task_2_commit",
        "source_task_2_signature",
        "review_scope",
        "milestone_18_scope",
        "review_only",
        "planning_only",
        "review_count",
        "blocking_issue_count",
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_blocked",
        "implementation_performed",
        "runtime_execution_allowed",
        "runtime_execution_performed",
        "real_evaluation_allowed",
        "real_submission_allowed",
        "manual_upload_allowed",
        "upload_performed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_submission_sent",
        "competitive_score_claim_allowed",
        "official_score_claim_allowed",
        "private_core_exposure",
        "legal_certification",
        "fail_closed_required",
        "fail_closed_active",
        "local_only",
        "deterministic",
        "public_safe",
        "external_api_dependency",
        "internet_during_eval",
        "review_gate_count",
        "review_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for item in status["review_items"]:
        print(
            f"review_item={item['review_id']}|{item['source_limitation_id']}|{item['area']}|"
            f"{item['review_status']}|blocking_issue={item['blocking_issue']}|"
            f"implementation_authorized={item['implementation_authorized']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
