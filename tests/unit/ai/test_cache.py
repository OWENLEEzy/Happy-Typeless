from src.ai.cache import AICache
from src.models.ai_analysis import (
    AITranscriptionAnalysis,
    EmotionAnalysis,
    IntentAnalysis,
    SentimentAnalysis,
)


def _make_analysis() -> AITranscriptionAnalysis:
    return AITranscriptionAnalysis(
        sentiment=SentimentAnalysis(score=0.5, label="positive"),
        intent=IntentAnalysis(primary="statement"),
        emotion=EmotionAnalysis(primary="joy", intensity=0.7),
    )


def test_cache_miss_returns_none(tmp_path):
    cache = AICache(tmp_path / "cache.json", model="glm-4-flash", provider="zhipu")
    assert cache.get("nonexistent_id") is None


def test_cache_set_and_get(tmp_path):
    cache = AICache(tmp_path / "cache.json", model="glm-4-flash", provider="zhipu")
    analysis = _make_analysis()
    cache.set("id_001", analysis)
    result = cache.get("id_001")
    assert result is not None
    assert result.sentiment.label == "positive"


def test_cache_persists_to_disk(tmp_path):
    path = tmp_path / "cache.json"
    cache1 = AICache(path, model="glm-4-flash", provider="zhipu")
    cache1.set("id_001", _make_analysis())
    cache1.save()

    # Reload from disk
    cache2 = AICache(path, model="glm-4-flash", provider="zhipu")
    assert cache2.get("id_001") is not None


def test_cache_model_mismatch_warning(tmp_path, caplog):
    import logging

    path = tmp_path / "cache.json"
    cache1 = AICache(path, model="glm-4-flash", provider="zhipu")
    cache1.set("id_001", _make_analysis())
    cache1.save()

    # Load with different model — triggers a logger.warning
    with caplog.at_level(logging.WARNING, logger="src.ai.cache"):
        AICache(path, model="deepseek-v3", provider="deepseek")

    assert any("deepseek-v3" in r.message for r in caplog.records)


def test_cache_stats(tmp_path):
    cache = AICache(tmp_path / "cache.json", model="glm-4-flash", provider="zhipu")
    cache.set("id_001", _make_analysis())
    cache.set("id_002", _make_analysis())
    stats = cache.stats()
    assert stats["total"] == 2
    assert stats["model"] == "glm-4-flash"
