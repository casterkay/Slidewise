"""Video metadata extraction via yt-dlp."""

import hashlib
import logging
import os
import re

from api.video.models import Chapter, VideoInfo, VideoSourceType

logger = logging.getLogger(__name__)

try:
    import yt_dlp

    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False

# YouTube URL patterns
YOUTUBE_PATTERNS = [
    re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})"),
    re.compile(r"(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})"),
    re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})"),
    re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})"),
]


def extract_video_id(url: str) -> str | None:
    for pattern in YOUTUBE_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    return None


def detect_video_source_type(url_or_path: str) -> VideoSourceType:
    if os.path.isfile(url_or_path):
        return VideoSourceType.LOCAL_FILE
    if os.path.isdir(url_or_path):
        return VideoSourceType.LOCAL_DIRECTORY
    url_lower = url_or_path.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return VideoSourceType.YOUTUBE
    if "vimeo.com" in url_lower:
        return VideoSourceType.VIMEO
    return VideoSourceType.LOCAL_FILE


def _check_ytdlp():
    if not HAS_YTDLP:
        raise RuntimeError("yt-dlp is required. Install with: pip install yt-dlp")


def extract_youtube_metadata(url: str) -> VideoInfo:
    _check_ytdlp()

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    video_id = info.get("id", extract_video_id(url) or "unknown")

    chapters = []
    raw_chapters = info.get("chapters") or []
    for i, ch in enumerate(raw_chapters):
        end_time = ch.get("end_time", 0)
        if i + 1 < len(raw_chapters):
            end_time = raw_chapters[i + 1].get("start_time", end_time)
        chapters.append(
            Chapter(
                title=ch.get("title", f"Chapter {i + 1}"),
                start_time=ch.get("start_time", 0),
                end_time=end_time,
            )
        )

    return VideoInfo(
        video_id=video_id,
        source_type=VideoSourceType.YOUTUBE,
        source_url=url,
        title=info.get("title", ""),
        description=info.get("description", ""),
        duration=float(info.get("duration", 0)),
        upload_date=info.get("upload_date"),
        language=info.get("language") or "en",
        channel_name=info.get("channel") or info.get("uploader"),
        channel_url=info.get("channel_url") or info.get("uploader_url"),
        view_count=info.get("view_count"),
        like_count=info.get("like_count"),
        tags=info.get("tags") or [],
        categories=info.get("categories") or [],
        thumbnail_url=info.get("thumbnail"),
        chapters=chapters,
    )


def extract_local_metadata(file_path: str) -> VideoInfo:
    path = os.path.abspath(file_path)
    name = os.path.splitext(os.path.basename(path))[0]
    video_id = hashlib.sha256(path.encode()).hexdigest()[:16]

    return VideoInfo(
        video_id=video_id,
        source_type=VideoSourceType.LOCAL_FILE,
        file_path=path,
        title=name.replace("-", " ").replace("_", " ").title(),
        duration=0.0,
    )
