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
            "intent_distribution": self._intent_distribution(paired),
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
            # New aggregations for expanded cards
            "communication_style": self._aggregate_communication_style(paired),
            "speech_patterns": self._aggregate_speech_patterns(paired),
            "social_indicators": self._aggregate_social_indicators(paired),
            "cognitive_distortions": self._aggregate_cognitive_distortions(paired),
            "question_depth": self._aggregate_question_depth(paired),
            "complexity_metrics": self._aggregate_complexity(paired),
            "entities": self._aggregate_entities(paired),
            "time_perception": self._aggregate_time_perception(paired),
            "temporal_context": self._aggregate_temporal_context(paired),
            "urgency_patterns": self._aggregate_urgency_patterns(paired),
            "sentiment_timeline": self._sentiment_timeline(paired),
            "mental_health_trends": self._mental_health_trends(paired),
        }

    def _sentiment_distribution(self, paired: list) -> dict:
        dist = {"positive": 0, "neutral": 0, "negative": 0}
        for _, a in paired:
            dist[a.sentiment.label] += 1
        return dist

    def _intent_distribution(self, paired: list) -> dict:
        counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            counts[a.intent.primary] += 1
        return dict(counts)

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
                        "word_count": len(t.content),
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

    def _aggregate_communication_style(self, paired: list) -> dict:
        """Average communication style metrics."""
        if not paired:
            return {"directness": 0.5, "formality": 0.5, "assertiveness": 0.5}
        n = len(paired)
        return {
            "directness": round(sum(a.communication_style.directness for _, a in paired) / n, 3),
            "formality": round(sum(a.communication_style.formality for _, a in paired) / n, 3),
            "assertiveness": round(
                sum(a.communication_style.assertiveness for _, a in paired) / n, 3
            ),
        }

    def _aggregate_speech_patterns(self, paired: list) -> dict:
        """Aggregate speech pattern metrics."""
        if not paired:
            return {"fluency": 0.8, "hesitation_count": 0, "pace_distribution": {}}
        n = len(paired)
        pace_counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            pace_counts[a.speech_patterns.pace] += 1
        return {
            "avg_fluency": round(sum(a.speech_patterns.fluency for _, a in paired) / n, 3),
            "total_hesitations": sum(a.speech_patterns.hesitation_count for _, a in paired),
            "pace_distribution": dict(pace_counts),
        }

    def _aggregate_social_indicators(self, paired: list) -> dict:
        """Aggregate social indicators."""
        if not paired:
            return {"pronoun_ratio": {}, "social_focus": "individual"}
        n = len(paired)
        pronoun_totals: dict[str, float] = defaultdict(float)
        social_focus_counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            for k, v in a.social_indicators.pronoun_ratio.items():
                pronoun_totals[k] += v
            social_focus_counts[a.social_indicators.social_focus] += 1
        top_focus = (
            max(social_focus_counts.items(), key=lambda x: x[1])[0]
            if social_focus_counts
            else "individual"
        )
        return {
            "avg_pronoun_ratio": {k: round(v / n, 3) for k, v in pronoun_totals.items()},
            "social_focus": top_focus,
        }

    def _aggregate_cognitive_distortions(self, paired: list) -> dict:
        """Count cognitive distortion flags."""
        counts = {
            "absolutist_language": 0,
            "catastrophizing": 0,
            "overgeneralization": 0,
        }
        for _, a in paired:
            if a.cognitive_distortions.absolutist_language:
                counts["absolutist_language"] += 1
            if a.cognitive_distortions.catastrophizing:
                counts["catastrophizing"] += 1
            if a.cognitive_distortions.overgeneralization:
                counts["overgeneralization"] += 1
        return counts

    def _aggregate_question_depth(self, paired: list) -> dict:
        """Aggregate question depth statistics."""
        question_entries = [(t, a) for t, a in paired if a.question_depth]
        if not question_entries:
            return {
                "rhetorical_count": 0,
                "open_count": 0,
                "complex_count": 0,
                "avg_chain_depth": 0,
            }
        return {
            "rhetorical_count": sum(
                1 for _, a in question_entries if a.question_depth.is_rhetorical
            ),
            "open_count": sum(1 for _, a in question_entries if a.question_depth.is_open),
            "complex_count": sum(1 for _, a in question_entries if a.question_depth.is_complex),
            "avg_chain_depth": round(
                sum(a.question_depth.chain_depth for _, a in question_entries)
                / len(question_entries),
                2,
            ),
        }

    def _aggregate_complexity(self, paired: list) -> dict:
        """Aggregate complexity metrics."""
        if not paired:
            return {
                "overall": 0.4,
                "syntactic": 0.3,
                "lexical_diversity": 0.5,
                "readability_distribution": {},
            }
        n = len(paired)
        readability_counts: dict[str, int] = defaultdict(int)
        for _, a in paired:
            readability_counts[a.complexity.readability] += 1
        return {
            "avg_overall": round(sum(a.complexity.overall for _, a in paired) / n, 3),
            "avg_syntactic": round(sum(a.complexity.syntactic for _, a in paired) / n, 3),
            "avg_lexical_diversity": round(
                sum(a.complexity.lexical_diversity for _, a in paired) / n, 3
            ),
            "readability_distribution": dict(readability_counts),
        }

    def _aggregate_entities(self, paired: list) -> dict:
        """Aggregate named entities."""
        people: dict[str, int] = defaultdict(int)
        places: dict[str, int] = defaultdict(int)
        organizations: dict[str, int] = defaultdict(int)
        for _, a in paired:
            for p in a.entities.people:
                people[p] += 1
            for p in a.entities.places:
                places[p] += 1
            for o in a.entities.organizations:
                organizations[o] += 1
        return {
            "top_people": dict(sorted(people.items(), key=lambda x: -x[1])[:10]),
            "top_places": dict(sorted(places.items(), key=lambda x: -x[1])[:10]),
            "top_organizations": dict(sorted(organizations.items(), key=lambda x: -x[1])[:10]),
        }

    def _aggregate_time_perception(self, paired: list) -> dict:
        """Aggregate time perception patterns."""
        if not paired:
            return {"urgency_distribution": {}, "past_ref_count": 0, "future_ref_count": 0}
        urgency_counts: dict[str, int] = defaultdict(int)
        past_ref_count = 0
        future_ref_count = 0
        for _, a in paired:
            urgency_counts[a.time_perception.urgency] += 1
            if a.time_perception.references_past:
                past_ref_count += 1
            if a.time_perception.references_future:
                future_ref_count += 1
        return {
            "urgency_distribution": dict(urgency_counts),
            "past_ref_count": past_ref_count,
            "future_ref_count": future_ref_count,
        }

    def _aggregate_temporal_context(self, paired: list) -> dict:
        """Aggregate temporal context by hour."""
        hourly_energy: dict[int, list[float]] = defaultdict(list)
        fatigue_counts: dict[str, int] = defaultdict(int)
        for t, a in paired:
            hourly_energy[t.datetime.hour].append(a.temporal_context.energy_level)
            fatigue_counts[a.temporal_context.fatigue_indicator] += 1
        hourly_avg = {h: round(sum(vals) / len(vals), 3) for h, vals in hourly_energy.items()}
        return {
            "hourly_energy": dict(sorted(hourly_avg.items())),
            "fatigue_distribution": dict(fatigue_counts),
        }

    def _aggregate_urgency_patterns(self, paired: list) -> dict:
        """Aggregate urgency patterns over time."""
        urgency_by_date: dict[str, dict[str, int]] = defaultdict(
            lambda: {"immediate": 0, "normal": 0, "low": 0}
        )
        for t, a in paired:
            urgency_by_date[t.date][a.intent.urgency] += 1
        # Convert to sorted list for timeline
        timeline = [{"date": d, **urgency_by_date[d]} for d in sorted(urgency_by_date.keys())]
        return {"timeline": timeline[-30:]}  # Last 30 days

    def _sentiment_timeline(self, paired: list) -> dict:
        """Sentiment score trend over time."""
        sentiment_by_date: dict[str, list[float]] = defaultdict(list)
        for t, a in paired:
            sentiment_by_date[t.date].append(a.sentiment.score)
        timeline = [
            {
                "date": d,
                "avg_score": round(sum(scores) / len(scores), 3),
                "count": len(scores),
            }
            for d, scores in sorted(sentiment_by_date.items())
        ]
        return {"timeline": timeline[-30:]}  # Last 30 days

    def _mental_health_trends(self, paired: list) -> dict:
        """Mental health metrics over time."""
        stress_by_date: dict[str, list[float]] = defaultdict(list)
        for t, a in paired:
            stress_by_date[t.date].append(a.mental_health.stress_level)
        timeline = [
            {
                "date": d,
                "avg_stress": round(sum(scores) / len(scores), 3),
            }
            for d, scores in sorted(stress_by_date.items())
        ]
        return {"timeline": timeline[-30:]}  # Last 30 days

    def _empty_insights(self) -> dict:
        return {
            "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
            "emotion_distribution": {},
            "intent_distribution": {},
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
            # New aggregations
            "communication_style": {"directness": 0.5, "formality": 0.5, "assertiveness": 0.5},
            "speech_patterns": {"fluency": 0.8, "hesitation_count": 0, "pace_distribution": {}},
            "social_indicators": {"pronoun_ratio": {}, "social_focus": "individual"},
            "cognitive_distortions": {
                "absolutist_language": 0,
                "catastrophizing": 0,
                "overgeneralization": 0,
            },
            "question_depth": {
                "rhetorical_count": 0,
                "open_count": 0,
                "complex_count": 0,
                "avg_chain_depth": 0,
            },
            "complexity_metrics": {
                "overall": 0.4,
                "syntactic": 0.3,
                "lexical_diversity": 0.5,
                "readability_distribution": {},
            },
            "entities": {"top_people": {}, "top_places": {}, "top_organizations": {}},
            "time_perception": {
                "urgency_distribution": {},
                "past_ref_count": 0,
                "future_ref_count": 0,
            },
            "temporal_context": {"hourly_energy": {}, "fatigue_distribution": {}},
            "urgency_patterns": {"timeline": []},
            "sentiment_timeline": {"timeline": []},
            "mental_health_trends": {"timeline": []},
        }
