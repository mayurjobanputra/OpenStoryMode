# Implementation Plan: Typewriter Captions

## Overview

Add typewriter-style captions to OpenStoryMode videos. Implementation proceeds bottom-up: data model changes first, then the pure-function caption renderer, then video assembler integration, pipeline wiring, API/validation updates, and finally the UI toggle. Each step builds on the previous one so there is no orphaned code.

## Tasks

- [x] 1. Add CaptionMode enum and update GenerationRequest model
  - [x] 1.1 Add `CaptionMode` enum and `caption_mode` field to `GenerationRequest` in `app/models.py`
    - Add `CaptionMode(str, Enum)` with values `YES = "yes"`, `NO = "no"`, `BOTH = "both"`
    - Add `caption_mode: CaptionMode = CaptionMode.YES` field to `GenerationRequest` dataclass
    - Add optional `video_paths: list[Path]` field to `Job` dataclass for BOTH mode dual output
    - _Requirements: 5.1_

  - [ ]* 1.2 Write unit tests for CaptionMode and updated GenerationRequest
    - Test `CaptionMode` enum values and string coercion
    - Test `GenerationRequest` default `caption_mode` is `CaptionMode.YES`
    - Test `Job` dataclass accepts `video_paths`
    - _Requirements: 5.1_

- [x] 2. Implement caption renderer module
  - [x] 2.1 Create `app/caption_renderer.py` with `escape_ffmpeg_text` and `unescape_ffmpeg_text`
    - Implement FFmpeg drawtext special character escaping (`: \ ' ; [ ] =`)
    - Replace non-renderable characters with a space fallback
    - Implement `unescape_ffmpeg_text` as the inverse operation
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ]* 2.2 Write property test for escape/unescape round trip
    - **Property 8: Escape/unescape round trip**
    - **Validates: Requirements 7.1, 7.3**

  - [ ]* 2.3 Write property test for non-renderable character fallback
    - **Property 9: Non-renderable character fallback**
    - **Validates: Requirements 7.2**

  - [x] 2.4 Implement `build_drawtext_filter` in `app/caption_renderer.py`
    - Define caption style constants (`FONT_FAMILY`, `FONT_SIZE_HORIZONTAL`, `FONT_SIZE_VERTICAL`, `FONT_COLOR`, `BOX_COLOR`, `BOX_BORDER_W`, `MAX_WIDTH_RATIO`, `LOWER_THIRD_Y_RATIO`)
    - Implement word-level reveal: split text at word boundaries, compute per-word reveal times evenly distributed across the duration
    - Generate N stacked `drawtext` filters (one per word group) with staggered `enable='between(t, reveal_time, scene_end)'` expressions
    - Position text in the lower third with centered x, semi-transparent background box, horizontal padding
    - Constrain text block to 80% of video frame width
    - Accept `start_time` and `crossfade_duration` parameters for multi-scene timing
    - Return empty string for empty text input; raise `ValueError` for non-positive duration
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 6.1, 6.2_

  - [ ]* 2.5 Write property test for even character reveal timing
    - **Property 1: Even character reveal timing**
    - **Validates: Requirements 1.1, 1.2, 1.3**

  - [ ]* 2.6 Write property test for drawtext filter styling correctness
    - **Property 2: Drawtext filter styling correctness**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4**

  - [ ]* 2.7 Write property test for text width constraint
    - **Property 3: Text width constraint**
    - **Validates: Requirements 3.1, 3.3**

  - [ ]* 2.8 Write property test for word-boundary wrapping
    - **Property 4: Word-boundary wrapping**
    - **Validates: Requirements 3.2**

  - [ ]* 2.9 Write property test for scene caption timing with crossfade handling
    - **Property 7: Scene caption timing with crossfade handling**
    - **Validates: Requirements 6.1, 6.2, 6.3**

  - [ ]* 2.10 Write unit tests for `build_drawtext_filter` edge cases
    - Test empty text returns empty string
    - Test single-character text
    - Test text with only special characters
    - Test non-positive duration raises `ValueError`
    - Test both horizontal (1280×720) and vertical (720×1280) resolutions
    - _Requirements: 1.1, 2.1, 2.3, 7.1_

- [x] 3. Checkpoint - Ensure all caption renderer tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Integrate captions into video assembler
  - [x] 4.1 Update `assemble_video` signature in `app/video_assembler.py` to accept `scenes` and `caption_mode`
    - Add `scenes: list[Scene] | None = None` and `caption_mode: CaptionMode = CaptionMode.YES` parameters
    - Import `CaptionMode` from `app.models` and `build_drawtext_filter` from `app.caption_renderer`
    - When `caption_mode=NO` or `scenes` is `None`, behavior is unchanged (no captions)
    - _Requirements: 4.4, 5.2_

  - [x] 4.2 Update `_assemble_single_scene` to inject drawtext caption filters when captions are enabled
    - Call `build_drawtext_filter` for the scene's narration text
    - Chain the drawtext filter(s) after the existing `scale/pad/format` filter in the `-vf` argument
    - Handle caption generation failures gracefully (log warning, proceed without captions)
    - _Requirements: 4.1, 4.2_

  - [x] 4.3 Update `_assemble_multi_scene` to inject per-scene drawtext caption filters with correct timing
    - For each scene, call `build_drawtext_filter` with the scene's `start_time` and `crossfade_duration`
    - Compute cumulative start times accounting for crossfade overlaps
    - Chain drawtext filters after the scale filter for each video stream in the filter graph
    - Ensure caption time windows do not overlap between scenes
    - _Requirements: 4.1, 4.3, 6.1, 6.2, 6.3_

  - [x] 4.4 Implement BOTH mode in `assemble_video` — produce two output files
    - When `caption_mode=BOTH`, run the FFmpeg pipeline twice: once without captions (`output.mp4`) and once with captions (`output_captioned.mp4`)
    - Return `tuple[Path, Path]` as `(captioned_path, no_captions_path)` for BOTH mode
    - Return single `Path` for YES and NO modes
    - _Requirements: 5.3, 5.4, 5.5_

  - [ ]* 4.5 Write property test for caption filters present when caption_mode is YES
    - **Property 5: Caption filters present when caption_mode is YES**
    - **Validates: Requirements 4.1, 4.2, 4.3, 5.3**

  - [ ]* 4.6 Write property test for no caption filters when caption_mode is NO
    - **Property 6: No caption filters when caption_mode is NO**
    - **Validates: Requirements 5.2**

  - [ ]* 4.7 Write property test for BOTH mode producing two distinct output files
    - **Property 6a: BOTH mode produces two distinct output files**
    - **Validates: Requirements 5.4, 5.5**

  - [ ]* 4.8 Write integration tests for video assembler with captions
    - Test single-scene assembly with `caption_mode=YES` produces valid MP4
    - Test multi-scene assembly with `caption_mode=YES` produces valid MP4
    - Test `caption_mode=BOTH` produces two files with correct names
    - Test `caption_mode=NO` produces single file without captions (backward compatible)
    - Extend existing fixtures in `tests/test_video_assembler.py`
    - _Requirements: 4.1, 4.2, 4.3, 5.2, 5.3, 5.4, 5.5_

- [x] 5. Checkpoint - Ensure all video assembler tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Wire caption mode through pipeline, API, and validation
  - [x] 6.1 Update `app/validation.py` to validate `caption_mode`
    - Add `validate_caption_mode` function that maps string to `CaptionMode` enum
    - Extend `validate_generation_request` to accept and validate `caption_mode` parameter (default `"yes"`)
    - Return `CaptionMode` on the `GenerationRequest` in `ValidationResult`
    - _Requirements: 5.1_

  - [x] 6.2 Update `app/pipeline.py` to pass `scenes` and `caption_mode` to `assemble_video`
    - Pass `job.scenes` and `job.request.caption_mode` to `assemble_video()`
    - Handle BOTH mode return value: store both paths on `Job` (`video_path` for captioned, `video_paths` for both)
    - Report both output file paths in logs
    - _Requirements: 4.4, 5.4, 5.6_

  - [x] 6.3 Update `app/main.py` API endpoint to accept and forward `caption_mode`
    - Add `caption_mode: str = "yes"` field to `GenerateRequest` Pydantic model
    - Pass `caption_mode` to `validate_generation_request`
    - Update `/api/status/{job_id}` response to include `video_urls` list when `caption_mode=BOTH`
    - _Requirements: 5.1, 5.6_

  - [ ]* 6.4 Write unit tests for caption_mode validation and API integration
    - Test `validate_caption_mode` accepts "yes", "no", "both" and rejects invalid values
    - Test `validate_generation_request` includes `caption_mode` on the returned `GenerationRequest`
    - Test API endpoint accepts `caption_mode` field and rejects invalid values
    - Test default `caption_mode` is "yes" when not provided
    - _Requirements: 5.1_

- [x] 7. Update UI for caption mode selection
  - [x] 7.1 Add caption mode selector to `static/index.html`
    - Add a three-option radio group or dropdown for caption mode (Yes / No / Both) on the create page
    - Default selection to "Yes"
    - Include the `caption_mode` value in the POST request body to `/api/generate`
    - Display both video links on the job detail page when `caption_mode=BOTH`
    - _Requirements: 5.1, 5.6_

- [x] 8. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests use the Hypothesis library (already in `requirements.txt`)
- Checkpoints ensure incremental validation
- The caption renderer is a pure-function module with no I/O, making it straightforward to test
- BOTH mode runs FFmpeg twice — once with and once without caption filters
