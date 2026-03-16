# Requirements Document

## Introduction

This feature adds typewriter-style captions to OpenStoryMode-generated videos. Captions reveal character-by-character in sync with the narration audio, creating a "typed as spoken" visual effect. The caption text is derived from each scene's `narration_text` and rendered as an FFmpeg text overlay during video assembly.

## Glossary

- **Video_Assembler**: The module (`app/video_assembler.py`) that composites scene images and narration audio into a final MP4 using FFmpeg filter graphs.
- **Caption_Renderer**: The component responsible for generating FFmpeg drawtext filter expressions that produce the typewriter reveal effect.
- **TTS_Engine**: The module (`app/tts_engine.py`) that synthesizes narration audio from scene text via OpenRouter's TTS endpoint.
- **Scene**: A data object containing an index, narration_text, and visual_description.
- **SceneAsset**: A data object holding file paths to a scene's generated image and audio.
- **Typewriter_Effect**: A text animation where characters appear progressively from left to right, simulating typing, timed to match the narration audio duration.
- **Caption_Style**: A set of visual properties (font, size, color, background, position) that define how caption text is rendered on the video frame.

## Requirements

### Requirement 1: Character-by-Character Caption Reveal

**User Story:** As a viewer, I want captions to appear character by character in time with the narration, so that the text feels like it is being typed as the narrator speaks.

#### Acceptance Criteria

1. WHEN a scene's narration audio plays, THE Caption_Renderer SHALL reveal the scene's narration_text one character at a time over the duration of that scene's audio.
2. THE Caption_Renderer SHALL distribute character reveal timing evenly across the audio duration so that the full text is visible by the time the audio ends.
3. WHEN the narration_text contains multiple sentences, THE Caption_Renderer SHALL reveal all sentences sequentially within the same scene without resetting the typewriter animation.

### Requirement 2: Caption Positioning and Styling

**User Story:** As a viewer, I want captions to be clearly readable against any background image, so that I can follow the narration text without difficulty.

#### Acceptance Criteria

1. THE Caption_Renderer SHALL render caption text in the lower third of the video frame.
2. THE Caption_Renderer SHALL render a semi-transparent dark background behind the caption text to ensure readability against varying scene images.
3. THE Caption_Renderer SHALL use a white, sans-serif font at a size legible on both 720x1280 (vertical) and 1280x720 (horizontal) resolutions.
4. THE Caption_Renderer SHALL apply horizontal padding so that caption text does not touch the left or right edges of the video frame.

### Requirement 3: Word Wrapping for Long Narration Text

**User Story:** As a viewer, I want long narration text to wrap across multiple lines, so that text remains readable and does not overflow the video frame.

#### Acceptance Criteria

1. WHEN the narration_text for a scene exceeds the available horizontal width, THE Caption_Renderer SHALL wrap the text onto multiple lines.
2. THE Caption_Renderer SHALL wrap text at word boundaries rather than splitting words mid-character.
3. THE Caption_Renderer SHALL constrain the caption text block to a maximum width equal to 80% of the video frame width.

### Requirement 4: Integration with Video Assembly Pipeline

**User Story:** As a developer, I want the typewriter caption effect to be applied during video assembly, so that captions are baked into the final MP4 output without requiring a separate processing step.

#### Acceptance Criteria

1. THE Video_Assembler SHALL apply the typewriter caption overlay as part of the FFmpeg filter graph during video assembly.
2. WHEN assembling a single-scene video, THE Video_Assembler SHALL include the caption overlay filter for that scene.
3. WHEN assembling a multi-scene video, THE Video_Assembler SHALL include a caption overlay filter for each scene, timed to that scene's position in the final video timeline.
4. THE Video_Assembler SHALL accept the narration_text for each scene alongside the existing SceneAsset data to generate caption filters.

### Requirement 5: Caption Mode Selection

**User Story:** As a user, I want to choose whether captions are included, excluded, or both versions are generated, so that I can produce the exact video outputs I need without re-running the pipeline.

#### Acceptance Criteria

1. THE GenerationRequest SHALL include a caption_mode option as a three-way enum (YES, NO, BOTH) that defaults to YES.
2. WHEN caption_mode is set to NO, THE Video_Assembler SHALL produce a single video file without any caption overlay.
3. WHEN caption_mode is set to YES, THE Video_Assembler SHALL produce a single video file with the typewriter caption overlay.
4. WHEN caption_mode is set to BOTH, THE Video_Assembler SHALL produce two output files: one with captions and one without captions.
5. WHEN caption_mode is BOTH, THE Video_Assembler SHALL name the captioned output `output_captioned.mp4` and the non-captioned output `output.mp4`.
6. WHEN caption_mode is BOTH, THE pipeline SHALL report both output file paths upon completion.

### Requirement 6: Scene Transition Caption Handling

**User Story:** As a viewer, I want captions to reset cleanly between scenes, so that each scene starts with a fresh typewriter animation.

#### Acceptance Criteria

1. WHEN a new scene begins in the video timeline, THE Caption_Renderer SHALL start a new typewriter animation from the first character of that scene's narration_text.
2. WHEN a crossfade transition occurs between scenes, THE Caption_Renderer SHALL fade out the previous scene's caption during the crossfade and begin the next scene's caption after the crossfade completes.
3. THE Caption_Renderer SHALL ensure no caption text from a previous scene remains visible when the next scene's narration begins.

### Requirement 7: Special Character Handling

**User Story:** As a developer, I want the caption system to handle special characters in narration text without breaking the FFmpeg filter graph, so that video assembly remains reliable.

#### Acceptance Criteria

1. WHEN narration_text contains characters that are special in FFmpeg drawtext syntax (such as colons, backslashes, single quotes, or semicolons), THE Caption_Renderer SHALL escape those characters before embedding them in the filter graph.
2. IF narration_text contains characters that cannot be rendered by the selected font, THEN THE Caption_Renderer SHALL substitute a fallback character rather than causing an FFmpeg error.
3. FOR ALL valid narration_text strings, escaping then unescaping SHALL produce the original text (round-trip property).
