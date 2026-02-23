"""Mock AI analysis data for -m mode (no real API calls needed)."""

import random

from src.models.ai_analysis import (
    AITranscriptionAnalysis,
    BigFivePersonality,
    CommunicationStyle,
    ComplexityMetrics,
    CreativeSignal,
    EmotionAnalysis,
    HumorSignal,
    IntentAnalysis,
    LanguageMixing,
    MentalHealthIndicators,
    PersonalityProfile,
    ProfanityDetection,
    SentimentAnalysis,
    TemporalContext,
    TimePerception,
)
from src.models.transcription import Transcription

_NEGATIVE_WORDS = [
    "烦",
    "累",
    "崩溃",
    "糟糕",
    "失败",
    "terrible",
    "annoying",
    "frustrating",
    "ridiculous",
    "crazy",
    "nightmare",
    "waste",
    "done with",
    "so tired",
]
_POSITIVE_WORDS = ["好", "棒", "完成", "成功", "great", "done", "nice", "perfect", "sounds good"]

# Emotion primaries that map to emotion_deep categories:
# anger/disgust → anger, fear → anxiety, sadness → sadness
_EMOTION_POOL = ["anger", "disgust", "fear", "sadness", "neutral", "joy"]
_EMOTION_WEIGHTS = [10, 5, 8, 7, 40, 30]


def generate_mock_analysis(transcription: Transcription) -> AITranscriptionAnalysis:
    """Generate deterministic mock AI analysis based on transcription content."""
    rng = random.Random(hash(transcription.id))  # same ID -> same result

    content = transcription.content
    hour = transcription.datetime.hour

    complexity = min(len(content) / 200, 1.0)
    fatigue: str = "high" if hour >= 23 or hour <= 5 else "low" if 9 <= hour <= 17 else "medium"

    has_negative = any(w in content.lower() for w in _NEGATIVE_WORDS)
    has_positive = any(w in content.lower() for w in _POSITIVE_WORDS)

    sentiment_score = -0.4 if has_negative else (0.5 if has_positive else rng.uniform(-0.15, 0.35))
    sentiment_label = (
        "negative"
        if sentiment_score < -0.1
        else ("positive" if sentiment_score > 0.2 else "neutral")
    )

    # Use weighted pool so all emotion categories appear in mock data
    if has_negative:
        emotion_primary = rng.choices(
            ["anger", "disgust", "fear", "sadness"], weights=[40, 20, 20, 20]
        )[0]
    elif has_positive:
        emotion_primary = rng.choices(["joy", "neutral"], weights=[70, 30])[0]
    else:
        emotion_primary = rng.choices(_EMOTION_POOL, weights=_EMOTION_WEIGHTS)[0]

    # Allow stress to exceed 0.6 threshold (previously capped at 0.59)
    stress_level = round(rng.uniform(0.1, 0.9), 2)

    return AITranscriptionAnalysis(
        sentiment=SentimentAnalysis(
            score=round(sentiment_score, 2),
            label=sentiment_label,
            confidence=round(rng.uniform(0.7, 0.95), 2),
        ),
        intent=IntentAnalysis(
            primary="question" if "?" in content or "吗" in content else "statement",
        ),
        emotion=EmotionAnalysis(
            primary=emotion_primary,
            intensity=round(rng.uniform(0.2, 0.8), 2),
        ),
        topics=["工作", "技术"] if rng.random() > 0.5 else ["生活"],
        communication_style=CommunicationStyle(
            directness=round(rng.uniform(0.4, 0.9), 2),
            formality=round(rng.uniform(0.2, 0.7), 2),
            assertiveness=round(rng.uniform(0.3, 0.8), 2),
        ),
        personality=PersonalityProfile(
            big_five=BigFivePersonality(
                openness=round(rng.uniform(0.3, 0.8), 2),
                conscientiousness=round(rng.uniform(0.4, 0.9), 2),
                extraversion=round(rng.uniform(0.2, 0.7), 2),
                agreeableness=round(rng.uniform(0.4, 0.8), 2),
                neuroticism=round(rng.uniform(0.2, 0.6), 2),
            ),
        ),
        mental_health=MentalHealthIndicators(
            stress_level=stress_level,
            burnout_risk="low",
        ),
        complexity=ComplexityMetrics(
            overall=round(complexity, 2),
            syntactic=round(complexity * 0.8, 2),
            lexical_diversity=round(rng.uniform(0.3, 0.7), 2),
            readability="simple" if complexity < 0.3 else "medium",
        ),
        profanity=ProfanityDetection(
            has_profanity=has_negative and rng.random() > 0.7,
        ),
        temporal_context=TemporalContext(
            fatigue_indicator=fatigue,
            circadian_phase="rest" if hour >= 23 or hour <= 6 else "active",
        ),
        language_mixing=LanguageMixing(
            dominant="mixed" if rng.random() > 0.7 else "zh",
            code_switch_count=rng.randint(0, 3),
        ),
        creative_signal=CreativeSignal(
            is_brainstorm=rng.random() > 0.8,
        ),
        humor=HumorSignal(
            detected=rng.random() > 0.9,
        ),
        time_perception=TimePerception(
            urgency=rng.choice(["urgent", "normal", "relaxed"]),
        ),
    )


def generate_mock_analyses(
    transcriptions: list[Transcription],
) -> dict[str, AITranscriptionAnalysis]:
    """Generate mock analyses for all transcriptions."""
    return {t.id: generate_mock_analysis(t) for t in transcriptions}
