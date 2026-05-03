"""Video data models adapted from Skill Seekers, using Pydantic for auto JSON serialization."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# =============================================================================
# Enumerations
# =============================================================================


class VideoSourceType(str, Enum):
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    LOCAL_FILE = "local_file"
    LOCAL_DIRECTORY = "local_directory"


class TranscriptSource(str, Enum):
    YOUTUBE_MANUAL = "youtube_manual"
    YOUTUBE_AUTO = "youtube_auto_generated"
    WHISPER = "whisper"
    SUBTITLE_FILE = "subtitle_file"
    NONE = "none"


class FrameType(str, Enum):
    CODE_EDITOR = "code_editor"
    TERMINAL = "terminal"
    SLIDE = "slide"
    DIAGRAM = "diagram"
    BROWSER = "browser"
    WEBCAM = "webcam"
    SCREENCAST = "screencast"
    OTHER = "other"


class SegmentContentType(str, Enum):
    EXPLANATION = "explanation"
    LIVE_CODING = "live_coding"
    DEMO = "demo"
    SLIDES = "slides"
    Q_AND_A = "q_and_a"
    INTRO = "intro"
    OUTRO = "outro"
    MIXED = "mixed"


# =============================================================================
# Supporting Models
# =============================================================================


class Chapter(BaseModel):
    title: str
    start_time: float
    end_time: float

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time


class TranscriptSegment(BaseModel):
    text: str
    start: float
    end: float
    confidence: float = 1.0
    source: TranscriptSource = TranscriptSource.NONE


class KeyFrame(BaseModel):
    timestamp: float
    image_base64: str = ""
    frame_type: FrameType = FrameType.OTHER
    storage_path: str | None = None  # Supabase Storage path


class CodeBlock(BaseModel):
    code: str
    language: str | None = None
    source_frame: float = 0.0
    confidence: float = 0.0


# =============================================================================
# Core Models
# =============================================================================


class VideoSegment(BaseModel):
    index: int
    start_time: float
    end_time: float
    duration: float

    # Audio
    transcript: str = ""
    transcript_confidence: float = 0.0

    # Visual
    keyframe: KeyFrame | None = None
    has_code_on_screen: bool = False
    has_slides: bool = False
    has_diagram: bool = False
    detected_code_blocks: list[CodeBlock] = Field(default_factory=list)

    # Metadata
    chapter_title: str | None = None
    content_type: SegmentContentType = SegmentContentType.MIXED

    # For slides
    suggested_slide_type: str = "content"
    speaker_notes: str = ""

    @property
    def timestamp_display(self) -> str:
        start_min, start_sec = divmod(int(self.start_time), 60)
        end_min, end_sec = divmod(int(self.end_time), 60)
        if self.start_time >= 3600 or self.end_time >= 3600:
            start_hr, start_min = divmod(start_min, 60)
            end_hr, end_min = divmod(end_min, 60)
            return f"{start_hr:d}:{start_min:02d}:{start_sec:02d} - {end_hr:d}:{end_min:02d}:{end_sec:02d}"
        return f"{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}"


class VideoInfo(BaseModel):
    video_id: str
    source_type: VideoSourceType
    source_url: str | None = None
    file_path: str | None = None

    title: str = ""
    description: str = ""
    duration: float = 0.0
    upload_date: str | None = None
    language: str = "en"

    channel_name: str | None = None
    channel_url: str | None = None

    view_count: int | None = None
    like_count: int | None = None

    tags: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    thumbnail_url: str | None = None

    chapters: list[Chapter] = Field(default_factory=list)

    transcript_source: TranscriptSource = TranscriptSource.NONE


class VideoSourceConfig(BaseModel):
    url: str | None = None
    languages: list[str] | None = None
    time_window_seconds: float = 120.0
    clip_start: float | None = None
    clip_end: float | None = None
