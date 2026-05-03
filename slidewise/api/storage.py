"""Supabase Storage helpers for keyframe images."""

import base64
import logging

from api.config import settings
from api.supabase_client import get_supabase

logger = logging.getLogger(__name__)


def upload_keyframe(job_id: str, segment_index: int, image_base64: str) -> str:
    """Upload a base64 keyframe image to Supabase Storage.

    Returns the storage path (bucket-relative).
    """
    sb = get_supabase()
    bucket = settings.storage_bucket

    # Strip data URI prefix if present
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)
    path = f"{job_id}/segment_{segment_index:03d}.jpg"

    sb.storage.from_(bucket).upload(
        path,
        image_bytes,
        file_options={"content-type": "image/jpeg"},
    )

    return path


def get_keyframe_url(path: str) -> str:
    """Get a signed URL for a keyframe image."""
    sb = get_supabase()
    bucket = settings.storage_bucket
    result = sb.storage.from_(bucket).create_signed_url(path, 3600)
    return result.get("signedURL", "")
