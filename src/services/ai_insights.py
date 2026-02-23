from collections import defaultdict

from src.models.ai_analysis import AITranscriptionAnalysis
from src.models.transcription import Transcription


class AIInsightsService:
    """Aggregate per-entry AI analysis results into report-ready statistics."""

    def __init__(
        self,
        analyses: dict[str, AITranscriptionAnalysis],
        transcriptions: list[Transcription],
    ) -> None:
        self._analyses = analyses
        self._trans_map = {t.id: t for t in transcriptions}

    def get_insights(self) -> dict:
        """Return all aggregated AI insights."""
        if not self._analyses:
            return self._empty_insights()

        paired = [
            (self._trans_map[id_], analysis)
            for id_, analysis in self._analyses.items()
            if id_ in self._trans_map
        ]

        return {
            "sentiment_distribution": self._sentiment_distribution(paired),
            "emotion_distribution": self._emotion_distribution(paired),
            "personality_profile": self._aggregate_personality(paired),
            "mental_health_avg": self._avg_mental_health(paired),
            "topic_distribution": self._topic_distribution(paired),
            "profanity_calendar": self._profanity_calendar(paired),
            "creative_moments": self._creative_moments(paired),
            "language_mixing": self._language_mixing_stats(paired),
            "hourly_sentiment": self._hourly_sentiment(paired),
            "emotion_triggers": self._emotion_triggers(paired),
            "commitment_distribution": self._commitment_distribution(paired),
            "humor_entries": self._humor_entries(paired),
            "content_flags_summary": self._content_flags_summary(paired),
            "action_items": self._action_items(paired),
        }

    def _sentiment_distribution(self, paired: list) -> dict:
        dist = {"positive": 0, "neutral": 0, "negative": 0}
        for _, a in paired:
            dist[a.sentiment.label] += 1
        return dist

    def _emotion_distribution(self, paired: list) -> dict:
        dist: dict[str, int] = defaultdict(int)
        for _, a in paired:
            dist[a.emotion.primary] += 1
        return dict(dist)

    def _aggregate_personality(self, paired: list) -> dict:
        """Average Big Five personality scores."""
        if not paired:
            return {}
        fields = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        totals = {f: 0.0 for f in fields}
        for _, a in paired:
            for f in fields:
                totals[f] += getattr(a.personality.big_five, f)
        n = len(paired)
        return {f: round(totals[f] / n, 3) for f in fields}

    def _avg_mental_health(self, paired: list) -> dict:
        if not paired:
            return {}
        stress_total = sum(a.mental_health.stress_level for _, a in paired)
        optimism_total = sum(a.mental_health.optimism_score for _, a in paired)
        n = len(paired)
        burnout_counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            burnout_counts[a.mental_health.burnout_risk] += 1
        return {
            "avg_stress": round(stress_total / n, 3),
            "avg_optimism": round(optimism_total / n, 3),
            "burnout_distribution": dict(burnout_counts),
        }

    def _topic_distribution(self, paired: list) -> dict:
        counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            for topic in a.topics:
                counts[topic] += 1
        return dict(sorted(counts.items(), key=lambda x: -x[1])[:20])

    def _profanity_calendar(self, paired: list) -> list[dict]:
        results = []
        for t, a in paired:
            if a.profanity.has_profanity:
                results.append(
                    {
                        "date": t.date,
                        "hour": t.datetime.hour,
                        "content": t.content[:100],
                        "severity": a.profanity.severity,
                        "trigger": a.profanity.trigger_category,
                    }
                )
        return sorted(results, key=lambda x: x["date"])

    def _creative_moments(self, paired: list) -> list[dict]:
        moments = []
        for t, a in paired:
            if a.creative_signal.is_brainstorm or a.creative_signal.novelty == "breakthrough":
                moments.append(
                    {
                        "date": t.date,
                        "content": t.content[:150],
                        "novelty": a.creative_signal.novelty,
                        "idea_density": a.creative_signal.idea_density,
                    }
                )
        return moments[:20]

    def _language_mixing_stats(self, paired: list) -> dict:
        counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            counts[a.language_mixing.dominant] += 1
        return dict(counts)

    def _hourly_sentiment(self, paired: list) -> dict[int, float]:
        hour_scores: dict[int, list[float]] = defaultdict(list)
        for t, a in paired:
            hour_scores[t.datetime.hour].append(a.sentiment.score)
        return {
            hour: round(sum(scores) / len(scores), 3)
            for hour, scores in sorted(hour_scores.items())
        }

    def _emotion_triggers(self, paired: list) -> dict:
        counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            if a.emotion_trigger:
                counts[a.emotion_trigger] += 1
        return dict(counts)

    def _commitment_distribution(self, paired: list) -> dict:
        counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            if a.commitment_strength:
                counts[a.commitment_strength] += 1
        return dict(counts)

    def _humor_entries(self, paired: list) -> list[dict]:
        return [
            {"date": t.date, "content": t.content[:100], "type": a.humor.type}
            for t, a in paired
            if a.humor.detected
        ][:10]

    def _content_flags_summary(self, paired: list) -> dict:
        flags = [
            "has_goal",
            "has_decision",
            "has_complaint",
            "has_gratitude",
            "has_plan",
            "has_action_item",
            "is_profound",
        ]
        counts = {f: 0 for f in flags}
        for _, a in paired:
            for f in flags:
                if getattr(a.content_flags, f):
                    counts[f] += 1
        return counts

    def _action_items(self, paired: list) -> list[dict]:
        return [
            {
                "date": t.date,
                "content": t.content[:200],
                "commitment": a.commitment_strength,
            }
            for t, a in paired
            if a.content_flags.has_action_item
        ][:20]

    def _empty_insights(self) -> dict:
        return {
            "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
            "emotion_distribution": {},
            "personality_profile": {},
            "mental_health_avg": {},
            "topic_distribution": {},
            "profanity_calendar": [],
            "creative_moments": [],
            "language_mixing": {},
            "hourly_sentiment": {},
            "emotion_triggers": {},
            "commitment_distribution": {},
            "humor_entries": [],
            "content_flags_summary": {},
            "action_items": [],
        }
