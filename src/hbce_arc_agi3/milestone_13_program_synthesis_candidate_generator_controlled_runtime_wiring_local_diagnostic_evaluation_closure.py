"""Milestone #13 Task 18 - Controlled Runtime Wiring Local Diagnostic Evaluation Closure v1.

This task closes the local diagnostic evaluation chain produced by Task 16 and
reviewed by Task 17.

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


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_CLOSURE_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 18
TASK_LABEL = "Milestone #13 Task 18 - Program Synthesis Candidate Generator Controlled Runtime Wiring Local Diagnostic Evaluation Closure v1"

SOURCE_TASK = "MILESTONE_13_TASK_17_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_REVIEW_V1"
NEXT_STAGE = "MILESTONE_13_TASK_19_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_MILESTONE_CLOSURE_REVIEW_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_CLOSURE_V1_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_CLOSURE_READY"
CLOSURE_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_CLOSED_READY_FOR_MILESTONE_CLOSURE_REVIEW"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-v1"
)

SOURCE_REVIEW_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-review-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-review-v1.json"
)

CLOSURE_DECISIONS = [
    {
        "decision_id": "TASK18-CLOSURE-01",
        "name": "accept_task16_diagnostic_evaluation",
        "status": "CLOSED_ACCEPTED",
        "description": "The Task 16 local diagnostic evaluation is accepted as deterministic local diagnostic evidence.",
    },
    {
        "decision_id": "TASK18-CLOSURE-02",
        "name": "accept_task17_review",
        "status": "CLOSED_ACCEPTED",
        "description": "The Task 17 review is accepted as passing and ready for closure.",
    },
    {
        "decision_id": "TASK18-CLOSURE-03",
        "name": "preserve_not_kaggle_score_semantics",
        "status": "CLOSED_ACCEPTED",
        "description": "The diagnostic score remains explicitly classified as NOT_A_KAGGLE_SCORE.",
    },
    {
        "decision_id": "TASK18-CLOSURE-04",
        "name": "preserve_no_runtime_execution_boundary",
        "status": "CLOSED_ACCEPTED",
        "description": "Runtime activation and runtime execution remain false.",
    },
    {
        "decision_id": "TASK18-CLOSURE-05",
        "name": "preserve_no_submission_boundary",
        "status": "CLOSED_ACCEPTED",
        "description": "Kaggle authentication, upload, and submission remain false.",
    },
    {
        "decision_id": "TASK18-CLOSURE-06",
        "name": "preserve_public_safety_boundary",
        "status": "CLOSED_ACCEPTED",
        "description": "No private core exposure, no API keys, no internet during evaluation, and no legal certification.",
    },
    {
        "decision_id": "TASK18-CLOSURE-07",
        "name": "advance_to_milestone_closure_review",
        "status": "CLOSED_ACCEPTED",
        "description": "The local diagnostic evaluation branch is closed and ready for milestone closure review.",
    },
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


def review_source_review_artifact() -> dict[str, Any]:
    source = _load_json(SOURCE_REVIEW_ARTIFACT)

    if source is None:
        return {
            "source_review_artifact_present": False,
            "source_review_artifact_parseable": False,
            "source_review_passed": False,
            "source_record": None,
        }

    source_review_passed = bool(
        source.get("local_diagnostic_evaluation_review_valid") is True
        and source.get("local_diagnostic_evaluation_review_passed") is True
        and source.get("ready_for_local_diagnostic_evaluation_closure") is True
        and source.get("runtime_candidate_count") == 4
        and source.get("candidate_fixture_matrix_count") == 12
        and source.get("diagnostic_case_count") == 12
        and source.get("diagnostic_pass_count") == 12
        and source.get("diagnostic_failure_count") == 0
        and source.get("diagnostic_average_score") == 0.6875
        and source.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE"
        and source.get("runtime_activation_performed") is False
        and source.get("runtime_execution_performed") is False
        and source.get("real_evaluation_performed") is False
        and source.get("real_submission_allowed") is False
        and source.get("kaggle_authentication_performed") is False
        and source.get("kaggle_upload_performed") is False
        and source.get("kaggle_submission_sent") is False
        and source.get("external_api_dependency") is False
        and source.get("internet_during_eval") is False
        and source.get("private_core_exposure") is False
        and source.get("legal_certification") is False
        and source.get("next_stage")
        == "MILESTONE_13_TASK_18_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_CLOSURE_V1"
    )

    return {
        "source_review_artifact_present": True,
        "source_review_artifact_parseable": True,
        "source_review_passed": source_review_passed,
        "source_record": source,
    }


def build_closure_gate_map(source_record: dict[str, Any]) -> dict[str, bool]:
    return {
        "source_review_passed": source_record.get("local_diagnostic_evaluation_review_passed") is True,
        "ready_for_closure": source_record.get("ready_for_local_diagnostic_evaluation_closure") is True,
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


def build_local_diagnostic_evaluation_closure_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_review = review_source_review_artifact()
    source_record = source_review.get("source_record") if isinstance(source_review.get("source_record"), dict) else {}
    closure_gates = build_closure_gate_map(source_record)

    gate_failures = [name for name, passed in closure_gates.items() if passed is not True]
    closure_valid = (
        source_review["source_review_artifact_present"] is True
        and source_review["source_review_artifact_parseable"] is True
        and source_review["source_review_passed"] is True
        and len(gate_failures) == 0
    )

    closure_checks = {
        "source_review_artifact_present": source_review["source_review_artifact_present"] is True,
        "source_review_artifact_parseable": source_review["source_review_artifact_parseable"] is True,
        "source_review_passed": source_review["source_review_passed"] is True,
        **closure_gates,
    }

    blocking_issues = [name for name, passed in closure_checks.items() if passed is not True]

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_review_artifact": str(SOURCE_REVIEW_ARTIFACT.relative_to(PROJECT_ROOT)),
        "task_mode": TASK_MODE,
        "task_verdict": TASK_VERDICT,
        "closure_verdict": CLOSURE_VERDICT,
        "local_diagnostic_evaluation_closure_ready": True,
        "local_diagnostic_evaluation_closure_valid": closure_valid,
        "local_diagnostic_evaluation_closed": closure_valid,
        "ready_for_milestone_closure_review": closure_valid,
        "source_review": source_review,
        "closure_decisions": CLOSURE_DECISIONS,
        "closure_decision_count": len(CLOSURE_DECISIONS),
        "closure_gates": closure_gates,
        "closure_gate_count": len(closure_gates),
        "closure_checks": closure_checks,
        "closure_check_count": len(closure_checks),
        "closure_pass_count": len(closure_checks) - len(blocking_issues),
        "closure_failure_count": len(blocking_issues),
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
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-CONTROLLED-RUNTIME-WIRING-LOCAL-DIAGNOSTIC-EVALUATION-CLOSURE-" + signature[:12]
    return record


def validate_local_diagnostic_evaluation_closure_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "local_diagnostic_evaluation_closure_ready",
        "local_diagnostic_evaluation_closure_valid",
        "local_diagnostic_evaluation_closed",
        "ready_for_milestone_closure_review",
        "diagnostic_only",
        "candidate_generator_wiring_implemented",
        "runtime_wiring_implemented",
        "local_diagnostic_evaluation_performed",
        "local_diagnostic_evaluation_review_passed",
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
    if record.get("closure_verdict") != CLOSURE_VERDICT:
        issues.append("CLOSURE_VERDICT_MISMATCH")

    expected_counts = {
        "runtime_candidate_count": 4,
        "candidate_fixture_matrix_count": 12,
        "diagnostic_case_count": 12,
        "diagnostic_pass_count": 12,
        "diagnostic_failure_count": 0,
        "closure_decision_count": 7,
        "closure_gate_count": 36,
        "closure_check_count": 38,
        "closure_pass_count": 38,
        "closure_failure_count": 0,
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
        if source_review.get("source_review_passed") is not True:
            issues.append("SOURCE_REVIEW_NOT_PASSED")

    closure_gates = record.get("closure_gates")
    if not isinstance(closure_gates, dict):
        issues.append("CLOSURE_GATES_MISSING")
    else:
        failed = [name for name, passed in closure_gates.items() if passed is not True]
        if failed:
            issues.append("CLOSURE_GATES_FAILED")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "closure_verdict": record["closure_verdict"],
        "next_stage": record["next_stage"],
        "local_diagnostic_evaluation_closed": record["local_diagnostic_evaluation_closed"],
        "ready_for_milestone_closure_review": record["ready_for_milestone_closure_review"],
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
        f"closure_verdict={record['closure_verdict']}",
        f"next_stage={record['next_stage']}",
        f"local_diagnostic_evaluation_closed={record['local_diagnostic_evaluation_closed']}",
        f"ready_for_milestone_closure_review={record['ready_for_milestone_closure_review']}",
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

    decision_lines = "\n".join(
        [
            f"- `{decision['decision_id']}` `{decision['name']}`: `{decision['status']}` - {decision['description']}"
            for decision in record["closure_decisions"]
        ]
    )

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- closure_verdict: `{record['closure_verdict']}`
- next_stage: `{record['next_stage']}`

## Closure

- local_diagnostic_evaluation_closed: `{record['local_diagnostic_evaluation_closed']}`
- ready_for_milestone_closure_review: `{record['ready_for_milestone_closure_review']}`
- runtime_candidate_count: `{record['runtime_candidate_count']}`
- candidate_fixture_matrix_count: `{record['candidate_fixture_matrix_count']}`
- diagnostic_case_count: `{record['diagnostic_case_count']}`
- diagnostic_pass_count: `{record['diagnostic_pass_count']}`
- diagnostic_failure_count: `{record['diagnostic_failure_count']}`
- diagnostic_average_score: `{record['diagnostic_average_score']}`
- kaggle_score_semantics: `{record['kaggle_score_semantics']}`

## Closure decisions

{decision_lines}

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
    record = build_local_diagnostic_evaluation_closure_record()
    issues = validate_local_diagnostic_evaluation_closure_record(record)
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
    print(record["closure_verdict"])
    print(record["next_stage"])
    print(f"local_diagnostic_evaluation_closed={record['local_diagnostic_evaluation_closed']}")
    print(f"ready_for_milestone_closure_review={record['ready_for_milestone_closure_review']}")
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
