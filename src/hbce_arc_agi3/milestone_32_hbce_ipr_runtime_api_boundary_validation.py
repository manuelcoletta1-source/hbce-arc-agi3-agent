"""Milestone 32 Task 4 validation for the HBCE IPR Runtime API v1 boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary import (
    BOUNDARY_MODE_ID,
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_REVISION,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    REQUIRED_LINK_KEYS,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_operational_identity_proof_layer,
    run_milestone_32_boundary_implementation,
    task_3_signature,
    validate_milestone_32_boundary_implementation_report,
    validate_operational_identity_proof_layer,
)

TASK_ID = "MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_V1"
SOURCE_IMPLEMENTATION_TASK_ID = SOURCE_TASK_ID
VALIDATION_REVISION = "MILESTONE_32_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_V1"
VALIDATION_STATUS = "VALID"

CURRENT_TASK_NUMBER = 4
VALIDATION_CASE_COUNT = 12
REQUIRED_PASS_COUNT = 12
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = "MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_V1"

ARTIFACT_DIR = Path("examples/milestone-32/hbce-ipr-runtime-api-v1-operational-identity-proof-layer-boundary-validation-v1")
SOURCE_DOC_PATH = Path("docs/milestone-32-task-3-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-implementation-v1.md")


def _stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()[:16]


def task_4_signature() -> str:
    return _stable_hash(
        {
            "task_id": TASK_ID,
            "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "validation_revision": VALIDATION_REVISION,
            "task_3_signature": task_3_signature(),
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


def _complete_layer() -> dict[str, Any]:
    return build_operational_identity_proof_layer(
        operational_subject_id="IPR-OPERATIONAL-SUBJECT-MANUEL-VERIFIED",
        governed_session_id="GOVERNED-SESSION-HBCE-IPR-RUNTIME-API-V1",
        event_trace_id="EVT-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
        technical_proof_receipt_id="OPC-HBCE-IPR-RUNTIME-API-V1-TECHNICAL-PROOF",
        audit_record_id="AUDIT-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
        model_usage_record_id="USAGE-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
    )


def _blocked_layer(missing_parameter: str) -> dict[str, Any]:
    kwargs = {
        "operational_subject_id": "IPR-OPERATIONAL-SUBJECT-MANUEL-VERIFIED",
        "governed_session_id": "GOVERNED-SESSION-HBCE-IPR-RUNTIME-API-V1",
        "event_trace_id": "EVT-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
        "technical_proof_receipt_id": "OPC-HBCE-IPR-RUNTIME-API-V1-TECHNICAL-PROOF",
        "audit_record_id": "AUDIT-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
        "model_usage_record_id": "USAGE-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
    }
    kwargs[missing_parameter] = ""
    return build_operational_identity_proof_layer(**kwargs)


def _blocked_validation_result(layer_key: str, parameter_name: str) -> dict[str, Any]:
    layer = _blocked_layer(parameter_name)
    return {
        "layer_key": layer_key,
        "parameter_name": parameter_name,
        "status": layer["proof_layer_status"],
        "missing_required_links": layer["missing_required_links"],
        "validator_passed": validate_operational_identity_proof_layer(layer),
    }


def run_milestone_32_boundary_validation() -> dict[str, Any]:
    source_report = run_milestone_32_boundary_implementation()
    source_valid = validate_milestone_32_boundary_implementation_report(source_report)
    complete_layer = _complete_layer()

    blocked_results = [
        _blocked_validation_result("verified_operational_subject", "operational_subject_id"),
        _blocked_validation_result("governed_session", "governed_session_id"),
        _blocked_validation_result("event_trace", "event_trace_id"),
        _blocked_validation_result("technical_proof_receipt", "technical_proof_receipt_id"),
        _blocked_validation_result("audit_record", "audit_record_id"),
        _blocked_validation_result("model_usage_record", "model_usage_record_id"),
    ]

    cases = [
        _case(
            "TASK_3_IMPLEMENTATION_REMAINS_READY",
            source_valid and source_report.get("implementation_status") == "READY" and source_report.get("implementation_passed") is True,
            "Task 3 implementation remains READY",
            {"implementation_status": source_report.get("implementation_status"), "implementation_passed": source_report.get("implementation_passed")},
        ),
        _case(
            "TASK_3_TO_TASK_4_TRANSITION_CONFIRMED",
            SOURCE_NEXT_STAGE == TASK_ID and source_report.get("next_stage") == TASK_ID,
            TASK_ID,
            {"source_constant_next_stage": SOURCE_NEXT_STAGE, "source_report_next_stage": source_report.get("next_stage")},
        ),
        _case(
            "TASK_3_DOCUMENT_BOUNDARY_MARKERS_PRESENT",
            _doc_contains(SOURCE_DOC_PATH, "MILESTONE_32_TASK_3_IMPLEMENTATION_STATUS=READY")
            and _doc_contains(SOURCE_DOC_PATH, "MILESTONE_32_TASK_3_LEGAL_CERTIFICATION=false")
            and _doc_contains(SOURCE_DOC_PATH, "MILESTONE_32_TASK_3_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false"),
            "Task 3 implementation doc has READY and boundary markers",
            str(SOURCE_DOC_PATH),
        ),
        _case(
            "COMPLETE_PROOF_LAYER_VALIDATES",
            validate_operational_identity_proof_layer(complete_layer),
            "complete proof layer validates",
            complete_layer["proof_layer_id"],
        ),
        _case(
            "MISSING_VERIFIED_OPERATIONAL_SUBJECT_BLOCKS",
            blocked_results[0]["validator_passed"] is False and blocked_results[0]["status"] == "BLOCKED",
            "missing verified operational subject blocks",
            blocked_results[0],
        ),
        _case(
            "MISSING_GOVERNED_SESSION_BLOCKS",
            blocked_results[1]["validator_passed"] is False and blocked_results[1]["status"] == "BLOCKED",
            "missing governed session blocks",
            blocked_results[1],
        ),
        _case(
            "MISSING_EVENT_TRACE_BLOCKS",
            blocked_results[2]["validator_passed"] is False and blocked_results[2]["status"] == "BLOCKED",
            "missing event trace blocks",
            blocked_results[2],
        ),
        _case(
            "MISSING_TECHNICAL_PROOF_RECEIPT_BLOCKS",
            blocked_results[3]["validator_passed"] is False and blocked_results[3]["status"] == "BLOCKED",
            "missing technical proof receipt blocks",
            blocked_results[3],
        ),
        _case(
            "MISSING_AUDIT_RECORD_BLOCKS",
            blocked_results[4]["validator_passed"] is False and blocked_results[4]["status"] == "BLOCKED",
            "missing audit record blocks",
            blocked_results[4],
        ),
        _case(
            "MISSING_MODEL_USAGE_RECORD_BLOCKS",
            blocked_results[5]["validator_passed"] is False and blocked_results[5]["status"] == "BLOCKED",
            "missing model usage record blocks",
            blocked_results[5],
        ),
        _case(
            "LEGAL_BOUNDARY_REMAINS_EXPLICIT_AND_FALSE_CERTIFICATION",
            complete_layer["legal_certification"] is False
            and complete_layer["opc_technical_proof_receipt_only"] is True
            and complete_layer["ipr_card_official_public_identity_document"] is False
            and complete_layer["explicit_legal_boundary_required"] is True,
            {
                "legalCertification": False,
                "opcTechnicalProofReceiptOnly": True,
                "iprCardOfficialPublicIdentityDocument": False,
                "explicitLegalBoundaryRequired": True,
            },
            {
                "legalCertification": complete_layer["legal_certification"],
                "opcTechnicalProofReceiptOnly": complete_layer["opc_technical_proof_receipt_only"],
                "iprCardOfficialPublicIdentityDocument": complete_layer["ipr_card_official_public_identity_document"],
                "explicitLegalBoundaryRequired": complete_layer["explicit_legal_boundary_required"],
            },
        ),
        _case(
            "TASK_BUDGET_AND_NEXT_STAGE_VALIDATION_READY",
            TASK_BUDGET_MAX == 8 and SOURCE_CURRENT_TASK_NUMBER == 3 and CURRENT_TASK_NUMBER == 4 and NEXT_STAGE.endswith("_REGRESSION_INTEGRATION_V1"),
            {"task_budget_max": 8, "source_current_task_number": 3, "current_task_number": 4, "next_stage_suffix": "_REGRESSION_INTEGRATION_V1"},
            {"task_budget_max": TASK_BUDGET_MAX, "source_current_task_number": SOURCE_CURRENT_TASK_NUMBER, "current_task_number": CURRENT_TASK_NUMBER, "next_stage": NEXT_STAGE},
        ),
    ]

    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    validation_passed = pass_count == REQUIRED_PASS_COUNT and fail_count == REQUIRED_FAIL_COUNT
    validation_status = VALIDATION_STATUS if validation_passed else "INVALID"

    validation_id = "MILESTONE-32-HBCE-IPR-RUNTIME-API-BOUNDARY-VALIDATION-" + _stable_hash(
        {
            "task_id": TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "task_4_signature": task_4_signature(),
            "complete_layer_id": complete_layer["proof_layer_id"],
            "validation_status": validation_status,
        }
    )

    validation_signature = _stable_hash(
        {
            "validation_id": validation_id,
            "task_id": TASK_ID,
            "source_implementation_signature": source_report.get("implementation_signature"),
            "task_4_signature": task_4_signature(),
            "validation_status": validation_status,
            "validation_passed": validation_passed,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        "task_id": TASK_ID,
        "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
        "source_implementation_revision": IMPLEMENTATION_REVISION,
        "source_task_3_signature": task_3_signature(),
        "source_implementation_id": source_report.get("implementation_id"),
        "source_implementation_signature": source_report.get("implementation_signature"),
        "source_implementation_status": source_report.get("implementation_status"),
        "source_implementation_passed": source_report.get("implementation_passed"),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "validation_revision": VALIDATION_REVISION,
        "task_4_signature": task_4_signature(),
        "validation_id": validation_id,
        "validation_signature": validation_signature,
        "validation_status": validation_status,
        "validation_case_count": len(cases),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "validation_passed": validation_passed,
        "complete_layer": complete_layer,
        "blocked_validation_results": blocked_results,
        "required_link_keys": list(REQUIRED_LINK_KEYS),
        "opc_technical_proof_receipt_only": complete_layer["opc_technical_proof_receipt_only"],
        "legal_certification": complete_layer["legal_certification"],
        "ipr_card_internal_operational_identity_certificate": complete_layer["ipr_card_internal_operational_identity_certificate"],
        "ipr_card_official_public_identity_document": complete_layer["ipr_card_official_public_identity_document"],
        "explicit_legal_boundary_required": complete_layer["explicit_legal_boundary_required"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "source_generated_artifact_count": SOURCE_GENERATED_ARTIFACT_COUNT,
        "validation_cases": cases,
        "next_stage": NEXT_STAGE,
    }


def validate_milestone_32_boundary_validation_report(report: dict[str, Any]) -> bool:
    required = {
        "task_id": TASK_ID,
        "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
        "source_task_3_signature": task_3_signature(),
        "source_implementation_status": "READY",
        "source_implementation_passed": True,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "validation_revision": VALIDATION_REVISION,
        "task_4_signature": task_4_signature(),
        "validation_status": VALIDATION_STATUS,
        "validation_case_count": VALIDATION_CASE_COUNT,
        "pass_count": REQUIRED_PASS_COUNT,
        "fail_count": REQUIRED_FAIL_COUNT,
        "validation_passed": True,
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

    if not validate_operational_identity_proof_layer(report.get("complete_layer", {})):
        return False

    blocked_results = report.get("blocked_validation_results")
    if not isinstance(blocked_results, list) or len(blocked_results) != 6:
        return False

    if any(result.get("validator_passed") is not False or result.get("status") != "BLOCKED" for result in blocked_results):
        return False

    cases = report.get("validation_cases")
    if not isinstance(cases, list) or len(cases) != VALIDATION_CASE_COUNT:
        return False

    return all(case.get("passed") is True and case.get("failure_reason") == "NONE" for case in cases)


def _report_markdown(report: dict[str, Any]) -> str:
    case_lines = "\n".join(
        f"- {case['case_id']}: {'PASS' if case['passed'] else 'FAIL'}"
        for case in report["validation_cases"]
    )
    return f"""# Milestone 32 Task 4 - HBCE IPR Runtime API v1 Boundary Validation v1

MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_READY=true

MILESTONE_32_TASK_4_TASK_ID={report['task_id']}
MILESTONE_32_TASK_4_SOURCE_IMPLEMENTATION_TASK_ID={report['source_implementation_task_id']}
MILESTONE_32_TASK_4_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_32_TASK_4_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_32_TASK_4_BOUNDARY_MODE_ID={report['boundary_mode_id']}
MILESTONE_32_TASK_4_VALIDATION_REVISION={report['validation_revision']}

MILESTONE_32_TASK_4_VALIDATION_ID={report['validation_id']}
MILESTONE_32_TASK_4_VALIDATION_SIGNATURE={report['validation_signature']}
MILESTONE_32_TASK_4_VALIDATION_STATUS={report['validation_status']}
MILESTONE_32_TASK_4_VALIDATION_CASE_COUNT={report['validation_case_count']}
MILESTONE_32_TASK_4_PASS_COUNT={report['pass_count']}
MILESTONE_32_TASK_4_FAIL_COUNT={report['fail_count']}
MILESTONE_32_TASK_4_VALIDATION_PASSED={str(report['validation_passed']).lower()}

MILESTONE_32_TASK_4_OPC_TECHNICAL_PROOF_RECEIPT_ONLY={str(report['opc_technical_proof_receipt_only']).lower()}
MILESTONE_32_TASK_4_LEGAL_CERTIFICATION={str(report['legal_certification']).lower()}
MILESTONE_32_TASK_4_IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE={str(report['ipr_card_internal_operational_identity_certificate']).lower()}
MILESTONE_32_TASK_4_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT={str(report['ipr_card_official_public_identity_document']).lower()}

MILESTONE_32_TASK_4_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_32_TASK_4_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_32_TASK_4_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}

MILESTONE_32_TASK_4_NEXT_STAGE={report['next_stage']}

## Validation Cases

{case_lines}
"""


def write_task_4_artifacts(base_dir: Path | str = ARTIFACT_DIR) -> dict[str, Any]:
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)

    report = run_milestone_32_boundary_validation()
    if not validate_milestone_32_boundary_validation_report(report):
        raise ValueError("Milestone 32 Task 4 boundary validation report is invalid")

    report_path = base / "task-4-boundary-validation-report.json"
    markdown_path = base / "task-4-boundary-validation-report.md"
    cases_path = base / "task-4-boundary-validation-cases.json"
    manifest_path = base / "task-4-manifest.json"
    index_path = base / "task-4-index.txt"

    cases_payload = {
        "task_id": TASK_ID,
        "validation_id": report["validation_id"],
        "validation_status": report["validation_status"],
        "validation_case_count": report["validation_case_count"],
        "validation_cases": report["validation_cases"],
    }

    manifest = {
        "task_id": TASK_ID,
        "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "validation_revision": VALIDATION_REVISION,
        "task_4_signature": task_4_signature(),
        "source_task_3_signature": task_3_signature(),
        "validation_id": report["validation_id"],
        "validation_signature": report["validation_signature"],
        "validation_status": report["validation_status"],
        "validation_passed": report["validation_passed"],
        "validation_case_count": report["validation_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    index = "\n".join(
        [
            "MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_READY=true",
            f"TASK_ID={TASK_ID}",
            f"SOURCE_IMPLEMENTATION_TASK_ID={SOURCE_IMPLEMENTATION_TASK_ID}",
            f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
            f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
            f"BOUNDARY_MODE_ID={BOUNDARY_MODE_ID}",
            f"VALIDATION_REVISION={VALIDATION_REVISION}",
            f"TASK_4_SIGNATURE={task_4_signature()}",
            f"VALIDATION_ID={report['validation_id']}",
            f"VALIDATION_SIGNATURE={report['validation_signature']}",
            f"VALIDATION_STATUS={report['validation_status']}",
            f"VALIDATION_CASE_COUNT={report['validation_case_count']}",
            f"PASS_COUNT={report['pass_count']}",
            f"FAIL_COUNT={report['fail_count']}",
            f"VALIDATION_PASSED={str(report['validation_passed']).lower()}",
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
    artifacts = write_task_4_artifacts()
    report = artifacts["report"]

    print("MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_READY=true")
    print(f"MILESTONE_32_TASK_4_TASK_ID={TASK_ID}")
    print(f"MILESTONE_32_TASK_4_SOURCE_IMPLEMENTATION_TASK_ID={SOURCE_IMPLEMENTATION_TASK_ID}")
    print(f"MILESTONE_32_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}")
    print(f"MILESTONE_32_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}")
    print(f"MILESTONE_32_TASK_4_BOUNDARY_MODE_ID={BOUNDARY_MODE_ID}")
    print(f"MILESTONE_32_TASK_4_VALIDATION_REVISION={VALIDATION_REVISION}")
    print(f"MILESTONE_32_TASK_4_TASK_4_SIGNATURE={task_4_signature()}")
    print(f"MILESTONE_32_TASK_4_VALIDATION_ID={report['validation_id']}")
    print(f"MILESTONE_32_TASK_4_VALIDATION_SIGNATURE={report['validation_signature']}")
    print(f"MILESTONE_32_TASK_4_VALIDATION_STATUS={report['validation_status']}")
    print(f"MILESTONE_32_TASK_4_VALIDATION_CASE_COUNT={report['validation_case_count']}")
    print(f"MILESTONE_32_TASK_4_PASS_COUNT={report['pass_count']}")
    print(f"MILESTONE_32_TASK_4_FAIL_COUNT={report['fail_count']}")
    print(f"MILESTONE_32_TASK_4_VALIDATION_PASSED={str(report['validation_passed']).lower()}")
    print(f"MILESTONE_32_TASK_4_OPC_TECHNICAL_PROOF_RECEIPT_ONLY={str(report['opc_technical_proof_receipt_only']).lower()}")
    print(f"MILESTONE_32_TASK_4_LEGAL_CERTIFICATION={str(report['legal_certification']).lower()}")
    print(f"MILESTONE_32_TASK_4_IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE={str(report['ipr_card_internal_operational_identity_certificate']).lower()}")
    print(f"MILESTONE_32_TASK_4_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT={str(report['ipr_card_official_public_identity_document']).lower()}")
    print(f"MILESTONE_32_TASK_4_TASK_BUDGET_MAX={TASK_BUDGET_MAX}")
    print(f"MILESTONE_32_TASK_4_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}")
    print(f"MILESTONE_32_TASK_4_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}")
    print(f"MILESTONE_32_TASK_4_NEXT_STAGE={NEXT_STAGE}")


if __name__ == "__main__":
    main()
