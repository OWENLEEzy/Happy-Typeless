# Happy-Typeless | Typeless Voice Data Analyzer

English | [中文](docs/zh/README.md)

> Analyze your Typeless voice-to-text history and generate a beautiful AI-powered report — personality insights, mood trends, topic mapping, and more.

**[→ View Example Report (Chinese)](https://htmlpreview.github.io/?https://github.com/OWENLEEzy/Happy-Typeless/blob/main/output/examples/Typeless_Report_Example_zh.html)** · **[View Example Report (English)](https://htmlpreview.github.io/?https://github.com/OWENLEEzy/Happy-Typeless/blob/main/output/examples/Typeless_Report_Example_en.html)**

---

## What You'll Get

A single offline HTML report covering:

- **Overview** — total records, words, duration, and achievement badges
- **Usage Habits** — streaks, active days, busiest vs laziest weeks
- **Time Patterns** — 30-day trend chart, 24-hour bio-clock distribution
- **Content Deep Dive** — word cloud, topic breakdown, sentence length analysis
- **Efficiency Scores** — sleep health, work hours, focus score
- **App Usage** — which apps you voice-type in most
- **AI Deep Insights** ⭐ — Big Five personality radar, emotion analysis, mood triggers, creative moments, mental health indicators

---

## What You Need

| Requirement | Notes |
|-------------|-------|
| [Typeless](https://typeless.app) | The voice-to-text app (must have some recordings) |
| Python 3.12+ | [Download](https://www.python.org/downloads/) |
| uv | Python package manager — `pip install uv` or [see docs](https://docs.astral.sh/uv/getting-started/installation/) |
| AI API Key | Any one of: Zhipu · DeepSeek · OpenAI · Anthropic · Moonshot · Alibaba |

---

## Setup (5 minutes)

**1. Clone the repo**

```bash
git clone https://github.com/OWENLEEzy/Happy-Typeless.git
cd Happy-Typeless
```

**2. Install dependencies**

```bash
uv sync
```

**3. Configure your AI key**

```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in your API key:

```env
AI_API_KEY=your_api_key_here
AI_PRIMARY_PROVIDER=deepseek        # or: zhipu / openai / anthropic / moonshot / alibaba
AI_PRIMARY_MODEL=deepseek-chat      # model name for your chosen provider
```

**4. Run**

```bash
uv run typeless analyze
```

The report opens in your browser automatically when done.

---

## Commands

```bash
# Analyze (auto-exports from Typeless database)
uv run typeless analyze

# Generate in English
uv run typeless analyze --lang en

# Try it without Typeless or an API key (mock data)
uv run typeless analyze -m

# Re-run AI analysis from scratch (after changing model/provider)
uv run typeless analyze --force-refresh

# Cache and cost management
uv run typeless cache status
uv run typeless cache clear
uv run typeless cost
```

| Option | Description |
|--------|-------------|
| `-i, --input PATH` | Use an exported JSON file instead of the database |
| `-o, --output PATH` | Output path (default: `output/personal/Typeless_Report.html`) |
| `-l, --lang` | Report language: `zh` or `en` (default) |
| `-m, --mock` | Use mock data — no API key or Typeless needed |
| `--force-refresh` | Ignore cache and re-run all AI analysis |
| `--no-open` | Don't auto-open the browser |

---

## How Much Does It Cost?

AI analysis runs once per record, then results are cached — **subsequent runs are free**.

Estimated cost for the first run (approximate, based on ~900 tokens per record):

| Records | DeepSeek | Zhipu GLM-4-Flash | Anthropic Claude |
|---------|----------|-------------------|-----------------|
| 500 | ~¥0.1 | ~¥0.6 | ~¥2.5 |
| 1,000 | ~¥0.2 | ~¥1.2 | ~¥5 |
| 3,000 | ~¥0.5 | ~¥3.5 | ~¥15 |

> After the first run, you can re-generate the report as many times as you like at no cost.

---

## Frequently Asked Questions

**Where is the Typeless database?**
macOS: `~/Library/Application Support/Typeless/typeless.db` — the tool finds it automatically.

**Will my voice data be uploaded?**
Only the text content of each recording is sent to the AI API for analysis. Raw audio is never accessed.

**Can I use a custom database path?**
Yes — set `TYPELESS_DB_PATH=/your/path` in `.env`.

**The report won't open / I'm on Windows**
Run with `--no-open` and open the HTML file manually from `output/personal/`.
