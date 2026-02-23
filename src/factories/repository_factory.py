# src/factories/repository_factory.py
from pathlib import Path

from src.repositories.base import TranscriptionRepository
from src.repositories.json_repository import JSONTranscriptionRepository
from src.repositories.mock_repository import MockTranscriptionRepository


class RepositoryFactory:
    """Factory for creating repository instances"""

    def create_json_repository(self, filepath: Path) -> JSONTranscriptionRepository:
        """Create JSON repository"""
        return JSONTranscriptionRepository(filepath)

    def create_mock_repository(self) -> MockTranscriptionRepository:
        """Create mock repository"""
        return MockTranscriptionRepository()

    def create_repository(self, source: Path | str | None = None) -> TranscriptionRepository:
        """Create repository based on source type

        Args:
            source: File path for JSON, or None for mock

        Returns:
            Appropriate repository instance
        """
        if source is None:
            return self.create_mock_repository()

        source_path = Path(source) if isinstance(source, str) else source
        return self.create_json_repository(source_path)
