import platform
from pathlib import Path

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ThresholdConfig(BaseModel):
    """Various threshold values"""

    fragmentation_high: int = 70
    fragmentation_low: int = 40
    short_sentence: int = 20
    long_sentence: int = 100

    # Time periods
    late_night_hours: list[int] = list(range(23, 24)) + list(range(0, 7))
    work_hours: list[int] = list(range(9, 19))

    # Badge levels (name is i18n key)
    badge_levels: list[tuple[int, str, str, str]] = [
        (10000, "badge_keyboard_terminator", "⌨️", "#3B82F6"),
        (50000, "badge_chatterbox", "🗣️", "#CD7F32"),
        (100000, "badge_human_typewriter", "⌨️", "#C0C0C0"),
        (500000, "badge_socrates", "🏛️", "#FFD700"),
    ]

    # Personality tag thresholds
    conscientiousness_high: float = 0.6
    conscientiousness_low: float = 0.4
    question_ratio_high: int = 30  # percentage; above → "questioner"
    command_ratio_min: int = 20  # percentage; above → "commander"
    neg_ratio_low: int = 10  # percentage; below → "stable"
    neg_ratio_high: int = 30  # percentage; above → "emotional"
    work_efficiency_high: int = 70  # percentage; above → "workaholic"
    work_efficiency_low: int = 30  # percentage; below → "lifestyle"

    # Efficiency score thresholds (must be > 0 to avoid ZeroDivisionError in score formulas)
    late_night_score_zero_at: float = Field(default=0.5, gt=0)
    work_efficiency_full_at: float = Field(default=0.6, gt=0)
    focus_min_seconds: float = Field(default=10.0, gt=0)
    focus_optimal_seconds: float = Field(default=30.0, gt=0)
    # Separate denominator for the penalty slope above the optimal range.
    # Decoupled from focus_optimal_seconds so adjusting the upper bound
    # does not silently change how steeply the score falls for long entries.
    focus_decay_seconds: float = Field(default=30.0, gt=0)

    @model_validator(mode="after")
    def check_threshold_pairs(self) -> "ThresholdConfig":
        """Validate that high/low pairs are correctly ordered and focus range is valid."""
        pairs = [
            ("conscientiousness_high", "conscientiousness_low"),
            ("neg_ratio_high", "neg_ratio_low"),
            ("work_efficiency_high", "work_efficiency_low"),
            ("focus_optimal_seconds", "focus_min_seconds"),
        ]
        for high_name, low_name in pairs:
            high_val = getattr(self, high_name)
            low_val = getattr(self, low_name)
            if high_val <= low_val:
                raise ValueError(
                    f"{high_name} ({high_val}) must be greater than {low_name} ({low_val})"
                )
        return self


class NLPConfig(BaseModel):
    """NLP configuration for a language"""

    stop_words_path: Path
    filler_words_path: Path
    connector_words_path: Path
    topic_keywords_path: Path


class Settings(BaseSettings):
    """Global configuration"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Project paths
    base_dir: Path = Path(__file__).parent.parent
    config_dir: Path = Path(__file__).parent.parent / "config"
    data_dir: Path = Path(__file__).parent.parent / "data"
    output_dir: Path = Path(__file__).parent.parent / "output"

    # Sub-configurations
    nlp: dict[str, NLPConfig] = {}
    thresholds: ThresholdConfig = ThresholdConfig()

    # Typeless database path (auto-detected if empty)
    typeless_db_path: str = ""

    # AI configuration
    ai_primary_provider: str = "zhipu"
    ai_primary_model: str = "glm-4-flash"
    ai_api_key: str = ""
    ai_fallback_provider: str = "deepseek"
    ai_fallback_model: str = "deepseek-v3"
    ai_fallback_api_key: str = ""
    ai_max_cost_per_run: float = 10.0
    ai_concurrency: int = 20

    # Report configuration
    report_lang: str = "en"
    auto_open_report: bool = True

    # AI cache behaviour (must be >= 1 to avoid ZeroDivisionError in modulo check)
    ai_cache_save_frequency: int = Field(default=20, ge=1)

    # ── Computed paths ────────────────────────────────────────────────────────

    @property
    def cache_path(self) -> Path:
        """Path to AI analysis disk cache."""
        return self.data_dir / "ai_cache.json"

    @property
    def cost_log_path(self) -> Path:
        """Path to API cost log."""
        return self.data_dir / "cost_log.json"

    @property
    def temp_export_path(self) -> Path:
        """Temporary JSON export from Typeless database."""
        return self.data_dir / "raw" / "temp_export.json"

    @property
    def default_report_path(self) -> Path:
        """Default output path for generated HTML report."""
        return self.output_dir / "personal" / "Typeless_Report.html"

    def get_db_path(self) -> Path:
        """Return Typeless database path, with custom override support."""
        if self.typeless_db_path:
            return Path(self.typeless_db_path)

        system = platform.system()
        if system == "Darwin":
            return Path.home() / "Library/Application Support/Typeless/typeless.db"
        if system == "Windows":
            import os

            appdata = os.environ.get("APPDATA", "")
            if appdata:
                p = Path(appdata) / "Typeless/Typeless.db"
                if p.exists():
                    return p
            localappdata = os.environ.get("LOCALAPPDATA", "")
            if localappdata:
                return Path(localappdata) / "Typeless/Typeless.db"
        return Path.home() / ".local/share/Typeless/typeless.db"

    def load_nlp_configs(self):
        """Load NLP configs from config directory"""
        for lang in ["zh", "en"]:
            lang_dir = self.config_dir / lang
            self.nlp[lang] = NLPConfig(
                stop_words_path=lang_dir / "stopwords.txt",
                filler_words_path=lang_dir / "filler_words.txt",
                connector_words_path=lang_dir / "connector_words.txt",
                topic_keywords_path=lang_dir / "topic_keywords.txt",
            )


# Global singleton
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get global settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.load_nlp_configs()
    return _settings


def reset_settings() -> None:
    """Reset global settings singleton.

    This function is primarily intended for testing purposes, allowing
    tests to reset the global state between test runs.
    """
    global _settings
    _settings = None
