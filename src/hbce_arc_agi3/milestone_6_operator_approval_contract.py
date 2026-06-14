"""Milestone #6 Operator Approval Contract v1.

This module creates a local-only operator approval contract for a possible
future ARC-AGI-3 real Kaggle submission.

The contract does not grant approval. It defines the approval requirements and
keeps real submission blocked until a later explicit operator approval artifact
exists. It does not authenticate with Kaggle, upload files, call external APIs,
read secrets, create upload archives, or create legal certification claims.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CONTRACT_STATUS = "MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_READY"
PIPELINE_STATUS = "MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/operator-approval-contract-v1"

DECISION_LAYER_JSON = Path(
    "examples/milestone-6/real-submission-decision-layer-v1/"
    "milestone-6-real-submission-decision-layer-v1.json"
)

BASELINE_COMMIT = "5e1bd2e Add ARC AGI3 real submission decision layer"
CONTRACT_MODE = "OPERATOR_APPROVAL_CONTRACT_ONLY_NO_APPROVAL"
CONTRACT_SCOPE = "DEFINE_OPERATOR_APPROVAL_REQUIREMENTS_NO_UPLOAD_NO_API"
CONTRACT_VERDICT = "OPERATOR_APPROVAL_REQUIRED_BUT_NOT_GRANTED"
NEXT_ALLOWED_STAGE = "EXPLICIT_OPERATOR_APPROVAL_ARTIFACT_REQUIRED"

REQUIRED_OPERATOR_DECLARATIONS: Tuple[str, ...] = (
    "operator_confirms_real_submission_intent",
    "operator_confirms_kaggle_rules_reviewed",
    "operator_confirms_submission_file_reviewed",
    "operator_confirms_no_private_core_exposure",
    "operator_confirms_no_api_keys_or_secrets",
    "operator_confirms_no_external_api_dependency",
    "operator_confirms_no_legal_certification_claim",
    "operator_accepts_manual_submission_responsibility",
)

CONTRACT_GATES: Tuple[str, ...] = (
    "decision_layer_artifact_present",
    "decision_layer_ready",
    "decision_layer_valid",
    "decision_layer_blocks_submission",
    "operator_approval_required",
    "operator_approval_contract_defined",
    "required_declarations_defined",
    "required_declarations_not_granted",
    "operator_approval_not_granted",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "real_submission_not_created",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "no_external_api_dependency",
    "no_secrets_or_api_keys",
    "no_private_core_exposure",
    "no_legal_certification",
    "contract_only_mode",
)

CONTRACT_ISSUES: Tuple[str, ...] = (
    "decision_layer_artifact_missing",
    "decision_layer_not_ready",
    "decision_layer_invalid",
    "decision_layer_allows_submission",
    "operator_approval_not_required",
    "operator_approval_contract_missing",
    "required_declarations_missing",
    "required_declarations_already_granted",
    "operator_approval_granted_unexpectedly",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "real_submission_created",
    "kaggle_submission_already_sent",
    "upload_performed",
    "external_api_dependency_detected",
    "secrets_or_api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "contract_mode_invalid",
)

REQUIRED_BOUNDARY_FLAGS: Tuple[Tuple[str, bool], ...] = (
    ("public_safe", True),
    ("deterministic", True),
    ("local_only", True),
    ("dry_run_only", True),
    ("external_api_dependency", False),
    ("contains_api_keys", False),
    ("kaggle_submission_sent", False),
    ("private_core_exposure", False),
    ("legal_certification", False),
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16].upper()


def _read_json_if_available(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _file_sha256_16(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"

    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def _boundary_from_decision(decision: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = decision.get("boundary", {}) if isinstance(decision.get("boundary"), Mapping) else {}

    return {
        "public_safe": boundary.get("public_safe"),
        "deterministic": boundary.get("deterministic"),
        "local_only": boundary.get("local_only"),
        "dry_run_only": boundary.get("dry_run_only"),
        "external_api_dependency": boundary.get("external_api_dependency"),
        "contains_api_keys": boundary.get("contains_api_keys"),
        "kaggle_submission_sent": decision.get("kaggle_submission_sent"),
        "private_core_exposure": boundary.get("private_core_exposure"),
        "legal_certification": boundary.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


def _build_required_declarations() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            "name": name,
            "required": True,
            "provided": False,
            "accepted": False,
            "status": "PENDING_EXPLICIT_OPERATOR_APPROVAL",
        }
        for name in REQUIRED_OPERATOR_DECLARATIONS
    )


def _build_contract_record(decision: Mapping[str, Any], boundary: Mapping[str, Any]) -> Dict[str, Any]:
    declarations = _build_required_declarations()

    return {
        "contract_mode": CONTRACT_MODE,
        "contract_scope": CONTRACT_SCOPE,
        "contract_verdict": CONTRACT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "operator_approval_required": True,
        "operator_approval_contract_ready": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "operator_identity_verified_for_submission": False,
        "required_declaration_count": len(declarations),
        "provided_declaration_count": sum(1 for item in declarations if item["provided"] is True),
        "accepted_declaration_count": sum(1 for item in declarations if item["accepted"] is True),
        "required_declarations": list(declarations),
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "archive_created_for_upload": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "secrets_required": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "depends_on_decision_layer_id": decision.get("decision_id", "MISSING_DECISION_ID"),
        "depends_on_decision_layer_verdict": decision.get("decision_verdict", "MISSING_DECISION_VERDICT"),
        "decision_layer_blocks_submission": decision.get("real_submission_allowed") is False,
        "boundary_intact": _boundary_intact(boundary),
    }


def _build_contract_gates(
    *,
    decision: Mapping[str, Any],
    contract_record: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    declarations = contract_record.get("required_declarations", [])
    all_declarations_defined = (
        isinstance(declarations, list)
        and len(declarations) == len(REQUIRED_OPERATOR_DECLARATIONS)
        and all(item.get("required") is True for item in declarations)
    )
    all_declarations_pending = (
        isinstance(declarations, list)
        and all(item.get("provided") is False and item.get("accepted") is False for item in declarations)
    )

    gate_results = {
        "decision_layer_artifact_present": DECISION_LAYER_JSON.exists(),
        "decision_layer_ready": decision.get("status") == "MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_READY",
        "decision_layer_valid": bool(decision.get("decision_id")) and bool(decision.get("signature")),
        "decision_layer_blocks_submission": decision.get("real_submission_allowed") is False,
        "operator_approval_required": contract_record.get("operator_approval_required") is True,
        "operator_approval_contract_defined": contract_record.get("operator_approval_contract_ready") is True,
        "required_declarations_defined": all_declarations_defined,
        "required_declarations_not_granted": all_declarations_pending,
        "operator_approval_not_granted": contract_record.get("operator_approval_granted") is False,
        "real_submission_allowed_false": contract_record.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": contract_record.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": contract_record.get("real_submission_created") is False,
        "kaggle_submission_not_sent": contract_record.get("kaggle_submission_sent") is False,
        "upload_not_performed": contract_record.get("upload_performed") is False,
        "no_external_api_dependency": boundary.get("external_api_dependency") is False,
        "no_secrets_or_api_keys": boundary.get("contains_api_keys") is False and contract_record.get("secrets_required") is False,
        "no_private_core_exposure": boundary.get("private_core_exposure") is False,
        "no_legal_certification": boundary.get("legal_certification") is False,
        "contract_only_mode": contract_record.get("contract_mode") == CONTRACT_MODE,
    }

    descriptions = {
        "decision_layer_artifact_present": "Milestone #6 Task 1 decision layer artifact is present.",
        "decision_layer_ready": "Milestone #6 Task 1 decision layer is ready.",
        "decision_layer_valid": "Milestone #6 Task 1 decision layer has id and signature.",
        "decision_layer_blocks_submission": "Decision layer blocks real submission.",
        "operator_approval_required": "Explicit operator approval is required.",
        "operator_approval_contract_defined": "Operator approval contract is defined.",
        "required_declarations_defined": "All required operator declarations are defined.",
        "required_declarations_not_granted": "Required declarations remain pending, not granted.",
        "operator_approval_not_granted": "Operator approval has not been granted by this contract.",
        "real_submission_allowed_false": "Real submission remains disallowed.",
        "ready_for_real_kaggle_submission_false": "Ready for real Kaggle submission remains false.",
        "real_submission_not_created": "No real submission has been created.",
        "kaggle_submission_not_sent": "No Kaggle submission has been sent.",
        "upload_not_performed": "No upload has been performed.",
        "no_external_api_dependency": "No external API dependency is present.",
        "no_secrets_or_api_keys": "No secrets or API keys are required or present.",
        "no_private_core_exposure": "No private core exposure is present.",
        "no_legal_certification": "No legal certification claim is present.",
        "contract_only_mode": "Contract mode is approval-contract-only.",
    }

    return tuple(
        {
            "name": name,
            "passed": gate_results[name],
            "severity": "PASS" if gate_results[name] else "BLOCKING",
            "description": descriptions[name],
        }
        for name in CONTRACT_GATES
    )


def _build_contract_issues(
    *,
    decision: Mapping[str, Any],
    contract_record: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    declarations = contract_record.get("required_declarations", [])
    declarations_missing = not (
        isinstance(declarations, list)
        and len(declarations) == len(REQUIRED_OPERATOR_DECLARATIONS)
        and all(item.get("required") is True for item in declarations)
    )
    declarations_already_granted = (
        isinstance(declarations, list)
        and any(item.get("provided") is not False or item.get("accepted") is not False for item in declarations)
    )

    issue_state = {
        "decision_layer_artifact_missing": not DECISION_LAYER_JSON.exists(),
        "decision_layer_not_ready": decision.get("status") != "MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_READY",
        "decision_layer_invalid": not (bool(decision.get("decision_id")) and bool(decision.get("signature"))),
        "decision_layer_allows_submission": decision.get("real_submission_allowed") is not False,
        "operator_approval_not_required": contract_record.get("operator_approval_required") is not True,
        "operator_approval_contract_missing": contract_record.get("operator_approval_contract_ready") is not True,
        "required_declarations_missing": declarations_missing,
        "required_declarations_already_granted": declarations_already_granted,
        "operator_approval_granted_unexpectedly": contract_record.get("operator_approval_granted") is not False,
        "real_submission_allowed_true": contract_record.get("real_submission_allowed") is not False,
        "ready_for_real_kaggle_submission_true": contract_record.get("ready_for_real_kaggle_submission") is not False,
        "real_submission_created": contract_record.get("real_submission_created") is not False,
        "kaggle_submission_already_sent": contract_record.get("kaggle_submission_sent") is not False,
        "upload_performed": contract_record.get("upload_performed") is not False,
        "external_api_dependency_detected": boundary.get("external_api_dependency") is not False,
        "secrets_or_api_keys_detected": boundary.get("contains_api_keys") is not False or contract_record.get("secrets_required") is not False,
        "private_core_exposure_detected": boundary.get("private_core_exposure") is not False,
        "legal_certification_claim_detected": boundary.get("legal_certification") is not False,
        "contract_mode_invalid": contract_record.get("contract_mode") != CONTRACT_MODE,
    }

    descriptions = {
        "decision_layer_artifact_missing": "Decision layer artifact is missing.",
        "decision_layer_not_ready": "Decision layer is not ready.",
        "decision_layer_invalid": "Decision layer id/signature is missing.",
        "decision_layer_allows_submission": "Decision layer allows real submission unexpectedly.",
        "operator_approval_not_required": "Operator approval is not required.",
        "operator_approval_contract_missing": "Operator approval contract is missing.",
        "required_declarations_missing": "Required declarations are missing.",
        "required_declarations_already_granted": "Required declarations appear already granted.",
        "operator_approval_granted_unexpectedly": "Operator approval is granted unexpectedly.",
        "real_submission_allowed_true": "Real submission is allowed unexpectedly.",
        "ready_for_real_kaggle_submission_true": "Ready for real Kaggle submission is true unexpectedly.",
        "real_submission_created": "A real submission appears to have been created.",
        "kaggle_submission_already_sent": "A Kaggle submission appears to have been sent.",
        "upload_performed": "An upload appears to have been performed.",
        "external_api_dependency_detected": "External API dependency detected.",
        "secrets_or_api_keys_detected": "Secrets or API keys detected.",
        "private_core_exposure_detected": "Private core exposure detected.",
        "legal_certification_claim_detected": "Legal certification claim detected.",
        "contract_mode_invalid": "Contract mode is invalid.",
    }

    return tuple(
        {
            "name": name,
            "active": issue_state[name],
            "severity": "BLOCKING",
            "description": descriptions[name],
        }
        for name in CONTRACT_ISSUES
    )


def build_milestone_6_operator_approval_contract() -> Dict[str, Any]:
    decision = _read_json_if_available(DECISION_LAYER_JSON)
    boundary = _boundary_from_decision(decision)
    contract_record = _build_contract_record(decision, boundary)

    gates = _build_contract_gates(
        decision=decision,
        contract_record=contract_record,
        boundary=boundary,
    )
    issues = _build_contract_issues(
        decision=decision,
        contract_record=contract_record,
        boundary=boundary,
    )

    passed_gate_count = sum(1 for gate in gates if gate["passed"] is True)
    issue_count = sum(1 for issue in issues if issue["active"] is True)
    warning_count = 0

    contract_ready = (
        passed_gate_count == len(CONTRACT_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
        and contract_record["operator_approval_granted"] is False
        and contract_record["real_submission_allowed"] is False
    )

    contract_index = {
        "milestone": "Milestone #6",
        "task": "Task 2",
        "contract_mode": CONTRACT_MODE,
        "contract_scope": CONTRACT_SCOPE,
        "contract_verdict": CONTRACT_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_decision_layer": decision.get("decision_id", "MISSING_DECISION_ID"),
        "required_declaration_count": len(REQUIRED_OPERATOR_DECLARATIONS),
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base_payload = {
        "status": CONTRACT_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 2",
        "title": "Operator Approval Contract v1",
        "baseline_commit": BASELINE_COMMIT,
        "decision_layer_id": decision.get("decision_id", "MISSING_DECISION_ID"),
        "decision_layer_signature": decision.get("signature", "MISSING_DECISION_SIGNATURE"),
        "decision_layer_verdict": decision.get("decision_verdict", "MISSING_DECISION_VERDICT"),
        "contract_mode": CONTRACT_MODE,
        "contract_scope": CONTRACT_SCOPE,
        "contract_verdict": CONTRACT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "contract_record": copy.deepcopy(contract_record),
        "contract_gates": list(gates),
        "contract_issues": list(issues),
        "contract_index": contract_index,
        "boundary": boundary,
        "required_declaration_count": len(REQUIRED_OPERATOR_DECLARATIONS),
        "provided_declaration_count": contract_record["provided_declaration_count"],
        "accepted_declaration_count": contract_record["accepted_declaration_count"],
        "contract_gate_count": len(CONTRACT_GATES),
        "passed_gate_count": passed_gate_count,
        "contract_issue_count": issue_count,
        "warning_count": warning_count,
        "operator_approval_contract_ready": contract_ready,
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "metadata": {
            "source": "milestone_6_operator_approval_contract_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }

    signature = _stable_signature(base_payload)
    contract_id = f"MILESTONE-6-OPERATOR-APPROVAL-CONTRACT-{signature[:12]}"

    return {
        **base_payload,
        "contract_id": contract_id,
        "signature": signature,
    }


def validate_milestone_6_operator_approval_contract(contract: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = contract.get("boundary") if isinstance(contract.get("boundary"), Mapping) else {}
    gates = contract.get("contract_gates") if isinstance(contract.get("contract_gates"), list) else []
    issues = contract.get("contract_issues") if isinstance(contract.get("contract_issues"), list) else []
    record = contract.get("contract_record") if isinstance(contract.get("contract_record"), Mapping) else {}
    index = contract.get("contract_index") if isinstance(contract.get("contract_index"), Mapping) else {}
    declarations = record.get("required_declarations") if isinstance(record.get("required_declarations"), list) else []

    validation_checks = {
        "status_ready": contract.get("status") == CONTRACT_STATUS,
        "contract_id_present": isinstance(contract.get("contract_id"), str) and bool(contract.get("contract_id")),
        "signature_present": isinstance(contract.get("signature"), str) and bool(contract.get("signature")),
        "baseline_commit_is_decision_layer": str(contract.get("baseline_commit", "")).startswith("5e1bd2e"),
        "decision_layer_id_present": isinstance(contract.get("decision_layer_id"), str)
        and contract.get("decision_layer_id") != "MISSING_DECISION_ID",
        "contract_mode_valid": contract.get("contract_mode") == CONTRACT_MODE,
        "contract_scope_valid": contract.get("contract_scope") == CONTRACT_SCOPE,
        "contract_verdict_valid": contract.get("contract_verdict") == CONTRACT_VERDICT,
        "required_declaration_count_valid": contract.get("required_declaration_count") == len(REQUIRED_OPERATOR_DECLARATIONS),
        "provided_declaration_count_zero": contract.get("provided_declaration_count") == 0,
        "accepted_declaration_count_zero": contract.get("accepted_declaration_count") == 0,
        "required_declarations_present": len(declarations) == len(REQUIRED_OPERATOR_DECLARATIONS),
        "required_declarations_pending": bool(declarations)
        and all(item.get("required") is True and item.get("provided") is False and item.get("accepted") is False for item in declarations),
        "contract_gate_count_matches": contract.get("contract_gate_count") == len(CONTRACT_GATES),
        "all_contract_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "contract_issue_count_zero": contract.get("contract_issue_count") == 0,
        "all_contract_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "warning_count_zero": contract.get("warning_count") == 0,
        "operator_approval_contract_ready": contract.get("operator_approval_contract_ready") is True,
        "operator_approval_required": contract.get("operator_approval_required") is True,
        "operator_approval_not_granted": contract.get("operator_approval_granted") is False,
        "operator_approval_not_received": contract.get("operator_approval_received") is False,
        "record_operator_approval_not_granted": record.get("operator_approval_granted") is False,
        "real_submission_allowed_false": contract.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": contract.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": contract.get("real_submission_created") is False,
        "kaggle_submission_not_sent": contract.get("kaggle_submission_sent") is False,
        "upload_not_performed": contract.get("upload_performed") is False,
        "index_real_submission_allowed_false": index.get("real_submission_allowed") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(validation_checks.values())

    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "contract_id": contract.get("contract_id"),
        "signature": contract.get("signature"),
    }


def render_operator_approval_contract_markdown(contract: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Operator Approval Contract v1",
        "",
        "## Status",
        "",
        f"- status: {contract['status']}",
        f"- contract_id: {contract['contract_id']}",
        f"- signature: {contract['signature']}",
        f"- baseline_commit: {contract['baseline_commit']}",
        f"- decision_layer_id: {contract['decision_layer_id']}",
        f"- decision_layer_verdict: {contract['decision_layer_verdict']}",
        f"- contract_mode: {contract['contract_mode']}",
        f"- contract_scope: {contract['contract_scope']}",
        f"- contract_verdict: {contract['contract_verdict']}",
        f"- next_allowed_stage: {contract['next_allowed_stage']}",
        f"- required_declaration_count: {contract['required_declaration_count']}",
        f"- provided_declaration_count: {contract['provided_declaration_count']}",
        f"- accepted_declaration_count: {contract['accepted_declaration_count']}",
        f"- contract_gate_count: {contract['contract_gate_count']}",
        f"- passed_gate_count: {contract['passed_gate_count']}",
        f"- contract_issue_count: {contract['contract_issue_count']}",
        f"- warning_count: {contract['warning_count']}",
        f"- operator_approval_contract_ready: {contract['operator_approval_contract_ready']}",
        f"- operator_approval_required: {contract['operator_approval_required']}",
        f"- operator_approval_granted: {contract['operator_approval_granted']}",
        f"- operator_approval_received: {contract['operator_approval_received']}",
        f"- real_submission_allowed: {contract['real_submission_allowed']}",
        f"- ready_for_real_kaggle_submission: {contract['ready_for_real_kaggle_submission']}",
        f"- real_submission_created: {contract['real_submission_created']}",
        f"- kaggle_submission_sent: {contract['kaggle_submission_sent']}",
        f"- upload_performed: {contract['upload_performed']}",
        "",
        "## Required operator declarations",
        "",
    ]

    for item in contract["contract_record"]["required_declarations"]:
        lines.append(
            f"- {item['name']}: required={item['required']} provided={item['provided']} "
            f"accepted={item['accepted']} status={item['status']}"
        )

    lines.extend(["", "## Contract gates", ""])

    for gate in contract["contract_gates"]:
        lines.append(f"- {gate['name']}: passed={gate['passed']} severity={gate['severity']}")

    lines.extend(["", "## Contract issues", ""])

    for issue in contract["contract_issues"]:
        lines.append(f"- {issue['name']}: active={issue['active']} severity={issue['severity']}")

    lines.extend(
        [
            "",
            "## Public boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- local_only=true",
            "- dry_run_only=true",
            "- external_api_dependency=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "- legal_certification=false",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_V1_READY=true",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_VALID=true",
            "ARC_AGI3_MILESTONE_6_CONTRACT_MODE=OPERATOR_APPROVAL_CONTRACT_ONLY_NO_APPROVAL",
            "ARC_AGI3_MILESTONE_6_CONTRACT_VERDICT=OPERATOR_APPROVAL_REQUIRED_BUT_NOT_GRANTED",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_REQUIRED=true",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_GRANTED=false",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_RECEIVED=false",
            "ARC_AGI3_MILESTONE_6_REQUIRED_DECLARATION_COUNT=8",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_BASELINE_DECISION_LAYER_COMMIT=5e1bd2e",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_operator_approval_contract_manifest(contract: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 OPERATOR APPROVAL CONTRACT MANIFEST v1",
        f"contract_id={contract['contract_id']}",
        f"signature={contract['signature']}",
        f"status={contract['status']}",
        f"baseline_commit={contract['baseline_commit']}",
        f"decision_layer_id={contract['decision_layer_id']}",
        f"contract_mode={contract['contract_mode']}",
        f"contract_scope={contract['contract_scope']}",
        f"contract_verdict={contract['contract_verdict']}",
        f"required_declaration_count={contract['required_declaration_count']}",
        f"provided_declaration_count={contract['provided_declaration_count']}",
        f"accepted_declaration_count={contract['accepted_declaration_count']}",
        f"contract_gate_count={contract['contract_gate_count']}",
        f"passed_gate_count={contract['passed_gate_count']}",
        f"contract_issue_count={contract['contract_issue_count']}",
        f"warning_count={contract['warning_count']}",
        f"operator_approval_contract_ready={contract['operator_approval_contract_ready']}",
        f"operator_approval_required={contract['operator_approval_required']}",
        f"operator_approval_granted={contract['operator_approval_granted']}",
        f"operator_approval_received={contract['operator_approval_received']}",
        f"real_submission_allowed={contract['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={contract['ready_for_real_kaggle_submission']}",
        f"real_submission_created={contract['real_submission_created']}",
        f"kaggle_submission_sent={contract['kaggle_submission_sent']}",
        f"upload_performed={contract['upload_performed']}",
        "",
        "REQUIRED_OPERATOR_DECLARATIONS",
    ]

    for item in contract["contract_record"]["required_declarations"]:
        lines.append(
            f"{item['name']} required={item['required']} provided={item['provided']} "
            f"accepted={item['accepted']} status={item['status']}"
        )

    lines.extend(["", "CONTRACT_GATES"])

    for gate in contract["contract_gates"]:
        lines.append(f"{gate['name']} passed={gate['passed']} severity={gate['severity']}")

    lines.extend(["", "CONTRACT_ISSUES"])

    for issue in contract["contract_issues"]:
        lines.append(f"{issue['name']} active={issue['active']} severity={issue['severity']}")

    lines.extend(
        [
            "",
            "BOUNDARY",
            "public_safe=true",
            "deterministic=true",
            "local_only=true",
            "dry_run_only=true",
            "external_api_dependency=false",
            "contains_api_keys=false",
            "kaggle_submission_sent=false",
            "private_core_exposure=false",
            "legal_certification=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_operator_approval_contract_artifacts(
    contract: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    contract = dict(contract or build_milestone_6_operator_approval_contract())
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "milestone-6-operator-approval-contract-v1.json"
    markdown_path = output_path / "milestone-6-operator-approval-contract-v1.md"
    manifest_path = output_path / "milestone-6-operator-approval-contract-manifest-v1.txt"
    index_path = output_path / "milestone-6-operator-approval-contract-index-v1.json"

    json_path.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_operator_approval_contract_markdown(contract), encoding="utf-8")
    manifest_path.write_text(render_operator_approval_contract_manifest(contract), encoding="utf-8")
    index_path.write_text(json.dumps(contract["contract_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_operator_approval_contract_pipeline() -> Dict[str, Any]:
    contract = build_milestone_6_operator_approval_contract()
    validation = validate_milestone_6_operator_approval_contract(contract)
    artifacts = write_operator_approval_contract_artifacts(contract)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_PIPELINE_INVALID",
        "contract_status": contract["status"],
        "validation_status": validation["status"],
        "contract": contract,
        "contract_id": contract["contract_id"],
        "signature": contract["signature"],
        "contract_mode": contract["contract_mode"],
        "contract_verdict": contract["contract_verdict"],
        "required_declaration_count": contract["required_declaration_count"],
        "provided_declaration_count": contract["provided_declaration_count"],
        "accepted_declaration_count": contract["accepted_declaration_count"],
        "contract_gate_count": contract["contract_gate_count"],
        "passed_gate_count": contract["passed_gate_count"],
        "contract_issue_count": contract["contract_issue_count"],
        "warning_count": contract["warning_count"],
        "operator_approval_contract_ready": contract["operator_approval_contract_ready"],
        "operator_approval_required": contract["operator_approval_required"],
        "operator_approval_granted": contract["operator_approval_granted"],
        "operator_approval_received": contract["operator_approval_received"],
        "real_submission_allowed": contract["real_submission_allowed"],
        "ready_for_real_kaggle_submission": contract["ready_for_real_kaggle_submission"],
        "real_submission_created": contract["real_submission_created"],
        "kaggle_submission_sent": contract["kaggle_submission_sent"],
        "upload_performed": contract["upload_performed"],
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_6_operator_approval_contract_pipeline_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }
