# tests/unit/models/test_analysis.py
from src.models.analysis import (
    OverviewStats,
    UsageHabits,
)


def test_overview_stats():
    stats = OverviewStats(
        total_records=100,
        total_words=5000,
        total_duration=150.5,
        active_days=30,
        date_range_days=45,
        daily_avg=2.2,
        avg_words=50.0,
        avg_duration=15.5,
        start_date="2025-01-01",
        end_date="2025-02-15",
    )
    assert stats.total_records == 100
    assert stats.total_words == 5000
    assert stats.daily_avg == 2.2


def test_usage_habits():
    habits = UsageHabits(
        consecutive_days=7,
        active_days=30,
        gap_days=15,
        busiest_week=25,
        laziest_week=2,
        week_ratio=12.5,
    )
    assert habits.consecutive_days == 7
    assert habits.week_ratio == 12.5
