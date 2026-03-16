# Implementation Plan: Graceful Missing API Key

## Overview

Transform the OpenStoryMode application to start gracefully when the OpenRouter API key is missing, instead of crashing. Changes span config, lifespan, routes, and frontend across four existing files.

## Tasks

- [x] 1. Update Config and remove crash behavior
  - [x] 1.1 Add `api_key_configured` property to `Config` dataclass in `app/config.py`
    - Add a `@property` that returns `True` iff `openrouter_api_key` is a non-empty, non-whitespace string
    - Modify `validate_config()` to log a warning instead of raising `ValueError`
    - _Requirements: 1.2, 1.3_

  - [ ]* 1.2 Write property test for `api_key_configured` flag (Property 1)
    - **Property 1: API key configured flag correctness**
    - Use Hypothesis `@given(text())` to generate random strings including empty and whitespace-only
    - Assert `Config(openrouter_api_key=s, port=8000).api_key_configured == bool(s and s.strip())`
    - Use `@settings(max_examples=100)`
    - **Validates: Requirements 1.2, 1.3**

  - [ ]* 1.3 Write unit tests for Config changes
    - Test empty string → `api_key_configured` is `False`
    - Test whitespace-only string → `api_key_configured` is `False`
    - Test valid key string → `api_key_configured` is `True`
    - _Requirements: 1.2, 1.3_

- [x] 2. Update lifespan handler and add health endpoint in `app/main.py`
  - [x] 2.1 Modify lifespan handler to replace crash with warning log
    - Remove or replace the `validate_config(config)` call
    - Check `config.api_key_configured`; if `False`, log a warning message and continue startup
    - _Requirements: 1.1, 1.4_

  - [x] 2.2 Add `GET /api/health` endpoint
    - Return `JSONResponse` with `{"api_key_configured": config.api_key_configured}`
    - Register the route before the static files mount
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [ ]* 2.3 Write property test for health endpoint (Property 3)
    - **Property 3: Health endpoint reflects config state**
    - Use Hypothesis `@given(booleans())` to generate random boolean values
    - Patch `config.api_key_configured` and call `GET /api/health`
    - Assert response JSON `api_key_configured` field matches the patched value
    - Use `@settings(max_examples=100)`
    - **Validates: Requirements 3.2, 3.3, 3.4**

  - [ ]* 2.4 Write unit tests for lifespan and health endpoint
    - Test app starts without crash when API key is missing (no `ValueError`)
    - Test `GET /api/health` returns `{"api_key_configured": true}` when key is set
    - Test `GET /api/health` returns `{"api_key_configured": false}` when key is missing
    - _Requirements: 1.1, 3.2, 3.3, 3.4_

- [x] 3. Add generation guard in `app/main.py`
  - [x] 3.1 Add 503 check at top of `generate()` handler
    - If `config.api_key_configured` is `False`, return `JSONResponse(status_code=503)` with `{"detail": "API key not configured. Set the OPENROUTER_API_KEY environment variable and restart the server."}`
    - Existing logic remains unchanged when key is configured
    - _Requirements: 2.1, 2.2_

  - [ ]* 3.2 Write property test for generate endpoint gating (Property 2)
    - **Property 2: Generate endpoint gating**
    - Use Hypothesis to generate valid prompts, video lengths, and aspect ratios
    - With `api_key_configured` patched to `False`, assert 503 response with correct message
    - With `api_key_configured` patched to `True`, assert 202 response
    - Use `@settings(max_examples=100)`
    - **Validates: Requirements 2.1, 2.2**

  - [ ]* 3.3 Write unit tests for generation guard
    - Test `POST /api/generate` returns 503 with correct JSON when key is missing
    - Test `POST /api/generate` returns 202 when key is present and request is valid
    - _Requirements: 2.1, 2.2_

- [x] 4. Checkpoint - Ensure all backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Add frontend banner and health check in `static/index.html`
  - [x] 5.1 Add API key banner HTML element and CSS styles
    - Add `<div id="api-key-banner" class="api-key-banner" role="alert" hidden>` with `<span id="api-key-banner-text">` inside `#create-video-view`, above `#form-section`
    - Add CSS for `.api-key-banner` with amber/yellow warning styling
    - _Requirements: 4.2, 4.3_

  - [x] 5.2 Add health check fetch on page load
    - On page load, `fetch('/api/health')` and inspect `api_key_configured`
    - If `false`: show banner with text "OpenRouter API key not configured. Set the OPENROUTER_API_KEY environment variable in your .env file and restart the server.", disable `#submit-btn`
    - If `true`: hide banner, ensure submit button is enabled
    - If fetch fails: show banner with fallback text "Unable to check server configuration."
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 6. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties from the design document
- All changes are in existing files: `app/config.py`, `app/main.py`, `static/index.html`, and test files under `tests/`
