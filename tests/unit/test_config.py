import pytest
from pydantic import ValidationError

from src.config import Settings, ThresholdConfig, get_settings


def test_settings_defaults():
    settings = Settings()
    assert settings.base_dir.exists()
    assert settings.config_dir.name == "config"
    assert settings.data_dir.name == "data"


def test_settings_thresholds():
    settings = Settings()
    assert settings.thresholds.short_sentence == 20
    assert settings.thresholds.long_sentence == 100
    assert settings.thresholds.fragmentation_high == 70


def test_get_settings_singleton():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2  # Same instance


# ── New threshold fields ───────────────────────────────────────────────────────


def test_threshold_personality_defaults():
    t = ThresholdConfig()
    assert t.conscientiousness_high == 0.6
    assert t.conscientiousness_low == 0.4
    assert t.question_ratio_high == 30
    assert t.command_ratio_min == 20
    assert t.neg_ratio_low == 10
    assert t.neg_ratio_high == 30
    assert t.work_efficiency_high == 70
    assert t.work_efficiency_low == 30


def test_threshold_efficiency_defaults():
    t = ThresholdConfig()
    assert t.late_night_score_zero_at == 0.5
    assert t.work_efficiency_full_at == 0.6
    assert t.focus_min_seconds == 10.0
    assert t.focus_optimal_seconds == 30.0
    assert t.focus_decay_seconds == 30.0


def test_cache_save_frequency_default():
    s = Settings()
    assert s.ai_cache_save_frequency == 20


# ── Field(gt=0) / Field(ge=1) constraints (BUG-01, BUG-02) ───────────────────


def test_cache_save_frequency_rejects_zero():
    with pytest.raises(ValidationError):
        Settings(ai_cache_save_frequency=0)


def test_cache_save_frequency_rejects_negative():
    with pytest.raises(ValidationError):
        Settings(ai_cache_save_frequency=-5)


def test_efficiency_thresholds_reject_zero():
    for field in [
        "late_night_score_zero_at",
        "work_efficiency_full_at",
        "focus_min_seconds",
        "focus_optimal_seconds",
        "focus_decay_seconds",
    ]:
        with pytest.raises(ValidationError, match=field):
            ThresholdConfig(**{field: 0.0})


# ── Cross-field validators (BUG-04, BUG-07) ───────────────────────────────────


def test_focus_range_inverted_raises():
    with pytest.raises(ValidationError):
        ThresholdConfig(focus_min_seconds=60.0, focus_optimal_seconds=10.0)


def test_conscientiousness_inverted_raises():
    with pytest.raises(ValidationError):
        ThresholdConfig(conscientiousness_high=0.3, conscientiousness_low=0.8)


def test_neg_ratio_inverted_raises():
    with pytest.raises(ValidationError):
        ThresholdConfig(neg_ratio_high=5, neg_ratio_low=30)


def test_work_efficiency_inverted_raises():
    with pytest.raises(ValidationError):
        ThresholdConfig(work_efficiency_high=20, work_efficiency_low=80)


# ── Computed paths ────────────────────────────────────────────────────────────


def test_computed_paths_follow_data_dir():
    s = Settings()
    assert s.cache_path == s.data_dir / "ai_cache.json"
    assert s.cost_log_path == s.data_dir / "cost_log.json"
    assert s.temp_export_path == s.data_dir / "raw" / "temp_export.json"
    assert s.default_report_path == s.output_dir / "personal" / "Typeless_Report.html"


# ── _build_personality_profile threshold paths (BUG-06) ──────────────────────


def test_build_personality_profile_uses_injected_thresholds():
    """Function must honour injected thresholds, not pull from global state."""
    from src.cli import _build_personality_profile
    from src.translations import I18n

    strict = ThresholdConfig(
        conscientiousness_high=0.9,  # very hard to be "concise"
        conscientiousness_low=0.1,  # very hard to be "verbose"
        neg_ratio_low=1,
        neg_ratio_high=99,
        work_efficiency_high=99,
        work_efficiency_low=1,
    )
    i18n = I18n("zh")

    result = _build_personality_profile(
        ai_personality={"conscientiousness": 0.5},  # in-between → "moderate"
        intent_dist={"statement": 10},
        sentiment_dist={"neutral": 10},
        work_efficiency=50,
        i18n=i18n,
        thresholds=strict,
    )
    names = [tag["name"] for tag in result["tags"]]
    # With strict thresholds, 0.5 conscientiousness should yield "moderate" tag
    moderate_key = i18n.t("tag_moderate")
    assert moderate_key in names


def test_build_personality_profile_questioner_tag():
    from src.cli import _build_personality_profile
    from src.translations import I18n

    t = ThresholdConfig()
    i18n = I18n("zh")
    result = _build_personality_profile(
        ai_personality={"conscientiousness": 0.5},
        intent_dist={"question": 40, "statement": 60},  # 40% > threshold 30%
        sentiment_dist={"neutral": 100},
        work_efficiency=50,
        i18n=i18n,
        thresholds=t,
    )
    names = [tag["name"] for tag in result["tags"]]
    assert i18n.t("tag_questioner") in names
