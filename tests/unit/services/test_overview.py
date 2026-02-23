# tests/unit/services/test_overview.py
from src.models.analysis import OverviewStats
from src.models.transcription import Transcription, TranscriptionList
from src.services.overview import OverviewService


def test_overview_service_get_stats():
    data = TranscriptionList(
        items=[
            Transcription(id="1", timestamp=1737550800, content="测试", duration=10.0),
            Transcription(
                id="2", timestamp=1737554400, content="Another test content here", duration=15.0
            ),
        ]
    )
    service = OverviewService(data)

    stats = service.get_stats()

    assert isinstance(stats, OverviewStats)
    assert stats.total_records == 2
    assert stats.total_words == 27
    assert stats.active_days == 1


def test_overview_calculates_daily_avg():
    data = TranscriptionList(
        items=[
            Transcription(id="1", timestamp=1737550800, content="a", duration=10.0),
            Transcription(id="2", timestamp=1737637200, content="b", duration=10.0),
        ]
    )
    service = OverviewService(data)

    stats = service.get_stats()

    # 2 records over 2 days = 1.0 daily avg
    assert stats.daily_avg == 1.0


def test_overview_empty_stats():
    data = TranscriptionList(items=[])
    service = OverviewService(data)

    stats = service.get_stats()

    assert stats.total_records == 0
    assert stats.total_words == 0
