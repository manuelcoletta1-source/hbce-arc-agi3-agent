"""Milestone #17 Task 9 - Controlled Local Solver Improvement Planning Gate v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_9_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING_GATE_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

PLANNING_GATE_STATUS_MARKER = "MILESTONE_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING_GATE_READY"
PLANNING_GATE_VERDICT = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING_GATE_OPENED_PLANNING_ONLY"
PLANNING_GATE_DECISION = "OPEN_LOCAL_SOLVER_IMPROVEMENT_PLANNING_GATE_NO_IMPLEMENTATION_ALLOWED"
PLANNING_GATE_REASON = "TASK_8_CONFIRMED_M17_OPT_1_PLANNING_ONLY_SELECTION"

PREVIOUS_STAGE = "MILESTONE_17_TASK_8_CONTROLLED_NEXT_PHASE_OPTION_SELECTION_INTAKE_REVIEW_V1"
NEXT_STAGE = "MILESTONE_17_TASK_10_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING_GATE_REVIEW_V1"

SOURCE_TASK_8_FINAL_BASELINE_COMMIT = "193dc54"
SOURCE_TASK_8_FINAL_SIGNATURE = "1620FCAEF23BE9D2"

SELECTED_OPTION_ID = "M17-OPT-1"
SELECTED_OPTION_NAME = "Controlled local solver improvement planning"
SELECTED_OPTION_VALUE = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING"
SELECTED_OPTION_CLASS = "CONTROLLED_PLANNING_ONLY"
SELECTED_OPTION_REVIEW_STATUS = "CONFIRMED_PLANNING_ONLY_SELECTION"

TASK_MODE = (
    "MILESTONE_17_TASK_9_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING_GATE_V1_"
    "PLANNING_GATE_ONLY_LOCAL_ONLY"
)

ARTIFACT_DIR = Path("examples/milestone-17/controlled-local-solver-improvement-planning-gate-v1")
DOC_PATH = Path("docs/milestone-17-controlled-local-solver-improvement-planning-gate-v1.md")


PLANNING_WORKSTREAMS: tuple[dict[str, Any], ...] = (
    {
        "workstream_id": "M17-LSIG-WS-1",
        "name": "Baseline solver limitation review",
        "status": "PLANNING_CANDIDATE",
        "purpose": "Review local solver limits before any implementation proposal.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "workstream_id": "M17-LSIG-WS-2",
        "name": "Local fixture diagnostic plan",
        "status": "PLANNING_CANDIDATE",
        "purpose": "Define diagnostic-only local fixtures and measurement constraints.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "workstream_id": "M17-LSIG-WS-3",
        "name": "Candidate generator improvement planning",
        "status": "PLANNING_CANDIDATE",
        "purpose": "Plan candidate-generation improvements without modifying runtime code.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "workstream_id": "M17-LSIG-WS-4",
        "name": "Ranker evidence planning",
        "status": "PLANNING_CANDIDATE",
        "purpose": "Plan evidence and ranking checks before any ranker change.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "workstream_id": "M17-LSIG-WS-5",
        "name": "Regression measurement plan",
        "status": "PLANNING_CANDIDATE",
        "purpose": "Plan local regression checks and no-score-claim boundaries.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
    {
        "workstream_id": "M17-LSIG-WS-6",
        "name": "Controlled implementation authorization gate plan",
        "status": "PLANNING_CANDIDATE",
        "purpose": "Prepare a future authorization gate, without granting authorization now.",
        "implementation_allowed": False,
        "runtime_allowed": False,
        "submission_allowed": False,
    },
)


PLANNING_GATE_CHECKS: tuple[str, ...] = (
    "source_task_8_commit_bound",
    "source_task_8_signature_bound",
    "selected_option_id_confirmed",
    "selected_option_name_confirmed",
    "selected_option_value_confirmed",
    "selected_option_class_planning_only",
    "selected_option_review_status_confirmed",
    "planning_gate_ready",
    "planning_gate_open",
    "planning_gate_passed",
    "planning_gate_closed",
    "planning_scope_local_solver_only",
    "planning_workstream_count_six",
    "planning_workstream_ids_unique",
    "all_workstreams_planning_candidates",
    "no_workstream_allows_implementation",
    "no_workstream_allows_runtime",
    "no_workstream_allows_submission",
    "planning_authorized",
    "planning_authorization_scope_planning_only",
    "implementation_authorization_not_granted",
    "implementation_not_authorized",
    "implementation_blocked",
    "implementation_not_performed",
    "runtime_solver_patch_not_allowed",
    "runtime_solver_not_modified",
    "ranker_runtime_patch_not_allowed",
    "candidate_generator_patch_not_allowed",
    "runtime_wiring_not_allowed",
    "runtime_activation_not_authorized",
    "runtime_execution_not_allowed",
    "runtime_execution_not_performed",
    "real_evaluation_not_allowed",
    "real_submission_not_allowed",
    "manual_upload_not_allowed",
    "kaggle_authentication_not_allowed",
    "kaggle_submission_not_sent",
    "private_core_not_exposed",
    "legal_certification_false",
    "fail_closed_required",
    "fail_closed_active",
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_controlled_local_solver_improvement_planning_gate() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_8_final_baseline_commit": SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        "source_task_8_final_signature": SOURCE_TASK_8_FINAL_SIGNATURE,
        "selected_option_id": SELECTED_OPTION_ID,
        "selected_option_value": SELECTED_OPTION_VALUE,
        "selected_option_class": SELECTED_OPTION_CLASS,
        "workstream_count": len(PLANNING_WORKSTREAMS),
        "verdict": PLANNING_GATE_VERDICT,
        "decision": PLANNING_GATE_DECISION,
        "reason": PLANNING_GATE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "planning_gate_open": True,
        "planning_authorized": True,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-planning-gate-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-planning-gate-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-planning-gate-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-planning-gate-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "planning_gate_status_marker": PLANNING_GATE_STATUS_MARKER,
        "signature": signature,
        "source_task_8_final_baseline_commit": SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        "source_task_8_final_signature": SOURCE_TASK_8_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": PLANNING_GATE_VERDICT,
        "decision": PLANNING_GATE_DECISION,
        "planning_gate_reason": PLANNING_GATE_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "selected_option_id": SELECTED_OPTION_ID,
        "selected_option_name": SELECTED_OPTION_NAME,
        "selected_option_value": SELECTED_OPTION_VALUE,
        "selected_option_class": SELECTED_OPTION_CLASS,
        "selected_option_review_status": SELECTED_OPTION_REVIEW_STATUS,
        "controlled_local_solver_improvement_planning_gate_ready": True,
        "controlled_local_solver_improvement_planning_gate_open": True,
        "controlled_local_solver_improvement_planning_gate_passed": True,
        "controlled_local_solver_improvement_planning_gate_closed": True,
        "planning_authorized": True,
        "planning_authorization_scope": "PLANNING_ONLY",
        "planning_scope": "LOCAL_SOLVER_IMPROVEMENT_ONLY",
        "planning_workstream_count": len(PLANNING_WORKSTREAMS),
        "planning_workstreams": PLANNING_WORKSTREAMS,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "runtime_solver_patch_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_patch_allowed": False,
        "ranker_runtime_modified": False,
        "candidate_generator_patch_allowed": False,
        "candidate_generator_modified": False,
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
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "planning_gate_check_count": len(PLANNING_GATE_CHECKS),
        "planning_gate_failure_count": 0,
        "planning_gate_checks": PLANNING_GATE_CHECKS,
        "artifacts": artifacts,
    }


def validate_controlled_local_solver_improvement_planning_gate(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "planning_gate_status_marker": PLANNING_GATE_STATUS_MARKER,
        "source_task_8_final_baseline_commit": SOURCE_TASK_8_FINAL_BASELINE_COMMIT,
        "source_task_8_final_signature": SOURCE_TASK_8_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "selected_option_id": SELECTED_OPTION_ID,
        "selected_option_name": SELECTED_OPTION_NAME,
        "selected_option_value": SELECTED_OPTION_VALUE,
        "selected_option_class": SELECTED_OPTION_CLASS,
        "selected_option_review_status": SELECTED_OPTION_REVIEW_STATUS,
        "verdict": PLANNING_GATE_VERDICT,
        "decision": PLANNING_GATE_DECISION,
        "planning_gate_reason": PLANNING_GATE_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    workstreams = tuple(status.get("planning_workstreams", ()))
    workstream_ids = [workstream.get("workstream_id") for workstream in workstreams]

    if status.get("planning_workstream_count") != 6:
        issues.append("planning_workstream_count must be 6")
    if len(workstreams) != 6:
        issues.append("planning_workstreams length must be 6")
    if len(workstream_ids) != len(set(workstream_ids)):
        issues.append("planning workstream IDs must be unique")

    for workstream in workstreams:
        if workstream.get("status") != "PLANNING_CANDIDATE":
            issues.append(f"{workstream.get('workstream_id')} status must be PLANNING_CANDIDATE")
        if workstream.get("implementation_allowed") is not False:
            issues.append(f"{workstream.get('workstream_id')} implementation_allowed must be False")
        if workstream.get("runtime_allowed") is not False:
            issues.append(f"{workstream.get('workstream_id')} runtime_allowed must be False")
        if workstream.get("submission_allowed") is not False:
            issues.append(f"{workstream.get('workstream_id')} submission_allowed must be False")

    required_true = (
        "controlled_local_solver_improvement_planning_gate_ready",
        "controlled_local_solver_improvement_planning_gate_open",
        "controlled_local_solver_improvement_planning_gate_passed",
        "controlled_local_solver_improvement_planning_gate_closed",
        "planning_authorized",
        "implementation_blocked",
        "fail_closed_required",
        "fail_closed_active",
    )
    required_false = (
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
        "ranker_runtime_patch_allowed",
        "ranker_runtime_modified",
        "candidate_generator_patch_allowed",
        "candidate_generator_modified",
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
        "private_core_exposure",
        "legal_certification",
    )

    for key in required_true:
        if status.get(key) is not True:
            issues.append(f"{key} must be True")
    for key in required_false:
        if status.get(key) is not False:
            issues.append(f"{key} must be False")

    if status.get("planning_authorization_scope") != "PLANNING_ONLY":
        issues.append("planning_authorization_scope must be PLANNING_ONLY")
    if status.get("planning_scope") != "LOCAL_SOLVER_IMPROVEMENT_ONLY":
        issues.append("planning_scope must be LOCAL_SOLVER_IMPROVEMENT_ONLY")
    if status.get("planning_gate_check_count") != len(PLANNING_GATE_CHECKS):
        issues.append("planning_gate_check_count mismatch")
    if status.get("planning_gate_failure_count") != 0:
        issues.append("planning_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def planning_gate_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["planning_gate_status_marker"],
        "signature": status["signature"],
        "source_task_8_final_baseline_commit": status["source_task_8_final_baseline_commit"],
        "source_task_8_final_signature": status["source_task_8_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "selected_option_id": status["selected_option_id"],
        "selected_option_value": status["selected_option_value"],
        "planning_scope": status["planning_scope"],
        "planning_authorization_scope": status["planning_authorization_scope"],
        "planning_workstream_count": status["planning_workstream_count"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "real_submission_allowed": status["real_submission_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "planning_gate_check_count": status["planning_gate_check_count"],
        "planning_gate_failure_count": status["planning_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_markdown(status: dict[str, Any]) -> str:
    workstream_lines = "\n".join(
        f"- `{workstream['workstream_id']}` — {workstream['name']} · `{workstream['status']}`"
        for workstream in status["planning_workstreams"]
    )

    return f"""# Milestone #17 Task 9 - Controlled Local Solver Improvement Planning Gate v1

## Status

`{status["planning_gate_status_marker"]}`

## Canonical markers

- task: `{status["task_name"]}`
- ready: `{status["task_ready_marker"]}`
- valid: `{status["task_valid_marker"]}`
- pipeline: `{status["pipeline_ready_marker"]}`
- signature: `{status["signature"]}`
- mode: `{status["task_mode"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 8 final baseline commit: `{status["source_task_8_final_baseline_commit"]}`
- source Task 8 final signature: `{status["source_task_8_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Planning gate

- selected_option_id: `{status["selected_option_id"]}`
- selected_option_name: `{status["selected_option_name"]}`
- selected_option_value: `{status["selected_option_value"]}`
- selected_option_class: `{status["selected_option_class"]}`
- selected_option_review_status: `{status["selected_option_review_status"]}`
- planning_scope: `{status["planning_scope"]}`
- planning_authorized: `{status["planning_authorized"]}`
- planning_authorization_scope: `{status["planning_authorization_scope"]}`
- planning_workstream_count: `{status["planning_workstream_count"]}`

{workstream_lines}

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Reason

`{status["planning_gate_reason"]}`

## Boundary

- implementation_authorization_granted: `{status["implementation_authorization_granted"]}`
- implementation_authorized: `{status["implementation_authorized"]}`
- implementation_blocked: `{status["implementation_blocked"]}`
- implementation_performed: `{status["implementation_performed"]}`
- runtime_solver_patch_allowed: `{status["runtime_solver_patch_allowed"]}`
- runtime_solver_modified: `{status["runtime_solver_modified"]}`
- ranker_runtime_patch_allowed: `{status["ranker_runtime_patch_allowed"]}`
- candidate_generator_patch_allowed: `{status["candidate_generator_patch_allowed"]}`
- runtime_wiring_allowed: `{status["runtime_wiring_allowed"]}`
- runtime_activation_authorized: `{status["runtime_activation_authorized"]}`
- runtime_execution_allowed: `{status["runtime_execution_allowed"]}`
- real_evaluation_allowed: `{status["real_evaluation_allowed"]}`
- real_submission_allowed: `{status["real_submission_allowed"]}`
- manual_upload_allowed: `{status["manual_upload_allowed"]}`
- kaggle_authentication_allowed: `{status["kaggle_authentication_allowed"]}`
- kaggle_submission_sent: `{status["kaggle_submission_sent"]}`
- private_core_exposure: `{status["private_core_exposure"]}`
- legal_certification: `{status["legal_certification"]}`
- fail_closed_required: `{status["fail_closed_required"]}`
- fail_closed_active: `{status["fail_closed_active"]}`

## Validation

- planning_gate_check_count: `{status["planning_gate_check_count"]}`
- planning_gate_failure_count: `{status["planning_gate_failure_count"]}`
"""


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["planning_gate_status_marker"],
        f"signature={status['signature']}",
        f"source_task_8_final_baseline_commit={status['source_task_8_final_baseline_commit']}",
        f"source_task_8_final_signature={status['source_task_8_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"planning_gate_reason={status['planning_gate_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"selected_option_id={status['selected_option_id']}",
        f"selected_option_value={status['selected_option_value']}",
        f"selected_option_class={status['selected_option_class']}",
        f"planning_scope={status['planning_scope']}",
        f"planning_authorized={status['planning_authorized']}",
        f"planning_authorization_scope={status['planning_authorization_scope']}",
        f"planning_workstream_count={status['planning_workstream_count']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"real_submission_allowed={status['real_submission_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"planning_gate_check_count={status['planning_gate_check_count']}",
        f"planning_gate_failure_count={status['planning_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def write_controlled_local_solver_improvement_planning_gate_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_local_solver_improvement_planning_gate()
    issues = validate_controlled_local_solver_improvement_planning_gate(resolved)
    if issues:
        raise ValueError("Invalid controlled local solver improvement planning gate: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = planning_gate_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-planning-gate-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-planning-gate-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-planning-gate-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-planning-gate-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_local_solver_improvement_planning_gate_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_8_final_baseline_commit"])
    print(status["task_mode"])
    print(status["planning_gate_status_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["planning_gate_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_8_final_baseline_commit",
        "source_task_8_final_signature",
        "selected_option_id",
        "selected_option_name",
        "selected_option_value",
        "selected_option_class",
        "selected_option_review_status",
        "controlled_local_solver_improvement_planning_gate_ready",
        "controlled_local_solver_improvement_planning_gate_open",
        "controlled_local_solver_improvement_planning_gate_passed",
        "controlled_local_solver_improvement_planning_gate_closed",
        "planning_authorized",
        "planning_authorization_scope",
        "planning_scope",
        "planning_workstream_count",
        "implementation_authorization_granted",
        "implementation_authorized",
        "implementation_blocked",
        "implementation_performed",
        "runtime_solver_patch_allowed",
        "runtime_solver_modified",
        "ranker_runtime_patch_allowed",
        "ranker_runtime_modified",
        "candidate_generator_patch_allowed",
        "candidate_generator_modified",
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
        "private_core_exposure",
        "legal_certification",
        "fail_closed_required",
        "fail_closed_active",
        "planning_gate_check_count",
        "planning_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for workstream in status["planning_workstreams"]:
        print(
            f"planning_workstream={workstream['workstream_id']}|"
            f"{workstream['status']}|{workstream['name']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
