def test_package_imports():
    import hbce_arc_agi3
    from hbce_arc_agi3.agent import run_agent

    assert hbce_arc_agi3.__version__ == "0.1.0"
    assert callable(run_agent)
