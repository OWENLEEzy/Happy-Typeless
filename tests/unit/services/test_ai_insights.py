from src.models.ai_analysis import (
    AITranscriptionAnalysis,
    EmotionAnalysis,
    IntentAnalysis,
    ProfanityDetection,
    SentimentAnalysis,
)
from src.models.transcription import Transcription
from src.services.ai_insights import AIInsightsService


def _analysis(label="neutral", emotion="neutral", has_profanity=False):
    score = 0.0 if label == "neutral" else (-0.5 if label == "negative" else 0.5)
    return AITranscriptionAnalysis(
        sentiment=SentimentAnalysis(score=score, label=label),
        intent=IntentAnalysis(primary="statement"),
        emotion=EmotionAnalysis(primary=emotion, intensity=0.5),
        profanity=ProfanityDetection(has_profanity=has_profanity),
    )


def _transcription(id_: str, hour: int = 10) -> Transcription:
    ts = 1700000000 + hour * 3600
    return Transcription(id=id_, timestamp=ts, content="test")


def test_sentiment_distribution():
    analyses = {
        "id1": _analysis("positive"),
        "id2": _analysis("negative"),
        "id3": _analysis("neutral"),
    }
    transcriptions = [_transcription(id_) for id_ in analyses]
    service = AIInsightsService(analyses, transcriptions)
    result = service.get_insights()

    dist = result["sentiment_distribution"]
    assert dist["positive"] == 1
    assert dist["negative"] == 1
    assert dist["neutral"] == 1


def test_profanity_calendar():
    analyses = {
        "id1": _analysis(has_profanity=True),
        "id2": _analysis(has_profanity=False),
    }
    transcriptions = [_transcription("id1"), _transcription("id2")]
    service = AIInsightsService(analyses, transcriptions)
    result = service.get_insights()

    assert len(result["profanity_calendar"]) == 1


def test_empty_analyses():
    service = AIInsightsService({}, [])
    result = service.get_insights()
    assert result["sentiment_distribution"]["positive"] == 0
