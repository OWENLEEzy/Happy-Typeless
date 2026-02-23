# Happy-Typeless CODEX

> **Project**: Typeless Voice Data Analytics

---

## Table of Contents

1. [File Structure](#file-structure)
2. [Models Layer](#models-layer)
3. [Repository Layer](#repository-layer)
4. [Service Layer](#service-layer)
5. [NLP Layer](#nlp-layer)
6. [AI Layer](#ai-layer)
7. [Factory Layer](#factory-layer)
8. [Configuration](#configuration)
9. [CLI](#cli)
10. [Report Generation](#report-generation)
11. [Usage Examples](#usage-examples)

---

## File Structure

```
src/
├── ai/                      # AI analysis layer
│   ├── __init__.py
│   ├── base.py              # ProviderType, ModelConfig, PRICING_TABLE
│   ├── cache.py             # AICache (disk-backed, model-mismatch warning)
│   ├── client.py            # AIClient (instructor + asyncio + tenacity)
│   ├── analyzer.py          # AIAnalyzer (batch processing facade)
│   ├── prompts.py           # ANALYSIS_PROMPT, build_prompt()
│   └── fixtures.py          # Mock AI data for -m mode
├── models/                  # Pydantic v2 data models
│   ├── transcription.py     # Transcription, TranscriptionList
│   ├── analysis.py          # Statistical analysis result models
│   ├── ai_analysis.py       # AITranscriptionAnalysis and 20+ sub-models
│   └── errors.py            # Error models (optional)
├── repositories/            # Data access layer
│   ├── base.py              # TranscriptionRepository (ABC)
│   ├── json_repository.py   # JSONTranscriptionRepository
│   └── mock_repository.py   # MockTranscriptionRepository
├── services/                # Business logic layer
│   ├── overview.py          # OverviewService
│   ├── usage_habits.py      # UsageHabitsService
│   ├── time_trends.py       # TimeTrendsService
│   ├── content_analysis.py  # ContentAnalysisService
│   ├── efficiency.py        # EfficiencyService
│   ├── app_usage.py         # AppUsageService
│   └── ai_insights.py       # AIInsightsService
├── nlp/                     # NLP processing (segmentation only)
│   ├── factory.py           # NLPProcessorFactory
│   └── strategies/
│       ├── analysis.py      # AnalysisStrategy (batch word frequency + questions)
│       ├── segment.py       # SegmentStrategy (ABC)
│       ├── segment_zh.py    # ChineseSegmentStrategy (jieba)
│       └── segment_en.py    # EnglishSegmentStrategy (spaCy optional)
├── factories/               # Factory pattern
│   └── repository_factory.py # RepositoryFactory
├── config.py                # Global settings (pydantic-settings)
├── cli.py                   # CLI entry point (Typer + Rich)
├── translations.py          # I18n helper (shared by services and main layers)
└── main/                    # Report generation
    └── generator.py         # BrutalistHTMLGenerator
```

---

## Models Layer

### Transcription Models

**File**: `src/models/transcription.py`

```python
class Transcription(BaseModel):
    """Single voice transcription record"""
    id: str
    timestamp: int
    content: str
    duration: float | None = None
    app_name: str | None = None
    window_title: str | None = None

    @property
    def datetime(self) -> datetime:
        """Convert UNIX timestamp to datetime (UTC)"""

    @property
    def date(self) -> str:
        """Get date in YYYY-MM-DD format"""

class TranscriptionList(BaseModel):
    """List of transcription records"""
    items: list[Transcription] = []
```

### Statistical Analysis Models

**File**: `src/models/analysis.py`

| Model | Purpose |
|-------|---------|
| `OverviewStats` | Core overview metrics |
| `UsageHabits` | Usage habits analysis |
| `EfficiencyMetrics` | Efficiency scores and fragmentation |
| `AppUsage` | App usage statistics |
| `TimeTrends` | Time trends analysis |
| `ContentAnalysis` | Content deep dive analysis |
| `WordFrequency` | Word frequency item |
| `DateEntry` | Top date entry |

### AI Analysis Models

**File**: `src/models/ai_analysis.py`

Per-transcription AI output model with 20+ fields. See `AITranscriptionAnalysis` for the full schema.

---

## Repository Layer

### Base Repository

**File**: `src/repositories/base.py`

```python
class TranscriptionRepository(ABC):
    """Transcription repository interface"""

    @abstractmethod
    def get_all(self) -> TranscriptionList:
        """Get all transcription records"""

    def get_by_date_range(self, start: str, end: str) -> TranscriptionList:
        """Get transcriptions within date range (default implementation)"""
```

### JSON Repository

**File**: `src/repositories/json_repository.py`

```python
class JSONTranscriptionRepository(TranscriptionRepository):
    """JSON file repository"""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._ensure_exists()

    def get_all(self) -> TranscriptionList:
        """Load all transcriptions from JSON file"""
```

### Mock Repository

**File**: `src/repositories/mock_repository.py`

```python
class MockTranscriptionRepository(TranscriptionRepository):
    """Mock repository for testing"""

    def __init__(self):
        self._data: TranscriptionList = TranscriptionList(items=[])

    def generate_mock(self, count: int = 500, days: int = 61):
        """Generate mock transcription data"""
```

---

## Service Layer

| Service | Method | Returns | Description |
|---------|--------|---------|-------------|
| `OverviewService` | `get_stats()` | `OverviewStats` | Core overview metrics |
| `UsageHabitsService` | `get_habits()` | `UsageHabits` | Usage habits analysis |
| `TimeTrendsService` | `get_trends()` | `TimeTrends` | Time trends analysis |
| `ContentAnalysisService` | `analyze_content()` | `ContentAnalysis` | Deep content analysis |
| `EfficiencyService` | `get_metrics()` | `EfficiencyMetrics` | Efficiency scoring |
| `AppUsageService` | `get_app_usage()` | `AppUsage` | App usage statistics |
| `AIInsightsService` | `get_insights()` | `dict` | Aggregated AI analysis results |

### Service Pattern

All statistical services follow this pattern:

```python
class ExampleService:
    """Service for X analysis"""

    def __init__(self, data: TranscriptionList, lang: str = "zh"):
        self.data = data
        self.lang = lang

    def get_result(self) -> ResultModel:
        """Calculate and return analysis result"""
```

---

## NLP Layer

NLP is used for segmentation and word frequency only. Emotion/sentiment analysis is handled by the AI layer.

### AnalysisStrategy (Batch Processing)

**File**: `src/nlp/strategies/analysis.py`

```python
class AnalysisStrategy:
    """Batch analysis strategy for NLP operations.

    Wraps SegmentStrategy to provide batch processing methods.
    """

    def __init__(self, segment_strategy: SegmentStrategy):
        self.segment = segment_strategy

    def get_word_frequency(self, data: TranscriptionList, limit: int = 30) -> list[WordFrequency]:
        """Get word frequency statistics"""

    def count_questions(self, data: TranscriptionList) -> int:
        """Count question sentences"""

    def get_question_ratio(self, data: TranscriptionList) -> tuple[int, float]:
        """Get question sentence ratio (count, percentage)"""
```

### Segment Strategy Interface

**File**: `src/nlp/strategies/segment.py`

```python
class SegmentStrategy(ABC):
    """Word segmentation strategy interface"""

    @abstractmethod
    def segment(self, text: str) -> list[str]:
        """Segment text into words, filtering stop words"""

    @abstractmethod
    def is_question(self, text: str) -> bool:
        """Check if text is a question"""

    @abstractmethod
    def is_stop_word(self, word: str) -> bool:
        """Check if word is a stop word"""

    @abstractmethod
    def is_filler_word(self, word: str) -> bool:
        """Check if word is a filler word"""
```

### Chinese Segment Strategy

**File**: `src/nlp/strategies/segment_zh.py`

```python
class ChineseSegmentStrategy(SegmentStrategy):
    """Chinese word segmentation strategy using jieba"""

    def __init__(self, stop_words: set[str], filler_words: set[str] | None = None):
        self.stop_words = stop_words
        self.filler_words = filler_words or set()

    def segment(self, text: str) -> list[str]:
        """Segment Chinese text and filter stop words"""
        words = jieba.cut(text)
        return [w for w in words if len(w) > 1 and w not in self.stop_words and not w.isdigit()]

    def is_question(self, text: str) -> bool:
        """Check if Chinese text is a question"""
        question_marks = ["？", "?"]
        return any(mark in text for mark in question_marks)
```

---

## AI Layer

AI analysis provides per-transcription deep insights, replacing NLP-based emotion/sentiment detection.

### Key Classes

| Class | File | Purpose |
|-------|------|---------|
| `AIAnalyzer` | `src/ai/analyzer.py` | Public facade: batch analyze + cost log |
| `AIClient` | `src/ai/client.py` | Async parallel calls, fallback, budget breaker |
| `AICache` | `src/ai/cache.py` | Disk-backed cache keyed by transcription ID |
| `build_instructor_client` | `src/ai/client.py` | Build instructor-wrapped async client |
| `build_prompt` | `src/ai/prompts.py` | Build analysis prompt from Transcription |

### Supported Providers

| Provider | Enum | Mode |
|----------|------|------|
| Zhipu (GLM) | `ProviderType.ZHIPU` | TOOLS |
| DeepSeek | `ProviderType.DEEPSEEK` | TOOLS |
| OpenAI | `ProviderType.OPENAI` | TOOLS |
| Anthropic | `ProviderType.ANTHROPIC` | from_anthropic |
| Moonshot | `ProviderType.MOONSHOT` | JSON |
| Alibaba | `ProviderType.ALIBABA` | JSON |

### Usage

```python
from src.ai.analyzer import AIAnalyzer
from src.ai.base import ModelConfig, ProviderType

config = ModelConfig(
    provider=ProviderType.ZHIPU,
    model_name="glm-4-flash",
    api_key="your_key",
)
analyzer = AIAnalyzer(primary=config)
results = analyzer.analyze(transcription_list)
# returns dict[str, AITranscriptionAnalysis]
```

### AITranscriptionAnalysis Fields

| Group | Fields |
|-------|--------|
| Core | `sentiment`, `intent`, `emotion`, `topics` |
| Style | `communication_style`, `personality`, `mental_health` |
| Content | `content_flags`, `profanity`, `complexity`, `entities` |
| Patterns | `speech_patterns`, `social_indicators`, `cognitive_distortions` |
| Extended | `language_mixing`, `creative_signal`, `humor`, `time_perception`, `emotion_trigger`, `commitment_strength` |

### Cache

- Path: `data/ai_cache.json` (gitignored)
- Keyed by `transcription.id`; model-mismatch prints warning, cached data reused
- Cost log: `data/cost_log.json` (gitignored)

---

## Factory Layer

### NLP Factory

**File**: `src/nlp/factory.py`

```python
class NLPProcessorFactory:
    """Factory for creating NLP processing strategies.

    Uses class-level caching for strategies, shared across all instances.
    """

    _strategies: dict[str, SegmentStrategy] = {}

    def __init__(self, config_dir: Path, config: Settings):
        self.config_dir = config_dir
        self.config = config

    def get_segment_strategy(self, lang: str) -> SegmentStrategy:
        """Get segment strategy for language (with class-level caching)"""

    def get_analysis_strategy(self, lang: str = "zh") -> AnalysisStrategy:
        """Get batch analysis strategy for language"""
        segment = self.get_segment_strategy(lang)
        return AnalysisStrategy(segment)
```

### Repository Factory

**File**: `src/factories/repository_factory.py`

```python
class RepositoryFactory:
    """Factory for creating repository instances"""

    def create_json_repository(self, filepath: Path) -> JSONTranscriptionRepository:
        """Create JSON repository"""

    def create_mock_repository(self) -> MockTranscriptionRepository:
        """Create mock repository"""
```

---

## Configuration

**File**: `src/config.py`

```python
class Settings(BaseSettings):
    """Global configuration using pydantic-settings"""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Project paths
    base_dir: Path = Path(__file__).parent.parent
    config_dir: Path = Path(__file__).parent.parent / "config"
    data_dir: Path = Path(__file__).parent.parent / "data"
    output_dir: Path = Path(__file__).parent.parent / "output"

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

def get_settings() -> Settings:
    """Get global settings singleton"""

def reset_settings() -> None:
    """Reset global settings singleton (for testing)"""
```

---

## CLI

**File**: `src/cli.py`

```python
app = typer.Typer(name="typeless")
cache_app = typer.Typer(help="Cache management")
app.add_typer(cache_app, name="cache")

@app.command()
def analyze(
    input: Path = typer.Option(None, "-i", "--input"),
    output: Path = typer.Option("output/personal/Typeless_Report.html", "-o", "--output"),
    lang: str = typer.Option(None, "-l", "--lang"),
    mock: bool = typer.Option(False, "-m", "--mock"),
    mock_count: int = typer.Option(500, "--mock-count"),
    force_refresh: bool = typer.Option(False, "--force-refresh"),
    no_open: bool = typer.Option(False, "--no-open"),
):
    """Analyze Typeless voice data and generate AI insights report"""

@cache_app.command("status")
def cache_status():
    """Show AI analysis cache status"""

@cache_app.command("clear")
def cache_clear(yes: bool = typer.Option(False, "--yes", "-y")):
    """Clear AI analysis cache"""

@app.command("cost")
def show_cost():
    """Show historical AI API cost records"""
```

---

## Report Generation

**File**: `src/main/generator.py`

```python
class BrutalistHTMLGenerator:
    """Brutalist style HTML report generator"""

    def __init__(self, lang: str = "zh"):
        self.i18n = I18n(lang)

    def generate(self, analysis_data: dict[str, Any], output_path: str) -> None:
        """Generate HTML report"""
```

**File**: `src/translations.py`

```python
class I18n:
    """Internationalization helper class for HTMLGenerator"""

    def __init__(self, lang: str = "en"):
        self.lang = lang if lang in TRANSLATIONS else "en"
        self._translations = TRANSLATIONS[self.lang]

    def t(self, key: str, *args, **kwargs) -> str:
        """Get translated text"""
```

---

## Usage Examples

### CLI Usage

```bash
# Auto-export from Typeless database + analyze
uv run typeless analyze

# From existing JSON file
uv run typeless analyze -i data/raw/typeless_export.json -o output/report.html

# With mock data (no API key needed)
uv run typeless analyze -m

# Force re-run AI analysis
uv run typeless analyze --force-refresh

# Cache management
uv run typeless cache status
uv run typeless cache clear

# Cost history
uv run typeless cost
```

### Python API Usage

```python
from src.factories.repository_factory import RepositoryFactory
from src.services.overview import OverviewService
from src.main.generator import BrutalistHTMLGenerator

# Load data
repository = RepositoryFactory().create_json_repository("data/raw/typeless_export.json")
data = repository.get_all()

# Analyze
overview = OverviewService(data).get_stats()

# Generate report
generator = BrutalistHTMLGenerator(lang="zh")
result = {"overview": overview.model_dump()}
generator.generate(result, "output/report.html")
```

---

## Git Hash Tracking

| Project | Value |
|---------|-------|
| **Branch** | `main` |
| **Commit Hash** | `ac6f026110ed4dc79b6693874a3c4f53318c783d` |
| **Short Hash** | `ac6f026` |
