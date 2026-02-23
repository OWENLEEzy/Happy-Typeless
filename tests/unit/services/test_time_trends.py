import time

from src.models.transcription import Transcription, TranscriptionList
from src.services.time_trends import TimeTrendsService


def test_daily_trend_fills_empty_days():
    """30-day trend should include all 30 days even if most have no data (count=0)."""
    now = int(time.time())
    transcriptions = TranscriptionList(
        items=[Transcription(id="id1", timestamp=now, content="test")]
    )
    service = TimeTrendsService(transcriptions)
    trends = service.get_trends()

    dates = trends.daily_trend["dates"]
    counts = trends.daily_trend["counts"]
    assert len(dates) == 30
    assert len(counts) == 30
