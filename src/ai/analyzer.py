from pathlib import Path

from src.ai.base import ModelConfig
from src.ai.cache import AICache
from src.ai.client import AIClient
from src.models.ai_analysis import AITranscriptionAnalysis
from src.models.transcription import TranscriptionList


class AIAnalyzer:
    """Batch AI analyzer encapsulating cache, client, and cost logging."""

    def __init__(
        self,
        primary: ModelConfig,
        cache_path: Path = Path("data/ai_cache.json"),
        fallbacks: list[ModelConfig] | None = None,
        concurrency: int = 20,
        max_cost_cny: float = 10.0,
        force_refresh: bool = False,
        cost_log_path: Path = Path("data/cost_log.json"),
    ) -> None:
        self._cache = AICache(
            cache_path,
            model=primary.model_name,
            provider=primary.provider.value,
        )
        if force_refresh:
            self._cache.clear()

        self._client = AIClient(
            primary=primary,
            cache=self._cache,
            fallbacks=fallbacks,
            concurrency=concurrency,
            max_cost_cny=max_cost_cny,
            cost_log_path=cost_log_path,
        )

    def analyze(self, transcriptions: TranscriptionList) -> dict[str, AITranscriptionAnalysis]:
        """Analyze all items; return {transcription_id: analysis}.

        - Cache hits skip API calls
        - Failed API calls are excluded from results
        - Cache and cost log are saved even on KeyboardInterrupt
        """
        try:
            results_list = self._client.analyze_batch(list(transcriptions))
        finally:
            self._cache.save()
            self._client.save_cost_log()

        results: dict[str, AITranscriptionAnalysis] = {}
        for transcription, result in zip(transcriptions, results_list):
            if result is not None:
                results[transcription.id] = result
        return results

    @property
    def cache_hits(self) -> int:
        """Number of cache hits in the last analyze() call."""
        return self._client._cache_hits

    @property
    def failed_count(self) -> int:
        """Number of entries where all API providers failed."""
        return self._client._failed_count

    @property
    def run_cost(self) -> float:
        """Total API cost (CNY) for this run."""
        return self._client._total_cost

    @property
    def new_entries(self) -> int:
        """Number of entries newly analyzed via API (not from cache)."""
        return self._client._new_entries
