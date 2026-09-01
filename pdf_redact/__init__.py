"""Offline, verifiable PDF redaction for documents containing sensitive data."""

from .patterns import ALL_PATTERNS, DEFAULT_PATTERNS, Pattern, REGISTRY
from .redactor import FileResult, Match, redact_file
from .verify import verify_output

__version__ = "1.0.0"

__all__ = [
    "ALL_PATTERNS",
    "DEFAULT_PATTERNS",
    "FileResult",
    "Match",
    "Pattern",
    "REGISTRY",
    "redact_file",
    "verify_output",
]
