"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    storage_bucket: str = "keyframes"

    # Processing
    max_video_duration: int = 7200  # seconds
    max_upload_size_mb: int = 500
    temp_dir: str = "/tmp/slidewise"
    keyframe_quality: int = 85  # JPEG quality

    model_config = {"env_prefix": "SLIDEWISE_"}


settings = Settings()
