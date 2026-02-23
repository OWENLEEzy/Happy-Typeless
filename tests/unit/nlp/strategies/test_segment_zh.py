# tests/unit/nlp/strategies/test_segment_en.py
from src.nlp.strategies.segment_en import EnglishSegmentStrategy


def test_english_segment_fallback():
    strategy = EnglishSegmentStrategy(
        stop_words={"the", "a", "an"},
        spacy_model=None,  # Force fallback
    )

    result = strategy.segment("This is a test")

    assert "the" not in result
    assert "a" not in result
    assert "test" in result


def test_english_is_question():
    strategy = EnglishSegmentStrategy(stop_words=set())

    assert strategy.is_question("What is this?") is True
    assert strategy.is_question("How are you?") is True
    assert strategy.is_question("This is a statement.") is False
