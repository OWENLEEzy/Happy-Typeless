# src/services/app_usage.py
"""Service for app usage statistics analysis."""

from collections import Counter

from src.config import get_settings
from src.models.analysis import AppUsage, AppUsageItem
from src.models.transcription import TranscriptionList


class AppUsageService:
    """Service for analyzing app usage statistics."""

    def __init__(self, data: TranscriptionList):
        self.data = data
        self.settings = get_settings()

    def get_app_usage(self) -> AppUsage:
        """Calculate app usage statistics.

        Returns:
            AppUsage with app statistics including counts, ratios,
            and average duration/words per app.
        """
        if len(self.data) == 0:
            return AppUsage(apps=[], total=0, has_data=False, unique_apps=0)

        # Check if data has app_name field
        has_app_data = any(t.app_name for t in self.data if t.app_name)
        if not has_app_data:
            return AppUsage(apps=[], total=len(self.data), has_data=False, unique_apps=0)

        # Collect app names and aggregate stats
        app_counter = Counter()
        app_duration_sum: dict[str, float] = {}
        app_words_sum: dict[str, int] = {}

        for t in self.data:
            if t.app_name:
                app_name = t.app_name
                app_counter[app_name] += 1

                duration = t.duration or 0
                app_duration_sum[app_name] = app_duration_sum.get(app_name, 0) + duration

                word_count = len(t.content)
                app_words_sum[app_name] = app_words_sum.get(app_name, 0) + word_count

        total = len(self.data)
        unique_apps = len(app_counter)

        # Build app usage items (top 20)
        apps = []
        for app_name, count in app_counter.most_common(20):
            avg_duration = app_duration_sum.get(app_name, 0) / count
            avg_words = app_words_sum.get(app_name, 0) / count
            ratio = count / total if total > 0 else 0

            apps.append(
                AppUsageItem(
                    app_name=app_name,
                    count=count,
                    ratio=round(ratio, 4),
                    avg_duration=round(avg_duration, 1),
                    avg_words=round(avg_words, 1),
                )
            )

        return AppUsage(apps=apps, total=total, has_data=True, unique_apps=unique_apps)
