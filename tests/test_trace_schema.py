import json

from hbce_arc_agi3.trace_schema import (
    TRACE_SCHEMA_VERSION,
    build_agent_trace,
    validate_trace_dict,
)


def test_build_agent_trace_contract():
    trace = build_agent_trace(
        task_id="demo-task",
        observation={"grid": [[1]]},
        model={"dimensions": [1, 1]},
        goal="solve",
        plan={"candidate_actions": ["noop"]},
        action={"type": "noop"},
        verification={"verified": True},
        score={"score": 1.0},
    )

    assert trace.status == "TRACE_SCHEMA_READY"
    assert trace.schema_version == TRACE_SCHEMA_VERSION
    assert trace.trace_id.startswith("ARC-TRACE-")
    assert trace.task_id == "demo-task"
    assert trace.metadata["source"] == "trace_schema_v1"
    assert trace.metadata["stage_count"] == 7
    assert [step.stage for step in trace.steps] == [
        "observation",
        "model",
        "goal",
        "plan",
        "action",
        "verification",
        "score",
    ]


def test_trace_schema_is_json_serializable_and_deterministic():
    trace_a = build_agent_trace(task_id="same", observation={"grid": [[1, 0]]})
    trace_b = build_agent_trace(task_id="same", observation={"grid": [[1, 0]]})

    assert trace_a.trace_id == trace_b.trace_id

    encoded = json.dumps(trace_a.to_dict(), sort_keys=True)
    assert "TRACE_SCHEMA_READY" in encoded
    assert "ARC-TRACE-" in encoded


def test_validate_trace_dict():
    trace = build_agent_trace(task_id="validate-me").to_dict()
    result = validate_trace_dict(trace)

    assert result["status"] == "TRACE_SCHEMA_VALID"
    assert result["valid"] is True
    assert result["missing"] == []
    assert result["schema_version"] == TRACE_SCHEMA_VERSION

    invalid = validate_trace_dict({"status": "TRACE_SCHEMA_READY"})
    assert invalid["status"] == "TRACE_SCHEMA_INVALID"
    assert invalid["valid"] is False
    assert "trace_id" in invalid["missing"]
