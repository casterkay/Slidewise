"""Slidewise API — FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.auth import log_usage, validate_api_key
from api.models import ExtractRequest, ExtractResponse
from api.pipeline import SlidewisePipeline

logger = logging.getLogger(__name__)

pipeline = SlidewisePipeline()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(name)s: %(message)s")
    logger.info("Slidewise API starting")
    yield
    logger.info("Slidewise API shutting down")


app = FastAPI(
    title="Slidewise",
    description="Turn videos into beautiful slides. Extracts transcripts, keyframes, and generates slide outlines.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "Slidewise",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "0.1.0"}


@app.post("/api/v1/extract", response_model=ExtractResponse)
async def extract_video(
    request: ExtractRequest,
    api_key_info: dict = Depends(validate_api_key),
):
    """Extract video content and generate a slide outline.

    Requires a valid API key via X-API-Key header.
    """
    if not request.url and not request.file_path:
        raise HTTPException(status_code=422, detail="Either 'url' or 'file_path' is required")

    try:
        result = pipeline.extract(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Log usage
    if result.job_id:
        try:
            log_usage(api_key_info["id"], result.job_id, result.processing_time_seconds)
        except Exception:
            logger.warning("Failed to log usage", exc_info=True)

    return result
