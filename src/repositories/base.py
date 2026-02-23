# src/repositories/base.py
from abc import ABC, abstractmethod

from src.models.transcription import TranscriptionList


class TranscriptionRepository(ABC):
    """Transcription repository interface"""

    @abstractmethod
    def get_all(self) -> TranscriptionList:
        """Get all transcription records

        Returns:
            All transcriptions in the repository
        """
        pass
