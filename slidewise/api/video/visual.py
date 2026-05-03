"""Simplified keyframe extraction — one representative frame per segment."""

import base64
import io
import logging
import os
import tempfile

from api.video.models import FrameType, KeyFrame, VideoSegment

logger = logging.getLogger(__name__)

try:
    import cv2

    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from PIL import Image

    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import yt_dlp

    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False


def download_video(url: str, output_dir: str) -> str:
    """Download video to a temp directory, return file path."""
    if not HAS_YTDLP:
        raise RuntimeError("yt-dlp required for video download")

    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(id)s.%(ext)s")

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "outtmpl": output_template,
        "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    if not os.path.exists(filename):
        # Try mp4 extension
        base = os.path.splitext(filename)[0]
        filename = base + ".mp4"

    return filename


def _classify_frame(frame) -> FrameType:
    """Simple heuristic frame classification based on color distribution."""
    if not HAS_CV2:
        return FrameType.OTHER

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = gray.mean()

    # Dark frames likely code editors/terminals
    if mean_brightness < 60:
        return FrameType.CODE_EDITOR
    # Very bright, uniform frames likely slides
    if mean_brightness > 200:
        return FrameType.SLIDE

    # Check edge density for diagrams
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = edges.mean() / 255.0
    if edge_ratio > 0.15:
        return FrameType.DIAGRAM

    return FrameType.SCREENCAST


def _frame_to_base64(frame, quality: int = 85) -> str:
    """Encode an OpenCV frame as base64 JPEG data URI."""
    if not HAS_PIL:
        # Fallback to cv2 encoding
        _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        return "data:image/jpeg;base64," + base64.b64encode(buf.tobytes()).decode()

    # Convert BGR to RGB for PIL
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def extract_keyframes(
    video_path: str,
    segments: list[VideoSegment],
    quality: int = 85,
) -> list[KeyFrame]:
    """Extract one representative keyframe per segment (at midpoint)."""
    if not HAS_CV2:
        logger.warning("opencv not available — skipping keyframe extraction")
        return []

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error(f"Cannot open video: {video_path}")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    keyframes = []

    for segment in segments:
        midpoint = (segment.start_time + segment.end_time) / 2.0
        frame_number = int(midpoint * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if not ret:
            continue

        frame_type = _classify_frame(frame)
        image_b64 = _frame_to_base64(frame, quality)

        keyframes.append(
            KeyFrame(
                timestamp=midpoint,
                image_base64=image_b64,
                frame_type=frame_type,
            )
        )

    cap.release()
    return keyframes
