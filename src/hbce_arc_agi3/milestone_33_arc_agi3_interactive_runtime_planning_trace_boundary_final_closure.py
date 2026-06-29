from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TASK_ID = "MILESTONE_33_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_FINAL_CLOSURE_V1"
SOURCE_REGRESSION_TASK_ID = "MILESTONE_33_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_REGRESSION_INTEGRATION_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
SCOPE_LOCK_ID = "MILESTONE_33_SCOPE_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
RUNTIME_MODE_ID = "ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY"
FINAL_CLOSURE_REVISION = "MILESTONE_33_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_FINAL_CLOSURE_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 6
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = "MILESTONE_34_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs" / "milestone-33-task-6-hbce-arc-agi3-interactive-runtime-planning-trace-boundary-final-closure-v1.md"
SOURCE_REGRESSION_DOC_PATH = ROOT / "docs" / "milestone-33-task-5-hbce-arc-agi3-interactive-runtime-planning-trace-boundary-regression-integration-v1.md"
ARTIFACT_DIR = ROOT / "examples" / "milestone-33" / "hbce-arc-agi3-interactive-runtime-planning-trace-boundary-final-closure-v1"

def _digest(*parts: Any, length: int = 16) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:length].upper()

def _bool(value: bool) -> str:
    return "true" if value else "false"

TASK_6_SIGNATURE = _digest(TASK_ID, SELECTED_OBJECTIVE_ID, FINAL_CLOSURE_REVISION)
CLOSURE_ID = "MILESTONE-33-ARC-AGI3-INTERACTIVE-RUNTIME-FINAL-CLOSURE-" + _digest(SCOPE_LOCK_ID, RUNTIME_MODE_ID)
CLOSURE_SIGNATURE = _digest(CLOSURE_ID, TASK_6_SIGNATURE, NEXT_STAGE)

def _source_integration_report() -> dict[str, Any]:
    from hbce_arc_agi3.milestone_33_arc_agi3_interactive_runtime_planning_trace_boundary_regression_integration import (
        run_milestone_33_boundary_regression_integration,
        validate_milestone_33_boundary_regression_integration_report,
    )
    report = run_milestone_33_boundary_regression_integration()
    report["_integration_report_valid"] = validate_milestone_33_boundary_regression_integration_report(report)
    return report

def _case(case_id: str, expected: Any, observed: Any, passed: bool) -> dict[str, Any]:
    return {"case_id": case_id, "expected": expected, "observed": observed, "passed": passed, "failure_reason": None if passed else f"{case_id}_FAILED"}

def build_milestone_33_boundary_final_closure_cases(report: dict[str, Any]) -> list[dict[str, Any]]:
    source_text = SOURCE_REGRESSION_DOC_PATH.read_text(encoding="utf-8")
    source = report["source_integration_report"]
    snapshot = source.get("regression_snapshot", {})
    return [
        _case("TASK_5_REGRESSION_READY", True, "MILESTONE_33_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_REGRESSION_INTEGRATION_READY=true" in source_text, "MILESTONE_33_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_REGRESSION_INTEGRATION_READY=true" in source_text),
        _case("SOURCE_INTEGRATION_STATUS_VALID", "VALID", report["source_integration_status"], report["source_integration_status"] == "VALID"),
        _case("SOURCE_INTEGRATION_PASSED", True, report["source_integration_passed"], report["source_integration_passed"] is True),
        _case("SOURCE_INTEGRATION_REPORT_VALID", True, source.get("_integration_report_valid"), source.get("_integration_report_valid") is True),
        _case("OBJECTIVE_CLOSED", SELECTED_OBJECTIVE_ID, report["selected_objective_id"], report["selected_objective_id"] == SELECTED_OBJECTIVE_ID),
        _case("SCOPE_LOCK_CLOSED", SCOPE_LOCK_ID, report["scope_lock_id"], report["scope_lock_id"] == SCOPE_LOCK_ID),
        _case("REGRESSION_EVENT_COUNT_CLOSED", 4, snapshot.get("event_count"), snapshot.get("event_count") == 4),
        _case("REGRESSION_FINGERPRINT_CLOSED", "non-empty", snapshot.get("event_trace_fingerprint"), bool(snapshot.get("event_trace_fingerprint"))),
        _case("PLANNING_TRACE_BOUNDARY_CLOSED", True, report["planning_trace_required"], report["planning_trace_required"] is True),
        _case("ACTION_OBSERVATION_TRACE_BOUNDARY_CLOSED", True, report["action_observation_event_trace_required"], report["action_observation_event_trace_required"] is True),
        _case("GOAL_INFERENCE_BOUNDARY_CLOSED", True, report["goal_inference_boundary_required"], report["goal_inference_boundary_required"] is True),
        _case("MEMORY_STATE_BOUNDARY_CLOSED", True, report["memory_state_boundary_required"], report["memory_state_boundary_required"] is True),
        _case("LEGAL_CERTIFICATION_FALSE", False, report["legal_certification"], report["legal_certification"] is False),
        _case("KAGGLE_SCORE_CLAIM_FALSE", False, report["kaggle_score_claim"], report["kaggle_score_claim"] is False),
        _case("RUNTIME_SIDE_EFFECTS_DENIED", True, report["network_access_allowed"] is False and report["shell_execution_allowed"] is False and report["repository_mutation_allowed"] is False, report["network_access_allowed"] is False and report["shell_execution_allowed"] is False and report["repository_mutation_allowed"] is False),
        _case("NEXT_STAGE_MILESTONE_34_OPENING", NEXT_STAGE, report["next_stage"], report["next_stage"] == NEXT_STAGE),
    ]

def run_milestone_33_boundary_final_closure() -> dict[str, Any]:
    source = _source_integration_report()
    report: dict[str, Any] = {
        "ready": True,
        "task_id": TASK_ID,
        "source_regression_task_id": SOURCE_REGRESSION_TASK_ID,
        "source_integration_status": source.get("integration_status"),
        "source_integration_passed": bool(source.get("integration_passed")) and bool(source.get("_integration_report_valid")),
        "source_integration_case_count": source.get("integration_case_count"),
        "source_pass_count": source.get("pass_count"),
        "source_fail_count": source.get("fail_count"),
        "source_task_5_signature": source.get("task_5_signature", ""),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "runtime_mode_id": RUNTIME_MODE_ID,
        "final_closure_revision": FINAL_CLOSURE_REVISION,
        "task_6_signature": TASK_6_SIGNATURE,
        "closure_id": CLOSURE_ID,
        "closure_signature": CLOSURE_SIGNATURE,
        "closure_status": "CLOSED",
        "arc_agi3_interactive_runtime_boundary": source.get("arc_agi3_interactive_runtime_boundary"),
        "planning_trace_required": source.get("planning_trace_required"),
        "action_observation_event_trace_required": source.get("action_observation_event_trace_required"),
        "goal_inference_boundary_required": source.get("goal_inference_boundary_required"),
        "memory_state_boundary_required": source.get("memory_state_boundary_required"),
        "technical_trace_artifact_only": source.get("technical_trace_artifact_only"),
        "legal_certification": source.get("legal_certification"),
        "kaggle_score_claim": source.get("kaggle_score_claim"),
        "network_access_allowed": source.get("network_access_allowed"),
        "shell_execution_allowed": source.get("shell_execution_allowed"),
        "repository_mutation_allowed": source.get("repository_mutation_allowed"),
        "regression_event_count": source.get("regression_snapshot", {}).get("event_count"),
        "regression_event_trace_fingerprint": source.get("regression_snapshot", {}).get("event_trace_fingerprint"),
        "source_integration_report": source,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    cases = build_milestone_33_boundary_final_closure_cases(report)
    pass_count = sum(1 for c in cases if c["passed"])
    fail_count = len(cases) - pass_count
    report.update({"closure_case_count": len(cases), "pass_count": pass_count, "fail_count": fail_count, "closure_passed": fail_count == 0, "cases": cases})
    if fail_count:
        report["closure_status"] = "INVALID"
    return report

def validate_milestone_33_boundary_final_closure_report(report: dict[str, Any]) -> bool:
    required = {
        "ready": True, "task_id": TASK_ID, "source_regression_task_id": SOURCE_REGRESSION_TASK_ID,
        "source_integration_status": "VALID", "source_integration_passed": True,
        "selected_objective_id": SELECTED_OBJECTIVE_ID, "scope_lock_id": SCOPE_LOCK_ID,
        "runtime_mode_id": RUNTIME_MODE_ID, "final_closure_revision": FINAL_CLOSURE_REVISION,
        "closure_status": "CLOSED", "planning_trace_required": True,
        "action_observation_event_trace_required": True, "goal_inference_boundary_required": True,
        "memory_state_boundary_required": True, "technical_trace_artifact_only": True,
        "legal_certification": False, "kaggle_score_claim": False,
        "network_access_allowed": False, "shell_execution_allowed": False,
        "repository_mutation_allowed": False, "regression_event_count": 4,
        "task_budget_max": TASK_BUDGET_MAX, "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT, "next_stage": NEXT_STAGE,
    }
    return (
        all(report.get(k) == v for k, v in required.items())
        and bool(report.get("regression_event_trace_fingerprint"))
        and report.get("closure_case_count") == len(report.get("cases", []))
        and report.get("pass_count") == len(report.get("cases", []))
        and report.get("fail_count") == 0
        and report.get("closure_passed") is True
        and all(c.get("passed") is True for c in report.get("cases", []))
    )

def _md(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 33 Task 6 Boundary Final Closure", "",
        f"- Task ID: `{report['task_id']}`",
        f"- Closure ID: `{report['closure_id']}`",
        f"- Status: `{report['closure_status']}`",
        f"- Cases: `{report['pass_count']}/{report['closure_case_count']}`",
        f"- Regression fingerprint: `{report['regression_event_trace_fingerprint']}`",
        "- legalCertification=false.",
        "- kaggleScoreClaim=false.", "", "## Cases", "",
    ]
    lines.extend(f"- `{'PASS' if c['passed'] else 'FAIL'}` `{c['case_id']}`" for c in report["cases"])
    return "\n".join(lines) + "\n"

def _doc(report: dict[str, Any]) -> str:
    return f"""# Milestone 33 Task 6 - HBCE ARC AGI3 Interactive Runtime Planning Trace Boundary Final Closure v1

MILESTONE_33_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_FINAL_CLOSURE_READY={_bool(report['ready'])}
MILESTONE_33_TASK_6_TASK_ID={report['task_id']}
MILESTONE_33_TASK_6_SOURCE_REGRESSION_TASK_ID={report['source_regression_task_id']}
MILESTONE_33_TASK_6_SOURCE_INTEGRATION_STATUS={report['source_integration_status']}
MILESTONE_33_TASK_6_SOURCE_INTEGRATION_PASSED={_bool(report['source_integration_passed'])}
MILESTONE_33_TASK_6_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_33_TASK_6_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_33_TASK_6_RUNTIME_MODE_ID={report['runtime_mode_id']}
MILESTONE_33_TASK_6_FINAL_CLOSURE_REVISION={report['final_closure_revision']}
MILESTONE_33_TASK_6_TASK_6_SIGNATURE={report['task_6_signature']}
MILESTONE_33_TASK_6_CLOSURE_ID={report['closure_id']}
MILESTONE_33_TASK_6_CLOSURE_SIGNATURE={report['closure_signature']}
MILESTONE_33_TASK_6_CLOSURE_STATUS={report['closure_status']}
MILESTONE_33_TASK_6_CLOSURE_CASE_COUNT={report['closure_case_count']}
MILESTONE_33_TASK_6_PASS_COUNT={report['pass_count']}
MILESTONE_33_TASK_6_FAIL_COUNT={report['fail_count']}
MILESTONE_33_TASK_6_CLOSURE_PASSED={_bool(report['closure_passed'])}
MILESTONE_33_TASK_6_ARC_AGI3_INTERACTIVE_RUNTIME_BOUNDARY={_bool(report['arc_agi3_interactive_runtime_boundary'])}
MILESTONE_33_TASK_6_PLANNING_TRACE_REQUIRED={_bool(report['planning_trace_required'])}
MILESTONE_33_TASK_6_ACTION_OBSERVATION_EVENT_TRACE_REQUIRED={_bool(report['action_observation_event_trace_required'])}
MILESTONE_33_TASK_6_GOAL_INFERENCE_BOUNDARY_REQUIRED={_bool(report['goal_inference_boundary_required'])}
MILESTONE_33_TASK_6_MEMORY_STATE_BOUNDARY_REQUIRED={_bool(report['memory_state_boundary_required'])}
MILESTONE_33_TASK_6_TECHNICAL_TRACE_ARTIFACT_ONLY={_bool(report['technical_trace_artifact_only'])}
MILESTONE_33_TASK_6_LEGAL_CERTIFICATION={_bool(report['legal_certification'])}
MILESTONE_33_TASK_6_KAGGLE_SCORE_CLAIM={_bool(report['kaggle_score_claim'])}
MILESTONE_33_TASK_6_NETWORK_ACCESS_ALLOWED={_bool(report['network_access_allowed'])}
MILESTONE_33_TASK_6_SHELL_EXECUTION_ALLOWED={_bool(report['shell_execution_allowed'])}
MILESTONE_33_TASK_6_REPOSITORY_MUTATION_ALLOWED={_bool(report['repository_mutation_allowed'])}
MILESTONE_33_TASK_6_REGRESSION_EVENT_COUNT={report['regression_event_count']}
MILESTONE_33_TASK_6_REGRESSION_EVENT_TRACE_FINGERPRINT={report['regression_event_trace_fingerprint']}
MILESTONE_33_TASK_6_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_33_TASK_6_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_33_TASK_6_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_33_TASK_6_NEXT_STAGE={report['next_stage']}

## Final Closure Boundary

Milestone 33 is closed for the HBCE ARC-AGI-3 interactive runtime planning trace boundary.
The closed boundary preserves planning trace, action/observation trace, goal inference boundary,
memory state boundary, regression fingerprint, local-only side-effect denial, and explicit
legal/Kaggle claim denial.

Generated runtime traces are technical artifacts only.
legalCertification=false.
kaggleScoreClaim=false.
"""

def write_milestone_33_task_6_artifacts() -> dict[str, str]:
    report = run_milestone_33_boundary_final_closure()
    if not validate_milestone_33_boundary_final_closure_report(report):
        raise ValueError("Milestone 33 Task 6 boundary final closure report is invalid")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    cases = ARTIFACT_DIR / "task-6-boundary-final-closure-cases.json"
    report_json = ARTIFACT_DIR / "task-6-boundary-final-closure-report.json"
    report_md = ARTIFACT_DIR / "task-6-boundary-final-closure-report.md"
    index = ARTIFACT_DIR / "task-6-index.txt"
    manifest = ARTIFACT_DIR / "task-6-manifest.json"
    cases.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md.write_text(_md(report), encoding="utf-8")
    index.write_text("\n".join(["MILESTONE_33_TASK_6_ARTIFACT_INDEX", cases.name, report_json.name, report_md.name, manifest.name]) + "\n", encoding="utf-8")
    manifest.write_text(json.dumps({"task_id": TASK_ID, "closure_id": CLOSURE_ID, "closure_signature": CLOSURE_SIGNATURE, "artifact_count": GENERATED_ARTIFACT_COUNT, "artifacts": [cases.name, report_json.name, report_md.name, index.name, manifest.name]}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    DOC_PATH.write_text(_doc(report), encoding="utf-8")
    return {"cases": cases.as_posix(), "report_json": report_json.as_posix(), "report_md": report_md.as_posix(), "index": index.as_posix(), "manifest": manifest.as_posix(), "doc": DOC_PATH.as_posix()}

def main() -> None:
    write_milestone_33_task_6_artifacts()
    report = run_milestone_33_boundary_final_closure()
    markers = {
        "MILESTONE_33_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_FINAL_CLOSURE_READY": report["ready"],
        "MILESTONE_33_TASK_6_TASK_ID": report["task_id"],
        "MILESTONE_33_TASK_6_SOURCE_REGRESSION_TASK_ID": report["source_regression_task_id"],
        "MILESTONE_33_TASK_6_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_33_TASK_6_CLOSURE_ID": report["closure_id"],
        "MILESTONE_33_TASK_6_CLOSURE_STATUS": report["closure_status"],
        "MILESTONE_33_TASK_6_CLOSURE_CASE_COUNT": report["closure_case_count"],
        "MILESTONE_33_TASK_6_PASS_COUNT": report["pass_count"],
        "MILESTONE_33_TASK_6_FAIL_COUNT": report["fail_count"],
        "MILESTONE_33_TASK_6_CLOSURE_PASSED": report["closure_passed"],
        "MILESTONE_33_TASK_6_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_33_TASK_6_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_33_TASK_6_REGRESSION_EVENT_TRACE_FINGERPRINT": report["regression_event_trace_fingerprint"],
        "MILESTONE_33_TASK_6_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        print(f"{key}={_bool(value) if isinstance(value, bool) else value}")

if __name__ == "__main__":
    main()
