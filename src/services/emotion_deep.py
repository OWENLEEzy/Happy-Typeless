from collections import defaultdict

from src.models.ai_analysis import AITranscriptionAnalysis
from src.models.transcription import Transcription

_STRESS_THRESHOLD = 0.6
_FATIGUE_LEVELS = {"medium", "high"}


class EmotionDeepService:
    """Build the emotion_deep block from per-entry AI analyses.

    Produces five negative-emotion categories:
        anger   → emotion.primary in [anger, disgust]
        anxiety → emotion.primary == fear
        sadness → emotion.primary == sadness
        fatigue → temporal_context.fatigue_indicator in [medium, high]
        stress  → mental_health.stress_level > 0.6

    A single transcription may appear in multiple categories.
    """

    def __init__(
        self,
        analyses: dict[str, AITranscriptionAnalysis],
        transcriptions: list[Transcription],
    ) -> None:
        self._analyses = analyses
        self._trans_map = {t.id: t for t in transcriptions}

    def get_emotion_deep(self) -> dict:
        """Return emotion_deep dict; empty dict if no analyses."""
        if not self._analyses:
            return {}

        paired = [
            (self._trans_map[tid], analysis)
            for tid, analysis in self._analyses.items()
            if tid in self._trans_map
        ]

        if not paired:
            return {}

        return {
            "categories": self._build_categories(paired),
            "daily_trend": self._build_daily_trend(paired),
        }

    # ── private helpers ────────────────────────────────────────────────────────

    def _classify(self, analysis: AITranscriptionAnalysis) -> list[str]:
        """Return which negative-emotion categories this entry belongs to."""
        cats: list[str] = []
        primary = analysis.emotion.primary
        if primary in ("anger", "disgust"):
            cats.append("anger")
        if primary == "fear":
            cats.append("anxiety")
        if primary == "sadness":
            cats.append("sadness")
        if analysis.temporal_context.fatigue_indicator in _FATIGUE_LEVELS:
            cats.append("fatigue")
        if analysis.mental_health.stress_level > _STRESS_THRESHOLD:
            cats.append("stress")
        return cats

    def _build_categories(self, paired: list) -> dict:
        """Build per-category count / ratio / records."""
        bucket: dict[str, list[dict]] = {
            "anger": [],
            "anxiety": [],
            "sadness": [],
            "fatigue": [],
            "stress": [],
        }
        total = len(paired)

        for t, a in paired:
            record = {
                "date": t.date,
                "hour": t.datetime.hour,
                "sentiment_score": a.sentiment.score,
                "word_count": len(t.content),
                "content": t.content,
            }
            for cat in self._classify(a):
                if cat in bucket:
                    bucket[cat].append(record)

        result = {}
        for key, records in bucket.items():
            count = len(records)
            ratio = round(count / total * 100, 1) if total > 0 else 0.0
            result[key] = {
                "count": count,
                "ratio": ratio,
                "records": sorted(records, key=lambda r: (r["date"], r["hour"])),
            }
        return result

    def _build_daily_trend(self, paired: list) -> list[dict]:
        """Build daily average sentiment score for trend chart."""
        daily: dict[str, list[float]] = defaultdict(list)
        for t, a in paired:
            daily[t.date].append(a.sentiment.score)

        return [
            {
                "date": date,
                "avg_sentiment": round(sum(scores) / len(scores), 3),
            }
            for date, scores in sorted(daily.items())
        ]
