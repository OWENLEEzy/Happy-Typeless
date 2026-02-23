from unittest.mock import MagicMock

from src.ai.analyzer import AIAnalyzer
from src.models.transcription import Transcription, TranscriptionList


def _make_transcriptions(n: int) -> TranscriptionList:
    return TranscriptionList(
        items=[
            Transcription(id=f"id_{i}", timestamp=1700000000 + i * 60, content=f"test content {i}")
            for i in range(n)
        ]
    )


def test_analyzer_returns_dict(tmp_path, monkeypatch):
    """Analyzer returns id -> analysis dict; None results are filtered out."""
    monkeypatch.setenv("AI_API_KEY", "test_key")

    from src.ai.base import ModelConfig, ProviderType

    config = ModelConfig(provider=ProviderType.ZHIPU, model_name="glm-4-flash", api_key="test")
    analyzer = AIAnalyzer(primary=config, cache_path=tmp_path / "cache.json")

    # Mock client to return None (no real API key)
    analyzer._client.analyze_batch = MagicMock(return_value=[None, None])

    transcriptions = _make_transcriptions(2)
    result = analyzer.analyze(transcriptions)

    assert isinstance(result, dict)
    # None results are filtered out
    assert len(result) == 0
