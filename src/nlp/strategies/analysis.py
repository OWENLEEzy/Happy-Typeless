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

    def get_word_categories(self, data: TranscriptionList) -> dict[str, int]:
        """Categorize words into filler, connector, and content words.

        Returns:
            Dictionary with keys 'filler', 'connector', 'content' and their counts.
        """
        filler_count = 0
        connector_count = 0
        content_count = 0

        filler_words = self.segment.get_filler_words()
        connector_words = self.segment.get_connector_words()

        for t in data:
            words = self.segment.segment(t.content)
            for word in words:
                if word in filler_words:
                    filler_count += 1
                elif word in connector_words:
                    connector_count += 1
                else:
                    content_count += 1

        return {
            "filler": filler_count,
            "connector": connector_count,
            "content": content_count,
        }

    def get_top_phrases(self, data: TranscriptionList, limit: int = 10) -> list[dict]:
        """Get top recurring phrases/n-grams.

        Args:
            data: Transcription data list
            limit: Maximum number of phrases to return

        Returns:
            List of dicts with 'phrase' and 'count' keys.
        """

        phrase_counts: Counter = Counter()

        for t in data:
            words = self.segment.segment(t.content)
            # Extract 2-grams and 3-grams
            for n in [2, 3]:
                for i in range(len(words) - n + 1):
                    phrase = " ".join(words[i : i + n])
                    # Skip if contains too many stop words
                    word_list = phrase.split()
                    if len(word_list) == n:
                        phrase_counts[phrase] += 1

        # Only return phrases that appear at least twice
        filtered = {p: c for p, c in phrase_counts.items() if c >= 2}
        return [
            {"phrase": phrase, "count": count}
            for phrase, count in sorted(filtered.items(), key=lambda x: -x[1])[:limit]
        ]
