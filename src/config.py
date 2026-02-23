import platform
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ThresholdConfig(BaseModel):
    """Various threshold values"""

    concise: int = 30
    verbose: int = 80
    question_high: int = 30
    question_low: int = 10
    negative_stable: int = 5
    negative_emotional: int = 20
    workaholic: float = 2.0
    lifestyle: float = 0.5
    fragmentation_high: int = 70
    fragmentation_low: int = 40
    short_sentence: int = 20
    long_sentence: int = 100

    # Additional keywords for topic classification
    ai_keywords: list[str] = [
        "AI",
        "人工智能",
        "机器学习",
        "深度学习",
        "模型",
        "算法",
        "Python",
        "代码",
        "编程",
        "API",
        "前端",
        "后端",
        "数据库",
        "训练",
        "推理",
        "参数",
        "优化",
        "部署",
        "神经网络",
    ]
    design_keywords: list[str] = [
        "设计",
        "UI",
        "UX",
        "界面",
        "交互",
        "视觉",
        "颜色",
        "字体",
        "布局",
        "原型",
        "Figma",
        "Sketch",
        "用户体验",
        "产品",
        "功能",
        "需求",
    ]

    # Time periods
    late_night_hours: list[int] = list(range(23, 24)) + list(range(0, 7))
    work_hours: list[int] = list(range(9, 19))

    # Connector words
    connector_words: set[str] = {
        "那个",
        "这个",
        "这些",
        "那些",
        "一下",
        "的话",
        "然后",
        "就是",
        "就是说",
        "其实",
        "怎么说呢",
    }

    # Filler words
    filler_words: set[str] = {"嗯", "唔", "呃", "啊", "呀", "哎", "咳", "嘿", "噢", "嚯"}

    # Badge levels
    badge_levels: list[tuple[int, str, str, str]] = [
        (10000, "键盘终结者", "⌨️", "#3B82F6"),
        (50000, "话痨本痨", "🗣️", "#CD7F32"),
        (100000, "人形打字机", "⌨️", "#C0C0C0"),
        (500000, "当代苏格拉底", "🏛️", "#FFD700"),
    ]


class NLPConfig(BaseModel):
    """NLP configuration for a language"""

    stop_words_path: Path
    filler_words_path: Path
    question_patterns_path: Path


class EmotionConfig(BaseModel):
    """Emotion analysis configuration"""

    categories: dict[str, list[str]] = {}
    swear_words: list[str] = []
    intensity_heavy: list[str] = []
    intensity_light: list[str] = []


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
    emotion: EmotionConfig = EmotionConfig()
    thresholds: ThresholdConfig = ThresholdConfig()

    # Typeless database path (auto-detected if empty)
    typeless_db_path: str = ""

    # AI configuration
    ai_primary_provider: str = "zhipu"
    ai_primary_model: str = "glm-4-flash"
    ai_api_key: str = ""
    ai_fallback_provider: str = "deepseek"
    ai_fallback_api_key: str = ""
    ai_max_cost_per_run: float = 10.0
    ai_concurrency: int = 20

    # Report configuration
    report_lang: str = "zh"
    auto_open_report: bool = True

    # Display settings
    max_swear_display_items: int = 8
    phrase_tags_count: int = 10
    word_cloud_count: int = 20
    top_dates_count: int = 5

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
                question_patterns_path=lang_dir / "question_patterns.txt",
            )

    def load_emotion_config(self):
        """Load emotion config from files"""
        emotion_file = self.config_dir / "emotion_words.txt"
        if emotion_file.exists():
            self._parse_emotion_file(emotion_file)

    def _parse_emotion_file(self, filepath: Path):
        """Parse emotion words configuration file"""
        import re

        current_category = None
        categories = {}
        swear_words = []

        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Category header like [anger]
                if match := re.match(r"\[(\w+)\]", line):
                    current_category = match.group(1)
                    categories[current_category] = []
                elif current_category:
                    # Handle space-separated words on same line
                    words = line.split()
                    categories[current_category].extend(words)
                    if current_category in ["anger", "anxiety", "sadness", "fatigue", "stress"]:
                        swear_words.extend(words)

        # Default swear words from old Config
        if not swear_words:
            swear_words = [
                "卧槽",
                "妈的",
                "傻逼",
                "靠",
                "离谱",
                "烦",
                "崩溃",
                "他妈",
                "妈蛋",
                "滚",
                "扯淡",
                "放屁",
                "废物",
                "垃圾",
                "累死了",
                "烦死了",
                "气死了",
                "受不了",
                "太离谱了",
            ]

        self.emotion = EmotionConfig(
            categories=categories,
            swear_words=swear_words,
            intensity_heavy=["非常", "特别", "超级", "太", "极其"],
            intensity_light=["有点", "稍微", "还算"],
        )


# Global singleton
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get global settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.load_nlp_configs()
        _settings.load_emotion_config()
    return _settings


def reset_settings() -> None:
    """Reset global settings singleton.

    This function is primarily intended for testing purposes, allowing
    tests to reset the global state between test runs.
    """
    global _settings
    _settings = None
