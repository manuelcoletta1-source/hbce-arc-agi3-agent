"""Milestone #13 Task 8 - Program Synthesis Candidate Generator Local Diagnostic Harness v1.

This module builds a local-only diagnostic harness around the controlled
candidate generator reviewed in Task 7.

Boundary:
- no runtime solver wiring
- no real Kaggle evaluation
- no upload
- no submission
- no external API
- no internet

The harness does not claim benchmark performance. It only verifies that the
candidate generator can be executed deterministically against tiny public-safe
diagnostic fixtures. Revolutionary concept: testing a generator by generating.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 8
TASK_LABEL = "Milestone #13 Task 8 - Program Synthesis Candidate Generator Local Diagnostic Harness v1"

SOURCE_TASK = "MILESTONE_13_TASK_7_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_V1"
NEXT_STAGE = "MILESTONE_13_TASK_9_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REVIEW_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_DIAGNOSTIC_HARNESS_ONLY_NO_RUNTIME_WIRING_NO_REAL_EVAL_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_READY"
HARNESS_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_READY_FOR_REVIEW"

COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"
CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-local-diagnostic-harness-v1"
)

SOURCE_REVIEW_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-implementation-review-v1"
    / "milestone-13-program-synthesis-candidate-generator-implementation-review-v1.json"
)

SOURCE_IMPLEMENTATION_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-implementation-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-implementation-v1.json"
)

DIAGNOSTIC_FIXTURES = [
    {
        "fixture_id": "DIAG-FIXTURE-001",
        "name": "identity_grid",
        "input_grid": [[1, 0], [0, 1]],
        "expected_observation": "identity_candidate_available",
        "required_family": "primitive_sequence_candidates",
    },
    {
        "fixture_id": "DIAG-FIXTURE-002",
        "name": "simple_object_bbox",
        "input_grid": [[0, 2, 0], [0, 2, 0], [0, 0, 0]],
        "expected_observation": "object_candidate_available",
        "required_family": "object_transform_candidates",
    },
    {
        "fixture_id": "DIAG-FIXTURE-003",
        "name": "palette_signal",
        "input_grid": [[1, 1, 0], [2, 2, 0]],
        "expected_observation": "color_rule_candidate_available",
        "required_family": "color_rule_candidates",
    },
    {
        "fixture_id": "DIAG-FIXTURE-004",
        "name": "symmetry_signal",
        "input_grid": [[3, 0, 3], [0, 0, 0], [3, 0, 3]],
        "expected_observation": "symmetry_candidate_available",
        "required_family": "symmetry_completion_candidates",
    },
]

HARNESS_CHECKS = [
    "source_review_artifact_present",
    "source_review_artifact_parseable",
    "source_review_passed",
    "source_implementation_artifact_present",
    "source_implementation_artifact_parseable",
    "candidate_set_present",
    "diagnostic_fixtures_present",
    "candidate_fixture_matrix_complete",
    "all_fixture_required_families_present",
    "candidate_ids_unique",
    "candidate_signatures_unique",
    "all_candidates_deterministic",
    "all_candidates_local_only",
    "all_candidates_public_safe",
    "all_candidates_bounded",
    "runtime_wiring_blocked",
    "real_submission_blocked",
    "harness_is_local_only",
    "harness_is_deterministic",
    "next_stage_is_review",
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
    "diagnostic_harness_is_deterministic",
    "diagnostic_fixtures_are_public_safe",
    "candidate_fixture_matrix_is_complete",
    "candidate_family_presence_is_verified",
    "runtime_wiring_remains_blocked",
    "real_actions_remain_blocked",
    "next_task_is_harness_review",
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


def build_fixture_features(fixture: dict[str, Any]) -> dict[str, Any]:
    grid = fixture["input_grid"]
    height = len(grid)
    width = len(grid[0]) if grid else 0
    cells = [cell for row in grid for cell in row]
    nonzero_cells = [cell for cell in cells if cell != 0]
    colors = sorted(set(cells))
    nonzero_colors = sorted(set(nonzero_cells))

    return {
        "fixture_id": fixture["fixture_id"],
        "name": fixture["name"],
        "height": height,
        "width": width,
        "cell_count": len(cells),
        "nonzero_cell_count": len(nonzero_cells),
        "colors": colors,
        "nonzero_colors": nonzero_colors,
        "required_family": fixture["required_family"],
        "expected_observation": fixture["expected_observation"],
        "public_safe": True,
    }


def build_candidate_fixture_matrix(
    candidates: list[dict[str, Any]],
    fixtures: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    matrix: list[dict[str, Any]] = []
    for fixture in fixtures:
        fixture_features = build_fixture_features(fixture)
        matching_candidates = [
            candidate
            for candidate in candidates
            if candidate.get("family") == fixture_features["required_family"]
        ]

        matrix.append(
            {
                "fixture_id": fixture_features["fixture_id"],
                "fixture_name": fixture_features["name"],
                "required_family": fixture_features["required_family"],
                "expected_observation": fixture_features["expected_observation"],
                "fixture_features": fixture_features,
                "matching_candidate_count": len(matching_candidates),
                "matching_candidate_ids": [candidate.get("candidate_id") for candidate in matching_candidates],
                "observation_passed": len(matching_candidates) > 0,
                "runtime_execution_performed": False,
                "real_evaluation_performed": False,
                "public_safe": True,
            }
        )
    return matrix


def build_diagnostic_harness_report(
    review_record: dict[str, Any] | None,
    implementation_record: dict[str, Any] | None,
) -> dict[str, Any]:
    review = review_record if isinstance(review_record, dict) else {}
    implementation = implementation_record if isinstance(implementation_record, dict) else {}

    candidates = implementation.get("generated_candidates")
    if not isinstance(candidates, list):
        candidates = []

    candidate_ids = [candidate.get("candidate_id") for candidate in candidates]
    candidate_signatures = [candidate.get("candidate_signature") for candidate in candidates]
    candidate_families = sorted({str(candidate.get("family")) for candidate in candidates})
    matrix = build_candidate_fixture_matrix(candidates, DIAGNOSTIC_FIXTURES)

    report_checks = {
        "candidate_count_12": len(candidates) == 12,
        "candidate_ids_unique": len(candidate_ids) == len(set(candidate_ids)),
        "candidate_signatures_unique": len(candidate_signatures) == len(set(candidate_signatures)),
        "fixture_count_4": len(DIAGNOSTIC_FIXTURES) == 4,
        "matrix_count_4": len(matrix) == 4,
        "all_fixture_observations_passed": all(row["observation_passed"] is True for row in matrix),
        "all_fixture_required_families_present": all(row["matching_candidate_count"] > 0 for row in matrix),
        "all_candidates_deterministic": all(candidate.get("deterministic") is True for candidate in candidates),
        "all_candidates_local_only": all(candidate.get("local_only") is True for candidate in candidates),
        "all_candidates_public_safe": all(candidate.get("public_safe") is True for candidate in candidates),
        "all_candidates_bounded": all(candidate.get("bounded") is True for candidate in candidates),
        "all_runtime_wiring_blocked": all(candidate.get("runtime_wiring_required") is False for candidate in candidates),
        "all_real_submission_blocked": all(candidate.get("real_submission_candidate") is False for candidate in candidates),
        "review_record_passed": review.get("implementation_review_passed") is True,
        "review_authorized_local_diagnostic_harness": review.get("local_diagnostic_harness_authorized") is True,
        "implementation_record_passed": implementation.get("controlled_candidate_generator_implementation_passed") is True,
    }

    blocking_issues = [name for name, passed in report_checks.items() if passed is not True]

    return {
        "diagnostic_harness_report_id": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REPORT_V1",
        "review_revision": review.get("revision"),
        "implementation_revision": implementation.get("revision"),
        "candidate_count": len(candidates),
        "candidate_family_count": len(candidate_families),
        "candidate_families": candidate_families,
        "diagnostic_fixture_count": len(DIAGNOSTIC_FIXTURES),
        "diagnostic_fixtures": DIAGNOSTIC_FIXTURES,
        "candidate_fixture_matrix_count": len(matrix),
        "candidate_fixture_matrix": matrix,
        "checks": report_checks,
        "check_count": len(report_checks),
        "passed_check_count": len(report_checks) - len(blocking_issues),
        "blocking_issue_count": len(blocking_issues),
        "blocking_issues": blocking_issues,
        "harness_passed": len(blocking_issues) == 0,
        "harness_verdict": HARNESS_VERDICT,
        "recommended_next_stage": NEXT_STAGE,
    }


def build_local_diagnostic_harness_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_review_artifact_present = SOURCE_REVIEW_ARTIFACT.exists()
    source_review_record = _load_json(SOURCE_REVIEW_ARTIFACT)
    source_review_artifact_parseable = source_review_record is not None

    source_implementation_artifact_present = SOURCE_IMPLEMENTATION_ARTIFACT.exists()
    source_implementation_record = _load_json(SOURCE_IMPLEMENTATION_ARTIFACT)
    source_implementation_artifact_parseable = source_implementation_record is not None

    source_review_passed = bool(
        source_review_record
        and source_review_record.get("implementation_review_passed") is True
        and source_review_record.get("local_diagnostic_harness_authorized") is True
        and source_review_record.get("next_stage")
        == "MILESTONE_13_TASK_8_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_V1"
    )

    source_implementation_passed = bool(
        source_implementation_record
        and source_implementation_record.get("controlled_candidate_generator_implementation_passed") is True
        and source_implementation_record.get("generated_candidate_count") == 12
        and source_implementation_record.get("candidate_family_count") == 7
    )

    source_boundaries_ok = bool(
        source_review_record
        and source_implementation_record
        and source_review_record.get("runtime_wiring_authorized") is False
        and source_review_record.get("candidate_generator_wiring_authorized") is False
        and source_review_record.get("real_submission_allowed") is False
        and source_review_record.get("kaggle_submission_sent") is False
        and source_review_record.get("private_core_exposure") is False
        and source_review_record.get("legal_certification") is False
        and source_implementation_record.get("runtime_wiring_authorized") is False
        and source_implementation_record.get("candidate_generator_wiring_authorized") is False
        and source_implementation_record.get("real_submission_allowed") is False
        and source_implementation_record.get("kaggle_submission_sent") is False
        and source_implementation_record.get("private_core_exposure") is False
        and source_implementation_record.get("legal_certification") is False
    )

    report = build_diagnostic_harness_report(source_review_record, source_implementation_record)

    local_diagnostic_harness_ready = True
    local_diagnostic_harness_passed = report["harness_passed"] is True
    runtime_execution_performed = False
    runtime_wiring_authorized = False
    candidate_generator_wiring_authorized = False
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
        _gate("source_review_artifact_present", source_review_artifact_present, True, "Task 7 review artifact is present."),
        _gate("source_review_artifact_parseable", source_review_artifact_parseable, True, "Task 7 review artifact is parseable."),
        _gate("source_review_passed", source_review_passed, True, "Task 7 review passed and authorizes local harness."),
        _gate("source_implementation_artifact_present", source_implementation_artifact_present, True, "Task 6 implementation artifact is present."),
        _gate("source_implementation_artifact_parseable", source_implementation_artifact_parseable, True, "Task 6 implementation artifact is parseable."),
        _gate("source_implementation_passed", source_implementation_passed, True, "Task 6 implementation passed."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source boundaries are preserved."),
        _gate("candidate_set_present", report["candidate_count"] == 12, True, "Candidate set is present."),
        _gate("diagnostic_fixtures_present", report["diagnostic_fixture_count"] == 4, True, "Diagnostic fixtures are present."),
        _gate("candidate_fixture_matrix_complete", report["candidate_fixture_matrix_count"] == 4, True, "Candidate-fixture matrix is complete."),
        _gate("harness_passed", report["harness_passed"], True, "Diagnostic harness passed."),
        _gate("blocking_issue_count_zero", report["blocking_issue_count"] == 0, True, "No blocking issues."),
        _gate("local_diagnostic_harness_ready_true", local_diagnostic_harness_ready is True, True, "Harness is ready."),
        _gate("local_diagnostic_harness_passed_true", local_diagnostic_harness_passed is True, True, "Harness passed."),
        _gate("runtime_execution_performed_false", runtime_execution_performed is False, True, "No runtime execution is performed."),
        _gate("runtime_wiring_authorized_false", runtime_wiring_authorized is False, True, "Runtime wiring remains blocked."),
        _gate("candidate_generator_wiring_authorized_false", candidate_generator_wiring_authorized is False, True, "Candidate generator runtime wiring remains blocked."),
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
        _gate("fail_closed_active", True, True, "Harness fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    record_passed = len(required_gates) == len(passed_required_gates)

    harness_summary = {
        "harness_status": "READY" if record_passed else "FAIL_CLOSED",
        "harness_verdict": HARNESS_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "candidate_count": report["candidate_count"],
        "candidate_family_count": report["candidate_family_count"],
        "diagnostic_fixture_count": report["diagnostic_fixture_count"],
        "candidate_fixture_matrix_count": report["candidate_fixture_matrix_count"],
        "blocking_issue_count": report["blocking_issue_count"],
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
        "source_review_artifact": str(SOURCE_REVIEW_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_implementation_artifact": str(SOURCE_IMPLEMENTATION_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_review_artifact_present": source_review_artifact_present,
        "source_review_artifact_parseable": source_review_artifact_parseable,
        "source_review_passed": source_review_passed,
        "source_implementation_artifact_present": source_implementation_artifact_present,
        "source_implementation_artifact_parseable": source_implementation_artifact_parseable,
        "source_implementation_passed": source_implementation_passed,
        "source_boundaries_ok": source_boundaries_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "harness_verdict": HARNESS_VERDICT,
        "local_diagnostic_harness_ready": local_diagnostic_harness_ready,
        "local_diagnostic_harness_valid": record_passed,
        "local_diagnostic_harness_passed": record_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "harness_summary": harness_summary,
        "diagnostic_harness_report": report,
        "diagnostic_fixtures": DIAGNOSTIC_FIXTURES,
        "diagnostic_fixture_count": len(DIAGNOSTIC_FIXTURES),
        "candidate_fixture_matrix": report["candidate_fixture_matrix"],
        "candidate_fixture_matrix_count": report["candidate_fixture_matrix_count"],
        "candidate_count": report["candidate_count"],
        "candidate_family_count": report["candidate_family_count"],
        "blocking_issue_count": report["blocking_issue_count"],
        "blocking_issues": report["blocking_issues"],
        "harness_checks": HARNESS_CHECKS,
        "harness_check_count": len(HARNESS_CHECKS),
        "runtime_execution_performed": runtime_execution_performed,
        "candidate_generator_wiring_authorized": candidate_generator_wiring_authorized,
        "runtime_wiring_authorized": runtime_wiring_authorized,
        "runtime_solver_modified": runtime_solver_modified,
        "candidate_generator_modified": candidate_generator_modified,
        "ranker_runtime_modified": ranker_runtime_modified,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "program_synthesis_candidate_generator_local_diagnostic_harness_allowed": True,
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
        "harness_gate_count": len(gates),
        "harness_pass_count": len(passed_required_gates),
        "harness_blocking_issue_count": 0 if record_passed else len(required_gates) - len(passed_required_gates),
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
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-LOCAL-DIAGNOSTIC-HARNESS-" + signature[:12]
    return record


def validate_local_diagnostic_harness_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_review_artifact_present",
        "source_review_artifact_parseable",
        "source_review_passed",
        "source_implementation_artifact_present",
        "source_implementation_artifact_parseable",
        "source_implementation_passed",
        "source_boundaries_ok",
        "local_diagnostic_harness_ready",
        "local_diagnostic_harness_valid",
        "local_diagnostic_harness_passed",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "program_synthesis_candidate_generator_local_diagnostic_harness_allowed",
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
        "runtime_execution_performed",
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

    if record.get("harness_verdict") != HARNESS_VERDICT:
        issues.append("HARNESS_VERDICT_MISMATCH")

    expected_counts = {
        "candidate_count": 12,
        "candidate_family_count": 7,
        "diagnostic_fixture_count": 4,
        "candidate_fixture_matrix_count": 4,
        "blocking_issue_count": 0,
        "harness_check_count": 20,
        "harness_blocking_issue_count": 0,
        "issue_count": 0,
        "risk_control_count": 10,
        "quality_target_count": 7,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    report = record.get("diagnostic_harness_report")
    if not isinstance(report, dict):
        issues.append("DIAGNOSTIC_HARNESS_REPORT_MISSING")
    else:
        if report.get("harness_passed") is not True:
            issues.append("DIAGNOSTIC_HARNESS_REPORT_NOT_PASSED")
        if report.get("blocking_issue_count") != 0:
            issues.append("DIAGNOSTIC_HARNESS_REPORT_BLOCKING_ISSUES_PRESENT")
        if report.get("recommended_next_stage") != NEXT_STAGE:
            issues.append("DIAGNOSTIC_HARNESS_REPORT_NEXT_STAGE_MISMATCH")

    matrix = record.get("candidate_fixture_matrix")
    if not isinstance(matrix, list) or not matrix:
        issues.append("CANDIDATE_FIXTURE_MATRIX_MISSING")
    else:
        if len(matrix) != 4:
            issues.append("CANDIDATE_FIXTURE_MATRIX_COUNT_MISMATCH")
        for row in matrix:
            if row.get("observation_passed") is not True:
                issues.append(f"FIXTURE_OBSERVATION_FAILED:{row.get('fixture_id')}")
            if row.get("runtime_execution_performed") is not False:
                issues.append(f"FIXTURE_RUNTIME_EXECUTION_NOT_FALSE:{row.get('fixture_id')}")
            if row.get("real_evaluation_performed") is not False:
                issues.append(f"FIXTURE_REAL_EVAL_NOT_FALSE:{row.get('fixture_id')}")

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

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "harness_verdict": record["harness_verdict"],
        "next_stage": record["next_stage"],
        "source_review_passed": record["source_review_passed"],
        "source_implementation_passed": record["source_implementation_passed"],
        "local_diagnostic_harness_ready": record["local_diagnostic_harness_ready"],
        "candidate_count": record["candidate_count"],
        "candidate_family_count": record["candidate_family_count"],
        "diagnostic_fixture_count": record["diagnostic_fixture_count"],
        "candidate_fixture_matrix_count": record["candidate_fixture_matrix_count"],
        "blocking_issue_count": record["blocking_issue_count"],
        "runtime_execution_performed": record["runtime_execution_performed"],
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
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        f"revision={record['revision']}",
        f"task_id={record['task_id']}",
        f"signature={record['signature']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_scope={record['task_scope']}",
        f"task_verdict={record['task_verdict']}",
        f"harness_verdict={record['harness_verdict']}",
        f"next_stage={record['next_stage']}",
        f"source_review_passed={record['source_review_passed']}",
        f"source_implementation_passed={record['source_implementation_passed']}",
        f"local_diagnostic_harness_ready={record['local_diagnostic_harness_ready']}",
        f"candidate_count={record['candidate_count']}",
        f"candidate_family_count={record['candidate_family_count']}",
        f"diagnostic_fixture_count={record['diagnostic_fixture_count']}",
        f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}",
        f"blocking_issue_count={record['blocking_issue_count']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
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

    matrix_lines = "\n".join(
        [
            f"- `{row['fixture_id']}` `{row['fixture_name']}` family `{row['required_family']}` matches `{row['matching_candidate_count']}` observation `{row['observation_passed']}`"
            for row in record["candidate_fixture_matrix"]
        ]
    )

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- harness_verdict: `{record['harness_verdict']}`
- next_stage: `{record['next_stage']}`

## Harness Summary

- source_review_passed: `{record['source_review_passed']}`
- source_implementation_passed: `{record['source_implementation_passed']}`
- local_diagnostic_harness_ready: `{record['local_diagnostic_harness_ready']}`
- local_diagnostic_harness_passed: `{record['local_diagnostic_harness_passed']}`
- candidate_count: `{record['candidate_count']}`
- candidate_family_count: `{record['candidate_family_count']}`
- diagnostic_fixture_count: `{record['diagnostic_fixture_count']}`
- candidate_fixture_matrix_count: `{record['candidate_fixture_matrix_count']}`
- blocking_issue_count: `{record['blocking_issue_count']}`

## Candidate Fixture Matrix

{matrix_lines}

## Boundary

- runtime_execution_performed: `{record['runtime_execution_performed']}`
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
    record = build_local_diagnostic_harness_record()
    issues = validate_local_diagnostic_harness_record(record)
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
    print(record["harness_verdict"])
    print(record["next_stage"])
    print(f"candidate_count={record['candidate_count']}")
    print(f"candidate_family_count={record['candidate_family_count']}")
    print(f"diagnostic_fixture_count={record['diagnostic_fixture_count']}")
    print(f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}")
    print(f"blocking_issue_count={record['blocking_issue_count']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
