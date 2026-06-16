from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_plan import (
    NEXT_STAGE,
    PLAN_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    build_program_synthesis_candidate_generator_plan,
    build_program_synthesis_candidate_generator_plan_record,
    validate_program_synthesis_candidate_generator_plan_record,
    write_artifacts,
)


def _sample_source_record():
    return {
        "revision": "MILESTONE_13_OBJECT_CENTRIC_REASONING_PLAN_V1",
        "task_verdict": "MILESTONE_13_OBJECT_CENTRIC_REASONING_PLAN_READY",
        "plan_verdict": "OBJECT_CENTRIC_REASONING_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION",
        "next_stage": "MILESTONE_13_TASK_5_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_V1",
        "object_operation_count": 35,
    }


def test_program_synthesis_candidate_generator_plan_record_is_valid():
    record = build_program_synthesis_candidate_generator_plan_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["plan_verdict"] == PLAN_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_plan_ready"] is True
    assert record["source_object_plan_ok"] is True
    assert record["program_synthesis_candidate_generator_plan_ready"] is True
    assert record["program_synthesis_candidate_generator_plan_valid"] is True
    assert record["synthesis_stage_count"] == 6
    assert record["program_template_count"] == 12
    assert record["candidate_family_count"] == 7
    assert record["search_control_count"] == 8
    assert record["implementation_lane_count"] == 6
    assert record["runtime_wiring_forbidden_count"] == 6
    assert record["candidate_generator_wiring_authorized"] is False
    assert record["runtime_wiring_authorized"] is False
    assert record["runtime_solver_modified"] is False
    assert record["candidate_generator_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_program_synthesis_candidate_generator_plan_record(record) == []


def test_program_synthesis_candidate_generator_plan_has_expected_shape():
    plan = build_program_synthesis_candidate_generator_plan(_sample_source_record())

    assert plan["synthesis_stage_count"] == 6
    assert plan["program_template_count"] == 12
    assert plan["candidate_family_count"] == 7
    assert plan["search_control_count"] == 8
    assert plan["implementation_lane_count"] == 6
    assert plan["runtime_wiring_forbidden_count"] == 6
    assert plan["risk_control_count"] == 10
    assert plan["quality_target_count"] == 7
    assert plan["candidate_generator_wiring_authorized"] is False
    assert plan["runtime_wiring_authorized"] is False
    assert plan["recommended_next_stage"] == NEXT_STAGE


def test_program_synthesis_blocks_candidate_generator_wiring():
    record = build_program_synthesis_candidate_generator_plan_record(baseline_commit="TEST-COMMIT")
    record["candidate_generator_wiring_authorized"] = True

    issues = validate_program_synthesis_candidate_generator_plan_record(record)

    assert "candidate_generator_wiring_authorized_NOT_FALSE" in issues


def test_program_synthesis_blocks_runtime_wiring():
    record = build_program_synthesis_candidate_generator_plan_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_program_synthesis_candidate_generator_plan_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_program_synthesis_blocks_kaggle_submission():
    record = build_program_synthesis_candidate_generator_plan_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_program_synthesis_candidate_generator_plan_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_program_synthesis_fails_if_template_count_mutated():
    record = build_program_synthesis_candidate_generator_plan_record(baseline_commit="TEST-COMMIT")
    record["program_template_count"] = 11

    issues = validate_program_synthesis_candidate_generator_plan_record(record)

    assert "PROGRAM_TEMPLATE_COUNT_MISMATCH" in issues


def test_program_synthesis_artifacts_are_written(tmp_path: Path):
    record = build_program_synthesis_candidate_generator_plan_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-plan-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-plan-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-plan-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-plan-v1.md" in written_files
