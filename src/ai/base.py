from enum import Enum

from pydantic import BaseModel


class ProviderType(str, Enum):
    """Supported AI providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    ZHIPU = "zhipu"
    ALIBABA = "alibaba"
    DEEPSEEK = "deepseek"
    MOONSHOT = "moonshot"
    MINIMAX = "minimax"


# OpenAI-compatible provider endpoints (base_url + api_key only)
OPENAI_COMPATIBLE_BASE_URLS: dict[ProviderType, str] = {
    ProviderType.OPENAI: "https://api.openai.com/v1",
    ProviderType.ZHIPU: "https://open.bigmodel.cn/api/paas/v4/",
    ProviderType.DEEPSEEK: "https://api.deepseek.com/v1",
    ProviderType.MOONSHOT: "https://api.moonshot.cn/v1",
    ProviderType.ALIBABA: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    ProviderType.MINIMAX: "https://api.minimax.chat/v1",
}

# Providers that use JSON mode instead of function calling
JSON_MODE_PROVIDERS: set[ProviderType] = {
    ProviderType.MOONSHOT,
    ProviderType.MINIMAX,
    ProviderType.ALIBABA,
}

# Pricing table (CNY / 1M tokens)
PRICING_TABLE: dict[ProviderType, dict[str, float]] = {
    ProviderType.ZHIPU: {"input": 0.5, "output": 2.0},
    ProviderType.DEEPSEEK: {"input": 0.1, "output": 0.1},
    ProviderType.OPENAI: {"input": 10.0, "output": 30.0},
    ProviderType.ANTHROPIC: {"input": 2.0, "output": 8.0},
    ProviderType.MOONSHOT: {"input": 1.0, "output": 3.0},
    ProviderType.ALIBABA: {"input": 0.5, "output": 1.5},
    ProviderType.MINIMAX: {"input": 1.0, "output": 3.0},
}


class ModelConfig(BaseModel):
    """Configuration for a single AI provider."""

    provider: ProviderType
    model_name: str
    api_key: str
    base_url: str | None = None
    timeout: int = 30
    max_tokens: int = 2048


class TokenUsage(BaseModel):
    """Token usage record."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class CostRecord(BaseModel):
    """Single-run cost record, appended to data/cost_log.json."""

    date: str
    provider: str
    model: str
    new_entries: int
    cache_hits: int
    tokens: int
    cost_cny: float
