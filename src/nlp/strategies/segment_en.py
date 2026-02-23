# src/nlp/strategies/segment_en.py
import string

from src.nlp.strategies.segment import SegmentStrategy


class EnglishSegmentStrategy(SegmentStrategy):
    """English word segmentation strategy"""

    def __init__(
        self,
        stop_words: set[str],
        filler_words: set[str] | None = None,
        connector_words: set[str] | None = None,
        spacy_model=None,
    ):
        self.stop_words = stop_words
        self.filler_words = filler_words or set()
        self.nlp = spacy_model
        self.connector_words = connector_words or set()

    def segment(self, text: str) -> list[str]:
        """Segment English text"""
        if self.nlp is not None:
            return self._segment_with_spacy(text)
        return self._segment_basic(text)

    def _segment_with_spacy(self, text: str) -> list[str]:
        """Segment using spaCy"""
        if self.nlp is None:
            return self._segment_basic(text)
        doc = self.nlp(text)
        return [
            token.text.lower()
            for token in doc
            if not token.is_stop
            and not token.is_punct
            and len(token.text) > 1
            and not token.text.isdigit()
            and token.text.lower() not in self.filler_words
        ]

    def _segment_basic(self, text: str) -> list[str]:
        """Fallback basic tokenization"""
        words = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
        return [
            w
            for w in words
            if len(w) > 1
            and w not in self.stop_words
            and w not in self.filler_words
            and not w.isdigit()
        ]

    def get_filler_words(self) -> set[str]:
        """Get set of filler words for English."""
        return self.filler_words

    def get_connector_words(self) -> set[str]:
        """Get set of connector words for English."""
        return self.connector_words
