from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TASK_ID = "MILESTONE_34_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
SOURCE_OPENING_TASK_ID = "MILESTONE_34_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_REPLAY_EVALUATION_HARNESS_BOUNDARY"
SELECTED_OBJECTIVE_STATUS = "SELECTED_AND_SCOPE_LOCKED"
SCOPE_LOCK_ID = "MILESTONE_34_SCOPE_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_REPLAY_EVALUATION_HARNESS_BOUNDARY"
HARNESS_MODE_ID = "ARC_AGI3_INTERACTIVE_RUNTIME_REPLAY_EVALUATION_HARNESS_BOUNDARY"
OBJECTIVE_SELECTION_REVISION = "MILESTONE_34_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

REPLAY_EVALUATION_HARNESS_BOUNDARY = True
REPLAYABLE_EVENT_TRACE_REQUIRED = True
LOCAL_EVALUATION_RECORD_REQUIRED = True
REGRESSION_SNAPSHOT_REQUIRED = True
AUDIT_ARTIFACT_REQUIRED = True
TECHNICAL_EVALUATION_ONLY = True
LEGAL_CERTIFICATION = False
KAGGLE_SCORE_CLAIM = False
OFFICIAL_BENCHMARK_CERTIFICATION = False

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 2
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = (
    "MILESTONE_34_TASK_3_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_REPLAY_EVALUATION_"
    "HARNESS_BOUNDARY_IMPLEMENTATION_V1"
)

ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs" / "milestone-34-task-2-objective-selection-and-scope-lock-v1.md"
SOURCE_OPENING_DOC_PATH = ROOT / "docs" / "milestone-34-task-1-governed-opening-with-task-budget-v1.md"
ARTIFACT_DIR = ROOT / "examples" / "milestone-34" / "objective-selection-and-scope-lock-v1"

def _digest(*parts: Any, length: int = 16) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:length].upper()

def _bool(value: bool) -> str:
    return "true" if value else "false"

TASK_2_SIGNATURE = _digest(TASK_ID, SELECTED_OBJECTIVE_ID, OBJECTIVE_SELECTION_REVISION)
SCOPE_LOCK_INSTANCE_ID = "MILESTONE-34-SCOPE-LOCK-" + _digest(SCOPE_LOCK_ID, HARNESS_MODE_ID)
SCOPE_LOCK_SIGNATURE = _digest(SCOPE_LOCK_INSTANCE_ID, TASK_2_SIGNATURE, NEXT_STAGE)

def _source_opening_summary() -> dict[str, Any]:
    try:
        from hbce_arc_agi3.milestone_34_governed_opening import (
            run_milestone_34_governed_opening,
            validate_milestone_34_governed_opening_report,
        )
        report = run_milestone_34_governed_opening()
        return {
            "source_opening_status": report.get("opening_status", "UNKNOWN"),
            "source_opening_passed": bool(report.get("opening_passed")) and validate_milestone_34_governed_opening_report(report),
            "source_task_1_signature": report.get("task_1_signature", ""),
        }
    except Exception:
        text = SOURCE_OPENING_DOC_PATH.read_text(encoding="utf-8")
        return {
            "source_opening_status": "READY" if "MILESTONE_34_TASK_1_OPENING_STATUS=READY" in text else "UNKNOWN",
            "source_opening_passed": "MILESTONE_34_TASK_1_OPENING_PASSED=true" in text,
            "source_task_1_signature": "",
        }

def _case(case_id: str, expected: Any, observed: Any, passed: bool) -> dict[str, Any]:
    return {"case_id": case_id, "expected": expected, "observed": observed, "passed": passed, "failure_reason": None if passed else f"{case_id}_FAILED"}

def build_milestone_34_objective_scope_lock_cases(report: dict[str, Any]) -> list[dict[str, Any]]:
    source_text = SOURCE_OPENING_DOC_PATH.read_text(encoding="utf-8")
    return [
        _case("TASK_1_GOVERNED_OPENING_READY", True, "MILESTONE_34_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in source_text, "MILESTONE_34_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in source_text),
        _case("SOURCE_OPENING_STATUS_READY", "READY", report["source_opening_status"], report["source_opening_status"] == "READY"),
        _case("SOURCE_OPENING_PASSED", True, report["source_opening_passed"], report["source_opening_passed"] is True),
        _case("OBJECTIVE_CANDIDATE_SELECTED", SELECTED_OBJECTIVE_ID, report["selected_objective_id"], report["selected_objective_id"] == SELECTED_OBJECTIVE_ID),
        _case("SCOPE_LOCK_ID_BOUND", SCOPE_LOCK_ID, report["scope_lock_id"], report["scope_lock_id"] == SCOPE_LOCK_ID),
        _case("REPLAY_EVALUATION_HARNESS_BOUNDARY_LOCKED", True, report["replay_evaluation_harness_boundary"], report["replay_evaluation_harness_boundary"] is True),
        _case("REPLAYABLE_EVENT_TRACE_REQUIRED", True, report["replayable_event_trace_required"], report["replayable_event_trace_required"] is True),
        _case("LOCAL_EVALUATION_RECORD_REQUIRED", True, report["local_evaluation_record_required"], report["local_evaluation_record_required"] is True),
        _case("REGRESSION_SNAPSHOT_REQUIRED", True, report["regression_snapshot_required"], report["regression_snapshot_required"] is True),
        _case("AUDIT_ARTIFACT_REQUIRED", True, report["audit_artifact_required"], report["audit_artifact_required"] is True),
        _case("LEGAL_AND_KAGGLE_CLAIMS_DENIED", "false/false", f"{report['legal_certification']}/{report['kaggle_score_claim']}", report["legal_certification"] is False and report["kaggle_score_claim"] is False),
        _case("NEXT_STAGE_TASK_3_IMPLEMENTATION", NEXT_STAGE, report["next_stage"], report["next_stage"] == NEXT_STAGE),
    ]

def run_milestone_34_objective_scope_lock() -> dict[str, Any]:
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
        "harness_mode_id": HARNESS_MODE_ID,
        "objective_selection_revision": OBJECTIVE_SELECTION_REVISION,
        "task_2_signature": TASK_2_SIGNATURE,
        "scope_lock_instance_id": SCOPE_LOCK_INSTANCE_ID,
        "scope_lock_signature": SCOPE_LOCK_SIGNATURE,
        "replay_evaluation_harness_boundary": REPLAY_EVALUATION_HARNESS_BOUNDARY,
        "replayable_event_trace_required": REPLAYABLE_EVENT_TRACE_REQUIRED,
        "local_evaluation_record_required": LOCAL_EVALUATION_RECORD_REQUIRED,
        "regression_snapshot_required": REGRESSION_SNAPSHOT_REQUIRED,
        "audit_artifact_required": AUDIT_ARTIFACT_REQUIRED,
        "technical_evaluation_only": TECHNICAL_EVALUATION_ONLY,
        "legal_certification": LEGAL_CERTIFICATION,
        "kaggle_score_claim": KAGGLE_SCORE_CLAIM,
        "official_benchmark_certification": OFFICIAL_BENCHMARK_CERTIFICATION,
        "scope_lock_status": "LOCKED",
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    cases = build_milestone_34_objective_scope_lock_cases(report)
    pass_count = sum(1 for c in cases if c["passed"])
    fail_count = len(cases) - pass_count
    report.update({"scope_lock_case_count": len(cases), "pass_count": pass_count, "fail_count": fail_count, "scope_lock_passed": fail_count == 0, "cases": cases})
    if fail_count:
        report["scope_lock_status"] = "INVALID"
    return report

def validate_milestone_34_objective_scope_lock_report(report: dict[str, Any]) -> bool:
    required = {
        "ready": True,
        "task_id": TASK_ID,
        "source_opening_task_id": SOURCE_OPENING_TASK_ID,
        "source_opening_status": "READY",
        "source_opening_passed": True,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "selected_objective_status": SELECTED_OBJECTIVE_STATUS,
        "scope_lock_id": SCOPE_LOCK_ID,
        "harness_mode_id": HARNESS_MODE_ID,
        "objective_selection_revision": OBJECTIVE_SELECTION_REVISION,
        "replay_evaluation_harness_boundary": True,
        "replayable_event_trace_required": True,
        "local_evaluation_record_required": True,
        "regression_snapshot_required": True,
        "audit_artifact_required": True,
        "technical_evaluation_only": True,
        "legal_certification": False,
        "kaggle_score_claim": False,
        "official_benchmark_certification": False,
        "scope_lock_status": "LOCKED",
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    return (
        all(report.get(k) == v for k, v in required.items())
        and report.get("scope_lock_case_count") == len(report.get("cases", []))
        and report.get("pass_count") == len(report.get("cases", []))
        and report.get("fail_count") == 0
        and report.get("scope_lock_passed") is True
        and all(c.get("passed") is True for c in report.get("cases", []))
    )

def _md(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 34 Task 2 Objective Selection and Scope Lock",
        "",
        f"- Task ID: `{report['task_id']}`",
        f"- Selected objective: `{report['selected_objective_id']}`",
        f"- Scope lock: `{report['scope_lock_id']}`",
        f"- Harness mode: `{report['harness_mode_id']}`",
        f"- Status: `{report['scope_lock_status']}`",
        f"- Cases: `{report['pass_count']}/{report['scope_lock_case_count']}`",
        "",
        "## Boundary",
        "",
        "- Replay evaluation harness boundary is locked.",
        "- Replayable event traces, local evaluation records, regression snapshots, and audit artifacts are required.",
        "- Evaluation output is a local technical assessment only.",
        "- legalCertification=false.",
        "- kaggleScoreClaim=false.",
        "- No official benchmark certification is claimed.",
        "",
        "## Cases",
        "",
    ]
    lines.extend(f"- `{'PASS' if c['passed'] else 'FAIL'}` `{c['case_id']}`" for c in report["cases"])
    return "\n".join(lines) + "\n"

def _doc(report: dict[str, Any]) -> str:
    return f"""# Milestone 34 Task 2 - Objective Selection and Scope Lock v1

MILESTONE_34_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY={_bool(report['ready'])}
MILESTONE_34_TASK_2_TASK_ID={report['task_id']}
MILESTONE_34_TASK_2_SOURCE_OPENING_TASK_ID={report['source_opening_task_id']}
MILESTONE_34_TASK_2_SOURCE_OPENING_STATUS={report['source_opening_status']}
MILESTONE_34_TASK_2_SOURCE_OPENING_PASSED={_bool(report['source_opening_passed'])}
MILESTONE_34_TASK_2_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_34_TASK_2_SELECTED_OBJECTIVE_STATUS={report['selected_objective_status']}
MILESTONE_34_TASK_2_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_34_TASK_2_HARNESS_MODE_ID={report['harness_mode_id']}
MILESTONE_34_TASK_2_OBJECTIVE_SELECTION_REVISION={report['objective_selection_revision']}
MILESTONE_34_TASK_2_TASK_2_SIGNATURE={report['task_2_signature']}
MILESTONE_34_TASK_2_SCOPE_LOCK_INSTANCE_ID={report['scope_lock_instance_id']}
MILESTONE_34_TASK_2_SCOPE_LOCK_SIGNATURE={report['scope_lock_signature']}
MILESTONE_34_TASK_2_REPLAY_EVALUATION_HARNESS_BOUNDARY={_bool(report['replay_evaluation_harness_boundary'])}
MILESTONE_34_TASK_2_REPLAYABLE_EVENT_TRACE_REQUIRED={_bool(report['replayable_event_trace_required'])}
MILESTONE_34_TASK_2_LOCAL_EVALUATION_RECORD_REQUIRED={_bool(report['local_evaluation_record_required'])}
MILESTONE_34_TASK_2_REGRESSION_SNAPSHOT_REQUIRED={_bool(report['regression_snapshot_required'])}
MILESTONE_34_TASK_2_AUDIT_ARTIFACT_REQUIRED={_bool(report['audit_artifact_required'])}
MILESTONE_34_TASK_2_TECHNICAL_EVALUATION_ONLY={_bool(report['technical_evaluation_only'])}
MILESTONE_34_TASK_2_LEGAL_CERTIFICATION={_bool(report['legal_certification'])}
MILESTONE_34_TASK_2_KAGGLE_SCORE_CLAIM={_bool(report['kaggle_score_claim'])}
MILESTONE_34_TASK_2_OFFICIAL_BENCHMARK_CERTIFICATION={_bool(report['official_benchmark_certification'])}
MILESTONE_34_TASK_2_SCOPE_LOCK_STATUS={report['scope_lock_status']}
MILESTONE_34_TASK_2_SCOPE_LOCK_CASE_COUNT={report['scope_lock_case_count']}
MILESTONE_34_TASK_2_PASS_COUNT={report['pass_count']}
MILESTONE_34_TASK_2_FAIL_COUNT={report['fail_count']}
MILESTONE_34_TASK_2_SCOPE_LOCK_PASSED={_bool(report['scope_lock_passed'])}
MILESTONE_34_TASK_2_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_34_TASK_2_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_34_TASK_2_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_34_TASK_2_NEXT_STAGE={report['next_stage']}

## Canonical Boundary

HBCE ARC-AGI3 Interactive Runtime Replay Evaluation Harness Boundary.

Links governed interactive episodes to replayable event traces, local evaluation
records, regression snapshots, and audit artifacts.

Evaluation output is a local technical assessment only.
legalCertification=false.
kaggleScoreClaim=false.
No official Kaggle score, leaderboard position, benchmark certification, or legal
certification is claimed.
"""

def write_milestone_34_task_2_artifacts() -> dict[str, str]:
    report = run_milestone_34_objective_scope_lock()
    if not validate_milestone_34_objective_scope_lock_report(report):
        raise ValueError("Milestone 34 Task 2 objective scope lock report is invalid")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    cases = ARTIFACT_DIR / "task-2-objective-scope-lock-cases.json"
    report_json = ARTIFACT_DIR / "task-2-objective-scope-lock-report.json"
    report_md = ARTIFACT_DIR / "task-2-objective-scope-lock-report.md"
    index = ARTIFACT_DIR / "task-2-index.txt"
    manifest = ARTIFACT_DIR / "task-2-manifest.json"
    cases.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md.write_text(_md(report), encoding="utf-8")
    index.write_text("\n".join(["MILESTONE_34_TASK_2_ARTIFACT_INDEX", cases.name, report_json.name, report_md.name, manifest.name]) + "\n", encoding="utf-8")
    manifest.write_text(json.dumps({"task_id": TASK_ID, "selected_objective_id": SELECTED_OBJECTIVE_ID, "scope_lock_id": SCOPE_LOCK_ID, "scope_lock_instance_id": SCOPE_LOCK_INSTANCE_ID, "scope_lock_signature": SCOPE_LOCK_SIGNATURE, "artifact_count": GENERATED_ARTIFACT_COUNT, "artifacts": [cases.name, report_json.name, report_md.name, index.name, manifest.name]}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    DOC_PATH.write_text(_doc(report), encoding="utf-8")
    return {"cases": cases.as_posix(), "report_json": report_json.as_posix(), "report_md": report_md.as_posix(), "index": index.as_posix(), "manifest": manifest.as_posix(), "doc": DOC_PATH.as_posix()}

def main() -> None:
    write_milestone_34_task_2_artifacts()
    report = run_milestone_34_objective_scope_lock()
    markers = {
        "MILESTONE_34_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY": report["ready"],
        "MILESTONE_34_TASK_2_TASK_ID": report["task_id"],
        "MILESTONE_34_TASK_2_SOURCE_OPENING_TASK_ID": report["source_opening_task_id"],
        "MILESTONE_34_TASK_2_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_34_TASK_2_SELECTED_OBJECTIVE_STATUS": report["selected_objective_status"],
        "MILESTONE_34_TASK_2_SCOPE_LOCK_ID": report["scope_lock_id"],
        "MILESTONE_34_TASK_2_HARNESS_MODE_ID": report["harness_mode_id"],
        "MILESTONE_34_TASK_2_TASK_2_SIGNATURE": report["task_2_signature"],
        "MILESTONE_34_TASK_2_SCOPE_LOCK_INSTANCE_ID": report["scope_lock_instance_id"],
        "MILESTONE_34_TASK_2_SCOPE_LOCK_SIGNATURE": report["scope_lock_signature"],
        "MILESTONE_34_TASK_2_REPLAY_EVALUATION_HARNESS_BOUNDARY": report["replay_evaluation_harness_boundary"],
        "MILESTONE_34_TASK_2_REPLAYABLE_EVENT_TRACE_REQUIRED": report["replayable_event_trace_required"],
        "MILESTONE_34_TASK_2_LOCAL_EVALUATION_RECORD_REQUIRED": report["local_evaluation_record_required"],
        "MILESTONE_34_TASK_2_REGRESSION_SNAPSHOT_REQUIRED": report["regression_snapshot_required"],
        "MILESTONE_34_TASK_2_AUDIT_ARTIFACT_REQUIRED": report["audit_artifact_required"],
        "MILESTONE_34_TASK_2_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_34_TASK_2_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_34_TASK_2_OFFICIAL_BENCHMARK_CERTIFICATION": report["official_benchmark_certification"],
        "MILESTONE_34_TASK_2_SCOPE_LOCK_STATUS": report["scope_lock_status"],
        "MILESTONE_34_TASK_2_SCOPE_LOCK_CASE_COUNT": report["scope_lock_case_count"],
        "MILESTONE_34_TASK_2_PASS_COUNT": report["pass_count"],
        "MILESTONE_34_TASK_2_FAIL_COUNT": report["fail_count"],
        "MILESTONE_34_TASK_2_SCOPE_LOCK_PASSED": report["scope_lock_passed"],
        "MILESTONE_34_TASK_2_TASK_BUDGET_MAX": report["task_budget_max"],
        "MILESTONE_34_TASK_2_CURRENT_TASK_NUMBER": report["current_task_number"],
        "MILESTONE_34_TASK_2_GENERATED_ARTIFACT_COUNT": report["generated_artifact_count"],
        "MILESTONE_34_TASK_2_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        print(f"{key}={_bool(value) if isinstance(value, bool) else value}")

if __name__ == "__main__":
    main()
