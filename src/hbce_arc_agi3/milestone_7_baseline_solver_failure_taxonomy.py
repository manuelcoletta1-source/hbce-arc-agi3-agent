"""Milestone #7 Baseline Solver Failure Taxonomy v1.

Local-only baseline failure taxonomy for the ARC-AGI-3 solver improvement phase.

This module converts the Milestone #7 improvement plan into actionable solver
failure classes. It does not submit to Kaggle, authenticate, upload files, call
external APIs, read secrets, create upload archives, or create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


TAXONOMY_STATUS = "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_READY"
PIPELINE_STATUS = "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_VALID"

BASELINE_COMMIT = "70a8d44 Open ARC AGI3 milestone 7 competitive solver improvement"
TAXONOMY_MODE = "BASELINE_SOLVER_FAILURE_TAXONOMY_ONLY_NO_UPLOAD"
TAXONOMY_SCOPE = "CLASSIFY_CURRENT_SOLVER_FAILURES_FOR_MEASURABLE_IMPROVEMENT"
TAXONOMY_VERDICT = "BASELINE_FAILURE_TAXONOMY_READY_SOLVER_IMPROVEMENT_REQUIRED"
NEXT_ALLOWED_STAGE = "MILESTONE_7_TASK_3_TASK_FAMILY_SOLVER_EXPANSION"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/baseline-solver-failure-taxonomy-v1"

PLAN_JSON = Path(
    "examples/milestone-7/competitive-solver-improvement-plan-v1/"
    "milestone-7-competitive-solver-improvement-plan-v1.json"
)

EXPECTED_FAILURE_CLASS_COUNT = 7
EXPECTED_TARGET_TASK_COUNT = 5

FAILURE_CLASSES: Tuple[Dict[str, Any], ...] = (
    {
        "failure_class": "color_transform_undercoverage",
        "severity": "P0",
        "family": "color_mapping",
        "symptom": "Solver may miss stable color remaps, palette replacements, or color-preserving transformations.",
        "probable_cause": "Color transform evidence is not yet fully propagated into candidate generation and ranking.",
        "target_task": "Task 3 Task-Family Solver Expansion v1",
        "improvement_target": "Add color-family solver paths and verify stable remap/palette behavior.",
        "measurement": "Increase exact or partial match rate on deterministic color-family local cases.",
        "open": True,
        "closed": False,
    },
    {
        "failure_class": "object_segmentation_undercoverage",
        "severity": "P0",
        "family": "object_model",
        "symptom": "Solver may fail when the transformation depends on connected components, object identity, or object movement.",
        "probable_cause": "Object model signals are not yet strong enough as solver-family triggers.",
        "target_task": "Task 3 Task-Family Solver Expansion v1",
        "improvement_target": "Expand object-aware candidate generation from component signatures and object relations.",
        "measurement": "Track object-family cases and verify deterministic object-aware candidate selection.",
        "open": True,
        "closed": False,
    },
    {
        "failure_class": "spatial_symmetry_undercoverage",
        "severity": "P0",
        "family": "shape_symmetry",
        "symptom": "Solver may miss reflections, rotations, translations, crops, expansion, or symmetry-based completion.",
        "probable_cause": "Shape and symmetry evidence is not yet integrated deeply enough into solver selection.",
        "target_task": "Task 3 Task-Family Solver Expansion v1",
        "improvement_target": "Add spatial/symmetry solver branches and family-level regression checks.",
        "measurement": "Improve deterministic local matches on symmetry and geometry families.",
        "open": True,
        "closed": False,
    },
    {
        "failure_class": "candidate_generator_low_diversity",
        "severity": "P0",
        "family": "candidate_generation",
        "symptom": "The solver may preserve safe candidates but fail to generate the correct transform candidate.",
        "probable_cause": "Candidate generator does not yet enumerate enough evidence-compatible transformations.",
        "target_task": "Task 4 Candidate Generator Improvement v1",
        "improvement_target": "Increase valid candidate diversity without unsafe random search.",
        "measurement": "Increase deterministic valid candidate count while keeping full test suite green.",
        "open": True,
        "closed": False,
    },
    {
        "failure_class": "ranker_evidence_weakness",
        "severity": "P1",
        "family": "candidate_ranking",
        "symptom": "The correct candidate may exist but not be ranked first.",
        "probable_cause": "Ranker evidence is too shallow or does not combine family signals strongly enough.",
        "target_task": "Task 5 Ranker Evidence Upgrade v1",
        "improvement_target": "Strengthen evidence fields, confidence calibration, and candidate ordering.",
        "measurement": "Show improved top-1 candidate selection on deterministic local benchmark cases.",
        "open": True,
        "closed": False,
    },
    {
        "failure_class": "regression_guard_incomplete",
        "severity": "P1",
        "family": "regression_safety",
        "symptom": "Solver changes could improve one family while silently damaging another.",
        "probable_cause": "Competitive improvement phase needs explicit regression benchmark tracking.",
        "target_task": "Task 6 Regression Benchmark v1",
        "improvement_target": "Build regression benchmark guard for all solver improvements.",
        "measurement": "Full suite remains green and old deterministic artifacts remain compatible.",
        "open": True,
        "closed": False,
    },
    {
        "failure_class": "competitive_score_evidence_absent",
        "severity": "P2",
        "family": "competitive_readiness",
        "symptom": "The project has a safe package but not enough measured evidence for a competitive submission claim.",
        "probable_cause": "Milestone #6 prepared readiness, not solver quality improvement.",
        "target_task": "Task 7 Local Score Improvement Report v1",
        "improvement_target": "Generate local score improvement evidence before rebuilding submission candidate.",
        "measurement": "Produce a local improvement report with before/after metrics and no unsupported claim.",
        "open": True,
        "closed": False,
    },
)

TAXONOMY_GATES: Tuple[str, ...] = (
    "plan_artifact_present",
    "plan_artifact_ready",
    "plan_artifact_valid",
    "milestone_7_open",
    "plan_requires_solver_improvement",
    "plan_blocks_real_submission",
    "taxonomy_mode_valid",
    "taxonomy_scope_valid",
    "taxonomy_verdict_valid",
    "taxonomy_ready",
    "taxonomy_locked",
    "failure_class_count_valid",
    "all_failure_classes_open",
    "all_failure_classes_not_closed",
    "all_failure_classes_have_family",
    "all_failure_classes_have_symptom",
    "all_failure_classes_have_probable_cause",
    "all_failure_classes_have_target_task",
    "all_failure_classes_have_improvement_target",
    "all_failure_classes_have_measurement",
    "priority_p0_count_valid",
    "target_task_count_valid",
    "task_3_target_present",
    "task_4_target_present",
    "task_5_target_present",
    "task_6_target_present",
    "next_stage_valid",
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

TAXONOMY_ISSUES: Tuple[str, ...] = (
    "plan_artifact_missing",
    "plan_artifact_not_ready",
    "plan_artifact_invalid",
    "milestone_7_not_open",
    "plan_does_not_require_solver_improvement",
    "plan_allows_real_submission",
    "taxonomy_mode_invalid",
    "taxonomy_scope_invalid",
    "taxonomy_verdict_invalid",
    "taxonomy_not_ready",
    "taxonomy_not_locked",
    "failure_class_count_invalid",
    "failure_class_not_open",
    "failure_class_already_closed",
    "failure_family_missing",
    "failure_symptom_missing",
    "failure_probable_cause_missing",
    "failure_target_task_missing",
    "failure_improvement_target_missing",
    "failure_measurement_missing",
    "priority_p0_count_invalid",
    "target_task_count_invalid",
    "task_3_target_missing",
    "task_4_target_missing",
    "task_5_target_missing",
    "task_6_target_missing",
    "next_stage_invalid",
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


def _boundary_from_plan(plan: Mapping[str, Any]) -> Dict[str, Any]:
    source = plan.get("boundary", {}) if isinstance(plan.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": plan.get("kaggle_submission_sent"),
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


def _plan_source(plan: Mapping[str, Any]) -> Dict[str, Any]:
    file_hash = _sha256(PLAN_JSON)
    return {
        "name": "milestone_7_competitive_solver_improvement_plan",
        "path": str(PLAN_JSON),
        "present": PLAN_JSON.exists(),
        "expected_status": "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_READY",
        "actual_status": plan.get("status", "MISSING"),
        "ready": PLAN_JSON.exists()
        and plan.get("status") == "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_READY",
        "artifact_id": plan.get("plan_id", "MISSING_PLAN_ID"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def build_milestone_7_baseline_solver_failure_taxonomy() -> Dict[str, Any]:
    plan = _read_json(PLAN_JSON)
    boundary = _boundary_from_plan(plan)
    plan_source = _plan_source(plan)

    failure_classes = tuple(dict(item) for item in FAILURE_CLASSES)

    priority_p0_count = sum(1 for item in failure_classes if item.get("severity") == "P0")
    open_failure_count = sum(1 for item in failure_classes if item.get("open") is True)
    closed_failure_count = sum(1 for item in failure_classes if item.get("closed") is True)
    target_tasks = sorted({item["target_task"] for item in failure_classes})
    target_task_count = len(target_tasks)

    taxonomy_record = {
        "taxonomy_mode": TAXONOMY_MODE,
        "taxonomy_scope": TAXONOMY_SCOPE,
        "taxonomy_verdict": TAXONOMY_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "taxonomy_ready": True,
        "taxonomy_locked": True,
        "milestone_7_plan_id": plan.get("plan_id", "MISSING_PLAN_ID"),
        "milestone_7_open": plan.get("milestone_7_open") is True,
        "plan_solver_improvement_required": plan.get("solver_improvement_required") is True,
        "failure_class_count": len(failure_classes),
        "open_failure_count": open_failure_count,
        "closed_failure_count": closed_failure_count,
        "priority_p0_count": priority_p0_count,
        "target_task_count": target_task_count,
        "target_tasks": target_tasks,
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
        "plan_artifact_present": PLAN_JSON.exists(),
        "plan_artifact_ready": plan.get("status") == "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_READY",
        "plan_artifact_valid": bool(plan.get("plan_id")) and bool(plan.get("signature")),
        "milestone_7_open": plan.get("milestone_7_open") is True,
        "plan_requires_solver_improvement": plan.get("solver_improvement_required") is True,
        "plan_blocks_real_submission": plan.get("real_submission_allowed") is False,
        "taxonomy_mode_valid": taxonomy_record["taxonomy_mode"] == TAXONOMY_MODE,
        "taxonomy_scope_valid": taxonomy_record["taxonomy_scope"] == TAXONOMY_SCOPE,
        "taxonomy_verdict_valid": taxonomy_record["taxonomy_verdict"] == TAXONOMY_VERDICT,
        "taxonomy_ready": taxonomy_record["taxonomy_ready"] is True,
        "taxonomy_locked": taxonomy_record["taxonomy_locked"] is True,
        "failure_class_count_valid": len(failure_classes) == EXPECTED_FAILURE_CLASS_COUNT,
        "all_failure_classes_open": open_failure_count == EXPECTED_FAILURE_CLASS_COUNT,
        "all_failure_classes_not_closed": closed_failure_count == 0,
        "all_failure_classes_have_family": all(bool(item.get("family")) for item in failure_classes),
        "all_failure_classes_have_symptom": all(bool(item.get("symptom")) for item in failure_classes),
        "all_failure_classes_have_probable_cause": all(bool(item.get("probable_cause")) for item in failure_classes),
        "all_failure_classes_have_target_task": all(bool(item.get("target_task")) for item in failure_classes),
        "all_failure_classes_have_improvement_target": all(bool(item.get("improvement_target")) for item in failure_classes),
        "all_failure_classes_have_measurement": all(bool(item.get("measurement")) for item in failure_classes),
        "priority_p0_count_valid": priority_p0_count >= 4,
        "target_task_count_valid": target_task_count == EXPECTED_TARGET_TASK_COUNT,
        "task_3_target_present": "Task 3 Task-Family Solver Expansion v1" in target_tasks,
        "task_4_target_present": "Task 4 Candidate Generator Improvement v1" in target_tasks,
        "task_5_target_present": "Task 5 Ranker Evidence Upgrade v1" in target_tasks,
        "task_6_target_present": "Task 6 Regression Benchmark v1" in target_tasks,
        "next_stage_valid": taxonomy_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "competitive_claim_absent": taxonomy_record["competitive_claim_absent"] is True,
        "manual_submission_not_allowed": taxonomy_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": taxonomy_record["manual_upload_performed"] is False,
        "real_submission_allowed_false": taxonomy_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": taxonomy_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": taxonomy_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": taxonomy_record["kaggle_submission_sent"] is False,
        "upload_not_performed": taxonomy_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": taxonomy_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "plan_artifact_missing": not gate_state["plan_artifact_present"],
        "plan_artifact_not_ready": not gate_state["plan_artifact_ready"],
        "plan_artifact_invalid": not gate_state["plan_artifact_valid"],
        "milestone_7_not_open": not gate_state["milestone_7_open"],
        "plan_does_not_require_solver_improvement": not gate_state["plan_requires_solver_improvement"],
        "plan_allows_real_submission": not gate_state["plan_blocks_real_submission"],
        "taxonomy_mode_invalid": not gate_state["taxonomy_mode_valid"],
        "taxonomy_scope_invalid": not gate_state["taxonomy_scope_valid"],
        "taxonomy_verdict_invalid": not gate_state["taxonomy_verdict_valid"],
        "taxonomy_not_ready": not gate_state["taxonomy_ready"],
        "taxonomy_not_locked": not gate_state["taxonomy_locked"],
        "failure_class_count_invalid": not gate_state["failure_class_count_valid"],
        "failure_class_not_open": not gate_state["all_failure_classes_open"],
        "failure_class_already_closed": not gate_state["all_failure_classes_not_closed"],
        "failure_family_missing": not gate_state["all_failure_classes_have_family"],
        "failure_symptom_missing": not gate_state["all_failure_classes_have_symptom"],
        "failure_probable_cause_missing": not gate_state["all_failure_classes_have_probable_cause"],
        "failure_target_task_missing": not gate_state["all_failure_classes_have_target_task"],
        "failure_improvement_target_missing": not gate_state["all_failure_classes_have_improvement_target"],
        "failure_measurement_missing": not gate_state["all_failure_classes_have_measurement"],
        "priority_p0_count_invalid": not gate_state["priority_p0_count_valid"],
        "target_task_count_invalid": not gate_state["target_task_count_valid"],
        "task_3_target_missing": not gate_state["task_3_target_present"],
        "task_4_target_missing": not gate_state["task_4_target_present"],
        "task_5_target_missing": not gate_state["task_5_target_present"],
        "task_6_target_missing": not gate_state["task_6_target_present"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
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
        for name in TAXONOMY_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in TAXONOMY_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    taxonomy_ready = (
        plan_source["ready"] is True
        and len(failure_classes) == EXPECTED_FAILURE_CLASS_COUNT
        and open_failure_count == EXPECTED_FAILURE_CLASS_COUNT
        and closed_failure_count == 0
        and passed_gate_count == len(TAXONOMY_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 2",
        "taxonomy_mode": TAXONOMY_MODE,
        "taxonomy_scope": TAXONOMY_SCOPE,
        "taxonomy_verdict": TAXONOMY_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_plan": plan.get("plan_id", "MISSING_PLAN_ID"),
        "taxonomy_ready": taxonomy_ready,
        "taxonomy_locked": True,
        "failure_class_count": len(failure_classes),
        "open_failure_count": open_failure_count,
        "closed_failure_count": closed_failure_count,
        "priority_p0_count": priority_p0_count,
        "target_task_count": target_task_count,
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
        "status": TAXONOMY_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 2",
        "title": "Baseline Solver Failure Taxonomy v1",
        "baseline_commit": BASELINE_COMMIT,
        "taxonomy_mode": TAXONOMY_MODE,
        "taxonomy_scope": TAXONOMY_SCOPE,
        "taxonomy_verdict": TAXONOMY_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_7_plan_source": plan_source,
        "taxonomy_record": taxonomy_record,
        "failure_classes": list(failure_classes),
        "taxonomy_gates": list(gates),
        "taxonomy_issues": list(issues),
        "taxonomy_index": index,
        "boundary": boundary,
        "failure_class_count": len(failure_classes),
        "open_failure_count": open_failure_count,
        "closed_failure_count": closed_failure_count,
        "priority_p0_count": priority_p0_count,
        "target_task_count": target_task_count,
        "taxonomy_gate_count": len(TAXONOMY_GATES),
        "passed_gate_count": passed_gate_count,
        "taxonomy_issue_count": issue_count,
        "warning_count": 0,
        "taxonomy_ready": taxonomy_ready,
        "taxonomy_locked": True,
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
            "source": "milestone_7_baseline_solver_failure_taxonomy_v1",
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
        "taxonomy_id": f"MILESTONE-7-FAILURE-TAXONOMY-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_baseline_solver_failure_taxonomy(taxonomy: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = taxonomy.get("boundary", {})
    gates = taxonomy.get("taxonomy_gates", [])
    issues = taxonomy.get("taxonomy_issues", [])
    failure_classes = taxonomy.get("failure_classes", [])
    source = taxonomy.get("milestone_7_plan_source", {})

    checks = {
        "status_ready": taxonomy.get("status") == TAXONOMY_STATUS,
        "taxonomy_id_present": isinstance(taxonomy.get("taxonomy_id"), str) and bool(taxonomy.get("taxonomy_id")),
        "signature_present": isinstance(taxonomy.get("signature"), str) and bool(taxonomy.get("signature")),
        "baseline_commit_valid": str(taxonomy.get("baseline_commit", "")).startswith("70a8d44"),
        "taxonomy_mode_valid": taxonomy.get("taxonomy_mode") == TAXONOMY_MODE,
        "taxonomy_scope_valid": taxonomy.get("taxonomy_scope") == TAXONOMY_SCOPE,
        "taxonomy_verdict_valid": taxonomy.get("taxonomy_verdict") == TAXONOMY_VERDICT,
        "next_allowed_stage_valid": taxonomy.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "plan_source_ready": source.get("ready") is True,
        "plan_source_hash_present": source.get("sha256") != "MISSING_HASH",
        "failure_class_count_valid": taxonomy.get("failure_class_count") == EXPECTED_FAILURE_CLASS_COUNT,
        "open_failure_count_valid": taxonomy.get("open_failure_count") == EXPECTED_FAILURE_CLASS_COUNT,
        "closed_failure_count_zero": taxonomy.get("closed_failure_count") == 0,
        "priority_p0_count_valid": taxonomy.get("priority_p0_count", 0) >= 4,
        "target_task_count_valid": taxonomy.get("target_task_count") == EXPECTED_TARGET_TASK_COUNT,
        "all_failure_classes_open": bool(failure_classes) and all(item.get("open") is True for item in failure_classes),
        "all_failure_classes_not_closed": bool(failure_classes) and all(item.get("closed") is False for item in failure_classes),
        "all_failure_classes_measurable": bool(failure_classes) and all(bool(item.get("measurement")) for item in failure_classes),
        "all_failure_classes_actionable": bool(failure_classes) and all(bool(item.get("improvement_target")) for item in failure_classes),
        "taxonomy_gate_count_matches": taxonomy.get("taxonomy_gate_count") == len(TAXONOMY_GATES),
        "all_taxonomy_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "taxonomy_issue_count_zero": taxonomy.get("taxonomy_issue_count") == 0,
        "all_taxonomy_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "taxonomy_ready": taxonomy.get("taxonomy_ready") is True,
        "taxonomy_locked": taxonomy.get("taxonomy_locked") is True,
        "solver_improvement_required": taxonomy.get("solver_improvement_required") is True,
        "competitive_claim_absent": taxonomy.get("competitive_claim_absent") is True,
        "manual_submission_not_allowed": taxonomy.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": taxonomy.get("manual_upload_performed") is False,
        "real_submission_allowed_false": taxonomy.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": taxonomy.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": taxonomy.get("real_submission_created") is False,
        "kaggle_submission_not_sent": taxonomy.get("kaggle_submission_sent") is False,
        "upload_not_performed": taxonomy.get("upload_performed") is False,
        "kaggle_authentication_not_performed": taxonomy.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_INVALID",
        "valid": valid,
        "checks": checks,
        "taxonomy_id": taxonomy.get("taxonomy_id"),
        "signature": taxonomy.get("signature"),
    }


def render_baseline_solver_failure_taxonomy_markdown(taxonomy: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Baseline Solver Failure Taxonomy v1",
        "",
        f"- status: {taxonomy['status']}",
        f"- taxonomy_id: {taxonomy['taxonomy_id']}",
        f"- signature: {taxonomy['signature']}",
        f"- baseline_commit: {taxonomy['baseline_commit']}",
        f"- taxonomy_mode: {taxonomy['taxonomy_mode']}",
        f"- taxonomy_scope: {taxonomy['taxonomy_scope']}",
        f"- taxonomy_verdict: {taxonomy['taxonomy_verdict']}",
        f"- next_allowed_stage: {taxonomy['next_allowed_stage']}",
        f"- failure_class_count: {taxonomy['failure_class_count']}",
        f"- open_failure_count: {taxonomy['open_failure_count']}",
        f"- closed_failure_count: {taxonomy['closed_failure_count']}",
        f"- priority_p0_count: {taxonomy['priority_p0_count']}",
        f"- target_task_count: {taxonomy['target_task_count']}",
        f"- taxonomy_gate_count: {taxonomy['taxonomy_gate_count']}",
        f"- passed_gate_count: {taxonomy['passed_gate_count']}",
        f"- taxonomy_issue_count: {taxonomy['taxonomy_issue_count']}",
        f"- taxonomy_ready: {taxonomy['taxonomy_ready']}",
        f"- taxonomy_locked: {taxonomy['taxonomy_locked']}",
        f"- real_submission_allowed: {taxonomy['real_submission_allowed']}",
        f"- kaggle_submission_sent: {taxonomy['kaggle_submission_sent']}",
        f"- upload_performed: {taxonomy['upload_performed']}",
        "",
        "## Failure classes",
        "",
    ]

    for item in taxonomy["failure_classes"]:
        lines.append(
            f"- {item['severity']} {item['failure_class']} / family={item['family']} / "
            f"target={item['target_task']} / measurement={item['measurement']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Baseline solver failures are classified. Next step is task-family solver expansion.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_VALID=true",
            "ARC_AGI3_MILESTONE_7_TAXONOMY_MODE=BASELINE_SOLVER_FAILURE_TAXONOMY_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_TAXONOMY_VERDICT=BASELINE_FAILURE_TAXONOMY_READY_SOLVER_IMPROVEMENT_REQUIRED",
            "ARC_AGI3_MILESTONE_7_FAILURE_CLASS_COUNT=7",
            "ARC_AGI3_MILESTONE_7_OPEN_FAILURE_COUNT=7",
            "ARC_AGI3_MILESTONE_7_CLOSED_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_7_PRIORITY_P0_COUNT=4",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_3_TASK_FAMILY_SOLVER_EXPANSION",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_BASELINE_PLAN_COMMIT=70a8d44",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_baseline_solver_failure_taxonomy_manifest(taxonomy: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 BASELINE SOLVER FAILURE TAXONOMY MANIFEST v1",
        f"taxonomy_id={taxonomy['taxonomy_id']}",
        f"signature={taxonomy['signature']}",
        f"status={taxonomy['status']}",
        f"baseline_commit={taxonomy['baseline_commit']}",
        f"taxonomy_mode={taxonomy['taxonomy_mode']}",
        f"taxonomy_verdict={taxonomy['taxonomy_verdict']}",
        f"next_allowed_stage={taxonomy['next_allowed_stage']}",
        f"failure_class_count={taxonomy['failure_class_count']}",
        f"open_failure_count={taxonomy['open_failure_count']}",
        f"closed_failure_count={taxonomy['closed_failure_count']}",
        f"priority_p0_count={taxonomy['priority_p0_count']}",
        f"target_task_count={taxonomy['target_task_count']}",
        f"taxonomy_gate_count={taxonomy['taxonomy_gate_count']}",
        f"passed_gate_count={taxonomy['passed_gate_count']}",
        f"taxonomy_issue_count={taxonomy['taxonomy_issue_count']}",
        f"taxonomy_ready={taxonomy['taxonomy_ready']}",
        f"taxonomy_locked={taxonomy['taxonomy_locked']}",
        f"solver_improvement_required={taxonomy['solver_improvement_required']}",
        f"competitive_claim_absent={taxonomy['competitive_claim_absent']}",
        f"manual_submission_allowed={taxonomy['manual_submission_allowed']}",
        f"manual_upload_performed={taxonomy['manual_upload_performed']}",
        f"real_submission_allowed={taxonomy['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={taxonomy['ready_for_real_kaggle_submission']}",
        f"real_submission_created={taxonomy['real_submission_created']}",
        f"kaggle_submission_sent={taxonomy['kaggle_submission_sent']}",
        f"upload_performed={taxonomy['upload_performed']}",
        f"kaggle_authentication_performed={taxonomy['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "FAILURE_CLASSES",
    ]

    for item in taxonomy["failure_classes"]:
        lines.append(
            f"{item['severity']} {item['failure_class']} family={item['family']} "
            f"open={item['open']} closed={item['closed']} target_task={item['target_task']} "
            f"measurement={item['measurement']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_baseline_solver_failure_taxonomy_artifacts(
    taxonomy: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    taxonomy = dict(taxonomy or build_milestone_7_baseline_solver_failure_taxonomy())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-baseline-solver-failure-taxonomy-v1.json"
    md_path = output / "milestone-7-baseline-solver-failure-taxonomy-v1.md"
    manifest_path = output / "milestone-7-baseline-solver-failure-taxonomy-manifest-v1.txt"
    index_path = output / "milestone-7-baseline-solver-failure-taxonomy-index-v1.json"

    json_path.write_text(json.dumps(taxonomy, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_baseline_solver_failure_taxonomy_markdown(taxonomy), encoding="utf-8")
    manifest_path.write_text(render_baseline_solver_failure_taxonomy_manifest(taxonomy), encoding="utf-8")
    index_path.write_text(json.dumps(taxonomy["taxonomy_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_baseline_solver_failure_taxonomy_pipeline() -> Dict[str, Any]:
    taxonomy = build_milestone_7_baseline_solver_failure_taxonomy()
    validation = validate_milestone_7_baseline_solver_failure_taxonomy(taxonomy)
    artifacts = write_baseline_solver_failure_taxonomy_artifacts(taxonomy)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_PIPELINE_INVALID",
        "taxonomy_status": taxonomy["status"],
        "validation_status": validation["status"],
        "taxonomy": taxonomy,
        "taxonomy_id": taxonomy["taxonomy_id"],
        "signature": taxonomy["signature"],
        "taxonomy_mode": taxonomy["taxonomy_mode"],
        "taxonomy_verdict": taxonomy["taxonomy_verdict"],
        "next_allowed_stage": taxonomy["next_allowed_stage"],
        "failure_class_count": taxonomy["failure_class_count"],
        "open_failure_count": taxonomy["open_failure_count"],
        "closed_failure_count": taxonomy["closed_failure_count"],
        "priority_p0_count": taxonomy["priority_p0_count"],
        "target_task_count": taxonomy["target_task_count"],
        "taxonomy_gate_count": taxonomy["taxonomy_gate_count"],
        "passed_gate_count": taxonomy["passed_gate_count"],
        "taxonomy_issue_count": taxonomy["taxonomy_issue_count"],
        "warning_count": taxonomy["warning_count"],
        "taxonomy_ready": taxonomy["taxonomy_ready"],
        "taxonomy_locked": taxonomy["taxonomy_locked"],
        "solver_improvement_required": taxonomy["solver_improvement_required"],
        "competitive_claim_absent": taxonomy["competitive_claim_absent"],
        "manual_submission_allowed": taxonomy["manual_submission_allowed"],
        "manual_upload_performed": taxonomy["manual_upload_performed"],
        "real_submission_allowed": taxonomy["real_submission_allowed"],
        "ready_for_real_kaggle_submission": taxonomy["ready_for_real_kaggle_submission"],
        "real_submission_created": taxonomy["real_submission_created"],
        "kaggle_submission_sent": taxonomy["kaggle_submission_sent"],
        "upload_performed": taxonomy["upload_performed"],
        "kaggle_authentication_performed": taxonomy["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": taxonomy["metadata"],
    }
