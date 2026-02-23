from src.models.ai_analysis import (
    AIAnalysisCache,
    AITranscriptionAnalysis,
    CreativeSignal,
    HumorSignal,
    LanguageMixing,
    SentimentAnalysis,
)


def test_sentiment_analysis_valid():
    s = SentimentAnalysis(score=0.5, label="positive", confidence=0.9)
    assert s.score == 0.5
    assert s.label == "positive"


def test_ai_transcription_analysis_minimal():
    """Minimal valid construction (all required fields)."""
    data = _minimal_analysis_dict()
    analysis = AITranscriptionAnalysis(**data)
    assert analysis.sentiment.label in ("positive", "neutral", "negative")


def test_language_mixing_defaults():
    lm = LanguageMixing(dominant="zh")
    assert lm.code_switch_count == 0
    assert lm.en_ratio == 0.0


def test_creative_signal_defaults():
    cs = CreativeSignal()
    assert cs.is_brainstorm is False
    assert cs.novelty == "routine"


def test_humor_signal_defaults():
    hs = HumorSignal()
    assert hs.detected is False
    assert hs.type is None


def test_ai_analysis_cache_structure():
    cache = AIAnalysisCache(
        last_updated="2026-02-23T10:00:00Z",
        model="glm-4-flash",
        provider="zhipu",
        analyses={},
    )
    assert cache.version == "1.0"
    assert cache.analyses == {}


def _minimal_analysis_dict() -> dict:
    """Build a minimal valid AITranscriptionAnalysis dict."""
    return {
        "sentiment": {"score": 0.0, "label": "neutral", "confidence": 0.8},
        "intent": {"primary": "statement"},
        "emotion": {"primary": "neutral", "intensity": 0.3},
        "communication_style": {"directness": 0.5, "formality": 0.5, "assertiveness": 0.5},
        "personality": {
            "big_five": {
                "openness": 0.5,
                "conscientiousness": 0.5,
                "extraversion": 0.5,
                "agreeableness": 0.5,
                "neuroticism": 0.5,
            },
            "thinking_style": "analytical",
            "problem_style": "systematic",
        },
        "mental_health": {
            "stress_level": 0.3,
            "burnout_risk": "low",
            "anxiety_pattern": "stable",
            "optimism_score": 0.6,
            "rumination_score": 0.2,
        },
        "content_flags": {},
        "profanity": {},
        "complexity": {
            "overall": 0.4,
            "syntactic": 0.3,
            "lexical_diversity": 0.5,
            "readability": "medium",
        },
        "entities": {},
        "speech_patterns": {"fluency": 0.8, "pace": "normal"},
        "social_indicators": {
            "pronoun_ratio": {"i": 1.0},
            "gratitude_complaint_ratio": 0.5,
            "social_focus": "individual",
        },
        "cognitive_distortions": {},
        "temporal_context": {},
        "language_mixing": {"dominant": "zh"},
        "creative_signal": {},
        "humor": {},
        "time_perception": {},
    }
