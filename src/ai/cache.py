import json
from datetime import UTC, datetime
from pathlib import Path

from src.models.ai_analysis import AIAnalysisCache, AITranscriptionAnalysis


class AICache:
    """AI analysis result cache manager.

    - Fixed cache path (data/ai_cache.json)
    - Keyed by transcription ID
    - Prints warning on model change; cached data remains usable
    - save() is synchronous; callers must hold asyncio.Lock in async contexts
    """

    def __init__(self, cache_path: Path, model: str, provider: str) -> None:
        self._path = cache_path
        self._model = model
        self._provider = provider
        self._data = self._load()

    def _load(self) -> AIAnalysisCache:
        """Load cache from disk; create fresh cache if file does not exist."""
        if not self._path.exists():
            return AIAnalysisCache(
                last_updated=datetime.now(UTC).isoformat(),
                model=self._model,
                provider=self._provider,
            )

        with open(self._path, encoding="utf-8") as f:
            raw = json.load(f)

        cache = AIAnalysisCache(**raw)

        # Warn on model change
        if cache.model != self._model:
            import logging

            logging.getLogger(__name__).warning(
                "Cache was built with %s/%s but current model is %s/%s. "
                "Cached entries will be reused; new entries use the current model. "
                "Run with --force-refresh to re-analyze everything.",
                cache.provider,
                cache.model,
                self._provider,
                self._model,
            )

        return cache

    def get(self, transcription_id: str) -> AITranscriptionAnalysis | None:
        """Return cached result, or None on cache miss."""
        return self._data.analyses.get(transcription_id)

    def set(self, transcription_id: str, analysis: AITranscriptionAnalysis) -> None:
        """Write to in-memory cache. Call save() to persist to disk."""
        self._data.analyses[transcription_id] = analysis
        self._data.last_updated = datetime.now(UTC).isoformat()

    def save(self) -> None:
        """Persist cache to disk. Callers must hold asyncio.Lock in async contexts."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data.model_dump(mode="json"), f, ensure_ascii=False, indent=2)

    def stats(self) -> dict:
        """Return cache statistics."""
        return {
            "total": len(self._data.analyses),
            "model": self._data.model,
            "provider": self._data.provider,
            "last_updated": self._data.last_updated,
            "size_bytes": self._path.stat().st_size if self._path.exists() else 0,
        }

    def clear(self) -> None:
        """Clear cache in memory and on disk."""
        self._data.analyses.clear()
        self.save()

    def uncached_ids(self, all_ids: list[str]) -> list[str]:
        """Return list of IDs not yet in cache."""
        return [id_ for id_ in all_ids if id_ not in self._data.analyses]
