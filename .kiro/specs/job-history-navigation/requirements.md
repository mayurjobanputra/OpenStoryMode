# Requirements Document

## Introduction

This feature adds job history persistence and app navigation to OpenStoryMode. Currently, the app is a single-page form that loses all job history when the server restarts and provides no way to view past jobs. This feature introduces filesystem-based job metadata persistence (via `job.json` files in each job's output directory), a navigation bar for switching between views, and a Jobs view that displays all past and in-progress jobs with their status, prompts, scripts, and results.

## Glossary

- **App**: The OpenStoryMode web application consisting of a FastAPI backend and vanilla HTML/JS frontend.
- **Navigation_Bar**: A persistent UI element at the top of the App that allows users to switch between views.
- **Create_Video_View**: The view containing the prompt input form for generating new videos (the current main UI).
- **Jobs_View**: The view displaying a list of all past and in-progress jobs with their details.
- **Job_Metadata**: A JSON object containing a job's prompt, video length, aspect ratio, status, timestamps, error details, and generated script, persisted as `job.json` in the job's output directory.
- **Job_Card**: A UI element in the Jobs_View representing a single job with its details and status.
- **Pipeline**: The backend video generation pipeline that processes a job through script generation, visual generation, TTS synthesis, and video assembly stages.
- **Generated_Script**: The LLM-produced scene breakdown (list of scenes with narration text and visual descriptions) created during the script generation stage of the Pipeline.
- **Job_Store**: The in-memory dictionary of Job objects maintained by the backend server.

## Requirements

### Requirement 1: Job Metadata Persistence

**User Story:** As a user, I want my job history to survive server restarts, so that I can review past video generations without losing them.

#### Acceptance Criteria

1. WHEN the Pipeline completes the script generation stage for a job, THE App SHALL write a `job.json` file to the `output/{job_id}/` directory containing the original prompt, video length, aspect ratio, current status, a created-at timestamp, and the Generated_Script.
2. WHEN the Pipeline transitions a job to a new stage, THE App SHALL update the `job.json` file in the `output/{job_id}/` directory with the current status and an updated-at timestamp.
3. WHEN the Pipeline completes a job successfully, THE App SHALL update the `job.json` file with a status of "complete" and the final updated-at timestamp.
4. WHEN the Pipeline encounters an error for a job, THE App SHALL update the `job.json` file with a status of "error", the error message, the stage at which the error occurred, and an updated-at timestamp.
5. THE Job_Metadata file SHALL contain the following fields: `job_id`, `prompt`, `video_length`, `aspect_ratio`, `status`, `created_at`, `updated_at`, `error` (nullable), `error_stage` (nullable), and `script` (list of scene objects with index, narration_text, and visual_description).

### Requirement 2: Job History Restoration on Startup

**User Story:** As a user, I want the app to restore my job history when the server starts, so that I can see all my previous jobs immediately.

#### Acceptance Criteria

1. WHEN the App server starts, THE App SHALL scan all `output/*/job.json` files and load each valid Job_Metadata into the Job_Store.
2. WHEN the App server starts and a `job.json` file contains invalid or unparseable JSON, THE App SHALL log a warning with the file path and skip that file without preventing startup.
3. WHEN the App server starts and a job directory exists without a `job.json` file, THE App SHALL skip that directory without error.
4. WHEN the App server completes the startup scan, THE Job_Store SHALL contain one entry for each valid `job.json` file found, keyed by job_id.

### Requirement 3: List Jobs API Endpoint

**User Story:** As a frontend developer, I want an API endpoint that returns all jobs, so that the Jobs_View can display the full job history.

#### Acceptance Criteria

1. THE App SHALL expose a `GET /api/jobs` endpoint that returns a JSON array of all jobs in the Job_Store.
2. WHEN the `GET /api/jobs` endpoint is called, THE App SHALL return each job with the fields: `job_id`, `prompt`, `video_length`, `aspect_ratio`, `status`, `stage`, `progress_pct`, `created_at`, `updated_at`, `error` (nullable), `error_stage` (nullable), `script` (nullable), and `video_url` (nullable).
3. THE App SHALL sort the jobs array by `created_at` in descending order so that the most recent job appears first.

### Requirement 4: Navigation Bar

**User Story:** As a user, I want a navigation bar so that I can switch between creating videos and viewing my job history.

#### Acceptance Criteria

1. THE Navigation_Bar SHALL be displayed at the top of every view in the App.
2. THE Navigation_Bar SHALL contain at minimum three items: "Create Video", "Jobs", and "GitHub".
3. WHEN the user clicks "Create Video" in the Navigation_Bar, THE App SHALL display the Create_Video_View and hide other views.
4. WHEN the user clicks "Jobs" in the Navigation_Bar, THE App SHALL display the Jobs_View and hide other views.
5. WHEN the user clicks "GitHub" in the Navigation_Bar, THE App SHALL open the URL `https://github.com/mayurjobanputra/OpenStoryMode` in a new browser tab.
6. THE Navigation_Bar SHALL visually indicate which view is currently active by highlighting the corresponding navigation item.

### Requirement 5: Jobs View

**User Story:** As a user, I want to see a list of all my past and current jobs, so that I can track progress and access completed videos.

#### Acceptance Criteria

1. WHEN the Jobs_View is displayed, THE App SHALL fetch the job list from `GET /api/jobs` and render a Job_Card for each job.
2. THE Job_Card SHALL display the original user prompt text.
3. THE Job_Card SHALL display the Generated_Script (scene breakdown with narration text and visual descriptions) when available.
4. THE Job_Card SHALL display the current job status as one of: "In Progress", "Complete", or "Error".
5. WHILE a job has a status of "In Progress", THE Job_Card SHALL display a progress indicator showing the current pipeline stage and progress percentage.
6. WHILE a job has a status of "In Progress", THE App SHALL poll the `GET /api/status/{job_id}` endpoint and update the Job_Card progress indicator.
7. WHEN a job has a status of "Complete", THE Job_Card SHALL display an inline video player and a download button for the generated video.
8. WHEN a job has a status of "Error", THE Job_Card SHALL display the error message and the pipeline stage at which the error occurred.
9. WHEN the Jobs_View contains no jobs, THE App SHALL display a message indicating no jobs exist and suggest creating a video.

### Requirement 6: Post-Submit Redirect to Jobs View

**User Story:** As a user, I want to be taken to the Jobs view after submitting a video generation request, so that I can monitor progress alongside my other jobs.

#### Acceptance Criteria

1. WHEN the user submits a video generation request via the Create_Video_View and the `POST /api/generate` endpoint returns a successful response, THE App SHALL switch the active view to the Jobs_View.
2. WHEN the App switches to the Jobs_View after submission, THE App SHALL refresh the job list so the newly created job is visible.
3. WHEN the App switches to the Jobs_View after submission, THE Create_Video_View form SHALL be reset to its default state.

### Requirement 7: Job Metadata Includes Created-At Timestamp

**User Story:** As a user, I want to know when each job was created, so that I can identify jobs by their creation time.

#### Acceptance Criteria

1. WHEN a new Job is created via the `POST /api/generate` endpoint, THE App SHALL record an ISO 8601 `created_at` timestamp on the Job object.
2. THE `created_at` timestamp SHALL be persisted in the `job.json` file and returned by the `GET /api/jobs` and `GET /api/status/{job_id}` endpoints.
