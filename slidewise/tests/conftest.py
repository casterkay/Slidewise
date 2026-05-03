"""Shared test fixtures for Slidewise."""

import pytest

from api.video.models import (
    Chapter,
    SegmentContentType,
    TranscriptSegment,
    TranscriptSource,
    VideoInfo,
    VideoSegment,
    VideoSourceType,
)


@pytest.fixture
def sample_video_info():
    return VideoInfo(
        video_id="test123abc",
        source_type=VideoSourceType.YOUTUBE,
        source_url="https://www.youtube.com/watch?v=test123abc",
        title="Test Video: Python Basics",
        description="A tutorial on Python basics",
        duration=600.0,
        upload_date="20260401",
        language="en",
        channel_name="Python Academy",
        chapters=[
            Chapter(title="Introduction", start_time=0.0, end_time=60.0),
            Chapter(title="Variables", start_time=60.0, end_time=240.0),
            Chapter(title="Functions", start_time=240.0, end_time=480.0),
            Chapter(title="Summary", start_time=480.0, end_time=600.0),
        ],
    )


@pytest.fixture
def sample_transcript_segments():
    return [
        TranscriptSegment(
            text="Welcome to this tutorial on Python basics. Today we will learn about variables and functions.",
            start=0.0, end=15.0, confidence=1.0, source=TranscriptSource.YOUTUBE_MANUAL,
        ),
        TranscriptSegment(
            text="Let's get started with the basics of Python programming.",
            start=15.0, end=30.0, confidence=1.0, source=TranscriptSource.YOUTUBE_MANUAL,
        ),
        TranscriptSegment(
            text="A variable is a name that refers to a value. In Python you can create a variable by assigning a value.",
            start=60.0, end=80.0, confidence=1.0, source=TranscriptSource.YOUTUBE_MANUAL,
        ),
        TranscriptSegment(
            text="For example, x equals 5, name equals hello. Python uses dynamic typing so you don't need to declare types.",
            start=80.0, end=100.0, confidence=1.0, source=TranscriptSource.YOUTUBE_MANUAL,
        ),
        TranscriptSegment(
            text="Now let's talk about functions. You define a function using the def keyword. def greet name: print hello name.",
            start=240.0, end=270.0, confidence=1.0, source=TranscriptSource.YOUTUBE_MANUAL,
        ),
        TranscriptSegment(
            text="Functions can take parameters and return values. import os and import sys are common imports you'll use.",
            start=270.0, end=300.0, confidence=1.0, source=TranscriptSource.YOUTUBE_MANUAL,
        ),
        TranscriptSegment(
            text="That's it for today. Thanks for watching and subscribe for more Python tutorials. See you next time!",
            start=480.0, end=510.0, confidence=1.0, source=TranscriptSource.YOUTUBE_MANUAL,
        ),
    ]


@pytest.fixture
def sample_segments():
    return [
        VideoSegment(
            index=0, start_time=0.0, end_time=60.0, duration=60.0,
            transcript="Welcome to this tutorial. Let's get started.",
            content_type=SegmentContentType.INTRO,
            chapter_title="Introduction",
            speaker_notes="Welcome to this tutorial. Let's get started.",
        ),
        VideoSegment(
            index=1, start_time=60.0, end_time=240.0, duration=180.0,
            transcript="Variables store values. x equals 5. Python uses dynamic typing.",
            content_type=SegmentContentType.EXPLANATION,
            chapter_title="Variables",
            speaker_notes="Variables store values. x equals 5. Python uses dynamic typing.",
        ),
        VideoSegment(
            index=2, start_time=240.0, end_time=480.0, duration=240.0,
            transcript="Functions use def keyword. import os and import sys. def greet name print hello.",
            content_type=SegmentContentType.LIVE_CODING,
            chapter_title="Functions",
            speaker_notes="Functions use def keyword. import os and import sys. def greet name print hello.",
        ),
        VideoSegment(
            index=3, start_time=480.0, end_time=600.0, duration=120.0,
            transcript="Thanks for watching. Subscribe for more. See you next time!",
            content_type=SegmentContentType.OUTRO,
            chapter_title="Summary",
            speaker_notes="Thanks for watching. Subscribe for more. See you next time!",
        ),
    ]
