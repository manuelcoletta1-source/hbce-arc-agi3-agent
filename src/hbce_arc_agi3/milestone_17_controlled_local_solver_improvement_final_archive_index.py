"""Milestone #17 Task 22 - Controlled Local Solver Improvement Final Archive Index v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_17_TASK_22_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_V1"
TASK_READY_MARKER = f"{TASK_NAME}_READY"
TASK_VALID_MARKER = f"{TASK_NAME}_VALID"
PIPELINE_READY_MARKER = f"{TASK_NAME}_PIPELINE_READY"

FINAL_ARCHIVE_INDEX_MARKER = "MILESTONE_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_READY"
FINAL_ARCHIVE_INDEX_VERDICT = "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_PASS_INDEX_CREATED"
FINAL_ARCHIVE_INDEX_DECISION = "INDEX_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_NO_IMPLEMENTATION_AUTHORIZED"
FINAL_ARCHIVE_INDEX_REASON = (
    "TASK_21_CLOSED_FINAL_CYCLE_CLOSURE_REVIEW_WITHOUT_IMPLEMENTATION_RUNTIME_OR_SUBMISSION"
)

PREVIOUS_STAGE = "MILESTONE_17_TASK_21_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_REVIEW_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_17_TASK_23_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_REVIEW_V1"

SOURCE_TASK_21_FINAL_BASELINE_COMMIT = "717c924"
SOURCE_TASK_21_FINAL_SIGNATURE = "A3E1BE3B64387C85"

FINAL_ARCHIVE_INDEX_SCOPE = "INDEX_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_ONLY"
PLAN_AUTHORIZATION_SCOPE = "PLAN_ONLY"
IMPLEMENTATION_AUTHORIZATION_SCOPE = "NOT_GRANTED"

TASK_MODE = "MILESTONE_17_TASK_22_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_V1_INDEX_ONLY_LOCAL_ONLY"

ARTIFACT_DIR = Path("examples/milestone-17/controlled-local-solver-improvement-final-archive-index-v1")
DOC_PATH = Path("docs/milestone-17-controlled-local-solver-improvement-final-archive-index-v1.md")


INDEXED_FINAL_CYCLE_STAGES: tuple[dict[str, Any], ...] = (
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-1",
        "task": "MILESTONE_17_TASK_11_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_V1",
        "commit": "566dad4",
        "signature": "6380B16C08C60A41",
        "archive_status": "INDEXED_FINAL_CYCLE_PLAN",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-2",
        "task": "MILESTONE_17_TASK_12_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_REVIEW_V1",
        "commit": "ee29733",
        "signature": "B83CF1D86F83BDE8",
        "archive_status": "INDEXED_FINAL_CYCLE_PLAN_REVIEW",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-3",
        "task": "MILESTONE_17_TASK_13_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_CLOSURE_V1",
        "commit": "e3b6528",
        "signature": "D992AEA3A992CA7F",
        "archive_status": "INDEXED_FINAL_CYCLE_PLAN_CLOSURE",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-4",
        "task": "MILESTONE_17_TASK_14_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_V1",
        "commit": "a04d19e",
        "signature": "F32F27EF4D9D20E8",
        "archive_status": "INDEXED_FINAL_CYCLE_STATUS_REVIEW",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-5",
        "task": "MILESTONE_17_TASK_15_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_CLOSURE_V1",
        "commit": "36e2084",
        "signature": "416DA88ECB7960B9",
        "archive_status": "INDEXED_FINAL_CYCLE_STATUS_REVIEW_CLOSURE",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-6",
        "task": "MILESTONE_17_TASK_16_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_ARCHIVE_V1",
        "commit": "b6a494e",
        "signature": "45575F06C7ED5E24",
        "archive_status": "INDEXED_FINAL_CYCLE_ARCHIVE",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-7",
        "task": "MILESTONE_17_TASK_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_ARCHIVE_REVIEW_V1",
        "commit": "879ad75",
        "signature": "B66AA97FFE0C8BD8",
        "archive_status": "INDEXED_FINAL_CYCLE_ARCHIVE_REVIEW",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-8",
        "task": "MILESTONE_17_TASK_18_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_ARCHIVE_REVIEW_CLOSURE_V1",
        "commit": "473fdca",
        "signature": "A75818655560BAD7",
        "archive_status": "INDEXED_FINAL_CYCLE_ARCHIVE_REVIEW_CLOSURE",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-9",
        "task": "MILESTONE_17_TASK_19_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_V1",
        "commit": "9d65af4",
        "signature": "6CEF8B7CAD046107",
        "archive_status": "INDEXED_FINAL_CYCLE_CLOSURE",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-10",
        "task": "MILESTONE_17_TASK_20_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_REVIEW_V1",
        "commit": "8dc2d30",
        "signature": "B804FD3E5DB9E083",
        "archive_status": "INDEXED_FINAL_CYCLE_CLOSURE_REVIEW",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
    {
        "stage_id": "M17-FINAL-ARCHIVE-INDEX-STAGE-11",
        "task": "MILESTONE_17_TASK_21_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_REVIEW_CLOSURE_V1",
        "commit": "717c924",
        "signature": "A3E1BE3B64387C85",
        "archive_status": "INDEXED_FINAL_CYCLE_CLOSURE_REVIEW_CLOSURE",
        "implementation_authorized": False,
        "runtime_execution_allowed": False,
        "submission_allowed": False,
    },
)


FINAL_ARCHIVE_INDEX_GATES: tuple[str, ...] = (
    "source_task_21_commit_bound",
    "source_task_21_signature_bound",
    "previous_stage_bound",
    "next_stage_declared",
    "final_archive_index_scope_confirmed",
    "plan_authorization_scope_plan_only",
    "implementation_authorization_scope_not_granted",
    "indexed_final_cycle_stage_count_eleven",
    "all_final_cycle_stages_indexed",
    "all_indexed_final_cycle_stages_have_commits",
    "all_indexed_final_cycle_stages_have_signatures",
    "all_indexed_final_cycle_stages_no_implementation",
    "all_indexed_final_cycle_stages_no_runtime_execution",
    "all_indexed_final_cycle_stages_no_submission",
    "final_archive_index_ready",
    "final_archive_index_passed",
    "final_archive_index_locked",
    "implementation_authorization_not_granted",
    "implementation_not_authorized",
    "implementation_blocked",
    "implementation_not_performed",
    "runtime_solver_patch_not_allowed",
    "runtime_solver_not_modified",
    "ranker_runtime_patch_not_allowed",
    "ranker_runtime_not_modified",
    "candidate_generator_patch_not_allowed",
    "candidate_generator_not_modified",
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
)


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_signature(seed_payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(seed_payload).encode("utf-8")).hexdigest()
    return digest[:16].upper()


def build_controlled_local_solver_improvement_final_archive_index() -> dict[str, Any]:
    seed_payload = {
        "task_name": TASK_NAME,
        "source_task_21_final_baseline_commit": SOURCE_TASK_21_FINAL_BASELINE_COMMIT,
        "source_task_21_final_signature": SOURCE_TASK_21_FINAL_SIGNATURE,
        "final_archive_index_scope": FINAL_ARCHIVE_INDEX_SCOPE,
        "indexed_final_cycle_stage_count": len(INDEXED_FINAL_CYCLE_STAGES),
        "verdict": FINAL_ARCHIVE_INDEX_VERDICT,
        "decision": FINAL_ARCHIVE_INDEX_DECISION,
        "reason": FINAL_ARCHIVE_INDEX_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "implementation_blocked": True,
        "runtime_execution_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    signature = compute_signature(seed_payload)

    artifacts = (
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-final-archive-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-final-archive-index-index-v1.json"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-final-archive-index-manifest-v1.txt"),
        str(ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-final-archive-index-v1.md"),
        str(DOC_PATH),
    )

    return {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "final_archive_index_marker": FINAL_ARCHIVE_INDEX_MARKER,
        "signature": signature,
        "source_task_21_final_baseline_commit": SOURCE_TASK_21_FINAL_BASELINE_COMMIT,
        "source_task_21_final_signature": SOURCE_TASK_21_FINAL_SIGNATURE,
        "task_mode": TASK_MODE,
        "verdict": FINAL_ARCHIVE_INDEX_VERDICT,
        "decision": FINAL_ARCHIVE_INDEX_DECISION,
        "final_archive_index_reason": FINAL_ARCHIVE_INDEX_REASON,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_archive_index_scope": FINAL_ARCHIVE_INDEX_SCOPE,
        "plan_authorized": True,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "controlled_local_solver_improvement_final_archive_index_ready": True,
        "controlled_local_solver_improvement_final_archive_index_passed": True,
        "controlled_local_solver_improvement_final_archive_index_locked": True,
        "indexed_final_cycle_stage_count": len(INDEXED_FINAL_CYCLE_STAGES),
        "indexed_final_cycle_stages": INDEXED_FINAL_CYCLE_STAGES,
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
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "final_archive_index_gate_count": len(FINAL_ARCHIVE_INDEX_GATES),
        "final_archive_index_gate_failure_count": 0,
        "final_archive_index_gates": FINAL_ARCHIVE_INDEX_GATES,
        "artifacts": artifacts,
    }


def validate_controlled_local_solver_improvement_final_archive_index(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected = {
        "task_name": TASK_NAME,
        "task_ready_marker": TASK_READY_MARKER,
        "task_valid_marker": TASK_VALID_MARKER,
        "pipeline_ready_marker": PIPELINE_READY_MARKER,
        "final_archive_index_marker": FINAL_ARCHIVE_INDEX_MARKER,
        "source_task_21_final_baseline_commit": SOURCE_TASK_21_FINAL_BASELINE_COMMIT,
        "source_task_21_final_signature": SOURCE_TASK_21_FINAL_SIGNATURE,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "final_archive_index_scope": FINAL_ARCHIVE_INDEX_SCOPE,
        "plan_authorization_scope": PLAN_AUTHORIZATION_SCOPE,
        "implementation_authorization_scope": IMPLEMENTATION_AUTHORIZATION_SCOPE,
        "verdict": FINAL_ARCHIVE_INDEX_VERDICT,
        "decision": FINAL_ARCHIVE_INDEX_DECISION,
        "final_archive_index_reason": FINAL_ARCHIVE_INDEX_REASON,
    }

    for key, expected_value in expected.items():
        if status.get(key) != expected_value:
            issues.append(f"{key} mismatch")

    stages = tuple(status.get("indexed_final_cycle_stages", ()))
    stage_ids = [stage.get("stage_id") for stage in stages]

    if status.get("indexed_final_cycle_stage_count") != 11:
        issues.append("indexed_final_cycle_stage_count must be 11")
    if len(stages) != 11:
        issues.append("indexed_final_cycle_stages length must be 11")
    if len(stage_ids) != len(set(stage_ids)):
        issues.append("indexed final cycle stage IDs must be unique")

    for stage in stages:
        if not stage.get("archive_status"):
            issues.append(f"{stage.get('stage_id')} must have archive_status")
        if not stage.get("commit"):
            issues.append(f"{stage.get('stage_id')} must have commit")
        if not stage.get("signature"):
            issues.append(f"{stage.get('stage_id')} must have signature")
        if stage.get("implementation_authorized") is not False:
            issues.append(f"{stage.get('stage_id')} implementation_authorized must be False")
        if stage.get("runtime_execution_allowed") is not False:
            issues.append(f"{stage.get('stage_id')} runtime_execution_allowed must be False")
        if stage.get("submission_allowed") is not False:
            issues.append(f"{stage.get('stage_id')} submission_allowed must be False")

    required_true = (
        "plan_authorized",
        "controlled_local_solver_improvement_final_archive_index_ready",
        "controlled_local_solver_improvement_final_archive_index_passed",
        "controlled_local_solver_improvement_final_archive_index_locked",
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
        "competitive_score_claim_allowed",
        "official_score_claim_allowed",
        "private_core_exposure",
        "legal_certification",
    )

    for key in required_true:
        if status.get(key) is not True:
            issues.append(f"{key} must be True")
    for key in required_false:
        if status.get(key) is not False:
            issues.append(f"{key} must be False")

    if status.get("final_archive_index_gate_count") != len(FINAL_ARCHIVE_INDEX_GATES):
        issues.append("final_archive_index_gate_count mismatch")
    if status.get("final_archive_index_gate_failure_count") != 0:
        issues.append("final_archive_index_gate_failure_count must be 0")
    if len(status.get("artifacts", ())) != 5:
        issues.append("artifact count mismatch")

    return issues


def final_archive_index_to_dict(status: dict[str, Any]) -> dict[str, Any]:
    return dict(status)


def build_index_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_name": status["task_name"],
        "status": status["final_archive_index_marker"],
        "signature": status["signature"],
        "source_task_21_final_baseline_commit": status["source_task_21_final_baseline_commit"],
        "source_task_21_final_signature": status["source_task_21_final_signature"],
        "previous_stage": status["previous_stage"],
        "next_stage": status["next_stage"],
        "final_archive_index_scope": status["final_archive_index_scope"],
        "indexed_final_cycle_stage_count": status["indexed_final_cycle_stage_count"],
        "implementation_blocked": status["implementation_blocked"],
        "runtime_execution_allowed": status["runtime_execution_allowed"],
        "kaggle_submission_sent": status["kaggle_submission_sent"],
        "official_score_claim_allowed": status["official_score_claim_allowed"],
        "private_core_exposure": status["private_core_exposure"],
        "legal_certification": status["legal_certification"],
        "fail_closed_active": status["fail_closed_active"],
        "final_archive_index_gate_count": status["final_archive_index_gate_count"],
        "final_archive_index_gate_failure_count": status["final_archive_index_gate_failure_count"],
        "artifact_count": len(status["artifacts"]),
    }


def build_manifest(status: dict[str, Any]) -> str:
    lines = [
        status["pipeline_ready_marker"],
        status["task_ready_marker"],
        status["task_valid_marker"],
        status["final_archive_index_marker"],
        f"signature={status['signature']}",
        f"source_task_21_final_baseline_commit={status['source_task_21_final_baseline_commit']}",
        f"source_task_21_final_signature={status['source_task_21_final_signature']}",
        f"task_mode={status['task_mode']}",
        f"verdict={status['verdict']}",
        f"decision={status['decision']}",
        f"final_archive_index_reason={status['final_archive_index_reason']}",
        f"previous_stage={status['previous_stage']}",
        f"next_stage={status['next_stage']}",
        f"final_archive_index_scope={status['final_archive_index_scope']}",
        f"indexed_final_cycle_stage_count={status['indexed_final_cycle_stage_count']}",
        f"implementation_blocked={status['implementation_blocked']}",
        f"runtime_execution_allowed={status['runtime_execution_allowed']}",
        f"kaggle_submission_sent={status['kaggle_submission_sent']}",
        f"official_score_claim_allowed={status['official_score_claim_allowed']}",
        f"private_core_exposure={status['private_core_exposure']}",
        f"legal_certification={status['legal_certification']}",
        f"fail_closed_active={status['fail_closed_active']}",
        f"final_archive_index_gate_count={status['final_archive_index_gate_count']}",
        f"final_archive_index_gate_failure_count={status['final_archive_index_gate_failure_count']}",
    ]
    return "\n".join(lines) + "\n"


def build_markdown(status: dict[str, Any]) -> str:
    stage_lines = "\n".join(
        f"- `{stage['stage_id']}` — `{stage['task']}` · commit `{stage['commit']}` · `{stage['archive_status']}`"
        for stage in status["indexed_final_cycle_stages"]
    )

    return f"""# Milestone #17 Task 22 - Controlled Local Solver Improvement Final Archive Index v1

## Status

`{status["final_archive_index_marker"]}`

## Source binding

- previous stage: `{status["previous_stage"]}`
- source Task 21 final baseline commit: `{status["source_task_21_final_baseline_commit"]}`
- source Task 21 final signature: `{status["source_task_21_final_signature"]}`
- next stage: `{status["next_stage"]}`

## Final archive index

- final_archive_index_scope: `{status["final_archive_index_scope"]}`
- indexed_final_cycle_stage_count: `{status["indexed_final_cycle_stage_count"]}`

{stage_lines}

## Verdict

`{status["verdict"]}`

## Decision

`{status["decision"]}`

## Boundary

- implementation_authorized: `{status["implementation_authorized"]}`
- implementation_blocked: `{status["implementation_blocked"]}`
- runtime_execution_allowed: `{status["runtime_execution_allowed"]}`
- real_submission_allowed: `{status["real_submission_allowed"]}`
- kaggle_submission_sent: `{status["kaggle_submission_sent"]}`
- private_core_exposure: `{status["private_core_exposure"]}`
- legal_certification: `{status["legal_certification"]}`
- fail_closed_active: `{status["fail_closed_active"]}`
"""


def write_controlled_local_solver_improvement_final_archive_index_artifacts(
    status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = status or build_controlled_local_solver_improvement_final_archive_index()
    issues = validate_controlled_local_solver_improvement_final_archive_index(resolved)
    if issues:
        raise ValueError("Invalid controlled local solver improvement final archive index: " + "; ".join(issues))

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = final_archive_index_to_dict(resolved)
    index_payload = build_index_payload(resolved)
    markdown = build_markdown(resolved)
    manifest = build_manifest(resolved)

    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-final-archive-index-v1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-final-archive-index-index-v1.json").write_text(
        json.dumps(index_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-final-archive-index-manifest-v1.txt").write_text(
        manifest,
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "milestone-17-controlled-local-solver-improvement-final-archive-index-v1.md").write_text(
        markdown,
        encoding="utf-8",
    )
    DOC_PATH.write_text(markdown, encoding="utf-8")

    return resolved


def main() -> int:
    status = write_controlled_local_solver_improvement_final_archive_index_artifacts()

    print(status["pipeline_ready_marker"])
    print(status["task_ready_marker"])
    print(status["task_valid_marker"])
    print(status["signature"])
    print(status["source_task_21_final_baseline_commit"])
    print(status["task_mode"])
    print(status["final_archive_index_marker"])
    print(status["verdict"])
    print(status["decision"])
    print(status["final_archive_index_reason"])
    print(status["previous_stage"])
    print(status["next_stage"])

    ordered_keys = (
        "source_task_21_final_baseline_commit",
        "source_task_21_final_signature",
        "final_archive_index_scope",
        "indexed_final_cycle_stage_count",
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
        "final_archive_index_gate_count",
        "final_archive_index_gate_failure_count",
    )
    for key in ordered_keys:
        print(f"{key}={status[key]}")
    for stage in status["indexed_final_cycle_stages"]:
        print(
            f"indexed_final_cycle_stage={stage['stage_id']}|{stage['task']}|"
            f"{stage['commit']}|{stage['signature']}|{stage['archive_status']}"
        )
    for artifact in status["artifacts"]:
        print(artifact)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
