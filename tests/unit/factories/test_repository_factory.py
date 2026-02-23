# tests/unit/factories/test_repository_factory.py
from src.factories.repository_factory import RepositoryFactory
from src.repositories.json_repository import JSONTranscriptionRepository
from src.repositories.mock_repository import MockTranscriptionRepository


def test_factory_creates_json_repository(tmp_path):
    factory = RepositoryFactory()
    json_file = tmp_path / "test.json"
    json_file.write_text("[]")

    repo = factory.create_json_repository(json_file)

    assert isinstance(repo, JSONTranscriptionRepository)
    assert repo.filepath == json_file


def test_factory_creates_mock_repository():
    factory = RepositoryFactory()
    repo = factory.create_mock_repository()

    assert isinstance(repo, MockTranscriptionRepository)


def test_factory_creates_from_path(tmp_path):
    factory = RepositoryFactory()

    # Create JSON file
    json_file = tmp_path / "data.json"
    json_file.write_text('[{"id":"1","timestamp":1000,"content":"test"}]')

    repo = factory.create_repository(json_file)

    assert isinstance(repo, JSONTranscriptionRepository)
