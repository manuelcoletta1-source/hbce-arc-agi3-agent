"""Milestone 32 Task 3 implementation for the HBCE IPR Runtime API v1 boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_32_objective_scope_lock import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    OPC_TECHNICAL_PROOF_RECEIPT_ONLY,
    LEGAL_CERTIFICATION,
    IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE,
    IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT,
    EXPLICIT_LEGAL_BOUNDARY_REQUIRED,
    run_milestone_32_objective_scope_lock,
    task_2_signature,
    validate_milestone_32_objective_scope_lock_report,
)

TASK_ID = "MILESTONE_32_TASK_3_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_V1"
SOURCE_SCOPE_TASK_ID = SOURCE_TASK_ID
IMPLEMENTATION_REVISION = "MILESTONE_32_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_V1"
IMPLEMENTATION_STATUS = "READY"
BOUNDARY_MODE_ID = "HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY"

REQUIRED_LINK_KEYS = (
    "verified_operational_subject",
    "governed_session",
    "event_trace",
    "technical_proof_receipt",
    "audit_record",
    "model_usage_record",
    "explicit_legal_boundary",
)

CURRENT_TASK_NUMBER = 3
IMPLEMENTATION_CASE_COUNT = 11
REQUIRED_PASS_COUNT = 11
REQUIRED_FAIL_COUNT = 0
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = "MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_V1"

ARTIFACT_DIR = Path("examples/milestone-32/hbce-ipr-runtime-api-v1-operational-identity-proof-layer-boundary-implementation-v1")
SOURCE_DOC_PATH = Path("docs/milestone-32-task-2-objective-selection-and-scope-lock-v1.md")


def _stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()[:16]


def task_3_signature() -> str:
    return _stable_hash(
        {
            "task_id": TASK_ID,
            "source_scope_task_id": SOURCE_SCOPE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "implementation_revision": IMPLEMENTATION_REVISION,
            "boundary_mode_id": BOUNDARY_MODE_ID,
            "task_2_signature": task_2_signature(),
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


def build_operational_identity_proof_layer(
    *,
    operational_subject_id: str,
    governed_session_id: str,
    event_trace_id: str,
    technical_proof_receipt_id: str,
    audit_record_id: str,
    model_usage_record_id: str,
) -> dict[str, Any]:
    proof_links = {
        "verified_operational_subject": operational_subject_id,
        "governed_session": governed_session_id,
        "event_trace": event_trace_id,
        "technical_proof_receipt": technical_proof_receipt_id,
        "audit_record": audit_record_id,
        "model_usage_record": model_usage_record_id,
        "explicit_legal_boundary": "legalCertification=false; OPC technical proof receipt only; IPR Card internal operational identity certificate only",
    }

    missing = [key for key, value in proof_links.items() if not str(value).strip()]
    boundary_passed = not missing

    proof_layer_id = "HBCE-IPR-RUNTIME-API-V1-BOUNDARY-" + _stable_hash(
        {
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "proof_links": proof_links,
            "legal_certification": LEGAL_CERTIFICATION,
            "opc_technical_proof_receipt_only": OPC_TECHNICAL_PROOF_RECEIPT_ONLY,
        }
    )

    return {
        "proof_layer_id": proof_layer_id,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "proof_links": proof_links,
        "missing_required_links": missing,
        "proof_layer_status": "READY" if boundary_passed else "BLOCKED",
        "proof_layer_passed": boundary_passed,
        "opc_technical_proof_receipt_only": OPC_TECHNICAL_PROOF_RECEIPT_ONLY,
        "legal_certification": LEGAL_CERTIFICATION,
        "ipr_card_internal_operational_identity_certificate": IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE,
        "ipr_card_official_public_identity_document": IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT,
        "explicit_legal_boundary_required": EXPLICIT_LEGAL_BOUNDARY_REQUIRED,
    }


def validate_operational_identity_proof_layer(layer: dict[str, Any]) -> bool:
    links = layer.get("proof_links")
    if not isinstance(links, dict):
        return False

    if any(not str(links.get(key, "")).strip() for key in REQUIRED_LINK_KEYS):
        return False

    return (
        layer.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and layer.get("scope_lock_id") == SCOPE_LOCK_ID
        and layer.get("proof_layer_status") == "READY"
        and layer.get("proof_layer_passed") is True
        and layer.get("opc_technical_proof_receipt_only") is True
        and layer.get("legal_certification") is False
        and layer.get("ipr_card_internal_operational_identity_certificate") is True
        and layer.get("ipr_card_official_public_identity_document") is False
        and layer.get("explicit_legal_boundary_required") is True
    )


def run_milestone_32_boundary_implementation() -> dict[str, Any]:
    source_report = run_milestone_32_objective_scope_lock()
    source_valid = validate_milestone_32_objective_scope_lock_report(source_report)

    sample_layer = build_operational_identity_proof_layer(
        operational_subject_id="IPR-OPERATIONAL-SUBJECT-MANUEL-VERIFIED",
        governed_session_id="GOVERNED-SESSION-HBCE-IPR-RUNTIME-API-V1",
        event_trace_id="EVT-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
        technical_proof_receipt_id="OPC-HBCE-IPR-RUNTIME-API-V1-TECHNICAL-PROOF",
        audit_record_id="AUDIT-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
        model_usage_record_id="USAGE-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
    )
    sample_layer_valid = validate_operational_identity_proof_layer(sample_layer)

    blocked_layer = build_operational_identity_proof_layer(
        operational_subject_id="IPR-OPERATIONAL-SUBJECT-MANUEL-VERIFIED",
        governed_session_id="",
        event_trace_id="EVT-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
        technical_proof_receipt_id="OPC-HBCE-IPR-RUNTIME-API-V1-TECHNICAL-PROOF",
        audit_record_id="AUDIT-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
        model_usage_record_id="USAGE-HBCE-IPR-RUNTIME-API-V1-BOUNDARY",
    )
    blocked_layer_valid = not validate_operational_identity_proof_layer(blocked_layer)

    cases = [
        _case(
            "TASK_2_SCOPE_LOCK_REMAINS_VALID",
            source_valid and source_report.get("scope_lock_status") == "LOCKED" and source_report.get("scope_lock_passed") is True,
            "Task 2 scope lock remains LOCKED",
            {"scope_lock_status": source_report.get("scope_lock_status"), "scope_lock_passed": source_report.get("scope_lock_passed")},
        ),
        _case(
            "TASK_2_TO_TASK_3_TRANSITION_CONFIRMED",
            SOURCE_NEXT_STAGE == TASK_ID and source_report.get("next_stage") == TASK_ID,
            TASK_ID,
            {"source_constant_next_stage": SOURCE_NEXT_STAGE, "source_report_next_stage": source_report.get("next_stage")},
        ),
        _case(
            "TASK_2_DOCUMENT_BOUNDARY_MARKERS_PRESENT",
            _doc_contains(SOURCE_DOC_PATH, "MILESTONE_32_TASK_2_LEGAL_CERTIFICATION=false")
            and _doc_contains(SOURCE_DOC_PATH, "MILESTONE_32_TASK_2_OPC_TECHNICAL_PROOF_RECEIPT_ONLY=true")
            and _doc_contains(SOURCE_DOC_PATH, "MILESTONE_32_TASK_2_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false"),
            "Task 2 doc has legal and identity boundary markers",
            str(SOURCE_DOC_PATH),
        ),
        _case(
            "IMPLEMENTATION_MODE_MATCHES_SELECTED_OBJECTIVE",
            BOUNDARY_MODE_ID == SELECTED_OBJECTIVE_ID,
            SELECTED_OBJECTIVE_ID,
            BOUNDARY_MODE_ID,
        ),
        _case(
            "SAMPLE_PROOF_LAYER_VALID",
            sample_layer_valid,
            "sample proof layer validates",
            sample_layer["proof_layer_id"],
        ),
        _case(
            "MISSING_GOVERNED_SESSION_FAILS_CLOSED",
            blocked_layer_valid and blocked_layer["proof_layer_status"] == "BLOCKED",
            "missing governed session blocks layer",
            {"status": blocked_layer["proof_layer_status"], "missing": blocked_layer["missing_required_links"]},
        ),
        _case(
            "OPC_REMAINS_TECHNICAL_PROOF_RECEIPT_ONLY",
            sample_layer["opc_technical_proof_receipt_only"] is True and sample_layer["legal_certification"] is False,
            {"opcTechnicalProofReceiptOnly": True, "legalCertification": False},
            {"opcTechnicalProofReceiptOnly": sample_layer["opc_technical_proof_receipt_only"], "legalCertification": sample_layer["legal_certification"]},
        ),
        _case(
            "IPR_CARD_REMAINS_INTERNAL_NOT_OFFICIAL_PUBLIC_ID",
            sample_layer["ipr_card_internal_operational_identity_certificate"] is True
            and sample_layer["ipr_card_official_public_identity_document"] is False,
            {"internalOperationalIdentityCertificate": True, "officialPublicIdentityDocument": False},
            {
                "internalOperationalIdentityCertificate": sample_layer["ipr_card_internal_operational_identity_certificate"],
                "officialPublicIdentityDocument": sample_layer["ipr_card_official_public_identity_document"],
            },
        ),
        _case(
            "REQUIRED_PROOF_LINK_KEYS_COMPLETE",
            set(REQUIRED_LINK_KEYS).issubset(sample_layer["proof_links"].keys()),
            list(REQUIRED_LINK_KEYS),
            sorted(sample_layer["proof_links"].keys()),
        ),
        _case(
            "TASK_BUDGET_REMAINS_WITHIN_GOVERNED_LIMIT",
            TASK_BUDGET_MAX == 8 and SOURCE_CURRENT_TASK_NUMBER == 2 and CURRENT_TASK_NUMBER == 3,
            {"task_budget_max": 8, "source_current_task_number": 2, "current_task_number": 3},
            {"task_budget_max": TASK_BUDGET_MAX, "source_current_task_number": SOURCE_CURRENT_TASK_NUMBER, "current_task_number": CURRENT_TASK_NUMBER},
        ),
        _case(
            "NEXT_STAGE_VALIDATION_READY",
            NEXT_STAGE == "MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_V1",
            "MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_V1",
            NEXT_STAGE,
        ),
    ]

    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    implementation_passed = pass_count == REQUIRED_PASS_COUNT and fail_count == REQUIRED_FAIL_COUNT
    implementation_status = IMPLEMENTATION_STATUS if implementation_passed else "INVALID"

    implementation_id = "MILESTONE-32-HBCE-IPR-RUNTIME-API-BOUNDARY-" + _stable_hash(
        {
            "task_id": TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "task_3_signature": task_3_signature(),
            "sample_proof_layer_id": sample_layer["proof_layer_id"],
            "implementation_status": implementation_status,
        }
    )

    implementation_signature = _stable_hash(
        {
            "implementation_id": implementation_id,
            "task_id": TASK_ID,
            "source_scope_lock_signature": source_report.get("scope_lock_signature"),
            "task_3_signature": task_3_signature(),
            "implementation_status": implementation_status,
            "implementation_passed": implementation_passed,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        "task_id": TASK_ID,
        "source_scope_task_id": SOURCE_SCOPE_TASK_ID,
        "source_task_2_signature": task_2_signature(),
        "source_scope_lock_id": SCOPE_LOCK_ID,
        "source_scope_lock_status": source_report.get("scope_lock_status"),
        "source_scope_lock_passed": source_report.get("scope_lock_passed"),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "task_3_signature": task_3_signature(),
        "implementation_id": implementation_id,
        "implementation_signature": implementation_signature,
        "implementation_status": implementation_status,
        "implementation_case_count": len(cases),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "implementation_passed": implementation_passed,
        "sample_proof_layer": sample_layer,
        "blocked_layer": blocked_layer,
        "required_link_keys": list(REQUIRED_LINK_KEYS),
        "opc_technical_proof_receipt_only": OPC_TECHNICAL_PROOF_RECEIPT_ONLY,
        "legal_certification": LEGAL_CERTIFICATION,
        "ipr_card_internal_operational_identity_certificate": IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE,
        "ipr_card_official_public_identity_document": IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT,
        "explicit_legal_boundary_required": EXPLICIT_LEGAL_BOUNDARY_REQUIRED,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "source_generated_artifact_count": SOURCE_GENERATED_ARTIFACT_COUNT,
        "implementation_cases": cases,
        "next_stage": NEXT_STAGE,
    }


def validate_milestone_32_boundary_implementation_report(report: dict[str, Any]) -> bool:
    required = {
        "task_id": TASK_ID,
        "source_scope_task_id": SOURCE_SCOPE_TASK_ID,
        "source_task_2_signature": task_2_signature(),
        "source_scope_lock_status": "LOCKED",
        "source_scope_lock_passed": True,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "task_3_signature": task_3_signature(),
        "implementation_status": IMPLEMENTATION_STATUS,
        "implementation_case_count": IMPLEMENTATION_CASE_COUNT,
        "pass_count": REQUIRED_PASS_COUNT,
        "fail_count": REQUIRED_FAIL_COUNT,
        "implementation_passed": True,
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

    if not validate_operational_identity_proof_layer(report.get("sample_proof_layer", {})):
        return False

    if validate_operational_identity_proof_layer(report.get("blocked_layer", {})):
        return False

    cases = report.get("implementation_cases")
    if not isinstance(cases, list) or len(cases) != IMPLEMENTATION_CASE_COUNT:
        return False

    return all(case.get("passed") is True and case.get("failure_reason") == "NONE" for case in cases)


def _report_markdown(report: dict[str, Any]) -> str:
    case_lines = "\n".join(
        f"- {case['case_id']}: {'PASS' if case['passed'] else 'FAIL'}"
        for case in report["implementation_cases"]
    )
    return f"""# Milestone 32 Task 3 - HBCE IPR Runtime API v1 Boundary Implementation v1

MILESTONE_32_TASK_3_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_READY=true

MILESTONE_32_TASK_3_TASK_ID={report['task_id']}
MILESTONE_32_TASK_3_SOURCE_SCOPE_TASK_ID={report['source_scope_task_id']}
MILESTONE_32_TASK_3_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_32_TASK_3_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_32_TASK_3_IMPLEMENTATION_REVISION={report['implementation_revision']}
MILESTONE_32_TASK_3_BOUNDARY_MODE_ID={report['boundary_mode_id']}

MILESTONE_32_TASK_3_IMPLEMENTATION_ID={report['implementation_id']}
MILESTONE_32_TASK_3_IMPLEMENTATION_SIGNATURE={report['implementation_signature']}
MILESTONE_32_TASK_3_IMPLEMENTATION_STATUS={report['implementation_status']}
MILESTONE_32_TASK_3_IMPLEMENTATION_CASE_COUNT={report['implementation_case_count']}
MILESTONE_32_TASK_3_PASS_COUNT={report['pass_count']}
MILESTONE_32_TASK_3_FAIL_COUNT={report['fail_count']}
MILESTONE_32_TASK_3_IMPLEMENTATION_PASSED={str(report['implementation_passed']).lower()}

MILESTONE_32_TASK_3_OPC_TECHNICAL_PROOF_RECEIPT_ONLY={str(report['opc_technical_proof_receipt_only']).lower()}
MILESTONE_32_TASK_3_LEGAL_CERTIFICATION={str(report['legal_certification']).lower()}
MILESTONE_32_TASK_3_IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE={str(report['ipr_card_internal_operational_identity_certificate']).lower()}
MILESTONE_32_TASK_3_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT={str(report['ipr_card_official_public_identity_document']).lower()}

MILESTONE_32_TASK_3_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_32_TASK_3_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_32_TASK_3_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}

MILESTONE_32_TASK_3_NEXT_STAGE={report['next_stage']}

## Implementation Cases

{case_lines}
"""


def write_task_3_artifacts(base_dir: Path | str = ARTIFACT_DIR) -> dict[str, Any]:
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)

    report = run_milestone_32_boundary_implementation()
    if not validate_milestone_32_boundary_implementation_report(report):
        raise ValueError("Milestone 32 Task 3 boundary implementation report is invalid")

    report_path = base / "task-3-boundary-implementation-report.json"
    markdown_path = base / "task-3-boundary-implementation-report.md"
    cases_path = base / "task-3-boundary-implementation-cases.json"
    manifest_path = base / "task-3-manifest.json"
    index_path = base / "task-3-index.txt"

    cases_payload = {
        "task_id": TASK_ID,
        "implementation_id": report["implementation_id"],
        "implementation_status": report["implementation_status"],
        "implementation_case_count": report["implementation_case_count"],
        "implementation_cases": report["implementation_cases"],
    }

    manifest = {
        "task_id": TASK_ID,
        "source_scope_task_id": SOURCE_SCOPE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "boundary_mode_id": BOUNDARY_MODE_ID,
        "task_3_signature": task_3_signature(),
        "implementation_id": report["implementation_id"],
        "implementation_signature": report["implementation_signature"],
        "implementation_status": report["implementation_status"],
        "implementation_passed": report["implementation_passed"],
        "implementation_case_count": report["implementation_case_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    index = "\n".join(
        [
            "MILESTONE_32_TASK_3_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_READY=true",
            f"TASK_ID={TASK_ID}",
            f"SOURCE_SCOPE_TASK_ID={SOURCE_SCOPE_TASK_ID}",
            f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
            f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
            f"IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}",
            f"BOUNDARY_MODE_ID={BOUNDARY_MODE_ID}",
            f"TASK_3_SIGNATURE={task_3_signature()}",
            f"IMPLEMENTATION_ID={report['implementation_id']}",
            f"IMPLEMENTATION_SIGNATURE={report['implementation_signature']}",
            f"IMPLEMENTATION_STATUS={report['implementation_status']}",
            f"IMPLEMENTATION_CASE_COUNT={report['implementation_case_count']}",
            f"PASS_COUNT={report['pass_count']}",
            f"FAIL_COUNT={report['fail_count']}",
            f"IMPLEMENTATION_PASSED={str(report['implementation_passed']).lower()}",
            f"OPC_TECHNICAL_PROOF_RECEIPT_ONLY={str(OPC_TECHNICAL_PROOF_RECEIPT_ONLY).lower()}",
            f"LEGAL_CERTIFICATION={str(LEGAL_CERTIFICATION).lower()}",
            f"IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE={str(IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE).lower()}",
            f"IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT={str(IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT).lower()}",
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
    artifacts = write_task_3_artifacts()
    report = artifacts["report"]

    print("MILESTONE_32_TASK_3_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_READY=true")
    print(f"MILESTONE_32_TASK_3_TASK_ID={TASK_ID}")
    print(f"MILESTONE_32_TASK_3_SOURCE_SCOPE_TASK_ID={SOURCE_SCOPE_TASK_ID}")
    print(f"MILESTONE_32_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}")
    print(f"MILESTONE_32_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}")
    print(f"MILESTONE_32_TASK_3_IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}")
    print(f"MILESTONE_32_TASK_3_BOUNDARY_MODE_ID={BOUNDARY_MODE_ID}")
    print(f"MILESTONE_32_TASK_3_TASK_3_SIGNATURE={task_3_signature()}")
    print(f"MILESTONE_32_TASK_3_IMPLEMENTATION_ID={report['implementation_id']}")
    print(f"MILESTONE_32_TASK_3_IMPLEMENTATION_SIGNATURE={report['implementation_signature']}")
    print(f"MILESTONE_32_TASK_3_IMPLEMENTATION_STATUS={report['implementation_status']}")
    print(f"MILESTONE_32_TASK_3_IMPLEMENTATION_CASE_COUNT={report['implementation_case_count']}")
    print(f"MILESTONE_32_TASK_3_PASS_COUNT={report['pass_count']}")
    print(f"MILESTONE_32_TASK_3_FAIL_COUNT={report['fail_count']}")
    print(f"MILESTONE_32_TASK_3_IMPLEMENTATION_PASSED={str(report['implementation_passed']).lower()}")
    print(f"MILESTONE_32_TASK_3_OPC_TECHNICAL_PROOF_RECEIPT_ONLY={str(OPC_TECHNICAL_PROOF_RECEIPT_ONLY).lower()}")
    print(f"MILESTONE_32_TASK_3_LEGAL_CERTIFICATION={str(LEGAL_CERTIFICATION).lower()}")
    print(f"MILESTONE_32_TASK_3_IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE={str(IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE).lower()}")
    print(f"MILESTONE_32_TASK_3_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT={str(IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT).lower()}")
    print(f"MILESTONE_32_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}")
    print(f"MILESTONE_32_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}")
    print(f"MILESTONE_32_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}")
    print(f"MILESTONE_32_TASK_3_NEXT_STAGE={NEXT_STAGE}")


if __name__ == "__main__":
    main()
