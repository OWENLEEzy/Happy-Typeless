# src/models/transcription.py
from collections.abc import Iterator
from datetime import UTC, datetime

from pydantic import BaseModel, field_validator


class Transcription(BaseModel):
    """Single voice transcription record"""

    id: str
    timestamp: int
    content: str
    duration: float | None = None  # in seconds
    app_name: str | None = None
    window_title: str | None = None

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, v) -> int:
        if not isinstance(v, int) or v < 0:
            raise ValueError("timestamp must be a positive integer")
        return v

    @property
    def datetime(self) -> datetime:
        """Convert UNIX timestamp to datetime (UTC)"""
        return datetime.fromtimestamp(self.timestamp, tz=UTC)

    @property
    def date(self) -> str:
        """Get date in YYYY-MM-DD format"""
        return self.datetime.strftime("%Y-%m-%d")


class TranscriptionList(BaseModel):
    """List of transcription records"""

    items: list[Transcription] = []

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator["Transcription"]:
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def unique_dates_count(self) -> int:
        """Get count of unique dates"""
        return len(set(t.date for t in self.items))
