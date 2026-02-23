# src/services/usage_habits.py
from datetime import date

from src.models.analysis import UsageHabits
from src.models.transcription import TranscriptionList


class UsageHabitsService:
    """Service for analyzing user usage habits"""

    def __init__(self, data: TranscriptionList):
        self.data = data

    def get_habits(self) -> UsageHabits:
        """Calculate usage habits metrics

        Returns:
            UsageHabits with consecutive days, active days, gap days,
            and weekly comparison data
        """
        if len(self.data) == 0:
            return self._empty_habits()

        consecutive_days = self._calculate_consecutive_days()
        active_days = self.data.unique_dates_count()

        # Calculate date range for gap days
        unique_dates = sorted(set(t.date for t in self.data))
        if len(unique_dates) >= 2:
            date_range = (
                date.fromisoformat(unique_dates[-1]) - date.fromisoformat(unique_dates[0])
            ).days + 1
        else:
            date_range = 1

        gap_days = date_range - active_days

        # Weekly comparison
        weekly_counts = self._count_by_week()
        busiest_week = max(weekly_counts.values()) if weekly_counts else 0
        laziest_week = min(weekly_counts.values()) if weekly_counts else 0
        week_ratio = round(busiest_week / max(laziest_week, 1), 1)

        return UsageHabits(
            consecutive_days=consecutive_days,
            active_days=active_days,
            gap_days=gap_days,
            busiest_week=busiest_week,
            laziest_week=laziest_week,
            week_ratio=week_ratio,
        )

    def _calculate_consecutive_days(self) -> int:
        """Calculate longest consecutive usage days"""
        unique_dates = sorted(set(t.date for t in self.data))
        if len(unique_dates) == 0:
            return 0

        max_consecutive = 1
        current_consecutive = 1

        for i in range(1, len(unique_dates)):
            prev_date = date.fromisoformat(unique_dates[i - 1])
            curr_date = date.fromisoformat(unique_dates[i])
            diff = (curr_date - prev_date).days

            if diff == 1:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1

        return max_consecutive

    def _count_by_week(self) -> dict[tuple[int, int], int]:
        """Count transcriptions per week.

        Uses (year, week) tuple as key to handle cross-year data correctly.
        Returns dict with (year, week) keys and count values.
        """
        week_counts: dict[tuple[int, int], int] = {}
        for t in self.data:
            iso = t.datetime.isocalendar()
            week_key = (iso.year, iso.week)  # (year, week) to handle year boundary
            week_counts[week_key] = week_counts.get(week_key, 0) + 1
        return week_counts

    def _empty_habits(self) -> UsageHabits:
        """Return empty habits for empty data"""
        return UsageHabits(
            consecutive_days=0,
            active_days=0,
            gap_days=0,
            busiest_week=0,
            laziest_week=0,
            week_ratio=0.0,
        )
