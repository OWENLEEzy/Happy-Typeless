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

# Model-specific pricing (CNY / 1M tokens). Checked against official pricing pages.
# Input rates use cache-miss prices; actual cost may be lower with prefix caching.
# MODEL_PRICING takes precedence; PRICING_TABLE is the provider-level fallback.
MODEL_PRICING: dict[str, dict[str, float]] = {
    # ── DeepSeek (USD×7.2; cache-miss input) ──────────────────────────────────
    # V3/V3.2 and R1 unified at $0.28/$0.42 as of late 2025
    "deepseek-chat": {"input": 2.0, "output": 3.0},
    "deepseek-v3": {"input": 2.0, "output": 3.0},
    "deepseek-v3-0324": {"input": 2.0, "output": 3.0},
    "deepseek-reasoner": {"input": 2.0, "output": 3.0},
    "deepseek-r1": {"input": 2.0, "output": 3.0},
    "deepseek-r1-0528": {"input": 2.0, "output": 3.0},
    # ── Zhipu AI (bigmodel.cn CNY pricing) ────────────────────────────────────
    "glm-4-flash": {"input": 0.0, "output": 0.0},  # free
    "glm-4-flash-250414": {"input": 0.0, "output": 0.0},  # free
    "glm-4-air": {"input": 0.5, "output": 0.5},
    "glm-4-airx": {"input": 10.0, "output": 10.0},
    "glm-4-long": {"input": 1.0, "output": 1.0},
    "glm-4-plus": {"input": 5.0, "output": 5.0},
    "glm-4": {"input": 50.0, "output": 50.0},
    "glm-4.6": {"input": 2.0, "output": 8.0},  # thinking
    "glm-4.7": {"input": 4.0, "output": 16.0},  # thinking; $0.60/$2.20×7.2
    # ── OpenAI (USD×7.2) ──────────────────────────────────────────────────────
    "gpt-4o": {"input": 18.0, "output": 72.0},  # $2.50/$10.00
    "gpt-4o-mini": {"input": 1.1, "output": 4.3},  # $0.15/$0.60
    "gpt-4.1": {"input": 14.4, "output": 57.6},  # $2.00/$8.00
    "gpt-4.1-mini": {"input": 2.9, "output": 11.5},  # $0.40/$1.60
    "gpt-4.1-nano": {"input": 0.7, "output": 2.9},  # $0.10/$0.40
    "o1": {"input": 108.0, "output": 432.0},  # $15.00/$60.00
    "o1-mini": {"input": 21.6, "output": 86.4},  # $3.00/$12.00
    "o3": {"input": 14.4, "output": 57.6},  # $2.00/$8.00
    "o3-mini": {"input": 7.9, "output": 31.7},  # $1.10/$4.40
    "o4-mini": {"input": 7.9, "output": 31.7},  # $1.10/$4.40
    # ── Anthropic (USD×7.2) ───────────────────────────────────────────────────
    "claude-3-5-sonnet-20241022": {"input": 21.6, "output": 108.0},  # $3.00/$15.00
    "claude-3-5-haiku-20241022": {"input": 5.8, "output": 28.8},  # $0.80/$4.00
    "claude-3-opus-20240229": {"input": 108.0, "output": 540.0},  # $15.00/$75.00
    "claude-sonnet-4-6": {"input": 21.6, "output": 108.0},  # $3.00/$15.00
    "claude-haiku-4-5-20251001": {"input": 7.2, "output": 36.0},  # $1.00/$5.00
    "claude-opus-4-6": {"input": 108.0, "output": 540.0},  # $15.00/$75.00
    # ── Moonshot (USD×7.2; platform.moonshot.ai) ──────────────────────────────
    "moonshot-v1-8k": {"input": 1.4, "output": 14.4},  # $0.20/$2.00
    "moonshot-v1-32k": {"input": 7.2, "output": 21.6},  # $1.00/$3.00
    "moonshot-v1-128k": {"input": 14.4, "output": 36.0},  # $2.00/$5.00
    # ── Alibaba (Qwen; dashscope CNY pricing) ─────────────────────────────────
    "qwen-turbo": {"input": 0.3, "output": 0.6},
    "qwen-plus": {"input": 0.8, "output": 2.0},
    "qwen-max": {"input": 40.0, "output": 120.0},
    "qwen2.5-72b-instruct": {"input": 4.0, "output": 12.0},
    "qwen2.5-7b-instruct": {"input": 0.4, "output": 1.2},
    # ── MiniMax ───────────────────────────────────────────────────────────────
    "abab6.5s-chat": {"input": 1.0, "output": 1.0},
    "abab6.5-chat": {"input": 1.0, "output": 1.0},
}

# Provider-level fallback when model is not listed in MODEL_PRICING.
PRICING_TABLE: dict[ProviderType, dict[str, float]] = {
    ProviderType.ZHIPU: {"input": 0.5, "output": 2.0},  # GLM-4-Air level
    ProviderType.DEEPSEEK: {"input": 2.0, "output": 3.0},  # V3 rate
    ProviderType.OPENAI: {"input": 18.0, "output": 72.0},  # GPT-4o rate
    ProviderType.ANTHROPIC: {"input": 21.6, "output": 108.0},  # Sonnet rate
    ProviderType.MOONSHOT: {"input": 7.2, "output": 21.6},  # 32k rate
    ProviderType.ALIBABA: {"input": 1.0, "output": 3.0},
    ProviderType.MINIMAX: {"input": 1.0, "output": 1.0},
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
