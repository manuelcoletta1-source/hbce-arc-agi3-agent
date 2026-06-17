"""Milestone #13 Task 19 - Controlled Runtime Wiring Milestone Closure Review v1.

This task reviews the Milestone #13 controlled runtime wiring chain and checks
that the local diagnostic evaluation closure is ready for final milestone
closure.

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


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_MILESTONE_CLOSURE_REVIEW_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 19
TASK_LABEL = "Milestone #13 Task 19 - Program Synthesis Candidate Generator Controlled Runtime Wiring Milestone Closure Review v1"

SOURCE_TASK = "MILESTONE_13_TASK_18_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_13_TASK_20_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_MILESTONE_CLOSURE_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_MILESTONE_CLOSURE_REVIEW_V1_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_MILESTONE_CLOSURE_REVIEW_READY"
REVIEW_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_MILESTONE_CLOSURE_REVIEW_PASS_READY_FOR_FINAL_CLOSURE"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-milestone-closure-review-v1"
)

SOURCE_CLOSURE_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-v1.json"
)

REVIEW_SCOPE_ITEMS = [
    "controlled_runtime_wiring_plan_reviewed",
    "controlled_runtime_wiring_implementation_reviewed",
    "local_diagnostic_evaluation_completed",
    "local_diagnostic_evaluation_reviewed",
    "local_diagnostic_evaluation_closed",
    "not_kaggle_score_semantics_preserved",
    "runtime_execution_boundary_preserved",
    "submission_boundary_preserved",
    "public_safety_boundary_preserved",
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


def review_source_closure_artifact() -> dict[str, Any]:
    source = _load_json(SOURCE_CLOSURE_ARTIFACT)

    if source is None:
        return {
            "source_closure_artifact_present": False,
            "source_closure_artifact_parseable": False,
            "source_closure_passed": False,
            "source_record": None,
        }

    source_closure_passed = bool(
        source.get("local_diagnostic_evaluation_closure_valid") is True
        and source.get("local_diagnostic_evaluation_closed") is True
        and source.get("ready_for_milestone_closure_review") is True
        and source.get("runtime_candidate_count") == 4
        and source.get("candidate_fixture_matrix_count") == 12
        and source.get("diagnostic_case_count") == 12
        and source.get("diagnostic_pass_count") == 12
        and source.get("diagnostic_failure_count") == 0
        and source.get("diagnostic_average_score") == 0.6875
        and source.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
        and source.get("diagnostic_only") is True
        and source.get("runtime_activation_performed") is False
        and source.get("runtime_execution_performed") is False
        and source.get("real_evaluation_performed") is False
        and source.get("real_submission_allowed") is False
        and source.get("ready_for_real_kaggle_submission") is False
        and source.get("manual_upload_allowed") is False
        and source.get("kaggle_authentication_allowed") is False
        and source.get("kaggle_authentication_performed") is False
        and source.get("kaggle_upload_allowed") is False
        and source.get("kaggle_upload_performed") is False
        and source.get("kaggle_submission_sent") is False
        and source.get("external_api_dependency") is False
        and source.get("internet_during_eval") is False
        and source.get("private_core_exposure") is False
        and source.get("legal_certification") is False
        and source.get("next_stage")
        == "MILESTONE_13_TASK_19_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_MILESTONE_CLOSURE_REVIEW_V1"
    )

    return {
        "source_closure_artifact_present": True,
        "source_closure_artifact_parseable": True,
        "source_closure_passed": source_closure_passed,
        "source_record": source,
    }


def build_review_gate_map(source_record: dict[str, Any]) -> dict[str, bool]:
    return {
        "source_closure_valid": source_record.get("local_diagnostic_evaluation_closure_valid") is True,
        "source_closure_closed": source_record.get("local_diagnostic_evaluation_closed") is True,
        "ready_for_milestone_closure_review": source_record.get("ready_for_milestone_closure_review") is True,
        "runtime_candidate_count_4": source_record.get("runtime_candidate_count") == 4,
        "candidate_fixture_matrix_count_12": source_record.get("candidate_fixture_matrix_count") == 12,
        "diagnostic_case_count_12": source_record.get("diagnostic_case_count") == 12,
        "diagnostic_pass_count_12": source_record.get("diagnostic_pass_count") == 12,
        "diagnostic_failure_count_0": source_record.get("diagnostic_failure_count") == 0,
        "diagnostic_average_score_0_6875": source_record.get("diagnostic_average_score") == 0.6875,
        "not_kaggle_score": source_record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "diagnostic_only": source_record.get("diagnostic_only") is True,
        "runtime_activation_false": source_record.get("runtime_activation_performed") is False,
        "runtime_execution_false": source_record.get("runtime_execution_performed") is False,
        "real_evaluation_false": source_record.get("real_evaluation_performed") is False,
        "real_submission_false": source_record.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": source_record.get("ready_for_real_kaggle_submission") is False,
        "manual_upload_false": source_record.get("manual_upload_allowed") is False,
        "kaggle_authentication_allowed_false": source_record.get("kaggle_authentication_allowed") is False,
        "kaggle_authentication_performed_false": source_record.get("kaggle_authentication_performed") is False,
        "kaggle_upload_allowed_false": source_record.get("kaggle_upload_allowed") is False,
        "kaggle_upload_performed_false": source_record.get("kaggle_upload_performed") is False,
        "kaggle_submission_false": source_record.get("kaggle_submission_sent") is False,
        "external_api_dependency_false": source_record.get("external_api_dependency") is False,
        "internet_during_eval_false": source_record.get("internet_during_eval") is False,
        "private_core_false": source_record.get("private_core_exposure") is False,
        "legal_certification_false": source_record.get("legal_certification") is False,
        "official_score_claim_false": source_record.get("official_score_claim_allowed") is False,
        "competitive_score_claim_false": source_record.get("competitive_score_claim_allowed") is False,
        "local_only": source_record.get("local_only") is True,
        "deterministic": source_record.get("deterministic") is True,
        "public_safe": source_record.get("public_safe") is True,
        "public_overfit_false": source_record.get("public_overfit_allowed") is False,
        "public_overfit_guard_required": source_record.get("public_overfit_guard_required") is True,
        "operator_approval_required": source_record.get("operator_approval_required") is True,
        "operator_approval_received_false": source_record.get("operator_approval_received") is False,
        "fail_closed_required": source_record.get("fail_closed_required") is True,
        "fail_closed_active": source_record.get("fail_closed_active") is True,
    }


def build_milestone_closure_review_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_review = review_source_closure_artifact()
    source_record = source_review.get("source_record") if isinstance(source_review.get("source_record"), dict) else {}
    review_gates = build_review_gate_map(source_record)

    review_checks = {
        "source_closure_artifact_present": source_review["source_closure_artifact_present"] is True,
        "source_closure_artifact_parseable": source_review["source_closure_artifact_parseable"] is True,
        "source_closure_passed": source_review["source_closure_passed"] is True,
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
        "source_closure_artifact": str(SOURCE_CLOSURE_ARTIFACT.relative_to(PROJECT_ROOT)),
        "task_mode": TASK_MODE,
        "task_verdict": TASK_VERDICT,
        "review_verdict": REVIEW_VERDICT,
        "milestone_closure_review_ready": True,
        "milestone_closure_review_valid": review_valid,
        "milestone_closure_review_passed": review_valid,
        "ready_for_final_milestone_closure": review_valid,
        "review_scope_items": REVIEW_SCOPE_ITEMS,
        "review_scope_item_count": len(REVIEW_SCOPE_ITEMS),
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
        "diagnostic_case_count": source_record.get("diagnostic_case_count"),
        "diagnostic_pass_count": source_record.get("diagnostic_pass_count"),
        "diagnostic_failure_count": source_record.get("diagnostic_failure_count"),
        "diagnostic_average_score": source_record.get("diagnostic_average_score"),
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "diagnostic_only": True,
        "runtime_activation_performed": False,
        "runtime_execution_performed": False,
        "real_evaluation_performed": False,
        "ranker_runtime_modified": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
        "candidate_generator_wiring_implemented": True,
        "runtime_wiring_implemented": True,
        "local_diagnostic_evaluation_performed": True,
        "local_diagnostic_evaluation_review_passed": True,
        "local_diagnostic_evaluation_closed": True,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
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
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-CONTROLLED-RUNTIME-WIRING-MILESTONE-CLOSURE-REVIEW-" + signature[:12]
    return record


def validate_milestone_closure_review_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "milestone_closure_review_ready",
        "milestone_closure_review_valid",
        "milestone_closure_review_passed",
        "ready_for_final_milestone_closure",
        "diagnostic_only",
        "candidate_generator_wiring_implemented",
        "runtime_wiring_implemented",
        "local_diagnostic_evaluation_performed",
        "local_diagnostic_evaluation_review_passed",
        "local_diagnostic_evaluation_closed",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
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
        "real_evaluation_performed",
        "ranker_runtime_modified",
        "runtime_solver_modified",
        "candidate_generator_modified",
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
        "diagnostic_case_count": 12,
        "diagnostic_pass_count": 12,
        "diagnostic_failure_count": 0,
        "review_scope_item_count": 9,
        "review_gate_count": 37,
        "review_check_count": 40,
        "review_pass_count": 40,
        "review_failure_count": 0,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
    }

    for key, expected in expected_counts.items():
        if record.get(key) != expected:
            issues.append(f"{key.upper()}_MISMATCH")

    if record.get("diagnostic_average_score") != 0.6875:
        issues.append("DIAGNOSTIC_AVERAGE_SCORE_MISMATCH")
    if record.get("kaggle_score_semantics") != "NOT_A_KAGGLE_SCORE":
        issues.append("KAGGLE_SCORE_SEMANTICS_MISMATCH")

    source_review = record.get("source_review")
    if not isinstance(source_review, dict):
        issues.append("SOURCE_REVIEW_MISSING")
    else:
        if source_review.get("source_closure_passed") is not True:
            issues.append("SOURCE_CLOSURE_NOT_PASSED")

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

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-milestone-closure-review-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-milestone-closure-review-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-milestone-closure-review-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-milestone-closure-review-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "review_verdict": record["review_verdict"],
        "next_stage": record["next_stage"],
        "milestone_closure_review_passed": record["milestone_closure_review_passed"],
        "ready_for_final_milestone_closure": record["ready_for_final_milestone_closure"],
        "diagnostic_case_count": record["diagnostic_case_count"],
        "diagnostic_pass_count": record["diagnostic_pass_count"],
        "diagnostic_failure_count": record["diagnostic_failure_count"],
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
        f"review_verdict={record['review_verdict']}",
        f"next_stage={record['next_stage']}",
        f"milestone_closure_review_passed={record['milestone_closure_review_passed']}",
        f"ready_for_final_milestone_closure={record['ready_for_final_milestone_closure']}",
        f"runtime_candidate_count={record['runtime_candidate_count']}",
        f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}",
        f"diagnostic_case_count={record['diagnostic_case_count']}",
        f"diagnostic_pass_count={record['diagnostic_pass_count']}",
        f"diagnostic_failure_count={record['diagnostic_failure_count']}",
        f"diagnostic_average_score={record['diagnostic_average_score']}",
        f"kaggle_score_semantics={record['kaggle_score_semantics']}",
        f"runtime_activation_performed={record['runtime_activation_performed']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
        f"real_evaluation_performed={record['real_evaluation_performed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    scope_lines = "\n".join(f"- `{item}`" for item in record["review_scope_items"])

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- review_verdict: `{record['review_verdict']}`
- next_stage: `{record['next_stage']}`

## Milestone closure review

- milestone_closure_review_passed: `{record['milestone_closure_review_passed']}`
- ready_for_final_milestone_closure: `{record['ready_for_final_milestone_closure']}`
- runtime_candidate_count: `{record['runtime_candidate_count']}`
- candidate_fixture_matrix_count: `{record['candidate_fixture_matrix_count']}`
- diagnostic_case_count: `{record['diagnostic_case_count']}`
- diagnostic_pass_count: `{record['diagnostic_pass_count']}`
- diagnostic_failure_count: `{record['diagnostic_failure_count']}`
- diagnostic_average_score: `{record['diagnostic_average_score']}`
- kaggle_score_semantics: `{record['kaggle_score_semantics']}`

## Review scope

{scope_lines}

## Boundary

- diagnostic_only: `{record['diagnostic_only']}`
- runtime_activation_performed: `{record['runtime_activation_performed']}`
- runtime_execution_performed: `{record['runtime_execution_performed']}`
- real_evaluation_performed: `{record['real_evaluation_performed']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- kaggle_authentication_performed: `{record['kaggle_authentication_performed']}`
- kaggle_upload_performed: `{record['kaggle_upload_performed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- external_api_dependency: `{record['external_api_dependency']}`
- internet_during_eval: `{record['internet_during_eval']}`
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
    record = build_milestone_closure_review_record()
    issues = validate_milestone_closure_review_record(record)
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
    print(f"milestone_closure_review_passed={record['milestone_closure_review_passed']}")
    print(f"ready_for_final_milestone_closure={record['ready_for_final_milestone_closure']}")
    print(f"runtime_candidate_count={record['runtime_candidate_count']}")
    print(f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}")
    print(f"diagnostic_case_count={record['diagnostic_case_count']}")
    print(f"diagnostic_pass_count={record['diagnostic_pass_count']}")
    print(f"diagnostic_failure_count={record['diagnostic_failure_count']}")
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
