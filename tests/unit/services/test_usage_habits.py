import datetime

from src.models.transcription import Transcription, TranscriptionList
from src.services.usage_habits import UsageHabitsService


def _make_list(dates: list[str]) -> TranscriptionList:
    """Create TranscriptionList from list of YYYY-MM-DD date strings."""
    items = [
        Transcription(
            id=f"t{i}",
            timestamp=int(
                datetime.datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=datetime.UTC).timestamp()
            ),
            content="test",
        )
        for i, d in enumerate(dates)
    ]
    return TranscriptionList(items=items)


def test_consecutive_days_simple():
    data = _make_list(["2024-01-01", "2024-01-02", "2024-01-03"])
    habits = UsageHabitsService(data).get_habits()
    assert habits.consecutive_days == 3


def test_consecutive_days_with_gap():
    data = _make_list(["2024-01-01", "2024-01-02", "2024-01-05"])
    habits = UsageHabitsService(data).get_habits()
    assert habits.consecutive_days == 2


def test_gap_days_correct():
    """gap_days = date_range - active_days, not date_range - consecutive_days."""
    # date_range = 5 (Jan 1 to Jan 5), active_days = 3, gap_days = 2
    data = _make_list(["2024-01-01", "2024-01-02", "2024-01-05"])
    habits = UsageHabitsService(data).get_habits()
    assert habits.active_days == 3
    assert habits.gap_days == 2  # 5 - 3 = 2


def test_empty_data():
    data = TranscriptionList()
    habits = UsageHabitsService(data).get_habits()
    assert habits.consecutive_days == 0
    assert habits.active_days == 0
    assert habits.gap_days == 0


def test_single_day():
    data = _make_list(["2024-01-15"])
    habits = UsageHabitsService(data).get_habits()
    assert habits.consecutive_days == 1
    assert habits.gap_days == 0
