# Requirements Document

## Introduction

When a new user clones the OpenStoryMode repository and starts the application without configuring an OpenRouter API key, the application currently crashes during startup. This feature changes that behavior so the application starts gracefully, serves the home page, disables video generation functionality, and displays a clear message guiding the user to configure their API key.

## Glossary

- **App**: The OpenStoryMode FastAPI application defined in `app/main.py`.
- **Config**: The application configuration dataclass in `app/config.py` that loads environment variables including the OpenRouter API key.
- **Lifespan_Handler**: The FastAPI async context manager in `app/main.py` that runs on application startup and currently calls `validate_config`.
- **Home_Page**: The static SPA served from `static/index.html` at the root URL `/`.
- **API_Key**: The `OPENROUTER_API_KEY` environment variable used to authenticate with the OpenRouter service.
- **Generation_Endpoint**: The `POST /api/generate` route that accepts video generation requests.
- **Health_Endpoint**: The `GET /api/health` route that reports application configuration status.
- **API_Key_Banner**: A visible UI element on the Home_Page that informs the user the API key is missing and functionality is disabled.

## Requirements

### Requirement 1: Graceful Startup Without API Key

**User Story:** As a new user, I want the App to start without crashing when no API_Key is configured, so that I can see the Home_Page and understand what to do next.

#### Acceptance Criteria

1. WHEN the API_Key environment variable is empty or unset, THE Lifespan_Handler SHALL log a warning message and continue startup without raising an exception.
2. WHEN the API_Key environment variable is empty or unset, THE Config SHALL set an `api_key_configured` flag to `false`.
3. WHEN the API_Key environment variable contains a non-empty value, THE Config SHALL set the `api_key_configured` flag to `true`.
4. THE App SHALL serve the Home_Page at the root URL regardless of whether the API_Key is configured.

### Requirement 2: Block Generation Requests When API Key Is Missing

**User Story:** As a new user without an API key, I want the App to reject generation requests with a clear error, so that I understand why video creation is unavailable.

#### Acceptance Criteria

1. WHILE the `api_key_configured` flag is `false`, THE Generation_Endpoint SHALL reject requests with HTTP status 503 and a JSON body containing the message "API key not configured. Set the OPENROUTER_API_KEY environment variable and restart the server."
2. WHILE the `api_key_configured` flag is `true`, THE Generation_Endpoint SHALL process requests normally.

### Requirement 3: Configuration Status Endpoint

**User Story:** As a frontend developer, I want an API endpoint that reports whether the API key is configured, so that the Home_Page can adapt its UI accordingly.

#### Acceptance Criteria

1. THE App SHALL expose a `GET /api/health` endpoint.
2. THE Health_Endpoint SHALL return a JSON response with an `api_key_configured` boolean field.
3. WHEN the API_Key is configured, THE Health_Endpoint SHALL return `{"api_key_configured": true}`.
4. WHEN the API_Key is not configured, THE Health_Endpoint SHALL return `{"api_key_configured": false}`.

### Requirement 4: Frontend API Key Missing Banner

**User Story:** As a new user, I want to see a clear message on the Home_Page when the API key is missing, so that I know how to configure the application.

#### Acceptance Criteria

1. WHEN the Home_Page loads, THE Home_Page SHALL call the Health_Endpoint to check configuration status.
2. WHEN the Health_Endpoint returns `api_key_configured` as `false`, THE Home_Page SHALL display the API_Key_Banner with the text "OpenRouter API key not configured. Set the OPENROUTER_API_KEY environment variable in your .env file and restart the server."
3. WHEN the Health_Endpoint returns `api_key_configured` as `false`, THE Home_Page SHALL disable the submit button for video generation.
4. WHEN the Health_Endpoint returns `api_key_configured` as `true`, THE Home_Page SHALL hide the API_Key_Banner and enable the submit button.
5. IF the Health_Endpoint request fails, THEN THE Home_Page SHALL display the API_Key_Banner with a fallback message "Unable to check server configuration."
