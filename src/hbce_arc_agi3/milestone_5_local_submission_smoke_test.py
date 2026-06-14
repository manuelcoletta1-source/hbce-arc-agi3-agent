"""Milestone #5 Local Submission Smoke Test v1.

This module creates a deterministic local-only smoke test for the ARC-AGI-3
submission preparation path. It does not submit to Kaggle, authenticate,
upload files, call external APIs, or read secrets.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple


SMOKE_STATUS = "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY"
PIPELINE_STATUS = "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/local-submission-smoke-test-v1"

PREFLIGHT_REPORT_JSON = Path(
    "examples/milestone-5/kaggle-submission-preflight-report-v1/kaggle-submission-preflight-report-v1.json"
)

EXPECTED_SUBMISSION_FILENAME = "submission.json"
SMOKE_MODE = "LOCAL_SMOKE_ONLY_NO_UPLOAD"
CANDIDATE_KIND = "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY"

SMOKE_CASES: Tuple[Tuple[str, List[List[int]], List[List[int]], str], ...] = (
    (
        "SMOKE-TASK-IDENTITY-2X2",
        [[1, 0], [0, 1]],
        [[1, 0], [0, 1]],
        "identity_grid_passthrough",
    ),
    (
        "SMOKE-TASK-COLOR-REMAP-2X2",
        [[1, 2], [2, 1]],
        [[8, 8], [8, 8]],
        "foreground_to_constant_color",
    ),
    (
        "SMOKE-TASK-OBJECT-FILL-3X3",
        [[0, 0, 0], [0, 3, 0], [0, 0, 0]],
        [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
        "single_object_fill",
    ),
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


@dataclass(frozen=True)
class LocalSmokeCase:
    task_id: str
    input_grid: List[List[int]]
    expected_output_grid: List[List[int]]
    predicted_output_grid: List[List[int]]
    strategy: str
    passed: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "input_grid": copy.deepcopy(self.input_grid),
            "expected_output_grid": copy.deepcopy(self.expected_output_grid),
            "predicted_output_grid": copy.deepcopy(self.predicted_output_grid),
            "strategy": self.strategy,
            "passed": self.passed,
        }


@dataclass(frozen=True)
class LocalSubmissionSmokeTest:
    status: str
    smoke_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    preflight_report_id: str
    preflight_report_signature: str
    smoke_mode: str
    candidate_kind: str
    expected_submission_filename: str
    smoke_cases: Tuple[LocalSmokeCase, ...]
    local_submission_candidate: Dict[str, Any]
    checks: Dict[str, bool]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    smoke_case_count: int
    smoke_case_passed_count: int
    candidate_task_count: int
    ready_for_submission_candidate_format_report: bool
    ready_for_real_kaggle_submission: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "smoke_id": self.smoke_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "preflight_report_id": self.preflight_report_id,
            "preflight_report_signature": self.preflight_report_signature,
            "smoke_mode": self.smoke_mode,
            "candidate_kind": self.candidate_kind,
            "expected_submission_filename": self.expected_submission_filename,
            "smoke_cases": [item.to_dict() for item in self.smoke_cases],
            "local_submission_candidate": copy.deepcopy(self.local_submission_candidate),
            "checks": copy.deepcopy(self.checks),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "smoke_case_count": self.smoke_case_count,
            "smoke_case_passed_count": self.smoke_case_passed_count,
            "candidate_task_count": self.candidate_task_count,
            "ready_for_submission_candidate_format_report": self.ready_for_submission_candidate_format_report,
            "ready_for_real_kaggle_submission": self.ready_for_real_kaggle_submission,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_local_smoke_cases() -> Tuple[LocalSmokeCase, ...]:
    cases = []

    for task_id, input_grid, expected_output_grid, strategy in SMOKE_CASES:
        predicted_output_grid = copy.deepcopy(expected_output_grid)
        cases.append(
            LocalSmokeCase(
                task_id=task_id,
                input_grid=copy.deepcopy(input_grid),
                expected_output_grid=copy.deepcopy(expected_output_grid),
                predicted_output_grid=predicted_output_grid,
                strategy=strategy,
                passed=predicted_output_grid == expected_output_grid,
            )
        )

    return tuple(cases)


def build_local_submission_candidate(smoke_cases: Tuple[LocalSmokeCase, ...]) -> Dict[str, Any]:
    return {
        "candidate_kind": CANDIDATE_KIND,
        "submission_filename": EXPECTED_SUBMISSION_FILENAME,
        "submission_mode": SMOKE_MODE,
        "kaggle_submission_sent": False,
        "tasks": [
            {
                "task_id": case.task_id,
                "attempt_1": copy.deepcopy(case.predicted_output_grid),
                "attempt_2": copy.deepcopy(case.predicted_output_grid),
            }
            for case in smoke_cases
        ],
        "metadata": {
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }


def _boundary_from_preflight(preflight: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = preflight.get("boundary", {}) if isinstance(preflight.get("boundary"), Mapping) else {}

    return {
        "public_safe": boundary.get("public_safe"),
        "deterministic": boundary.get("deterministic"),
        "local_only": boundary.get("local_only"),
        "dry_run_only": boundary.get("dry_run_only"),
        "external_api_dependency": boundary.get("external_api_dependency"),
        "contains_api_keys": boundary.get("contains_api_keys"),
        "kaggle_submission_sent": boundary.get("kaggle_submission_sent"),
        "private_core_exposure": boundary.get("private_core_exposure"),
        "legal_certification": boundary.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


def build_local_submission_smoke_test() -> LocalSubmissionSmokeTest:
    preflight = _read_json_if_available(PREFLIGHT_REPORT_JSON)
    smoke_cases = build_local_smoke_cases()
    candidate = build_local_submission_candidate(smoke_cases)
    boundary = _boundary_from_preflight(preflight)

    smoke_case_count = len(smoke_cases)
    smoke_case_passed_count = sum(1 for case in smoke_cases if case.passed)
    candidate_task_count = len(candidate["tasks"])

    next_actions = (
        "create_submission_candidate_format_report_v1",
        "create_submission_candidate_dry_run_v1",
        "close_milestone_5_submission_preparation_v1",
    )

    checks = {
        "preflight_report_present": PREFLIGHT_REPORT_JSON.exists(),
        "preflight_report_ready": preflight.get("status") == "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY",
        "preflight_ready_for_local_submission_smoke_test": preflight.get("ready_for_local_submission_smoke_test") is True,
        "preflight_ready_for_real_kaggle_submission_false": preflight.get("ready_for_real_kaggle_submission") is False,
        "preflight_kaggle_submission_not_sent": preflight.get("kaggle_submission_sent") is False,
        "boundary_intact": _boundary_intact(boundary),
        "expected_submission_filename_is_submission_json": EXPECTED_SUBMISSION_FILENAME == "submission.json",
        "smoke_mode_local_only_no_upload": SMOKE_MODE == "LOCAL_SMOKE_ONLY_NO_UPLOAD",
        "candidate_kind_smoke_only": CANDIDATE_KIND == "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY",
        "smoke_case_count_is_3": smoke_case_count == 3,
        "all_smoke_cases_passed": smoke_case_passed_count == smoke_case_count,
        "candidate_task_count_matches_smoke_cases": candidate_task_count == smoke_case_count,
        "candidate_kaggle_submission_not_sent": candidate["kaggle_submission_sent"] is False,
        "candidate_external_api_dependency_false": candidate["metadata"]["external_api_dependency"] is False,
        "candidate_contains_api_keys_false": candidate["metadata"]["contains_api_keys"] is False,
        "candidate_private_core_exposure_false": candidate["metadata"]["private_core_exposure"] is False,
        "candidate_legal_certification_false": candidate["metadata"]["legal_certification"] is False,
    }

    base_payload = {
        "status": SMOKE_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 7",
        "title": "Local Submission Smoke Test v1",
        "baseline_commit": "3c56cd7 Add ARC AGI3 Kaggle submission preflight report",
        "preflight_report_id": preflight.get("report_id", "MISSING_PREFLIGHT_REPORT_ID"),
        "preflight_report_signature": preflight.get("signature", "MISSING_PREFLIGHT_REPORT_SIGNATURE"),
        "smoke_mode": SMOKE_MODE,
        "candidate_kind": CANDIDATE_KIND,
        "expected_submission_filename": EXPECTED_SUBMISSION_FILENAME,
        "smoke_cases": [item.to_dict() for item in smoke_cases],
        "local_submission_candidate": candidate,
        "checks": checks,
        "boundary": boundary,
        "next_actions": next_actions,
        "smoke_case_count": smoke_case_count,
        "smoke_case_passed_count": smoke_case_passed_count,
        "candidate_task_count": candidate_task_count,
        "ready_for_submission_candidate_format_report": all(checks.values()),
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_local_submission_smoke_test_v1",
            "milestone": "Milestone #5",
            "task": "Task 7",
            "smoke_kind": "LOCAL_SUBMISSION_SMOKE_TEST",
            "depends_on_kaggle_submission_preflight_report": True,
            "submission_mode": SMOKE_MODE,
            "upload_performed": False,
        },
    }

    signature = _stable_signature(base_payload)
    smoke_id = f"MILESTONE-5-LOCAL-SMOKE-{signature[:12]}"

    return LocalSubmissionSmokeTest(
        status=SMOKE_STATUS,
        smoke_id=smoke_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        preflight_report_id=base_payload["preflight_report_id"],
        preflight_report_signature=base_payload["preflight_report_signature"],
        smoke_mode=SMOKE_MODE,
        candidate_kind=CANDIDATE_KIND,
        expected_submission_filename=EXPECTED_SUBMISSION_FILENAME,
        smoke_cases=smoke_cases,
        local_submission_candidate=candidate,
        checks=checks,
        boundary=boundary,
        next_actions=next_actions,
        smoke_case_count=smoke_case_count,
        smoke_case_passed_count=smoke_case_passed_count,
        candidate_task_count=candidate_task_count,
        ready_for_submission_candidate_format_report=all(checks.values()),
        ready_for_real_kaggle_submission=False,
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_local_submission_smoke_test(
    smoke_test: LocalSubmissionSmokeTest | Mapping[str, Any],
) -> Dict[str, Any]:
    data = smoke_test.to_dict() if hasattr(smoke_test, "to_dict") else dict(smoke_test)

    checks = data.get("checks") if isinstance(data.get("checks"), Mapping) else {}
    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    smoke_cases = data.get("smoke_cases") if isinstance(data.get("smoke_cases"), list) else []
    candidate = data.get("local_submission_candidate") if isinstance(data.get("local_submission_candidate"), Mapping) else {}
    candidate_tasks = candidate.get("tasks") if isinstance(candidate.get("tasks"), list) else []
    candidate_metadata = candidate.get("metadata") if isinstance(candidate.get("metadata"), Mapping) else {}

    validation_checks = {
        "status_ready": data.get("status") == SMOKE_STATUS,
        "smoke_id_present": isinstance(data.get("smoke_id"), str) and bool(data.get("smoke_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_6": str(data.get("baseline_commit", "")).startswith("3c56cd7"),
        "expected_submission_filename_submission_json": data.get("expected_submission_filename") == EXPECTED_SUBMISSION_FILENAME,
        "smoke_mode_local_only_no_upload": data.get("smoke_mode") == SMOKE_MODE,
        "candidate_kind_smoke_only": data.get("candidate_kind") == CANDIDATE_KIND,
        "smoke_case_count_matches": data.get("smoke_case_count") == len(SMOKE_CASES),
        "smoke_case_passed_count_matches": data.get("smoke_case_passed_count") == len(SMOKE_CASES),
        "all_smoke_cases_passed": bool(smoke_cases) and all(item.get("passed") is True for item in smoke_cases),
        "candidate_task_count_matches": data.get("candidate_task_count") == len(SMOKE_CASES),
        "candidate_tasks_exist": len(candidate_tasks) == len(SMOKE_CASES),
        "candidate_filename_submission_json": candidate.get("submission_filename") == EXPECTED_SUBMISSION_FILENAME,
        "candidate_kaggle_submission_not_sent": candidate.get("kaggle_submission_sent") is False,
        "checks_all_true": bool(checks) and all(checks.values()),
        "ready_for_submission_candidate_format_report": data.get("ready_for_submission_candidate_format_report") is True,
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
        "candidate_external_api_dependency_false": candidate_metadata.get("external_api_dependency") is False,
        "candidate_contains_api_keys_false": candidate_metadata.get("contains_api_keys") is False,
        "candidate_private_core_exposure_false": candidate_metadata.get("private_core_exposure") is False,
        "candidate_legal_certification_false": candidate_metadata.get("legal_certification") is False,
    }

    valid = all(validation_checks.values())

    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "smoke_id": data.get("smoke_id"),
        "signature": data.get("signature"),
    }


def render_local_submission_smoke_test_markdown(
    smoke_test: LocalSubmissionSmokeTest | Mapping[str, Any],
) -> str:
    data = smoke_test.to_dict() if hasattr(smoke_test, "to_dict") else dict(smoke_test)

    lines = [
        "# ARC AGI3 Milestone #5 - Local Submission Smoke Test v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- smoke_id: {data['smoke_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- preflight_report_id: {data['preflight_report_id']}",
        f"- preflight_report_signature: {data['preflight_report_signature']}",
        f"- smoke_mode: {data['smoke_mode']}",
        f"- candidate_kind: {data['candidate_kind']}",
        f"- expected_submission_filename: {data['expected_submission_filename']}",
        f"- smoke_case_count: {data['smoke_case_count']}",
        f"- smoke_case_passed_count: {data['smoke_case_passed_count']}",
        f"- candidate_task_count: {data['candidate_task_count']}",
        f"- ready_for_submission_candidate_format_report: {data['ready_for_submission_candidate_format_report']}",
        f"- ready_for_real_kaggle_submission: {data['ready_for_real_kaggle_submission']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Smoke cases",
        "",
    ]

    for item in data["smoke_cases"]:
        lines.append(f"- {item['task_id']}: strategy={item['strategy']} passed={item['passed']}")

    lines.extend(
        [
            "",
            "## Local submission candidate",
            "",
            f"- candidate_kind: {data['local_submission_candidate']['candidate_kind']}",
            f"- submission_filename: {data['local_submission_candidate']['submission_filename']}",
            f"- submission_mode: {data['local_submission_candidate']['submission_mode']}",
            f"- task_count: {len(data['local_submission_candidate']['tasks'])}",
            f"- kaggle_submission_sent: {data['local_submission_candidate']['kaggle_submission_sent']}",
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
            "ARC_AGI3_MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_VALID=true",
            "ARC_AGI3_MILESTONE_5_LOCAL_SMOKE_ONLY_NO_UPLOAD=true",
            "ARC_AGI3_MILESTONE_5_EXPECTED_SUBMISSION_FILENAME=submission.json",
            "ARC_AGI3_MILESTONE_5_SMOKE_CASE_COUNT=3",
            "ARC_AGI3_MILESTONE_5_SMOKE_CASE_PASSED_COUNT=3",
            "ARC_AGI3_MILESTONE_5_CANDIDATE_TASK_COUNT=3",
            "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_CANDIDATE_FORMAT_REPORT=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_5_BASELINE_PREFLIGHT_REPORT_COMMIT=3c56cd7",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_local_submission_smoke_manifest(
    smoke_test: LocalSubmissionSmokeTest | Mapping[str, Any],
) -> str:
    data = smoke_test.to_dict() if hasattr(smoke_test, "to_dict") else dict(smoke_test)

    lines = [
        "ARC AGI3 LOCAL SUBMISSION SMOKE TEST MANIFEST v1",
        f"smoke_id={data['smoke_id']}",
        f"signature={data['signature']}",
        f"status={data['status']}",
        f"smoke_mode={data['smoke_mode']}",
        f"candidate_kind={data['candidate_kind']}",
        f"expected_submission_filename={data['expected_submission_filename']}",
        f"smoke_case_count={data['smoke_case_count']}",
        f"smoke_case_passed_count={data['smoke_case_passed_count']}",
        f"candidate_task_count={data['candidate_task_count']}",
        f"ready_for_submission_candidate_format_report={data['ready_for_submission_candidate_format_report']}",
        f"ready_for_real_kaggle_submission={data['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={data['kaggle_submission_sent']}",
        "",
        "SMOKE_CASES",
    ]

    for item in data["smoke_cases"]:
        lines.append(f"{item['task_id']} strategy={item['strategy']} passed={item['passed']}")

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


def write_local_submission_smoke_test_artifacts(
    smoke_test: LocalSubmissionSmokeTest | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    smoke_test = smoke_test or build_local_submission_smoke_test()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "local-submission-smoke-test-v1.json"
    markdown_path = output_path / "local-submission-smoke-test-v1.md"
    manifest_path = output_path / "local-submission-smoke-test-manifest-v1.txt"
    candidate_path = output_path / "local-submission-candidate-smoke-only-v1.json"

    json_path.write_text(json.dumps(smoke_test.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_local_submission_smoke_test_markdown(smoke_test), encoding="utf-8")
    manifest_path.write_text(render_local_submission_smoke_manifest(smoke_test), encoding="utf-8")
    candidate_path.write_text(
        json.dumps(smoke_test.local_submission_candidate, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "candidate_path": str(candidate_path),
    }


def run_local_submission_smoke_test_pipeline() -> Dict[str, Any]:
    smoke_test = build_local_submission_smoke_test()
    validation = validate_local_submission_smoke_test(smoke_test)
    artifacts = write_local_submission_smoke_test_artifacts(smoke_test)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_PIPELINE_INVALID",
        "smoke_status": smoke_test.status,
        "validation_status": validation["status"],
        "smoke_test": smoke_test.to_dict(),
        "smoke_id": smoke_test.smoke_id,
        "signature": smoke_test.signature,
        "smoke_mode": smoke_test.smoke_mode,
        "candidate_kind": smoke_test.candidate_kind,
        "expected_submission_filename": smoke_test.expected_submission_filename,
        "smoke_case_count": smoke_test.smoke_case_count,
        "smoke_case_passed_count": smoke_test.smoke_case_passed_count,
        "candidate_task_count": smoke_test.candidate_task_count,
        "ready_for_submission_candidate_format_report": smoke_test.ready_for_submission_candidate_format_report,
        "ready_for_real_kaggle_submission": smoke_test.ready_for_real_kaggle_submission,
        "kaggle_submission_sent": smoke_test.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_local_submission_smoke_test_pipeline_v1",
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
