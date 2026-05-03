"""Tests for the slide planner logic."""

import sys
from pathlib import Path

# Ensure the project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.slide_planner import _extract_bullets, _suggest_slide_type, plan_slides
from api.video.models import (
    FrameType,
    KeyFrame,
    SegmentContentType,
    VideoInfo,
    VideoSegment,
    VideoSourceType,
)


class TestExtractBullets:
    def test_extracts_from_long_transcript(self):
        text = (
            "React hooks allow you to use state in functional components. "
            "This is important because it simplifies your code significantly. "
            "You should always call hooks at the top level of your component. "
            "Never call hooks inside loops or conditions."
        )
        bullets = _extract_bullets(text, max_bullets=3)
        assert len(bullets) <= 3
        assert all(isinstance(b, str) for b in bullets)

    def test_returns_fallback_for_short_text(self):
        bullets = _extract_bullets("Hello world.", max_bullets=3)
        assert len(bullets) >= 1

    def test_respects_max_bullets(self):
        text = ". ".join([f"This is sentence number {i} which is long enough" for i in range(20)])
        bullets = _extract_bullets(text, max_bullets=2)
        assert len(bullets) <= 2


class TestSuggestSlideType:
    def _make_segment(self, content_type, has_code=False):
        return VideoSegment(
            index=0, start_time=0, end_time=60, duration=60,
            content_type=content_type, has_code_on_screen=has_code,
        )

    def test_first_segment_is_title(self):
        seg = self._make_segment(SegmentContentType.EXPLANATION)
        assert _suggest_slide_type(seg, None, is_first=True, is_last=False) == "title"

    def test_last_segment_is_summary(self):
        seg = self._make_segment(SegmentContentType.EXPLANATION)
        assert _suggest_slide_type(seg, None, is_first=False, is_last=True) == "summary"

    def test_live_coding_is_code(self):
        seg = self._make_segment(SegmentContentType.LIVE_CODING)
        assert _suggest_slide_type(seg, None, is_first=False, is_last=False) == "code"

    def test_slide_keyframe_is_image(self):
        seg = self._make_segment(SegmentContentType.EXPLANATION)
        kf = KeyFrame(timestamp=30.0, frame_type=FrameType.SLIDE)
        assert _suggest_slide_type(seg, kf, is_first=False, is_last=False) == "image"

    def test_default_is_content(self):
        seg = self._make_segment(SegmentContentType.EXPLANATION)
        assert _suggest_slide_type(seg, None, is_first=False, is_last=False) == "content"

    def test_intro_is_title(self):
        seg = self._make_segment(SegmentContentType.INTRO)
        assert _suggest_slide_type(seg, None, is_first=False, is_last=False) == "title"

    def test_outro_is_summary(self):
        seg = self._make_segment(SegmentContentType.OUTRO)
        assert _suggest_slide_type(seg, None, is_first=False, is_last=False) == "summary"


class TestPlanSlides:
    def test_generates_outline(self, sample_video_info, sample_segments):
        outline = plan_slides(sample_video_info, sample_segments, keyframes=[], max_slides=30)
        assert len(outline) > 0
        assert outline[0].type == "title"
        assert outline[-1].type == "summary"

    def test_respects_max_slides(self, sample_video_info, sample_segments):
        outline = plan_slides(sample_video_info, sample_segments, keyframes=[], max_slides=2)
        assert len(outline) <= 2

    def test_slide_numbers_sequential(self, sample_video_info, sample_segments):
        outline = plan_slides(sample_video_info, sample_segments, keyframes=[], max_slides=30)
        for i, slide in enumerate(outline):
            assert slide.slide_number == i + 1

    def test_title_slide_uses_video_title(self, sample_video_info, sample_segments):
        outline = plan_slides(sample_video_info, sample_segments, keyframes=[], max_slides=30)
        assert outline[0].title == sample_video_info.title
