---
name: slidewise
description: Convert YouTube videos or local video files into beautiful reveal.js HTML slide decks. Use when the user wants to create a presentation from a video, lecture, tutorial, or talk.
version: 0.1.0
---

# Slidewise

Create beautiful reveal.js slide decks from any video. The Slidewise API extracts transcripts, keyframes, and segments from videos, then you generate a self-contained HTML presentation that the user can open in any browser.

## When to Use This Skill

- User wants to create slides from a YouTube video URL
- User wants to turn a lecture, talk, or tutorial into a presentation
- User has a local video file and wants a slide deck
- User wants to summarize video content visually

## Prerequisites

The user needs a Slidewise API key. Check for `SLIDEWISE_API_KEY` in the environment, or ask the user to provide one.

## Recommended Workflow

### 1. Confirm the video

Ask the user for the video URL or file path. Confirm the target before calling the API.

### 2. Call the Slidewise API

```bash
curl -s -X POST https://api.slidewise.dev/api/v1/extract \
  -H "X-API-Key: $SLIDEWISE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "VIDEO_URL_HERE",
    "options": {
      "extract_keyframes": true,
      "max_slides": 25,
      "language": "en"
    }
  }'
```

For local development: replace the host with `http://localhost:8000`.

### 3. Parse the response

The API returns JSON with three key sections:

- `video` — title, duration, channel, chapters
- `segments[]` — per-segment transcript, content type, keyframe images (base64), speaker notes
- `slide_outline[]` — suggested slide structure with types, titles, bullets, and code

### 4. Generate reveal.js HTML

Use the template below and the `slide_outline` to build the HTML file. Write it to the user's working directory.

### 5. Preview and iterate

Tell the user to open the HTML file in a browser. Then refine based on their feedback.

## reveal.js HTML Template

Use this as the skeleton for every slide deck:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TITLE_HERE</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/night.css" id="theme">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/monokai.css">
  <style>
    .reveal h1 { font-size: 2.2em; }
    .reveal h2 { font-size: 1.6em; }
    .reveal ul { text-align: left; }
    .reveal li { margin-bottom: 0.4em; line-height: 1.4; }
    .reveal pre { width: 95%; font-size: 0.65em; }
    .reveal img { max-height: 55vh; border-radius: 8px; }
    .reveal .subtitle { font-size: 0.7em; color: #aaa; margin-top: 0.3em; }
    .reveal .timestamp { font-size: 0.5em; color: #666; }
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- SLIDES GO HERE -->
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.js"></script>
  <script>
    Reveal.initialize({
      hash: true,
      plugins: [RevealHighlight, RevealNotes],
      transition: 'slide',
    });
  </script>
</body>
</html>
```

## Slide Type Templates

### Title Slide

```html
<section>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  <p class="timestamp">{upload_date}</p>
  <aside class="notes">{speaker_notes}</aside>
</section>
```

### Content Slide

```html
<section>
  <h2>{title}</h2>
  <ul>
    <li>{bullet_1}</li>
    <li>{bullet_2}</li>
    <li>{bullet_3}</li>
  </ul>
  <aside class="notes">{speaker_notes}</aside>
</section>
```

### Code Slide

```html
<section>
  <h2>{title}</h2>
  <pre><code class="{language}" data-trim data-noescape>
{code}
  </code></pre>
  <aside class="notes">{speaker_notes}</aside>
</section>
```

### Image Slide (with keyframe)

```html
<section>
  <h2>{title}</h2>
  <img src="{keyframe_base64_data_uri}" alt="{title}">
  <aside class="notes">{speaker_notes}</aside>
</section>
```

### Summary Slide

```html
<section>
  <h2>Key Takeaways</h2>
  <ol>
    <li>{takeaway_1}</li>
    <li>{takeaway_2}</li>
    <li>{takeaway_3}</li>
  </ol>
</section>
```

### Section Divider

```html
<section data-background-color="#1a1a2e">
  <h2>{section_title}</h2>
</section>
```

## How to Build the Slides

1. Start with the HTML template above
2. For each entry in `slide_outline[]`, pick the matching template by `type`
3. Fill in: title from `slide_outline[].title`, bullets from `slide_outline[].bullets`
4. For speaker notes, use the `speaker_notes` field from the matching `segments[]` entry (matched via `source_segment`)
5. For image slides, use `segments[source_segment].keyframe.image_base64` as the `src`
6. For code slides, use `slide_outline[].code` if present, otherwise extract from transcript context
7. Write the complete HTML to a file like `slides.html`

## Customization

### Themes

The user can request any reveal.js theme. Change the theme CSS URL:

| Theme | URL path |
|-------|----------|
| Night (default) | `theme/night.css` |
| Moon | `theme/moon.css` |
| Dracula | `theme/dracula.css` |
| Black | `theme/black.css` |
| White | `theme/white.css` |
| League | `theme/league.css` |
| Solarized | `theme/solarized.css` |
| Sky | `theme/sky.css` |

### Transitions

Available: `slide`, `fade`, `convex`, `concave`, `zoom`, `none`

Change in the `Reveal.initialize()` config.

## Iteration Patterns

Common user requests and how to handle them:

| Request | Action |
|---------|--------|
| "Make slide 3 more concise" | Rewrite the bullets to be shorter, keep the speaker notes full |
| "Add more code examples" | Check `segments[].code_blocks` for adjacent segments, add code slides |
| "Change the theme" | Swap the theme CSS URL in the `<head>` |
| "Split slide 5 into two" | Create two `<section>` elements, divide the content |
| "Remove slides 8-10" | Delete those `<section>` elements |
| "Make the text bigger" | Adjust `font-size` in the `<style>` block |
| "Add a slide between 3 and 4" | Insert a new `<section>`, use transcript from that time range |
| "Reorder slides" | Move `<section>` elements within the HTML |
| "Add slide numbers" | Add `slideNumber: true` to `Reveal.initialize()` config |
| "Export to PDF" | Add `?print-pdf` to the URL, then print to PDF from the browser |

## API Reference

### POST /api/v1/extract

**Headers:** `X-API-Key: <your_key>`, `Content-Type: application/json`

**Request body:**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "options": {
    "extract_keyframes": true,
    "max_slides": 30,
    "language": "en",
    "time_window_seconds": 120
  }
}
```

**Response shape:**
```json
{
  "status": "success",
  "job_id": "a1b2c3d4e5f6",
  "video": {
    "title": "...",
    "duration": 1234.0,
    "channel": "...",
    "url": "...",
    "thumbnail_url": "...",
    "upload_date": "20260101",
    "chapters": [{"title": "...", "start_time": 0.0, "end_time": 45.0}]
  },
  "segments": [
    {
      "index": 0,
      "title": "Introduction",
      "start_time": 0.0,
      "end_time": 45.0,
      "transcript": "Welcome to...",
      "content_type": "intro",
      "suggested_slide_type": "title",
      "keyframe": {"timestamp": 22.5, "image_base64": "data:image/jpeg;base64,...", "frame_type": "webcam"},
      "code_blocks": [],
      "speaker_notes": "Welcome to..."
    }
  ],
  "slide_outline": [
    {
      "slide_number": 1,
      "type": "title",
      "title": "Video Title",
      "subtitle": "by Channel Name",
      "source_segment": 0,
      "has_image": true
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "Getting Started",
      "bullets": ["Point one", "Point two", "Point three"],
      "source_segment": 1,
      "has_image": false
    }
  ],
  "processing_time_seconds": 8.5
}
```
