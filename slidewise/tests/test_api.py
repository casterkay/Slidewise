"""Tests for the FastAPI endpoints (mocked pipeline)."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.auth import validate_api_key
from api.main import app
from api.models import ExtractResponse, SegmentOut, SlideOutline, VideoMeta
from api.video.models import SegmentContentType


# Override the auth dependency for all tests
async def _mock_api_key():
    return {"id": "key-123", "user_id": "user-1", "name": "test"}


app.dependency_overrides[validate_api_key] = _mock_api_key


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_response():
    return ExtractResponse(
        job_id="test123",
        video=VideoMeta(
            title="Test Video",
            duration=300.0,
            channel="Test Channel",
            chapters=[],
        ),
        segments=[
            SegmentOut(
                index=0,
                title="Intro",
                start_time=0.0,
                end_time=60.0,
                transcript="Hello world",
                content_type=SegmentContentType.INTRO,
                suggested_slide_type="title",
                speaker_notes="Hello world",
            )
        ],
        slide_outline=[
            SlideOutline(
                slide_number=1,
                type="title",
                title="Test Video",
                subtitle="by Test Channel",
                source_segment=0,
            )
        ],
        processing_time_seconds=1.5,
    )


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"


class TestRootEndpoint:
    def test_root_returns_info(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "Slidewise" in resp.json()["service"]


class TestExtractEndpoint:
    def test_extract_requires_url_or_file(self, client):
        resp = client.post(
            "/api/v1/extract",
            json={"options": {}},
            headers={"X-API-Key": "test_key"},
        )
        assert resp.status_code == 422

    def test_extract_returns_result(self, client, mock_response):
        with patch("api.main.pipeline") as mock_pipeline, \
             patch("api.main.log_usage"):
            mock_pipeline.extract.return_value = mock_response
            resp = client.post(
                "/api/v1/extract",
                json={"url": "https://www.youtube.com/watch?v=test123", "options": {}},
                headers={"X-API-Key": "test_key"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert data["video"]["title"] == "Test Video"
        assert len(data["segments"]) == 1
        assert len(data["slide_outline"]) == 1
