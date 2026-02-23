"""
HTML Report Generator - Brutalist Style
========================================
Prepare analysis context and render via Jinja2 template.
"""

from pathlib import Path
from typing import Any

import jinja2

from src.translations import I18n

_TEMPLATES_DIR = Path(__file__).parent / "templates"
_TEMPLATE_NAME = "report.html.j2"

_MEDALS = ["🥇", "🥈", "🥉"]


def _score_color(score: float) -> str:
    if score >= 80:
        return "#00D26A"
    if score >= 60:
        return "#FFAB00"
    return "#FF4D4D"


def _rank_class(i: int) -> str:
    return ["gold", "silver", "bronze"][i] if i < 3 else ""


def _medal(i: int) -> str:
    return _MEDALS[i] if i < 3 else f"{i + 1}."


def _word_size_class(val: float, max_val: float) -> str:
    ratio = val / max_val if max_val else 0
    if ratio > 0.7:
        return "text-lg"
    if ratio > 0.4:
        return "text-base"
    if ratio > 0.2:
        return "text-sm"
    return "text-xs"


class BrutalistHTMLGenerator:
    """Brutalist style HTML report generator — Jinja2 template rendering."""

    def __init__(self, lang: str = "en") -> None:
        self.i18n = I18n(lang)
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(_TEMPLATES_DIR)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self, analysis_data: dict[str, Any], output_path: str) -> None:
        """Generate HTML report to output_path."""
        ctx = self._build_context(analysis_data)
        template = self._env.get_template(_TEMPLATE_NAME)
        html_content = template.render(**ctx)
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_content, encoding="utf-8")

    # ── context builder ────────────────────────────────────────────────────

    def _build_context(self, data: dict[str, Any]) -> dict[str, Any]:
        overview = data.get("overview", {})
        habits = data.get("usage_habits", {})
        sentiment = data.get("language_sentiment", {})
        trends = data.get("time_trends", {})
        content = data.get("content_deep_dive", {})
        personality = data.get("personality_profile", {}) or {}
        efficiency = data.get("efficiency_metrics", {}) or {}
        app_usage = data.get("app_usage", {}) or {}
        emotion_deep = data.get("emotion_deep", {}) or {}
        ai_insights = data.get("ai_insights", {}) or {}

        sentence_patterns = sentiment.get("sentence_patterns", {})
        sentiment_stats = sentiment.get("sentiment_stats", {})
        badge = overview.get("badge", {})
        topic_dist = content.get("topic_distribution", {})
        length_dist = content.get("sentence_length_distribution", {})
        longest_yap = content.get("longest_yap", {})
        word_cloud = sentiment.get("top_words", [])[:20]
        daily_trend = trends.get("daily_trend", {"dates": [], "counts": []})
        hour_dist = trends.get("hour_distribution", [0] * 24)

        # sentence conclusion
        q_ratio = sentence_patterns.get("question_ratio", 0)
        s_ratio = sentence_patterns.get("statement_ratio", 0)
        if q_ratio > 60:
            sentence_conclusion = self.i18n.t("conclusion_questioner")
        elif s_ratio > 60:
            sentence_conclusion = self.i18n.t("conclusion_commander")
        else:
            sentence_conclusion = self.i18n.t("conclusion_balanced")

        # normal ratio
        sentiment_total = sentiment_stats.get("normal", 0) + sentiment_stats.get("negative", 0)
        normal_ratio = (
            sentiment_stats.get("normal", 0) / sentiment_total * 100 if sentiment_total > 0 else 0
        )

        # AI insights sub-data
        ai_personality = ai_insights.get("personality_profile", {})
        ai_emotion_triggers = ai_insights.get("emotion_triggers", {})
        ai_sentiment_dist = ai_insights.get("sentiment_distribution", {})
        mental_health = ai_insights.get("mental_health_avg", {})
        ai_big_five = {
            "openness": ai_personality.get("openness", 0),
            "conscientiousness": ai_personality.get("conscientiousness", 0),
            "extraversion": ai_personality.get("extraversion", 0),
            "agreeableness": ai_personality.get("agreeableness", 0),
            "neuroticism": ai_personality.get("neuroticism", 0),
        }
        sorted_triggers = sorted(ai_emotion_triggers.items(), key=lambda x: -x[1])[:10]

        # Emotion trend
        emotion_trend = emotion_deep.get("daily_trend", [])
        emotion_trend_dates = [t.get("date", "") for t in emotion_trend]
        emotion_trend_scores = [t.get("avg_sentiment", 0) for t in emotion_trend]

        return {
            # i18n
            "t": self.i18n.t,
            "lang": self.i18n.lang,
            "html_lang": self.i18n.html_lang,
            # date range
            "start_date": overview.get("start_date", ""),
            "end_date": overview.get("end_date", ""),
            # overview metrics
            "total_records": overview.get("total_records", 0),
            "total_words": overview.get("total_words", 0),
            "total_duration": overview.get("total_duration", 0),
            "daily_avg": overview.get("daily_avg", 0),
            "avg_words": overview.get("avg_words", 0),
            "avg_duration": overview.get("avg_duration", 0),
            # badge
            "badge_icon": badge.get("icon", "📝"),
            "badge_name": badge.get("name", self.i18n.t("badge_default")),
            "badge_progress": badge.get("progress", 0),
            "badge_color": badge.get("color", "#9B9B9B"),
            "badge_threshold": badge.get("threshold", 10000),
            # sentence patterns
            "question_ratio": sentence_patterns.get("question_ratio", 0),
            "question_count": sentence_patterns.get("question_count", 0),
            "statement_ratio": sentence_patterns.get("statement_ratio", 0),
            "statement_count": sentence_patterns.get("statement_count", 0),
            "sentence_conclusion": sentence_conclusion,
            # emotion overview
            "normal_ratio": normal_ratio,
            "normal_count": sentiment_stats.get("normal", 0),
            "negative_ratio": sentiment_stats.get("negative_ratio", 0),
            "negative_count": sentiment_stats.get("negative", 0),
            # personality tags
            "personality_tags": self._prep_personality_tags(personality),
            # efficiency
            "eff_scores": self._prep_eff_scores(efficiency),
            "frag_level": efficiency.get("fragmentation", {}).get("level", ""),
            "frag_ratio": efficiency.get("fragmentation", {}).get("ratio", 0),
            "frag_desc": efficiency.get("fragmentation", {}).get("desc", ""),
            # word cloud
            "word_tags": self._prep_word_tags(word_cloud),
            # topic
            "topic_daily": topic_dist.get("daily", 0),
            "topic_ai": topic_dist.get("ai", 0),
            "topic_design": topic_dist.get("design", 0),
            "topic_total": topic_dist.get("daily", 0)
            + topic_dist.get("ai", 0)
            + topic_dist.get("design", 0),
            # longest yap
            "yap_date": longest_yap.get("date", ""),
            "yap_hour": longest_yap.get("hour", 0),
            "yap_duration": longest_yap.get("duration", 0),
            "yap_words": longest_yap.get("word_count", 0),
            "yap_content": longest_yap.get("content", ""),
            # emotion deep
            "emotion_cats": self._prep_emotion_cats(emotion_deep),
            "has_emotion_trend": bool(emotion_trend),
            # swear calendar
            **self._prep_swear(sentiment.get("swear_calendar", [])),
            # app usage
            **self._prep_apps(app_usage),
            # AI mental health
            "avg_stress": mental_health.get("avg_stress", 0),
            "avg_optimism": mental_health.get("avg_optimism", 0),
            # AI topics
            "ai_topics": [
                {"topic": t, "count": c}
                for t, c in list(ai_insights.get("topic_distribution", {}).items())[:15]
            ],
            # AI creative
            "ai_creative": [
                {
                    "date": m.get("date", ""),
                    "novelty": m.get("novelty", ""),
                    "content": m.get("content", "")[:120],
                }
                for m in ai_insights.get("creative_moments", [])[:5]
            ],
            # AI humor
            "ai_humor": [
                {
                    "date": h.get("date", ""),
                    "type": h.get("type", ""),
                    "content": h.get("content", "")[:100],
                }
                for h in ai_insights.get("humor_entries", [])[:5]
            ],
            # usage habits
            "consecutive_days": habits.get("consecutive_days", 0),
            "active_days": habits.get("active_days", 0),
            "gap_days": habits.get("gap_days", 0),
            "busiest_week": habits.get("busiest_week", 0),
            "laziest_week": habits.get("laziest_week", 0),
            "week_ratio": habits.get("week_ratio", 0),
            # top dates
            "top_dates": self._prep_top_dates(trends.get("top_dates", [])),
            # chart data (passed as JSON)
            "chart_data": {
                "hour_dist": hour_dist,
                "daily_trend": {
                    "dates": daily_trend.get("dates", []),
                    "counts": daily_trend.get("counts", []),
                },
                "length_dist": {
                    "short": length_dist.get("short", 0),
                    "medium": length_dist.get("medium", 0),
                    "long": length_dist.get("long", 0),
                },
                "emotion_trend": {
                    "dates": emotion_trend_dates,
                    "scores": emotion_trend_scores,
                },
                "ai_insights": {
                    "big_five": ai_big_five,
                    "triggers_labels": [k for k, _ in sorted_triggers],
                    "triggers_values": [v for _, v in sorted_triggers],
                    "sentiment": ai_sentiment_dist,
                },
                "i18n": {
                    "chart_short": self.i18n.t("chart_short"),
                    "chart_medium": self.i18n.t("chart_medium"),
                    "chart_long": self.i18n.t("chart_long"),
                    "btn_dark": self.i18n.t("btn_dark_mode"),
                    "btn_light": self.i18n.t("btn_light_mode"),
                    "big_five_labels": [
                        self.i18n.t("big_five_openness"),
                        self.i18n.t("big_five_conscient"),
                        self.i18n.t("big_five_extravers"),
                        self.i18n.t("big_five_agreeable"),
                        self.i18n.t("big_five_neurotic"),
                    ],
                },
            },
        }

    # ── data preparation helpers ───────────────────────────────────────────

    def _prep_personality_tags(self, personality: dict) -> list[dict]:
        return [
            {
                "name": tag.get("name", ""),
                "desc": tag.get("desc", ""),
                "color": tag.get("color", "#9B9B9B"),
            }
            for tag in personality.get("tags", [])
        ]

    def _prep_eff_scores(self, efficiency: dict) -> list[dict]:
        scores = efficiency.get("scores", {})
        if not scores:
            return []
        return [
            {
                "label_key": "score_sleep",
                "value": scores.get("sleep_health", 0),
                "color": _score_color(scores.get("sleep_health", 0)),
            },
            {
                "label_key": "score_efficiency",
                "value": scores.get("work_efficiency", 0),
                "color": _score_color(scores.get("work_efficiency", 0)),
            },
            {
                "label_key": "score_focus",
                "value": scores.get("focus", 0),
                "color": _score_color(scores.get("focus", 0)),
            },
            {
                "label_key": "score_overall",
                "value": scores.get("overall", 0),
                "color": _score_color(scores.get("overall", 0)),
            },
        ]

    def _prep_word_tags(self, items: list[dict]) -> list[dict]:
        if not items:
            return []
        max_val = max((item.get("value", 0) for item in items), default=1) or 1
        return [
            {
                "name": item.get("name", ""),
                "count": item.get("value", 0),
                "size_class": _word_size_class(item.get("value", 0), max_val),
                "highlight": i < 3,
            }
            for i, item in enumerate(items)
        ]

    def _prep_emotion_cats(self, emotion_deep: dict) -> list[dict]:
        if not emotion_deep:
            return []
        categories = emotion_deep.get("categories", {})
        if not categories:
            return []

        cat_meta = {
            "anger": (self.i18n.t("emotion_anger"), "#FF4D4D"),
            "anxiety": (self.i18n.t("emotion_anxiety"), "#FFAB00"),
            "sadness": (self.i18n.t("emotion_sadness"), "#6FC2FF"),
            "fatigue": (self.i18n.t("emotion_fatigue"), "#9B9B9B"),
            "stress": (self.i18n.t("emotion_stress"), "#A855F7"),
        }
        result = []
        for key in ["anger", "anxiety", "sadness", "fatigue", "stress"]:
            cat_data = categories.get(key)
            if cat_data is None:
                continue
            label, color = cat_meta[key]
            records = [
                {
                    "date_str": f"{r.get('date', '')} {r.get('hour', 0):02d}:00",
                    "score": r.get("sentiment_score", 0),
                    "words": r.get("word_count", 0),
                    "content": r.get("content", ""),
                }
                for r in cat_data.get("records", [])[:50]
            ]
            result.append(
                {
                    "key": key,
                    "label": label,
                    "color": color,
                    "count": cat_data.get("count", 0),
                    "ratio": cat_data.get("ratio", 0),
                    "records": records,
                }
            )
        return result

    def _prep_swear(self, swear_list: list[dict]) -> dict:
        word_label = self.i18n.t("word_count_label")
        items = [
            {
                "date_str": f"{item.get('date', '')} {item.get('hour', 0):02d}",
                "extra_text": f"{word_label}\u00a0{item.get('word_count', '')}",
                "content": item.get("content", ""),
            }
            for item in swear_list
        ]
        return {
            "swear_items": items,
            "has_swear": bool(items),
            "swear_col_datetime": self.i18n.t("swear_col_datetime"),
            "swear_col_extra": self.i18n.t("swear_col_extra"),
            "swear_col_content": self.i18n.t("swear_col_content"),
        }

    def _prep_apps(self, app_usage: dict) -> dict:
        if not app_usage.get("has_data", False):
            return {
                "app_items": [],
                "has_app_data": False,
                "app_col_app": self.i18n.t("app_col_app"),
                "app_col_count": self.i18n.t("app_col_count"),
            }
        apps = app_usage.get("apps", [])[:5]
        items = [
            {
                "medal": _medal(i),
                "name": app.get("app_name", ""),
                "ratio": app.get("ratio", 0),
                "count": app.get("count", 0),
            }
            for i, app in enumerate(apps)
        ]
        return {
            "app_items": items,
            "has_app_data": bool(items),
            "app_col_app": self.i18n.t("app_col_app"),
            "app_col_count": self.i18n.t("app_col_count"),
        }

    def _prep_top_dates(self, top_dates: list[dict]) -> list[dict]:
        if not top_dates:
            return []
        max_count = max((d.get("count", 0) for d in top_dates), default=1) or 1
        return [
            {
                "medal": _medal(i),
                "rank_class": _rank_class(i),
                "date": d.get("date", ""),
                "count": d.get("count", 0),
                "bar_width": round(d.get("count", 0) / max_count * 100, 1),
            }
            for i, d in enumerate(top_dates[:5])
        ]
