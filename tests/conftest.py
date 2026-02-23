# tests/conftest.py
import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(autouse=True)
def reset_global_settings():
    """Reset global settings singleton between tests to prevent state leakage."""
    from src.config import reset_settings

    yield
    reset_settings()
