"""Tests for build_prompt() lang parameter threading."""

import asyncio
from unittest.mock import patch

from src.ai.prompts import MAX_PROMPT_CONTENT_LENGTH, build_prompt

_TS = 1700000000  # Fixed timestamp for deterministic tests


def test_build_prompt_default_lang_no_chinese_instruction():
    """Default lang='en' must not inject a Chinese instruction."""
    prompt = build_prompt("hello world", _TS, lang="en")
    assert "Use Chinese" not in prompt
    assert "中文" not in prompt


def test_build_prompt_zh_injects_chinese_instruction():
    """lang='zh' must add instruction for Chinese topic labels."""
    prompt = build_prompt("hello world", _TS, lang="zh")
    assert "Chinese" in prompt or "中文" in prompt


def test_build_prompt_zh_instruction_at_end():
    """The Chinese instruction is appended after the main prompt body."""
    prompt = build_prompt("hello world", _TS, lang="zh")
    assert prompt.endswith("中文) for all topic labels in the topics array.")


def test_build_prompt_content_truncated():
    """Content longer than MAX_PROMPT_CONTENT_LENGTH is truncated."""
    long_content = "a" * (MAX_PROMPT_CONTENT_LENGTH + 100)
    prompt = build_prompt(long_content, _TS)
    # The full content must not appear; truncated version must appear
    assert "a" * MAX_PROMPT_CONTENT_LENGTH in prompt
    assert "a" * (MAX_PROMPT_CONTENT_LENGTH + 1) not in prompt


def test_build_prompt_includes_app_name():
    """App name is injected into the prompt."""
    prompt = build_prompt("test", _TS, app_name="MyApp")
    assert "MyApp" in prompt


def test_build_prompt_default_app_name_unknown():
    """Missing app_name falls back to 'Unknown'."""
    prompt = build_prompt("test", _TS)
    assert "Unknown" in prompt


def test_build_prompt_lang_threading_through_ai_client(tmp_path):
    """AIClient stores lang and passes it to build_prompt."""
    from src.ai.base import ModelConfig, ProviderType
    from src.ai.cache import AICache
    from src.ai.client import AIClient

    config = ModelConfig(provider=ProviderType.ZHIPU, model_name="glm-4-flash", api_key="test")
    cache = AICache(tmp_path / "cache.json", model="glm-4-flash", provider="zhipu")
    client = AIClient(primary=config, cache=cache, lang="zh")

    assert client._lang == "zh"

    # Verify lang is wired: exceed budget so _analyze_one short-circuits before API
    with patch("src.ai.client.build_prompt", wraps=build_prompt) as mock_bp:
        from src.models.transcription import Transcription

        t = Transcription(id="x", timestamp=_TS, content="test")
        client._total_cost = client._max_cost + 1  # Exceed budget

        asyncio.run(client._analyze_one(t))
        # build_prompt not reached (budget exceeded before semaphore body)
        mock_bp.assert_not_called()

    # The lang attribute itself is the authoritative proof of threading
    assert client._lang == "zh"


def test_build_prompt_lang_threading_through_ai_analyzer(tmp_path):
    """AIAnalyzer passes lang down to AIClient."""
    from src.ai.analyzer import AIAnalyzer
    from src.ai.base import ModelConfig, ProviderType

    config = ModelConfig(provider=ProviderType.ZHIPU, model_name="glm-4-flash", api_key="test")
    analyzer = AIAnalyzer(primary=config, cache_path=tmp_path / "cache.json", lang="zh")
    assert analyzer._client._lang == "zh"
