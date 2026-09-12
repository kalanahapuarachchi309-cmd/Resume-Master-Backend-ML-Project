"""PDF Document Parser Service (Mahen & Team)."""
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class PDFParser:
    """Extracts clean text content from PDF resume files using pdfplumber / pypdf."""

    @staticmethod
    def validate_file(file_bytes: bytes) -> bool:
        """Verify that the byte stream has a valid PDF magic number header."""
        return file_bytes.startswith(b"%PDF")

    @classmethod
    def extract_text(cls, file_bytes: bytes) -> str:
        """Extract multi-column text from PDF raw bytes while preserving reading structure."""
        if not file_bytes:
            return ""

        extracted_pages = []

        # 1. Try pdfplumber first (best for multi-column resumes)
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text and text.strip():
                        extracted_pages.append(text.strip())
            if extracted_pages:
                return "\n\n".join(extracted_pages)
        except Exception as e:
            logger.debug(f"pdfplumber extraction skipped or failed: {e}")

        # 2. Fallback to pypdf
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                text = page.extract_text()
                if text and text.strip():
                    extracted_pages.append(text.strip())
            if extracted_pages:
                return "\n\n".join(extracted_pages)
        except Exception as e:
            logger.error(f"pypdf extraction error: {e}")

        return ""
