# 🎬 Vibe Your Videos

**Turn any idea into a narrated video — powered by AI, built for creators.**

Type a prompt. Get a fully produced video with AI-generated visuals, narration, and typewriter-style captions. No editing. No timeline. Just vibes.

[VibeYourVideos.com](https://vibeyourvideos.com)

---

## What It Does

Vibe Your Videos takes your idea and runs it through a complete production pipeline:

1. An LLM writes a scene-by-scene script from your prompt
2. AI generates a unique image for each scene
3. Text-to-speech narrates the script
4. FFmpeg assembles everything into a polished MP4 with crossfade transitions

The whole thing runs locally on your machine. Your content, your data, your videos.

## ✨ Typewriter Captions

Words appear on screen as they're spoken — a rolling window of bold, high-contrast text that keeps viewers locked in. Choose from three caption modes:

- **Yes** — Video with captions baked in
- **No** — Clean video, no text overlay
- **Create Both** — Get two versions in one job

Captions are rendered directly into the video via FFmpeg drawtext filters. Heavy sans-serif font, black stroke border, auto line-wrapped to fit any aspect ratio.

## Screenshots

### Create Page
Simple interface — enter your idea, pick a length, aspect ratio, and caption mode. Hit generate.

![Create Page](create-page.png)

### Jobs Page
All your video generation jobs in a grid. Click any card for full details.

![Jobs Page](jobs-page.png)

### Job Details
Original prompt, metadata, and scene-by-scene script on the left. Video playback on the right.

![Job Details](job-details-1.png)


## Free & Open Source

Everything in this repo is MIT-licensed and runs locally. You get:

- Short-form video generation (up to 90 seconds)
- Horizontal (16:9) and vertical (9:16) aspect ratios
- AI script writing, image generation, and TTS narration
- Typewriter captions with three modes (Yes / No / Create Both)
- Job history with persistence across restarts
- Single-command setup via `start.sh`

## 🚀 Pro (Coming Soon)

For creators and teams who want more, **Vibe Your Videos Pro** will include:

- Longer videos beyond 90 seconds
- Content Design Studio — fine-tune scripts, visuals, and pacing before rendering
- Advanced caption styling and positioning options
- Animated content instead of static images
- Brand Kit — upload logos, fonts, and color palettes for consistent branding
- Video reference — use existing footage as a style guide
- Scheduler — queue and schedule video generation
- Automation Engine — trigger video creation from external events
- Direct upload to social media platforms

Stay tuned at [VibeYourVideos.com](https://vibeyourvideos.com) for updates.

---

## Getting Started

### Prerequisites

- Python 3.10+
- An [OpenRouter](https://openrouter.ai/) API key

### Setup

1. Clone the repo:

```bash
git clone https://github.com/mayurjobanputra/VibeYourVideos.git
cd VibeYourVideos
```

2. Start the app:

```bash
./start.sh
```

On first run, it will:
- Ask for your [OpenRouter API key](https://openrouter.ai/) and create a `.env` file
- Set up a Python virtual environment and install dependencies
- Start the server

Open http://localhost:8000 in your browser.

To use a different port:

```bash
PORT=8001 ./start.sh
```

### Manual Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Running Multiple Instances

Each instance is self-contained with its own `output/` directory, job history, and `.env` config. Just use a different port:

```bash
PORT=8001 ./start.sh
```

## Utilities

### Migrate Legacy Jobs

If you have existing output directories from before job history was added:

```bash
.venv/bin/python migrate_jobs.py
```

Restart the server afterward to load migrated jobs.

## Other AI Providers

Currently only [OpenRouter](https://openrouter.ai/) is supported. Want a different provider? [Open an issue](https://github.com/mayurjobanputra/VibeYourVideos/issues) or submit a PR.

## License

MIT — see [LICENSE](LICENSE) for details.
