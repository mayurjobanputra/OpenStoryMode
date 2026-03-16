# Requirements Document

## Introduction

This feature adds client-side URL routing to the OpenStoryMode single-page application. Currently, the app uses a tab-based navigation model with no URL changes — all views share the same `/` URL. This feature introduces hash-based or History API routing so that the jobs listing lives at `/jobs`, individual job detail pages live at `/job/{job_id}`, and the create video form remains at `/`. It also redesigns the jobs listing into a multi-column card grid showing only the prompt and a "View Details" button, and introduces a dedicated two-column job detail page with prompt/details on the left and video playback (no autoplay) on the right.

## Glossary

- **App**: The OpenStoryMode web application consisting of a FastAPI backend and vanilla HTML/JS frontend.
- **Router**: The client-side JavaScript component that maps URL paths to views and handles browser navigation events (popstate, link clicks).
- **Jobs_List_View**: The view at `/jobs` displaying all jobs as a multi-column grid of summary cards.
- **Job_Detail_View**: The view at `/job/{job_id}` displaying full details for a single job in a two-column layout.
- **Create_Video_View**: The existing view at `/` containing the prompt input form for generating new videos.
- **Job_Summary_Card**: A compact card in the Jobs_List_View showing only the job prompt and a button to navigate to the Job_Detail_View.
- **Navigation_Bar**: The persistent top navigation bar that allows switching between views.
- **Video_Player**: The HTML5 video element on the Job_Detail_View that plays the generated video without autoplay.

## Requirements

### Requirement 1: Client-Side URL Routing

**User Story:** As a user, I want the browser URL to reflect which page I am viewing, so that I can bookmark, share, and use browser back/forward navigation.

#### Acceptance Criteria

1. WHEN the user navigates to `/`, THE Router SHALL display the Create_Video_View.
2. WHEN the user navigates to `/jobs`, THE Router SHALL display the Jobs_List_View.
3. WHEN the user navigates to `/job/{job_id}`, THE Router SHALL display the Job_Detail_View for the specified job.
4. WHEN the user clicks a navigation link or in-app link, THE Router SHALL update the browser URL using the History API without a full page reload.
5. WHEN the user presses the browser back or forward button, THE Router SHALL display the view corresponding to the new URL.
6. WHEN the user navigates to an unrecognized URL path, THE Router SHALL redirect to `/`.

### Requirement 2: Backend Catch-All Route for SPA

**User Story:** As a user, I want to be able to directly load any app URL in the browser, so that bookmarked or shared links work correctly.

#### Acceptance Criteria

1. WHEN the Backend receives a GET request for `/jobs`, `/job/{job_id}`, or `/`, THE Backend SHALL serve the `index.html` file.
2. THE Backend SHALL continue to serve API routes (`/api/*`) and static assets (CSS, JS, images) at their existing paths without interference from the catch-all route.

### Requirement 3: Navigation Bar URL Integration

**User Story:** As a user, I want the navigation bar to update the URL when I switch views, so that the URL always reflects my current location.

#### Acceptance Criteria

1. WHEN the user clicks "Create Video" in the Navigation_Bar, THE Router SHALL navigate to `/`.
2. WHEN the user clicks "Jobs" in the Navigation_Bar, THE Router SHALL navigate to `/jobs`.
3. THE Navigation_Bar SHALL highlight the active navigation item based on the current URL path.
4. WHEN the URL changes via browser navigation, THE Navigation_Bar SHALL update the active highlight to match the current path.

### Requirement 4: Jobs List View — Multi-Column Card Grid

**User Story:** As a user, I want to see my jobs as a compact multi-column grid of cards, so that I can quickly scan many jobs at once.

#### Acceptance Criteria

1. WHEN the Jobs_List_View is displayed, THE App SHALL fetch the job list from `GET /api/jobs` and render a Job_Summary_Card for each job.
2. THE Jobs_List_View SHALL arrange Job_Summary_Cards in a responsive multi-column grid layout (minimum two columns on desktop viewports, single column on narrow viewports).
3. THE Job_Summary_Card SHALL display the job prompt text, truncated with an ellipsis if the text exceeds the card height.
4. THE Job_Summary_Card SHALL display a status badge indicating the current job status ("In Progress", "Complete", or "Error").
5. THE Job_Summary_Card SHALL display a "View Details" button that navigates to `/job/{job_id}`.
6. WHEN the Jobs_List_View contains no jobs, THE App SHALL display a message indicating no jobs exist.

### Requirement 5: Job Detail View — Two-Column Layout

**User Story:** As a user, I want a dedicated page for each job showing full details and the video, so that I can review the generation results in detail.

#### Acceptance Criteria

1. WHEN the Job_Detail_View is displayed, THE App SHALL fetch the job data from `GET /api/status/{job_id}` and render the two-column layout.
2. THE Job_Detail_View left column SHALL display the original prompt text.
3. THE Job_Detail_View left column SHALL display the job metadata including video length, aspect ratio, creation timestamp, and current status.
4. WHILE the job has a status of "In Progress", THE Job_Detail_View left column SHALL display a progress indicator showing the current pipeline stage and progress percentage.
5. WHEN the job has a status of "Error", THE Job_Detail_View left column SHALL display the error message and the pipeline stage at which the error occurred.
6. WHEN the job has a status of "Complete", THE Job_Detail_View right column SHALL display the Video_Player with the generated video loaded.
7. THE Video_Player SHALL have autoplay disabled and require the user to manually initiate playback.
8. WHEN the job has a status of "Complete", THE Job_Detail_View right column SHALL display a download button for the video file.
9. WHILE the job has a status of "In Progress", THE Job_Detail_View SHALL poll the `GET /api/status/{job_id}` endpoint and update the displayed information.
10. IF the Router navigates to `/job/{job_id}` and the job does not exist, THEN THE App SHALL display an error message and provide a link back to `/jobs`.

### Requirement 6: Post-Submit Navigation

**User Story:** As a user, I want to be taken to the Jobs page after submitting a video generation request, so that I can monitor progress.

#### Acceptance Criteria

1. WHEN the user submits a video generation request and the `POST /api/generate` endpoint returns a successful response, THE Router SHALL navigate to `/jobs`.
2. WHEN the Router navigates to `/jobs` after submission, THE Jobs_List_View SHALL refresh the job list so the newly created job is visible.
3. WHEN the Router navigates to `/jobs` after submission, THE Create_Video_View form SHALL be reset to its default state.
