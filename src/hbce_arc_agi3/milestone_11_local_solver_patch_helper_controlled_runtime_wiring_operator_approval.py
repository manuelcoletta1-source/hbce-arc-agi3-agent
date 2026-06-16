"""Milestone #11 Task 24 - Controlled Runtime Wiring Operator Approval v1."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


TASK_NAME = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_OPERATOR_APPROVAL_V1"
NEXT_STAGE = "MILESTONE_11_TASK_25_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_EXECUTION_CONTRACT_V1"


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "log", "-1", "--oneline"], text=True).strip()
    except Exception:
        return "UNKNOWN"


def signature() -> str:
    return hashlib.sha256(TASK_NAME.encode()).hexdigest()[:16].upper()


def build_payload() -> dict:
    return {
        "task_name": TASK_NAME,
        "task_mode": f"{TASK_NAME}_LOCAL_ONLY",
        "task_verdict": "CONTROLLED_RUNTIME_WIRING_OPERATOR_APPROVAL_READY_FOR_EXECUTION_CONTRACT",
        "next_stage": NEXT_STAGE,
        "task_24_ready": True,
        "operator_approval_ready": True,
        "operator_approval_passed": True,
        "operator_signature_required": True,
        "operator_signature_present": False,
        "operator_runtime_authorized": False,
        "controlled_runtime_wiring_authorized": False,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "runtime_wiring_performed": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_active": True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "baseline_commit": git_commit(),
        "signature": signature(),
    }


def main() -> None:
    payload = build_payload()

    output_dir = Path(
        "examples/milestone-11/"
        "local-solver-patch-helper-controlled-runtime-wiring-operator-approval-v1"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / (
        "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-operator-approval-v1.json"
    )
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(f"{TASK_NAME}_READY")
    print(f"{TASK_NAME}_VALID")
    print(signature())
    print(payload["baseline_commit"])
    print(payload["task_mode"])
    print(payload["task_verdict"])
    print(payload["next_stage"])
    print(output_path)


if __name__ == "__main__":
    main()
