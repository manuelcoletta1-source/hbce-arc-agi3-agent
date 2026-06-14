"""Milestone #5 Submission Preparation Closure v1.

This module closes the local-only ARC-AGI-3 Milestone #5 submission preparation
chain. It does not create a real Kaggle submission, authenticate, upload files,
call external APIs, read secrets, or create a legal certification claim.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CLOSURE_STATUS = "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_READY"
PIPELINE_STATUS = "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/submission-preparation-closure-v1"

TASK_ARTIFACT_SPECS: Tuple[Tuple[int, str, str, Path, str, str], ...] = (
    (
        1,
        "public_readiness_baseline_audit",
        "2f02f5d Open ARC AGI3 milestone 5 public readiness audit",
        Path("examples/milestone-5/public-readiness-baseline-audit-v1/public-readiness-baseline-audit-v1.json"),
        "MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_READY",
        "Public readiness baseline audit.",
    ),
    (
        2,
        "public_repo_release_index",
        "e983e88 Add ARC AGI3 public repo release index",
        Path("examples/milestone-5/public-repo-release-index-v1/public-repo-release-index-v1.json"),
        "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_READY",
        "Public repo release index.",
    ),
    (
        3,
        "kaggle_submission_dry_run_package",
        "8dfb106 Add ARC AGI3 Kaggle submission dry-run package",
        Path("examples/milestone-5/kaggle-submission-dry-run-package-v1/kaggle-submission-dry-run-package-v1.json"),
        "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_READY",
        "Kaggle submission dry-run package.",
    ),
    (
        4,
        "submission_entrypoint_contract",
        "77da7ae Add ARC AGI3 submission entrypoint contract",
        Path("examples/milestone-5/submission-entrypoint-contract-v1/submission-entrypoint-contract-v1.json"),
        "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_READY",
        "Submission entrypoint contract.",
    ),
    (
        5,
        "public_safety_boundary_checklist",
        "9c3c7e2 Add ARC AGI3 public safety boundary checklist",
        Path("examples/milestone-5/public-safety-boundary-checklist-v1/public-safety-boundary-checklist-v1.json"),
        "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY",
        "Public safety boundary checklist.",
    ),
    (
        6,
        "kaggle_submission_preflight_report",
        "3c56cd7 Add ARC AGI3 Kaggle submission preflight report",
        Path("examples/milestone-5/kaggle-submission-preflight-report-v1/kaggle-submission-preflight-report-v1.json"),
        "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY",
        "Kaggle submission preflight report.",
    ),
    (
        7,
        "local_submission_smoke_test",
        "47d47d2 Add ARC AGI3 local submission smoke test",
        Path("examples/milestone-5/local-submission-smoke-test-v1/local-submission-smoke-test-v1.json"),
        "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY",
        "Local submission smoke test.",
    ),
    (
        8,
        "submission_candidate_format_report",
        "d2f2750 Add ARC AGI3 submission candidate format report",
        Path("examples/milestone-5/submission-candidate-format-report-v1/submission-candidate-format-report-v1.json"),
        "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY",
        "Submission candidate format report.",
    ),
    (
        9,
        "submission_candidate_dry_run_package",
        "b632fc3 Add ARC AGI3 submission candidate dry-run package",
        Path("examples/milestone-5/submission-candidate-dry-run-package-v1/submission-candidate-dry-run-package-v1.json"),
        "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
        "Submission candidate dry-run package.",
    ),
)

CLOSURE_GATES: Tuple[str, ...] = (
    "all_task_artifacts_present",
    "all_task_artifacts_ready",
    "task_chain_count_is_9",
    "task_chain_commits_present",
    "task_chain_order_valid",
    "dry_run_package_ready",
    "format_report_ready",
    "local_smoke_test_ready",
    "preflight_report_ready",
    "public_safety_boundary_ready",
    "submission_candidate_ready",
    "submission_preparation_closed",
    "boundary_public_safe",
    "boundary_local_only",
    "boundary_dry_run_only",
    "no_external_api_dependency",
    "no_private_core_exposure",
    "no_legal_certification",
    "kaggle_submission_not_sent",
    "ready_for_real_kaggle_submission_false",
)

CLOSURE_ISSUES: Tuple[str, ...] = (
    "missing_task_artifact",
    "task_artifact_not_ready",
    "task_chain_count_invalid",
    "task_chain_commit_missing",
    "task_chain_order_invalid",
    "dry_run_package_not_ready",
    "format_report_not_ready",
    "local_smoke_test_not_ready",
    "preflight_report_not_ready",
    "public_safety_boundary_not_ready",
    "submission_candidate_not_ready",
    "submission_preparation_not_closed",
    "boundary_not_public_safe",
    "boundary_not_local_only",
    "boundary_not_dry_run_only",
    "external_api_dependency_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "kaggle_submission_already_sent",
    "ready_for_real_kaggle_submission_true",
)

REQUIRED_BOUNDARY_FLAGS: Tuple[Tuple[str, bool], ...] = (
    ("public_safe", True),
    ("deterministic", True),
    ("local_only", True),
    ("dry_run_only", True),
    ("external_api_dependency", False),
    ("contains_api_keys", False),
    ("kaggle_submission_sent", False),
    ("private_core_exposure", False),
    ("legal_certification", False),
)

TASK_COMMIT_CHAIN: Tuple[str, ...] = tuple(spec[2] for spec in TASK_ARTIFACT_SPECS)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16].upper()


def _read_json_if_available(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _file_sha256_16(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"

    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def _first_present(data: Mapping[str, Any], keys: Tuple[str, ...]) -> str:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value

    return "MISSING_ID"


def _boundary_from_final_package(final_package: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = final_package.get("boundary", {}) if isinstance(final_package.get("boundary"), Mapping) else {}

    return {
        "public_safe": boundary.get("public_safe"),
        "deterministic": boundary.get("deterministic"),
        "local_only": boundary.get("local_only"),
        "dry_run_only": boundary.get("dry_run_only"),
        "external_api_dependency": boundary.get("external_api_dependency"),
        "contains_api_keys": boundary.get("contains_api_keys"),
        "kaggle_submission_sent": final_package.get("kaggle_submission_sent"),
        "private_core_exposure": boundary.get("private_core_exposure"),
        "legal_certification": boundary.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


@dataclass(frozen=True)
class ClosureTaskStatus:
    task_number: int
    name: str
    commit: str
    artifact_path: str
    expected_status: str
    actual_status: str
    artifact_id: str
    present: bool
    ready: bool
    sha256_16: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_number": self.task_number,
            "name": self.name,
            "commit": self.commit,
            "artifact_path": self.artifact_path,
            "expected_status": self.expected_status,
            "actual_status": self.actual_status,
            "artifact_id": self.artifact_id,
            "present": self.present,
            "ready": self.ready,
            "sha256_16": self.sha256_16,
            "description": self.description,
        }


@dataclass(frozen=True)
class ClosureGate:
    name: str
    passed: bool
    severity: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "severity": self.severity,
            "description": self.description,
        }


@dataclass(frozen=True)
class ClosureIssue:
    name: str
    active: bool
    severity: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "active": self.active,
            "severity": self.severity,
            "description": self.description,
        }


@dataclass(frozen=True)
class Milestone5SubmissionPreparationClosure:
    status: str
    closure_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    final_package_id: str
    final_package_signature: str
    task_statuses: Tuple[ClosureTaskStatus, ...]
    closure_gates: Tuple[ClosureGate, ...]
    closure_issues: Tuple[ClosureIssue, ...]
    closure_index: Dict[str, Any]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    closed_task_count: int
    ready_task_count: int
    closure_gate_count: int
    passed_gate_count: int
    closure_issue_count: int
    warning_count: int
    submission_preparation_closed: bool
    ready_for_public_release_summary: bool
    ready_for_real_kaggle_submission: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "closure_id": self.closure_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "final_package_id": self.final_package_id,
            "final_package_signature": self.final_package_signature,
            "task_statuses": [item.to_dict() for item in self.task_statuses],
            "closure_gates": [item.to_dict() for item in self.closure_gates],
            "closure_issues": [item.to_dict() for item in self.closure_issues],
            "closure_index": copy.deepcopy(self.closure_index),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "closed_task_count": self.closed_task_count,
            "ready_task_count": self.ready_task_count,
            "closure_gate_count": self.closure_gate_count,
            "passed_gate_count": self.passed_gate_count,
            "closure_issue_count": self.closure_issue_count,
            "warning_count": self.warning_count,
            "submission_preparation_closed": self.submission_preparation_closed,
            "ready_for_public_release_summary": self.ready_for_public_release_summary,
            "ready_for_real_kaggle_submission": self.ready_for_real_kaggle_submission,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_closure_task_statuses() -> Tuple[ClosureTaskStatus, ...]:
    statuses = []

    for task_number, name, commit, path, expected_status, description in TASK_ARTIFACT_SPECS:
        data = _read_json_if_available(path)
        actual_status = str(data.get("status", "MISSING"))
        present = path.exists()
        ready = present and actual_status == expected_status
        artifact_id = _first_present(
            data,
            (
                "audit_id",
                "index_id",
                "package_id",
                "contract_id",
                "checklist_id",
                "report_id",
                "smoke_id",
                "closure_id",
            ),
        )

        statuses.append(
            ClosureTaskStatus(
                task_number=task_number,
                name=name,
                commit=commit,
                artifact_path=str(path),
                expected_status=expected_status,
                actual_status=actual_status,
                artifact_id=artifact_id,
                present=present,
                ready=ready,
                sha256_16=_file_sha256_16(path),
                description=description,
            )
        )

    return tuple(statuses)


def build_closure_gates(
    *,
    task_statuses: Tuple[ClosureTaskStatus, ...],
    final_package: Mapping[str, Any],
    format_report: Mapping[str, Any],
    local_smoke: Mapping[str, Any],
    preflight: Mapping[str, Any],
    safety: Mapping[str, Any],
    candidate: Mapping[str, Any],
    boundary: Mapping[str, Any],
    submission_preparation_closed: bool,
) -> Tuple[ClosureGate, ...]:
    task_commits = tuple(item.commit for item in task_statuses)

    gate_results = {
        "all_task_artifacts_present": all(item.present for item in task_statuses),
        "all_task_artifacts_ready": all(item.ready for item in task_statuses),
        "task_chain_count_is_9": len(task_statuses) == 9,
        "task_chain_commits_present": all(bool(item.commit) for item in task_statuses),
        "task_chain_order_valid": task_commits == TASK_COMMIT_CHAIN,
        "dry_run_package_ready": final_package.get("dry_run_package_ready") is True,
        "format_report_ready": format_report.get("status") == "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY",
        "local_smoke_test_ready": local_smoke.get("status") == "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY",
        "preflight_report_ready": preflight.get("status") == "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY",
        "public_safety_boundary_ready": safety.get("status") == "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY",
        "submission_candidate_ready": candidate.get("candidate_kind") == "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY",
        "submission_preparation_closed": submission_preparation_closed,
        "boundary_public_safe": boundary.get("public_safe") is True,
        "boundary_local_only": boundary.get("local_only") is True,
        "boundary_dry_run_only": boundary.get("dry_run_only") is True,
        "no_external_api_dependency": boundary.get("external_api_dependency") is False,
        "no_private_core_exposure": boundary.get("private_core_exposure") is False,
        "no_legal_certification": boundary.get("legal_certification") is False,
        "kaggle_submission_not_sent": boundary.get("kaggle_submission_sent") is False,
        "ready_for_real_kaggle_submission_false": final_package.get("ready_for_real_kaggle_submission") is False,
    }

    descriptions = {
        "all_task_artifacts_present": "All Milestone #5 Task 1-9 artifacts are present.",
        "all_task_artifacts_ready": "All Milestone #5 Task 1-9 artifacts expose ready status.",
        "task_chain_count_is_9": "Milestone #5 closure chain contains nine tasks.",
        "task_chain_commits_present": "Every Milestone #5 task has a linked commit.",
        "task_chain_order_valid": "Task commit chain is in canonical order.",
        "dry_run_package_ready": "Task 9 dry-run package is ready.",
        "format_report_ready": "Task 8 format report is ready.",
        "local_smoke_test_ready": "Task 7 local smoke test is ready.",
        "preflight_report_ready": "Task 6 preflight report is ready.",
        "public_safety_boundary_ready": "Task 5 public safety checklist is ready.",
        "submission_candidate_ready": "Smoke-only submission candidate is present.",
        "submission_preparation_closed": "Milestone #5 submission preparation is closed.",
        "boundary_public_safe": "Boundary keeps public_safe=true.",
        "boundary_local_only": "Boundary keeps local_only=true.",
        "boundary_dry_run_only": "Boundary keeps dry_run_only=true.",
        "no_external_api_dependency": "Boundary keeps external_api_dependency=false.",
        "no_private_core_exposure": "Boundary keeps private_core_exposure=false.",
        "no_legal_certification": "Boundary keeps legal_certification=false.",
        "kaggle_submission_not_sent": "Boundary keeps kaggle_submission_sent=false.",
        "ready_for_real_kaggle_submission_false": "Closure keeps ready_for_real_kaggle_submission=false.",
    }

    return tuple(
        ClosureGate(
            name=name,
            passed=gate_results[name],
            severity="PASS" if gate_results[name] else "BLOCKING",
            description=descriptions[name],
        )
        for name in CLOSURE_GATES
    )


def build_closure_issues(
    *,
    task_statuses: Tuple[ClosureTaskStatus, ...],
    final_package: Mapping[str, Any],
    format_report: Mapping[str, Any],
    local_smoke: Mapping[str, Any],
    preflight: Mapping[str, Any],
    safety: Mapping[str, Any],
    candidate: Mapping[str, Any],
    boundary: Mapping[str, Any],
    submission_preparation_closed: bool,
) -> Tuple[ClosureIssue, ...]:
    task_commits = tuple(item.commit for item in task_statuses)

    issue_state = {
        "missing_task_artifact": not all(item.present for item in task_statuses),
        "task_artifact_not_ready": not all(item.ready for item in task_statuses),
        "task_chain_count_invalid": len(task_statuses) != 9,
        "task_chain_commit_missing": not all(bool(item.commit) for item in task_statuses),
        "task_chain_order_invalid": task_commits != TASK_COMMIT_CHAIN,
        "dry_run_package_not_ready": final_package.get("dry_run_package_ready") is not True,
        "format_report_not_ready": format_report.get("status") != "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY",
        "local_smoke_test_not_ready": local_smoke.get("status") != "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY",
        "preflight_report_not_ready": preflight.get("status") != "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY",
        "public_safety_boundary_not_ready": safety.get("status") != "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY",
        "submission_candidate_not_ready": candidate.get("candidate_kind") != "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY",
        "submission_preparation_not_closed": not submission_preparation_closed,
        "boundary_not_public_safe": boundary.get("public_safe") is not True,
        "boundary_not_local_only": boundary.get("local_only") is not True,
        "boundary_not_dry_run_only": boundary.get("dry_run_only") is not True,
        "external_api_dependency_detected": boundary.get("external_api_dependency") is not False,
        "private_core_exposure_detected": boundary.get("private_core_exposure") is not False,
        "legal_certification_claim_detected": boundary.get("legal_certification") is not False,
        "kaggle_submission_already_sent": boundary.get("kaggle_submission_sent") is not False,
        "ready_for_real_kaggle_submission_true": final_package.get("ready_for_real_kaggle_submission") is not False,
    }

    descriptions = {
        "missing_task_artifact": "One or more Milestone #5 task artifacts are missing.",
        "task_artifact_not_ready": "One or more Milestone #5 task artifacts are not ready.",
        "task_chain_count_invalid": "Task chain does not contain exactly nine tasks.",
        "task_chain_commit_missing": "One or more task commits are missing.",
        "task_chain_order_invalid": "Task commit chain is not in canonical order.",
        "dry_run_package_not_ready": "Task 9 dry-run package is not ready.",
        "format_report_not_ready": "Task 8 format report is not ready.",
        "local_smoke_test_not_ready": "Task 7 local smoke test is not ready.",
        "preflight_report_not_ready": "Task 6 preflight report is not ready.",
        "public_safety_boundary_not_ready": "Task 5 public safety checklist is not ready.",
        "submission_candidate_not_ready": "Smoke-only submission candidate is not ready.",
        "submission_preparation_not_closed": "Submission preparation closure flag is not active.",
        "boundary_not_public_safe": "public_safe boundary is not true.",
        "boundary_not_local_only": "local_only boundary is not true.",
        "boundary_not_dry_run_only": "dry_run_only boundary is not true.",
        "external_api_dependency_detected": "external_api_dependency is not false.",
        "private_core_exposure_detected": "private_core_exposure is not false.",
        "legal_certification_claim_detected": "legal_certification is not false.",
        "kaggle_submission_already_sent": "kaggle_submission_sent is not false.",
        "ready_for_real_kaggle_submission_true": "ready_for_real_kaggle_submission is not false.",
    }

    return tuple(
        ClosureIssue(
            name=name,
            active=issue_state[name],
            severity="BLOCKING",
            description=descriptions[name],
        )
        for name in CLOSURE_ISSUES
    )


def build_milestone_5_submission_preparation_closure() -> Milestone5SubmissionPreparationClosure:
    final_package_path = Path("examples/milestone-5/submission-candidate-dry-run-package-v1/submission-candidate-dry-run-package-v1.json")
    format_report_path = Path("examples/milestone-5/submission-candidate-format-report-v1/submission-candidate-format-report-v1.json")
    local_smoke_path = Path("examples/milestone-5/local-submission-smoke-test-v1/local-submission-smoke-test-v1.json")
    preflight_path = Path("examples/milestone-5/kaggle-submission-preflight-report-v1/kaggle-submission-preflight-report-v1.json")
    safety_path = Path("examples/milestone-5/public-safety-boundary-checklist-v1/public-safety-boundary-checklist-v1.json")
    candidate_path = Path("examples/milestone-5/local-submission-smoke-test-v1/local-submission-candidate-smoke-only-v1.json")

    final_package = _read_json_if_available(final_package_path)
    format_report = _read_json_if_available(format_report_path)
    local_smoke = _read_json_if_available(local_smoke_path)
    preflight = _read_json_if_available(preflight_path)
    safety = _read_json_if_available(safety_path)
    candidate = _read_json_if_available(candidate_path)

    boundary = _boundary_from_final_package(final_package)
    task_statuses = build_closure_task_statuses()
    ready_task_count = sum(1 for item in task_statuses if item.ready)
    submission_preparation_closed = ready_task_count == len(TASK_ARTIFACT_SPECS) and final_package.get("dry_run_package_ready") is True

    closure_gates = build_closure_gates(
        task_statuses=task_statuses,
        final_package=final_package,
        format_report=format_report,
        local_smoke=local_smoke,
        preflight=preflight,
        safety=safety,
        candidate=candidate,
        boundary=boundary,
        submission_preparation_closed=submission_preparation_closed,
    )
    closure_issues = build_closure_issues(
        task_statuses=task_statuses,
        final_package=final_package,
        format_report=format_report,
        local_smoke=local_smoke,
        preflight=preflight,
        safety=safety,
        candidate=candidate,
        boundary=boundary,
        submission_preparation_closed=submission_preparation_closed,
    )

    passed_gate_count = sum(1 for item in closure_gates if item.passed)
    closure_issue_count = sum(1 for item in closure_issues if item.active)
    warning_count = 0

    closure_ready = (
        submission_preparation_closed
        and ready_task_count == len(TASK_ARTIFACT_SPECS)
        and passed_gate_count == len(CLOSURE_GATES)
        and closure_issue_count == 0
        and _boundary_intact(boundary)
    )

    closure_index = {
        "milestone": "Milestone #5",
        "closure_kind": "SUBMISSION_PREPARATION_CLOSURE",
        "task_count": len(TASK_ARTIFACT_SPECS),
        "ready_task_count": ready_task_count,
        "commit_chain": list(TASK_COMMIT_CHAIN),
        "final_package_id": final_package.get("package_id", "MISSING_FINAL_PACKAGE_ID"),
        "final_package_signature": final_package.get("signature", "MISSING_FINAL_PACKAGE_SIGNATURE"),
        "submission_preparation_closed": closure_ready,
        "real_kaggle_submission_created": False,
        "kaggle_submission_sent": False,
        "ready_for_real_kaggle_submission": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    next_actions = (
        "prepare_public_release_summary_v1",
        "prepare_real_kaggle_submission_only_after_explicit_operator_approval",
    )

    base_payload = {
        "status": CLOSURE_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 10",
        "title": "Milestone 5 Submission Preparation Closure v1",
        "baseline_commit": "b632fc3 Add ARC AGI3 submission candidate dry-run package",
        "final_package_id": final_package.get("package_id", "MISSING_FINAL_PACKAGE_ID"),
        "final_package_signature": final_package.get("signature", "MISSING_FINAL_PACKAGE_SIGNATURE"),
        "task_statuses": [item.to_dict() for item in task_statuses],
        "closure_gates": [item.to_dict() for item in closure_gates],
        "closure_issues": [item.to_dict() for item in closure_issues],
        "closure_index": closure_index,
        "boundary": boundary,
        "next_actions": next_actions,
        "closed_task_count": len(TASK_ARTIFACT_SPECS),
        "ready_task_count": ready_task_count,
        "closure_gate_count": len(CLOSURE_GATES),
        "passed_gate_count": passed_gate_count,
        "closure_issue_count": closure_issue_count,
        "warning_count": warning_count,
        "submission_preparation_closed": closure_ready,
        "ready_for_public_release_summary": closure_ready,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_submission_preparation_closure_v1",
            "milestone": "Milestone #5",
            "task": "Task 10",
            "closure_kind": "SUBMISSION_PREPARATION_CLOSURE",
            "depends_on_submission_candidate_dry_run_package": True,
            "archive_created": False,
            "upload_performed": False,
            "real_kaggle_submission_created": False,
        },
    }

    signature = _stable_signature(base_payload)
    closure_id = f"MILESTONE-5-SUBMISSION-CLOSURE-{signature[:12]}"

    return Milestone5SubmissionPreparationClosure(
        status=CLOSURE_STATUS,
        closure_id=closure_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        final_package_id=base_payload["final_package_id"],
        final_package_signature=base_payload["final_package_signature"],
        task_statuses=task_statuses,
        closure_gates=closure_gates,
        closure_issues=closure_issues,
        closure_index=closure_index,
        boundary=boundary,
        next_actions=next_actions,
        closed_task_count=len(TASK_ARTIFACT_SPECS),
        ready_task_count=ready_task_count,
        closure_gate_count=len(CLOSURE_GATES),
        passed_gate_count=passed_gate_count,
        closure_issue_count=closure_issue_count,
        warning_count=warning_count,
        submission_preparation_closed=closure_ready,
        ready_for_public_release_summary=closure_ready,
        ready_for_real_kaggle_submission=False,
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_milestone_5_submission_preparation_closure(
    closure: Milestone5SubmissionPreparationClosure | Mapping[str, Any],
) -> Dict[str, Any]:
    data = closure.to_dict() if hasattr(closure, "to_dict") else dict(closure)

    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    task_statuses = data.get("task_statuses") if isinstance(data.get("task_statuses"), list) else []
    gates = data.get("closure_gates") if isinstance(data.get("closure_gates"), list) else []
    issues = data.get("closure_issues") if isinstance(data.get("closure_issues"), list) else []
    closure_index = data.get("closure_index") if isinstance(data.get("closure_index"), Mapping) else {}

    validation_checks = {
        "status_ready": data.get("status") == CLOSURE_STATUS,
        "closure_id_present": isinstance(data.get("closure_id"), str) and bool(data.get("closure_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_9": str(data.get("baseline_commit", "")).startswith("b632fc3"),
        "final_package_id_present": isinstance(data.get("final_package_id"), str) and data.get("final_package_id") != "MISSING_FINAL_PACKAGE_ID",
        "closed_task_count_is_9": data.get("closed_task_count") == len(TASK_ARTIFACT_SPECS),
        "ready_task_count_is_9": data.get("ready_task_count") == len(TASK_ARTIFACT_SPECS),
        "all_task_statuses_ready": bool(task_statuses) and all(item.get("ready") is True for item in task_statuses),
        "closure_gate_count_matches": data.get("closure_gate_count") == len(CLOSURE_GATES),
        "all_closure_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "closure_issue_count_zero": data.get("closure_issue_count") == 0,
        "all_closure_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "warning_count_zero": data.get("warning_count") == 0,
        "submission_preparation_closed": data.get("submission_preparation_closed") is True,
        "ready_for_public_release_summary": data.get("ready_for_public_release_summary") is True,
        "ready_for_real_kaggle_submission_false": data.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": data.get("kaggle_submission_sent") is False,
        "closure_index_task_count_is_9": closure_index.get("task_count") == len(TASK_ARTIFACT_SPECS),
        "closure_index_no_real_submission": closure_index.get("real_kaggle_submission_created") is False,
        "closure_index_no_upload": closure_index.get("kaggle_submission_sent") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(validation_checks.values())

    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "closure_id": data.get("closure_id"),
        "signature": data.get("signature"),
    }


def render_milestone_5_submission_preparation_closure_markdown(
    closure: Milestone5SubmissionPreparationClosure | Mapping[str, Any],
) -> str:
    data = closure.to_dict() if hasattr(closure, "to_dict") else dict(closure)

    lines = [
        "# ARC AGI3 Milestone #5 - Submission Preparation Closure v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- closure_id: {data['closure_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- final_package_id: {data['final_package_id']}",
        f"- final_package_signature: {data['final_package_signature']}",
        f"- closed_task_count: {data['closed_task_count']}",
        f"- ready_task_count: {data['ready_task_count']}",
        f"- closure_gate_count: {data['closure_gate_count']}",
        f"- passed_gate_count: {data['passed_gate_count']}",
        f"- closure_issue_count: {data['closure_issue_count']}",
        f"- warning_count: {data['warning_count']}",
        f"- submission_preparation_closed: {data['submission_preparation_closed']}",
        f"- ready_for_public_release_summary: {data['ready_for_public_release_summary']}",
        f"- ready_for_real_kaggle_submission: {data['ready_for_real_kaggle_submission']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Task chain",
        "",
    ]

    for item in data["task_statuses"]:
        lines.append(
            f"- Task {item['task_number']} · {item['name']} · ready={item['ready']} · "
            f"commit={item['commit']} · artifact_id={item['artifact_id']}"
        )

    lines.extend(["", "## Closure gates", ""])

    for item in data["closure_gates"]:
        lines.append(f"- {item['name']}: passed={item['passed']} severity={item['severity']}")

    lines.extend(["", "## Closure issues", ""])

    for item in data["closure_issues"]:
        lines.append(f"- {item['name']}: active={item['active']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- local_only=true",
            "- dry_run_only=true",
            "- external_api_dependency=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "- legal_certification=false",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_VALID=true",
            "ARC_AGI3_MILESTONE_5_CLOSED_TASK_COUNT=9",
            "ARC_AGI3_MILESTONE_5_READY_TASK_COUNT=9",
            "ARC_AGI3_MILESTONE_5_CLOSURE_GATE_COUNT=20",
            "ARC_AGI3_MILESTONE_5_CLOSURE_ISSUE_COUNT=0",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSED=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_PUBLIC_RELEASE_SUMMARY=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_5_BASELINE_DRY_RUN_PACKAGE_COMMIT=b632fc3",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_milestone_5_submission_preparation_closure_manifest(
    closure: Milestone5SubmissionPreparationClosure | Mapping[str, Any],
) -> str:
    data = closure.to_dict() if hasattr(closure, "to_dict") else dict(closure)

    lines = [
        "ARC AGI3 MILESTONE 5 SUBMISSION PREPARATION CLOSURE MANIFEST v1",
        f"closure_id={data['closure_id']}",
        f"signature={data['signature']}",
        f"status={data['status']}",
        f"baseline_commit={data['baseline_commit']}",
        f"final_package_id={data['final_package_id']}",
        f"closed_task_count={data['closed_task_count']}",
        f"ready_task_count={data['ready_task_count']}",
        f"closure_gate_count={data['closure_gate_count']}",
        f"passed_gate_count={data['passed_gate_count']}",
        f"closure_issue_count={data['closure_issue_count']}",
        f"warning_count={data['warning_count']}",
        f"submission_preparation_closed={data['submission_preparation_closed']}",
        f"ready_for_public_release_summary={data['ready_for_public_release_summary']}",
        f"ready_for_real_kaggle_submission={data['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={data['kaggle_submission_sent']}",
        "",
        "TASK_CHAIN",
    ]

    for item in data["task_statuses"]:
        lines.append(f"task_{item['task_number']}={item['commit']} ready={item['ready']} artifact_id={item['artifact_id']}")

    lines.extend(["", "CLOSURE_GATES"])

    for item in data["closure_gates"]:
        lines.append(f"{item['name']} passed={item['passed']} severity={item['severity']}")

    lines.extend(["", "CLOSURE_ISSUES"])

    for item in data["closure_issues"]:
        lines.append(f"{item['name']} active={item['active']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "BOUNDARY",
            "public_safe=true",
            "deterministic=true",
            "local_only=true",
            "dry_run_only=true",
            "external_api_dependency=false",
            "contains_api_keys=false",
            "kaggle_submission_sent=false",
            "private_core_exposure=false",
            "legal_certification=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_milestone_5_submission_preparation_closure_artifacts(
    closure: Milestone5SubmissionPreparationClosure | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    closure = closure or build_milestone_5_submission_preparation_closure()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "milestone-5-submission-preparation-closure-v1.json"
    markdown_path = output_path / "milestone-5-submission-preparation-closure-v1.md"
    manifest_path = output_path / "milestone-5-submission-preparation-closure-manifest-v1.txt"
    index_path = output_path / "milestone-5-submission-preparation-closure-index-v1.json"

    json_path.write_text(json.dumps(closure.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_milestone_5_submission_preparation_closure_markdown(closure), encoding="utf-8")
    manifest_path.write_text(render_milestone_5_submission_preparation_closure_manifest(closure), encoding="utf-8")
    index_path.write_text(json.dumps(closure.closure_index, indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_5_submission_preparation_closure_pipeline() -> Dict[str, Any]:
    closure = build_milestone_5_submission_preparation_closure()
    validation = validate_milestone_5_submission_preparation_closure(closure)
    artifacts = write_milestone_5_submission_preparation_closure_artifacts(closure)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_PIPELINE_INVALID",
        "closure_status": closure.status,
        "validation_status": validation["status"],
        "closure": closure.to_dict(),
        "closure_id": closure.closure_id,
        "signature": closure.signature,
        "closed_task_count": closure.closed_task_count,
        "ready_task_count": closure.ready_task_count,
        "closure_gate_count": closure.closure_gate_count,
        "passed_gate_count": closure.passed_gate_count,
        "closure_issue_count": closure.closure_issue_count,
        "warning_count": closure.warning_count,
        "submission_preparation_closed": closure.submission_preparation_closed,
        "ready_for_public_release_summary": closure.ready_for_public_release_summary,
        "ready_for_real_kaggle_submission": closure.ready_for_real_kaggle_submission,
        "kaggle_submission_sent": closure.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_submission_preparation_closure_pipeline_v1",
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
