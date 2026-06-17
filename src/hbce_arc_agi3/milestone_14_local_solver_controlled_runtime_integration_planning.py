"""Milestone #14 Task 1 - Local Solver Controlled Runtime Integration Planning v1.

This task opens Milestone #14 after the formal closure of Milestone #13.

It plans the next controlled local solver integration branch.
It does not modify the solver runtime.
It does not execute runtime solving.
It does not perform real Kaggle evaluation.
It does not authenticate, upload, or submit.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLANNING_V1"
MILESTONE_NUMBER = 14
TASK_NUMBER = 1
TASK_LABEL = "Milestone #14 Task 1 - Local Solver Controlled Runtime Integration Planning v1"

SOURCE_MILESTONE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_MILESTONE_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_14_TASK_2_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLAN_REVIEW_V1"

TASK_MODE = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLANNING_V1_PLANNING_ONLY_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLANNING_READY"
PLANNING_VERDICT = "LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLANNING_READY_FOR_PLAN_REVIEW"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-14" / "local-solver-controlled-runtime-integration-planning-v1"

SOURCE_MILESTONE_13_CLOSURE_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-milestone-closure-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-milestone-closure-v1.json"
)

PLANNING_OBJECTIVES = [
    {
        "id": "M14-PLAN-01",
        "name": "consume_milestone_13_candidate_generator_output",
        "status": "PLANNED",
        "description": "Use the Milestone 13 controlled candidate generator wiring as a local-only input signal.",
    },
    {
        "id": "M14-PLAN-02",
        "name": "define_solver_integration_contract",
        "status": "PLANNED",
        "description": "Define the local solver contract for accepting controlled program synthesis candidates.",
    },
    {
        "id": "M14-PLAN-03",
        "name": "preserve_diagnostic_only_boundary",
        "status": "PLANNED",
        "description": "Keep Milestone 14 in diagnostic-only mode until explicit future authorization.",
    },
    {
        "id": "M14-PLAN-04",
        "name": "define_runtime_activation_guard",
        "status": "PLANNED",
        "description": "Specify guards that prevent accidental runtime activation or real solver execution.",
    },
    {
        "id": "M14-PLAN-05",
        "name": "define_local_evaluation_harness_contract",
        "status": "PLANNED",
        "description": "Plan a deterministic local evaluation harness without Kaggle score semantics.",
    },
    {
        "id": "M14-PLAN-06",
        "name": "preserve_public_overfit_guard",
        "status": "PLANNED",
        "description": "Keep public-overfit protection required during any diagnostic evaluation.",
    },
    {
        "id": "M14-PLAN-07",
        "name": "preserve_no_submission_boundary",
        "status": "PLANNED",
        "description": "Keep Kaggle authentication, upload, and submission disabled.",
    },
    {
        "id": "M14-PLAN-08",
        "name": "prepare_plan_review_gate",
        "status": "PLANNED",
        "description": "Prepare Task 2 as a review gate before any implementation work.",
    },
]

PLANNED_TASK_CHAIN = [
    "MILESTONE_14_TASK_1_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLANNING_V1",
    "MILESTONE_14_TASK_2_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLAN_REVIEW_V1",
    "MILESTONE_14_TASK_3_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_V1",
    "MILESTONE_14_TASK_4_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_REVIEW_V1",
    "MILESTONE_14_TASK_5_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_DRY_RUN_DESIGN_V1",
    "MILESTONE_14_TASK_6_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_DRY_RUN_REVIEW_V1",
]


def _run_git_head() -> str:
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "NO_GIT_HEAD_AVAILABLE"
    return result.stdout.strip() or "NO_GIT_HEAD_AVAILABLE"


def _stable_signature(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return loaded if isinstance(loaded, dict) else None


def review_milestone_13_closure_artifact() -> dict[str, Any]:
    source = _load_json(SOURCE_MILESTONE_13_CLOSURE_ARTIFACT)

    if source is None:
        return {
            "milestone_13_closure_artifact_present": False,
            "milestone_13_closure_artifact_parseable": False,
            "milestone_13_closure_valid": False,
            "source_record": None,
        }

    valid = bool(
        source.get("milestone_closure_valid") is True
        and source.get("milestone_13_closed") is True
        and source.get("ready_for_next_milestone_planning") is True
        and source.get("runtime_candidate_count") == 4
        and source.get("candidate_fixture_matrix_count") == 12
        and source.get("diagnostic_case_count") == 12
        and source.get("diagnostic_pass_count") == 12
        and source.get("diagnostic_failure_count") == 0
        and source.get("diagnostic_average_score") == 0.6875
        and source.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
        and source.get("runtime_activation_performed") is False
        and source.get("runtime_execution_performed") is False
        and source.get("real_submission_allowed") is False
        and source.get("kaggle_submission_sent") is False
        and source.get("private_core_exposure") is False
        and source.get("legal_certification") is False
        and source.get("next_stage") == "MILESTONE_13_CLOSED_READY_FOR_NEXT_MILESTONE_PLANNING"
    )

    return {
        "milestone_13_closure_artifact_present": True,
        "milestone_13_closure_artifact_parseable": True,
        "milestone_13_closure_valid": valid,
        "source_record": source,
    }


def build_planning_gate_map(source_record: dict[str, Any]) -> dict[str, bool]:
    return {
        "milestone_13_closed": source_record.get("milestone_13_closed") is True,
        "ready_for_next_milestone_planning": source_record.get("ready_for_next_milestone_planning") is True,
        "runtime_candidate_count_4": source_record.get("runtime_candidate_count") == 4,
        "candidate_fixture_matrix_count_12": source_record.get("candidate_fixture_matrix_count") == 12,
        "diagnostic_case_count_12": source_record.get("diagnostic_case_count") == 12,
        "diagnostic_pass_count_12": source_record.get("diagnostic_pass_count") == 12,
        "diagnostic_failure_count_0": source_record.get("diagnostic_failure_count") == 0,
        "diagnostic_average_score_0_6875": source_record.get("diagnostic_average_score") == 0.6875,
        "not_kaggle_score": source_record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "runtime_activation_false": source_record.get("runtime_activation_performed") is False,
        "runtime_execution_false": source_record.get("runtime_execution_performed") is False,
        "real_submission_false": source_record.get("real_submission_allowed") is False,
        "kaggle_submission_false": source_record.get("kaggle_submission_sent") is False,
        "private_core_false": source_record.get("private_core_exposure") is False,
        "legal_certification_false": source_record.get("legal_certification") is False,
    }


def build_milestone_14_planning_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_review = review_milestone_13_closure_artifact()
    source_record = source_review.get("source_record") if isinstance(source_review.get("source_record"), dict) else {}
    planning_gates = build_planning_gate_map(source_record)

    planning_checks = {
        "milestone_13_closure_artifact_present": source_review["milestone_13_closure_artifact_present"] is True,
        "milestone_13_closure_artifact_parseable": source_review["milestone_13_closure_artifact_parseable"] is True,
        "milestone_13_closure_valid": source_review["milestone_13_closure_valid"] is True,
        **planning_gates,
    }

    blocking_issues = [name for name, passed in planning_checks.items() if passed is not True]
    planning_valid = len(blocking_issues) == 0

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_milestone": SOURCE_MILESTONE,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_milestone_13_closure_artifact": str(SOURCE_MILESTONE_13_CLOSURE_ARTIFACT.relative_to(PROJECT_ROOT)),
        "task_mode": TASK_MODE,
        "task_verdict": TASK_VERDICT,
        "planning_verdict": PLANNING_VERDICT,
        "milestone_14_opened": planning_valid,
        "milestone_14_planning_ready": planning_valid,
        "ready_for_plan_review": planning_valid,
        "planning_objectives": PLANNING_OBJECTIVES,
        "planning_objective_count": len(PLANNING_OBJECTIVES),
        "planned_task_chain": PLANNED_TASK_CHAIN,
        "planned_task_chain_count": len(PLANNED_TASK_CHAIN),
        "source_review": source_review,
        "planning_gates": planning_gates,
        "planning_gate_count": len(planning_gates),
        "planning_checks": planning_checks,
        "planning_check_count": len(planning_checks),
        "planning_pass_count": len(planning_checks) - len(blocking_issues),
        "planning_failure_count": len(blocking_issues),
        "blocking_issue_count": len(blocking_issues),
        "blocking_issues": blocking_issues,
        "runtime_candidate_count": source_record.get("runtime_candidate_count"),
        "candidate_fixture_matrix_count": source_record.get("candidate_fixture_matrix_count"),
        "diagnostic_case_count": source_record.get("diagnostic_case_count"),
        "diagnostic_pass_count": source_record.get("diagnostic_pass_count"),
        "diagnostic_failure_count": source_record.get("diagnostic_failure_count"),
        "diagnostic_average_score": source_record.get("diagnostic_average_score"),
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "planning_only": True,
        "diagnostic_only": True,
        "runtime_activation_performed": False,
        "runtime_execution_performed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "candidate_generator_modified": False,
        "implementation_performed": False,
        "real_evaluation_performed": False,
        "real_kaggle_evaluation_allowed": False,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_upload_allowed": False,
        "kaggle_upload_performed": False,
        "kaggle_submission_sent": False,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "issue_count": len(blocking_issues),
        "warning_count": 0,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-14-LOCAL-SOLVER-CONTROLLED-RUNTIME-INTEGRATION-PLANNING-" + signature[:12]
    return record


def validate_milestone_14_planning_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "milestone_14_opened",
        "milestone_14_planning_ready",
        "ready_for_plan_review",
        "planning_only",
        "diagnostic_only",
        "public_overfit_guard_required",
        "operator_approval_required",
        "local_only",
        "deterministic",
        "public_safe",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "runtime_activation_performed",
        "runtime_execution_performed",
        "runtime_solver_modified",
        "ranker_runtime_modified",
        "candidate_generator_modified",
        "implementation_performed",
        "real_evaluation_performed",
        "real_kaggle_evaluation_allowed",
        "public_overfit_allowed",
        "external_api_dependency",
        "internet_during_eval",
        "real_submission_allowed",
        "ready_for_real_kaggle_submission",
        "manual_upload_allowed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_upload_allowed",
        "kaggle_upload_performed",
        "kaggle_submission_sent",
        "operator_approval_received",
        "contains_api_keys",
        "private_core_exposure",
        "legal_certification",
        "official_score_claim_allowed",
        "competitive_score_claim_allowed",
    ]

    for key in expected_true:
        if record.get(key) is not True:
            issues.append(f"{key}_NOT_TRUE")

    for key in expected_false:
        if record.get(key) is not False:
            issues.append(f"{key}_NOT_FALSE")

    if record.get("revision") != TASK_NAME:
        issues.append("REVISION_MISMATCH")
    if record.get("source_milestone") != SOURCE_MILESTONE:
        issues.append("SOURCE_MILESTONE_MISMATCH")
    if record.get("next_stage") != NEXT_STAGE:
        issues.append("NEXT_STAGE_MISMATCH")
    if record.get("task_verdict") != TASK_VERDICT:
        issues.append("TASK_VERDICT_MISMATCH")
    if record.get("planning_verdict") != PLANNING_VERDICT:
        issues.append("PLANNING_VERDICT_MISMATCH")

    expected_counts = {
        "runtime_candidate_count": 4,
        "candidate_fixture_matrix_count": 12,
        "diagnostic_case_count": 12,
        "diagnostic_pass_count": 12,
        "diagnostic_failure_count": 0,
        "planning_objective_count": 8,
        "planned_task_chain_count": 6,
        "planning_gate_count": 15,
        "planning_failure_count": 0,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
    }

    for key, expected in expected_counts.items():
        if record.get(key) != expected:
            issues.append(f"{key.upper()}_MISMATCH")

    planning_checks = record.get("planning_checks")
    if not isinstance(planning_checks, dict):
        issues.append("PLANNING_CHECKS_MISSING")
    else:
        if record.get("planning_check_count") != len(planning_checks):
            issues.append("PLANNING_CHECK_COUNT_MISMATCH")
        if record.get("planning_pass_count") != len(planning_checks):
            issues.append("PLANNING_PASS_COUNT_MISMATCH")

    if record.get("diagnostic_average_score") != 0.6875:
        issues.append("DIAGNOSTIC_AVERAGE_SCORE_MISMATCH")
    if record.get("kaggle_score_semantics") != "NOT_A_KAGGLE_SCORE":
        issues.append("KAGGLE_SCORE_SEMANTICS_MISMATCH")

    source_review = record.get("source_review")
    if not isinstance(source_review, dict):
        issues.append("SOURCE_REVIEW_MISSING")
    else:
        if source_review.get("milestone_13_closure_valid") is not True:
            issues.append("MILESTONE_13_CLOSURE_NOT_VALID")

    planning_gates = record.get("planning_gates")
    if not isinstance(planning_gates, dict):
        issues.append("PLANNING_GATES_MISSING")
    else:
        failed = [name for name, passed in planning_gates.items() if passed is not True]
        if failed:
            issues.append("PLANNING_GATES_FAILED")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-planning-v1.json"
    index_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-planning-index-v1.json"
    manifest_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-planning-manifest-v1.txt"
    markdown_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-planning-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "planning_verdict": record["planning_verdict"],
        "next_stage": record["next_stage"],
        "milestone_14_opened": record["milestone_14_opened"],
        "milestone_14_planning_ready": record["milestone_14_planning_ready"],
        "ready_for_plan_review": record["ready_for_plan_review"],
        "runtime_candidate_count": record["runtime_candidate_count"],
        "candidate_fixture_matrix_count": record["candidate_fixture_matrix_count"],
        "diagnostic_average_score": record["diagnostic_average_score"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "runtime_activation_performed": record["runtime_activation_performed"],
        "runtime_execution_performed": record["runtime_execution_performed"],
        "real_submission_allowed": record["real_submission_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "private_core_exposure": record["private_core_exposure"],
        "legal_certification": record["legal_certification"],
    }
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        f"revision={record['revision']}",
        f"task_id={record['task_id']}",
        f"signature={record['signature']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"planning_verdict={record['planning_verdict']}",
        f"next_stage={record['next_stage']}",
        f"milestone_14_opened={record['milestone_14_opened']}",
        f"milestone_14_planning_ready={record['milestone_14_planning_ready']}",
        f"ready_for_plan_review={record['ready_for_plan_review']}",
        f"runtime_candidate_count={record['runtime_candidate_count']}",
        f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}",
        f"diagnostic_case_count={record['diagnostic_case_count']}",
        f"diagnostic_pass_count={record['diagnostic_pass_count']}",
        f"diagnostic_failure_count={record['diagnostic_failure_count']}",
        f"diagnostic_average_score={record['diagnostic_average_score']}",
        f"kaggle_score_semantics={record['kaggle_score_semantics']}",
        f"runtime_activation_performed={record['runtime_activation_performed']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    objective_lines = "\n".join(
        f"- `{item['id']}` `{item['name']}`: `{item['status']}` - {item['description']}"
        for item in record["planning_objectives"]
    )
    task_chain_lines = "\n".join(f"- `{item}`" for item in record["planned_task_chain"])

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- planning_verdict: `{record['planning_verdict']}`
- next_stage: `{record['next_stage']}`

## Milestone 14 planning

- milestone_14_opened: `{record['milestone_14_opened']}`
- milestone_14_planning_ready: `{record['milestone_14_planning_ready']}`
- ready_for_plan_review: `{record['ready_for_plan_review']}`

## Planning objectives

{objective_lines}

## Planned task chain

{task_chain_lines}

## Boundary

- planning_only: `{record['planning_only']}`
- diagnostic_only: `{record['diagnostic_only']}`
- runtime_activation_performed: `{record['runtime_activation_performed']}`
- runtime_execution_performed: `{record['runtime_execution_performed']}`
- implementation_performed: `{record['implementation_performed']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`
"""
    markdown_path.write_text(markdown, encoding="utf-8")

    def _artifact_ref(path: Path) -> str:
        try:
            return str(path.relative_to(PROJECT_ROOT))
        except ValueError:
            return str(path)

    return {
        "json": _artifact_ref(json_path),
        "index": _artifact_ref(index_path),
        "manifest": _artifact_ref(manifest_path),
        "markdown": _artifact_ref(markdown_path),
    }


def main() -> int:
    record = build_milestone_14_planning_record()
    issues = validate_milestone_14_planning_record(record)
    if issues:
        print(f"{TASK_NAME}_INVALID")
        for issue in issues:
            print(issue)
        return 1

    artifacts = write_artifacts(record)

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(f"{TASK_NAME}_READY")
    print(f"{TASK_NAME}_VALID")
    print(record["signature"])
    print(record["baseline_commit"])
    print(record["task_mode"])
    print(record["task_verdict"])
    print(record["planning_verdict"])
    print(record["next_stage"])
    print(f"milestone_14_opened={record['milestone_14_opened']}")
    print(f"milestone_14_planning_ready={record['milestone_14_planning_ready']}")
    print(f"ready_for_plan_review={record['ready_for_plan_review']}")
    print(f"runtime_candidate_count={record['runtime_candidate_count']}")
    print(f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}")
    print(f"diagnostic_average_score={record['diagnostic_average_score']}")
    print(f"kaggle_score_semantics={record['kaggle_score_semantics']}")
    print(f"runtime_activation_performed={record['runtime_activation_performed']}")
    print(f"runtime_execution_performed={record['runtime_execution_performed']}")
    print(f"real_submission_allowed={record['real_submission_allowed']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
