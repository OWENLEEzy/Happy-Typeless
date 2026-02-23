# src/services/overview.py
from datetime import datetime

from src.config import get_settings
from src.models.analysis import BadgeInfo, OverviewStats
from src.models.transcription import TranscriptionList
from src.translations import I18n


class OverviewService:
    """Service for calculating overview statistics"""

    def __init__(self, data: TranscriptionList, lang: str = "en"):
        self.data = data
        self.i18n = I18n(lang)

    def get_stats(self) -> OverviewStats:
        """Calculate overview statistics"""
        if len(self.data) == 0:
            return self._empty_stats()

        total_words = sum(len(t.content) for t in self.data)
        total_duration_seconds = sum(t.duration or 0 for t in self.data)
        total_duration_minutes = total_duration_seconds / 60  # to minutes for total_duration

        unique_dates = set(t.date for t in self.data)
        active_days = len(unique_dates)

        if len(unique_dates) >= 2:
            dates_sorted = sorted(unique_dates)
            date_range_days = (
                datetime.strptime(dates_sorted[-1], "%Y-%m-%d")
                - datetime.strptime(dates_sorted[0], "%Y-%m-%d")
            ).days + 1
        else:
            date_range_days = 1

        return OverviewStats(
            total_records=len(self.data),
            total_words=total_words,
            total_duration=round(total_duration_minutes, 1),
            active_days=active_days,
            date_range_days=date_range_days,
            daily_avg=round(len(self.data) / max(date_range_days, 1), 1),
            avg_words=round(total_words / max(len(self.data), 1), 1),
            avg_duration=round(total_duration_seconds / max(len(self.data), 1), 1),
            start_date=min(unique_dates) if unique_dates else "",
            end_date=max(unique_dates) if unique_dates else "",
            badge=self._calculate_badge(total_words),
        )

    def _calculate_badge(self, total_words: int) -> BadgeInfo:
        """Calculate achievement badge based on total word count"""
        levels = get_settings().thresholds.badge_levels
        for threshold, name_key, icon, color in levels:
            if total_words < threshold:
                return BadgeInfo(
                    icon=icon,
                    name=self.i18n.t(name_key),
                    color=color,
                    threshold=threshold,
                    progress=total_words / threshold,
                )
        # All levels surpassed - show highest badge at 100%
        threshold, name_key, icon, color = levels[-1]
        return BadgeInfo(
            icon=icon, name=self.i18n.t(name_key), color=color, threshold=threshold, progress=1.0
        )

    def _empty_stats(self) -> OverviewStats:
        """Return empty stats"""
        return OverviewStats(
            total_records=0,
            total_words=0,
            total_duration=0.0,
            active_days=0,
            date_range_days=0,
            daily_avg=0.0,
            avg_words=0.0,
            avg_duration=0.0,
            start_date="",
            end_date="",
        )
