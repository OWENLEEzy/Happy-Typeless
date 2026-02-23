#!/usr/bin/env python3
"""
HTML Report Generator - Brutalist Style
========================================
Generate single-file HTML report with all analysis data

Author: Claude Code
"""

import html as _html
import json
from pathlib import Path
from typing import Any

from src.translations import I18n


class BrutalistHTMLGenerator:
    """Brutalist style HTML report generator"""

    def __init__(self, lang: str = "en"):
        """Initialize HTML generator with language setting.

        Args:
            lang: Output language ('zh' for Chinese, 'en' for English)
        """
        self.i18n = I18n(lang)

    def generate(self, analysis_data: dict[str, Any], output_path: str) -> None:
        """
        Generate HTML report

        Args:
            analysis_data: Complete data returned by analyzer
            output_path: Output file path
        """

        # Extract module data
        overview = analysis_data.get("overview", {})
        habits = analysis_data.get("usage_habits", {})
        sentiment = analysis_data.get("language_sentiment", {})
        trends = analysis_data.get("time_trends", {})
        content = analysis_data.get("content_deep_dive", {})
        # Phase 1 additions
        personality = analysis_data.get("personality_profile", {})
        word_categories = analysis_data.get("word_categories", {})
        efficiency = analysis_data.get("efficiency_metrics", {})
        app_usage = analysis_data.get("app_usage", {})
        emotion_deep = analysis_data.get("emotion_deep", {})
        # AI insights
        ai_insights = analysis_data.get("ai_insights", {})

        # Render template
        html_content = self._render_template(
            overview,
            habits,
            sentiment,
            trends,
            content,
            personality,
            word_categories,
            efficiency,
            app_usage,
            emotion_deep,
            ai_insights,
        )

        # Write to file
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _render_template(
        self,
        overview: dict,
        habits: dict,
        sentiment: dict,
        trends: dict,
        content: dict,
        personality: dict | None = None,
        word_categories: dict | None = None,
        efficiency: dict | None = None,
        app_usage: dict | None = None,
        emotion_deep: dict | None = None,
        ai_insights: dict | None = None,
    ) -> str:
        """Render HTML template"""

        # Prepare data
        ai_insights = ai_insights or {}
        ai_personality = ai_insights.get("personality_profile", {})
        ai_emotion_triggers = ai_insights.get("emotion_triggers", {})
        ai_sentiment_dist = ai_insights.get("sentiment_distribution", {})
        sorted_triggers = sorted(ai_emotion_triggers.items(), key=lambda x: -x[1])[:10]
        ai_triggers_labels = [k for k, v in sorted_triggers]
        ai_triggers_values = [v for k, v in sorted_triggers]
        ai_big_five = {
            "openness": ai_personality.get("openness", 0),
            "conscientiousness": ai_personality.get("conscientiousness", 0),
            "extraversion": ai_personality.get("extraversion", 0),
            "agreeableness": ai_personality.get("agreeableness", 0),
            "neuroticism": ai_personality.get("neuroticism", 0),
        }

        swear_calendar = sentiment.get("swear_calendar", [])
        sentence_patterns = sentiment.get("sentence_patterns", {})
        sentiment_stats = sentiment.get("sentiment_stats", {})
        hour_dist = trends.get("hour_distribution", [0] * 24)
        daily_trend = trends.get("daily_trend", {"dates": [], "counts": []})
        topic_dist = content.get("topic_distribution", {})
        length_dist = content.get("sentence_length_distribution", {})
        longest_yap = content.get("longest_yap", {})
        word_cloud = sentiment.get("top_words", [])[:20]
        badge = overview.get("badge", {})

        # Prepare emotion trend data
        emotion_trend = emotion_deep.get("daily_trend", []) if emotion_deep else []
        emotion_trend_dates = [t.get("date", "") for t in emotion_trend]
        emotion_trend_scores = [t.get("avg_sentiment", 0) for t in emotion_trend]

        # Calculate normal_ratio (not in SentimentStats model)
        sentiment_total = sentiment_stats.get("normal", 0) + sentiment_stats.get("negative", 0)
        normal_ratio_calc = (
            sentiment_stats.get("normal", 0) / sentiment_total * 100 if sentiment_total > 0 else 0
        )

        html = f"""<!DOCTYPE html>
<html lang="{self.i18n.html_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.i18n.t("html_title")}</title>
    <!-- Tailwind CSS - disabled some utilities that conflict -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            corePlugins: {{
                preflight: false,
            }},
            // Important: don't override grid utilities
            theme: {{
                extend: {{
                    gridTemplateColumns: {{
                        '4': 'repeat(4, minmax(0, 1fr))',
                    }}
                }}
            }}
        }}
    </script>
    <style>
        /* Override Tailwind grid utilities for bento-grid */
        .bento-grid {{
            display: grid !important;
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 1rem;
            align-items: start !important;
            align-content: start !important;
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {{
            --bg-primary: #F4EFEA;
            --bg-card: #FFFFFF;
            --bg-elevated: #FAF9F6;
            --bg-hover: #F0EDE8;
            --text-primary: #2D2D2D;
            --text-secondary: #6B6B6B;
            --text-tertiary: #9B9B9B;
            --border-default: #2D2D2D;
            --border-subtle: #E5E5E5;
            --border-color: #2D2D2D;
            --accent-primary: #FFDE00;
            --accent-secondary: #6FC2FF;
            --accent-success: #00D26A;
            --accent-warning: #FFAB00;
            --accent-error: #FF4D4D;
            --accent-purple: #A855F7;
            --accent-orange: #FF8C00;
            --accent-blue: #6FC2FF;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            transition: background 0.3s, color 0.3s;
        }}

        body.theme-dark {{
            --bg-primary: #121212;
            --bg-card: #1E1E1E;
            --bg-elevated: #2A2A2A;
            --bg-hover: #323232;
            --text-primary: #F4EFEA;
            --text-secondary: #9B9B9B;
            --border-default: #6B6B6B;
            --border-subtle: #3A3A3A;
            --border-color: #6B6B6B;
        }}

        .font-mono {{
            font-family: 'JetBrains Mono', 'SF Mono', 'Consolas', monospace;
        }}

        /* Card base styles */
        .card {{
            background: var(--bg-card);
            border: 2px solid var(--border-default);
            border-radius: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .card:hover {{
            transform: translate(-2px, -2px);
            box-shadow: 4px 4px 0 var(--accent-primary);
        }}

        .card-header {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .card-body {{
            padding: 20px;
        }}

        /* Tag styles */
        .tag {{
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            background: var(--bg-elevated);
            border: 1px solid var(--border-subtle);
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .tag-primary {{
            background: var(--accent-primary);
            border-color: var(--accent-primary);
        }}

        .tag-success {{
            background: var(--accent-success);
            border-color: var(--accent-success);
            color: white;
        }}

        .tag-error {{
            background: var(--accent-error);
            border-color: var(--accent-error);
            color: white;
        }}

        /* Data number styles */
        .data-value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 36px;
            font-weight: 400;
            line-height: 1;
            letter-spacing: -0.02em;
        }}

        .data-value-lg {{
            font-size: 48px;
        }}

        .data-label {{
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            font-weight: 500;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Progress bar */
        .progress-bar {{
            height: 8px;
            background: var(--bg-elevated);
            border: 1px solid var(--border-subtle);
            position: relative;
        }}

        .progress-fill {{
            height: 100%;
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* Navigation bar */
        .nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 48px;
            background: var(--bg-primary);
            border-bottom: 2px solid var(--border-default);
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            font-weight: 400;
            border: 2px solid var(--border-default);
            border-radius: 0;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: var(--bg-card);
            color: var(--text-primary);
        }}

        .btn:hover {{
            background: var(--text-primary);
            color: var(--bg-card);
            transform: translate(-2px, -2px);
            box-shadow: 4px 4px 0 var(--accent-primary);
        }}

        /* Catchphrase tags */
        .phrase-tag {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 6px 12px;
            margin: 4px;
            background: var(--bg-elevated);
            border: 1px solid var(--border-subtle);
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            transition: all 0.2s ease;
        }}

        .phrase-tag:hover {{
            background: var(--accent-primary);
            transform: translate(-1px, -1px);
        }}

        .phrase-count {{
            font-size: 10px;
            padding: 2px 6px;
            background: var(--accent-secondary);
            border-radius: 0;
        }}

        /* Sentence pattern comparison blocks */
        .sentence-compare {{
            display: flex;
            gap: 1rem;
        }}

        .sentence-block {{
            flex: 1;
            padding: 1.5rem;
            text-align: center;
        }}

        .sentence-block.question {{
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(168, 85, 247, 0.05));
            border: 2px solid var(--accent-purple);
        }}

        .sentence-block.statement {{
            background: linear-gradient(135deg, rgba(0, 210, 106, 0.15), rgba(0, 210, 106, 0.05));
            border: 2px solid var(--accent-success);
        }}

        .sentence-percent {{
            font-size: 2.5rem;
            font-weight: 900;
            line-height: 1;
        }}

        .question .sentence-percent {{ color: var(--accent-purple); }}
        .statement .sentence-percent {{ color: var(--accent-success); }}

        /* Emotion three-part section */
        .emotion-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
        }}

        .emotion-item {{
            text-align: center;
            padding: 1rem;
            border: 2px solid;
            background: var(--bg-elevated);
        }}

        .emotion-item.normal {{ border-color: var(--accent-success); }}
        .emotion-item.swear {{ border-color: var(--accent-orange); }}
        .emotion-item.negative {{ border-color: var(--accent-error); }}

        /* Profanity calendar */
        .swear-item {{
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding: 0.5rem;
            background: var(--bg-elevated);
            margin-bottom: 0.4rem;
            font-size: 0.8rem;
        }}

        .swear-time {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            color: var(--accent-error);
            white-space: nowrap;
        }}

        /* Top 5 */
        .top-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.3rem 0;
        }}

        .top-rank {{
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
            background: var(--bg-elevated);
        }}

        .top-rank.gold {{ background: var(--accent-primary); }}
        .top-rank.silver {{ background: var(--accent-secondary); }}
        .top-rank.bronze {{ background: var(--accent-error); }}

        .top-bar {{
            flex: 1;
            height: 4px;
            background: var(--bg-primary);
            margin-top: 0.25rem;
        }}

        .top-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--accent-success), var(--accent-secondary));
        }}

        /* Word cloud tags */
        .word-tag {{
            display: inline-block;
            padding: 6px 14px;
            margin: 4px;
            border: 1px solid var(--border-default);
            font-family: 'JetBrains Mono', monospace;
            transition: all 0.2s ease;
        }}

        .word-tag:hover {{
            background: var(--accent-primary);
            transform: translate(-1px, -1px);
            box-shadow: 2px 2px 0 var(--border-default);
        }}

        /* Topic classification */
        .topic-grid {{
            display: flex;
            gap: 0.75rem;
        }}

        .topic-item {{
            flex: 1;
            padding: 1rem;
            text-align: center;
            border: 2px solid;
        }}

        .topic-item.daily {{ border-color: var(--accent-success); }}
        .topic-item.ai {{ border-color: var(--accent-secondary); }}
        .topic-item.design {{ border-color: var(--accent-purple); }}

        /* Longest recording */
        .longest-yap {{
            background: var(--bg-primary);
            border: 1px solid var(--border-subtle);
            padding: 1rem;
        }}

        .yap-meta {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }}

        /* Achievement badge */
        .badge-card {{
            background: linear-gradient(135deg, var(--bg-elevated), var(--bg-card));
            border: 2px solid var(--border-default);
            padding: 1.5rem;
            text-align: center;
        }}

        .badge-icon {{
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }}

        .badge-name {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }}

        .badge-progress {{
            height: 6px;
            background: var(--bg-primary);
            border: 1px solid var(--border-subtle);
            border-radius: 0;
            overflow: hidden;
        }}

        .badge-progress-fill {{
            height: 100%;
            background: var(--accent-success);
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* Bento Grid column span - use bento- prefix to avoid Tailwind conflicts */
        .bento-col-1 {{ grid-column: span 1; }}
        .bento-col-2 {{ grid-column: span 2; }}
        .bento-col-3 {{ grid-column: span 3; }}
        .bento-col-4 {{ grid-column: span 4; }}

        /* Chart container */
        .chart-container {{
            width: 100%;
            height: 200px;
        }}

        /* ==========================================
           Phase 1 new styles
           ========================================== */

        /* Language style tags */
        .personality-tag {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 8px 14px;
            margin: 4px;
            background: var(--bg-elevated);
            border: 2px solid;
            border-radius: 0;
            transition: all 0.2s ease;
        }}

        .personality-tag:hover {{
            transform: translate(-1px, -1px);
            box-shadow: 2px 2px 0 var(--accent-primary);
        }}

        .tag-name {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .tag-desc {{
            font-size: 11px;
            color: var(--text-secondary);
        }}

        /* Word categories */
        .word-category {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .word-category:last-child {{
            border-bottom: none;
        }}

        .cat-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            padding: 3px 8px;
            color: white;
            text-transform: uppercase;
            font-weight: 600;
            min-width: 50px;
            text-align: center;
        }}

        .cat-words {{
            flex: 1;
        }}

        .cat-word {{
            display: inline-block;
            padding: 4px 8px;
            margin: 2px;
            background: var(--bg-elevated);
            border: 1px solid var(--border-subtle);
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
        }}

        .cat-word small {{
            color: var(--text-tertiary);
            font-size: 10px;
            margin-left: 4px;
        }}

        /* Efficiency scores */
        .efficiency-grid {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 1rem;
        }}

        .eff-item {{
            text-align: center;
        }}

        .eff-score {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 28px;
            font-weight: 600;
            display: block;
        }}

        .eff-label {{
            font-size: 11px;
            color: var(--text-secondary);
            text-transform: uppercase;
        }}

        .fragmentation-box {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            padding: 0.75rem;
            background: var(--bg-elevated);
            border: 1px solid var(--border-subtle);
        }}

        .frag-level {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            font-weight: 600;
            padding: 4px 10px;
            background: var(--accent-warning);
            color: white;
        }}

        .frag-desc {{
            font-size: 12px;
            color: var(--text-secondary);
        }}

        .frag-text {{
            font-size: 11px;
            color: var(--text-tertiary);
        }}

        /* App usage stats */
        .app-list {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .app-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .app-rank {{
            width: 24px;
            font-size: 12px;
            text-align: center;
        }}

        .app-info {{
            flex: 1;
        }}

        .app-name {{
            font-size: 12px;
            margin-bottom: 2px;
        }}

        .app-bar {{
            height: 4px;
            background: var(--bg-primary);
        }}

        .app-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--accent-success), var(--accent-secondary));
        }}

        .app-count {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            min-width: 30px;
            text-align: right;
        }}

        /* Emotion deep analysis */
        .emotion-deep-list {{
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }}

        .emotion-deep-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.5rem 0.75rem;
            background: var(--bg-elevated);
            border-left: 3px solid;
        }}

        .emotion-deep-item:nth-child(1) {{ border-color: #FF4D4D; }}
        .emotion-deep-item:nth-child(2) {{ border-color: #FFAB00; }}
        .emotion-deep-item:nth-child(3) {{ border-color: #6FC2FF; }}
        .emotion-deep-item:nth-child(4) {{ border-color: #9B9B9B; }}
        .emotion-deep-item:nth-child(5) {{ border-color: #A855F7; }}

        .emotion-label {{
            font-size: 12px;
            color: var(--text-secondary);
        }}

        .emotion-count {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            font-weight: 600;
        }}

        .emotion-ratio {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: var(--text-tertiary);
            min-width: 40px;
            text-align: right;
        }}

        /* Emotion collapsible panels */
        .emotion-accordion {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        .emotion-accordion-item {{
            background: var(--bg-elevated);
            border: 2px solid var(--border-default);
            border-radius: 0;
        }}
        .emotion-accordion-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1rem;
            cursor: pointer;
            user-select: none;
            transition: background 0.2s;
        }}
        .emotion-accordion-header:hover {{
            background: var(--bg-hover);
        }}
        .emotion-accordion-title {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .emotion-accordion-label {{
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
        }}
        .emotion-accordion-count {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: var(--text-secondary);
        }}
        .emotion-accordion-icon {{
            font-size: 12px;
            transition: transform 0.2s;
            color: var(--text-secondary);
        }}
        .emotion-accordion-header.active .emotion-accordion-icon {{
            transform: rotate(180deg);
        }}
        .emotion-accordion-content {{
            display: none;
            border-top: 2px solid var(--border-default);
            max-height: 300px;
            overflow-y: auto;
        }}
        .emotion-accordion-content.active {{
            display: block;
        }}
        .emotion-record-item {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-subtle);
        }}
        .emotion-record-item:last-child {{
            border-bottom: none;
        }}
        .emotion-record-meta {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: var(--text-secondary);
        }}
        .emotion-record-score {{
            color: var(--accent-error);
            font-weight: 600;
        }}
        .emotion-record-content {{
            font-size: 13px;
            line-height: 1.6;
            color: var(--text-primary);
        }}

        /* Bento Grid Layout */
        .bento-grid {{
            display: grid !important;
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 1rem;
            align-items: start !important;
            align-content: start !important;
        }}

        /* Fix grid child flexbox collapse - CRITICAL for content visibility */
        .bento-grid > * {{
            min-height: auto !important;
            min-width: 0;
            height: auto !important;
        }}

        /* Ensure flex containers inside grid items expand */
        .bento-grid .card {{
            display: flex !important;
            flex-direction: column !important;
            min-height: auto !important;
            height: auto !important;
            align-self: start !important;
        }}

        .bento-grid .card > * {{
            min-height: auto !important;
            flex-shrink: 0;
        }}

        .bento-grid .card-body {{
            flex: 1;
            min-height: auto !important;
        }}

        /* Responsive */
        @media (max-width: 1024px) {{
            .bento-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
            .bento-col-4 {{ grid-column: span 2 !important; }}
        }}

        @media (max-width: 640px) {{
            .bento-grid {{ grid-template-columns: 1fr !important; }}
            .bento-col-1, .bento-col-2, .bento-col-3, .bento-col-4 {{ grid-column: span 1 !important; }}
            .nav {{ padding: 12px 16px; }}
            .sentence-compare {{ flex-direction: column; }}
            .emotion-grid {{ grid-template-columns: 1fr; }}
        }}

        /* Tab Navigation */
        .tabs-container {{
            display: flex;
            gap: 0.5rem;
            border-bottom: 2px solid var(--border-default);
            margin-bottom: 2rem;
            overflow-x: auto;
        }}

        .tab-btn {{
            padding: 0.75rem 1.25rem;
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .tab-btn:hover {{
            color: var(--text-primary);
            background: var(--bg-elevated);
        }}

        .tab-btn.active {{
            color: var(--text-primary);
            border-bottom-color: var(--accent-primary);
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="nav">
        <div class="flex items-center gap-3">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                <line x1="12" y1="19" x2="12" y2="23"/>
                <line x1="8" y1="23" x2="16" y2="23"/>
            </svg>
            <span class="font-mono font-semibold text-lg">{self.i18n.t("brand_name")}</span>
        </div>
        <button class="btn" id="theme-toggle-btn">{self.i18n.t("btn_dark_mode")}</button>
    </nav>

    <!-- Main content -->
    <main class="p-6 lg:p-12">
        <!-- Page title -->
        <header class="mb-8">
            <p class="data-label">{self.i18n.t("report_header")}</p>
            <h1 class="font-mono text-4xl lg:text-5xl font-normal tracking-wide mt-2">
                {self.i18n.t("report_subtitle")}
            </h1>
            <p class="text-neutral-600 mt-2 text-sm" id="date-range">
                {self.i18n.t("data_range_label")}: {overview.get("start_date", "")} {self.i18n.t("to")} {overview.get("end_date", "")}
            </p>
        </header>

        <!-- Tab Navigation -->
        <div class="tabs-container">
            <button class="tab-btn active" data-tab="overview">{self.i18n.t("tab_overview")}</button>
            <button class="tab-btn" data-tab="personality">{self.i18n.t("tab_personality")}</button>
            <button class="tab-btn" data-tab="time">{self.i18n.t("tab_time")}</button>
            <button class="tab-btn" data-tab="content">{self.i18n.t("tab_content")}</button>
            <button class="tab-btn" data-tab="ai">{self.i18n.t("ai_insights")}</button>
        </div>

        <!-- Tab 1: Overview -->
        <div id="tab-overview" class="tab-content active">
            <!-- Bento Grid -->
        <div class="bento-grid">

            <!-- 1. Core Data Overview (6 cards) -->
            <div class="card bento-col-1">
                <div class="card-body">
                    <p class="data-label">{self.i18n.t("card_total_records")}</p>
                    <p class="data-value">{overview.get("total_records", 0):,}</p>
                </div>
            </div>

            <div class="card bento-col-1">
                <div class="card-body">
                    <p class="data-label">{self.i18n.t("card_total_words")}</p>
                    <p class="data-value" style="color: var(--accent-success);">{overview.get("total_words", 0):,}</p>
                </div>
            </div>

            <div class="card bento-col-1">
                <div class="card-body">
                    <p class="data-label">{self.i18n.t("card_total_duration")}</p>
                    <p class="data-value">{overview.get("total_duration", 0):.0f}<span class="text-sm text-neutral-500">{self.i18n.t("unit_minutes")}</span></p>
                </div>
            </div>

            <div class="card bento-col-1">
                <div class="card-body">
                    <p class="data-label">{self.i18n.t("card_daily_avg")}</p>
                    <p class="data-value">{overview.get("daily_avg", 0):.1f}</p>
                </div>
            </div>

            <div class="card bento-col-1">
                <div class="card-body">
                    <p class="data-label">{self.i18n.t("card_avg_words")}</p>
                    <p class="data-value">{overview.get("avg_words", 0):.1f}</p>
                </div>
            </div>

            <div class="card bento-col-1">
                <div class="card-body">
                    <p class="data-label">{self.i18n.t("card_avg_duration")}</p>
                    <p class="data-value">{overview.get("avg_duration", 0):.1f}<span class="text-sm text-neutral-500">{self.i18n.t("unit_seconds")}</span></p>
                </div>
            </div>

            <!-- Achievement badge -->
            <div class="badge-card bento-col-1">
                <div class="badge-icon">{badge.get("icon", "📝")}</div>
                <p class="badge-name">{badge.get("name", self.i18n.t("badge_default"))}</p>
                <div class="badge-progress">
                    <div class="badge-progress-fill" style="width: {badge.get("progress", 0) * 100}%; background-color: {badge.get("color", "#9B9B9B")};"></div>
                </div>
                <p class="font-mono text-xs text-neutral-500 mt-2">{overview.get("total_words", 0):,} / {badge.get("threshold", 10000):,} {self.i18n.t("badge_progress")}</p>
            </div>

            <!-- 2. Usage Habits -->
            <div class="card bento-col-2">
                <div class="card-header">
                    <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_usage_habits")}</h3>
                </div>
                <div class="card-body">
                    <div class="grid grid-cols-3 gap-4 text-center">
                        <div>
                            <p class="data-value">{habits.get("consecutive_days", 0)}</p>
                            <p class="text-xs text-neutral-500 mt-1">{self.i18n.t("label_consecutive_days")}</p>
                        </div>
                        <div>
                            <p class="data-value">{habits.get("active_days", 0)}</p>
                            <p class="text-xs text-neutral-500 mt-1">{self.i18n.t("label_active_days")}</p>
                        </div>
                        <div>
                            <p class="data-value">{habits.get("gap_days", 0)}</p>
                            <p class="text-xs text-neutral-500 mt-1">{self.i18n.t("label_gap_days")}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 2.1 Extreme comparison -->
            <div class="card bento-col-2">
                <div class="card-header">
                    <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_extreme_comparison")}</h3>
                </div>
                <div class="card-body">
                    <div class="flex items-center justify-around">
                        <div class="text-center">
                            <p class="text-xs text-neutral-500">{self.i18n.t("label_busiest_week")}</p>
                            <p class="data-value text-xl" style="color: var(--accent-success);">{habits.get("busiest_week", 0)}</p>
                        </div>
                        <div class="text-center">
                            <p class="data-value" style="color: var(--accent-warning);">x{habits.get("week_ratio", 1):.1f}</p>
                            <p class="text-xs text-neutral-500">{self.i18n.t("label_gap_ratio")}</p>
                        </div>
                        <div class="text-center">
                            <p class="text-xs text-neutral-500">{self.i18n.t("label_laziest_week")}</p>
                            <p class="data-value text-xl" style="color: var(--accent-error);">{habits.get("laziest_week", 0)}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4. Sentence patterns -->
            <div class="card bento-col-2">
                <div class="card-header">
                    <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_sentence_patterns")}</h3>
                </div>
                <div class="card-body">
                    <div class="sentence-compare">
                        <div class="sentence-block question">
                            <p class="sentence-percent">{sentence_patterns.get("question_ratio", 0):.0f}%</p>
                            <p class="text-sm text-neutral-600 mt-1">{self.i18n.t("label_question")}</p>
                            <p class="font-mono text-xs text-neutral-500">{sentence_patterns.get("question_count", 0)} {self.i18n.t("label_unit_suffix")}</p>
                        </div>
                        <div class="sentence-block statement">
                            <p class="sentence-percent">{sentence_patterns.get("statement_ratio", 0):.0f}%</p>
                            <p class="text-sm text-neutral-600 mt-1">{self.i18n.t("label_statement")}</p>
                            <p class="font-mono text-xs text-neutral-500">{sentence_patterns.get("statement_count", 0)} {self.i18n.t("label_unit_suffix")}</p>
                        </div>
                    </div>
                    <p class="text-center text-sm text-neutral-500 mt-4 p-2 bg-[var(--bg-elevated)] border border-[var(--border-subtle)]">
                        {self.i18n.t("conclusion_commander")}
                    </p>
                </div>
            </div>

            <!-- 4.1 Emotion three-part analysis -->
            <div class="card bento-col-2">
                <div class="card-header">
                    <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_emotion_overview")}</h3>
                </div>
                <div class="card-body">
                    <div class="emotion-grid" style="grid-template-columns: repeat(2, 1fr);">
                        <div class="emotion-item normal">
                            <p class="text-lg font-bold" style="color: var(--accent-success);">{normal_ratio_calc:.0f}%</p>
                            <p class="text-xs text-neutral-600 mt-1">{self.i18n.t("label_normal_positive")}</p>
                            <p class="font-mono text-xs text-neutral-500">{sentiment_stats.get("normal", 0)} {self.i18n.t("label_unit_suffix")}</p>
                        </div>
                        <div class="emotion-item negative">
                            <p class="text-lg font-bold" style="color: var(--accent-error);">{sentiment_stats.get("negative_ratio", 0):.1f}%</p>
                            <p class="text-xs text-neutral-600 mt-1">{self.i18n.t("label_negative")}</p>
                            <p class="font-mono text-xs text-neutral-500">{sentiment_stats.get("negative", 0)} {self.i18n.t("label_unit_suffix")}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 30-day trend chart -->
            <div class="card bento-col-2">
                <div class="card-header">
                    <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_30day_trend")}</h3>
                </div>
                <div class="card-body">
                    <div id="chart-trend-overview" class="chart-container" style="height: 200px;"></div>
                </div>
            </div>

            <!-- 24-hour distribution chart -->
            <div class="card bento-col-2">
                <div class="card-header">
                    <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_24hour_dist")}</h3>
                </div>
                <div class="card-body">
                    <div id="chart-hour-overview" class="chart-container" style="height: 200px;"></div>
                </div>
            </div>

        </div>
        </div>
        <!-- End Tab 1: Overview -->

        <!-- Tab 2: Personality & Efficiency -->
        <div id="tab-personality" class="tab-content">
            <div class="bento-grid">
                <!-- Personality Profile (Full Width) -->
                <div class="card bento-col-4">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_personality")}</h3>
                    </div>
                    <div class="card-body">
                        <div class="flex flex-wrap justify-center">
                            {self._render_personality_profile(personality) if personality else ""}
                        </div>
                    </div>
                </div>

                <!-- Efficiency Metrics -->
                <div class="card bento-col-4">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_efficiency")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_efficiency_metrics(efficiency) if efficiency else ""}
                    </div>
                </div>

                <!-- Word Categories -->
                <div class="card bento-col-4">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_word_categories")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_word_categories(word_categories) if word_categories else ""}
                    </div>
                </div>

                <!-- Sentence Patterns -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_sentence_patterns")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_sentence_patterns(sentence_patterns)}
                    </div>
                </div>

                <!-- Emotion Overview -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_emotion_overview")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_emotion_overview(sentiment_stats)}
                    </div>
                </div>

                <!-- App Usage Stats -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_app_usage")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_app_usage(app_usage) if app_usage else ""}
                    </div>
                </div>
            </div>
        </div>
        <!-- End Tab 2: Personality -->

        <!-- Tab 3: Time Trends -->
        <div id="tab-time" class="tab-content">
            <div class="bento-grid">
                <!-- Usage Habits -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_usage_habits")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_usage_habits(habits)}
                    </div>
                </div>

                <!-- Extreme Comparison -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_extreme_comparison")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_extreme_comparison(habits)}
                    </div>
                </div>

                <!-- 30 Day Trend -->
                <div class="card bento-col-4">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_30day_trend")}</h3>
                    </div>
                    <div class="card-body">
                        <div id="chart-trend-time" class="chart-container" style="height: 200px;"></div>
                    </div>
                </div>

                <!-- 24 Hour Distribution -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_24hour_dist")}</h3>
                    </div>
                    <div class="card-body">
                        <div id="chart-hour-time" class="chart-container" style="height: 200px;"></div>
                    </div>
                </div>

                <!-- Top 5 Dates -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_top_dates")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_top_dates(trends.get("top_dates", []))}
                    </div>
                </div>
            </div>
        </div>
        <!-- End Tab 3: Time Trends -->

        <!-- Tab 4: Content Deep Dive -->
        <div id="tab-content" class="tab-content">
            <div class="bento-grid">
                <!-- Topic Classification -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_topic_classification")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_topic_classification(topic_dist)}
                    </div>
                </div>

                <!-- High Frequency Words -->
                <div class="card bento-col-4">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_word_cloud")}</h3>
                    </div>
                    <div class="card-body">
                        <div class="flex flex-wrap content-start" style="max-height: 160px; overflow: hidden;">
                            {self._render_word_cloud(word_cloud)}
                        </div>
                    </div>
                </div>

                <!-- Sentence Length Distribution -->
                <div class="card bento-col-2">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_length_distribution")}</h3>
                    </div>
                    <div class="card-body">
                        <div id="chart-length-content" class="chart-container" style="height: 180px;"></div>
                    </div>
                </div>

                <!-- Longest Voice Recording -->
                <div class="card bento-col-4">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_longest_yap")}</h3>
                    </div>
                    <div class="card-body">
                        <div class="longest-yap">
                            <div class="yap-meta">
                                <span>{self.i18n.t("meta_date")} {longest_yap.get("date", "")}</span>
                                <span>{self.i18n.t("meta_hour")} {longest_yap.get("hour", 0)}:00</span>
                                <span>{self.i18n.t("meta_duration")} {longest_yap.get("duration", 0):.0f}{self.i18n.t("meta_seconds")}</span>
                                <span>{self.i18n.t("meta_words")} {longest_yap.get("word_count", 0)}{self.i18n.t("meta_words_unit")}</span>
                            </div>
                            <p class="text-sm leading-relaxed">"{_html.escape(longest_yap.get("content", ""))}"</p>
                        </div>
                    </div>
                </div>

                <!-- Emotion Deep Analysis -->
                <div class="card bento-col-4">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_emotion_deep")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_emotion_deep(emotion_deep)}
                    </div>
                </div>

                <!-- Swear Calendar -->
                <div class="card bento-col-4">
                    <div class="card-header">
                        <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("section_swear_calendar")}</h3>
                    </div>
                    <div class="card-body">
                        {self._render_swear_calendar(swear_calendar)}
                    </div>
                </div>
            </div>
        </div>
        <!-- End Tab 4: Content -->

        <!-- Tab 5: AI Insights -->
        <div id="tab-ai" class="tab-content">
            <div class="bento-grid">
                {self._render_ai_insights(ai_insights)}
            </div>
        </div>
        <!-- End Tab 5: AI Insights -->

    </main>

    <footer class="text-center py-8 text-sm text-neutral-500 font-mono">
        {self.i18n.t("footer_generated")} · {overview.get("end_date", "")}
    </footer>

    <script>
        // Data
        const DATA = {{
            hour_dist: {json.dumps(hour_dist)},
            daily_trend: {{
                dates: {json.dumps(daily_trend.get("dates", []))},
                counts: {json.dumps(daily_trend.get("counts", []))}
            }},
            length_dist: {{
                short: {length_dist.get("short", 0)},
                medium: {length_dist.get("medium", 0)},
                long: {length_dist.get("long", 0)}
            }},
            i18n: {{
                chart_short: "{self.i18n.t("chart_short")}",
                chart_medium: "{self.i18n.t("chart_medium")}",
                chart_long: "{self.i18n.t("chart_long")}",
                btn_dark: "{self.i18n.t("btn_dark_mode")}",
                btn_light: "{self.i18n.t("btn_light_mode")}"
            }},
            emotion_trend: {{
                dates: {json.dumps(emotion_trend_dates)},
                scores: {json.dumps(emotion_trend_scores)}
            }},
            ai_insights: {{
                big_five: {json.dumps(ai_big_five)},
                triggers_labels: {json.dumps(ai_triggers_labels)},
                triggers_values: {json.dumps(ai_triggers_values)},
                sentiment: {json.dumps(ai_sentiment_dist)}
            }}
        }};

        // Colors
        function getColors() {{
            const isDark = document.body.classList.contains('theme-dark');
            return {{
                bg: isDark ? '#1E1E1E' : '#FFFFFF',
                text: isDark ? '#9B9B9B' : '#6B6B6B',
                border: isDark ? '#3A3A3A' : '#E5E5E5',
                green: '#00D26A',
                blue: '#6FC2FF',
                yellow: '#FFDE00',
                purple: '#A855F7',
                pink: '#FF4D4D'
            }};
        }}

        // Chart instance cache
        const charts = {{}};

        // 30-day trend chart
        function renderTrendChart(tabName = 'overview') {{
            const chartId = 'chart-trend-' + tabName;
            const container = document.getElementById(chartId);
            if (!container) return;

            if (!charts[chartId]) {{
                charts[chartId] = echarts.init(container);
            }}

            const c = getColors();
            charts[chartId].setOption({{
                grid: {{ left: 40, right: 20, top: 20, bottom: 30 }},
                xAxis: {{
                    type: 'category',
                    data: DATA.daily_trend.dates,
                    axisLine: {{ lineStyle: {{ color: c.border }} }},
                    axisLabel: {{ fontFamily: 'JetBrains Mono', fontSize: 10, color: c.text }}
                }},
                yAxis: {{
                    type: 'value',
                    splitLine: {{ lineStyle: {{ color: c.border, type: 'dashed' }} }},
                    axisLabel: {{ fontFamily: 'JetBrains Mono', fontSize: 10, color: c.text }}
                }},
                series: [{{
                    type: 'line',
                    data: DATA.daily_trend.counts,
                    smooth: true,
                    itemStyle: {{ color: c.yellow }},
                    lineStyle: {{ width: 2, color: c.yellow }},
                    areaStyle: {{
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            {{ offset: 0, color: 'rgba(255, 222, 0, 0.3)' }},
                            {{ offset: 1, color: 'rgba(255, 222, 0, 0)' }}
                        ])
                    }}
                }}]
            }});
        }}

        // 24-hour distribution
        function renderHourChart(tabName = 'overview') {{
            const chartId = 'chart-hour-' + tabName;
            const container = document.getElementById(chartId);
            if (!container) return;

            if (!charts[chartId]) {{
                charts[chartId] = echarts.init(container);
            }}

            const c = getColors();
            charts[chartId].setOption({{
                grid: {{ left: 40, right: 20, top: 20, bottom: 30 }},
                xAxis: {{
                    type: 'category',
                    data: Array.from({{length: 24}}, (_, i) => i + 'h'),
                    axisLine: {{ lineStyle: {{ color: c.border }} }},
                    axisLabel: {{ fontFamily: 'JetBrains Mono', fontSize:10, color: c.text }}
                }},
                yAxis: {{
                    type: 'value',
                    splitLine: {{ lineStyle: {{ color: c.border, type: 'dashed' }} }},
                    axisLabel: {{ fontFamily: 'JetBrains Mono', fontSize: 10, color: c.text }}
                }},
                series: [{{
                    type: 'bar',
                    data: DATA.hour_dist,
                    itemStyle: {{
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            {{ offset: 0, color: c.blue }},
                            {{ offset: 1, color: 'rgba(111, 194, 255, 0.2)' }}
                        ]),
                        borderRadius: [0, 0, 0, 0]
                    }}
                }}]
            }});
        }}

        // Length distribution
        function renderLengthChart(tabName = 'overview') {{
            const chartId = 'chart-length-' + tabName;
            const container = document.getElementById(chartId);
            if (!container) return;

            if (!charts[chartId]) {{
                charts[chartId] = echarts.init(container);
            }}

            const c = getColors();
            charts[chartId].setOption({{
                series: [{{
                    type: 'pie',
                    radius: ['50%', '75%'],
                    center: ['50%', '50%'],
                    label: {{ show: false }},
                    data: [
                        {{ value: DATA.length_dist.short, name: DATA.i18n.chart_short, itemStyle: {{ color: c.green }} }},
                        {{ value: DATA.length_dist.medium, name: DATA.i18n.chart_medium, itemStyle: {{ color: c.blue }} }},
                        {{ value: DATA.length_dist.long, name: DATA.i18n.chart_long, itemStyle: {{ color: c.purple }} }}
                    ]
                }}]
            }});
        }}

        // Emotion trend chart
        function renderEmotionTrendChart() {{
            const container = document.getElementById('chart-emotion-trend');
            if (!container || DATA.emotion_trend.dates.length === 0) return;

            if (!charts['emotion-trend']) {{
                charts['emotion-trend'] = echarts.init(container);
            }}

            const c = getColors();
            charts['emotion-trend'].setOption({{
                grid: {{ left: 40, right: 20, top: 20, bottom: 40 }},
                xAxis: {{
                    type: 'category',
                    data: DATA.emotion_trend.dates,
                    axisLine: {{ lineStyle: {{ color: c.border }} }},
                    axisLabel: {{ fontFamily: 'JetBrains Mono', fontSize: 9, color: c.text, rotate: 30 }}
                }},
                yAxis: {{
                    type: 'value',
                    splitLine: {{ lineStyle: {{ color: c.border, type: 'dashed' }} }},
                    axisLabel: {{ fontFamily: 'JetBrains Mono', fontSize: 10, color: c.text }}
                }},
                series: [{{
                    type: 'line',
                    data: DATA.emotion_trend.scores,
                    smooth: true,
                    itemStyle: {{ color: c.pink }},
                    lineStyle: {{ width: 2, color: c.pink }},
                    areaStyle: {{
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            {{ offset: 0, color: 'rgba(255, 77, 77, 0.3)' }},
                            {{ offset: 1, color: 'rgba(255, 77, 77, 0)' }}
                        ])
                    }}
                }}]
            }});
        }}

        // Big Five radar chart
        function renderBigFiveChart() {{
            const container = document.getElementById('chart-bigfive-ai');
            if (!container) return;
            if (!charts['bigfive-ai']) {{
                charts['bigfive-ai'] = echarts.init(container);
            }}
            const c = getColors();
            const bf = DATA.ai_insights.big_five;
            charts['bigfive-ai'].setOption({{
                radar: {{
                    indicator: [
                        {{ name: 'Open.', max: 1 }},
                        {{ name: 'Conscient.', max: 1 }},
                        {{ name: 'Extravers.', max: 1 }},
                        {{ name: 'Agreeable.', max: 1 }},
                        {{ name: 'Neurotic.', max: 1 }},
                    ],
                    splitLine: {{ lineStyle: {{ color: c.border }} }},
                    axisLine: {{ lineStyle: {{ color: c.border }} }},
                    name: {{ textStyle: {{ color: c.text, fontFamily: 'JetBrains Mono', fontSize: 10 }} }}
                }},
                series: [{{
                    type: 'radar',
                    data: [{{
                        value: [bf.openness, bf.conscientiousness, bf.extraversion, bf.agreeableness, bf.neuroticism],
                        itemStyle: {{ color: c.yellow }},
                        lineStyle: {{ color: c.yellow }},
                        areaStyle: {{ color: 'rgba(255, 222, 0, 0.2)' }}
                    }}]
                }}]
            }});
        }}

        // Emotion triggers bar chart
        function renderTriggersChart() {{
            const container = document.getElementById('chart-triggers-ai');
            if (!container || DATA.ai_insights.triggers_labels.length === 0) return;
            if (!charts['triggers-ai']) {{
                charts['triggers-ai'] = echarts.init(container);
            }}
            const c = getColors();
            charts['triggers-ai'].setOption({{
                grid: {{ left: 120, right: 20, top: 10, bottom: 30 }},
                xAxis: {{
                    type: 'value',
                    splitLine: {{ lineStyle: {{ color: c.border, type: 'dashed' }} }},
                    axisLabel: {{ fontFamily: 'JetBrains Mono', fontSize: 10, color: c.text }}
                }},
                yAxis: {{
                    type: 'category',
                    data: DATA.ai_insights.triggers_labels,
                    axisLabel: {{ fontFamily: 'JetBrains Mono', fontSize: 10, color: c.text }}
                }},
                series: [{{
                    type: 'bar',
                    data: DATA.ai_insights.triggers_values,
                    itemStyle: {{ color: c.blue }}
                }}]
            }});
        }}

        // Initial render
        renderTrendChart('overview');
        renderHourChart('overview');
        renderLengthChart('overview');
        renderEmotionTrendChart();

        // Theme toggle
        function toggleTheme() {{
            document.body.classList.toggle('theme-dark');
            const btn = document.querySelector('.nav button');
            if (document.body.classList.contains('theme-dark')) {{
                btn.textContent = DATA.i18n.btn_light;
            }} else {{
                btn.textContent = DATA.i18n.btn_dark;
            }}
            setTimeout(() => {{
                // Re-render active tab charts
                const activeTab = document.querySelector('.tab-content.active');
                const tabName = activeTab ? activeTab.id.replace('tab-', '') : 'overview';
                renderTrendChart(tabName);
                renderHourChart(tabName);
                if (tabName === 'content' || tabName === 'overview') {{
                    renderLengthChart(tabName);
                }}
            }}, 100);
        }}

        // Tab switching
        function switchTab(tabName) {{
            // Hide all tab content
            document.querySelectorAll('.tab-content').forEach(el => {{
                el.classList.remove('active');
            }});
            // Remove active state from all tab buttons
            document.querySelectorAll('.tab-btn').forEach(el => {{
                el.classList.remove('active');
            }});
            // Show selected tab
            document.getElementById('tab-' + tabName).classList.add('active');
            // Add active state to button
            document.querySelector(`[data-tab="${{tabName}}"]`).classList.add('active');

            // Delay chart rendering to ensure DOM is visible
            setTimeout(() => {{
                // Render charts based on active tab
                if (tabName === 'overview') {{
                    renderTrendChart('overview');
                    renderHourChart('overview');
                    renderLengthChart('overview');
                }} else if (tabName === 'time') {{
                    renderTrendChart('time');
                    renderHourChart('time');
                }} else if (tabName === 'content') {{
                    renderLengthChart('content');
                }} else if (tabName === 'ai') {{
                    renderBigFiveChart();
                    renderTriggersChart();
                }}
                // personality tab has no charts, skip rendering
            }}, 100);
        }}

        // Responsive
        window.addEventListener('resize', () => {{
            Object.values(charts).forEach(chart => {{
                if (chart) chart.resize();
            }});
        }});

        // Tab button event listeners
        document.querySelectorAll('.tab-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                const tabName = e.target.getAttribute('data-tab');
                switchTab(tabName);
            }});
        }});

        // Theme toggle button event listeners
        const themeToggleBtn = document.getElementById('theme-toggle-btn');
        if (themeToggleBtn) {{
            themeToggleBtn.addEventListener('click', toggleTheme);
        }}
    </script>
</body>
</html>"""
        return html

    # ==========================================
    # Generic Rendering Helpers
    # ==========================================

    def _render_tag_cloud(
        self,
        items: list[dict],
        css_class: str = "word-tag",
        show_count: bool = True,
        top_n: int = 30,
    ) -> str:
        """Generic tag cloud rendering

        Args:
            items: List of {name, value} items
            css_class: CSS class for tags
            show_count: Whether to show count after name
            top_n: Maximum number of items to render
        """
        if not items:
            return f'<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        max_val = max(item.get("value", 0) for item in items[:top_n]) if items else 1

        tags = []
        for i, item in enumerate(items[:top_n]):
            val = item.get("value", 0)
            name = item.get("name", "")

            # Size based on relative frequency
            if val > max_val * 0.7:
                size = "text-lg"
            elif val > max_val * 0.4:
                size = "text-base"
            elif val > max_val * 0.2:
                size = "text-sm"
            else:
                size = "text-xs"

            # Highlight top 3
            bg = "bg-[#FFDE00]" if i < 3 else ""

            if show_count:
                content = f"{name} ({val})"
            else:
                content = name

            tags.append(f'<span class="{css_class} {size} {bg}">{content}</span>')

        return "".join(tags)

    def _render_ranked_list(
        self,
        items: list[dict],
        label_field: str,
        value_field: str,
        ratio_field: str | None = None,
        top_n: int = 5,
    ) -> str:
        """Generic ranking list rendering

        Args:
            items: List of items with label and value
            label_field: Field name for label
            value_field: Field name for value
            ratio_field: Optional field for bar width ratio
            top_n: Maximum items to render
        """
        if not items:
            return f'<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        items = items[:top_n]
        max_value = max(item.get(value_field, 0) for item in items) if items else 1

        result = []
        for i, item in enumerate(items):
            medals = ["🥇", "🥈", "🥉"]
            medal = medals[i] if i < 3 else f"{i + 1}."

            label = item.get(label_field, "")
            value = item.get(value_field, 0)

            if ratio_field:
                ratio = item.get(ratio_field, value / max_value * 100)
            else:
                ratio = value / max_value * 100

            result.append(f"""
                <div class="top-item">
                    <span class="top-rank {"gold" if i == 0 else "silver" if i == 1 else "bronze" if i < 3 else ""}">{medal}</span>
                    <div class="flex-1">
                        <div class="flex justify-between">
                            <span class="text-sm">{label}</span>
                            <span class="font-mono text-sm font-medium">{value}</span>
                        </div>
                        <div class="top-bar"><div class="top-bar-fill" style="width: {ratio}%;"></div></div>
                    </div>
                </div>
            """)

        return "".join(result)

    def _render_record_list(
        self,
        items: list[dict],
        date_field: str,
        content_field: str,
        hour_field: str = "hour",
        extra_field: str | None = None,
        extra_label: str = "",
    ) -> str:
        """Generic record list rendering (e.g., profanity calendar)

        Args:
            items: List of record items
            date_field: Field name for date
            content_field: Field name for content
            hour_field: Field name for hour
            extra_field: Optional extra field to display
            extra_label: Label for extra field
        """
        if not items:
            return f'<div class="text-center text-neutral-500 p-4">{self.i18n.t("no_data")}</div>'

        result = []
        for item in items:
            date = item.get(date_field, "")
            hour = item.get(hour_field, 0)
            content = _html.escape(item.get(content_field, ""))

            extra_html = ""
            if extra_field and extra_field in item:
                extra_html = f"<span>{extra_label} {item.get(extra_field, '')}</span>"

            result.append(f"""
                <div class="swear-item">
                    <span class="swear-time">{date} {hour:02d}</span>
                    {extra_html}
                    <span class="swear-content">{content}</span>
                </div>
            """)

        return "".join(result)

    # ==========================================
    # Phase 1 Specific Rendering Methods
    # ==========================================

    def _render_phrase_tags(self, top_words: list[dict]) -> str:
        """Render catchphrase tags (uses generic helper)"""
        return self._render_tag_cloud(top_words, css_class="phrase-tag", top_n=30)

    def _render_swear_calendar(self, swear_list: list[dict]) -> str:
        """Render profanity calendar (uses generic helper)"""
        return self._render_record_list(
            swear_list,
            date_field="date",
            content_field="content",
            hour_field="hour",
            extra_field="word_count",
            extra_label="words" if self.i18n.lang == "en" else "字数",
        )

    def _render_top_dates(self, top_dates: list[dict]) -> str:
        """Render Top 5 dates (uses generic helper)"""
        return self._render_ranked_list(top_dates, label_field="date", value_field="count", top_n=5)

    def _render_word_cloud(self, word_cloud: list[dict]) -> str:
        """Render word cloud tags (uses generic helper)"""
        return self._render_tag_cloud(word_cloud, css_class="word-tag", top_n=50)

    # ==========================================
    # Phase 1 Specific Rendering Methods
    # ==========================================

    def _render_personality_profile(self, personality: dict) -> str:
        """Render language style profile tags"""
        tags = personality.get("tags", [])
        if not tags:
            return f'<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        html_tags = []
        for tag in tags:
            # Tags are now pre-translated by PersonalityService
            name = tag.get("name", "")
            desc = tag.get("desc", "")

            html_tags.append(f"""
                <div class="personality-tag" style="border-color: {tag.get("color", "#9B9B9B")};">
                    <span class="tag-name" style="color: {tag.get("color", "#9B9B9B")};">{name}</span>
                    <span class="tag-desc">{desc}</span>
                </div>
            """)
        return "".join(html_tags)

    def _render_word_categories(self, categories: dict) -> str:
        """Render word categories display"""
        if not categories:
            return f'<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        category_labels = {
            "filler": (self.i18n.t("cat_filler"), "#FFAB00"),
            "connector": (self.i18n.t("cat_connector"), "#6FC2FF"),
            "content": (self.i18n.t("cat_content"), "#00D26A"),
        }

        html_parts = []
        for key, (label, color) in category_labels.items():
            words = categories.get(key, [])[:5]
            if not words:
                continue

            word_spans = " ".join(
                [
                    f"<span class='cat-word'>{w['name']}<small>{w['value']}</small></span>"
                    for w in words
                ]
            )

            html_parts.append(f"""
                <div class="word-category">
                    <span class="cat-label" style="background: {color};">{label}</span>
                    <div class="cat-words">{word_spans}</div>
                </div>
            """)

        return "".join(html_parts)

    def _render_efficiency_metrics(self, efficiency: dict) -> str:
        """Render efficiency score cards"""
        scores = efficiency.get("scores", {})
        fragmentation = efficiency.get("fragmentation", {})

        if not scores:
            return f'<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        # Score colors
        def get_score_color(score):
            if score >= 80:
                return "#00D26A"
            elif score >= 60:
                return "#FFAB00"
            else:
                return "#FF4D4D"

        sleep_color = get_score_color(scores.get("sleep_health", 0))
        work_color = get_score_color(scores.get("work_efficiency", 0))
        focus_color = get_score_color(scores.get("focus", 0))
        overall_color = get_score_color(scores.get("overall", 0))

        # Map fragmentation level from Chinese to English
        level = fragmentation.get("level", "")
        # Fragmentation level and description are now pre-translated by EfficiencyService
        frag_level = level
        frag_desc = fragmentation.get("desc", "")

        return f"""
            <div class="efficiency-grid">
                <div class="eff-item">
                    <span class="eff-score" style="color: {sleep_color};">{scores.get("sleep_health", 0)}</span>
                    <span class="eff-label">{self.i18n.t("score_sleep")}</span>
                </div>
                <div class="eff-item">
                    <span class="eff-score" style="color: {work_color};">{scores.get("work_efficiency", 0)}</span>
                    <span class="eff-label">{self.i18n.t("score_efficiency")}</span>
                </div>
                <div class="eff-item">
                    <span class="eff-score" style="color: {focus_color};">{scores.get("focus", 0)}</span>
                    <span class="eff-label">{self.i18n.t("score_focus")}</span>
                </div>
                <div class="eff-item">
                    <span class="eff-score" style="color: {overall_color};">{scores.get("overall", 0)}</span>
                    <span class="eff-label">{self.i18n.t("score_overall")}</span>
                </div>
            </div>
            <div class="fragmentation-box">
                <span class="frag-level">{frag_level}</span>
                <span class="frag-desc">{self.i18n.t("fragmentation_title")} {fragmentation.get("ratio", 0)}%</span>
                <span class="frag-text">{frag_desc}</span>
            </div>
        """

    def _render_app_usage(self, app_usage: dict) -> str:
        """Render app usage stats"""
        if not app_usage.get("has_data", False):
            return f'<p class="text-neutral-500 text-sm">{self.i18n.t("no_app_data")}</p>'

        apps = app_usage.get("apps", [])[:5]
        if not apps:
            return f'<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        items = []
        for i, app in enumerate(apps):
            medals = ["🥇", "🥈", "🥉"]
            medal = medals[i] if i < 3 else f"{i + 1}."

            items.append(f"""
                <div class="app-item">
                    <span class="app-rank">{medal}</span>
                    <div class="app-info">
                        <div class="app-name">{app.get("app_name", "")}</div>
                        <div class="app-bar">
                            <div class="app-bar-fill" style="width: {app.get("ratio", 0)}%;"></div>
                        </div>
                    </div>
                    <span class="app-count">{app.get("count", 0)}</span>
                </div>
            """)

        return f'<div class="app-list">{"".join(items)}</div>'

    def _render_emotion_deep(self, emotion_deep: dict) -> str:
        """Render emotion deep analysis - collapsible panels with trend chart"""
        if not emotion_deep:
            return f'<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        categories = emotion_deep.get("categories", {})
        daily_trend = emotion_deep.get("daily_trend", [])

        if not categories and not daily_trend:
            return f'<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        # Trend chart section (if data available)
        trend_html = ""
        if daily_trend:
            trend_html = f"""
            <div class="mb-4">
                <h4 class="font-mono text-xs uppercase tracking-wider text-neutral-500 mb-2">{self.i18n.t("section_emotion_trend")}</h4>
                <div id="chart-emotion-trend" class="chart-container" style="height: 160px;"></div>
            </div>
            """

        # Category labels
        category_labels = {
            "anger": (self.i18n.t("emotion_anger"), "#FF4D4D"),
            "anxiety": (self.i18n.t("emotion_anxiety"), "#FFAB00"),
            "sadness": (self.i18n.t("emotion_sadness"), "#6FC2FF"),
            "fatigue": (self.i18n.t("emotion_fatigue"), "#9B9B9B"),
            "stress": (self.i18n.t("emotion_stress"), "#A855F7"),
        }

        # Generate collapsible panels
        accordion_items = []
        for key in ["anger", "anxiety", "sadness", "fatigue", "stress"]:
            if key not in categories:
                continue

            cat_data = categories[key]
            label, color = category_labels[key]
            count = cat_data.get("count", 0)
            ratio = cat_data.get("ratio", 0)
            records = cat_data.get("records", [])

            # Generate record list for this category
            records_html = ""
            for record in records[:50]:  # Show max 50 records
                records_html += f"""
            <div class="emotion-record-item">
                <div class="emotion-record-meta">
                    <span>{record.get("date", "")} {record.get("hour", 0):02d}:00</span>
                    <span class="emotion-record-score">{record.get("sentiment_score", 0):.2f}</span>
                    <span>{record.get("word_count", 0)} {self.i18n.t("meta_words_unit")}</span>
                </div>
                <div class="emotion-record-content">{_html.escape(record.get("content", ""))}</div>
            </div>"""

            if not records:
                records_html = f'<div class="emotion-record-item"><p class="text-neutral-500">{self.i18n.t("no_data")}</p></div>'

            accordion_items.append(f"""
        <div class="emotion-accordion-item">
            <div class="emotion-accordion-header" onclick="toggleEmotionAccordion(this)">
                <div class="emotion-accordion-title">
                    <span class="emotion-accordion-label" style="color: {color};">{label}</span>
                    <span class="emotion-accordion-count">{count} ({ratio}%)</span>
                </div>
                <span class="emotion-accordion-icon">❯</span>
            </div>
            <div class="emotion-accordion-content">
                {records_html}
            </div>
        </div>""")

        return f"""
    {trend_html}
    <div class="emotion-accordion">
        {''.join(accordion_items)}
    </div>
    <script>
    function toggleEmotionAccordion(header) {{
        const content = header.nextElementSibling;
        const isActive = header.classList.contains('active');

        // Close all other panels
        document.querySelectorAll('.emotion-accordion-header').forEach(h => {{
            h.classList.remove('active');
            h.nextElementSibling.classList.remove('active');
        }});

        // Toggle current panel
        if (!isActive) {{
            header.classList.add('active');
            content.classList.add('active');
        }}
    }}
    </script>
    """

    def _render_sentence_patterns(self, patterns: dict) -> str:
        """Render sentence patterns"""
        if not patterns:
            return '<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        question_count = patterns.get("question_count", 0)
        statement_count = patterns.get("statement_count", 0)
        total = question_count + statement_count

        if total == 0:
            return '<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        question_ratio = question_count / total * 100 if total > 0 else 0
        statement_ratio = statement_count / total * 100 if total > 0 else 0

        conclusion = ""
        if question_ratio > 60:
            conclusion = self.i18n.t("conclusion_questioner")
        elif statement_ratio > 60:
            conclusion = self.i18n.t("conclusion_commander")
        else:
            conclusion = self.i18n.t("conclusion_balanced")

        return f"""
            <div class="sentence-compare flex gap-4">
                <div class="flex-1 text-center p-4" style="border: 2px solid var(--border-default);">
                    <p class="font-mono text-2xl" style="color: var(--accent-secondary);">{question_count}</p>
                    <p class="text-sm text-neutral-500">{self.i18n.t("label_question")}</p>
                    <p class="font-mono text-xs">{question_ratio:.0f}%</p>
                </div>
                <div class="flex-1 text-center p-4" style="border: 2px solid var(--border-default);">
                    <p class="font-mono text-2xl" style="color: var(--accent-success);">{statement_count}</p>
                    <p class="text-sm text-neutral-500">{self.i18n.t("label_statement")}</p>
                    <p class="font-mono text-xs">{statement_ratio:.0f}%</p>
                </div>
            </div>
            <p class="text-xs text-center mt-3 text-neutral-500">{conclusion}</p>
        """

    def _render_emotion_overview(self, sentiment_stats: dict) -> str:
        """Render emotion overview"""
        if not sentiment_stats:
            return '<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        normal = sentiment_stats.get("normal", 0)
        negative = sentiment_stats.get("negative", 0)
        total = normal + negative

        if total == 0:
            return '<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        normal_ratio = normal / total * 100 if total > 0 else 0
        negative_ratio = negative / total * 100 if total > 0 else 0

        return f"""
            <div class="emotion-grid" style="grid-template-columns: repeat(2, 1fr);">
                <div class="emotion-item normal">
                    <p class="text-lg font-bold" style="color: var(--accent-success);">{normal_ratio:.0f}%</p>
                    <p class="text-xs">{self.i18n.t("label_normal_positive")}</p>
                    <p class="font-mono text-xs text-neutral-500">{normal} {self.i18n.t("label_unit_suffix")}</p>
                </div>
                <div class="emotion-item negative">
                    <p class="text-lg font-bold" style="color: var(--accent-error);">{negative_ratio:.0f}%</p>
                    <p class="text-xs">{self.i18n.t("label_negative")}</p>
                    <p class="font-mono text-xs text-neutral-500">{negative} {self.i18n.t("label_unit_suffix")}</p>
                </div>
            </div>
        """

    def _render_usage_habits(self, habits: dict) -> str:
        """Render usage habits"""
        if not habits:
            return '<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        return f"""
            <div class="grid grid-cols-3 gap-4 text-center">
                <div>
                    <p class="data-value">{habits.get("consecutive_days", 0)}</p>
                    <p class="text-xs text-neutral-500">{self.i18n.t("label_consecutive_days")}</p>
                </div>
                <div>
                    <p class="data-value">{habits.get("active_days", 0)}</p>
                    <p class="text-xs text-neutral-500">{self.i18n.t("label_active_days")}</p>
                </div>
                <div>
                    <p class="data-value">{habits.get("gap_days", 0)}</p>
                    <p class="text-xs text-neutral-500">{self.i18n.t("label_gap_days")}</p>
                </div>
            </div>
        """

    def _render_extreme_comparison(self, habits: dict) -> str:
        """Render extreme comparison"""
        if not habits:
            return '<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        busiest_week = habits.get("busiest_week", 0)
        laziest_week = habits.get("laziest_week", 0)
        week_ratio = habits.get("week_ratio", 0)

        return f"""
            <div class="space-y-4">
                <div class="flex justify-between items-center">
                    <span class="text-sm">{self.i18n.t("label_busiest_week")}</span>
                    <span class="font-mono">{self.i18n.t("label_unit_suffix")} {busiest_week}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-sm">{self.i18n.t("label_laziest_week")}</span>
                    <span class="font-mono">{self.i18n.t("label_unit_suffix")} {laziest_week}</span>
                </div>
                <div class="flex justify-between items-center pt-2" style="border-top: 1px solid var(--border-subtle);">
                    <span class="text-sm">{self.i18n.t("label_gap_ratio")}</span>
                    <span class="font-mono" style="color: var(--accent-primary);">{week_ratio:.1f}x</span>
                </div>
            </div>
        """

    def _render_topic_classification(self, topic_dist: dict) -> str:
        """Render topic classification"""
        if not topic_dist:
            return '<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        daily = topic_dist.get("daily", 0)
        ai = topic_dist.get("ai", 0)
        design = topic_dist.get("design", 0)
        total = daily + ai + design

        if total == 0:
            return '<p class="text-neutral-500">{self.i18n.t("no_data")}</p>'

        return f"""
            <div class="topic-grid">
                <div class="topic-item daily">
                    <p class="text-sm">{self.i18n.t("topic_daily")}</p>
                    <p class="data-value">{daily}</p>
                    <p class="font-mono text-xs">{daily/total*100:.0f}%</p>
                </div>
                <div class="topic-item ai">
                    <p class="text-sm">{self.i18n.t("topic_ai")}</p>
                    <p class="data-value" style="color: var(--accent-blue);">{ai}</p>
                    <p class="font-mono text-xs">{ai/total*100:.0f}%</p>
                </div>
                <div class="topic-item design">
                    <p class="text-sm">{self.i18n.t("topic_design")}</p>
                    <p class="data-value" style="color: var(--accent-purple);">{design}</p>
                    <p class="font-mono text-xs">{design/total*100:.0f}%</p>
                </div>
            </div>
        """
        # Add CSS for topic-grid
        # Added to style section

    def _render_ai_insights(self, ai_insights: dict) -> str:
        """Render AI deep insights tab content as bento grid cards."""
        if not ai_insights:
            return (
                f'<div class="card bento-col-4"><div class="card-body">'
                f'<p class="text-neutral-500">{self.i18n.t("empty_no_data")}</p>'
                f'</div></div>'
            )

        sentiment_dist = ai_insights.get("sentiment_distribution", {})
        mental_health = ai_insights.get("mental_health_avg", {})
        topic_dist = ai_insights.get("topic_distribution", {})
        creative_moments = ai_insights.get("creative_moments", [])
        humor_entries = ai_insights.get("humor_entries", [])

        # Sentiment distribution (3 colored blocks)
        total = sum(sentiment_dist.values()) or 1
        pos = sentiment_dist.get("positive", 0)
        neu = sentiment_dist.get("neutral", 0)
        neg = sentiment_dist.get("negative", 0)
        sentiment_card = f"""
        <div class="card bento-col-2">
            <div class="card-header">
                <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("sentiment_distribution")}</h3>
            </div>
            <div class="card-body">
                <div class="emotion-grid" style="grid-template-columns: repeat(3, 1fr);">
                    <div class="emotion-item">
                        <p class="text-lg font-bold" style="color: var(--accent-success);">{pos / total * 100:.0f}%</p>
                        <p class="text-xs">{self.i18n.t("positive")}</p>
                        <p class="font-mono text-xs text-neutral-500">{pos}</p>
                    </div>
                    <div class="emotion-item">
                        <p class="text-lg font-bold">{neu / total * 100:.0f}%</p>
                        <p class="text-xs">{self.i18n.t("neutral")}</p>
                        <p class="font-mono text-xs text-neutral-500">{neu}</p>
                    </div>
                    <div class="emotion-item">
                        <p class="text-lg font-bold" style="color: var(--accent-error);">{neg / total * 100:.0f}%</p>
                        <p class="text-xs">{self.i18n.t("negative")}</p>
                        <p class="font-mono text-xs text-neutral-500">{neg}</p>
                    </div>
                </div>
            </div>
        </div>"""

        # Big Five radar chart
        big_five_card = f"""
        <div class="card bento-col-2">
            <div class="card-header">
                <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("personality_big_five")}</h3>
            </div>
            <div class="card-body">
                <div id="chart-bigfive-ai" class="chart-container" style="height: 220px;"></div>
            </div>
        </div>"""

        # Mental health avg cards
        avg_stress = mental_health.get("avg_stress", 0)
        avg_optimism = mental_health.get("avg_optimism", 0)
        mental_card = f"""
        <div class="card bento-col-2">
            <div class="card-header">
                <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("mental_health")}</h3>
            </div>
            <div class="card-body">
                <div class="grid grid-cols-2 gap-4 text-center">
                    <div>
                        <p class="data-value" style="color: var(--accent-warning);">{avg_stress:.2f}</p>
                        <p class="text-xs text-neutral-500">{self.i18n.t("avg_stress")}</p>
                    </div>
                    <div>
                        <p class="data-value" style="color: var(--accent-success);">{avg_optimism:.2f}</p>
                        <p class="text-xs text-neutral-500">{self.i18n.t("avg_optimism")}</p>
                    </div>
                </div>
            </div>
        </div>"""

        # Emotion triggers bar chart
        triggers_card = f"""
        <div class="card bento-col-2">
            <div class="card-header">
                <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("emotion_triggers")}</h3>
            </div>
            <div class="card-body">
                <div id="chart-triggers-ai" class="chart-container" style="height: 220px;"></div>
            </div>
        </div>"""

        # Topic distribution tags
        topic_items = "".join(
            f'<span class="word-tag" style="font-size: 0.75rem;">'
            f'{topic} <span class="font-mono text-neutral-500 text-xs">({count})</span></span>\n'
            for topic, count in list(topic_dist.items())[:15]
        )
        no_data = self.i18n.t("empty_no_data")
        topic_inner = topic_items if topic_items else f'<p class="text-neutral-500">{no_data}</p>'
        topic_card = f"""
        <div class="card bento-col-4">
            <div class="card-header">
                <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("topic_distribution")}</h3>
            </div>
            <div class="card-body">
                <div class="flex flex-wrap gap-2">
                    {topic_inner}
                </div>
            </div>
        </div>"""

        # Creative moments list
        creative_items = "".join(
            f'<div class="p-3 mb-2" style="border: 1px solid var(--border-subtle);">'
            f'<p class="font-mono text-xs text-neutral-500 mb-1">'
            f'{m.get("date", "")} · {m.get("novelty", "")}</p>'
            f'<p class="text-sm leading-relaxed">"{_html.escape(m.get("content", "")[:120])}"</p>'
            f'</div>\n'
            for m in creative_moments[:5]
        )
        creative_inner = (
            creative_items if creative_items else f'<p class="text-neutral-500">{no_data}</p>'
        )
        creative_card = f"""
        <div class="card bento-col-2">
            <div class="card-header">
                <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("creative_moments")}</h3>
            </div>
            <div class="card-body" style="max-height: 260px; overflow-y: auto;">
                {creative_inner}
            </div>
        </div>"""

        # Humor entries list
        humor_items = "".join(
            f'<div class="p-3 mb-2" style="border: 1px solid var(--border-subtle);">'
            f'<p class="font-mono text-xs text-neutral-500 mb-1">'
            f'{h.get("date", "")} · {h.get("type", "")}</p>'
            f'<p class="text-sm leading-relaxed">"{_html.escape(h.get("content", "")[:100])}"</p>'
            f'</div>\n'
            for h in humor_entries[:5]
        )
        humor_inner = humor_items if humor_items else f'<p class="text-neutral-500">{no_data}</p>'
        humor_card = f"""
        <div class="card bento-col-2">
            <div class="card-header">
                <h3 class="font-mono text-sm font-medium uppercase tracking-wider text-neutral-600">{self.i18n.t("humor_moments")}</h3>
            </div>
            <div class="card-body" style="max-height: 260px; overflow-y: auto;">
                {humor_inner}
            </div>
        </div>"""

        return (
            sentiment_card
            + big_five_card
            + mental_card
            + triggers_card
            + topic_card
            + creative_card
            + humor_card
        )
