"""HBCE ARC-AGI-3 public smoke baseline agent.

This is not the final competition agent.
It is the canonical minimal loop used to verify package structure,
trace generation and offline reproducibility.
"""

from __future__ import annotations

from typing import Any, Dict

from hbce_arc_agi3.audit import make_trace
from hbce_arc_agi3.memory import AgentMemory
from hbce_arc_agi3.observer import observe
from hbce_arc_agi3.planner import plan_action
from hbce_arc_agi3.scoring import score_plan
from hbce_arc_agi3.world_model import build_world_model


def run_agent(raw_state: Dict[str, Any] | None = None) -> Dict[str, Any]:
    memory = AgentMemory()
    observation = observe(raw_state)
    memory.remember_observation(observation)

    world_model = build_world_model(observation)
    plan = plan_action(world_model)
    score = score_plan(plan)

    decision = {
        "observation": observation,
        "world_model": world_model,
        "plan": plan,
        "score": score,
        "memory": memory.snapshot(),
    }
    memory.remember_decision(decision)

    return {
        "status": "ARC_AGI3_SMOKE_AGENT_READY",
        "verified": score["verified"],
        "decision": decision,
        "trace": make_trace(
            event="ARC_AGI3_SMOKE_AGENT_RUN",
            status="PASS" if score["verified"] else "FAIL",
            payload={"score": score["score"], "goal": plan["goal"]},
        ),
    }


if __name__ == "__main__":
    result = run_agent({"grid": [[1, 0], [0, 1]], "objects": [{"id": "A"}], "goal_hint": "solve"})
    print(result["status"])
    print(f"verified={result['verified']}")
    print(f"score={result['decision']['score']['score']}")
