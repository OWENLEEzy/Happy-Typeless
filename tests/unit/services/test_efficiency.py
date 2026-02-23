import datetime

from src.models.transcription import Transcription, TranscriptionList
from src.services.efficiency import EfficiencyService


def _make_list_with_hours(hour_durations: list[tuple[int, float]]) -> TranscriptionList:
    """Create TranscriptionList with entries at specific hours.

    Args:
        hour_durations: List of (hour_of_day, duration_seconds) tuples
    """
    items = []
    for i, (hour, duration) in enumerate(hour_durations):
        dt = datetime.datetime(2024, 1, 15, hour, 0, 0, tzinfo=datetime.UTC)
        items.append(
            Transcription(
                id=f"t{i}",
                timestamp=int(dt.timestamp()),
                content="test content that is long enough",
                duration=duration,
            )
        )
    return TranscriptionList(items=items)


def test_empty_data():
    data = TranscriptionList()
    metrics = EfficiencyService(data).get_metrics()
    assert metrics.scores.overall == 0


def test_work_hours_boost_efficiency():
    """Entries during work hours (9-17) should score higher work efficiency."""
    work_data = _make_list_with_hours([(10, 30.0), (14, 30.0), (16, 30.0)])
    night_data = _make_list_with_hours([(1, 30.0), (2, 30.0), (3, 30.0)])

    work_metrics = EfficiencyService(work_data).get_metrics()
    night_metrics = EfficiencyService(night_data).get_metrics()

    assert work_metrics.scores.work_efficiency > night_metrics.scores.work_efficiency


def test_scores_in_range():
    data = _make_list_with_hours([(9, 45.0), (13, 60.0), (15, 30.0)])
    metrics = EfficiencyService(data).get_metrics()
    assert 0 <= metrics.scores.sleep_health <= 100
    assert 0 <= metrics.scores.work_efficiency <= 100
    assert 0 <= metrics.scores.focus <= 100
    assert 0 <= metrics.scores.overall <= 100
