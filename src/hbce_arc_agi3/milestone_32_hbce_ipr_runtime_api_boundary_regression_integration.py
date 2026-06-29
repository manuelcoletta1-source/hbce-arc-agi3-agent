"""Milestone 32 Task 5 regression integration for the HBCE IPR Runtime API v1 boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary_validation import (
    BOUNDARY_MODE_ID,
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_IMPLEMENTATION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    VALIDATION_CASE_COUNT as SOURCE_VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    run_milestone_32_boundary_validation,
    task_4_signature,
    validate_milestone_32_boundary_validation_report,
)

TASK_ID = "MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_V1"
SOURCE_VALIDATION_TASK_ID = SOURCE_TASK_ID
SOURCE_SCOPE_TASK_ID = "MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
SOURCE_OPENING_TASK_ID = "MILESTONE_32_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"

REGRESSION_INTEGRATION_REVISION = "MILESTONE_32_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_V1"
REGRESSION_INTEGRATION_STATUS = "VALID"

CURRENT_TASK_NUMBER = 5
REGRESSION_CASE_COUNT = 12
REQUIRED_PASS_COUNT = 12
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = "MILESTONE_32_TASK_6_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_FINAL_CLOSURE_V1"

ARTIFACT_DIR = Path("examples/milestone-32/hbce-ipr-runtime-api-v1-operational-identity-proof-layer-boundary-regression-integration-v1")
TASK_1_DOC_PATH = Path("docs/milestone-32-task-1-governed-opening-with-task-budget-v1.md")
TASK_2_DOC_PATH = Path("docs/milestone-32-task-2-objective-selection-and-scope-lock-v1.md")
TASK_3_DOC_PATH = Path("docs/milestone-32-task-3-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-implementation-v1.md")
TASK_4_DOC_PATH = Path("docs/milestone-32-task-4-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-validation-v1.md")


def _stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()[:16]


def task_5_signature() -> str:
    return _stable_hash(
        {
            "task_id": TASK_ID,
            "source_validation_task_id": SOURCE_VALIDATION_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "boundary_mode_id": BOUNDARY_MODE_ID,
            "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
            "task_4_signature": task_4_signature(),
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


def _task_4_artifacts_present() -> bool:
    artifact_dir = Path("examples/milestone-32/hbce-ipr-runtime-api-v1-operational-identity-proof-layer-boundary-validation-v1")
    required = [
        "task-4-boundary-validation-report.json",
        "task-4-boundary-validation-report.md",
        "task-4-boundary-validation-cases.json",
        "task-4-manifest.json",
        "task-4-index.txt",
    ]
    return artifact_dir.exists() and all((artifact_dir / name).exists() for name in required)


def run_milestone_32_boundary_regression_integration() -> dict[str, Any]:
    source_report = run_milestone_32_boundary_validation()
    source_valid = validate_milestone_32_boundary_validation_report(source_report)

    blocked_results = source_report.get("blocked_validation_results", [])
    all_blocked_cases_remain_blocked = (
        isinstance(blocked_results, list)
        and len(blocked_results) == 6
        and all(item.get("status") == "BLOCKED" and item.get("validator_passed") is False for item in blocked_results)
    )

    complete_layer = source_report.get("complete_layer", {})
    validation_cases = source_report.get("validation_cases", [])
    validation_cases_valid = (
        source_report.get("validation_case_count") == SOURCE_VALIDATION_CASE_COUNT
        and len(validation_cases) == SOURCE_VALIDATION_CASE_COUNT
        and all(case.get("passed") is True and case.get("failure_reason") == "NONE" for case in validation_cases)
    )

    cases = [
        _case(
            "TASK_4_VALIDATION_REMAINS_VALID",
            source_valid and source_report.get("validation_status") == "VALID" and source_report.get("validation_passed") is True,
            "Task 4 validation remains VALID",
            {
                "validation_status": source_report.get("validation_status"),
                "validation_passed": source_report.get("validation_passed"),
                "pass_count": source_report.get("pass_count"),
                "fail_count": source_report.get("fail_count"),
            },
        ),
        _case(
            "TASK_4_VALIDATION_CASES_REMAIN_VALID",
            validation_cases_valid,
            SOURCE_VALIDATION_CASE_COUNT,
            {
                "validation_case_count": source_report.get("validation_case_count"),
                "all_cases_passed": all(case.get("passed") is True for case in validation_cases),
            },
        ),
        _case(
            "TASK_4_ARTIFACT_SET_REMAINS_PRESENT",
            _task_4_artifacts_present(),
            "Task 4 persisted artifact set present",
            "present" if _task_4_artifacts_present() else "missing",
        ),
        _case(
            "TASK_4_TO_TASK_5_TRANSITION_CONFIRMED",
            SOURCE_NEXT_STAGE == TASK_ID and source_report.get("next_stage") == TASK_ID,
            TASK_ID,
            {"source_constant_next_stage": SOURCE_NEXT_STAGE, "source_report_next_stage": source_report.get("next_stage")},
        ),
        _case(
            "COMPLETE_LAYER_REMAINS_READY",
            complete_layer.get("proof_layer_status") == "READY" and complete_layer.get("proof_layer_passed") is True,
            {"proof_layer_status": "READY", "proof_layer_passed": True},
            {"proof_layer_status": complete_layer.get("proof_layer_status"), "proof_layer_passed": complete_layer.get("proof_layer_passed")},
        ),
        _case(
            "MISSING_REQUIRED_LINKS_REMAIN_FAIL_CLOSED",
            all_blocked_cases_remain_blocked,
            "six missing-link probes remain BLOCKED",
            blocked_results,
        ),
        _case(
            "LEGAL_BOUNDARY_REMAINS_FALSE_CERTIFICATION",
            source_report.get("legal_certification") is False
            and source_report.get("opc_technical_proof_receipt_only") is True
            and source_report.get("ipr_card_official_public_identity_document") is False
            and source_report.get("explicit_legal_boundary_required") is True,
            {
                "legalCertification": False,
                "opcTechnicalProofReceiptOnly": True,
                "iprCardOfficialPublicIdentityDocument": False,
                "explicitLegalBoundaryRequired": True,
            },
            {
                "legalCertification": source_report.get("legal_certification"),
                "opcTechnicalProofReceiptOnly": source_report.get("opc_technical_proof_receipt_only"),
                "iprCardOfficialPublicIdentityDocument": source_report.get("ipr_card_official_public_identity_document"),
                "explicitLegalBoundaryRequired": source_report.get("explicit_legal_boundary_required"),
            },
        ),
        _case(
            "TASK_4_DOCUMENT_MARKERS_REMAIN_PRESENT",
            _doc_contains(TASK_4_DOC_PATH, "MILESTONE_32_TASK_4_VALIDATION_STATUS=VALID")
            and _doc_contains(TASK_4_DOC_PATH, "MILESTONE_32_TASK_4_LEGAL_CERTIFICATION=false")
            and _doc_contains(TASK_4_DOC_PATH, f"MILESTONE_32_TASK_4_NEXT_STAGE={TASK_ID}"),
            "Task 4 validation doc remains aligned",
            str(TASK_4_DOC_PATH),
        ),
        _case(
            "TASK_3_IMPLEMENTATION_CHAIN_REMAINS_READY",
            _doc_contains(TASK_3_DOC_PATH, "MILESTONE_32_TASK_3_IMPLEMENTATION_STATUS=READY")
            and _doc_contains(TASK_3_DOC_PATH, "MILESTONE_32_TASK_3_LEGAL_CERTIFICATION=false"),
            "Task 3 implementation doc remains ready",
            str(TASK_3_DOC_PATH),
        ),
        _case(
            "TASK_2_SCOPE_LOCK_CHAIN_REMAINS_LOCKED",
            _doc_contains(TASK_2_DOC_PATH, f"MILESTONE_32_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}")
            and _doc_contains(TASK_2_DOC_PATH, "MILESTONE_32_TASK_2_SCOPE_LOCK_STATUS=LOCKED")
            and _doc_contains(TASK_2_DOC_PATH, "MILESTONE_32_TASK_2_LEGAL_CERTIFICATION=false"),
            "Task 2 scope lock doc remains locked",
            str(TASK_2_DOC_PATH),
        ),
        _case(
            "TASK_1_GOVERNED_OPENING_CHAIN_REMAINS_READY",
            _doc_contains(TASK_1_DOC_PATH, "MILESTONE_32_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true")
            and _doc_contains(TASK_1_DOC_PATH, "MILESTONE_32_TASK_1_OPENING_STATUS=READY"),
            "Task 1 governed opening doc remains ready",
            str(TASK_1_DOC_PATH),
        ),
        _case(
            "TASK_BUDGET_AND_FINAL_CLOSURE_STAGE_READY",
            TASK_BUDGET_MAX == 8 and SOURCE_CURRENT_TASK_NUMBER == 4 and CURRENT_TASK_NUMBER == 5 and NEXT_STAGE.endswith("_FINAL_CLOSURE_V1"),
            {"task_budget_max": 8, "source_current_task_number": 4, "current_task_number": 5, "next_stage_suffix": "_FINAL_CLOSURE_V1"},
            {"task_budget_max": TASK_BUDGET_MAX, "source_current_task_number": SOURCE_CURRENT_TASK_NUMBER, "current_task_number": CURRENT_TASK_NUMBER, "next_stage": NEXT_STAGE},
        ),
    ]

    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    integration_passed = pass_count == REQUIRED_PASS_COUNT and fail_count == REQUIRED_FAIL_COUNT
    integration_status = REGRESSION_INTEGRATION_STATUS if integration_passed else "INVALID"

    integration_id = "MILESTONE-32-HBCE-IPR-RUNTIME-API-BOUNDARY-INTEGRATION-" + _stable_hash(
        {
            "task_id": TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "task_5_signature": task_5_signature(),
            "source_validation_id": source_report.get("validation_id"),
            "integration_status": integration_status,
        }
    )

    integration_signature = _stable_hash(
        {
            "integration_id": integration_id,
            "task_id": TASK_ID,
            "source_validation_signature": source_report.get("validation_signature"),
            "task_5_signature": task_5_signature(),
            "integration_status": integration_status,
            "integration_passed": integration_passed,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        "task_id": TASK_ID,
        "source_validation_task_id": SOURCE_VALIDATION_TASK_ID,
        "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
        "source_scope_task_id": SOURCE_SCOPE_TASK_ID,
        "source_opening_task_id": SOURCE_OPENING_TASK_ID,
        "source_validation_revision": VALIDATION_REVISION,
        "source_task_4_signature": task_4_signature(),
        "source_validation_id": source_report.get("validation_id"),
        "source_validation_signature": source_report.get("validation_signature"),
        "source_validation_status": source_report.get("validation_status"),
        "source_validation_passed": source_report.get("validation_passed"),
        "source_validation_case_count": source_report.get("validation_case_count"),
        "source_pass_count": source_report.get("pass_count"),
        "source_fail_count": source_report.get("fail_count"),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_5_signature": task_5_signature(),
        "integration_id": integration_id,
        "integration_signature": integration_signature,
        "integration_status": integration_status,
        "integration_case_count": len(cases),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "integration_passed": integration_passed,
        "opc_technical_proof_receipt_only": source_report.get("opc_technical_proof_receipt_only"),
        "legal_certification": source_report.get("legal_certification"),
        "ipr_card_internal_operational_identity_certificate": source_report.get("ipr_card_internal_operational_identity_certificate"),
        "ipr_card_official_public_identity_document": source_report.get("ipr_card_official_public_identity_document"),
        "explicit_legal_boundary_required": source_report.get("explicit_legal_boundary_required"),
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "source_generated_artifact_count": SOURCE_GENERATED_ARTIFACT_COUNT,
        "integration_cases": cases,
        "next_stage": NEXT_STAGE,
    }


def validate_milestone_32_boundary_regression_integration_report(report: dict[str, Any]) -> bool:
    required = {
        "task_id": TASK_ID,
        "source_validation_task_id": SOURCE_VALIDATION_TASK_ID,
        "source_task_4_signature": task_4_signature(),
        "source_validation_status": "VALID",
        "source_validation_passed": True,
        "source_validation_case_count": SOURCE_VALIDATION_CASE_COUNT,
        "source_pass_count": 12,
        "source_fail_count": 0,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_5_signature": task_5_signature(),
        "integration_status": REGRESSION_INTEGRATION_STATUS,
        "integration_case_count": REGRESSION_CASE_COUNT,
        "pass_count": REQUIRED_PASS_COUNT,
        "fail_count": REQUIRED_FAIL_COUNT,
        "integration_passed": True,
        "opc_technical_proof_receipt_only": True,
        "legal_certification": False,
        "ipr_card_internal_operational_identity_certificate": True,
        "ipr_card_official_public_identity_document": False,
        "explicit_legal_boundary_required": True,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    if any(report.get(key) != value for key, value in required.items()):
        return False

    cases = report.get("integration_cases")
    if not isinstance(cases, list) or len(cases) != REGRESSION_CASE_COUNT:
        return False

    return all(case.get("passed") is True and case.get("failure_reason") == "NONE" for case in cases)


def _report_markdown(report: dict[str, Any]) -> str:
    case_lines = "\n".join(
        f"- {case['case_id']}: {'PASS' if case['passed'] else 'FAIL'}"
        for case in report["integration_cases"]
    )
    return f"""# Milestone 32 Task 5 - HBCE IPR Runtime API v1 Boundary Regression Integration v1

MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_READY=true

MILESTONE_32_TASK_5_TASK_ID={report['task_id']}
MILESTONE_32_TASK_5_SOURCE_VALIDATION_TASK_ID={report['source_validation_task_id']}
MILESTONE_32_TASK_5_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_32_TASK_5_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_32_TASK_5_BOUNDARY_MODE_ID={report['boundary_mode_id']}
MILESTONE_32_TASK_5_REGRESSION_INTEGRATION_REVISION={report['regression_integration_revision']}

MILESTONE_32_TASK_5_SOURCE_VALIDATION_STATUS={report['source_validation_status']}
MILESTONE_32_TASK_5_SOURCE_VALIDATION_PASSED={str(report['source_validation_passed']).lower()}
MILESTONE_32_TASK_5_SOURCE_VALIDATION_CASE_COUNT={report['source_validation_case_count']}

MILESTONE_32_TASK_5_INTEGRATION_ID={report['integration_id']}
MILESTONE_32_TASK_5_INTEGRATION_SIGNATURE={report['integration_signature']}
MILESTONE_32_TASK_5_INTEGRATION_STATUS={report['integration_status']}
MILESTONE_32_TASK_5_INTEGRATION_CASE_COUNT={report['integration_case_count']}
MILESTONE_32_TASK_5_PASS_COUNT={report['pass_count']}
MILESTONE_32_TASK_5_FAIL_COUNT={report['fail_count']}
MILESTONE_32_TASK_5_INTEGRATION_PASSED={str(report['integration_passed']).lower()}

MILESTONE_32_TASK_5_OPC_TECHNICAL_PROOF_RECEIPT_ONLY={str(report['opc_technical_proof_receipt_only']).lower()}
MILESTONE_32_TASK_5_LEGAL_CERTIFICATION={str(report['legal_certification']).lower()}
MILESTONE_32_TASK_5_IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE={str(report['ipr_card_internal_operational_identity_certificate']).lower()}
MILESTONE_32_TASK_5_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT={str(report['ipr_card_official_public_identity_document']).lower()}

MILESTONE_32_TASK_5_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_32_TASK_5_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_32_TASK_5_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}

MILESTONE_32_TASK_5_NEXT_STAGE={report['next_stage']}

## Regression Integration Cases

{case_lines}
"""


def write_task_5_artifacts(base_dir: Path | str = ARTIFACT_DIR) -> dict[str, Any]:
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)

    report = run_milestone_32_boundary_regression_integration()
    if not validate_milestone_32_boundary_regression_integration_report(report):
        raise ValueError("Milestone 32 Task 5 boundary regression integration report is invalid")

    report_path = base / "task-5-boundary-regression-integration-report.json"
    markdown_path = base / "task-5-boundary-regression-integration-report.md"
    cases_path = base / "task-5-boundary-regression-integration-cases.json"
    manifest_path = base / "task-5-manifest.json"
    index_path = base / "task-5-index.txt"

    cases_payload = {
        "task_id": TASK_ID,
        "integration_id": report["integration_id"],
        "integration_status": report["integration_status"],
        "integration_case_count": report["integration_case_count"],
        "integration_cases": report["integration_cases"],
    }

    manifest = {
        "task_id": TASK_ID,
        "source_validation_task_id": SOURCE_VALIDATION_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_5_signature": task_5_signature(),
        "integration_id": report["integration_id"],
        "integration_signature": report["integration_signature"],
        "integration_status": report["integration_status"],
        "integration_passed": report["integration_passed"],
        "integration_case_count": report["integration_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    index = "\n".join(
        [
            "MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_READY=true",
            f"TASK_ID={TASK_ID}",
            f"SOURCE_VALIDATION_TASK_ID={SOURCE_VALIDATION_TASK_ID}",
            f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
            f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
            f"BOUNDARY_MODE_ID={BOUNDARY_MODE_ID}",
            f"REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}",
            f"TASK_5_SIGNATURE={task_5_signature()}",
            f"INTEGRATION_ID={report['integration_id']}",
            f"INTEGRATION_SIGNATURE={report['integration_signature']}",
            f"INTEGRATION_STATUS={report['integration_status']}",
            f"INTEGRATION_CASE_COUNT={report['integration_case_count']}",
            f"PASS_COUNT={report['pass_count']}",
            f"FAIL_COUNT={report['fail_count']}",
            f"INTEGRATION_PASSED={str(report['integration_passed']).lower()}",
            f"OPC_TECHNICAL_PROOF_RECEIPT_ONLY={str(report['opc_technical_proof_receipt_only']).lower()}",
            f"LEGAL_CERTIFICATION={str(report['legal_certification']).lower()}",
            f"IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE={str(report['ipr_card_internal_operational_identity_certificate']).lower()}",
            f"IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT={str(report['ipr_card_official_public_identity_document']).lower()}",
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

    return {"report": report, "manifest": manifest, "cases": cases_payload}


def main() -> None:
    artifacts = write_task_5_artifacts()
    report = artifacts["report"]

    print("MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_READY=true")
    print(f"MILESTONE_32_TASK_5_TASK_ID={TASK_ID}")
    print(f"MILESTONE_32_TASK_5_SOURCE_VALIDATION_TASK_ID={SOURCE_VALIDATION_TASK_ID}")
    print(f"MILESTONE_32_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}")
    print(f"MILESTONE_32_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}")
    print(f"MILESTONE_32_TASK_5_BOUNDARY_MODE_ID={BOUNDARY_MODE_ID}")
    print(f"MILESTONE_32_TASK_5_REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}")
    print(f"MILESTONE_32_TASK_5_TASK_5_SIGNATURE={task_5_signature()}")
    print(f"MILESTONE_32_TASK_5_INTEGRATION_ID={report['integration_id']}")
    print(f"MILESTONE_32_TASK_5_INTEGRATION_SIGNATURE={report['integration_signature']}")
    print(f"MILESTONE_32_TASK_5_INTEGRATION_STATUS={report['integration_status']}")
    print(f"MILESTONE_32_TASK_5_INTEGRATION_CASE_COUNT={report['integration_case_count']}")
    print(f"MILESTONE_32_TASK_5_PASS_COUNT={report['pass_count']}")
    print(f"MILESTONE_32_TASK_5_FAIL_COUNT={report['fail_count']}")
    print(f"MILESTONE_32_TASK_5_INTEGRATION_PASSED={str(report['integration_passed']).lower()}")
    print(f"MILESTONE_32_TASK_5_OPC_TECHNICAL_PROOF_RECEIPT_ONLY={str(report['opc_technical_proof_receipt_only']).lower()}")
    print(f"MILESTONE_32_TASK_5_LEGAL_CERTIFICATION={str(report['legal_certification']).lower()}")
    print(f"MILESTONE_32_TASK_5_IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE={str(report['ipr_card_internal_operational_identity_certificate']).lower()}")
    print(f"MILESTONE_32_TASK_5_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT={str(report['ipr_card_official_public_identity_document']).lower()}")
    print(f"MILESTONE_32_TASK_5_TASK_BUDGET_MAX={TASK_BUDGET_MAX}")
    print(f"MILESTONE_32_TASK_5_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}")
    print(f"MILESTONE_32_TASK_5_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}")
    print(f"MILESTONE_32_TASK_5_NEXT_STAGE={NEXT_STAGE}")


if __name__ == "__main__":
    main()
