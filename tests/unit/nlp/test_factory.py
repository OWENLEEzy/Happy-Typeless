# tests/unit/nlp/test_factory.py
from src.config import get_settings
from src.nlp.factory import NLPProcessorFactory
from src.nlp.strategies.segment_en import EnglishSegmentStrategy
from src.nlp.strategies.segment_zh import ChineseSegmentStrategy


def test_factory_creates_chinese_strategy():
    settings = get_settings()
    factory = NLPProcessorFactory(settings.config_dir, settings)

    strategy = factory.get_segment_strategy("zh")

    assert isinstance(strategy, ChineseSegmentStrategy)


def test_factory_creates_english_strategy():
    settings = get_settings()
    factory = NLPProcessorFactory(settings.config_dir, settings)

    strategy = factory.get_segment_strategy("en")

    assert isinstance(strategy, EnglishSegmentStrategy)


def test_factory_caches_strategies():
    settings = get_settings()
    factory = NLPProcessorFactory(settings.config_dir, settings)

    s1 = factory.get_segment_strategy("zh")
    s2 = factory.get_segment_strategy("zh")

    assert s1 is s2  # Same instance
