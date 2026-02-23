# src/services/efficiency.py
from src.config import get_settings
from src.models.analysis import (
    EfficiencyMetrics,
    EfficiencyScores,
    FragmentationInfo,
)
from src.models.transcription import TranscriptionList
from src.translations import I18n


class EfficiencyService:
    """Service for efficiency metrics calculation"""

    def __init__(self, data: TranscriptionList, lang: str = "zh"):
        self.data = data
        self.lang = lang
        self.settings = get_settings()
        self.thresholds = self.settings.thresholds
        self.i18n = I18n(lang)

    def get_metrics(self) -> EfficiencyMetrics:
        """Calculate efficiency metrics

        Returns:
            EfficiencyMetrics with scores and fragmentation info
        """
        if len(self.data) == 0:
            return self._empty_metrics()

        scores = self._calculate_scores()
        fragmentation = self._calculate_fragmentation()
        late_night_ratio = self._calculate_late_night_ratio()
        avg_duration = self._calculate_avg_duration()

        return EfficiencyMetrics(
            scores=scores,
            fragmentation=fragmentation,
            late_night_ratio=late_night_ratio,
            avg_duration=avg_duration,
        )

    def _calculate_scores(self) -> EfficiencyScores:
        """Calculate efficiency scores

        Scoring logic:
        - Sleep health: 0% late night = 100, 50%+ late night = 0
        - Work efficiency: based on work hours usage ratio (workdays 9-18)
        - Focus: 10-30 seconds avg duration = optimal range
        """
        total = len(self.data)

        # Sleep health score
        # 0% late night usage = 100 points, 50%+ = 0 points
        late_night_hours = self.thresholds.late_night_hours
        late_night_count = sum(1 for t in self.data if t.datetime.hour in late_night_hours)
        late_night_ratio = late_night_count / max(total, 1)
        # Formula: 100 - (late_night_ratio / threshold) * 100, clamped to [0, 100]
        sleep_health_score = max(
            0,
            min(100, 100 - (late_night_ratio / self.thresholds.late_night_score_zero_at) * 100),
        )

        # Work efficiency score
        # Based on usage during work hours (9-18) on weekdays
        work_hours = self.thresholds.work_hours
        work_count = sum(
            1 for t in self.data if t.datetime.weekday() < 5 and t.datetime.hour in work_hours
        )
        work_ratio = work_count / max(total, 1)
        # 0% work hours = 0 points, full-at threshold = 100 points
        work_efficiency_score = min(100, work_ratio / self.thresholds.work_efficiency_full_at * 100)

        # Focus score
        # Optimal range: focus_min_seconds to focus_optimal_seconds per entry
        avg_duration = self._calculate_avg_duration()
        f_min = self.thresholds.focus_min_seconds
        f_opt = self.thresholds.focus_optimal_seconds
        if f_min <= avg_duration <= f_opt:
            focus_score = 100
        elif avg_duration < f_min:
            focus_score = max(0, avg_duration / f_min * 100)
        else:
            focus_score = max(
                0, 100 - (avg_duration - f_opt) / self.thresholds.focus_decay_seconds * 100
            )

        overall_score = round((sleep_health_score + work_efficiency_score + focus_score) / 3)

        return EfficiencyScores(
            sleep_health=round(sleep_health_score),
            work_efficiency=round(work_efficiency_score),
            focus=round(focus_score),
            overall=overall_score,
        )

    def _calculate_fragmentation(self) -> FragmentationInfo:
        """Calculate fragmentation index"""
        short_threshold = self.thresholds.short_sentence
        short_count = sum(1 for t in self.data if len(t.content) < short_threshold)
        fragmentation_ratio = short_count / max(len(self.data), 1) * 100

        high_threshold = self.thresholds.fragmentation_high
        low_threshold = self.thresholds.fragmentation_low

        if fragmentation_ratio > high_threshold:
            level = self.i18n.t("fragmentation_high")
            desc = self.i18n.t("fragmentation_high_desc")
        elif fragmentation_ratio < low_threshold:
            level = self.i18n.t("fragmentation_low")
            desc = self.i18n.t("fragmentation_low_desc")
        else:
            level = self.i18n.t("fragmentation_medium")
            desc = self.i18n.t("fragmentation_medium_desc")

        return FragmentationInfo(
            level=level,
            desc=desc,
            ratio=round(fragmentation_ratio, 1),
            short_count=short_count,
        )

    def _calculate_late_night_ratio(self) -> float:
        """Calculate late night usage ratio (percentage)"""
        total = len(self.data)
        late_night_hours = self.thresholds.late_night_hours
        late_night_count = sum(1 for t in self.data if t.datetime.hour in late_night_hours)
        return round(late_night_count / max(total, 1) * 100, 1)

    def _calculate_avg_duration(self) -> float:
        """Calculate average duration in seconds"""
        durations = [t.duration for t in self.data if t.duration is not None]
        if durations:
            return round(sum(durations) / len(durations), 1)
        # Fallback: estimate from word count (assuming ~3 words/second)
        return round(sum(len(t.content) for t in self.data) / max(len(self.data), 1) / 3, 1)

    def _empty_metrics(self) -> EfficiencyMetrics:
        """Return empty metrics for empty data"""
        return EfficiencyMetrics(
            scores=EfficiencyScores(sleep_health=0, work_efficiency=0, focus=0, overall=0),
            fragmentation=FragmentationInfo(
                level=self.i18n.t("fragmentation_medium"),
                desc=self.i18n.t("fragmentation_empty"),
                ratio=0.0,
                short_count=0,
            ),
            late_night_ratio=0.0,
            avg_duration=0.0,
        )
