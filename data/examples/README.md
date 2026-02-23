# Data Examples

This directory contains example Typeless export files for testing and demonstration.

## Files

### `typeless_export_example.json`
- **Records**: 50 mock voice transcriptions
- **Purpose**: Testing and development
- **Usage**: `uv run python src/main.py -i data/examples/typeless_export_example.json -o output/MyReport.html`

## Generating New Examples

```bash
# Generate 100 mock records
uv run python -c "
from src.factories.repository_factory import RepositoryFactory
import json

repo = RepositoryFactory().create_mock_repository()
repo.generate_mock(count=100)
data = repo.get_all()

with open('data/examples/custom_example.json', 'w', encoding='utf-8') as f:
    json.dump([d.model_dump() for d in data], f, ensure_ascii=False, indent=2)
"
```
