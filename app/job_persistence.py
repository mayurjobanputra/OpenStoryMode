"""Job metadata persistence — writes and reads job.json files."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.models import (
    AspectRatio,
    GenerationRequest,
    Job,
    JobStage,
    Scene,
    VideoLength,
)

logger = logging.getLogger(__name__)


def _serialize_job(job: Job) -> dict:
    """Serialize a Job to a dict suitable for job.json."""
    script = None
    if job.scenes:
        script = [
            {
                "index": s.index,
                "narration_text": s.narration_text,
                "visual_description": s.visual_description,
            }
            for s in job.scenes
        ]

    return {
        "job_id": job.job_id,
        "prompt": job.request.prompt if job.request else None,
        "video_length": job.request.video_length.value if job.request else None,
        "aspect_ratio": job.request.aspect_ratio.value if job.request else None,
        "status": job.stage.value,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "error": job.error,
        "error_stage": job.error_stage.value if job.error_stage else None,
        "script": script,
    }


def _job_json_path(job_id: str) -> Path:
    return Path(f"output/{job_id}/job.json")


def save_job_metadata(job: Job) -> None:
    """Write the full job.json to output/{job_id}/job.json.

    Best-effort: logs errors but never raises.
    """
    try:
        path = _job_json_path(job.job_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = _serialize_job(job)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        logger.exception("Failed to save job metadata for %s", job.job_id)


def update_job_metadata(job: Job) -> None:
    """Update job.json with current state, setting updated_at to now.

    Best-effort: logs errors but never raises.
    """
    try:
        job.updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        save_job_metadata(job)
    except Exception:
        logger.exception("Failed to update job metadata for %s", job.job_id)


# Required fields that must be present in a valid job.json
_REQUIRED_FIELDS = {"job_id", "prompt", "video_length", "aspect_ratio", "status", "created_at"}


def load_job_metadata(path: Path) -> Optional[dict]:
    """Read and parse a single job.json file.

    Returns the parsed dict on success, or None on any failure
    (missing file, invalid JSON, missing required fields).
    """
    try:
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
        if not isinstance(data, dict):
            logger.warning("job.json is not a JSON object: %s", path)
            return None
        missing = _REQUIRED_FIELDS - data.keys()
        if missing:
            logger.warning("job.json missing required fields %s: %s", missing, path)
            return None
        return data
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Failed to load job metadata from %s: %s", path, exc)
        return None


def _reconstruct_job(data: dict) -> Job:
    """Reconstruct a Job object from a parsed job.json dict."""
    # Reconstruct GenerationRequest
    request = GenerationRequest(
        prompt=data["prompt"],
        video_length=VideoLength(data["video_length"]),
        aspect_ratio=AspectRatio(data["aspect_ratio"]),
    )

    # Map status string to JobStage enum
    stage = JobStage(data["status"])

    # Reconstruct scenes from script array
    scenes: list[Scene] = []
    if data.get("script"):
        for s in data["script"]:
            scenes.append(
                Scene(
                    index=s["index"],
                    narration_text=s["narration_text"],
                    visual_description=s["visual_description"],
                )
            )

    # Map error_stage string to JobStage if present
    error_stage = JobStage(data["error_stage"]) if data.get("error_stage") else None

    return Job(
        job_id=data["job_id"],
        request=request,
        stage=stage,
        scenes=scenes,
        error=data.get("error"),
        error_stage=error_stage,
        created_at=data["created_at"],
        updated_at=data.get("updated_at"),
    )


def restore_jobs_from_disk(jobs_store: dict[str, Job]) -> None:
    """Scan output/*/job.json, parse each, and populate jobs_store.

    Invalid or unparseable files are logged and skipped.
    Directories without job.json are silently skipped.
    """
    output_dir = Path("output")
    if not output_dir.exists():
        logger.info("No output directory found; skipping job restoration.")
        return

    for job_json_path in sorted(output_dir.glob("*/job.json")):
        data = load_job_metadata(job_json_path)
        if data is None:
            continue
        try:
            job = _reconstruct_job(data)
            jobs_store[job.job_id] = job
        except Exception:
            logger.warning("Failed to reconstruct job from %s", job_json_path, exc_info=True)
