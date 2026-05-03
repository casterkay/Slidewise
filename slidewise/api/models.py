"""Pydantic request/response schemas for the Slidewise API."""

from __future__ import annotations

from pydantic import BaseModel, Field

from api.video.models import KeyFrame, SegmentContentType, VideoSegment


# =============================================================================
# Request
# =============================================================================


class ExtractOptions(BaseModel):
    extract_keyframes: bool = False
    max_slides: int = 30
    language: str = "en"
    time_window_seconds: float = 120.0


class ExtractRequest(BaseModel):
    url: str | None = None
    file_path: str | None = None
    options: ExtractOptions = Field(default_factory=ExtractOptions)


# =============================================================================
# Response
# =============================================================================


class VideoMeta(BaseModel):
    title: str
    duration: float
    channel: str | None = None
    url: str | None = None
    thumbnail_url: str | None = None
    upload_date: str | None = None
    chapters: list[ChapterOut] = Field(default_factory=list)


class ChapterOut(BaseModel):
    title: str
    start_time: float
    end_time: float


class SegmentOut(BaseModel):
    index: int
    title: str
    start_time: float
    end_time: float
    transcript: str
    content_type: SegmentContentType
    suggested_slide_type: str
    keyframe: KeyFrame | None = None
    code_blocks: list[dict] = Field(default_factory=list)
    speaker_notes: str = ""


class SlideOutline(BaseModel):
    slide_number: int
    type: str  # title, content, code, image, summary, divider
    title: str
    subtitle: str | None = None
    bullets: list[str] | None = None
    code: str | None = None
    code_language: str | None = None
    has_image: bool = False
    source_segment: int | None = None


class ExtractResponse(BaseModel):
    status: str = "success"
    job_id: str | None = None
    video: VideoMeta
    segments: list[SegmentOut]
    slide_outline: list[SlideOutline]
    processing_time_seconds: float = 0.0


# Rebuild models that have forward references
VideoMeta.model_rebuild()
