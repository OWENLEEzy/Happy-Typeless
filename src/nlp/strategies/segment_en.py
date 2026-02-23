# src/nlp/strategies/segment_en.py
import string

from src.nlp.strategies.segment import SegmentStrategy


class EnglishSegmentStrategy(SegmentStrategy):
    """English word segmentation strategy"""

    def __init__(
        self, stop_words: set[str], filler_words: set[str] | None = None, spacy_model=None
    ):
        self.stop_words = stop_words
        self.filler_words = filler_words or set()
        self.nlp = spacy_model

    def segment(self, text: str) -> list[str]:
        """Segment English text"""
        if self.nlp is not None:
            return self._segment_with_spacy(text)
        return self._segment_basic(text)

    def _segment_with_spacy(self, text: str) -> list[str]:
        """Segment using spaCy"""
        doc = self.nlp(text)
        return [
            token.text.lower()
            for token in doc
            if not token.is_stop
            and not token.is_punct
            and len(token.text) > 1
            and not token.text.isdigit()
        ]

    def _segment_basic(self, text: str) -> list[str]:
        """Fallback basic tokenization"""
        words = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
        return [w for w in words if len(w) > 1 and w not in self.stop_words and not w.isdigit()]

    def is_question(self, text: str) -> bool:
        """Check if English text is a question"""
        return "?" in text

    def is_stop_word(self, word: str) -> bool:
        """Check if word is a stop word (case-insensitive for English)"""
        return self._check_word_in_set(word, self.stop_words, case_sensitive=False)

    def is_filler_word(self, word: str) -> bool:
        """Check if word is a filler word (case-insensitive for English)"""
        return self._check_word_in_set(word, self.filler_words, case_sensitive=False)
