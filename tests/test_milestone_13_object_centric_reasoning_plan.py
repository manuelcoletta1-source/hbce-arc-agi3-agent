from pathlib import Path

from hbce_arc_agi3.milestone_13_object_centric_reasoning_plan import (
    NEXT_STAGE,
    PLAN_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    build_object_centric_reasoning_plan,
    build_object_centric_reasoning_plan_record,
    validate_object_centric_reasoning_plan_record,
    write_artifacts,
)


def _sample_source_record():
    return {
        "revision": "MILESTONE_13_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_V1",
        "task_verdict": "MILESTONE_13_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_READY",
        "plan_verdict": "TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION",
        "next_stage": "MILESTONE_13_TASK_4_OBJECT_CENTRIC_REASONING_PLAN_V1",
        "primitive_count": 43,
    }


def test_object_centric_reasoning_plan_record_is_valid():
    record = build_object_centric_reasoning_plan_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["plan_verdict"] == PLAN_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_plan_ready"] is True
    assert record["source_primitive_plan_ok"] is True
    assert record["object_centric_reasoning_plan_ready"] is True
    assert record["object_centric_reasoning_plan_valid"] is True
    assert record["object_reasoning_stage_count"] == 6
    assert record["object_feature_count"] == 14
    assert record["object_operation_group_count"] == 7
    assert record["object_operation_count"] == 35
    assert record["implementation_lane_count"] == 6
    assert record["runtime_wiring_forbidden_count"] == 6
    assert record["runtime_wiring_authorized"] is False
    assert record["runtime_solver_modified"] is False
    assert record["candidate_generator_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_object_centric_reasoning_plan_record(record) == []


def test_object_centric_reasoning_plan_has_expected_shape():
    plan = build_object_centric_reasoning_plan(_sample_source_record())

    assert plan["object_reasoning_stage_count"] == 6
    assert plan["object_feature_count"] == 14
    assert plan["object_operation_group_count"] == 7
    assert plan["object_operation_count"] == 35
    assert plan["implementation_lane_count"] == 6
    assert plan["runtime_wiring_forbidden_count"] == 6
    assert plan["risk_control_count"] == 10
    assert plan["quality_target_count"] == 7
    assert plan["runtime_wiring_authorized"] is False
    assert plan["recommended_next_stage"] == NEXT_STAGE


def test_object_centric_reasoning_blocks_runtime_wiring():
    record = build_object_centric_reasoning_plan_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_object_centric_reasoning_plan_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_object_centric_reasoning_blocks_candidate_generator_wiring():
    record = build_object_centric_reasoning_plan_record(baseline_commit="TEST-COMMIT")
    record["candidate_generator_modified"] = True

    issues = validate_object_centric_reasoning_plan_record(record)

    assert "candidate_generator_modified_NOT_FALSE" in issues


def test_object_centric_reasoning_blocks_kaggle_submission():
    record = build_object_centric_reasoning_plan_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_object_centric_reasoning_plan_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_object_centric_reasoning_fails_if_operation_count_mutated():
    record = build_object_centric_reasoning_plan_record(baseline_commit="TEST-COMMIT")
    record["object_operation_count"] = 34

    issues = validate_object_centric_reasoning_plan_record(record)

    assert "OBJECT_OPERATION_COUNT_MISMATCH" in issues


def test_object_centric_reasoning_artifacts_are_written(tmp_path: Path):
    record = build_object_centric_reasoning_plan_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-object-centric-reasoning-plan-v1.json" in written_files
    assert "milestone-13-object-centric-reasoning-plan-index-v1.json" in written_files
    assert "milestone-13-object-centric-reasoning-plan-manifest-v1.txt" in written_files
    assert "milestone-13-object-centric-reasoning-plan-v1.md" in written_files
