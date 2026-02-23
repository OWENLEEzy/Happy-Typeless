# tests/unit/nlp/strategies/test_segment.py
from abc import ABC

from src.nlp.strategies.segment import SegmentStrategy


def test_segment_strategy_is_abstract():
    assert issubclass(SegmentStrategy, ABC)


def test_segment_strategy_has_required_methods():
    assert hasattr(SegmentStrategy, "segment")
    assert hasattr(SegmentStrategy, "is_question")
    assert hasattr(SegmentStrategy, "is_stop_word")
    assert hasattr(SegmentStrategy, "is_filler_word")
