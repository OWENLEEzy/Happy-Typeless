# src/nlp/factory.py
from pathlib import Path

from src.config import Settings
from src.nlp.strategies.analysis import AnalysisStrategy
from src.nlp.strategies.segment import SegmentStrategy
from src.nlp.strategies.segment_en import EnglishSegmentStrategy
from src.nlp.strategies.segment_zh import ChineseSegmentStrategy


def load_words_from_file(filepath: Path) -> set[str]:
    """Load words from a text file"""
    if not filepath.exists():
        return set()

    words = set()
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                words.update(line.split())
    return words


class NLPProcessorFactory:
    """Factory for creating NLP processing strategies"""

    def __init__(self, config_dir: Path, config: Settings):
        self.config_dir = config_dir
        self.config = config
        self._strategies: dict[str, SegmentStrategy] = {}

    def get_segment_strategy(self, lang: str) -> SegmentStrategy:
        """Get segment strategy for language

        Args:
            lang: Language code ("zh", "en", etc.)

        Returns:
            SegmentStrategy instance
        """
        if lang not in self._strategies:
            self._strategies[lang] = self._create_segment_strategy(lang)
        return self._strategies[lang]

    def _create_segment_strategy(self, lang: str) -> SegmentStrategy:
        """Create segment strategy for language"""
        if lang == "zh":
            return ChineseSegmentStrategy(
                stop_words=self._load_word_type(lang, "stop_words"),
                filler_words=self._load_word_type(lang, "filler_words"),
            )
        elif lang == "en":
            return EnglishSegmentStrategy(
                stop_words=self._load_word_type(lang, "stop_words"),
                filler_words=self._load_word_type(lang, "filler_words"),
                spacy_model=self._load_spacy_if_available(),
            )
        else:
            # Default to Chinese
            return self._create_segment_strategy("zh")

    def _load_word_type(self, lang: str, word_type: str) -> set[str]:
        """Load word set for a specific language and word type

        Args:
            lang: Language code ("zh", "en", etc.)
            word_type: Type of word set ("stop_words" or "filler_words")

        Returns:
            Set of words for the specified language and type
        """
        nlp_config = self.config.nlp.get(lang)
        if nlp_config:
            path_attr = f"{word_type}_path"
            filepath = getattr(nlp_config, path_attr, None)
            if filepath:
                return load_words_from_file(filepath)
        return set()

    def _load_spacy_if_available(self):
        """Load spaCy model if available"""
        try:
            import spacy

            return spacy.load("en_core_web_sm")
        except (OSError, ImportError):
            return None

    def get_analysis_strategy(self, lang: str = "zh") -> AnalysisStrategy:
        """Get batch analysis strategy for language

        Args:
            lang: Language code ("zh", "en", etc.)

        Returns:
            AnalysisStrategy instance with segment strategy
        """
        segment = self.get_segment_strategy(lang)
        return AnalysisStrategy(segment)
