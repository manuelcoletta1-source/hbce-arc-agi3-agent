"""Deterministic environment harness for HBCE ARC-AGI-3 public baseline.

Environment Harness v1 executes a loaded public-safe task through the current
ARC-AGI-3 baseline pipeline:

task_loader -> task_adapter -> observer -> world_model -> planner
-> verification_scoring -> trace_schema

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict

from hbce_arc_agi3.observer import observe_agent_state
from hbce_arc_agi3.planner import build_plan
from hbce_arc_agi3.scoring import verify_and_score_plan
from hbce_arc_agi3.task_loader import LoadedTask, load_task_file
from hbce_arc_agi3.trace_schema import build_agent_trace, validate_trace_dict
from hbce_arc_agi3.world_model import build_world_model_from_observation


@dataclass(frozen=True)
class EnvironmentRun:
    status: str
    run_id: str
    task_id: str
    observation: Dict[str, Any]
    world_model: Dict[str, Any]
    plan: Dict[str, Any]
    verification_scoring: Dict[str, Any]
    trace: Dict[str, Any]
    trace_validation: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_run_id(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")
    return "ARC-RUN-" + sha256(serial).hexdigest()[:16].upper()


def run_loaded_task(loaded_task: LoadedTask | Dict[str, Any]) -> EnvironmentRun:
    """Run one loaded task through the deterministic public pipeline."""

    loaded = loaded_task.to_dict() if isinstance(loaded_task, LoadedTask) else dict(loaded_task)

    if loaded.get("status") != "TASK_LOADER_READY":
        raise ValueError("Environment harness requires TASK_LOADER_READY input")

    task_id = str(loaded.get("task_id") or "anonymous-task")
    normalized = loaded.get("normalized")

    if not isinstance(normalized, dict):
        raise ValueError("Loaded task must contain normalized agent state")

    goal = str(normalized.get("goal_hint") or "solve")

    observation_obj = observe_agent_state(normalized)
    observation = observation_obj.to_dict()

    world_obj = build_world_model_from_observation(observation)
    world_model = world_obj.to_dict()

    plan = build_plan(world_model, goal=goal)
    verification_scoring = verify_and_score_plan(plan, world_model)

    trace_obj = build_agent_trace(
        task_id=task_id,
        observation=observation,
        model=world_model,
        goal=goal,
        plan=plan,
        action=plan["selected_action"],
        verification=verification_scoring["verification"],
        score=verification_scoring["score"],
    )
    trace = trace_obj.to_dict()
    trace_validation = validate_trace_dict(trace)

    run_basis = {
        "task_id": task_id,
        "source_path": loaded.get("source_path"),
        "observation_status": observation.get("status"),
        "world_model_status": world_model.get("status"),
        "plan_status": plan.get("status"),
        "verification_status": verification_scoring.get("verification", {}).get("status"),
        "score_status": verification_scoring.get("score", {}).get("status"),
        "trace_status": trace.get("status"),
        "trace_validation_status": trace_validation.get("status"),
    }

    run_id = _stable_run_id(run_basis)

    return EnvironmentRun(
        status="ENVIRONMENT_HARNESS_READY",
        run_id=run_id,
        task_id=task_id,
        observation=observation,
        world_model=world_model,
        plan=plan,
        verification_scoring=verification_scoring,
        trace=trace,
        trace_validation=trace_validation,
        metadata={
            "source": "environment_harness_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "pipeline": [
                "task_loader",
                "observer",
                "world_model",
                "planner",
                "verification_scoring",
                "trace_schema",
            ],
        },
    )


def run_task_file(path: str | Path, *, base_dir: str | Path | None = None) -> EnvironmentRun:
    """Load and run one local JSON task file."""

    loaded = load_task_file(path, base_dir=base_dir)
    return run_loaded_task(loaded)


def validate_environment_run(run: EnvironmentRun | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Environment Harness v1 public run contract."""

    data = run.to_dict() if isinstance(run, EnvironmentRun) else dict(run)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    checks = {
        "status_ready": data.get("status") == "ENVIRONMENT_HARNESS_READY",
        "run_id_present": bool(data.get("run_id")),
        "task_id_present": bool(data.get("task_id")),
        "observation_ready": isinstance(data.get("observation"), dict) and data["observation"].get("status") == "OBSERVER_READY",
        "world_model_ready": isinstance(data.get("world_model"), dict) and data["world_model"].get("status") == "WORLD_MODEL_READY",
        "plan_ready": isinstance(data.get("plan"), dict) and data["plan"].get("status") == "PLANNER_READY",
        "verification_scoring_ready": isinstance(data.get("verification_scoring"), dict) and data["verification_scoring"].get("status") == "VERIFICATION_SCORING_READY",
        "trace_schema_ready": isinstance(data.get("trace"), dict) and data["trace"].get("status") == "TRACE_SCHEMA_READY",
        "trace_validation_ready": isinstance(data.get("trace_validation"), dict) and data["trace_validation"].get("status") == "TRACE_SCHEMA_VALID",
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
    }

    valid = all(checks.values())

    return {
        "status": "ENVIRONMENT_HARNESS_VALID" if valid else "ENVIRONMENT_HARNESS_INVALID",
        "valid": valid,
        "checks": checks,
        "run_id": data.get("run_id"),
        "task_id": data.get("task_id"),
        "metadata": {
            "source": "environment_harness_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def run_and_validate_task_file(
    path: str | Path,
    *,
    base_dir: str | Path | None = None,
) -> Dict[str, Any]:
    """Compatibility wrapper for task-file execution and validation."""

    run = run_task_file(path, base_dir=base_dir)
    validation = validate_environment_run(run)

    return {
        "status": "ENVIRONMENT_HARNESS_PIPELINE_READY",
        "run": run.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "environment_harness_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
        },
    }
