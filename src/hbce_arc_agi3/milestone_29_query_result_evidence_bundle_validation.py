from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    EVIDENCE_BUNDLE_REVISION,
    EVIDENCE_ITEM_COUNT,
    MILESTONE_ID,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_query_result_evidence_bundle,
    evidence_source_paths,
    task_3_signature,
    validate_evidence_items,
    validate_query_result_evidence_bundle,
)


TASK_ID = "MILESTONE_29_TASK_4_QUERY_RESULT_EVIDENCE_BUNDLE_VALIDATION_V1"
VALIDATION_REVISION = "MILESTONE_29_QUERY_RESULT_EVIDENCE_BUNDLE_VALIDATION_V1"

CURRENT_TASK_NUMBER = 4
NEXT_STAGE = "MILESTONE_29_TASK_5_QUERY_RESULT_EVIDENCE_BUNDLE_REGRESSION_INTEGRATION_V1"

VALIDATION_STATUS = "VALID"
VALIDATION_CASE_COUNT = 8
REQUIRED_PASS_COUNT = 8
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5

TASK_3_BUNDLE_PATH = Path("examples/milestone-29/query-result-evidence-bundle-implementation-v1/task-3-evidence-bundle.json")
TASK_3_EVIDENCE_INDEX_PATH = Path("examples/milestone-29/query-result-evidence-bundle-implementation-v1/task-3-evidence-index.json")
TASK_3_MANIFEST_PATH = Path("examples/milestone-29/query-result-evidence-bundle-implementation-v1/task-3-manifest.json")
TASK_3_INDEX_PATH = Path("examples/milestone-29/query-result-evidence-bundle-implementation-v1/task-3-index.txt")
TASK_3_MARKDOWN_PATH = Path("examples/milestone-29/query-result-evidence-bundle-implementation-v1/task-3-evidence-bundle.md")


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_4_signature() -> str:
    return _stable_digest(
        {
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
            "validation_revision": VALIDATION_REVISION,
            "task_3_signature": task_3_signature(),
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


def build_bundle_snapshot() -> dict[str, Any]:
    runtime = build_query_result_evidence_bundle()
    persisted = _load_json(TASK_3_BUNDLE_PATH)
    runtime_valid = validate_query_result_evidence_bundle(runtime)
    persisted_valid = validate_query_result_evidence_bundle(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_bundle_id": runtime.get("evidence_bundle_id"),
        "persisted_bundle_id": persisted.get("evidence_bundle_id"),
        "runtime_bundle_signature": runtime.get("evidence_bundle_signature"),
        "persisted_bundle_signature": persisted.get("evidence_bundle_signature"),
        "runtime_task_3_signature": runtime.get("task_3_signature"),
        "persisted_task_3_signature": persisted.get("task_3_signature"),
        "selected_objective_id": persisted.get("selected_objective_id"),
        "scope_lock_id": persisted.get("scope_lock_id"),
        "implementation_status": persisted.get("implementation_status"),
        "implementation_complete": persisted.get("implementation_complete"),
        "scope_lock_valid": persisted.get("scope_lock_valid"),
        "source_chain_valid": persisted.get("source_chain_valid"),
        "evidence_valid": persisted.get("evidence_valid"),
        "evidence_item_count": persisted.get("evidence_item_count"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_bundle": (
            runtime.get("evidence_bundle_id") == persisted.get("evidence_bundle_id")
            and runtime.get("evidence_bundle_signature") == persisted.get("evidence_bundle_signature")
            and runtime.get("task_3_signature") == persisted.get("task_3_signature") == task_3_signature()
        ),
    }


def validate_bundle_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if snapshot.get("implementation_status") != "READY":
        return False
    if snapshot.get("implementation_complete") is not True:
        return False
    if snapshot.get("scope_lock_valid") is not True:
        return False
    if snapshot.get("source_chain_valid") is not True:
        return False
    if snapshot.get("evidence_valid") is not True:
        return False
    if snapshot.get("evidence_item_count") != EVIDENCE_ITEM_COUNT:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_bundle"))


def _validate_bundle_report_case() -> dict[str, Any]:
    bundle = _load_json(TASK_3_BUNDLE_PATH)
    passed = (
        validate_query_result_evidence_bundle(bundle)
        and bundle.get("implementation_status") == "READY"
        and bundle.get("implementation_complete") is True
        and bundle.get("scope_lock_valid") is True
        and bundle.get("source_chain_valid") is True
        and bundle.get("evidence_valid") is True
        and bundle.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_3_EVIDENCE_BUNDLE_REPORT_VALID",
        passed,
        {
            "implementation_status": "READY",
            "implementation_complete": True,
            "scope_lock_valid": True,
            "source_chain_valid": True,
            "evidence_valid": True,
        },
        {
            "implementation_status": bundle.get("implementation_status"),
            "implementation_complete": bundle.get("implementation_complete"),
            "scope_lock_valid": bundle.get("scope_lock_valid"),
            "source_chain_valid": bundle.get("source_chain_valid"),
            "evidence_valid": bundle.get("evidence_valid"),
            "next_stage": bundle.get("next_stage"),
        },
        "TASK_3_EVIDENCE_BUNDLE_REPORT_INVALID",
    )


def _validate_runtime_stability_case() -> dict[str, Any]:
    snapshot = build_bundle_snapshot()
    passed = validate_bundle_snapshot(snapshot)
    return _case(
        "TASK_3_EVIDENCE_BUNDLE_RUNTIME_STABILITY_VALID",
        passed,
        {"stable_bundle": True},
        snapshot,
        "TASK_3_EVIDENCE_BUNDLE_RUNTIME_STABILITY_INVALID",
    )


def _validate_artifact_set_case() -> dict[str, Any]:
    paths = (
        TASK_3_BUNDLE_PATH,
        TASK_3_EVIDENCE_INDEX_PATH,
        TASK_3_MANIFEST_PATH,
        TASK_3_INDEX_PATH,
        TASK_3_MARKDOWN_PATH,
    )
    missing = [str(path) for path in paths if not path.exists()]
    readable = []
    for path in paths:
        if path.exists():
            readable.append(path.read_text(encoding="utf-8") != "")
    passed = not missing and all(readable)
    return _case(
        "TASK_3_EVIDENCE_BUNDLE_ARTIFACT_SET_PRESENT",
        passed,
        {"artifact_count": 5, "missing": []},
        {"artifact_count": len(paths), "missing": missing, "readable_count": sum(1 for item in readable if item)},
        "TASK_3_EVIDENCE_BUNDLE_ARTIFACT_SET_INCOMPLETE",
    )


def _validate_manifest_case() -> dict[str, Any]:
    bundle = _load_json(TASK_3_BUNDLE_PATH)
    manifest = _load_json(TASK_3_MANIFEST_PATH)
    passed = (
        manifest.get("task_id") == SOURCE_TASK_ID
        and manifest.get("source_task_id") == bundle.get("source_task_id")
        and manifest.get("evidence_bundle_id") == bundle.get("evidence_bundle_id")
        and manifest.get("evidence_bundle_signature") == bundle.get("evidence_bundle_signature")
        and manifest.get("implementation_status") == bundle.get("implementation_status") == "READY"
        and manifest.get("implementation_complete") is True
        and manifest.get("scope_lock_valid") is True
        and manifest.get("source_chain_valid") is True
        and manifest.get("evidence_valid") is True
        and manifest.get("evidence_item_count") == bundle.get("evidence_item_count") == EVIDENCE_ITEM_COUNT
        and manifest.get("next_stage") == SOURCE_NEXT_STAGE
    )
    return _case(
        "TASK_3_EVIDENCE_BUNDLE_MANIFEST_CONSISTENCY_VALID",
        passed,
        {"manifest_matches_bundle": True},
        {
            "manifest_bundle_id": manifest.get("evidence_bundle_id"),
            "bundle_id": bundle.get("evidence_bundle_id"),
            "manifest_status": manifest.get("implementation_status"),
            "manifest_next_stage": manifest.get("next_stage"),
        },
        "TASK_3_EVIDENCE_BUNDLE_MANIFEST_CONSISTENCY_INVALID",
    )


def _validate_index_case() -> dict[str, Any]:
    bundle = _load_json(TASK_3_BUNDLE_PATH)
    index = TASK_3_INDEX_PATH.read_text(encoding="utf-8")
    required_markers = (
        "MILESTONE_29_TASK_3_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_READY=true",
        f"EVIDENCE_BUNDLE_ID={bundle.get('evidence_bundle_id')}",
        f"EVIDENCE_BUNDLE_SIGNATURE={bundle.get('evidence_bundle_signature')}",
        "IMPLEMENTATION_STATUS=READY",
        "IMPLEMENTATION_STARTED=true",
        "IMPLEMENTATION_COMPLETE=true",
        "SCOPE_LOCK_VALID=true",
        "SOURCE_CHAIN_VALID=true",
        "EVIDENCE_VALID=true",
        "EVIDENCE_ITEM_COUNT=6",
        "LOCAL_ONLY=true",
        "NETWORK_ACCESS_ALLOWED=false",
        "SHELL_EXECUTION_ALLOWED=false",
        f"NEXT_STAGE={SOURCE_NEXT_STAGE}",
    )
    missing = [marker for marker in required_markers if marker not in index]
    passed = not missing
    return _case(
        "TASK_3_EVIDENCE_BUNDLE_INDEX_MARKERS_VALID",
        passed,
        {"missing_markers": []},
        {"missing_markers": missing, "required_marker_count": len(required_markers)},
        "TASK_3_EVIDENCE_BUNDLE_INDEX_MARKERS_INVALID",
    )


def _validate_evidence_index_case() -> dict[str, Any]:
    bundle = _load_json(TASK_3_BUNDLE_PATH)
    evidence_index = _load_json(TASK_3_EVIDENCE_INDEX_PATH)
    passed = (
        evidence_index.get("task_id") == SOURCE_TASK_ID
        and evidence_index.get("evidence_bundle_id") == bundle.get("evidence_bundle_id")
        and evidence_index.get("evidence_bundle_signature") == bundle.get("evidence_bundle_signature")
        and evidence_index.get("evidence_item_count") == bundle.get("evidence_item_count") == EVIDENCE_ITEM_COUNT
        and evidence_index.get("evidence_items") == bundle.get("evidence_items")
        and validate_evidence_items(evidence_index.get("evidence_items", []))
    )
    return _case(
        "TASK_3_EVIDENCE_INDEX_CONSISTENCY_VALID",
        passed,
        {"evidence_index_matches_bundle": True},
        {
            "index_bundle_id": evidence_index.get("evidence_bundle_id"),
            "bundle_id": bundle.get("evidence_bundle_id"),
            "index_item_count": evidence_index.get("evidence_item_count"),
            "bundle_item_count": bundle.get("evidence_item_count"),
        },
        "TASK_3_EVIDENCE_INDEX_CONSISTENCY_INVALID",
    )


def _validate_evidence_digest_case() -> dict[str, Any]:
    bundle = _load_json(TASK_3_BUNDLE_PATH)
    observed = []
    for item in bundle.get("evidence_items", []):
        path = Path(str(item.get("path")))
        observed.append(
            {
                "path": str(path),
                "expected_sha256": item.get("sha256"),
                "observed_sha256": _sha256_file(path) if path.exists() else "MISSING",
                "exists": path.exists(),
            }
        )
    source_paths = {str(path) for path in evidence_source_paths()}
    passed = (
        len(observed) == EVIDENCE_ITEM_COUNT
        and all(item["exists"] for item in observed)
        and all(item["expected_sha256"] == item["observed_sha256"] for item in observed)
        and {item["path"] for item in observed} == source_paths
    )
    return _case(
        "TASK_3_EVIDENCE_DIGESTS_VALID",
        passed,
        {"digest_match": True, "evidence_item_count": EVIDENCE_ITEM_COUNT},
        observed,
        "TASK_3_EVIDENCE_DIGESTS_INVALID",
    )


def _validate_source_chain_case() -> dict[str, Any]:
    bundle = _load_json(TASK_3_BUNDLE_PATH)
    source_chain = bundle.get("source_chain", {})
    passed = (
        bundle.get("source_chain_valid") is True
        and source_chain.get("export_status") == "READY"
        and source_chain.get("exported_record_count") == 1
        and source_chain.get("validation_status") == "VALID"
        and source_chain.get("validation_pass_count") == 6
        and source_chain.get("validation_fail_count") == 0
        and source_chain.get("integration_status") == "VALID"
        and source_chain.get("integration_pass_count") == 7
        and source_chain.get("integration_fail_count") == 0
        and source_chain.get("closure_status") == "CLOSED"
        and source_chain.get("technical_status") == "PASS"
        and source_chain.get("process_status") == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    )
    return _case(
        "TASK_3_SOURCE_CHAIN_STATUS_VALID",
        passed,
        {
            "export_status": "READY",
            "validation_status": "VALID",
            "integration_status": "VALID",
            "closure_status": "CLOSED",
        },
        source_chain,
        "TASK_3_SOURCE_CHAIN_STATUS_INVALID",
    )


def run_query_result_evidence_bundle_validation() -> dict[str, Any]:
    case_results = [
        _validate_bundle_report_case(),
        _validate_runtime_stability_case(),
        _validate_artifact_set_case(),
        _validate_manifest_case(),
        _validate_index_case(),
        _validate_evidence_index_case(),
        _validate_evidence_digest_case(),
        _validate_source_chain_case(),
    ]

    pass_count = sum(1 for case in case_results if case["passed"])
    fail_count = len(case_results) - pass_count
    validation_passed = (
        len(case_results) == VALIDATION_CASE_COUNT
        and pass_count == REQUIRED_PASS_COUNT
        and fail_count == REQUIRED_FAIL_COUNT
    )

    bundle = _load_json(TASK_3_BUNDLE_PATH)

    report = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "evidence_bundle_revision": EVIDENCE_BUNDLE_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "source_evidence_bundle_id": bundle.get("evidence_bundle_id"),
        "source_evidence_bundle_signature": bundle.get("evidence_bundle_signature"),
        "source_implementation_status": bundle.get("implementation_status"),
        "source_scope_lock_valid": bundle.get("scope_lock_valid"),
        "source_chain_valid": bundle.get("source_chain_valid"),
        "source_evidence_valid": bundle.get("evidence_valid"),
        "validation_status": VALIDATION_STATUS if validation_passed else "INVALID",
        "validation_case_count": len(case_results),
        "required_pass_count": REQUIRED_PASS_COUNT,
        "required_fail_count": REQUIRED_FAIL_COUNT,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "validation_passed": validation_passed,
        "case_results": case_results,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    report["validation_id"] = "MILESTONE-29-QUERY-RESULT-EVIDENCE-BUNDLE-VALIDATION-" + _stable_digest(report)
    report["validation_signature"] = _stable_digest(
        {
            "validation_id": report["validation_id"],
            "source_evidence_bundle_id": report["source_evidence_bundle_id"],
            "source_evidence_bundle_signature": report["source_evidence_bundle_signature"],
            "task_3_signature": report["task_3_signature"],
            "task_4_signature": report["task_4_signature"],
            "case_results": case_results,
            "validation_revision": VALIDATION_REVISION,
        }
    )
    return report


def validate_validation_report(report: Mapping[str, Any]) -> bool:
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
    if report.get("task_3_signature") != task_3_signature():
        return False
    if report.get("task_4_signature") != task_4_signature():
        return False
    if report.get("source_implementation_status") != "READY":
        return False
    if report.get("source_scope_lock_valid") is not True:
        return False
    if report.get("source_chain_valid") is not True:
        return False
    if report.get("source_evidence_valid") is not True:
        return False
    if report.get("validation_status") != VALIDATION_STATUS:
        return False
    if report.get("validation_case_count") != VALIDATION_CASE_COUNT:
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
    return bool(report.get("validation_passed") and report.get("validation_id") and report.get("validation_signature"))


def render_validation_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 29 Task 4 Query Result Evidence Bundle Validation",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"VALIDATION_ID={report.get('validation_id')}",
        f"VALIDATION_SIGNATURE={report.get('validation_signature')}",
        f"SOURCE_EVIDENCE_BUNDLE_ID={report.get('source_evidence_bundle_id')}",
        f"SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report.get('source_evidence_bundle_signature')}",
        f"VALIDATION_STATUS={report.get('validation_status')}",
        f"PASS_COUNT={report.get('pass_count')}",
        f"FAIL_COUNT={report.get('fail_count')}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Validation cases",
    ]
    for case in report.get("case_results", []):
        lines.append(f"- {case['case_id']} passed={str(case['passed']).lower()}")
    lines.append("")
    return "\n".join(lines)


def write_task_4_artifacts(base_dir: str | Path = "examples/milestone-29/query-result-evidence-bundle-validation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_query_result_evidence_bundle_validation()
    cases = {
        "task_id": TASK_ID,
        "validation_id": report["validation_id"],
        "validation_status": report["validation_status"],
        "validation_case_count": report["validation_case_count"],
        "case_results": report["case_results"],
    }
    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "validation_revision": VALIDATION_REVISION,
        "task_3_signature": task_3_signature(),
        "task_4_signature": task_4_signature(),
        "source_evidence_bundle_id": report["source_evidence_bundle_id"],
        "source_evidence_bundle_signature": report["source_evidence_bundle_signature"],
        "validation_id": report["validation_id"],
        "validation_signature": report["validation_signature"],
        "validation_status": report["validation_status"],
        "validation_passed": report["validation_passed"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-4-validation-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-validation-report.md").write_text(
        render_validation_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-4-validation-cases.json").write_text(
        json.dumps(cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-4-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_29_TASK_4_QUERY_RESULT_EVIDENCE_BUNDLE_VALIDATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"EVIDENCE_BUNDLE_REVISION={EVIDENCE_BUNDLE_REVISION}",
                f"VALIDATION_REVISION={VALIDATION_REVISION}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                f"TASK_4_SIGNATURE={task_4_signature()}",
                f"SOURCE_EVIDENCE_BUNDLE_ID={report['source_evidence_bundle_id']}",
                f"SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report['source_evidence_bundle_signature']}",
                f"SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}",
                f"SOURCE_SCOPE_LOCK_VALID={str(report['source_scope_lock_valid']).lower()}",
                f"SOURCE_CHAIN_VALID={str(report['source_chain_valid']).lower()}",
                f"SOURCE_EVIDENCE_VALID={str(report['source_evidence_valid']).lower()}",
                f"VALIDATION_ID={report['validation_id']}",
                f"VALIDATION_SIGNATURE={report['validation_signature']}",
                f"VALIDATION_STATUS={report['validation_status']}",
                f"VALIDATION_CASE_COUNT={report['validation_case_count']}",
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


def task_4_status_lines() -> tuple[str, ...]:
    report = run_query_result_evidence_bundle_validation()
    return (
        "MILESTONE_29_TASK_4_QUERY_RESULT_EVIDENCE_BUNDLE_VALIDATION_READY=true",
        f"MILESTONE_29_TASK_4_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_29_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_29_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_29_TASK_4_EVIDENCE_BUNDLE_REVISION={EVIDENCE_BUNDLE_REVISION}",
        f"MILESTONE_29_TASK_4_VALIDATION_REVISION={VALIDATION_REVISION}",
        f"MILESTONE_29_TASK_4_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_29_TASK_4_TASK_4_SIGNATURE={task_4_signature()}",
        f"MILESTONE_29_TASK_4_SOURCE_EVIDENCE_BUNDLE_ID={report['source_evidence_bundle_id']}",
        f"MILESTONE_29_TASK_4_SOURCE_EVIDENCE_BUNDLE_SIGNATURE={report['source_evidence_bundle_signature']}",
        f"MILESTONE_29_TASK_4_SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}",
        f"MILESTONE_29_TASK_4_SOURCE_SCOPE_LOCK_VALID={str(report['source_scope_lock_valid']).lower()}",
        f"MILESTONE_29_TASK_4_SOURCE_CHAIN_VALID={str(report['source_chain_valid']).lower()}",
        f"MILESTONE_29_TASK_4_SOURCE_EVIDENCE_VALID={str(report['source_evidence_valid']).lower()}",
        f"MILESTONE_29_TASK_4_VALIDATION_ID={report['validation_id']}",
        f"MILESTONE_29_TASK_4_VALIDATION_SIGNATURE={report['validation_signature']}",
        f"MILESTONE_29_TASK_4_VALIDATION_STATUS={report['validation_status']}",
        f"MILESTONE_29_TASK_4_VALIDATION_CASE_COUNT={report['validation_case_count']}",
        f"MILESTONE_29_TASK_4_PASS_COUNT={report['pass_count']}",
        f"MILESTONE_29_TASK_4_FAIL_COUNT={report['fail_count']}",
        f"MILESTONE_29_TASK_4_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_29_TASK_4_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_29_TASK_4_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_29_TASK_4_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_4_artifacts()
    for line in task_4_status_lines():
        print(line)
