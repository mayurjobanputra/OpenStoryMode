# Implementation Plan: Job Page Routing

## Overview

Introduce client-side History API routing to the OpenStoryMode SPA, add backend catch-all routes for direct URL access, redesign the jobs list as a multi-column card grid, and create a dedicated two-column job detail page. Implementation proceeds backend-first, then client-side router, then view refactoring, then wiring and integration.

## Tasks

- [x] 1. Add backend catch-all SPA routes
  - [x] 1.1 Add explicit FastAPI GET routes for `/`, `/jobs`, and `/job/{job_id}` that return `static/index.html` as a `FileResponse`
    - Register these routes **before** the `app.mount("/", StaticFiles(...))` call so they take priority
    - Ensure `/api/*` routes and static asset serving remain unaffected
    - _Requirements: 2.1, 2.2_

  - [ ]* 1.2 Write pytest tests for backend catch-all routes
    - Verify GET `/`, `/jobs`, `/job/some-id` all return 200 with `text/html` content type
    - Verify GET `/api/jobs` still returns JSON (not HTML)
    - Verify GET `/api/status/{job_id}` still returns JSON
    - _Requirements: 2.1, 2.2_

  - [ ]* 1.3 Write property test for backend catch-all (Property 4)
    - **Property 4: Backend catch-all serves index.html**
    - Generate random `job_id` strings, send GET `/job/{job_id}`, verify HTML response with 200 status
    - Also verify GET `/` and GET `/jobs` return HTML
    - Use `hypothesis` library
    - **Validates: Requirements 2.1**

- [x] 2. Checkpoint — Ensure backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 3. Implement client-side Router module
  - [x] 3.1 Create the Router object in `static/index.html`
    - Implement `Router.init()`, `Router.navigate(path)`, `Router._dispatch(path)`, `Router._onPopState(event)`
    - Define route table: `/` → `showCreateVideoView()`, `/jobs` → `showJobsListView()`, `/job/:job_id` → `showJobDetailView(jobId)`
    - Unknown routes redirect to `/`
    - `Router.navigate()` uses `history.pushState()` and calls `_dispatch()`
    - `_onPopState` calls `_dispatch(window.location.pathname)`
    - Call `Router.init()` on DOMContentLoaded
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x] 3.2 Update Navigation Bar to use Router
    - Change nav link `href` attributes to `/` and `/jobs`
    - Click handlers call `event.preventDefault()` then `Router.navigate(path)`
    - Active nav item highlight is set in `_dispatch()` based on `window.location.pathname`
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 4. Implement Jobs List View — multi-column card grid
  - [x] 4.1 Add Jobs List View HTML section and CSS grid layout
    - Add a `<section id="jobs-list-view">` container with a `.jobs-grid` CSS grid
    - Grid uses `repeat(auto-fill, minmax(280px, 1fr))` for responsive multi-column layout
    - Single column on narrow viewports via CSS (no media query needed with auto-fill)
    - _Requirements: 4.2_

  - [x] 4.2 Implement `showJobsListView()` function
    - Fetch jobs from `GET /api/jobs`, render a Job_Summary_Card for each job
    - Each card shows: prompt text (truncated via CSS `line-clamp`), status badge ("In Progress" / "Complete" / "Error"), "View Details" button linking to `/job/{job_id}`
    - Display "No jobs yet" message with link to create a video when list is empty
    - Stop any active polling timers when entering this view
    - _Requirements: 4.1, 4.3, 4.4, 4.5, 4.6_

- [x] 5. Implement Job Detail View — two-column layout
  - [x] 5.1 Add Job Detail View HTML section and two-column CSS layout
    - Add a `<section id="job-detail-view">` with a `.job-detail` CSS grid (`1fr 1fr`, collapses to `1fr` at 768px)
    - Left column: prompt, metadata (video length, aspect ratio, created_at, status), progress indicator area, error area
    - Right column: video player area, download button area
    - _Requirements: 5.2, 5.3_

  - [x] 5.2 Implement `showJobDetailView(jobId)` function
    - Fetch job data from `GET /api/status/{job_id}`
    - Render left column: prompt text, metadata fields (video length, aspect ratio, creation timestamp, status)
    - If status is "in_progress": show pipeline stage name and progress percentage, start polling `GET /api/status/{job_id}` to update display
    - If status is "error": show error message and error stage
    - If status is "complete": show `<video>` element with `autoplay` disabled and a download button in the right column
    - If job not found (404): show error message with link back to `/jobs`
    - Stop polling when navigating away from this view
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10_

- [x] 6. Wire post-submit navigation
  - [x] 6.1 Update the form submit handler to use Router
    - After successful `POST /api/generate` response, call `Router.navigate('/jobs')` instead of manual view toggling
    - Reset the form fields to defaults (prompt empty, video length "30s", aspect ratio "9:16")
    - _Requirements: 6.1, 6.2, 6.3_

- [x] 7. Checkpoint — Ensure all views work end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ]* 8. Write property-based tests for client-side router logic
  - [ ]* 8.1 Write property test for route parameter extraction (Property 1)
    - **Property 1: Route parameter extraction**
    - Generate random `job_id` strings, verify router path matching extracts the correct `job_id` from `/job/{job_id}`
    - Use `fast-check` library
    - **Validates: Requirements 1.3**

  - [ ]* 8.2 Write property test for unknown route fallback (Property 3)
    - **Property 3: Unknown route fallback**
    - Generate random path strings that don't match `/`, `/jobs`, or `/job/{id}`, verify router redirects to `/`
    - Use `fast-check` library
    - **Validates: Requirements 1.6**

  - [ ]* 8.3 Write property test for nav bar active state (Property 5)
    - **Property 5: Nav bar active state matches current route**
    - Generate random valid route paths, verify exactly one nav item has the `active` class and it matches the current path
    - Use `fast-check` library
    - **Validates: Requirements 3.3, 3.4**

  - [ ]* 8.4 Write property test for job summary card rendering (Property 6)
    - **Property 6: Job summary card contains required elements**
    - Generate random job objects (id, prompt, status), verify rendered card contains prompt text, correct status badge, and "View Details" link with correct href
    - Use `fast-check` library
    - **Validates: Requirements 4.1, 4.4, 4.5**

  - [ ]* 8.5 Write property test for job detail view rendering (Property 7)
    - **Property 7: Job detail view renders all job information**
    - Generate random job objects with all metadata fields, verify detail view renders prompt and all metadata in the left column
    - Use `fast-check` library
    - **Validates: Requirements 5.2, 5.3**

  - [ ]* 8.6 Write property test for status-specific detail rendering (Property 8)
    - **Property 8: Status-specific detail rendering**
    - Generate random job objects with each status type, verify correct status-specific content is rendered (progress for in-progress, error info for error, video player for complete)
    - Use `fast-check` library
    - **Validates: Requirements 5.4, 5.5, 5.6, 5.7, 5.8**

  - [ ]* 8.7 Write property test for form reset after submission (Property 9)
    - **Property 9: Form reset after submission**
    - Generate random form states, simulate submission and navigation, verify form resets to defaults (empty prompt, "30s" video length, "9:16" aspect ratio)
    - Use `fast-check` library
    - **Validates: Requirements 6.3**

- [x] 9. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- The backend uses Python/FastAPI; the frontend is vanilla HTML/JS — no framework dependencies
- Property tests use `hypothesis` (Python) for backend and `fast-check` (JavaScript) for frontend
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
