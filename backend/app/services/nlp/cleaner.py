"""Text Preprocessing and Cleaning Service (Member 2 Focus)."""
import re


class TextCleaner:
    """Preprocesses and sanitizes unstructured resume and job description text."""

    @staticmethod
    def clean(text: str) -> str:
        """Strip URLs, emails, special characters, and normalize whitespaces."""
        # Stub: Member 2 to implement regex sanitization and normalization
        pass

    @staticmethod
    def remove_stopwords(text: str) -> str:
        """Filter out common English stop words while preserving domain keywords."""
        # Stub: Member 2 to implement stopword filtering using NLTK/custom list
        pass
