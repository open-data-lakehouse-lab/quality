import json
from pathlib import Path
from typing import Any

def read_json(path: Path) -> Any:
    """Read a local JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")
