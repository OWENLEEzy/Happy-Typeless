# src/models/errors.py
from typing import Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Structured error detail"""

    code: str
    message: str
    context: dict[str, Any] = {}


class TypelessError(Exception):
    """Unified exception class"""

    def __init__(self, code: str, message: str, **context):
        self.detail = ErrorDetail(code=code, message=message, context=context)
        super().__init__(message)


class Errors:
    """Predefined error codes"""

    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    INVALID_DATA_FORMAT = "INVALID_DATA_FORMAT"
    ANALYSIS_FAILED = "ANALYSIS_FAILED"
    REPORT_GENERATION_FAILED = "REPORT_GENERATION_FAILED"
    UNSUPPORTED_LANGUAGE = "UNSUPPORTED_LANGUAGE"
