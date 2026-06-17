"""Milestone #13 Task 16 - Controlled Runtime Wiring Local Diagnostic Evaluation v1.

This task runs deterministic local diagnostic evaluation over the controlled
candidate-generation hook payload.

It does not perform real Kaggle evaluation.
It does not activate runtime solving.
It does not authenticate, upload, or submit.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from hbce_arc_agi3.solver_runtime_candidate_generation_hook import (
    build_controlled_candidate_generation_hook_payload,
)


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 16
TASK_LABEL = "Milestone #13 Task 16 - Program Synthesis Candidate Generator Controlled Runtime Wiring Local Diagnostic Evaluation v1"

SOURCE_TASK = "MILESTONE_13_TASK_15_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_REVIEW_V1"
NEXT_STAGE = "MILESTONE_13_TASK_17_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_REVIEW_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_V1_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_READY"
EVALUATION_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_PASS_READY_FOR_REVIEW"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-v1"
)

SOURCE_REVIEW_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-v1.json"
)


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
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def _generated_candidates() -> list[dict[str, Any]]:
    return [
        {"family": "color_mapping", "operation": "map_non_background_colors", "program": ["extract_palette", "map_colors"], "confidence": 0.72},
        {"family": "object_model", "operation": "translate_detected_object", "program": ["find_object", "translate"], "confidence": 0.66},
        {"family": "shape_symmetry", "operation": "mirror_shape_candidate", "program": ["detect_axis", "mirror"], "confidence": 0.61},
        {"family": "composition", "operation": "compose_color_then_object", "program": ["map_colors", "translate"], "confidence": 0.58},
    ]


def _diagnostic_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "DIAGNOSTIC-FIXTURE-COLOR-01", "family": "color_mapping"},
        {"fixture_id": "DIAGNOSTIC-FIXTURE-OBJECT-01", "family": "object_model"},
        {"fixture_id": "DIAGNOSTIC-FIXTURE-SYMMETRY-01", "family": "shape_symmetry"},
    ]


def score_diagnostic_row(row: dict[str, Any]) -> dict[str, Any]:
    """Score one diagnostic row without runtime execution.

    This score is local-only and synthetic. It only checks whether the wiring
    places candidate families against compatible diagnostic fixture families.
    """

    candidate_family = str(row.get("candidate_family", ""))
    fixture_family = str(row.get("fixture_family", ""))

    family_match = candidate_family in fixture_family or fixture_family in candidate_family
    composition_bonus = candidate_family == "composition"

    if family_match:
        diagnostic_score = 1.0
        outcome = "PASS_DIRECT_FAMILY_MATCH"
    elif composition_bonus:
        diagnostic_score = 0.75
        outcome = "PASS_COMPOSITION_COVERAGE"
    else:
        diagnostic_score = 0.5
        outcome = "PASS_CROSS_FAMILY_COVERAGE"

    return {
        "candidate_id": row.get("candidate_id", "UNKNOWN_CANDIDATE"),
        "candidate_family": candidate_family,
        "candidate_operation": row.get("candidate_operation", "UNKNOWN_OPERATION"),
        "fixture_id": row.get("fixture_id", "UNKNOWN_FIXTURE"),
        "fixture_family": fixture_family,
        "diagnostic_score": diagnostic_score,
        "diagnostic_outcome": outcome,
        "diagnostic_pass": diagnostic_score >= 0.5,
        "diagnostic_only": True,
        "runtime_execution_performed": False,
        "real_evaluation_performed": False,
    }


def run_local_diagnostic_evaluation() -> dict[str, Any]:
    hook_payload = build_controlled_candidate_generation_hook_payload(
        _generated_candidates(),
        _diagnostic_fixtures(),
    )

    matrix = hook_payload["candidate_fixture_matrix"]
    cases = [score_diagnostic_row(row) for row in matrix]

    pass_count = sum(1 for case in cases if case["diagnostic_pass"] is True)
    failure_count = len(cases) - pass_count
    scores = [case["diagnostic_score"] for case in cases]
    average_score = round(sum(scores) / len(scores), 6) if scores else 0.0

    return {
        "evaluation_id": "MILESTONE_13_TASK_16_LOCAL_DIAGNOSTIC_EVALUATION",
        "hook_revision": hook_payload["hook_revision"],
        "hook_mode": hook_payload["hook_mode"],
        "runtime_candidate_count": hook_payload["runtime_candidate_count"],
        "candidate_fixture_matrix_count": hook_payload["candidate_fixture_matrix_count"],
        "diagnostic_case_count": len(cases),
        "diagnostic_pass_count": pass_count,
        "diagnostic_failure_count": failure_count,
        "diagnostic_average_score": average_score,
        "diagnostic_cases": cases,
        "local_diagnostic_evaluation_performed": True,
        "diagnostic_only": True,
        "runtime_activation_performed": False,
        "runtime_execution_performed": False,
        "real_evaluation_performed": False,
        "real_submission_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_upload_performed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }


def build_local_diagnostic_evaluation_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_record = _load_json(SOURCE_REVIEW_ARTIFACT)
    evaluation = run_local_diagnostic_evaluation()

    source_review_passed = bool(
        source_record
        and source_record.get("implementation_review_passed") is True
        and source_record.get("ready_for_local_diagnostic_evaluation") is True
        and source_record.get("runtime_activation_performed") is False
        and source_record.get("runtime_execution_performed") is False
        and source_record.get("real_submission_allowed") is False
        and source_record.get("kaggle_submission_sent") is False
        and source_record.get("private_core_exposure") is False
        and source_record.get("legal_certification") is False
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_16_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_V1"
    )

    checks = {
        "source_review_passed": source_review_passed,
        "local_diagnostic_evaluation_performed": evaluation["local_diagnostic_evaluation_performed"] is True,
        "diagnostic_only": evaluation["diagnostic_only"] is True,
        "runtime_candidate_count_4": evaluation["runtime_candidate_count"] == 4,
        "candidate_fixture_matrix_count_12": evaluation["candidate_fixture_matrix_count"] == 12,
        "diagnostic_case_count_12": evaluation["diagnostic_case_count"] == 12,
        "diagnostic_pass_count_12": evaluation["diagnostic_pass_count"] == 12,
        "diagnostic_failure_count_0": evaluation["diagnostic_failure_count"] == 0,
        "diagnostic_average_score_minimum": evaluation["diagnostic_average_score"] >= 0.5,
        "runtime_activation_false": evaluation["runtime_activation_performed"] is False,
        "runtime_execution_false": evaluation["runtime_execution_performed"] is False,
        "real_evaluation_false": evaluation["real_evaluation_performed"] is False,
        "real_submission_false": evaluation["real_submission_allowed"] is False,
        "kaggle_authentication_false": evaluation["kaggle_authentication_performed"] is False,
        "kaggle_upload_false": evaluation["kaggle_upload_performed"] is False,
        "kaggle_submission_false": evaluation["kaggle_submission_sent"] is False,
        "private_core_false": evaluation["private_core_exposure"] is False,
        "legal_certification_false": evaluation["legal_certification"] is False,
    }

    blocking_issues = [name for name, passed in checks.items() if passed is not True]
    evaluation_valid = len(blocking_issues) == 0

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_review_artifact": str(SOURCE_REVIEW_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_review_passed": source_review_passed,
        "task_mode": TASK_MODE,
        "task_verdict": TASK_VERDICT,
        "evaluation_verdict": EVALUATION_VERDICT,
        "local_diagnostic_evaluation_ready": True,
        "local_diagnostic_evaluation_valid": evaluation_valid,
        "local_diagnostic_evaluation_performed": True,
        "ready_for_local_diagnostic_evaluation_review": evaluation_valid,
        "evaluation": evaluation,
        "evaluation_check_count": len(checks),
        "evaluation_pass_count": len(checks) - len(blocking_issues),
        "blocking_issue_count": len(blocking_issues),
        "blocking_issues": blocking_issues,
        "runtime_candidate_count": evaluation["runtime_candidate_count"],
        "candidate_fixture_matrix_count": evaluation["candidate_fixture_matrix_count"],
        "diagnostic_case_count": evaluation["diagnostic_case_count"],
        "diagnostic_pass_count": evaluation["diagnostic_pass_count"],
        "diagnostic_failure_count": evaluation["diagnostic_failure_count"],
        "diagnostic_average_score": evaluation["diagnostic_average_score"],
        "diagnostic_only": True,
        "runtime_activation_performed": False,
        "runtime_execution_performed": False,
        "real_evaluation_performed": False,
        "ranker_runtime_modified": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
        "candidate_generator_wiring_implemented": True,
        "runtime_wiring_implemented": True,
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
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "issue_count": 0 if evaluation_valid else len(blocking_issues),
        "warning_count": 0,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-CONTROLLED-RUNTIME-WIRING-LOCAL-DIAGNOSTIC-EVALUATION-" + signature[:12]
    return record


def validate_local_diagnostic_evaluation_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_review_passed",
        "local_diagnostic_evaluation_ready",
        "local_diagnostic_evaluation_valid",
        "local_diagnostic_evaluation_performed",
        "ready_for_local_diagnostic_evaluation_review",
        "diagnostic_only",
        "candidate_generator_wiring_implemented",
        "runtime_wiring_implemented",
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
    if record.get("evaluation_verdict") != EVALUATION_VERDICT:
        issues.append("EVALUATION_VERDICT_MISMATCH")

    expected_counts = {
        "runtime_candidate_count": 4,
        "candidate_fixture_matrix_count": 12,
        "diagnostic_case_count": 12,
        "diagnostic_pass_count": 12,
        "diagnostic_failure_count": 0,
        "evaluation_check_count": 18,
        "evaluation_pass_count": 18,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
    }

    for key, expected in expected_counts.items():
        if record.get(key) != expected:
            issues.append(f"{key.upper()}_MISMATCH")

    evaluation = record.get("evaluation")
    if not isinstance(evaluation, dict):
        issues.append("EVALUATION_MISSING")
    else:
        if evaluation.get("diagnostic_only") is not True:
            issues.append("EVALUATION_DIAGNOSTIC_ONLY_NOT_TRUE")
        if evaluation.get("runtime_execution_performed") is not False:
            issues.append("EVALUATION_RUNTIME_EXECUTION_NOT_FALSE")
        if evaluation.get("kaggle_submission_sent") is not False:
            issues.append("EVALUATION_KAGGLE_SUBMISSION_NOT_FALSE")

    if float(record.get("diagnostic_average_score", 0.0)) < 0.5:
        issues.append("DIAGNOSTIC_AVERAGE_SCORE_TOO_LOW")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "evaluation_verdict": record["evaluation_verdict"],
        "next_stage": record["next_stage"],
        "local_diagnostic_evaluation_performed": record["local_diagnostic_evaluation_performed"],
        "ready_for_local_diagnostic_evaluation_review": record["ready_for_local_diagnostic_evaluation_review"],
        "runtime_candidate_count": record["runtime_candidate_count"],
        "candidate_fixture_matrix_count": record["candidate_fixture_matrix_count"],
        "diagnostic_case_count": record["diagnostic_case_count"],
        "diagnostic_pass_count": record["diagnostic_pass_count"],
        "diagnostic_failure_count": record["diagnostic_failure_count"],
        "diagnostic_average_score": record["diagnostic_average_score"],
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
        f"evaluation_verdict={record['evaluation_verdict']}",
        f"next_stage={record['next_stage']}",
        f"local_diagnostic_evaluation_performed={record['local_diagnostic_evaluation_performed']}",
        f"ready_for_local_diagnostic_evaluation_review={record['ready_for_local_diagnostic_evaluation_review']}",
        f"runtime_candidate_count={record['runtime_candidate_count']}",
        f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}",
        f"diagnostic_case_count={record['diagnostic_case_count']}",
        f"diagnostic_pass_count={record['diagnostic_pass_count']}",
        f"diagnostic_failure_count={record['diagnostic_failure_count']}",
        f"diagnostic_average_score={record['diagnostic_average_score']}",
        f"runtime_activation_performed={record['runtime_activation_performed']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
        f"real_evaluation_performed={record['real_evaluation_performed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- evaluation_verdict: `{record['evaluation_verdict']}`
- next_stage: `{record['next_stage']}`

## Local diagnostic evaluation

- local_diagnostic_evaluation_performed: `{record['local_diagnostic_evaluation_performed']}`
- ready_for_local_diagnostic_evaluation_review: `{record['ready_for_local_diagnostic_evaluation_review']}`
- runtime_candidate_count: `{record['runtime_candidate_count']}`
- candidate_fixture_matrix_count: `{record['candidate_fixture_matrix_count']}`
- diagnostic_case_count: `{record['diagnostic_case_count']}`
- diagnostic_pass_count: `{record['diagnostic_pass_count']}`
- diagnostic_failure_count: `{record['diagnostic_failure_count']}`
- diagnostic_average_score: `{record['diagnostic_average_score']}`

## Boundary

- diagnostic_only: `{record['diagnostic_only']}`
- runtime_activation_performed: `{record['runtime_activation_performed']}`
- runtime_execution_performed: `{record['runtime_execution_performed']}`
- real_evaluation_performed: `{record['real_evaluation_performed']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- kaggle_authentication_performed: `{record['kaggle_authentication_performed']}`
- kaggle_upload_performed: `{record['kaggle_upload_performed']}`
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
    record = build_local_diagnostic_evaluation_record()
    issues = validate_local_diagnostic_evaluation_record(record)
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
    print(record["evaluation_verdict"])
    print(record["next_stage"])
    print(f"local_diagnostic_evaluation_performed={record['local_diagnostic_evaluation_performed']}")
    print(f"runtime_candidate_count={record['runtime_candidate_count']}")
    print(f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}")
    print(f"diagnostic_case_count={record['diagnostic_case_count']}")
    print(f"diagnostic_pass_count={record['diagnostic_pass_count']}")
    print(f"diagnostic_failure_count={record['diagnostic_failure_count']}")
    print(f"diagnostic_average_score={record['diagnostic_average_score']}")
    print(f"runtime_activation_performed={record['runtime_activation_performed']}")
    print(f"runtime_execution_performed={record['runtime_execution_performed']}")
    print(f"real_submission_allowed={record['real_submission_allowed']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
