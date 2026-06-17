"""Milestone #13 Task 15 - Controlled Runtime Wiring Implementation Review v1.

This task reviews the local-only controlled runtime wiring implementation
introduced by Task 14.

It does not activate runtime execution.
It does not run real Kaggle evaluation.
It does not authenticate, upload, or submit.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from hbce_arc_agi3.program_synthesis_candidate_fixture_bridge import build_candidate_fixture_matrix
from hbce_arc_agi3.program_synthesis_candidate_generator_runtime_adapter import normalize_generated_candidates
from hbce_arc_agi3.solver_runtime_candidate_generation_hook import (
    build_controlled_candidate_generation_hook_payload,
)


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_REVIEW_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 15
TASK_LABEL = "Milestone #13 Task 15 - Program Synthesis Candidate Generator Controlled Runtime Wiring Implementation Review v1"

SOURCE_TASK = "MILESTONE_13_TASK_14_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_V1"
NEXT_STAGE = "MILESTONE_13_TASK_16_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_LOCAL_DIAGNOSTIC_EVALUATION_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_REVIEW_V1_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_REVIEW_READY"
REVIEW_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_REVIEW_PASS_READY_FOR_LOCAL_DIAGNOSTIC_EVALUATION"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-v1"
)

SOURCE_IMPLEMENTATION_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-v1.json"
)

IMPLEMENTED_FILES = [
    "src/hbce_arc_agi3/program_synthesis_candidate_generator_runtime_adapter.py",
    "src/hbce_arc_agi3/program_synthesis_candidate_fixture_bridge.py",
    "src/hbce_arc_agi3/solver_runtime_candidate_generation_hook.py",
]

REVIEW_FINDINGS = [
    {
        "finding_id": "TASK15-IMPLEMENTATION-REVIEW-01",
        "name": "runtime_adapter_present",
        "severity": "PASS",
        "description": "The runtime adapter module exists and normalizes generated candidates deterministically.",
    },
    {
        "finding_id": "TASK15-IMPLEMENTATION-REVIEW-02",
        "name": "fixture_bridge_present",
        "severity": "PASS",
        "description": "The fixture bridge module exists and builds diagnostic-only candidate/fixture matrices.",
    },
    {
        "finding_id": "TASK15-IMPLEMENTATION-REVIEW-03",
        "name": "solver_hook_present",
        "severity": "PASS",
        "description": "The controlled solver hook exists and returns a local-only blocked runtime payload.",
    },
    {
        "finding_id": "TASK15-IMPLEMENTATION-REVIEW-04",
        "name": "runtime_not_activated",
        "severity": "PASS",
        "description": "The implementation does not activate runtime solving or real evaluation.",
    },
    {
        "finding_id": "TASK15-IMPLEMENTATION-REVIEW-05",
        "name": "kaggle_actions_blocked",
        "severity": "PASS",
        "description": "Kaggle authentication, upload, and submission remain blocked.",
    },
    {
        "finding_id": "TASK15-IMPLEMENTATION-REVIEW-06",
        "name": "local_diagnostic_evaluation_can_open",
        "severity": "PASS",
        "description": "The next stage may run local diagnostic evaluation under boundaries.",
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


def review_implemented_file_presence() -> dict[str, Any]:
    rows = []
    for file_name in IMPLEMENTED_FILES:
        path = PROJECT_ROOT / file_name
        rows.append(
            {
                "file": file_name,
                "present": path.exists(),
                "is_file": path.is_file(),
            }
        )

    return {
        "implemented_file_count": len(rows),
        "present_file_count": sum(1 for row in rows if row["present"] and row["is_file"]),
        "all_implemented_files_present": all(row["present"] and row["is_file"] for row in rows),
        "files": rows,
    }


def review_runtime_candidate_adapter_behavior() -> dict[str, Any]:
    runtime_candidates = normalize_generated_candidates(_generated_candidates())

    candidate_ids = [candidate["candidate_id"] for candidate in runtime_candidates]

    return {
        "runtime_candidate_count": len(runtime_candidates),
        "runtime_candidate_ids_unique": len(candidate_ids) == len(set(candidate_ids)),
        "all_runtime_activation_blocked": all(
            candidate["runtime_activation_allowed"] is False for candidate in runtime_candidates
        ),
        "all_candidate_ids_runtime_prefixed": all(
            str(candidate["candidate_id"]).startswith("RUNTIME-CANDIDATE-")
            for candidate in runtime_candidates
        ),
        "runtime_candidates": runtime_candidates,
    }


def review_fixture_bridge_behavior() -> dict[str, Any]:
    runtime_candidates = normalize_generated_candidates(_generated_candidates())
    matrix = build_candidate_fixture_matrix(runtime_candidates, _diagnostic_fixtures())

    return {
        "candidate_fixture_matrix_count": len(matrix),
        "all_rows_diagnostic_only": all(row["diagnostic_only"] is True for row in matrix),
        "all_rows_runtime_execution_false": all(row["runtime_execution_performed"] is False for row in matrix),
        "all_rows_real_evaluation_false": all(row["real_evaluation_performed"] is False for row in matrix),
        "candidate_fixture_matrix": matrix,
    }


def review_solver_hook_behavior() -> dict[str, Any]:
    payload = build_controlled_candidate_generation_hook_payload(
        _generated_candidates(),
        _diagnostic_fixtures(),
    )

    return {
        "hook_revision": payload.get("hook_revision"),
        "hook_mode": payload.get("hook_mode"),
        "runtime_candidate_count": payload.get("runtime_candidate_count"),
        "candidate_fixture_matrix_count": payload.get("candidate_fixture_matrix_count"),
        "controlled_implementation_performed": payload.get("controlled_implementation_performed"),
        "runtime_activation_performed": payload.get("runtime_activation_performed"),
        "runtime_execution_performed": payload.get("runtime_execution_performed"),
        "real_evaluation_performed": payload.get("real_evaluation_performed"),
        "real_submission_allowed": payload.get("real_submission_allowed"),
        "kaggle_authentication_performed": payload.get("kaggle_authentication_performed"),
        "kaggle_upload_performed": payload.get("kaggle_upload_performed"),
        "kaggle_submission_sent": payload.get("kaggle_submission_sent"),
        "private_core_exposure": payload.get("private_core_exposure"),
        "legal_certification": payload.get("legal_certification"),
        "payload": payload,
    }


def build_controlled_runtime_wiring_implementation_review_record(
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_record = _load_json(SOURCE_IMPLEMENTATION_ARTIFACT)

    file_review = review_implemented_file_presence()
    adapter_review = review_runtime_candidate_adapter_behavior()
    bridge_review = review_fixture_bridge_behavior()
    hook_review = review_solver_hook_behavior()

    source_implementation_passed = bool(
        source_record
        and source_record.get("controlled_implementation_performed") is True
        and source_record.get("implementation_valid") is True
        and source_record.get("controlled_runtime_adapter_created") is True
        and source_record.get("controlled_solver_hook_created") is True
        and source_record.get("controlled_fixture_bridge_created") is True
        and source_record.get("runtime_candidate_count") == 4
        and source_record.get("candidate_fixture_matrix_count") == 12
        and source_record.get("runtime_activation_performed") is False
        and source_record.get("runtime_execution_performed") is False
        and source_record.get("real_submission_allowed") is False
        and source_record.get("kaggle_submission_sent") is False
        and source_record.get("private_core_exposure") is False
        and source_record.get("legal_certification") is False
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_15_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_REVIEW_V1"
    )

    checks = {
        "source_implementation_passed": source_implementation_passed,
        "all_implemented_files_present": file_review["all_implemented_files_present"] is True,
        "implemented_file_count_3": file_review["implemented_file_count"] == 3,
        "present_file_count_3": file_review["present_file_count"] == 3,
        "adapter_runtime_candidate_count_4": adapter_review["runtime_candidate_count"] == 4,
        "adapter_candidate_ids_unique": adapter_review["runtime_candidate_ids_unique"] is True,
        "adapter_runtime_activation_blocked": adapter_review["all_runtime_activation_blocked"] is True,
        "adapter_candidate_ids_runtime_prefixed": adapter_review["all_candidate_ids_runtime_prefixed"] is True,
        "bridge_matrix_count_12": bridge_review["candidate_fixture_matrix_count"] == 12,
        "bridge_rows_diagnostic_only": bridge_review["all_rows_diagnostic_only"] is True,
        "bridge_rows_runtime_execution_false": bridge_review["all_rows_runtime_execution_false"] is True,
        "bridge_rows_real_evaluation_false": bridge_review["all_rows_real_evaluation_false"] is True,
        "hook_runtime_candidate_count_4": hook_review["runtime_candidate_count"] == 4,
        "hook_matrix_count_12": hook_review["candidate_fixture_matrix_count"] == 12,
        "hook_controlled_implementation_performed_true": hook_review["controlled_implementation_performed"] is True,
        "hook_runtime_activation_false": hook_review["runtime_activation_performed"] is False,
        "hook_runtime_execution_false": hook_review["runtime_execution_performed"] is False,
        "hook_real_evaluation_false": hook_review["real_evaluation_performed"] is False,
        "hook_real_submission_false": hook_review["real_submission_allowed"] is False,
        "hook_kaggle_auth_false": hook_review["kaggle_authentication_performed"] is False,
        "hook_kaggle_upload_false": hook_review["kaggle_upload_performed"] is False,
        "hook_kaggle_submission_false": hook_review["kaggle_submission_sent"] is False,
        "hook_private_core_false": hook_review["private_core_exposure"] is False,
        "hook_legal_certification_false": hook_review["legal_certification"] is False,
    }

    blocking_issues = [name for name, passed in checks.items() if passed is not True]
    review_passed = len(blocking_issues) == 0

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_implementation_artifact": str(SOURCE_IMPLEMENTATION_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_implementation_passed": source_implementation_passed,
        "task_mode": TASK_MODE,
        "task_verdict": TASK_VERDICT,
        "review_verdict": REVIEW_VERDICT,
        "implementation_review_ready": True,
        "implementation_review_valid": review_passed,
        "implementation_review_passed": review_passed,
        "ready_for_local_diagnostic_evaluation": review_passed,
        "file_review": file_review,
        "adapter_review": adapter_review,
        "bridge_review": bridge_review,
        "hook_review": hook_review,
        "review_findings": REVIEW_FINDINGS,
        "review_finding_count": len(REVIEW_FINDINGS),
        "review_checks": checks,
        "review_check_count": len(checks),
        "review_pass_count": len(checks) - len(blocking_issues),
        "blocking_issue_count": len(blocking_issues),
        "blocking_issues": blocking_issues,
        "implemented_file_count": file_review["implemented_file_count"],
        "runtime_candidate_count": adapter_review["runtime_candidate_count"],
        "candidate_fixture_matrix_count": bridge_review["candidate_fixture_matrix_count"],
        "controlled_implementation_performed": True,
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
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "issue_count": 0 if review_passed else len(blocking_issues),
        "warning_count": 0,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-CONTROLLED-RUNTIME-WIRING-IMPLEMENTATION-REVIEW-" + signature[:12]
    return record


def validate_controlled_runtime_wiring_implementation_review_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_implementation_passed",
        "implementation_review_ready",
        "implementation_review_valid",
        "implementation_review_passed",
        "ready_for_local_diagnostic_evaluation",
        "controlled_implementation_performed",
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
    if record.get("review_verdict") != REVIEW_VERDICT:
        issues.append("REVIEW_VERDICT_MISMATCH")

    expected_counts = {
        "implemented_file_count": 3,
        "runtime_candidate_count": 4,
        "candidate_fixture_matrix_count": 12,
        "review_finding_count": 6,
        "review_check_count": 24,
        "review_pass_count": 24,
        "blocking_issue_count": 0,
        "issue_count": 0,
        "warning_count": 0,
    }

    for key, expected in expected_counts.items():
        if record.get(key) != expected:
            issues.append(f"{key.upper()}_MISMATCH")

    file_review = record.get("file_review")
    if not isinstance(file_review, dict) or file_review.get("all_implemented_files_present") is not True:
        issues.append("FILE_REVIEW_NOT_PASSED")

    adapter_review = record.get("adapter_review")
    if not isinstance(adapter_review, dict) or adapter_review.get("all_runtime_activation_blocked") is not True:
        issues.append("ADAPTER_REVIEW_NOT_PASSED")

    bridge_review = record.get("bridge_review")
    if not isinstance(bridge_review, dict) or bridge_review.get("all_rows_diagnostic_only") is not True:
        issues.append("BRIDGE_REVIEW_NOT_PASSED")

    hook_review = record.get("hook_review")
    if not isinstance(hook_review, dict):
        issues.append("HOOK_REVIEW_MISSING")
    else:
        if hook_review.get("runtime_activation_performed") is not False:
            issues.append("HOOK_RUNTIME_ACTIVATION_NOT_FALSE")
        if hook_review.get("runtime_execution_performed") is not False:
            issues.append("HOOK_RUNTIME_EXECUTION_NOT_FALSE")
        if hook_review.get("kaggle_submission_sent") is not False:
            issues.append("HOOK_KAGGLE_SUBMISSION_NOT_FALSE")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "review_verdict": record["review_verdict"],
        "next_stage": record["next_stage"],
        "source_implementation_passed": record["source_implementation_passed"],
        "implementation_review_passed": record["implementation_review_passed"],
        "ready_for_local_diagnostic_evaluation": record["ready_for_local_diagnostic_evaluation"],
        "implemented_file_count": record["implemented_file_count"],
        "runtime_candidate_count": record["runtime_candidate_count"],
        "candidate_fixture_matrix_count": record["candidate_fixture_matrix_count"],
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
        f"source_implementation_passed={record['source_implementation_passed']}",
        f"implementation_review_passed={record['implementation_review_passed']}",
        f"ready_for_local_diagnostic_evaluation={record['ready_for_local_diagnostic_evaluation']}",
        f"implemented_file_count={record['implemented_file_count']}",
        f"runtime_candidate_count={record['runtime_candidate_count']}",
        f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}",
        f"runtime_activation_performed={record['runtime_activation_performed']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
        f"real_evaluation_performed={record['real_evaluation_performed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    finding_lines = "\n".join(
        [
            f"- `{finding['finding_id']}` `{finding['name']}`: `{finding['severity']}` - {finding['description']}"
            for finding in record["review_findings"]
        ]
    )

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- review_verdict: `{record['review_verdict']}`
- next_stage: `{record['next_stage']}`

## Review result

- source_implementation_passed: `{record['source_implementation_passed']}`
- implementation_review_passed: `{record['implementation_review_passed']}`
- ready_for_local_diagnostic_evaluation: `{record['ready_for_local_diagnostic_evaluation']}`
- implemented_file_count: `{record['implemented_file_count']}`
- runtime_candidate_count: `{record['runtime_candidate_count']}`
- candidate_fixture_matrix_count: `{record['candidate_fixture_matrix_count']}`
- blocking_issue_count: `{record['blocking_issue_count']}`

## Findings

{finding_lines}

## Boundary

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
    record = build_controlled_runtime_wiring_implementation_review_record()
    issues = validate_controlled_runtime_wiring_implementation_review_record(record)
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
    print(f"implementation_review_passed={record['implementation_review_passed']}")
    print(f"ready_for_local_diagnostic_evaluation={record['ready_for_local_diagnostic_evaluation']}")
    print(f"implemented_file_count={record['implemented_file_count']}")
    print(f"runtime_candidate_count={record['runtime_candidate_count']}")
    print(f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}")
    print(f"runtime_activation_performed={record['runtime_activation_performed']}")
    print(f"runtime_execution_performed={record['runtime_execution_performed']}")
    print(f"real_submission_allowed={record['real_submission_allowed']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
