# src/models/analysis.py

from pydantic import BaseModel


class BadgeInfo(BaseModel):
    """Achievement badge info"""

    icon: str
    name: str
    color: str
    threshold: int
    progress: float  # 0.0 to 1.0


class OverviewStats(BaseModel):
    """Core overview metrics"""

    total_records: int
    total_words: int
    total_duration: float  # in minutes
    active_days: int
    date_range_days: int
    daily_avg: float
    avg_words: float
    avg_duration: float  # in seconds
    start_date: str
    end_date: str
    badge: BadgeInfo | None = None


class UsageHabits(BaseModel):
    """Usage habits analysis"""

    consecutive_days: int
    active_days: int
    gap_days: int
    busiest_week: int
    laziest_week: int
    week_ratio: float


class EfficiencyScores(BaseModel):
    """Efficiency scores"""

    sleep_health: int
    work_efficiency: int
    focus: int
    overall: int


class FragmentationInfo(BaseModel):
    """Fragmentation index info"""

    level: str  # "high", "medium", "low"
    desc: str
    ratio: float
    short_count: int


class EfficiencyMetrics(BaseModel):
    """Efficiency metrics"""

    scores: EfficiencyScores
    fragmentation: FragmentationInfo
    late_night_ratio: float
    avg_duration: float  # in seconds (average per entry)


class AppUsageItem(BaseModel):
    """App usage item"""

    app_name: str
    count: int
    ratio: float
    avg_duration: float | None = None  # in seconds (average per entry)
    avg_words: float | None = None


class AppUsage(BaseModel):
    """App usage statistics"""

    apps: list[AppUsageItem] = []
    total: int
    has_data: bool
    unique_apps: int


class WordFrequency(BaseModel):
    """Word frequency item"""

    name: str
    value: int


class DateEntry(BaseModel):
    """Top date entry"""

    date: str
    count: int


class TimeTrends(BaseModel):
    """Time trends analysis result"""

    daily_trend: dict[str, list[str | int]]
    hour_distribution: list[int]
    top_dates: list[DateEntry]


class SentenceLengthDistribution(BaseModel):
    """Sentence length distribution"""

    short: int
    medium: int
    long: int
    short_ratio: float
    medium_ratio: float
    long_ratio: float


class LongestYap(BaseModel):
    """Longest voice recording"""

    content: str
    word_count: int
    date: str
    hour: int
    duration: float  # in seconds


class ContentAnalysis(BaseModel):
    """Content deep dive analysis result"""

    sentence_length_distribution: SentenceLengthDistribution
    longest_yap: LongestYap
    word_cloud: list[WordFrequency] = []
    topic_distribution: dict[str, int] = {}  # Topic name -> count
    word_categories: dict[str, int] = {}  # filler, connector, content word counts
    top_phrases: list[dict] = []  # Top recurring phrases
