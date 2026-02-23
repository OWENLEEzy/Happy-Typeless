ANALYSIS_PROMPT = """You are a professional voice transcription analyst. Analyze the following voice content and return structured JSON data.

Voice content:
{content}

Recording time: {time}
Date: {date}
App in use: {app}

Return ONLY the following JSON (no other text):

{{
  "sentiment": {{"score": -1.0 to 1.0, "label": "positive|neutral|negative", "confidence": 0 to 1}},
  "intent": {{"primary": "question|statement|command|request|expression|complaint|gratitude", "secondary": [], "urgency": "immediate|normal|low"}},
  "emotion": {{"primary": "joy|anger|sadness|fear|surprise|disgust|neutral", "intensity": 0 to 1, "mixed": false}},
  "topics": ["topic1", "topic2"],
  "communication_style": {{"directness": 0 to 1, "formality": 0 to 1, "assertiveness": 0 to 1}},
  "personality": {{
    "big_five": {{"openness": 0 to 1, "conscientiousness": 0 to 1, "extraversion": 0 to 1, "agreeableness": 0 to 1, "neuroticism": 0 to 1}},
    "thinking_style": "analytical|intuitive|creative|practical",
    "problem_style": "systematic|intuitive|collaborative|independent"
  }},
  "mental_health": {{"stress_level": 0 to 1, "burnout_risk": "low|medium|high", "anxiety_pattern": "improving|stable|worsening", "optimism_score": 0 to 1, "rumination_score": 0 to 1}},
  "content_flags": {{"has_goal": false, "has_decision": false, "has_complaint": false, "has_gratitude": false, "has_plan": false, "has_action_item": false, "is_profound": false}},
  "profanity": {{"has_profanity": false, "severity": null, "trigger_category": null}},
  "complexity": {{"overall": 0 to 1, "syntactic": 0 to 1, "lexical_diversity": 0 to 1, "readability": "simple|medium|complex|academic"}},
  "entities": {{"people": [], "places": [], "organizations": [], "dates": [], "numbers": []}},
  "speech_patterns": {{"fluency": 0 to 1, "hesitation_count": 0, "self_correction_count": 0, "repetition_count": 0, "pace": "slow|normal|fast|variable"}},
  "social_indicators": {{"pronoun_ratio": {{"i": 0.5}}, "gratitude_complaint_ratio": 0 to 1, "social_focus": "individual|collaborative|observational"}},
  "cognitive_distortions": {{"absolutist_language": false, "catastrophizing": false, "overgeneralization": false}},
  "question_depth": null,
  "temporal_context": {{"circadian_phase": "active|rest|transition", "fatigue_indicator": "low|medium|high", "energy_level": 0 to 1}},
  "language_mixing": {{"dominant": "zh|en|mixed", "code_switch_count": 0, "en_ratio": 0 to 1}},
  "creative_signal": {{"is_brainstorm": false, "idea_density": 0 to 1, "novelty": "routine|variation|breakthrough"}},
  "emotion_trigger": null,
  "commitment_strength": null,
  "humor": {{"detected": false, "type": null}},
  "time_perception": {{"urgency": "urgent|normal|relaxed", "references_past": false, "references_future": false}}
}}
"""


def build_prompt(content: str, timestamp: int, app_name: str | None = None) -> str:
    """Build analysis prompt from transcription data."""
    from datetime import UTC, datetime

    dt = datetime.fromtimestamp(timestamp, tz=UTC).astimezone()
    truncated = content[:2000] if len(content) > 2000 else content  # ~1000 tokens for Chinese
    return ANALYSIS_PROMPT.format(
        content=truncated,
        time=dt.strftime("%H:%M"),
        date=dt.strftime("%Y-%m-%d"),
        app=app_name or "Unknown",
    )
