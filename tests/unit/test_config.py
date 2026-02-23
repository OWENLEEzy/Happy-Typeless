# tests/unit/test_config.py
from src.config import Settings, get_settings


def test_settings_defaults():
    settings = Settings()
    assert settings.base_dir.exists()
    assert settings.config_dir.name == "config"
    assert settings.data_dir.name == "data"


def test_settings_thresholds():
    settings = Settings()
    assert settings.thresholds.concise == 30
    assert settings.thresholds.verbose == 80
    assert settings.thresholds.question_high == 30


def test_get_settings_singleton():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2  # Same instance
