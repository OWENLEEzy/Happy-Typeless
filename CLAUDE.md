# CLAUDE.md - Happy-Typeless

> **Project**: Happy-Typeless | Typeless 语音数据分析可视化
> **Description**: 分析 Typeless 导出的语音数据，生成 Brutalist 风格仪表盘

---

## TOP 10 必读规则

| #   | 规则                       | 说明                                                                                     |
| --- | -------------------------- | ---------------------------------------------------------------------------------------- |
| 1   | **质量门禁**               | 见「完成检查清单」章节                                                                   |
| 2   | **先读后写**               | 修改任何文件前必须先用 Read 工具读取，理解现有代码                                       |
| 3   | **文档同步**               | **修改代码前必须读 `docs/CODEX.md`，修改后必须更新文档中的 Git Hash**                   |
| 4   | **类型优先**               | Python 使用类型注解，函数必须有参数和返回值类型                                          |
| 5   | **搜索优先**               | 写代码前用 `Grep` 搜索已有实现，避免重复                                                 |
| 6   | **配置分离**               | 硬编码配置（如颜色、阈值）必须在 `Config` 类或 `config/` 目录管理                         |
| 7   | **错误处理**               | 数据处理必须有异常捕获，提供清晰的错误信息                                               |
| 8   **测试覆盖**               | 新核心逻辑必须有测试，运行 `pytest` 验证                                                |
| 9   | **数据安全**               | 处理用户数据时注意隐私，不要在日志中输出敏感内容                                         |
| 10  | **禁止 push**              | Claude 可以 commit，但 **禁止 push** 到远程仓库                                          |

---

## 完成检查清单（最重要！）

> 🚨 **没有完成检查就说"完成了" = 严重违规**

### 质量门禁（按顺序执行）

```bash
# Python 项目检查
ruff check .          # 代码规范检查
ruff format .         # 代码格式化
pytest                # 运行测试
python -m py_compile src/main/*.py  # 语法检查
```

### 检查清单

| 检查项         | 命令                           | 说明            |
| -------------- | ------------------------------ | --------------- |
| **Ruff**       | `ruff check .`                 | 代码规范检查    |
| **Format**     | `ruff format .`                | 代码格式化      |
| **Test**       | `pytest`                       | 单元测试        |
| **Syntax**     | `python -m py_compile *.py`    | Python 语法检查 |

### 代码审查项

| 类别          | 检查项                             |
| ------------- | ---------------------------------- |
| **空值/边界** | 空列表/空字符串不报错、索引越界保护 |
| **错误处理**  | 文件操作、数据库操作有 `try/except` |
| **清理**      | 删除调试用的 `print()` 语句        |

### 文档更新检查（🚨 必须执行）

```bash
# 修改代码后，检查并更新文档
cat docs/CODEX.md  # 确认文档是否需要更新

# 更新 Git Hash（当代码有变更时）
git log -1 --format="%H"  # 获取当前 commit hash
# 然后手动更新 CODEX.md 中的 Git Hash 追踪表格
```

| 文档变更场景 | 必须更新                 |
| ------------ | ------------------------ |
| 新增分析方法 | 更新 `docs/CODEX.md` |
| 修改返回结构 | 更新 `docs/CODEX.md` |
| 新增配置项   | 更新 `docs/CODEX.md` |
| 新增渲染方法 | 更新 `docs/CODEX.md` |
| 代码有 commit | 更新 `docs/CODEX.md` 中的 Git Hash |

### 检查报告格式（完成后必须输出）

```
📝 改动报告：
📁 文件：xxx.py
✏️ 改了什么：...
🤔 为什么要改：...
✨ 改完之后：...
📚 文档更新：docs/CODEX.md 已同步 (Git Hash: xxx)

✅ 功能完成检查报告
📋 Ruff Check: ✅ 通过
📋 Ruff Format: ✅ 通过
📋 Pytest:     ✅ 通过

📦 已提交："commit message"
```

---

## 红线禁区（绝对不能违反）

### 代码安全

| 禁止事项                              | 后果                                   |
| ------------------------------------- | -------------------------------------- |
| 🚫 把数据库路径写进代码提交到仓库      | 泄露本地文件结构                       |
| 🚫 在日志中打印完整的语音内容          | 暴露用户隐私                           |
| 🚫 信任未验证的 JSON 数据不做校验      | 程序崩溃、数据错误                     |

### 代码质量

| 禁止事项                              | 后果                         |
| ------------------------------------- | ---------------------------- |
| 🚫 硬编码颜色值（如 `#FFDE00`）        | 设计不一致，难以维护主题切换 |
| 🚫 在代码中直接定义配置常量            | 违反单一数据源原则           |
| 🚫 不使用配置文件                      | 无法保证配置一致性           |
| 🚫 代码注释（`#`）或 docstring 使用中文 | 所有代码注释必须用英文，中文仅限 Claude 回复 |

**Code language rule**: All code must be written in English — variable names, function names, class names, `#` comments, and docstrings. Chinese appears only in user-facing output data, never in source code.

```python
# ✅ Correct
def calculate_score(items: list) -> float:
    """Calculate overall score, returns float between 0-100."""
    # Filter out null values
    valid = [x for x in items if x is not None]
    return sum(valid) / len(valid)

# ❌ Wrong
def calculate_score(items: list) -> float:
    """计算综合评分，返回 0-100 之间的浮点数。"""
    # 过滤空值
    valid = [x for x in items if x is not None]
    return sum(valid) / len(valid)
```

**配置使用规范**：

```python
# ✅ 正确
from src.main.typeless_analyzer import Config

STOP_WORDS = Config.STOP_WORDS
BG_COLOR = Config.BG_COLOR

# ❌ 错误
STOP_WORDS = ["的", "了", "是"]
BG_COLOR = "#F4EFEA"
```

### 代码提交

| 禁止事项                     | 后果                                              |
| ---------------------------- | ------------------------------------------------- |
| 🚫 未经测试就说"完成了"      | Bug 上线后才发现                                  |
| 🚫 git commit 暴露 AI 身份   | commit message 不能有 Claude/AI/LLM/Co-Authored-By |
| 🚫 执行 git push             | 推送必须由用户自己操作                            |
| 🚫 使用中文 commit message   | 所有 git commit 必须使用英文                       |

**Commit 规范**：
- 使用英文编写 commit message
- 格式：`<type>: <description>`
- Type: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`
- 示例：`feat: add emotion analysis module`

### 文档同步

| 禁止事项                              | 后果                       |
| ------------------------------------- | -------------------------- |
| 🚫 修改代码后不更新 CODEX.md  | 文档与代码不一致，误导开发 |
| 🚫 新增功能不更新文档                  | 功能无法被发现和使用       |

### 文档国际化原则

| 规则                              | 说明                                                                 |
| --------------------------------- | -------------------------------------------------------------------- |
| 🚫 `docs/CODEX.md` 必须纯英文       | CODEX.md 是技术 API 文档，所有内容必须使用英文（包括注释、示例代码）   |
| 🚫 `docs/CODEX.md` 不包含版本信息    | 不在文档中添加版本号或日期，避免维护开销；Git Hash 追踪足够             |
| 🚫 避免中英混杂                     | 文档中不要出现中英文混杂的情况，保持语言一致性                         |
| ✅ 中文文档放在 `docs/zh/` 目录     | 中文版文档应放在 `docs/zh/` 子目录，与英文版分离                       |
| ✅ 主 README.md 保持英文            | 主 README 使用英文，在顶部添加语言切换链接                             |
| ✅ 删除重复内容                     | 文档中不应有重复的章节，维护单一数据源                                 |

**文档语言规范**：
```
docs/
├── CODEX.md          # 纯英文 API 文档（已在 .gitignore，本地使用）
├── zh/               # 中文文档目录
│   └── README.md     # 中文版 README
└── CODEX.md 已经在 .gitignore 中，不会被提交
```

**检查命令**：
```bash
# 检查 CODEX.md 中是否有中文字符
grep -n "[一-龥]" docs/CODEX.md

# 检查是否有版本信息
grep -i "version\|updated" docs/CODEX.md | head -5
```

---

## 行为规范

| 规则                       | 说明                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------- |
| **永远用简体中文**         | 所有**回复**用中文；代码（注释、docstring）必须用英文                                   |
| **讨论时不写代码**         | 讨论阶段只分析逻辑、效果、代码行为，不实际修改代码；必须等用户确认方案后再动手           |
| **改前必读文档**           | 修改代码前必须读取 `docs/CODEX.md`，了解现有架构                              |
| **改后必更文档**           | 修改代码后必须同步更新 `docs/CODEX.md`                                        |
| **新功能要有测试**         | 核心逻辑必须有测试                                                                     |
| **新依赖要确认**           | 添加 Python 包前先问用户                                                               |
| **清理调试代码**           | 完成后删除 print() 语句                                                                |
| **一次只改一个功能**       | 不要顺手改其他东西                                                                     |

---

## 🎯 项目目标

将 Typeless 导出的语音转文字数据进行深度挖掘，生成精美的 Brutalist（新粗野主义）风格仪表盘 HTML 报告。

---

## 🛠️ 技术架构

```
Typeless SQLite 数据库
         ↓
    export_from_database (内建于 CLI)
         ↓
    JSON 数据文件
         ↓
    Repository Layer (数据访问)
    ├── JSONTranscriptionRepository
    └── MockTranscriptionRepository
         ↓
    Service Layer (业务逻辑)
    ├── OverviewService
    ├── UsageHabitsService
    ├── TimeTrendsService
    ├── ContentAnalysisService
    ├── EfficiencyService
    ├── AppUsageService
    └── AIInsightsService
         ↓
    AI Layer (深度分析)
    ├── AIAnalyzer (批处理门面)
    ├── AIClient (instructor + asyncio + tenacity)
    ├── AICache (磁盘缓存 data/ai_cache.json)
    └── 支持: Zhipu / DeepSeek / OpenAI / Anthropic / Moonshot / Alibaba
         ↓
    HTML 报告生成 (BrutalistHTMLGenerator)
    ├── Tailwind CSS (Bento Box 布局)
    ├── ECharts (图表可视化)
    └── 单文件离线 HTML
```

---

## 📁 项目结构

```
Happy-Typeless/
├── src/
│   ├── ai/                          # AI 分析层
│   │   ├── base.py                  # ProviderType, ModelConfig, PRICING_TABLE
│   │   ├── cache.py                 # AICache (磁盘缓存)
│   │   ├── client.py                # AIClient (instructor + asyncio + tenacity)
│   │   ├── analyzer.py              # AIAnalyzer (批处理门面)
│   │   ├── prompts.py               # ANALYSIS_PROMPT, build_prompt()
│   │   └── fixtures.py              # Mock AI 数据 (-m 模式)
│   ├── models/                      # Pydantic v2 数据模型
│   │   ├── transcription.py         # Transcription, TranscriptionList
│   │   ├── analysis.py              # Statistical analysis result models
│   │   ├── ai_analysis.py           # AITranscriptionAnalysis (20+ 字段)
│   │   └── errors.py                # Error models
│   ├── repositories/                # 数据访问层 (Repository pattern)
│   │   ├── base.py                  # TranscriptionRepository (ABC)
│   │   ├── json_repository.py       # JSONTranscriptionRepository
│   │   └── mock_repository.py       # MockTranscriptionRepository
│   ├── services/                    # 业务逻辑层
│   │   ├── overview.py              # OverviewService
│   │   ├── usage_habits.py          # UsageHabitsService
│   │   ├── time_trends.py           # TimeTrendsService
│   │   ├── content_analysis.py      # ContentAnalysisService
│   │   ├── efficiency.py            # EfficiencyService
│   │   ├── app_usage.py             # AppUsageService
│   │   └── ai_insights.py           # AIInsightsService
│   ├── nlp/                         # NLP 处理 (分词，Strategy pattern)
│   │   ├── factory.py               # NLPProcessorFactory
│   │   └── strategies/
│   │       ├── analysis.py          # AnalysisStrategy (词频 + 问句统计)
│   │       ├── segment.py           # SegmentStrategy (ABC)
│   │       ├── segment_zh.py        # ChineseSegmentStrategy (jieba)
│   │       └── segment_en.py        # EnglishSegmentStrategy (spaCy 可选)
│   ├── factories/                   # Factory pattern
│   │   └── repository_factory.py    # RepositoryFactory
│   ├── config.py                    # Global settings (pydantic-settings)
│   ├── cli.py                       # CLI entry point (Typer + Rich)
│   └── main/                        # Report generation
│       ├── generator.py             # BrutalistHTMLGenerator
│       └── translations.py          # I18n translations
├── scripts/
│   └── export_from_db.py            # Database export script (deprecated - integrated)
├── config/                          # Configuration files
│   ├── emotion_words.txt            # Emotion word library (5 categories)
│   ├── zh/                          # Chinese config
│   │   ├── stopwords.txt
│   │   ├── filler_words.txt
│   │   └── question_patterns.txt
│   └── en/                          # English config
│       ├── stopwords.txt
│       ├── filler_words.txt
│       └── question_patterns.txt
├── data/
│   ├── raw/                         # Typeless exported raw data (gitignored)
│   └── examples/                    # Example data files
│       └── typeless_export_example.json
├── output/                          # Generated HTML reports
│   └── examples/                    # Example HTML reports
│       └── Typeless_Report_Example.html
├── docs/                            # 📚 Project documentation
│   └── CODEX.md                     # API documentation (修改代码前必读)
├── tests/                           # Test files
├── CLAUDE.md                        # Claude Code working guide
├── README.md                        # Project README
└── pyproject.toml
```

---

## 🎨 设计风格 - Brutalist（新粗野主义）

### 配色方案（统一在 Config 类管理）

| 用途         | 变量名        | 值          |
| ------------ | ------------- | ----------- |
| 背景         | BG_COLOR      | `#F4EFEA`   |
| 卡片         | CARD_BG       | `#FFFFFF`   |
| 主文字       | TEXT_PRIMARY  | `#2D2D2D`   |
| 次要文字     | TEXT_SECONDARY| `#6B6B6B`   |
| 边框         | BORDER_COLOR  | `#2D2D2D`   |
| 强调黄       | ACCENT_YELLOW | `#FFDE00`   |
| 强调蓝       | ACCENT_BLUE   | `#6FC2FF`   |
| 成功绿       | SUCCESS_GREEN | `#00D26A`   |
| 错误红       | ERROR_RED     | `#FF4D4D`   |

### 组件特点
- 零圆角 (`border-radius: 0`)
- 2px 硬边框
- 悬停效果: `transform: translate(-2px, -2px)` + `box-shadow: 4px 4px 0 var(--accent-primary)`
- 等宽字体 (JetBrains Mono) 用于数字和标签
- Inter 字体用于正文

### 深色模式
- 背景: `#121212`
- 卡片: `#1E1E1E`
- 主文字: `#F4EFEA`

---

## 🚀 使用方式

### 一键从数据库分析
```bash
# 安装依赖
uv sync

# 一键：从数据库导出 + 分析 + 生成报告
uv run typeless analyze
```

### 从已有 JSON 文件分析
```bash
uv run typeless analyze -i data/raw/typeless_export.json
```

### 使用模拟数据测试
```bash
uv run typeless analyze -m
```

### 缓存与费用管理
```bash
uv run typeless cache status   # 查看缓存
uv run typeless cache clear    # 清理缓存
uv run typeless cost           # 查看 API 费用记录
```

---

## 🔧 核心功能模块

> 📌 **详细 API 文档请查看 `docs/CODEX.md`**

### 数据层 (Repository)
```python
class TranscriptionRepository(ABC):
    def get_all(self) -> TranscriptionList:
        """获取所有语音记录"""

class JSONTranscriptionRepository(TranscriptionRepository):
    """从 JSON 文件读取数据"""

class MockTranscriptionRepository(TranscriptionRepository):
    """生成模拟数据用于测试"""
```

### 服务层 (Service)
```python
class OverviewService:
    def get_stats(self) -> OverviewStats:
        """核心大盘指标"""

class UsageHabitsService:
    def get_habits(self) -> UsageHabits:
        """使用习惯分析"""

class TimeTrendsService:
    def get_trends(self) -> TimeTrends:
        """时间规律探索"""

class ContentAnalysisService:
    def analyze_content(self) -> ContentAnalysis:
        """深度内容解析（词云、句长分布、话题）"""

class EfficiencyService:
    def get_metrics(self) -> EfficiencyMetrics:
        """效率评分"""

class AppUsageService:
    def get_app_usage(self) -> AppUsage:
        """App 使用统计"""

class AIInsightsService:
    def get_insights(self) -> dict:
        """聚合 AI 分析结果（人格、情绪、话题等）"""
```

### HTML 生成器 (BrutalistHTMLGenerator)
```python
class BrutalistHTMLGenerator:
    def generate(self, analysis_data: Dict, output_path: str) -> None:
        """生成 Brutalist 风格 HTML 报告"""
```

---

## 📊 核心分析维度

### 1. 核心大盘指标 (Overview)
- 总览数据：总语音条数、总输出字数、总语音时长
- 平均数据：日均使用次数、平均每条字数、平均每条时长
- 成就徽章：根据总字数授予不同等级

### 2. 个人使用习惯 (Usage Habits)
- 连续性分析：最长连续使用天数、总活跃天数、断档天数
- 极值对比：最勤奋的一周 vs 最慵懒的一周，差距倍数

### 3. 语言风格与情绪 (Language & Sentiment)
- 口头禅检测：每日最常说的词汇及日均出现频次
- 句式倾向：问句 vs 陈述句占比分析
- 情绪大盘：正常/含脏话/负面情绪分类及占比
- 脏话日历：情绪崩溃日记录与上下文原话

### 4. 时间规律探索 (Time Trends)
- 短期趋势：最近30天使用趋势面积图
- 生物钟：24小时使用分布柱状图
- 劳模榜单：使用量 Top 5 日期

### 5. 深度内容解析 (Content Deep Dive)
- 主题分类：日常/其他、AI技术、设计/创作等领域占比
- 高频词云：Top 50 词汇标签云
- 长短句分布：短句(<20字)、中等(20-100字)、长句(>100字)
- 单条之最：耗时最长语音的完整文本

### 6. 语言风格画像 (Personality Profile) ⭐ Phase 1
- 风格标签：简洁派/絮叨派、提问者/下命令者、情绪稳定/情绪化、工作狂/生活家
- 指标：平均句长、问句占比、负面情绪占比、工作日/周末比

### 7. 效率评分 (Efficiency Metrics) ⭐ Phase 1
- 作息健康评分：深夜使用占比
- 工作效率评分：工作时段使用占比
- 专注度评分：平均时长
- 碎片化指数：短句占比

---

## 📝 数据格式

### SQLite 数据库
Typeless 数据库位置:
- macOS: `~/Library/Application Support/Typeless/typeless.db`
- 表名: `history`
- 关键字段: `id`, `created_at`, `refined_text`, `duration`, `focused_app_name`

### JSON 导出格式
```json
[
  {
    "id": "xxx",
    "timestamp": 1737550800,
    "content": "语音内容文字",
    "duration": 15.5,
    "app_name": "应用名称",
    "window_title": "窗口标题"
  }
]
```

---

## 🔑 关键配置

### Settings 类配置
配置位于 `src/config.py` 中的 `Settings` 类。

| 类别 | 配置项 | 说明 |
|------|--------|------|
| 阈值 | `ThresholdConfig` | 风格判断阈值、句长阈值、碎片化阈值 |
| 主题词 | `ai_keywords` / `design_keywords` | 主题关键词 |
| 连接词 | `connector_words` | 连接词集合 |
| 填充词 | `filler_words` | 填充词集合 |
| 时间段 | `late_night_hours` / `work_hours` | 时间分段 |
| 徽章 | `badge_levels` | 成就徽章等级配置 |
| 情绪 | `EmotionConfig` | 情绪词库、强度词 |
| 显示 | `max_swear_display_items` 等 | 显示数量控制 |

### 配置文件目录结构
```
config/
├── emotion_words.txt    # 情绪词库 (5 类)
├── zh/                  # 中文配置
│   ├── stopwords.txt
│   ├── filler_words.txt
│   └── question_patterns.txt
└── en/                  # 英文配置
    ├── stopwords.txt
    ├── filler_words.txt
    └── question_patterns.txt
```

---

## 📊 报告功能清单

### 已实现功能 ✅
- [x] 核心大盘指标 (6项卡片 + 成就徽章)
- [x] 使用习惯分析 (连续性 + 极值对比)
- [x] 高频词词云 (Top 50)
- [x] 30天趋势面积图 (ECharts)
- [x] 24小时分布柱状图 (ECharts)
- [x] 使用高峰 Top 5
- [x] 内容主题分类
- [x] 长短句环形图 (ECharts)
- [x] 最长语音展示
- [x] 深色模式切换
- [x] 效率评分卡片
- [x] App 使用统计
- [x] AI 深度洞察：大五人格雷达图
- [x] AI 深度洞察：情绪分布与触发原因
- [x] AI 深度洞察：话题分布
- [x] AI 深度洞察：灵感/幽默检测
- [x] AI 深度洞察：心理健康指标

### Phase 2 待实现 🚧
- [ ] A3. 经典语录 - 最情绪化一条、字数最多那天精华
- [ ] C2. 情绪强度分级 - 强度修饰词 x1.5/x0.7
- [ ] C3. 情绪趋势图 - 30天负面情绪占比折线图
- [ ] D1. 高质量语录 - 有价值内容筛选
- [ ] D2. 时间胶囊 - 每周精选

---

## ⚠️ 开发注意事项

1. **jieba 首次运行**: 会下载词典缓存，约需 1 秒
2. **时间戳格式**: 数据库导出时处理 ISO 8601 字符串转 UNIX 时间戳
3. **大文件处理**: 数据量大时 jieba 分词可能较慢
4. **图表渲染**: ECharts 需要 JavaScript 支持，确保浏览器环境
5. **文档同步**: 修改任何分析方法或返回结构后，必须更新 `docs/CODEX.md`

---

## Quick Reference

```bash
# 质量门禁
ruff check . && ruff format . && uv run pytest

# 开发/运行
uv run typeless analyze -m --no-open

# 搜索代码
grep -r "关键词" src/
```

| 操作         | Claude 权限 |
| ------------ | ----------- |
| `git commit` | 允许        |
| `git push`   | **禁止**    |
| `python *`   | 允许        |

---

## 文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| CODEX | `docs/CODEX.md` | 完整 API 文档（含 Git Hash 追踪），修改代码前必读 |

---

🤖 Generated with Claude Code for Typeless Data Analysis
