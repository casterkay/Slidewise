"""Video transcript extraction: YouTube API, SRT, VTT."""

import logging
import re
from pathlib import Path

from api.video.models import (
    TranscriptSegment,
    TranscriptSource,
    VideoInfo,
    VideoSourceConfig,
    VideoSourceType,
)

logger = logging.getLogger(__name__)

try:
    from youtube_transcript_api import YouTubeTranscriptApi

    HAS_YOUTUBE_TRANSCRIPT = True
except ImportError:
    HAS_YOUTUBE_TRANSCRIPT = False


# =============================================================================
# YouTube Transcript
# =============================================================================


def extract_youtube_transcript(
    video_id: str,
    languages: list[str] | None = None,
) -> tuple[list[TranscriptSegment], TranscriptSource]:
    if not HAS_YOUTUBE_TRANSCRIPT:
        raise RuntimeError("youtube-transcript-api required. pip install youtube-transcript-api")

    if languages is None:
        languages = ["en"]

    try:
        ytt_api = YouTubeTranscriptApi()
        source = TranscriptSource.YOUTUBE_MANUAL

        try:
            transcript_list = ytt_api.list(video_id)
            try:
                transcript_entry = transcript_list.find_manually_created_transcript(languages)
                source = TranscriptSource.YOUTUBE_MANUAL
            except Exception:
                try:
                    transcript_entry = transcript_list.find_generated_transcript(languages)
                    source = TranscriptSource.YOUTUBE_AUTO
                except Exception:
                    transcript_entry = transcript_list.find_transcript(languages)
                    source = (
                        TranscriptSource.YOUTUBE_AUTO
                        if transcript_entry.is_generated
                        else TranscriptSource.YOUTUBE_MANUAL
                    )
            transcript = transcript_entry.fetch()
        except Exception:
            transcript = ytt_api.fetch(video_id, languages=languages)
            if getattr(transcript, "is_generated", False):
                source = TranscriptSource.YOUTUBE_AUTO

        segments = []
        for snippet in transcript.snippets:
            text = snippet.text.strip()
            if not text:
                continue
            segments.append(
                TranscriptSegment(
                    text=text,
                    start=snippet.start,
                    end=snippet.start + snippet.duration,
                    confidence=1.0,
                    source=source,
                )
            )

        return (segments, source) if segments else ([], TranscriptSource.NONE)

    except Exception as e:
        logger.warning(f"Failed to fetch YouTube transcript for {video_id}: {e}")
        return [], TranscriptSource.NONE


# =============================================================================
# Subtitle File Parsing
# =============================================================================


def _parse_timestamp_srt(ts: str) -> float:
    ts = ts.strip().replace(",", ".")
    parts = ts.split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def _parse_timestamp_vtt(ts: str) -> float:
    ts = ts.strip()
    parts = ts.split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return 0.0


def parse_srt(path: str) -> list[TranscriptSegment]:
    content = Path(path).read_text(encoding="utf-8", errors="replace")
    segments = []
    blocks = re.split(r"\n\s*\n", content.strip())
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue
        ts_line = None
        text_lines = []
        for line in lines:
            if "-->" in line:
                ts_line = line
            elif ts_line is not None:
                text_lines.append(line)
        if ts_line is None:
            continue
        parts = ts_line.split("-->")
        if len(parts) != 2:
            continue
        start = _parse_timestamp_srt(parts[0])
        end = _parse_timestamp_srt(parts[1])
        text = re.sub(r"<[^>]+>", "", " ".join(text_lines).strip())
        if text:
            segments.append(
                TranscriptSegment(
                    text=text, start=start, end=end,
                    confidence=1.0, source=TranscriptSource.SUBTITLE_FILE,
                )
            )
    return segments


def parse_vtt(path: str) -> list[TranscriptSegment]:
    content = Path(path).read_text(encoding="utf-8", errors="replace")
    segments = []
    lines = content.strip().split("\n")
    i = 0
    while i < len(lines) and not re.match(r"\d{2}:\d{2}", lines[i]):
        i += 1

    current_text_lines: list[str] = []
    current_start = 0.0
    current_end = 0.0
    in_cue = False

    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if "-->" in line:
            if in_cue and current_text_lines:
                text = re.sub(r"<[^>]+>", "", " ".join(current_text_lines).strip())
                if text:
                    segments.append(
                        TranscriptSegment(
                            text=text, start=current_start, end=current_end,
                            confidence=1.0, source=TranscriptSource.SUBTITLE_FILE,
                        )
                    )
            parts = line.split("-->")
            current_start = _parse_timestamp_vtt(parts[0])
            current_end = _parse_timestamp_vtt(parts[1].split()[0])
            current_text_lines = []
            in_cue = True
        elif line == "":
            if in_cue and current_text_lines:
                text = re.sub(r"<[^>]+>", "", " ".join(current_text_lines).strip())
                if text:
                    segments.append(
                        TranscriptSegment(
                            text=text, start=current_start, end=current_end,
                            confidence=1.0, source=TranscriptSource.SUBTITLE_FILE,
                        )
                    )
                current_text_lines = []
                in_cue = False
        elif in_cue and not line.isdigit():
            current_text_lines.append(line)

    if in_cue and current_text_lines:
        text = re.sub(r"<[^>]+>", "", " ".join(current_text_lines).strip())
        if text:
            segments.append(
                TranscriptSegment(
                    text=text, start=current_start, end=current_end,
                    confidence=1.0, source=TranscriptSource.SUBTITLE_FILE,
                )
            )
    return segments


# =============================================================================
# Main Entry Point
# =============================================================================


def get_transcript(
    video_info: VideoInfo,
    config: VideoSourceConfig,
) -> tuple[list[TranscriptSegment], TranscriptSource]:
    languages = config.languages or ["en"]

    # 1. YouTube API
    if video_info.source_type == VideoSourceType.YOUTUBE and HAS_YOUTUBE_TRANSCRIPT:
        try:
            segments, source = extract_youtube_transcript(video_info.video_id, languages)
            if segments:
                logger.info(
                    f"Got {len(segments)} transcript segments via YouTube API "
                    f"({source.value}) for '{video_info.title}'"
                )
                return segments, source
        except Exception as e:
            logger.warning(f"YouTube transcript failed: {e}")

    # 2. Subtitle files for local videos
    if video_info.file_path:
        base = Path(video_info.file_path).stem
        parent = Path(video_info.file_path).parent
        for ext in [".srt", ".vtt"]:
            sub_path = parent / f"{base}{ext}"
            if sub_path.exists():
                logger.info(f"Found subtitle file: {sub_path}")
                parser = parse_srt if ext == ".srt" else parse_vtt
                segments = parser(str(sub_path))
                if segments:
                    return segments, TranscriptSource.SUBTITLE_FILE

    logger.warning(f"No transcript available for '{video_info.title}'")
    return [], TranscriptSource.NONE
