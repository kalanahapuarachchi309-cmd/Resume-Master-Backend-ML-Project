"""Cloudinary Cloud Storage Integration Service (Mahen & Team)."""
import os
import uuid
import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    _has_cloudinary = True
except ImportError:
    _has_cloudinary = False

from app.core.config import settings


class CloudinaryService:
    """Uploads and manages resume documents in Cloudinary CDN."""

    _initialized = False

    @classmethod
    def _init_cloudinary(cls):
        """Initialize Cloudinary client with credentials."""
        if not cls._initialized and _has_cloudinary:
            if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
                cloudinary.config(
                    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                    api_key=settings.CLOUDINARY_API_KEY,
                    api_secret=settings.CLOUDINARY_API_SECRET,
                    secure=True,
                )
                cls._initialized = True
                logger.info(f"Cloudinary successfully configured for cloud: {settings.CLOUDINARY_CLOUD_NAME}")

    @classmethod
    def upload_resume(cls, file_bytes: bytes, filename: str) -> Optional[str]:
        """Upload resume bytes to Cloudinary raw storage and return secure HTTPS URL."""
        if not _has_cloudinary or not file_bytes:
            return None

        cls._init_cloudinary()

        try:
            # Generate safe public_id with unique prefix to avoid collision while retaining readable filename
            clean_name = os.path.splitext(filename)[0]
            clean_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in clean_name).strip("_")
            public_id = f"{clean_name}_{uuid.uuid4().hex[:8]}"

            folder = settings.CLOUDINARY_FOLDER or "resume_master"

            upload_result = cloudinary.uploader.upload(
                file_bytes,
                resource_type="raw",
                folder=folder,
                public_id=public_id,
                overwrite=True,
            )

            secure_url = upload_result.get("secure_url") or upload_result.get("url")
            logger.info(f"Uploaded resume '{filename}' to Cloudinary: {secure_url}")
            return secure_url
        except Exception as e:
            logger.error(f"Cloudinary upload failed for '{filename}': {e}")
            return None
