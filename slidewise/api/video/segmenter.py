"""Video segmentation: chapter-based (primary) + time-window fallback."""

import logging

from api.video.models import (
    SegmentContentType,
    TranscriptSegment,
    VideoInfo,
    VideoSegment,
    VideoSourceConfig,
)

logger = logging.getLogger(__name__)


def _classify_content_type(transcript: str) -> SegmentContentType:
    lower = transcript.lower()

    code_indicators = ["import ", "def ", "class ", "function ", "const ", "npm ", "pip ", "git "]
    intro_indicators = ["welcome", "hello", "today we", "in this video", "let's get started"]
    outro_indicators = ["thanks for watching", "subscribe", "see you next", "that's it for"]

    if any(kw in lower for kw in outro_indicators):
        return SegmentContentType.OUTRO
    if any(kw in lower for kw in intro_indicators):
        return SegmentContentType.INTRO
    if sum(1 for kw in code_indicators if kw in lower) >= 2:
        return SegmentContentType.LIVE_CODING
    return SegmentContentType.EXPLANATION


def _get_transcript_in_range(
    transcript_segments: list[TranscriptSegment],
    start_time: float,
    end_time: float,
) -> tuple[str, float]:
    texts = []
    confidences = []
    for seg in transcript_segments:
        if seg.end > start_time and seg.start < end_time:
            texts.append(seg.text)
            confidences.append(seg.confidence)
    text = " ".join(texts)
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    return text, avg_confidence


def segment_by_chapters(
    video_info: VideoInfo,
    transcript_segments: list[TranscriptSegment],
) -> list[VideoSegment]:
    segments = []
    for i, chapter in enumerate(video_info.chapters):
        transcript, confidence = _get_transcript_in_range(
            transcript_segments, chapter.start_time, chapter.end_time
        )
        content_type = _classify_content_type(transcript)
        segments.append(
            VideoSegment(
                index=i,
                start_time=chapter.start_time,
                end_time=chapter.end_time,
                duration=chapter.end_time - chapter.start_time,
                transcript=transcript,
                transcript_confidence=confidence,
                chapter_title=chapter.title,
                content_type=content_type,
                speaker_notes=transcript,
            )
        )
    return segments


def segment_by_time_window(
    video_info: VideoInfo,
    transcript_segments: list[TranscriptSegment],
    window_seconds: float = 120.0,
    start_offset: float = 0.0,
    end_limit: float | None = None,
) -> list[VideoSegment]:
    segments = []
    duration = video_info.duration
    if duration <= 0 and transcript_segments:
        duration = max(seg.end for seg in transcript_segments)
    if end_limit is not None:
        duration = min(duration, end_limit)
    if duration <= 0:
        return segments

    current_time = start_offset
    index = 0
    while current_time < duration:
        end_time = min(current_time + window_seconds, duration)
        transcript, confidence = _get_transcript_in_range(
            transcript_segments, current_time, end_time
        )
        if transcript.strip():
            content_type = _classify_content_type(transcript)
            segments.append(
                VideoSegment(
                    index=index,
                    start_time=current_time,
                    end_time=end_time,
                    duration=end_time - current_time,
                    transcript=transcript,
                    transcript_confidence=confidence,
                    content_type=content_type,
                    speaker_notes=transcript,
                )
            )
            index += 1
        current_time = end_time
    return segments


def segment_video(
    video_info: VideoInfo,
    transcript_segments: list[TranscriptSegment],
    config: VideoSourceConfig,
) -> list[VideoSegment]:
    if video_info.chapters:
        logger.info(f"Using chapter-based segmentation ({len(video_info.chapters)} chapters)")
        segments = segment_by_chapters(video_info, transcript_segments)
        if segments:
            return segments

    window = config.time_window_seconds
    logger.info(f"Using time-window segmentation ({window}s windows)")
    return segment_by_time_window(
        video_info,
        transcript_segments,
        window,
        start_offset=config.clip_start or 0.0,
        end_limit=config.clip_end,
    )
