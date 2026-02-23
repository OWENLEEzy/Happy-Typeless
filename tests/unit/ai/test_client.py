import asyncio

from src.ai.base import ModelConfig, ProviderType
from src.ai.client import AIClient, build_instructor_client


def _zhipu_config() -> ModelConfig:
    return ModelConfig(provider=ProviderType.ZHIPU, model_name="glm-4-flash", api_key="test_key")


def _deepseek_config() -> ModelConfig:
    return ModelConfig(provider=ProviderType.DEEPSEEK, model_name="deepseek-v3", api_key="test_key")


def test_build_instructor_client_openai_compatible():
    """OpenAI-compatible provider uses from_openai."""
    client = build_instructor_client(_zhipu_config())
    assert client is not None


def test_build_instructor_client_anthropic():
    """Anthropic uses from_anthropic."""
    config = ModelConfig(
        provider=ProviderType.ANTHROPIC,
        model_name="claude-3-5-sonnet-20241022",
        api_key="test_key",
    )
    client = build_instructor_client(config)
    assert client is not None


def test_budget_exceeded_skips_api(tmp_path):
    """When budget is exceeded, skip API call and return None."""
    from src.ai.cache import AICache

    cache = AICache(tmp_path / "cache.json", model="glm-4-flash", provider="zhipu")

    client = AIClient(
        primary=_zhipu_config(),
        cache=cache,
        max_cost_cny=0.0,  # zero budget triggers circuit breaker immediately
    )

    from src.models.transcription import Transcription

    t = Transcription(id="id1", timestamp=1700000000, content="test")

    result = asyncio.run(client._analyze_one(t))
    assert result is None
