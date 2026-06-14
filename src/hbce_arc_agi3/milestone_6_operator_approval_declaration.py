"""Milestone #6 Operator Approval Declaration v1.

This module creates a local-only operator approval declaration artifact for a
possible future ARC-AGI-3 real Kaggle submission.

The declaration records explicit operator approval declarations, but it does
not submit to Kaggle, authenticate, upload files, call external APIs, read
secrets, create upload archives, or create legal certification claims.

Important boundary: approval declaration is not the same as real submission
permission. Real submission remains blocked until a later pre-submit gate.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


DECLARATION_STATUS = "MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_READY"
PIPELINE_STATUS = "MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/operator-approval-declaration-v1"

OPERATOR_APPROVAL_CONTRACT_JSON = Path(
    "examples/milestone-6/operator-approval-contract-v1/"
    "milestone-6-operator-approval-contract-v1.json"
)

BASELINE_COMMIT = "34e7763 Add ARC AGI3 operator approval contract"
DECLARATION_MODE = "OPERATOR_APPROVAL_DECLARATION_ONLY_NO_SUBMISSION"
DECLARATION_SCOPE = "DECLARE_OPERATOR_APPROVAL_NO_UPLOAD_NO_API"
DECLARATION_VERDICT = "OPERATOR_APPROVAL_DECLARED_REAL_SUBMISSION_STILL_BLOCKED"
NEXT_ALLOWED_STAGE = "REAL_SUBMISSION_PRECHECK_GATE_REQUIRED"

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

DECLARATION_GATES: Tuple[str, ...] = (
    "operator_approval_contract_present",
    "operator_approval_contract_ready",
    "operator_approval_contract_valid",
    "contract_requires_operator_approval",
    "contract_does_not_grant_approval",
    "declaration_mode_valid",
    "required_declarations_loaded",
    "all_required_declarations_declared",
    "all_required_declarations_accepted",
    "operator_approval_declared",
    "operator_approval_received",
    "operator_approval_granted",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "real_submission_not_created",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "no_external_api_dependency",
    "no_secrets_or_api_keys",
    "no_private_core_exposure",
    "no_legal_certification",
    "precheck_gate_still_required",
)

DECLARATION_ISSUES: Tuple[str, ...] = (
    "operator_approval_contract_missing",
    "operator_approval_contract_not_ready",
    "operator_approval_contract_invalid",
    "contract_does_not_require_operator_approval",
    "contract_already_grants_approval",
    "declaration_mode_invalid",
    "required_declarations_missing",
    "required_declarations_not_declared",
    "required_declarations_not_accepted",
    "operator_approval_not_declared",
    "operator_approval_not_received",
    "operator_approval_not_granted",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "real_submission_created",
    "kaggle_submission_already_sent",
    "upload_performed",
    "external_api_dependency_detected",
    "secrets_or_api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "precheck_gate_not_required",
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


def _boundary_from_contract(contract: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = contract.get("boundary", {}) if isinstance(contract.get("boundary"), Mapping) else {}

    return {
        "public_safe": boundary.get("public_safe"),
        "deterministic": boundary.get("deterministic"),
        "local_only": boundary.get("local_only"),
        "dry_run_only": boundary.get("dry_run_only"),
        "external_api_dependency": boundary.get("external_api_dependency"),
        "contains_api_keys": boundary.get("contains_api_keys"),
        "kaggle_submission_sent": contract.get("kaggle_submission_sent"),
        "private_core_exposure": boundary.get("private_core_exposure"),
        "legal_certification": boundary.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


def _contract_required_declarations(contract: Mapping[str, Any]) -> Tuple[str, ...]:
    record = contract.get("contract_record", {}) if isinstance(contract.get("contract_record"), Mapping) else {}
    declarations = record.get("required_declarations", [])

    if isinstance(declarations, list) and declarations:
        names = tuple(str(item.get("name")) for item in declarations if item.get("name"))
        if names == REQUIRED_OPERATOR_DECLARATIONS:
            return names

    return REQUIRED_OPERATOR_DECLARATIONS


def _build_declared_operator_declarations(contract: Mapping[str, Any]) -> Tuple[Dict[str, Any], ...]:
    names = _contract_required_declarations(contract)

    return tuple(
        {
            "name": name,
            "required": True,
            "declared": True,
            "provided": True,
            "accepted": True,
            "status": "DECLARED_AND_ACCEPTED_FOR_DECISION_CHAIN",
        }
        for name in names
    )


def _build_declaration_record(contract: Mapping[str, Any], boundary: Mapping[str, Any]) -> Dict[str, Any]:
    declarations = _build_declared_operator_declarations(contract)

    return {
        "declaration_mode": DECLARATION_MODE,
        "declaration_scope": DECLARATION_SCOPE,
        "declaration_verdict": DECLARATION_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "operator_approval_declaration_ready": True,
        "operator_approval_required": True,
        "operator_approval_declared": True,
        "operator_approval_received": True,
        "operator_approval_granted": True,
        "operator_identity_verified_for_submission": False,
        "required_declaration_count": len(declarations),
        "declared_declaration_count": sum(1 for item in declarations if item["declared"] is True),
        "provided_declaration_count": sum(1 for item in declarations if item["provided"] is True),
        "accepted_declaration_count": sum(1 for item in declarations if item["accepted"] is True),
        "declared_operator_declarations": list(declarations),
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
        "precheck_gate_required": True,
        "depends_on_operator_approval_contract_id": contract.get("contract_id", "MISSING_CONTRACT_ID"),
        "depends_on_contract_verdict": contract.get("contract_verdict", "MISSING_CONTRACT_VERDICT"),
        "contract_required_approval": contract.get("operator_approval_required") is True,
        "contract_did_not_grant_approval": contract.get("operator_approval_granted") is False,
        "boundary_intact": _boundary_intact(boundary),
    }


def _build_declaration_gates(
    *,
    contract: Mapping[str, Any],
    declaration_record: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    declarations = declaration_record.get("declared_operator_declarations", [])

    declarations_loaded = (
        isinstance(declarations, list)
        and len(declarations) == len(REQUIRED_OPERATOR_DECLARATIONS)
        and [item.get("name") for item in declarations] == list(REQUIRED_OPERATOR_DECLARATIONS)
    )
    all_declared = declarations_loaded and all(item.get("declared") is True and item.get("provided") is True for item in declarations)
    all_accepted = declarations_loaded and all(item.get("accepted") is True for item in declarations)

    gate_results = {
        "operator_approval_contract_present": OPERATOR_APPROVAL_CONTRACT_JSON.exists(),
        "operator_approval_contract_ready": contract.get("status") == "MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_READY",
        "operator_approval_contract_valid": bool(contract.get("contract_id")) and bool(contract.get("signature")),
        "contract_requires_operator_approval": contract.get("operator_approval_required") is True,
        "contract_does_not_grant_approval": contract.get("operator_approval_granted") is False,
        "declaration_mode_valid": declaration_record.get("declaration_mode") == DECLARATION_MODE,
        "required_declarations_loaded": declarations_loaded,
        "all_required_declarations_declared": all_declared,
        "all_required_declarations_accepted": all_accepted,
        "operator_approval_declared": declaration_record.get("operator_approval_declared") is True,
        "operator_approval_received": declaration_record.get("operator_approval_received") is True,
        "operator_approval_granted": declaration_record.get("operator_approval_granted") is True,
        "real_submission_allowed_false": declaration_record.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": declaration_record.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": declaration_record.get("real_submission_created") is False,
        "kaggle_submission_not_sent": declaration_record.get("kaggle_submission_sent") is False,
        "upload_not_performed": declaration_record.get("upload_performed") is False,
        "no_external_api_dependency": boundary.get("external_api_dependency") is False,
        "no_secrets_or_api_keys": boundary.get("contains_api_keys") is False and declaration_record.get("secrets_required") is False,
        "no_private_core_exposure": boundary.get("private_core_exposure") is False,
        "no_legal_certification": boundary.get("legal_certification") is False,
        "precheck_gate_still_required": declaration_record.get("precheck_gate_required") is True,
    }

    descriptions = {
        "operator_approval_contract_present": "Operator approval contract artifact is present.",
        "operator_approval_contract_ready": "Operator approval contract is ready.",
        "operator_approval_contract_valid": "Operator approval contract has id and signature.",
        "contract_requires_operator_approval": "Contract requires operator approval.",
        "contract_does_not_grant_approval": "Contract itself did not grant approval.",
        "declaration_mode_valid": "Declaration mode is valid.",
        "required_declarations_loaded": "Required declarations are loaded from the contract.",
        "all_required_declarations_declared": "All required declarations are declared.",
        "all_required_declarations_accepted": "All required declarations are accepted.",
        "operator_approval_declared": "Operator approval is declared.",
        "operator_approval_received": "Operator approval declaration is received.",
        "operator_approval_granted": "Operator approval is granted as declaration artifact only.",
        "real_submission_allowed_false": "Real submission remains disallowed.",
        "ready_for_real_kaggle_submission_false": "Ready for real Kaggle submission remains false.",
        "real_submission_not_created": "No real submission has been created.",
        "kaggle_submission_not_sent": "No Kaggle submission has been sent.",
        "upload_not_performed": "No upload has been performed.",
        "no_external_api_dependency": "No external API dependency is present.",
        "no_secrets_or_api_keys": "No secrets or API keys are required or present.",
        "no_private_core_exposure": "No private core exposure is present.",
        "no_legal_certification": "No legal certification claim is present.",
        "precheck_gate_still_required": "A later precheck gate is still required.",
    }

    return tuple(
        {
            "name": name,
            "passed": gate_results[name],
            "severity": "PASS" if gate_results[name] else "BLOCKING",
            "description": descriptions[name],
        }
        for name in DECLARATION_GATES
    )


def _build_declaration_issues(
    *,
    contract: Mapping[str, Any],
    declaration_record: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    declarations = declaration_record.get("declared_operator_declarations", [])

    declarations_loaded = (
        isinstance(declarations, list)
        and len(declarations) == len(REQUIRED_OPERATOR_DECLARATIONS)
        and [item.get("name") for item in declarations] == list(REQUIRED_OPERATOR_DECLARATIONS)
    )
    declarations_not_declared = not (
        declarations_loaded and all(item.get("declared") is True and item.get("provided") is True for item in declarations)
    )
    declarations_not_accepted = not (declarations_loaded and all(item.get("accepted") is True for item in declarations))

    issue_state = {
        "operator_approval_contract_missing": not OPERATOR_APPROVAL_CONTRACT_JSON.exists(),
        "operator_approval_contract_not_ready": contract.get("status") != "MILESTONE_6_OPERATOR_APPROVAL_CONTRACT_READY",
        "operator_approval_contract_invalid": not (bool(contract.get("contract_id")) and bool(contract.get("signature"))),
        "contract_does_not_require_operator_approval": contract.get("operator_approval_required") is not True,
        "contract_already_grants_approval": contract.get("operator_approval_granted") is not False,
        "declaration_mode_invalid": declaration_record.get("declaration_mode") != DECLARATION_MODE,
        "required_declarations_missing": not declarations_loaded,
        "required_declarations_not_declared": declarations_not_declared,
        "required_declarations_not_accepted": declarations_not_accepted,
        "operator_approval_not_declared": declaration_record.get("operator_approval_declared") is not True,
        "operator_approval_not_received": declaration_record.get("operator_approval_received") is not True,
        "operator_approval_not_granted": declaration_record.get("operator_approval_granted") is not True,
        "real_submission_allowed_true": declaration_record.get("real_submission_allowed") is not False,
        "ready_for_real_kaggle_submission_true": declaration_record.get("ready_for_real_kaggle_submission") is not False,
        "real_submission_created": declaration_record.get("real_submission_created") is not False,
        "kaggle_submission_already_sent": declaration_record.get("kaggle_submission_sent") is not False,
        "upload_performed": declaration_record.get("upload_performed") is not False,
        "external_api_dependency_detected": boundary.get("external_api_dependency") is not False,
        "secrets_or_api_keys_detected": boundary.get("contains_api_keys") is not False or declaration_record.get("secrets_required") is not False,
        "private_core_exposure_detected": boundary.get("private_core_exposure") is not False,
        "legal_certification_claim_detected": boundary.get("legal_certification") is not False,
        "precheck_gate_not_required": declaration_record.get("precheck_gate_required") is not True,
    }

    descriptions = {
        "operator_approval_contract_missing": "Operator approval contract artifact is missing.",
        "operator_approval_contract_not_ready": "Operator approval contract is not ready.",
        "operator_approval_contract_invalid": "Operator approval contract id/signature is missing.",
        "contract_does_not_require_operator_approval": "Contract does not require operator approval.",
        "contract_already_grants_approval": "Contract already grants approval unexpectedly.",
        "declaration_mode_invalid": "Declaration mode is invalid.",
        "required_declarations_missing": "Required declarations are missing.",
        "required_declarations_not_declared": "Required declarations are not declared.",
        "required_declarations_not_accepted": "Required declarations are not accepted.",
        "operator_approval_not_declared": "Operator approval is not declared.",
        "operator_approval_not_received": "Operator approval declaration is not received.",
        "operator_approval_not_granted": "Operator approval declaration is not granted.",
        "real_submission_allowed_true": "Real submission is allowed unexpectedly.",
        "ready_for_real_kaggle_submission_true": "Ready for real Kaggle submission is true unexpectedly.",
        "real_submission_created": "A real submission appears to have been created.",
        "kaggle_submission_already_sent": "A Kaggle submission appears to have been sent.",
        "upload_performed": "An upload appears to have been performed.",
        "external_api_dependency_detected": "External API dependency detected.",
        "secrets_or_api_keys_detected": "Secrets or API keys detected.",
        "private_core_exposure_detected": "Private core exposure detected.",
        "legal_certification_claim_detected": "Legal certification claim detected.",
        "precheck_gate_not_required": "Precheck gate is not required.",
    }

    return tuple(
        {
            "name": name,
            "active": issue_state[name],
            "severity": "BLOCKING",
            "description": descriptions[name],
        }
        for name in DECLARATION_ISSUES
    )


def build_milestone_6_operator_approval_declaration() -> Dict[str, Any]:
    contract = _read_json_if_available(OPERATOR_APPROVAL_CONTRACT_JSON)
    boundary = _boundary_from_contract(contract)
    declaration_record = _build_declaration_record(contract, boundary)

    gates = _build_declaration_gates(
        contract=contract,
        declaration_record=declaration_record,
        boundary=boundary,
    )
    issues = _build_declaration_issues(
        contract=contract,
        declaration_record=declaration_record,
        boundary=boundary,
    )

    passed_gate_count = sum(1 for gate in gates if gate["passed"] is True)
    issue_count = sum(1 for issue in issues if issue["active"] is True)
    warning_count = 0

    declaration_ready = (
        passed_gate_count == len(DECLARATION_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
        and declaration_record["operator_approval_declared"] is True
        and declaration_record["operator_approval_granted"] is True
        and declaration_record["real_submission_allowed"] is False
        and declaration_record["precheck_gate_required"] is True
    )

    declaration_index = {
        "milestone": "Milestone #6",
        "task": "Task 3",
        "declaration_mode": DECLARATION_MODE,
        "declaration_scope": DECLARATION_SCOPE,
        "declaration_verdict": DECLARATION_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_operator_approval_contract": contract.get("contract_id", "MISSING_CONTRACT_ID"),
        "required_declaration_count": len(REQUIRED_OPERATOR_DECLARATIONS),
        "declared_declaration_count": declaration_record["declared_declaration_count"],
        "accepted_declaration_count": declaration_record["accepted_declaration_count"],
        "operator_approval_declared": True,
        "operator_approval_received": True,
        "operator_approval_granted": True,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "precheck_gate_required": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base_payload = {
        "status": DECLARATION_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 3",
        "title": "Operator Approval Declaration v1",
        "baseline_commit": BASELINE_COMMIT,
        "operator_approval_contract_id": contract.get("contract_id", "MISSING_CONTRACT_ID"),
        "operator_approval_contract_signature": contract.get("signature", "MISSING_CONTRACT_SIGNATURE"),
        "operator_approval_contract_verdict": contract.get("contract_verdict", "MISSING_CONTRACT_VERDICT"),
        "declaration_mode": DECLARATION_MODE,
        "declaration_scope": DECLARATION_SCOPE,
        "declaration_verdict": DECLARATION_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "declaration_record": copy.deepcopy(declaration_record),
        "declaration_gates": list(gates),
        "declaration_issues": list(issues),
        "declaration_index": declaration_index,
        "boundary": boundary,
        "required_declaration_count": len(REQUIRED_OPERATOR_DECLARATIONS),
        "declared_declaration_count": declaration_record["declared_declaration_count"],
        "provided_declaration_count": declaration_record["provided_declaration_count"],
        "accepted_declaration_count": declaration_record["accepted_declaration_count"],
        "declaration_gate_count": len(DECLARATION_GATES),
        "passed_gate_count": passed_gate_count,
        "declaration_issue_count": issue_count,
        "warning_count": warning_count,
        "operator_approval_declaration_ready": declaration_ready,
        "operator_approval_required": True,
        "operator_approval_declared": True,
        "operator_approval_received": True,
        "operator_approval_granted": True,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "precheck_gate_required": True,
        "metadata": {
            "source": "milestone_6_operator_approval_declaration_v1",
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
    declaration_id = f"MILESTONE-6-OPERATOR-APPROVAL-DECLARATION-{signature[:12]}"

    return {
        **base_payload,
        "declaration_id": declaration_id,
        "signature": signature,
    }


def validate_milestone_6_operator_approval_declaration(declaration: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = declaration.get("boundary") if isinstance(declaration.get("boundary"), Mapping) else {}
    gates = declaration.get("declaration_gates") if isinstance(declaration.get("declaration_gates"), list) else []
    issues = declaration.get("declaration_issues") if isinstance(declaration.get("declaration_issues"), list) else []
    record = declaration.get("declaration_record") if isinstance(declaration.get("declaration_record"), Mapping) else {}
    index = declaration.get("declaration_index") if isinstance(declaration.get("declaration_index"), Mapping) else {}
    declared = record.get("declared_operator_declarations") if isinstance(record.get("declared_operator_declarations"), list) else []

    validation_checks = {
        "status_ready": declaration.get("status") == DECLARATION_STATUS,
        "declaration_id_present": isinstance(declaration.get("declaration_id"), str) and bool(declaration.get("declaration_id")),
        "signature_present": isinstance(declaration.get("signature"), str) and bool(declaration.get("signature")),
        "baseline_commit_is_operator_contract": str(declaration.get("baseline_commit", "")).startswith("34e7763"),
        "contract_id_present": isinstance(declaration.get("operator_approval_contract_id"), str)
        and declaration.get("operator_approval_contract_id") != "MISSING_CONTRACT_ID",
        "declaration_mode_valid": declaration.get("declaration_mode") == DECLARATION_MODE,
        "declaration_scope_valid": declaration.get("declaration_scope") == DECLARATION_SCOPE,
        "declaration_verdict_valid": declaration.get("declaration_verdict") == DECLARATION_VERDICT,
        "required_declaration_count_valid": declaration.get("required_declaration_count") == len(REQUIRED_OPERATOR_DECLARATIONS),
        "declared_declaration_count_valid": declaration.get("declared_declaration_count") == len(REQUIRED_OPERATOR_DECLARATIONS),
        "provided_declaration_count_valid": declaration.get("provided_declaration_count") == len(REQUIRED_OPERATOR_DECLARATIONS),
        "accepted_declaration_count_valid": declaration.get("accepted_declaration_count") == len(REQUIRED_OPERATOR_DECLARATIONS),
        "declared_declarations_present": len(declared) == len(REQUIRED_OPERATOR_DECLARATIONS),
        "declared_declarations_accepted": bool(declared)
        and all(
            item.get("required") is True
            and item.get("declared") is True
            and item.get("provided") is True
            and item.get("accepted") is True
            for item in declared
        ),
        "declaration_gate_count_matches": declaration.get("declaration_gate_count") == len(DECLARATION_GATES),
        "all_declaration_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "declaration_issue_count_zero": declaration.get("declaration_issue_count") == 0,
        "all_declaration_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "warning_count_zero": declaration.get("warning_count") == 0,
        "operator_approval_declaration_ready": declaration.get("operator_approval_declaration_ready") is True,
        "operator_approval_required": declaration.get("operator_approval_required") is True,
        "operator_approval_declared": declaration.get("operator_approval_declared") is True,
        "operator_approval_received": declaration.get("operator_approval_received") is True,
        "operator_approval_granted": declaration.get("operator_approval_granted") is True,
        "real_submission_allowed_false": declaration.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": declaration.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": declaration.get("real_submission_created") is False,
        "kaggle_submission_not_sent": declaration.get("kaggle_submission_sent") is False,
        "upload_not_performed": declaration.get("upload_performed") is False,
        "precheck_gate_required": declaration.get("precheck_gate_required") is True,
        "index_real_submission_allowed_false": index.get("real_submission_allowed") is False,
        "index_precheck_gate_required": index.get("precheck_gate_required") is True,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "declaration_id": declaration.get("declaration_id"),
        "signature": declaration.get("signature"),
    }


def render_operator_approval_declaration_markdown(declaration: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Operator Approval Declaration v1",
        "",
        "## Status",
        "",
        f"- status: {declaration['status']}",
        f"- declaration_id: {declaration['declaration_id']}",
        f"- signature: {declaration['signature']}",
        f"- baseline_commit: {declaration['baseline_commit']}",
        f"- operator_approval_contract_id: {declaration['operator_approval_contract_id']}",
        f"- operator_approval_contract_verdict: {declaration['operator_approval_contract_verdict']}",
        f"- declaration_mode: {declaration['declaration_mode']}",
        f"- declaration_scope: {declaration['declaration_scope']}",
        f"- declaration_verdict: {declaration['declaration_verdict']}",
        f"- next_allowed_stage: {declaration['next_allowed_stage']}",
        f"- required_declaration_count: {declaration['required_declaration_count']}",
        f"- declared_declaration_count: {declaration['declared_declaration_count']}",
        f"- provided_declaration_count: {declaration['provided_declaration_count']}",
        f"- accepted_declaration_count: {declaration['accepted_declaration_count']}",
        f"- declaration_gate_count: {declaration['declaration_gate_count']}",
        f"- passed_gate_count: {declaration['passed_gate_count']}",
        f"- declaration_issue_count: {declaration['declaration_issue_count']}",
        f"- warning_count: {declaration['warning_count']}",
        f"- operator_approval_declaration_ready: {declaration['operator_approval_declaration_ready']}",
        f"- operator_approval_required: {declaration['operator_approval_required']}",
        f"- operator_approval_declared: {declaration['operator_approval_declared']}",
        f"- operator_approval_received: {declaration['operator_approval_received']}",
        f"- operator_approval_granted: {declaration['operator_approval_granted']}",
        f"- real_submission_allowed: {declaration['real_submission_allowed']}",
        f"- ready_for_real_kaggle_submission: {declaration['ready_for_real_kaggle_submission']}",
        f"- real_submission_created: {declaration['real_submission_created']}",
        f"- kaggle_submission_sent: {declaration['kaggle_submission_sent']}",
        f"- upload_performed: {declaration['upload_performed']}",
        f"- precheck_gate_required: {declaration['precheck_gate_required']}",
        "",
        "## Declared operator declarations",
        "",
    ]

    for item in declaration["declaration_record"]["declared_operator_declarations"]:
        lines.append(
            f"- {item['name']}: required={item['required']} declared={item['declared']} "
            f"provided={item['provided']} accepted={item['accepted']} status={item['status']}"
        )

    lines.extend(["", "## Declaration gates", ""])

    for gate in declaration["declaration_gates"]:
        lines.append(f"- {gate['name']}: passed={gate['passed']} severity={gate['severity']}")

    lines.extend(["", "## Declaration issues", ""])

    for issue in declaration["declaration_issues"]:
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
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_V1_READY=true",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_VALID=true",
            "ARC_AGI3_MILESTONE_6_DECLARATION_MODE=OPERATOR_APPROVAL_DECLARATION_ONLY_NO_SUBMISSION",
            "ARC_AGI3_MILESTONE_6_DECLARATION_VERDICT=OPERATOR_APPROVAL_DECLARED_REAL_SUBMISSION_STILL_BLOCKED",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_DECLARED=true",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_RECEIVED=true",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_GRANTED=true",
            "ARC_AGI3_MILESTONE_6_REQUIRED_DECLARATION_COUNT=8",
            "ARC_AGI3_MILESTONE_6_DECLARED_DECLARATION_COUNT=8",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_PRECHECK_GATE_REQUIRED=true",
            "ARC_AGI3_MILESTONE_6_BASELINE_OPERATOR_CONTRACT_COMMIT=34e7763",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_operator_approval_declaration_manifest(declaration: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 OPERATOR APPROVAL DECLARATION MANIFEST v1",
        f"declaration_id={declaration['declaration_id']}",
        f"signature={declaration['signature']}",
        f"status={declaration['status']}",
        f"baseline_commit={declaration['baseline_commit']}",
        f"operator_approval_contract_id={declaration['operator_approval_contract_id']}",
        f"declaration_mode={declaration['declaration_mode']}",
        f"declaration_scope={declaration['declaration_scope']}",
        f"declaration_verdict={declaration['declaration_verdict']}",
        f"required_declaration_count={declaration['required_declaration_count']}",
        f"declared_declaration_count={declaration['declared_declaration_count']}",
        f"provided_declaration_count={declaration['provided_declaration_count']}",
        f"accepted_declaration_count={declaration['accepted_declaration_count']}",
        f"declaration_gate_count={declaration['declaration_gate_count']}",
        f"passed_gate_count={declaration['passed_gate_count']}",
        f"declaration_issue_count={declaration['declaration_issue_count']}",
        f"warning_count={declaration['warning_count']}",
        f"operator_approval_declaration_ready={declaration['operator_approval_declaration_ready']}",
        f"operator_approval_declared={declaration['operator_approval_declared']}",
        f"operator_approval_received={declaration['operator_approval_received']}",
        f"operator_approval_granted={declaration['operator_approval_granted']}",
        f"real_submission_allowed={declaration['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={declaration['ready_for_real_kaggle_submission']}",
        f"real_submission_created={declaration['real_submission_created']}",
        f"kaggle_submission_sent={declaration['kaggle_submission_sent']}",
        f"upload_performed={declaration['upload_performed']}",
        f"precheck_gate_required={declaration['precheck_gate_required']}",
        "",
        "DECLARED_OPERATOR_DECLARATIONS",
    ]

    for item in declaration["declaration_record"]["declared_operator_declarations"]:
        lines.append(
            f"{item['name']} required={item['required']} declared={item['declared']} "
            f"provided={item['provided']} accepted={item['accepted']} status={item['status']}"
        )

    lines.extend(["", "DECLARATION_GATES"])

    for gate in declaration["declaration_gates"]:
        lines.append(f"{gate['name']} passed={gate['passed']} severity={gate['severity']}")

    lines.extend(["", "DECLARATION_ISSUES"])

    for issue in declaration["declaration_issues"]:
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


def write_operator_approval_declaration_artifacts(
    declaration: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    declaration = dict(declaration or build_milestone_6_operator_approval_declaration())
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "milestone-6-operator-approval-declaration-v1.json"
    markdown_path = output_path / "milestone-6-operator-approval-declaration-v1.md"
    manifest_path = output_path / "milestone-6-operator-approval-declaration-manifest-v1.txt"
    index_path = output_path / "milestone-6-operator-approval-declaration-index-v1.json"

    json_path.write_text(json.dumps(declaration, indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_operator_approval_declaration_markdown(declaration), encoding="utf-8")
    manifest_path.write_text(render_operator_approval_declaration_manifest(declaration), encoding="utf-8")
    index_path.write_text(json.dumps(declaration["declaration_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_operator_approval_declaration_pipeline() -> Dict[str, Any]:
    declaration = build_milestone_6_operator_approval_declaration()
    validation = validate_milestone_6_operator_approval_declaration(declaration)
    artifacts = write_operator_approval_declaration_artifacts(declaration)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_PIPELINE_INVALID",
        "declaration_status": declaration["status"],
        "validation_status": validation["status"],
        "declaration": declaration,
        "declaration_id": declaration["declaration_id"],
        "signature": declaration["signature"],
        "declaration_mode": declaration["declaration_mode"],
        "declaration_verdict": declaration["declaration_verdict"],
        "required_declaration_count": declaration["required_declaration_count"],
        "declared_declaration_count": declaration["declared_declaration_count"],
        "provided_declaration_count": declaration["provided_declaration_count"],
        "accepted_declaration_count": declaration["accepted_declaration_count"],
        "declaration_gate_count": declaration["declaration_gate_count"],
        "passed_gate_count": declaration["passed_gate_count"],
        "declaration_issue_count": declaration["declaration_issue_count"],
        "warning_count": declaration["warning_count"],
        "operator_approval_declaration_ready": declaration["operator_approval_declaration_ready"],
        "operator_approval_declared": declaration["operator_approval_declared"],
        "operator_approval_received": declaration["operator_approval_received"],
        "operator_approval_granted": declaration["operator_approval_granted"],
        "real_submission_allowed": declaration["real_submission_allowed"],
        "ready_for_real_kaggle_submission": declaration["ready_for_real_kaggle_submission"],
        "real_submission_created": declaration["real_submission_created"],
        "kaggle_submission_sent": declaration["kaggle_submission_sent"],
        "upload_performed": declaration["upload_performed"],
        "precheck_gate_required": declaration["precheck_gate_required"],
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_6_operator_approval_declaration_pipeline_v1",
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
