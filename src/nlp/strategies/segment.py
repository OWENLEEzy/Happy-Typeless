# src/nlp/strategies/segment.py
from abc import ABC, abstractmethod


class SegmentStrategy(ABC):
    """Word segmentation strategy interface

    Provides default implementations for word checking methods that
    can be reused by subclasses with different case-sensitivity needs.
    """

    @abstractmethod
    def segment(self, text: str) -> list[str]:
        """Segment text into words, filtering stop words

        Returns:
            List of filtered words
        """
        pass

    @abstractmethod
    def is_question(self, text: str) -> bool:
        """Check if text is a question"""
        pass

    @abstractmethod
    def is_stop_word(self, word: str) -> bool:
        """Check if word is a stop word"""
        pass

    @abstractmethod
    def is_filler_word(self, word: str) -> bool:
        """Check if word is a filler word"""
        pass

    def _check_word_in_set(
        self, word: str, word_set: set[str], *, case_sensitive: bool = True
    ) -> bool:
        """Check if word is in a set, with optional case-insensitive matching

        This is a utility method for subclasses to reuse common word checking logic.

        Args:
            word: The word to check
            word_set: The set of words to check against
            case_sensitive: Whether to do case-sensitive matching (default: True)

        Returns:
            True if the word is in the set (respecting case sensitivity setting)
        """
        if case_sensitive:
            return word in word_set
        word_lower = word.lower()
        return any(w.lower() == word_lower for w in word_set)
