# src/nlp/strategies/segment.py
from abc import ABC, abstractmethod


class SegmentStrategy(ABC):
    """Word segmentation strategy interface"""

    @abstractmethod
    def segment(self, text: str) -> list[str]:
        """Segment text into words, filtering stop words

        Returns:
            List of filtered words
        """
        pass

    @abstractmethod
    def get_filler_words(self) -> set[str]:
        """Get set of filler words for this language.

        Returns:
            Set of filler words
        """
        pass

    @abstractmethod
    def get_connector_words(self) -> set[str]:
        """Get set of connector words for this language.

        Returns:
            Set of connector words
        """
        pass
