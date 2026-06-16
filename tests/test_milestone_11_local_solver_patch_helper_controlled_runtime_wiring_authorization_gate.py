from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_authorization_gate import (
    NEXT_STAGE,
    build_record,
    validate_record,
    write_artifacts,
)


def test_task_23_record_is_ready_and_valid():
    record = build_record()
    validation = validate_record(record)

    assert record["task_23_ready"] is True
    assert record["authorization_gate_ready"] is True
    assert record["authorization_gate_passed"] is True
    assert validation["valid"] is True
    assert validation["failure_count"] == 0


def test_task_23_keeps_runtime_wiring_blocked():
    record = build_record()

    assert record["operator_approval_required"] is True
    assert record["operator_approval_granted"] is False
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_solver_patch_allowed"] is False
    assert record["ranker_runtime_patch_allowed"] is False
    assert record["runtime_wiring_performed"] is False


def test_task_23_keeps_score_and_submission_blocked():
    record = build_record()

    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["official_score_claim_allowed"] is False
    assert record["competitive_score_claim_allowed"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False


def test_task_23_next_stage_is_operator_approval():
    record = build_record()

    assert record["next_stage"] == NEXT_STAGE
    assert record["decision"]["next_stage"] == NEXT_STAGE


def test_task_23_artifacts_are_written():
    record = build_record()
    paths = write_artifacts(record)

    assert len(paths) >= 9
    assert any(path.endswith(".json") for path in paths)
    assert any(path.endswith(".md") for path in paths)
    assert any(path.endswith(".txt") for path in paths)
