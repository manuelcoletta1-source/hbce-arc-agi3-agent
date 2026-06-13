from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Dict, List


@dataclass(frozen=True)
class SubmissionArtifact:
    artifact_id: str
    artifact_type: str
    path: str
    required: bool
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubmissionPackage:
    status: str
    package_id: str
    task_id: str
    artifacts: List[SubmissionArtifact]
    trace: Dict[str, Any]
    verification: Dict[str, Any]
    score: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "package_id": self.package_id,
            "task_id": self.task_id,
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "trace": self.trace,
            "verification": self.verification,
            "score": self.score,
            "metadata": self.metadata,
        }


def _stable_hash(payload: Dict[str, Any]) -> str:
    serial = repr(sorted(payload.items())).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def default_submission_artifacts() -> List[SubmissionArtifact]:
    return [
        SubmissionArtifact(
            artifact_id="artifact-agent-source",
            artifact_type="source",
            path="src/hbce_arc_agi3",
            required=True,
            description="Public ARC-AGI-3 baseline agent source package.",
        ),
        SubmissionArtifact(
            artifact_id="artifact-tests",
            artifact_type="tests",
            path="tests",
            required=True,
            description="Public reproducibility and contract tests.",
        ),
        SubmissionArtifact(
            artifact_id="artifact-docs",
            artifact_type="documentation",
            path="docs",
            required=True,
            description="Public benchmark documentation and milestone records.",
        ),
        SubmissionArtifact(
            artifact_id="artifact-scripts",
            artifact_type="scripts",
            path="scripts",
            required=True,
            description="Public local execution and packaging scripts.",
        ),
    ]


def build_submission_package(
    *,
    task_id: str,
    trace: Dict[str, Any],
    verification: Dict[str, Any],
    score: Dict[str, Any],
) -> SubmissionPackage:
    basis = {
        "task_id": task_id,
        "trace_status": trace.get("status"),
        "verification_status": verification.get("status"),
        "verified": verification.get("verified"),
        "score_status": score.get("status"),
        "score": score.get("score"),
    }

    package_id = "ARC-SUBMISSION-" + _stable_hash(basis)

    return SubmissionPackage(
        status="SUBMISSION_PACKAGE_READY",
        package_id=package_id,
        task_id=task_id,
        artifacts=default_submission_artifacts(),
        trace=trace,
        verification=verification,
        score=score,
        metadata={
            "source": "submission_package_skeleton_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "kaggle_submission_sent": False,
            "contains_api_keys": False,
            "contains_private_runtime": False,
        },
    )


def validate_submission_package(package: SubmissionPackage | Dict[str, Any]) -> Dict[str, Any]:
    data = package.to_dict() if isinstance(package, SubmissionPackage) else package

    artifacts = data.get("artifacts") if isinstance(data.get("artifacts"), list) else []
    artifact_ids = {artifact.get("artifact_id") for artifact in artifacts if isinstance(artifact, dict)}

    checks = {
        "package_status_ready": data.get("status") == "SUBMISSION_PACKAGE_READY",
        "package_id_present": bool(data.get("package_id")),
        "task_id_present": bool(data.get("task_id")),
        "trace_present": isinstance(data.get("trace"), dict),
        "verification_present": isinstance(data.get("verification"), dict),
        "score_present": isinstance(data.get("score"), dict),
        "required_agent_source_artifact": "artifact-agent-source" in artifact_ids,
        "required_tests_artifact": "artifact-tests" in artifact_ids,
        "required_docs_artifact": "artifact-docs" in artifact_ids,
        "required_scripts_artifact": "artifact-scripts" in artifact_ids,
        "public_safe": bool(data.get("metadata", {}).get("public_safe")) if isinstance(data.get("metadata"), dict) else False,
        "deterministic": bool(data.get("metadata", {}).get("deterministic")) if isinstance(data.get("metadata"), dict) else False,
        "external_api_dependency_false": data.get("metadata", {}).get("external_api_dependency") is False if isinstance(data.get("metadata"), dict) else False,
        "kaggle_submission_not_sent": data.get("metadata", {}).get("kaggle_submission_sent") is False if isinstance(data.get("metadata"), dict) else False,
        "contains_no_api_keys": data.get("metadata", {}).get("contains_api_keys") is False if isinstance(data.get("metadata"), dict) else False,
        "contains_no_private_runtime": data.get("metadata", {}).get("contains_private_runtime") is False if isinstance(data.get("metadata"), dict) else False,
    }

    valid = all(checks.values())

    return {
        "status": "SUBMISSION_PACKAGE_VALID" if valid else "SUBMISSION_PACKAGE_INVALID",
        "valid": valid,
        "checks": checks,
        "package_id": data.get("package_id"),
        "task_id": data.get("task_id"),
        "metadata": {
            "source": "submission_package_skeleton_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def build_public_submission_package_from_pipeline(
    *,
    task_id: str,
    trace: Dict[str, Any],
    verification_scoring: Dict[str, Any],
) -> Dict[str, Any]:
    verification = verification_scoring.get("verification", {})
    score = verification_scoring.get("score", {})

    package = build_submission_package(
        task_id=task_id,
        trace=trace,
        verification=verification,
        score=score,
    )

    validation = validate_submission_package(package)

    return {
        "status": "PUBLIC_SUBMISSION_PACKAGE_SKELETON_READY",
        "package": package.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "submission_package_skeleton_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "kaggle_submission_sent": False,
        },
    }
