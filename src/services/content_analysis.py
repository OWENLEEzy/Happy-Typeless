# src/services/content_analysis.py
from collections import defaultdict

from src.config import get_settings
from src.models.analysis import (
    ContentAnalysis,
    LongestYap,
    SentenceLengthDistribution,
    WordFrequency,
)
from src.models.transcription import TranscriptionList
from src.nlp.factory import NLPProcessorFactory


def _load_topic_keywords(filepath) -> dict[str, set[str]]:
    """Load topic keywords from file, organized by category.

    Each line in the file represents a topic category followed by its keywords.
    Format: "category keyword1 keyword2 keyword3 ..."

    Args:
        filepath: Path to the topic keywords file.

    Returns:
        Dictionary mapping category names to sets of keywords.
    """
    if not filepath.exists():
        return {}

    topics: dict[str, set[str]] = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if parts:
                category = parts[0]
                keywords = set(parts[1:])
                topics[category] = keywords
    return topics


class ContentAnalysisService:
    """Service for deep content analysis"""

    def __init__(self, data: TranscriptionList, lang: str = "en"):
        self.data = data
        self.lang = lang
        self.settings = get_settings()
        self.nlp_factory = NLPProcessorFactory(self.settings.config_dir, self.settings)
        self.analysis_strategy = self.nlp_factory.get_analysis_strategy(lang)
        self.thresholds = self.settings.thresholds

        # Load topic keywords from config file
        nlp_config = self.settings.nlp.get(lang, self.settings.nlp.get("en"))
        if nlp_config:
            self.topic_keywords = _load_topic_keywords(nlp_config.topic_keywords_path)
        else:
            self.topic_keywords = {}

    def analyze_content(self) -> ContentAnalysis:
        """Analyze word frequency and sentence length distribution.

        Returns:
            ContentAnalysis with sentence length distribution, longest yap,
            word cloud, topic distribution, word categories, and top phrases.
        """
        length_distribution = self._analyze_sentence_length()
        longest_yap = self._get_longest_yap()
        word_cloud = self._get_word_cloud(limit=50)
        topic_distribution = self._classify_topics()
        word_categories = self._get_word_categories()
        top_phrases = self._get_top_phrases()

        return ContentAnalysis(
            sentence_length_distribution=length_distribution,
            longest_yap=longest_yap,
            word_cloud=word_cloud,
            topic_distribution=topic_distribution,
            word_categories=word_categories,
            top_phrases=top_phrases,
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
        """Get the recording with the most text content."""
        if len(self.data) == 0:
            return LongestYap(content="", word_count=0, date="", hour=0, duration=0.0)

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

    def _classify_topics(self) -> dict[str, int]:
        """Classify content into topics using keyword matching.

        Returns:
            Dictionary mapping topic names to occurrence counts.
        """
        topics: dict[str, int] = defaultdict(int)
        matched_count = 0

        # Map file category names to internal topic names
        category_mapping = {
            "ai": "ai_tech",
            "人工智能": "ai_tech",
            "design": "design",
            "设计": "design",
            "work": "work",
            "工作": "work",
        }

        for entry in self.data.items:
            content_lower = entry.content.lower()
            matched = False

            # Check each topic category from the loaded keywords
            for category, keywords in self.topic_keywords.items():
                if any(kw in content_lower for kw in keywords):
                    internal_name = category_mapping.get(category, category)
                    topics[internal_name] += 1
                    matched = True

            if matched:
                matched_count += 1

        # Add daily/life for entries that didn't match any topic
        if matched_count < len(self.data):
            topics["daily"] = len(self.data) - matched_count

        return dict(sorted(topics.items(), key=lambda x: -x[1]))

    def _get_word_categories(self) -> dict[str, int]:
        """Categorize words into filler, connector, and content words.

        Returns:
            Dictionary with 'filler', 'connector', 'content' keys and counts.
        """
        return self.analysis_strategy.get_word_categories(self.data)

    def _get_top_phrases(self, limit: int = 10) -> list[dict]:
        """Get top recurring phrases/n-grams.

        Returns:
            List of dicts with 'phrase' and 'count' keys.
        """
        return self.analysis_strategy.get_top_phrases(self.data, limit)
