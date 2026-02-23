import asyncio
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

import instructor
from openai import AsyncOpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from src.ai.base import (
    JSON_MODE_PROVIDERS,
    OPENAI_COMPATIBLE_BASE_URLS,
    PRICING_TABLE,
    CostRecord,
    ModelConfig,
    ProviderType,
    TokenUsage,
)
from src.ai.cache import AICache
from src.ai.prompts import build_prompt
from src.models.ai_analysis import AITranscriptionAnalysis
from src.models.transcription import Transcription

logger = logging.getLogger(__name__)


def build_instructor_client(config: ModelConfig):
    """Build an instructor-wrapped async client.

    - OpenAI-compatible providers: from_openai (TOOLS or JSON mode)
    - Anthropic: from_anthropic (separate SDK)
    """
    if config.provider == ProviderType.ANTHROPIC:
        from anthropic import AsyncAnthropic

        return instructor.from_anthropic(AsyncAnthropic(api_key=config.api_key))

    base_url = config.base_url or OPENAI_COMPATIBLE_BASE_URLS[config.provider]
    raw = AsyncOpenAI(
        api_key=config.api_key,
        base_url=base_url,
        timeout=config.timeout,
    )
    mode = instructor.Mode.JSON if config.provider in JSON_MODE_PROVIDERS else instructor.Mode.TOOLS
    return instructor.from_openai(raw, mode=mode)


class AIClient:
    """Unified AI client with fallback, async parallel, and budget circuit breaker."""

    def __init__(
        self,
        primary: ModelConfig,
        cache: AICache,
        fallbacks: list[ModelConfig] | None = None,
        concurrency: int = 20,
        max_cost_cny: float = 10.0,
        cost_log_path: Path = Path("data/cost_log.json"),
    ) -> None:
        self._providers = [primary] + (fallbacks or [])
        self._clients = {cfg.provider: build_instructor_client(cfg) for cfg in self._providers}
        self._configs = {cfg.provider: cfg for cfg in self._providers}
        self._semaphore = asyncio.Semaphore(concurrency)
        self._max_cost = max_cost_cny
        self._cache = cache
        self._cost_log_path = cost_log_path
        self._total_cost: float = 0.0
        self._new_entries: int = 0
        self._cache_hits: int = 0
        self._failed_count: int = 0
        self._total_tokens: int = 0
        self._cache_lock = asyncio.Lock()

    def _primary_config(self) -> ModelConfig:
        return self._providers[0]

    def _exceeded_budget(self) -> bool:
        return self._total_cost >= self._max_cost

    @staticmethod
    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((TimeoutError, ConnectionError)),
        reraise=True,
    )
    async def _call_api(
        client, config: ModelConfig, prompt: str
    ) -> tuple[AITranscriptionAnalysis, object]:
        """Returns (parsed_model, raw_completion) to allow token usage extraction."""
        return await client.chat.completions.create_with_completion(
            model=config.model_name,
            messages=[{"role": "user", "content": prompt}],
            response_model=AITranscriptionAnalysis,
            max_retries=3,
            temperature=0.3,
        )

    def _calc_cost(self, provider: ProviderType, usage: TokenUsage) -> float:
        pricing = PRICING_TABLE.get(provider, {"input": 1.0, "output": 1.0})
        return (
            usage.prompt_tokens * pricing["input"] / 1_000_000
            + usage.completion_tokens * pricing["output"] / 1_000_000
        )

    async def _analyze_one(self, transcription: Transcription) -> AITranscriptionAnalysis | None:
        """Analyze a single transcription: return cache hit or call API."""
        cached = self._cache.get(transcription.id)
        if cached is not None:
            self._cache_hits += 1
            return cached

        async with self._semaphore:
            if self._exceeded_budget():
                return None

            prompt = build_prompt(
                transcription.content,
                transcription.timestamp,
                transcription.app_name,
            )

            for provider_type, client in self._clients.items():
                config = self._configs[provider_type]
                try:
                    result, completion = await self._call_api(client, config, prompt)

                    if completion.usage:
                        usage = TokenUsage(
                            prompt_tokens=completion.usage.prompt_tokens,
                            completion_tokens=completion.usage.completion_tokens,
                        )
                        call_cost = self._calc_cost(provider_type, usage)
                        self._total_cost += call_cost
                        self._total_tokens += usage.prompt_tokens + usage.completion_tokens

                    async with self._cache_lock:
                        self._cache.set(transcription.id, result)
                        self._new_entries += 1
                        if self._new_entries % 20 == 0:
                            self._cache.save()

                    return result

                except Exception as exc:
                    logger.warning(
                        "API call failed (provider=%s, id=%s): %s",
                        provider_type.value,
                        transcription.id,
                        exc,
                    )
                    continue

        self._failed_count += 1
        return None

    async def _analyze_batch_async(
        self, transcriptions: list[Transcription]
    ) -> list[AITranscriptionAnalysis | None]:
        from rich.progress import (
            BarColumn,
            MofNCompleteColumn,
            Progress,
            SpinnerColumn,
            TextColumn,
            TimeRemainingColumn,
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Analyzing...", total=len(transcriptions))

            async def wrapped(t: Transcription) -> AITranscriptionAnalysis | None:
                result = await self._analyze_one(t)
                desc = (
                    f"Analyzing  "
                    f"[green]cached: {self._cache_hits}[/green]  "
                    f"[cyan]new: {self._new_entries}[/cyan]"
                )
                if self._failed_count:
                    desc += f"  [red]failed: {self._failed_count}[/red]"
                progress.update(task, advance=1, description=desc)
                return result

            try:
                return await asyncio.gather(*[wrapped(t) for t in transcriptions])
            except asyncio.CancelledError:
                self._cache.save()
                raise

    def analyze_batch(
        self, transcriptions: list[Transcription]
    ) -> list[AITranscriptionAnalysis | None]:
        """Synchronous public interface; runs async internals via asyncio.run."""
        return asyncio.run(self._analyze_batch_async(transcriptions))

    def save_cost_log(self) -> None:
        """Append current run cost record to data/cost_log.json."""
        cfg = self._primary_config()
        record = CostRecord(
            date=datetime.now(UTC).isoformat(),
            provider=cfg.provider.value,
            model=cfg.model_name,
            new_entries=self._new_entries,
            cache_hits=self._cache_hits,
            tokens=self._total_tokens,
            cost_cny=round(self._total_cost, 4),
        )

        self._cost_log_path.parent.mkdir(parents=True, exist_ok=True)
        existing: list[dict] = []
        if self._cost_log_path.exists():
            with open(self._cost_log_path, encoding="utf-8") as f:
                existing = json.load(f)

        existing.append(record.model_dump())
        with open(self._cost_log_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
