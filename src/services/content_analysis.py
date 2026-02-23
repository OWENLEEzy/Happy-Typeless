# src/services/content_analysis.py
import re

from src.config import get_settings
from src.models.analysis import (
    ContentAnalysis,
    LongestYap,
    SentenceLengthDistribution,
    TopicDistribution,
    WordFrequency,
)
from src.models.transcription import TranscriptionList
from src.nlp.factory import NLPProcessorFactory


class ContentAnalysisService:
    """Service for deep content analysis"""

    def __init__(self, data: TranscriptionList, lang: str = "zh"):
        self.data = data
        self.lang = lang
        self.settings = get_settings()
        self.nlp_factory = NLPProcessorFactory(self.settings.config_dir, self.settings)
        self.analysis_strategy = self.nlp_factory.get_analysis_strategy(lang)
        self.thresholds = self.settings.thresholds

    def analyze_content(self) -> ContentAnalysis:
        """Analyze content themes, word frequency, and sentence length

        Returns:
            ContentAnalysis with topic distribution, sentence length
            distribution, longest yap, and word cloud
        """
        topic_distribution = self._classify_topics()
        length_distribution = self._analyze_sentence_length()
        longest_yap = self._get_longest_yap()
        word_cloud = self._get_word_cloud(limit=50)

        return ContentAnalysis(
            topic_distribution=topic_distribution,
            sentence_length_distribution=length_distribution,
            longest_yap=longest_yap,
            word_cloud=word_cloud,
        )

    def _classify_topics(self) -> TopicDistribution:
        """Classify content into topics (AI, design, daily)"""
        ai_keywords = self.thresholds.ai_keywords
        design_keywords = self.thresholds.design_keywords

        ai_pattern = re.compile("|".join(ai_keywords), re.IGNORECASE)
        design_pattern = re.compile("|".join(design_keywords), re.IGNORECASE)

        ai_only = 0
        design_only = 0
        both = 0

        for t in self.data:
            has_ai = bool(ai_pattern.search(t.content))
            has_design = bool(design_pattern.search(t.content))

            if has_ai and not has_design:
                ai_only += 1
            elif has_design and not has_ai:
                design_only += 1
            elif has_ai and has_design:
                both += 1

        total = len(self.data)
        daily_count = total - ai_only - design_only - both

        return TopicDistribution(
            ai=ai_only + both,
            design=design_only + both,
            daily=daily_count,
            ai_ratio=round((ai_only + both) / max(total, 1) * 100, 1),
            design_ratio=round((design_only + both) / max(total, 1) * 100, 1),
            daily_ratio=round(daily_count / max(total, 1) * 100, 1),
        )

    def _analyze_sentence_length(self) -> SentenceLengthDistribution:
        """Analyze sentence length distribution"""
        short_threshold = self.thresholds.short_sentence
        long_threshold = self.thresholds.long_sentence

        short = sum(1 for t in self.data if len(t.content) < short_threshold)
        long = sum(1 for t in self.data if len(t.content) >= long_threshold)
        medium = len(self.data) - short - long

        total = len(self.data)

        return SentenceLengthDistribution(
            short=short,
            medium=medium,
            long=long,
            short_ratio=round(short / max(total, 1) * 100, 1),
            medium_ratio=round(medium / max(total, 1) * 100, 1),
            long_ratio=round(long / max(total, 1) * 100, 1),
        )

    def _get_longest_yap(self) -> LongestYap:
        """Get the longest voice recording"""
        if len(self.data) == 0:
            return LongestYap(content="", word_count=0, date="", hour=0, duration=0.0)

        # Find by duration or word count
        if all(t.duration is not None for t in self.data):
            longest = max(self.data.items, key=lambda t: t.duration or 0)
        else:
            longest = max(self.data.items, key=lambda t: len(t.content))

        return LongestYap(
            content=longest.content,
            word_count=len(longest.content),
            date=longest.date,
            hour=longest.datetime.hour,
            duration=longest.duration or len(longest.content) / 3,
        )

    def _get_word_cloud(self, limit: int = 50) -> list[WordFrequency]:
        """Get word frequency cloud"""
        return self.analysis_strategy.get_word_frequency(self.data, limit)
