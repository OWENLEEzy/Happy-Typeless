# src/nlp/strategies/segment_zh.py

import jieba

from src.nlp.strategies.segment import SegmentStrategy


class ChineseSegmentStrategy(SegmentStrategy):
    """Chinese word segmentation strategy using jieba"""

    def __init__(self, stop_words: set[str], filler_words: set[str] | None = None):
        self.stop_words = stop_words
        self.filler_words = filler_words or set()

    def segment(self, text: str) -> list[str]:
        """Segment Chinese text and filter stop words"""
        words = jieba.cut(text)
        return [w for w in words if len(w) > 1 and w not in self.stop_words and not w.isdigit()]

    def is_question(self, text: str) -> bool:
        """Check if Chinese text is a question"""
        question_marks = ["？", "?"]
        return any(mark in text for mark in question_marks)

    def is_stop_word(self, word: str) -> bool:
        """Check if word is a stop word (case-sensitive for Chinese)"""
        return self._check_word_in_set(word, self.stop_words, case_sensitive=True)

    def is_filler_word(self, word: str) -> bool:
        """Check if word is a filler word (case-sensitive for Chinese)"""
        return self._check_word_in_set(word, self.filler_words, case_sensitive=True)
