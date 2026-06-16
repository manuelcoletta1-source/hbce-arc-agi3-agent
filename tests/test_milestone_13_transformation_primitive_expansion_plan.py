from pathlib import Path

from hbce_arc_agi3.milestone_13_transformation_primitive_expansion_plan import (
    NEXT_STAGE,
    PLAN_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    build_primitive_expansion_plan,
    build_transformation_primitive_expansion_plan_record,
    validate_transformation_primitive_expansion_plan_record,
    write_artifacts,
)


def _sample_source_record():
    return {
        "revision": "MILESTONE_13_SOLVER_CAPABILITY_GAP_AUDIT_V1",
        "task_verdict": "MILESTONE_13_SOLVER_CAPABILITY_GAP_AUDIT_READY",
        "audit_verdict": "SOLVER_CAPABILITY_GAP_AUDIT_READY_FOR_LOCAL_IMPROVEMENT_PLAN",
        "top_priority": "TRANSFORMATION_PRIMITIVE_EXPANSION",
        "next_stage": "MILESTONE_13_TASK_3_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_V1",
    }


def test_transformation_primitive_expansion_plan_record_is_valid():
    record = build_transformation_primitive_expansion_plan_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["plan_verdict"] == PLAN_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_audit_ready"] is True
    assert record["source_top_priority_ok"] is True
    assert record["transformation_primitive_expansion_plan_ready"] is True
    assert record["transformation_primitive_expansion_plan_valid"] is True
    assert record["primitive_group_count"] == 7
    assert record["primitive_count"] == 43
    assert record["implementation_slice_count"] == 6
    assert record["runtime_wiring_forbidden_count"] == 6
    assert record["runtime_wiring_authorized"] is False
    assert record["runtime_solver_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_transformation_primitive_expansion_plan_record(record) == []


def test_primitive_expansion_plan_has_expected_shape():
    plan = build_primitive_expansion_plan(_sample_source_record())

    assert plan["primitive_group_count"] == 7
    assert plan["primitive_count"] == 43
    assert plan["implementation_slice_count"] == 6
    assert plan["runtime_wiring_forbidden_count"] == 6
    assert plan["risk_control_count"] == 10
    assert plan["quality_target_count"] == 7
    assert plan["runtime_wiring_authorized"] is False
    assert plan["recommended_next_stage"] == NEXT_STAGE


def test_transformation_primitive_expansion_blocks_runtime_wiring():
    record = build_transformation_primitive_expansion_plan_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_transformation_primitive_expansion_plan_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_transformation_primitive_expansion_blocks_runtime_solver_modification():
    record = build_transformation_primitive_expansion_plan_record(baseline_commit="TEST-COMMIT")
    record["runtime_solver_modified"] = True

    issues = validate_transformation_primitive_expansion_plan_record(record)

    assert "runtime_solver_modified_NOT_FALSE" in issues


def test_transformation_primitive_expansion_blocks_kaggle_submission():
    record = build_transformation_primitive_expansion_plan_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_transformation_primitive_expansion_plan_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_transformation_primitive_expansion_fails_if_primitive_count_mutated():
    record = build_transformation_primitive_expansion_plan_record(baseline_commit="TEST-COMMIT")
    record["primitive_count"] = 42

    issues = validate_transformation_primitive_expansion_plan_record(record)

    assert "PRIMITIVE_COUNT_MISMATCH" in issues


def test_transformation_primitive_expansion_artifacts_are_written(tmp_path: Path):
    record = build_transformation_primitive_expansion_plan_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-transformation-primitive-expansion-plan-v1.json" in written_files
    assert "milestone-13-transformation-primitive-expansion-plan-index-v1.json" in written_files
    assert "milestone-13-transformation-primitive-expansion-plan-manifest-v1.txt" in written_files
    assert "milestone-13-transformation-primitive-expansion-plan-v1.md" in written_files
