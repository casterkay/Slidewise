"""Orchestrator: URL → structured extraction package."""

import logging
import os
import shutil
import time
import uuid

from api.config import settings
from api.models import (
    ChapterOut,
    ExtractRequest,
    ExtractResponse,
    SegmentOut,
    VideoMeta,
)
from api.slide_planner import plan_slides
from api.video.metadata import (
    detect_video_source_type,
    extract_local_metadata,
    extract_youtube_metadata,
)
from api.video.models import VideoSourceConfig, VideoSourceType
from api.video.segmenter import segment_video
from api.video.transcript import get_transcript
from api.video.visual import download_video, extract_keyframes

logger = logging.getLogger(__name__)


class SlidewisePipeline:
    def extract(self, request: ExtractRequest) -> ExtractResponse:
        start = time.time()
        job_id = uuid.uuid4().hex[:12]

        # Phase 1: Resolve source
        source = request.url or request.file_path or ""
        source_type = detect_video_source_type(source)

        # Phase 2: Metadata
        if source_type == VideoSourceType.YOUTUBE:
            video_info = extract_youtube_metadata(source)
        else:
            video_info = extract_local_metadata(source)

        # Check duration limit
        if video_info.duration > settings.max_video_duration:
            raise ValueError(
                f"Video duration ({video_info.duration:.0f}s) exceeds limit "
                f"({settings.max_video_duration}s)"
            )

        # Phase 3: Transcript
        config = VideoSourceConfig(
            url=request.url,
            languages=[request.options.language],
            time_window_seconds=request.options.time_window_seconds,
        )
        transcript_segments, transcript_source = get_transcript(video_info, config)
        video_info.transcript_source = transcript_source

        # Phase 4: Segmentation
        segments = segment_video(video_info, transcript_segments, config)

        # Phase 5: Keyframes (optional)
        keyframes = []
        video_path = None
        if request.options.extract_keyframes and segments:
            try:
                temp_dir = os.path.join(settings.temp_dir, job_id)
                if source_type == VideoSourceType.YOUTUBE:
                    video_path = download_video(source, temp_dir)
                elif video_info.file_path:
                    video_path = video_info.file_path

                if video_path and os.path.exists(video_path):
                    keyframes = extract_keyframes(
                        video_path, segments, settings.keyframe_quality
                    )
                    # Attach keyframes to segments
                    for i, kf in enumerate(keyframes):
                        if i < len(segments):
                            segments[i].keyframe = kf
            except Exception as e:
                logger.warning(f"Keyframe extraction failed: {e}")
            finally:
                # Cleanup downloaded video
                temp_dir = os.path.join(settings.temp_dir, job_id)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)

        # Phase 6: Slide planning
        slide_outline = plan_slides(
            video_info, segments, keyframes, request.options.max_slides
        )

        # Update suggested_slide_type on segments
        for slide in slide_outline:
            if slide.source_segment is not None and slide.source_segment < len(segments):
                segments[slide.source_segment].suggested_slide_type = slide.type

        elapsed = time.time() - start

        # Build response
        return ExtractResponse(
            job_id=job_id,
            video=VideoMeta(
                title=video_info.title,
                duration=video_info.duration,
                channel=video_info.channel_name,
                url=video_info.source_url,
                thumbnail_url=video_info.thumbnail_url,
                upload_date=video_info.upload_date,
                chapters=[
                    ChapterOut(
                        title=ch.title,
                        start_time=ch.start_time,
                        end_time=ch.end_time,
                    )
                    for ch in video_info.chapters
                ],
            ),
            segments=[
                SegmentOut(
                    index=seg.index,
                    title=seg.chapter_title or f"Part {seg.index + 1}",
                    start_time=seg.start_time,
                    end_time=seg.end_time,
                    transcript=seg.transcript,
                    content_type=seg.content_type,
                    suggested_slide_type=seg.suggested_slide_type,
                    keyframe=seg.keyframe,
                    code_blocks=[cb.model_dump() for cb in seg.detected_code_blocks],
                    speaker_notes=seg.speaker_notes,
                )
                for seg in segments
            ],
            slide_outline=slide_outline,
            processing_time_seconds=round(elapsed, 2),
        )
