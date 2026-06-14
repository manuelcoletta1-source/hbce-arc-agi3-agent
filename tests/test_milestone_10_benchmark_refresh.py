from __future__ import annotations

from pathlib import Path

from hbce_arc_agi3.milestone_10_benchmark_refresh import (
    BENCHMARK_REFRESH_LABEL,
    BENCHMARK_REFRESH_MODE,
    BENCHMARK_REFRESH_PIPELINE_LABEL,
    BENCHMARK_REFRESH_VALIDATION,
    build_local_benchmark_cases,
    compute_signature,
    discover_solver_patch_helpers,
    repo_root,
    run_benchmark_refresh,
    write_benchmark_refresh_artifacts,
)


def test_solver_patch_helpers_are_discovered() -> None:
    helper_names = discover_solver_patch_helpers()

    assert len(helper_names) >= 6
    assert all(isinstance(name, str) for name in helper_names)
    assert helper_names == sorted(helper_names)


def test_local_benchmark_cases_use_helper_targets() -> None:
    helper_names = discover_solver_patch_helpers()
    cases = build_local_benchmark_cases(helper_names)

    assert len(cases) == 12
    assert all(case.case_id.startswith("M10-BR-") for case in cases)
    assert all(case.helper_targets for case in cases)
    assert all(case.baseline_score > 0 for case in cases)
    assert all(case.expected_patch_delta > 0 for case in cases)


def test_benchmark_refresh_result_is_valid_and_fail_closed() -> None:
    result = run_benchmark_refresh()

    assert result["pipelineLabel"] == BENCHMARK_REFRESH_PIPELINE_LABEL
    assert result["label"] == BENCHMARK_REFRESH_LABEL
    assert result["validation"] == BENCHMARK_REFRESH_VALIDATION
    assert result["mode"] == BENCHMARK_REFRESH_MODE

    assert result["benchmark_refresh_ready"] is True
    assert result["benchmark_refresh_valid"] is True
    assert result["helper_module_imported"] is True
    assert result["helper_count"] >= 6

    assert result["benchmark_case_count"] == 12
    assert result["measurement_count"] == 12
    assert result["improved_case_count"] == 12
    assert result["regression_case_count"] == 0
    assert result["mean_delta"] > 0

    assert result["runtime_integration_performed"] is False
    assert result["solver_runtime_modified"] is False
    assert result["candidate_refresh_created"] is False
    assert result["submission_candidate_created"] is False
    assert result["real_submission_allowed"] is False
    assert result["manual_upload_allowed"] is False
    assert result["kaggle_authentication_allowed"] is False
    assert result["kaggle_submission_sent"] is False
    assert result["fail_closed_required"] is True
    assert result["fail_closed_active"] is True


def test_benchmark_refresh_signature_is_deterministic() -> None:
    result = run_benchmark_refresh()
    signature = result["signature"]

    result_without_signature = dict(result)
    result_without_signature["signature"] = ""
    result_without_signature["benchmark_refresh_id"] = ""

    assert signature == compute_signature(result_without_signature)


def test_benchmark_refresh_artifacts_are_written(tmp_path: Path) -> None:
    result = run_benchmark_refresh()
    artifact_paths = write_benchmark_refresh_artifacts(result, output_dir=tmp_path)

    assert set(artifact_paths) == {
        "artifact_json_path",
        "artifact_markdown_path",
        "artifact_manifest_path",
        "artifact_index_path",
    }

    for path in tmp_path.iterdir():
        assert path.exists()
        assert path.read_text(encoding="utf-8").strip()

    json_file = tmp_path / "milestone-10-benchmark-refresh-v1.json"
    md_file = tmp_path / "milestone-10-benchmark-refresh-v1.md"
    manifest_file = tmp_path / "milestone-10-benchmark-refresh-manifest-v1.txt"
    index_file = tmp_path / "milestone-10-benchmark-refresh-index-v1.json"

    assert json_file.exists()
    assert md_file.exists()
    assert manifest_file.exists()
    assert index_file.exists()

    text = md_file.read_text(encoding="utf-8")
    assert "Benchmark Refresh v1" in text
    assert "Runtime integration performed: `False`" in text
    assert "Candidate refresh created: `False`" in text
    assert "`legalCertification=false`" in text


def test_default_artifact_paths_are_inside_repo() -> None:
    result = run_benchmark_refresh()
    artifact_paths = write_benchmark_refresh_artifacts(result)

    root = repo_root()
    for relative_path in artifact_paths.values():
        path = root / relative_path
        assert path.exists()
        assert str(path).startswith(str(root))
