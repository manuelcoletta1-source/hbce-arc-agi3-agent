#!/usr/bin/env python3
"""Run local HBCE ARC-AGI-3 smoke agent."""

from hbce_arc_agi3.agent import run_agent


def main() -> int:
    result = run_agent({"grid": [[1, 0], [0, 1]], "objects": [{"id": "seed"}], "goal_hint": "solve"})
    print(result["status"])
    print(f"verified={result['verified']}")
    print(f"goal={result['decision']['plan']['goal']}")
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
