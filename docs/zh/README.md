# Happy-Typeless | Typeless 语音数据分析器

[English](../../README.md) | 中文

> 把你在 Typeless 里积累的语音转文字记录，生成一份好看的 AI 分析报告——人格画像、情绪变化、话题分布，一次看透。

**[→ 点击查看示例报告](https://htmlpreview.github.io/?https://github.com/OWENLEEzy/Happy-Typeless/blob/main/output/examples/Typeless_Report_Example.html)**

---

## 能生成什么

一份可离线查看的单页 HTML 报告，包含：

- **核心大盘** — 总条数、总字数、总时长、成就徽章
- **使用习惯** — 连续打卡天数、最勤奋 vs 最懒一周
- **时间规律** — 近 30 天趋势图、24 小时生物钟分布
- **深度内容** — 高频词云、话题分类、长短句分布、最长语音原文
- **效率评分** — 作息健康、工作时段、专注度评分
- **App 统计** — 各 App 使用分布
- **AI 深度洞察** ⭐ — 大五人格雷达图、情绪分布与触发原因、灵感时刻、幽默检测、心理健康指标

---

## 需要准备什么

| 条件 | 说明 |
|------|------|
| [Typeless](https://typeless.app) | 语音转文字工具（需已有一些录音数据）|
| Python 3.12+ | [下载地址](https://www.python.org/downloads/) |
| uv | Python 包管理器 — `pip install uv` 或参考[安装文档](https://docs.astral.sh/uv/getting-started/installation/) |
| AI API Key | 以下任选其一：智谱 · DeepSeek · OpenAI · Anthropic · Moonshot · 阿里云 |

---

## 安装步骤（约 5 分钟）

**第一步：下载项目**

```bash
git clone https://github.com/OWENLEEzy/Happy-Typeless.git
cd Happy-Typeless
```

**第二步：安装依赖**

```bash
uv sync
```

**第三步：配置 AI Key**

```bash
cp .env.example .env
```

用任意文本编辑器打开 `.env`，填入你的 API Key：

```env
AI_API_KEY=your_api_key_here
AI_PRIMARY_PROVIDER=deepseek        # 可选：zhipu / openai / anthropic / moonshot / alibaba
AI_PRIMARY_MODEL=deepseek-chat      # 对应提供商的模型名
```

**第四步：运行**

```bash
uv run typeless analyze
```

分析完成后报告会自动在浏览器中打开。

---

## 常用命令

```bash
# 一键分析（自动从 Typeless 数据库读取）
uv run typeless analyze

# 生成英文报告
uv run typeless analyze --lang en

# 用模拟数据体验（无需 Typeless 也无需 API Key）
uv run typeless analyze -m

# 换了模型或 API 后重新跑 AI 分析
uv run typeless analyze --force-refresh

# 缓存与费用管理
uv run typeless cache status
uv run typeless cache clear
uv run typeless cost
```

| 参数 | 说明 |
|------|------|
| `-i, --input PATH` | 指定 JSON 文件（不填则自动从数据库读取）|
| `-o, --output PATH` | 输出路径（默认：`output/personal/Typeless_Report.html`）|
| `-l, --lang` | 报告语言：`zh`（默认）或 `en` |
| `-m, --mock` | 使用模拟数据，无需 API Key 和 Typeless |
| `--force-refresh` | 忽略缓存，重新跑全部 AI 分析 |
| `--no-open` | 生成后不自动打开浏览器 |

---

## 费用大概是多少？

AI 分析每条记录只跑一次，结果缓存到本地——**之后重新生成报告完全免费**。

首次分析的大概费用（按每条约 900 个 token 估算）：

| 记录数 | DeepSeek | 智谱 GLM-4-Flash | Anthropic Claude |
|--------|----------|-----------------|-----------------|
| 500 条 | ~¥0.1 | ~¥0.6 | ~¥2.5 |
| 1000 条 | ~¥0.2 | ~¥1.2 | ~¥5 |
| 3000 条 | ~¥0.5 | ~¥3.5 | ~¥15 |

> 首次跑完之后，不管改多少次 HTML 报告，都不会再产生费用。

---

## 常见问题

**Typeless 数据库在哪里？**
macOS：`~/Library/Application Support/Typeless/typeless.db`，工具会自动找到，无需手动配置。

**我的语音内容会上传吗？**
只有每条录音的**文字内容**会发给 AI API 分析，原始音频不会被访问。

**可以自定义数据库路径吗？**
可以，在 `.env` 里设置 `TYPELESS_DB_PATH=/你的路径`。

**报告无法自动打开 / 在 Windows 上使用**
加上 `--no-open` 参数运行，然后手动打开 `output/personal/Typeless_Report.html`。
