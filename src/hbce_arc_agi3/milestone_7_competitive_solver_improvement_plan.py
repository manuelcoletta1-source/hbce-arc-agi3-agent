"""Milestone #7 Competitive Solver Improvement Plan v1.

Local-only opening plan for the competitive solver improvement phase.

This module opens Milestone #7 after Milestone #6 closed the real-submission
readiness chain with real submission blocked pending solver improvement. It
does not submit to Kaggle, authenticate, upload files, call external APIs, read
secrets, create upload archives, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PLAN_STATUS = "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_READY"
PIPELINE_STATUS = "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_VALID"

BASELINE_COMMIT = "8e26ed1 Close ARC AGI3 milestone 6 real submission readiness"
PLAN_MODE = "COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_ONLY_NO_UPLOAD"
PLAN_SCOPE = "OPEN_MILESTONE_7_FOR_MEASURABLE_SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION"
PLAN_VERDICT = "MILESTONE_7_OPEN_COMPETITIVE_SOLVER_IMPROVEMENT_REQUIRED"
NEXT_ALLOWED_STAGE = "MILESTONE_7_TASK_2_BASELINE_SOLVER_FAILURE_TAXONOMY"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/competitive-solver-improvement-plan-v1"

MILESTONE_6_CLOSURE_JSON = Path(
    "examples/milestone-6/real-submission-readiness-closure-v1/"
    "milestone-6-real-submission-readiness-closure-v1.json"
)

EXPECTED_WORKSTREAM_COUNT = 6
EXPECTED_TASK_COUNT = 10

WORKSTREAMS: Tuple[Dict[str, Any], ...] = (
    {
        "name": "baseline_failure_taxonomy",
        "priority": "P0",
        "goal": "Map current solver failures into deterministic, actionable categories.",
        "measurement": "Produce a local failure taxonomy with closed and open failure classes.",
        "required": True,
    },
    {
        "name": "task_family_solver_expansion",
        "priority": "P0",
        "goal": "Expand solver coverage by task family instead of random one-off hacks.",
        "measurement": "Add family-specific improvement records and regression-safe solver paths.",
        "required": True,
    },
    {
        "name": "candidate_generator_improvement",
        "priority": "P0",
        "goal": "Improve candidate diversity and correctness before ranking.",
        "measurement": "Increase deterministic valid candidate count without increasing unsafe fallbacks.",
        "required": True,
    },
    {
        "name": "ranker_evidence_upgrade",
        "priority": "P1",
        "goal": "Make the ranker prefer stronger evidence-backed candidates.",
        "measurement": "Track ranker evidence fields and compare candidate selection before and after changes.",
        "required": True,
    },
    {
        "name": "regression_benchmark",
        "priority": "P1",
        "goal": "Keep the full pipeline green while changing solver behavior.",
        "measurement": "Full suite remains green and submission/upload/authentication flags remain false.",
        "required": True,
    },
    {
        "name": "competitive_readiness_audit",
        "priority": "P2",
        "goal": "Permit a later manual submission decision only after measurable solver improvement.",
        "measurement": "Produce a final competitive readiness audit with no unsupported competitive claim.",
        "required": True,
    },
)

MILESTONE_7_TASKS: Tuple[Dict[str, Any], ...] = (
    {
        "task": 1,
        "name": "Competitive Solver Improvement Plan v1",
        "status": "CURRENT_TASK_READY",
        "output": "Milestone 7 plan, gates, workstreams, and no-upload boundary.",
    },
    {
        "task": 2,
        "name": "Baseline Solver Failure Taxonomy v1",
        "status": "PLANNED",
        "output": "Failure classes from current local solver behavior.",
    },
    {
        "task": 3,
        "name": "Task-Family Solver Expansion v1",
        "status": "PLANNED",
        "output": "Family-specific deterministic solver improvements.",
    },
    {
        "task": 4,
        "name": "Candidate Generator Improvement v1",
        "status": "PLANNED",
        "output": "Improved candidate generation and candidate diversity guard.",
    },
    {
        "task": 5,
        "name": "Ranker Evidence Upgrade v1",
        "status": "PLANNED",
        "output": "Evidence-aware ranker signals and selection audit.",
    },
    {
        "task": 6,
        "name": "Regression Benchmark v1",
        "status": "PLANNED",
        "output": "Regression proof that solver changes preserve public-safe boundary.",
    },
    {
        "task": 7,
        "name": "Local Score Improvement Report v1",
        "status": "PLANNED",
        "output": "Measured improvement report from local deterministic evaluation.",
    },
    {
        "task": 8,
        "name": "Submission Candidate Rebuild v1",
        "status": "PLANNED",
        "output": "Rebuilt local candidate after solver improvements.",
    },
    {
        "task": 9,
        "name": "Final Competitive Readiness Audit v1",
        "status": "PLANNED",
        "output": "Final audit before any manual submission decision.",
    },
    {
        "task": 10,
        "name": "Manual Submission Decision Closure v1",
        "status": "PLANNED",
        "output": "Human decision closure with upload still not automatic.",
    },
)

PLAN_GATES: Tuple[str, ...] = (
    "milestone_6_closure_artifact_present",
    "milestone_6_closure_artifact_ready",
    "milestone_6_closure_valid",
    "milestone_6_closed",
    "milestone_6_blocks_real_submission",
    "milestone_6_solver_improvement_required",
    "milestone_6_solver_improvement_not_completed",
    "plan_mode_valid",
    "plan_scope_valid",
    "plan_verdict_valid",
    "plan_ready",
    "plan_locked",
    "milestone_7_open",
    "workstream_count_valid",
    "all_workstreams_required",
    "priority_p0_workstreams_present",
    "task_count_valid",
    "task_sequence_valid",
    "task_1_current_ready",
    "next_stage_valid",
    "measurable_outputs_defined",
    "competitive_claim_absent",
    "manual_submission_not_allowed",
    "manual_upload_not_performed",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "real_submission_not_created",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

PLAN_ISSUES: Tuple[str, ...] = (
    "milestone_6_closure_artifact_missing",
    "milestone_6_closure_artifact_not_ready",
    "milestone_6_closure_invalid",
    "milestone_6_not_closed",
    "milestone_6_allows_real_submission",
    "milestone_6_solver_improvement_not_required",
    "milestone_6_solver_improvement_already_completed",
    "plan_mode_invalid",
    "plan_scope_invalid",
    "plan_verdict_invalid",
    "plan_not_ready",
    "plan_not_locked",
    "milestone_7_not_open",
    "workstream_count_invalid",
    "workstream_not_required",
    "priority_p0_workstreams_missing",
    "task_count_invalid",
    "task_sequence_invalid",
    "task_1_not_current_ready",
    "next_stage_invalid",
    "measurable_outputs_missing",
    "competitive_claim_detected",
    "manual_submission_allowed",
    "manual_upload_performed",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "real_submission_created",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "external_api_dependency_detected",
    "api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _sha256(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha16(value: str) -> str:
    return value[:16].upper() if value != "MISSING_HASH" else value


def _boundary_from_closure(closure: Mapping[str, Any]) -> Dict[str, Any]:
    source = closure.get("boundary", {}) if isinstance(closure.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": closure.get("kaggle_submission_sent"),
        "private_core_exposure": source.get("private_core_exposure"),
        "legal_certification": source.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    expected = {
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
    return all(boundary.get(key) is value for key, value in expected.items())


def _closure_source(closure: Mapping[str, Any]) -> Dict[str, Any]:
    file_hash = _sha256(MILESTONE_6_CLOSURE_JSON)
    return {
        "name": "milestone_6_real_submission_readiness_closure",
        "path": str(MILESTONE_6_CLOSURE_JSON),
        "present": MILESTONE_6_CLOSURE_JSON.exists(),
        "expected_status": "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_READY",
        "actual_status": closure.get("status", "MISSING"),
        "ready": MILESTONE_6_CLOSURE_JSON.exists()
        and closure.get("status") == "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_READY",
        "artifact_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def build_milestone_7_competitive_solver_improvement_plan() -> Dict[str, Any]:
    closure = _read_json(MILESTONE_6_CLOSURE_JSON)
    boundary = _boundary_from_closure(closure)
    closure_source = _closure_source(closure)

    workstreams = tuple(dict(item) for item in WORKSTREAMS)
    tasks = tuple(dict(item) for item in MILESTONE_7_TASKS)

    required_workstream_count = sum(1 for item in workstreams if item.get("required") is True)
    priority_p0_count = sum(1 for item in workstreams if item.get("priority") == "P0")
    measurement_count = sum(1 for item in workstreams if bool(item.get("measurement")))
    task_sequence = tuple(item["task"] for item in tasks)

    plan_record = {
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "plan_ready": True,
        "plan_locked": True,
        "milestone_7_open": True,
        "milestone_6_closure_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "milestone_6_closed": closure.get("milestone_closed") is True,
        "milestone_6_solver_improvement_required": closure.get("solver_improvement_required") is True,
        "milestone_6_solver_improvement_completed": closure.get("solver_improvement_completed") is True,
        "workstream_count": len(workstreams),
        "required_workstream_count": required_workstream_count,
        "priority_p0_count": priority_p0_count,
        "measurement_count": measurement_count,
        "task_count": len(tasks),
        "task_sequence": list(task_sequence),
        "solver_improvement_required": True,
        "competitive_claim_absent": True,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "boundary_intact": _boundary_intact(boundary),
    }

    gate_state = {
        "milestone_6_closure_artifact_present": MILESTONE_6_CLOSURE_JSON.exists(),
        "milestone_6_closure_artifact_ready": closure.get("status") == "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_READY",
        "milestone_6_closure_valid": bool(closure.get("closure_id")) and bool(closure.get("signature")),
        "milestone_6_closed": closure.get("milestone_closed") is True,
        "milestone_6_blocks_real_submission": closure.get("real_submission_allowed") is False,
        "milestone_6_solver_improvement_required": closure.get("solver_improvement_required") is True,
        "milestone_6_solver_improvement_not_completed": closure.get("solver_improvement_completed") is False,
        "plan_mode_valid": plan_record["plan_mode"] == PLAN_MODE,
        "plan_scope_valid": plan_record["plan_scope"] == PLAN_SCOPE,
        "plan_verdict_valid": plan_record["plan_verdict"] == PLAN_VERDICT,
        "plan_ready": plan_record["plan_ready"] is True,
        "plan_locked": plan_record["plan_locked"] is True,
        "milestone_7_open": plan_record["milestone_7_open"] is True,
        "workstream_count_valid": len(workstreams) == EXPECTED_WORKSTREAM_COUNT,
        "all_workstreams_required": required_workstream_count == EXPECTED_WORKSTREAM_COUNT,
        "priority_p0_workstreams_present": priority_p0_count >= 3,
        "task_count_valid": len(tasks) == EXPECTED_TASK_COUNT,
        "task_sequence_valid": task_sequence == tuple(range(1, EXPECTED_TASK_COUNT + 1)),
        "task_1_current_ready": tasks[0]["status"] == "CURRENT_TASK_READY",
        "next_stage_valid": plan_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "measurable_outputs_defined": measurement_count == EXPECTED_WORKSTREAM_COUNT,
        "competitive_claim_absent": plan_record["competitive_claim_absent"] is True,
        "manual_submission_not_allowed": plan_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": plan_record["manual_upload_performed"] is False,
        "real_submission_allowed_false": plan_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": plan_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": plan_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": plan_record["kaggle_submission_sent"] is False,
        "upload_not_performed": plan_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": plan_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "milestone_6_closure_artifact_missing": not gate_state["milestone_6_closure_artifact_present"],
        "milestone_6_closure_artifact_not_ready": not gate_state["milestone_6_closure_artifact_ready"],
        "milestone_6_closure_invalid": not gate_state["milestone_6_closure_valid"],
        "milestone_6_not_closed": not gate_state["milestone_6_closed"],
        "milestone_6_allows_real_submission": not gate_state["milestone_6_blocks_real_submission"],
        "milestone_6_solver_improvement_not_required": not gate_state["milestone_6_solver_improvement_required"],
        "milestone_6_solver_improvement_already_completed": not gate_state["milestone_6_solver_improvement_not_completed"],
        "plan_mode_invalid": not gate_state["plan_mode_valid"],
        "plan_scope_invalid": not gate_state["plan_scope_valid"],
        "plan_verdict_invalid": not gate_state["plan_verdict_valid"],
        "plan_not_ready": not gate_state["plan_ready"],
        "plan_not_locked": not gate_state["plan_locked"],
        "milestone_7_not_open": not gate_state["milestone_7_open"],
        "workstream_count_invalid": not gate_state["workstream_count_valid"],
        "workstream_not_required": not gate_state["all_workstreams_required"],
        "priority_p0_workstreams_missing": not gate_state["priority_p0_workstreams_present"],
        "task_count_invalid": not gate_state["task_count_valid"],
        "task_sequence_invalid": not gate_state["task_sequence_valid"],
        "task_1_not_current_ready": not gate_state["task_1_current_ready"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
        "measurable_outputs_missing": not gate_state["measurable_outputs_defined"],
        "competitive_claim_detected": not gate_state["competitive_claim_absent"],
        "manual_submission_allowed": not gate_state["manual_submission_not_allowed"],
        "manual_upload_performed": not gate_state["manual_upload_not_performed"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
    }

    gates = tuple(
        {"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"}
        for name in PLAN_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in PLAN_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    plan_ready = (
        closure_source["ready"] is True
        and len(workstreams) == EXPECTED_WORKSTREAM_COUNT
        and len(tasks) == EXPECTED_TASK_COUNT
        and passed_gate_count == len(PLAN_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 1",
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_milestone_6_closure": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "plan_ready": plan_ready,
        "plan_locked": True,
        "milestone_7_open": True,
        "workstream_count": len(workstreams),
        "task_count": len(tasks),
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "solver_improvement_required": True,
        "competitive_claim_absent": True,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": PLAN_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 1",
        "title": "Competitive Solver Improvement Plan v1",
        "baseline_commit": BASELINE_COMMIT,
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_6_closure_source": closure_source,
        "plan_record": plan_record,
        "workstreams": list(workstreams),
        "milestone_7_tasks": list(tasks),
        "plan_gates": list(gates),
        "plan_issues": list(issues),
        "plan_index": index,
        "boundary": boundary,
        "workstream_count": len(workstreams),
        "required_workstream_count": required_workstream_count,
        "priority_p0_count": priority_p0_count,
        "measurement_count": measurement_count,
        "task_count": len(tasks),
        "plan_gate_count": len(PLAN_GATES),
        "passed_gate_count": passed_gate_count,
        "plan_issue_count": issue_count,
        "warning_count": 0,
        "plan_ready": plan_ready,
        "plan_locked": True,
        "milestone_7_open": True,
        "solver_improvement_required": True,
        "competitive_claim_absent": True,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "metadata": {
            "source": "milestone_7_competitive_solver_improvement_plan_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }

    signature = _stable_signature(base)
    return {
        **base,
        "plan_id": f"MILESTONE-7-COMPETITIVE-SOLVER-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_competitive_solver_improvement_plan(plan: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = plan.get("boundary", {})
    gates = plan.get("plan_gates", [])
    issues = plan.get("plan_issues", [])
    workstreams = plan.get("workstreams", [])
    tasks = plan.get("milestone_7_tasks", [])
    source = plan.get("milestone_6_closure_source", {})

    checks = {
        "status_ready": plan.get("status") == PLAN_STATUS,
        "plan_id_present": isinstance(plan.get("plan_id"), str) and bool(plan.get("plan_id")),
        "signature_present": isinstance(plan.get("signature"), str) and bool(plan.get("signature")),
        "baseline_commit_valid": str(plan.get("baseline_commit", "")).startswith("8e26ed1"),
        "plan_mode_valid": plan.get("plan_mode") == PLAN_MODE,
        "plan_scope_valid": plan.get("plan_scope") == PLAN_SCOPE,
        "plan_verdict_valid": plan.get("plan_verdict") == PLAN_VERDICT,
        "next_allowed_stage_valid": plan.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "milestone_6_closure_source_ready": source.get("ready") is True,
        "milestone_6_closure_hash_present": source.get("sha256") != "MISSING_HASH",
        "workstream_count_valid": plan.get("workstream_count") == EXPECTED_WORKSTREAM_COUNT,
        "required_workstream_count_valid": plan.get("required_workstream_count") == EXPECTED_WORKSTREAM_COUNT,
        "priority_p0_count_valid": plan.get("priority_p0_count", 0) >= 3,
        "measurement_count_valid": plan.get("measurement_count") == EXPECTED_WORKSTREAM_COUNT,
        "all_workstreams_required": bool(workstreams) and all(item.get("required") is True for item in workstreams),
        "all_workstreams_measurable": bool(workstreams) and all(bool(item.get("measurement")) for item in workstreams),
        "task_count_valid": plan.get("task_count") == EXPECTED_TASK_COUNT,
        "task_sequence_valid": tuple(item.get("task") for item in tasks) == tuple(range(1, EXPECTED_TASK_COUNT + 1)),
        "task_1_current_ready": bool(tasks) and tasks[0].get("status") == "CURRENT_TASK_READY",
        "plan_gate_count_matches": plan.get("plan_gate_count") == len(PLAN_GATES),
        "all_plan_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "plan_issue_count_zero": plan.get("plan_issue_count") == 0,
        "all_plan_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "plan_ready": plan.get("plan_ready") is True,
        "plan_locked": plan.get("plan_locked") is True,
        "milestone_7_open": plan.get("milestone_7_open") is True,
        "solver_improvement_required": plan.get("solver_improvement_required") is True,
        "competitive_claim_absent": plan.get("competitive_claim_absent") is True,
        "manual_submission_not_allowed": plan.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": plan.get("manual_upload_performed") is False,
        "real_submission_allowed_false": plan.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": plan.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": plan.get("real_submission_created") is False,
        "kaggle_submission_not_sent": plan.get("kaggle_submission_sent") is False,
        "upload_not_performed": plan.get("upload_performed") is False,
        "kaggle_authentication_not_performed": plan.get("kaggle_authentication_performed") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_INVALID",
        "valid": valid,
        "checks": checks,
        "plan_id": plan.get("plan_id"),
        "signature": plan.get("signature"),
    }


def render_competitive_solver_improvement_plan_markdown(plan: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Competitive Solver Improvement Plan v1",
        "",
        f"- status: {plan['status']}",
        f"- plan_id: {plan['plan_id']}",
        f"- signature: {plan['signature']}",
        f"- baseline_commit: {plan['baseline_commit']}",
        f"- plan_mode: {plan['plan_mode']}",
        f"- plan_scope: {plan['plan_scope']}",
        f"- plan_verdict: {plan['plan_verdict']}",
        f"- next_allowed_stage: {plan['next_allowed_stage']}",
        f"- workstream_count: {plan['workstream_count']}",
        f"- required_workstream_count: {plan['required_workstream_count']}",
        f"- priority_p0_count: {plan['priority_p0_count']}",
        f"- measurement_count: {plan['measurement_count']}",
        f"- task_count: {plan['task_count']}",
        f"- plan_gate_count: {plan['plan_gate_count']}",
        f"- passed_gate_count: {plan['passed_gate_count']}",
        f"- plan_issue_count: {plan['plan_issue_count']}",
        f"- plan_ready: {plan['plan_ready']}",
        f"- plan_locked: {plan['plan_locked']}",
        f"- milestone_7_open: {plan['milestone_7_open']}",
        f"- real_submission_allowed: {plan['real_submission_allowed']}",
        f"- kaggle_submission_sent: {plan['kaggle_submission_sent']}",
        f"- upload_performed: {plan['upload_performed']}",
        "",
        "## Workstreams",
        "",
    ]

    for workstream in plan["workstreams"]:
        lines.append(
            f"- {workstream['priority']} {workstream['name']}: required={workstream['required']} "
            f"measurement={workstream['measurement']}"
        )

    lines.extend(["", "## Milestone #7 tasks", ""])

    for task in plan["milestone_7_tasks"]:
        lines.append(f"- Task {task['task']}: {task['name']} - {task['status']}")

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Milestone #7 is opened for competitive solver improvement. Real submission remains blocked until measurable local solver improvement is completed and audited.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_VALID=true",
            "ARC_AGI3_MILESTONE_7_PLAN_MODE=COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_PLAN_VERDICT=MILESTONE_7_OPEN_COMPETITIVE_SOLVER_IMPROVEMENT_REQUIRED",
            "ARC_AGI3_MILESTONE_7_OPEN=true",
            "ARC_AGI3_MILESTONE_7_WORKSTREAM_COUNT=6",
            "ARC_AGI3_MILESTONE_7_TASK_COUNT=10",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_2_BASELINE_SOLVER_FAILURE_TAXONOMY",
            "ARC_AGI3_MILESTONE_7_SOLVER_IMPROVEMENT_REQUIRED=true",
            "ARC_AGI3_MILESTONE_7_COMPETITIVE_CLAIM_ABSENT=true",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_BASELINE_MILESTONE_6_CLOSURE_COMMIT=8e26ed1",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_competitive_solver_improvement_plan_manifest(plan: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 COMPETITIVE SOLVER IMPROVEMENT PLAN MANIFEST v1",
        f"plan_id={plan['plan_id']}",
        f"signature={plan['signature']}",
        f"status={plan['status']}",
        f"baseline_commit={plan['baseline_commit']}",
        f"plan_mode={plan['plan_mode']}",
        f"plan_verdict={plan['plan_verdict']}",
        f"next_allowed_stage={plan['next_allowed_stage']}",
        f"workstream_count={plan['workstream_count']}",
        f"required_workstream_count={plan['required_workstream_count']}",
        f"priority_p0_count={plan['priority_p0_count']}",
        f"measurement_count={plan['measurement_count']}",
        f"task_count={plan['task_count']}",
        f"plan_gate_count={plan['plan_gate_count']}",
        f"passed_gate_count={plan['passed_gate_count']}",
        f"plan_issue_count={plan['plan_issue_count']}",
        f"plan_ready={plan['plan_ready']}",
        f"plan_locked={plan['plan_locked']}",
        f"milestone_7_open={plan['milestone_7_open']}",
        f"solver_improvement_required={plan['solver_improvement_required']}",
        f"competitive_claim_absent={plan['competitive_claim_absent']}",
        f"manual_submission_allowed={plan['manual_submission_allowed']}",
        f"manual_upload_performed={plan['manual_upload_performed']}",
        f"real_submission_allowed={plan['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={plan['ready_for_real_kaggle_submission']}",
        f"real_submission_created={plan['real_submission_created']}",
        f"kaggle_submission_sent={plan['kaggle_submission_sent']}",
        f"upload_performed={plan['upload_performed']}",
        f"kaggle_authentication_performed={plan['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "WORKSTREAMS",
    ]

    for workstream in plan["workstreams"]:
        lines.append(
            f"{workstream['priority']} {workstream['name']} required={workstream['required']} "
            f"measurement={workstream['measurement']}"
        )

    lines.append("")
    lines.append("TASKS")

    for task in plan["milestone_7_tasks"]:
        lines.append(f"Task {task['task']} {task['name']} status={task['status']} output={task['output']}")

    lines.append("")
    return "\n".join(lines)


def write_competitive_solver_improvement_plan_artifacts(
    plan: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    plan = dict(plan or build_milestone_7_competitive_solver_improvement_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-competitive-solver-improvement-plan-v1.json"
    md_path = output / "milestone-7-competitive-solver-improvement-plan-v1.md"
    manifest_path = output / "milestone-7-competitive-solver-improvement-plan-manifest-v1.txt"
    index_path = output / "milestone-7-competitive-solver-improvement-plan-index-v1.json"

    json_path.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_competitive_solver_improvement_plan_markdown(plan), encoding="utf-8")
    manifest_path.write_text(render_competitive_solver_improvement_plan_manifest(plan), encoding="utf-8")
    index_path.write_text(json.dumps(plan["plan_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_competitive_solver_improvement_plan_pipeline() -> Dict[str, Any]:
    plan = build_milestone_7_competitive_solver_improvement_plan()
    validation = validate_milestone_7_competitive_solver_improvement_plan(plan)
    artifacts = write_competitive_solver_improvement_plan_artifacts(plan)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_PIPELINE_INVALID",
        "plan_status": plan["status"],
        "validation_status": validation["status"],
        "plan": plan,
        "plan_id": plan["plan_id"],
        "signature": plan["signature"],
        "plan_mode": plan["plan_mode"],
        "plan_verdict": plan["plan_verdict"],
        "next_allowed_stage": plan["next_allowed_stage"],
        "workstream_count": plan["workstream_count"],
        "required_workstream_count": plan["required_workstream_count"],
        "priority_p0_count": plan["priority_p0_count"],
        "measurement_count": plan["measurement_count"],
        "task_count": plan["task_count"],
        "plan_gate_count": plan["plan_gate_count"],
        "passed_gate_count": plan["passed_gate_count"],
        "plan_issue_count": plan["plan_issue_count"],
        "warning_count": plan["warning_count"],
        "plan_ready": plan["plan_ready"],
        "plan_locked": plan["plan_locked"],
        "milestone_7_open": plan["milestone_7_open"],
        "solver_improvement_required": plan["solver_improvement_required"],
        "competitive_claim_absent": plan["competitive_claim_absent"],
        "manual_submission_allowed": plan["manual_submission_allowed"],
        "manual_upload_performed": plan["manual_upload_performed"],
        "real_submission_allowed": plan["real_submission_allowed"],
        "ready_for_real_kaggle_submission": plan["ready_for_real_kaggle_submission"],
        "real_submission_created": plan["real_submission_created"],
        "kaggle_submission_sent": plan["kaggle_submission_sent"],
        "upload_performed": plan["upload_performed"],
        "kaggle_authentication_performed": plan["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": plan["metadata"],
    }
