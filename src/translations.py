# src/translations.py
"""Internationalization (i18n) module for HTML report generation."""

import logging

# Translation dictionaries
TRANSLATIONS: dict[str, dict[str, str]] = {
    "zh": {
        # Page metadata
        "html_title": "Typeless Analytics - 语音数据报告",
        "html_lang": "zh-CN",
        # Header
        "report_header": "语音数据分析报告",
        "report_subtitle": "口喷成果分析",
        "data_range_label": "数据范围",
        "to": "至",
        # Navigation
        "brand_name": "Typeless Analytics",
        "btn_dark_mode": "🌙 深色模式",
        "btn_light_mode": "☀️ 浅色模式",
        "tab_overview": "概览",
        "tab_personality": "风格画像",
        "tab_time": "时间趋势",
        "tab_content": "内容分析",
        # Section 1: Overview Cards
        "card_total_records": "总语音条数",
        "card_total_words": "总输出字数",
        "card_total_duration": "总语音时长",
        "card_daily_avg": "日均使用次数",
        "card_avg_words": "平均每条字数",
        "card_avg_duration": "平均每条时长",
        "unit_minutes": "分钟",
        "unit_seconds": "秒",
        # Badge
        "badge_default": "奋笔疾书",
        "badge_progress": "字",
        # Section 2: Personality Profile
        "section_personality": "🎭 语言风格画像",
        "tag_concise": "简洁派",
        "tag_concise_desc": "说话干脆利落",
        "tag_verbose": "絮叨派",
        "tag_verbose_desc": "喜欢详细表达",
        "tag_moderate": "适中派",
        "tag_moderate_desc": "表达平衡",
        "tag_questioner": "提问者",
        "tag_questioner_desc": "{}在提问",
        "tag_commander": "下命令者",
        "tag_commander_desc": "倾向陈述",
        "tag_balanced": "平衡者",
        "tag_balanced_desc": "问答均衡",
        "tag_stable": "情绪稳定",
        "tag_stable_desc": "负面仅{}%",
        "tag_emotional": "情绪化",
        "tag_emotional_desc": "负面{}%",
        "tag_normal_emotion": "情绪正常",
        "tag_normal_emotion_desc": "情绪波动适中",
        "tag_workaholic": "工作狂",
        "tag_workaholic_desc": "工作日说话多",
        "tag_lifestyle": "生活家",
        "tag_lifestyle_desc": "周末说话多",
        "tag_balance_schedule": "平衡作息",
        "tag_balance_schedule_desc": "工作生活平衡",
        # Section 3: Efficiency Metrics
        "section_efficiency": "⚡ 效率评分",
        "score_sleep": "作息",
        "score_efficiency": "效率",
        "score_focus": "专注",
        "score_overall": "综合",
        "fragmentation_title": "碎片化指数",
        "fragmentation_high": "高",
        "fragmentation_high_desc": "注意力高度碎片化",
        "fragmentation_medium": "中",
        "fragmentation_medium_desc": "正常范围",
        "fragmentation_low": "低",
        "fragmentation_low_desc": "思考有深度",
        # Section 4: Word Categories
        "section_word_categories": "📝 口头禅分类",
        "cat_filler": "语气词",
        "cat_connector": "连接词",
        "cat_content": "实词",
        # Section 5: Usage Habits
        "section_usage_habits": "使用习惯",
        "label_consecutive_days": "最长连续(天)",
        "label_active_days": "活跃天数",
        "label_gap_days": "断档天数",
        # Section 6: Extreme Comparison
        "section_extreme_comparison": "极值对比",
        "label_busiest_week": "最勤奋一周",
        "label_laziest_week": "最慵懒一周",
        "label_gap_ratio": "差距倍数",
        # Section 7: Sentence Patterns
        "section_sentence_patterns": "句式倾向",
        "label_question": "问句",
        "label_statement": "陈述句",
        "label_unit_suffix": "条",
        "conclusion_commander": "💡 结论：你主要是在「下指令」，而不是「提问」",
        "conclusion_questioner": "💡 结论：你更倾向于「提问」而非「下指令」",
        "conclusion_balanced": "💡 结论：你提问与陈述并重",
        # Section 8: Emotion Overview
        "section_emotion_overview": "情绪大盘",
        "label_normal_positive": "正常/积极",
        "label_swear": "含脏话",
        "label_negative": "负面情绪",
        "negative_hint": "错误、不行、烦",
        # Section 9: App Usage
        "section_app_usage": "📱 App 使用统计",
        "no_app_data": "数据中无 app_name 字段",
        "no_data": "暂无数据",
        # Section 10: Emotion Deep Analysis
        "section_emotion_deep": "😔 情绪深度分析",
        "section_emotion_trend": "📈 每日情绪趋势",
        "chart_emotion_trend_title": "每日情绪得分 (负值=负面)",
        "chart_emotion_negative_ratio": "负面情绪占比 (%)",
        "emotion_anger": "愤怒",
        "emotion_anxiety": "焦虑",
        "emotion_sadness": "悲伤",
        "emotion_fatigue": "疲惫",
        "emotion_stress": "压力",
        # Section 11: Swear Calendar
        "section_swear_calendar": "⚠️ 脏话日历",
        "no_swear_data": "🎉 最近情绪稳定，没有检测到粗口",
        # Section 12: Time Trends
        "section_30day_trend": "最近 30 天使用趋势",
        "section_24hour_dist": "24 小时使用分布",
        "section_top_dates": "劳模榜单 Top 5",
        # Section 13: Content Analysis
        "section_topic_classification": "内容主题分类",
        "topic_daily": "日常/其他",
        "topic_ai": "AI技术",
        "topic_design": "设计/创作",
        "section_word_cloud": "高频词汇 Top 20",
        "section_length_distribution": "内容长度分布",
        "section_longest_yap": "🎙️ 最长的一条语音",
        "meta_date": "📅",
        "meta_hour": "⏰",
        "meta_duration": "🎙️",
        "meta_seconds": "秒",
        "meta_words": "📝",
        "meta_words_unit": "字",
        # Chart labels
        "chart_short": "短句≤20字",
        "chart_medium": "中等21-100字",
        "chart_long": "长句>100字",
        # Footer
        "footer_generated": "Generated by Typeless Analytics",
        # Empty states
        "empty_no_data": "暂无数据",
        # Personality tags (additional variants)
        "tag_concise_alt": "干脆利落",
        "tag_verbose_alt": "详细表达",
        "tag_commander_alt": "倾向陈述",
        "tag_balanced_alt": "问答均衡",
        "tag_normal_emotion_alt": "情绪波动适中",
        # Fragmentation levels
        "fragmentation_empty": "无数据",
        # AI Insights
        "ai_insights": "AI 深度洞察",
        "sentiment_distribution": "情绪分布",
        "positive": "正面",
        "neutral": "中性",
        "personality_big_five": "大五人格画像",
        "mental_health": "心理健康指标",
        "avg_stress": "平均压力",
        "avg_optimism": "乐观指数",
        "topic_distribution": "话题分布",
        "creative_moments": "灵感时刻",
        "language_mixing": "语言混用",
        "emotion_triggers": "情绪触发原因",
        "action_items": "行动承诺",
        "humor_moments": "幽默时刻",
        "profanity_severity": "情绪崩溃记录",
    },
    "en": {
        # Page metadata
        "html_title": "Typeless Analytics - Voice Data Report",
        "html_lang": "en",
        # Header
        "report_header": "Voice Data Analytics Report",
        "report_subtitle": "Speaking Pattern Analysis",
        "data_range_label": "Data Range",
        "to": "to",
        # Navigation
        "brand_name": "Typeless Analytics",
        "btn_dark_mode": "🌙 Dark Mode",
        "btn_light_mode": "☀️ Light Mode",
        "tab_overview": "Overview",
        "tab_personality": "Personality",
        "tab_time": "Time Trends",
        "tab_content": "Content",
        # Section 1: Overview Cards
        "card_total_records": "Total Records",
        "card_total_words": "Total Words",
        "card_total_duration": "Total Duration",
        "card_daily_avg": "Daily Avg",
        "card_avg_words": "Avg Words",
        "card_avg_duration": "Avg Duration",
        "unit_minutes": "min",
        "unit_seconds": "sec",
        # Badge
        "badge_default": "Prolific Writer",
        "badge_progress": "words",
        # Section 2: Personality Profile
        "section_personality": "🎭 Language Style Profile",
        "tag_concise": "Concise",
        "tag_concise_desc": "Straight to the point",
        "tag_verbose": "Verbose",
        "tag_verbose_desc": "Likes detailed expression",
        "tag_moderate": "Moderate",
        "tag_moderate_desc": "Balanced expression",
        "tag_questioner": "Questioner",
        "tag_questioner_desc": "{} asking questions",
        "tag_commander": "Commander",
        "tag_commander_desc": "Tends to state",
        "tag_balanced": "Balanced",
        "tag_balanced_desc": "Q&A balanced",
        "tag_stable": "Emotionally Stable",
        "tag_stable_desc": "Only {}% negative",
        "tag_emotional": "Emotional",
        "tag_emotional_desc": "{}% negative",
        "tag_normal_emotion": "Normal Emotion",
        "tag_normal_emotion_desc": "Moderate mood swings",
        "tag_workaholic": "Workaholic",
        "tag_workaholic_desc": "Talks more on workdays",
        "tag_lifestyle": "Lifestyle Oriented",
        "tag_lifestyle_desc": "Talks more on weekends",
        "tag_balance_schedule": "Balanced Schedule",
        "tag_balance_schedule_desc": "Work-life balance",
        # Section 3: Efficiency Metrics
        "section_efficiency": "⚡ Efficiency Score",
        "score_sleep": "Sleep",
        "score_efficiency": "Efficiency",
        "score_focus": "Focus",
        "score_overall": "Overall",
        "fragmentation_title": "Fragmentation Index",
        "fragmentation_high": "High",
        "fragmentation_high_desc": "Highly fragmented attention",
        "fragmentation_medium": "Medium",
        "fragmentation_medium_desc": "Normal range",
        "fragmentation_low": "Low",
        "fragmentation_low_desc": "Deep thinking",
        # Section 4: Word Categories
        "section_word_categories": "📝 Word Categories",
        "cat_filler": "Filler",
        "cat_connector": "Connector",
        "cat_content": "Content",
        # Section 5: Usage Habits
        "section_usage_habits": "Usage Habits",
        "label_consecutive_days": "Longest Streak (days)",
        "label_active_days": "Active Days",
        "label_gap_days": "Gap Days",
        # Section 6: Extreme Comparison
        "section_extreme_comparison": "Extreme Comparison",
        "label_busiest_week": "Busiest Week",
        "label_laziest_week": "Laziest Week",
        "label_gap_ratio": "Gap Ratio",
        # Section 7: Sentence Patterns
        "section_sentence_patterns": "Sentence Patterns",
        "label_question": "Questions",
        "label_statement": "Statements",
        "label_unit_suffix": "items",
        "conclusion_commander": '💡 Conclusion: You tend to "give commands" rather than "ask questions"',
        "conclusion_questioner": '💡 Conclusion: You prefer "asking questions" over "giving commands"',
        "conclusion_balanced": "💡 Conclusion: You balance questions and statements equally",
        # Section 8: Emotion Overview
        "section_emotion_overview": "Emotion Overview",
        "label_normal_positive": "Normal/Positive",
        "label_swear": "Profanity",
        "label_negative": "Negative",
        "negative_hint": "Errors, no, annoying",
        # Section 9: App Usage
        "section_app_usage": "📱 App Usage Stats",
        "no_app_data": "No app_name field in data",
        "no_data": "No data available",
        # Section 10: Emotion Deep Analysis
        "section_emotion_deep": "😔 Emotion Deep Dive",
        "section_emotion_trend": "📈 Daily Sentiment Trend",
        "chart_emotion_trend_title": "Daily Sentiment Score (Negative = Bad Mood)",
        "chart_emotion_negative_ratio": "Negative Emotion Ratio (%)",
        "emotion_anger": "Anger",
        "emotion_anxiety": "Anxiety",
        "emotion_sadness": "Sadness",
        "emotion_fatigue": "Fatigue",
        "emotion_stress": "Stress",
        # Section 11: Swear Calendar
        "section_swear_calendar": "⚠️ Profanity Calendar",
        "no_swear_data": "🎉 Emotionally stable lately, no profanity detected",
        # Section 12: Time Trends
        "section_30day_trend": "Last 30 Days Trend",
        "section_24hour_dist": "24-Hour Distribution",
        "section_top_dates": "Top 5 Dates",
        # Section 13: Content Analysis
        "section_topic_classification": "Content Topic Classification",
        "topic_daily": "Daily/Other",
        "topic_ai": "AI Tech",
        "topic_design": "Design/Creative",
        "section_word_cloud": "Top 20 High-Frequency Words",
        "section_length_distribution": "Content Length Distribution",
        "section_longest_yap": "🎙️ Longest Voice Recording",
        "meta_date": "📅",
        "meta_hour": "⏰",
        "meta_duration": "🎙️",
        "meta_seconds": "sec",
        "meta_words": "📝",
        "meta_words_unit": "words",
        # Chart labels
        "chart_short": "Short ≤20",
        "chart_medium": "Medium 21-100",
        "chart_long": "Long >100",
        # Footer
        "footer_generated": "Generated by Typeless Analytics",
        # Empty states
        "empty_no_data": "No data available",
        # Personality tags (additional variants)
        "tag_concise_alt": "Straight to the point",
        "tag_verbose_alt": "Detailed expression",
        "tag_commander_alt": "Tends to state",
        "tag_balanced_alt": "Q&A balanced",
        "tag_normal_emotion_alt": "Moderate mood swings",
        # Fragmentation levels
        "fragmentation_empty": "No data",
        # AI Insights
        "ai_insights": "AI Deep Insights",
        "sentiment_distribution": "Sentiment Distribution",
        "positive": "Positive",
        "neutral": "Neutral",
        "personality_big_five": "Big Five Personality",
        "mental_health": "Mental Health Indicators",
        "avg_stress": "Avg Stress",
        "avg_optimism": "Optimism Score",
        "topic_distribution": "Topic Distribution",
        "creative_moments": "Creative Moments",
        "language_mixing": "Language Mixing",
        "emotion_triggers": "Emotion Triggers",
        "action_items": "Action Items",
        "humor_moments": "Humor Moments",
        "profanity_severity": "Emotional Crash Log",
    },
}


class I18n:
    """Internationalization helper class for HTMLGenerator."""

    def __init__(self, lang: str = "en"):
        """Initialize i18n helper.

        Args:
            lang: Language code ('zh' or 'en'), default 'en'
        """
        self.lang = lang if lang in TRANSLATIONS else "en"
        self._translations = TRANSLATIONS[self.lang]
        self._logger = logging.getLogger(__name__)

    def t(self, key: str, *args, **kwargs) -> str:
        """Get translated text.

        Args:
            key: Translation key
            *args: Format arguments
            **kwargs: Format keyword arguments

        Returns:
            Translated text
        """
        text = self._translations.get(key, key)
        if args:
            try:
                return text.format(*args)
            except (IndexError, KeyError) as e:
                self._logger.debug(f"Translation format error: key={key}, args={args}, error={e}")
                return text
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError as e:
                self._logger.debug(
                    f"Translation format error: key={key}, kwargs={kwargs}, error={e}"
                )
                return text
        return text

    @property
    def html_lang(self) -> str:
        """Get HTML lang attribute value."""
        return self._translations.get("html_lang", "en")

    @property
    def is_chinese(self) -> bool:
        """Check if current language is Chinese."""
        return self.lang == "zh"
