"""Milestone #14 Task 2 - Local Solver Controlled Runtime Integration Plan Review v1.

Reviews the Task 1 planning artifact before any implementation work.

This is review-only.
It does not modify solver runtime.
It does not execute runtime solving.
It does not authenticate, upload, submit, or claim Kaggle score.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLAN_REVIEW_V1"
MILESTONE_NUMBER = 14
TASK_NUMBER = 2
TASK_LABEL = "Milestone #14 Task 2 - Local Solver Controlled Runtime Integration Plan Review v1"

SOURCE_TASK = "MILESTONE_14_TASK_1_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLANNING_V1"
NEXT_STAGE = "MILESTONE_14_TASK_3_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_PLAN_V1"

TASK_MODE = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLAN_REVIEW_V1_REVIEW_ONLY_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_14_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLAN_REVIEW_READY"
REVIEW_VERDICT = "LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLAN_REVIEW_PASS_READY_FOR_IMPLEMENTATION_PLAN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-14" / "local-solver-controlled-runtime-integration-plan-review-v1"

SOURCE_PLANNING_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-14"
    / "local-solver-controlled-runtime-integration-planning-v1"
    / "milestone-14-local-solver-controlled-runtime-integration-planning-v1.json"
)

REVIEW_DIMENSIONS = [
    "source_planning_artifact_present",
    "source_planning_artifact_valid",
    "milestone_14_opened",
    "planning_ready_for_review",
    "objective_count_complete",
    "planned_chain_complete",
    "not_kaggle_score_preserved",
    "no_runtime_activation",
    "no_runtime_execution",
    "no_implementation_performed",
    "no_kaggle_auth_upload_submission",
    "public_safe_boundary_preserved",
    "fail_closed_boundary_preserved",
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


def review_source_planning_artifact() -> dict[str, Any]:
    source = _load_json(SOURCE_PLANNING_ARTIFACT)

    if source is None:
        return {
            "source_planning_artifact_present": False,
            "source_planning_artifact_parseable": False,
            "source_planning_artifact_valid": False,
            "source_record": None,
        }

    valid = bool(
        source.get("milestone_14_opened") is True
        and source.get("milestone_14_planning_ready") is True
        and source.get("ready_for_plan_review") is True
        and source.get("planning_objective_count") == 8
        and source.get("planned_task_chain_count") == 6
        and source.get("planning_gate_count") == 15
        and source.get("planning_failure_count") == 0
        and source.get("blocking_issue_count") == 0
        and source.get("runtime_candidate_count") == 4
        and source.get("candidate_fixture_matrix_count") == 12
        and source.get("diagnostic_average_score") == 0.6875
        and source.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
        and source.get("planning_only") is True
        and source.get("diagnostic_only") is True
        and source.get("runtime_activation_performed") is False
        and source.get("runtime_execution_performed") is False
        and source.get("implementation_performed") is False
        and source.get("real_submission_allowed") is False
        and source.get("kaggle_authentication_performed") is False
        and source.get("kaggle_upload_performed") is False
        and source.get("kaggle_submission_sent") is False
        and source.get("private_core_exposure") is False
        and source.get("legal_certification") is False
        and source.get("next_stage") == "MILESTONE_14_TASK_2_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_PLAN_REVIEW_V1"
    )

    return {
        "source_planning_artifact_present": True,
        "source_planning_artifact_parseable": True,
        "source_planning_artifact_valid": valid,
        "source_record": source,
    }


def build_review_gate_map(source_record: dict[str, Any]) -> dict[str, bool]:
    return {
        "milestone_14_opened": source_record.get("milestone_14_opened") is True,
        "planning_ready": source_record.get("milestone_14_planning_ready") is True,
        "ready_for_plan_review": source_record.get("ready_for_plan_review") is True,
        "planning_objective_count_8": source_record.get("planning_objective_count") == 8,
        "planned_task_chain_count_6": source_record.get("planned_task_chain_count") == 6,
        "runtime_candidate_count_4": source_record.get("runtime_candidate_count") == 4,
        "candidate_fixture_matrix_count_12": source_record.get("candidate_fixture_matrix_count") == 12,
        "diagnostic_average_score_0_6875": source_record.get("diagnostic_average_score") == 0.6875,
        "not_kaggle_score": source_record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "planning_only": source_record.get("planning_only") is True,
        "diagnostic_only": source_record.get("diagnostic_only") is True,
        "runtime_activation_false": source_record.get("runtime_activation_performed") is False,
        "runtime_execution_false": source_record.get("runtime_execution_performed") is False,
        "implementation_false": source_record.get("implementation_performed") is False,
        "real_submission_false": source_record.get("real_submission_allowed") is False,
        "kaggle_authentication_false": source_record.get("kaggle_authentication_performed") is False,
        "kaggle_upload_false": source_record.get("kaggle_upload_performed") is False,
        "kaggle_submission_false": source_record.get("kaggle_submission_sent") is False,
        "private_core_false": source_record.get("private_core_exposure") is False,
        "legal_certification_false": source_record.get("legal_certification") is False,
        "public_safe": source_record.get("public_safe") is True,
        "fail_closed_active": source_record.get("fail_closed_active") is True,
    }


def build_plan_review_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_review = review_source_planning_artifact()
    source_record = source_review.get("source_record") if isinstance(source_review.get("source_record"), dict) else {}
    review_gates = build_review_gate_map(source_record)

    review_checks = {
        "source_planning_artifact_present": source_review["source_planning_artifact_present"] is True,
        "source_planning_artifact_parseable": source_review["source_planning_artifact_parseable"] is True,
        "source_planning_artifact_valid": source_review["source_planning_artifact_valid"] is True,
        **review_gates,
    }

    blocking_issues = [name for name, passed in review_checks.items() if passed is not True]
    review_valid = len(blocking_issues) == 0

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_planning_artifact": str(SOURCE_PLANNING_ARTIFACT.relative_to(PROJECT_ROOT)),
        "task_mode": TASK_MODE,
        "task_verdict": TASK_VERDICT,
        "review_verdict": REVIEW_VERDICT,
        "plan_review_ready": True,
        "plan_review_valid": review_valid,
        "plan_review_passed": review_valid,
        "ready_for_implementation_plan": review_valid,
        "review_dimensions": REVIEW_DIMENSIONS,
        "review_dimension_count": len(REVIEW_DIMENSIONS),
        "source_review": source_review,
        "review_gates": review_gates,
        "review_gate_count": len(review_gates),
        "review_checks": review_checks,
        "review_check_count": len(review_checks),
        "review_pass_count": len(review_checks) - len(blocking_issues),
        "review_failure_count": len(blocking_issues),
        "blocking_issue_count": len(blocking_issues),
        "blocking_issues": blocking_issues,
        "runtime_candidate_count": source_record.get("runtime_candidate_count"),
        "candidate_fixture_matrix_count": source_record.get("candidate_fixture_matrix_count"),
        "diagnostic_average_score": source_record.get("diagnostic_average_score"),
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "review_only": True,
        "planning_only_source": True,
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
    record["task_id"] = "MILESTONE-14-LOCAL-SOLVER-CONTROLLED-RUNTIME-INTEGRATION-PLAN-REVIEW-" + signature[:12]
    return record


def validate_plan_review_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "plan_review_ready",
        "plan_review_valid",
        "plan_review_passed",
        "ready_for_implementation_plan",
        "review_only",
        "planning_only_source",
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
    if record.get("source_task") != SOURCE_TASK:
        issues.append("SOURCE_TASK_MISMATCH")
    if record.get("next_stage") != NEXT_STAGE:
        issues.append("NEXT_STAGE_MISMATCH")
    if record.get("task_verdict") != TASK_VERDICT:
        issues.append("TASK_VERDICT_MISMATCH")
    if record.get("review_verdict") != REVIEW_VERDICT:
        issues.append("REVIEW_VERDICT_MISMATCH")

    expected_counts = {
        "runtime_candidate_count": 4,
        "candidate_fixture_matrix_count": 12,
        "review_dimension_count": 13,
        "review_gate_count": 22,
        "review_failure_count": 0,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
    }

    for key, expected in expected_counts.items():
        if record.get(key) != expected:
            issues.append(f"{key.upper()}_MISMATCH")

    review_checks = record.get("review_checks")
    if not isinstance(review_checks, dict):
        issues.append("REVIEW_CHECKS_MISSING")
    else:
        if record.get("review_check_count") != len(review_checks):
            issues.append("REVIEW_CHECK_COUNT_MISMATCH")
        if record.get("review_pass_count") != len(review_checks):
            issues.append("REVIEW_PASS_COUNT_MISMATCH")

    if record.get("diagnostic_average_score") != 0.6875:
        issues.append("DIAGNOSTIC_AVERAGE_SCORE_MISMATCH")
    if record.get("kaggle_score_semantics") != "NOT_A_KAGGLE_SCORE":
        issues.append("KAGGLE_SCORE_SEMANTICS_MISMATCH")

    source_review = record.get("source_review")
    if not isinstance(source_review, dict):
        issues.append("SOURCE_REVIEW_MISSING")
    else:
        if source_review.get("source_planning_artifact_valid") is not True:
            issues.append("SOURCE_PLANNING_ARTIFACT_NOT_VALID")

    review_gates = record.get("review_gates")
    if not isinstance(review_gates, dict):
        issues.append("REVIEW_GATES_MISSING")
    else:
        failed = [name for name, passed in review_gates.items() if passed is not True]
        if failed:
            issues.append("REVIEW_GATES_FAILED")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-plan-review-v1.json"
    index_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-plan-review-index-v1.json"
    manifest_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-plan-review-manifest-v1.txt"
    markdown_path = target_dir / "milestone-14-local-solver-controlled-runtime-integration-plan-review-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "review_verdict": record["review_verdict"],
        "next_stage": record["next_stage"],
        "plan_review_passed": record["plan_review_passed"],
        "ready_for_implementation_plan": record["ready_for_implementation_plan"],
        "runtime_candidate_count": record["runtime_candidate_count"],
        "candidate_fixture_matrix_count": record["candidate_fixture_matrix_count"],
        "diagnostic_average_score": record["diagnostic_average_score"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "runtime_activation_performed": record["runtime_activation_performed"],
        "runtime_execution_performed": record["runtime_execution_performed"],
        "implementation_performed": record["implementation_performed"],
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
        f"review_verdict={record['review_verdict']}",
        f"next_stage={record['next_stage']}",
        f"plan_review_passed={record['plan_review_passed']}",
        f"ready_for_implementation_plan={record['ready_for_implementation_plan']}",
        f"runtime_candidate_count={record['runtime_candidate_count']}",
        f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}",
        f"diagnostic_average_score={record['diagnostic_average_score']}",
        f"kaggle_score_semantics={record['kaggle_score_semantics']}",
        f"runtime_activation_performed={record['runtime_activation_performed']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
        f"implementation_performed={record['implementation_performed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    dimension_lines = "\n".join(f"- `{item}`" for item in record["review_dimensions"])

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- review_verdict: `{record['review_verdict']}`
- next_stage: `{record['next_stage']}`

## Plan review

- plan_review_passed: `{record['plan_review_passed']}`
- ready_for_implementation_plan: `{record['ready_for_implementation_plan']}`

## Review dimensions

{dimension_lines}

## Boundary

- review_only: `{record['review_only']}`
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
    record = build_plan_review_record()
    issues = validate_plan_review_record(record)
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
    print(record["review_verdict"])
    print(record["next_stage"])
    print(f"plan_review_passed={record['plan_review_passed']}")
    print(f"ready_for_implementation_plan={record['ready_for_implementation_plan']}")
    print(f"runtime_candidate_count={record['runtime_candidate_count']}")
    print(f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}")
    print(f"diagnostic_average_score={record['diagnostic_average_score']}")
    print(f"kaggle_score_semantics={record['kaggle_score_semantics']}")
    print(f"runtime_activation_performed={record['runtime_activation_performed']}")
    print(f"runtime_execution_performed={record['runtime_execution_performed']}")
    print(f"implementation_performed={record['implementation_performed']}")
    print(f"real_submission_allowed={record['real_submission_allowed']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
