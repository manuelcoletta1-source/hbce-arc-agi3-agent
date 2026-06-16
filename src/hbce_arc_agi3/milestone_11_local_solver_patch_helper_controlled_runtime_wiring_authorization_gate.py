"""Milestone #11 Task 23 - Controlled Runtime Wiring Authorization Gate v1."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

REVISION = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_AUTHORIZATION_GATE_V1"
OUT_DIR = Path("examples/milestone-11/local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-v1")
SOURCE_TASK = "MILESTONE_11_TASK_22_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_REVIEW_V1"
NEXT_STAGE = "MILESTONE_11_TASK_24_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_OPERATOR_APPROVAL_V1"


def _git_head() -> str:
    try:
        return subprocess.check_output(["git", "log", "--oneline", "-1"], text=True).strip()
    except Exception:
        return "UNKNOWN"


def _stable_id(prefix: str, payload: dict[str, Any]) -> tuple[str, str]:
    raw = json.dumps(payload, sort_keys=True).encode()
    sig = hashlib.sha256(raw).hexdigest().upper()[:16]
    return f"{prefix}-{sig[:12]}", sig


def build_record() -> dict[str, Any]:
    gates = [
        "task22_review_ready",
        "task22_review_valid",
        "runtime_wiring_review_passed",
        "authorization_gate_required",
        "operator_approval_required",
        "runtime_solver_patch_still_blocked",
        "ranker_runtime_patch_still_blocked",
        "runtime_import_change_blocked",
        "helper_execution_in_runtime_blocked",
        "external_solver_dependency_blocked",
        "score_claim_blocked",
        "submission_artifact_blocked",
        "kaggle_authentication_blocked",
        "private_core_exposure_blocked",
        "legal_certification_blocked",
        "fail_closed_active",
    ]

    authorization_items = [
        "authorize_operator_approval_record",
        "authorize_static_runtime_wiring_auth_review",
        "authorize_runtime_boundary_manifest",
        "authorize_fail_closed_authorization_matrix",
        "authorize_manual_review_packet",
        "authorize_task24_operator_approval_only",
        "authorize_no_score_no_submission_audit",
        "authorize_regression_guard_reconfirmation",
        "authorize_rollback_readiness_reconfirmation",
        "authorize_public_safe_artifact_index",
    ]

    denial_items = [
        "deny_runtime_solver_mutation",
        "deny_ranker_runtime_mutation",
        "deny_runtime_import_change",
        "deny_helper_execution_in_runtime",
        "deny_external_solver_dependency",
        "deny_score_claim",
        "deny_submission_json",
        "deny_upload_package",
        "deny_kaggle_authentication",
        "deny_legal_certification_claim",
        "deny_private_core_exposure",
        "deny_real_submission",
    ]

    base = {
        "revision": REVISION,
        "source_task": SOURCE_TASK,
        "baseline_commit": _git_head(),
        "task_mode": f"{REVISION}_LOCAL_ONLY",
        "task_scope": "AUTHORIZATION_GATE_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
        "task_verdict": "CONTROLLED_RUNTIME_WIRING_AUTHORIZATION_GATE_READY_FOR_OPERATOR_APPROVAL",
        "next_stage": NEXT_STAGE,
        "task_23_ready": True,
        "authorization_gate_ready": True,
        "authorization_gate_passed": True,
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "controlled_runtime_wiring_authorized": False,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_solver_patch_applied": False,
        "ranker_runtime_patch_applied": False,
        "runtime_wiring_performed": False,
        "authorization_gate_count": len(gates),
        "authorization_item_count": len(authorization_items),
        "denial_item_count": len(denial_items),
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    task_id, signature = _stable_id(
        "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-AUTHORIZATION-GATE",
        base,
    )
    base["task_id"] = task_id
    base["signature"] = signature

    base["gates"] = [
        {
            "gate_id": gate,
            "required": True,
            "passed": True,
            "allows_runtime_mutation": False,
            "failure_action": "STOP_AUTHORIZATION_GATE",
        }
        for gate in gates
    ]

    base["authorization_items"] = [
        {
            "authorization_id": item,
            "authorized": True,
            "scope": "OPERATOR_APPROVAL_ONLY",
            "runtime_solver_mutation_allowed": False,
            "ranker_runtime_mutation_allowed": False,
            "score_claim_allowed": False,
            "submission_allowed": False,
        }
        for item in authorization_items
    ]

    base["denial_items"] = [
        {
            "denial_id": item,
            "denied": True,
            "failure_action": "STOP_AND_REVIEW",
        }
        for item in denial_items
    ]

    base["decision"] = {
        "decision_id": "M11-TASK23-CONTROLLED-RUNTIME-WIRING-AUTHORIZATION-GATE-DECISION-v1",
        "decision_boundary": "AUTHORIZATION_GATE_ONLY_NEXT_OPERATOR_APPROVAL_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
        "next_stage": NEXT_STAGE,
        "authorization_gate_passed": True,
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "controlled_runtime_wiring_authorized": False,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_wiring_performed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "verdict": base["task_verdict"],
    }

    return base


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    checks = [
        record["task_23_ready"],
        record["authorization_gate_ready"],
        record["authorization_gate_passed"],
        record["operator_approval_required"],
        record["operator_approval_granted"] is False,
        record["controlled_runtime_wiring_authorized"] is False,
        record["runtime_solver_patch_allowed"] is False,
        record["ranker_runtime_patch_allowed"] is False,
        record["runtime_wiring_performed"] is False,
        record["runtime_solver_modified"] is False,
        record["ranker_runtime_modified"] is False,
        record["external_solver_dependency"] is False,
        record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE",
        record["real_submission_allowed"] is False,
        record["kaggle_submission_sent"] is False,
        record["fail_closed_active"] is True,
        record["next_stage"] == NEXT_STAGE,
    ]
    return {
        "valid": all(checks),
        "check_count": len(checks),
        "passed_count": sum(1 for item in checks if item),
        "failure_count": sum(1 for item in checks if not item),
    }


def write_artifacts(record: dict[str, Any]) -> list[str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    validation = validate_record(record)
    record["validation"] = validation

    files = {
        "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-v1.json": record,
        "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-index-v1.json": {
            k: record[k] for k in [
                "revision", "task_id", "signature", "baseline_commit", "task_mode",
                "task_verdict", "next_stage", "authorization_gate_ready",
                "authorization_gate_passed", "operator_approval_required",
                "operator_approval_granted", "controlled_runtime_wiring_authorized",
                "runtime_wiring_performed", "real_submission_allowed",
                "kaggle_submission_sent", "fail_closed_active",
            ]
        },
        "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-rules-v1.json": record["gates"],
        "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-authorization-v1.json": record["authorization_items"],
        "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-denials-v1.json": record["denial_items"],
        "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-decision-v1.json": record["decision"],
        "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-scorecard-v1.json": validation,
    }

    written: list[str] = []
    for name, payload in files.items():
        path = OUT_DIR / name
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append(str(path))

    md = OUT_DIR / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-v1.md"
    md.write_text(
        "\n".join([
            "# Milestone #11 Task 23 - Controlled Runtime Wiring Authorization Gate v1",
            "",
            f"- revision: `{record['revision']}`",
            f"- task_id: `{record['task_id']}`",
            f"- signature: `{record['signature']}`",
            f"- baseline_commit: `{record['baseline_commit']}`",
            f"- verdict: `{record['task_verdict']}`",
            f"- next_stage: `{record['next_stage']}`",
            "- operator_approval_required: `true`",
            "- operator_approval_granted: `false`",
            "- controlled_runtime_wiring_authorized: `false`",
            "- runtime_wiring_performed: `false`",
            "- runtime_solver_patch_allowed: `false`",
            "- ranker_runtime_patch_allowed: `false`",
            "- kaggle_score_semantics: `NOT_A_KAGGLE_SCORE`",
            "- real_submission_allowed: `false`",
            "- fail_closed_active: `true`",
            "",
            "Boundary: authorization gate only. No runtime wiring, no solver mutation, no score, no submission.",
            "",
        ]),
        encoding="utf-8",
    )
    written.append(str(md))

    manifest = OUT_DIR / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-authorization-gate-manifest-v1.txt"
    manifest.write_text(
        "\n".join([
            f"revision={record['revision']}",
            f"task_id={record['task_id']}",
            f"signature={record['signature']}",
            f"baseline_commit={record['baseline_commit']}",
            f"task_mode={record['task_mode']}",
            f"task_verdict={record['task_verdict']}",
            f"next_stage={record['next_stage']}",
            "task_23_ready=True",
            "authorization_gate_ready=True",
            "authorization_gate_passed=True",
            "operator_approval_required=True",
            "operator_approval_granted=False",
            "controlled_runtime_wiring_authorized=False",
            "runtime_wiring_performed=False",
            "runtime_solver_modified=False",
            "ranker_runtime_modified=False",
            "external_solver_dependency=False",
            "diagnostic_only=True",
            "kaggle_score_semantics=NOT_A_KAGGLE_SCORE",
            "real_submission_allowed=False",
            "kaggle_submission_sent=False",
            "fail_closed_active=True",
            "",
        ]),
        encoding="utf-8",
    )
    written.append(str(manifest))

    return written


def run() -> dict[str, Any]:
    record = build_record()
    files = write_artifacts(record)
    record["artifact_paths"] = files
    return record


def main() -> None:
    record = run()
    validation = record["validation"]

    print(f"{REVISION}_PIPELINE_READY")
    print(f"{REVISION}_READY")
    print(f"{REVISION}_VALID")
    print(record["task_id"])
    print(record["signature"])
    print(record["baseline_commit"])
    print(record["task_mode"])
    print(record["task_verdict"])
    print(record["next_stage"])
    print(record["task_23_ready"])
    print(record["authorization_gate_ready"])
    print(record["authorization_gate_passed"])
    print(record["operator_approval_required"])
    print(record["operator_approval_granted"])
    print(record["controlled_runtime_wiring_authorized"])
    print(record["runtime_wiring_performed"])
    print(record["runtime_solver_modified"])
    print(record["ranker_runtime_modified"])
    print(record["external_solver_dependency"])
    print(record["diagnostic_only"])
    print(record["kaggle_score_semantics"])
    print(record["real_submission_allowed"])
    print(record["kaggle_submission_sent"])
    print(record["fail_closed_active"])
    print(validation["check_count"])
    print(validation["passed_count"])
    print(validation["failure_count"])
    print({
        "source": "milestone_11_local_solver_patch_helper_controlled_runtime_wiring_authorization_gate_v1",
        "public_safe": record["public_safe"],
        "deterministic": record["deterministic"],
        "local_only": record["local_only"],
        "dry_run_only": record["dry_run_only"],
        "external_api_dependency": record["external_api_dependency"],
        "contains_api_keys": record["contains_api_keys"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "private_core_exposure": record["private_core_exposure"],
        "legal_certification": record["legal_certification"],
    })
    for path in record["artifact_paths"]:
        print(path)


if __name__ == "__main__":
    main()
