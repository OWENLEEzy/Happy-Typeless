# src/nlp/strategies/segment_zh.py

import jieba

from src.nlp.strategies.segment import SegmentStrategy


class ChineseSegmentStrategy(SegmentStrategy):
    """Chinese word segmentation strategy using jieba"""

    def __init__(
        self,
        stop_words: set[str],
        filler_words: set[str] | None = None,
        connector_words: set[str] | None = None,
    ):
        self.stop_words = stop_words
        self.filler_words = filler_words or set()
        self.connector_words = connector_words or set()

    def segment(self, text: str) -> list[str]:
        """Segment Chinese text and filter stop and filler words"""
        words = jieba.cut(text)
        return [
            w
            for w in words
            if len(w) > 1
            and w not in self.stop_words
            and w not in self.filler_words
            and not w.isdigit()
        ]

    def get_filler_words(self) -> set[str]:
        """Get set of filler words for Chinese."""
        return self.filler_words

    def get_connector_words(self) -> set[str]:
        """Get set of connector words for Chinese."""
        return self.connector_words

    def is_stop_word(self, word: str) -> bool:
        """Check if word is a stop word."""
        return word in self.stop_words

    def is_filler_word(self, word: str) -> bool:
        """Check if word is a filler word."""
        return word in self.filler_words
