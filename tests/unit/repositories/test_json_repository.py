# tests/unit/repositories/test_json_repository.py
import json

import pytest

from src.repositories.json_repository import JSONTranscriptionRepository


@pytest.fixture
def temp_json_file(tmp_path):
    data = [
        {
            "id": "1",
            "timestamp": 1737550800,
            "content": "测试内容",
            "duration": 15.5,
            "app_name": "WeChat",
        },
        {
            "id": "2",
            "timestamp": 1737554400,
            "content": "Another test content here",
            "duration": 10.0,
        },
    ]
    file_path = tmp_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return file_path


def test_json_repository_get_all(temp_json_file):
    repo = JSONTranscriptionRepository(temp_json_file)
    result = repo.get_all()

    assert len(result) == 2
    assert result[0].id == "1"
    assert result[0].content == "测试内容"
    assert result[1].content == "Another test content here"


def test_json_repository_dict_format(tmp_path):
    data = {"data": [{"id": "1", "timestamp": 1737550800, "content": "test"}]}
    file_path = tmp_path / "wrapped.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    repo = JSONTranscriptionRepository(file_path)
    result = repo.get_all()

    assert len(result) == 1
    assert result[0].id == "1"
