"""Map video segments to a slide outline — the intelligence layer."""

from __future__ import annotations

import re

from api.models import SlideOutline
from api.video.models import KeyFrame, SegmentContentType, VideoInfo, VideoSegment


def _extract_bullets(transcript: str, max_bullets: int = 5) -> list[str]:
    """Extract key bullet points from transcript text."""
    sentences = re.split(r'[.!?]+', transcript)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) > 4]

    filler = {"um", "uh", "like", "you know", "basically", "actually", "so yeah"}

    scored: list[tuple[float, str]] = []
    for s in sentences:
        words = s.lower().split()
        if len(words) < 5:
            continue
        score = len(words)
        # Penalize filler
        score -= sum(3 for f in filler if f in s.lower())
        # Boost sentences with key phrases
        if any(kw in s.lower() for kw in ["important", "key", "need to", "must", "should", "first", "then"]):
            score += 5
        scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    bullets = []
    for _, s in scored[:max_bullets]:
        # Truncate long sentences
        words = s.split()
        if len(words) > 18:
            s = " ".join(words[:18]) + "..."
        bullets.append(s)
    return bullets if bullets else [transcript[:120] + "..." if len(transcript) > 120 else transcript]


def _suggest_slide_type(
    segment: VideoSegment,
    keyframe: KeyFrame | None,
    is_first: bool,
    is_last: bool,
) -> str:
    if is_first or segment.content_type == SegmentContentType.INTRO:
        return "title"
    if is_last or segment.content_type == SegmentContentType.OUTRO:
        return "summary"
    if segment.content_type == SegmentContentType.LIVE_CODING or segment.has_code_on_screen:
        return "code"
    if keyframe and keyframe.frame_type in ("slide", "diagram"):
        return "image"
    if segment.content_type == SegmentContentType.SLIDES:
        return "image"
    return "content"


def plan_slides(
    video_info: VideoInfo,
    segments: list[VideoSegment],
    keyframes: list[KeyFrame],
    max_slides: int = 30,
) -> list[SlideOutline]:
    """Generate a slide outline from video segments."""
    outline: list[SlideOutline] = []
    keyframe_map = {i: kf for i, kf in enumerate(keyframes)} if keyframes else {}

    for i, seg in enumerate(segments):
        kf = keyframe_map.get(i)
        is_first = i == 0
        is_last = i == len(segments) - 1

        slide_type = _suggest_slide_type(seg, kf, is_first, is_last)

        slide = SlideOutline(
            slide_number=len(outline) + 1,
            type=slide_type,
            title=seg.chapter_title or f"Part {seg.index + 1}",
            source_segment=seg.index,
            has_image=kf is not None,
        )

        if slide_type == "title":
            slide.title = video_info.title
            slide.subtitle = f"by {video_info.channel_name}" if video_info.channel_name else None
        elif slide_type == "content":
            slide.bullets = _extract_bullets(seg.transcript)
        elif slide_type == "code":
            # Try to extract code from transcript
            code_match = re.search(r'(import |def |class |function |const |let |var )\S+', seg.transcript)
            if code_match:
                # Extract surrounding context as pseudo-code
                start = max(0, code_match.start() - 20)
                end = min(len(seg.transcript), code_match.end() + 200)
                slide.code = seg.transcript[start:end]
            slide.bullets = _extract_bullets(seg.transcript, max_bullets=3)
        elif slide_type == "summary":
            # Collect top takeaways from all segments
            all_bullets = []
            for s in segments:
                all_bullets.extend(_extract_bullets(s.transcript, max_bullets=1))
            slide.bullets = all_bullets[:5]
            slide.title = "Key Takeaways"
        elif slide_type == "image":
            slide.bullets = _extract_bullets(seg.transcript, max_bullets=3)

        outline.append(slide)

        if len(outline) >= max_slides:
            break

    return outline
