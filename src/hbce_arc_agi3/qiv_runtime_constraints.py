from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


QIV_LINK_NAME = "QIV_V2_4_RUNTIME_CONSTRAINT_LINK_V1"
QIV_LINK_READY = "QIV_V2_4_RUNTIME_CONSTRAINT_LINK_V1_READY"
QIV_LINK_VALID = "QIV_V2_4_RUNTIME_CONSTRAINT_LINK_V1_VALID"
QIV_PIPELINE_READY = "QIV_V2_4_RUNTIME_CONSTRAINT_LINK_V1_PIPELINE_READY"

SOURCE_DOCUMENT_TITLE = "Quadro Quantistico-Informazionale dei Vincoli v2.4"
SOURCE_DOCUMENT_FILENAME = "QIV_v2_4_Quadro_Quantistico_Informazionale_dei_Vincoli.pdf"
SOURCE_DOCUMENT_VERSION = "v2.4"
SOURCE_DOCUMENT_MODULE = "Programmazione & Addestramento"

MILESTONE_CONTEXT = "MILESTONE_14_CONTROLLED_RUNTIME_INTEGRATION"
LINK_STAGE = "QIV_CONSTRAINT_LAYER_ATTACHED_AFTER_OPERATOR_APPROVAL_GATE"
PREVIOUS_STAGE = "MILESTONE_14_TASK_8_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_OPERATOR_APPROVAL_GATE_V1"
NEXT_STAGE = "MILESTONE_14_TASK_9_LOCAL_SOLVER_CONTROLLED_RUNTIME_INTEGRATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"

OUTPUT_DIR = Path("examples/milestone-14/qiv-runtime-constraint-link-v1")
OUTPUT_JSON = OUTPUT_DIR / "qiv-runtime-constraint-link-v1.json"
OUTPUT_INDEX = OUTPUT_DIR / "qiv-runtime-constraint-link-index-v1.json"
OUTPUT_MANIFEST = OUTPUT_DIR / "qiv-runtime-constraint-link-manifest-v1.txt"
OUTPUT_MD = OUTPUT_DIR / "qiv-runtime-constraint-link-v1.md"
DOC_PATH = Path("docs/theory/qiv-v2-4-runtime-constraint-framework.md")


DomainMode = Literal["QUANTUM", "CLASSICAL_STOCHASTIC", "HYBRID", "RUNTIME_AUDIT"]
FailClosedAction = Literal["BLOCK", "AUDIT", "ROLLBACK", "HUMAN_REVIEW"]


QIV_REQUIRED_FIELDS = [
    "domain_mode",
    "initial_state",
    "observed_system",
    "environment_context",
    "physical_record",
    "digital_record",
    "proof_record",
    "modeling_gauge",
    "active_constraints",
    "dynamic_engine",
    "measurement_mode",
    "observable_prediction",
    "outcome",
    "cost_layers",
    "error_threshold",
    "falsification_criterion",
    "fail_closed_action",
]


QIV_ENGINE_MAP = {
    "QEngine": "quantum_state_and_physical_quantum_dynamics",
    "CEngine": "classical_or_stochastic_runtime_dynamics",
    "IEngine": "physical_to_digital_record_interface",
    "ProofEngine": "technical_proof_and_fail_closed_verification",
}


@dataclass(frozen=True)
class QivRuntimeConstraintRecord:
    domain_mode: DomainMode
    initial_state: str
    observed_system: str
    environment_context: str
    physical_record: str
    digital_record: str
    proof_record: str
    modeling_gauge: str
    active_constraints: tuple[str, ...]
    dynamic_engine: str
    measurement_mode: str
    observable_prediction: str
    outcome: str
    cost_layers: tuple[str, ...]
    error_threshold: str
    falsification_criterion: str
    fail_closed_action: FailClosedAction


@dataclass(frozen=True)
class QivRuntimeConstraintLink:
    link_name: str
    status: str
    milestone_context: str
    link_stage: str
    previous_stage: str
    next_stage: str
    source_document_title: str
    source_document_filename: str
    source_document_version: str
    source_document_module: str
    signature: str
    baseline_commit: str
    qiv_core_chain: tuple[str, ...]
    qiv_engine_map: dict[str, str]
    qiv_required_fields: tuple[str, ...]
    example_record: QivRuntimeConstraintRecord
    qiv_linked_to_programming: bool
    qiv_linked_to_training: bool
    qiv_linked_to_runtime_audit: bool
    qiv_linked_to_fail_closed: bool
    qiv_linked_to_robotics: bool
    qiv_linked_to_arc_agi3_diagnostics: bool
    qiv_is_solver_direct: bool
    qiv_changes_runtime_solver: bool
    qiv_authorizes_implementation: bool
    qiv_overrides_operator_gate: bool
    runtime_activation_performed: bool
    runtime_execution_performed: bool
    implementation_performed: bool
    real_submission_allowed: bool
    legal_certification: bool
    private_core_exposure: bool
    public_safe: bool
    deterministic: bool
    local_only: bool
    fail_closed_required: bool
    fail_closed_active: bool
    created_at_utc: str


@dataclass(frozen=True)
class ValidationResult:
    status: str
    valid: bool
    issue_count: int
    warning_count: int
    issues: list[str]
    warnings: list[str]


def _git_head() -> str:
    try:
        value = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return value or "NO_GIT_HEAD"
    except Exception:
        return "NO_GIT_HEAD"


def _signature(seed: dict[str, object]) -> str:
    canonical = json.dumps(seed, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16].upper()


def build_example_qiv_runtime_constraint_record() -> QivRuntimeConstraintRecord:
    return QivRuntimeConstraintRecord(
        domain_mode="RUNTIME_AUDIT",
        initial_state="operator_gate_closed_after_milestone_14_task_8",
        observed_system="hbce_arc_agi3_controlled_runtime_integration_chain",
        environment_context="local_only_public_safe_deterministic_repository_workflow",
        physical_record="not_applicable_for_pure_runtime_audit_record",
        digital_record="git_commit_hash_and_json_artifact_record",
        proof_record="technical_audit_receipt_with_validation_status",
        modeling_gauge="declared_runtime_audit_domain_not_quantum_physical_claim",
        active_constraints=(
            "operator_approval_required",
            "operator_approval_received_false",
            "runtime_activation_forbidden",
            "implementation_authorized_false",
            "real_submission_allowed_false",
        ),
        dynamic_engine="ProofEngine",
        measurement_mode="artifact_validation_and_pytest_suite",
        observable_prediction="gate_remains_closed_until_explicit_operator_approval",
        outcome="implementation_blocked",
        cost_layers=(
            "digital_record_cost",
            "proof_record_cost",
            "review_cost",
        ),
        error_threshold="zero_gate_failures_allowed",
        falsification_criterion="any_runtime_activation_or_authorization_without_operator_approval_invalidates_record",
        fail_closed_action="BLOCK",
    )


def build_qiv_runtime_constraint_link(*, baseline_commit: str | None = None) -> QivRuntimeConstraintLink:
    baseline = baseline_commit or _git_head()
    example = build_example_qiv_runtime_constraint_record()

    seed = {
        "link_name": QIV_LINK_NAME,
        "baseline_commit": baseline,
        "source_document_title": SOURCE_DOCUMENT_TITLE,
        "source_document_version": SOURCE_DOCUMENT_VERSION,
        "previous_stage": PREVIOUS_STAGE,
        "next_stage": NEXT_STAGE,
        "example_record": asdict(example),
    }

    return QivRuntimeConstraintLink(
        link_name=QIV_LINK_NAME,
        status=QIV_LINK_READY,
        milestone_context=MILESTONE_CONTEXT,
        link_stage=LINK_STAGE,
        previous_stage=PREVIOUS_STAGE,
        next_stage=NEXT_STAGE,
        source_document_title=SOURCE_DOCUMENT_TITLE,
        source_document_filename=SOURCE_DOCUMENT_FILENAME,
        source_document_version=SOURCE_DOCUMENT_VERSION,
        source_document_module=SOURCE_DOCUMENT_MODULE,
        signature=_signature(seed),
        baseline_commit=baseline,
        qiv_core_chain=(
            "state",
            "constrained_dynamics",
            "measurement",
            "outcome",
            "record",
            "cost",
            "verification",
        ),
        qiv_engine_map=QIV_ENGINE_MAP,
        qiv_required_fields=tuple(QIV_REQUIRED_FIELDS),
        example_record=example,
        qiv_linked_to_programming=True,
        qiv_linked_to_training=True,
        qiv_linked_to_runtime_audit=True,
        qiv_linked_to_fail_closed=True,
        qiv_linked_to_robotics=True,
        qiv_linked_to_arc_agi3_diagnostics=True,
        qiv_is_solver_direct=False,
        qiv_changes_runtime_solver=False,
        qiv_authorizes_implementation=False,
        qiv_overrides_operator_gate=False,
        runtime_activation_performed=False,
        runtime_execution_performed=False,
        implementation_performed=False,
        real_submission_allowed=False,
        legal_certification=False,
        private_core_exposure=False,
        public_safe=True,
        deterministic=True,
        local_only=True,
        fail_closed_required=True,
        fail_closed_active=True,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def validate_qiv_runtime_constraint_record(record: QivRuntimeConstraintRecord) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    data = asdict(record)

    for field in QIV_REQUIRED_FIELDS:
        value = data.get(field)
        if value in (None, "", (), []):
            issues.append(f"missing_required_qiv_field:{field}")

    if record.domain_mode not in {"QUANTUM", "CLASSICAL_STOCHASTIC", "HYBRID", "RUNTIME_AUDIT"}:
        issues.append("invalid_domain_mode")

    if record.dynamic_engine not in QIV_ENGINE_MAP:
        issues.append("invalid_dynamic_engine")

    if record.fail_closed_action not in {"BLOCK", "AUDIT", "ROLLBACK", "HUMAN_REVIEW"}:
        issues.append("invalid_fail_closed_action")

    if "falsification" not in " ".join([record.falsification_criterion.lower(), record.error_threshold.lower()]):
        warnings.append("falsification_language_not_explicit")

    status = QIV_LINK_VALID if not issues else "QIV_V2_4_RUNTIME_CONSTRAINT_RECORD_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def validate_qiv_runtime_constraint_link(link: QivRuntimeConstraintLink) -> ValidationResult:
    issues: list[str] = []
    warnings: list[str] = []

    example_validation = validate_qiv_runtime_constraint_record(link.example_record)
    if not example_validation.valid:
        issues.extend(example_validation.issues)

    expected_true = {
        "qiv_linked_to_programming": link.qiv_linked_to_programming,
        "qiv_linked_to_training": link.qiv_linked_to_training,
        "qiv_linked_to_runtime_audit": link.qiv_linked_to_runtime_audit,
        "qiv_linked_to_fail_closed": link.qiv_linked_to_fail_closed,
        "qiv_linked_to_arc_agi3_diagnostics": link.qiv_linked_to_arc_agi3_diagnostics,
        "public_safe": link.public_safe,
        "deterministic": link.deterministic,
        "local_only": link.local_only,
        "fail_closed_required": link.fail_closed_required,
        "fail_closed_active": link.fail_closed_active,
    }

    for key, value in expected_true.items():
        if value is not True:
            issues.append(f"{key}:expected_true")

    expected_false = {
        "qiv_is_solver_direct": link.qiv_is_solver_direct,
        "qiv_changes_runtime_solver": link.qiv_changes_runtime_solver,
        "qiv_authorizes_implementation": link.qiv_authorizes_implementation,
        "qiv_overrides_operator_gate": link.qiv_overrides_operator_gate,
        "runtime_activation_performed": link.runtime_activation_performed,
        "runtime_execution_performed": link.runtime_execution_performed,
        "implementation_performed": link.implementation_performed,
        "real_submission_allowed": link.real_submission_allowed,
        "legal_certification": link.legal_certification,
        "private_core_exposure": link.private_core_exposure,
    }

    for key, value in expected_false.items():
        if value is not False:
            issues.append(f"{key}:expected_false")

    if len(link.qiv_required_fields) != 17:
        issues.append("qiv_required_fields_count_mismatch")

    if set(link.qiv_engine_map) != {"QEngine", "CEngine", "IEngine", "ProofEngine"}:
        issues.append("qiv_engine_map_incomplete")

    if link.previous_stage != PREVIOUS_STAGE:
        issues.append("previous_stage_mismatch")

    if link.next_stage != NEXT_STAGE:
        issues.append("next_stage_mismatch")

    status = QIV_LINK_VALID if not issues else "QIV_V2_4_RUNTIME_CONSTRAINT_LINK_V1_INVALID"
    return ValidationResult(
        status=status,
        valid=not issues,
        issue_count=len(issues),
        warning_count=len(warnings),
        issues=issues,
        warnings=warnings,
    )


def write_qiv_runtime_constraint_link_artifacts(
    *,
    output_dir: Path = OUTPUT_DIR,
    doc_path: Path = DOC_PATH,
) -> tuple[QivRuntimeConstraintLink, ValidationResult, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    output_json = output_dir / "qiv-runtime-constraint-link-v1.json"
    output_index = output_dir / "qiv-runtime-constraint-link-index-v1.json"
    output_manifest = output_dir / "qiv-runtime-constraint-link-manifest-v1.txt"
    output_md = output_dir / "qiv-runtime-constraint-link-v1.md"

    link = build_qiv_runtime_constraint_link()
    validation = validate_qiv_runtime_constraint_link(link)

    payload = {
        "record": asdict(link),
        "validation": asdict(validation),
    }

    index = {
        "link_name": link.link_name,
        "status": link.status,
        "validation_status": validation.status,
        "valid": validation.valid,
        "signature": link.signature,
        "baseline_commit": link.baseline_commit,
        "source_document_title": link.source_document_title,
        "source_document_filename": link.source_document_filename,
        "previous_stage": link.previous_stage,
        "next_stage": link.next_stage,
        "artifact_paths": {
            "json": str(output_json),
            "index": str(output_index),
            "manifest": str(output_manifest),
            "markdown": str(output_md),
            "doc": str(doc_path),
        },
    }

    manifest = "\n".join(
        [
            f"link_name={link.link_name}",
            f"status={link.status}",
            f"validation_status={validation.status}",
            f"valid={validation.valid}",
            f"signature={link.signature}",
            f"baseline_commit={link.baseline_commit}",
            f"source_document_title={link.source_document_title}",
            f"source_document_filename={link.source_document_filename}",
            f"source_document_version={link.source_document_version}",
            f"source_document_module={link.source_document_module}",
            f"previous_stage={link.previous_stage}",
            f"next_stage={link.next_stage}",
            f"qiv_linked_to_programming={link.qiv_linked_to_programming}",
            f"qiv_linked_to_training={link.qiv_linked_to_training}",
            f"qiv_linked_to_runtime_audit={link.qiv_linked_to_runtime_audit}",
            f"qiv_linked_to_fail_closed={link.qiv_linked_to_fail_closed}",
            f"qiv_is_solver_direct={link.qiv_is_solver_direct}",
            f"qiv_changes_runtime_solver={link.qiv_changes_runtime_solver}",
            f"qiv_authorizes_implementation={link.qiv_authorizes_implementation}",
            f"qiv_overrides_operator_gate={link.qiv_overrides_operator_gate}",
            f"runtime_activation_performed={link.runtime_activation_performed}",
            f"implementation_performed={link.implementation_performed}",
            f"real_submission_allowed={link.real_submission_allowed}",
            f"legal_certification={link.legal_certification}",
            "",
        ]
    )

    md = "\n".join(
        [
            "# QIV v2.4 Runtime Constraint Framework",
            "",
            f"Status: `{link.status}`",
            f"Validation: `{validation.status}`",
            f"Signature: `{link.signature}`",
            f"Baseline commit: `{link.baseline_commit}`",
            "",
            "## Source",
            "",
            f"- Document: `{link.source_document_title}`",
            f"- Version: `{link.source_document_version}`",
            f"- Module: `{link.source_document_module}`",
            f"- Filename reference: `{link.source_document_filename}`",
            "",
            "## Runtime chain",
            "",
            "`state -> constrained_dynamics -> measurement -> outcome -> record -> cost -> verification`",
            "",
            "## Engine map",
            "",
            "- `QEngine`: quantum state and physical quantum dynamics",
            "- `CEngine`: classical/stochastic runtime dynamics",
            "- `IEngine`: physical-to-digital record interface",
            "- `ProofEngine`: technical proof and fail-closed verification",
            "",
            "## Project placement",
            "",
            f"- Previous stage: `{link.previous_stage}`",
            f"- Link stage: `{link.link_stage}`",
            f"- Next stage: `{link.next_stage}`",
            "",
            "## Boundary",
            "",
            f"- qiv_is_solver_direct: `{link.qiv_is_solver_direct}`",
            f"- qiv_changes_runtime_solver: `{link.qiv_changes_runtime_solver}`",
            f"- qiv_authorizes_implementation: `{link.qiv_authorizes_implementation}`",
            f"- qiv_overrides_operator_gate: `{link.qiv_overrides_operator_gate}`",
            f"- implementation_performed: `{link.implementation_performed}`",
            f"- runtime_activation_performed: `{link.runtime_activation_performed}`",
            f"- real_submission_allowed: `{link.real_submission_allowed}`",
            f"- legal_certification: `{link.legal_certification}`",
            "",
        ]
    )

    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_index.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_manifest.write_text(manifest, encoding="utf-8")
    output_md.write_text(md, encoding="utf-8")
    doc_path.write_text(md, encoding="utf-8")

    return link, validation, {
        "json": str(output_json),
        "index": str(output_index),
        "manifest": str(output_manifest),
        "markdown": str(output_md),
        "doc": str(doc_path),
    }


__all__ = [
    "QIV_LINK_NAME",
    "QIV_LINK_READY",
    "QIV_LINK_VALID",
    "QIV_PIPELINE_READY",
    "SOURCE_DOCUMENT_TITLE",
    "PREVIOUS_STAGE",
    "NEXT_STAGE",
    "QivRuntimeConstraintRecord",
    "QivRuntimeConstraintLink",
    "ValidationResult",
    "build_example_qiv_runtime_constraint_record",
    "build_qiv_runtime_constraint_link",
    "validate_qiv_runtime_constraint_record",
    "validate_qiv_runtime_constraint_link",
    "write_qiv_runtime_constraint_link_artifacts",
]
