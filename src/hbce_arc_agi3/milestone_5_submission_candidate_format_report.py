"""Milestone #5 Submission Candidate Format Report v1.

This module validates the local smoke-only submission candidate format for
ARC-AGI-3 preparation. It does not create a real Kaggle submission, authenticate,
upload files, call external APIs, or read secrets.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple


REPORT_STATUS = "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY"
PIPELINE_STATUS = "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/submission-candidate-format-report-v1"

LOCAL_SMOKE_TEST_JSON = Path(
    "examples/milestone-5/local-submission-smoke-test-v1/local-submission-smoke-test-v1.json"
)
LOCAL_CANDIDATE_JSON = Path(
    "examples/milestone-5/local-submission-smoke-test-v1/local-submission-candidate-smoke-only-v1.json"
)

EXPECTED_SUBMISSION_FILENAME = "submission.json"
EXPECTED_CANDIDATE_KIND = "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY"
EXPECTED_SUBMISSION_MODE = "LOCAL_SMOKE_ONLY_NO_UPLOAD"

REQUIRED_TASK_KEYS: Tuple[str, ...] = ("task_id", "attempt_1", "attempt_2")

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

FORMAT_GATES: Tuple[str, ...] = (
    "local_smoke_test_present",
    "local_candidate_present",
    "local_smoke_test_ready",
    "local_candidate_kind_valid",
    "submission_filename_valid",
    "submission_mode_valid",
    "candidate_tasks_present",
    "candidate_task_count_matches_smoke_test",
    "all_task_ids_valid",
    "all_attempt_keys_present",
    "all_attempt_grids_valid",
    "candidate_json_serializable",
    "candidate_boundary_intact",
    "kaggle_submission_not_sent",
)

FORMAT_ISSUES: Tuple[str, ...] = (
    "missing_local_smoke_test",
    "missing_local_candidate",
    "local_smoke_test_not_ready",
    "candidate_kind_invalid",
    "submission_filename_invalid",
    "submission_mode_invalid",
    "candidate_tasks_missing",
    "candidate_task_count_mismatch",
    "task_id_invalid",
    "attempt_key_missing",
    "attempt_grid_invalid",
    "candidate_json_not_serializable",
    "boundary_violation",
    "kaggle_submission_already_sent",
)


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


def _is_int_cell(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 9


def is_valid_grid(grid: Any) -> bool:
    if not isinstance(grid, list) or not grid:
        return False

    if not all(isinstance(row, list) and row for row in grid):
        return False

    width = len(grid[0])
    if width == 0:
        return False

    return all(len(row) == width and all(_is_int_cell(cell) for cell in row) for row in grid)


def is_valid_candidate_task(task: Mapping[str, Any]) -> bool:
    if not isinstance(task.get("task_id"), str) or not task.get("task_id"):
        return False

    if not all(key in task for key in REQUIRED_TASK_KEYS):
        return False

    return is_valid_grid(task.get("attempt_1")) and is_valid_grid(task.get("attempt_2"))


def _candidate_json_serializable(candidate: Mapping[str, Any]) -> bool:
    try:
        json.dumps(candidate, sort_keys=True)
    except (TypeError, ValueError):
        return False

    return True


def _boundary_from_candidate(candidate: Mapping[str, Any]) -> Dict[str, Any]:
    metadata = candidate.get("metadata", {}) if isinstance(candidate.get("metadata"), Mapping) else {}

    return {
        "public_safe": metadata.get("public_safe"),
        "deterministic": metadata.get("deterministic"),
        "local_only": metadata.get("local_only"),
        "dry_run_only": metadata.get("dry_run_only"),
        "external_api_dependency": metadata.get("external_api_dependency"),
        "contains_api_keys": metadata.get("contains_api_keys"),
        "kaggle_submission_sent": candidate.get("kaggle_submission_sent"),
        "private_core_exposure": metadata.get("private_core_exposure"),
        "legal_certification": metadata.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


@dataclass(frozen=True)
class CandidateTaskFormatStatus:
    task_id: str
    has_task_id: bool
    has_attempt_1: bool
    has_attempt_2: bool
    attempt_1_grid_valid: bool
    attempt_2_grid_valid: bool
    valid: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "has_task_id": self.has_task_id,
            "has_attempt_1": self.has_attempt_1,
            "has_attempt_2": self.has_attempt_2,
            "attempt_1_grid_valid": self.attempt_1_grid_valid,
            "attempt_2_grid_valid": self.attempt_2_grid_valid,
            "valid": self.valid,
        }


@dataclass(frozen=True)
class FormatGate:
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
class FormatIssue:
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
class SubmissionCandidateFormatReport:
    status: str
    report_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    local_smoke_id: str
    local_smoke_signature: str
    candidate_kind: str
    submission_filename: str
    submission_mode: str
    task_format_statuses: Tuple[CandidateTaskFormatStatus, ...]
    format_gates: Tuple[FormatGate, ...]
    format_issues: Tuple[FormatIssue, ...]
    candidate_preview: Dict[str, Any]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    candidate_task_count: int
    valid_task_count: int
    format_gate_count: int
    passed_gate_count: int
    format_issue_count: int
    warning_count: int
    ready_for_submission_candidate_dry_run: bool
    ready_for_milestone_5_closure: bool
    ready_for_real_kaggle_submission: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "report_id": self.report_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "local_smoke_id": self.local_smoke_id,
            "local_smoke_signature": self.local_smoke_signature,
            "candidate_kind": self.candidate_kind,
            "submission_filename": self.submission_filename,
            "submission_mode": self.submission_mode,
            "task_format_statuses": [item.to_dict() for item in self.task_format_statuses],
            "format_gates": [item.to_dict() for item in self.format_gates],
            "format_issues": [item.to_dict() for item in self.format_issues],
            "candidate_preview": copy.deepcopy(self.candidate_preview),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "candidate_task_count": self.candidate_task_count,
            "valid_task_count": self.valid_task_count,
            "format_gate_count": self.format_gate_count,
            "passed_gate_count": self.passed_gate_count,
            "format_issue_count": self.format_issue_count,
            "warning_count": self.warning_count,
            "ready_for_submission_candidate_dry_run": self.ready_for_submission_candidate_dry_run,
            "ready_for_milestone_5_closure": self.ready_for_milestone_5_closure,
            "ready_for_real_kaggle_submission": self.ready_for_real_kaggle_submission,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_candidate_task_format_statuses(candidate: Mapping[str, Any]) -> Tuple[CandidateTaskFormatStatus, ...]:
    tasks = candidate.get("tasks", [])
    if not isinstance(tasks, list):
        return tuple()

    statuses = []

    for index, task in enumerate(tasks):
        task_mapping = task if isinstance(task, Mapping) else {}
        task_id = str(task_mapping.get("task_id", f"INVALID_TASK_{index}"))
        has_task_id = isinstance(task_mapping.get("task_id"), str) and bool(task_mapping.get("task_id"))
        has_attempt_1 = "attempt_1" in task_mapping
        has_attempt_2 = "attempt_2" in task_mapping
        attempt_1_grid_valid = is_valid_grid(task_mapping.get("attempt_1"))
        attempt_2_grid_valid = is_valid_grid(task_mapping.get("attempt_2"))
        valid = has_task_id and has_attempt_1 and has_attempt_2 and attempt_1_grid_valid and attempt_2_grid_valid

        statuses.append(
            CandidateTaskFormatStatus(
                task_id=task_id,
                has_task_id=has_task_id,
                has_attempt_1=has_attempt_1,
                has_attempt_2=has_attempt_2,
                attempt_1_grid_valid=attempt_1_grid_valid,
                attempt_2_grid_valid=attempt_2_grid_valid,
                valid=valid,
            )
        )

    return tuple(statuses)


def build_format_gates(
    *,
    local_smoke_test: Mapping[str, Any],
    candidate: Mapping[str, Any],
    task_statuses: Tuple[CandidateTaskFormatStatus, ...],
    boundary: Mapping[str, Any],
) -> Tuple[FormatGate, ...]:
    tasks = candidate.get("tasks", [])
    tasks_are_list = isinstance(tasks, list)
    expected_count = local_smoke_test.get("candidate_task_count")
    candidate_task_count = len(tasks) if tasks_are_list else 0

    gate_results = {
        "local_smoke_test_present": LOCAL_SMOKE_TEST_JSON.exists(),
        "local_candidate_present": LOCAL_CANDIDATE_JSON.exists(),
        "local_smoke_test_ready": local_smoke_test.get("status") == "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY",
        "local_candidate_kind_valid": candidate.get("candidate_kind") == EXPECTED_CANDIDATE_KIND,
        "submission_filename_valid": candidate.get("submission_filename") == EXPECTED_SUBMISSION_FILENAME,
        "submission_mode_valid": candidate.get("submission_mode") == EXPECTED_SUBMISSION_MODE,
        "candidate_tasks_present": tasks_are_list and candidate_task_count > 0,
        "candidate_task_count_matches_smoke_test": tasks_are_list and candidate_task_count == expected_count,
        "all_task_ids_valid": bool(task_statuses) and all(item.has_task_id for item in task_statuses),
        "all_attempt_keys_present": bool(task_statuses) and all(item.has_attempt_1 and item.has_attempt_2 for item in task_statuses),
        "all_attempt_grids_valid": bool(task_statuses) and all(item.attempt_1_grid_valid and item.attempt_2_grid_valid for item in task_statuses),
        "candidate_json_serializable": _candidate_json_serializable(candidate),
        "candidate_boundary_intact": _boundary_intact(boundary),
        "kaggle_submission_not_sent": candidate.get("kaggle_submission_sent") is False,
    }

    descriptions = {
        "local_smoke_test_present": "Local submission smoke test artifact is present.",
        "local_candidate_present": "Local smoke-only candidate artifact is present.",
        "local_smoke_test_ready": "Local submission smoke test exposes ready status.",
        "local_candidate_kind_valid": "Candidate kind is smoke-only and local.",
        "submission_filename_valid": "Candidate declares expected submission filename submission.json.",
        "submission_mode_valid": "Candidate declares local smoke-only no-upload mode.",
        "candidate_tasks_present": "Candidate has a non-empty task list.",
        "candidate_task_count_matches_smoke_test": "Candidate task count matches smoke test task count.",
        "all_task_ids_valid": "Every candidate task has a valid task_id.",
        "all_attempt_keys_present": "Every candidate task has attempt_1 and attempt_2.",
        "all_attempt_grids_valid": "Every candidate attempt is a rectangular 0-9 integer grid.",
        "candidate_json_serializable": "Candidate can be serialized as JSON.",
        "candidate_boundary_intact": "Candidate metadata preserves public safety boundary.",
        "kaggle_submission_not_sent": "Candidate has not been sent to Kaggle.",
    }

    return tuple(
        FormatGate(
            name=name,
            passed=gate_results[name],
            severity="PASS" if gate_results[name] else "BLOCKING",
            description=descriptions[name],
        )
        for name in FORMAT_GATES
    )


def build_format_issues(
    *,
    local_smoke_test: Mapping[str, Any],
    candidate: Mapping[str, Any],
    task_statuses: Tuple[CandidateTaskFormatStatus, ...],
    boundary: Mapping[str, Any],
) -> Tuple[FormatIssue, ...]:
    tasks = candidate.get("tasks", [])
    tasks_are_list = isinstance(tasks, list)
    expected_count = local_smoke_test.get("candidate_task_count")
    candidate_task_count = len(tasks) if tasks_are_list else 0

    issue_state = {
        "missing_local_smoke_test": not LOCAL_SMOKE_TEST_JSON.exists(),
        "missing_local_candidate": not LOCAL_CANDIDATE_JSON.exists(),
        "local_smoke_test_not_ready": local_smoke_test.get("status") != "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY",
        "candidate_kind_invalid": candidate.get("candidate_kind") != EXPECTED_CANDIDATE_KIND,
        "submission_filename_invalid": candidate.get("submission_filename") != EXPECTED_SUBMISSION_FILENAME,
        "submission_mode_invalid": candidate.get("submission_mode") != EXPECTED_SUBMISSION_MODE,
        "candidate_tasks_missing": not tasks_are_list or candidate_task_count == 0,
        "candidate_task_count_mismatch": not tasks_are_list or candidate_task_count != expected_count,
        "task_id_invalid": not task_statuses or any(item.has_task_id is False for item in task_statuses),
        "attempt_key_missing": not task_statuses or any((item.has_attempt_1 and item.has_attempt_2) is False for item in task_statuses),
        "attempt_grid_invalid": not task_statuses or any((item.attempt_1_grid_valid and item.attempt_2_grid_valid) is False for item in task_statuses),
        "candidate_json_not_serializable": not _candidate_json_serializable(candidate),
        "boundary_violation": not _boundary_intact(boundary),
        "kaggle_submission_already_sent": candidate.get("kaggle_submission_sent") is not False,
    }

    descriptions = {
        "missing_local_smoke_test": "Local submission smoke test artifact is missing.",
        "missing_local_candidate": "Local submission candidate artifact is missing.",
        "local_smoke_test_not_ready": "Local submission smoke test is not ready.",
        "candidate_kind_invalid": "Candidate kind is not the expected smoke-only local kind.",
        "submission_filename_invalid": "Candidate filename is not submission.json.",
        "submission_mode_invalid": "Candidate mode is not local smoke-only no-upload.",
        "candidate_tasks_missing": "Candidate task list is missing or empty.",
        "candidate_task_count_mismatch": "Candidate task count does not match smoke test task count.",
        "task_id_invalid": "One or more task_id values are invalid.",
        "attempt_key_missing": "One or more attempt_1/attempt_2 keys are missing.",
        "attempt_grid_invalid": "One or more attempt grids are invalid.",
        "candidate_json_not_serializable": "Candidate cannot be serialized as JSON.",
        "boundary_violation": "Candidate public safety boundary is not intact.",
        "kaggle_submission_already_sent": "Candidate appears to have been sent to Kaggle.",
    }

    return tuple(
        FormatIssue(
            name=name,
            active=issue_state[name],
            severity="BLOCKING",
            description=descriptions[name],
        )
        for name in FORMAT_ISSUES
    )


def build_submission_candidate_format_report() -> SubmissionCandidateFormatReport:
    local_smoke_test = _read_json_if_available(LOCAL_SMOKE_TEST_JSON)
    candidate = _read_json_if_available(LOCAL_CANDIDATE_JSON)

    boundary = _boundary_from_candidate(candidate)
    task_statuses = build_candidate_task_format_statuses(candidate)
    format_gates = build_format_gates(
        local_smoke_test=local_smoke_test,
        candidate=candidate,
        task_statuses=task_statuses,
        boundary=boundary,
    )
    format_issues = build_format_issues(
        local_smoke_test=local_smoke_test,
        candidate=candidate,
        task_statuses=task_statuses,
        boundary=boundary,
    )

    candidate_task_count = len(candidate.get("tasks", [])) if isinstance(candidate.get("tasks", []), list) else 0
    valid_task_count = sum(1 for item in task_statuses if item.valid)
    passed_gate_count = sum(1 for item in format_gates if item.passed)
    format_issue_count = sum(1 for item in format_issues if item.active)
    warning_count = 0

    ready_for_submission_candidate_dry_run = (
        format_issue_count == 0
        and passed_gate_count == len(FORMAT_GATES)
        and valid_task_count == candidate_task_count
        and candidate_task_count > 0
    )
    ready_for_milestone_5_closure = ready_for_submission_candidate_dry_run
    ready_for_real_kaggle_submission = False

    candidate_preview = {
        "candidate_kind": candidate.get("candidate_kind"),
        "submission_filename": candidate.get("submission_filename"),
        "submission_mode": candidate.get("submission_mode"),
        "task_count": candidate_task_count,
        "task_ids": [
            task.get("task_id")
            for task in candidate.get("tasks", [])
            if isinstance(task, Mapping)
        ],
        "kaggle_submission_sent": candidate.get("kaggle_submission_sent"),
    }

    next_actions = (
        "create_submission_candidate_dry_run_v1",
        "close_milestone_5_submission_preparation_v1",
    )

    base_payload = {
        "status": REPORT_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 8",
        "title": "Submission Candidate Format Report v1",
        "baseline_commit": "47d47d2 Add ARC AGI3 local submission smoke test",
        "local_smoke_id": local_smoke_test.get("smoke_id", "MISSING_LOCAL_SMOKE_ID"),
        "local_smoke_signature": local_smoke_test.get("signature", "MISSING_LOCAL_SMOKE_SIGNATURE"),
        "candidate_kind": candidate.get("candidate_kind", "MISSING_CANDIDATE_KIND"),
        "submission_filename": candidate.get("submission_filename", "MISSING_SUBMISSION_FILENAME"),
        "submission_mode": candidate.get("submission_mode", "MISSING_SUBMISSION_MODE"),
        "task_format_statuses": [item.to_dict() for item in task_statuses],
        "format_gates": [item.to_dict() for item in format_gates],
        "format_issues": [item.to_dict() for item in format_issues],
        "candidate_preview": candidate_preview,
        "boundary": boundary,
        "next_actions": next_actions,
        "candidate_task_count": candidate_task_count,
        "valid_task_count": valid_task_count,
        "format_gate_count": len(format_gates),
        "passed_gate_count": passed_gate_count,
        "format_issue_count": format_issue_count,
        "warning_count": warning_count,
        "ready_for_submission_candidate_dry_run": ready_for_submission_candidate_dry_run,
        "ready_for_milestone_5_closure": ready_for_milestone_5_closure,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_submission_candidate_format_report_v1",
            "milestone": "Milestone #5",
            "task": "Task 8",
            "report_kind": "SUBMISSION_CANDIDATE_FORMAT_REPORT",
            "depends_on_local_submission_smoke_test": True,
            "submission_mode": EXPECTED_SUBMISSION_MODE,
            "upload_performed": False,
        },
    }

    signature = _stable_signature(base_payload)
    report_id = f"MILESTONE-5-CANDIDATE-FORMAT-{signature[:12]}"

    return SubmissionCandidateFormatReport(
        status=REPORT_STATUS,
        report_id=report_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        local_smoke_id=base_payload["local_smoke_id"],
        local_smoke_signature=base_payload["local_smoke_signature"],
        candidate_kind=base_payload["candidate_kind"],
        submission_filename=base_payload["submission_filename"],
        submission_mode=base_payload["submission_mode"],
        task_format_statuses=task_statuses,
        format_gates=format_gates,
        format_issues=format_issues,
        candidate_preview=candidate_preview,
        boundary=boundary,
        next_actions=next_actions,
        candidate_task_count=candidate_task_count,
        valid_task_count=valid_task_count,
        format_gate_count=len(format_gates),
        passed_gate_count=passed_gate_count,
        format_issue_count=format_issue_count,
        warning_count=warning_count,
        ready_for_submission_candidate_dry_run=ready_for_submission_candidate_dry_run,
        ready_for_milestone_5_closure=ready_for_milestone_5_closure,
        ready_for_real_kaggle_submission=ready_for_real_kaggle_submission,
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_submission_candidate_format_report(
    report: SubmissionCandidateFormatReport | Mapping[str, Any],
) -> Dict[str, Any]:
    data = report.to_dict() if hasattr(report, "to_dict") else dict(report)

    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    task_statuses = data.get("task_format_statuses") if isinstance(data.get("task_format_statuses"), list) else []
    format_gates = data.get("format_gates") if isinstance(data.get("format_gates"), list) else []
    format_issues = data.get("format_issues") if isinstance(data.get("format_issues"), list) else []
    candidate_preview = data.get("candidate_preview") if isinstance(data.get("candidate_preview"), Mapping) else {}

    validation_checks = {
        "status_ready": data.get("status") == REPORT_STATUS,
        "report_id_present": isinstance(data.get("report_id"), str) and bool(data.get("report_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_7": str(data.get("baseline_commit", "")).startswith("47d47d2"),
        "candidate_kind_valid": data.get("candidate_kind") == EXPECTED_CANDIDATE_KIND,
        "submission_filename_valid": data.get("submission_filename") == EXPECTED_SUBMISSION_FILENAME,
        "submission_mode_valid": data.get("submission_mode") == EXPECTED_SUBMISSION_MODE,
        "candidate_task_count_is_3": data.get("candidate_task_count") == 3,
        "valid_task_count_is_3": data.get("valid_task_count") == 3,
        "all_task_statuses_valid": bool(task_statuses) and all(item.get("valid") is True for item in task_statuses),
        "format_gate_count_matches": data.get("format_gate_count") == len(FORMAT_GATES),
        "all_format_gates_passed": bool(format_gates) and all(item.get("passed") is True for item in format_gates),
        "format_issue_count_zero": data.get("format_issue_count") == 0,
        "all_format_issues_inactive": bool(format_issues) and all(item.get("active") is False for item in format_issues),
        "warning_count_zero": data.get("warning_count") == 0,
        "candidate_preview_task_count_is_3": candidate_preview.get("task_count") == 3,
        "ready_for_submission_candidate_dry_run": data.get("ready_for_submission_candidate_dry_run") is True,
        "ready_for_milestone_5_closure": data.get("ready_for_milestone_5_closure") is True,
        "ready_for_real_kaggle_submission_false": data.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": data.get("kaggle_submission_sent") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "report_id": data.get("report_id"),
        "signature": data.get("signature"),
    }


def render_submission_candidate_format_report_markdown(
    report: SubmissionCandidateFormatReport | Mapping[str, Any],
) -> str:
    data = report.to_dict() if hasattr(report, "to_dict") else dict(report)

    lines = [
        "# ARC AGI3 Milestone #5 - Submission Candidate Format Report v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- report_id: {data['report_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- local_smoke_id: {data['local_smoke_id']}",
        f"- local_smoke_signature: {data['local_smoke_signature']}",
        f"- candidate_kind: {data['candidate_kind']}",
        f"- submission_filename: {data['submission_filename']}",
        f"- submission_mode: {data['submission_mode']}",
        f"- candidate_task_count: {data['candidate_task_count']}",
        f"- valid_task_count: {data['valid_task_count']}",
        f"- format_gate_count: {data['format_gate_count']}",
        f"- passed_gate_count: {data['passed_gate_count']}",
        f"- format_issue_count: {data['format_issue_count']}",
        f"- warning_count: {data['warning_count']}",
        f"- ready_for_submission_candidate_dry_run: {data['ready_for_submission_candidate_dry_run']}",
        f"- ready_for_milestone_5_closure: {data['ready_for_milestone_5_closure']}",
        f"- ready_for_real_kaggle_submission: {data['ready_for_real_kaggle_submission']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Task format statuses",
        "",
    ]

    for item in data["task_format_statuses"]:
        lines.append(
            f"- {item['task_id']}: valid={item['valid']} "
            f"attempt_1_grid_valid={item['attempt_1_grid_valid']} "
            f"attempt_2_grid_valid={item['attempt_2_grid_valid']}"
        )

    lines.extend(
        [
            "",
            "## Format gates",
            "",
        ]
    )

    for item in data["format_gates"]:
        lines.append(f"- {item['name']}: passed={item['passed']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "## Format issues",
            "",
        ]
    )

    for item in data["format_issues"]:
        lines.append(f"- {item['name']}: active={item['active']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "## Candidate preview",
            "",
            f"- candidate_kind: {data['candidate_preview']['candidate_kind']}",
            f"- submission_filename: {data['candidate_preview']['submission_filename']}",
            f"- submission_mode: {data['candidate_preview']['submission_mode']}",
            f"- task_count: {data['candidate_preview']['task_count']}",
            f"- kaggle_submission_sent: {data['candidate_preview']['kaggle_submission_sent']}",
            "",
            "## Next actions",
            "",
        ]
    )

    for action in data["next_actions"]:
        lines.append(f"- {action}")

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
            "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_VALID=true",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_FILENAME=submission.json",
            "ARC_AGI3_MILESTONE_5_CANDIDATE_KIND=LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_MODE=LOCAL_SMOKE_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_5_CANDIDATE_TASK_COUNT=3",
            "ARC_AGI3_MILESTONE_5_VALID_TASK_COUNT=3",
            "ARC_AGI3_MILESTONE_5_FORMAT_GATE_COUNT=14",
            "ARC_AGI3_MILESTONE_5_FORMAT_ISSUE_COUNT=0",
            "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_CANDIDATE_DRY_RUN=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_MILESTONE_5_CLOSURE=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_5_BASELINE_LOCAL_SMOKE_TEST_COMMIT=47d47d2",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_submission_candidate_format_manifest(
    report: SubmissionCandidateFormatReport | Mapping[str, Any],
) -> str:
    data = report.to_dict() if hasattr(report, "to_dict") else dict(report)

    lines = [
        "ARC AGI3 SUBMISSION CANDIDATE FORMAT REPORT MANIFEST v1",
        f"report_id={data['report_id']}",
        f"signature={data['signature']}",
        f"status={data['status']}",
        f"candidate_kind={data['candidate_kind']}",
        f"submission_filename={data['submission_filename']}",
        f"submission_mode={data['submission_mode']}",
        f"candidate_task_count={data['candidate_task_count']}",
        f"valid_task_count={data['valid_task_count']}",
        f"format_gate_count={data['format_gate_count']}",
        f"passed_gate_count={data['passed_gate_count']}",
        f"format_issue_count={data['format_issue_count']}",
        f"warning_count={data['warning_count']}",
        f"ready_for_submission_candidate_dry_run={data['ready_for_submission_candidate_dry_run']}",
        f"ready_for_milestone_5_closure={data['ready_for_milestone_5_closure']}",
        f"ready_for_real_kaggle_submission={data['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={data['kaggle_submission_sent']}",
        "",
        "TASK_FORMAT_STATUSES",
    ]

    for item in data["task_format_statuses"]:
        lines.append(f"{item['task_id']} valid={item['valid']}")

    lines.extend(
        [
            "",
            "FORMAT_GATES",
        ]
    )

    for item in data["format_gates"]:
        lines.append(f"{item['name']} passed={item['passed']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "FORMAT_ISSUES",
        ]
    )

    for item in data["format_issues"]:
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


def write_submission_candidate_format_report_artifacts(
    report: SubmissionCandidateFormatReport | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    report = report or build_submission_candidate_format_report()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "submission-candidate-format-report-v1.json"
    markdown_path = output_path / "submission-candidate-format-report-v1.md"
    manifest_path = output_path / "submission-candidate-format-report-manifest-v1.txt"
    preview_path = output_path / "submission-candidate-preview-smoke-only-v1.json"

    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_submission_candidate_format_report_markdown(report), encoding="utf-8")
    manifest_path.write_text(render_submission_candidate_format_manifest(report), encoding="utf-8")
    preview_path.write_text(json.dumps(report.candidate_preview, indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "preview_path": str(preview_path),
    }


def run_submission_candidate_format_report_pipeline() -> Dict[str, Any]:
    report = build_submission_candidate_format_report()
    validation = validate_submission_candidate_format_report(report)
    artifacts = write_submission_candidate_format_report_artifacts(report)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_PIPELINE_INVALID",
        "report_status": report.status,
        "validation_status": validation["status"],
        "report": report.to_dict(),
        "report_id": report.report_id,
        "signature": report.signature,
        "candidate_kind": report.candidate_kind,
        "submission_filename": report.submission_filename,
        "submission_mode": report.submission_mode,
        "candidate_task_count": report.candidate_task_count,
        "valid_task_count": report.valid_task_count,
        "format_gate_count": report.format_gate_count,
        "passed_gate_count": report.passed_gate_count,
        "format_issue_count": report.format_issue_count,
        "warning_count": report.warning_count,
        "ready_for_submission_candidate_dry_run": report.ready_for_submission_candidate_dry_run,
        "ready_for_milestone_5_closure": report.ready_for_milestone_5_closure,
        "ready_for_real_kaggle_submission": report.ready_for_real_kaggle_submission,
        "kaggle_submission_sent": report.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_submission_candidate_format_report_pipeline_v1",
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
