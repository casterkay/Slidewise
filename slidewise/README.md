# Slidewise

Turn YouTube videos and local video files into beautiful reveal.js slide decks.

**Architecture:** A paid API service handles all heavy video processing (transcript extraction, keyframe capture, segmentation, slide planning). A local agent skill uses the API output to generate self-contained HTML slides that users can iterate on with their agent.

## Quick Start

### 1. Install dependencies

```bash
cd slidewise
pip install -e ".[dev]"
```

### 2. Set up Supabase

Create a Supabase project at [supabase.com](https://supabase.com). Run the migration:

```bash
# Via Supabase CLI
supabase db push

# Or manually run supabase/migrations/001_initial.sql in the SQL editor
```

Create a `.env` file from the example:

```bash
cp .env.example .env
# Fill in your Supabase URL and keys
```

### 3. Run the API

```bash
uvicorn api.main:app --reload --port 8000
```

### 4. Extract from a video

```bash
curl -X POST http://localhost:8000/api/v1/extract \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID", "options": {"extract_keyframes": false}}'
```

### 5. Use the agent skill

Feed `skill/SKILL.md` to your agent (Claude, etc.), then ask:

> "Create slides from https://www.youtube.com/watch?v=VIDEO_ID"

The agent will call the API, generate a reveal.js HTML file, and let you iterate.

### 6. Preview

Open the generated `.html` file in a browser. Press `S` for speaker notes view.

## Project Structure

```
slidewise/
├── api/                     # FastAPI service
│   ├── main.py             # Endpoints
│   ├── config.py           # Settings (env vars)
│   ├── auth.py             # API key auth via Supabase
│   ├── storage.py          # Supabase Storage for keyframes
│   ├── supabase_client.py  # Client singleton
│   ├── models.py           # Request/response schemas
│   ├── pipeline.py         # Orchestrator
│   ├── slide_planner.py    # Segment → slide mapping
│   └── video/              # Video processing (adapted from Skill Seekers)
│       ├── models.py       # Pydantic data models
│       ├── metadata.py     # yt-dlp metadata extraction
│       ├── transcript.py   # YouTube API / SRT / VTT transcript
│       ├── segmenter.py    # Chapter-based + time-window segmentation
│       └── visual.py       # Keyframe extraction via OpenCV
├── skill/
│   └── SKILL.md            # Agent skill definition
├── supabase/
│   └── migrations/         # SQL migrations
├── tests/                  # Test suite
├── examples/
│   ├── sample_response.json
│   └── sample_slides.html  # Open in browser to preview
└── pyproject.toml
```

## Running Tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/api/v1/extract` | Extract video → slide materials |

## Technology

- **API:** FastAPI + Supabase (PostgreSQL, Auth, Storage)
- **Video:** yt-dlp, youtube-transcript-api, OpenCV
- **Slides:** reveal.js 5.x (generated as self-contained HTML)
- **Auth:** API keys validated against Supabase `api_keys` table
