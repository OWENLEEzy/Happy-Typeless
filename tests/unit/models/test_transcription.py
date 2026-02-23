# tests/unit/models/test_transcription.py
from datetime import datetime

from src.models.transcription import Transcription, TranscriptionList


def test_transcription_creation():
    t = Transcription(id="123", timestamp=1737550800, content="测试内容")
    assert t.id == "123"
    assert t.content == "测试内容"
    assert t.duration is None
    assert t.app_name is None


def test_transcription_with_optional_fields():
    t = Transcription(
        id="123",
        timestamp=1737550800,
        content="测试内容",
        duration=15.5,
        app_name="WeChat",
        window_title="Chat",
    )
    assert t.duration == 15.5
    assert t.app_name == "WeChat"
    assert t.window_title == "Chat"


def test_transcription_datetime_property():
    t = Transcription(id="123", timestamp=1737550800, content="测试")
    dt = t.datetime
    assert isinstance(dt, datetime)
    assert dt.year == 2025
    assert dt.month == 1
    assert dt.day == 22


def test_transcription_date_property():
    t = Transcription(id="123", timestamp=1737550800, content="测试")
    assert t.date == "2025-01-22"


def test_transcription_list():
    items = [
        Transcription(id="1", timestamp=1000, content="a"),
        Transcription(id="2", timestamp=2000, content="b"),
    ]
    tl = TranscriptionList(items=items)
    assert len(tl) == 2
    assert list(tl) == items


def test_transcription_list_iteration():
    items = [
        Transcription(id="1", timestamp=1000, content="a"),
        Transcription(id="2", timestamp=2000, content="b"),
    ]
    tl = TranscriptionList(items=items)
    result = [t for t in tl]
    assert len(result) == 2
    assert result[0].id == "1"
