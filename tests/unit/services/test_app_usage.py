# tests/unit/services/test_app_usage.py
"""Tests for AppUsageService."""

import pytest

from src.models.transcription import Transcription, TranscriptionList
from src.services.app_usage import AppUsageService


@pytest.fixture
def sample_data():
    """Create sample transcription data with app names."""
    return TranscriptionList(
        items=[
            Transcription(
                id="1",
                timestamp=1609459200,
                content="Hello world",
                duration=5.0,
                app_name="VS Code",
                window_title="main.py",
            ),
            Transcription(
                id="2",
                timestamp=1609459260,
                content="Testing code",
                duration=10.0,
                app_name="VS Code",
                window_title="test.py",
            ),
            Transcription(
                id="3",
                timestamp=1609459320,
                content="Browse web",
                duration=3.0,
                app_name="Chrome",
                window_title="Google",
            ),
            Transcription(
                id="4",
                timestamp=1609459380,
                content="No app",
                duration=2.0,
                app_name=None,
                window_title=None,
            ),
            Transcription(
                id="5",
                timestamp=1609459440,
                content="Message",
                duration=4.0,
                app_name="Slack",
                window_title="general",
            ),
        ]
    )


def test_get_app_usage_with_data(sample_data):
    """Test app usage calculation with sample data."""
    service = AppUsageService(sample_data)
    result = service.get_app_usage()

    assert result.has_data is True
    assert result.total == 5
    assert result.unique_apps == 3  # VS Code, Chrome, Slack

    # VS Code should be top app with 2 uses
    assert result.apps[0].app_name == "VS Code"
    assert result.apps[0].count == 2
    assert result.apps[0].ratio == 0.4

    # Chrome second with 1 use
    assert result.apps[1].app_name == "Chrome"
    assert result.apps[1].count == 1
    assert result.apps[1].ratio == 0.2

    # Slack third with 1 use
    assert result.apps[2].app_name == "Slack"
    assert result.apps[2].count == 1

    # Check average duration for VS Code
    assert result.apps[0].avg_duration == 7.5  # (5.0 + 10.0) / 2


def test_get_app_usage_empty():
    """Test app usage with empty data."""
    service = AppUsageService(TranscriptionList(items=[]))
    result = service.get_app_usage()

    assert result.has_data is False
    assert result.total == 0
    assert result.unique_apps == 0
    assert result.apps == []


def test_get_app_usage_no_app_names():
    """Test app usage when no app names are present."""
    data = TranscriptionList(
        items=[
            Transcription(
                id="1", timestamp=1609459200, content="Hello", duration=5.0, app_name=None
            ),
            Transcription(id="2", timestamp=1609459260, content="World", duration=3.0, app_name=""),
        ]
    )
    service = AppUsageService(data)
    result = service.get_app_usage()

    assert result.has_data is False
    assert result.total == 2
    assert result.unique_apps == 0
    assert result.apps == []
