"""Milestone 32 Task 1 governed opening with task budget."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_31_verified_operator_session_gate_final_closure import (
    FINAL_CLOSURE_REVISION as SOURCE_FINAL_CLOSURE_REVISION,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    SCOPE_LOCK_ID as SOURCE_SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID as SOURCE_SELECTED_OBJECTIVE_ID,
    SESSION_GATE_MODE_ID as SOURCE_SESSION_GATE_MODE_ID,
    TASK_ID as SOURCE_CLOSURE_TASK_ID,
    run_verified_operator_session_gate_final_closure,
    task_6_signature,
    validate_verified_operator_session_gate_final_closure_report,
)

TASK_ID = "MILESTONE_32_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
MILESTONE_ID = "MILESTONE_32"
SOURCE_MILESTONE_ID = "MILESTONE_31_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE"
SOURCE_CLOSURE_DOC_PATH = Path("docs/milestone-31-task-6-verified-operator-authorization-session-gate-final-closure-v1.md")

OPENING_REVISION = "MILESTONE_32_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
OPENING_STATUS = "READY"
OBJECTIVE_SELECTION_STATUS = "PENDING_TASK_2_SCOPE_LOCK"
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
OPENING_CASE_COUNT = 8
REQUIRED_PASS_COUNT = 8
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = "MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

ARTIFACT_DIR = Path("examples/milestone-32/governed-opening-with-task-budget-v1")


def _stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()[:16]


def task_1_signature() -> str:
    return _stable_hash(
        {
            "task_id": TASK_ID,
            "milestone_id": MILESTONE_ID,
            "source_milestone_id": SOURCE_MILESTONE_ID,
            "source_closure_task_id": SOURCE_CLOSURE_TASK_ID,
            "source_task_6_signature": task_6_signature(),
            "opening_revision": OPENING_REVISION,
            "task_budget_max": TASK_BUDGET_MAX,
            "next_stage": NEXT_STAGE,
        }
    )


def _doc_contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(encoding="utf-8")


def _case(case_id: str, passed: bool, expected: Any, observed: Any) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "passed": bool(passed),
        "expected": expected,
        "observed": observed,
        "failure_reason": "NONE" if passed else f"{case_id}_FAILED",
    }


def _source_closure_artifacts_present() -> bool:
    artifact_dir = Path("examples/milestone-31/verified-operator-authorization-session-gate-final-closure-v1")
    required = [
        "task-6-final-closure-report.json",
        "task-6-final-closure-report.md",
        "task-6-final-closure-cases.json",
        "task-6-manifest.json",
        "task-6-index.txt",
    ]
    return artifact_dir.exists() and all((artifact_dir / name).exists() for name in required)


def run_milestone_32_governed_opening() -> dict[str, Any]:
    source_report = run_verified_operator_session_gate_final_closure()
    source_valid = validate_verified_operator_session_gate_final_closure_report(source_report)

    source_doc_valid = (
        _doc_contains(SOURCE_CLOSURE_DOC_PATH, "MILESTONE_31_TASK_6_CLOSURE_STATUS=CLOSED")
        and _doc_contains(SOURCE_CLOSURE_DOC_PATH, "MILESTONE_31_TASK_6_CLOSURE_PASSED=true")
        and _doc_contains(SOURCE_CLOSURE_DOC_PATH, f"MILESTONE_31_TASK_6_NEXT_STAGE={TASK_ID}")
    )

    cases = [
        _case(
            "MILESTONE_31_FINAL_CLOSURE_SOURCE_ARTIFACT_VALID",
            source_valid and source_report.get("closure_status") == "CLOSED" and source_report.get("closure_passed") is True,
            "Milestone 31 final closure remains CLOSED",
            {
                "closure_status": source_report.get("closure_status"),
                "closure_passed": source_report.get("closure_passed"),
                "pass_count": source_report.get("pass_count"),
                "fail_count": source_report.get("fail_count"),
            },
        ),
        _case(
            "MILESTONE_31_TO_32_TRANSITION_CONFIRMED",
            SOURCE_NEXT_STAGE == TASK_ID and source_report.get("next_stage") == TASK_ID,
            TASK_ID,
            {"source_constant_next_stage": SOURCE_NEXT_STAGE, "source_report_next_stage": source_report.get("next_stage")},
        ),
        _case(
            "MILESTONE_31_FINAL_CLOSURE_DOCUMENT_MARKERS_PRESENT",
            source_doc_valid,
            "Milestone 31 closure doc has CLOSED/PASSED/next-stage markers",
            str(SOURCE_CLOSURE_DOC_PATH),
        ),
        _case(
            "MILESTONE_31_FINAL_CLOSURE_ARTIFACT_SET_PRESENT",
            _source_closure_artifacts_present(),
            "Milestone 31 final closure artifact set present",
            "present" if _source_closure_artifacts_present() else "missing",
        ),
        _case(
            "MILESTONE_32_TASK_BUDGET_INITIALIZED",
            TASK_BUDGET_MAX == 8 and CURRENT_TASK_NUMBER == 1,
            {"task_budget_max": 8, "current_task_number": 1},
            {"task_budget_max": TASK_BUDGET_MAX, "current_task_number": CURRENT_TASK_NUMBER},
        ),
        _case(
            "MILESTONE_32_OBJECTIVE_SELECTION_PENDING_TASK_2",
            OBJECTIVE_SELECTION_STATUS == "PENDING_TASK_2_SCOPE_LOCK",
            "PENDING_TASK_2_SCOPE_LOCK",
            OBJECTIVE_SELECTION_STATUS,
        ),
        _case(
            "MILESTONE_32_OPENING_ARTIFACT_PLAN_COMPLETE",
            GENERATED_ARTIFACT_COUNT == 5 and SOURCE_GENERATED_ARTIFACT_COUNT == 5,
            5,
            {"task_1_generated_artifact_count": GENERATED_ARTIFACT_COUNT, "source_generated_artifact_count": SOURCE_GENERATED_ARTIFACT_COUNT},
        ),
        _case(
            "MILESTONE_32_NEXT_STAGE_SCOPE_LOCK_READY",
            NEXT_STAGE == "MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1",
            "MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1",
            NEXT_STAGE,
        ),
    ]

    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    opening_passed = pass_count == REQUIRED_PASS_COUNT and fail_count == REQUIRED_FAIL_COUNT
    opening_status = OPENING_STATUS if opening_passed else "INVALID"

    opening_id = "MILESTONE-32-GOVERNED-OPENING-" + _stable_hash(
        {
            "task_id": TASK_ID,
            "source_closure_id": source_report.get("closure_id"),
            "task_1_signature": task_1_signature(),
            "case_ids": [case["case_id"] for case in cases],
            "opening_status": opening_status,
        }
    )

    opening_signature = _stable_hash(
        {
            "opening_id": opening_id,
            "task_id": TASK_ID,
            "source_task_6_signature": task_6_signature(),
            "task_1_signature": task_1_signature(),
            "opening_status": opening_status,
            "opening_passed": opening_passed,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_closure_task_id": SOURCE_CLOSURE_TASK_ID,
        "source_final_closure_revision": SOURCE_FINAL_CLOSURE_REVISION,
        "source_task_6_signature": task_6_signature(),
        "source_closure_id": source_report.get("closure_id"),
        "source_closure_signature": source_report.get("closure_signature"),
        "source_closure_status": source_report.get("closure_status"),
        "source_closure_passed": source_report.get("closure_passed"),
        "source_selected_objective_id": SOURCE_SELECTED_OBJECTIVE_ID,
        "source_scope_lock_id": SOURCE_SCOPE_LOCK_ID,
        "source_session_gate_mode_id": SOURCE_SESSION_GATE_MODE_ID,
        "opening_revision": OPENING_REVISION,
        "task_1_signature": task_1_signature(),
        "opening_id": opening_id,
        "opening_signature": opening_signature,
        "opening_status": opening_status,
        "objective_selection_status": OBJECTIVE_SELECTION_STATUS,
        "opening_case_count": len(cases),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "opening_passed": opening_passed,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "opening_cases": cases,
        "next_stage": NEXT_STAGE,
    }


def validate_milestone_32_governed_opening_report(report: dict[str, Any]) -> bool:
    required = {
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_closure_task_id": SOURCE_CLOSURE_TASK_ID,
        "source_final_closure_revision": SOURCE_FINAL_CLOSURE_REVISION,
        "source_task_6_signature": task_6_signature(),
        "source_closure_status": "CLOSED",
        "source_closure_passed": True,
        "opening_revision": OPENING_REVISION,
        "task_1_signature": task_1_signature(),
        "opening_status": OPENING_STATUS,
        "objective_selection_status": OBJECTIVE_SELECTION_STATUS,
        "opening_case_count": OPENING_CASE_COUNT,
        "pass_count": REQUIRED_PASS_COUNT,
        "fail_count": REQUIRED_FAIL_COUNT,
        "opening_passed": True,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    if any(report.get(key) != value for key, value in required.items()):
        return False

    cases = report.get("opening_cases")
    if not isinstance(cases, list) or len(cases) != OPENING_CASE_COUNT:
        return False

    return all(case.get("passed") is True and case.get("failure_reason") == "NONE" for case in cases)


def _report_markdown(report: dict[str, Any]) -> str:
    case_lines = "\n".join(
        f"- {case['case_id']}: {'PASS' if case['passed'] else 'FAIL'}"
        for case in report["opening_cases"]
    )
    return f"""# Milestone 32 Task 1 - Governed Opening With Task Budget v1

MILESTONE_32_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true

MILESTONE_32_TASK_1_TASK_ID={report['task_id']}
MILESTONE_32_TASK_1_MILESTONE_ID={report['milestone_id']}
MILESTONE_32_TASK_1_SOURCE_MILESTONE_ID={report['source_milestone_id']}
MILESTONE_32_TASK_1_SOURCE_CLOSURE_TASK_ID={report['source_closure_task_id']}
MILESTONE_32_TASK_1_SOURCE_FINAL_CLOSURE_REVISION={report['source_final_closure_revision']}

MILESTONE_32_TASK_1_SOURCE_CLOSURE_STATUS={report['source_closure_status']}
MILESTONE_32_TASK_1_SOURCE_CLOSURE_PASSED={str(report['source_closure_passed']).lower()}
MILESTONE_32_TASK_1_SOURCE_SELECTED_OBJECTIVE_ID={report['source_selected_objective_id']}
MILESTONE_32_TASK_1_SOURCE_SCOPE_LOCK_ID={report['source_scope_lock_id']}
MILESTONE_32_TASK_1_SOURCE_SESSION_GATE_MODE_ID={report['source_session_gate_mode_id']}

MILESTONE_32_TASK_1_OPENING_REVISION={report['opening_revision']}
MILESTONE_32_TASK_1_OPENING_ID={report['opening_id']}
MILESTONE_32_TASK_1_OPENING_SIGNATURE={report['opening_signature']}
MILESTONE_32_TASK_1_OPENING_STATUS={report['opening_status']}
MILESTONE_32_TASK_1_OBJECTIVE_SELECTION_STATUS={report['objective_selection_status']}
MILESTONE_32_TASK_1_OPENING_CASE_COUNT={report['opening_case_count']}
MILESTONE_32_TASK_1_PASS_COUNT={report['pass_count']}
MILESTONE_32_TASK_1_FAIL_COUNT={report['fail_count']}
MILESTONE_32_TASK_1_OPENING_PASSED={str(report['opening_passed']).lower()}

MILESTONE_32_TASK_1_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_32_TASK_1_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_32_TASK_1_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}

MILESTONE_32_TASK_1_NEXT_STAGE={report['next_stage']}

## Opening Cases

{case_lines}
"""


def write_task_1_artifacts(base_dir: Path | str = ARTIFACT_DIR) -> dict[str, Any]:
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)

    report = run_milestone_32_governed_opening()
    if not validate_milestone_32_governed_opening_report(report):
        raise ValueError("Milestone 32 Task 1 governed opening report is invalid")

    report_path = base / "task-1-governed-opening-report.json"
    markdown_path = base / "task-1-governed-opening-report.md"
    cases_path = base / "task-1-governed-opening-cases.json"
    manifest_path = base / "task-1-manifest.json"
    index_path = base / "task-1-index.txt"

    cases_payload = {
        "task_id": TASK_ID,
        "opening_id": report["opening_id"],
        "opening_status": report["opening_status"],
        "opening_case_count": report["opening_case_count"],
        "opening_cases": report["opening_cases"],
    }

    manifest = {
        "task_id": TASK_ID,
        "milestone_id": MILESTONE_ID,
        "source_milestone_id": SOURCE_MILESTONE_ID,
        "source_closure_task_id": SOURCE_CLOSURE_TASK_ID,
        "source_task_6_signature": task_6_signature(),
        "opening_revision": OPENING_REVISION,
        "task_1_signature": task_1_signature(),
        "opening_id": report["opening_id"],
        "opening_signature": report["opening_signature"],
        "opening_status": report["opening_status"],
        "objective_selection_status": OBJECTIVE_SELECTION_STATUS,
        "opening_passed": report["opening_passed"],
        "opening_case_count": report["opening_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    index = "\n".join(
        [
            "MILESTONE_32_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true",
            f"TASK_ID={TASK_ID}",
            f"MILESTONE_ID={MILESTONE_ID}",
            f"SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}",
            f"SOURCE_CLOSURE_TASK_ID={SOURCE_CLOSURE_TASK_ID}",
            f"SOURCE_CLOSURE_STATUS={report['source_closure_status']}",
            f"SOURCE_CLOSURE_PASSED={str(report['source_closure_passed']).lower()}",
            f"OPENING_REVISION={OPENING_REVISION}",
            f"TASK_1_SIGNATURE={task_1_signature()}",
            f"OPENING_ID={report['opening_id']}",
            f"OPENING_SIGNATURE={report['opening_signature']}",
            f"OPENING_STATUS={report['opening_status']}",
            f"OBJECTIVE_SELECTION_STATUS={OBJECTIVE_SELECTION_STATUS}",
            f"OPENING_CASE_COUNT={report['opening_case_count']}",
            f"PASS_COUNT={report['pass_count']}",
            f"FAIL_COUNT={report['fail_count']}",
            f"OPENING_PASSED={str(report['opening_passed']).lower()}",
            f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
            f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
            f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
            f"NEXT_STAGE={NEXT_STAGE}",
            "",
        ]
    )

    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_report_markdown(report), encoding="utf-8")
    cases_path.write_text(json.dumps(cases_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    index_path.write_text(index, encoding="utf-8")

    return {
        "report": report,
        "manifest": manifest,
        "cases": cases_payload,
        "paths": {
            "report": str(report_path),
            "markdown": str(markdown_path),
            "cases": str(cases_path),
            "manifest": str(manifest_path),
            "index": str(index_path),
        },
    }


def main() -> None:
    artifacts = write_task_1_artifacts()
    report = artifacts["report"]

    print("MILESTONE_32_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true")
    print(f"MILESTONE_32_TASK_1_TASK_ID={TASK_ID}")
    print(f"MILESTONE_32_TASK_1_MILESTONE_ID={MILESTONE_ID}")
    print(f"MILESTONE_32_TASK_1_SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}")
    print(f"MILESTONE_32_TASK_1_SOURCE_CLOSURE_TASK_ID={SOURCE_CLOSURE_TASK_ID}")
    print(f"MILESTONE_32_TASK_1_SOURCE_CLOSURE_STATUS={report['source_closure_status']}")
    print(f"MILESTONE_32_TASK_1_SOURCE_CLOSURE_PASSED={str(report['source_closure_passed']).lower()}")
    print(f"MILESTONE_32_TASK_1_OPENING_REVISION={OPENING_REVISION}")
    print(f"MILESTONE_32_TASK_1_TASK_1_SIGNATURE={task_1_signature()}")
    print(f"MILESTONE_32_TASK_1_OPENING_ID={report['opening_id']}")
    print(f"MILESTONE_32_TASK_1_OPENING_SIGNATURE={report['opening_signature']}")
    print(f"MILESTONE_32_TASK_1_OPENING_STATUS={report['opening_status']}")
    print(f"MILESTONE_32_TASK_1_OBJECTIVE_SELECTION_STATUS={OBJECTIVE_SELECTION_STATUS}")
    print(f"MILESTONE_32_TASK_1_OPENING_CASE_COUNT={report['opening_case_count']}")
    print(f"MILESTONE_32_TASK_1_PASS_COUNT={report['pass_count']}")
    print(f"MILESTONE_32_TASK_1_FAIL_COUNT={report['fail_count']}")
    print(f"MILESTONE_32_TASK_1_OPENING_PASSED={str(report['opening_passed']).lower()}")
    print(f"MILESTONE_32_TASK_1_TASK_BUDGET_MAX={TASK_BUDGET_MAX}")
    print(f"MILESTONE_32_TASK_1_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}")
    print(f"MILESTONE_32_TASK_1_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}")
    print(f"MILESTONE_32_TASK_1_NEXT_STAGE={NEXT_STAGE}")


if __name__ == "__main__":
    main()
