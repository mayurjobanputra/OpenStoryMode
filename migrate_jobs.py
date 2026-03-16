"""One-time migration: generate job.json for existing output directories."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def migrate():
    output_dir = Path("output")
    if not output_dir.exists():
        print("No output directory found.")
        return

    migrated = 0
    skipped = 0

    for job_dir in sorted(output_dir.iterdir()):
        if not job_dir.is_dir():
            continue

        job_json = job_dir / "job.json"
        if job_json.exists():
            skipped += 1
            continue

        job_id = job_dir.name
        script = None
        script_path = job_dir / "script.json"
        if script_path.exists():
            try:
                script = json.loads(script_path.read_text())
            except Exception:
                pass

        has_video = (job_dir / "output.mp4").exists()

        # Determine status
        if has_video:
            status = "complete"
        elif script:
            status = "error"  # had script but no video — likely failed mid-pipeline
        else:
            status = "error"

        # Use directory mtime as a rough timestamp
        mtime = os.path.getmtime(str(job_dir))
        created_at = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat().replace("+00:00", "Z")

        data = {
            "job_id": job_id,
            "prompt": "(migrated — original prompt unavailable)",
            "video_length": "30s",
            "aspect_ratio": "16:9",
            "status": status,
            "created_at": created_at,
            "updated_at": created_at,
            "error": None if has_video else "Pre-migration job — status inferred",
            "error_stage": None if has_video else "script_generation",
            "script": script,
        }

        job_json.write_text(json.dumps(data, indent=2))
        migrated += 1
        print(f"  Migrated: {job_id} -> {status}")

    print(f"\nDone. Migrated: {migrated}, Skipped (already had job.json): {skipped}")


if __name__ == "__main__":
    migrate()
