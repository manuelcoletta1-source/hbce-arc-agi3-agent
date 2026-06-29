"""Milestone 33 Task 5 regression integration for ARC-AGI-3 trace boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TASK_ID = "MILESTONE_33_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_REGRESSION_INTEGRATION_V1"
SOURCE_VALIDATION_TASK_ID = "MILESTONE_33_TASK_4_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_VALIDATION_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
SCOPE_LOCK_ID = "MILESTONE_33_SCOPE_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
RUNTIME_MODE_ID = "ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
REGRESSION_INTEGRATION_REVISION = "MILESTONE_33_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_REGRESSION_INTEGRATION_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 5
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = (
    "MILESTONE_33_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_"
    "BOUNDARY_FINAL_CLOSURE_V1"
)

ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs" / "milestone-33-task-5-hbce-arc-agi3-interactive-runtime-planning-trace-boundary-regression-integration-v1.md"
SOURCE_VALIDATION_DOC_PATH = ROOT / "docs" / "milestone-33-task-4-hbce-arc-agi3-interactive-runtime-planning-trace-boundary-validation-v1.md"
ARTIFACT_DIR = ROOT / "examples" / "milestone-33" / "hbce-arc-agi3-interactive-runtime-planning-trace-boundary-regression-integration-v1"


def _digest(*parts: Any, length: int = 16) -> str:
    raw = "|".join(str(part) for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:length].upper()


TASK_5_SIGNATURE = _digest(TASK_ID, SELECTED_OBJECTIVE_ID, REGRESSION_INTEGRATION_REVISION)
INTEGRATION_ID = "MILESTONE-33-ARC-AGI3-INTERACTIVE-RUNTIME-INTEGRATION-" + _digest(
    SCOPE_LOCK_ID,
    RUNTIME_MODE_ID,
)
INTEGRATION_SIGNATURE = _digest(INTEGRATION_ID, TASK_5_SIGNATURE, NEXT_STAGE)


def _bool_marker(value: bool) -> str:
    return "true" if value else "false"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _validation_report() -> dict[str, Any]:
    from hbce_arc_agi3.milestone_33_arc_agi3_interactive_runtime_planning_trace_boundary_validation import (
        run_milestone_33_boundary_validation,
        validate_milestone_33_boundary_validation_report,
    )

    report = run_milestone_33_boundary_validation()
    report["_validation_report_valid"] = validate_milestone_33_boundary_validation_report(report)
    return report


def _sample_episode_from_validation(validation: dict[str, Any]) -> dict[str, Any]:
    implementation = validation.get("source_implementation_report", {})
    return implementation.get("sample_episode", {})


def _event_trace_fingerprint(episode: dict[str, Any]) -> str:
    events = episode.get("events", [])
    payload = [
        {
            "step_number": event.get("step_number"),
            "event_id": event.get("event_id"),
            "action_id": event.get("action_id"),
            "observation_id": event.get("observation_id"),
            "planning_step_id": event.get("planning_step_id"),
            "memory_state_digest": event.get("memory_state_digest"),
        }
        for event in events
    ]
    return _digest(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def _regression_snapshot(validation: dict[str, Any]) -> dict[str, Any]:
    episode = _sample_episode_from_validation(validation)
    events = episode.get("events", [])
    return {
        "validation_id": validation.get("validation_id"),
        "validation_signature": validation.get("validation_signature"),
        "source_implementation_id": validation.get("source_implementation_report", {}).get("implementation_id"),
        "episode_id": episode.get("episode_id"),
        "event_count": episode.get("event_count"),
        "event_trace_fingerprint": _event_trace_fingerprint(episode),
        "event_ids": [event.get("event_id") for event in events],
        "action_ids": [event.get("action_id") for event in events],
        "observation_ids": [event.get("observation_id") for event in events],
        "planning_step_ids": [event.get("planning_step_id") for event in events],
        "memory_state_digests": [event.get("memory_state_digest") for event in events],
    }


def _ids_unique(values: list[Any]) -> bool:
    return len(values) == len(set(values)) and all(values)


def _steps_are_sequential(values: list[str], prefix: str) -> bool:
    return values == [f"{prefix}-{index:03d}" for index in range(1, len(values) + 1)]


def _side_effect_flags_are_denied(report: dict[str, Any]) -> bool:
    return (
        report.get("network_access_allowed") is False
        and report.get("shell_execution_allowed") is False
        and report.get("repository_mutation_allowed") is False
    )


def _case(case_id: str, expected: Any, observed: Any, passed: bool) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "passed": passed,
        "failure_reason": None if passed else f"{case_id}_FAILED",
    }


def build_milestone_33_boundary_regression_integration_cases(report: dict[str, Any]) -> list[dict[str, Any]]:
    source_text = _read_text(SOURCE_VALIDATION_DOC_PATH)
    validation = report["source_validation_report"]
    snapshot = report["regression_snapshot"]
    return [
        _case("TASK_4_VALIDATION_READY", "Task 4 validation ready", SOURCE_VALIDATION_DOC_PATH.as_posix(), "MILESTONE_33_TASK_4_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_VALIDATION_READY=true" in source_text),
        _case("SOURCE_VALIDATION_STATUS_VALID", "VALID", report.get("source_validation_status"), report.get("source_validation_status") == "VALID"),
        _case("SOURCE_VALIDATION_PASSED", True, report.get("source_validation_passed"), report.get("source_validation_passed") is True),
        _case("SOURCE_VALIDATION_REPORT_VALID", True, validation.get("_validation_report_valid"), validation.get("_validation_report_valid") is True),
        _case("OBJECTIVE_ID_MATCHES_VALIDATION", SELECTED_OBJECTIVE_ID, report.get("selected_objective_id"), report.get("selected_objective_id") == SELECTED_OBJECTIVE_ID),
        _case("SCOPE_LOCK_ID_MATCHES_VALIDATION", SCOPE_LOCK_ID, report.get("scope_lock_id"), report.get("scope_lock_id") == SCOPE_LOCK_ID),
        _case("VALIDATION_CASE_COUNT_STABLE", 16, validation.get("validation_case_count"), validation.get("validation_case_count") == 16),
        _case("VALIDATION_PASS_COUNT_STABLE", 16, validation.get("pass_count"), validation.get("pass_count") == 16),
        _case("VALIDATION_FAIL_COUNT_ZERO", 0, validation.get("fail_count"), validation.get("fail_count") == 0),
        _case("REGRESSION_SNAPSHOT_EVENT_COUNT_STABLE", 4, snapshot.get("event_count"), snapshot.get("event_count") == 4),
        _case("REGRESSION_EVENT_TRACE_FINGERPRINT_PRESENT", "non-empty fingerprint", snapshot.get("event_trace_fingerprint"), bool(snapshot.get("event_trace_fingerprint"))),
        _case("REGRESSION_EVENT_IDS_UNIQUE", True, _ids_unique(snapshot.get("event_ids", [])), _ids_unique(snapshot.get("event_ids", []))),
        _case("REGRESSION_ACTION_IDS_SEQUENTIAL", "ACTION-001..ACTION-004", snapshot.get("action_ids"), _steps_are_sequential(snapshot.get("action_ids", []), "ACTION")),
        _case("REGRESSION_OBSERVATION_IDS_SEQUENTIAL", "OBSERVATION-001..OBSERVATION-004", snapshot.get("observation_ids"), _steps_are_sequential(snapshot.get("observation_ids", []), "OBSERVATION")),
        _case("REGRESSION_PLANNING_STEP_IDS_SEQUENTIAL", "PLAN-001..PLAN-004", snapshot.get("planning_step_ids"), _steps_are_sequential(snapshot.get("planning_step_ids", []), "PLAN")),
        _case("REGRESSION_MEMORY_DIGESTS_PRESENT", True, all(snapshot.get("memory_state_digests", [])), all(snapshot.get("memory_state_digests", []))),
        _case("LEGAL_CERTIFICATION_FALSE", False, report.get("legal_certification"), report.get("legal_certification") is False),
        _case("KAGGLE_SCORE_CLAIM_FALSE", False, report.get("kaggle_score_claim"), report.get("kaggle_score_claim") is False),
        _case("RUNTIME_SIDE_EFFECT_FLAGS_DENIED", True, _side_effect_flags_are_denied(report), _side_effect_flags_are_denied(report)),
        _case("NEXT_STAGE_TASK_6_FINAL_CLOSURE", NEXT_STAGE, report.get("next_stage"), report.get("next_stage") == NEXT_STAGE),
    ]


def run_milestone_33_boundary_regression_integration() -> dict[str, Any]:
    validation = _validation_report()
    snapshot = _regression_snapshot(validation)
    report: dict[str, Any] = {
        "ready": True,
        "task_id": TASK_ID,
        "source_validation_task_id": SOURCE_VALIDATION_TASK_ID,
        "source_validation_status": validation.get("validation_status", "UNKNOWN"),
        "source_validation_passed": bool(validation.get("validation_passed")) and bool(validation.get("_validation_report_valid")),
        "source_task_4_signature": validation.get("task_4_signature", ""),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "runtime_mode_id": RUNTIME_MODE_ID,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_5_signature": TASK_5_SIGNATURE,
        "integration_id": INTEGRATION_ID,
        "integration_signature": INTEGRATION_SIGNATURE,
        "integration_status": "VALID",
        "arc_agi3_interactive_runtime_boundary": validation.get("arc_agi3_interactive_runtime_boundary"),
        "planning_trace_required": validation.get("planning_trace_required"),
        "action_observation_event_trace_required": validation.get("action_observation_event_trace_required"),
        "goal_inference_boundary_required": validation.get("goal_inference_boundary_required"),
        "memory_state_boundary_required": validation.get("memory_state_boundary_required"),
        "technical_trace_artifact_only": validation.get("technical_trace_artifact_only"),
        "legal_certification": validation.get("legal_certification"),
        "kaggle_score_claim": validation.get("kaggle_score_claim"),
        "network_access_allowed": validation.get("network_access_allowed"),
        "shell_execution_allowed": validation.get("shell_execution_allowed"),
        "repository_mutation_allowed": validation.get("repository_mutation_allowed"),
        "source_validation_report": validation,
        "regression_snapshot": snapshot,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    cases = build_milestone_33_boundary_regression_integration_cases(report)
    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    report.update(
        {
            "integration_case_count": len(cases),
            "pass_count": pass_count,
            "fail_count": fail_count,
            "integration_passed": fail_count == 0,
            "cases": cases,
        }
    )
    if fail_count:
        report["integration_status"] = "INVALID"
    return report


def validate_milestone_33_boundary_regression_integration_report(report: dict[str, Any]) -> bool:
    required = {
        "ready": True,
        "task_id": TASK_ID,
        "source_validation_task_id": SOURCE_VALIDATION_TASK_ID,
        "source_validation_status": "VALID",
        "source_validation_passed": True,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "runtime_mode_id": RUNTIME_MODE_ID,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "integration_status": "VALID",
        "arc_agi3_interactive_runtime_boundary": True,
        "planning_trace_required": True,
        "action_observation_event_trace_required": True,
        "goal_inference_boundary_required": True,
        "memory_state_boundary_required": True,
        "technical_trace_artifact_only": True,
        "legal_certification": False,
        "kaggle_score_claim": False,
        "network_access_allowed": False,
        "shell_execution_allowed": False,
        "repository_mutation_allowed": False,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    for key, expected in required.items():
        if report.get(key) != expected:
            return False
    snapshot = report.get("regression_snapshot", {})
    if snapshot.get("event_count") != 4:
        return False
    if not snapshot.get("event_trace_fingerprint"):
        return False
    cases = report.get("cases", [])
    if len(cases) != report.get("integration_case_count"):
        return False
    if report.get("pass_count") != len(cases):
        return False
    if report.get("fail_count") != 0:
        return False
    if report.get("integration_passed") is not True:
        return False
    return all(case.get("passed") is True for case in cases)


def _markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 33 Task 5 Boundary Regression Integration",
        "",
        f"- Task ID: `{report['task_id']}`",
        f"- Integration ID: `{report['integration_id']}`",
        f"- Status: `{report['integration_status']}`",
        f"- Cases: `{report['pass_count']}/{report['integration_case_count']}`",
        "",
        "## Regression Snapshot",
        "",
        f"- Episode ID: `{report['regression_snapshot']['episode_id']}`",
        f"- Event trace fingerprint: `{report['regression_snapshot']['event_trace_fingerprint']}`",
        "- legalCertification=false.",
        "- kaggleScoreClaim=false.",
        "",
        "## Cases",
        "",
    ]
    for case in report["cases"]:
        status = "PASS" if case["passed"] else "FAIL"
        lines.append(f"- `{status}` `{case['case_id']}`")
    lines.append("")
    return "\n".join(lines)


def _doc_text(report: dict[str, Any]) -> str:
    return f"""# Milestone 33 Task 5 - HBCE ARC AGI3 Interactive Runtime Planning Trace Boundary Regression Integration v1

MILESTONE_33_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_REGRESSION_INTEGRATION_READY={_bool_marker(report['ready'])}
MILESTONE_33_TASK_5_TASK_ID={report['task_id']}
MILESTONE_33_TASK_5_SOURCE_VALIDATION_TASK_ID={report['source_validation_task_id']}
MILESTONE_33_TASK_5_SOURCE_VALIDATION_STATUS={report['source_validation_status']}
MILESTONE_33_TASK_5_SOURCE_VALIDATION_PASSED={_bool_marker(report['source_validation_passed'])}
MILESTONE_33_TASK_5_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_33_TASK_5_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_33_TASK_5_RUNTIME_MODE_ID={report['runtime_mode_id']}
MILESTONE_33_TASK_5_REGRESSION_INTEGRATION_REVISION={report['regression_integration_revision']}
MILESTONE_33_TASK_5_TASK_5_SIGNATURE={report['task_5_signature']}
MILESTONE_33_TASK_5_INTEGRATION_ID={report['integration_id']}
MILESTONE_33_TASK_5_INTEGRATION_SIGNATURE={report['integration_signature']}
MILESTONE_33_TASK_5_INTEGRATION_STATUS={report['integration_status']}
MILESTONE_33_TASK_5_INTEGRATION_CASE_COUNT={report['integration_case_count']}
MILESTONE_33_TASK_5_PASS_COUNT={report['pass_count']}
MILESTONE_33_TASK_5_FAIL_COUNT={report['fail_count']}
MILESTONE_33_TASK_5_INTEGRATION_PASSED={_bool_marker(report['integration_passed'])}
MILESTONE_33_TASK_5_ARC_AGI3_INTERACTIVE_RUNTIME_BOUNDARY={_bool_marker(report['arc_agi3_interactive_runtime_boundary'])}
MILESTONE_33_TASK_5_PLANNING_TRACE_REQUIRED={_bool_marker(report['planning_trace_required'])}
MILESTONE_33_TASK_5_ACTION_OBSERVATION_EVENT_TRACE_REQUIRED={_bool_marker(report['action_observation_event_trace_required'])}
MILESTONE_33_TASK_5_GOAL_INFERENCE_BOUNDARY_REQUIRED={_bool_marker(report['goal_inference_boundary_required'])}
MILESTONE_33_TASK_5_MEMORY_STATE_BOUNDARY_REQUIRED={_bool_marker(report['memory_state_boundary_required'])}
MILESTONE_33_TASK_5_TECHNICAL_TRACE_ARTIFACT_ONLY={_bool_marker(report['technical_trace_artifact_only'])}
MILESTONE_33_TASK_5_LEGAL_CERTIFICATION={_bool_marker(report['legal_certification'])}
MILESTONE_33_TASK_5_KAGGLE_SCORE_CLAIM={_bool_marker(report['kaggle_score_claim'])}
MILESTONE_33_TASK_5_NETWORK_ACCESS_ALLOWED={_bool_marker(report['network_access_allowed'])}
MILESTONE_33_TASK_5_SHELL_EXECUTION_ALLOWED={_bool_marker(report['shell_execution_allowed'])}
MILESTONE_33_TASK_5_REPOSITORY_MUTATION_ALLOWED={_bool_marker(report['repository_mutation_allowed'])}
MILESTONE_33_TASK_5_REGRESSION_EPISODE_ID={report['regression_snapshot']['episode_id']}
MILESTONE_33_TASK_5_REGRESSION_EVENT_COUNT={report['regression_snapshot']['event_count']}
MILESTONE_33_TASK_5_REGRESSION_EVENT_TRACE_FINGERPRINT={report['regression_snapshot']['event_trace_fingerprint']}
MILESTONE_33_TASK_5_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_33_TASK_5_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_33_TASK_5_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_33_TASK_5_NEXT_STAGE={report['next_stage']}

## Regression Integration Boundary

This integration records regression invariants for the ARC-AGI-3 interactive
runtime planning trace boundary: validation report validity, stable event trace
shape, sequential action/observation/planning IDs, memory digest presence,
side-effect denial, and explicit legal/Kaggle claim denial.

Generated runtime traces are technical artifacts only.
legalCertification=false.
kaggleScoreClaim=false.
"""


def write_milestone_33_task_5_artifacts() -> dict[str, str]:
    report = run_milestone_33_boundary_regression_integration()
    if not validate_milestone_33_boundary_regression_integration_report(report):
        raise ValueError("Milestone 33 Task 5 boundary regression integration report is invalid")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    cases_path = ARTIFACT_DIR / "task-5-boundary-regression-integration-cases.json"
    report_json_path = ARTIFACT_DIR / "task-5-boundary-regression-integration-report.json"
    report_md_path = ARTIFACT_DIR / "task-5-boundary-regression-integration-report.md"
    index_path = ARTIFACT_DIR / "task-5-index.txt"
    manifest_path = ARTIFACT_DIR / "task-5-manifest.json"

    cases_path.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md_path.write_text(_markdown_report(report), encoding="utf-8")
    index_path.write_text(
        "\n".join(["MILESTONE_33_TASK_5_ARTIFACT_INDEX", cases_path.name, report_json_path.name, report_md_path.name, manifest_path.name]) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "task_id": TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "integration_id": INTEGRATION_ID,
        "integration_signature": INTEGRATION_SIGNATURE,
        "artifact_count": GENERATED_ARTIFACT_COUNT,
        "artifacts": [cases_path.name, report_json_path.name, report_md_path.name, index_path.name, manifest_path.name],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    DOC_PATH.write_text(_doc_text(report), encoding="utf-8")

    return {
        "cases": cases_path.as_posix(),
        "report_json": report_json_path.as_posix(),
        "report_md": report_md_path.as_posix(),
        "index": index_path.as_posix(),
        "manifest": manifest_path.as_posix(),
        "doc": DOC_PATH.as_posix(),
    }


def main() -> None:
    write_milestone_33_task_5_artifacts()
    report = run_milestone_33_boundary_regression_integration()
    markers = {
        "MILESTONE_33_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_REGRESSION_INTEGRATION_READY": report["ready"],
        "MILESTONE_33_TASK_5_TASK_ID": report["task_id"],
        "MILESTONE_33_TASK_5_SOURCE_VALIDATION_TASK_ID": report["source_validation_task_id"],
        "MILESTONE_33_TASK_5_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_33_TASK_5_SCOPE_LOCK_ID": report["scope_lock_id"],
        "MILESTONE_33_TASK_5_RUNTIME_MODE_ID": report["runtime_mode_id"],
        "MILESTONE_33_TASK_5_REGRESSION_INTEGRATION_REVISION": report["regression_integration_revision"],
        "MILESTONE_33_TASK_5_TASK_5_SIGNATURE": report["task_5_signature"],
        "MILESTONE_33_TASK_5_INTEGRATION_ID": report["integration_id"],
        "MILESTONE_33_TASK_5_INTEGRATION_SIGNATURE": report["integration_signature"],
        "MILESTONE_33_TASK_5_INTEGRATION_STATUS": report["integration_status"],
        "MILESTONE_33_TASK_5_INTEGRATION_CASE_COUNT": report["integration_case_count"],
        "MILESTONE_33_TASK_5_PASS_COUNT": report["pass_count"],
        "MILESTONE_33_TASK_5_FAIL_COUNT": report["fail_count"],
        "MILESTONE_33_TASK_5_INTEGRATION_PASSED": report["integration_passed"],
        "MILESTONE_33_TASK_5_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_33_TASK_5_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_33_TASK_5_NETWORK_ACCESS_ALLOWED": report["network_access_allowed"],
        "MILESTONE_33_TASK_5_SHELL_EXECUTION_ALLOWED": report["shell_execution_allowed"],
        "MILESTONE_33_TASK_5_REPOSITORY_MUTATION_ALLOWED": report["repository_mutation_allowed"],
        "MILESTONE_33_TASK_5_REGRESSION_EVENT_COUNT": report["regression_snapshot"]["event_count"],
        "MILESTONE_33_TASK_5_REGRESSION_EVENT_TRACE_FINGERPRINT": report["regression_snapshot"]["event_trace_fingerprint"],
        "MILESTONE_33_TASK_5_TASK_BUDGET_MAX": report["task_budget_max"],
        "MILESTONE_33_TASK_5_CURRENT_TASK_NUMBER": report["current_task_number"],
        "MILESTONE_33_TASK_5_GENERATED_ARTIFACT_COUNT": report["generated_artifact_count"],
        "MILESTONE_33_TASK_5_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        if isinstance(value, bool):
            value = _bool_marker(value)
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
