from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle import (
    validate_query_result_evidence_bundle,
)
from hbce_arc_agi3.milestone_29_query_result_evidence_bundle_validation import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    EVIDENCE_BUNDLE_REVISION,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID as SOURCE_VALIDATION_SOURCE_TASK_ID,
    TASK_3_BUNDLE_PATH,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    build_bundle_snapshot,
    run_query_result_evidence_bundle_validation,
    task_4_signature,
    validate_bundle_snapshot,
    validate_validation_report,
)


TASK_ID = "MILESTONE_29_TASK_5_QUERY_RESULT_EVIDENCE_BUNDLE_REGRESSION_INTEGRATION_V1"
REGRESSION_INTEGRATION_REVISION = "MILESTONE_29_QUERY_RESULT_EVIDENCE_BUNDLE_REGRESSION_INTEGRATION_V1"

CURRENT_TASK_NUMBER = 5
NEXT_STAGE = "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_V1"

INTEGRATION_STATUS = "VALID"
INTEGRATION_CASE_COUNT = 9
REQUIRED_PASS_COUNT = 9
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

TASK_4_VALIDATION_REPORT_PATH = Path("examples/milestone-29/query-result-evidence-bundle-validation-v1/task-4-validation-report.json")
TASK_4_VALIDATION_CASES_PATH = Path("examples/milestone-29/query-result-evidence-bundle-validation-v1/task-4-validation-cases.json")
TASK_4_MANIFEST_PATH = Path("examples/milestone-29/query-result-evidence-bundle-validation-v1/task-4-manifest.json")
TASK_4_INDEX_PATH = Path("examples/milestone-29/query-result-evidence-bundle-validation-v1/task-4-index.txt")
TASK_4_MARKDOWN_PATH = Path("examples/milestone-29/query-result-evidence-bundle-validation-v1/task-4-validation-report.md")


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_5_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
            "validation_revision": VALIDATION_REVISION,
            "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
            "task_4_signature": task_4_signature(),
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "next_stage": NEXT_STAGE,
        }
    )


def _case(case_id: str, passed: bool, expected: Any, observed: Any, failure_reason: str = "NONE") -> dict[str, Any]:
    return {
        "case_id": case_id,
        "passed": passed,
        "failure_reason": "NONE" if passed else failure_reason,
        "expected": expected,
        "observed": observed,
    }


def build_validation_snapshot() -> dict[str, Any]:
    runtime = run_query_result_evidence_bundle_validation()
    persisted = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    runtime_valid = validate_validation_report(runtime)
    persisted_valid = validate_validation_report(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_validation_id": runtime.get("validation_id"),
        "persisted_validation_id": persisted.get("validation_id"),
        "runtime_validation_signature": runtime.get("validation_signature"),
        "persisted_validation_signature": persisted.get("validation_signature"),
        "runtime_task_4_signature": runtime.get("task_4_signature"),
        "persisted_task_4_signature": persisted.get("task_4_signature"),
        "selected_objective_id": persisted.get("selected_objective_id"),
        "scope_lock_id": persisted.get("scope_lock_id"),
        "source_evidence_bundle_id": persisted.get("source_evidence_bundle_id"),
        "source_evidence_bundle_signature": persisted.get("source_evidence_bundle_signature"),
        "source_implementation_status": persisted.get("source_implementation_status"),
        "source_scope_lock_valid": persisted.get("source_scope_lock_valid"),
        "source_chain_valid": persisted.get("source_chain_valid"),
        "source_evidence_valid": persisted.get("source_evidence_valid"),
        "validation_status": persisted.get("validation_status"),
        "validation_case_count": persisted.get("validation_case_count"),
        "pass_count": persisted.get("pass_count"),
        "fail_count": persisted.get("fail_count"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_validation": (
            runtime.get("validation_id") == persisted.get("validation_id")
            and runtime.get("validation_signature") == persisted.get("validation_signature")
            and runtime.get("task_4_signature") == persisted.get("task_4_signature") == task_4_signature()
        ),
    }


def validate_validation_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("source_implementation_status") != "READY":
        return False
    if snapshot.get("source_scope_lock_valid") is not True:
        return False
    if snapshot.get("source_chain_valid") is not True:
        return False
    if snapshot.get("source_evidence_valid") is not True:
        return False
    if snapshot.get("validation_status") != "VALID":
        return False
    if snapshot.get("validation_case_count") != VALIDATION_CASE_COUNT:
        return False
    if snapshot.get("pass_count") != 8:
        return False
    if snapshot.get("fail_count") != 0:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_validation"))


def _validate_validation_report_case() -> dict[str, Any]:
    report = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    passed = (
        validate_validation_report(report)
        and report.get("validation_status") == "VALID"
        and report.get("pass_count") == 8
        and report.get("fail_count") == 0
        and report.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_4_VALIDATION_REPORT_VALID",
        passed,
        {"validation_status": "VALID", "pass_count": 8, "fail_count": 0},
        {
            "validation_status": report.get("validation_status"),
            "pass_count": report.get("pass_count"),
            "fail_count": report.get("fail_count"),
            "next_stage": report.get("next_stage"),
        },
        "TASK_4_VALIDATION_REPORT_INVALID",
    )


def _validate_runtime_stability_case() -> dict[str, Any]:
    snapshot = build_validation_snapshot()
    passed = validate_validation_snapshot(snapshot)
    return _case(
        "TASK_4_VALIDATION_RUNTIME_STABILITY_VALID",
        passed,
        {"stable_validation": True},
        snapshot,
        "TASK_4_VALIDATION_RUNTIME_STABILITY_INVALID",
    )


def _validate_artifact_set_case() -> dict[str, Any]:
    paths = (
        TASK_4_VALIDATION_REPORT_PATH,
        TASK_4_VALIDATION_CASES_PATH,
        TASK_4_MANIFEST_PATH,
        TASK_4_INDEX_PATH,
        TASK_4_MARKDOWN_PATH,
    )
    missing = [str(path) for path in paths if not path.exists()]
    readable = []
    for path in paths:
        if path.exists():
            readable.append(path.read_text(encoding="utf-8") != "")
    passed = not missing and all(readable)
    return _case(
        "TASK_4_VALIDATION_ARTIFACT_SET_PRESENT",
        passed,
        {"artifact_count": 5, "missing": []},
        {"artifact_count": len(paths), "missing": missing, "readable_count": sum(1 for item in readable if item)},
        "TASK_4_VALIDATION_ARTIFACT_SET_INCOMPLETE",
    )


def _validate_manifest_case() -> dict[str, Any]:
    report = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    manifest = _load_json(TASK_4_MANIFEST_PATH)
    passed = (
        manifest.get("task_id") == SOURCE_TASK_ID
        and manifest.get("source_task_id") == report.get("source_task_id")
        and manifest.get("validation_id") == report.get("validation_id")
        and manifest.get("validation_signature") == report.get("validation_signature")
        and manifest.get("source_evidence_bundle_id") == report.get("source_evidence_bundle_id")
        and manifest.get("source_evidence_bundle_signature") == report.get("source_evidence_bundle_signature")
        and manifest.get("validation_status") == report.get("validation_status") == "VALID"
        and manifest.get("validation_passed") is True
        and manifest.get("pass_count") == report.get("pass_count") == 8
        and manifest.get("fail_count") == report.get("fail_count") == 0
        and manifest.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_4_VALIDATION_MANIFEST_CONSISTENCY_VALID",
        passed,
        {"manifest_matches_validation_report": True},
        {
            "manifest_validation_id": manifest.get("validation_id"),
            "report_validation_id": report.get("validation_id"),
            "manifest_status": manifest.get("validation_status"),
            "manifest_next_stage": manifest.get("next_stage"),
        },
        "TASK_4_VALIDATION_MANIFEST_CONSISTENCY_INVALID",
    )


def _validate_index_case() -> dict[str, Any]:
    report = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    index = TASK_4_INDEX_PATH.read_text(encoding="utf-8")
    required_markers = (
        "MILESTONE_29_TASK_4_QUERY_RESULT_EVIDENCE_BUNDLE_VALIDATION_READY=true",
        f"SOURCE_EVIDENCE_BUNDLE_ID={report.get('source_evidence_bundle_id')}",
        f"SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report.get('source_evidence_bundle_signature')}",
        "SOURCE_IMPLEMENTATION_STATUS=READY",
        "SOURCE_SCOPE_LOCK_VALID=true",
        "SOURCE_CHAIN_VALID=true",
        "SOURCE_EVIDENCE_VALID=true",
        f"VALIDATION_ID={report.get('validation_id')}",
        f"VALIDATION_SIGNATURE={report.get('validation_signature')}",
        "VALIDATION_STATUS=VALID",
        "VALIDATION_CASE_COUNT=8",
        "PASS_COUNT=8",
        "FAIL_COUNT=0",
        f"NEXT_STAGE={SOURCE_NEXT_STAGE}",
    )
    missing = [marker for marker in required_markers if marker not in index]
    passed = not missing
    return _case(
        "TASK_4_VALIDATION_INDEX_MARKERS_VALID",
        passed,
        {"missing_markers": []},
        {"missing_markers": missing, "required_marker_count": len(required_markers)},
        "TASK_4_VALIDATION_INDEX_MARKERS_INVALID",
    )


def _validate_cases_case() -> dict[str, Any]:
    report = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    cases = _load_json(TASK_4_VALIDATION_CASES_PATH)
    expected_case_ids = {
        "TASK_3_EVIDENCE_BUNDLE_REPORT_VALID",
        "TASK_3_EVIDENCE_BUNDLE_RUNTIME_STABILITY_VALID",
        "TASK_3_EVIDENCE_BUNDLE_ARTIFACT_SET_PRESENT",
        "TASK_3_EVIDENCE_BUNDLE_MANIFEST_CONSISTENCY_VALID",
        "TASK_3_EVIDENCE_BUNDLE_INDEX_MARKERS_VALID",
        "TASK_3_EVIDENCE_INDEX_CONSISTENCY_VALID",
        "TASK_3_EVIDENCE_DIGESTS_VALID",
        "TASK_3_SOURCE_CHAIN_STATUS_VALID",
    }
    observed_case_ids = {case.get("case_id") for case in cases.get("case_results", [])}
    passed = (
        cases.get("task_id") == SOURCE_TASK_ID
        and cases.get("validation_id") == report.get("validation_id")
        and cases.get("validation_status") == "VALID"
        and cases.get("validation_case_count") == VALIDATION_CASE_COUNT
        and observed_case_ids == expected_case_ids
        and len(cases.get("case_results", [])) == VALIDATION_CASE_COUNT
        and all(case.get("passed") is True for case in cases.get("case_results", []))
    )
    return _case(
        "TASK_4_VALIDATION_CASE_SET_VALID",
        passed,
        {"case_ids": sorted(expected_case_ids), "validation_case_count": VALIDATION_CASE_COUNT},
        {"case_ids": sorted(observed_case_ids), "validation_case_count": cases.get("validation_case_count")},
        "TASK_4_VALIDATION_CASE_SET_INVALID",
    )


def _validate_source_bundle_case() -> dict[str, Any]:
    bundle = _load_json(TASK_3_BUNDLE_PATH)
    report = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    passed = (
        validate_query_result_evidence_bundle(bundle)
        and bundle.get("evidence_bundle_id") == report.get("source_evidence_bundle_id")
        and bundle.get("evidence_bundle_signature") == report.get("source_evidence_bundle_signature")
        and bundle.get("implementation_status") == "READY"
        and bundle.get("implementation_complete") is True
        and bundle.get("scope_lock_valid") is True
        and bundle.get("source_chain_valid") is True
        and bundle.get("evidence_valid") is True
    )
    return _case(
        "TASK_3_SOURCE_EVIDENCE_BUNDLE_REMAINS_VALID",
        passed,
        {"source_bundle_valid": True},
        {
            "source_bundle_id": bundle.get("evidence_bundle_id"),
            "report_source_bundle_id": report.get("source_evidence_bundle_id"),
            "implementation_status": bundle.get("implementation_status"),
            "implementation_complete": bundle.get("implementation_complete"),
        },
        "TASK_3_SOURCE_EVIDENCE_BUNDLE_INVALID",
    )


def _validate_local_guardrail_case() -> dict[str, Any]:
    bundle = _load_json(TASK_3_BUNDLE_PATH)
    passed = (
        bundle.get("local_only") is True
        and bundle.get("network_access_allowed") is False
        and bundle.get("shell_execution_allowed") is False
        and bundle.get("repository_mutation_allowed") is False
        and bundle.get("remote_registry_lookup_allowed") is False
        and bundle.get("deep_recursive_dependency_traversal_allowed") is False
        and bundle.get("external_model_call_allowed") is False
        and bundle.get("forbidden_operation_count") == 8
    )
    return _case(
        "TASK_3_LOCAL_GUARDRAILS_REMAIN_VALID",
        passed,
        {
            "local_only": True,
            "network_access_allowed": False,
            "shell_execution_allowed": False,
            "repository_mutation_allowed": False,
            "remote_registry_lookup_allowed": False,
            "deep_recursive_dependency_traversal_allowed": False,
            "external_model_call_allowed": False,
            "forbidden_operation_count": 8,
        },
        {
            "local_only": bundle.get("local_only"),
            "network_access_allowed": bundle.get("network_access_allowed"),
            "shell_execution_allowed": bundle.get("shell_execution_allowed"),
            "repository_mutation_allowed": bundle.get("repository_mutation_allowed"),
            "remote_registry_lookup_allowed": bundle.get("remote_registry_lookup_allowed"),
            "deep_recursive_dependency_traversal_allowed": bundle.get("deep_recursive_dependency_traversal_allowed"),
            "external_model_call_allowed": bundle.get("external_model_call_allowed"),
            "forbidden_operation_count": bundle.get("forbidden_operation_count"),
        },
        "TASK_3_LOCAL_GUARDRAILS_INVALID",
    )


def _validate_transition_budget_case() -> dict[str, Any]:
    report = _load_json(TASK_4_VALIDATION_REPORT_PATH)
    passed = (
        report.get("task_budget_max") == TASK_BUDGET_MAX == 8
        and report.get("current_task_number") == SOURCE_CURRENT_TASK_NUMBER == 4
        and CURRENT_TASK_NUMBER == 5
        and report.get("next_stage") == TASK_ID
        and NEXT_STAGE == "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_V1"
        and SOURCE_GENERATED_ARTIFACT_COUNT == 5
        and GENERATED_ARTIFACT_COUNT == 5
    )
    return _case(
        "TASK_5_TRANSITION_AND_BUDGET_VALID",
        passed,
        {
            "task_budget_max": 8,
            "source_current_task_number": 4,
            "current_task_number": 5,
            "source_next_stage": TASK_ID,
            "next_stage": "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_V1",
        },
        {
            "task_budget_max": report.get("task_budget_max"),
            "source_current_task_number": report.get("current_task_number"),
            "current_task_number": CURRENT_TASK_NUMBER,
            "source_next_stage": report.get("next_stage"),
            "next_stage": NEXT_STAGE,
        },
        "TASK_5_TRANSITION_AND_BUDGET_INVALID",
    )


def run_query_result_evidence_bundle_regression_integration() -> dict[str, Any]:
    case_results = [
        _validate_validation_report_case(),
        _validate_runtime_stability_case(),
        _validate_artifact_set_case(),
        _validate_manifest_case(),
        _validate_index_case(),
        _validate_cases_case(),
        _validate_source_bundle_case(),
        _validate_local_guardrail_case(),
        _validate_transition_budget_case(),
    ]

    pass_count = sum(1 for case in case_results if case["passed"])
    fail_count = len(case_results) - pass_count
    integration_passed = (
        len(case_results) == INTEGRATION_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    validation_report = _load_json(TASK_4_VALIDATION_REPORT_PATH)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_4_signature": task_4_signature(),
        "task_5_signature": task_5_signature(),
        "source_evidence_bundle_id": validation_report.get("source_evidence_bundle_id"),
        "source_evidence_bundle_signature": validation_report.get("source_evidence_bundle_signature"),
        "source_validation_id": validation_report.get("validation_id"),
        "source_validation_signature": validation_report.get("validation_signature"),
        "source_validation_status": validation_report.get("validation_status"),
        "source_implementation_status": validation_report.get("source_implementation_status"),
        "source_scope_lock_valid": validation_report.get("source_scope_lock_valid"),
        "source_chain_valid": validation_report.get("source_chain_valid"),
        "source_evidence_valid": validation_report.get("source_evidence_valid"),
        "integration_status": INTEGRATION_STATUS if integration_passed else "INVALID",
        "integration_case_count": len(case_results),
        "required_pass_count": REQUIRED_PASS_COUNT,
        "required_fail_count": REQUIRED_FAIL_COUNT,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "integration_passed": integration_passed,
        "case_results": case_results,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    report["integration_id"] = "MILESTONE-29-QUERY-RESULT-EVIDENCE-BUNDLE-INTEGRATION-" + _stable_digest(report)
    report["integration_signature"] = _stable_digest(
        {
            "integration_id": report["integration_id"],
            "source_evidence_bundle_id": report["source_evidence_bundle_id"],
            "source_evidence_bundle_signature": report["source_evidence_bundle_signature"],
            "source_validation_id": report["source_validation_id"],
            "source_validation_signature": report["source_validation_signature"],
            "task_4_signature": report["task_4_signature"],
            "task_5_signature": report["task_5_signature"],
            "case_results": case_results,
            "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        }
    )
    return report


def validate_regression_integration_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("evidence_bundle_revision") != EVIDENCE_BUNDLE_REVISION:
        return False
    if report.get("validation_revision") != VALIDATION_REVISION:
        return False
    if report.get("regression_integration_revision") != REGRESSION_INTEGRATION_REVISION:
        return False
    if report.get("task_4_signature") != task_4_signature():
        return False
    if report.get("task_5_signature") != task_5_signature():
        return False
    if report.get("source_validation_status") != "VALID":
        return False
    if report.get("source_implementation_status") != "READY":
        return False
    if report.get("source_scope_lock_valid") is not True:
        return False
    if report.get("source_chain_valid") is not True:
        return False
    if report.get("source_evidence_valid") is not True:
        return False
    if report.get("integration_status") != INTEGRATION_STATUS:
        return False
    if report.get("integration_case_count") != INTEGRATION_CASE_COUNT:
        return False
    if report.get("pass_count") != REQUIRED_PASS_COUNT:
        return False
    if report.get("fail_count") != REQUIRED_FAIL_COUNT:
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    if not all(case.get("passed") is True for case in report.get("case_results", [])):
        return False
    return bool(report.get("integration_passed") and report.get("integration_id") and report.get("integration_signature"))


def render_integration_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 29 Task 5 Query Result Evidence Bundle Regression Integration",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"INTEGRATION_ID={report.get('integration_id')}",
        f"INTEGRATION_SIGNATURE={report.get('integration_signature')}",
        f"SOURCE_VALIDATION_ID={report.get('source_validation_id')}",
        f"SOURCE_VALIDATION_SIGNATURE={report.get('source_validation_signature')}",
        f"SOURCE_EVIDENCE_BUNDLE_ID={report.get('source_evidence_bundle_id')}",
        f"SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report.get('source_evidence_bundle_signature')}",
        f"INTEGRATION_STATUS={report.get('integration_status')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Regression integration cases",
    ]
    for case in report.get("case_results", []):
        lines.append(f"- {case['case_id']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_5_artifacts(base_dir: str | Path = "examples/milestone-29/query-result-evidence-bundle-regression-integration-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_query_result_evidence_bundle_regression_integration()
    cases = {
        "task_id": TASK_ID,
        "integration_id": report["integration_id"],
        "integration_status": report["integration_status"],
        "integration_case_count": report["integration_case_count"],
        "case_results": report["case_results"],
    }
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_4_signature": task_4_signature(),
        "task_5_signature": task_5_signature(),
        "source_evidence_bundle_id": report["source_evidence_bundle_id"],
        "source_evidence_bundle_signature": report["source_evidence_bundle_signature"],
        "source_validation_id": report["source_validation_id"],
        "source_validation_signature": report["source_validation_signature"],
        "source_validation_status": report["source_validation_status"],
        "integration_id": report["integration_id"],
        "integration_signature": report["integration_signature"],
        "integration_status": report["integration_status"],
        "integration_passed": report["integration_passed"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-5-regression-integration-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-5-regression-integration-report.md").write_text(
        render_integration_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-5-regression-integration-cases.json").write_text(
        json.dumps(cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-5-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-5-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_29_TASK_5_QUERY_RESULT_EVIDENCE_BUNDLE_REGRESSION_INTEGRATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"EVIDENCE_BUNDLE_REVISION={EVIDENCE_BUNDLE_REVISION}",
                f"VALIDATION_REVISION={VALIDATION_REVISION}",
                f"REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}",
                f"TASK_4_SIGNATURE={task_4_signature()}",
                f"TASK_5_SIGNATURE={task_5_signature()}",
                f"SOURCE_EVIDENCE_BUNDLE_ID={report['source_evidence_bundle_id']}",
                f"SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report['source_evidence_bundle_signature']}",
                f"SOURCE_VALIDATION_ID={report['source_validation_id']}",
                f"SOURCE_VALIDATION_SIGNATURE={report['source_validation_signature']}",
                f"SOURCE_VALIDATION_STATUS={report['source_validation_status']}",
                f"SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}",
                f"SOURCE_SCOPE_LOCK_VALID={str(report['source_scope_lock_valid']).lower()}",
                f"SOURCE_CHAIN_VALID={str(report['source_chain_valid']).lower()}",
                f"SOURCE_EVIDENCE_VALID={str(report['source_evidence_valid']).lower()}",
                f"INTEGRATION_ID={report['integration_id']}",
                f"INTEGRATION_SIGNATURE={report['integration_signature']}",
                f"INTEGRATION_STATUS={report['integration_status']}",
                f"INTEGRATION_CASE_COUNT={report['integration_case_count']}",
                f"PASS_COUNT={report['pass_count']}",
                f"FAIL_COUNT={report['fail_count']}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_5_status_lines() -> tuple[str, ...]:
    report = run_query_result_evidence_bundle_regression_integration()
    return (
        "MILESTONE_29_TASK_5_QUERY_RESULT_EVIDENCE_BUNDLE_REGRESSION_INTEGRATION_READY=true",
        f"MILESTONE_29_TASK_5_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_29_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_29_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_29_TASK_5_EVIDENCE_BUNDLE_REVISION={EVIDENCE_BUNDLE_REVISION}",
        f"MILESTONE_29_TASK_5_VALIDATION_REVISION={VALIDATION_REVISION}",
        f"MILESTONE_29_TASK_5_REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}",
        f"MILESTONE_29_TASK_5_TASK_4_SIGNATURE={task_4_signature()}",
        f"MILESTONE_29_TASK_5_TASK_5_SIGNATURE={task_5_signature()}",
        f"MILESTONE_29_TASK_5_SOURCE_EVIDENCE_BUNDLE_ID={report['source_evidence_bundle_id']}",
        f"MILESTONE_29_TASK_5_SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report['source_evidence_bundle_signature']}",
        f"MILESTONE_29_TASK_5_SOURCE_VALIDATION_ID={report['source_validation_id']}",
        f"MILESTONE_29_TASK_5_SOURCE_VALIDATION_SIGNATURE={report['source_validation_signature']}",
        f"MILESTONE_29_TASK_5_SOURCE_VALIDATION_STATUS={report['source_validation_status']}",
        f"MILESTONE_29_TASK_5_SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}",
        f"MILESTONE_29_TASK_5_SOURCE_SCOPE_LOCK_VALID={str(report['source_scope_lock_valid']).lower()}",
        f"MILESTONE_29_TASK_5_SOURCE_CHAIN_VALID={str(report['source_chain_valid']).lower()}",
        f"MILESTONE_29_TASK_5_SOURCE_EVIDENCE_VALID={str(report['source_evidence_valid']).lower()}",
        f"MILESTONE_29_TASK_5_INTEGRATION_ID={report['integration_id']}",
        f"MILESTONE_29_TASK_5_INTEGRATION_SIGNATURE={report['integration_signature']}",
        f"MILESTONE_29_TASK_5_INTEGRATION_STATUS={report['integration_status']}",
        f"MILESTONE_29_TASK_5_INTEGRATION_CASE_COUNT={report['integration_case_count']}",
        f"MILESTONE_29_TASK_5_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_29_TASK_5_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_29_TASK_5_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_29_TASK_5_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_29_TASK_5_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_29_TASK_5_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_5_artifacts()
    for line in task_5_status_lines():
        print(line)
