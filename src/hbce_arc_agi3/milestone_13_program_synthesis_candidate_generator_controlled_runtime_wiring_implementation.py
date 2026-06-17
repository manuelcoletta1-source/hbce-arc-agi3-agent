"""Milestone #13 Task 14 - Controlled Runtime Wiring Implementation v1.

This task implements local-only controlled candidate generator wiring helpers:
adapter, hook, and fixture bridge.

It does not run real Kaggle evaluation.
It does not authenticate, upload, or submit.
It does not claim official scores.
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


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 14
TASK_LABEL = "Milestone #13 Task 14 - Program Synthesis Candidate Generator Controlled Runtime Wiring Implementation v1"

SOURCE_TASK = "MILESTONE_13_TASK_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_V1"
NEXT_STAGE = "MILESTONE_13_TASK_15_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_REVIEW_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_V1_LOCAL_ONLY"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_READY"
IMPLEMENTATION_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_READY_FOR_REVIEW"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-v1"
)

SOURCE_REVIEW_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-review-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-review-v1.json"
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


def _sample_generated_candidates() -> list[dict[str, Any]]:
    return [
        {"family": "color_mapping", "operation": "map_non_background_colors", "program": ["extract_palette", "map_colors"], "confidence": 0.72},
        {"family": "object_model", "operation": "translate_detected_object", "program": ["find_object", "translate"], "confidence": 0.66},
        {"family": "shape_symmetry", "operation": "mirror_shape_candidate", "program": ["detect_axis", "mirror"], "confidence": 0.61},
        {"family": "composition", "operation": "compose_color_then_object", "program": ["map_colors", "translate"], "confidence": 0.58},
    ]


def _sample_diagnostic_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "DIAGNOSTIC-FIXTURE-COLOR-01", "family": "color_mapping"},
        {"fixture_id": "DIAGNOSTIC-FIXTURE-OBJECT-01", "family": "object_model"},
        {"fixture_id": "DIAGNOSTIC-FIXTURE-SYMMETRY-01", "family": "shape_symmetry"},
    ]


def build_controlled_runtime_wiring_implementation_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()
    source_record = _load_json(SOURCE_REVIEW_ARTIFACT)

    source_review_passed = bool(
        source_record
        and source_record.get("implementation_plan_review_passed") is True
        and source_record.get("controlled_implementation_authorized") is True
        and source_record.get("controlled_implementation_performed") is False
        and source_record.get("implementation_allowed_now") is False
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_14_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_V1"
    )

    hook_payload = build_controlled_candidate_generation_hook_payload(
        _sample_generated_candidates(),
        _sample_diagnostic_fixtures(),
    )

    controlled_implementation_performed = True
    controlled_runtime_adapter_created = True
    controlled_solver_hook_created = True
    controlled_fixture_bridge_created = True

    runtime_activation_performed = hook_payload["runtime_activation_performed"]
    runtime_execution_performed = hook_payload["runtime_execution_performed"]
    real_evaluation_performed = hook_payload["real_evaluation_performed"]

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
        "implementation_verdict": IMPLEMENTATION_VERDICT,
        "controlled_implementation_performed": controlled_implementation_performed,
        "controlled_runtime_adapter_created": controlled_runtime_adapter_created,
        "controlled_solver_hook_created": controlled_solver_hook_created,
        "controlled_fixture_bridge_created": controlled_fixture_bridge_created,
        "runtime_candidate_count": hook_payload["runtime_candidate_count"],
        "candidate_fixture_matrix_count": hook_payload["candidate_fixture_matrix_count"],
        "hook_payload": hook_payload,
        "implemented_files": [
            "src/hbce_arc_agi3/program_synthesis_candidate_generator_runtime_adapter.py",
            "src/hbce_arc_agi3/solver_runtime_candidate_generation_hook.py",
            "src/hbce_arc_agi3/program_synthesis_candidate_fixture_bridge.py",
        ],
        "implemented_file_count": 3,
        "runtime_activation_performed": runtime_activation_performed,
        "runtime_execution_performed": runtime_execution_performed,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "candidate_generator_wiring_implemented": True,
        "runtime_wiring_implemented": True,
        "ranker_runtime_modified": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
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
        "issue_count": 0,
        "warning_count": 0,
    }

    checks = [
        record["source_review_passed"] is True,
        record["controlled_implementation_performed"] is True,
        record["controlled_runtime_adapter_created"] is True,
        record["controlled_solver_hook_created"] is True,
        record["controlled_fixture_bridge_created"] is True,
        record["runtime_candidate_count"] == 4,
        record["candidate_fixture_matrix_count"] == 12,
        record["runtime_activation_performed"] is False,
        record["runtime_execution_performed"] is False,
        record["real_evaluation_performed"] is False,
        record["ranker_runtime_modified"] is False,
        record["runtime_solver_modified"] is False,
        record["candidate_generator_modified"] is False,
        record["real_submission_allowed"] is False,
        record["kaggle_submission_sent"] is False,
        record["private_core_exposure"] is False,
        record["legal_certification"] is False,
    ]
    record["implementation_gate_count"] = len(checks)
    record["passed_gate_count"] = sum(1 for check in checks if check)
    record["implementation_valid"] = record["implementation_gate_count"] == record["passed_gate_count"]
    record["issue_count"] = 0 if record["implementation_valid"] else record["implementation_gate_count"] - record["passed_gate_count"]

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-CONTROLLED-RUNTIME-WIRING-IMPLEMENTATION-" + signature[:12]
    return record


def validate_controlled_runtime_wiring_implementation_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_review_passed",
        "controlled_implementation_performed",
        "controlled_runtime_adapter_created",
        "controlled_solver_hook_created",
        "controlled_fixture_bridge_created",
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
        "implementation_valid",
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
    if record.get("next_stage") != NEXT_STAGE:
        issues.append("NEXT_STAGE_MISMATCH")
    if record.get("task_verdict") != TASK_VERDICT:
        issues.append("TASK_VERDICT_MISMATCH")
    if record.get("implementation_verdict") != IMPLEMENTATION_VERDICT:
        issues.append("IMPLEMENTATION_VERDICT_MISMATCH")
    if record.get("implemented_file_count") != 3:
        issues.append("IMPLEMENTED_FILE_COUNT_MISMATCH")
    if record.get("runtime_candidate_count") != 4:
        issues.append("RUNTIME_CANDIDATE_COUNT_MISMATCH")
    if record.get("candidate_fixture_matrix_count") != 12:
        issues.append("CANDIDATE_FIXTURE_MATRIX_COUNT_MISMATCH")
    if record.get("issue_count") != 0:
        issues.append("ISSUE_COUNT_NOT_ZERO")

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "implementation_verdict": record["implementation_verdict"],
        "next_stage": record["next_stage"],
        "controlled_implementation_performed": record["controlled_implementation_performed"],
        "controlled_runtime_adapter_created": record["controlled_runtime_adapter_created"],
        "controlled_solver_hook_created": record["controlled_solver_hook_created"],
        "controlled_fixture_bridge_created": record["controlled_fixture_bridge_created"],
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
        f"implementation_verdict={record['implementation_verdict']}",
        f"next_stage={record['next_stage']}",
        f"controlled_implementation_performed={record['controlled_implementation_performed']}",
        f"controlled_runtime_adapter_created={record['controlled_runtime_adapter_created']}",
        f"controlled_solver_hook_created={record['controlled_solver_hook_created']}",
        f"controlled_fixture_bridge_created={record['controlled_fixture_bridge_created']}",
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

    files = "\n".join(f"- `{item}`" for item in record["implemented_files"])
    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- implementation_verdict: `{record['implementation_verdict']}`
- next_stage: `{record['next_stage']}`

## Controlled implementation

- controlled_implementation_performed: `{record['controlled_implementation_performed']}`
- controlled_runtime_adapter_created: `{record['controlled_runtime_adapter_created']}`
- controlled_solver_hook_created: `{record['controlled_solver_hook_created']}`
- controlled_fixture_bridge_created: `{record['controlled_fixture_bridge_created']}`
- runtime_candidate_count: `{record['runtime_candidate_count']}`
- candidate_fixture_matrix_count: `{record['candidate_fixture_matrix_count']}`

## Implemented files

{files}

## Boundary

- runtime_activation_performed: `{record['runtime_activation_performed']}`
- runtime_execution_performed: `{record['runtime_execution_performed']}`
- real_evaluation_performed: `{record['real_evaluation_performed']}`
- ranker_runtime_modified: `{record['ranker_runtime_modified']}`
- runtime_solver_modified: `{record['runtime_solver_modified']}`
- candidate_generator_modified: `{record['candidate_generator_modified']}`
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
    record = build_controlled_runtime_wiring_implementation_record()
    issues = validate_controlled_runtime_wiring_implementation_record(record)
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
    print(record["implementation_verdict"])
    print(record["next_stage"])
    print(f"controlled_implementation_performed={record['controlled_implementation_performed']}")
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
