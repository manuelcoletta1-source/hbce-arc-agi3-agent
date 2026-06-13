from hbce_arc_agi3.agent import run_agent


def test_agent_smoke_contract():
    result = run_agent({"grid": [[1]], "objects": [{"id": "x"}], "goal_hint": "solve"})

    assert result["status"] == "ARC_AGI3_SMOKE_AGENT_READY"
    assert result["verified"] is True
    assert result["decision"]["world_model"]["status"] == "WORLD_MODEL_READY"
    assert result["decision"]["plan"]["status"] == "PLAN_READY"
    assert result["decision"]["score"]["status"] == "SCORE_READY"
    assert result["trace"]["legal_certification"] is False
    assert result["trace"]["opc_boundary"] == "technical research trace only"
