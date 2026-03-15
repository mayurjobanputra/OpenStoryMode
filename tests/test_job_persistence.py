"""Unit tests for job persistence module (save and update)."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from app.models import (
    AspectRatio,
    GenerationRequest,
    Job,
    JobStage,
    Scene,
    VideoLength,
)
from app.job_persistence import (
    save_job_metadata,
    update_job_metadata,
    load_job_metadata,
    restore_jobs_from_disk,
    _serialize_job,
)


def _make_job(
    job_id: str = "test-job-1",
    stage: JobStage = JobStage.SCRIPT_GENERATION,
    scenes: list | None = None,
    error: str | None = None,
    error_stage: JobStage | None = None,
) -> Job:
    return Job(
        job_id=job_id,
        request=GenerationRequest(
            prompt="A cat on the moon",
            video_length=VideoLength.THIRTY,
            aspect_ratio=AspectRatio.HORIZONTAL,
        ),
        stage=stage,
        scenes=scenes or [],
        error=error,
        error_stage=error_stage,
        created_at="2025-01-15T10:30:00Z",
    )


class TestSerializeJob:
    def test_basic_fields(self):
        job = _make_job()
        data = _serialize_job(job)
        assert data["job_id"] == "test-job-1"
        assert data["prompt"] == "A cat on the moon"
        assert data["video_length"] == "30s"
        assert data["aspect_ratio"] == "16:9"
        assert data["status"] == "script_generation"
        assert data["created_at"] == "2025-01-15T10:30:00Z"
        assert data["updated_at"] is None
        assert data["error"] is None
        assert data["error_stage"] is None
        assert data["script"] is None

    def test_with_scenes(self):
        scenes = [
            Scene(index=0, narration_text="Hello", visual_description="A sunrise"),
            Scene(index=1, narration_text="World", visual_description="A sunset"),
        ]
        job = _make_job(scenes=scenes)
        data = _serialize_job(job)
        assert len(data["script"]) == 2
        assert data["script"][0] == {
            "index": 0,
            "narration_text": "Hello",
            "visual_description": "A sunrise",
        }

    def test_with_error(self):
        job = _make_job(
            stage=JobStage.ERROR,
            error="TTS failed",
            error_stage=JobStage.TTS_SYNTHESIS,
        )
        data = _serialize_job(job)
        assert data["status"] == "error"
        assert data["error"] == "TTS failed"
        assert data["error_stage"] == "tts_synthesis"


class TestSaveJobMetadata:
    def test_writes_job_json(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        job = _make_job()
        save_job_metadata(job)

        path = tmp_path / "output" / "test-job-1" / "job.json"
        assert path.exists()
        data = json.loads(path.read_text())
        assert data["job_id"] == "test-job-1"
        assert data["prompt"] == "A cat on the moon"

    def test_creates_directory(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        job = _make_job(job_id="new-dir-job")
        save_job_metadata(job)

        assert (tmp_path / "output" / "new-dir-job" / "job.json").exists()

    def test_overwrites_existing(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        job = _make_job()
        save_job_metadata(job)
        job.stage = JobStage.COMPLETE
        save_job_metadata(job)

        data = json.loads(
            (tmp_path / "output" / "test-job-1" / "job.json").read_text()
        )
        assert data["status"] == "complete"

    def test_best_effort_no_raise(self):
        """Write failure should be logged, not raised."""
        job = _make_job()
        with patch("app.job_persistence.Path.write_text", side_effect=OSError("disk full")):
            # Should not raise
            save_job_metadata(job)


class TestUpdateJobMetadata:
    def test_sets_updated_at(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        job = _make_job()
        assert job.updated_at is None
        update_job_metadata(job)

        assert job.updated_at is not None
        assert job.updated_at.endswith("Z")

        data = json.loads(
            (tmp_path / "output" / "test-job-1" / "job.json").read_text()
        )
        assert data["updated_at"] == job.updated_at

    def test_best_effort_no_raise(self):
        """Write failure should be logged, not raised."""
        job = _make_job()
        with patch("app.job_persistence.Path.write_text", side_effect=OSError("disk full")):
            # Should not raise
            update_job_metadata(job)


def _write_job_json(tmp_path, job_id: str, data: dict) -> Path:
    """Helper to write a job.json file under output/{job_id}/."""
    job_dir = tmp_path / "output" / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    path = job_dir / "job.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _valid_job_data(job_id: str = "test-job-1") -> dict:
    return {
        "job_id": job_id,
        "prompt": "A cat on the moon",
        "video_length": "30s",
        "aspect_ratio": "16:9",
        "status": "script_generation",
        "created_at": "2025-01-15T10:30:00Z",
        "updated_at": None,
        "error": None,
        "error_stage": None,
        "script": None,
    }


class TestLoadJobMetadata:
    def test_loads_valid_file(self, tmp_path):
        data = _valid_job_data("job-1")
        path = _write_job_json(tmp_path, "job-1", data)
        result = load_job_metadata(path)
        assert result is not None
        assert result["job_id"] == "job-1"

    def test_returns_none_for_missing_file(self, tmp_path):
        path = tmp_path / "output" / "missing" / "job.json"
        result = load_job_metadata(path)
        assert result is None

    def test_returns_none_for_invalid_json(self, tmp_path):
        job_dir = tmp_path / "output" / "bad-json"
        job_dir.mkdir(parents=True)
        path = job_dir / "job.json"
        path.write_text("not valid json {{{", encoding="utf-8")
        result = load_job_metadata(path)
        assert result is None

    def test_returns_none_for_missing_required_fields(self, tmp_path):
        data = {"job_id": "incomplete"}  # missing prompt, video_length, etc.
        path = _write_job_json(tmp_path, "incomplete", data)
        result = load_job_metadata(path)
        assert result is None

    def test_returns_none_for_non_dict_json(self, tmp_path):
        job_dir = tmp_path / "output" / "array-json"
        job_dir.mkdir(parents=True)
        path = job_dir / "job.json"
        path.write_text("[1, 2, 3]", encoding="utf-8")
        result = load_job_metadata(path)
        assert result is None

    def test_loads_file_with_script(self, tmp_path):
        data = _valid_job_data()
        data["script"] = [
            {"index": 0, "narration_text": "Hello", "visual_description": "A sunrise"},
        ]
        path = _write_job_json(tmp_path, "with-script", data)
        result = load_job_metadata(path)
        assert result is not None
        assert len(result["script"]) == 1

    def test_loads_file_with_error(self, tmp_path):
        data = _valid_job_data()
        data["status"] = "error"
        data["error"] = "Something broke"
        data["error_stage"] = "tts_synthesis"
        path = _write_job_json(tmp_path, "with-error", data)
        result = load_job_metadata(path)
        assert result is not None
        assert result["error"] == "Something broke"


class TestRestoreJobsFromDisk:
    def test_restores_valid_jobs(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        _write_job_json(tmp_path, "job-a", _valid_job_data("job-a"))
        _write_job_json(tmp_path, "job-b", _valid_job_data("job-b"))

        store: dict[str, Job] = {}
        restore_jobs_from_disk(store)
        assert len(store) == 2
        assert "job-a" in store
        assert "job-b" in store

    def test_reconstructed_job_has_correct_fields(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        data = _valid_job_data("job-x")
        data["script"] = [
            {"index": 0, "narration_text": "Narration", "visual_description": "Visual"},
        ]
        _write_job_json(tmp_path, "job-x", data)

        store: dict[str, Job] = {}
        restore_jobs_from_disk(store)
        job = store["job-x"]
        assert job.job_id == "job-x"
        assert job.request.prompt == "A cat on the moon"
        assert job.request.video_length == VideoLength.THIRTY
        assert job.request.aspect_ratio == AspectRatio.HORIZONTAL
        assert job.stage == JobStage.SCRIPT_GENERATION
        assert len(job.scenes) == 1
        assert job.scenes[0].narration_text == "Narration"
        assert job.created_at == "2025-01-15T10:30:00Z"

    def test_skips_invalid_json(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        # Write one valid and one invalid
        _write_job_json(tmp_path, "good", _valid_job_data("good"))
        bad_dir = tmp_path / "output" / "bad"
        bad_dir.mkdir(parents=True)
        (bad_dir / "job.json").write_text("not json!", encoding="utf-8")

        store: dict[str, Job] = {}
        restore_jobs_from_disk(store)
        assert len(store) == 1
        assert "good" in store

    def test_skips_dirs_without_job_json(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        # Directory exists but no job.json
        (tmp_path / "output" / "empty-dir").mkdir(parents=True)
        _write_job_json(tmp_path, "valid", _valid_job_data("valid"))

        store: dict[str, Job] = {}
        restore_jobs_from_disk(store)
        assert len(store) == 1
        assert "valid" in store

    def test_no_output_dir(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        store: dict[str, Job] = {}
        restore_jobs_from_disk(store)
        assert len(store) == 0

    def test_restores_error_job(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        data = _valid_job_data("err-job")
        data["status"] = "error"
        data["error"] = "TTS failed"
        data["error_stage"] = "tts_synthesis"
        _write_job_json(tmp_path, "err-job", data)

        store: dict[str, Job] = {}
        restore_jobs_from_disk(store)
        job = store["err-job"]
        assert job.stage == JobStage.ERROR
        assert job.error == "TTS failed"
        assert job.error_stage == JobStage.TTS_SYNTHESIS

    def test_skips_missing_required_fields(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        incomplete = {"job_id": "incomplete"}
        _write_job_json(tmp_path, "incomplete", incomplete)

        store: dict[str, Job] = {}
        restore_jobs_from_disk(store)
        assert len(store) == 0
