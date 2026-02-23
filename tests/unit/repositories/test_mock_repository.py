# tests/unit/repositories/test_mock_repository.py
from src.models.transcription import Transcription
from src.repositories.mock_repository import MockTranscriptionRepository


def test_mock_repository_empty():
    repo = MockTranscriptionRepository()
    result = repo.get_all()

    assert len(result) == 0


def test_mock_repository_with_data():
    repo = MockTranscriptionRepository()
    data = [
        Transcription(id="1", timestamp=1000, content="test1"),
        Transcription(id="2", timestamp=2000, content="test2"),
    ]
    repo.set_data(data)

    result = repo.get_all()
    assert len(result) == 2
    assert result[0].content == "test1"


def test_mock_repository_generate():
    repo = MockTranscriptionRepository()
    repo.generate_mock(count=100, days=30)

    result = repo.get_all()
    assert len(result) == 100
