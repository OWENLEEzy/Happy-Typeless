# src/nlp/strategies/analysis.py
"""Batch analysis strategy for aggregating NLP operations.

This module provides AnalysisStrategy, which wraps SegmentStrategy to offer
batch processing methods. This eliminates code duplication in the Service layer.
"""

from collections import Counter
from typing import TYPE_CHECKING

from src.models.analysis import WordFrequency
from src.models.transcription import TranscriptionList

if TYPE_CHECKING:
    from src.nlp.strategies.segment import SegmentStrategy


class AnalysisStrategy:
    """Batch analysis strategy for NLP operations.

    Wraps SegmentStrategy to provide batch processing methods, avoiding
    repetitive loop logic in the Service layer.

    Example:
        >>> strategy = factory.get_analysis_strategy("zh")
        >>> word_freq = strategy.get_word_frequency(data, limit=30)
        >>> question_count = strategy.count_questions(data)

    Args:
        segment_strategy: Strategy for word segmentation and question detection
    """

    def __init__(self, segment_strategy: "SegmentStrategy"):
        self.segment = segment_strategy

    # ===== Text Analysis Batch Methods =====

    def get_word_frequency(self, data: TranscriptionList, limit: int = 30) -> list[WordFrequency]:
        """Get word frequency statistics.

        Args:
            data: Transcription data list
            limit: Maximum number of words to return

        Returns:
            List of word frequencies, sorted by frequency descending
        """
        all_words = []
        for t in data:
            all_words.extend(self.segment.segment(t.content))

        counts = Counter(all_words)
        return [WordFrequency(name=word, value=count) for word, count in counts.most_common(limit)]

    def count_questions(self, data: TranscriptionList) -> int:
        """Count question sentences.

        Args:
            data: Transcription data list

        Returns:
            Number of question sentences
        """
        return sum(1 for t in data if self.segment.is_question(t.content))

    def get_question_ratio(self, data: TranscriptionList) -> tuple[int, float]:
        """Get question sentence ratio.

        Args:
            data: Transcription data list

        Returns:
            Tuple of (question_count, question_percentage)
        """
        count = self.count_questions(data)
        total = max(len(data), 1)
        ratio = count / total * 100
        return count, round(ratio, 1)
