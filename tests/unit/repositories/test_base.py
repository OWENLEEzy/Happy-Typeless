# tests/unit/repositories/test_base.py
from abc import ABC

import pytest

from src.repositories.base import TranscriptionRepository


def test_repository_is_abstract():
    assert issubclass(TranscriptionRepository, ABC)


def test_cannot_instantiate_abstract_repository():
    with pytest.raises(TypeError):
        TranscriptionRepository()


def test_repository_has_required_methods():
    assert hasattr(TranscriptionRepository, "get_all")
