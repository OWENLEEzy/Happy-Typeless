# tests/unit/nlp/strategies/test_segment_zh.py
from src.nlp.strategies.segment_zh import ChineseSegmentStrategy


def test_chinese_segment():
    strategy = ChineseSegmentStrategy(stop_words={"的", "了", "是", "在", "我"})

    result = strategy.segment("我测试一下分词功能")

    assert "我" not in result  # Stop word filtered
    assert "测试" in result
    assert "分词" in result
    assert "功能" in result


def test_chinese_is_question():
    strategy = ChineseSegmentStrategy(stop_words=set())

    assert strategy.is_question("这是什么？") is True
    assert strategy.is_question("What is this?") is True
    assert strategy.is_question("这是一个陈述句") is False
