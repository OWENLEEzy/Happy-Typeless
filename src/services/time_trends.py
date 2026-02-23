# src/services/time_trends.py
from collections import Counter

from src.models.analysis import DateEntry, TimeTrends
from src.models.transcription import TranscriptionList


class TimeTrendsService:
    """Service for time trend analysis"""

    def __init__(self, data: TranscriptionList):
        self.data = data

    def get_trends(self) -> TimeTrends:
        """Calculate time trends

        Returns:
            TimeTrends with daily trends, hourly distribution, and top dates
        """
        if len(self.data) == 0:
            return self._empty_trends()

        hour_distribution = self._get_hour_distribution()
        daily_trend = self._get_daily_trend(days=30)
        top_dates = self._get_top_dates(n=5)

        return TimeTrends(
            daily_trend=daily_trend,
            hour_distribution=hour_distribution,
            top_dates=top_dates,
        )

    def _get_hour_distribution(self) -> list[int]:
        """Get hourly distribution (0-23)"""
        hour_counts = Counter(t.datetime.hour for t in self.data)
        return [hour_counts.get(h, 0) for h in range(24)]

    def _get_daily_trend(self, days: int = 30) -> dict[str, list[str | int]]:
        """Get recent N days trend, filling empty days with zero."""
        from datetime import date, timedelta

        daily_counts: dict[str, int] = {}
        for t in self.data:
            daily_counts[t.date] = daily_counts.get(t.date, 0) + 1

        today = date.today()
        dates = []
        counts = []
        for i in range(days - 1, -1, -1):
            d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            dates.append(d)
            counts.append(daily_counts.get(d, 0))

        return {"dates": dates, "counts": counts}

    def _get_top_dates(self, n: int = 5) -> list[DateEntry]:
        """Get top N dates by transcription count"""
        date_counts = Counter(t.date for t in self.data)
        top_dates = date_counts.most_common(n)
        return [DateEntry(date=date, count=count) for date, count in top_dates]

    def _empty_trends(self) -> TimeTrends:
        """Return empty trends for empty data"""
        return TimeTrends(
            daily_trend={"dates": [], "counts": []},
            hour_distribution=[0] * 24,
            top_dates=[],
        )
