# tests/unit/models/test_errors.py
from src.models.errors import ErrorDetail, Errors, TypelessError


def test_error_detail_creation():
    detail = ErrorDetail(code="TEST_ERROR", message="Test message", context={"key": "value"})
    assert detail.code == "TEST_ERROR"
    assert detail.message == "Test message"
    assert detail.context == {"key": "value"}


def test_typeless_error_creation():
    error = TypelessError(code="TEST_ERROR", message="Test message", key="value")
    assert isinstance(error.detail, ErrorDetail)
    assert error.detail.code == "TEST_ERROR"
    assert str(error) == "Test message"


def test_predefined_error_codes():
    assert hasattr(Errors, "FILE_NOT_FOUND")
    assert hasattr(Errors, "INVALID_DATA_FORMAT")
    assert hasattr(Errors, "ANALYSIS_FAILED")
    assert Errors.FILE_NOT_FOUND == "FILE_NOT_FOUND"
