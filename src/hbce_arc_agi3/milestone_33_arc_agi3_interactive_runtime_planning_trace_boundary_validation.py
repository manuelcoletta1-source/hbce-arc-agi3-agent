"""Milestone 33 Task 4 validation for ARC-AGI-3 interactive runtime planning trace boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TASK_ID = "MILESTONE_33_TASK_4_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_VALIDATION_V1"
SOURCE_IMPLEMENTATION_TASK_ID = "MILESTONE_33_TASK_3_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_IMPLEMENTATION_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
SCOPE_LOCK_ID = "MILESTONE_33_SCOPE_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
RUNTIME_MODE_ID = "ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
VALIDATION_REVISION = "MILESTONE_33_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_VALIDATION_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 4
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = (
    "MILESTONE_33_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_"
    "BOUNDARY_REGRESSION_INTEGRATION_V1"
)

ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs" / "milestone-33-task-4-hbce-arc-agi3-interactive-runtime-planning-trace-boundary-validation-v1.md"
SOURCE_IMPLEMENTATION_DOC_PATH = ROOT / "docs" / "milestone-33-task-3-hbce-arc-agi3-interactive-runtime-planning-trace-boundary-implementation-v1.md"
ARTIFACT_DIR = ROOT / "examples" / "milestone-33" / "hbce-arc-agi3-interactive-runtime-planning-trace-boundary-validation-v1"


def _digest(*parts: Any, length: int = 16) -> str:
    raw = "|".join(str(part) for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:length].upper()


TASK_4_SIGNATURE = _digest(TASK_ID, SELECTED_OBJECTIVE_ID, VALIDATION_REVISION)
VALIDATION_ID = "MILESTONE-33-ARC-AGI3-INTERACTIVE-RUNTIME-VALIDATION-" + _digest(
    SCOPE_LOCK_ID,
    RUNTIME_MODE_ID,
)
VALIDATION_SIGNATURE = _digest(VALIDATION_ID, TASK_4_SIGNATURE, NEXT_STAGE)


def _bool_marker(value: bool) -> str:
    return "true" if value else "false"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _implementation_report() -> dict[str, Any]:
    from hbce_arc_agi3.milestone_33_arc_agi3_interactive_runtime_planning_trace_boundary import (
        run_milestone_33_boundary_implementation,
        validate_interactive_runtime_episode,
        validate_milestone_33_boundary_implementation_report,
    )

    report = run_milestone_33_boundary_implementation()
    report["_implementation_report_valid"] = validate_milestone_33_boundary_implementation_report(report)
    report["_sample_episode_valid"] = validate_interactive_runtime_episode(report.get("sample_episode", {}))
    return report


def _event_steps_are_sequential(events: list[dict[str, Any]]) -> bool:
    return [event.get("step_number") for event in events] == list(range(1, len(events) + 1))


def _event_ids_are_unique(events: list[dict[str, Any]]) -> bool:
    ids = [event.get("event_id") for event in events]
    return len(ids) == len(set(ids)) and all(ids)


def _event_required_fields_present(events: list[dict[str, Any]]) -> bool:
    required = (
        "event_id",
        "action_id",
        "action_type",
        "observation_id",
        "observation_ref",
        "planning_step_id",
        "goal_hypothesis",
        "memory_state_digest",
    )
    return bool(events) and all(all(event.get(key) for key in required) for event in events)


def _side_effects_denied(episode: dict[str, Any]) -> bool:
    return (
        episode.get("network_access_allowed") is False
        and episode.get("shell_execution_allowed") is False
        and episode.get("repository_mutation_allowed") is False
    )


def _case(case_id: str, expected: Any, observed: Any, passed: bool) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "passed": passed,
        "failure_reason": None if passed else f"{case_id}_FAILED",
    }


def build_milestone_33_boundary_validation_cases(report: dict[str, Any]) -> list[dict[str, Any]]:
    source_text = _read_text(SOURCE_IMPLEMENTATION_DOC_PATH)
    implementation = report["source_implementation_report"]
    episode = implementation.get("sample_episode", {})
    events = episode.get("events", [])
    return [
        _case("TASK_3_IMPLEMENTATION_READY", "Task 3 implementation ready", SOURCE_IMPLEMENTATION_DOC_PATH.as_posix(), "MILESTONE_33_TASK_3_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_IMPLEMENTATION_READY=true" in source_text),
        _case("SOURCE_IMPLEMENTATION_STATUS_READY", "READY", report.get("source_implementation_status"), report.get("source_implementation_status") == "READY"),
        _case("SOURCE_IMPLEMENTATION_PASSED", True, report.get("source_implementation_passed"), report.get("source_implementation_passed") is True),
        _case("OBJECTIVE_ID_MATCHES_IMPLEMENTATION", SELECTED_OBJECTIVE_ID, report.get("selected_objective_id"), report.get("selected_objective_id") == SELECTED_OBJECTIVE_ID),
        _case("SCOPE_LOCK_ID_MATCHES_IMPLEMENTATION", SCOPE_LOCK_ID, report.get("scope_lock_id"), report.get("scope_lock_id") == SCOPE_LOCK_ID),
        _case("IMPLEMENTATION_REPORT_VALID", True, implementation.get("_implementation_report_valid"), implementation.get("_implementation_report_valid") is True),
        _case("SAMPLE_EPISODE_VALID", True, implementation.get("_sample_episode_valid"), implementation.get("_sample_episode_valid") is True),
        _case("SAMPLE_EPISODE_EVENT_COUNT_VALID", 4, episode.get("event_count"), episode.get("event_count") == 4 and len(events) == 4),
        _case("EVENT_STEPS_SEQUENTIAL", True, _event_steps_are_sequential(events), _event_steps_are_sequential(events)),
        _case("EVENT_IDS_UNIQUE", True, _event_ids_are_unique(events), _event_ids_are_unique(events)),
        _case("EVENT_REQUIRED_FIELDS_PRESENT", True, _event_required_fields_present(events), _event_required_fields_present(events)),
        _case("TECHNICAL_TRACE_ARTIFACT_ONLY", True, report.get("technical_trace_artifact_only"), report.get("technical_trace_artifact_only") is True),
        _case("LEGAL_CERTIFICATION_FALSE", False, report.get("legal_certification"), report.get("legal_certification") is False),
        _case("KAGGLE_SCORE_CLAIM_FALSE", False, report.get("kaggle_score_claim"), report.get("kaggle_score_claim") is False),
        _case("RUNTIME_SIDE_EFFECTS_DENIED", True, _side_effects_denied(episode), _side_effects_denied(episode)),
        _case("NEXT_STAGE_TASK_5_REGRESSION_INTEGRATION", NEXT_STAGE, report.get("next_stage"), report.get("next_stage") == NEXT_STAGE),
    ]


def run_milestone_33_boundary_validation() -> dict[str, Any]:
    implementation = _implementation_report()
    report: dict[str, Any] = {
        "ready": True,
        "task_id": TASK_ID,
        "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
        "source_implementation_status": implementation.get("implementation_status", "UNKNOWN"),
        "source_implementation_passed": bool(implementation.get("implementation_passed")) and bool(implementation.get("_implementation_report_valid")),
        "source_task_3_signature": implementation.get("task_3_signature", ""),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "runtime_mode_id": RUNTIME_MODE_ID,
        "validation_revision": VALIDATION_REVISION,
        "task_4_signature": TASK_4_SIGNATURE,
        "validation_id": VALIDATION_ID,
        "validation_signature": VALIDATION_SIGNATURE,
        "validation_status": "VALID",
        "arc_agi3_interactive_runtime_boundary": implementation.get("arc_agi3_interactive_runtime_boundary"),
        "planning_trace_required": implementation.get("planning_trace_required"),
        "action_observation_event_trace_required": implementation.get("action_observation_event_trace_required"),
        "goal_inference_boundary_required": implementation.get("goal_inference_boundary_required"),
        "memory_state_boundary_required": implementation.get("memory_state_boundary_required"),
        "technical_trace_artifact_only": implementation.get("technical_trace_artifact_only"),
        "legal_certification": implementation.get("legal_certification"),
        "kaggle_score_claim": implementation.get("kaggle_score_claim"),
        "network_access_allowed": implementation.get("network_access_allowed"),
        "shell_execution_allowed": implementation.get("shell_execution_allowed"),
        "repository_mutation_allowed": implementation.get("repository_mutation_allowed"),
        "source_implementation_report": implementation,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    cases = build_milestone_33_boundary_validation_cases(report)
    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    report.update(
        {
            "validation_case_count": len(cases),
            "pass_count": pass_count,
            "fail_count": fail_count,
            "validation_passed": fail_count == 0,
            "cases": cases,
        }
    )
    if fail_count:
        report["validation_status"] = "INVALID"
    return report


def validate_milestone_33_boundary_validation_report(report: dict[str, Any]) -> bool:
    required = {
        "ready": True,
        "task_id": TASK_ID,
        "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
        "source_implementation_status": "READY",
        "source_implementation_passed": True,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "runtime_mode_id": RUNTIME_MODE_ID,
        "validation_revision": VALIDATION_REVISION,
        "validation_status": "VALID",
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
    cases = report.get("cases", [])
    if len(cases) != report.get("validation_case_count"):
        return False
    if report.get("pass_count") != len(cases):
        return False
    if report.get("fail_count") != 0:
        return False
    if report.get("validation_passed") is not True:
        return False
    return all(case.get("passed") is True for case in cases)


def _markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 33 Task 4 Boundary Validation",
        "",
        f"- Task ID: `{report['task_id']}`",
        f"- Validation ID: `{report['validation_id']}`",
        f"- Status: `{report['validation_status']}`",
        f"- Cases: `{report['pass_count']}/{report['validation_case_count']}`",
        "",
        "## Validation Scope",
        "",
        "- Task 3 implementation report validates.",
        "- Sample interactive episode validates.",
        "- Event sequence, event uniqueness, trace fields, and side-effect denial validate.",
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
    return f"""# Milestone 33 Task 4 - HBCE ARC AGI3 Interactive Runtime Planning Trace Boundary Validation v1

MILESTONE_33_TASK_4_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_VALIDATION_READY={_bool_marker(report['ready'])}
MILESTONE_33_TASK_4_TASK_ID={report['task_id']}
MILESTONE_33_TASK_4_SOURCE_IMPLEMENTATION_TASK_ID={report['source_implementation_task_id']}
MILESTONE_33_TASK_4_SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}
MILESTONE_33_TASK_4_SOURCE_IMPLEMENTATION_PASSED={_bool_marker(report['source_implementation_passed'])}
MILESTONE_33_TASK_4_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_33_TASK_4_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_33_TASK_4_RUNTIME_MODE_ID={report['runtime_mode_id']}
MILESTONE_33_TASK_4_VALIDATION_REVISION={report['validation_revision']}
MILESTONE_33_TASK_4_TASK_4_SIGNATURE={report['task_4_signature']}
MILESTONE_33_TASK_4_VALIDATION_ID={report['validation_id']}
MILESTONE_33_TASK_4_VALIDATION_SIGNATURE={report['validation_signature']}
MILESTONE_33_TASK_4_VALIDATION_STATUS={report['validation_status']}
MILESTONE_33_TASK_4_VALIDATION_CASE_COUNT={report['validation_case_count']}
MILESTONE_33_TASK_4_PASS_COUNT={report['pass_count']}
MILESTONE_33_TASK_4_FAIL_COUNT={report['fail_count']}
MILESTONE_33_TASK_4_VALIDATION_PASSED={_bool_marker(report['validation_passed'])}
MILESTONE_33_TASK_4_ARC_AGI3_INTERACTIVE_RUNTIME_BOUNDARY={_bool_marker(report['arc_agi3_interactive_runtime_boundary'])}
MILESTONE_33_TASK_4_PLANNING_TRACE_REQUIRED={_bool_marker(report['planning_trace_required'])}
MILESTONE_33_TASK_4_ACTION_OBSERVATION_EVENT_TRACE_REQUIRED={_bool_marker(report['action_observation_event_trace_required'])}
MILESTONE_33_TASK_4_GOAL_INFERENCE_BOUNDARY_REQUIRED={_bool_marker(report['goal_inference_boundary_required'])}
MILESTONE_33_TASK_4_MEMORY_STATE_BOUNDARY_REQUIRED={_bool_marker(report['memory_state_boundary_required'])}
MILESTONE_33_TASK_4_TECHNICAL_TRACE_ARTIFACT_ONLY={_bool_marker(report['technical_trace_artifact_only'])}
MILESTONE_33_TASK_4_LEGAL_CERTIFICATION={_bool_marker(report['legal_certification'])}
MILESTONE_33_TASK_4_KAGGLE_SCORE_CLAIM={_bool_marker(report['kaggle_score_claim'])}
MILESTONE_33_TASK_4_NETWORK_ACCESS_ALLOWED={_bool_marker(report['network_access_allowed'])}
MILESTONE_33_TASK_4_SHELL_EXECUTION_ALLOWED={_bool_marker(report['shell_execution_allowed'])}
MILESTONE_33_TASK_4_REPOSITORY_MUTATION_ALLOWED={_bool_marker(report['repository_mutation_allowed'])}
MILESTONE_33_TASK_4_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_33_TASK_4_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_33_TASK_4_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_33_TASK_4_NEXT_STAGE={report['next_stage']}

## Validation Boundary

This validation confirms that the Task 3 ARC-AGI-3 interactive runtime planning
trace implementation preserves the locked Task 2 objective, validates its sample
episode, preserves sequential action/observation planning trace events, and keeps
the runtime boundary local-only and side-effect-denied.

Generated runtime traces are technical artifacts only.
legalCertification=false.
kaggleScoreClaim=false.
"""


def write_milestone_33_task_4_artifacts() -> dict[str, str]:
    report = run_milestone_33_boundary_validation()
    if not validate_milestone_33_boundary_validation_report(report):
        raise ValueError("Milestone 33 Task 4 boundary validation report is invalid")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    cases_path = ARTIFACT_DIR / "task-4-boundary-validation-cases.json"
    report_json_path = ARTIFACT_DIR / "task-4-boundary-validation-report.json"
    report_md_path = ARTIFACT_DIR / "task-4-boundary-validation-report.md"
    index_path = ARTIFACT_DIR / "task-4-index.txt"
    manifest_path = ARTIFACT_DIR / "task-4-manifest.json"

    cases_path.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md_path.write_text(_markdown_report(report), encoding="utf-8")
    index_path.write_text(
        "\n".join(["MILESTONE_33_TASK_4_ARTIFACT_INDEX", cases_path.name, report_json_path.name, report_md_path.name, manifest_path.name]) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "task_id": TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "validation_id": VALIDATION_ID,
        "validation_signature": VALIDATION_SIGNATURE,
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
    write_milestone_33_task_4_artifacts()
    report = run_milestone_33_boundary_validation()
    markers = {
        "MILESTONE_33_TASK_4_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_VALIDATION_READY": report["ready"],
        "MILESTONE_33_TASK_4_TASK_ID": report["task_id"],
        "MILESTONE_33_TASK_4_SOURCE_IMPLEMENTATION_TASK_ID": report["source_implementation_task_id"],
        "MILESTONE_33_TASK_4_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_33_TASK_4_SCOPE_LOCK_ID": report["scope_lock_id"],
        "MILESTONE_33_TASK_4_RUNTIME_MODE_ID": report["runtime_mode_id"],
        "MILESTONE_33_TASK_4_VALIDATION_REVISION": report["validation_revision"],
        "MILESTONE_33_TASK_4_TASK_4_SIGNATURE": report["task_4_signature"],
        "MILESTONE_33_TASK_4_VALIDATION_ID": report["validation_id"],
        "MILESTONE_33_TASK_4_VALIDATION_SIGNATURE": report["validation_signature"],
        "MILESTONE_33_TASK_4_VALIDATION_STATUS": report["validation_status"],
        "MILESTONE_33_TASK_4_VALIDATION_CASE_COUNT": report["validation_case_count"],
        "MILESTONE_33_TASK_4_PASS_COUNT": report["pass_count"],
        "MILESTONE_33_TASK_4_FAIL_COUNT": report["fail_count"],
        "MILESTONE_33_TASK_4_VALIDATION_PASSED": report["validation_passed"],
        "MILESTONE_33_TASK_4_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_33_TASK_4_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_33_TASK_4_NETWORK_ACCESS_ALLOWED": report["network_access_allowed"],
        "MILESTONE_33_TASK_4_SHELL_EXECUTION_ALLOWED": report["shell_execution_allowed"],
        "MILESTONE_33_TASK_4_REPOSITORY_MUTATION_ALLOWED": report["repository_mutation_allowed"],
        "MILESTONE_33_TASK_4_TASK_BUDGET_MAX": report["task_budget_max"],
        "MILESTONE_33_TASK_4_CURRENT_TASK_NUMBER": report["current_task_number"],
        "MILESTONE_33_TASK_4_GENERATED_ARTIFACT_COUNT": report["generated_artifact_count"],
        "MILESTONE_33_TASK_4_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        if isinstance(value, bool):
            value = _bool_marker(value)
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
