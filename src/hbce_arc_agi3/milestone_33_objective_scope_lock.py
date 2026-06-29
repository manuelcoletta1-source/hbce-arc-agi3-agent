"""Milestone 33 Task 2 objective selection and scope lock.

Locks the HBCE ARC-AGI-3 interactive runtime planning trace boundary for the
next implementation stage.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TASK_ID = "MILESTONE_33_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
SOURCE_OPENING_TASK_ID = "MILESTONE_33_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
SELECTED_OBJECTIVE_STATUS = "SELECTED_AND_SCOPE_LOCKED"
SCOPE_LOCK_ID = "MILESTONE_33_SCOPE_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
OBJECTIVE_SELECTION_REVISION = "MILESTONE_33_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
RUNTIME_MODE_ID = "ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 2
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = (
    "MILESTONE_33_TASK_3_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_"
    "BOUNDARY_IMPLEMENTATION_V1"
)

ARC_AGI3_INTERACTIVE_RUNTIME_BOUNDARY = True
PLANNING_TRACE_REQUIRED = True
ACTION_OBSERVATION_EVENT_TRACE_REQUIRED = True
GOAL_INFERENCE_BOUNDARY_REQUIRED = True
MEMORY_STATE_BOUNDARY_REQUIRED = True
TECHNICAL_TRACE_ARTIFACT_ONLY = True
LEGAL_CERTIFICATION = False
KAGGLE_SCORE_CLAIM = False

ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs" / "milestone-33-task-2-objective-selection-and-scope-lock-v1.md"
SOURCE_OPENING_DOC_PATH = ROOT / "docs" / "milestone-33-task-1-governed-opening-with-task-budget-v1.md"
ARTIFACT_DIR = ROOT / "examples" / "milestone-33" / "objective-selection-and-scope-lock-v1"


def _digest(*parts: Any, length: int = 16) -> str:
    raw = "|".join(str(part) for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:length].upper()


TASK_2_SIGNATURE = _digest(TASK_ID, SELECTED_OBJECTIVE_ID, OBJECTIVE_SELECTION_REVISION)
SCOPE_LOCK_INSTANCE_ID = "MILESTONE-33-SCOPE-LOCK-" + _digest(
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    RUNTIME_MODE_ID,
)
SCOPE_LOCK_SIGNATURE = _digest(SCOPE_LOCK_INSTANCE_ID, TASK_2_SIGNATURE, NEXT_STAGE)


def _bool_marker(value: bool) -> str:
    return "true" if value else "false"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _source_opening_summary() -> dict[str, Any]:
    try:
        from hbce_arc_agi3.milestone_33_governed_opening import (
            run_milestone_33_governed_opening,
            validate_milestone_33_governed_opening_report,
        )

        report = run_milestone_33_governed_opening()
        valid = validate_milestone_33_governed_opening_report(report)
        return {
            "source_opening_status": report.get("opening_status", "UNKNOWN"),
            "source_opening_passed": bool(report.get("opening_passed")) and valid,
            "source_task_1_signature": report.get("task_1_signature", ""),
        }
    except Exception:
        text = _read_text(SOURCE_OPENING_DOC_PATH)
        return {
            "source_opening_status": (
                "READY" if "MILESTONE_33_TASK_1_OPENING_STATUS=READY" in text else "UNKNOWN"
            ),
            "source_opening_passed": (
                "MILESTONE_33_TASK_1_OPENING_PASSED=true" in text
                or "MILESTONE_33_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
            ),
            "source_task_1_signature": "",
        }


def _case(case_id: str, expected: Any, observed: Any, passed: bool) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "passed": passed,
        "failure_reason": None if passed else f"{case_id}_FAILED",
    }


def build_milestone_33_objective_scope_lock_cases(report: dict[str, Any]) -> list[dict[str, Any]]:
    source_text = _read_text(SOURCE_OPENING_DOC_PATH)
    return [
        _case(
            "TASK_1_GOVERNED_OPENING_READY",
            "Task 1 governed opening ready",
            SOURCE_OPENING_DOC_PATH.as_posix(),
            "MILESTONE_33_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in source_text,
        ),
        _case("SOURCE_OPENING_STATUS_READY", "READY", report.get("source_opening_status"), report.get("source_opening_status") == "READY"),
        _case("SOURCE_OPENING_PASSED", True, report.get("source_opening_passed"), report.get("source_opening_passed") is True),
        _case("OBJECTIVE_CANDIDATE_SELECTED", SELECTED_OBJECTIVE_ID, report.get("selected_objective_id"), report.get("selected_objective_id") == SELECTED_OBJECTIVE_ID),
        _case("SCOPE_LOCK_ID_BOUND", SCOPE_LOCK_ID, report.get("scope_lock_id"), report.get("scope_lock_id") == SCOPE_LOCK_ID),
        _case("INTERACTIVE_RUNTIME_BOUNDARY_LOCKED", True, report.get("arc_agi3_interactive_runtime_boundary"), report.get("arc_agi3_interactive_runtime_boundary") is True),
        _case("PLANNING_TRACE_REQUIRED", True, report.get("planning_trace_required"), report.get("planning_trace_required") is True),
        _case("ACTION_OBSERVATION_EVENT_TRACE_REQUIRED", True, report.get("action_observation_event_trace_required"), report.get("action_observation_event_trace_required") is True),
        _case("GOAL_INFERENCE_BOUNDARY_REQUIRED", True, report.get("goal_inference_boundary_required"), report.get("goal_inference_boundary_required") is True),
        _case("MEMORY_STATE_BOUNDARY_REQUIRED", True, report.get("memory_state_boundary_required"), report.get("memory_state_boundary_required") is True),
        _case("LEGAL_CERTIFICATION_REMAINS_FALSE", False, report.get("legal_certification"), report.get("legal_certification") is False),
        _case("NEXT_STAGE_TASK_3_IMPLEMENTATION", NEXT_STAGE, report.get("next_stage"), report.get("next_stage") == NEXT_STAGE),
    ]


def run_milestone_33_objective_scope_lock() -> dict[str, Any]:
    source = _source_opening_summary()
    report: dict[str, Any] = {
        "ready": True,
        "task_id": TASK_ID,
        "source_opening_task_id": SOURCE_OPENING_TASK_ID,
        "source_opening_status": source["source_opening_status"],
        "source_opening_passed": source["source_opening_passed"],
        "source_task_1_signature": source["source_task_1_signature"],
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "selected_objective_status": SELECTED_OBJECTIVE_STATUS,
        "scope_lock_id": SCOPE_LOCK_ID,
        "runtime_mode_id": RUNTIME_MODE_ID,
        "objective_selection_revision": OBJECTIVE_SELECTION_REVISION,
        "task_2_signature": TASK_2_SIGNATURE,
        "scope_lock_instance_id": SCOPE_LOCK_INSTANCE_ID,
        "scope_lock_signature": SCOPE_LOCK_SIGNATURE,
        "arc_agi3_interactive_runtime_boundary": ARC_AGI3_INTERACTIVE_RUNTIME_BOUNDARY,
        "planning_trace_required": PLANNING_TRACE_REQUIRED,
        "action_observation_event_trace_required": ACTION_OBSERVATION_EVENT_TRACE_REQUIRED,
        "goal_inference_boundary_required": GOAL_INFERENCE_BOUNDARY_REQUIRED,
        "memory_state_boundary_required": MEMORY_STATE_BOUNDARY_REQUIRED,
        "technical_trace_artifact_only": TECHNICAL_TRACE_ARTIFACT_ONLY,
        "legal_certification": LEGAL_CERTIFICATION,
        "kaggle_score_claim": KAGGLE_SCORE_CLAIM,
        "scope_lock_status": "LOCKED",
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    cases = build_milestone_33_objective_scope_lock_cases(report)
    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    report.update(
        {
            "scope_lock_case_count": len(cases),
            "pass_count": pass_count,
            "fail_count": fail_count,
            "scope_lock_passed": fail_count == 0,
            "cases": cases,
        }
    )
    if fail_count:
        report["scope_lock_status"] = "INVALID"
    return report


def validate_milestone_33_objective_scope_lock_report(report: dict[str, Any]) -> bool:
    required = {
        "ready": True,
        "task_id": TASK_ID,
        "source_opening_task_id": SOURCE_OPENING_TASK_ID,
        "source_opening_status": "READY",
        "source_opening_passed": True,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "selected_objective_status": SELECTED_OBJECTIVE_STATUS,
        "scope_lock_id": SCOPE_LOCK_ID,
        "runtime_mode_id": RUNTIME_MODE_ID,
        "objective_selection_revision": OBJECTIVE_SELECTION_REVISION,
        "scope_lock_status": "LOCKED",
        "arc_agi3_interactive_runtime_boundary": True,
        "planning_trace_required": True,
        "action_observation_event_trace_required": True,
        "goal_inference_boundary_required": True,
        "memory_state_boundary_required": True,
        "technical_trace_artifact_only": True,
        "legal_certification": False,
        "kaggle_score_claim": False,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    for key, expected in required.items():
        if report.get(key) != expected:
            return False
    cases = report.get("cases", [])
    if len(cases) != report.get("scope_lock_case_count"):
        return False
    if report.get("pass_count") != len(cases):
        return False
    if report.get("fail_count") != 0:
        return False
    if report.get("scope_lock_passed") is not True:
        return False
    return all(case.get("passed") is True for case in cases)


def _markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 33 Task 2 Objective Selection and Scope Lock",
        "",
        f"- Task ID: `{report['task_id']}`",
        f"- Selected objective: `{report['selected_objective_id']}`",
        f"- Scope lock: `{report['scope_lock_id']}`",
        f"- Runtime mode: `{report['runtime_mode_id']}`",
        f"- Status: `{report['scope_lock_status']}`",
        f"- Cases: `{report['pass_count']}/{report['scope_lock_case_count']}`",
        "",
        "## Boundary",
        "",
        "- ARC-AGI-3 interactive runtime planning trace boundary is locked.",
        "- Planning trace, action/observation event trace, goal inference boundary, and memory state boundary are required.",
        "- Generated traces are technical artifacts only.",
        "- legalCertification=false.",
        "- No Kaggle score or leaderboard claim is made by this scope lock.",
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
    return f"""# Milestone 33 Task 2 - Objective Selection and Scope Lock v1

MILESTONE_33_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY={_bool_marker(report['ready'])}
MILESTONE_33_TASK_2_TASK_ID={report['task_id']}
MILESTONE_33_TASK_2_SOURCE_OPENING_TASK_ID={report['source_opening_task_id']}
MILESTONE_33_TASK_2_SOURCE_OPENING_STATUS={report['source_opening_status']}
MILESTONE_33_TASK_2_SOURCE_OPENING_PASSED={_bool_marker(report['source_opening_passed'])}
MILESTONE_33_TASK_2_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_33_TASK_2_SELECTED_OBJECTIVE_STATUS={report['selected_objective_status']}
MILESTONE_33_TASK_2_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_33_TASK_2_RUNTIME_MODE_ID={report['runtime_mode_id']}
MILESTONE_33_TASK_2_OBJECTIVE_SELECTION_REVISION={report['objective_selection_revision']}
MILESTONE_33_TASK_2_TASK_2_SIGNATURE={report['task_2_signature']}
MILESTONE_33_TASK_2_SCOPE_LOCK_INSTANCE_ID={report['scope_lock_instance_id']}
MILESTONE_33_TASK_2_SCOPE_LOCK_SIGNATURE={report['scope_lock_signature']}
MILESTONE_33_TASK_2_ARC_AGI3_INTERACTIVE_RUNTIME_BOUNDARY={_bool_marker(report['arc_agi3_interactive_runtime_boundary'])}
MILESTONE_33_TASK_2_PLANNING_TRACE_REQUIRED={_bool_marker(report['planning_trace_required'])}
MILESTONE_33_TASK_2_ACTION_OBSERVATION_EVENT_TRACE_REQUIRED={_bool_marker(report['action_observation_event_trace_required'])}
MILESTONE_33_TASK_2_GOAL_INFERENCE_BOUNDARY_REQUIRED={_bool_marker(report['goal_inference_boundary_required'])}
MILESTONE_33_TASK_2_MEMORY_STATE_BOUNDARY_REQUIRED={_bool_marker(report['memory_state_boundary_required'])}
MILESTONE_33_TASK_2_TECHNICAL_TRACE_ARTIFACT_ONLY={_bool_marker(report['technical_trace_artifact_only'])}
MILESTONE_33_TASK_2_LEGAL_CERTIFICATION={_bool_marker(report['legal_certification'])}
MILESTONE_33_TASK_2_KAGGLE_SCORE_CLAIM={_bool_marker(report['kaggle_score_claim'])}
MILESTONE_33_TASK_2_SCOPE_LOCK_STATUS={report['scope_lock_status']}
MILESTONE_33_TASK_2_SCOPE_LOCK_CASE_COUNT={report['scope_lock_case_count']}
MILESTONE_33_TASK_2_PASS_COUNT={report['pass_count']}
MILESTONE_33_TASK_2_FAIL_COUNT={report['fail_count']}
MILESTONE_33_TASK_2_SCOPE_LOCK_PASSED={_bool_marker(report['scope_lock_passed'])}
MILESTONE_33_TASK_2_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_33_TASK_2_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_33_TASK_2_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_33_TASK_2_NEXT_STAGE={report['next_stage']}

## Canonical Boundary

HBCE ARC-AGI-3 Interactive Runtime Planning Trace Boundary.

The scope links interactive runtime episodes to action/observation traces,
planning traces, goal inference boundaries, memory state boundaries, technical
proof artifacts, and governed audit records.

Generated runtime traces are technical artifacts only.
legalCertification=false.
No Kaggle score, leaderboard position, benchmark certification, or public
identity/legal certification is claimed by this milestone scope lock.
"""


def write_milestone_33_task_2_artifacts() -> dict[str, str]:
    report = run_milestone_33_objective_scope_lock()
    if not validate_milestone_33_objective_scope_lock_report(report):
        raise ValueError("Milestone 33 Task 2 objective scope lock report is invalid")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    cases_path = ARTIFACT_DIR / "task-2-objective-scope-lock-cases.json"
    report_json_path = ARTIFACT_DIR / "task-2-objective-scope-lock-report.json"
    report_md_path = ARTIFACT_DIR / "task-2-objective-scope-lock-report.md"
    index_path = ARTIFACT_DIR / "task-2-index.txt"
    manifest_path = ARTIFACT_DIR / "task-2-manifest.json"

    cases_path.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md_path.write_text(_markdown_report(report), encoding="utf-8")
    index_path.write_text(
        "\n".join(
            [
                "MILESTONE_33_TASK_2_ARTIFACT_INDEX",
                cases_path.name,
                report_json_path.name,
                report_md_path.name,
                manifest_path.name,
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    manifest = {
        "task_id": TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_instance_id": SCOPE_LOCK_INSTANCE_ID,
        "scope_lock_signature": SCOPE_LOCK_SIGNATURE,
        "artifact_count": GENERATED_ARTIFACT_COUNT,
        "artifacts": [
            cases_path.name,
            report_json_path.name,
            report_md_path.name,
            index_path.name,
            manifest_path.name,
        ],
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
    write_milestone_33_task_2_artifacts()
    report = run_milestone_33_objective_scope_lock()
    markers = {
        "MILESTONE_33_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY": report["ready"],
        "MILESTONE_33_TASK_2_TASK_ID": report["task_id"],
        "MILESTONE_33_TASK_2_SOURCE_OPENING_TASK_ID": report["source_opening_task_id"],
        "MILESTONE_33_TASK_2_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_33_TASK_2_SELECTED_OBJECTIVE_STATUS": report["selected_objective_status"],
        "MILESTONE_33_TASK_2_SCOPE_LOCK_ID": report["scope_lock_id"],
        "MILESTONE_33_TASK_2_RUNTIME_MODE_ID": report["runtime_mode_id"],
        "MILESTONE_33_TASK_2_TASK_2_SIGNATURE": report["task_2_signature"],
        "MILESTONE_33_TASK_2_SCOPE_LOCK_INSTANCE_ID": report["scope_lock_instance_id"],
        "MILESTONE_33_TASK_2_SCOPE_LOCK_SIGNATURE": report["scope_lock_signature"],
        "MILESTONE_33_TASK_2_ARC_AGI3_INTERACTIVE_RUNTIME_BOUNDARY": report["arc_agi3_interactive_runtime_boundary"],
        "MILESTONE_33_TASK_2_PLANNING_TRACE_REQUIRED": report["planning_trace_required"],
        "MILESTONE_33_TASK_2_ACTION_OBSERVATION_EVENT_TRACE_REQUIRED": report["action_observation_event_trace_required"],
        "MILESTONE_33_TASK_2_GOAL_INFERENCE_BOUNDARY_REQUIRED": report["goal_inference_boundary_required"],
        "MILESTONE_33_TASK_2_MEMORY_STATE_BOUNDARY_REQUIRED": report["memory_state_boundary_required"],
        "MILESTONE_33_TASK_2_TECHNICAL_TRACE_ARTIFACT_ONLY": report["technical_trace_artifact_only"],
        "MILESTONE_33_TASK_2_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_33_TASK_2_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_33_TASK_2_SCOPE_LOCK_STATUS": report["scope_lock_status"],
        "MILESTONE_33_TASK_2_SCOPE_LOCK_CASE_COUNT": report["scope_lock_case_count"],
        "MILESTONE_33_TASK_2_PASS_COUNT": report["pass_count"],
        "MILESTONE_33_TASK_2_FAIL_COUNT": report["fail_count"],
        "MILESTONE_33_TASK_2_SCOPE_LOCK_PASSED": report["scope_lock_passed"],
        "MILESTONE_33_TASK_2_TASK_BUDGET_MAX": report["task_budget_max"],
        "MILESTONE_33_TASK_2_CURRENT_TASK_NUMBER": report["current_task_number"],
        "MILESTONE_33_TASK_2_GENERATED_ARTIFACT_COUNT": report["generated_artifact_count"],
        "MILESTONE_33_TASK_2_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        if isinstance(value, bool):
            value = _bool_marker(value)
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
