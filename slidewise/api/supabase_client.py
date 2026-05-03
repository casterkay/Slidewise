"""Supabase client singleton for DB, Auth, and Storage."""

from functools import lru_cache

from supabase import Client, create_client

from api.config import settings


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    """Return a cached Supabase client using the service role key."""
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def get_anon_client() -> Client:
    """Return a Supabase client using the anon key (for RLS-scoped access)."""
    return create_client(settings.supabase_url, settings.supabase_anon_key)
