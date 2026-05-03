"""API key authentication via Supabase api_keys table."""

import hashlib
import logging
from datetime import datetime, timezone

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from api.supabase_client import get_supabase

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key")


def _hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


async def validate_api_key(api_key: str = Security(api_key_header)) -> dict:
    """Validate an API key against the Supabase api_keys table.

    Returns the key row (id, user_id, name) on success.
    """
    sb = get_supabase()
    key_hash = _hash_key(api_key)

    result = (
        sb.table("api_keys")
        .select("id, user_id, name")
        .eq("key_hash", key_hash)
        .eq("revoked", False)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid or revoked API key")

    key_row = result.data[0]

    # Update last_used_at
    sb.table("api_keys").update(
        {"last_used_at": datetime.now(timezone.utc).isoformat()}
    ).eq("id", key_row["id"]).execute()

    return key_row


def log_usage(api_key_id: str, job_id: str, processing_time: float):
    """Record API usage for billing/analytics."""
    sb = get_supabase()
    sb.table("usage_log").insert({
        "api_key_id": api_key_id,
        "job_id": job_id,
        "processing_time_seconds": processing_time,
    }).execute()
