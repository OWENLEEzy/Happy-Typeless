from typing import Literal

from pydantic import BaseModel


class SentimentAnalysis(BaseModel):
    """Sentiment polarity analysis."""

    score: float  # -1.0 to 1.0
    label: Literal["positive", "neutral", "negative"]
    confidence: float = 0.8


class IntentAnalysis(BaseModel):
    """Intent classification."""

    primary: Literal[
        "question",
        "statement",
        "command",
        "request",
        "expression",
        "complaint",
        "gratitude",
    ]
    secondary: list[str] = []
    urgency: Literal["immediate", "normal", "low"] = "normal"


class EmotionAnalysis(BaseModel):
    """Emotion classification."""

    primary: Literal["joy", "anger", "sadness", "fear", "surprise", "disgust", "neutral"]
    intensity: float = 0.3
    mixed: bool = False
    transition_potential: float = 0.0


class CommunicationStyle(BaseModel):
    """Communication style metrics."""

    directness: float = 0.5
    formality: float = 0.5
    assertiveness: float = 0.5


class BigFivePersonality(BaseModel):
    """Big Five personality traits."""

    openness: float = 0.5
    conscientiousness: float = 0.5
    extraversion: float = 0.5
    agreeableness: float = 0.5
    neuroticism: float = 0.5


class PersonalityProfile(BaseModel):
    """Extended personality profile."""

    big_five: BigFivePersonality = BigFivePersonality()
    thinking_style: Literal["analytical", "intuitive", "creative", "practical"] = "analytical"
    problem_style: Literal["systematic", "intuitive", "collaborative", "independent"] = "systematic"


class MentalHealthIndicators(BaseModel):
    """Mental health indicators (non-diagnostic)."""

    stress_level: float = 0.3
    burnout_risk: Literal["low", "medium", "high"] = "low"
    anxiety_pattern: Literal["improving", "stable", "worsening"] = "stable"
    optimism_score: float = 0.6
    rumination_score: float = 0.2


class ContentFlags(BaseModel):
    """Content type flags."""

    has_goal: bool = False
    has_decision: bool = False
    has_complaint: bool = False
    has_gratitude: bool = False
    has_plan: bool = False
    has_action_item: bool = False
    is_profound: bool = False


class ProfanityDetection(BaseModel):
    """Profanity and negative language detection."""

    has_profanity: bool = False
    severity: Literal["mild", "moderate", "severe"] | None = None
    trigger_category: Literal["frustration", "anger", "habit", "humor"] | None = None


class ComplexityMetrics(BaseModel):
    """Text complexity metrics."""

    overall: float = 0.4
    syntactic: float = 0.3
    lexical_diversity: float = 0.5
    readability: Literal["simple", "medium", "complex", "academic"] = "medium"


class Entities(BaseModel):
    """Named entity extraction."""

    people: list[str] = []
    places: list[str] = []
    organizations: list[str] = []
    dates: list[str] = []
    numbers: list[float] = []


class SpeechPatterns(BaseModel):
    """Speech fluency and rhythm."""

    fluency: float = 0.8
    hesitation_count: int = 0
    self_correction_count: int = 0
    repetition_count: int = 0
    pace: Literal["slow", "normal", "fast", "variable"] = "normal"


class SocialIndicators(BaseModel):
    """Social and relationship patterns."""

    pronoun_ratio: dict[str, float] = {"i": 1.0}
    gratitude_complaint_ratio: float = 0.5
    social_focus: Literal["individual", "collaborative", "observational"] = "individual"


class CognitiveDistortions(BaseModel):
    """Cognitive distortion detection."""

    absolutist_language: bool = False
    catastrophizing: bool = False
    overgeneralization: bool = False


class QuestionDepth(BaseModel):
    """Question depth analysis."""

    is_rhetorical: bool = False
    is_open: bool = False
    is_complex: bool = False
    chain_depth: int = 0


class TemporalContext(BaseModel):
    """Temporal dimension context."""

    circadian_phase: Literal["active", "rest", "transition"] = "active"
    fatigue_indicator: Literal["low", "medium", "high"] = "low"
    energy_level: float = 0.5


class LanguageMixing(BaseModel):
    """Language mixing detection."""

    dominant: Literal["zh", "en", "mixed"] = "zh"
    code_switch_count: int = 0
    en_ratio: float = 0.0


class CreativeSignal(BaseModel):
    """Creative / inspiration pattern detection."""

    is_brainstorm: bool = False
    idea_density: float = 0.0
    novelty: Literal["routine", "variation", "breakthrough"] = "routine"


class HumorSignal(BaseModel):
    """Humor / joke detection."""

    detected: bool = False
    type: Literal["self_deprecating", "observational", "sarcastic"] | None = None


class TimePerception(BaseModel):
    """Time perception analysis."""

    urgency: Literal["urgent", "normal", "relaxed"] = "normal"
    references_past: bool = False
    references_future: bool = False


class AITranscriptionAnalysis(BaseModel):
    """Complete AI analysis result for a single voice transcription."""

    # Core
    sentiment: SentimentAnalysis
    intent: IntentAnalysis
    emotion: EmotionAnalysis
    topics: list[str] = []

    # Style and personality
    communication_style: CommunicationStyle = CommunicationStyle()
    personality: PersonalityProfile = PersonalityProfile()
    mental_health: MentalHealthIndicators = MentalHealthIndicators()

    # Content
    content_flags: ContentFlags = ContentFlags()
    profanity: ProfanityDetection = ProfanityDetection()
    complexity: ComplexityMetrics = ComplexityMetrics()
    entities: Entities = Entities()

    # Patterns
    speech_patterns: SpeechPatterns = SpeechPatterns()
    social_indicators: SocialIndicators = SocialIndicators()
    cognitive_distortions: CognitiveDistortions = CognitiveDistortions()
    question_depth: QuestionDepth | None = None

    # Temporal context
    temporal_context: TemporalContext = TemporalContext()

    # Extended insights
    language_mixing: LanguageMixing = LanguageMixing()
    creative_signal: CreativeSignal = CreativeSignal()
    emotion_trigger: (
        Literal[
            "technical_frustration",
            "social_conflict",
            "achievement",
            "uncertainty",
            "external_pressure",
        ]
        | None
    ) = None
    commitment_strength: Literal["vague", "intended", "committed"] | None = None
    humor: HumorSignal = HumorSignal()
    time_perception: TimePerception = TimePerception()


class AIAnalysisCache(BaseModel):
    """AI analysis cache structure, stored at data/ai_cache.json."""

    version: str = "1.0"
    last_updated: str
    model: str
    provider: str
    analyses: dict[str, AITranscriptionAnalysis] = {}
