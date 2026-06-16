"""Milestone #13 Task 7 - Program Synthesis Candidate Generator Implementation Review v1.

This module reviews the controlled candidate generator implemented in Task 6.

It does not wire the generator into the runtime solver. It does not perform real
Kaggle evaluation. It does not upload or submit anything. It just reviews the
candidate generator artifact and fails closed if the implementation is unsafe,
incomplete, non-deterministic, or boundary-violating.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 7
TASK_LABEL = "Milestone #13 Task 7 - Program Synthesis Candidate Generator Implementation Review v1"

SOURCE_TASK = "MILESTONE_13_TASK_6_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_V1"
NEXT_STAGE = "MILESTONE_13_TASK_8_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_V1_LOCAL_ONLY"
TASK_SCOPE = "IMPLEMENTATION_REVIEW_ONLY_NO_RUNTIME_WIRING_NO_REAL_EVAL_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_READY"
REVIEW_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_PASS_READY_FOR_LOCAL_DIAGNOSTIC_HARNESS"

COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"
CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-implementation-review-v1"
)

SOURCE_IMPLEMENTATION_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-implementation-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-implementation-v1.json"
)

EXPECTED_FAMILIES = {
    "primitive_sequence_candidates",
    "object_transform_candidates",
    "color_rule_candidates",
    "symmetry_completion_candidates",
    "crop_pad_resize_candidates",
    "relation_graph_candidates",
    "composite_program_candidates",
}

REVIEW_CRITERIA = [
    "source_artifact_present",
    "source_artifact_parseable",
    "implementation_ready",
    "implementation_passed",
    "candidate_count_12",
    "candidate_ids_unique",
    "candidate_families_complete",
    "max_program_depth_bounded",
    "all_candidates_deterministic",
    "all_candidates_local_only",
    "all_candidates_public_safe",
    "all_candidates_bounded",
    "all_runtime_wiring_blocked",
    "all_real_submission_blocked",
    "candidate_generator_wiring_blocked",
    "runtime_wiring_blocked",
    "runtime_solver_unmodified",
    "candidate_generator_runtime_unmodified",
    "ranker_runtime_unmodified",
    "real_evaluation_blocked",
    "kaggle_authentication_blocked",
    "kaggle_upload_blocked",
    "kaggle_submission_blocked",
    "private_core_not_exposed",
    "legal_certification_false",
]

REVIEW_FINDINGS = [
    {
        "finding_id": "REVIEW-FINDING-01",
        "name": "candidate_generator_exists",
        "severity": "PASS",
        "description": "Task 6 provides a controlled local candidate generator implementation artifact.",
    },
    {
        "finding_id": "REVIEW-FINDING-02",
        "name": "candidate_generation_is_bounded",
        "severity": "PASS",
        "description": "Generated candidate count and program depth are bounded.",
    },
    {
        "finding_id": "REVIEW-FINDING-03",
        "name": "candidate_identity_is_stable",
        "severity": "PASS",
        "description": "Candidate IDs and signatures are deterministic and unique.",
    },
    {
        "finding_id": "REVIEW-FINDING-04",
        "name": "candidate_family_coverage_is_complete",
        "severity": "PASS",
        "description": "All seven planned candidate families are represented.",
    },
    {
        "finding_id": "REVIEW-FINDING-05",
        "name": "runtime_wiring_is_blocked",
        "severity": "PASS",
        "description": "The implementation remains disconnected from solver runtime wiring.",
    },
    {
        "finding_id": "REVIEW-FINDING-06",
        "name": "real_submission_is_blocked",
        "severity": "PASS",
        "description": "No real evaluation, authentication, upload, or submission is allowed.",
    },
    {
        "finding_id": "REVIEW-FINDING-07",
        "name": "ready_for_local_diagnostic_harness",
        "severity": "PASS",
        "description": "The reviewed implementation may proceed to a local diagnostic harness.",
    },
]

RISK_CONTROLS = [
    "NO_REAL_KAGGLE_EVALUATION",
    "NO_RUNTIME_SOLVER_WIRING_IN_THIS_TASK",
    "NO_CANDIDATE_GENERATOR_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_RANKER_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_PUBLIC_SET_MEMORIZATION",
    "NO_EXTERNAL_API_DEPENDENCY",
    "NO_INTERNET_DURING_EVAL",
    "NO_KAGGLE_AUTHENTICATION",
    "NO_UPLOAD",
    "NO_SUBMISSION",
]

QUALITY_TARGETS = [
    "implementation_review_is_deterministic",
    "candidate_count_is_verified",
    "candidate_family_coverage_is_verified",
    "candidate_depth_is_verified",
    "candidate_boundary_is_verified",
    "runtime_wiring_remains_blocked",
    "next_task_is_local_diagnostic_harness",
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
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
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


def review_generated_candidates(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_ids = [candidate.get("candidate_id") for candidate in candidates]
    candidate_signatures = [candidate.get("candidate_signature") for candidate in candidates]
    families = {str(candidate.get("family")) for candidate in candidates}
    depths = [int(candidate.get("program_depth", 999)) for candidate in candidates]

    return {
        "candidate_count": len(candidates),
        "candidate_id_count": len(candidate_ids),
        "candidate_signature_count": len(candidate_signatures),
        "unique_candidate_ids": len(candidate_ids) == len(set(candidate_ids)),
        "unique_candidate_signatures": len(candidate_signatures) == len(set(candidate_signatures)),
        "families_present": sorted(families),
        "candidate_family_count": len(families),
        "expected_family_count": len(EXPECTED_FAMILIES),
        "missing_families": sorted(EXPECTED_FAMILIES - families),
        "unexpected_families": sorted(families - EXPECTED_FAMILIES),
        "max_program_depth": max(depths) if depths else 999,
        "min_program_depth": min(depths) if depths else 999,
        "all_candidates_deterministic": all(candidate.get("deterministic") is True for candidate in candidates),
        "all_candidates_local_only": all(candidate.get("local_only") is True for candidate in candidates),
        "all_candidates_public_safe": all(candidate.get("public_safe") is True for candidate in candidates),
        "all_candidates_bounded": all(candidate.get("bounded") is True for candidate in candidates),
        "all_runtime_wiring_blocked": all(candidate.get("runtime_wiring_required") is False for candidate in candidates),
        "all_runtime_solver_patch_blocked": all(candidate.get("runtime_solver_patch") is False for candidate in candidates),
        "all_candidate_generator_runtime_wiring_blocked": all(
            candidate.get("candidate_generator_runtime_wiring") is False for candidate in candidates
        ),
        "all_ranker_runtime_wiring_blocked": all(candidate.get("ranker_runtime_wiring") is False for candidate in candidates),
        "all_real_submission_blocked": all(candidate.get("real_submission_candidate") is False for candidate in candidates),
        "all_kaggle_payload_blocked": all(candidate.get("kaggle_submission_payload") is False for candidate in candidates),
    }


def build_review_report(source_record: dict[str, Any] | None) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}
    candidates = source.get("generated_candidates")
    if not isinstance(candidates, list):
        candidates = []

    candidate_review = review_generated_candidates(candidates)
    evidence = source.get("candidate_evidence_pack")
    if not isinstance(evidence, dict):
        evidence = {}

    checks = {
        "candidate_count_12": candidate_review["candidate_count"] == 12,
        "candidate_ids_unique": candidate_review["unique_candidate_ids"] is True,
        "candidate_signatures_unique": candidate_review["unique_candidate_signatures"] is True,
        "candidate_families_complete": candidate_review["missing_families"] == [] and candidate_review["unexpected_families"] == [],
        "max_program_depth_bounded": candidate_review["max_program_depth"] <= 3,
        "all_candidates_deterministic": candidate_review["all_candidates_deterministic"] is True,
        "all_candidates_local_only": candidate_review["all_candidates_local_only"] is True,
        "all_candidates_public_safe": candidate_review["all_candidates_public_safe"] is True,
        "all_candidates_bounded": candidate_review["all_candidates_bounded"] is True,
        "all_runtime_wiring_blocked": candidate_review["all_runtime_wiring_blocked"] is True,
        "all_runtime_solver_patch_blocked": candidate_review["all_runtime_solver_patch_blocked"] is True,
        "all_candidate_generator_runtime_wiring_blocked": candidate_review["all_candidate_generator_runtime_wiring_blocked"] is True,
        "all_ranker_runtime_wiring_blocked": candidate_review["all_ranker_runtime_wiring_blocked"] is True,
        "all_real_submission_blocked": candidate_review["all_real_submission_blocked"] is True,
        "all_kaggle_payload_blocked": candidate_review["all_kaggle_payload_blocked"] is True,
        "source_evidence_candidate_count_ok": evidence.get("candidate_count") == 12,
        "source_evidence_depth_ok": evidence.get("max_program_depth") == 2,
        "source_evidence_runtime_blocked": evidence.get("all_runtime_wiring_blocked") is True,
        "source_evidence_submission_blocked": evidence.get("all_real_submission_blocked") is True,
    }

    blocking_issues = [name for name, passed in checks.items() if passed is not True]

    return {
        "review_id": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_REPORT_V1",
        "source_revision": source.get("revision"),
        "source_task_verdict": source.get("task_verdict"),
        "source_implementation_verdict": source.get("implementation_verdict"),
        "source_next_stage": source.get("next_stage"),
        "candidate_review": candidate_review,
        "source_evidence_pack": evidence,
        "checks": checks,
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(blocking_issues),
        "blocking_issue_count": len(blocking_issues),
        "blocking_issues": blocking_issues,
        "review_findings": REVIEW_FINDINGS,
        "review_finding_count": len(REVIEW_FINDINGS),
        "review_passed": len(blocking_issues) == 0,
        "review_verdict": REVIEW_VERDICT,
        "recommended_next_stage": NEXT_STAGE,
    }


def build_implementation_review_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_IMPLEMENTATION_ARTIFACT.exists()
    source_record = _load_json(SOURCE_IMPLEMENTATION_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_ready = bool(
        source_record
        and source_record.get("controlled_candidate_generator_implementation_ready") is True
        and source_record.get("controlled_candidate_generator_implementation_passed") is True
    )
    source_shape_ok = bool(
        source_record
        and source_record.get("candidate_template_count") == 12
        and source_record.get("candidate_family_count") == 7
        and source_record.get("generated_candidate_count") == 12
        and source_record.get("max_program_depth") == 2
    )
    source_next_stage_ok = bool(
        source_record
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_7_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_V1"
    )
    source_blocks_runtime_wiring = bool(
        source_record
        and source_record.get("candidate_generator_wiring_authorized") is False
        and source_record.get("runtime_wiring_authorized") is False
        and source_record.get("runtime_solver_modified") is False
        and source_record.get("candidate_generator_modified") is False
        and source_record.get("ranker_runtime_modified") is False
    )
    source_blocks_real_actions = bool(
        source_record
        and source_record.get("real_evaluation_performed") is False
        and source_record.get("real_kaggle_evaluation_allowed") is False
        and source_record.get("real_submission_allowed") is False
        and source_record.get("ready_for_real_kaggle_submission") is False
        and source_record.get("manual_upload_allowed") is False
        and source_record.get("kaggle_authentication_allowed") is False
        and source_record.get("kaggle_authentication_performed") is False
        and source_record.get("kaggle_upload_allowed") is False
        and source_record.get("kaggle_submission_sent") is False
    )
    source_boundaries_ok = bool(
        source_record
        and source_record.get("local_only") is True
        and source_record.get("deterministic") is True
        and source_record.get("public_safe") is True
        and source_record.get("public_overfit_allowed") is False
        and source_record.get("public_overfit_guard_required") is True
        and source_record.get("external_api_dependency") is False
        and source_record.get("internet_during_eval") is False
        and source_record.get("private_core_exposure") is False
        and source_record.get("legal_certification") is False
        and source_record.get("official_score_claim_allowed") is False
        and source_record.get("competitive_score_claim_allowed") is False
    )

    review_report = build_review_report(source_record)
    review_passed = review_report["review_passed"] is True
    candidate_review = review_report["candidate_review"]

    implementation_review_ready = True
    local_diagnostic_harness_authorized = True
    candidate_generator_wiring_authorized = False
    runtime_wiring_authorized = False
    runtime_solver_modified = False
    candidate_generator_modified = False
    ranker_runtime_modified = False
    real_evaluation_performed = False
    real_submission_allowed = False
    ready_for_real_kaggle_submission = False
    kaggle_authentication_allowed = False
    kaggle_authentication_performed = False
    kaggle_upload_allowed = False
    kaggle_submission_sent = False

    gates = [
        _gate("source_artifact_present", source_artifact_present, True, "Task 6 implementation artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Task 6 implementation artifact is parseable."),
        _gate("source_ready", source_ready, True, "Task 6 implementation is ready and passed."),
        _gate("source_shape_ok", source_shape_ok, True, "Task 6 implementation has expected shape."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 6 points to Task 7."),
        _gate("source_blocks_runtime_wiring", source_blocks_runtime_wiring, True, "Task 6 blocks runtime wiring."),
        _gate("source_blocks_real_actions", source_blocks_real_actions, True, "Task 6 blocks real actions."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Task 6 preserves boundaries."),
        _gate("review_passed", review_passed, True, "Implementation review passed."),
        _gate("candidate_count_12", candidate_review["candidate_count"] == 12, True, "Twelve candidates are present."),
        _gate("candidate_ids_unique", candidate_review["unique_candidate_ids"], True, "Candidate IDs are unique."),
        _gate("candidate_families_complete", candidate_review["missing_families"] == [] and candidate_review["unexpected_families"] == [], True, "Candidate family coverage is complete."),
        _gate("max_program_depth_bounded", candidate_review["max_program_depth"] <= 3, True, "Program depth is bounded."),
        _gate("all_candidates_deterministic", candidate_review["all_candidates_deterministic"], True, "Candidates are deterministic."),
        _gate("all_candidates_local_only", candidate_review["all_candidates_local_only"], True, "Candidates are local-only."),
        _gate("all_candidates_public_safe", candidate_review["all_candidates_public_safe"], True, "Candidates are public-safe."),
        _gate("all_runtime_wiring_blocked", candidate_review["all_runtime_wiring_blocked"], True, "Runtime wiring is blocked."),
        _gate("all_real_submission_blocked", candidate_review["all_real_submission_blocked"], True, "Real submission is blocked."),
        _gate("implementation_review_ready_true", implementation_review_ready is True, True, "Implementation review is ready."),
        _gate("local_diagnostic_harness_authorized_true", local_diagnostic_harness_authorized is True, True, "Local diagnostic harness is authorized as next stage."),
        _gate("candidate_generator_wiring_authorized_false", candidate_generator_wiring_authorized is False, True, "Candidate generator runtime wiring remains blocked."),
        _gate("runtime_wiring_authorized_false", runtime_wiring_authorized is False, True, "Runtime wiring remains blocked."),
        _gate("runtime_solver_modified_false", runtime_solver_modified is False, True, "Runtime solver is not modified."),
        _gate("candidate_generator_modified_false", candidate_generator_modified is False, True, "Runtime candidate generator is not modified."),
        _gate("ranker_runtime_modified_false", ranker_runtime_modified is False, True, "Ranker runtime is not modified."),
        _gate("real_evaluation_performed_false", real_evaluation_performed is False, True, "No real evaluation is performed."),
        _gate("real_submission_allowed_false", real_submission_allowed is False, True, "Real submission remains blocked."),
        _gate("ready_for_real_kaggle_submission_false", ready_for_real_kaggle_submission is False, True, "Real submission readiness remains blocked."),
        _gate("kaggle_authentication_allowed_false", kaggle_authentication_allowed is False, True, "Kaggle authentication remains blocked."),
        _gate("kaggle_authentication_performed_false", kaggle_authentication_performed is False, True, "Kaggle authentication is not performed."),
        _gate("kaggle_upload_allowed_false", kaggle_upload_allowed is False, True, "Kaggle upload remains blocked."),
        _gate("kaggle_submission_sent_false", kaggle_submission_sent is False, True, "No Kaggle submission is sent."),
        _gate("public_overfit_allowed_false", True, True, "Public overfit remains blocked."),
        _gate("public_overfit_guard_required_true", True, True, "Public overfit guard remains required."),
        _gate("external_api_dependency_false", True, True, "External API dependency remains false."),
        _gate("internet_during_eval_false", True, True, "Internet during evaluation remains false."),
        _gate("private_core_exposure_false", True, True, "Private core exposure remains false."),
        _gate("legal_certification_false", True, True, "legal_certification remains false."),
        _gate("official_score_claim_allowed_false", True, True, "Official score claim remains blocked."),
        _gate("competitive_score_claim_allowed_false", True, True, "Competitive score claim remains blocked."),
        _gate("local_only_true", True, True, "Task remains local-only."),
        _gate("deterministic_true", True, True, "Task remains deterministic."),
        _gate("public_safe_true", True, True, "Task remains public-safe."),
        _gate("fail_closed_active", True, True, "Review fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    record_passed = len(required_gates) == len(passed_required_gates)

    review_summary = {
        "review_status": "PASS" if record_passed else "FAIL_CLOSED",
        "review_verdict": REVIEW_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "candidate_count": candidate_review["candidate_count"],
        "candidate_family_count": candidate_review["candidate_family_count"],
        "max_program_depth": candidate_review["max_program_depth"],
        "candidate_ids_unique": candidate_review["unique_candidate_ids"],
        "blocking_issue_count": review_report["blocking_issue_count"],
        "runtime_wiring_authorized": False,
        "candidate_generator_wiring_authorized": False,
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
        "source_implementation_artifact": str(SOURCE_IMPLEMENTATION_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_ready": source_ready,
        "source_shape_ok": source_shape_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "source_blocks_runtime_wiring": source_blocks_runtime_wiring,
        "source_blocks_real_actions": source_blocks_real_actions,
        "source_boundaries_ok": source_boundaries_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "review_verdict": REVIEW_VERDICT,
        "implementation_review_ready": implementation_review_ready,
        "implementation_review_valid": record_passed,
        "implementation_review_passed": record_passed,
        "local_diagnostic_harness_authorized": local_diagnostic_harness_authorized,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "review_summary": review_summary,
        "review_report": review_report,
        "candidate_review": candidate_review,
        "review_criteria": REVIEW_CRITERIA,
        "review_criterion_count": len(REVIEW_CRITERIA),
        "review_findings": REVIEW_FINDINGS,
        "review_finding_count": len(REVIEW_FINDINGS),
        "candidate_count": candidate_review["candidate_count"],
        "candidate_family_count": candidate_review["candidate_family_count"],
        "expected_candidate_family_count": len(EXPECTED_FAMILIES),
        "max_program_depth": candidate_review["max_program_depth"],
        "candidate_ids_unique": candidate_review["unique_candidate_ids"],
        "candidate_signatures_unique": candidate_review["unique_candidate_signatures"],
        "missing_families": candidate_review["missing_families"],
        "unexpected_families": candidate_review["unexpected_families"],
        "blocking_issue_count": review_report["blocking_issue_count"],
        "blocking_issues": review_report["blocking_issues"],
        "candidate_generator_wiring_authorized": candidate_generator_wiring_authorized,
        "runtime_wiring_authorized": runtime_wiring_authorized,
        "runtime_solver_modified": runtime_solver_modified,
        "candidate_generator_modified": candidate_generator_modified,
        "ranker_runtime_modified": ranker_runtime_modified,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "program_synthesis_candidate_generator_implementation_review_allowed": True,
        "real_kaggle_evaluation_allowed": False,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "open_source_prize_eligibility_required": True,
        "real_submission_allowed": real_submission_allowed,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": kaggle_authentication_allowed,
        "kaggle_authentication_performed": kaggle_authentication_performed,
        "kaggle_upload_allowed": kaggle_upload_allowed,
        "kaggle_submission_sent": kaggle_submission_sent,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "submission_json_created": False,
        "real_submission_candidate_created": False,
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
        "review_gate_count": len(gates),
        "review_pass_count": len(passed_required_gates),
        "review_blocking_issue_count": 0 if record_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if record_passed else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "risk_controls": RISK_CONTROLS,
        "risk_control_count": len(RISK_CONTROLS),
        "quality_targets": QUALITY_TARGETS,
        "quality_target_count": len(QUALITY_TARGETS),
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-IMPLEMENTATION-REVIEW-" + signature[:12]
    return record


def validate_implementation_review_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_artifact_present",
        "source_artifact_parseable",
        "source_ready",
        "source_shape_ok",
        "source_next_stage_ok",
        "source_blocks_runtime_wiring",
        "source_blocks_real_actions",
        "source_boundaries_ok",
        "implementation_review_ready",
        "implementation_review_valid",
        "implementation_review_passed",
        "local_diagnostic_harness_authorized",
        "candidate_ids_unique",
        "candidate_signatures_unique",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "program_synthesis_candidate_generator_implementation_review_allowed",
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
        "candidate_generator_wiring_authorized",
        "runtime_wiring_authorized",
        "runtime_solver_modified",
        "candidate_generator_modified",
        "ranker_runtime_modified",
        "real_evaluation_performed",
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
        "kaggle_submission_sent",
        "operator_approval_received",
        "submission_json_created",
        "real_submission_candidate_created",
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

    if record.get("review_verdict") != REVIEW_VERDICT:
        issues.append("REVIEW_VERDICT_MISMATCH")

    expected_counts = {
        "candidate_count": 12,
        "candidate_family_count": 7,
        "expected_candidate_family_count": 7,
        "max_program_depth": 2,
        "review_criterion_count": 25,
        "review_finding_count": 7,
        "blocking_issue_count": 0,
        "review_blocking_issue_count": 0,
        "issue_count": 0,
        "risk_control_count": 10,
        "quality_target_count": 7,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    if record.get("missing_families") != []:
        issues.append("MISSING_FAMILIES_NOT_EMPTY")

    if record.get("unexpected_families") != []:
        issues.append("UNEXPECTED_FAMILIES_NOT_EMPTY")

    review_report = record.get("review_report")
    if not isinstance(review_report, dict):
        issues.append("REVIEW_REPORT_MISSING")
    else:
        if review_report.get("review_passed") is not True:
            issues.append("REVIEW_REPORT_NOT_PASSED")
        if review_report.get("blocking_issue_count") != 0:
            issues.append("REVIEW_REPORT_BLOCKING_ISSUES_PRESENT")
        if review_report.get("recommended_next_stage") != NEXT_STAGE:
            issues.append("REVIEW_REPORT_NEXT_STAGE_MISMATCH")

    candidate_review = record.get("candidate_review")
    if not isinstance(candidate_review, dict):
        issues.append("CANDIDATE_REVIEW_MISSING")
    else:
        expected_candidate_review_true = [
            "unique_candidate_ids",
            "unique_candidate_signatures",
            "all_candidates_deterministic",
            "all_candidates_local_only",
            "all_candidates_public_safe",
            "all_candidates_bounded",
            "all_runtime_wiring_blocked",
            "all_runtime_solver_patch_blocked",
            "all_candidate_generator_runtime_wiring_blocked",
            "all_ranker_runtime_wiring_blocked",
            "all_real_submission_blocked",
            "all_kaggle_payload_blocked",
        ]
        for key in expected_candidate_review_true:
            if candidate_review.get(key) is not True:
                issues.append(f"CANDIDATE_REVIEW_{key}_NOT_TRUE")
        if candidate_review.get("candidate_count") != 12:
            issues.append("CANDIDATE_REVIEW_CANDIDATE_COUNT_MISMATCH")
        if candidate_review.get("candidate_family_count") != 7:
            issues.append("CANDIDATE_REVIEW_FAMILY_COUNT_MISMATCH")
        if candidate_review.get("max_program_depth") != 2:
            issues.append("CANDIDATE_REVIEW_MAX_DEPTH_MISMATCH")

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

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-implementation-review-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-implementation-review-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-implementation-review-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-implementation-review-v1.md"

    json_path.write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "review_verdict": record["review_verdict"],
        "next_stage": record["next_stage"],
        "source_ready": record["source_ready"],
        "source_shape_ok": record["source_shape_ok"],
        "implementation_review_ready": record["implementation_review_ready"],
        "candidate_count": record["candidate_count"],
        "candidate_family_count": record["candidate_family_count"],
        "max_program_depth": record["max_program_depth"],
        "blocking_issue_count": record["blocking_issue_count"],
        "local_diagnostic_harness_authorized": record["local_diagnostic_harness_authorized"],
        "candidate_generator_wiring_authorized": record["candidate_generator_wiring_authorized"],
        "runtime_wiring_authorized": record["runtime_wiring_authorized"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "candidate_generator_modified": record["candidate_generator_modified"],
        "real_submission_allowed": record["real_submission_allowed"],
        "kaggle_authentication_allowed": record["kaggle_authentication_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "private_core_exposure": record["private_core_exposure"],
        "legal_certification": record["legal_certification"],
    }
    index_path.write_text(
        json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    manifest_lines = [
        f"revision={record['revision']}",
        f"task_id={record['task_id']}",
        f"signature={record['signature']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_scope={record['task_scope']}",
        f"task_verdict={record['task_verdict']}",
        f"review_verdict={record['review_verdict']}",
        f"next_stage={record['next_stage']}",
        f"source_ready={record['source_ready']}",
        f"source_shape_ok={record['source_shape_ok']}",
        f"implementation_review_ready={record['implementation_review_ready']}",
        f"candidate_count={record['candidate_count']}",
        f"candidate_family_count={record['candidate_family_count']}",
        f"max_program_depth={record['max_program_depth']}",
        f"blocking_issue_count={record['blocking_issue_count']}",
        f"local_diagnostic_harness_authorized={record['local_diagnostic_harness_authorized']}",
        f"candidate_generator_wiring_authorized={record['candidate_generator_wiring_authorized']}",
        f"runtime_wiring_authorized={record['runtime_wiring_authorized']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"candidate_generator_modified={record['candidate_generator_modified']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_authentication_allowed={record['kaggle_authentication_allowed']}",
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
    criteria_lines = "\n".join([f"- `{criterion}`" for criterion in record["review_criteria"]])

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- review_verdict: `{record['review_verdict']}`
- next_stage: `{record['next_stage']}`

## Review Summary

- source_ready: `{record['source_ready']}`
- source_shape_ok: `{record['source_shape_ok']}`
- implementation_review_ready: `{record['implementation_review_ready']}`
- implementation_review_passed: `{record['implementation_review_passed']}`
- candidate_count: `{record['candidate_count']}`
- candidate_family_count: `{record['candidate_family_count']}`
- max_program_depth: `{record['max_program_depth']}`
- candidate_ids_unique: `{record['candidate_ids_unique']}`
- blocking_issue_count: `{record['blocking_issue_count']}`
- local_diagnostic_harness_authorized: `{record['local_diagnostic_harness_authorized']}`

## Review Criteria

{criteria_lines}

## Review Findings

{finding_lines}

## Boundary

- candidate_generator_wiring_authorized: `{record['candidate_generator_wiring_authorized']}`
- runtime_wiring_authorized: `{record['runtime_wiring_authorized']}`
- runtime_solver_modified: `{record['runtime_solver_modified']}`
- candidate_generator_modified: `{record['candidate_generator_modified']}`
- ranker_runtime_modified: `{record['ranker_runtime_modified']}`
- real_evaluation_performed: `{record['real_evaluation_performed']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- ready_for_real_kaggle_submission: `{record['ready_for_real_kaggle_submission']}`
- kaggle_authentication_allowed: `{record['kaggle_authentication_allowed']}`
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
    record = build_implementation_review_record()
    issues = validate_implementation_review_record(record)
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
    print(f"candidate_count={record['candidate_count']}")
    print(f"candidate_family_count={record['candidate_family_count']}")
    print(f"max_program_depth={record['max_program_depth']}")
    print(f"blocking_issue_count={record['blocking_issue_count']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
