# Implementation Plan: Job History Navigation

## Overview

Add job metadata persistence, startup restoration, a list-jobs API endpoint, a navigation bar, a Jobs view, and post-submit redirect to the OpenStoryMode app. Backend changes are additive (new persistence module, new endpoint, startup scan, model updates). Frontend changes restructure the single-page app into a multi-view SPA with client-side nav.

## Tasks

- [x] 1. Add timestamp fields to Job model and update status endpoint
  - [x] 1.1 Add `created_at` and `updated_at` fields to the `Job` dataclass in `app/models.py`
    - Add `created_at: str` with default factory `datetime.utcnow().isoformat() + "Z"`
    - Add `updated_at: Optional[str] = None`
    - Import `datetime` from the standard library
    - _Requirements: 7.1, 1.5_

  - [x] 1.2 Update `GET /api/status/{job_id}` in `app/main.py` to include `created_at`, `updated_at`, `prompt`, `video_length`, and `aspect_ratio` in the response
    - Add the new fields to the response dict
    - _Requirements: 7.2, 3.2_

  - [ ]* 1.3 Write property test: created_at is valid ISO 8601
    - **Property 5: Job created_at is valid ISO 8601**
    - Generate random Job objects, verify `created_at` parses as ISO 8601 datetime
    - **Validates: Requirements 7.1**

- [x] 2. Implement job persistence module (`app/job_persistence.py`)
  - [x] 2.1 Create `app/job_persistence.py` with `save_job_metadata(job)` and `update_job_metadata(job)` functions
    - Serialize job fields (job_id, prompt, video_length, aspect_ratio, status, created_at, updated_at, error, error_stage, script) to JSON
    - Write to `output/{job_id}/job.json`
    - `update_job_metadata` should set `updated_at` to current UTC timestamp before writing
    - Use best-effort writes: log errors but do not raise exceptions
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [x] 2.2 Implement `load_job_metadata(path)` and `restore_jobs_from_disk(jobs_store)` functions in `app/job_persistence.py`
    - `load_job_metadata` reads and parses a single `job.json`, returns `None` on failure
    - `restore_jobs_from_disk` globs `output/*/job.json`, calls `load_job_metadata` for each, populates `jobs_store` dict
    - Log warnings for invalid/unparseable files, skip directories without `job.json`
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ]* 2.3 Write property test: job metadata serialization round-trip
    - **Property 1: Job metadata serialization round-trip**
    - Generate random Job objects with varied statuses, prompts, scripts. Serialize to `job.json`, read back, verify all fields match.
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 7.2**

  - [ ]* 2.4 Write property test: restore from disk populates job store
    - **Property 2: Restore from disk populates job store with all valid files**
    - Generate random sets of valid job metadata dicts, write to temp directories, run restore, verify store count matches.
    - **Validates: Requirements 2.1, 2.4**

  - [ ]* 2.5 Write property test: invalid job.json files are skipped
    - **Property 3: Invalid job.json files are skipped without error**
    - Generate random invalid strings (not valid JSON, or JSON missing required keys). Write to job.json paths, run restore, verify no crash and no store entries.
    - **Validates: Requirements 2.2**

- [ ] 3. Integrate persistence into pipeline and startup
  - [x] 3.1 Modify `run_pipeline()` in `app/pipeline.py` to call persistence functions
    - Call `save_job_metadata(job)` after script generation completes (initial write with script)
    - Call `update_job_metadata(job)` on each subsequent stage transition (visual_generation, tts_synthesis, video_assembly)
    - Call `update_job_metadata(job)` on completion (status=complete)
    - Call `update_job_metadata(job)` on error (status=error with error details)
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [x] 3.2 Add startup restoration to `lifespan()` in `app/main.py`
    - Call `restore_jobs_from_disk(jobs)` after config validation, before yielding
    - Log the number of jobs restored
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [x] 3.3 Set `created_at` on Job creation in the `generate()` endpoint in `app/main.py`
    - Ensure the `created_at` timestamp is set when the Job is instantiated (already handled by default factory, but verify)
    - _Requirements: 7.1, 7.2_

- [x] 4. Checkpoint
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Add `GET /api/jobs` endpoint
  - [x] 5.1 Implement `GET /api/jobs` endpoint in `app/main.py`
    - Return JSON array of all jobs in the `jobs` store
    - Each entry includes: job_id, prompt, video_length, aspect_ratio, status, stage, progress_pct, created_at, updated_at, error, error_stage, script, video_url
    - Sort by `created_at` descending (newest first)
    - Return empty array when no jobs exist
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]* 5.2 Write property test: GET /api/jobs returns all jobs sorted descending
    - **Property 4: GET /api/jobs returns all jobs with required fields sorted by created_at descending**
    - Generate random sets of Job objects with distinct timestamps, populate the store, call the endpoint, verify response shape and sort order.
    - **Validates: Requirements 3.1, 3.2, 3.3**

  - [ ]* 5.3 Write unit tests for `GET /api/jobs` edge cases
    - Test empty store returns `[]`
    - Test single job returns correct fields
    - Test multiple jobs are sorted by created_at descending
    - _Requirements: 3.1, 3.2, 3.3_

- [x] 6. Implement navigation bar and multi-view structure in `static/index.html`
  - [x] 6.1 Replace the current `<header>` with a navigation bar
    - Add nav items: "Create Video", "Jobs", "GitHub"
    - "GitHub" links to `https://github.com/mayurjobanputra/OpenStoryMode` with `target="_blank"`
    - Visually highlight the active nav item
    - Style the nav bar to match the existing dark theme
    - _Requirements: 4.1, 4.2, 4.5, 4.6_

  - [x] 6.2 Wrap existing form/progress/result/error sections in a `<section id="create-video-view">` container
    - Add a `<section id="jobs-view" hidden>` container for the Jobs view
    - Implement view switching via `hidden` attribute toggling when nav items are clicked
    - _Requirements: 4.3, 4.4_

- [x] 7. Implement Jobs view frontend
  - [x] 7.1 Implement job list fetching and Job Card rendering in the Jobs view
    - Fetch `GET /api/jobs` when the Jobs view becomes active
    - Render a Job Card for each job showing: prompt text, script (scene breakdown) when available, status badge ("In Progress", "Complete", "Error")
    - Show empty state message with suggestion to create a video when no jobs exist
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.9_

  - [x] 7.2 Implement in-progress job polling, video playback, and error display in Job Cards
    - For "In Progress" jobs: show progress bar with stage name and percentage, poll `GET /api/status/{job_id}` to update
    - For "Complete" jobs: show inline `<video>` player and download button
    - For "Error" jobs: show error message and failed stage
    - _Requirements: 5.5, 5.6, 5.7, 5.8_

- [x] 8. Implement post-submit redirect to Jobs view
  - [x] 8.1 Modify the submit handler in `static/index.html` to redirect to Jobs view after successful `POST /api/generate`
    - Switch active view to Jobs view
    - Refresh the job list so the new job is visible
    - Reset the Create Video form to defaults
    - _Requirements: 6.1, 6.2, 6.3_

- [x] 9. Final checkpoint
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests use Hypothesis (already in requirements.txt)
- Backend is Python/FastAPI, frontend is vanilla HTML/JS in `static/index.html`
