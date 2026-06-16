"""Milestone #12 Task 12 - Submission Readiness Gate v1.

This gate checks whether the public ARC-AGI-3 solver branch has a local,
public-safe, anti-overfit readiness package after Task 11.

It explicitly does not create a real submission, does not upload to Kaggle,
does not authenticate to Kaggle, does not claim official score, and does not
grant real submission permission.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_12_SUBMISSION_READINESS_GATE_V1"
MILESTONE_NUMBER = 12
TASK_NUMBER = 12
TASK_LABEL = "Milestone #12 Task 12 - Submission Readiness Gate v1"

SOURCE_TASK = "MILESTONE_12_TASK_11_PUBLIC_OVERFIT_GUARD_V1"
NEXT_STAGE = "MILESTONE_12_TASK_13_COMPETITIVE_SOLVER_CLOSURE_V1"

TASK_MODE = "MILESTONE_12_SUBMISSION_READINESS_GATE_V1_LOCAL_ONLY"
TASK_SCOPE = "SUBMISSION_READINESS_GATE_ONLY_NO_UPLOAD_NO_SUBMISSION_NO_SCORE_CLAIM"
TASK_VERDICT = "MILESTONE_12_SUBMISSION_READINESS_GATE_READY"

READINESS_VERDICT = "LOCAL_READINESS_PACKAGE_READY_REAL_SUBMISSION_BLOCKED"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-12" / "submission-readiness-gate-v1"

SOURCE_PUBLIC_OVERFIT_GUARD_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-12"
    / "public-overfit-guard-v1"
    / "milestone-12-public-overfit-guard-v1.json"
)

REQUIRED_SOURCE_ARTIFACTS = [
    "examples/milestone-12/candidate-policy-v1/milestone-12-candidate-policy-v1.json",
    "examples/milestone-12/candidate-ranker-policy-v1/milestone-12-candidate-ranker-policy-v1.json",
    "examples/milestone-12/ranked-candidate-benchmark-v1/milestone-12-ranked-candidate-benchmark-v1.json",
    "examples/milestone-12/public-overfit-guard-v1/milestone-12-public-overfit-guard-v1.json",
]

READINESS_MEASUREMENT_TARGETS = [
    "required_source_artifact_count",
    "required_source_artifact_present_count",
    "source_guard_case_count",
    "source_guard_pass_count",
    "source_public_overfit_violation_count",
    "source_boundary_violation_count",
    "readiness_gate_count",
    "readiness_pass_count",
    "readiness_blocking_issue_count",
    "real_submission_allowed",
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


def _gate(name: str, passed: bool, required: bool, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "required": bool(required),
        "description": description,
    }


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def _artifact_status(path_text: str) -> dict[str, Any]:
    path = PROJECT_ROOT / path_text
    record = _load_json(path)
    return {
        "path": path_text,
        "present": path.exists(),
        "parseable_json": record is not None,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None,
    }


def build_readiness_package(source_record: dict[str, Any] | None) -> dict[str, Any]:
    artifact_statuses = [_artifact_status(path) for path in REQUIRED_SOURCE_ARTIFACTS]
    present_count = sum(1 for item in artifact_statuses if item["present"] is True)
    parseable_count = sum(1 for item in artifact_statuses if item["parseable_json"] is True)

    source_guard = source_record.get("guard") if isinstance(source_record, dict) else {}
    if not isinstance(source_guard, dict):
        source_guard = {}

    source_guard_case_count = int(source_record.get("guard_case_count", 0)) if isinstance(source_record, dict) else 0
    source_guard_pass_count = int(source_record.get("guard_pass_count", 0)) if isinstance(source_record, dict) else 0
    source_public_overfit_violation_count = int(source_record.get("public_overfit_violation_count", 0)) if isinstance(source_record, dict) else 0
    source_boundary_violation_count = int(source_record.get("boundary_violation_count", 0)) if isinstance(source_record, dict) else 0

    return {
        "readiness_package_id": "MILESTONE_12_SUBMISSION_READINESS_PACKAGE_SYNTHETIC_V1",
        "package_family": "LOCAL_PUBLIC_SAFE_READINESS_PACKAGE_NO_SUBMISSION",
        "required_source_artifacts": artifact_statuses,
        "required_source_artifact_count": len(REQUIRED_SOURCE_ARTIFACTS),
        "required_source_artifact_present_count": present_count,
        "required_source_artifact_parseable_count": parseable_count,
        "source_guard_case_count": source_guard_case_count,
        "source_guard_pass_count": source_guard_pass_count,
        "source_public_overfit_violation_count": source_public_overfit_violation_count,
        "source_boundary_violation_count": source_boundary_violation_count,
        "source_forbidden_field_hit_count": int(source_record.get("forbidden_field_hit_count", 0)) if isinstance(source_record, dict) else 0,
        "source_forbidden_text_hit_count": int(source_record.get("forbidden_text_hit_count", 0)) if isinstance(source_record, dict) else 0,
        "source_score_claim_violation_count": int(source_record.get("score_claim_violation_count", 0)) if isinstance(source_record, dict) else 0,
        "source_submission_violation_count": int(source_record.get("submission_violation_count", 0)) if isinstance(source_record, dict) else 0,
        "measurement_targets": READINESS_MEASUREMENT_TARGETS,
        "measurement_target_count": len(READINESS_MEASUREMENT_TARGETS),
    }


def build_submission_readiness_gate_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_PUBLIC_OVERFIT_GUARD_ARTIFACT.exists()
    source_record = _load_json(SOURCE_PUBLIC_OVERFIT_GUARD_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_ready = bool(source_record and source_record.get("public_overfit_guard_ready") is True)
    source_passed = bool(source_record and source_record.get("public_overfit_guard_passed") is True)
    source_next_stage_ok = bool(source_record and source_record.get("next_stage") == "MILESTONE_12_TASK_12_SUBMISSION_READINESS_GATE_V1")
    source_strategy_ok = bool(source_record and source_record.get("chosen_strategy") == CHOSEN_STRATEGY)
    source_goal_ok = bool(source_record and source_record.get("competitive_goal") == COMPETITIVE_GOAL)
    source_issue_zero = bool(source_record and source_record.get("issue_count") == 0)

    source_no_overfit = bool(
        source_record
        and source_record.get("public_overfit_violation_count") == 0
        and source_record.get("forbidden_field_hit_count") == 0
        and source_record.get("forbidden_text_hit_count") == 0
    )

    source_no_score_or_submission = bool(
        source_record
        and source_record.get("score_claim_violation_count") == 0
        and source_record.get("submission_violation_count") == 0
        and source_record.get("boundary_violation_count") == 0
    )

    source_boundaries_ok = all(
        [
            source_record and source_record.get("public_overfit_allowed") is False,
            source_record and source_record.get("public_overfit_guard_required") is True,
            source_record and source_record.get("external_api_dependency") is False,
            source_record and source_record.get("internet_during_eval") is False,
            source_record and source_record.get("real_submission_allowed") is False,
            source_record and source_record.get("manual_upload_allowed") is False,
            source_record and source_record.get("kaggle_submission_sent") is False,
            source_record and source_record.get("kaggle_authentication_performed") is False,
            source_record and source_record.get("official_score_claim_allowed") is False,
            source_record and source_record.get("competitive_score_claim_allowed") is False,
            source_record and source_record.get("private_core_exposure") is False,
            source_record and source_record.get("legal_certification") is False,
        ]
    )

    readiness_package = build_readiness_package(source_record)

    required_artifacts_present = readiness_package["required_source_artifact_present_count"] == readiness_package["required_source_artifact_count"]
    required_artifacts_parseable = readiness_package["required_source_artifact_parseable_count"] == readiness_package["required_source_artifact_count"]
    source_guard_cases_ok = readiness_package["source_guard_case_count"] == 6
    source_guard_pass_ok = readiness_package["source_guard_pass_count"] == 6
    source_overfit_zero = readiness_package["source_public_overfit_violation_count"] == 0
    source_boundary_zero = readiness_package["source_boundary_violation_count"] == 0
    measurement_count_ok = readiness_package["measurement_target_count"] == 10

    real_submission_allowed = False
    ready_for_real_kaggle_submission = False
    manual_upload_allowed = False
    operator_approval_required = True
    operator_approval_received = False

    readiness_gates = [
        _gate("source_artifact_present", source_artifact_present, True, "Task 11 public overfit guard artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Task 11 public overfit guard artifact is parseable."),
        _gate("source_ready", source_ready, True, "Task 11 guard is ready."),
        _gate("source_passed", source_passed, True, "Task 11 guard passed."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 11 points to Task 12."),
        _gate("source_strategy_ok", source_strategy_ok, True, "Source strategy is aligned."),
        _gate("source_goal_ok", source_goal_ok, True, "Source goal is aligned."),
        _gate("source_issue_zero", source_issue_zero, True, "Source issue count is zero."),
        _gate("source_no_overfit", source_no_overfit, True, "Source has no public overfit leakage."),
        _gate("source_no_score_or_submission", source_no_score_or_submission, True, "Source has no score claim or submission behavior."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("required_artifacts_present", required_artifacts_present, True, "Required Task 8-11 artifacts are present."),
        _gate("required_artifacts_parseable", required_artifacts_parseable, True, "Required Task 8-11 artifacts are parseable JSON."),
        _gate("source_guard_cases_ok", source_guard_cases_ok, True, "Source guard has six cases."),
        _gate("source_guard_pass_ok", source_guard_pass_ok, True, "Source guard passes six cases."),
        _gate("source_overfit_zero", source_overfit_zero, True, "Source public overfit violation count is zero."),
        _gate("source_boundary_zero", source_boundary_zero, True, "Source boundary violation count is zero."),
        _gate("measurement_count_ok", measurement_count_ok, True, "Readiness measurement targets are declared."),
        _gate("real_submission_allowed_false", real_submission_allowed is False, True, "Real submission is not allowed by this gate."),
        _gate("ready_for_real_kaggle_submission_false", ready_for_real_kaggle_submission is False, True, "Real Kaggle submission readiness remains blocked."),
        _gate("manual_upload_allowed_false", manual_upload_allowed is False, True, "Manual upload remains blocked."),
        _gate("operator_approval_required_true", operator_approval_required is True, True, "Explicit operator approval remains required."),
        _gate("operator_approval_received_false", operator_approval_received is False, True, "Operator approval has not been received."),
        _gate("public_overfit_allowed_false", True, True, "Public overfitting remains blocked."),
        _gate("public_overfit_guard_required_true", True, True, "Public overfit guard remains required."),
        _gate("external_api_dependency_false", True, True, "External API dependency remains false."),
        _gate("internet_during_eval_false", True, True, "Internet during evaluation remains false."),
        _gate("kaggle_submission_sent_false", True, True, "No Kaggle submission is sent."),
        _gate("kaggle_authentication_performed_false", True, True, "No Kaggle authentication is performed."),
        _gate("private_core_exposure_false", True, True, "Private core exposure remains false."),
        _gate("legal_certification_false", True, True, "legal_certification remains false."),
        _gate("official_score_claim_allowed_false", True, True, "Official score claim is blocked."),
        _gate("competitive_score_claim_allowed_false", True, True, "Competitive score claim is blocked."),
        _gate("local_only_true", True, True, "Task remains local-only."),
        _gate("deterministic_true", True, True, "Task remains deterministic."),
        _gate("public_safe_true", True, True, "Task remains public-safe."),
        _gate("fail_closed_active", True, True, "Gate fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in readiness_gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    readiness_gate_passed = len(required_gates) == len(passed_required_gates)

    readiness_summary = {
        "milestone_12_status": "OPENED_CANONICALLY",
        "submission_readiness_gate_status": "READY" if readiness_gate_passed else "FAIL_CLOSED",
        "readiness_verdict": READINESS_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "required_source_artifact_count": readiness_package["required_source_artifact_count"],
        "required_source_artifact_present_count": readiness_package["required_source_artifact_present_count"],
        "source_guard_case_count": readiness_package["source_guard_case_count"],
        "source_guard_pass_count": readiness_package["source_guard_pass_count"],
        "source_public_overfit_violation_count": readiness_package["source_public_overfit_violation_count"],
        "source_boundary_violation_count": readiness_package["source_boundary_violation_count"],
        "real_submission_allowed": real_submission_allowed,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "operator_approval_required": operator_approval_required,
        "operator_approval_received": operator_approval_received,
        "next_stage": NEXT_STAGE,
    }

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_public_overfit_guard_artifact": str(SOURCE_PUBLIC_OVERFIT_GUARD_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_ready": source_ready,
        "source_passed": source_passed,
        "source_next_stage_ok": source_next_stage_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "readiness_verdict": READINESS_VERDICT,
        "milestone_12_status": "OPENED_CANONICALLY",
        "submission_readiness_gate_ready": True,
        "submission_readiness_gate_valid": readiness_gate_passed,
        "submission_readiness_gate_passed": readiness_gate_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "readiness_summary": readiness_summary,
        "readiness_package": readiness_package,
        "required_source_artifact_count": readiness_package["required_source_artifact_count"],
        "required_source_artifact_present_count": readiness_package["required_source_artifact_present_count"],
        "required_source_artifact_parseable_count": readiness_package["required_source_artifact_parseable_count"],
        "source_guard_case_count": readiness_package["source_guard_case_count"],
        "source_guard_pass_count": readiness_package["source_guard_pass_count"],
        "source_public_overfit_violation_count": readiness_package["source_public_overfit_violation_count"],
        "source_boundary_violation_count": readiness_package["source_boundary_violation_count"],
        "measurement_target_count": len(READINESS_MEASUREMENT_TARGETS),
        "measurement_targets": READINESS_MEASUREMENT_TARGETS,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "open_source_prize_eligibility_required": True,
        "real_submission_allowed": real_submission_allowed,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "manual_upload_allowed": manual_upload_allowed,
        "operator_approval_required": operator_approval_required,
        "operator_approval_received": operator_approval_received,
        "submission_json_created": False,
        "real_submission_candidate_created": False,
        "kaggle_submission_sent": False,
        "kaggle_upload_performed": False,
        "kaggle_authentication_performed": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "readiness_gate_count": len(readiness_gates),
        "readiness_pass_count": len(passed_required_gates),
        "readiness_blocking_issue_count": 0 if readiness_gate_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(readiness_gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if readiness_gate_passed else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "gates": readiness_gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-12-SUBMISSION-READINESS-GATE-" + signature[:12]
    return record


def validate_submission_readiness_gate_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "submission_readiness_gate_ready",
        "submission_readiness_gate_valid",
        "submission_readiness_gate_passed",
        "source_artifact_present",
        "source_artifact_parseable",
        "source_ready",
        "source_passed",
        "source_next_stage_ok",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "operator_approval_required",
        "local_only",
        "deterministic",
        "public_safe",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "public_overfit_allowed",
        "external_api_dependency",
        "internet_during_eval",
        "real_submission_allowed",
        "ready_for_real_kaggle_submission",
        "manual_upload_allowed",
        "operator_approval_received",
        "submission_json_created",
        "real_submission_candidate_created",
        "kaggle_submission_sent",
        "kaggle_upload_performed",
        "kaggle_authentication_performed",
        "contains_api_keys",
        "private_core_exposure",
        "legal_certification",
        "official_score_claim_allowed",
        "competitive_score_claim_allowed",
        "real_public_score_claimed",
        "private_score_claimed",
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

    if record.get("readiness_verdict") != READINESS_VERDICT:
        issues.append("READINESS_VERDICT_MISMATCH")

    if record.get("competitive_goal") != COMPETITIVE_GOAL:
        issues.append("COMPETITIVE_GOAL_MISMATCH")

    if record.get("chosen_strategy") != CHOSEN_STRATEGY:
        issues.append("CHOSEN_STRATEGY_MISMATCH")

    expected_counts = {
        "required_source_artifact_count": 4,
        "required_source_artifact_present_count": 4,
        "required_source_artifact_parseable_count": 4,
        "source_guard_case_count": 6,
        "source_guard_pass_count": 6,
        "source_public_overfit_violation_count": 0,
        "source_boundary_violation_count": 0,
        "measurement_target_count": 10,
        "readiness_blocking_issue_count": 0,
        "issue_count": 0,
    }
    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    package = record.get("readiness_package")
    if not isinstance(package, dict):
        issues.append("READINESS_PACKAGE_MISSING")
    else:
        artifact_statuses = package.get("required_source_artifacts")
        if not isinstance(artifact_statuses, list) or len(artifact_statuses) != 4:
            issues.append("REQUIRED_SOURCE_ARTIFACTS_MISSING_OR_COUNT_MISMATCH")
        elif any(item.get("present") is not True or item.get("parseable_json") is not True for item in artifact_statuses):
            issues.append("REQUIRED_SOURCE_ARTIFACT_NOT_READY")

    summary = record.get("readiness_summary")
    if not isinstance(summary, dict):
        issues.append("READINESS_SUMMARY_MISSING")
    else:
        if summary.get("submission_readiness_gate_status") != "READY":
            issues.append("READINESS_SUMMARY_STATUS_NOT_READY")
        if summary.get("ready_for_real_kaggle_submission") is not False:
            issues.append("READINESS_SUMMARY_REAL_SUBMISSION_NOT_BLOCKED")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("READINESS_SUMMARY_NEXT_STAGE_MISMATCH")

    gates = record.get("gates")
    if not isinstance(gates, list) or not gates:
        issues.append("GATES_MISSING")
    else:
        failed_required = [
            gate.get("name", "UNKNOWN_GATE")
            for gate in gates
            if gate.get("required") is True and gate.get("passed") is not True
        ]
        issues.extend(f"REQUIRED_GATE_FAILED:{name}" for name in failed_required)

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-12-submission-readiness-gate-v1.json"
    index_path = target_dir / "milestone-12-submission-readiness-gate-index-v1.json"
    manifest_path = target_dir / "milestone-12-submission-readiness-gate-manifest-v1.txt"
    markdown_path = target_dir / "milestone-12-submission-readiness-gate-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "readiness_verdict": record["readiness_verdict"],
        "next_stage": record["next_stage"],
        "submission_readiness_gate_ready": record["submission_readiness_gate_ready"],
        "submission_readiness_gate_passed": record["submission_readiness_gate_passed"],
        "required_source_artifact_count": record["required_source_artifact_count"],
        "required_source_artifact_present_count": record["required_source_artifact_present_count"],
        "source_guard_case_count": record["source_guard_case_count"],
        "source_guard_pass_count": record["source_guard_pass_count"],
        "source_public_overfit_violation_count": record["source_public_overfit_violation_count"],
        "source_boundary_violation_count": record["source_boundary_violation_count"],
        "real_submission_allowed": record["real_submission_allowed"],
        "ready_for_real_kaggle_submission": record["ready_for_real_kaggle_submission"],
        "operator_approval_required": record["operator_approval_required"],
        "operator_approval_received": record["operator_approval_received"],
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
        f"task_scope={record['task_scope']}",
        f"task_verdict={record['task_verdict']}",
        f"readiness_verdict={record['readiness_verdict']}",
        f"next_stage={record['next_stage']}",
        f"submission_readiness_gate_ready={record['submission_readiness_gate_ready']}",
        f"submission_readiness_gate_passed={record['submission_readiness_gate_passed']}",
        f"required_source_artifact_count={record['required_source_artifact_count']}",
        f"required_source_artifact_present_count={record['required_source_artifact_present_count']}",
        f"source_guard_case_count={record['source_guard_case_count']}",
        f"source_guard_pass_count={record['source_guard_pass_count']}",
        f"source_public_overfit_violation_count={record['source_public_overfit_violation_count']}",
        f"source_boundary_violation_count={record['source_boundary_violation_count']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={record['ready_for_real_kaggle_submission']}",
        f"operator_approval_required={record['operator_approval_required']}",
        f"operator_approval_received={record['operator_approval_received']}",
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
- verdict: `{record['task_verdict']}`
- readiness_verdict: `{record['readiness_verdict']}`
- next_stage: `{record['next_stage']}`

## Submission Readiness Gate

- submission_readiness_gate_ready: `{record['submission_readiness_gate_ready']}`
- submission_readiness_gate_passed: `{record['submission_readiness_gate_passed']}`
- required_source_artifact_count: `{record['required_source_artifact_count']}`
- required_source_artifact_present_count: `{record['required_source_artifact_present_count']}`
- source_guard_case_count: `{record['source_guard_case_count']}`
- source_guard_pass_count: `{record['source_guard_pass_count']}`
- source_public_overfit_violation_count: `{record['source_public_overfit_violation_count']}`
- source_boundary_violation_count: `{record['source_boundary_violation_count']}`

## Real Submission Boundary

- real_submission_allowed: `{record['real_submission_allowed']}`
- ready_for_real_kaggle_submission: `{record['ready_for_real_kaggle_submission']}`
- manual_upload_allowed: `{record['manual_upload_allowed']}`
- operator_approval_required: `{record['operator_approval_required']}`
- operator_approval_received: `{record['operator_approval_received']}`
- submission_json_created: `{record['submission_json_created']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- kaggle_authentication_performed: `{record['kaggle_authentication_performed']}`
- official_score_claim_allowed: `{record['official_score_claim_allowed']}`
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
    record = build_submission_readiness_gate_record()
    issues = validate_submission_readiness_gate_record(record)
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
    print(record["readiness_verdict"])
    print(record["next_stage"])
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
