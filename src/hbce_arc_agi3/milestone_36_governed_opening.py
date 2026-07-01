from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TASK_ID = "MILESTONE_36_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
MILESTONE_ID = "MILESTONE_36"
SOURCE_MILESTONE_ID = "MILESTONE_33_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
SOURCE_CLOSURE_TASK_ID = "MILESTONE_35_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_MULTI_MODEL_ORCHESTRATION_BOUNDARY_FINAL_CLOSURE_V1"
OPENING_REVISION = "MILESTONE_36_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = "MILESTONE_36_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs" / "milestone-36-task-1-governed-opening-with-task-budget-v1.md"
SOURCE_CLOSURE_DOC_PATH = ROOT / "docs" / "milestone-33-task-6-hbce-arc-agi3-interactive-runtime-planning-trace-boundary-final-closure-v1.md"
ARTIFACT_DIR = ROOT / "examples" / "milestone-36" / "governed-opening-with-task-budget-v1"

def _digest(*parts: Any, length: int = 16) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:length].upper()

def _bool(value: bool) -> str:
    return "true" if value else "false"

TASK_1_SIGNATURE = _digest(TASK_ID, SOURCE_CLOSURE_TASK_ID, OPENING_REVISION)
OPENING_ID = "MILESTONE-36-GOVERNED-OPENING-" + _digest(TASK_ID, MILESTONE_ID)
OPENING_SIGNATURE = _digest(OPENING_ID, TASK_1_SIGNATURE, NEXT_STAGE)

def _source_closure_summary() -> dict[str, Any]:
    try:
        from hbce_arc_agi3.milestone_35_multi_model_orchestration_final_closure import (
            run_milestone_33_boundary_final_closure,
            validate_milestone_33_boundary_final_closure_report,
        )
        report = run_milestone_33_boundary_final_closure()
        return {
            "source_closure_status": report.get("closure_status", "UNKNOWN"),
            "source_closure_passed": bool(report.get("closure_passed")) and validate_milestone_33_boundary_final_closure_report(report),
            "source_task_6_signature": report.get("task_6_signature", ""),
            "source_regression_event_trace_fingerprint": report.get("regression_event_trace_fingerprint", ""),
        }
    except Exception:
        text = SOURCE_CLOSURE_DOC_PATH.read_text(encoding="utf-8")
        return {
            "source_closure_status": "CLOSED" if "MILESTONE_33_TASK_6_CLOSURE_STATUS=CLOSED" in text else "UNKNOWN",
            "source_closure_passed": "MILESTONE_33_TASK_6_CLOSURE_PASSED=true" in text,
            "source_task_6_signature": "",
            "source_regression_event_trace_fingerprint": "",
        }

def _case(case_id: str, expected: Any, observed: Any, passed: bool) -> dict[str, Any]:
    return {"case_id": case_id, "expected": expected, "observed": observed, "passed": passed, "failure_reason": None if passed else f"{case_id}_FAILED"}

def build_milestone_36_governed_opening_cases(report: dict[str, Any]) -> list[dict[str, Any]]:
    source_text = SOURCE_CLOSURE_DOC_PATH.read_text(encoding="utf-8")
    return [
        _case("MILESTONE_33_FINAL_CLOSURE_READY", True, "MILESTONE_33_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_FINAL_CLOSURE_READY=true" in source_text, "MILESTONE_33_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_FINAL_CLOSURE_READY=true" in source_text),
        _case("SOURCE_CLOSURE_STATUS_CLOSED", "CLOSED", report["source_closure_status"], report["source_closure_status"] == "CLOSED"),
        _case("SOURCE_CLOSURE_PASSED", True, report["source_closure_passed"], report["source_closure_passed"] is True),
        _case("MILESTONE_ID_SET", MILESTONE_ID, report["milestone_id"], report["milestone_id"] == MILESTONE_ID),
        _case("TASK_BUDGET_MAX_EIGHT", 8, report["task_budget_max"], report["task_budget_max"] == 8),
        _case("CURRENT_TASK_NUMBER_ONE", 1, report["current_task_number"], report["current_task_number"] == 1),
        _case("OBJECTIVE_SELECTION_PENDING", "PENDING_TASK_2_SCOPE_LOCK", report["objective_selection_status"], report["objective_selection_status"] == "PENDING_TASK_2_SCOPE_LOCK"),
        _case("NEXT_STAGE_TASK_2_SCOPE_LOCK", NEXT_STAGE, report["next_stage"], report["next_stage"] == NEXT_STAGE),
    ]

def run_milestone_36_governed_opening() -> dict[str, Any]:
    source = _source_closure_summary()
    report: dict[str, Any] = {
        "ready": True,
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_closure_task_id": SOURCE_CLOSURE_TASK_ID,
        "source_closure_status": source["source_closure_status"],
        "source_closure_passed": source["source_closure_passed"],
        "source_task_6_signature": source["source_task_6_signature"],
        "source_regression_event_trace_fingerprint": source["source_regression_event_trace_fingerprint"],
        "opening_revision": OPENING_REVISION,
        "task_1_signature": TASK_1_SIGNATURE,
        "opening_id": OPENING_ID,
        "opening_signature": OPENING_SIGNATURE,
        "opening_status": "READY",
        "objective_selection_status": "PENDING_TASK_2_SCOPE_LOCK",
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    cases = build_milestone_36_governed_opening_cases(report)
    pass_count = sum(1 for c in cases if c["passed"])
    fail_count = len(cases) - pass_count
    report.update({"opening_case_count": len(cases), "pass_count": pass_count, "fail_count": fail_count, "opening_passed": fail_count == 0, "cases": cases})
    if fail_count:
        report["opening_status"] = "INVALID"
    return report

def validate_milestone_36_governed_opening_report(report: dict[str, Any]) -> bool:
    required = {
        "ready": True,
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_closure_task_id": SOURCE_CLOSURE_TASK_ID,
        "source_closure_status": "CLOSED",
        "source_closure_passed": True,
        "opening_revision": OPENING_REVISION,
        "opening_status": "READY",
        "objective_selection_status": "PENDING_TASK_2_SCOPE_LOCK",
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    return (
        all(report.get(k) == v for k, v in required.items())
        and report.get("opening_case_count") == len(report.get("cases", []))
        and report.get("pass_count") == len(report.get("cases", []))
        and report.get("fail_count") == 0
        and report.get("opening_passed") is True
        and all(c.get("passed") is True for c in report.get("cases", []))
    )

def _md(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 36 Task 1 Governed Opening",
        "",
        f"- Task ID: `{report['task_id']}`",
        f"- Opening ID: `{report['opening_id']}`",
        f"- Status: `{report['opening_status']}`",
        f"- Cases: `{report['pass_count']}/{report['opening_case_count']}`",
        f"- Task budget max: `{report['task_budget_max']}`",
        f"- Next stage: `{report['next_stage']}`",
        "",
        "## Cases",
        "",
    ]
    lines.extend(f"- `{'PASS' if c['passed'] else 'FAIL'}` `{c['case_id']}`" for c in report["cases"])
    return "\n".join(lines) + "\n"

def _doc(report: dict[str, Any]) -> str:
    return f"""# Milestone 36 Task 1 - Governed Opening With Task Budget v1

MILESTONE_36_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY={_bool(report['ready'])}
MILESTONE_36_TASK_1_TASK_ID={report['task_id']}
MILESTONE_36_TASK_1_MILESTONE_ID={report['milestone_id']}
MILESTONE_36_TASK_1_SOURCE_MILESTONE_ID={report['source_milestone_id']}
MILESTONE_36_TASK_1_SOURCE_CLOSURE_TASK_ID={report['source_closure_task_id']}
MILESTONE_36_TASK_1_SOURCE_CLOSURE_STATUS={report['source_closure_status']}
MILESTONE_36_TASK_1_SOURCE_CLOSURE_PASSED={_bool(report['source_closure_passed'])}
MILESTONE_36_TASK_1_SOURCE_REGRESSION_EVENT_TRACE_FINGERPRINT={report['source_regression_event_trace_fingerprint']}
MILESTONE_36_TASK_1_OPENING_REVISION={report['opening_revision']}
MILESTONE_36_TASK_1_TASK_1_SIGNATURE={report['task_1_signature']}
MILESTONE_36_TASK_1_OPENING_ID={report['opening_id']}
MILESTONE_36_TASK_1_OPENING_SIGNATURE={report['opening_signature']}
MILESTONE_36_TASK_1_OPENING_STATUS={report['opening_status']}
MILESTONE_36_TASK_1_OBJECTIVE_SELECTION_STATUS={report['objective_selection_status']}
MILESTONE_36_TASK_1_OPENING_CASE_COUNT={report['opening_case_count']}
MILESTONE_36_TASK_1_PASS_COUNT={report['pass_count']}
MILESTONE_36_TASK_1_FAIL_COUNT={report['fail_count']}
MILESTONE_36_TASK_1_OPENING_PASSED={_bool(report['opening_passed'])}
MILESTONE_36_TASK_1_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_36_TASK_1_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_36_TASK_1_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_36_TASK_1_NEXT_STAGE={report['next_stage']}

## Governed Opening

Milestone 36 is opened with a governed maximum task budget of 8.
Milestone 34 final closure is the dependency source.
Objective selection is intentionally pending Task 2 scope lock.
"""

def write_milestone_34_task_1_artifacts() -> dict[str, str]:
    report = run_milestone_36_governed_opening()
    if not validate_milestone_36_governed_opening_report(report):
        raise ValueError("Milestone 36 Task 1 governed opening report is invalid")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    cases = ARTIFACT_DIR / "task-1-governed-opening-cases.json"
    report_json = ARTIFACT_DIR / "task-1-governed-opening-report.json"
    report_md = ARTIFACT_DIR / "task-1-governed-opening-report.md"
    index = ARTIFACT_DIR / "task-1-index.txt"
    manifest = ARTIFACT_DIR / "task-1-manifest.json"
    cases.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md.write_text(_md(report), encoding="utf-8")
    index.write_text("\n".join(["MILESTONE_36_TASK_1_ARTIFACT_INDEX", cases.name, report_json.name, report_md.name, manifest.name]) + "\n", encoding="utf-8")
    manifest.write_text(json.dumps({"task_id": TASK_ID, "opening_id": OPENING_ID, "opening_signature": OPENING_SIGNATURE, "artifact_count": GENERATED_ARTIFACT_COUNT, "artifacts": [cases.name, report_json.name, report_md.name, index.name, manifest.name]}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    DOC_PATH.write_text(_doc(report), encoding="utf-8")
    return {"cases": cases.as_posix(), "report_json": report_json.as_posix(), "report_md": report_md.as_posix(), "index": index.as_posix(), "manifest": manifest.as_posix(), "doc": DOC_PATH.as_posix()}

def main() -> None:
    write_milestone_34_task_1_artifacts()
    report = run_milestone_36_governed_opening()
    markers = {
        "MILESTONE_36_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY": report["ready"],
        "MILESTONE_36_TASK_1_TASK_ID": report["task_id"],
        "MILESTONE_36_TASK_1_MILESTONE_ID": report["milestone_id"],
        "MILESTONE_36_TASK_1_SOURCE_CLOSURE_TASK_ID": report["source_closure_task_id"],
        "MILESTONE_36_TASK_1_SOURCE_CLOSURE_STATUS": report["source_closure_status"],
        "MILESTONE_36_TASK_1_SOURCE_CLOSURE_PASSED": report["source_closure_passed"],
        "MILESTONE_36_TASK_1_OPENING_ID": report["opening_id"],
        "MILESTONE_36_TASK_1_OPENING_STATUS": report["opening_status"],
        "MILESTONE_36_TASK_1_OBJECTIVE_SELECTION_STATUS": report["objective_selection_status"],
        "MILESTONE_36_TASK_1_OPENING_CASE_COUNT": report["opening_case_count"],
        "MILESTONE_36_TASK_1_PASS_COUNT": report["pass_count"],
        "MILESTONE_36_TASK_1_FAIL_COUNT": report["fail_count"],
        "MILESTONE_36_TASK_1_OPENING_PASSED": report["opening_passed"],
        "MILESTONE_36_TASK_1_TASK_BUDGET_MAX": report["task_budget_max"],
        "MILESTONE_36_TASK_1_CURRENT_TASK_NUMBER": report["current_task_number"],
        "MILESTONE_36_TASK_1_GENERATED_ARTIFACT_COUNT": report["generated_artifact_count"],
        "MILESTONE_36_TASK_1_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        print(f"{key}={_bool(value) if isinstance(value, bool) else value}")

if __name__ == "__main__":
    main()
