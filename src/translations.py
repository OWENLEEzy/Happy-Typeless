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
        "tab_overview_profile": "概览与画像",
        "tab_content_communication": "内容与沟通",
        "tab_time_habits": "时间与习惯",
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
        "badge_keyboard_terminator": "键盘终结者",
        "badge_chatterbox": "话痨本痨",
        "badge_human_typewriter": "人形打字机",
        "badge_socrates": "当代苏格拉底",
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
        "section_fragmentation": "🧩 碎片化分析",
        "section_peak_hours": "⏰ 高峰时段",
        "peak_hours_label": "最活跃时段",
        "fragmentation_high": "高",
        "fragmentation_high_desc": "注意力高度碎片化",
        "fragmentation_medium": "中",
        "fragmentation_medium_desc": "正常范围",
        "fragmentation_low": "低",
        "fragmentation_low_desc": "思考有深度",
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
        "label_negative": "负面情绪",
        # Section 9: App Usage
        "section_app_usage": "📱 App 使用统计",
        "no_app_data": "数据中无 app_name 字段",
        "no_data": "暂无数据",
        # Section 10: Emotion Deep Analysis
        "section_emotion_deep": "😔 情绪深度分析",
        "section_emotion_trend": "📈 每日情绪趋势",
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
        "emotion_triggers": "情绪触发原因",
        "action_items": "行动承诺",
        "humor_moments": "幽默时刻",
        # Feature: Content Flags
        "section_content_flags": "📌 你在说什么",
        "flag_has_goal": "🎯 定了目标",
        "flag_has_decision": "✅ 做了决定",
        "flag_has_complaint": "💢 发了牢骚",
        "flag_has_gratitude": "🙏 表达感谢",
        "flag_has_plan": "📋 制定计划",
        "flag_has_action_item": "⚡ 含行动项",
        "flag_is_profound": "💡 深刻洞见",
        # Feature: Action Items
        "section_action_items": "🎯 行动承诺追踪",
        "commitment_committed": "已承诺",
        "commitment_intended": "有意向",
        "commitment_vague": "模糊提及",
        "action_items_empty": "暂无检测到行动承诺",
        # Feature: Hourly Sentiment Overlay
        "sentiment_score_label": "情绪得分",
        # Misc labels
        "word_count_label": "字数",
        # New tabs
        "tab_communication": "沟通风格",
        "tab_mental_wellness": "心理健康",
        "tab_intent_social": "意图与社交",
        # Communication tab
        "communication_radar": "沟通风格雷达",
        "speech_quality": "语音质量",
        "social_indicators": "社交指标",
        "directness": "直接性",
        "formality": "正式度",
        "assertiveness": "自信度",
        "fluency": "流利度",
        "hesitation_count": "犹豫次数",
        "pace_distribution": "语速分布",
        "pronoun_ratio": "代词比例",
        "social_focus": "社交关注",
        # Mental Wellness tab
        "mental_health_trends": "心理健康趋势",
        "sentiment_timeline": "情绪时间线",
        "cognitive_distortions": "认知扭曲",
        "absolutist_language": "绝对化语言",
        "catastrophizing": "灾难化思维",
        "overgeneralization": "过度概括",
        # Content Deep tab
        "entity_network": "实体网络",
        "question_depth": "问题深度",
        "complexity_metrics": "复杂度指标",
        "word_categories": "词汇分类",
        "phrase_tags": "高频短语",
        "rhetorical_count": "反问数量",
        "open_count": "开放性问题",
        "complex_count": "复杂问题",
        "avg_chain_depth": "平均追问深度",
        # Time Patterns tab
        "language_mixing": "语言混合",
        "time_perception": "时间感知",
        "temporal_context": "时间上下文",
        "creative_signal": "创意信号",
        "code_switch_count": "语码切换次数",
        "english_ratio": "英文比例",
        "urgency_distribution": "紧急度分布",
        "past_ref_count": "提及过去",
        "future_ref_count": "提及未来",
        "hourly_energy": "每小时能量",
        "fatigue_distribution": "疲劳分布",
        "idea_density": "想法密度",
        # Intent & Social tab
        "intent_distribution": "意图分布",
        "commitment_strength": "承诺强度",
        "urgency_patterns": "紧急度模式",
        # Word categories
        "word_cat_filler": "填充词",
        "word_cat_connector": "连接词",
        "word_cat_content": "实词",
        # Swear table column headers
        "swear_col_datetime": "时间",
        "swear_col_extra": "字数",
        "swear_col_content": "内容",
        # App table column headers
        "app_col_app": "应用",
        "app_col_count": "次数",
        # Topic category labels
        "topic_label_daily": "日常/其他",
        "topic_label_ai": "AI/技术",
        "topic_label_design": "设计/创作",
        # Big Five personality dimensions
        "big_five_openness": "开放性",
        "big_five_conscient": "尽责性",
        "big_five_extravers": "外向性",
        "big_five_agreeable": "亲和性",
        "big_five_neurotic": "神经质",
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
        "tab_overview_profile": "Overview & Profile",
        "tab_content_communication": "Content & Communication",
        "tab_time_habits": "Time & Habits",
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
        "badge_keyboard_terminator": "Keyboard Terminator",
        "badge_chatterbox": "Chatterbox",
        "badge_human_typewriter": "Human Typewriter",
        "badge_socrates": "Modern Socrates",
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
        "section_fragmentation": "🧩 Fragmentation Analysis",
        "section_peak_hours": "⏰ Peak Hours",
        "peak_hours_label": "Most Active Hours",
        "fragmentation_high": "High",
        "fragmentation_high_desc": "Highly fragmented attention",
        "fragmentation_medium": "Medium",
        "fragmentation_medium_desc": "Normal range",
        "fragmentation_low": "Low",
        "fragmentation_low_desc": "Deep thinking",
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
        "label_negative": "Negative",
        # Section 9: App Usage
        "section_app_usage": "📱 App Usage Stats",
        "no_app_data": "No app_name field in data",
        "no_data": "No data available",
        # Section 10: Emotion Deep Analysis
        "section_emotion_deep": "😔 Emotion Deep Dive",
        "section_emotion_trend": "📈 Daily Sentiment Trend",
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
        "emotion_triggers": "Emotion Triggers",
        "action_items": "Action Items",
        "humor_moments": "Humor Moments",
        # Feature: Content Flags
        "section_content_flags": "📌 What You Talk About",
        "flag_has_goal": "🎯 Set Goal",
        "flag_has_decision": "✅ Made Decision",
        "flag_has_complaint": "💢 Complained",
        "flag_has_gratitude": "🙏 Gratitude",
        "flag_has_plan": "📋 Made Plan",
        "flag_has_action_item": "⚡ Action Item",
        "flag_is_profound": "💡 Profound",
        # Feature: Action Items
        "section_action_items": "🎯 Action Item Tracker",
        "commitment_committed": "Committed",
        "commitment_intended": "Intended",
        "commitment_vague": "Vague",
        "action_items_empty": "No action items detected",
        # Feature: Hourly Sentiment Overlay
        "sentiment_score_label": "Sentiment",
        # Misc labels
        "word_count_label": "words",
        # New tabs
        "tab_communication": "Communication",
        "tab_mental_wellness": "Mental Wellness",
        "tab_intent_social": "Intent & Social",
        # Communication tab
        "communication_radar": "Communication Style Radar",
        "speech_quality": "Speech Quality",
        "social_indicators": "Social Indicators",
        "directness": "Directness",
        "formality": "Formality",
        "assertiveness": "Assertiveness",
        "fluency": "Fluency",
        "hesitation_count": "Hesitation Count",
        "pace_distribution": "Pace Distribution",
        "pronoun_ratio": "Pronoun Ratio",
        "social_focus": "Social Focus",
        # Mental Wellness tab
        "mental_health_trends": "Mental Health Trends",
        "sentiment_timeline": "Sentiment Timeline",
        "cognitive_distortions": "Cognitive Distortions",
        "absolutist_language": "Absolutist Language",
        "catastrophizing": "Catastrophizing",
        "overgeneralization": "Overgeneralization",
        # Content Deep tab
        "entity_network": "Entity Network",
        "question_depth": "Question Depth",
        "complexity_metrics": "Complexity Metrics",
        "word_categories": "Word Categories",
        "phrase_tags": "Top Phrases",
        "rhetorical_count": "Rhetorical Questions",
        "open_count": "Open Questions",
        "complex_count": "Complex Questions",
        "avg_chain_depth": "Avg Chain Depth",
        # Time Patterns tab
        "language_mixing": "Language Mixing",
        "time_perception": "Time Perception",
        "temporal_context": "Temporal Context",
        "creative_signal": "Creative Signal",
        "code_switch_count": "Code-Switch Count",
        "english_ratio": "English Ratio",
        "urgency_distribution": "Urgency Distribution",
        "past_ref_count": "Past References",
        "future_ref_count": "Future References",
        "hourly_energy": "Hourly Energy",
        "fatigue_distribution": "Fatigue Distribution",
        "idea_density": "Idea Density",
        # Intent & Social tab
        "intent_distribution": "Intent Distribution",
        "commitment_strength": "Commitment Strength",
        "urgency_patterns": "Urgency Patterns",
        # Word categories
        "word_cat_filler": "Filler Words",
        "word_cat_connector": "Connectors",
        "word_cat_content": "Content Words",
        # Swear table column headers
        "swear_col_datetime": "DATETIME",
        "swear_col_extra": "WORDS",
        "swear_col_content": "CONTENT",
        # App table column headers
        "app_col_app": "APP",
        "app_col_count": "COUNT",
        # Topic category labels
        "topic_label_daily": "Daily/Other",
        "topic_label_ai": "AI/Tech",
        "topic_label_design": "Design",
        # Big Five personality dimensions
        "big_five_openness": "Openness",
        "big_five_conscient": "Conscient.",
        "big_five_extravers": "Extravers.",
        "big_five_agreeable": "Agreeable.",
        "big_five_neurotic": "Neurotic.",
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
