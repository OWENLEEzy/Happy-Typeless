# src/repositories/json_repository.py
import json
from pathlib import Path

from src.models.errors import Errors, TypelessError
from src.models.transcription import Transcription, TranscriptionList
from src.repositories.base import TranscriptionRepository


class JSONTranscriptionRepository(TranscriptionRepository):
    """JSON file repository"""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._ensure_exists()

    def _ensure_exists(self) -> None:
        """Verify file exists"""
        if not self.filepath.exists():
            raise TypelessError(
                Errors.FILE_NOT_FOUND,
                f"Data file not found: {self.filepath}",
                filepath=str(self.filepath),
            )

    def get_all(self) -> TranscriptionList:
        """Load all transcriptions from JSON file"""
        try:
            with open(self.filepath, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise TypelessError(
                Errors.INVALID_DATA_FORMAT,
                f"Invalid JSON in {self.filepath}: {e.msg} at line {e.lineno}:{e.colno}",
            ) from e

        # Handle different JSON formats
        if isinstance(data, dict):
            data = self._extract_data(data)
        elif not isinstance(data, list):
            raise TypelessError(
                Errors.INVALID_DATA_FORMAT, f"Expected list or dict, got {type(data).__name__}"
            )

        items = [Transcription(**item) for item in data]
        return TranscriptionList(items=items)

    def _extract_data(self, data: dict) -> list:
        """Extract data array from dict wrapper"""
        for key in ["data", "records", "transcriptions", "items", "list"]:
            if key in data:
                return data[key]

        # Single item dict
        if "timestamp" in data and "content" in data:
            return [data]

        raise TypelessError(Errors.INVALID_DATA_FORMAT, "Cannot extract data from JSON dict")
